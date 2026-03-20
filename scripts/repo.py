import os
import sys
import argparse
import json
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
    parser_read = subparsers.add_parser("read", help="Read repository structure or content.")
    parser_read.add_argument("data_type", choices=["structure", "content"], help="The type of data to read.")
    parser_read.add_argument("--repo", required=True, dest="repo_name", help="The name of the repository (e.g., 'owner/repo').")
    parser_read.add_argument("--without-cache", action="store_true", help="Force fetch from the server, ignoring any local cache.")

    # --- 'ask' command ---
    parser_ask = subparsers.add_parser("ask", help="Ask a question about a repository.")
    parser_ask.add_argument("--repo", required=True, dest="repo_name", help="The name of the repository (e.g., 'owner/repo').")
    parser_ask.add_argument("--question", required=True, help="The question to ask.")
    
    # --- 'list' command ---
    subparsers.add_parser("list", help="List all available repositories.")

    return parser

def handle_read(args: argparse.Namespace, client: DeepWikiFetcher):
    """Handles the 'read' command, incorporating cache logic."""
    repo_name = args.repo_name
    data_type = args.data_type # "structure" or "content"

    # 1. Check cache (if not disabled)
    if not args.without_cache:
        cached_content = read_from_cache(repo_name, data_type)
        if cached_content is not None:
            print(cached_content)
            return

    # 2. Fetch from server
    fetch_function = client.fetch_structure if data_type == "structure" else client.fetch_contents
    
    try:
        content = fetch_function(repo_name=repo_name)
        if content:
            if isinstance(content, (dict, list)):
                 content_str = json.dumps(content, indent=2, ensure_ascii=False)
            else:
                 content_str = str(content)
            
            # 3. Print and cache the result
            print(content_str)
            write_to_cache(repo_name, data_type, content_str)
        else:
            # Handle cases where the server returns no content
            print(f"No {data_type} content received for repository '{repo_name}'.", file=sys.stderr)

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

def handle_list(client: DeepWikiFetcher):
    """Handles the 'list' command."""
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
        handle_list(client)
    else:
        # This case should not be reached due to `required=True` in subparsers
        print(f"Error: Unknown command '{args.command}'", file=sys.stderr)
        parser.print_help()
        sys.exit(1)

if __name__ == "__main__":
    main()
