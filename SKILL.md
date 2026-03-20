---
name: read-repo
description: Interacts with the DeepWiki service to get information about GitHub repositories. Use this skill to get repository documentation structure, read documentation content, ask questions about a repository, and list available repositories.
---

# Read Repo Skill

This skill allows you to interact with the DeepWiki service, providing a simple interface to access its features.

## Actions

This skill provides the following actions, which are implemented in a Python script:

- **`read_structure`**: Get the documentation structure of a GitHub repository.
- **`read_contents`**: Get the full documentation content of a GitHub repository.
- **`ask_question`**: Ask a question about a GitHub repository.
- **`list_available_repos`**: List all available repositories in DeepWiki.

## Usage

To use this skill, you will call the corresponding function in the `read-repo.py` script.

### `read_structure`

To get the structure of a repository's documentation, use the following command:

```bash
python <path-to-read-repo-skill>/scripts/read-repo.py read_structure --repo-name <owner>/<repo>
```

### `read_contents`

To read the full documentation of a repository, use the following command:

```bash
python <path-to-read-repo-skill>/scripts/read-repo.py read_contents --repo-name <owner>/<repo>
```

### `ask_question`

To ask a question about a repository, use the following command:

```bash
python <path-to-read-repo-skill>/scripts/read-repo.py ask_question --repo-name <owner>/<repo> --question "<your question>"
```

### `list_available_repos`

To list all available repositories, use the following command:

```bash
python <path-to-read-repo-skill>/scripts/read-repo.py list_available_repos
```
