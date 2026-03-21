---
name: read-repo
description: Interacts with the DeepWiki service to get information about GitHub repositories. Use this skill to get repository documentation structure, read documentation content, ask questions about a repository, and list available repositories. This skill includes a caching mechanism to speed up repeated reads.
---

# Read Repo Skill

This skill allows you to interact with the DeepWiki service, providing a simple interface to access its features. It uses a local cache to speed up subsequent requests for the same data.

## Commands

This skill provides the following commands via the `scripts/repo.py` script:

-   **`read`**: Get the documentation structure or full content of a GitHub repository.
-   **`ask`**: Ask a question about a GitHub repository.
-   **`list`**: List all available repositories in DeepWiki.

## Caching

The `read` command has a built-in caching mechanism.

-   When you request a repository's `structure` or `content`, the result is saved locally in the skill's `references/` directory.
-   The next time you request the same data, it will be served directly from the cache, which is much faster.
-   To bypass the cache and fetch fresh data from the server, use the `--without-cache` flag.
-   Each successful fetch from the server will update the cache.

## Usage

To use this skill, you will call the `repo.py` script with one of the available commands.

### `read`

To get the structure or content of a repository's documentation, use the following command:

```bash
# Read from cache if available, otherwise fetch and cache
python <path-to-read-repo-skill>/scripts/repo.py read [structure|content] --repo <owner>/<repo>

# Force a fetch from the server, bypassing the cache
python <path-to-read-repo-skill>/scripts/repo.py read [structure|content] --repo <owner>/<repo> --without-cache
```

**Examples:**

```bash
# Get the structure for 'google/googletest'
python ./.roo/skills/agent-skill-read-repo/scripts/repo.py read structure --repo google/googletest

# Get the content for 'microsoft/vscode'
python ./.roo/skills/agent-skill-read-repo/scripts/repo.py read content --repo microsoft/vscode
```

### `ask`

To ask a question about a repository, use the following command:

```bash
python <path-to-read-repo-skill>/scripts/repo.py ask --repo <owner>/<repo> --question "<your question>"
```

**Example:**

```bash
python ./.roo/skills/agent-skill-read-repo/scripts/repo.py ask --repo google/googletest --question "How do I write a basic test?"
```

### `list`

To list all available repositories, use the following command:

```bash
python <path-to-read-repo-skill>/scripts/repo.py list
```
