# agent-skill-read-repo

A Agent skill that interacts with the DeepWiki service to get information about GitHub repositories.

## Features

- **`read_structure`**: Get the documentation structure of a GitHub repository.
- **`read_contents`**: Get the full documentation content of a GitHub repository.
- **`ask_question`**: Ask a question about a GitHub repository.
- **`list_available_repos`**: List all available repositories in DeepWiki.

## Installation

Copy the contents of this repository into your `.roo/skills/read-repo` directory, or install it globally in your home directory's `.roo/skills` folder.

## Requirements

This skill requires the `requests` Python package.

```bash
pip install requests
```

## Usage

See [SKILL.md](SKILL.md) for detailed usage instructions.
