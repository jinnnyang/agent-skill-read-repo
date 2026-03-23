import os
import sys
import argparse
import json
import datetime
import re
from pathlib import Path
from typing import Optional

# Add the script directory to sys.path to import deepwiki_helper
script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, script_dir)

# Assuming deepwiki_helper.py is in the same directory
from deepwiki_helper import DeepWikiFetcher, MCPError, RequestError

# --- Cache Management ---
# Get the skill's root directory, which is one level above the 'scripts' directory
SKILL_ROOT = Path(script_dir).parent
REFERENCES_DIR = SKILL_ROOT / "references"

def get_cache_path(repo_name: str, data_type: str) -> Path:
    """
    Constructs the path for a cache file.
    e.g., <skill-root>/references/owner/repo/structure.md
    """
    return REFERENCES_DIR / repo_name / f"{data_type}.md"

def read_from_cache(repo_name: str, data_type: str) -> Optional[str]:
    """Reads content from a cache file if it exists."""
    cache_path = get_cache_path(repo_name, data_type)
    if cache_path.is_file():
        try:
            return cache_path.read_text(encoding='utf-8')
        except Exception:
            return None
    return None

def write_to_cache(repo_name: str, data_type: str, content: str):
    """Writes content to a cache file."""
    cache_path = get_cache_path(repo_name, data_type)
    # Ensure the parent directory exists
    cache_path.parent.mkdir(parents=True, exist_ok=True)
    try:
        cache_path.write_text(content, encoding='utf-8')
    except Exception as e:
        # Non-critical error, so we just print it to stderr
        print(f"Warning: Failed to write to cache file {cache_path}. Error: {e}", file=sys.stderr)


def print_table(headers, data):
    """
    Prints a formatted table with aligned columns.
    """
    # Calculate maximum width for each column
    column_widths = [len(header) for header in headers]
    for row in data:
        for i, cell in enumerate(row):
            if len(str(cell)) > column_widths[i]:
                column_widths[i] = len(str(cell))

    # Print header
    header_line = "  ".join(header.ljust(width) for header, width in zip(headers, column_widths))
    print(header_line)

    # Print separator
    separator_line = "  ".join("-" * width for width in column_widths)
    print(separator_line)

    # Print data rows
    for row in data:
        data_line = "  ".join(str(cell).ljust(width) for cell, width in zip(row, column_widths))
        print(data_line)

def list_cached_repos():
    """
    Lists all cached repositories, their authors, and last update time.
    """
    if not REFERENCES_DIR.is_dir():
        print("Cache directory not found.")
        return

    cached_repos_data = []
    repo_list = []
    for author_dir in REFERENCES_DIR.iterdir():
        if author_dir.is_dir():
            for repo_dir in author_dir.iterdir():
                if repo_dir.is_dir():
                    repo_name = repo_dir.name
                    author_name = author_dir.name

                    latest_mtime = 0
                    for file in repo_dir.iterdir():
                        if file.is_file():
                            mtime = file.stat().st_mtime
                            if mtime > latest_mtime:
                                latest_mtime = mtime
                    
                    if latest_mtime > 0:
                        last_update = datetime.datetime.fromtimestamp(latest_mtime).strftime('%Y-%m-%d %H:%M:%S')
                    else:
                        last_update = "N/A"
                    
                    repo_list.append((author_name, repo_name, last_update))

    if not repo_list:
        print("No cached repositories found.")
        return

    repo_list.sort()

    for i, (author, repo, last_update) in enumerate(repo_list, 1):
        cached_repos_data.append([i, author, repo, last_update])

    headers = ["No.", "Author", "Repository", "Last update"]
    print_table(headers, cached_repos_data)


def generate_markdown_outline(content: str):
    """
    Generates and prints a markdown outline from a string.
    """
    heading_pattern = re.compile(r'^(#+)\s+(.*)')
    
    found_headings = False
    print("\\n--- File Outline ---")
    lines = content.splitlines()
    for line_num, line in enumerate(lines, 1):
        match = heading_pattern.match(line)
        if match:
            found_headings = True
            level = len(match.group(1))
            title = match.group(2).strip()
            
            indent = "  " * (level - 1)
            print(f"{indent}- (Line: {line_num}) {title}")
    
    if not found_headings:
        print("No headings found in the content.")


# --- Command-Line Interface ---

def setup_arg_parser() -> argparse.ArgumentParser:
    """Sets up the argument parser for the new CLI structure."""
    parser = argparse.ArgumentParser(description="A script to read repository information from DeepWiki, with caching.")
    parser.add_argument(
        "--server-url",
        default=os.environ.get("MCP_SERVER_URL", "https://mcp.deepwiki.com/mcp"),
        help="The MCP server URL."
    )
    subparsers = parser.add_subparsers(dest="command", required=True, help="The main command to execute.")

    # --- 'read' command ---
    parser_read = subparsers.add_parser("read", help="Read repository structure, content, or outline.")
    parser_read.add_argument("data_type", choices=["structure", "content", "outline"], help="The type of data to read.")
    parser_read.add_argument("--repo", required=True, dest="repo_name", help="The name of the repository (e.g., 'owner/repo').")
    parser_read.add_argument("--without-cache", action="store_true", help="Force fetch from the server, ignoring any local cache.")
    parser_read.add_argument(
        "--range",
        type=str,
        help="For 'content' data_type, specify a line range to read (e.g., '100-250'). Cannot be used with --without-cache."
    )

    # --- 'ask' command ---
    parser_ask = subparsers.add_parser("ask", help="Ask a question about a repository.")
    parser_ask.add_argument("--repo", required=True, dest="repo_name", help="The name of the repository (e.g., 'owner/repo').")
    parser_ask.add_argument("--question", required=True, help="The question to ask.")
    
    # --- 'list' command ---
    parser_list = subparsers.add_parser("list", help="List all available repositories.")
    parser_list.add_argument("--cached", action="store_true", help="List only cached repositories.")

    return parser

def handle_read(args: argparse.Namespace, client: DeepWikiFetcher):
    """Handles the 'read' command, incorporating cache logic."""
    repo_name = args.repo_name
    data_type = args.data_type  # "structure", "content", or "outline"

    # For 'outline', we operate on 'content' data.
    effective_data_type = "content" if data_type == "outline" else data_type

    # Handle --range argument
    if args.range:
        if data_type != "content":
            print("Error: --range can only be used with 'content' data_type.", file=sys.stderr)
            sys.exit(1)
        if args.without_cache:
            print("Error: --range cannot be used with --without-cache. Content must be read from cache.", file=sys.stderr)
            sys.exit(1)
        
        try:
            start_str, end_str = args.range.split('-')
            start_line = int(start_str)
            end_line = int(end_str)
            if start_line <= 0 or end_line < start_line:
                raise ValueError("Line range format is incorrect.")
        except ValueError:
            print("Error: Invalid range format. Please use 'start-end', e.g., '100-250'.", file=sys.stderr)
            sys.exit(1)

        cached_content = read_from_cache(repo_name, effective_data_type)
        if cached_content is None:
            print(f"Error: No cached content found for '{repo_name}'. Cannot use --range without cached data.", file=sys.stderr)
            sys.exit(1)
        
        lines = cached_content.splitlines()
        for i, line in enumerate(lines, 1):
            if i >= start_line:
                if i > end_line:
                    break
                print(line)
        return

    # 1. Check cache (if not disabled)
    if not args.without_cache:
        cached_content = read_from_cache(repo_name, effective_data_type)
        if cached_content is not None:
            if data_type == "outline":
                generate_markdown_outline(cached_content)
            else:
                print(cached_content)
            return

    # 2. Fetch from server
    fetch_function = client.fetch_structure if effective_data_type == "structure" else client.fetch_contents

    try:
        content = fetch_function(repo_name=repo_name)
        if content:
            if isinstance(content, (dict, list)):
                content_str = json.dumps(content, indent=2, ensure_ascii=False)
            else:
                content_str = str(content)

            # 3. Cache the result
            write_to_cache(repo_name, effective_data_type, content_str)

            # 4. Print or process the result
            if data_type == "outline":
                generate_markdown_outline(content_str)
            else:
                print(content_str)
        else:
            # Handle cases where the server returns no content
            print(f"No {effective_data_type} content received for repository '{repo_name}'.", file=sys.stderr)

    except (MCPError, RequestError) as e:
        print(f"An error occurred while fetching data: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}", file=sys.stderr)
        sys.exit(1)


def handle_ask(args: argparse.Namespace, client: DeepWikiFetcher):
    """Handles the 'ask' command."""
    try:
        result = client.ask_question(repo_name=args.repo_name, question=args.question)
        if result:
            if isinstance(result, (dict, list)):
                print(json.dumps(result, indent=2, ensure_ascii=False))
            else:
                print(result)
    except (MCPError, RequestError) as e:
        print(f"An error occurred: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}", file=sys.stderr)
        sys.exit(1)

def handle_list(args: argparse.Namespace, client: DeepWikiFetcher):
    """Handles the 'list' command."""
    if args.cached:
        list_cached_repos()
    else:
        try:
            result = client.list_repos()
            if result:
                if isinstance(result, (dict, list)):
                    print(json.dumps(result, indent=2, ensure_ascii=False))
                else:
                    print(result)
        except (MCPError, RequestError) as e:
            print(f"An error occurred: {e}", file=sys.stderr)
            sys.exit(1)
        except Exception as e:
            print(f"An unexpected error occurred: {e}", file=sys.stderr)
            sys.exit(1)

def main():
    """Main function to parse arguments and dispatch commands."""
    parser = setup_arg_parser()
    args = parser.parse_args()

    client = DeepWikiFetcher(server_url=args.server_url)

    if args.command == "read":
        handle_read(args, client)
    elif args.command == "ask":
        handle_ask(args, client)
    elif args.command == "list":
        handle_list(args, client)
    else:
        # This case should not be reached due to `required=True` in subparsers
        print(f"Error: Unknown command '{args.command}'", file=sys.stderr)
        parser.print_help()
        sys.exit(1)

if __name__ == "__main__":
    main()
