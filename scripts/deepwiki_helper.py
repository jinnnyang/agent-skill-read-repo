#!/usr/bin/env python3
"""
MCP (Model Context Protocol) Client - Using requests library
A library to interact with the DeepWiki MCP.
"""

import os
import sys
import io
import requests
import json
from typing import Any, Dict, List, Optional, TypedDict, Callable

# Force UTF-8 encoding for stdout
if sys.stdout.encoding != 'utf-8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# --- Constants ---
MCP_PROTOCOL_VERSION = "2025-03-26"
JSONRPC_VERSION = "2.0"
DEFAULT_SERVER_URL = "https://mcp.deepwiki.com/mcp"
TOOL_CALL_METHOD = "tools/call"

# --- Custom Exceptions ---
class MCPError(Exception):
    """Represents an error returned by the MCP server."""
    def __init__(self, error_payload: Dict[str, Any]):
        self.code = error_payload.get('code')
        self.message = error_payload.get('message')
        self.data = error_payload.get('data')
        super().__init__(f"MCP Error {self.code}: {self.message}")

class RequestError(Exception):
    """Represents an error during the HTTP request."""
    pass

# --- Type Definitions ---
class JsonResult(TypedDict):
    id: int
    jsonrpc: str
    result: Optional[Dict[str, Any]]
    error: Optional[Dict[str, Any]]


# --- Constants ---
SSE_DATA_PREFIX = "data:"
SSE_DONE_MARKER = "[DONE]"

# --- MCP Client ---
class MCPClient:
    """
    MCP (Modular Agent Protocol) 协议的同步客户端。
    
    该客户端负责与 MCP 服务器进行通信，管理会话，并处理请求和响应。
    它使用 requests.Session 来保持长连接并复用设置。
    """

    def __init__(self, server_url: str):
        """
        初始化 MCP 客户端。

        Args:
            server_url (str): MCP 服务器的 URL 地址。
        """
        self.server_url = server_url
        self.session_id: Optional[str] = None  # 用于跟踪 MCP 会话的 ID
        self.request_id = 1  # 递增的请求 ID
        self._session = requests.Session()  # 使用 Session 对象以复用 TCP 连接
        # 设置所有请求共享的默认请求头
        self._session.headers.update({
            'Content-Type': 'application/json',
            'Accept': 'application/json,text/event-stream',  # 接受 JSON 或 SSE 流
            'Mcp-Protocol-Version': MCP_PROTOCOL_VERSION
        })

    def _make_request(self, method: str, params: Optional[Dict] = None, timeout: int = 60) -> Dict[str, Any]:
        """
        发送一个 MCP 请求并处理其响应。

        该方法构建 JSON-RPC 请求体，以流式方式（SSE）处理响应，
        并从事件流中解析出第一个有效的数据负载。

        Args:
            method (str): 要调用的 MCP 方法名。
            params (Optional[Dict]): 传递给方法的参数。
            timeout (int): 请求超时时间（秒）。

        Returns:
            Dict[str, Any]: 从服务器返回的 `result` 字段内容。

        Raises:
            RequestError: 如果 HTTP 请求失败、SSE 流结束但未收到有效数据，或 JSON 解码失败。
            MCPError: 如果服务器返回一个业务逻辑错误。
        """
        # 构建 JSON-RPC 2.0 请求体
        request_body = {
            "jsonrpc": JSONRPC_VERSION,
            "id": self.request_id,
            "method": method,
            "params": params or {}
        }
        self.request_id += 1

        # 如果已有会话 ID，则将其添加到请求头中
        headers = {}
        if self.session_id:
            headers['Mcp-Session-Id'] = self.session_id

        try:
            # 发送 POST 请求，并启用流式传输
            response = self._session.post(
                self.server_url,
                json=request_body,
                headers=headers,
                timeout=timeout,
                stream=True  # 启用流式响应处理，以支持 SSE
            )
            response.raise_for_status()  # 如果 HTTP 状态码是 4xx 或 5xx，则抛出异常

            # 从响应头中获取并更新会话 ID
            if 'mcp-session-id' in response.headers:
                self.session_id = response.headers['mcp-session-id']

            # 服务器使用 Server-Sent Events (SSE) 协议。我们需要处理这个事件流，
            # 以找到第一个有效的数据负载。
            for line in response.iter_lines():
                # 过滤掉用于保持连接的空行
                if not line:
                    continue

                decoded_line = line.decode('utf-8')
                # SSE 事件行必须以 "data:" 开头
                if not decoded_line.startswith(SSE_DATA_PREFIX):
                    continue

                # 提取数据部分
                data_str = decoded_line[len(SSE_DATA_PREFIX):].strip()
                # 忽略空的数据行或流结束标记 "[DONE]"
                if not data_str or data_str == SSE_DONE_MARKER:
                    continue

                try:
                    # 解析 JSON 数据
                    result: JsonResult = json.loads(data_str)
                    # 检查是否存在业务错误
                    if 'error' in result and result['error']:
                        raise MCPError(result['error'])
                    # 从第一个有效的 data 消息中返回 'result' 字段
                    return result.get('result', {})
                except json.JSONDecodeError as e:
                    # 如果 JSON 解码失败，则抛出自定义异常
                    raise RequestError(f"从 SSE 事件解码 JSON 失败: {data_str}") from e

            # 如果循环正常结束而没有返回任何数据，说明流已关闭但未找到有效负载。
            raise RequestError("SSE 流已结束，但未提供有效的数据负载。")

        except requests.exceptions.RequestException as e:
            # 捕获所有 requests 相关的异常，并包装成我们自己的异常类型
            raise RequestError(f"HTTP 请求失败: {e}") from e

    def call_tool(self, name: str, arguments: Optional[Dict] = None, timeout: int = 60) -> Any:
        """
        调用一个工具并返回其结果。

        这是一个对 `_make_request` 方法的便捷封装，专门用于调用 `tool_code` 方法。

        Args:
            name (str): 要调用的工具名称。
            arguments (Optional[Dict]): 传递给工具的参数。
            timeout (int): 请求超时时间（秒）。

        Returns:
            Any: 工具执行返回的结果。
        """
        params = {
            "name": name,
            "arguments": arguments or {}
        }
        return self._make_request(TOOL_CALL_METHOD, params, timeout=timeout)


# --- DeepWiki Client ---
class DeepWikiFetcher(MCPClient):
    """
    一个用于从 DeepWiki 服务获取数据的客户端。

    该类提供了与 DeepWiki MCP 工具交互的方法，
    简化了获取仓库结构、内容以及提问的流程。
    """

    def _extract_text_from_result(self, result: Any) -> Any:
        """
        安全地从工具调用结果中提取 'text' 内容。
        
        预期的结果格式是一个包含 'content' 列表的字典，
        列表的第一项是一个包含 'text' 键的字典。
        如果结构不匹配，则返回原始结果作为备选。
        """
        if isinstance(result, dict):
            content = result.get('content')
            if isinstance(content, list) and content:
                first_item = content[0]
                if isinstance(first_item, dict):
                    # 如果找到 'text' 则返回它，否则返回原始结果
                    return first_item.get('text', result)
        # 如果数据结构不符合预期，返回原始结果
        return result

    def fetch_structure(self, repo_name: str) -> Any:
        """
        获取指定仓库的文档结构。

        Args:
            repo_name (str): 仓库名称 (例如, "owner/repo")。

        Returns:
            Any: 文档结构，通常是主题列表或 Markdown 文本。
        """
        result = self.call_tool("read_wiki_structure", {"repoName": repo_name})
        return self._extract_text_from_result(result)

    def fetch_contents(self, repo_name: str) -> Any:
        """
        获取指定仓库的完整文档内容。

        Args:
            repo_name (str): 仓库名称 (例如, "owner/repo")。

        Returns:
            Any: 完整的文档内容字符串。
        """
        result = self.call_tool("read_wiki_contents", {"repoName": repo_name})
        return self._extract_text_from_result(result)

    def ask_question(self, repo_name: str, question: str) -> Any:
        """
        向指定仓库提出问题并获取 AI 生成的回答。

        Args:
            repo_name (str): 仓库名称 (例如, "owner/repo")。
            question (str): 要提出的问题。

        Returns:
            Any: 问题的回答。
        """
        result = self.call_tool("ask_question", {
            "repoName": repo_name,
            "question": question
        })
        return self._extract_text_from_result(result)

    def list_repos(self) -> Any:
        """
        列出所有可供查询的仓库。

        Returns:
            Any: 可用仓库名称的列表。
        """
        result = self.call_tool("list_available_repos", {})
        return self._extract_text_from_result(result)
