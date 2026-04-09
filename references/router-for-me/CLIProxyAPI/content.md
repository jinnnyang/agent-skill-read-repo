# Page: Overview

# Overview

<details>
<summary>Relevant source files</summary>

The following files were used as context for generating this wiki page:

- [README.md](README.md)
- [README_CN.md](README_CN.md)
- [README_JA.md](README_JA.md)
- [assets/bmoplus.png](assets/bmoplus.png)
- [assets/lingtrue.png](assets/lingtrue.png)
- [cmd/server/main.go](cmd/server/main.go)
- [config.example.yaml](config.example.yaml)
- [go.mod](go.mod)
- [go.sum](go.sum)
- [internal/api/handlers/management/config_basic.go](internal/api/handlers/management/config_basic.go)
- [internal/api/handlers/management/config_lists.go](internal/api/handlers/management/config_lists.go)
- [internal/api/server.go](internal/api/server.go)
- [internal/config/config.go](internal/config/config.go)
- [internal/store/gitstore.go](internal/store/gitstore.go)
- [internal/store/postgresstore.go](internal/store/postgresstore.go)
- [internal/watcher/watcher.go](internal/watcher/watcher.go)
- [sdk/cliproxy/service.go](sdk/cliproxy/service.go)
- [test/amp_management_test.go](test/amp_management_test.go)

</details>



## Purpose

CLIProxyAPI is a unified proxy gateway for multiple AI provider APIs, exposing OpenAI-compatible endpoints to CLI tools and IDE extensions. It provides multi-account management, OAuth authentication, request translation, dynamic configuration hot-reload, and automatic credential failover.

The system acts as middleware between client applications (Cursor, Claude Code, Cline, Amp CLI) and AI providers (Google Gemini, Anthropic Claude, OpenAI Codex, Qwen, iFlow, Antigravity), abstracting provider-specific authentication and API format differences behind a unified interface.

**Key Features:**
- OpenAI/Gemini/Claude compatible API endpoints for CLI models [README.md:46-48]()
- OpenAI Codex, Claude Code, Qwen, and iFlow support via OAuth login [README.md:47-51]()
- Amp CLI and IDE extensions support with provider routing and model mapping [README.md:75-83]()
- Streaming and non-streaming responses with function calling support [README.md:52-53]()
- Multi-account load balancing (round-robin, fill-first) [README.md:55,97]() [internal/config/config.go:83,97]()
- Hot-reload configuration and authentication files without service restart [internal/watcher/watcher.go:1-3]()
- Reusable Go SDK for embedding the proxy into other applications [README.md:65]() [sdk/cliproxy/service.go:29-32]()

Sources: [README.md:44-93](), [internal/api/server.go:1-5](), [sdk/cliproxy/service.go:1-4](), [internal/config/config.go:27-130]()

## System Architecture Overview

CLIProxyAPI uses a layered architecture separating concerns across HTTP API, authentication, routing, translation, and provider execution layers. The system is designed for extensibility through the `cliproxy.Service` wrapper and hot-reload capability via `watcher.Watcher`.

### Primary Components

| Component | Code Entity | Purpose |
|-----------|------------|---------|
| **Service** | `cliproxy.Service` | Application lifecycle coordinator, integrates all subsystems [sdk/cliproxy/service.go:32]() |
| **API Server** | `api.Server` | Gin HTTP engine, CORS middleware, route registration [internal/api/server.go:122]() |
| **Core Auth Manager** | `coreauth.Manager` | Credential lifecycle, OAuth refresh, and execution conductor [sdk/cliproxy/service.go:85]() |
| **Access Manager** | `sdkaccess.Manager` | Request authentication via API keys or custom providers [sdk/cliproxy/service.go:82]() |
| **Model Registry** | `registry.GlobalRegistry` | Centralized model availability and capability tracking [internal/config/config.go:16]() |
| **Provider Executors** | `executor.*Executor` | Per-provider HTTP request execution implementations [sdk/cliproxy/service.go:17]() |
| **Translators** | `translator.*Translator` | Bidirectional format conversion (OpenAI↔Claude↔Gemini) [cmd/server/main.go:29]() |
| **File Watcher** | `watcher.Watcher` | fsnotify-based config/auth hot-reload with debouncing [internal/watcher/watcher.go:32]() |
| **WebSocket Gateway** | `wsrelay.Manager` | Runtime AI Studio authentication via WebSocket [sdk/cliproxy/service.go:91]() |
| **Management API** | `management.Handler` | Runtime configuration control endpoints [internal/api/server.go:159]() |
| **Config Manager** | `config.Config` | YAML configuration structure with hot-reload support [internal/config/config.go:28]() |

Sources: [internal/api/server.go:120-179](), [sdk/cliproxy/service.go:29-92](), [internal/config/config.go:27-130](), [internal/watcher/watcher.go:32-62]()

## System Architecture Diagram

The following diagram maps high-level system components to their corresponding code entities and directories.

```mermaid
graph TB
    subgraph EntryPoints["Entry Points"]
        CLI["CLI Entry Point<br/>'cmd/server/main.go'<br/>Login flows, TUI, Server mode"]
        WebUI["Web Management UI<br/>Remote connections"]
    end
    
    subgraph APIServerLayer["API Server Layer"]
        Server["'api.Server'<br/>'internal/api/server.go'<br/>Gin Engine, Routes, Middleware"]
        MgmtAPI["'managementHandlers.Handler'<br/>'internal/api/handlers/management'<br/>Auth Files, Config, Models"]
        AmpModule["'ampmodule.AmpModule'<br/>'internal/api/modules/amp'<br/>Fallback routing, Model mapping"]
    end
    
    subgraph RequestProcessing["Request Processing"]
        Translators["Translation Layer<br/>'internal/translator'<br/>OpenAI ↔ Claude ↔ Gemini ↔ Codex"]
        Executors["'executor.ProviderExecutor'<br/>'internal/runtime/executor'<br/>Claude, Codex, Gemini, etc."]
    end
    
    subgraph CoreServices["Core Services"]
        AuthMgr["'coreauth.Manager'<br/>'sdk/cliproxy/auth'<br/>Credential selection, Retry logic"]
        Registry["'registry.GlobalRegistry'<br/>'internal/registry'<br/>Capability metadata"]
        Watcher["'watcher.Watcher'<br/>'internal/watcher/watcher.go'<br/>Hot-reload config & auth"]
    end
    
    subgraph StorageLayer["Storage Layer"]
        ConfigFile["'config.yaml'<br/>Server settings"]
        AuthDir["'auth-dir/'<br/>*.json credentials"]
        TokenStore["'store.TokenStore'<br/>'internal/store'<br/>Postgres/Git/Object/File"]
    end
    
    subgraph ExternalServices["External Services"]
        Providers["AI Providers<br/>OpenAI, Anthropic, Google,<br/>Antigravity, Qwen, etc."]
    end
    
    CLI --> Server
    WebUI --> MgmtAPI
    
    Server --> Translators
    Server --> MgmtAPI
    Server --> AmpModule
    
    Translators --> Executors
    
    Server --> AuthMgr
    AuthMgr --> Registry
    AuthMgr --> Executors
    
    Executors --> Providers
    
    Watcher -.->|monitors| ConfigFile
    Watcher -.->|monitors| AuthDir
    Watcher -.->|triggers reload| Server
    
    Server -.->|persists| ConfigFile
    MgmtAPI -.->|CRUD| AuthDir
    MgmtAPI -.->|OAuth flows| TokenStore
    
    Registry -.->|loads from| ConfigFile
    AuthMgr -.->|loads from| AuthDir
```

Sources: [internal/api/server.go:122-179](), [sdk/cliproxy/service.go:32-92](), [internal/watcher/watcher.go:32-62](), [cmd/server/main.go:56-127]()

## Request Flow Diagram

The following sequence diagram shows the complete request lifecycle from client to AI provider, including authentication, format translation, and retry logic.

```mermaid
sequenceDiagram
    participant Client
    participant APIServer as "api.Server<br/>internal/api/server.go"
    participant Amp as "ampmodule.AmpModule<br/>internal/api/modules/amp"
    participant Translator as "internal/translator"
    participant AuthMgr as "coreauth.Manager<br/>sdk/cliproxy/auth"
    participant Registry as "internal/registry"
    participant Executor as "executor.ProviderExecutor<br/>internal/runtime/executor"
    participant Provider as "AI Provider"
    
    Client->>APIServer: "HTTP Request<br/>(OpenAI/Claude/Gemini format)"
    APIServer->>APIServer: "CORS, Auth, Logging<br/>middleware chain"
    
    alt Amp Client
        APIServer->>Amp: "Check model mapping"
        Amp->>Registry: "Is model locally available?"
        alt Model mapped & available
            Amp->>Amp: "Rewrite model name"
        end
    end
    
    APIServer->>Translator: "TranslateRequest"
    Translator-->>APIServer: "Translated request body"
    
    APIServer->>AuthMgr: "ExecuteRequest"
    AuthMgr->>AuthMgr: "Pick auth via 'RoutingConfig'<br/>(RoundRobin/FillFirst)"
    
    loop Retry attempts
        AuthMgr->>Executor: "Execute"
        Executor->>Provider: "HTTP Request"
        Provider-->>Executor: "Response"
        
        alt Success (2xx)
            Executor-->>AuthMgr: "Response"
        else Retryable (429, 5xx)
            AuthMgr->>AuthMgr: "Cooldown credential"
            AuthMgr->>AuthMgr: "Try next credential"
        end
    end
    
    AuthMgr-->>APIServer: "Final response"
    APIServer->>Translator: "TranslateResponse"
    APIServer-->>Client: "HTTP Response"
```

Sources: [internal/api/server.go:181-191](), [sdk/cliproxy/service.go:174-202](), [internal/config/config.go:71-83]()

---

## Core Capabilities

### Multi-Provider Support

CLIProxyAPI integrates multiple AI providers through a unified interface. Supported providers include:

| Provider | Authentication Methods |
|----------|----------------------|
| **Google Gemini** | API Key, OAuth, Service Account [README.md:56-57]() |
| **Anthropic Claude** | API Key, OAuth [README.md:48,60]() |
| **OpenAI Codex** | OAuth login [README.md:47,63]() |
| **Qwen Code** | OAuth login [README.md:49,61]() |
| **iFlow** | OAuth login, Cookie [README.md:50,62]() |
| **Antigravity** | OAuth login [README.md:126,134]() |
| **OpenAI-Compatible** | API Key via config [README.md:64]() |

Sources: [README.md:46-64](), [internal/runtime/executor/]()

### Hot-Reload System

The hot-reload system enables zero-downtime configuration updates through file system monitoring with `fsnotify`.

**Key Features:**
- **Debouncing**: Rapid file changes are grouped to prevent update storms (`configReloadDebounce = 150ms`) [internal/watcher/watcher.go:84]().
- **Hash Verification**: SHA256 hashes are used to detect actual content changes before triggering reloads [internal/watcher/watcher.go:46,50]().
- **Graceful Updates**: Subsystems like the API server are updated in-place via the `reloadCallback` [internal/watcher/watcher.go:44,90]().

Sources: [internal/watcher/watcher.go:1-160](), [internal/api/server.go:1-5]()

### Authentication Architecture

CLIProxyAPI implements dual-layer authentication:

1.  **Request Authentication** (`sdkaccess.Manager`): Validates incoming client requests using configured API keys [sdk/cliproxy/service.go:21,82]().
2.  **Provider Authentication** (`coreauth.Manager`): Manages the lifecycle of credentials used to talk to upstream AI providers, including OAuth token refresh [sdk/cliproxy/service.go:23,85]().

**Storage Backends:**
Credentials can be stored in various backends by setting environment variables:
- **File**: Default local storage in `auth-dir` [internal/config/config.go:42]().
- **Postgres**: Set `PGSTORE_DSN` [cmd/server/main.go:179-181]().
- **Git**: Set `GITSTORE_GIT_URL` [cmd/server/main.go:199-201]().
- **Object Store**: Set `OBJECTSTORE_ENDPOINT` [cmd/server/main.go:215-217]().

Sources: [sdk/cliproxy/service.go:81-86](), [internal/config/config.go:42](), [cmd/server/main.go:179-220]()

### Management API

The management API (`/v0/management/*`) provides runtime control over the proxy's configuration and credentials.

**Key Endpoints:**
- `GET /v0/management/config`: Retrieve current configuration [internal/api/handlers/management/config_basic.go:26]().
- `PUT /v0/management/config.yaml`: Update configuration via YAML upload [internal/api/handlers/management/config_basic.go:111]().
- `GET /v0/management/api-keys`: List client API keys [internal/api/handlers/management/config_lists.go:108]().
- `PUT /v0/management/api-keys`: Update client API keys [internal/api/handlers/management/config_lists.go:109]().

Sources: [internal/api/handlers/management/config_basic.go:26-163](), [internal/api/handlers/management/config_lists.go:108-119]()

---

# Page: Getting Started

# Getting Started

<details>
<summary>Relevant source files</summary>

The following files were used as context for generating this wiki page:

- [.dockerignore](.dockerignore)
- [.gitignore](.gitignore)
- [README.md](README.md)
- [README_CN.md](README_CN.md)
- [README_JA.md](README_JA.md)
- [assets/bmoplus.png](assets/bmoplus.png)
- [assets/lingtrue.png](assets/lingtrue.png)
- [auths/.gitkeep](auths/.gitkeep)
- [cmd/server/main.go](cmd/server/main.go)
- [docker-build.ps1](docker-build.ps1)
- [docker-build.sh](docker-build.sh)
- [docker-compose.yml](docker-compose.yml)
- [go.mod](go.mod)
- [go.sum](go.sum)
- [internal/store/gitstore.go](internal/store/gitstore.go)
- [internal/store/postgresstore.go](internal/store/postgresstore.go)

</details>



This page guides you through initial setup, basic configuration, and first authentication for the CLI Proxy API. It covers the essential steps to get a working deployment with minimal configuration, bridging the gap between downloading the binary and making your first AI request.

For detailed installation options and deployment scenarios, see [Installation and Deployment](#2.1). For comprehensive configuration reference, see [Initial Configuration](#2.2). For provider-specific authentication guides, see [Authentication Setup](#2.3) and [Provider Integration](#6).

---

## Overview

CLI Proxy API is a unified proxy server that provides OpenAI/Gemini/Claude/Codex compatible API interfaces for CLI tools [README.md:1-9](). It is typically deployed as a single binary that:
1. Loads configuration from `config.yaml` or environment variables [cmd/server/main.go:92-167]().
2. Authenticates with AI providers using OAuth flows or API keys [cmd/server/main.go:80-90]().
3. Exposes standard AI HTTP endpoints for tools like Claude Code or Amp CLI [README.md:46-51]().
4. Translates requests between formats and routes them to configured provider executors [README.md:85-91]().

---

## Deployment Paths

The system supports multiple execution modes, ranging from a simple local server to a cloud-native distributed system using various storage backends for credentials.

### Code Entity Mapping: Storage Selection
The following diagram illustrates how environment variables trigger specific code entities for state persistence.

```mermaid
graph TB
    subgraph "Environment Variables (Natural Language Space)"
        EnvPG["PGSTORE_DSN"]
        EnvGit["GITSTORE_GIT_URL"]
        EnvObj["OBJECTSTORE_ENDPOINT"]
    end

    subgraph "Code Entity Space (internal/store)"
        StoreInt["interface Store"]
        PGStore["[PostgresStore]"]
        GitStore["[GitTokenStore]"]
        ObjStore["[ObjectTokenStore]"]
        FileStore["[FileStore]"]
    end

    EnvPG -->|"Triggers"| PGStore
    EnvGit -->|"Triggers"| GitStore
    EnvObj -->|"Triggers"| ObjStore
    
    PGStore -.->|Implements| StoreInt
    GitStore -.->|Implements| StoreInt
    ObjStore -.->|Implements| StoreInt
    FileStore -.->|Implements| StoreInt

    Default["No Env Vars"] --> FileStore
```
**Sources:** [cmd/server/main.go:179-202](), [internal/store/postgresstore.go:39-46](), [internal/store/gitstore.go:28-38]()

---

## Quick Start: Basic Setup

### 1. Obtain the Binary
Download the latest release or build from source. Developers can use the provided `docker-build.sh` script to build a local container with version metadata [docker-build.sh:138-159]().

### 2. Initial Configuration
Create a `config.yaml` in your working directory. The server uses `DefaultConfigPath` if none is specified via the `--config` flag [cmd/server/main.go:38-43]().
A minimal configuration defines the port and authentication directory:
```yaml
port: 8317
auth_dir: "./auths"
```
**Sources:** [cmd/server/main.go:92](), [.gitignore:6-26]()

### 3. First Authentication
Use CLI flags to initiate OAuth flows for your preferred provider. This generates credential files in your `auth_dir`.

**Common login flags:**
* `--login`: Google Gemini OAuth [cmd/server/main.go:80]()
* `--claude-login`: Anthropic Claude OAuth [cmd/server/main.go:83]()
* `--codex-login`: OpenAI Codex OAuth [cmd/server/main.go:81]()
* `--qwen-login`: Qwen OAuth [cmd/server/main.go:84]()
* `--iflow-login`: iFlow OAuth [cmd/server/main.go:85]()

### 4. Start the Server
Run the binary without login flags to start the proxy service. You can also use the `--tui` flag for an interactive management interface [cmd/server/main.go:75]().
```bash
./cli-proxy-api --tui
```
In Docker environments, the service is managed via `docker-compose.yml` which maps volumes for config, logs, and auth data [docker-compose.yml:24-27]().

---

## Startup and Request Flow

The following diagram bridges the high-level startup sequence to the specific functions and components in the codebase.

```mermaid
sequenceDiagram
    participant CLI as "CLI Flags/Env"
    participant Main as "main() [cmd/server/main.go]"
    participant Registry as "Registry [internal/registry]"
    participant Service as "Service [internal/cmd]"
    participant Store as "Store [internal/store]"

    CLI->>Main: "--config / --tui / --standalone"
    Main->>Main: "logging.SetupBaseLogger()"
    Main->>Main: "godotenv.Load()"
    Main->>Store: "NewPostgresStore / NewGitTokenStore"
    Main->>Registry: "Register Translators/Executors"
    Main->>Service: "cmd.RunServer(cfg)"
    Service-->>CLI: "Listening on :8317"
```
**Sources:** [cmd/server/main.go:46-57](), [cmd/server/main.go:161-212](), [cmd/server/main.go:22-32]()

---

## Storage Backend Configuration

The server automatically detects the persistence layer based on environment variables [cmd/server/main.go:168-177](). For detailed setup of these backends, see [Token Storage Configuration](#2.4).

| Backend | Environment Variable | Role |
| :--- | :--- | :--- |
| **PostgreSQL** | `PGSTORE_DSN` | Persists config and tokens in a database [internal/store/postgresstore.go:39-46]() |
| **Git** | `GITSTORE_GIT_URL` | Syncs state with a remote Git repository [internal/store/gitstore.go:91-101]() |
| **Object Store** | `OBJECTSTORE_ENDPOINT` | Uses S3/MinIO for cloud-native persistence [cmd/server/main.go:147-152]() |
| **File** | *(None)* | Default local filesystem storage in `./auths` [.gitignore:25-26]() |

---

## Management and TUI

For local management, CLIProxyAPI provides two primary interfaces:
1. **Management API**: A set of REST endpoints under `/v0/management` for runtime configuration and usage export/import [README.md:71-73](), [docker-build.sh:62-63]().
2. **Terminal UI (TUI)**: Accessible via the `--tui` flag, providing an interactive console for managing providers and logs [cmd/server/main.go:75]().

For details on managing the server via these interfaces, see [Initial Configuration](#2.2).

---

## Next Steps

*   **[Installation and Deployment](#2.1)**: Learn how to deploy via Docker or as a system service.
*   **[Initial Configuration](#2.2)**: Deep dive into the `config.yaml` schema and advanced settings.
*   **[Authentication Setup](#2.3)**: Step-by-step guides for OAuth and API key configuration for all providers.
*   **[Token Storage Configuration](#2.4)**: Configure shared storage for multi-instance deployments.

**Sources:** [README.md:67-73](), [cmd/server/main.go:56-127](), [docker-compose.yml:1-29]()

---

# Page: Installation and Deployment

# Installation and Deployment

<details>
<summary>Relevant source files</summary>

The following files were used as context for generating this wiki page:

- [.dockerignore](.dockerignore)
- [.github/workflows/docker-image.yml](.github/workflows/docker-image.yml)
- [.github/workflows/pr-test-build.yml](.github/workflows/pr-test-build.yml)
- [.github/workflows/release.yaml](.github/workflows/release.yaml)
- [.gitignore](.gitignore)
- [.goreleaser.yml](.goreleaser.yml)
- [Dockerfile](Dockerfile)
- [LICENSE](LICENSE)
- [auths/.gitkeep](auths/.gitkeep)
- [cmd/server/main.go](cmd/server/main.go)
- [docker-build.ps1](docker-build.ps1)
- [docker-build.sh](docker-build.sh)
- [docker-compose.yml](docker-compose.yml)
- [go.mod](go.mod)
- [go.sum](go.sum)
- [internal/store/gitstore.go](internal/store/gitstore.go)
- [internal/store/postgresstore.go](internal/store/postgresstore.go)

</details>



This page covers the installation of CLIProxyAPI binaries, deployment methods, and the various execution modes available (server, TUI, standalone, and cloud deploy). CLIProxyAPI is designed to be highly portable, supporting direct binary execution, Docker containers, and multi-backend storage for cloud-native environments.

## Installation Methods

### Binary Downloads
CLIProxyAPI provides pre-built binaries for multiple platforms (Linux, Windows, Darwin, FreeBSD) and architectures (amd64, arm64). Binaries are built using GoReleaser [[.goreleaser.yml:3-17]()] and include embedded version metadata [[cmd/server/main.go:48-51]()].

- **Main repository**: [https://github.com/router-for-me/CLIProxyAPI](https://github.com/router-for-me/CLIProxyAPI)
- **Automated Builds**: GitHub Actions handle tag-based releases [[.github/workflows/release.yaml:1-43]()] and Docker image pushes [[.github/workflows/docker-image.yml:1-112]()].

### Building from Source
To build from source, ensure Go 1.26+ is installed [[go.mod:3]()]:

```bash
git clone https://github.com/router-for-me/CLIProxyAPI.git
cd CLIProxyAPI
# The entry point is in cmd/server
go build -o cliproxyapi ./cmd/server/
```
The build process automatically refreshes the model catalog from a remote repository during CI/CD [[.github/workflows/pr-test-build.yml:15-18]()].

### Docker Deployment
The project provides a `Dockerfile` based on `alpine:3.22.0` [[Dockerfile:17-35]()] and a `docker-compose.yml` for simplified orchestration [[docker-compose.yml:1-29]()].

**Key Docker Ports:**
- `8317`: Default API port [[Dockerfile:29]()].
- `8085`, `1455`, `54545`, `51121`, `11451`: Ports mapped for various OAuth callback listeners [[docker-compose.yml:19-23]()].

**Sources:** [[cmd/server/main.go:38-51]()], [[Dockerfile:1-35]()], [[.goreleaser.yml:3-17]()], [[docker-compose.yml:1-29]()]

---

## Execution Modes

CLIProxyAPI logic branches into different modes based on command-line flags parsed in `main()` [[cmd/server/main.go:56-127]()].

### Execution Mode Architecture

```mermaid
graph TB
    subgraph "Entry: cmd/server/main.go"
        Main["main()"]
        Flags["flag.Parse()"]
    end

    subgraph "Mode Selection Logic"
        Main --> Flags
        Flags --> IsLogin{"Login Flag?"}
        Flags --> IsTUI{"-tui Flag?"}
        Flags --> IsCloud{"DEPLOY=cloud?"}
    end

    subgraph "Execution Paths"
        IsLogin -- "Yes" --> DoLogin["cmd.DoLogin() / cmd.DoCodexLogin()"]
        IsTUI -- "No" --> ServerMode["cmd.StartService()"]
        IsTUI -- "Yes" --> TUIBranch{"-standalone?"}
        
        TUIBranch -- "No" --> TUIClient["tui.Run() (Connect to Remote)"]
        TUIBranch -- "Yes" --> TUIStandalone["cmd.StartServiceBackground() + tui.Run()"]
        
        IsCloud -- "Config Missing" --> CloudWait["cmd.WaitForCloudDeploy()"]
    end

    subgraph "Code Entities"
        DoLogin -.-> L1["internal/cmd/login.go"]
        ServerMode -.-> S1["internal/cmd/run.go"]
        TUIStandalone -.-> T1["internal/tui/tui.go"]
        CloudWait -.-> W1["internal/cmd/run.go"]
    end
```
**Sources:** [[cmd/server/main.go:56-127]()], [[cmd/server/main.go:461-575]()]

### 1. Server Mode (Default)
The standard mode for hosting the proxy. It loads configuration and starts the Gin-based HTTP server.
- **Startup**: `main()` calls `cmd.StartService(cfg, configPath, localPassword)` [[cmd/server/main.go:569-573]()].
- **Implementation**: Uses a service builder to assemble the proxy components [[cmd/server/main.go:446-454]()].

### 2. TUI Client Mode
A terminal interface to manage a *remote* or already running CLIProxyAPI instance using the `charmbracelet/bubbletea` framework [[go.mod:9]()].
- **Flag**: `-tui` [[cmd/server/main.go:95]()].
- **Implementation**: Calls `tui.Run()` with the target port and management password [[cmd/server/main.go:562-567]()].

### 3. TUI Standalone Mode
Combines the API server and the TUI in a single process.
- **Flags**: `-tui -standalone` [[cmd/server/main.go:95-96]()].
- **Behavior**: Starts the service in a background goroutine via `cmd.StartServiceBackground()` [[cmd/server/main.go:531-536]()] and attaches the TUI to it.

### 4. Cloud Deploy Mode
Designed for environments like Kubernetes where the configuration might be injected after the container starts.
- **Activation**: Environment variable `DEPLOY=cloud` [[cmd/server/main.go:132, 228-232]()].
- **Behavior**: If `config.yaml` is missing, the process enters a standby state via `cmd.WaitForCloudDeploy()` [[cmd/server/main.go:398-417]()] instead of exiting.

### 5. Login Modes
One-time execution paths to perform OAuth authentication for specific providers.
- **Flags**: `-login` (Gemini), `-codex-login` (OpenAI), `-claude-login` (Anthropic), etc. [[cmd/server/main.go:80-90]()].
- **Behavior**: Executes the provider-specific login flow and saves credentials to the active `TokenStore` [[cmd/server/main.go:461-487]()].

**Sources:** [[cmd/server/main.go:75-98]()], [[cmd/server/main.go:495-560]()]

---

## Storage Backend Selection

CLIProxyAPI determines its `TokenStore` implementation based on environment variables. This selection happens early in `main()` [[cmd/server/main.go:179-225]()].

| Backend Type | Environment Variable Trigger | Implementation Class |
|--------------|------------------------------|----------------------|
| **PostgreSQL** | `PGSTORE_DSN` | `store.PostgresStore` [[internal/store/postgresstore.go:39]()] |
| **Object Store** | `OBJECTSTORE_ENDPOINT` | `store.ObjectTokenStore` [[cmd/server/main.go:276-281]()] |
| **Git** | `GITSTORE_GIT_URL` | `store.GitTokenStore` [[cmd/server/main.go:332-337]()] |
| **File (Local)** | (Default) | `sdkAuth.FileTokenStore` [[cmd/server/main.go:453]()]. |

### Storage Initialization Flow

```mermaid
graph LR
    subgraph "Environment Check"
        DSN{"PGSTORE_DSN?"}
        S3{"OBJECTSTORE_ENDPOINT?"}
        GIT{"GITSTORE_GIT_URL?"}
    end

    subgraph "Code Entity Space"
        PG_S["store.PostgresStore"]
        OBJ_S["store.ObjectTokenStore"]
        GIT_S["store.GitTokenStore"]
        FILE_S["sdkAuth.FileTokenStore"]
    end

    DSN -- "Yes" --> PG_S
    DSN -- "No" --> S3
    S3 -- "Yes" --> OBJ_S
    S3 -- "No" --> GIT
    GIT -- "Yes" --> GIT_S
    GIT -- "No" --> FILE_S

    PG_S --> Reg["sdkAuth.RegisterTokenStore()"]
    OBJ_S --> Reg
    GIT_S --> Reg
    FILE_S --> Reg
```
**Sources:** [[cmd/server/main.go:179-225]()], [[cmd/server/main.go:446-454]()]

---

## Command-Line Flag Reference

| Flag | Type | Description |
|------|------|-------------|
| `-config` | string | Path to the YAML configuration file [[cmd/server/main.go:92]()]. |
| `-login` | bool | Launch Google Gemini OAuth flow [[cmd/server/main.go:80]()]. |
| `-codex-login` | bool | Launch OpenAI Codex OAuth flow [[cmd/server/main.go:81]()]. |
| `-claude-login` | bool | Launch Anthropic Claude OAuth flow [[cmd/server/main.go:83]()]. |
| `-qwen-login` | bool | Launch Qwen OAuth flow [[cmd/server/main.go:84]()]. |
| `-iflow-login` | bool | Launch iFlow OAuth flow [[cmd/server/main.go:85]()]. |
| `-no-browser` | bool | Prevent the CLI from opening the system browser for OAuth [[cmd/server/main.go:87]()]. |
| `-tui` | bool | Start the Terminal UI management interface [[cmd/server/main.go:95]()]. |
| `-standalone` | bool | Start an embedded server when running in TUI mode [[cmd/server/main.go:96]()]. |
| `-local-model` | bool | Skip fetching the remote model catalog; use embedded JSON only [[cmd/server/main.go:97]()]. |

**Sources:** [[cmd/server/main.go:79-98]()]

---

## Deployment Lifecycle

### Initialization Sequence
1. **Environment Setup**: Load `.env` file and initialize the base logger [[cmd/server/main.go:47, 162-166]()].
2. **Store Selection**: Determine if `Postgres`, `Git`, or `ObjectStore` is used for credentials [[cmd/server/main.go:179-225]()].
3. **Configuration Loading**: Load `config.yaml`. If in `cloud` mode and the file is missing, wait for the Management API to provide it [[cmd/server/main.go:398-417]()].
4. **Postgres Bootstrap**: If using `PostgresStore`, it synchronizes records between the database and local spool directory [[internal/store/postgresstore.go:147-158]()].
5. **Service Building**: Assemble the service components using the builder pattern [[cmd/server/main.go:446-454]()].

### Graceful Shutdown
The application listens for termination signals. When a signal is received, it triggers a context cancellation to allow components like the HTTP server and background refreshers to shut down cleanly [[cmd/server/main.go:446-575]()].

**Sources:** [[cmd/server/main.go:47-575]()], [[internal/store/postgresstore.go:147-158]()]

---

# Page: Initial Configuration

# Initial Configuration

<details>
<summary>Relevant source files</summary>

The following files were used as context for generating this wiki page:

- [config.example.yaml](config.example.yaml)
- [internal/api/handlers/management/config_basic.go](internal/api/handlers/management/config_basic.go)
- [internal/api/handlers/management/config_lists.go](internal/api/handlers/management/config_lists.go)
- [internal/api/server.go](internal/api/server.go)
- [internal/cmd/login.go](internal/cmd/login.go)
- [internal/cmd/run.go](internal/cmd/run.go)
- [internal/config/config.go](internal/config/config.go)
- [internal/watcher/watcher.go](internal/watcher/watcher.go)
- [sdk/cliproxy/service.go](sdk/cliproxy/service.go)
- [test/amp_management_test.go](test/amp_management_test.go)

</details>



This page walks through the minimum settings required in `config.yaml` to get CLIProxyAPI accepting requests. It covers the configuration file location, server binding, the auth token directory, client access control, and connecting at least one AI provider.

For a complete reference of every field, see [Configuration File Structure](#5.1). For deployment-specific setup (Docker Compose, volumes), see [Installation and Deployment](#2.1). For adding OAuth credentials after the server is running, see [Authentication Setup](#2.3).

---

## How the Configuration File Is Located

At startup, the server resolves the configuration file path in this order:

1. The path given by the `--config` command-line flag.
2. `config.yaml` in the current working directory (default).
3. A path managed by an external storage backend (PostgreSQL, Git, or object storage — see [Storage Backend Options](#5.2)).

The file is parsed by `config.LoadConfigOptional` in [internal/config/config.go:515-652](), which populates a `config.Config` struct. That struct is passed to `api.NewServer` [internal/api/server.go:181-220]() to build the HTTP server, and to `watcher.NewWatcher` [internal/watcher/watcher.go:90-117]() for hot-reload support.

**Config Loading Pipeline**

```mermaid
flowchart LR
    flag["--config flag"] --> resolve["path resolution in cmd/server/main.go"]
    cwd["./config.yaml (cwd)"] --> resolve
    backend["external store (Postgres/Git/Object)"] --> resolve
    resolve --> LoadConfigOptional["config.LoadConfigOptional()"]
    LoadConfigOptional --> Config["config.Config struct"]
    Config --> NewServer["api.NewServer()"]
    Config --> NewWatcher["watcher.NewWatcher()"]
    NewServer --> APIServer["api.Server"]
    NewWatcher --> UpdateClients["Server.UpdateClients() on change"]
```

Sources: [internal/config/config.go:515-652](), [internal/api/server.go:181-220](), [internal/watcher/watcher.go:90-117](), [sdk/cliproxy/service.go:32-92]()

---

## YAML Keys Mapped to `config.Config`

The file is parsed into `config.Config` (defined at [internal/config/config.go:27-130]()). `SDKConfig` is inlined into `Config` and provides the `api-keys` and `proxy-url` fields.

**YAML keys to Go struct fields**

```mermaid
flowchart LR
    subgraph yaml_side["config.yaml YAML keys"]
        y_port["port"]
        y_host["host"]
        y_authdir["auth-dir"]
        y_apikeys["api-keys"]
        y_gemini["gemini-api-key"]
        y_claude["claude-api-key"]
        y_codex["codex-api-key"]
        y_openai["openai-compatibility"]
        y_vertex["vertex-api-key"]
        y_mgmt["remote-management"]
    end
    subgraph go_side["config.Config Go fields"]
        g_port["Config.Port int"]
        g_host["Config.Host string"]
        g_authdir["Config.AuthDir string"]
        g_apikeys["SDKConfig.APIKeys string-slice"]
        g_gemini["Config.GeminiKey GeminiKey-slice"]
        g_claude["Config.ClaudeKey ClaudeKey-slice"]
        g_codex["Config.CodexKey CodexKey-slice"]
        g_openai["Config.OpenAICompatibility slice"]
        g_vertex["Config.VertexCompatAPIKey slice"]
        g_mgmt["Config.RemoteManagement struct"]
    end
    y_port --> g_port
    y_host --> g_host
    y_authdir --> g_authdir
    y_apikeys --> g_apikeys
    y_gemini --> g_gemini
    y_claude --> g_claude
    y_codex --> g_codex
    y_openai --> g_openai
    y_vertex --> g_vertex
    y_mgmt --> g_mgmt
```

Sources: [internal/config/config.go:27-130](), [config.example.yaml:1-112]()

---

## Minimum Required Fields

| YAML key | Go field | Required | Default | Notes |
|---|---|---|---|---|
| `port` | `Config.Port` | **Yes** | none | e.g. `8317` |
| `auth-dir` | `Config.AuthDir` | **Yes** | none | Supports `~` expansion |
| (one provider key) | various | **Yes** | none | See provider sections below |
| `api-keys` | `SDKConfig.APIKeys` | No | none | Recommended; absent = all requests accepted |
| `host` | `Config.Host` | No | `""` | Empty = bind all interfaces |

Sources: [internal/config/config.go:32-43](), [config.example.yaml:3-38]()

---

## Server Binding

```yaml
# Bind all interfaces (default):
host: ""

# Restrict to localhost only:
host: "127.0.0.1"

port: 8317
```

`Config.Host` and `Config.Port` form the network address passed to the underlying HTTP server. An empty `host` binds to all interfaces (IPv4 and IPv6) [internal/config/config.go:32-34]().

### TLS (optional)

```yaml
tls:
  enable: true
  cert: "/path/to/cert.pem"
  key: "/path/to/key.pem"
```

When `tls.enable` is `true`, the server uses the provided certificate and key for HTTPS. The `TLSConfig` struct is defined at [internal/config/config.go:142-150]().

Sources: [internal/config/config.go:32-37](), [internal/config/config.go:142-150](), [config.example.yaml:3-12]()

---

## Auth Directory

```yaml
auth-dir: "~/.cli-proxy-api"
```

`Config.AuthDir` specifies where OAuth token JSON files are stored and watched [internal/config/config.go:43](). At startup, the service:

1. Creates the directory if it does not exist.
2. Watches for new, changed, or removed JSON files via `watcher.Watcher` [internal/watcher/watcher.go:31-62]().
3. Registers discovered credentials with the core auth manager.

The `~` prefix is expanded to the user home directory during path resolution.

> OAuth-based providers (Gemini CLI, Claude, Codex, Antigravity, Qwen, iFlow, Kimi) store their credentials here. These are created by running login commands (e.g., `DoLogin` in [internal/cmd/login.go:49-207]()) or via the Management API.

Sources: [internal/config/config.go:43](), [internal/watcher/watcher.go:31-62](), [internal/cmd/login.go:49-207](), [config.example.yaml:35-36]()

---

## Client Access Control

```yaml
api-keys:
  - "your-proxy-key-1"
  - "your-proxy-key-2"
```

When this list is non-empty, every request to the proxy endpoints must present a matching value as a Bearer token in the `Authorization` header. This is managed by the `access.Manager` [internal/api/server.go:139-141]().

When `api-keys` is empty or omitted, the server allows all requests without authentication. This is only recommended for isolated local development.

Sources: [config.example.yaml:38-42](), [internal/api/server.go:139-141](), [internal/config/config.go:28-29]()

---

## Connecting a Provider

At least one AI provider must be configured. Providers fall into two categories:

- **API key providers** — configured directly in `config.yaml`.
- **OAuth providers** — credentials are created by running a login flow; files are stored in `auth-dir`.

**Provider types and their config.Config fields**

```mermaid
flowchart TD
    Config["config.Config"] --> APIKeyGroup["API Key Providers"]
    Config --> OAuthGroup["OAuth Providers (stored in auth-dir)"]

    APIKeyGroup --> GeminiKey["Config.GeminiKey\nYAML: gemini-api-key"]
    APIKeyGroup --> ClaudeKey["Config.ClaudeKey\nYAML: claude-api-key"]
    APIKeyGroup --> CodexKey["Config.CodexKey\nYAML: codex-api-key"]
    APIKeyGroup --> OpenAICompat["Config.OpenAICompatibility\nYAML: openai-compatibility"]
    APIKeyGroup --> VertexCompat["Config.VertexCompatAPIKey\nYAML: vertex-api-key"]

    OAuthGroup --> GeminiCLI["provider: gemini-cli\ninternal/cmd/login.go"]
    OAuthGroup --> ClaudeOAuth["provider: claude\nsdk/auth/ClaudeAuthenticator"]
    OAuthGroup --> Others["provider: codex / antigravity\nqwen / iflow / kimi"]
```

Sources: [internal/config/config.go:87-110](), [internal/cmd/login.go:49-207](), [config.example.yaml:110-199]()

### Gemini API Key

```yaml
gemini-api-key:
  - api-key: "AIzaSy..."
```

Minimal form. The server uses all default Gemini models for this key. Optional per-entry fields include `base-url`, `proxy-url`, `prefix`, and `models` [internal/config/config.go:406-448]().

Sources: [internal/config/config.go:406-448](), [config.example.yaml:110-127]()

### Claude API Key

```yaml
claude-api-key:
  - api-key: "sk-ant-..."
```

No `base-url` is needed for the official Anthropic API. Set `base-url` only when routing to a compatible third-party endpoint. The `ClaudeKey` struct is defined at [internal/config/config.go:310-341]().

Sources: [internal/config/config.go:310-341](), [config.example.yaml:147-166]()

### Codex API Key

```yaml
codex-api-key:
  - api-key: "sk-..."
    base-url: "https://api.example.com"
```

`base-url` is typically required for Codex keys if not using a default. See [internal/config/config.go:358-389]() for the `CodexKey` struct.

Sources: [internal/config/config.go:358-389](), [config.example.yaml:129-145]()

### OpenAI-Compatible Provider

```yaml
openai-compatibility:
  - name: "openrouter"
    base-url: "https://openrouter.ai/api/v1"
    api-key-entries:
      - api-key: "sk-or-v1-..."
    models:
      - name: "moonshotai/kimi-k2:free"
        alias: "kimi-k2"
```

`name` and `base-url` are both required for OpenAI-compatible providers. The `OpenAICompatibility` struct is defined at [internal/config/config.go:450-493]().

Sources: [internal/config/config.go:450-493](), [config.example.yaml:172-185]()

### Vertex-Compatible API Key

```yaml
vertex-api-key:
  - api-key: "vk-123..."
    base-url: "https://example.com/api"
    models:
      - name: "gemini-2.5-pro"
        alias: "vertex-pro"
```

Used for services that expose a Vertex AI-style API path with simple API key authentication [internal/config/config.go:108-110]().

Sources: [internal/config/config.go:108-110](), [config.example.yaml:187-199]()

---

## Management API (Optional)

The Management API (`/v0/management/*`) is controlled by the `remote-management` section [internal/config/config.go:151-171]().

```yaml
remote-management:
  allow-remote: false       # false = localhost access only
  secret-key: "plaintext"   # hashed to bcrypt on first startup
  disable-control-panel: false
```

When `secret-key` is provided as plaintext, the server bcrypt-hashes it and writes the hash back to `config.yaml` during initialization [internal/config/config.go:582-592]().

Sources: [internal/config/config.go:151-171](), [internal/config/config.go:582-592](), [config.example.yaml:14-33]()

---

## Minimal Working Examples

**Absolute minimum** (no client auth, single Gemini key):

```yaml
port: 8317
auth-dir: "~/.cli-proxy-api"

gemini-api-key:
  - api-key: "AIzaSy..."
```

**Recommended minimum** (client auth, management API enabled):

```yaml
host: "127.0.0.1"
port: 8317
auth-dir: "~/.cli-proxy-api"

api-keys:
  - "your-proxy-access-key"

remote-management:
  secret-key: "your-management-secret"
  allow-remote: false

gemini-api-key:
  - api-key: "AIzaSy..."
```

Sources: [config.example.yaml:1-50](), [internal/config/config.go:515-652]()

---

## Hot Reload

After startup, changes to `config.yaml` are detected by `watcher.Watcher` (using `fsnotify`) [internal/watcher/watcher.go:31-62](). The watcher triggers a reload callback that updates the running server's configuration and client pool [internal/watcher/watcher.go:134-139](). Changes to files inside `auth-dir` are similarly watched and applied incrementally via the `authUpdates` channel [sdk/cliproxy/service.go:114-127]().

Sources: [internal/watcher/watcher.go:31-62](), [internal/watcher/watcher.go:134-139](), [internal/api/server.go:4-5](), [sdk/cliproxy/service.go:114-127]()

---

# Page: Authentication Setup

# Authentication Setup

<details>
<summary>Relevant source files</summary>

The following files were used as context for generating this wiki page:

- [internal/api/handlers/management/auth_files.go](internal/api/handlers/management/auth_files.go)
- [internal/auth/antigravity/auth.go](internal/auth/antigravity/auth.go)
- [internal/auth/codex/filename.go](internal/auth/codex/filename.go)
- [internal/auth/gemini/gemini_auth.go](internal/auth/gemini/gemini_auth.go)
- [internal/cmd/anthropic_login.go](internal/cmd/anthropic_login.go)
- [internal/cmd/iflow_login.go](internal/cmd/iflow_login.go)
- [internal/cmd/openai_login.go](internal/cmd/openai_login.go)
- [internal/cmd/qwen_login.go](internal/cmd/qwen_login.go)
- [internal/misc/oauth.go](internal/misc/oauth.go)
- [sdk/auth/antigravity.go](sdk/auth/antigravity.go)
- [sdk/auth/claude.go](sdk/auth/claude.go)
- [sdk/auth/codex.go](sdk/auth/codex.go)
- [sdk/auth/iflow.go](sdk/auth/iflow.go)

</details>



This page guides you through setting up your first provider authentication after completing the initial server installation and configuration. You will learn how to authenticate with AI service providers using OAuth flows or API keys, save credentials, and verify that models are accessible.

---

## Overview

CLIProxyAPI supports three primary authentication methods:

| Method | Use Case | Providers |
|--------|----------|-----------|
| **OAuth 2.0** | Browser-based authorization for personal accounts | Gemini CLI, Claude Code, Codex, Qwen, iFlow, Antigravity |
| **API Keys** | Direct API access with existing keys | Gemini (AI Studio), Claude (API), OpenAI-compatible upstreams |
| **Service Accounts** | Google Cloud service account JSON files | Vertex AI |

After authentication, credentials are persisted to the configured storage backend (file system by default) and registered with the Auth Manager for immediate use.

Sources: [internal/api/handlers/management/auth_files.go:25-31](), [internal/api/handlers/management/auth_files.go:245-255]()

---

## Authentication Methods

### CLI Commands

The server binary provides dedicated handlers for OAuth authentication with each provider. These are typically triggered via CLI flags which invoke specific logic in the `cmd` package:

```bash
# Google Gemini CLI OAuth
./cliproxyapi --login [--project_id PROJECT_ID]

# Claude Code OAuth  
./cliproxyapi --claude-login

# OpenAI Codex OAuth
./cliproxyapi --codex-login

# Qwen Code OAuth
./cliproxyapi --qwen-login

# iFlow OAuth
./cliproxyapi --iflow-login
```

Each command launches a provider-specific OAuth flow and saves the resulting credentials to the `AuthDir` configured in `config.yaml`.

**Key CLI Handlers:**
- `DoClaudeLogin`: Initiates the Claude OAuth flow using the shared authentication manager [internal/cmd/anthropic_login.go:22-59]().
- `DoCodexLogin`: Initiates the OpenAI Codex OAuth flow [internal/cmd/openai_login.go:29-72]().
- `DoQwenLogin`: Initiates the Qwen device flow [internal/cmd/qwen_login.go:20-60]().
- `DoIFlowLogin`: Initiates the iFlow OAuth login [internal/cmd/iflow_login.go:14-48]().

Sources: [internal/cmd/anthropic_login.go:41-41](), [internal/cmd/openai_login.go:55-55](), [internal/cmd/qwen_login.go:45-45](), [internal/cmd/iflow_login.go:33-48]()

### Management API

For web-based integrations or remote administration, the Management API exposes endpoints to list and manage these files:

| Endpoint | Action | Method |
|----------|----------|--------|
| `/v0/management/auth/files` | List registered credentials | GET |
| `/v0/management/auth/models` | List models for a specific file | GET |

The `ListAuthFiles` handler retrieves credentials from the `authManager` and builds structured entries for the response [internal/api/handlers/management/auth_files.go:240-259]().

Sources: [internal/api/handlers/management/auth_files.go:240-259]()

---

## Authentication Flow Architecture

The following diagram illustrates the data flow from initiation to credential registration.

```mermaid
graph TB
    subgraph "Authentication Initiation"
        CLIFlag["CLI Handler<br/>(DoClaudeLogin, DoCodexLogin)"]
        MgmtAPI["Management Handler<br/>(ListAuthFiles)"]
    end
    
    subgraph "OAuth Flow Execution"
        AuthSvc["Authenticator SDK<br/>(ClaudeAuthenticator, CodexAuthenticator)"]
        Browser["Browser Authorization"]
        CallbackServer["callbackForwarder<br/>(internal/api/handlers/management/auth_files.go)"]
    end
    
    subgraph "Token Exchange"
        CodeExchange["ExchangeCodeForTokens"]
        TokenResponse["Token Data<br/>(TokenResponse, OAuthResult)"]
    end
    
    subgraph "Credential Persistence"
        AuthManager["AuthManager.Login"]
        AuthFile["Auth JSON File<br/>(AuthDir/*.json)"]
    end
    
    subgraph "Registration"
        Synthesizer["FileSynthesizer"]
        CoreManager["CoreManager"]
    end
    
    CLIFlag --> AuthSvc
    MgmtAPI --> AuthSvc
    
    AuthSvc --> Browser
    Browser --> CallbackServer
    
    CallbackServer --> CodeExchange
    CodeExchange --> TokenResponse
    
    TokenResponse --> AuthManager
    AuthManager --> AuthFile
    
    AuthFile --> Synthesizer
    Synthesizer --> CoreManager
```

Sources: [internal/api/handlers/management/auth_files.go:54-62](), [sdk/auth/claude.go:38-220](), [sdk/auth/codex.go:38-198](), [sdk/auth/antigravity.go:35-220]()

---

## Setting Up Your First Authentication

### Step 1: Choose a Provider

Select a provider based on your existing subscriptions. Common providers use specific ports for local callbacks:
- **Claude**: Port `54545` [internal/api/handlers/management/auth_files.go:47-47]()
- **Gemini**: Port `8085` [internal/api/handlers/management/auth_files.go:48-48]()
- **Codex**: Port `1455` [internal/api/handlers/management/auth_files.go:49-49]()
- **Antigravity**: Default port defined in provider package [sdk/auth/antigravity.go:46-46]()

### Step 2: Run Authentication Command

**Example: Claude Code OAuth**
The `ClaudeAuthenticator` implementation handles PKCE code generation and state validation [sdk/auth/claude.go:54-62](). It starts a local `oauthServer` to listen for the callback [sdk/auth/claude.go:64-70](). Once the browser redirect is received, it exchanges the code for tokens via `ExchangeCodeForTokens` [sdk/auth/claude.go:191-195]().

**Example: Antigravity OAuth**
The `AntigravityAuthenticator` fetches user information (email) and attempts to resolve a GCP Project ID automatically via `loadCodeAssist` [sdk/auth/antigravity.go:166-185](). This allows the proxy to route requests to the correct project without manual configuration.

**Example: iFlow OAuth**
The `IFlowAuthenticator` uses a standard OAuth code flow, storing the resulting `APIKey` and `AccessToken` in the metadata for the generated credential file [sdk/auth/iflow.go:163-182]().

### Step 3: Verify Credential File

Check that the credential file was created in your `AuthDir`. Files are typically named using the provider and user email, such as `claude-user@example.com.json` [sdk/auth/claude.go:203-203]() or `antigravity-user@example.com.json` [sdk/auth/antigravity.go:203-203]().

Example metadata structure for iFlow:
```json
{
  "email": "user@example.com",
  "api_key": "...",
  "access_token": "...",
  "refresh_token": "...",
  "expired": "..."
}
```
Sources: [sdk/auth/iflow.go:176-182](), [internal/auth/codex/filename.go:12-27]()

---

## Code Entity Mapping

The following diagram bridges the natural language concepts to the specific code entities responsible for the authentication lifecycle.

```mermaid
graph LR
    subgraph "Provider SDK (sdk/auth/*)"
        ClaudeAuth["ClaudeAuthenticator<br/>claude.go"]
        CodexAuth["CodexAuthenticator<br/>codex.go"]
        AntiAuth["AntigravityAuthenticator<br/>antigravity.go"]
        IFlowAuth["IFlowAuthenticator<br/>iflow.go"]
    end
    
    subgraph "Internal Auth Logic (internal/auth/*)"
        ClaudeSvc["ClaudeAuth<br/>claude/anthropic_auth.go"]
        GeminiSvc["GeminiAuth<br/>gemini/gemini_auth.go"]
        AntiSvc["AntigravityAuth<br/>antigravity/auth.go"]
    end
    
    subgraph "Management API (internal/api/handlers/management/*)"
        Forwarder["callbackForwarder<br/>auth_files.go"]
        RefreshUtil["extractLastRefreshTimestamp<br/>auth_files.go"]
    end
    
    ClaudeAuth --> ClaudeSvc
    AntiAuth --> AntiSvc
    ClaudeSvc --> Forwarder
    RefreshUtil -.-> RefreshUtil
```

**Key Code Entities:**

| Entity | File Path | Purpose |
|--------|-----------|---------|
| `ClaudeAuthenticator` | [sdk/auth/claude.go:21-21]() | High-level SDK implementation for Claude OAuth. |
| `AntigravityAuth` | [internal/auth/antigravity/auth.go:33-35]() | Service for generating auth URLs and exchanging codes for Antigravity. |
| `GeminiAuth` | [internal/auth/gemini/gemini_auth.go:46-47]() | Manages Gemini OAuth2 client and user info fetching. |
| `callbackForwarder` | [internal/api/handlers/management/auth_files.go:54-58]() | Redirects local OAuth callbacks to a remote management target. |
| `CredentialFileName` | [internal/auth/codex/filename.go:12-12]() | Generates standardized filenames for credential storage. |

Sources: [sdk/auth/claude.go:21-21](), [internal/auth/antigravity/auth.go:33-35](), [internal/auth/gemini/gemini_auth.go:46-47](), [internal/api/handlers/management/auth_files.go:54-58]()

---

## Management API Authentication Endpoints

The Management API provides mechanisms to facilitate authentication in environments where the proxy is running remotely (e.g., in a container or on a server).

### Callback Forwarding
When the `is_webui` query parameter is detected [internal/api/handlers/management/auth_files.go:120-131](), the proxy can start a `callbackForwarder`. This server listens on the provider's standard callback port (e.g., `8085` for Gemini) and redirects incoming traffic to the proxy's management URL [internal/api/handlers/management/auth_files.go:133-162](). This allows a user to complete a browser-based OAuth flow on their local machine while the tokens are captured by the remote proxy.

### Token Refresh Tracking
The system monitors credential health by extracting refresh timestamps from metadata using keys like `last_refresh` or `lastRefreshedAt` [internal/api/handlers/management/auth_files.go:44-44](). The `extractLastRefreshTimestamp` function handles various time formats and Unix timestamps to provide a unified view of credential age [internal/api/handlers/management/auth_files.go:67-79]().

Sources: [internal/api/handlers/management/auth_files.go:120-131](), [internal/api/handlers/management/auth_files.go:151-162](), [internal/api/handlers/management/auth_files.go:44-44](), [internal/api/handlers/management/auth_files.go:67-79]()

---

# Page: Token Storage Configuration

# Token Storage Configuration

<details>
<summary>Relevant source files</summary>

The following files were used as context for generating this wiki page:

- [.env.example](.env.example)
- [cmd/server/main.go](cmd/server/main.go)
- [go.mod](go.mod)
- [go.sum](go.sum)
- [internal/store/gitstore.go](internal/store/gitstore.go)
- [internal/store/objectstore.go](internal/store/objectstore.go)
- [internal/store/postgresstore.go](internal/store/postgresstore.go)
- [internal/watcher/synthesizer/config_test.go](internal/watcher/synthesizer/config_test.go)
- [internal/watcher/synthesizer/context.go](internal/watcher/synthesizer/context.go)
- [internal/watcher/synthesizer/file.go](internal/watcher/synthesizer/file.go)
- [internal/watcher/synthesizer/file_test.go](internal/watcher/synthesizer/file_test.go)
- [internal/watcher/synthesizer/helpers.go](internal/watcher/synthesizer/helpers.go)
- [internal/watcher/synthesizer/helpers_test.go](internal/watcher/synthesizer/helpers_test.go)
- [internal/watcher/synthesizer/interface.go](internal/watcher/synthesizer/interface.go)
- [sdk/auth/filestore.go](sdk/auth/filestore.go)
- [sdk/cliproxy/service_excluded_models_test.go](sdk/cliproxy/service_excluded_models_test.go)

</details>



## Purpose and Scope

This page explains how to configure token storage backends for CLIProxyAPI. Token storage is the persistence layer that stores OAuth tokens, API keys, service account credentials, and the main configuration file. The system supports four storage backends: File (default), PostgreSQL, Git, and Object Storage (S3-compatible).

This page covers:
- Storage backend architecture and selection priority.
- Configuration via environment variables for each backend.
- Initialization and bootstrap behavior.
- Data flow between the storage backends and the local filesystem spool.

For information about credential file formats and OAuth token lifecycle, see [Authentication Setup](). For comprehensive environment variable configuration, see [Environment Variables and Overrides](). For deployment-specific storage recommendations, see [High Availability and Scaling]().

---

## Storage Backend Architecture

The token storage system uses a pluggable interface that allows different persistence backends to be selected at runtime via environment variables. All backends implement a common store interface that provides credential persistence, configuration storage, and hot-reload support.

### Storage Interface and Implementation Hierarchy

```mermaid
graph TB
    subgraph "Store Interface Space"
        StoreIF["Store Interface<br/>(sdk/auth package)"]
    end
    
    subgraph "Code Entity Space: Implementations"
        FileStore["FileTokenStore<br/>[sdk/auth/filestore.go:22-26]()"]
        PGStore["PostgresStore<br/>[internal/store/postgresstore.go:39-46]()"]
        GitStore["GitTokenStore<br/>[internal/store/gitstore.go:28-38]()"]
        ObjStore["ObjectTokenStore<br/>[internal/store/objectstore.go:45-52]()"]
    end
    
    subgraph "Registration and Selection Logic"
        Register["sdkAuth.RegisterTokenStore()<br/>[cmd/server/main.go:446-454]()"]
        Priority["Selection Priority:<br/>Postgres > Object > Git > File"]
    end
    
    subgraph "Consumer Systems"
        AuthMgr["Auth Manager<br/>Credential loading"]
        ConfigMgr["Config Manager<br/>config.yaml persistence"]
        Watcher["File Watcher<br/>[internal/watcher/synthesizer/file.go:20-25]()"]
    end
    
    StoreIF --> FileStore
    StoreIF --> PGStore
    StoreIF --> GitStore
    StoreIF --> ObjStore
    
    FileStore --> Register
    PGStore --> Register
    GitStore --> Register
    ObjStore --> Register
    
    Register --> Priority
    
    Priority --> AuthMgr
    Priority --> ConfigMgr
    Priority --> Watcher
    
    FileStore -.->|"Writes to"| LocalFS[("auth-dir/*.json<br/>config.yaml")]
    PGStore -.->|"Syncs to"| PGDB[("PostgreSQL DB<br/>+ local spool")]
    GitStore -.->|"Commits to"| GitRepo[("Git Repository<br/>+ local clone")]
    ObjStore -.->|"Uploads to"| S3Bucket[("S3 Bucket<br/>+ local cache")]
```

Sources: `[cmd/server/main.go:131-454]()`, `[internal/store/postgresstore.go:39-46]()`, `[internal/store/gitstore.go:28-38]()`, `[internal/store/objectstore.go:45-52]()`, `[sdk/auth/filestore.go:22-26]()`

---

## Storage Backend Selection Priority

The system determines which storage backend to use based on environment variable presence. The selection follows a strict priority order, evaluated once during startup in `main.go`:

### Priority Order and Environment Variable Triggers

```mermaid
flowchart TD
    Start["Application Startup<br/>[cmd/server/main.go:56]()"]
    
    CheckPG{"PGSTORE_DSN<br/>set?<br/>[cmd/server/main.go:179]()"}
    CheckObj{"OBJECTSTORE_ENDPOINT<br/>set?<br/>[cmd/server/main.go:210]()"}
    CheckGit{"GITSTORE_GIT_URL<br/>set?<br/>[cmd/server/main.go:199]()"}
    
    UsePG["Use PostgreSQL Storage<br/>PostgresStore"]
    UseObj["Use Object Storage<br/>ObjectTokenStore"]
    UseGit["Use Git Storage<br/>GitTokenStore"]
    UseFile["Use File Storage<br/>FileTokenStore (default)"]
    
    InitPG["NewPostgresStore<br/>[cmd/server/main.go:242]()"]
    InitObj["NewObjectTokenStore<br/>[cmd/server/main.go:312]()"]
    InitGit["NewGitTokenStore<br/>[cmd/server/main.go:344]()"]
    InitFile["NewFileTokenStore<br/>[cmd/server/main.go:453]()"]
    
    RegisterStore["RegisterTokenStore<br/>[cmd/server/main.go:446]()"]
    
    Start --> CheckPG
    CheckPG -->|Yes| UsePG
    CheckPG -->|No| CheckObj
    CheckObj -->|Yes| UseObj
    CheckObj -->|No| CheckGit
    CheckGit -->|Yes| UseGit
    CheckGit -->|No| UseFile
    
    UsePG --> InitPG
    UseObj --> InitObj
    UseGit --> InitGit
    UseFile --> InitFile
    
    InitPG --> RegisterStore
    InitObj --> RegisterStore
    InitGit --> RegisterStore
    InitFile --> RegisterStore
```

**Priority Rules:**

1. **PostgreSQL** takes precedence when `PGSTORE_DSN` is set `[cmd/server/main.go:179-182]()`.
2. **Object Storage** is selected if `OBJECTSTORE_ENDPOINT` is set and PostgreSQL is not configured `[cmd/server/main.go:210-213]()`.
3. **Git Storage** is selected if `GITSTORE_GIT_URL` is set and neither PostgreSQL nor Object Storage is configured `[cmd/server/main.go:199-202]()`.
4. **File Storage** is the default fallback when no storage environment variables are set `[cmd/server/main.go:453]()`.

Sources: `[cmd/server/main.go:177-196]()`, `[cmd/server/main.go:237-454]()`

---

## Storage Backend Options

### File Storage (Default)

File storage is the simplest backend, storing all credentials and configuration directly on the local filesystem. This is suitable for single-server deployments and local development.

**Characteristics:**
- No external dependencies.
- Credentials stored in `.json` files within the `auth` directory `[sdk/auth/filestore.go:125-155]()`.
- Configuration in `config.yaml`.
- Uses `FileSynthesizer` to convert disk files into runtime `Auth` entities `[internal/watcher/synthesizer/file.go:28-60]()`.

**Configuration:**
No environment variables are required. File storage is automatically selected when no other storage backend is configured `[cmd/server/main.go:453]()`.

Sources: `[cmd/server/main.go:453]()`, `[sdk/auth/filestore.go:22-40]()`, `[internal/watcher/synthesizer/file.go:18-25]()`

---

### PostgreSQL Storage

PostgreSQL storage persists credentials and configuration to a PostgreSQL database while maintaining a local spool directory for fast access and compatibility with file-based watchers.

**Characteristics:**
- Credentials stored in the `auth_store` table as `JSONB` `[internal/store/postgresstore.go:132-142]()`.
- Configuration stored in the `config_store` table `[internal/store/postgresstore.go:121-131]()`.
- Local spool directory for caching mirrored data `[internal/store/postgresstore.go:74-81]()`.
- Automatic schema creation via `EnsureSchema` `[internal/store/postgresstore.go:111-143]()`.

**Configuration:**

| Environment Variable | Required | Default | Description |
|---------------------|----------|---------|-------------|
| `PGSTORE_DSN` | Yes | - | PostgreSQL connection string `[cmd/server/main.go:179-182]()` |
| `PGSTORE_SCHEMA` | No | `public` | Database schema name `[cmd/server/main.go:184-186]()` |
| `PGSTORE_LOCAL_PATH` | No | Writable base | Local spool directory `[cmd/server/main.go:187-196]()` |

**Initialization Flow:**

```mermaid
sequenceDiagram
    participant Main as main.go
    participant PGStore as PostgresStore
    participant DB as PostgreSQL
    participant FS as Filesystem
    
    Main->>Main: "Detect PGSTORE_DSN [cmd/server/main.go:179]"
    Main->>PGStore: "NewPostgresStore(ctx, config) [cmd/server/main.go:243]"
    PGStore->>DB: "sql.Open('pgx') [internal/store/postgresstore.go:83]"
    PGStore->>FS: "Create spoolRoot/config and spoolRoot/auths [internal/store/postgresstore.go:76-81]"
    
    Main->>PGStore: "Bootstrap(ctx, examplePath) [cmd/server/main.go:255]"
    PGStore->>DB: "EnsureSchema(ctx) [internal/store/postgresstore.go:111]"
    PGStore->>DB: "syncConfigFromDatabase(ctx) [internal/store/postgresstore.go:151]"
    PGStore->>DB: "syncAuthFromDatabase(ctx) [internal/store/postgresstore.go:154]"
```

Sources: `[cmd/server/main.go:177-266]()`, `[internal/store/postgresstore.go:1-158]()`

---

### Git Storage

Git storage maintains credentials and configuration in a Git repository, with a local clone for fast access. This provides a full audit trail of credential changes.

**Characteristics:**
- Automatic commit and push on changes via `commitAndPushLocked` `[internal/store/gitstore.go:206-211]()`.
- Support for remote push for redundancy `[internal/store/gitstore.go:415-430]()`.
- Local clone management including `PlainClone`, `PlainOpen`, and `Pull` `[internal/store/gitstore.go:118-194]()`.

**Configuration:**

| Environment Variable | Required | Default | Description |
|---------------------|----------|---------|-------------|
| `GITSTORE_GIT_URL` | Yes | - | Git repository URL `[cmd/server/main.go:199-202]()` |
| `GITSTORE_GIT_USERNAME` | No | - | Git username `[cmd/server/main.go:203-205]()` |
| `GITSTORE_GIT_TOKEN` | No | - | Git token or password `[cmd/server/main.go:206-208]()` |
| `GITSTORE_LOCAL_PATH` | No | Writable base | Local repository clone directory `[cmd/server/main.go:209-218]()` |

Sources: `[cmd/server/main.go:198-377]()`, `[internal/store/gitstore.go:1-213]()`

---

### Object Storage (S3-Compatible)

Object storage persists credentials and configuration to S3-compatible object storage (AWS S3, MinIO, etc.) with a local cache.

**Characteristics:**
- S3-compatible API via `minio-go` `[internal/store/objectstore.go:18-19]()`.
- Files are mirrored to a local workspace `[internal/store/objectstore.go:88-96]()`.
- Automatic upload on changes via `uploadAuth` `[internal/store/objectstore.go:222-224]()`.

**Configuration:**

| Environment Variable | Required | Default | Description |
|---------------------|----------|---------|-------------|
| `OBJECTSTORE_ENDPOINT` | Yes | - | S3 endpoint URL `[cmd/server/main.go:210-213]()` |
| `OBJECTSTORE_ACCESS_KEY` | Yes | - | Access key ID `[cmd/server/main.go:214-216]()` |
| `OBJECTSTORE_SECRET_KEY` | Yes | - | Secret access key `[cmd/server/main.go:217-219]()` |
| `OBJECTSTORE_BUCKET` | Yes | - | Bucket name `[cmd/server/main.go:220-222]()` |
| `OBJECTSTORE_LOCAL_PATH` | No | Writable base | Local cache directory `[cmd/server/main.go:223-225]()` |

Sources: `[cmd/server/main.go:210-333]()`, `[internal/store/objectstore.go:1-150]()`

---

## Writable Path Resolution

The system includes writable path detection to handle scenarios where the application may not have write permissions to the current working directory (e.g., in certain containerized or restricted environments).

**Path Priority:**
1. Explicitly configured `*_LOCAL_PATH` environment variable.
2. `util.WritablePath()` if available `[cmd/server/main.go:178]()`.
3. Current working directory as fallback `[cmd/server/main.go:194]()`.

Sources: `[cmd/server/main.go:176-341]()`

---

## Token Store Registration

After initialization, the selected storage backend is registered with the SDK authentication system using `sdkAuth.RegisterTokenStore()` `[cmd/server/main.go:446-454]()`. This allows management commands and the server to use the same persistence logic regardless of the backend.

```mermaid
graph TB
    subgraph "Storage Backend Selection [cmd/server/main.go]"
        SelectedStore["Selected Store Instance<br/>(PGStore/GitStore/ObjStore/FileStore)"]
    end
    
    subgraph "SDK Registration [sdk/auth]"
        Register["sdkAuth.RegisterTokenStore(store)<br/>[cmd/server/main.go:446]"]
    end
    
    subgraph "Consumer Code Entities"
        Save["Auth.Save()<br/>[sdk/auth/filestore.go:42]"]
        List["Auth.List()<br/>[sdk/auth/filestore.go:126]"]
        Delete["Auth.Delete()<br/>[sdk/auth/filestore.go:158]"]
    end
    
    SelectedStore --> Register
    Register --> Save
    Register --> List
    Register --> Delete
```

Sources: `[cmd/server/main.go:446-454]()`, `[sdk/auth/filestore.go:1-171]()`

---

# Page: Core Architecture

# Core Architecture

<details>
<summary>Relevant source files</summary>

The following files were used as context for generating this wiki page:

- [config.example.yaml](config.example.yaml)
- [internal/api/handlers/management/config_basic.go](internal/api/handlers/management/config_basic.go)
- [internal/api/handlers/management/config_lists.go](internal/api/handlers/management/config_lists.go)
- [internal/api/server.go](internal/api/server.go)
- [internal/config/config.go](internal/config/config.go)
- [internal/registry/model_definitions.go](internal/registry/model_definitions.go)
- [internal/registry/model_registry.go](internal/registry/model_registry.go)
- [internal/registry/model_registry_cache_test.go](internal/registry/model_registry_cache_test.go)
- [internal/registry/model_registry_hook_test.go](internal/registry/model_registry_hook_test.go)
- [internal/registry/model_registry_safety_test.go](internal/registry/model_registry_safety_test.go)
- [internal/thinking/apply_user_defined_test.go](internal/thinking/apply_user_defined_test.go)
- [internal/watcher/watcher.go](internal/watcher/watcher.go)
- [sdk/api/handlers/handlers.go](sdk/api/handlers/handlers.go)
- [sdk/cliproxy/auth/conductor.go](sdk/cliproxy/auth/conductor.go)
- [sdk/cliproxy/auth/conductor_overrides_test.go](sdk/cliproxy/auth/conductor_overrides_test.go)
- [sdk/cliproxy/auth/openai_compat_pool_test.go](sdk/cliproxy/auth/openai_compat_pool_test.go)
- [sdk/cliproxy/model_registry.go](sdk/cliproxy/model_registry.go)
- [sdk/cliproxy/service.go](sdk/cliproxy/service.go)
- [test/amp_management_test.go](test/amp_management_test.go)

</details>



## Purpose and Scope

This document provides a technical overview of CLIProxyAPI's internal architecture and component interactions. It describes how the system initializes, processes requests, manages credentials, and coordinates between different AI providers through a unified interface.

For initial setup and deployment patterns, see [Getting Started](#2). For detailed subsystem documentation, see the child pages on [Service Lifecycle and Initialization](#3.1), [HTTP Server and Middleware Pipeline](#3.2), [Authentication and Credential Management](#3.3), [Provider Executor System](#3.4), [Request Translation System](#3.5), [Model Registry and Capability System](#3.6), and [Hot Reload and Configuration Updates](#3.7).

---

## System Overview

CLIProxyAPI is a proxy server that unifies multiple AI provider APIs (OpenAI, Claude, Gemini, Codex, etc.) behind a single interface. The system translates between different API formats, manages credentials across providers, and implements intelligent routing with automatic failover.

### Core Components

| Component | Primary File(s) | Responsibility |
|-----------|----------------|----------------|
| **Service** | [sdk/cliproxy/service.go:32-92]() | Service lifecycle, component orchestration |
| **API Server** | [internal/api/server.go:122-179]() | HTTP request handling, routing, middleware |
| **Access Manager** | [sdk/access/manager.go:1-100]() | Request authentication (API keys) |
| **Core Auth Manager** | [sdk/cliproxy/auth/conductor.go:130-160]() | Provider credential management, retry logic |
| **Executors** | [sdk/cliproxy/auth/conductor.go:28-43]() | `ProviderExecutor` interface for API implementations |
| **Translators** | [sdk/translator/registry.go:1-100]() | Request/response format conversion |
| **Model Registry** | [internal/registry/model_registry.go:112-128]() | Model metadata and capabilities |
| **File Watcher** | [internal/watcher/watcher.go:32-62]() | Hot-reload for config and credentials |
| **Config** | [internal/config/config.go:28-130]() | Configuration management |

**Sources:** [sdk/cliproxy/service.go:32-92](), [internal/api/server.go:120-179](), [sdk/cliproxy/auth/conductor.go:27-43](), [internal/config/config.go:26-129]()

---

## Architecture Diagram

The following diagram bridges the high-level system concepts with the specific Go entities found in the codebase.

```mermaid
graph TB
    subgraph "Entry Point"
        Main["main.go<br/>CLI entry point"]
    end
    
    subgraph "Service Layer - sdk/cliproxy"
        Service["Service struct<br/>Run(), Shutdown()"]
        TokenProvider["TokenClientProvider<br/>OAuth credential loader"]
        APIKeyProvider["APIKeyClientProvider<br/>API key credential loader"]
    end
    
    subgraph "HTTP Layer - internal/api"
        Server["Server struct<br/>Gin engine"]
        Routes["Route handlers<br/>openai.Handler, claude.Handler"]
        Middleware["Middleware chain<br/>CORS, Auth, Logging"]
    end
    
    subgraph "Authentication - sdk"
        AccessMgr["sdkaccess.Manager<br/>Request authentication"]
        CoreAuthMgr["coreauth.Manager<br/>Provider credentials<br/>Retry logic"]
        Scheduler["authScheduler<br/>Credential selection"]
    end
    
    subgraph "Request Processing - internal/runtime"
        Executors["ProviderExecutor interface<br/>ClaudeExecutor<br/>GeminiExecutor"]
        Translators["sdktranslator.Registry<br/>OpenAI ↔ Claude<br/>OpenAI ↔ Gemini"]
    end
    
    subgraph "Core Services - internal"
        ModelReg["registry.ModelRegistry<br/>Model metadata"]
        Watcher["watcher.Watcher<br/>fsnotify events"]
        Config["config.Config<br/>config.yaml"]
    end
    
    subgraph "Storage"
        AuthDir["auth-dir/*.json<br/>OAuth tokens"]
        TokenStore["coreauth.Store<br/>Postgres/Git/File"]
    end
    
    Main --> Service
    Service --> Server
    Service --> AccessMgr
    Service --> CoreAuthMgr
    Service --> Watcher
    Service --> TokenProvider
    Service --> APIKeyProvider
    
    Server --> Routes
    Server --> Middleware
    Routes --> Translators
    Routes --> CoreAuthMgr
    
    Middleware --> AccessMgr
    
    CoreAuthMgr --> Scheduler
    CoreAuthMgr --> Executors
    Executors --> Translators
    
    Translators --> ModelReg
    
    Watcher --> Config
    Watcher --> AuthDir
    Watcher --> Server
    
    TokenProvider --> TokenStore
    TokenStore --> AuthDir
    
    CoreAuthMgr --> TokenStore
```

**Sources:** [sdk/cliproxy/service.go:32-92](), [internal/api/server.go:122-179](), [sdk/cliproxy/auth/conductor.go:130-160](), [internal/watcher/watcher.go:32-62]()

---

## Request Flow Architecture

This sequence diagram illustrates how a request traverses the system, specifically highlighting the interaction between the `BaseAPIHandler` and the `coreauth.Manager`.

```mermaid
sequenceDiagram
    participant Client
    participant ServerEngine as "Server.engine (gin.Engine)"
    participant AuthMW as "AuthMiddleware (sdkaccess.Manager)"
    participant Handler as "BaseAPIHandler (openai/claude/gemini)"
    participant Translator as "sdktranslator.Registry"
    participant CoreAuth as "coreauth.Manager (Conductor)"
    participant Scheduler as "authScheduler"
    participant Executor as "ProviderExecutor"
    participant Provider as "AI Provider API"
    
    Client->>ServerEngine: HTTP Request
    ServerEngine->>AuthMW: Middleware chain
    AuthMW->>AuthMW: Validate API Key
    AuthMW->>Handler: Authorized request
    
    Handler->>Translator: TranslateRequest()
    Translator-->>Handler: Translated payload
    
    Handler->>CoreAuth: Execute(req, opts)
    CoreAuth->>Scheduler: Pick(provider, model)
    Scheduler-->>CoreAuth: Selected *Auth
    
    loop Retry attempts (request-retry)
        CoreAuth->>Executor: Execute(auth, req, opts)
        Executor->>Provider: HTTP Request
        Provider-->>Executor: Response
        
        alt Success
            Executor-->>CoreAuth: Response + usage
            CoreAuth->>CoreAuth: OnResult(Success=true)
        else Retryable error
            Executor-->>CoreAuth: Error
            CoreAuth->>CoreAuth: Try next credential (max-retry-credentials)
        end
    end
    
    CoreAuth-->>Handler: Final response
    Handler->>Translator: TranslateResponse()
    Translator-->>Handler: Translated response
    Handler-->>ServerEngine: Response
    ServerEngine-->>Client: HTTP Response
```

**Sources:** [internal/api/server.go:181-191](), [sdk/cliproxy/auth/conductor.go:28-43](), [sdk/cliproxy/auth/conductor.go:102-115](), [sdk/cliproxy/auth/conductor.go:130-160](), [sdk/api/handlers/handlers.go:1-50]()

---

## Component Responsibilities

### Service (`sdk/cliproxy/service.go`)

The `Service` struct is the top-level orchestrator that manages the complete application lifecycle:

- **Initialization**: Creates and wires all subsystem components.
- **Lifecycle Management**: Manages startup and graceful shutdown for embedded components.
- **Component Coordination**: Maintains references to `Server`, `authManager`, `accessManager`, `coreManager`, `watcher`, and `wsGateway`.
- **Auth Update Processing**: Consumes auth updates from file watcher via channel `authUpdates` [sdk/cliproxy/service.go:114-127]().
- **Websocket Gateway**: Manages `wsrelay.Manager` for runtime-only authentication, specifically for AI Studio providers [sdk/cliproxy/service.go:204-220]().

Key methods:
- `consumeAuthUpdates(ctx)`: Background loop that handles incremental auth changes [sdk/cliproxy/service.go:129-151]().
- `handleAuthUpdate(ctx, update)`: Dispatches add/modify/delete actions to the core manager [sdk/cliproxy/service.go:174-202]().
- `ensureWebsocketGateway()`: Initializes the WebSocket relay for dynamic providers [sdk/cliproxy/service.go:204-220]().

**Sources:** [sdk/cliproxy/service.go:32-92](), [sdk/cliproxy/service.go:129-202]()

---

### API Server (`internal/api/server.go`)

The `Server` struct wraps a Gin HTTP engine and provides:

- **Route Registration**: Defines endpoints for OpenAI, Claude, Gemini, and management APIs.
- **Middleware Pipeline**: CORS, request logging, and authentication via `sdkaccess.Manager`.
- **Configuration Hot-Reload**: Responds to configuration changes without restart [internal/api/server.go:135-138]().
- **Management API**: Conditionally serves `/v0/management/*` using the `managementHandlers.Handler` [internal/api/server.go:159-160]().
- **Keep-Alive Endpoint**: Optional `/keep-alive` for management tools to prevent idle timeout [internal/api/server.go:94-104]().

**Sources:** [internal/api/server.go:122-179](), [internal/api/server.go:181-191]()

---

### Authentication System

The system implements dual authentication layers:

#### 1. Request Authentication (`sdk/access/manager.go`)

The `sdkaccess.Manager` validates incoming client requests using API keys. This is configured via `config.yaml` in the `api-keys` field [internal/config/config.go:39-43]().

#### 2. Provider Credential Management (`sdk/cliproxy/auth/conductor.go`)

The `coreauth.Manager` (Conductor) manages provider credentials and execution logic:

- **Credential Storage**: In-memory map of `ID → Auth` entries [sdk/cliproxy/auth/conductor.go:136]().
- **Scheduler Integration**: Selects credentials based on model and routing strategy [sdk/cliproxy/auth/conductor.go:133]().
- **Retry Logic**: Configurable retry attempts (`request-retry`) and credential failover (`max-retry-credentials`) [internal/config/config.go:72-75]().
- **Quota Management**: Tracks credential cooldown periods unless `disable-cooling` is set [internal/config/config.go:69]().
- **Model Pool Resolution**: Maps client model names to provider models via aliases [sdk/cliproxy/auth/conductor.go:146-154]().

**Sources:** [sdk/cliproxy/auth/conductor.go:130-160](), [internal/config/config.go:70-82]()

---

### Provider Executor System (`sdk/cliproxy/auth/conductor.go`)

Each provider implements the `ProviderExecutor` interface, allowing the `Manager` to execute requests without knowing provider-specific details:

```go
type ProviderExecutor interface {
	Identifier() string
	Execute(ctx context.Context, auth *Auth, req cliproxyexecutor.Request, opts cliproxyexecutor.Options) (cliproxyexecutor.Response, error)
	ExecuteStream(ctx context.Context, auth *Auth, req cliproxyexecutor.Request, opts cliproxyexecutor.Options) (*cliproxyexecutor.StreamResult, error)
	Refresh(ctx context.Context, auth *Auth) (*Auth, error)
	CountTokens(ctx context.Context, auth *Auth, req cliproxyexecutor.Request, opts cliproxyexecutor.Options) (cliproxyexecutor.Response, error)
	HttpRequest(ctx context.Context, auth *Auth, req *http.Request) (*http.Response, error)
}
```

**Sources:** [sdk/cliproxy/auth/conductor.go:28-43]()

---

### Request Translation System (`sdk/translator/`)

The translation registry provides bidirectional format conversion between API formats. This allows an OpenAI-formatted request to be processed by a Claude or Gemini executor. It also handles advanced features like reasoning/thinking configuration across providers.

---

### Hot Reload System (`internal/watcher/watcher.go`)

The `Watcher` monitors filesystem changes and triggers zero-downtime updates:

- **Watched Resources**: `config.yaml` and the `auth-dir` directory [internal/watcher/watcher.go:33-34]().
- **Debouncing Strategy**:
    - Config changes: `configReloadDebounce` (150ms) [internal/watcher/watcher.go:84]().
    - Server updates: `serverUpdateDebounce` (1s) [internal/watcher/watcher.go:86]().
- **Persistence Propagation**: Detects persistence-capable token stores to propagate changes [internal/watcher/watcher.go:104-108]().

**Sources:** [internal/watcher/watcher.go:80-87](), [internal/watcher/watcher.go:104-115]()

---

## Configuration Management (`internal/config/config.go`)

The `Config` struct represents the complete application configuration, including server settings, provider-specific keys, and routing logic.

**Key Configuration Sections:**

| Section | Field(s) | Purpose |
|---------|----------|---------|
| Server | `Host`, `Port`, `TLS` | HTTP server binding [internal/config/config.go:30-37]() |
| Authentication | `AuthDir`, `WebsocketAuth` | Credential storage and WS security [internal/config/config.go:43, 86]() |
| Provider Keys | `GeminiKey`, `ClaudeKey`, `CodexKey` | Static API key configurations [internal/config/config.go:88-99]() |
| Routing | `Routing`, `RequestRetry` | Selection and failover behavior [internal/config/config.go:71-83]() |
| Model Aliases | `OAuthModelAlias` | Global model name mappings [internal/config/config.go:118-124]() |

**Sources:** [internal/config/config.go:26-129]()

---

## Subsystem Details

Detailed documentation for each subsystem is available in the child pages:

- **[Service Lifecycle and Initialization](#3.1)**: Service startup sequence, component initialization order, and graceful shutdown.
- **[HTTP Server and Middleware Pipeline](#3.2)**: Gin engine configuration, route registration, and middleware chain.
- **[Authentication and Credential Management](#3.3)**: Dual authentication system and credential lifecycle.
- **[Provider Executor System](#3.4)**: Executor interface and provider-specific implementations.
- **[Request Translation System](#3.5)**: Translation registry and format conversion logic.
- **[Model Registry and Capability System](#3.6)**: Model metadata and capability tracking.
- **[Hot Reload and Configuration Updates](#3.7)**: File watching and runtime configuration updates.

---

# Page: Service Lifecycle and Initialization

# Service Lifecycle and Initialization

<details>
<summary>Relevant source files</summary>

The following files were used as context for generating this wiki page:

- [cmd/server/main.go](cmd/server/main.go)
- [config.example.yaml](config.example.yaml)
- [go.mod](go.mod)
- [go.sum](go.sum)
- [internal/api/handlers/management/config_basic.go](internal/api/handlers/management/config_basic.go)
- [internal/api/handlers/management/config_lists.go](internal/api/handlers/management/config_lists.go)
- [internal/api/server.go](internal/api/server.go)
- [internal/cmd/login.go](internal/cmd/login.go)
- [internal/cmd/run.go](internal/cmd/run.go)
- [internal/config/config.go](internal/config/config.go)
- [internal/store/gitstore.go](internal/store/gitstore.go)
- [internal/store/postgresstore.go](internal/store/postgresstore.go)
- [internal/watcher/watcher.go](internal/watcher/watcher.go)
- [sdk/cliproxy/service.go](sdk/cliproxy/service.go)
- [test/amp_management_test.go](test/amp_management_test.go)

</details>



## Purpose and Scope

This page describes the internal mechanics of service startup, component initialization order, signal handling, and graceful shutdown. It covers the complete lifecycle from process start to clean termination, including the builder pattern for service construction, middleware pipeline setup, and background worker coordination.

For deployment modes and execution patterns, see **2.1 Installation and Deployment**. For configuration file structure and loading, see **5.1 Configuration File Structure**. For the HTTP middleware pipeline details, see **3.2 HTTP Server and Middleware Pipeline**.

---

## System Entry Points

The service provides multiple entry points depending on the execution mode, primarily managed through the `cmd` package and the `cliproxy` SDK.

| Entry Mode | Entry Point | Use Case |
|------------|-------------|----------|
| **Server Mode** | `StartService` | Standard HTTP server with signal handling [internal/cmd/run.go:27]() |
| **Background Mode** | `StartServiceBackground` | Embedded service with programmatic control [internal/cmd/run.go:60]() |
| **Cloud Deploy Mode** | `WaitForCloudDeploy` | Standby mode awaiting configuration [internal/cmd/run.go:88]() |
| **TUI Standalone** | `StartService` with local password | Embedded server with 10s keep-alive timeout [internal/cmd/run.go:37-44]() |

The `StartService` function implements signal-based lifecycle management using `signal.NotifyContext` to handle `SIGINT` and `SIGTERM` [internal/cmd/run.go:33]().

**Sources:** [internal/cmd/run.go:27-98](), [sdk/cliproxy/service.go:29-92]()

---

## Service Builder Pattern

The service uses a builder pattern (`cliproxy.Builder`) to construct instances with customizable providers. The builder accumulates configuration before producing a `Service` instance via the `Build()` method.

### Builder to Service Association

```mermaid
graph LR
    Builder["cliproxy.Builder"]
    Config["WithConfig(cfg)"]
    Path["WithConfigPath(path)"]
    Password["WithLocalManagementPassword(pwd)"]
    ServerOpts["WithServerOptions(opts...)"]
    Hooks["WithHooks(hooks)"]
    Build["Build()"]
    Service["cliproxy.Service"]
    
    Builder --> Config
    Builder --> Path
    Builder --> Password
    Builder --> ServerOpts
    Builder --> Hooks
    Config --> Build
    Path --> Build
    Password --> Build
    ServerOpts --> Build
    Hooks --> Build
    Build --> Service
```

The `Build()` method validates required inputs like `Config` and `ConfigPath`, then initializes default providers if none were supplied (e.g., `newDefaultAuthManager` [sdk/cliproxy/service.go:104]()).

**Sources:** [internal/cmd/run.go:28-46](), [sdk/cliproxy/service.go:32-92]()

---

## Complete Initialization Sequence

The following diagram shows the complete initialization order from service construction through startup:

```mermaid
sequenceDiagram
    participant Main as "main.go / StartService"
    participant Builder as "cliproxy.Builder"
    participant Service as "cliproxy.Service"
    participant Usage as "usage.RegisterPlugin"
    participant CoreAuth as "coreauth.Manager"
    participant TokenStore as "sdkAuth.GetTokenStore"
    participant APIServer as "api.Server"
    participant WSGateway as "wsrelay.Manager"
    participant Watcher as "watcher.Watcher"
    
    Main->>Builder: NewBuilder()
    Main->>Builder: WithConfig(cfg)
    Main->>Builder: Build()
    Builder->>Service: new Service instance
    
    Main->>Service: Run(ctx)
    Service->>Usage: RegisterUsagePlugin(plugin)
    
    Service->>TokenStore: GetTokenStore()
    Service->>CoreAuth: NewManager(store, ...)
    Note over CoreAuth: Load auth entries from store
    
    Service->>APIServer: NewServer(cfg, authManager, accessManager, ...)
    APIServer->>APIServer: Initialize gin engine
    APIServer->>APIServer: Setup middleware chain
    APIServer-->>Service: HTTP server ready
    
    Service->>Service: ensureWebsocketGateway()
    Service->>WSGateway: NewManager(opts)
    
    Service->>Watcher: NewWatcher(configPath, authDir, reload)
    Watcher-->>Service: watcher instance
    Service->>Service: ensureAuthUpdateQueue(ctx)
    Service->>Watcher: SetAuthUpdateQueue(authUpdates)
    Service->>Watcher: Start(ctx)
    
    Service->>APIServer: Start()
    Note over APIServer: ListenAndServe / ListenAndServeTLS
```

**Key Initialization Steps:**

1. **Usage Tracking**: Plugins are registered via `RegisterUsagePlugin` to monitor token consumption [sdk/cliproxy/service.go:99-101]().
2. **Auth Management**: `coreauth.Manager` is initialized to handle provider credentials, often using `sdkAuth.GetTokenStore()` for persistence [sdk/cliproxy/service.go:106]().
3. **HTTP Server**: `api.NewServer` constructs the Gin engine, registers routes (OpenAI, Claude, Gemini), and attaches middleware [internal/api/server.go:181-191]().
4. **WebSocket Gateway**: `ensureWebsocketGateway` initializes a `wsrelay.Manager` to handle runtime-only AI Studio providers [sdk/cliproxy/service.go:204-220]().
5. **File Watcher**: `watcher.NewWatcher` begins monitoring `config.yaml` and the `auth-dir` for hot-reloads [internal/watcher/watcher.go:90-117]().
6. **Auth Update Queue**: `ensureAuthUpdateQueue` starts a background goroutine `consumeAuthUpdates` to process incremental credential changes [sdk/cliproxy/service.go:114-127]().

**Sources:** [sdk/cliproxy/service.go:114-127](), [internal/api/server.go:181-191](), [internal/watcher/watcher.go:90-117]()

---

## HTTP Server Construction

The `api.Server` is constructed through `NewServer`, which sets up the Gin engine, middleware pipeline, and route handlers.

### Code Entity Mapping: Server Components

```mermaid
graph TB
    subgraph "api.Server Initialization"
        NewServer["api.NewServer()"]
        Engine["gin.Engine"]
        Access["sdkaccess.Manager"]
        Mgmt["managementHandlers.Handler"]
        Amp["ampmodule.AmpModule"]
    end
    
    subgraph "Middleware Components"
        BaseHandler["handlers.BaseAPIHandler"]
        RequestLogger["logging.RequestLogger"]
        WSAuth["atomic.Bool (wsAuthEnabled)"]
    end

    NewServer --> Engine
    NewServer --> Access
    NewServer --> Mgmt
    NewServer --> Amp
    NewServer --> BaseHandler
    NewServer --> RequestLogger
    
    BaseHandler --> Engine
```

**Route Registration** happens during server construction:
- **OpenAI-compatible routes**: `/v1/chat/completions`, `/v1/models` [internal/api/server.go:3]().
- **Gemini routes**: Handled via `gemini.Handler` [internal/api/server.go:35]().
- **Claude routes**: Handled via `claude.Handler` [internal/api/server.go:34]().
- **Management routes**: `/v0/management/*` handled by `managementHandlers.Handler` [internal/api/server.go:23]().

**Sources:** [internal/api/server.go:122-191](), [internal/api/server.go:23-36]()

---

## Signal Handling and Graceful Shutdown

The service implements a clean shutdown sequence to ensure active requests finish and resources are released.

### Shutdown Flow

```mermaid
sequenceDiagram
    participant OS as "OS Signal (SIGINT/SIGTERM)"
    participant Svc as "cliproxy.Service"
    participant Watcher as "watcher.Watcher"
    participant WS as "wsrelay.Manager"
    participant HTTP as "api.Server"
    
    OS->>Svc: Trigger Shutdown
    Svc->>Svc: shutdownOnce.Do()
    
    Svc->>Watcher: Stop()
    Watcher-->>Svc: Watcher Closed
    
    Svc->>WS: Stop(ctx)
    WS-->>Svc: Connections Closed
    
    Svc->>HTTP: Stop(ctx)
    HTTP->>HTTP: http.Server.Shutdown()
    HTTP-->>Svc: Server Stopped
    
    Svc->>Svc: authQueueStop()
```

**Graceful Shutdown Mechanics:**
1. **Signal Capture**: The service context is cancelled upon receiving a termination signal [internal/cmd/run.go:33]().
2. **File Watcher**: `watcher.Stop()` is called to close `fsnotify` handles and stop timers [internal/watcher/watcher.go:125-131]().
3. **HTTP Server**: The underlying `http.Server.Shutdown(ctx)` is invoked, which waits for active connections to close [internal/api/server.go:127]().
4. **Auth Updates**: The `authQueueStop` context cancellation terminates the `consumeAuthUpdates` loop [sdk/cliproxy/service.go:124-126]().

**Sources:** [internal/watcher/watcher.go:125-131](), [sdk/cliproxy/service.go:114-127](), [internal/cmd/run.go:33-44]()

---

## Auth Update Queue and Hot Reload

Incremental changes to credentials (from file changes or management API) are processed via the `authUpdates` channel [sdk/cliproxy/service.go:135]().

| Action | Logic | Code Entity |
|--------|-------|-------------|
| **Add/Modify** | `applyCoreAuthAddOrUpdate` | [sdk/cliproxy/service.go:189]() |
| **Delete** | `applyCoreAuthRemoval` | [sdk/cliproxy/service.go:198]() |
| **Runtime Update** | `DispatchRuntimeAuthUpdate` | [internal/watcher/watcher.go:149-151]() |

The `Watcher` debounces file system events to prevent rapid reload cycles:
- `configReloadDebounce`: 150ms [internal/watcher/watcher.go:84]().
- `serverUpdateDebounce`: 1s [internal/watcher/watcher.go:86]().

**Sources:** [sdk/cliproxy/service.go:129-151](), [internal/watcher/watcher.go:80-87](), [internal/watcher/watcher.go:149-151]()

---

# Page: HTTP Server and Middleware Pipeline

# HTTP Server and Middleware Pipeline

<details>
<summary>Relevant source files</summary>

The following files were used as context for generating this wiki page:

- [config.example.yaml](config.example.yaml)
- [internal/api/handlers/management/config_basic.go](internal/api/handlers/management/config_basic.go)
- [internal/api/handlers/management/config_lists.go](internal/api/handlers/management/config_lists.go)
- [internal/api/middleware/request_logging.go](internal/api/middleware/request_logging.go)
- [internal/api/middleware/response_writer.go](internal/api/middleware/response_writer.go)
- [internal/api/server.go](internal/api/server.go)
- [internal/config/config.go](internal/config/config.go)
- [internal/logging/gin_logger.go](internal/logging/gin_logger.go)
- [internal/logging/gin_logger_test.go](internal/logging/gin_logger_test.go)
- [internal/logging/request_logger.go](internal/logging/request_logger.go)
- [internal/runtime/executor/logging_helpers.go](internal/runtime/executor/logging_helpers.go)
- [internal/watcher/watcher.go](internal/watcher/watcher.go)
- [sdk/api/handlers/claude/code_handlers.go](sdk/api/handlers/claude/code_handlers.go)
- [sdk/api/handlers/gemini/gemini-cli_handlers.go](sdk/api/handlers/gemini/gemini-cli_handlers.go)
- [sdk/api/handlers/gemini/gemini_handlers.go](sdk/api/handlers/gemini/gemini_handlers.go)
- [sdk/api/handlers/openai/openai_handlers.go](sdk/api/handlers/openai/openai_handlers.go)
- [sdk/api/handlers/openai/openai_responses_handlers.go](sdk/api/handlers/openai/openai_responses_handlers.go)
- [sdk/cliproxy/service.go](sdk/cliproxy/service.go)
- [test/amp_management_test.go](test/amp_management_test.go)

</details>



This document details the HTTP server architecture and request processing pipeline in CLIProxyAPI. It covers server initialization, middleware stack, route registration, and the flow of requests from client to provider executor.

For authentication and credential management details, see **3.3 Authentication and Credential Management**. For provider executor implementations, see **3.4 Provider Executor System**. For configuration hot-reload mechanisms, see **3.1 Service Lifecycle and Initialization**.

---

## Overview

The HTTP server is built on the Gin web framework and provides multiple API surfaces:

- **OpenAI-compatible endpoints** (`/v1/*`) for chat completions and model listing [internal/api/server.go:332-339]().
- **Gemini endpoints** (`/v1beta/*`) for native Google Gemini API format [internal/api/server.go:342-348]().
- **Claude endpoints** (`/v1/messages`) for Anthropic-style messages API [internal/api/server.go:334-335]().
- **Management API** (`/v0/management/*`) for configuration and administration [internal/api/server.go:476-644]().
- **Amp integration routes** (`/api/provider/:provider/*`) for Amp CLI proxy support [internal/api/server.go:278]().
- **OAuth callback endpoints** for authentication flow completion [internal/api/server.go:366-435]().
- **WebSocket relay** (`/v1/ws`) for AI Studio provider connections [internal/api/server.go:429-464]().

The server supports TLS, hot-reload, conditional middleware, and multi-protocol request translation.

**Sources:** [internal/api/server.go:1-5]()

---

## Server Structure and Initialization

### Server Struct

The `api.Server` struct encapsulates the HTTP server state and dependencies.

**Title: Server Struct Entity Mapping**

```mermaid
graph TB
    subgraph "Core HTTP Components"
        Engine["engine [internal/api/server.go:124]<br/>*gin.Engine<br/>Routes & middleware"]
        HTTPServer["server [internal/api/server.go:127]<br/>*http.Server<br/>TCP listener"]
    end
    
    subgraph "Request Processing"
        Handlers["handlers [internal/api/server.go:130]<br/>*handlers.BaseAPIHandler<br/>Protocol handlers"]
        AccessMgr["accessManager [internal/api/server.go:139]<br/>*sdkaccess.Manager<br/>Request authentication"]
        ReqLogger["requestLogger [internal/api/server.go:142]<br/>logging.RequestLogger<br/>Request/capture"]
    end
    
    subgraph "Configuration & State"
        Config["cfg [internal/api/server.go:133]<br/>*config.Config<br/>Current config snapshot"]
        OldYAML["oldConfigYaml [internal/api/server.go:137]<br/>[]byte<br/>YAML snapshot for diff"]
        ConfigPath["configFilePath [internal/api/server.go:147]<br/>string<br/>Absolute config path"]
    end
    
    subgraph "Management & Admin"
        Mgmt["mgmt [internal/api/server.go:159]<br/>*managementHandlers.Handler<br/>Admin API logic"]
        MgmtEnabled["managementRoutesEnabled [internal/api/server.go:166]<br/>atomic.Bool<br/>Dynamic enable/disable"]
        MgmtRegistered["managementRoutesRegistered [internal/api/server.go:164]<br/>atomic.Bool<br/>Registration guard"]
    end
    
    subgraph "Feature Modules"
        Amp["ampModule [internal/api/server.go:161]<br/>*ampmodule.AmpModule<br/>Amp CLI routing"]
        WSRoutes["wsRoutes [internal/api/server.go:154]<br/>map[string]struct{}<br/>Registered WS paths"]
        WSAuthEnabled["wsAuthEnabled [internal/api/server.go:156]<br/>atomic.Bool<br/>WebSocket auth toggle"]
    end
    
    Engine --> Handlers
    Handlers --> AccessMgr
    Config --> Mgmt
    Mgmt --> MgmtEnabled
```

| Field | Type | Purpose |
|-------|------|---------|
| `engine` | `*gin.Engine` | Gin framework instance managing routes and middleware [internal/api/server.go:124]() |
| `server` | `*http.Server` | Underlying Go HTTP server with TCP listener [internal/api/server.go:127]() |
| `handlers` | `*handlers.BaseAPIHandler` | Base handler providing execution logic [internal/api/server.go:130]() |
| `cfg` | `*config.Config` | Current configuration snapshot [internal/api/server.go:133]() |
| `oldConfigYaml` | `[]byte` | YAML-serialized previous config for change detection [internal/api/server.go:137]() |
| `accessManager` | `*sdkaccess.Manager` | Request authentication provider manager [internal/api/server.go:139]() |
| `requestLogger` | `logging.RequestLogger` | Request/response logging subsystem [internal/api/server.go:142]() |
| `mgmt` | `*managementHandlers.Handler` | Management API handler with auth middleware [internal/api/server.go:159]() |
| `ampModule` | `*ampmodule.AmpModule` | Amp CLI integration for model mapping [internal/api/server.go:161]() |

**Sources:** [internal/api/server.go:122-179]()

### NewServer Constructor

The `NewServer` function initializes the server with layered configuration [internal/api/server.go:181]().

**Title: NewServer Initialization Flow**

```mermaid
graph TB
    Start["NewServer called [internal/api/server.go:181]"]
    
    subgraph "Option Processing"
        OptConfig["Process ServerOption[]<br/>Build serverOptionConfig"]
        CheckFactory["requestLoggerFactory<br/>default: defaultRequestLoggerFactory [internal/api/server.go:60]"]
    end
    
    subgraph "Gin Setup"
        SetMode["gin.SetMode<br/>(ReleaseMode if !cfg.Debug) [internal/api/server.go:193]"]
        CreateEngine["gin.New() [internal/api/server.go:198]"]
    end
    
    subgraph "Middleware Stack"
        MW1["engine.Use(logging.GinLogrusLogger()) [internal/api/server.go:210]"]
        MW2["engine.Use(logging.GinLogrusRecovery()) [internal/api/server.go:211]"]
        MW3["if !cfg.CommercialMode:<br/>engine.Use(middleware.RequestLoggingMiddleware) [internal/api/server.go:225]"]
        MW4["engine.Use(corsMiddleware()) [internal/api/server.go:232]"]
    end
    
    subgraph "Server Construction"
        CreateServer["s := &Server{...} [internal/api/server.go:237]"]
        SaveYAML["s.oldConfigYaml, _ = yaml.Marshal(cfg) [internal/api/server.go:251]"]
        ApplyAccess["s.applyAccessConfig(nil, cfg) [internal/api/server.go:254]"]
    end
    
    subgraph "Route Registration"
        SetupRoutes["s.setupRoutes() [internal/api/server.go:268]"]
        RegisterAmp["modules.RegisterModule(ctx, s.ampModule) [internal/api/server.go:278]"]
    end
    
    Start --> OptConfig
    OptConfig --> CheckFactory
    CheckFactory --> SetMode
    SetMode --> CreateEngine
    CreateEngine --> MW1
    MW1 --> MW2
    MW2 --> MW3
    MW3 --> MW4
    MW4 --> CreateServer
    CreateServer --> SaveYAML
    SaveYAML --> ApplyAccess
    ApplyAccess --> SetupRoutes
    SetupRoutes --> RegisterAmp
```

**Sources:** [internal/api/server.go:181-305]()

---

## Middleware Stack

### Middleware Execution Order

The middleware stack processes requests in a specific order:

1.  **`logging.GinLogrusLogger()`**: Request start/end logging with status codes and latency [internal/api/server.go:210]().
2.  **`logging.GinLogrusRecovery()`**: Panic recovery with stack trace logging [internal/api/server.go:211]().
3.  **`middleware.RequestLoggingMiddleware`**: Detailed request/response body capture [internal/api/server.go:225](). This is skipped if `CommercialMode` is enabled [internal/config/config.go:51-52]().
4.  **`corsMiddleware()`**: Injects permissive CORS headers [internal/api/server.go:232]().

### Request Logging Middleware

The `RequestLoggingMiddleware` uses a `ResponseWriterWrapper` to capture data without blocking the client response [internal/api/middleware/response_writer.go:31]().

- **Zero Latency**: It writes to the client first before handling logging [internal/api/middleware/response_writer.go:76-77]().
- **Streaming Support**: For `text/event-stream`, it uses an asynchronous chunk processor [internal/api/middleware/response_writer.go:175]().
- **TTFB Capture**: Captures Time-To-First-Byte for streaming responses [internal/api/middleware/response_writer.go:82-84]().

**Sources:** [internal/api/middleware/response_writer.go:1-180]()

---

## Route Registration

### setupRoutes Overview

The `setupRoutes` method registers endpoints across several logical groups [internal/api/server.go:319]().

**Title: Route Group and Handler Mapping**

| Route Group | Middleware | Key Handlers |
| :--- | :--- | :--- |
| `/v1` | `AuthMiddleware` | `ChatCompletions`, `ClaudeMessages` [internal/api/server.go:332-334]() |
| `/v1beta` | `AuthMiddleware` | `GeminiHandler`, `GeminiModels` [internal/api/server.go:342-348]() |
| `/v0/management` | `mgmt.Middleware` | `Config`, `Usage`, `API Keys` [internal/api/server.go:476-644]() |
| `/anthropic/callback` | None | OAuth callback for Claude [internal/api/server.go:366]() |

### OpenAI and Claude Routes (/v1)

The `/v1` group enforces request authentication via `AuthMiddleware` [internal/api/server.go:329]().

- **Chat Completions**: `POST /v1/chat/completions` -> `openaiHandlers.ChatCompletions` [internal/api/server.go:332]().
- **Claude Messages**: `POST /v1/messages` -> `claudeCodeHandlers.ClaudeMessages` [internal/api/server.go:334]().
- **Unified Models**: `GET /v1/models` routes to either OpenAI or Claude model lists based on headers [internal/api/server.go:338]().

**Sources:** [internal/api/server.go:328-339]()

### Gemini Routes (/v1beta)

Native Gemini API support is provided under `/v1beta` [internal/api/server.go:342]().

- **Generate Content**: `POST /v1beta/models/*action` -> `geminiHandlers.GeminiHandler` [internal/api/server.go:346]().
- **Model Info**: `GET /v1beta/models/*action` -> `geminiHandlers.GeminiGetHandler` [internal/api/server.go:347]().

**Sources:** [internal/api/server.go:342-348]()

---

## Request Flow and Execution

### Complete Request Pipeline

**Title: Request Execution Sequence**

```mermaid
sequenceDiagram
    participant Client
    participant Gin["gin.Engine [internal/api/server.go:124]"]
    participant MW["Middleware Stack [internal/api/middleware]"]
    participant Handler["openai.OpenAIAPIHandler [sdk/api/handlers/openai]"]
    participant Base["handlers.BaseAPIHandler [sdk/api/handlers/handlers.go]"]
    participant Provider["AI Provider API"]
    
    Client->>Gin: POST /v1/chat/completions
    Gin->>MW: Execute chain (Logrus -> RequestLog -> CORS)
    MW->>Handler: ChatCompletions(c)
    Handler->>Base: ExecuteStreamWithAuthManager(ctx, req, opts)
    Base->>Provider: Upstream Request
    Provider-->>Base: Response Stream
    Base-->>Handler: Translated Chunks
    Handler-->>Client: SSE Stream
```

**Sources:** [internal/api/server.go:328-339](), [sdk/api/handlers/openai/openai_handlers.go:1-10]()

---

## Hot Reload and Configuration Updates

The `UpdateClients(cfg)` method allows the server to adapt to configuration changes without a restart [internal/api/server.go:856]().

### Change Detection Logic

The server compares the new configuration against a YAML snapshot of the previous state [internal/api/server.go:867]().

| Condition | Action |
| :--- | :--- |
| `RequestLog` changed | Toggles `requestLogger.SetEnabled()` [internal/api/server.go:872-882]() |
| `LoggingToFile` changed | Reconfigures log output [internal/api/server.go:884-889]() |
| `Debug` changed | Updates log level [internal/api/server.go:910-912]() |
| `SecretKey` changed | Toggles `managementRoutesEnabled` atomic flag [internal/api/server.go:914-944]() |

**Sources:** [internal/api/server.go:856-1018]()

---

## Server Lifecycle

- **Start**: Binds to the configured `Host:Port` and starts `ListenAndServe()` or `ListenAndServeTLS()` [internal/api/server.go:767-792]().
- **Stop**: Performs a graceful shutdown via `server.Shutdown(ctx)` [internal/api/server.go:802-819]().
- **Keep-Alive**: Optional watchdog goroutine that triggers `onTimeout` if heartbeats to `/keep-alive` stop [internal/api/server.go:713-741]().

**Sources:** [internal/api/server.go:713-819]()

---

# Page: Authentication and Credential Management

# Authentication and Credential Management

<details>
<summary>Relevant source files</summary>

The following files were used as context for generating this wiki page:

- [docs/sdk-access.md](docs/sdk-access.md)
- [docs/sdk-access_CN.md](docs/sdk-access_CN.md)
- [internal/access/config_access/provider.go](internal/access/config_access/provider.go)
- [internal/access/reconcile.go](internal/access/reconcile.go)
- [internal/thinking/apply_user_defined_test.go](internal/thinking/apply_user_defined_test.go)
- [sdk/access/errors.go](sdk/access/errors.go)
- [sdk/access/manager.go](sdk/access/manager.go)
- [sdk/access/registry.go](sdk/access/registry.go)
- [sdk/api/handlers/handlers.go](sdk/api/handlers/handlers.go)
- [sdk/cliproxy/auth/conductor.go](sdk/cliproxy/auth/conductor.go)
- [sdk/cliproxy/auth/conductor_overrides_test.go](sdk/cliproxy/auth/conductor_overrides_test.go)
- [sdk/cliproxy/auth/openai_compat_pool_test.go](sdk/cliproxy/auth/openai_compat_pool_test.go)
- [sdk/cliproxy/auth/selector.go](sdk/cliproxy/auth/selector.go)
- [sdk/cliproxy/auth/selector_test.go](sdk/cliproxy/auth/selector_test.go)
- [sdk/cliproxy/auth/types.go](sdk/cliproxy/auth/types.go)
- [sdk/cliproxy/builder.go](sdk/cliproxy/builder.go)
- [sdk/config/config.go](sdk/config/config.go)

</details>



## Purpose and Scope

This page explains the **dual authentication system** in CLIProxyAPI:

1.  **Request Authentication** (`sdkaccess.Manager`): Validates incoming HTTP requests to the proxy using API keys or Authorization headers [sdk/access/manager.go:10-15]().
2.  **Provider Credential Management** (`coreauth.Manager`): Manages AI provider credentials (OAuth tokens, API keys, service accounts) and orchestrates request routing to available upstream accounts [sdk/cliproxy/auth/conductor.go:129-166]().

The system separates concerns: the proxy's own API key authentication is independent from managing credentials for upstream AI providers. This architecture enables multi-account management, credential rotation, and intelligent failover across provider accounts.

---

## Authentication Architecture Overview

The authentication system consists of **two independent layers**:

### Layer 1: Request Authentication (sdkaccess.Manager)

Validates that incoming HTTP requests are authorized to use the proxy. The `sdkaccess.Manager` chains multiple `Provider` implementations [sdk/access/manager.go:21-25](). The primary built-in provider is `config-api-key`, which checks keys defined in the configuration file [docs/sdk-access.md:56-61]().

Supported credential sources include:
*   `Authorization: Bearer <key>` header
*   `X-API-Key` or `X-Goog-Api-Key` headers
*   `?key=` or `?auth_token=` query parameters [docs/sdk-access.md:61-62]().

### Layer 2: Provider Credential Management (coreauth.Manager)

Manages credentials for upstream AI providers. After request authentication passes, this layer:
1.  **Selects** an available credential using a `Selector` strategy (Round-Robin or Fill-First) [sdk/cliproxy/auth/conductor.go:170-179]().
2.  **Applies Model Aliasing** to resolve requested names to upstream provider names [sdk/cliproxy/auth/conductor.go:146-151]().
3.  **Executes** the request via a provider-specific `ProviderExecutor` [sdk/cliproxy/auth/conductor.go:27-43]().
4.  **Records Results** to update credential state, including quota tracking and cooldowns [sdk/cliproxy/auth/conductor.go:87-100]().

**Diagram: Dual Authentication System Architecture**

```mermaid
graph TB
    subgraph "Layer 1: Request Authentication"
        IncomingReq["Incoming HTTP Request"]
        HandlerPkg["sdk/api/handlers/handlers.go"]
        AccessManager["sdkaccess.Manager<br/>sdk/access/manager.go"]
    end
    
    subgraph "Layer 2: Provider Credential Management"
        CoreManager["coreauth.Manager<br/>sdk/cliproxy/auth/conductor.go"]
        AuthStore["In-Memory Auths<br/>map[string]*Auth"]
        Selector["Selector Interface<br/>RoundRobin/FillFirst"]
        ModelAlias["Model Alias Tables<br/>apiKeyModelAlias"]
    end
    
    subgraph "Provider Execution"
        Executors["ProviderExecutor Interface<br/>sdk/cliproxy/auth/conductor.go"]
        Providers["Upstream AI APIs<br/>(Gemini, Claude, OpenAI)"]
    end
    
    subgraph "Credential Sources"
        Builder["cliproxy.Builder<br/>sdk/cliproxy/builder.go"]
        FileSystem["Auth Storage<br/>sdk/auth/filestore.go"]
        ConfigAccess["configaccess.Register<br/>internal/access/reconcile.go"]
    end
    
    IncomingReq --> HandlerPkg
    HandlerPkg --> AccessManager
    AccessManager -->|"Authorized Result"| CoreManager
    
    CoreManager --> AuthStore
    CoreManager --> Selector
    CoreManager --> ModelAlias
    Selector -->|"Pick *Auth"| Executors
    Executors --> Providers
    
    FileSystem --> Builder
    Builder -->|"Initialize"| CoreManager
    ConfigAccess -->|"SetProviders"| AccessManager
```

**Sources:** [sdk/access/manager.go:21-40](), [sdk/cliproxy/auth/conductor.go:129-166](), [sdk/cliproxy/builder.go:195-202](), [sdk/api/handlers/handlers.go:1-10]()

---

## Core Components

### coreauth.Manager

The `coreauth.Manager` is the central orchestrator for provider credential management [sdk/cliproxy/auth/conductor.go:129-166]().

**Key Responsibilities:**

| Responsibility | Description | Key Methods / Fields |
| :--- | :--- | :--- |
| **Credential Registry** | Maintains in-memory collection of `Auth` entries | `Register()`, `Update()`, `auths` map |
| **Selection** | Routes requests using pluggable strategies | `Pick()` (via `Selector`) |
| **Auto-Refresh** | Periodically refreshes expiring OAuth tokens | `Refresh()` (via `ProviderExecutor`) |
| **Quota Management** | Tracks 429 errors and manages cooldowns | `quotaBackoffBase`, `quotaBackoffMax` |
| **Model Aliasing** | Maps user-facing aliases to upstream model names | `oauthModelAlias`, `apiKeyModelAlias` |

**Sources:** [sdk/cliproxy/auth/conductor.go:129-191](), [sdk/cliproxy/auth/conductor.go:61-68]().

### Auth Structure

The `coreauth.Auth` structure encapsulates the runtime state and metadata for a single provider credential [sdk/cliproxy/auth/types.go:45-48]().

| Field | Type | Purpose |
| :--- | :--- | :--- |
| `ID` | string | Unique identifier across restarts [sdk/cliproxy/auth/types.go:48]() |
| `Provider` | string | Upstream provider key (e.g. "gemini", "claude") [sdk/cliproxy/auth/types.go:52]() |
| `Attributes` | map[string]string | Immutable configuration (API keys, project IDs) [sdk/cliproxy/auth/types.go:72]() |
| `Metadata` | map[string]any | Mutable state (OAuth tokens, refresh tokens) [sdk/cliproxy/auth/types.go:74]() |
| `Quota` | QuotaState | Tracks recent rate limit violations [sdk/cliproxy/auth/types.go:76]() |
| `ModelStates` | map[string]*ModelState | Tracks availability per-model for this credential [sdk/cliproxy/auth/types.go:89-90]() |

**Sources:** [sdk/cliproxy/auth/types.go:45-96]().

---

## Credential Lifecycle and Cooldowns

### Quota and Cooldown Logic

When a provider returns a rate limit error (HTTP 429), the manager updates the `QuotaState` [sdk/cliproxy/auth/types.go:98-108]().

*   **Exponential Backoff**: The cooldown duration increases based on `BackoffLevel` [sdk/cliproxy/auth/types.go:107]().
*   **Base Interval**: Defaults to 1 second [sdk/cliproxy/auth/conductor.go:66]().
*   **Maximum Interval**: Capped at 30 minutes [sdk/cliproxy/auth/conductor.go:67]().
*   **Global Disable**: Cooldowns can be disabled globally for testing or specific workflows [sdk/cliproxy/auth/conductor.go:70-75]().

**Sources:** [sdk/cliproxy/auth/conductor.go:61-84](), [sdk/cliproxy/auth/types.go:98-108]().

### Refresh Mechanism

The manager runs a background scheduler to handle token refreshes [sdk/cliproxy/auth/conductor.go:137]().
*   **Interval**: Checks every 5 seconds [sdk/cliproxy/auth/conductor.go:62]().
*   **Concurrency**: Limits simultaneous refreshes to 16 to avoid provider-side rate limits [sdk/cliproxy/auth/conductor.go:63]().
*   **Failure Backoff**: If a refresh fails, it waits 5 minutes before retrying [sdk/cliproxy/auth/conductor.go:65]().

**Sources:** [sdk/cliproxy/auth/conductor.go:61-68]().

---

## Credential Selection Strategies

The `Selector` interface determines which credential to pick from a list of valid candidates [sdk/cliproxy/auth/conductor.go:102-105]().

### RoundRobinSelector
Cycles through available credentials in a deterministic order [sdk/cliproxy/auth/selector.go:20-25]().
*   Maintains per-model cursors to ensure even distribution [sdk/cliproxy/auth/selector.go:23]().
*   Supports priority buckets; it will only select from the highest priority group available [sdk/cliproxy/auth/selector.go:194-212]().

### FillFirstSelector
Selects the first available credential after sorting by ID [sdk/cliproxy/auth/selector.go:27-30]().
*   Useful for "burning" through one account's daily/monthly quota before moving to the next [sdk/cliproxy/auth/selector.go:28-29]().

### Blocking Logic
An auth is excluded from selection if `isAuthBlockedForModel` returns true [sdk/cliproxy/auth/selector.go:198]().
*   **Cooldown**: Model is currently in a backoff period [sdk/cliproxy/auth/selector.go:36]().
*   **Disabled**: The operator explicitly disabled the credential [sdk/cliproxy/auth/selector.go:37]().

**Sources:** [sdk/cliproxy/auth/selector.go:20-40](), [sdk/cliproxy/auth/selector.go:194-212](), [sdk/cliproxy/auth/selector.go:255-265]().

---

## Model Aliasing and Pools

The `coreauth.Manager` handles two types of model mapping during the authentication/selection phase:

1.  **OAuth Model Aliases**: Global mappings (e.g., mapping a generic "claude-3" to a specific version) [sdk/cliproxy/auth/conductor.go:146-147]().
2.  **API Key Model Pools**: Allows an API key to represent a pool of upstream models. The manager rotates through the pool using `modelPoolOffsets` [sdk/cliproxy/auth/conductor.go:153-154]().

**Diagram: Model Resolution Flow**

```mermaid
graph LR
    UserReq["User Request<br/>(Model: 'my-alias')"]
    AliasTable["apiKeyModelAlias<br/>(Table: 'my-alias' -> 'gpt-4o')"]
    Selector["Selector.Pick"]
    Upstream["ProviderExecutor.Execute<br/>(Model: 'gpt-4o')"]
    
    UserReq --> AliasTable
    AliasTable -->|"Resolved Model"| Selector
    Selector -->|"Selected Auth"| Upstream
```

**Sources:** [sdk/cliproxy/auth/conductor.go:146-154](), [sdk/cliproxy/auth/openai_compat_pool_test.go:161-170]().

---

## Request Execution Metadata

During the transition from the HTTP handler to the `coreauth.Manager`, metadata is injected into the context to influence selection [sdk/api/handlers/handlers.go:188-191]().

*   **Pinned Auth**: Clients can request a specific credential via ID using `WithPinnedAuthID` [sdk/api/handlers/handlers.go:59-69]().
*   **Execution Sessions**: Long-lived sessions (like WebSockets) are tagged with an ID to allow executors to release resources via `ExecutionSessionCloser` [sdk/api/handlers/handlers.go:82-92](), [sdk/cliproxy/auth/conductor.go:45-48]().
*   **Idempotency**: A unique key is generated (or forwarded from headers) to correlate retries [sdk/api/handlers/handlers.go:189-199]().

**Sources:** [sdk/api/handlers/handlers.go:55-92](), [sdk/api/handlers/handlers.go:188-212](), [sdk/cliproxy/auth/conductor.go:45-48]().

---

# Page: Provider Executor System

# Provider Executor System

<details>
<summary>Relevant source files</summary>

The following files were used as context for generating this wiki page:

- [internal/config/claude_header_defaults_test.go](internal/config/claude_header_defaults_test.go)
- [internal/runtime/executor/aistudio_executor.go](internal/runtime/executor/aistudio_executor.go)
- [internal/runtime/executor/antigravity_executor.go](internal/runtime/executor/antigravity_executor.go)
- [internal/runtime/executor/claude_device_profile.go](internal/runtime/executor/claude_device_profile.go)
- [internal/runtime/executor/claude_executor.go](internal/runtime/executor/claude_executor.go)
- [internal/runtime/executor/claude_executor_test.go](internal/runtime/executor/claude_executor_test.go)
- [internal/runtime/executor/codex_executor.go](internal/runtime/executor/codex_executor.go)
- [internal/runtime/executor/gemini_cli_executor.go](internal/runtime/executor/gemini_cli_executor.go)
- [internal/runtime/executor/gemini_executor.go](internal/runtime/executor/gemini_executor.go)
- [internal/runtime/executor/gemini_vertex_executor.go](internal/runtime/executor/gemini_vertex_executor.go)
- [internal/runtime/executor/iflow_executor.go](internal/runtime/executor/iflow_executor.go)
- [internal/runtime/executor/openai_compat_executor.go](internal/runtime/executor/openai_compat_executor.go)
- [internal/runtime/executor/qwen_executor.go](internal/runtime/executor/qwen_executor.go)
- [internal/thinking/apply_user_defined_test.go](internal/thinking/apply_user_defined_test.go)
- [sdk/api/handlers/handlers.go](sdk/api/handlers/handlers.go)
- [sdk/cliproxy/auth/conductor.go](sdk/cliproxy/auth/conductor.go)
- [sdk/cliproxy/auth/conductor_overrides_test.go](sdk/cliproxy/auth/conductor_overrides_test.go)
- [sdk/cliproxy/auth/openai_compat_pool_test.go](sdk/cliproxy/auth/openai_compat_pool_test.go)

</details>



## Purpose and Scope

The Provider Executor System implements the abstraction layer that enables CLIProxyAPI to communicate with multiple AI service providers through a unified interface. Each provider executor handles provider-specific authentication, request translation, HTTP transport, streaming, token counting, and credential refresh. This system sits between the authentication manager ([3.3]()) and the request translation system ([3.5]()), orchestrating the actual API calls to upstream providers.

For information about how executors are selected and rotated during request processing, see Model Registry and Selection ([3.6]()). For authentication credential management, see Authentication and Credential Management ([3.3]()).

---

## ProviderExecutor Interface

All provider executors implement the `auth.ProviderExecutor` interface defined in the SDK package. This interface standardizes how the authentication manager and request handlers interact with different AI service providers:

[sdk/cliproxy/auth/conductor.go:28-43]()
```go
type ProviderExecutor interface {
	// Identifier returns the provider key handled by this executor.
	Identifier() string
	// Execute handles non-streaming execution and returns the provider response payload.
	Execute(ctx context.Context, auth *Auth, req cliproxyexecutor.Request, opts cliproxyexecutor.Options) (cliproxyexecutor.Response, error)
	// ExecuteStream handles streaming execution and returns a StreamResult containing
	// upstream headers and a channel of provider chunks.
	ExecuteStream(ctx context.Context, auth *Auth, req cliproxyexecutor.Request, opts cliproxyexecutor.Options) (*cliproxyexecutor.StreamResult, error)
	// Refresh attempts to refresh provider credentials and returns the updated auth state.
	Refresh(ctx context.Context, auth *Auth) (*Auth, error)
	// CountTokens returns the token count for the given request.
	CountTokens(ctx context.Context, auth *Auth, req cliproxyexecutor.Request, opts cliproxyexecutor.Options) (cliproxyexecutor.Response, error)
	// HttpRequest injects provider credentials into the supplied HTTP request and executes it.
	// Callers must close the response body when non-nil.
	HttpRequest(ctx context.Context, auth *Auth, req *http.Request) (*http.Response, error)
}
```

**Method Responsibilities:**

| Method | Purpose | Return Value |
|--------|---------|--------------|
| `Identifier()` | Returns provider key for routing (e.g., "gemini", "claude", "codex") | Provider string identifier |
| `Execute()` | Performs non-streaming requests | `cliproxyexecutor.Response` or error |
| `ExecuteStream()` | Performs streaming requests via Server-Sent Events or WebSocket | `*cliproxyexecutor.StreamResult` or error |
| `CountTokens()` | Counts tokens in request payload | `cliproxyexecutor.Response` with token count or error |
| `Refresh()` | Refreshes OAuth tokens or service account credentials | Updated `*cliproxyauth.Auth` object or error |
| `HttpRequest()` | Low-level method to inject credentials and proxy raw requests | `*http.Response` or error |

**Sources:** [sdk/cliproxy/auth/conductor.go:28-43]()

---

## Executor Implementations

### Code Entity Space to Provider Mapping

This diagram maps the internal Go structs (Code Entities) to the Natural Language providers they serve, illustrating the specialized logic contained within each.

```mermaid
graph LR
    subgraph "Natural Language Space"
        Anthropic["Anthropic Claude"]
        GoogleGemini["Google Gemini"]
        OpenAI["OpenAI / Codex"]
        Alibaba["Qwen Code"]
        GoogleDeepmind["Antigravity"]
    end

    subgraph "Code Entity Space"
        CE_Claude["ClaudeExecutor<br/>(claude_executor.go)"]
        CE_Gemini["GeminiExecutor<br/>(gemini_executor.go)"]
        CE_Codex["CodexExecutor<br/>(codex_executor.go)"]
        CE_Qwen["QwenExecutor<br/>(qwen_executor.go)"]
        CE_Anti["AntigravityExecutor<br/>(antigravity_executor.go)"]
    end

    Anthropic --- CE_Claude
    GoogleGemini --- CE_Gemini
    OpenAI --- CE_Codex
    Alibaba --- CE_Qwen
    GoogleDeepmind --- CE_Anti
```

**Sources:** [internal/runtime/executor/claude_executor.go:40-41](), [internal/runtime/executor/gemini_executor.go:40-43](), [internal/runtime/executor/codex_executor.go:39-41](), [internal/runtime/executor/qwen_executor.go:173-175](), [internal/runtime/executor/antigravity_executor.go:58-61]()

### Executor Registry and Authentication

| Executor | Identifier | Authentication Strategy | Primary File |
|----------|-----------|-------------------------|--------------|
| `GeminiExecutor` | `"gemini"` | API Key or OAuth Bearer | [internal/runtime/executor/gemini_executor.go:37-43]() |
| `GeminiCLIExecutor` | `"gemini-cli"` | Cloud Code Assist OAuth | [internal/runtime/executor/gemini_cli_executor.go:47-50]() |
| `ClaudeExecutor` | `"claude"` | API Key or Anthropic OAuth | [internal/runtime/executor/claude_executor.go:38-42]() |
| `CodexExecutor` | `"codex"` | OpenAI Codex OAuth | [internal/runtime/executor/codex_executor.go:37-41]() |
| `AntigravityExecutor`| `"antigravity"`| Google Internal OAuth | [internal/runtime/executor/antigravity_executor.go:58-61]() |
| `QwenExecutor` | `"qwen"` | Qwen Portal OAuth | [internal/runtime/executor/qwen_executor.go:171-175]() |
| `IFlowExecutor` | `"iflow"` | iFlow API Key / OAuth | [internal/runtime/executor/iflow_executor.go:34-37]() |
| `AIStudioExecutor` | `"aistudio"` | WebSocket Relay | [internal/runtime/executor/aistudio_executor.go:26-31]() |
| `OpenAICompatExecutor`| Provider-specific | Generic Bearer Token | [internal/runtime/executor/openai_compat_executor.go:23-29]() |

---

## Execution Flow

### Request Lifecycle Diagram

This diagram bridges the conceptual "Request Flow" to specific function calls and entities in the codebase.

```mermaid
sequenceDiagram
    participant M as "Manager (conductor.go)"
    participant E as "ClaudeExecutor (claude_executor.go)"
    participant T as "TranslateRequest (translator.go)"
    participant TH as "ApplyThinking (thinking.go)"
    participant R as "recordAPIRequest (executor.go)"
    participant H as "http.Client"

    M->>E: Execute(ctx, auth, req, opts)
    E->>T: TranslateRequest(from, to, model, payload, stream)
    T-->>E: translatedBody
    E->>TH: ApplyThinking(translatedBody, model, ...)
    TH-->>E: thinkingBody
    E->>E: applyCloaking(ctx, cfg, auth, thinkingBody, ...)
    E->>R: recordAPIRequest(ctx, cfg, logEntry)
    E->>H: Do(httpReq)
    H-->>E: httpResp
    E-->>M: cliproxyexecutor.Response
```

**Sources:** [internal/runtime/executor/claude_executor.go:98-188](), [sdk/cliproxy/auth/conductor.go:32-35]()

### Non-Streaming Request Flow

The `Execute` method handles the lifecycle of a single non-streaming request. It performs the following steps:
1. **Usage Reporting:** Initializes a `newUsageReporter` to track token consumption [internal/runtime/executor/claude_executor.go:109]().
2. **Translation:** Converts the incoming payload (e.g., OpenAI format) to the provider's native format (e.g., Claude Messages) using `sdktranslator.TranslateRequest` [internal/runtime/executor/claude_executor.go:120-121]().
3. **Thinking Injection:** Applies reasoning/thinking parameters via `thinking.ApplyThinking` [internal/runtime/executor/claude_executor.go:124]().
4. **Provider-Specific Logic:** Applies cloaking, cache control optimization, or model-specific token limits [internal/runtime/executor/claude_executor.go:131-151]().
5. **Authentication:** Injects credentials via `PrepareRequest` or `applyClaudeHeaders` [internal/runtime/executor/claude_executor.go:168]().
6. **Execution:** Dispatches the request using a proxy-aware HTTP client [internal/runtime/executor/claude_executor.go:187-188]().

**Sources:** [internal/runtime/executor/claude_executor.go:98-192](), [internal/runtime/executor/gemini_executor.go:105-185]()

---

## Authentication and Transport Strategies

### HTTP/1.1 Enforcement (Antigravity)

The `AntigravityExecutor` forces the use of HTTP/1.1 to perfectly mimic specific client environments (e.g., Node.js defaults) and prevent implicit HTTP/2 upgrades that might lead to fingerprinting.

[internal/runtime/executor/antigravity_executor.go:82-99]()
```go
func cloneTransportWithHTTP11(base *http.Transport) *http.Transport {
	if base == nil { return nil }
	clone := base.Clone()
	clone.ForceAttemptHTTP2 = false
	clone.TLSNextProto = make(map[string]func(authority string, c *tls.Conn) http.RoundTripper)
	if clone.TLSClientConfig == nil {
		clone.TLSClientConfig = &tls.Config{}
	} else {
		clone.TLSClientConfig = clone.TLSClientConfig.Clone()
	}
	clone.TLSClientConfig.NextProtos = []string{"http/1.1"}
	return clone
}
```

### Rate Limiting and Quota Handling (Qwen)

The `QwenExecutor` includes a specialized sliding-window rate limiter (60 RPM) and logic to detect daily quota exhaustion.

- **Rate Limiting:** `checkQwenRateLimit` tracks request timestamps per `authID` [internal/runtime/executor/qwen_executor.go:70-120]().
- **Quota Detection:** `isQwenQuotaError` parses error bodies for strings like "insufficient_quota" [internal/runtime/executor/qwen_executor.go:124-144]().
- **Cooldown:** When a quota error is detected, `wrapQwenError` calculates the duration until Beijing midnight (UTC+8) to set a `retryAfter` hint [internal/runtime/executor/qwen_executor.go:149-169]().

**Sources:** [internal/runtime/executor/qwen_executor.go:70-169](), [internal/runtime/executor/antigravity_executor.go:82-128]()

---

## Provider-Specific Implementations

### Claude: Fingerprinting and Cache Control

The `ClaudeExecutor` manages complex Anthropic-specific requirements:
- **Header Fingerprinting:** baseline fingerprints (User-Agent, Stainless-Package-Version) are applied to avoid detection [internal/runtime/executor/claude_executor_test.go:66-106]().
- **Cache Control:** Enforces Anthropic's limit of 4 `cache_control` blocks and normalizes TTL values [internal/runtime/executor/claude_executor.go:145-152]().
- **Beta Headers:** Automatically extracts beta features from the request body and moves them to `anthropic-beta` headers [internal/runtime/executor/claude_executor.go:155-156]().

### AI Studio: WebSocket Relay

The `AIStudioExecutor` does not use standard HTTP transports. Instead, it routes all requests through a `wsrelay.Manager`, which proxies traffic over persistent WebSockets to remote execution environments.

[internal/runtime/executor/aistudio_executor.go:83-89]()
```go
	wsReq := &wsrelay.HTTPRequest{
		Method:  httpReq.Method,
		URL:     httpReq.URL.String(),
		Headers: httpReq.Header.Clone(),
		Body:    body,
	}
	wsResp, errRelay := e.relay.NonStream(ctx, auth.ID, wsReq)
```

**Sources:** [internal/runtime/executor/claude_executor.go:145-156](), [internal/runtime/executor/aistudio_executor.go:26-44](), [internal/runtime/executor/aistudio_executor.go:83-89]()

---

## Error Handling and Logging

### Standardized Error Responses

The system uses `BuildErrorResponseBody` to ensure that errors from various providers are returned to the client in an OpenAI-compatible JSON format, mapping provider status codes to standard error types (`rate_limit_error`, `authentication_error`, etc.).

[sdk/api/handlers/handlers.go:96-130]()
```go
func BuildErrorResponseBody(status int, errText string) []byte {
    // ... logic to map status codes to OpenAI types ...
	errType := "invalid_request_error"
	switch status {
	case http.StatusUnauthorized:
		errType = "authentication_error"
	case http.StatusTooManyRequests:
		errType = "rate_limit_error"
    // ...
```

### Telemetry and Auditing

Every executor call triggers two key logging events:
1. **`recordAPIRequest`**: Logs the full upstream URL, method, headers, and body [internal/runtime/executor/claude_executor.go:175-185]().
2. **`recordAPIResponseMetadata`**: Logs the resulting status code and upstream headers [internal/runtime/executor/claude_executor.go:193]().

**Sources:** [sdk/api/handlers/handlers.go:96-142](), [internal/runtime/executor/claude_executor.go:175-193]()

---

# Page: Request Translation System

# Request Translation System

<details>
<summary>Relevant source files</summary>

The following files were used as context for generating this wiki page:

- [examples/translator/main.go](examples/translator/main.go)
- [internal/cache/signature_cache.go](internal/cache/signature_cache.go)
- [internal/cache/signature_cache_test.go](internal/cache/signature_cache_test.go)
- [internal/translator/antigravity/claude/antigravity_claude_request.go](internal/translator/antigravity/claude/antigravity_claude_request.go)
- [internal/translator/antigravity/claude/antigravity_claude_request_test.go](internal/translator/antigravity/claude/antigravity_claude_request_test.go)
- [internal/translator/antigravity/claude/antigravity_claude_response.go](internal/translator/antigravity/claude/antigravity_claude_response.go)
- [internal/translator/antigravity/claude/antigravity_claude_response_test.go](internal/translator/antigravity/claude/antigravity_claude_response_test.go)
- [internal/translator/antigravity/openai/chat-completions/antigravity_openai_request.go](internal/translator/antigravity/openai/chat-completions/antigravity_openai_request.go)
- [internal/translator/claude/gemini/claude_gemini_request.go](internal/translator/claude/gemini/claude_gemini_request.go)
- [internal/translator/claude/openai/chat-completions/claude_openai_request.go](internal/translator/claude/openai/chat-completions/claude_openai_request.go)
- [internal/translator/claude/openai/chat-completions/claude_openai_request_test.go](internal/translator/claude/openai/chat-completions/claude_openai_request_test.go)
- [internal/translator/claude/openai/responses/claude_openai-responses_request.go](internal/translator/claude/openai/responses/claude_openai-responses_request.go)
- [internal/translator/codex/claude/codex_claude_request.go](internal/translator/codex/claude/codex_claude_request.go)
- [internal/translator/codex/claude/codex_claude_request_test.go](internal/translator/codex/claude/codex_claude_request_test.go)
- [internal/translator/codex/gemini/codex_gemini_request.go](internal/translator/codex/gemini/codex_gemini_request.go)
- [internal/translator/gemini-cli/claude/gemini-cli_claude_request.go](internal/translator/gemini-cli/claude/gemini-cli_claude_request.go)
- [internal/translator/gemini-cli/gemini/gemini-cli_gemini_response.go](internal/translator/gemini-cli/gemini/gemini-cli_gemini_response.go)
- [internal/translator/gemini-cli/gemini/init.go](internal/translator/gemini-cli/gemini/init.go)
- [internal/translator/gemini-cli/openai/chat-completions/gemini-cli_openai_request.go](internal/translator/gemini-cli/openai/chat-completions/gemini-cli_openai_request.go)
- [internal/translator/gemini/claude/gemini_claude_request.go](internal/translator/gemini/claude/gemini_claude_request.go)
- [internal/translator/gemini/openai/chat-completions/gemini_openai_request.go](internal/translator/gemini/openai/chat-completions/gemini_openai_request.go)
- [internal/translator/gemini/openai/responses/gemini_openai-responses_request.go](internal/translator/gemini/openai/responses/gemini_openai-responses_request.go)
- [internal/translator/openai/claude/openai_claude_request.go](internal/translator/openai/claude/openai_claude_request.go)
- [internal/translator/openai/claude/openai_claude_request_test.go](internal/translator/openai/claude/openai_claude_request_test.go)
- [internal/translator/openai/gemini/openai_gemini_request.go](internal/translator/openai/gemini/openai_gemini_request.go)
- [sdk/translator/builtin/builtin.go](sdk/translator/builtin/builtin.go)
- [sdk/translator/formats.go](sdk/translator/formats.go)
- [sdk/translator/helpers.go](sdk/translator/helpers.go)

</details>



## Purpose and Scope

The Request Translation System is responsible for converting API requests and responses between different AI provider formats. It enables the CLI Proxy API to accept requests in one format (e.g., OpenAI Chat Completions) and translate them to the format expected by the target provider's executor (e.g., Gemini API, Claude Code API, Codex API, or Antigravity API). This system is the core component that enables multi-provider compatibility with a unified client-facing interface.

This page covers the translation layer architecture, individual translator implementations, format mappings, and specialized features like thinking block handling and signature caching.

---

## Translation Architecture Overview

The translation system implements a bidirectional conversion layer between API formats. Translators are stateless functions that transform JSON payloads using `gjson` for parsing and `sjson` for construction, ensuring high performance with zero reflection overhead.

### Translation Mapping Graph

The following diagram illustrates the translation paths between client-facing formats and internal provider formats.

```mermaid
graph TB
    subgraph ClientFormats["Client Formats"]
        OAI["OpenAI Chat Completions"]
        CLA["Claude Messages API"]
        GEM["Gemini API"]
        OAIRESP["OpenAI Responses API"]
    end
    
    subgraph TranslationLayer["Translation Layer (internal/translator)"]
        subgraph RequestTranslators["Request Translators"]
            OAI2GEM["ConvertOpenAIRequestToGemini()<br/>gemini/openai/chat-completions/"]
            OAI2GEMCLI["ConvertOpenAIRequestToGeminiCLI()<br/>gemini-cli/openai/chat-completions/"]
            OAI2ANTI["ConvertOpenAIRequestToAntigravity()<br/>antigravity/openai/chat-completions/"]
            CLA2ANTI["ConvertClaudeRequestToAntigravity()<br/>antigravity/claude/"]
            CLA2CODEX["ConvertClaudeRequestToCodex()<br/>codex/claude/"]
            OAIRESP2GEM["ConvertOpenAIResponsesRequestToGemini()<br/>gemini/openai/responses/"]
        end
        
        subgraph ResponseTranslators["Response Translators"]
            ANTI2CLA_STREAM["ConvertAntigravityResponseToClaude()<br/>antigravity/claude/"]
        end
        
        subgraph SupportingSystems["Supporting Systems"]
            SigCache["signatureCache (sync.Map)<br/>internal/cache/signature_cache.go"]
            ThinkingUtil["GetThinkingText()<br/>internal/thinking/thinking.go"]
        end
    end
    
    subgraph ProviderFormats["Provider API Formats"]
        GEMAPI["Gemini API Format<br/>{contents, systemInstruction}"]
        GEMCLIAPI["Gemini CLI Format<br/>{project, model, request}"]
        ANTIAPI["Antigravity API Format<br/>{project, model, request}"]
        CODEXAPI["Codex API Format<br/>{model, instructions, input}"]
    end
    
    OAI --> OAI2GEM --> GEMAPI
    OAI --> OAI2GEMCLI --> GEMCLIAPI
    OAI --> OAI2ANTI --> ANTIAPI
    CLA --> CLA2ANTI --> ANTIAPI
    CLA --> CLA2CODEX --> CODEXAPI
    OAIRESP --> OAIRESP2GEM --> GEMAPI
    
    ANTIAPI --> ANTI2CLA_STREAM --> CLA
    
    CLA2ANTI -.-> SigCache
    ANTI2CLA_STREAM -.-> SigCache
    CLA2CODEX -.-> ThinkingUtil
```

**Sources:**
- [internal/translator/antigravity/claude/antigravity_claude_request.go:38-406]()
- [internal/translator/gemini/openai/chat-completions/gemini_openai_request.go:29-401]()
- [internal/translator/codex/claude/codex_claude_request.go:36-248]()
- [internal/translator/gemini/openai/responses/gemini_openai-responses_request.go:15-419]()
- [internal/cache/signature_cache.go:31-60]()

---

## Format Characteristic Differences

The system manages several distinct API structures, mapping their specific nuances during translation:

| Format | Role Names | System Prompt Location | Tool Field | Thinking Support |
| :--- | :--- | :--- | :--- | :--- |
| **OpenAI** | `system`, `user`, `assistant` | `messages` array | `tools` (parameters) | `reasoning_effort` |
| **Claude** | `user`, `assistant` | Top-level `system` | `tools` (input_schema) | `thinking` blocks |
| **Gemini** | `user`, `model` | `systemInstruction` | `functionDeclarations` | `thinkingConfig` |
| **Codex** | `developer`, `user`, `assistant` | `instructions` / `input` | `tools` | `reasoning` |
| **Antigravity** | `user`, `model` | `request.systemInstruction` | `functionDeclarations` | `thought` parts |

**Sources:**
- [internal/translator/antigravity/claude/antigravity_claude_request.go:86-92]()
- [internal/translator/gemini/openai/chat-completions/gemini_openai_request.go:149-168]()
- [internal/translator/codex/claude/codex_claude_request.go:44-75]()

---

## Request Translators

### Claude → Antigravity Translation
The `ConvertClaudeRequestToAntigravity` function in `internal/translator/antigravity/claude/antigravity_claude_request.go` is the most complex translator. It handles Claude's unique content block format and implements thinking signature management for multi-turn conversations.

**Key Features:**
- **Signature Resolution:** It prioritizes cached signatures via `cache.GetCachedSignature` [internal/translator/antigravity/claude/antigravity_claude_request.go:109-113]() and falls back to client-provided signatures if valid [internal/translator/antigravity/claude/antigravity_claude_request.go:116-131]().
- **Unsigned Block Handling:** Unsigned thinking blocks are dropped entirely to prevent breaking Claude API requirements [internal/translator/antigravity/claude/antigravity_claude_request.go:144-148]().
- **Role Mapping:** Maps Claude's `assistant` role to Gemini's `model` role [internal/translator/antigravity/claude/antigravity_claude_request.go:88-90]().

### OpenAI → Gemini Translation
`ConvertOpenAIRequestToGemini` in `internal/translator/gemini/openai/chat-completions/gemini_openai_request.go` maps OpenAI Chat Completions to the native Gemini API.

**Transformations:**
- **Thinking Config:** Maps OpenAI `reasoning_effort` (auto/low/medium/high) to Gemini `thinkingConfig` (thinkingBudget or thinkingLevel) [internal/translator/gemini/openai/chat-completions/gemini_openai_request.go:44-57]().
- **Generation Config:** Direct mapping of `temperature`, `top_p`, `top_k`, and `n` (candidateCount) [internal/translator/gemini/openai/chat-completions/gemini_openai_request.go:59-75]().
- **Tool Grouping:** Collects tool responses and groups them into a single `user` role content node to satisfy Gemini's API structure [internal/translator/gemini/openai/chat-completions/gemini_openai_request.go:129-141]().

### Claude → Codex Translation
`ConvertClaudeRequestToCodex` in `internal/translator/codex/claude/codex_claude_request.go` transforms Claude requests for the Codex backend.

**Transformations:**
- **System Instructions:** Processes Claude's `system` field and converts it into Codex `developer` role messages [internal/translator/codex/claude/codex_claude_request.go:44-75]().
- **Tool Shortening:** Implements `shortenNameIfNeeded` to handle Codex's strict tool naming requirements [internal/translator/codex/claude/codex_claude_request.go:162]().
- **Thinking Configuration:** Maps Claude `thinking.budget_tokens` to Codex `reasoning` settings [internal/translator/codex/claude/codex_claude_request.go:215-231]().

**Sources:**
- [internal/translator/antigravity/claude/antigravity_claude_request.go:20-38]()
- [internal/translator/gemini/openai/chat-completions/gemini_openai_request.go:19-32]()
- [internal/translator/codex/claude/codex_claude_request.go:18-35]()

---

## Response Translation and State Management

### Antigravity → Claude Streaming
The `ConvertAntigravityResponseToClaude` function in `internal/translator/antigravity/claude/antigravity_claude_response.go` implements a sophisticated state machine to manage streaming Server-Sent Events (SSE).

**State Machine Logic:**
The `Params` struct tracks the current state across chunks [internal/translator/antigravity/claude/antigravity_claude_response.go:29-51]():
- `ResponseType`: 0=none, 1=content, 2=thinking, 3=function [internal/translator/antigravity/claude/antigravity_claude_response.go:31]().
- **Thinking Accumulation:** It uses `CurrentThinkingText` (a `strings.Builder`) to accumulate thinking content across multiple SSE chunks before caching the final signature [internal/translator/antigravity/claude/antigravity_claude_response.go:46]().
- **Signature Caching:** Upon receiving a signature delta, it caches the mapping between the accumulated text and the signature using `cache.CacheSignature` [internal/translator/antigravity/claude/antigravity_claude_response.go:176-180]().

```mermaid
graph TD
    subgraph StateMachine["Streaming State Machine (Params)"]
        S0["ResponseType: 0 (None)"]
        S1["ResponseType: 1 (Content)"]
        S2["ResponseType: 2 (Thinking)"]
        S3["ResponseType: 3 (Function)"]
    end

    Input["Gemini Part (text/thought/functionCall)"] --> Router{Check Part Type}
    Router -- "thought: true" --> S2
    Router -- "text" --> S1
    Router -- "functionCall" --> S3
    
    S2 -- "thoughtSignature received" --> CacheAction["cache.CacheSignature()"]
    S2 -- "Accumulate" --> Builder["Params.CurrentThinkingText"]
    
    S1 --> SSE["Emit message_delta / content_block_delta"]
    S2 --> SSE
    S3 --> SSE
```

**Sources:**
- [internal/translator/antigravity/claude/antigravity_claude_response.go:29-51]()
- [internal/translator/antigravity/claude/antigravity_claude_response.go:56-72]()
- [internal/translator/antigravity/claude/antigravity_claude_response.go:130-183]()

---

## Signature Caching System

The signature cache is critical for multi-turn Claude conversations where thinking blocks must be re-sent with their original signatures.

### Signature Cache Architecture

```mermaid
classDiagram
    class signatureCache {
        <<sync.Map>>
        +Load(modelGroup) groupCache
        +Store(modelGroup, groupCache)
    }
    class groupCache {
        +mu sync.RWMutex
        +entries map[string]SignatureEntry
    }
    class SignatureEntry {
        +Signature string
        +Timestamp time.Time
    }
    signatureCache "1" *-- "many" groupCache : contains
    groupCache "1" *-- "many" SignatureEntry : stores
    
    SignatureCacheOps ..> signatureCache : uses
    class SignatureCacheOps {
        +CacheSignature(modelName, text, sig)
        +GetCachedSignature(modelName, text)
        +HasValidSignature(modelName, sig)
    }
```

**Implementation Details:**
- **Storage:** Uses a `sync.Map` of `groupCache` objects, partitioned by model group (e.g., "claude", "gemini") [internal/cache/signature_cache.go:31-35]().
- **Hashing:** Thinking text is hashed using SHA-256 (truncated to 16 hex chars) to create stable keys for signature lookups [internal/cache/signature_cache.go:43-47]().
- **TTL:** Entries have a 3-hour TTL (`SignatureCacheTTL`), managed by a background cleanup goroutine that runs every 10 minutes [internal/cache/signature_cache.go:22-24](), [internal/cache/signature_cache.go:62-94]().
- **Validation:** `HasValidSignature` enforces a minimum length of 50 characters for real signatures or allows specific sentinels like `skip_thought_signature_validator` [internal/cache/signature_cache.go:181-184]().

**Sources:**
- [internal/cache/signature_cache.go:31-60]()
- [internal/cache/signature_cache.go:96-116]()
- [internal/cache/signature_cache.go:118-166]()
- [internal/cache/signature_cache.go:181-184]()

---

# Page: Model Registry and Capability System

# Model Registry and Capability System

<details>
<summary>Relevant source files</summary>

The following files were used as context for generating this wiki page:

- [internal/config/oauth_model_alias_test.go](internal/config/oauth_model_alias_test.go)
- [internal/registry/model_definitions.go](internal/registry/model_definitions.go)
- [internal/registry/model_registry.go](internal/registry/model_registry.go)
- [internal/registry/model_registry_cache_test.go](internal/registry/model_registry_cache_test.go)
- [internal/registry/model_registry_hook_test.go](internal/registry/model_registry_hook_test.go)
- [internal/registry/model_registry_safety_test.go](internal/registry/model_registry_safety_test.go)
- [internal/registry/model_updater.go](internal/registry/model_updater.go)
- [internal/registry/models/models.json](internal/registry/models/models.json)
- [internal/util/claude_model.go](internal/util/claude_model.go)
- [internal/util/claude_model_test.go](internal/util/claude_model_test.go)
- [internal/watcher/diff/oauth_model_alias.go](internal/watcher/diff/oauth_model_alias.go)
- [sdk/cliproxy/model_registry.go](sdk/cliproxy/model_registry.go)

</details>



## Purpose and Scope

The Model Registry and Capability System is the central metadata repository for all AI models supported by CLIProxyAPI. It manages model definitions, including capability metadata such as **thinking support** (reasoning budgets and levels), token limits, and modality support. The system provides a dynamic registry that tracks model availability based on active client registrations and quota status, ensuring that requests are only routed to functional providers.

This system facilitates:
- **Static Metadata**: Pre-defined capabilities for known models (Claude, Gemini, etc.) loaded from an embedded JSON.
- **Dynamic Tracking**: Real-time availability based on connected clients and quota limits.
- **Capability Normalization**: Providing standardized thinking/reasoning metadata used by the translation system to map budgets across different providers.
- **Hot-Updates**: Periodic background refreshing of the model catalog from remote sources (GitHub/CDN) without service restarts.

---

## Architecture and Data Flow

The registry operates as a multi-layered system combining embedded defaults, remote updates, and a runtime state manager.

### System Components and Code Entities

```mermaid
graph TB
    subgraph "Data Sources"
        Embed["models.json (Embedded)"]
        Remote["GitHub/CDN (Remote)"]
        Config["config.yaml (UserDefined)"]
    end

    subgraph "Registry Core [internal/registry]"
        Catalog["modelsCatalogStore"]
        GlobalReg["ModelRegistry (Global)"]
        Updater["ModelUpdater"]
    end

    subgraph "Code Entities"
        MInfo["ModelInfo struct"]
        MReg["ModelRegistration struct"]
        TSupp["ThinkingSupport struct"]
    end

    Embed -->|"init()"| Catalog
    Remote -->|"fetchModelsFromRemote()"| Updater
    Updater -->|"tryRefreshModels()"| Catalog
    
    Catalog -->|"LookupModelInfo()"| GlobalReg
    Config -->|"RegisterClient()"| GlobalReg

    GlobalReg -->|"GetAvailableModels()"| API["/v1/models"]
    GlobalReg -->|"ClientSupportsModel()"| Executor["Provider Executor"]

    MInfo --- TSupp
    MReg --- MInfo
```

**Sources:** [internal/registry/model_registry.go:19-128](), [internal/registry/model_updater.go:22-35](), [internal/registry/model_definitions.go:10-24]()

---

## Model Metadata Schema

The core data structure is the `ModelInfo` struct, which encapsulates the capabilities of a specific model version.

### ModelInfo Structure
The `ModelInfo` struct mirrors the OpenAI models API while adding provider-specific extensions for advanced features like internal reasoning.

| Field | Type | Description |
| :--- | :--- | :--- |
| `ID` | `string` | Unique identifier (e.g., `claude-3-7-sonnet-20250219`). |
| `Type` | `string` | Provider category (e.g., `claude`, `gemini`, `qwen`). |
| `ContextLength` | `int` | Maximum context window size. |
| `MaxCompletionTokens` | `int` | Maximum allowed output tokens. |
| `Thinking` | `*ThinkingSupport` | Metadata for internal reasoning/thinking budgets. |
| `UserDefined` | `bool` | Flag for models added via user configuration; bypasses some validations. |

**Sources:** [internal/registry/model_registry.go:19-63]()

### Thinking and Capability Metadata
The `ThinkingSupport` struct defines how a model handles reasoning. This is critical for the "Thinking System" to normalize requests between providers (e.g., converting Gemini's token budget to Claude's thinking levels).

| Capability Field | Description |
| :--- | :--- |
| `Min` / `Max` | Inclusive range for provider-native token units (e.g., 1024 to 128000). |
| `ZeroAllowed` | Whether the model allows disabling thinking (0 tokens). |
| `DynamicAllowed` | Whether `-1` is supported for automatic budget allocation. |
| `Levels` | Discrete effort strings (e.g., `["low", "medium", "high", "max"]`). |

**Sources:** [internal/registry/model_registry.go:72-84](), [internal/registry/models/models.json:12-16](), [internal/registry/models/models.json:67-72]()

---

## Global Registry and Runtime State

The `ModelRegistry` class manages the global state of available models. It uses reference counting to track how many active clients (credentials) support a specific model.

### Key Registry Functions

| Function | Code Entity | Purpose |
| :--- | :--- | :--- |
| **Registration** | `RegisterClient` | Associates a `clientID` with a set of models and increments availability counts. |
| **Deregistration** | `UnregisterClient` | Removes a client and updates model availability counts. |
| **Quota Management** | `SetModelQuotaExceeded` | Temporarily hides a model for a specific client to avoid routing failures. |
| **Lookup** | `LookupModelInfo` | Searches dynamic registry (provider-specific) then static definitions. |
| **Filtering** | `GetAvailableModels` | Returns a snapshot of models currently usable by the proxy, filtered by handler type. |

**Sources:** [internal/registry/model_registry.go:135-210](), [sdk/cliproxy/model_registry.go:12-20]()

### Registry State Diagram

```mermaid
stateDiagram-v2
    [*] --> Idle
    Idle --> Registered : "RegisterClient(clientID, provider, models)"
    Registered --> QuotaExceeded : "SetModelQuotaExceeded(clientID, modelID)"
    QuotaExceeded --> Registered : "CleanupExpiredQuotas() (After cooldown)"
    Registered --> Suspended : "SuspendClientModel(clientID, modelID)"
    Suspended --> Registered : "ResumeClientModel(clientID, modelID)"
    Registered --> Idle : "UnregisterClient(clientID)"
    
    note right of Registered
        "Model is visible in /v1/models"
        "if Count > 0"
    end
```

**Sources:** [internal/registry/model_registry.go:87-102](), [internal/registry/model_registry_safety_test.go:86-111](), [internal/registry/model_registry_cache_test.go:43-54]()

---

## Hot-Update Mechanism

To keep model definitions current without requiring binary updates, CLIProxyAPI implements a background updater that fetches a `models.json` file from remote repositories every 3 hours.

### Update Logic
1. **Startup**: Loads `embeddedModelsJSON` as a baseline [internal/registry/model_updater.go:67-72]().
2. **Fetch**: Attempts to download from `modelsURLs` (GitHub/CDN) with a 30s timeout [internal/registry/model_updater.go:22-25](), [internal/registry/model_updater.go:143-190]().
3. **Validation**: Runs `validateModelsCatalog` to ensure schema integrity [internal/registry/model_updater.go:182-185]().
4. **Comparison**: `detectChangedProviders` identifies which model families (e.g., `claude`, `gemini`) have updates [internal/registry/model_updater.go:195-234]().
5. **Notification**: Invokes `ModelRefreshCallback` to trigger internal re-registrations of active credentials [internal/registry/model_updater.go:138-139]().

**Sources:** [internal/registry/model_updater.go:17-25](), [internal/registry/model_updater.go:67-86](), [internal/registry/model_updater.go:195-234]()

---

## Thread Safety and Caching

The registry is designed for high-concurrency environments:
- **Cloning**: All lookup functions (e.g., `LookupStaticModelInfo`, `GetModelsForClient`) return deep clones of `ModelInfo` to prevent accidental mutation of the global state [internal/registry/model_registry_safety_test.go:8-30]().
- **Snapshot Caching**: `GetAvailableModels` maintains an `availableModelsCache` to avoid re-computing the visible model list for every HTTP request [internal/registry/model_registry.go:148-152]().
- **Invalidation**: Any change to client registration, suspension, or quota status calls `invalidateAvailableModelsCacheLocked` to ensure the next request gets fresh data [internal/registry/model_registry.go:154-159](), [internal/registry/model_registry_cache_test.go:25-54]().

**Sources:** [internal/registry/model_registry.go:148-159](), [internal/registry/model_registry_safety_test.go:8-30](), [internal/registry/model_registry_cache_test.go:25-54]()

---

## Static Model Accessors

The system provides provider-specific accessors for static definitions. These are used during the initialization of provider executors to determine default capabilities.

| Accessor | Channel / Provider |
| :--- | :--- |
| `GetClaudeModels()` | Anthropic Claude |
| `GetGeminiModels()` | Google Gemini API |
| `GetGeminiVertexModels()` | Google Cloud Vertex AI |
| `GetAIStudioModels()` | Google AI Studio |
| `GetCodexProModels()` | OpenAI Codex (Pro Tier) |
| `GetKimiModels()` | Moonshot AI (Kimi) |
| `GetQwenModels()` | Alibaba Qwen |

**Sources:** [internal/registry/model_definitions.go:26-89](), [internal/registry/model_definitions.go:117-143]()

---

# Page: Hot Reload and Configuration Updates

# Hot Reload and Configuration Updates

<details>
<summary>Relevant source files</summary>

The following files were used as context for generating this wiki page:

- [config.example.yaml](config.example.yaml)
- [internal/api/handlers/management/config_basic.go](internal/api/handlers/management/config_basic.go)
- [internal/api/handlers/management/config_lists.go](internal/api/handlers/management/config_lists.go)
- [internal/api/server.go](internal/api/server.go)
- [internal/config/config.go](internal/config/config.go)
- [internal/managementasset/updater.go](internal/managementasset/updater.go)
- [internal/watcher/clients.go](internal/watcher/clients.go)
- [internal/watcher/diff/auth_diff.go](internal/watcher/diff/auth_diff.go)
- [internal/watcher/diff/config_diff.go](internal/watcher/diff/config_diff.go)
- [internal/watcher/diff/config_diff_test.go](internal/watcher/diff/config_diff_test.go)
- [internal/watcher/diff/model_hash.go](internal/watcher/diff/model_hash.go)
- [internal/watcher/diff/model_hash_test.go](internal/watcher/diff/model_hash_test.go)
- [internal/watcher/diff/models_summary.go](internal/watcher/diff/models_summary.go)
- [internal/watcher/diff/oauth_excluded.go](internal/watcher/diff/oauth_excluded.go)
- [internal/watcher/diff/oauth_excluded_test.go](internal/watcher/diff/oauth_excluded_test.go)
- [internal/watcher/diff/openai_compat.go](internal/watcher/diff/openai_compat.go)
- [internal/watcher/diff/openai_compat_test.go](internal/watcher/diff/openai_compat_test.go)
- [internal/watcher/dispatcher.go](internal/watcher/dispatcher.go)
- [internal/watcher/events.go](internal/watcher/events.go)
- [internal/watcher/watcher.go](internal/watcher/watcher.go)
- [internal/watcher/watcher_test.go](internal/watcher/watcher_test.go)
- [sdk/cliproxy/service.go](sdk/cliproxy/service.go)
- [test/amp_management_test.go](test/amp_management_test.go)

</details>



This page explains how CLIProxyAPI detects changes to `config.yaml` and auth credential files, propagates those changes to the running server, and updates live state without requiring a restart.

For information about the auth credential lifecycle and token storage, see [3.3](). For management API endpoints that write config changes, see [4.4](). For the service startup sequence that initializes the watcher, see [3.1]().

---

## Overview

CLIProxyAPI uses two complementary hot-reload paths:

1.  **Config file watch**: `watcher.Watcher` monitors `config.yaml` with `fsnotify`. On change, a debounced reload re-parses the file and calls a callback that propagates the new config to all running components.
2.  **Auth directory watch**: The same `watcher.Watcher` also monitors the auth directory (`auth-dir`). New, modified, or deleted auth files are turned into `AuthUpdate` events and processed through a buffered channel.

Neither path requires a server restart. The HTTP server continues serving requests throughout.

**Diagram: High-level hot reload triggers**

```mermaid
flowchart LR
  FS["filesystem\n(fsnotify)"]
  CFG["config.yaml"]
  AUTHDIR["auth-dir/*.json"]
  FS --> CFG
  FS --> AUTHDIR

  CFG -->|"debounced\n150ms"| Watcher["watcher.Watcher"]
  AUTHDIR -->|"hashed\ncompare"| Watcher

  Watcher -->|"reloadCallback(*config.Config)"| SVC["cliproxy.Service"]
  Watcher -->|"chan AuthUpdate"| Queue["authUpdates channel"]

  SVC -->|"server.UpdateClients"| HTTPServer["api.Server"]
  Queue -->|"consumeAuthUpdates"| CoreMgr["coreauth.Manager"]
```

Sources: [internal/watcher/watcher.go:31-55](), [sdk/cliproxy/service.go:56-92](), [sdk/cliproxy/service.go:129-151]()

---

## The `watcher.Watcher`

`watcher.Watcher` in [internal/watcher/watcher.go]() is the core file-monitoring struct. It is created by `cliproxy.Service` during initialization.

### Key fields

| Field | Type | Purpose |
| :--- | :--- | :--- |
| `configPath` | `string` | Absolute path to `config.yaml` [internal/watcher/watcher.go:33-33]() |
| `authDir` | `string` | Absolute path to the auth directory [internal/watcher/watcher.go:34-34]() |
| `reloadCallback` | `func(*config.Config)` | Called when config changes are detected [internal/watcher/watcher.go:44-44]() |
| `watcher` | `*fsnotify.Watcher` | Underlying OS-level file watcher [internal/watcher/watcher.go:45-45]() |
| `lastAuthHashes` | `map[string]string` | SHA-256 hashes of known auth files [internal/watcher/watcher.go:46-46]() |
| `lastAuthContents` | `map[string]*coreauth.Auth` | Parsed auth entries from last scan [internal/watcher/watcher.go:47-47]() |
| `configReloadTimer` | `*time.Timer` | Debounce timer for config changes [internal/watcher/watcher.go:38-38]() |
| `lastConfigHash` | `string` | Hash of last seen config bytes [internal/watcher/watcher.go:50-50]() |
| `authQueue` | `chan<- AuthUpdate` | Write side of the auth update channel [internal/watcher/watcher.go:51-51]() |
| `pendingUpdates` | `map[string]AuthUpdate` | Coalesces rapid auth changes [internal/watcher/watcher.go:56-56]() |
| `storePersister` | `storePersister` | Propagates changes to external stores [internal/watcher/watcher.go:59-59]() |
| `oldConfigYaml` | `[]byte` | YAML snapshot for change detection [internal/watcher/watcher.go:61-61]() |

Sources: [internal/watcher/watcher.go:32-62]()

### Timing constants

```go
replaceCheckDelay        = 50 * time.Millisecond  // allow atomic replace to settle
configReloadDebounce     = 150 * time.Millisecond // debounce window for config writes
authRemoveDebounceWindow = 1 * time.Second        // window before emitting deletion
serverUpdateDebounce     = 1 * time.Second        // debounce for server-wide updates
```

Sources: [internal/watcher/watcher.go:80-87]()

---

## Config Change Detection and Debouncing

When `fsnotify` emits events for `config.yaml`, the watcher starts a debounce timer. This prevents issues with editors that perform multiple writes.

1.  **Event Detection**: `fsnotify` triggers on file modification [internal/watcher/watcher.go:91-94]().
2.  **Debouncing**: The `configReloadTimer` waits for `configReloadDebounce` (150ms) [internal/watcher/watcher.go:84-84]().
3.  **Hash Check**: The watcher computes a SHA-256 hash of the new content and compares it against `lastConfigHash` [internal/watcher/watcher.go:50-50]().
4.  **Callback**: If the hash differs, `reloadCallback(newCfg)` is invoked to update the service [internal/watcher/watcher.go:44-44]().

**Diagram: Config reload sequence**

```mermaid
sequenceDiagram
  participant FS as "fsnotify"
  participant W as "watcher.Watcher"
  participant Timer as "configReloadTimer"
  participant LC as "config.LoadConfig"
  participant CB as "reloadCallback"

  FS->>W: "Write/Create event for config.yaml"
  W->>Timer: "Reset(150ms)"
  Note over Timer: "debounce window"
  Timer-->>W: "timer fires"
  W->>W: "hash check (lastConfigHash)"
  alt "hash changed"
    W->>LC: "LoadConfig(configPath)"
    LC-->>W: "*config.Config"
    W->>CB: "reloadCallback(newCfg)"
  else "hash unchanged"
    W->>W: "skip reload"
  end
```

Sources: [internal/watcher/watcher.go:80-117](), [internal/watcher/clients.go:25-35]()

---

## Auth Directory Watching

The watcher tracks every JSON file in the auth directory. It uses hash-based detection to determine if an actual change occurred within a file.

### `AuthUpdate` Structure
Incremental changes are emitted as `AuthUpdate` objects:
```go
type AuthUpdate struct {
	Action AuthUpdateAction // "add", "modify", "delete"
	ID     string
	Auth   *coreauth.Auth
}
```
Sources: [internal/watcher/watcher.go:74-78]()

### Incremental Logic
*   **Add/Update**: When a file is modified, the watcher parses it into a `coreauth.Auth` object. It uses `diff.BuildAuthChangeDetails` to log specific field changes (e.g., `base-url` or `prefix` changes) [internal/watcher/clients.go:189-195]().
*   **Delete**: Deletions are debounced via `authRemoveDebounceWindow` to handle atomic "write-new-then-delete-old" patterns common in many text editors [internal/watcher/watcher.go:85-85]().

Sources: [internal/watcher/clients.go:143-210](), [internal/watcher/watcher.go:67-71]()

---

## The `reloadCallback` in `cliproxy.Service`

When a config reload is triggered, `cliproxy.Service` executes a series of updates to ensure the runtime state matches the new configuration.

| Component | Action |
| :--- | :--- |
| `coreManager` | Updates selection strategy and retry configuration [sdk/cliproxy/service.go:181-183]() |
| `api.Server` | Updates middleware, loggers, and routes [internal/api/server.go:879-1016]() |
| `ampModule` | Refreshes model mappings and upstream URLs [internal/api/server.go:1008-1010]() |
| `accessManager` | Reloads API keys and access rules [internal/api/server.go:943-952]() |

Sources: [sdk/cliproxy/service.go:174-202](), [internal/api/server.go:879-1016]()

---

## `Server.UpdateClients`

`api.Server.UpdateClients` is the central implementation for runtime configuration updates. It compares the current configuration against a YAML snapshot (`oldConfigYaml`) to detect specific changes [internal/api/server.go:137-137]().

**Diagram: `Server.UpdateClients` — Code Entity Space**

```mermaid
flowchart TD
  UC["api.Server.UpdateClients(newCfg)"]
  OC["oldConfigYaml (snapshot)"]
  
  UC --> DIFF["diff.BuildConfigChangeDetails"]
  DIFF --> LOG["logging.ConfigureLogOutput"]
  DIFF --> STATS["usage.SetStatisticsEnabled"]
  DIFF --> COOL["auth.SetQuotaCooldownDisabled"]
  DIFF --> ACCESS["applyAccessConfig"]
  DIFF --> HANDLERS["handlers.UpdateClients"]
  DIFF --> AMP["ampModule.OnConfigUpdated"]
  
  ACCESS --> AM["access.Manager"]
  HANDLERS --> BASE["handlers.BaseAPIHandler"]
  AMP --> AMOD["ampmodule.AmpModule"]
```

Sources: [internal/api/server.go:879-1016](), [internal/watcher/diff/config_diff.go:14-18]()

### Key Change Detection Points:
*   **Logging**: Toggles between stdout and file-based logging if `LoggingToFile` changes [internal/api/server.go:900-905]().
*   **Management Routes**: Dynamically registers or disables management endpoints if the `secret-key` is added or removed [internal/api/server.go:933-941]().
*   **Retry Logic**: Updates `RequestRetry` and `MaxRetryInterval` in the `authManager` [internal/api/server.go:924-927]().
*   **Management Asset Updater**: Notifies the background auto-updater of configuration changes [internal/managementasset/updater.go:50-56]().

Sources: [internal/api/server.go:879-1016](), [internal/managementasset/updater.go:50-56]()

---

## Config Diff Utilities

The `internal/watcher/diff` package provides specialized logic for comparing complex configuration structures without exposing secrets.

| Function | Source | Purpose |
| :--- | :--- | :--- |
| `BuildConfigChangeDetails` | [internal/watcher/diff/config_diff.go:14]() | Computes a human-readable list of structural config changes. |
| `ComputeExcludedModelsHash` | [internal/watcher/diff/model_hash.go]() | Generates a stable hash for model exclusion lists to detect changes. |
| `BuildAuthChangeDetails` | [internal/watcher/diff/auth_diff.go]() | Compares two `Auth` objects and lists modified fields. |

Sources: [internal/watcher/diff/config_diff.go:14-111](), [internal/watcher/clients.go:189-195]()

---

## Runtime and WebSocket Updates

Beyond file-based updates, the system supports runtime-only configuration updates via the WebSocket gateway.

*   **WebSocket Auth**: When an `aistudio` provider connects via WebSocket, `Service.wsOnConnected` synthesizes a runtime-only `coreauth.Auth` object [sdk/cliproxy/service.go:222-246]().
*   **Dispatch**: This is pushed through `watcher.DispatchRuntimeAuthUpdate`, ensuring it follows the same lifecycle as file-based credentials [internal/watcher/watcher.go:149-151]().

**Diagram: Runtime Auth Flow**

```mermaid
sequenceDiagram
  participant WS as "wsrelay.Manager"
  participant SVC as "cliproxy.Service"
  participant W as "watcher.Watcher"
  participant CM as "coreauth.Manager"

  WS->>SVC: "wsOnConnected(channelID)"
  SVC->>SVC: "Synthesize coreauth.Auth"
  SVC->>W: "DispatchRuntimeAuthUpdate(update)"
  W->>SVC: "emitAuthUpdate"
  SVC->>CM: "applyCoreAuthAddOrUpdate"
```

Sources: [sdk/cliproxy/service.go:222-273](), [internal/watcher/watcher.go:149-151]()

---

# Page: API Reference

# API Reference

<details>
<summary>Relevant source files</summary>

The following files were used as context for generating this wiki page:

- [config.example.yaml](config.example.yaml)
- [internal/api/handlers/management/config_basic.go](internal/api/handlers/management/config_basic.go)
- [internal/api/handlers/management/config_lists.go](internal/api/handlers/management/config_lists.go)
- [internal/api/server.go](internal/api/server.go)
- [internal/config/config.go](internal/config/config.go)
- [internal/watcher/watcher.go](internal/watcher/watcher.go)
- [sdk/cliproxy/service.go](sdk/cliproxy/service.go)
- [test/amp_management_test.go](test/amp_management_test.go)

</details>



This page is a complete reference index for all HTTP endpoints exposed by CLIProxyAPI. It covers the routing structure, authentication requirements, and shared conventions that apply across all endpoint families. Detailed documentation for each family is in the child pages:

- OpenAI-compatible endpoints → [OpenAI Compatible Endpoints](#4.1)
- Gemini and Vertex endpoints → [Gemini and Vertex Endpoints](#4.2)
- Claude API endpoints → [Claude API Endpoints](#4.3)
- Management API → [Management API](#4.4)
- Amp CLI integration routes → [Amp CLI Integration](#4.5)

For information about how requests are processed internally (translation, auth injection, executor dispatch), see [Core Architecture](#3).

---

## Endpoint Families Overview

All routes are registered inside `internal/api/server.go`. The `setupRoutes()` function registers the inference and callback routes; `registerManagementRoutes()` registers the `v0/management` tree lazily when a secret key is configured.

**Route registration diagram:**

```mermaid
flowchart TD
    NewServer["api.NewServer()"]
    setupRoutes["s.setupRoutes()"]
    registerManagementRoutes["s.registerManagementRoutes()"]
    RegisterModule["modules.RegisterModule(ctx, s.ampModule)"]

    NewServer --> setupRoutes
    NewServer --> RegisterModule
    NewServer --> registerManagementRoutes

    setupRoutes --> V1Group["s.engine.Group('/v1')\nv1.Use(AuthMiddleware)"]
    setupRoutes --> V1BetaGroup["s.engine.Group('/v1beta')\nv1beta.Use(AuthMiddleware)"]
    setupRoutes --> V1Internal["s.engine.POST('/v1internal:method')"]
    setupRoutes --> OAuthCallbacks["OAuth callback routes:\n/anthropic/callback\n/codex/callback\n/google/callback\n/iflow/callback\n/antigravity/callback"]
    setupRoutes --> RootRoutes["s.engine.GET('/')\ns.engine.GET('/management.html')"]

    V1Group --> V1Routes["v1.GET('/models')\nv1.POST('/chat/completions')\nv1.POST('/completions')\nv1.POST('/messages')\nv1.POST('/messages/count_tokens')\nv1.GET('/responses')\nv1.POST('/responses')\nv1.POST('/responses/compact')"]

    V1BetaGroup --> V1BetaRoutes["v1beta.GET('/models')\nv1beta.POST('/models/*action')\nv1beta.GET('/models/*action')"]

    registerManagementRoutes --> MgmtGroup["s.engine.Group('/v0/management')\nmgmt.Use(s.managementAvailabilityMiddleware())\nmgmt.Use(s.mgmt.Middleware())"]

    MgmtGroup --> MgmtRoutes["150+ management endpoints\n(config, auth-files, OAuth flows,\nAPI keys, usage, logs, etc.)"]

    RegisterModule --> AmpRoutes["Amp CLI routes\n(registered via modules.RegisterModule)"]
```

**Sources:** [internal/api/server.go:182-315](), [internal/api/server.go:321-438](), [internal/api/server.go:476-645](), [internal/api/server.go:282-291]()

---

## Endpoint Index

### Inference Endpoints

These routes require an `Authorization: Bearer <api-key>` header when `api-keys` is configured in `config.yaml`. All are registered under the Gin `AuthMiddleware`.

| Method | Path | Handler | Protocol Family |
|--------|------|---------|-----------------|
| `GET` | `/v1/models` | `unifiedModelsHandler` | OpenAI / Claude |
| `POST` | `/v1/chat/completions` | `OpenAIAPIHandler.ChatCompletions` | OpenAI |
| `POST` | `/v1/completions` | `OpenAIAPIHandler.Completions` | OpenAI |
| `POST` | `/v1/messages` | `ClaudeCodeAPIHandler.ClaudeMessages` | Claude |
| `POST` | `/v1/messages/count_tokens` | `ClaudeCodeAPIHandler.ClaudeCountTokens` | Claude |
| `POST` | `/v1/responses` | `OpenAIResponsesAPIHandler.Responses` | Codex/OpenAI |
| `POST` | `/v1/responses/compact` | `OpenAIResponsesAPIHandler.Compact` | Codex/OpenAI |
| `GET` | `/v1/responses` | `OpenAIResponsesAPIHandler.ResponsesWebsocket` | Codex/OpenAI WS |
| `GET` | `/v1beta/models` | `GeminiAPIHandler.GeminiModels` | Gemini |
| `POST` | `/v1beta/models/*action` | `GeminiAPIHandler.GeminiHandler` | Gemini |
| `GET` | `/v1beta/models/*action` | `GeminiAPIHandler.GeminiGetHandler` | Gemini |
| `POST` | `/v1internal:method` | `GeminiCLIAPIHandler.CLIHandler` | Gemini CLI |
| `GET` | `/v1/ws` | `wsrelay.Manager.Handler()` | WebSocket relay |

**Sources:** [internal/api/server.go:329-363]()

### Management Endpoints

All `/v0/management/*` routes are guarded by `managementAvailabilityMiddleware` and `mgmt.Middleware()`. They are registered when a `remote-management.secret-key` is set, when the `MANAGEMENT_PASSWORD` environment variable is present, or when a local password is provided via `WithLocalManagementPassword`.

**Endpoint categories:**

| Category | Example Endpoints | Count |
|----------|-------------------|-------|
| **Configuration** | `GET/PUT /config.yaml`, `GET /config`, `GET/PUT/PATCH /debug` | ~15 |
| **Usage & Statistics** | `GET /usage`, `GET /usage/export`, `POST /usage/import` | 3 |
| **Logs** | `GET/DELETE /logs`, `GET /request-error-logs`, `GET /request-log-by-id/:id` | ~7 |
| **Auth Files** | `GET/POST/DELETE /auth-files`, `PATCH /auth-files/status`, `GET /auth-files/models` | ~8 |
| **API Keys** | `GET/PUT/PATCH/DELETE /gemini-api-key`, `/claude-api-key`, `/codex-api-key` | ~12 |
| **OAuth Flows** | `GET /anthropic-auth-url`, `/codex-auth-url`, `/gemini-cli-auth-url`, `POST /oauth-callback` | ~9 |
| **OpenAI Compatibility** | `GET/PUT/PATCH/DELETE /openai-compatibility` | 4 |
| **Vertex AI** | `GET/PUT/PATCH/DELETE /vertex-api-key`, `POST /vertex/import` | 5 |
| **Amp Integration** | `GET/PUT/DELETE /ampcode/*` (upstream-url, model-mappings, etc.) | ~15 |
| **OAuth Model Config** | `GET/PUT/PATCH/DELETE /oauth-excluded-models`, `/oauth-model-alias` | ~8 |
| **Routing & Retry** | `GET/PUT/PATCH /routing/strategy`, `/request-retry`, `/max-retry-interval` | ~9 |
| **Quota Behavior** | `GET/PUT/PATCH /quota-exceeded/switch-project`, `/switch-preview-model` | 6 |
| **Proxy Settings** | `GET/PUT/PATCH/DELETE /proxy-url` | 4 |
| **Misc Settings** | `GET/PUT/PATCH /logging-to-file`, `/ws-auth`, `/force-model-prefix` | ~10 |

The complete management endpoint listing with request/response schemas is documented in [Management API](#4.4).

**Sources:** [internal/api/server.go:488-645](), [internal/api/handlers/management/config_lists.go:108-255](), [internal/api/handlers/management/config_basic.go:26-222]()

### OAuth Callback Endpoints

These receive redirects from provider authorization servers (Google, Anthropic, OpenAI, etc.). They are unauthenticated.

| Method | Path | Provider |
|--------|------|----------|
| `GET` | `/anthropic/callback` | Anthropic / Claude |
| `GET` | `/codex/callback` | OpenAI Codex |
| `GET` | `/google/callback` | Google Gemini CLI |
| `GET` | `/iflow/callback` | iFlow |
| `GET` | `/antigravity/callback` | Antigravity |

**Sources:** [internal/api/server.go:367-437]()

### Utility Endpoints

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/` | Server info JSON: `{"message": "CLI Proxy API Server", "endpoints": [...]}` |
| `GET` | `/management.html` | Management control panel HTML asset (auto-synced from GitHub) |
| `GET` | `/keep-alive` | Heartbeat endpoint (authenticated with local password, resets idle timeout) |

**Keep-Alive Mechanism:**
The `/keep-alive` endpoint is enabled via the `WithKeepAliveEndpoint` server option. If no heartbeat is received within the configured `keepAliveTimeout`, the `keepAliveOnTimeout` callback triggers (used in TUI mode to close the server when the UI exits).

**Sources:** [internal/api/server.go:351-362](), [internal/api/server.go:688-763]()

---

## Request Authentication

The `AuthMiddleware` function (defined in `internal/api/server.go`) wraps all inference endpoint groups. It delegates to `sdkaccess.Manager.Authenticate()`.

**Authentication middleware flow:**

```mermaid
flowchart TD
    REQ["HTTP request to inference endpoint"]
    AuthMiddleware["AuthMiddleware(accessManager)"]
    CheckManager{"accessManager\n== nil?"}
    NextNoAuth["c.Next()\n(no authentication)"]
    Authenticate["accessManager.Authenticate(ctx, req)"]
    AuthResult{"Authentication\nresult?"}
    SetContext["c.Set('apiKey', result.Principal)\nc.Set('accessProvider', result.Provider)\nc.Set('accessMetadata', result.Metadata)"]
    NextAuthed["c.Next()\n(authenticated)"]
    Abort401["c.AbortWithStatusJSON(401, error)"]

    REQ --> AuthMiddleware
    AuthMiddleware --> CheckManager
    CheckManager -- "yes\n(no providers)" --> NextNoAuth
    CheckManager -- "no" --> Authenticate
    Authenticate --> AuthResult
    AuthResult -- "success" --> SetContext
    SetContext --> NextAuthed
    AuthResult -- "error" --> Abort401
```

**Access provider resolution:**
The `accessManager` handles request authentication. If `api-keys` are defined in `config.yaml`, it uses `APIKeyProvider`. Supported headers include `Authorization: Bearer <key>` and `X-API-Key: <key>`.

**Sources:** [internal/api/server.go:1028-1056](), [internal/api/server.go:862-869](), [internal/config/config.go:35-38]()

### Management API Authentication

Management routes use a two-layer middleware stack:
1. **`managementAvailabilityMiddleware`**: Returns 404 when `managementRoutesEnabled` is false.
2. **`mgmt.Middleware()`**: Validates credentials against `localPassword`, `MANAGEMENT_PASSWORD` env, or `remote-management.secret-key`.

**Credential validation order:**

```mermaid
flowchart TD
    REQ["Request to /v0/management/*"]
    Avail["managementAvailabilityMiddleware"]
    Enabled{"managementRoutesEnabled\n.Load()?"}
    Abort404["c.AbortWithStatus(404)"]
    MgmtMW["mgmt.Middleware()"]
    CheckLocal{"Request from\nlocalhost AND\nlocalPassword set?"}
    ValidateLocal["Validate against\nlocalPassword"]
    CheckEnv{"MANAGEMENT_PASSWORD\nenvironment variable set?"}
    ValidateEnv["Validate against\nMANAGEMENT_PASSWORD"]
    ValidateConfig["Validate against\nremote-management.secret-key"]
    AuthResult{"Valid\ncredential?"}
    Next["c.Next()"]
    Abort401["c.AbortWithStatusJSON(401, error)"]

    REQ --> Avail
    Avail --> Enabled
    Enabled -- "false" --> Abort404
    Enabled -- "true" --> MgmtMW
    MgmtMW --> CheckLocal
    CheckLocal -- "yes" --> ValidateLocal
    CheckLocal -- "no" --> CheckEnv
    ValidateLocal --> AuthResult
    CheckEnv -- "yes" --> ValidateEnv
    CheckEnv -- "no" --> ValidateConfig
    ValidateEnv --> AuthResult
    ValidateConfig --> AuthResult
    AuthResult -- "valid" --> Next
    AuthResult -- "invalid" --> Abort401
```

**Sources:** [internal/api/server.go:238-304](), [internal/api/server.go:476-485](), [internal/api/server.go:862-958]()

---

## CORS

A global CORS middleware is applied to every response:
- `Access-Control-Allow-Origin: *`
- `Access-Control-Allow-Methods: GET, POST, PUT, PATCH, DELETE, OPTIONS`
- `Access-Control-Allow-Headers: *`

`OPTIONS` preflight requests return `204 No Content` immediately.

**Sources:** [internal/api/server.go:849-862]()

---

## Streaming

Endpoints that support streaming (e.g., `/v1/chat/completions`) return Server-Sent Events (SSE) when the request body includes `"stream": true`.

**Streaming configuration options:**

| Config Field | Type | Description |
|--------------|------|-------------|
| `streaming.keepalive-seconds` | int | SSE keep-alive interval (seconds). Sends `:ping` events. |
| `streaming.bootstrap-retries` | int | Retries before first byte is sent to client. |
| `nonstream-keepalive-interval` | int | Blank line interval (seconds) for non-streaming responses. |

**Sources:** [config.example.yaml:106-108](), [internal/config/config.go:102-103]()

---

## Handler Hierarchy

The handler objects that serve the inference routes share a common `BaseAPIHandler` base, which holds the auth manager and SDK configuration.

```mermaid
classDiagram
    class BaseAPIHandler {
        +*auth.Manager AuthManager
        +UpdateClients(cfg *config.SDKConfig)
    }
    class OpenAIAPIHandler {
        +*BaseAPIHandler
        +ChatCompletions(c *gin.Context)
        +Completions(c *gin.Context)
        +OpenAIModels(c *gin.Context)
    }
    class OpenAIResponsesAPIHandler {
        +*BaseAPIHandler
        +Responses(c *gin.Context)
        +ResponsesWebsocket(c *gin.Context)
        +Compact(c *gin.Context)
    }
    class ClaudeCodeAPIHandler {
        +*BaseAPIHandler
        +ClaudeMessages(c *gin.Context)
        +ClaudeCountTokens(c *gin.Context)
        +ClaudeModels(c *gin.Context)
    }
    class GeminiAPIHandler {
        +*BaseAPIHandler
        +GeminiModels(c *gin.Context)
        +GeminiHandler(c *gin.Context)
        +GeminiGetHandler(c *gin.Context)
    }
    class GeminiCLIAPIHandler {
        +*BaseAPIHandler
        +CLIHandler(c *gin.Context)
    }

    BaseAPIHandler <|-- OpenAIAPIHandler
    BaseAPIHandler <|-- OpenAIResponsesAPIHandler
    BaseAPIHandler <|-- ClaudeCodeAPIHandler
    BaseAPIHandler <|-- GeminiAPIHandler
    BaseAPIHandler <|-- GeminiCLIAPIHandler
```

**Unified models handler dispatch:**
The `unifiedModelsHandler` on `GET /v1/models` implements User-Agent-based routing to provide Claude-format listings to `claude-cli` and OpenAI-format listings to others.

**Sources:** [internal/api/server.go:321-341](), [internal/api/server.go:766-783](), [sdk/api/handlers/handlers.go]()

---

## Protocol Family Map

The following diagram maps each client protocol family to the route prefix and the handler/package that serves it.

```mermaid
flowchart LR
    subgraph "Client Protocol"
        OAI["OpenAI Chat\n(openai)"]
        CODEX["OpenAI Responses\n(codex)"]
        CLAUDE["Anthropic Claude\n(claude)"]
        GEMINI["Google Gemini\n(gemini)"]
        GCLI["Gemini CLI\n(v1internal)"]
        AMP["Amp CLI\n(ampcode)"]
    end

    subgraph "Route Prefix"
        V1["/v1"]
        V1BETA["/v1beta"]
        V1INT["/v1internal"]
        AMPR["Amp routes"]
    end

    subgraph "Handler Package"
        OPENAI_H["sdk/api/handlers/openai\nOpenAIAPIHandler\nOpenAIResponsesAPIHandler"]
        CLAUDE_H["sdk/api/handlers/claude\nClaudeCodeAPIHandler"]
        GEMINI_H["sdk/api/handlers/gemini\nGeminiAPIHandler\nGeminiCLIAPIHandler"]
        AMP_H["internal/api/modules/amp\nAmpModule"]
    end

    OAI --> V1 --> OPENAI_H
    CODEX --> V1 --> OPENAI_H
    CLAUDE --> V1 --> CLAUDE_H
    GEMINI --> V1BETA --> GEMINI_H
    GCLI --> V1INT --> GEMINI_H
    AMP --> AMPR --> AMP_H
```

**Sources:** [internal/api/server.go:321-363](), [internal/api/server.go:282-291]()

---

# Page: OpenAI Compatible Endpoints

# OpenAI Compatible Endpoints

<details>
<summary>Relevant source files</summary>

The following files were used as context for generating this wiki page:

- [internal/runtime/executor/codex_executor_cache_test.go](internal/runtime/executor/codex_executor_cache_test.go)
- [internal/runtime/executor/codex_websockets_executor.go](internal/runtime/executor/codex_websockets_executor.go)
- [internal/runtime/executor/codex_websockets_executor_test.go](internal/runtime/executor/codex_websockets_executor_test.go)
- [internal/translator/codex/openai/chat-completions/codex_openai_request.go](internal/translator/codex/openai/chat-completions/codex_openai_request.go)
- [internal/translator/codex/openai/chat-completions/codex_openai_request_test.go](internal/translator/codex/openai/chat-completions/codex_openai_request_test.go)
- [sdk/api/handlers/claude/code_handlers.go](sdk/api/handlers/claude/code_handlers.go)
- [sdk/api/handlers/gemini/gemini-cli_handlers.go](sdk/api/handlers/gemini/gemini-cli_handlers.go)
- [sdk/api/handlers/gemini/gemini_handlers.go](sdk/api/handlers/gemini/gemini_handlers.go)
- [sdk/api/handlers/openai/openai_handlers.go](sdk/api/handlers/openai/openai_handlers.go)
- [sdk/api/handlers/openai/openai_responses_handlers.go](sdk/api/handlers/openai/openai_responses_handlers.go)

</details>



This document describes the OpenAI-compatible HTTP endpoints exposed by the CLIProxyAPI. These endpoints implement the OpenAI API specification and translate requests to multiple backend providers including Gemini, Claude, Codex, Qwen, iFlow, Kimi, Antigravity, and generic OpenAI-compatible providers.

---

## Endpoint Overview

All OpenAI-compatible endpoints are mounted under the `/v1` path and require authentication via the `AuthMiddleware`. The server exposes the following routes:

| Method | Path | Handler | Purpose |
|--------|------|---------|---------|
| GET | `/v1/models` | `OpenAIModels` | List available models (filtered to OpenAI spec) |
| POST | `/v1/chat/completions` | `ChatCompletions` | OpenAI Chat Completions API |
| POST | `/v1/completions` | `Completions` | OpenAI legacy Completions API |
| POST | `/v1/messages` | `ClaudeMessages` | Claude Messages API (OpenAI-compatible mount) |
| POST | `/v1/messages/count_tokens` | `ClaudeCountTokens` | Claude token counting |
| POST | `/v1/responses` | `Responses` | OpenAI Responses API (Codex-specific) |
| POST | `/v1/responses/compact` | `Compact` | Compact response format for Codex |

**Sources:** [sdk/api/handlers/openai/openai_handlers.go:92-129](), [sdk/api/handlers/openai/openai_responses_handlers.go:66-93](), [sdk/api/handlers/claude/code_handlers.go:59-86]()

---

## Route Registration and Server Setup

The OpenAI-compatible handlers are instantiated and registered during server initialization. The `OpenAIAPIHandler` and `OpenAIResponsesAPIHandler` wrap a `BaseAPIHandler` which provides core execution logic, including context management and streaming utilities.

### Handler Architecture
The following diagram bridges the HTTP interface to the internal `Executor` system. Handlers use the `BaseAPIHandler` to access the `AuthManager` for credential selection.

```mermaid
graph TB
    subgraph "Natural Language Space (API)"
        CHAT["POST /v1/chat/completions"]
        MODELS["GET /v1/models"]
        RESP["POST /v1/responses"]
    end

    subgraph "Code Entity Space (Implementation)"
        OAI_H["OpenAIAPIHandler<br/>sdk/api/handlers/openai/openai_handlers.go"]
        RESP_H["OpenAIResponsesAPIHandler<br/>sdk/api/handlers/openai/openai_responses_handlers.go"]
        BASE["BaseAPIHandler<br/>sdk/api/handlers/handlers.go"]
        REG["GlobalRegistry<br/>internal/registry/registry.go"]
    end

    CHAT --> OAI_H
    MODELS --> OAI_H
    RESP --> RESP_H
    
    OAI_H -- "Inherits" --> BASE
    RESP_H -- "Inherits" --> BASE
    OAI_H -- "Queries" --> REG
```

**Sources:** [sdk/api/handlers/openai/openai_handlers.go:26-44](), [sdk/api/handlers/openai/openai_responses_handlers.go:24-42](), [internal/registry/registry.go:10-30]()

---

## Request Processing Pipeline

The execution flow involves translating the OpenAI-format JSON into the target provider's format (e.g., Codex or Gemini) before dispatching via the `ProviderExecutor`.

```mermaid
sequenceDiagram
    participant Client
    participant Handler as "OpenAIAPIHandler<br/>sdk/api/handlers/openai"
    participant Base as "BaseAPIHandler<br/>sdk/api/handlers/handlers.go"
    participant AuthMan as "AuthManager<br/>sdk/cliproxy/auth"
    participant Exec as "CodexWebsocketsExecutor<br/>internal/runtime/executor"

    Client->>Handler: POST /v1/chat/completions (JSON)
    Handler->>Handler: shouldTreatAsResponsesFormat() check
    
    alt Streaming Request
        Handler->>Base: ExecuteStreamWithAuthManager()
        Base->>AuthMan: ExecuteStream(...)
        AuthMan->>Exec: Execute(ctx, auth, req, opts)
        Exec->>Exec: buildCodexWebsocketRequestBody()
        Exec-->>Client: WebSocket / SSE Chunks
    else Non-Streaming Request
        Handler->>Base: ExecuteWithAuthManager()
        Base->>AuthMan: Execute(...)
        AuthMan->>Exec: Execute(...)
        Exec-->>Handler: Response Body
        Handler-->>Client: 200 OK (JSON)
    end
```

**Sources:** [sdk/api/handlers/openai/openai_handlers.go:115-129](), [internal/runtime/executor/codex_websockets_executor.go:144-180](), [sdk/api/handlers/handlers.go:185-212]()

---

## Chat Completions Endpoint

**POST** `/v1/chat/completions`

This endpoint accepts standard OpenAI Chat Completions payloads. It includes a specific detection mechanism for "Responses" format payloads (used by Codex/ChatGPT) accidentally sent to the chat endpoint.

### Responses Format Detection
The handler uses `shouldTreatAsResponsesFormat` to detect if a request uses `input` or `instructions` fields instead of the standard `messages` array. If detected, it converts the request using `ConvertOpenAIResponsesRequestToOpenAIChatCompletions` from the `responsesconverter` package.

**Sources:** [sdk/api/handlers/openai/openai_handlers.go:115-121](), [sdk/api/handlers/openai/openai_handlers.go:133-144](), [internal/translator/openai/openai/responses/converter.go:1-50]()

### Legacy Completions Support
The `/v1/completions` endpoint is also supported. Internally, it calls `convertCompletionsRequestToChatCompletions` to map the legacy `prompt` field into a `user` message, allowing it to leverage the modern chat completion infrastructure.

**Sources:** [sdk/api/handlers/openai/openai_handlers.go:153-174](), [sdk/api/handlers/openai/openai_handlers.go:184-207]()

---

## Models Endpoint

**GET** `/v1/models`

Returns a list of available models. The `OpenAIModels` handler filters the global registry to return only the four fields required by the OpenAI specification: `id`, `object`, `created`, and `owned_by`. It calls `h.Models()` which fetches data from `registry.GetGlobalRegistry()`.

**Sources:** [sdk/api/handlers/openai/openai_handlers.go:59-90](), [sdk/api/handlers/openai/openai_handlers.go:50-56]()

---

## Responses API (Codex)

The Responses API (`/v1/responses`) provides a more structured alternative to chat completions, specifically optimized for Codex-based models.

### WebSocket Transport
The `CodexWebsocketsExecutor` implements the `Execute` method for these requests. It attempts to establish a WebSocket connection using the `OpenAI-Beta` header `responses_websockets=2026-02-06`. It handles session management via `codexWebsocketSession`.

**Sources:** [internal/runtime/executor/codex_websockets_executor.go:34-49](), [internal/runtime/executor/codex_websockets_executor.go:144-175]()

### Compact Responses
The `Compact` handler (`/v1/responses/compact`) provides a minimized response format. It explicitly disables streaming; if `stream: true` is provided, it returns a `400 Bad Request`. It passes the `alt` parameter `responses/compact` to the executor.

**Sources:** [sdk/api/handlers/openai/openai_responses_handlers.go:95-137](), [internal/runtime/executor/codex_websockets_executor.go:148-150]()

---

## Translation Logic

When targeting Codex from an OpenAI request, the `ConvertOpenAIRequestToCodex` function performs the following transformations:
1.  **System Messages:** Maps `role: system` to `role: developer`.
2.  **Tool Calls:** Converts OpenAI `tool_calls` into Codex `function_call` objects.
3.  **Tool Outputs:** Maps `role: tool` messages to `type: function_call_output`.
4.  **Multimodal:** Maps `image_url` to `input_image`.

**Sources:** [internal/translator/codex/openai/chat-completions/codex_openai_request.go:120-142](), [internal/translator/codex/openai/chat-completions/codex_openai_request.go:172-181]()

---

## Streaming and Keep-Alives

The proxy supports sophisticated streaming management:

1.  **SSE Keep-Alives:** Controlled by heartbeats in `ForwardStream`. If `alt` is specified (e.g., in Gemini CLI), keep-alive intervals are adjusted.
2.  **Non-Streaming Keep-Alives:** For long-running non-streaming requests, `StartNonStreamingKeepAlive` emits periodic blank lines to prevent connection timeouts.
3.  **Decompression:** The Claude handler (`ClaudeMessages`) specifically handles gzipped responses that may arrive without headers, ensuring the client receives valid JSON.

**Sources:** [sdk/api/handlers/handlers.go:146-180](), [sdk/api/handlers/claude/code_handlers.go:179-196](), [sdk/api/handlers/gemini/gemini-cli_handlers.go:187-192]()

---

# Page: Gemini and Vertex Endpoints

# Gemini and Vertex Endpoints

<details>
<summary>Relevant source files</summary>

The following files were used as context for generating this wiki page:

- [internal/api/modules/amp/amp.go](internal/api/modules/amp/amp.go)
- [internal/api/modules/amp/fallback_handlers.go](internal/api/modules/amp/fallback_handlers.go)
- [internal/api/modules/amp/fallback_handlers_test.go](internal/api/modules/amp/fallback_handlers_test.go)
- [internal/api/modules/amp/gemini_bridge.go](internal/api/modules/amp/gemini_bridge.go)
- [internal/api/modules/amp/gemini_bridge_test.go](internal/api/modules/amp/gemini_bridge_test.go)
- [internal/api/modules/amp/model_mapping.go](internal/api/modules/amp/model_mapping.go)
- [internal/api/modules/amp/model_mapping_test.go](internal/api/modules/amp/model_mapping_test.go)
- [internal/api/modules/amp/response_rewriter.go](internal/api/modules/amp/response_rewriter.go)
- [internal/api/modules/amp/response_rewriter_test.go](internal/api/modules/amp/response_rewriter_test.go)
- [internal/api/modules/amp/routes.go](internal/api/modules/amp/routes.go)
- [internal/api/modules/amp/routes_test.go](internal/api/modules/amp/routes_test.go)
- [internal/auth/models.go](internal/auth/models.go)
- [internal/translator/antigravity/openai/chat-completions/antigravity_openai_request.go](internal/translator/antigravity/openai/chat-completions/antigravity_openai_request.go)
- [internal/translator/gemini-cli/claude/gemini-cli_claude_request.go](internal/translator/gemini-cli/claude/gemini-cli_claude_request.go)
- [internal/translator/gemini-cli/openai/chat-completions/gemini-cli_openai_request.go](internal/translator/gemini-cli/openai/chat-completions/gemini-cli_openai_request.go)
- [internal/translator/gemini/claude/gemini_claude_request.go](internal/translator/gemini/claude/gemini_claude_request.go)
- [internal/translator/gemini/openai/chat-completions/gemini_openai_request.go](internal/translator/gemini/openai/chat-completions/gemini_openai_request.go)
- [internal/translator/gemini/openai/responses/gemini_openai-responses_request.go](internal/translator/gemini/openai/responses/gemini_openai-responses_request.go)

</details>



## Purpose and Scope

This page documents the HTTP API endpoints that provide Google Gemini and Vertex AI integration. CLIProxyAPI exposes multiple endpoint families to support different Gemini access patterns: the standard Gemini REST API (`/v1beta`), the Gemini CLI internal API (`/v1internal:method`), Vertex AI-compatible endpoints, and Amp CLI integration routes. All endpoints accept OpenAI-format requests and translate them to the appropriate Gemini format using a sophisticated translation layer.

The system supports multiple authentication methods: API keys (`gemini-api-key`), OAuth tokens (`gemini-cli`), service accounts (`vertex`), and WebSocket-based runtime authentication for AI Studio. Additionally, the Amp module provides a Gemini bridge that enables local OAuth provider usage for Amp CLI requests while falling back to ampcode.com when models are unavailable.

For information about OpenAI-compatible endpoints, see [OpenAI Compatible Endpoints](#4.1). For Claude API endpoints, see [Claude API Endpoints](#4.3). For Amp CLI integration details, see [Amp CLI Integration](#4.5). For provider configuration and authentication setup, see [Provider Integration](#6) and [Authentication Flows](#7).

---

## Endpoint Families

CLIProxyAPI provides several families of Gemini-related endpoints, each supporting different authentication methods and API formats:

| Endpoint Pattern | Purpose | Authentication | Handler Implementation |
|-----------------|---------|----------------|----------|
| `/v1beta/models` | List available Gemini models | API Key, OAuth, Service Account | `GeminiAPIHandler.GeminiModels` |
| `/v1beta/models/:action` | Generate content, stream, count tokens | API Key, OAuth, Service Account | `GeminiAPIHandler.GeminiHandler` |
| `/v1internal:method` | Gemini CLI internal API gateway | OAuth (Gemini CLI) | `GeminiCLIAPIHandler.CLIHandler` |
| `/api/provider/google/v1beta1/*` | Amp CLI Gemini bridge with fallback | OAuth, API Key | `AmpModule.registerManagementRoutes` |

**Sources:** [sdk/api/handlers/gemini/gemini_handlers.go:50-164](), [sdk/api/handlers/gemini/gemini-cli_handlers.go:51-131](), [internal/api/modules/amp/routes.go:148-210]()

---

## Route Registration Architecture

The following diagram shows how Gemini endpoint handlers are registered in the HTTP server and how requests flow through the authentication and handler layers:

```mermaid
graph TB
    subgraph "Server_Route_Registration"
        setupRoutes["setupRoutes()"]
        v1betaGroup["v1beta := engine.Group('/v1beta')"]
        authMiddleware["AuthMiddleware(accessManager)"]
        geminiHandler["geminiHandlers := NewGeminiAPIHandler(handlers)"]
        cliHandler["geminiCLIHandlers := NewGeminiCLIAPIHandler(handlers)"]
    end
    
    subgraph "Standard_Gemini_Routes"
        modelsGET["GET /v1beta/models"]
        modelsPOST["POST /v1beta/models/*action"]
        modelsGETAction["GET /v1beta/models/*action"]
        cliMethod["POST /v1internal:method"]
    end
    
    subgraph "Handler_Implementations"
        GeminiModels["GeminiAPIHandler.GeminiModels()"]
        GeminiHandler["GeminiAPIHandler.GeminiHandler()"]
        GeminiGetHandler["GeminiAPIHandler.GeminiGetHandler()"]
        CLIHandler["GeminiCLIAPIHandler.CLIHandler()"]
    end
    
    subgraph "Request_Processing_Pipeline"
        AccessManager["sdkaccess.Manager<br/>Authenticate Request"]
        Translator["Translator Registry<br/>OpenAI → Gemini"]
        BaseAPIHandler["BaseAPIHandler.ExecuteWithAuthManager"]
        Executor["Provider Executor<br/>GeminiExecutor/VertexExecutor/GeminiCLIExecutor"]
    end
    
    setupRoutes --> v1betaGroup
    setupRoutes --> geminiHandler
    setupRoutes --> cliHandler
    
    v1betaGroup --> authMiddleware
    authMiddleware --> modelsGET
    authMiddleware --> modelsPOST
    authMiddleware --> modelsGETAction
    
    geminiHandler --> GeminiModels
    geminiHandler --> GeminiHandler
    geminiHandler --> GeminiGetHandler
    cliHandler --> CLIHandler
    
    modelsGET --> GeminiModels
    modelsPOST --> GeminiHandler
    modelsGETAction --> GeminiGetHandler
    cliMethod --> CLIHandler
    
    GeminiModels --> AccessManager
    GeminiHandler --> BaseAPIHandler
    CLIHandler --> AccessManager
    
    BaseAPIHandler --> Translator
    BaseAPIHandler --> Executor
```

**Sources:** [sdk/api/handlers/gemini/gemini_handlers.go:22-164](), [sdk/api/handlers/gemini/gemini-cli_handlers.go:25-131]()

---

## Standard Gemini API (`/v1beta`)

### Endpoint: `GET /v1beta/models`

Lists all available Gemini models accessible through registered credentials. Returns model metadata including names, display names, supported features, and version information. The handler dynamically fetches models from the `registry.GetGlobalRegistry()`.

**Implementation Detail:**
The `GeminiModels` handler normalizes model names to include the `models/` prefix if missing and ensures `supportedGenerationMethods` defaults to `generateContent`.

**Sources:** [sdk/api/handlers/gemini/gemini_handlers.go:50-78]()

---

### Endpoint: `POST /v1beta/models/:modelId:generateContent`

Generates content using a Gemini model. The handler parses the `:action` parameter to extract the model name and the method (e.g., `generateContent`, `streamGenerateContent`, or `countTokens`).

**Action Dispatch Logic:**
```go
// sdk/api/handlers/gemini/gemini_handlers.go:156-163
switch method {
case "generateContent":
    h.handleGenerateContent(c, action[0], rawJSON)
case "streamGenerateContent":
    h.handleStreamGenerateContent(c, action[0], rawJSON)
case "countTokens":
    h.handleCountTokens(c, action[0], rawJSON)
}
```

**Streaming Implementation:**
The `handleStreamGenerateContent` function establishes a Server-Sent Events connection. It uses `ExecuteStreamWithAuthManager` to get a data channel from the underlying provider executor.

**Sources:** [sdk/api/handlers/gemini/gemini_handlers.go:129-164](), [sdk/api/handlers/gemini/gemini_handlers.go:175-210]()

---

## Gemini CLI API (`/v1internal:method`)

The `GeminiCLIAPIHandler` provides compatibility with Google's internal Gemini CLI tool. 

### Security and Routing
This handler restricts access to `localhost` only. If the request is not from `127.0.0.1`, it returns a `403 Forbidden` error.

**Implementation:**
- **Internal Routes:** Handles `/v1internal:generateContent` and `/v1internal:streamGenerateContent` by calling `ExecuteWithAuthManager` or `ExecuteStreamWithAuthManager`.
- **Proxying:** For other internal URIs, it proxies the request directly to `cloudcode-pa.googleapis.com` using the system's configured proxy settings.

**Sources:** [sdk/api/handlers/gemini/gemini-cli_handlers.go:51-131]()

---

## Request Translation Pipeline

CLIProxyAPI utilizes a sophisticated translation layer to convert various input formats (OpenAI Chat, OpenAI Responses, Claude) into the native Gemini format. This process is performed using `gjson` and `sjson` for high-performance JSON manipulation without full struct unmarshaling.

### Translation Logic Overview

| Source Format | Translator Function | Key Transformations |
|---------------|---------------------|---------------------|
| OpenAI Chat | `ConvertOpenAIRequestToGemini` | Maps `reasoning_effort` to `thinkingConfig`, converts `messages` to `contents` and `systemInstruction`. |
| OpenAI Responses | `ConvertOpenAIResponsesRequestToGemini` | Extracts `instructions` to `systemInstruction`, flushes consecutive function calls/outputs into Gemini parts. |
| Claude API | `ConvertClaudeRequestToGemini` | Maps Claude `system` prompts to Gemini `system_instruction`, translates `tool_use` to `functionCall`. |

### Data Flow Diagram

```mermaid
graph LR
    subgraph "Input_Space"
        openaiReq["OpenAI Request JSON<br/>internal/translator/gemini/openai"]
        responsesReq["Responses Request JSON<br/>internal/translator/gemini/openai/responses"]
        claudeReq["Claude Request JSON<br/>internal/translator/gemini/claude"]
    end
    
    subgraph "Translation_Logic"
        Handler["BaseAPIHandler.ExecuteWithAuthManager"]
        SJSON["sjson.SetBytes / sjson.SetRawBytes"]
        GJSON["gjson.GetBytes / gjson.ParseBytes"]
    end
    
    subgraph "Output_Space"
        GeminiReq["Gemini Native JSON<br/>{contents, generationConfig, systemInstruction}"]
    end
    
    openaiReq --> Handler
    responsesReq --> Handler
    claudeReq --> Handler
    Handler --> GJSON
    GJSON --> SJSON
    SJSON --> GeminiReq
```

**Sources:** [internal/translator/gemini/openai/chat-completions/gemini_openai_request.go:29-57](), [internal/translator/gemini/openai/responses/gemini_openai-responses_request.go:15-32](), [internal/translator/gemini/claude/gemini_claude_request.go:32-62]()

---

## Amp CLI Gemini Bridge

The `AmpModule` provides a bridge for the Amp CLI, allowing it to use local Gemini credentials. It includes a fallback mechanism: if a requested model is not available locally, the request is proxied to `ampcode.com`.

### Routing and Fallback Logic
1. **Model Mapping:** The `FallbackHandler` first attempts to map the requested model name using `fh.modelMapper.MapModel`.
2. **Local Execution:** If a local provider is available for the (mapped) model, the handler processes the request locally.
3. **Upstream Proxy:** If no local provider is found, the `proxyHandler` forwards the request to the Amp upstream URL.
4. **Response Rewriting:** The `ResponseRewriter` intercepts the upstream response to ensure it contains the `originalModel` name and injects necessary Amp signatures to prevent CLI crashes.

**Implementation Detail:**
The bridge supports a "Force Mode" (`ForceModelMappings`) where model mappings take precedence over local API keys, allowing users to explicitly route Amp requests to preferred providers.

**Sources:** [internal/api/modules/amp/fallback_handlers.go:114-185](), [internal/api/modules/amp/routes.go:168-186](), [internal/api/modules/amp/response_rewriter.go:210-226]()

---

## Special Features

### Thinking and Reasoning Support
The translators support Gemini 2.0+ thinking capabilities. OpenAI's `reasoning_effort` is mapped to Gemini's `thinkingConfig`.
- `effort == "auto"`: Sets `thinkingBudget` to `-1` and `includeThoughts` to `true`.
- `effort == "none"`: Sets `includeThoughts` to `false`.
- Other values: Map directly to `thinkingLevel`.

**Sources:** [internal/translator/gemini/openai/chat-completions/gemini_openai_request.go:44-57]()

### Amp Signature Injection
To maintain compatibility with the Amp TUI, the `ResponseRewriter` injects empty `signature` fields into `tool_use` and `thinking` blocks if they are missing from the upstream response. This prevents the TUI from crashing when accessing `P.signature.length`.

**Sources:** [internal/api/modules/amp/response_rewriter.go:127-155]()

### Model Metadata Retrieval
The `GeminiGetHandler` (bound to `GET /v1beta/models/*action`) allows clients to retrieve detailed metadata for a specific model by name. It searches the global model registry for a match, supporting both the raw model ID and the `models/` prefixed ID.

**Sources:** [sdk/api/handlers/gemini/gemini_handlers.go:82-125]()

---

# Page: Claude API Endpoints

# Claude API Endpoints

<details>
<summary>Relevant source files</summary>

The following files were used as context for generating this wiki page:

- [internal/translator/claude/gemini/claude_gemini_request.go](internal/translator/claude/gemini/claude_gemini_request.go)
- [internal/translator/claude/openai/chat-completions/claude_openai_request.go](internal/translator/claude/openai/chat-completions/claude_openai_request.go)
- [internal/translator/claude/openai/chat-completions/claude_openai_request_test.go](internal/translator/claude/openai/chat-completions/claude_openai_request_test.go)
- [internal/translator/claude/openai/responses/claude_openai-responses_request.go](internal/translator/claude/openai/responses/claude_openai-responses_request.go)
- [internal/translator/codex/claude/codex_claude_request.go](internal/translator/codex/claude/codex_claude_request.go)
- [internal/translator/codex/claude/codex_claude_request_test.go](internal/translator/codex/claude/codex_claude_request_test.go)
- [internal/translator/codex/claude/codex_claude_response.go](internal/translator/codex/claude/codex_claude_response.go)
- [internal/translator/codex/gemini/codex_gemini_request.go](internal/translator/codex/gemini/codex_gemini_request.go)
- [internal/translator/gemini-cli/claude/gemini-cli_claude_response.go](internal/translator/gemini-cli/claude/gemini-cli_claude_response.go)
- [internal/translator/gemini/claude/gemini_claude_response.go](internal/translator/gemini/claude/gemini_claude_response.go)
- [internal/translator/openai/claude/openai_claude_request.go](internal/translator/openai/claude/openai_claude_request.go)
- [internal/translator/openai/claude/openai_claude_request_test.go](internal/translator/openai/claude/openai_claude_request_test.go)
- [internal/translator/openai/claude/openai_claude_response.go](internal/translator/openai/claude/openai_claude_response.go)
- [internal/translator/openai/gemini/openai_gemini_request.go](internal/translator/openai/gemini/openai_gemini_request.go)
- [internal/translator/openai/gemini/openai_gemini_response.go](internal/translator/openai/gemini/openai_gemini_response.go)

</details>



This page documents the Claude-compatible HTTP endpoints exposed by CLIProxyAPI: `POST /v1/messages`, `POST /v1/messages/count_tokens`, and the conditional Claude model listing on `GET /v1/models`. It covers request and response formats, how each endpoint is implemented, and how incoming Claude API requests are routed and translated for underlying providers like Codex, Gemini, and OpenAI.

---

## Endpoint Overview

All three endpoints share the `/v1` route group, which applies `AuthMiddleware` before any handler runs.

| Method | Path | Handler method | Description |
|--------|------|----------------|-------------|
| `POST` | `/v1/messages` | `ClaudeCodeAPIHandler.ClaudeMessages` | Claude Messages API – streaming and non-streaming |
| `POST` | `/v1/messages/count_tokens` | `ClaudeCodeAPIHandler.ClaudeCountTokens` | Count input tokens without generating a response |
| `GET` | `/v1/models` | `ClaudeCodeAPIHandler.ClaudeModels` (conditional) | Claude model listing; routed only when `User-Agent` starts with `claude-cli` |

**Sources:** [sdk/api/handlers/claude/code_handlers.go:59-65](), [sdk/api/handlers/claude/code_handlers.go:94-124](), [sdk/api/handlers/claude/code_handlers.go:131-150]()

---

## Route Registration

`ClaudeCodeAPIHandler` is instantiated from `BaseAPIHandler` and its methods are attached to the Gin engine. The `ClaudeMessages` handler serves as the primary entry point for chat completions, branching into streaming or non-streaming logic based on the request body.

**Route group / handler wiring diagram:**

```mermaid
flowchart LR
    A["v1_group\n/v1\nAuthMiddleware"] --> B["POST_/messages\nClaudeCodeAPIHandler.ClaudeMessages"]
    A --> C["POST_/messages/count_tokens\nClaudeCodeAPIHandler.ClaudeCountTokens"]
    A --> D["GET_/models\nunifiedModelsHandler"]
    D -- "User-Agent:claude-cli*" --> E["ClaudeCodeAPIHandler.ClaudeModels"]
    D -- "other_User-Agent" --> F["OpenAIAPIHandler.OpenAIModels"]
```

**Sources:** [sdk/api/handlers/claude/code_handlers.go:29-45](), [sdk/api/handlers/claude/code_handlers.go:79-85](), [sdk/api/handlers/openai/openai_handlers.go:58-90]()

---

## `POST /v1/messages`

### Handler Logic
`ClaudeCodeAPIHandler.ClaudeMessages` in `sdk/api/handlers/claude/code_handlers.go`.

The handler:
1. Extracts raw JSON data from the incoming request using `c.GetRawData()`. [sdk/api/handlers/claude/code_handlers.go:67-77]()
2. Checks for the `stream` field using `gjson`. [sdk/api/handlers/claude/code_handlers.go:80-85]()
3. Dispatches to either `handleStreamingResponse` or `handleNonStreamingResponse`. [sdk/api/handlers/claude/code_handlers.go:81-85]()

### Request Translation
When a Claude request is routed to a non-Claude provider (e.g., Codex or OpenAI), the system invokes specific translators.

*   **Claude to Codex:** `ConvertClaudeRequestToCodex` transforms system messages to `developer` roles and maps Claude thinking configurations to Codex reasoning settings. [internal/translator/codex/claude/codex_claude_request.go:18-36]()
*   **Claude to OpenAI:** `ConvertClaudeRequestToOpenAI` maps `max_tokens`, `stop_sequences`, and converts Claude's `thinking.budget_tokens` into OpenAI's `reasoning_effort`. [internal/translator/openai/claude/openai_claude_request.go:16-19](), [internal/translator/openai/claude/openai_claude_request.go:62-96]()

### Streaming Response (SSE)
Handled by `handleStreamingResponse`. It establishes a Server-Sent Events connection. The translation layer ensures that upstream chunks are converted back into Anthropic-compatible events:
*   **OpenAI to Claude:** Processes `reasoning_content` deltas into `thinking_delta` events and `content` deltas into `text_delta` events. [internal/translator/openai/claude/openai_claude_response.go:132-178]()
*   **Codex to Claude:** Implements a state machine to manage `message_start`, `content_block_start` (for thinking or text), and `message_delta`. [internal/translator/codex/claude/codex_claude_response.go:31-47]()

---

## Provider Translation Logic

The system supports complex bi-directional translation for Claude compatibility.

### Request Translation Examples

| Source Format | Target Format | Key Logic | File Reference |
| :--- | :--- | :--- | :--- |
| **OpenAI Chat** | **Claude** | Maps `reasoning_effort` to Claude `thinking.type` (adaptive/enabled). | [internal/translator/claude/openai/chat-completions/claude_openai_request.go:68-115]() |
| **Gemini** | **Claude** | Maps `generationConfig.thinkingConfig` to Claude thinking/budget. | [internal/translator/claude/gemini/claude_gemini_request.go:118-161]() |
| **Claude** | **Codex** | Transforms `tool_use` to `function_call` and handles tool name shortening. | [internal/translator/codex/claude/codex_claude_request.go:152-167]() |

### Response Translation Examples

| Upstream Provider | Downstream (Claude) | Event Mapping | File Reference |
| :--- | :--- | :--- | :--- |
| **Gemini** | **Claude SSE** | Maps `candidates.0.content.parts` to `content_block_delta`. | [internal/translator/gemini/claude/gemini_claude_response.go:100-145]() |
| **OpenAI** | **Claude SSE** | Accumulates tool calls and emits `content_block_start` for tools. | [internal/translator/openai/claude/openai_claude_response.go:198-230]() |

---

## Code Entity Map

The following diagram bridges the "Natural Language Space" (API concepts) to the "Code Entity Space" (Go implementations).

```mermaid
flowchart TD
    subgraph "Natural Language Space"
        Req["Claude Message Request"]
        Stream["SSE Stream"]
        Think["Thinking/Reasoning"]
    end

    subgraph "Code Entity Space"
        Handler["ClaudeCodeAPIHandler\nsdk/api/handlers/claude/code_handlers.go"]
        
        subgraph "Translators"
            C2O["ConvertClaudeRequestToOpenAI\ninternal/translator/openai/claude/openai_claude_request.go"]
            O2C["ConvertOpenAIResponseToClaude\ninternal/translator/openai/claude/openai_claude_response.go"]
            G2C["ConvertGeminiResponseToClaude\ninternal/translator/gemini/claude/gemini_claude_response.go"]
        end
        
        Executor["ExecuteWithAuthManager\nsdk/api/handlers/claude/code_handlers.go"]
    end

    Req --> Handler
    Handler --> Executor
    Executor --> C2O
    Stream --> O2C
    Stream --> G2C
    Think -.-> C2O
```

**Sources:** [sdk/api/handlers/claude/code_handlers.go:29-45](), [internal/translator/openai/claude/openai_claude_request.go:16-19](), [internal/translator/openai/claude/openai_claude_response.go:65-77](), [internal/translator/gemini/claude/gemini_claude_response.go:37-53]()

---

## Thinking and Reasoning Support

Claude's specific `thinking` block is supported across providers:
1.  **Incoming Claude Requests:** The translator checks for `thinking` configuration and maps it to the provider's equivalent (e.g., `reasoning_effort` for OpenAI or `thinkingConfig` for Gemini). [internal/translator/openai/claude/openai_claude_request.go:62-96](), [internal/translator/claude/gemini/claude_gemini_request.go:118-161]()
2.  **Outgoing Responses:** The response translators detect reasoning/thought parts from the provider and wrap them in Anthropic's `thinking` content block type. [internal/translator/gemini/claude/gemini_claude_response.go:113-138](), [internal/translator/openai/claude/openai_claude_response.go:161-178]()

**Sources:** [internal/translator/openai/claude/openai_claude_request.go:62-96](), [internal/translator/openai/claude/openai_claude_response.go:161-178](), [internal/translator/gemini/claude/gemini_claude_response.go:113-138]()

---

# Page: Management API

# Management API

<details>
<summary>Relevant source files</summary>

The following files were used as context for generating this wiki page:

- [internal/api/handlers/management/api_tools.go](internal/api/handlers/management/api_tools.go)
- [internal/api/handlers/management/api_tools_test.go](internal/api/handlers/management/api_tools_test.go)
- [internal/api/handlers/management/auth_files.go](internal/api/handlers/management/auth_files.go)
- [internal/api/handlers/management/handler.go](internal/api/handlers/management/handler.go)
- [internal/api/handlers/management/test_store_test.go](internal/api/handlers/management/test_store_test.go)
- [internal/auth/kimi/kimi.go](internal/auth/kimi/kimi.go)
- [internal/cmd/auth_manager.go](internal/cmd/auth_manager.go)
- [internal/cmd/kimi_login.go](internal/cmd/kimi_login.go)
- [internal/runtime/executor/kimi_executor.go](internal/runtime/executor/kimi_executor.go)
- [internal/runtime/executor/kimi_executor_test.go](internal/runtime/executor/kimi_executor_test.go)
- [internal/runtime/executor/proxy_helpers.go](internal/runtime/executor/proxy_helpers.go)
- [internal/runtime/executor/proxy_helpers_test.go](internal/runtime/executor/proxy_helpers_test.go)
- [internal/runtime/executor/thinking_providers.go](internal/runtime/executor/thinking_providers.go)
- [internal/util/proxy.go](internal/util/proxy.go)
- [sdk/api/management.go](sdk/api/management.go)
- [sdk/auth/kimi.go](sdk/auth/kimi.go)
- [sdk/auth/refresh_registry.go](sdk/auth/refresh_registry.go)
- [sdk/cliproxy/auth/types_test.go](sdk/cliproxy/auth/types_test.go)

</details>



## Overview

The Management API provides HTTP endpoints for dynamically configuring and managing the CLIProxyAPI server without requiring restarts. It exposes functionality for configuration updates, authentication management, OAuth flows, usage statistics, and operational controls.

This document covers the `/v0/management` endpoints and their implementation. For information about AI provider APIs (OpenAI, Claude, Gemini), see pages 4.1, 4.2, and 4.3. For Amp CLI-specific routes, see 4.5.

**Key Features:**
- Hot-reload configuration updates via YAML manipulation.
- OAuth flow orchestration for multiple providers (Gemini, Claude, Codex, Kimi, Qwen, iFlow, Antigravity).
- Authentication credential upload, download, and deletion.
- Usage statistics export and import.
- Real-time logging configuration and log retrieval.
- Provider-specific settings management (API keys, model aliases, exclusion lists).

**Security Model:**
- All management endpoints require authentication via a management key.
- Optional localhost-only restriction for sensitive operations.
- Secret keys are bcrypt-hashed on first use or provided via environment variables.
- Management routes are disabled (404) when no secret key is configured.

---

## Authentication and Authorization

### Secret Key Configuration

Management API authentication is controlled by the `remote-management.secret-key` configuration field or the `MANAGEMENT_PASSWORD` environment variable [internal/api/handlers/management/handler.go:55-56](). When neither is present, and no local password is set, management routes are restricted or disabled.

**Authentication Flow:**

```mermaid
sequenceDiagram
    participant Client as "Management Client"
    participant Handler as "management.Handler.Middleware()"
    participant Route as "Route Handler"
    
    Client->>Handler: "GET /v0/management/config"
    Note over Handler: Extract Key (Authorization or X-Management-Key)
    
    alt Remote request & !allow-remote
        Handler-->>Client: "403 Forbidden (remote management disabled)"
    else Invalid/missing auth
        Handler-->>Client: "401 Unauthorized"
    else Authorized
        Handler->>Route: Execute handler
        Route-->>Client: "200 OK + response"
    end
```

Sources: [internal/api/handlers/management/handler.go:140-230]()

### Middleware Implementation

The `Handler.Middleware()` function enforces access control. It supports multiple authentication methods:
1.  **Authorization Header**: `Bearer <key>` [internal/api/handlers/management/handler.go:212-219]().
2.  **X-Management-Key Header**: Direct key string [internal/api/handlers/management/handler.go:221]().

**IP Banning Logic**: To prevent brute-force attacks, the middleware tracks failed attempts by client IP [internal/api/handlers/management/handler.go:61](). If an IP exceeds 5 failures, it is banned for 30 minutes [internal/api/handlers/management/handler.go:141-142](). A background goroutine periodically purges stale IP entries [internal/api/handlers/management/handler.go:74-82]().

Sources: [internal/api/handlers/management/handler.go:140-230](), [internal/api/handlers/management/handler.go:61-100]()

---

## Route Registration Architecture

### Handler Structure

The `Handler` struct aggregates all configuration references and management state:

```go
type Handler struct {
    cfg                 *config.Config          // Current configuration [internal/api/handlers/management/handler.go:38]
    configFilePath      string                  // Path to config.yaml [internal/api/handlers/management/handler.go:39]
    authManager         *coreauth.Manager       // Global credential manager [internal/api/handlers/management/handler.go:43]
    usageStats          *usage.RequestStatistics // Usage tracker [internal/api/handlers/management/handler.go:44]
    tokenStore          coreauth.Store          // Persistence layer [internal/api/handlers/management/handler.go:45]
    failedAttempts      map[string]*attemptInfo // IP rate limiting [internal/api/handlers/management/handler.go:42]
}
```

Sources: [internal/api/handlers/management/handler.go:37-51]()

---

## Configuration Management Endpoints

### GET /v0/management/config

Returns the complete server configuration as JSON [internal/api/handlers/management/config_basic.go:26-32]().

### GET /v0/management/config.yaml

Returns the raw `config.yaml` file contents, preserving comments and original formatting [internal/api/handlers/management/config_basic.go:167-182]().

### PUT /v0/management/config.yaml

Replaces the entire configuration file after validation.

**Validation Process:**
1.  Read raw body [internal/api/handlers/management/config_basic.go:112]().
2.  Unmarshal into a temporary `config.Config` struct to check YAML syntax [internal/api/handlers/management/config_basic.go:118]().
3.  Write to a temporary file and attempt to load it using `config.LoadConfigOptional` to ensure logical validity [internal/api/handlers/management/config_basic.go:123-148]().
4.  If valid, overwrite the main config file and reload the in-memory handler reference [internal/api/handlers/management/config_basic.go:151-162]().

Sources: [internal/api/handlers/management/config_basic.go:111-163]()

### Generic Field Management

Individual configuration fields can be updated via dedicated endpoints:
-   **Boolean fields**: `/debug`, `/usage-statistics-enabled`, `/logging-to-file` [internal/api/handlers/management/config_basic.go:185-202]().
-   **Integer fields**: `/logs-max-total-size-mb` [internal/api/handlers/management/config_basic.go:205-222]().
-   **List fields**: `/api-keys` [internal/api/handlers/management/config_lists.go:108-119]().

---

## Authentication File Management

### GET /v0/management/auth-files

Lists all authentication credentials currently registered in the `authManager` [internal/api/handlers/management/auth_files.go:237-259](). If the manager is uninitialized, it falls back to listing `.json` files directly from the disk [internal/api/handlers/management/auth_files.go:243]().

**Credential Metadata Extraction**: The system attempts to extract the last refresh timestamp from various metadata keys like `last_refresh` or `lastRefreshedAt` [internal/api/handlers/management/auth_files.go:43-76]().

Sources: [internal/api/handlers/management/auth_files.go:237-259](), [internal/api/handlers/management/auth_files.go:43-76]()

### POST /v0/management/api-call

A powerful tool for testing credentials. It makes a generic HTTP request on behalf of the management caller using a specific credential's proxy and token [internal/api/handlers/management/api_tools.go:108]().

**Token Substitution**: The endpoint supports a magic `$TOKEN$` variable in headers. It automatically resolves the token for the selected `auth_index` by checking `metadata.access_token`, `attributes.api_key`, or refreshing OAuth tokens if necessary [internal/api/handlers/management/api_tools.go:144-164]().

**Proxy Logic**:
1.  Uses selected credential's `proxy_url` if set [internal/api/handlers/management/api_tools.go:88]().
2.  Falls back to global `proxy-url` [internal/api/handlers/management/api_tools.go:89]().
3.  Supports a `direct` keyword to bypass all proxies [internal/api/handlers/management/api_tools_test.go:13-30]().

Sources: [internal/api/handlers/management/api_tools.go:58-216](), [internal/api/handlers/management/api_tools_test.go:13-30]()

---

## OAuth Flow Orchestration

### Callback Forwarding System

The management API manages OAuth flows for providers that require local redirects (like Anthropic on port 54545 or Gemini on port 8085) [internal/api/handlers/management/auth_files.go:45-48]().

```mermaid
graph TD
    subgraph "Management API (Port 8317)"
        Handler["management.Handler"]
        StartForwarder["startCallbackForwarder()"]
    end

    subgraph "Ephemeral Forwarder"
        Port["Port 54545 / 8085"]
        Redirect["HTTP 302 Redirect to 8317"]
    end

    Handler --> StartForwarder
    StartForwarder --> Port
    Port --> Redirect
```

**Implementation Details**:
-   `startCallbackForwarder`: Launches a background `http.Server` on the required port [internal/api/handlers/management/auth_files.go:130-188]().
-   **Forwarding**: Any request received on the ephemeral port is redirected to the main management API with query parameters intact [internal/api/handlers/management/auth_files.go:148-159]().
-   **Cleanup**: Forwarders are tracked in a global map and shut down gracefully after use [internal/api/handlers/management/auth_files.go:190-221]().

Sources: [internal/api/handlers/management/auth_files.go:130-221]()

---

## Provider-Specific Configuration

### Gemini API Key Management

The API provides granular control over Gemini keys, including per-key model exclusions and custom headers [internal/api/handlers/management/config_lists.go:122-242]().

-   `GET /v0/management/gemini-api-key`: Returns the `[]GeminiKey` slice [internal/api/handlers/management/config_lists.go:122]().
-   `PATCH /v0/management/gemini-api-key`: Allows updating a specific key by `index` or `match` (matching the API key string) [internal/api/handlers/management/config_lists.go:146-213]().

Sources: [internal/api/handlers/management/config_lists.go:122-242]()

### Kimi Integration

The Kimi executor is managed through the management API and supports both OpenAI and Claude-compatible formats [internal/runtime/executor/kimi_executor.go:28-34](). It automatically strips the `kimi-` prefix before sending requests to the upstream `api.moonshot.cn` endpoint [internal/runtime/executor/kimi_executor.go:92-96]().

**Kimi Device Flow**:
Kimi authentication uses the RFC 8628 Device Authorization Grant flow [internal/auth/kimi/kimi.go:2-3](). The management API initiates this via `StartDeviceFlow` [internal/auth/kimi/kimi.go:57-59]() and polls for the token [internal/auth/kimi/kimi.go:62-72]().

Sources: [internal/runtime/executor/kimi_executor.go:28-166](), [internal/auth/kimi/kimi.go:2-72]()

---

## Versioning and Updates

### GET /v0/management/latest-version

Checks the GitHub repository for the latest release [internal/api/handlers/management/config_basic.go:40-92]().

-   **Proxy Awareness**: Uses the configured `proxy_url` to perform the GitHub API check [internal/api/handlers/management/config_basic.go:42-49]().
-   **Timeout**: Enforces a 10-second timeout on the version check [internal/api/handlers/management/config_basic.go:41]().

Sources: [internal/api/handlers/management/config_basic.go:40-92]()

---

## Code Entity Mapping

This diagram associates the Management API concepts with the specific code structures that implement them.

```mermaid
classDiagram
    class ManagementHandler["management.Handler"] {
        +cfg config.Config
        +authManager coreauth.Manager
        +tokenStore coreauth.Store
        +Middleware() gin.HandlerFunc
        +GetConfigYAML()
        +PutConfigYAML()
        +APICall()
    }

    class FileTokenStore["auth.FileTokenStore"] {
        +baseDir string
        +Save(Auth)
        +List()
        +Delete(id)
    }

    class KimiExecutor["executor.KimiExecutor"] {
        +Identifier() "kimi"
        +Execute()
        +ExecuteStream()
    }

    ManagementHandler --> FileTokenStore : uses for persistence
    ManagementHandler --> ManagementHandler : Middleware validates secret_key
    ManagementHandler ..> KimiExecutor : manages Kimi credentials
```

Sources: [internal/api/handlers/management/handler.go:37-51](), [internal/runtime/executor/kimi_executor.go:28-34](), [internal/auth/kimi/kimi.go:43-54]()

---

# Page: Amp CLI Integration

# Amp CLI Integration

<details>
<summary>Relevant source files</summary>

The following files were used as context for generating this wiki page:

- [internal/api/modules/amp/amp.go](internal/api/modules/amp/amp.go)
- [internal/api/modules/amp/amp_test.go](internal/api/modules/amp/amp_test.go)
- [internal/api/modules/amp/fallback_handlers.go](internal/api/modules/amp/fallback_handlers.go)
- [internal/api/modules/amp/fallback_handlers_test.go](internal/api/modules/amp/fallback_handlers_test.go)
- [internal/api/modules/amp/gemini_bridge.go](internal/api/modules/amp/gemini_bridge.go)
- [internal/api/modules/amp/gemini_bridge_test.go](internal/api/modules/amp/gemini_bridge_test.go)
- [internal/api/modules/amp/model_mapping.go](internal/api/modules/amp/model_mapping.go)
- [internal/api/modules/amp/model_mapping_test.go](internal/api/modules/amp/model_mapping_test.go)
- [internal/api/modules/amp/proxy.go](internal/api/modules/amp/proxy.go)
- [internal/api/modules/amp/proxy_test.go](internal/api/modules/amp/proxy_test.go)
- [internal/api/modules/amp/response_rewriter.go](internal/api/modules/amp/response_rewriter.go)
- [internal/api/modules/amp/response_rewriter_test.go](internal/api/modules/amp/response_rewriter_test.go)
- [internal/api/modules/amp/routes.go](internal/api/modules/amp/routes.go)
- [internal/api/modules/amp/routes_test.go](internal/api/modules/amp/routes_test.go)
- [internal/api/modules/amp/secret.go](internal/api/modules/amp/secret.go)
- [internal/api/modules/amp/secret_test.go](internal/api/modules/amp/secret_test.go)

</details>



The Amp module provides HTTP routing integration for the Amp CLI through three subsystems: provider-specific alias routes, management proxy routes, and intelligent fallback logic with model mapping support. When local OAuth providers are unavailable, requests can be automatically mapped to alternative models or proxied to ampcode.com.

For general API endpoint documentation, see [API Reference](#4). For configuration options, see [Configuration File Structure](#5.1).

---

## Overview

The `AmpModule` struct at [internal/api/modules/amp/amp.go:27-44]() implements the `RouteModuleV2` interface and registers three routing subsystems during `Register()`:

1. **Provider Alias Routes** (`registerProviderAliases`) - Routes matching `/api/provider/{provider}/v1/*` forward to local handlers (`OpenAIAPIHandler`, `ClaudeCodeAPIHandler`, `GeminiAPIHandler`) based on provider name.
2. **Management Routes** (`registerManagementRoutes`) - Routes matching `/api/auth/*`, `/api/user/*`, `/api/threads/*`, etc. proxy to ampcode.com for OAuth flows and user management.
3. **Fallback System** (`FallbackHandler`) - Wraps provider handlers to check local provider availability via `util.GetProviderName()`, applies model mappings via `DefaultModelMapper`, or proxies to ampcode.com via `httputil.ReverseProxy`.

Hot-reload via `OnConfigUpdated()` is supported for `upstream-url`, `upstream-api-key`, `upstream-api-keys`, `model-mappings`, `force-model-mappings`, and `restrict-management-to-localhost` configuration changes without service restart.

**Sources:** [internal/api/modules/amp/amp.go:27-44](), [internal/api/modules/amp/amp.go:116-159](), [internal/api/modules/amp/routes.go:144-257](), [internal/api/modules/amp/routes.go:265-334]()

---

## Module Architecture

**Title:** AmpModule Component Structure and Route Registration

```mermaid
graph TB
    subgraph "AmpModule struct (amp.go:27-44)"
        MODULE["AmpModule"]
        CONFIG["lastConfig: *config.AmpCode"]
        PROXY["proxy: *httputil.ReverseProxy"]
        MAPPER["modelMapper: *DefaultModelMapper"]
        SECRET["secretSource: SecretSource"]
        RESTRICT["restrictToLocalhost: bool"]
    end
    
    subgraph "Register() (amp.go:116)"
        REG_PROVIDER["registerProviderAliases()<br/>(routes.go:265)"]
        REG_MGMT["registerManagementRoutes()<br/>(routes.go:144)"]
        ENABLE_PROXY["enableUpstreamProxy()<br/>(amp.go:260)"]
    end
    
    subgraph "Provider Routes (routes.go:265-334)"
        PROVIDER_GRP["/api/provider/:provider"]
        OPENAI_H["OpenAIAPIHandler"]
        CLAUDE_H["ClaudeCodeAPIHandler"]
        GEMINI_H["GeminiAPIHandler"]
        FALLBACK_W["FallbackHandler.WrapHandler"]
    end
    
    subgraph "Management Routes (routes.go:144-257)"
        MGMT_GRP["/api/auth/*path<br/>/api/user/*path<br/>/api/threads/*path"]
        MGMT_MW["managementAvailabilityMiddleware<br/>noCORSMiddleware<br/>localhostOnlyMiddleware"]
        PROXY_H["proxyHandler (routes.go:168)"]
        REVERSE_PROXY["httputil.ReverseProxy"]
    end
    
    subgraph "Fallback Logic (fallback_handlers.go:113)"
        WRAP_H["WrapHandler()"]
        EXTRACT["extractModelFromRequest()"]
        GET_PROV["util.GetProviderName()"]
        MAP_MODEL["modelMapper.MapModel()"]
        REWRITE["rewriteModelInRequest()"]
    end
    
    MODULE --> CONFIG
    MODULE --> PROXY
    MODULE --> MAPPER
    MODULE --> SECRET
    MODULE --> RESTRICT
    
    MODULE --> REG_PROVIDER
    MODULE --> REG_MGMT
    
    REG_PROVIDER --> PROVIDER_GRP
    PROVIDER_GRP --> OPENAI_H
    PROVIDER_GRP --> CLAUDE_H
    PROVIDER_GRP --> GEMINI_H
    PROVIDER_GRP --> FALLBACK_W
    
    REG_MGMT --> MGMT_GRP
    MGMT_GRP --> MGMT_MW
    MGMT_MW --> PROXY_H
    PROXY_H --> REVERSE_PROXY
    
    FALLBACK_W --> WRAP_H
    WRAP_H --> EXTRACT
    WRAP_H --> GET_PROV
    WRAP_H --> MAP_MODEL
    WRAP_H --> REWRITE
    WRAP_H --> REVERSE_PROXY
```

**Sources:** [internal/api/modules/amp/amp.go:27-44](), [internal/api/modules/amp/amp.go:116-159](), [internal/api/modules/amp/routes.go:144-257](), [internal/api/modules/amp/routes.go:265-334](), [internal/api/modules/amp/fallback_handlers.go:78-272]()

---

## Provider Alias Routes

Provider alias routes allow the Amp CLI to specify the target provider explicitly in the URL path. This enables provider-specific routing without requiring model name inspection.

### Route Structure

All routes are registered in `registerProviderAliases()` and wrapped with `FallbackHandler.WrapHandler()`.

| Route Pattern | Supported Providers | Handler |
|---------------|-------------------|---------|
| `/api/provider/:provider/models` | `openai`, `anthropic`, `google`, `groq`, `cerebras` | `ampModelsHandler` |
| `/api/provider/:provider/chat/completions` | OpenAI-compatible | `openaiHandlers.ChatCompletions` |
| `/api/provider/:provider/v1/chat/completions` | OpenAI-compatible | `openaiHandlers.ChatCompletions` |
| `/api/provider/:provider/v1/messages` | `anthropic` | `claudeCodeHandlers.ClaudeMessages` |
| `/api/provider/:provider/v1/messages/count_tokens` | `anthropic` | `claudeCodeHandlers.ClaudeCountTokens` |
| `/api/provider/:provider/v1beta/models/*action` | `google` | `geminiHandlers.GeminiHandler` |
| `/api/provider/:provider/completions` | OpenAI-compatible | `openaiHandlers.Completions` |
| `/api/provider/:provider/responses` | OpenAI-compatible | `openaiResponsesHandlers.Responses` |

### Handler Selection

```mermaid
graph LR
    REQUEST["Request:<br/>/api/provider/:provider/v1/chat/completions"]
    EXTRACT["Extract provider<br/>from path param"]
    SWITCH["Switch on provider"]
    
    ANTHROPIC["anthropic → claudeCodeHandlers"]
    GOOGLE["google → geminiHandlers"]
    DEFAULT["default → openaiHandlers"]
    
    FALLBACK["FallbackHandler.WrapHandler()"]
    CHECK_LOCAL["Check local provider<br/>availability"]
    CHECK_MAPPING["Check model mapping<br/>if unavailable"]
    
    PROXY_UPSTREAM["Proxy to ampcode.com"]
    LOCAL_HANDLER["Execute local handler"]
    
    REQUEST --> EXTRACT
    EXTRACT --> SWITCH
    SWITCH --> ANTHROPIC
    SWITCH --> GOOGLE
    SWITCH --> DEFAULT
    
    ANTHROPIC --> FALLBACK
    GOOGLE --> FALLBACK
    DEFAULT --> FALLBACK
    
    FALLBACK --> CHECK_LOCAL
    CHECK_LOCAL -->|"Available"| LOCAL_HANDLER
    CHECK_LOCAL -->|"Unavailable"| CHECK_MAPPING
    CHECK_MAPPING -->|"Mapping found"| LOCAL_HANDLER
    CHECK_MAPPING -->|"No mapping"| PROXY_UPSTREAM
```

**Sources:** [internal/api/modules/amp/routes.go:265-334](), [internal/api/modules/amp/fallback_handlers.go:113-272]()

---

## Fallback Handler System

The `FallbackHandler` wraps request handlers to implement routing decisions based on provider availability and model mapping configuration. When a model's provider is unavailable locally, the handler either applies a configured model mapping to an available alternative, or forwards the request to ampcode.com. Response rewriting restores original model names when mappings are applied.

### Routing Decision Flow

**Title:** FallbackHandler Request Processing Flow with Code Entity References

```mermaid
sequenceDiagram
    participant Client
    participant WrapHandler as "FallbackHandler.WrapHandler<br/>(fallback_handlers.go:113)"
    participant Extract as "extractModelFromRequest<br/>(fallback_handlers.go:300)"
    participant ParseSuffix as "thinking.ParseSuffix<br/>(thinking pkg)"
    participant Mapper as "DefaultModelMapper.MapModel<br/>(model_mapping.go:53)"
    participant GetProv as "util.GetProviderName<br/>(util pkg)"
    participant Rewrite as "rewriteModelInRequest<br/>(fallback_handlers.go:287)"
    participant Proxy as "httputil.ReverseProxy"
    participant Handler as "gin.HandlerFunc"
    
    Client->>WrapHandler: POST /api/provider/{provider}/v1/...
    WrapHandler->>WrapHandler: io.ReadAll(c.Request.Body)
    WrapHandler->>Extract: extractModelFromRequest(bodyBytes, c)
    Extract-->>WrapHandler: modelName
    WrapHandler->>ParseSuffix: ParseSuffix(modelName)
    ParseSuffix-->>WrapHandler: suffixResult.ModelName
    
    alt forceModelMappings() == true
        WrapHandler->>Mapper: MapModel(modelName)
        Mapper->>GetProv: GetProviderName(mappedBaseModel)
        GetProv-->>Mapper: providers[]
        Mapper-->>WrapHandler: mappedModel (if len(providers) > 0)
        alt mappedModel != ""
            WrapHandler->>Rewrite: rewriteModelInRequest(bodyBytes, mappedModel)
            WrapHandler->>WrapHandler: c.Set("mapped_model", mappedModel)
            WrapHandler->>Handler: handler(c)
            Note over WrapHandler: logAmpRouting(RouteTypeModelMapping)
            Handler-->>Client: Response (free)
        else No mapping
            WrapHandler->>GetProv: GetProviderName(normalizedModel)
            GetProv-->>WrapHandler: providers[]
        end
    else forceModelMappings() == false (DEFAULT)
        WrapHandler->>GetProv: GetProviderName(normalizedModel)
        GetProv-->>WrapHandler: providers[]
        alt len(providers) == 0
            WrapHandler->>Mapper: MapModel(normalizedModel)
            Mapper->>GetProv: GetProviderName(mappedModel)
            GetProv-->>Mapper: providers[]
            Mapper-->>WrapHandler: mappedModel
            alt mappedModel != ""
                WrapHandler->>Rewrite: rewriteModelInRequest(bodyBytes, mappedModel)
                WrapHandler->>WrapHandler: c.Set("mapped_model", mappedModel)
                Note over WrapHandler: RouteTypeModelMapping
            end
        end
    end
    
    alt len(providers) > 0
        WrapHandler->>Handler: handler(c)
        Note over WrapHandler: logAmpRouting(RouteTypeLocalProvider)
        Handler-->>Client: Response (free)
    else len(providers) == 0 and m.getProxy() != nil
        WrapHandler->>Proxy: proxy.ServeHTTP(c.Writer, c.Request)
        Note over WrapHandler: logAmpRouting(RouteTypeAmpCredits)
        Proxy-->>Client: Response (uses amp credits)
    else No provider and no proxy
        WrapHandler->>Handler: handler(c) for error
        Note over WrapHandler: logAmpRouting(RouteTypeNoProvider)
        Handler-->>Client: Error response
    end
```

**Sources:** [internal/api/modules/amp/fallback_handlers.go:113-272](), [internal/api/modules/amp/fallback_handlers.go:300-332](), [internal/api/modules/amp/fallback_handlers.go:287-298](), [internal/api/modules/amp/model_mapping.go:53-109]()

### Route Type Logging

The system logs routing decisions with structured fields for observability:

| Route Type | Meaning | Cost | Log Level |
|------------|---------|------|-----------|
| `RouteTypeLocalProvider` | Request handled by local OAuth provider | Free | Debug |
| `RouteTypeModelMapping` | Request mapped to alternative local model | Free | Debug |
| `RouteTypeAmpCredits` | Request forwarded to ampcode.com | Uses Amp credits | Warn |
| `RouteTypeNoProvider` | No provider or fallback available | None | Warn |

**Sources:** [internal/api/modules/amp/fallback_handlers.go:18-76](), [internal/api/modules/amp/fallback_handlers.go:113-272]()

### Response Rewriting

When model mapping is applied, the `ResponseRewriter` transparently restores the original model name in responses to ensure client compatibility. It handles both streaming and non-streaming responses.

```mermaid
graph TB
    REWRITER["ResponseRewriter"]
    WRITE["Write(data)"]
    DETECT["Detect content type"]
    
    STREAM_CHECK{"Is streaming?"}
    BUFFER["Buffer to body"]
    CHUNK_REWRITE["rewriteStreamChunk(data)"]
    FULL_REWRITE["rewriteModelInResponse(body)"]
    
    FLUSH["Flush()"]
    
    REWRITER --> WRITE
    WRITE --> DETECT
    DETECT --> STREAM_CHECK
    
    STREAM_CHECK -->|"Yes (text/event-stream)"| CHUNK_REWRITE
    STREAM_CHECK -->|"No"| BUFFER
    
    CHUNK_REWRITE --> WRITE_UPSTREAM["Write to ResponseWriter"]
    BUFFER --> FLUSH
    
    FLUSH --> FULL_REWRITE
    FULL_REWRITE --> WRITE_UPSTREAM
    
    subgraph "Model Field Rewriting"
        FIELDS["modelFieldPaths:<br/>model, modelVersion,<br/>response.modelVersion,<br/>message.model"]
        REWRITE["sjson.SetBytes(data, path, originalModel)"]
        FIELDS --> REWRITE
    end
    
    subgraph "Amp Compatibility Filter"
        TOOL_CHECK["Check for tool_use block"]
        THINKING_CHECK["Filter thinking blocks"]
        SUPPRESS["content.#(type!='thinking')#"]
        TOOL_CHECK --> THINKING_CHECK
        THINKING_CHECK --> SUPPRESS
    end
    
    FULL_REWRITE --> FIELDS
    FULL_REWRITE --> TOOL_CHECK
```

**Amp Compatibility Filter:** `rewriteModelInResponse()` checks for the presence of `content.#(type=="tool_use")` blocks [internal/api/modules/amp/response_rewriter.go:170-185](). If found, it filters the `content` array to remove thinking blocks, as the Amp client does not render tool calls correctly when both block types are present. Additionally, `ensureAmpSignature` injects empty signature strings into `tool_use` or `thinking` blocks to prevent Amp TUI crashes [internal/api/modules/amp/response_rewriter.go:127-155]().

**Sources:** [internal/api/modules/amp/response_rewriter.go:14-128](), [internal/api/modules/amp/response_rewriter.go:170-208](), [internal/api/modules/amp/response_rewriter.go:127-155]()

---

## Model Mapping

Model mapping enables routing of unavailable models to alternative models that are locally available. This is particularly useful for Amp CLI users who want to use their local OAuth providers instead of Amp credits.

### Configuration Modes

The module supports two model mapping modes controlled by `ampcode.force-model-mappings` [internal/api/modules/amp/amp.go:104-111]():

| Mode | Behavior | Use Case |
|------|----------|----------|
| `false` (default) | Check local provider first, then apply mapping as fallback | Prefer local exact match |
| `true` | Check mapping first, then fall back to local provider | Prefer mapped model over original |

### Regex Support

Mappings can use regular expressions if the `Regex` flag is set in the configuration [internal/api/modules/amp/model_mapping.go:130](). Regex mappings are compiled case-insensitively and evaluated in the order they appear in the configuration [internal/api/modules/amp/model_mapping.go:132-138]().

### Model Extraction

The `extractModelFromRequest()` function handles multiple request formats:

```mermaid
graph TD
    EXTRACT["extractModelFromRequest(body, c)"]
    CHECK_JSON["Check JSON body<br/>gjson.GetBytes(body, 'model')"]
    CHECK_ACTION["Check :action param<br/>c.Param('action')"]
    CHECK_PATH["Check *path param<br/>c.Param('path')"]
    
    JSON_FOUND["Model from JSON<br/>(OpenAI, Claude)"]
    ACTION_FOUND["Split by ':' to extract model<br/>(Gemini standard)"]
    PATH_FOUND["Extract from '/models/{model}:method'<br/>(AMP CLI Gemini)"]
    
    EXTRACT --> CHECK_JSON
    CHECK_JSON -->|"exists"| JSON_FOUND
    CHECK_JSON -->|"not exists"| CHECK_ACTION
    CHECK_ACTION -->|"exists"| ACTION_FOUND
    CHECK_ACTION -->|"empty"| CHECK_PATH
    CHECK_PATH -->|"contains /models/"| PATH_FOUND
    CHECK_PATH -->|"no match"| EMPTY["Return ''"]
```

**Sources:** [internal/api/modules/amp/fallback_handlers.go:300-332]()

---

## Management Routes

Management routes proxy requests to the Amp control plane for OAuth flows, user management, and telemetry. These routes are secured with multiple layers of middleware.

### Security Middleware Stack

**Title:** Management Routes Middleware Chain with Code Locations

```mermaid
graph TB
    REQUEST["Incoming Request<br/>POST /api/user/profile"]
    AVAIL["managementAvailabilityMiddleware<br/>(routes.go:117)"]
    CORS["noCORSMiddleware<br/>(routes.go:97)"]
    LOCALHOST["localhostOnlyMiddleware<br/>(routes.go:53)"]
    AUTH["wrapManagementAuth<br/>(routes.go:131)"]
    INJECT["clientAPIKeyMiddleware<br/>(routes.go:26)"]
    PROXY["proxyHandler<br/>(routes.go:168)"]
    
    GET_PROXY["m.getProxy()<br/>(amp.go:402)"]
    IS_RESTRICT["m.IsRestrictedToLocalhost()<br/>(amp.go:416)"]
    SPLIT_HOST["net.SplitHostPort<br/>(c.Request.RemoteAddr)"]
    PARSE_IP["net.ParseIP(host)"]
    IS_LOOPBACK["ip.IsLoopback()"]
    GET_API_KEY["c.Get('apiKey')<br/>(gin.Context)"]
    CTX_VALUE["context.WithValue<br/>(clientAPIKeyContextKey)"]
    
    REQUEST --> AVAIL
    AVAIL --> GET_PROXY
    GET_PROXY -->|"nil"| ABORT["c.AbortWithStatusJSON(503)"]
    GET_PROXY -->|"not nil"| CORS
    CORS --> LOCALHOST
    LOCALHOST --> IS_RESTRICT
    IS_RESTRICT -->|"true"| SPLIT_HOST
    SPLIT_HOST --> PARSE_IP
    PARSE_IP --> IS_LOOPBACK
    IS_LOOPBACK -->|"false"| REJECT["c.AbortWithStatusJSON(403)"]
    IS_LOOPBACK -->|"true"| AUTH
    IS_RESTRICT -->|"false"| AUTH
    AUTH -->|"path matches /auth, /threads, /docs, /settings"| INJECT
    AUTH -->|"other paths"| AUTH_CHECK["auth middleware (gin.HandlerFunc)"]
    AUTH_CHECK -->|"invalid"| DENY["c.AbortWithStatus(401)"]
    AUTH_CHECK -->|"valid"| INJECT
    INJECT --> GET_API_KEY
    GET_API_KEY --> CTX_VALUE
    CTX_VALUE --> PROXY
    PROXY --> REVERSE["proxy.ServeHTTP<br/>(httputil.ReverseProxy)"]
```

**Sources:** [internal/api/modules/amp/routes.go:117-128](), [internal/api/modules/amp/routes.go:97-113](), [internal/api/modules/amp/routes.go:53-93](), [internal/api/modules/amp/routes.go:131-142](), [internal/api/modules/amp/routes.go:26-38](), [internal/api/modules/amp/routes.go:168-186](), [internal/api/modules/amp/amp.go:402-427]()

### Localhost Restriction

`localhostOnlyMiddleware()` [internal/api/modules/amp/routes.go:53-93]() checks `m.IsRestrictedToLocalhost()` (hot-reloadable) and enforces the following when enabled:

- Extracts IP from `c.Request.RemoteAddr` using `net.SplitHostPort()`.
- Parses IP with `net.ParseIP()` and validates using `IP.IsLoopback()`.
- Returns `403 Forbidden` for non-loopback IPs (IPv4 and IPv6).
- Cannot be bypassed via `X-Forwarded-For` or other client headers.

### Management Route Patterns

| Pattern | Purpose | Auth Required | Example Usage |
|---------|---------|---------------|---------------|
| `/api/auth/*path` | OAuth flows | Bypassed | `/api/auth/cli-login` |
| `/api/user/*path` | User account operations | Yes | `/api/user/profile` |
| `/api/internal/*path` | Internal operations | Yes | `/api/internal/health` |
| `/api/threads/*path` | Thread management | Bypassed | `/api/threads/123` |
| `/api/meta` | Metadata endpoints | Yes | `/api/meta` |
| `/api/telemetry/*path` | Telemetry data | Yes | `/api/telemetry/events` |
| `/api/otel/*path` | OpenTelemetry | Yes | `/api/otel/trace` |
| `/api/tab/*path` | Tab management | Yes | `/api/tab/active` |
| `/threads` | Root-level threads | Bypassed | `/threads` |
| `/auth/*path` | Root-level auth | Bypassed | `/auth/callback` |
| `/docs/*path` | Documentation | Bypassed | `/docs` |
| `/settings/*path` | Settings | Bypassed | `/settings` |

**Auth Bypass:** `wrapManagementAuth()` [internal/api/modules/amp/routes.go:131-142]() bypasses authentication for paths matching `/threads`, `/auth`, `/docs`, or `/settings` prefixes. All other management routes require valid API key authentication.

**Sources:** [internal/api/modules/amp/routes.go:53-93](), [internal/api/modules/amp/routes.go:117-128](), [internal/api/modules/amp/routes.go:144-257]()

---

## Gemini Bridge

The Gemini bridge handles the Amp CLI's non-standard Gemini API path format by rewriting requests to match the standard Gemini handler's expected format.

### Path Transformation

**Title:** Gemini Bridge Path Rewriting with Code Function References

```mermaid
graph LR
    AMP_PATH["AMP CLI Request:<br/>/publishers/google/models/gemini-3-pro:streamGenerateContent"]
    BRIDGE["createGeminiBridgeHandler<br/>(gemini_bridge.go:19)"]
    PARAM["c.Param('path')<br/>(gin.Context)"]
    INDEX["strings.Index(path, '/models/')<br/>(gemini_bridge.go:27)"]
    ACTION_PART["actionPart = path[idx+8:]"]
    CHECK_MAPPED["c.Get(MappedModelContextKey)<br/>(gemini_bridge.go:32)"]
    COLON_IDX["strings.Index(actionPart, ':')<br/>(gemini_bridge.go:36)"]
    REPLACE["actionPart = strModel + method"]
    APPEND["c.Params = append(...,<br/>gin.Param{Key: 'action', Value: actionPart})<br/>(gemini_bridge.go:44)"]
    HANDLER["handler(c)<br/>(GeminiAPIHandler.GeminiHandler)"]
    
    AMP_PATH --> BRIDGE
    BRIDGE --> PARAM
    PARAM --> INDEX
    INDEX --> ACTION_PART
    ACTION_PART --> CHECK_MAPPED
    CHECK_MAPPED -->|"exists"| COLON_IDX
    COLON_IDX --> REPLACE
    CHECK_MAPPED -->|"not exists"| APPEND
    REPLACE --> APPEND
    APPEND --> HANDLER
```

The bridge supports model mapping integration [internal/api/modules/amp/gemini_bridge.go:31-41]():
1. Checks for `MappedModelContextKey` in Gin context (set by `FallbackHandler`).
2. If found, replaces the model name while preserving the method (`:streamGenerateContent`, `:generateContent`, etc.).
3. Sets the modified value as the `:action` parameter for the standard handler [internal/api/modules/amp/gemini_bridge.go:44-47]().

**Sources:** [internal/api/modules/amp/gemini_bridge.go:9-60]()

---

## Upstream Proxy Configuration

The upstream proxy forwards requests to ampcode.com when local providers are unavailable. It includes automatic gzip decompression and API key injection.

### Proxy Creation

**Title:** createReverseProxy Function Flow with Code Entity Names

```mermaid
graph TB
    CREATE["createReverseProxy(upstreamURL, secretSource)<br/>(proxy.go:60)"]
    PARSE["url.Parse(upstreamURL)<br/>(proxy.go:61)"]
    NEW_PROXY["httputil.NewSingleHostReverseProxy(parsed)<br/>(proxy.go:66)"]
    DIRECTOR["proxy.Director = func(req)<br/>(proxy.go:70)"]
    MODIFY_RESP["proxy.ModifyResponse = func(resp)<br/>(proxy.go:110)"]
    ERROR_HANDLER["proxy.ErrorHandler = func(w, r, err)<br/>(proxy.go:196)"]
    
    subgraph "Director Function (proxy.go:70-106)"
        DEL_AUTH["req.Header.Del('Authorization')<br/>(proxy.go:76)"]
        SCRUB["ScrubProxyAndFingerprintHeaders(req)<br/>(proxy.go:81)"]
        GET_SECRET["secretSource.Get(ctx)<br/>(proxy.go:100)"]
        SET_X_API["req.Header.Set('X-Api-Key', key)<br/>(proxy.go:101)"]
        SET_AUTH["req.Header.Set('Authorization', 'Bearer ' + key)<br/>(proxy.go:102)"]
        SET_HOST["req.Host = parsed.Host<br/>(proxy.go:72)"]
    end
    
    subgraph "ModifyResponse Function (proxy.go:110-193)"
        CHECK_STATUS["resp.StatusCode < 200 || >= 300<br/>(proxy.go:112)"]
        CHECK_CE["resp.Header.Get('Content-Encoding') != ''<br/>(proxy.go:117)"]
        CHECK_STREAM["isStreamingResponse(resp)<br/>(proxy.go:122)"]
        READ_MAGIC["io.ReadFull(resp.Body, header)<br/>(proxy.go:131)"]
        CHECK_MAGIC["header[0] == 0x1f && header[1] == 0x8b<br/>(proxy.go:135)"]
        GZIP_READER["gzip.NewReader(bytes.NewReader(gzippedData))<br/>(proxy.go:151)"]
        UPDATE_BODY["resp.Body = io.NopCloser(bytes.NewReader(decompressed))<br/>(proxy.go:174)"]
        DEL_CE["resp.Header.Del('Content-Encoding')<br/>(proxy.go:178)"]
        UPDATE_CL["resp.Header.Set('Content-Length', ...)<br/>(proxy.go:180)"]
    end
    
    CREATE --> PARSE
    PARSE --> NEW_PROXY
    NEW_PROXY --> DIRECTOR
    DIRECTOR --> DEL_AUTH
    DEL_AUTH --> SCRUB
    SCRUB --> GET_SECRET
    GET_SECRET --> SET_X_API
    SET_X_API --> SET_AUTH
    SET_AUTH --> SET_HOST
    
    NEW_PROXY --> MODIFY_RESP
    MODIFY_RESP --> CHECK_STATUS
    CHECK_STATUS --> CHECK_CE
    CHECK_CE --> CHECK_STREAM
    CHECK_STREAM --> READ_MAGIC
    READ_MAGIC --> CHECK_MAGIC
    CHECK_MAGIC -->|"is gzip"| GZIP_READER
    GZIP_READER --> UPDATE_BODY
    UPDATE_BODY --> DEL_CE
    DEL_CE --> UPDATE_CL
    
    NEW_PROXY --> ERROR_HANDLER
```

**Sources:** [internal/api/modules/amp/proxy.go:60-208]()

### Gzip Handling

`ModifyResponse` [internal/api/modules/amp/proxy.go:110-193]() handles misconfigured upstreams by detecting gzip magic bytes (`0x1f`, `0x8b`) even when `Content-Encoding` headers are missing [internal/api/modules/amp/proxy.go:135](). It performs in-memory decompression and updates the `Content-Length` header accordingly [internal/api/modules/amp/proxy.go:175-180]().

### Error Recovery

`proxyHandler` [internal/api/modules/amp/routes.go:168-186]() includes deferred panic recovery to silence `http.ErrAbortHandler` errors [internal/api/modules/amp/routes.go:172](), which are common during client disconnects.

---

## Secret Management

The Amp module supports multiple API key sources with precedence-based lookup, caching, and per-client upstream routing for multi-tenancy scenarios.

### Architecture

The secret management system consists of two layers:

1. **`MultiSourceSecret`** [internal/api/modules/amp/secret.go:32-154]() - Handles default API key resolution from config, environment, or file.
2. **`MappedSecretSource`** [internal/api/modules/amp/secret.go:174-265]() - Wraps `MultiSourceSecret` to provide per-client upstream routing.

**Title:** Secret Resolution Flow with Code Entity Names

```mermaid
graph TB
    REQUEST["Request with client API key"]
    MIDDLEWARE["clientAPIKeyMiddleware<br/>(routes.go:26)"]
    GIN_GET["c.Get('apiKey')<br/>(routes.go:29)"]
    WITH_VALUE["context.WithValue(c.Request.Context(),<br/>clientAPIKeyContextKey{}, keyStr)<br/>(routes.go:32)"]
    
    PROXY_DIRECTOR["proxy.Director (proxy.go:70)"]
    MAPPED_GET["MappedSecretSource.Get(ctx)<br/>(secret.go:191)"]
    GET_CLIENT["getClientAPIKeyFromContext(ctx)<br/>(routes.go:42)"]
    
    CHECK_LOCK["s.mu.RLock()<br/>(secret.go:195)"]
    CHECK_MAPPING["upstreamKey, ok := s.lookup[clientKey]<br/>(secret.go:196)"]
    FALLBACK_GET["s.defaultSource.Get(ctx)<br/>(secret.go:204)"]
    
    MULTI_GET["MultiSourceSecret.Get(ctx)<br/>(secret.go:75)"]
    CHECK_EXPLICIT["s.explicitKey != ''<br/>(secret.go:77)"]
    CHECK_ENV["os.Getenv(s.envKey)<br/>(secret.go:82)"]
    CHECK_CACHE["s.cache.expiresAt<br/>(secret.go:89)"]
    READ_FILE["s.readFromFile()<br/>(secret.go:110)"]
    PARSE_JSON["json.Unmarshal(content, &secrets)<br/>(secret.go:120)"]
    
    RETURN["Return upstream API key"]
    
    REQUEST --> MIDDLEWARE
    MIDDLEWARE --> GIN_GET
    GIN_GET --> WITH_VALUE
    WITH_VALUE --> PROXY_DIRECTOR
    PROXY_DIRECTOR --> MAPPED_GET
    MAPPED_GET --> GET_CLIENT
    GET_CLIENT --> CHECK_LOCK
    CHECK_LOCK --> CHECK_MAPPING
    CHECK_MAPPING -->|"match found"| RETURN
    CHECK_MAPPING -->|"no match"| FALLBACK_GET
    FALLBACK_GET --> MULTI_GET
    MULTI_GET --> CHECK_EXPLICIT
    CHECK_EXPLICIT -->|"set"| RETURN
    CHECK_EXPLICIT -->|"empty"| CHECK_ENV
    CHECK_ENV -->|"set"| RETURN
    CHECK_ENV -->|"empty"| CHECK_CACHE
    CHECK_CACHE -->|"valid"| RETURN
    CHECK_CACHE -->|"expired/empty"| READ_FILE
    READ_FILE --> PARSE_JSON
    PARSE_JSON --> RETURN
```

**Sources:** [internal/api/modules/amp/secret.go:14-265](), [internal/api/modules/amp/routes.go:26-49](), [internal/api/modules/amp/proxy.go:70-106]()

### Per-Client Upstream Routing

The `MappedSecretSource` enables multi-tenant deployments where different clients use different Amp upstream accounts. `UpdateMappings()` [internal/api/modules/amp/secret.go:209-234]() rebuilds the client-to-upstream key mapping from `upstream-api-keys` configuration entries.

### Default Secret Source Precedence

When no client-specific mapping exists, `MultiSourceSecret` resolves the default key [internal/api/modules/amp/secret.go:75-107]():

| Level | Source | Cached | Hot-Reloadable |
|-------|--------|--------|----------------|
| 1 (Highest) | `config.yaml`: `ampcode.upstream-api-key` | No | Yes |
| 2 | Environment: `AMP_API_KEY` | No | No |
| 3 (Lowest) | File: `~/.local/share/amp/secrets.json` | Yes (5 min TTL) | No |

**Sources:** [internal/api/modules/amp/secret.go:32-154](), [internal/api/modules/amp/routes.go:22-49]()

---

## Hot Reload Support

The Amp module supports hot-reload for multiple configuration settings without requiring service restart.

### Reloadable Configuration

**Title:** OnConfigUpdated Hot-Reload Flow with Code Entities

```mermaid
graph TB
    ON_CONFIG["OnConfigUpdated(cfg *config.Config)<br/>(amp.go:180)"]
    LOCK_OLD["m.configMu.RLock()<br/>(amp.go:184)"]
    GET_OLD["oldSettings := m.lastConfig<br/>(amp.go:185)"]
    
    subgraph "Configuration Change Detection (amp.go:188-248)"
        CMP_RESTRICT["oldSettings.RestrictManagementToLocalhost != newSettings.RestrictManagementToLocalhost<br/>(amp.go:188)"]
        CMP_URL["strings.TrimSpace(newSettings.UpstreamURL)<br/>(amp.go:192)"]
        HAS_MODEL["m.hasModelMappingsChanged(oldSettings, &newSettings)<br/>(amp.go:205)"]
        HAS_API_KEY["m.hasAPIKeyChanged(oldSettings, &newSettings)<br/>(amp.go:228)"]
        HAS_UPSTREAM_KEYS["m.hasUpstreamAPIKeysChanged(oldSettings, &newSettings)<br/>(amp.go:229)"]
    end
    
    subgraph "Update Actions"
        SET_RESTRICT["m.setRestrictToLocalhost(newSettings.RestrictManagementToLocalhost)<br/>(amp.go:189)"]
        ENABLE_PROXY["m.enableUpstreamProxy(newUpstreamURL, &newSettings)<br/>(amp.go:199)"]
        CREATE_PROXY["createReverseProxy(newUpstreamURL, m.secretSource)<br/>(amp.go:219)"]
        SET_PROXY["m.setProxy(proxy)<br/>(amp.go:223)"]
        UPDATE_DEFAULT["ms.UpdateDefaultExplicitKey(newSettings.UpstreamAPIKey)<br/>(amp.go:234)"]
        INVALIDATE["ms.InvalidateCache()<br/>(amp.go:235)"]
        UPDATE_MAP["ms.UpdateMappings(newSettings.UpstreamAPIKeys)<br/>(amp.go:238)"]
        UPDATE_MAPPER["m.modelMapper.UpdateMappings(newSettings.ModelMappings)<br/>(amp.go:208)"]
    end
    
    LOCK_LAST["m.configMu.Lock()<br/>(amp.go:252)"]
    SAVE_LAST["m.lastConfig = new(newSettings)<br/>(amp.go:253)"]
    
    ON_CONFIG --> LOCK_OLD
    LOCK_OLD --> GET_OLD
    GET_OLD --> CMP_RESTRICT
    CMP_RESTRICT -->|"changed"| SET_RESTRICT
    GET_OLD --> CMP_URL
    CMP_URL -->|"enabled"| ENABLE_PROXY
    CMP_URL -->|"URL changed"| CREATE_PROXY
    CREATE_PROXY --> SET_PROXY
    CMP_URL -->|"disabled"| SET_PROXY_NIL["m.setProxy(nil)<br/>(amp.go:215)"]
    GET_OLD --> HAS_MODEL
    HAS_MODEL -->|"true"| UPDATE_MAPPER
    GET_OLD --> HAS_API_KEY
    HAS_API_KEY -->|"true"| UPDATE_DEFAULT
    UPDATE_DEFAULT --> INVALIDATE
    GET_OLD --> HAS_UPSTREAM_KEYS
    HAS_UPSTREAM_KEYS -->|"true"| UPDATE_MAP
    
    SET_RESTRICT --> LOCK_LAST
    ENABLE_PROXY --> LOCK_LAST
    SET_PROXY --> LOCK_LAST
    UPDATE_MAPPER --> LOCK_LAST
    UPDATE_MAP --> LOCK_LAST
    LOCK_LAST --> SAVE_LAST
```

**Sources:** [internal/api/modules/amp/amp.go:180-259](), [internal/api/modules/amp/amp.go:294-395](), [internal/api/modules/amp/secret.go:183-265]()

---

## Error Handling

The Amp module provides graceful error handling with specific behaviors for different failure scenarios.

### Proxy Errors

When the upstream proxy encounters errors, the `ErrorHandler` [internal/api/modules/amp/proxy.go:196-206]() returns:

```json
{
  "error": "amp_upstream_proxy_error",
  "message": "Failed to reach Amp upstream"
}
```

Status Code: `502 Bad Gateway`

### Unavailable Management Routes

When management routes are accessed but the upstream proxy is disabled, `managementAvailabilityMiddleware()` [internal/api/modules/amp/routes.go:117-128]() returns:

```json
{
  "error": "amp upstream proxy not available"
}
```

Status Code: `503 Service Unavailable`

### Localhost Restriction Violations

When non-localhost clients attempt to access management routes, `localhostOnlyMiddleware()` [internal/api/modules/amp/routes.go:53-93]() returns:

```json
{
  "error": "Access denied: management routes restricted to localhost"
}
```

Status Code: `403 Forbidden`

**Sources:** [internal/api/modules/amp/proxy.go:196-206](), [internal/api/modules/amp/routes.go:117-128](), [internal/api/modules/amp/routes.go:53-93]()

---

# Page: Configuration Guide

# Configuration Guide

<details>
<summary>Relevant source files</summary>

The following files were used as context for generating this wiki page:

- [config.example.yaml](config.example.yaml)
- [internal/api/handlers/management/config_basic.go](internal/api/handlers/management/config_basic.go)
- [internal/api/handlers/management/config_lists.go](internal/api/handlers/management/config_lists.go)
- [internal/api/server.go](internal/api/server.go)
- [internal/config/config.go](internal/config/config.go)
- [internal/watcher/watcher.go](internal/watcher/watcher.go)
- [sdk/cliproxy/service.go](sdk/cliproxy/service.go)
- [test/amp_management_test.go](test/amp_management_test.go)

</details>



This document provides a comprehensive overview of CLIProxyAPI's configuration system, including file-based configuration, environment variable overrides, runtime updates, and hot-reload mechanisms. For detailed coverage of specific configuration categories, see:
- [Configuration File Structure](#5.1) — Detail `config.yaml` schema, all available fields, and their purposes
- [Storage Backend Options](#5.2) — Explain token storage backends (Postgres, Git, Object Store, File) and their configuration
- [Environment Variables and Overrides](#5.3) — List all environment variables (`DEPLOY`, `PGSTORE_DSN`, `OBJECTSTORE_*`, `GITSTORE_*`) and their effects
- [Provider-Specific Configuration](#5.4) — Detail configuration entries for each provider (Gemini, Claude, OpenAI-compat, Vertex, etc.) including API keys and model exclusions

## Configuration Overview

CLIProxyAPI uses a multi-layered configuration system that combines:
- **YAML configuration file** (`config.yaml`) for persistent settings [internal/config/config.go:27-130]()
- **Environment variables** for deployment-specific overrides [internal/api/server.go:169-170]()
- **Management API** for runtime updates without restart [internal/api/server.go:159-166]()
- **Hot-reload system** for automatic change detection [internal/watcher/watcher.go:32-62]()

### Configuration Sources

The following diagram bridges the high-level configuration sources to the specific code entities responsible for processing them.

**Configuration Processing Flow**
```mermaid
graph TB
    subgraph "Configuration Sources"
        ConfigFile["config.yaml<br/>(Primary)"]
        EnvVars["Environment Variables<br/>(Overrides)"]
        MgmtAPI["Management API<br/>(Runtime Updates)"]
    end
    
    subgraph "Configuration Loading"
        Loader["config.LoadConfig()<br/>internal/config/config.go"]
        Parser["yaml.Unmarshal()<br/>into Config struct"]
        Validator["Sanitize & Validate<br/>SanitizeGeminiKeys, etc."]
        HashCheck["Secret Hashing<br/>bcrypt for management key"]
    end
    
    subgraph "In-Memory State"
        ConfigStruct["config.Config<br/>internal/config/config.go:28"]
        Server["api.Server.cfg<br/>internal/api/server.go:133"]
        ServiceCfg["cliproxy.Service.cfg<br/>sdk/cliproxy/service.go:34"]
    end
    
    subgraph "Runtime Updates"
        Watcher["watcher.Watcher<br/>internal/watcher/watcher.go:32"]
        MgmtHandler["management.Handler<br/>internal/api/handlers/management"]
        ReloadCallback["reloadCallback<br/>server.UpdateClients()"]
    end
    
    ConfigFile -->|Read| Loader
    EnvVars -->|Override| Loader
    Loader --> Parser
    Parser --> Validator
    Validator --> HashCheck
    HashCheck --> ConfigStruct
    
    ConfigStruct --> Server
    ConfigStruct --> ServiceCfg
    
    MgmtAPI --> MgmtHandler
    MgmtHandler -->|Persist| ConfigFile
    
    Watcher -->|Monitor| ConfigFile
    Watcher -->|Trigger| ReloadCallback
    ReloadCallback -->|Update| Server
```
**Sources:** [internal/config/config.go:27-130](), [internal/api/server.go:120-179](), [internal/watcher/watcher.go:32-62](), [sdk/cliproxy/service.go:32-92]()

## Configuration File Location

The configuration file path is specified at service startup. Common locations include:

| Mode | Default Path | Configuration Reference |
|------|--------------|-----------------|
| Binary execution | `./config.yaml` | [config.example.yaml:1-10]() |
| TUI / Local mode | `~/.cli-proxy-api/config.yaml` | [config.example.yaml:35-36]() |
| Management Path | `h.configFilePath` | [internal/api/handlers/management/config_basic.go:123]() |

The service supports optional configuration files via `config.LoadConfigOptional`. When `optional=true`, a missing file results in a default configuration rather than a fatal error [internal/api/handlers/management/config_basic.go:122-148]().

**Sources:** [internal/api/handlers/management/config_basic.go:111-163](), [config.example.yaml:35-36]()

## Configuration Structure Mapping

The primary configuration struct is `config.Config` with nested structures for different subsystems:

**Code Entity Mapping: Config Structs**
```mermaid
graph TB
    subgraph "config.Config - config/config.go:28"
        Core["Server Settings<br/>Host, Port, AuthDir, Debug"]
        TLS["TLSConfig struct<br/>internal/config/config.go:37"]
        RemoteMgmt["RemoteManagement struct<br/>internal/config/config.go:40"]
        Pprof["PprofConfig struct<br/>internal/config/config.go:49"]
        Routing["RoutingConfig struct<br/>internal/config/config.go:83"]
        QuotaExc["QuotaExceeded struct<br/>internal/config/config.go:80"]
        Payload["PayloadConfig struct<br/>internal/config/config.go:127"]
    end
    
    subgraph "Provider Configurations"
        GeminiKeys["[]GeminiKey<br/>gemini-api-key"]
        ClaudeKeys["[]ClaudeKey<br/>claude-api-key"]
        CodexKeys["[]CodexKey<br/>codex-api-key"]
        OpenAICompat["[]OpenAICompatibility<br/>openai-compatibility"]
        VertexKeys["[]VertexCompatKey<br/>vertex-api-key"]
        AmpConfig["AmpCode struct<br/>ampcode"]
    end
    
    Config["config.Config"] --> Core
    Config --> TLS
    Config --> RemoteMgmt
    Config --> Pprof
    Config --> Routing
    Config --> QuotaExc
    Config --> Payload
    
    Config --> GeminiKeys
    Config --> ClaudeKeys
    Config --> CodexKeys
    Config --> OpenAICompat
    Config --> VertexKeys
    Config --> AmpConfig
```
**Sources:** [internal/config/config.go:28-130](), [internal/config/config.go:137-141]()

### Key Configuration Fields

| Field Path | Type | YAML Key | Purpose |
|------------|------|----------|---------|
| `Config.Host` | `string` | `host` | Network interface binding [internal/config/config.go:32]() |
| `Config.Port` | `int` | `port` | HTTP server port [internal/config/config.go:34]() |
| `Config.AuthDir` | `string` | `auth-dir` | Directory for OAuth token files [internal/config/config.go:43]() |
| `Config.Debug` | `bool` | `debug` | Enable debug logging [internal/config/config.go:46]() |
| `Config.RequestRetry` | `int` | `request-retry` | Number of retry attempts [internal/config/config.go:72]() |
| `Config.Routing.Strategy` | `string` | `routing.strategy` | Credential selection strategy [internal/config/config.go:83]() |

**Sources:** [internal/config/config.go:28-130](), [config.example.yaml:1-100]()

## Hot-Reload Architecture

The configuration system supports zero-downtime updates through file system monitoring and atomic configuration swaps. The `watcher.Watcher` monitors `config.yaml` and triggers a `reloadCallback` which updates the `api.Server` instance [internal/watcher/watcher.go:32-62]().

### Hot-Reload Implementation Details

The watcher system uses these mechanisms:

1. **File System Events**: `fsnotify` monitors the configuration file [internal/watcher/watcher.go:91-99]().
2. **Debouncing**: Groups rapid changes into single reload using `configReloadDebounce` (150ms) [internal/watcher/watcher.go:84]().
3. **Hash-Based Detection**: Compares SHA256 hashes (stored in `lastConfigHash`) to avoid redundant processing [internal/watcher/watcher.go:50]().
4. **Atomic Updates**: Uses `sync.Mutex` (`configReloadMu`) for thread-safe configuration swaps [internal/watcher/watcher.go:37]().

**Sources:** [internal/watcher/watcher.go:32-117](), [internal/api/server.go:181-210]()

## Management API Configuration Updates

The Management API provides HTTP endpoints for runtime configuration updates. All endpoints are handled by `management.Handler` [internal/api/handlers/management/config_basic.go:14-16]().

### Configuration Endpoint Mapping

| Route | Handler Method | File |
|-------|----------------|------|
| `GET /v0/management/config` | `GetConfig` | [internal/api/handlers/management/config_basic.go:26]() |
| `PUT /v0/management/config.yaml` | `PutConfigYAML` | [internal/api/handlers/management/config_basic.go:111]() |
| `GET /v0/management/api-keys` | `GetAPIKeys` | [internal/api/handlers/management/config_lists.go:108]() |
| `PATCH /v0/management/gemini-api-key` | `PatchGeminiKey` | [internal/api/handlers/management/config_lists.go:146]() |

**Sources:** [internal/api/handlers/management/config_basic.go:26-182](), [internal/api/handlers/management/config_lists.go:108-214]()

## Configuration Validation and Sanitization

The configuration system applies validation and normalization during loading to ensure runtime stability:

1. **Gemini Sanitization**: `SanitizeGeminiKeys` removes entries without valid API keys and normalizes fields [internal/api/handlers/management/config_lists.go:143]().
2. **Header Normalization**: `NormalizeHeaders` ensures consistent casing and format for custom provider headers [internal/api/handlers/management/config_lists.go:205]().
3. **Secret Hashing**: Plaintext management keys are automatically hashed using `bcrypt` on startup [internal/config/config.go:18]().

**Sources:** [internal/config/config.go:18-20](), [internal/api/handlers/management/config_lists.go:143-212]()

## Configuration Example Locations

Reference examples for all configuration options:

- **Full Example**: [config.example.yaml]()
- **Provider configurations**: [config.example.yaml:110-160]()
- **Amp integration**: [config.example.yaml:219-251]()
- **Model mappings**: [test/amp_management_test.go:33-35]()

**Sources:** [config.example.yaml:1-345](), [test/amp_management_test.go:27-37]()

---

# Page: Configuration File Structure

# Configuration File Structure

<details>
<summary>Relevant source files</summary>

The following files were used as context for generating this wiki page:

- [config.example.yaml](config.example.yaml)
- [internal/api/handlers/management/config_basic.go](internal/api/handlers/management/config_basic.go)
- [internal/api/handlers/management/config_lists.go](internal/api/handlers/management/config_lists.go)
- [internal/api/server.go](internal/api/server.go)
- [internal/cmd/login.go](internal/cmd/login.go)
- [internal/cmd/run.go](internal/cmd/run.go)
- [internal/config/config.go](internal/config/config.go)
- [internal/watcher/watcher.go](internal/watcher/watcher.go)
- [sdk/cliproxy/service.go](sdk/cliproxy/service.go)
- [test/amp_management_test.go](test/amp_management_test.go)

</details>



## Purpose and Scope

This page documents the complete schema and structure of `config.yaml`, the primary configuration file for CLIProxyAPI. It covers all available configuration fields, their data types, nesting hierarchy, and relationships. For information about specific storage backend configuration, see [Storage Backend Options](5.2). For environment variable overrides, see [Environment Variables and Overrides](5.3). For detailed provider-specific setup guides, see [Provider-Specific Configuration](5.4).

The configuration file uses YAML format and is loaded at service startup. Most configuration changes trigger automatic hot-reload via a file watcher mechanism without requiring service restart.

**Sources:** [internal/config/config.go:1-129](), [config.example.yaml:1-345]()

---

## Configuration File Location

The configuration file path is passed to the service at startup via command-line argument or environment variable. When running via the SDK builder, the service reads the file, unmarshals it into the `Config` struct, applies validation and normalization, and optionally hashes plaintext secrets.

**Sources:** [internal/config/config.go:501-650](), [sdk/cliproxy/service.go:466-651](), [internal/cmd/run.go:27-56]()

---

## Top-Level Configuration Structure

```mermaid
graph TB
    Root["config.yaml<br/>(Config struct)"]
    
    Root --> Server["Server Settings<br/>host, port, tls, pprof"]
    Root --> Auth["Authentication<br/>auth-dir, api-keys,<br/>remote-management"]
    Root --> Logging["Logging & Monitoring<br/>debug, logging-to-file,<br/>request-log,<br/>usage-statistics-enabled"]
    Root --> Providers["Provider Credentials<br/>gemini-api-key,<br/>claude-api-key,<br/>codex-api-key,<br/>openai-compatibility,<br/>vertex-api-key"]
    Root --> Behavior["Request Behavior<br/>proxy-url, request-retry,<br/>quota-exceeded, routing,<br/>ws-auth,<br/>passthrough-headers"]
    Root --> OAuth["OAuth Settings<br/>oauth-excluded-models,<br/>oauth-model-alias"]
    Root --> Amp["Amp Integration<br/>ampcode<br/>(upstream-url,<br/>model-mappings, etc.)"]
    Root --> Payload["Payload Rules<br/>payload.default,<br/>payload.override,<br/>payload.filter"]
    Root --> Advanced["Advanced Options<br/>commercial-mode,<br/>disable-cooling,<br/>force-model-prefix,<br/>nonstream-keepalive-interval"]
    
    style Root stroke-width:2px
```

**Diagram: High-Level Config Structure**

The `Config` struct defined in `internal/config/config.go` embeds `SDKConfig` and adds server-specific fields. All fields are loaded from YAML using struct tags.

**Sources:** [internal/config/config.go:26-129]()

---

## Server Settings

### Basic Server Configuration

| Field | Type | YAML Key | Default | Description |
|-------|------|----------|---------|-------------|
| `Host` | `string` | `host` | `""` (all interfaces) | Network interface to bind. Use `"127.0.0.1"` or `"localhost"` for local-only access. |
| `Port` | `int` | `port` | Required | TCP port for the HTTP/HTTPS server. |

**Sources:** [internal/config/config.go:29-33](), [config.example.yaml:1-6]()

### TLS Configuration

The `TLS` field is a nested struct of type `TLSConfig`:

| Field | Type | YAML Key | Default | Description |
|-------|------|----------|---------|-------------|
| `Enable` | `bool` | `enable` | `false` | Toggles HTTPS mode. |
| `Cert` | `string` | `cert` | `""` | Path to TLS certificate file. |
| `Key` | `string` | `key` | `""` | Path to TLS private key file. |

**Sources:** [internal/config/config.go:35-36](), [config.example.yaml:8-12]()

### Pprof Debug Server

The `Pprof` field controls the optional pprof HTTP server for profiling:

| Field | Type | YAML Key | Default | Description |
|-------|------|----------|---------|-------------|
| `Enable` | `bool` | `enable` | `false` | Toggles pprof server. |
| `Addr` | `string` | `addr` | `"127.0.0.1:8316"` | Host:port for pprof server. |

**Sources:** [internal/config/config.go:47-48](), [config.example.yaml:43-46]()

---

## Authentication and Access Control

### Authentication Directory

| Field | Type | YAML Key | Default | Description |
|-------|------|----------|---------|-------------|
| `AuthDir` | `string` | `auth-dir` | Required | Directory where OAuth tokens and service account files are stored. Supports `~` for home directory expansion. |

**Sources:** [internal/config/config.go:42](), [config.example.yaml:32]()

### API Keys for Request Authentication

API keys are defined in the embedded `SDKConfig` struct:

| Field | Type | YAML Key | Default | Description |
|-------|------|----------|---------|-------------|
| `APIKeys` | `[]string` | `api-keys` | `nil` | List of API keys accepted for request authentication. |

**Sources:** [config.example.yaml:34-38]()

### Remote Management Configuration

The `RemoteManagement` nested struct controls Management API access:

| Field | Type | YAML Key | Default | Description |
|-------|------|----------|---------|-------------|
| `AllowRemote` | `bool` | `allow-remote` | `false` | Whether to allow non-localhost access to management endpoints. |
| `SecretKey` | `string` | `secret-key` | `""` | Management API key. Plaintext values are bcrypt-hashed on load. |
| `DisableControlPanel` | `bool` | `disable-control-panel` | `false` | Disables serving the management UI. |
| `PanelGitHubRepository` | `string` | `panel-github-repository` | `DefaultPanelGitHubRepository` | Source for management panel assets. |

**Sources:** [internal/config/config.go:38-39](), [config.example.yaml:14-29]()

---

## Logging and Monitoring

```mermaid
graph LR
    ConfigLogging["Config<br/>Logging Fields"]
    
    ConfigLogging --> Debug["debug: bool<br/>(log level)"]
    ConfigLogging --> LoggingToFile["logging-to-file: bool<br/>(file vs stdout)"]
    ConfigLogging --> RequestLog["request-log: bool<br/>(enable request logger)"]
    ConfigLogging --> UsageStats["usage-statistics-enabled: bool<br/>(in-memory aggregation)"]
    ConfigLogging --> LogsMax["logs-max-total-size-mb: int<br/>(cleanup threshold)"]
    ConfigLogging --> ErrorMax["error-logs-max-files: int<br/>(error log retention)"]
    
    style ConfigLogging stroke-width:2px
```

**Diagram: Logging and Monitoring Configuration Fields**

| Field | Type | YAML Key | Default | Description |
|-------|------|----------|---------|-------------|
| `Debug` | `bool` | `debug` | `false` | Enables debug-level logging. |
| `LoggingToFile` | `bool` | `logging-to-file` | `false` | Write application logs to rotating files. |
| `LogsMaxTotalSizeMB` | `int` | `logs-max-total-size-mb` | `0` | Maximum total size (MB) of log files. |
| `ErrorLogsMaxFiles` | `int` | `error-logs-max-files` | `10` | Maximum number of error log files retained. |
| `UsageStatisticsEnabled` | `bool` | `usage-statistics-enabled` | `false` | Toggles in-memory usage statistics. |

**Sources:** [internal/config/config.go:44-65](), [config.example.yaml:40-63]()

---

## Provider Credentials

### Gemini API Key Configuration

| Field | Type | YAML Key | Description |
|-------|------|----------|-------------|
| `APIKey` | `string` | `api-key` | Gemini API key. |
| `Prefix` | `string` | `prefix` | Optional namespace for models. |
| `BaseURL` | `string` | `base-url` | Override Gemini API endpoint. |
| `Models` | `[]GeminiModel` | `models` | Model name/alias mappings. |
| `ExcludedModels` | `[]string` | `excluded-models` | Model exclusion patterns. |

**Sources:** [internal/config/config.go:87-88](), [config.example.yaml:105-121]()

### Claude API Key Configuration

| Field | Type | YAML Key | Description |
|-------|------|----------|-------------|
| `APIKey` | `string` | `api-key` | Claude API key. |
| `Prefix` | `string` | `prefix` | Optional model namespace. |
| `BaseURL` | `string` | `base-url` | Override Claude API endpoint. |
| `Cloak` | `*CloakConfig` | `cloak` | Request cloaking for non-Claude-Code clients. |

**Sources:** [internal/config/config.go:97-98](), [config.example.yaml:140-166]()

---

## Request Behavior Configuration

### Proxy and Retry Settings

| Field | Type | YAML Key | Default | Description |
|-------|------|----------|---------|-------------|
| `ProxyURL` | `string` | `proxy-url` | `""` | Global proxy URL (SOCKS5/HTTP/HTTPS). |
| `RequestRetry` | `int` | `request-retry` | `3` | Number of retries for failed requests. |
| `MaxRetryCredentials` | `int` | `max-retry-credentials` | `0` | Max different credentials to try per request. |
| `MaxRetryInterval` | `int` | `max-retry-interval` | `30` | Max wait time (seconds) before retry. |

**Sources:** [internal/config/config.go:66-76](), [config.example.yaml:65-83]()

### Routing Strategy

The `Routing` nested struct configures credential selection behavior:

| Field | Type | YAML Key | Default | Description |
|-------|------|----------|---------|-------------|
| `Strategy` | `string` | `strategy` | `"round-robin"` | Supported: `"round-robin"`, `"fill-first"`. |

**Sources:** [internal/config/config.go:81-82](), [config.example.yaml:91-92]()

---

## Configuration Hot-Reload Mechanism

The system employs an `internal/watcher/Watcher` to monitor the configuration file for changes.

```mermaid
sequenceDiagram
    participant FS as "config.yaml (File System)"
    participant W as "watcher.Watcher"
    participant S as "api.Server"
    participant AM as "sdkaccess.Manager"
    
    FS->>W: fsnotify.Event (Write)
    W->>W: Debounce (150ms)
    W->>S: reloadCallback(newCfg)
    S->>S: UpdateClients(newCfg)
    S->>AM: Refresh Access Rules
    Note over S,AM: Updates middleware & executors
```

**Diagram: Configuration Hot-Reload Sequence**

The `Watcher` uses `fsnotify` to monitor `configPath` [internal/watcher/watcher.go:33-45](). When a write event occurs, it triggers a reload after a short debounce period [internal/watcher/watcher.go:84](). The `Server` then updates its internal state via `UpdateClients` [internal/api/server.go:877-1014]().

**Sources:** [internal/watcher/watcher.go:1-160](), [internal/api/server.go:877-1014]()

---

## Configuration Struct Hierarchy

```mermaid
graph TB
    Config["Config (internal/config/config.go)"]
    
    Config --> SDKConfig["SDKConfig (embedded)"]
    Config --> TLS["TLS: TLSConfig"]
    Config --> RemoteMgmt["RemoteManagement: RemoteManagement"]
    Config --> Pprof["Pprof: PprofConfig"]
    Config --> QuotaExceeded["QuotaExceeded: QuotaExceeded"]
    Config --> Routing["Routing: RoutingConfig"]
    Config --> GeminiKey["GeminiKey: []GeminiKey"]
    Config --> ClaudeKey["ClaudeKey: []ClaudeKey"]
    Config --> AmpCode["AmpCode: AmpCode"]
    Config --> Payload["Payload: PayloadConfig"]
    
    style Config stroke-width:3px
    style SDKConfig stroke-width:2px
```

**Diagram: Complete Configuration Struct Hierarchy**

The `Config` struct embeds `SDKConfig` using inline YAML unmarshaling [internal/config/config.go:28](). This design allows the configuration to include both server-specific settings and SDK-level settings in a unified structure.

**Sources:** [internal/config/config.go:26-129](), [internal/api/server.go:132-134]()

---

# Page: Storage Backend Options

# Storage Backend Options

<details>
<summary>Relevant source files</summary>

The following files were used as context for generating this wiki page:

- [.env.example](.env.example)
- [cmd/server/main.go](cmd/server/main.go)
- [go.mod](go.mod)
- [go.sum](go.sum)
- [internal/store/gitstore.go](internal/store/gitstore.go)
- [internal/store/objectstore.go](internal/store/objectstore.go)
- [internal/store/postgresstore.go](internal/store/postgresstore.go)
- [internal/watcher/synthesizer/config_test.go](internal/watcher/synthesizer/config_test.go)
- [internal/watcher/synthesizer/context.go](internal/watcher/synthesizer/context.go)
- [internal/watcher/synthesizer/file.go](internal/watcher/synthesizer/file.go)
- [internal/watcher/synthesizer/file_test.go](internal/watcher/synthesizer/file_test.go)
- [internal/watcher/synthesizer/helpers.go](internal/watcher/synthesizer/helpers.go)
- [internal/watcher/synthesizer/helpers_test.go](internal/watcher/synthesizer/helpers_test.go)
- [internal/watcher/synthesizer/interface.go](internal/watcher/synthesizer/interface.go)
- [sdk/auth/filestore.go](sdk/auth/filestore.go)
- [sdk/cliproxy/service_excluded_models_test.go](sdk/cliproxy/service_excluded_models_test.go)

</details>



## Purpose and Scope

This document explains the token storage backends available in CLIProxyAPI and how to configure them. Token storage backends persist OAuth tokens, authentication credentials, and the `config.yaml` file. The system supports four different storage backends that can be selected via environment variables at startup.

For information about the authentication credentials themselves and OAuth flows, see [Authentication Setup]() and [Authentication Flows](). For the structure of `config.yaml`, see [Configuration File Structure](). For environment variable reference, see [Environment Variables and Overrides]().

---

## Storage Backend Architecture

CLIProxyAPI uses a pluggable storage backend system to persist tokens and configuration. All backends implement a common storage interface that allows the core service to remain agnostic of the underlying persistence layer.

### Storage Backend Selection Flow

The selection logic is implemented in the server's entry point, checking for specific environment variables in a prioritized order.

```mermaid
graph TB
    Start["Application main()<br/>[cmd/server/main.go]"]
    
    CheckPG{"PGSTORE_DSN<br/>environment variable?"}
    CheckObject{"OBJECTSTORE_ENDPOINT<br/>environment variable?"}
    CheckGit{"GITSTORE_GIT_URL<br/>environment variable?"}
    
    InitPG["PostgresStore<br/>[internal/store/postgresstore.go]"]
    InitObject["ObjectTokenStore<br/>[internal/store/objectstore.go]"]
    InitGit["GitTokenStore<br/>[internal/store/gitstore.go]"]
    InitFile["FileTokenStore<br/>[sdk/auth/filestore.go]"]
    
    Bootstrap["Bootstrap Process<br/>(Sync Remote to Local Spool)"]
    
    Start --> CheckPG
    CheckPG -->|Yes| InitPG
    CheckPG -->|No| CheckObject
    CheckObject -->|Yes| InitObject
    CheckObject -->|No| CheckGit
    CheckGit -->|Yes| InitGit
    CheckGit -->|No| InitFile
    
    InitPG --> Bootstrap
    InitObject --> Bootstrap
    InitGit --> Bootstrap
    InitFile --> Bootstrap
```

**Sources:** Selection logic in [cmd/server/main.go:179-245](), implementation in [internal/store/postgresstore.go:49-100](), [internal/store/gitstore.go:42-48](), and [sdk/auth/filestore.go:30-32]().

---

## Backend Comparison

| Backend | Use Case | Persistence | Multi-Instance | Configuration |
|---------|----------|-------------|----------------|---------------|
| **FileTokenStore** | Local development, single server | Local filesystem | No | None (default) |
| **PostgresStore** | Distributed deployments, high availability | PostgreSQL database | Yes | `PGSTORE_DSN` |
| **GitTokenStore** | Version-controlled credentials, audit trail | Git repository | Yes (with sync) | `GITSTORE_GIT_URL` |
| **ObjectTokenStore** | Cloud-native, S3-compatible storage | Object storage (S3, MinIO) | Yes | `OBJECTSTORE_ENDPOINT` |

---

## FileTokenStore (Default)

The `FileTokenStore` is the default storage backend. It persists token records and auth metadata using the filesystem as backing storage [sdk/auth/filestore.go:22-26]().

### Characteristics

- **Storage Location**: Configurable `baseDir` [sdk/auth/filestore.go:35-39]().
- **Persistence**: Local filesystem only.
- **Multi-Instance**: Not supported (potential for write conflicts).
- **Setup**: Zero configuration required.

### Implementation Details

The `Save` method [sdk/auth/filestore.go:42-123]() resolves the auth file path and writes the metadata as a JSON file. It uses a `sync.Mutex` to prevent concurrent writes within a single process [sdk/auth/filestore.go:61-62](). It also handles `metadataSetter` injection for storage implementations that support metadata [sdk/auth/filestore.go:69-77]().

**Sources:** [sdk/auth/filestore.go:21-171]()

---

## PostgresStore

The `PostgresStore` backend uses PostgreSQL to persist all configuration and credentials while mirroring data to a local "spool" directory [internal/store/postgresstore.go:37-46]().

### Architecture

The `PostgresStore` maintains a local spool directory to ensure that components expecting local files (like the configuration watcher) continue to function.

```mermaid
graph TB
    subgraph "PostgresStore [internal/store/postgresstore.go]"
        PSInst["PostgresStore Struct"]
        DB["sql.DB (pgx driver)"]
        SpoolDir["Spool Directory<br/>(Local Mirror)"]
        
        subgraph "PostgreSQL Schema"
            ConfigTable["config_store Table<br/>(id, content, updated_at)"]
            AuthTable["auth_store Table<br/>(id, content, updated_at)"]
        end
    end
    
    PSInst --> DB
    PSInst --> SpoolDir
    DB --> ConfigTable
    DB --> AuthTable
```

### Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `PGSTORE_DSN` | Yes | - | PostgreSQL DSN [internal/store/postgresstore.go:50-54]() |
| `PGSTORE_SCHEMA` | No | - | Database schema name [internal/store/postgresstore.go:115-120]() |
| `PGSTORE_TABLE_CONFIG`| No | `config_store` | Table name for configuration [internal/store/postgresstore.go:23]() |
| `PGSTORE_TABLE_AUTH` | No | `auth_store` | Table name for auth files [internal/store/postgresstore.go:24]() |

### Bootstrap and Sync

The `Bootstrap` method [internal/store/postgresstore.go:147-158]() performs a bidirectional sync:
1. `EnsureSchema`: Creates tables if they don't exist [internal/store/postgresstore.go:111-144]().
2. `syncConfigFromDatabase`: Downloads `config.yaml` to the spool [internal/store/postgresstore.go:151]().
3. `syncAuthFromDatabase`: Downloads all `.json` auth files to the spool [internal/store/postgresstore.go:154]().

**Sources:** [internal/store/postgresstore.go:22-236]()

---

## GitTokenStore

The `GitTokenStore` backend persists configuration and credentials in a Git repository using the `go-git` library [go.mod:13]().

### Architecture

It mirrors the remote repository locally and performs `Pull` operations on startup and `Push` operations on every save.

```mermaid
graph TB
    subgraph "GitTokenStore [internal/store/gitstore.go]"
        GitInst["GitTokenStore Struct"]
        RepoDir["repoDir (Local Clone)"]
        Remote["Remote URL"]
    end
    
    subgraph "Git Operations"
        Pull["EnsureRepository()<br/>(git pull)"]
        CommitPush["commitAndPushLocked()<br/>(git commit & push)"]
    end
    
    GitInst --> RepoDir
    GitInst --> Remote
    RepoDir -- "Sync" --> Remote
    Pull --> RepoDir
    CommitPush --> RepoDir
```

### Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `GITSTORE_GIT_URL` | Yes | - | Git repository URL [cmd/server/main.go:199-202]() |
| `GITSTORE_GIT_USERNAME`| No | - | Git username [cmd/server/main.go:203-205]() |
| `GITSTORE_GIT_TOKEN` | No | - | Git password/token [cmd/server/main.go:206-208]() |

### Persistence Logic

The `Save` method [internal/store/gitstore.go:216-258]() writes the auth file locally and then triggers `commitAndPushLocked` to synchronize with the remote repository.

**Sources:** [internal/store/gitstore.go:28-258](), [cmd/server/main.go:199-211]()

---

## ObjectTokenStore

The `ObjectTokenStore` backend uses S3-compatible object storage (AWS S3, MinIO) via the `minio-go` SDK [go.mod:19]().

### Configuration

It requires an endpoint, bucket, and credentials. It determines SSL usage based on the endpoint prefix [internal/store/objectstore.go:56-118]().

### Directory Structure

All remote backends (Postgres, Git, Object Store) maintain a similar local directory structure within their spool/work directories:
- `config/config.yaml`: The primary configuration file [internal/store/objectstore.go:26]().
- `auths/`: Directory containing JSON authentication files [internal/store/objectstore.go:27]().

**Sources:** [internal/store/objectstore.go:25-119](), [internal/store/postgresstore.go:74-75](), [internal/store/gitstore.go:113-114]()

---

## Auth Synthesis and Metadata

When files are read from storage (specifically from the `auths/` directory), they are processed by the `FileSynthesizer`.

### FileSynthesizer Implementation

The `FileSynthesizer` [internal/watcher/synthesizer/file.go:20-25]() parses JSON payloads into `coreauth.Auth` entities.

- **Provider Mapping**: Maps JSON `type` to provider strings (e.g., "gemini" becomes "gemini-cli") [internal/watcher/synthesizer/file.go:78-85]().
- **ID Generation**: Uses the relative file path under the auth directory as the unique `Auth.ID` [internal/watcher/synthesizer/file.go:90-99]().
- **Attribute Extraction**: Extracts `priority`, `note`, `proxy_url`, and `prefix` [internal/watcher/synthesizer/file.go:101-159]().
- **Gemini Virtualization**: If the provider is `gemini-cli` and multiple project IDs are present, it generates virtual auth entries [internal/watcher/synthesizer/file.go:171-182]().
- **Model Exclusion**: Merges per-account excluded models with global config via `ApplyAuthExcludedModelsMeta` [internal/watcher/synthesizer/helpers.go:58-104]().

### Stable ID Generation

For API-key based auth (not file-based), the `StableIDGenerator` creates deterministic IDs using SHA256 hashes of the provider kind and key parts [internal/watcher/synthesizer/helpers.go:15-52]().

**Sources:** [internal/watcher/synthesizer/file.go:18-183](), [internal/watcher/synthesizer/helpers.go:15-104]()

---

# Page: Environment Variables and Overrides

# Environment Variables and Overrides

<details>
<summary>Relevant source files</summary>

The following files were used as context for generating this wiki page:

- [cmd/server/main.go](cmd/server/main.go)
- [config.example.yaml](config.example.yaml)
- [go.mod](go.mod)
- [go.sum](go.sum)
- [internal/api/handlers/management/config_basic.go](internal/api/handlers/management/config_basic.go)
- [internal/api/handlers/management/config_lists.go](internal/api/handlers/management/config_lists.go)
- [internal/api/server.go](internal/api/server.go)
- [internal/config/config.go](internal/config/config.go)
- [internal/store/gitstore.go](internal/store/gitstore.go)
- [internal/store/postgresstore.go](internal/store/postgresstore.go)
- [internal/watcher/watcher.go](internal/watcher/watcher.go)
- [sdk/cliproxy/service.go](sdk/cliproxy/service.go)
- [test/amp_management_test.go](test/amp_management_test.go)

</details>



## Purpose and Scope

This page documents all environment variables used by CLIProxyAPI to control runtime behavior and storage backend configuration. Environment variables provide deployment-flexible configuration that overrides default file-based settings, enabling containerized deployments, cloud-native storage, and runtime-specific customization.

For configuration file structure and field definitions, see [Configuration File Structure](). For detailed storage backend setup, see [Storage Backend Options](). For provider-specific configuration fields, see [Provider-Specific Configuration]().

---

## Environment Variable Loading Process

CLIProxyAPI loads environment variables during application startup using a two-stage process:

1.  **`.env` File Loading**: The application attempts to load a `.env` file from the current working directory using the `godotenv` package [cmd/server/main.go:161-166]().
2.  **System Environment Lookup**: Variables are read from the system environment with fallback support for both uppercase and lowercase names [cmd/server/main.go:168-177]().

### Environment Initialization Flow
Title: Environment Loading Logic
```mermaid
flowchart TD
    Start["Application Start"] --> GetWD["Get Working Directory<br/>os.Getwd()"]
    GetWD --> LoadEnv["Load .env File<br/>godotenv.Load()"]
    LoadEnv --> CheckErr{".env file<br/>found?"}
    CheckErr -->|"Yes"| ParseEnv["Parse .env variables"]
    CheckErr -->|"No"| CheckNotExist{".env missing<br/>(ErrNotExist)?"}
    CheckNotExist -->|"Yes"| SystemEnv["Use system environment only"]
    CheckNotExist -->|"No"| LogWarn["Log warning about .env error"]
    ParseEnv --> SystemEnv
    LogWarn --> SystemEnv
    SystemEnv --> LookupVars["lookupEnv() function<br/>Checks uppercase & lowercase"]
    LookupVars --> ConfigBackend["Configure storage backend"]
    ConfigBackend --> LoadConfig["Load config.yaml"]
```

**Sources**: [cmd/server/main.go:155-177]()

---

## Storage Backend Selection

Environment variables primarily control which token storage backend is used. The selection follows a priority order:

### Priority Order

Title: Storage Backend Selection Logic
```mermaid
flowchart LR
    Check["Storage Backend<br/>Selection"] --> PG{PGSTORE_DSN<br/>set?}
    PG -->|"Yes"| UsePG["PostgresStore<br/>usePostgresStore = true"]
    PG -->|"No"| OBJ{OBJECTSTORE_ENDPOINT<br/>set?}
    OBJ -->|"Yes"| UseObj["ObjectTokenStore<br/>useObjectStore = true"]
    OBJ -->|"No"| GIT{GITSTORE_GIT_URL<br/>set?}
    GIT -->|"Yes"| UseGit["GitTokenStore<br/>useGitStore = true"]
    GIT -->|"No"| UseFile["FileTokenStore<br/>default"]
    
    UsePG --> Register["sdkAuth.RegisterTokenStore()"]
    UseObj --> Register
    UseGit --> Register
    UseFile --> Register
```

**Sources**: [cmd/server/main.go:179-225](), [cmd/server/main.go:446-454]()

---

## Environment Variable Reference

### Deployment Mode

| Variable | Values | Default | Purpose |
| :--- | :--- | :--- | :--- |
| `DEPLOY` | `cloud`, (unset) | (unset) | When set to `cloud`, enables cloud deploy mode where the service waits for configuration to be provided externally. If no `config.yaml` exists, the service enters standby mode instead of failing. |

**Behavior**: Cloud deploy mode is checked via `os.Getenv("DEPLOY")` and sets `isCloudDeploy = true` when the value is `"cloud"` [cmd/server/main.go:228-232](). When enabled and no valid configuration exists, the service enters a blocking state awaiting configuration via the Management API [cmd/server/main.go:399-417]().

**Sources**: [cmd/server/main.go:228-232](), [cmd/server/main.go:399-417]()

---

### PostgreSQL Storage Backend

| Variable | Type | Default | Purpose |
| :--- | :--- | :--- | :--- |
| `PGSTORE_DSN` or `pgstore_dsn` | Connection String | (unset) | PostgreSQL connection string. Presence of this variable enables `PostgresStore` backend. Example: `postgres://user:pass@host:5432/dbname` |
| `PGSTORE_SCHEMA` or `pgstore_schema` | String | (empty) | PostgreSQL schema name for token tables. |
| `PGSTORE_LOCAL_PATH` or `pgstore_local_path` | Directory Path | Current working directory or writable path | Local spool directory for PostgreSQL-backed storage workspace. Appends `/pgstore` suffix. |

**Initialization Flow**:

Title: PostgresStore Initialization Sequence
```mermaid
sequenceDiagram
    participant Main as "main.go"
    participant PG as "store.PostgresStore"
    participant FS as "File System"
    
    Main->>Main: Check PGSTORE_DSN env var
    Main->>Main: Set usePostgresStore = true
    Main->>Main: Determine pgStoreLocalPath
    Main->>Main: Append "/pgstore" suffix
    Main->>PG: NewPostgresStore(DSN, Schema, SpoolDir)
    PG->>PG: Connect to database
    PG-->>Main: Return pgStoreInst
    Main->>FS: Check config.example.yaml
    Main->>PG: Bootstrap(examplePath)
    PG->>PG: Create tables & initial config
    PG-->>Main: Success
    Main->>PG: ConfigPath()
    PG-->>Main: Path to config file
    Main->>Main: LoadConfigOptional(configPath)
    Main->>Main: sdkAuth.RegisterTokenStore(pgStoreInst)
```

**Implementation Detail**: The `PostgresStore` mirrors data to a local workspace so existing file-based workflows (like the file watcher) continue to operate [internal/store/postgresstore.go:37-38](). It automatically creates the necessary tables (`config_store` and `auth_store`) if they do not exist [internal/store/postgresstore.go:121-143]().

**Sources**: [cmd/server/main.go:179-198](), [cmd/server/main.go:237-266](), [internal/store/postgresstore.go:22-143](), [cmd/server/main.go:446-447]()

---

### Git Storage Backend

| Variable | Type | Default | Purpose |
| :--- | :--- | :--- | :--- |
| `GITSTORE_GIT_URL` or `gitstore_git_url` | Git URL | (unset) | Git repository URL for token storage. Presence enables `GitTokenStore`. Example: `https://github.com/user/repo.git` |
| `GITSTORE_GIT_USERNAME` or `gitstore_git_username` | String | (empty) | Git authentication username. |
| `GITSTORE_GIT_TOKEN` or `gitstore_git_token` | String | (empty) | Git authentication token or password. |
| `GITSTORE_LOCAL_PATH` or `gitstore_local_path` | Directory Path | Current working directory or writable path | Local clone directory for Git repository. Appends `/gitstore` suffix. |

**Initialization Flow**:

Title: GitTokenStore Initialization Sequence
```mermaid
sequenceDiagram
    participant Main as "main.go"
    participant Git as "store.GitTokenStore"
    participant FS as "File System"
    participant Repo as "Git Repository"
    
    Main->>Main: Check GITSTORE_GIT_URL env var
    Main->>Main: Set useGitStore = true
    Main->>Main: Determine gitStoreLocalPath
    Main->>Main: Append "/gitstore" suffix
    Main->>Git: NewGitTokenStore(url, user, password)
    Git-->>Main: Return gitStoreInst
    Main->>Git: EnsureRepository()
    Git->>Repo: Clone or pull repository
    Repo-->>Git: Ready
    Git-->>Main: Success
    Main->>Git: ConfigPath()
    Git-->>Main: Path to config.yaml
    alt Config file missing
        Main->>FS: Read config.example.yaml
        Main->>FS: Copy to gitStoreRoot/config/config.yaml
    end
    Main->>Main: LoadConfigOptional(configPath)
    Main->>Main: sdkAuth.RegisterTokenStore(gitStoreInst)
```

**Sources**: [cmd/server/main.go:199-209](), [cmd/server/main.go:334-377](), [cmd/server/main.go:450-451]()

---

### Object Storage Backend

| Variable | Type | Default | Purpose |
| :--- | :--- | :--- | :--- |
| `OBJECTSTORE_ENDPOINT` or `objectstore_endpoint` | URL/Hostname | (unset) | S3-compatible object storage endpoint. Presence enables `ObjectTokenStore`. |
| `OBJECTSTORE_ACCESS_KEY` or `objectstore_access_key` | String | (empty) | Object storage access key ID. |
| `OBJECTSTORE_SECRET_KEY` or `objectstore_secret_key` | String | (empty) | Object storage secret access key. |
| `OBJECTSTORE_BUCKET` or `objectstore_bucket` | String | (empty) | Bucket name for storing tokens and configuration. |
| `OBJECTSTORE_LOCAL_PATH` or `objectstore_local_path` | Directory Path | Current working directory or writable path | Local cache directory for object storage. Appends `/objectstore` suffix. |

**Endpoint Parsing Logic**:

The `OBJECTSTORE_ENDPOINT` variable supports flexible URL formats [cmd/server/main.go:276-302]():

Title: Object Storage Endpoint Parsing
```mermaid
flowchart TD
    Input["OBJECTSTORE_ENDPOINT value"] --> TrimSpace["Trim whitespace"]
    TrimSpace --> CheckScheme{"Contains<br/>'://'?"}
    CheckScheme -->|"Yes"| ParseURL["url.Parse()"]
    CheckScheme -->|"No"| DefaultSSL["useSSL = true<br/>Use bare hostname"]
    
    ParseURL --> CheckSchemeType{"Scheme type?"}
    CheckSchemeType -->|"http"| SetNoSSL["useSSL = false"]
    CheckSchemeType -->|"https"| SetSSL["useSSL = true"]
    CheckSchemeType -->|"other"| Error["Log error and exit"]
    
    SetNoSSL --> ExtractHost["Extract parsed.Host"]
    SetSSL --> ExtractHost
    ExtractHost --> CheckPath{"parsed.Path<br/>present?"}
    CheckPath -->|"Yes"| AppendPath["Append path to host"]
    CheckPath -->|"No"| UseHost["Use host only"]
    
    AppendPath --> TrimSlash["Trim trailing slash"]
    UseHost --> TrimSlash
    DefaultSSL --> TrimSlash
    
    TrimSlash --> Configure["ObjectStoreConfig{<br/>Endpoint, UseSSL,<br/>PathStyle: true}"]
```

**Sources**: [cmd/server/main.go:210-225](), [cmd/server/main.go:267-333](), [cmd/server/main.go:448-449]()

---

## Variable Name Lookup Function

CLIProxyAPI implements a case-insensitive lookup function that checks multiple variations of each environment variable name:

Title: lookupEnv Implementation
```mermaid
flowchart LR
    Lookup["lookupEnv(keys...)"] --> Loop["For each key in keys"]
    Loop --> CheckEnv["os.LookupEnv(key)"]
    CheckEnv --> Found{Value found<br/>and non-empty?}
    Found -->|"Yes"| Trim["strings.TrimSpace(value)"]
    Trim --> CheckTrimmed{Trimmed value<br/>non-empty?}
    CheckTrimmed -->|"Yes"| Return["Return (value, true)"]
    CheckTrimmed -->|"No"| Loop
    Found -->|"No"| Loop
    Loop -->|"All keys checked"| ReturnEmpty["Return ('', false)"]
```

**Implementation**: The `lookupEnv` function accepts multiple key names (e.g., `"PGSTORE_DSN", "pgstore_dsn"`) and returns the first non-empty trimmed value found [cmd/server/main.go:168-177]().

**Sources**: [cmd/server/main.go:168-177]()

---

## Storage Backend Registration

After determining which storage backend to use, the selected store is registered globally for use by all components:

Title: Global Store Registration
```mermaid
flowchart TD
    Start["Storage backend selected"] --> CheckPG{"usePostgresStore?"}
    CheckPG -->|"Yes"| RegPG["sdkAuth.RegisterTokenStore(<br/>pgStoreInst)"]
    CheckPG -->|"No"| CheckObj{"useObjectStore?"}
    CheckObj -->|"Yes"| RegObj["sdkAuth.RegisterTokenStore(<br/>objectStoreInst)"]
    CheckObj -->|"No"| CheckGit{"useGitStore?"}
    CheckGit -->|"Yes"| RegGit["sdkAuth.RegisterTokenStore(<br/>gitStoreInst)"]
    CheckGit -->|"No"| RegFile["sdkAuth.RegisterTokenStore(<br/>NewFileTokenStore())"]
    
    RegPG --> Global["Global store instance<br/>used by all auth operations"]
    RegObj --> Global
    RegGit --> Global
    RegFile --> Global
```

**Sources**: [cmd/server/main.go:446-454]()

---

## Writable Path Resolution

For storage backends requiring local directories, CLIProxyAPI determines a writable base path:

Title: Local Path Determination Logic
```mermaid
flowchart LR
    Start["Determine local path"] --> CheckEnvVar{"Environment variable<br/>specifies path?"}
    CheckEnvVar -->|"Yes"| UseEnvPath["Use specified path"]
    CheckEnvVar -->|"No"| CheckWritable{"util.WritablePath()<br/>returns path?"}
    CheckWritable -->|"Yes"| UseWritable["Use writable base path"]
    CheckWritable -->|"No"| UseWD["Use current working directory"]
    
    UseEnvPath --> AppendSuffix["Append storage-specific suffix<br/>/pgstore, /gitstore, /objectstore"]
    UseWritable --> AppendSuffix
    UseWD --> AppendSuffix
```

**Sources**: [cmd/server/main.go:178](), [cmd/server/main.go:188-194](), [cmd/server/main.go:268-274](), [cmd/server/main.go:336-341]()

---

## Complete Environment Variable Table

| Variable | Type | Default | Effect | Code Reference |
| :--- | :--- | :--- | :--- | :--- |
| `DEPLOY` | String | (unset) | When `"cloud"`, enables cloud deploy mode with config wait behavior | [cmd/server/main.go:229]() |
| `PGSTORE_DSN` | String | (unset) | PostgreSQL DSN; enables PostgreSQL storage backend | [cmd/server/main.go:179-182]() |
| `PGSTORE_SCHEMA` | String | (empty) | PostgreSQL schema for token tables | [cmd/server/main.go:184-186]() |
| `PGSTORE_LOCAL_PATH` | Path | `writable/pgstore` | Local spool directory for PostgreSQL workspace | [cmd/server/main.go:187-196]() |
| `GITSTORE_GIT_URL` | URL | (unset) | Git repository URL; enables Git storage backend | [cmd/server/main.go:199-202]() |
| `GITSTORE_GIT_USERNAME` | String | (empty) | Git authentication username | [cmd/server/main.go:203-205]() |
| `GITSTORE_GIT_TOKEN` | String | (empty) | Git authentication token/password | [cmd/server/main.go:206-208]() |
| `GITSTORE_LOCAL_PATH` | Path | `writable/gitstore` | Local clone directory for Git repository | [cmd/server/main.go:209](), [cmd/server/main.go:336-341]() |
| `OBJECTSTORE_ENDPOINT` | URL | (unset) | S3-compatible endpoint; enables object storage backend | [cmd/server/main.go:210-213]() |
| `OBJECTSTORE_ACCESS_KEY` | String | (empty) | Object storage access key ID | [cmd/server/main.go:214-216]() |
| `OBJECTSTORE_SECRET_KEY` | String | (empty) | Object storage secret key | [cmd/server/main.go:217-219]() |
| `OBJECTSTORE_BUCKET` | String | (empty) | Bucket name for tokens and config | [cmd/server/main.go:220-222]() |
| `OBJECTSTORE_LOCAL_PATH` | Path | `writable/objectstore` | Local cache directory for object storage | [cmd/server/main.go:223-225](), [cmd/server/main.go:268-274]() |

**Sources**: [cmd/server/main.go:179-232]()

---

# Page: Provider-Specific Configuration

# Provider-Specific Configuration

<details>
<summary>Relevant source files</summary>

The following files were used as context for generating this wiki page:

- [config.example.yaml](config.example.yaml)
- [internal/api/handlers/management/config_basic.go](internal/api/handlers/management/config_basic.go)
- [internal/api/handlers/management/config_lists.go](internal/api/handlers/management/config_lists.go)
- [internal/api/server.go](internal/api/server.go)
- [internal/config/config.go](internal/config/config.go)
- [internal/config/oauth_model_alias_test.go](internal/config/oauth_model_alias_test.go)
- [internal/config/vertex_compat.go](internal/config/vertex_compat.go)
- [internal/util/claude_model.go](internal/util/claude_model.go)
- [internal/util/claude_model_test.go](internal/util/claude_model_test.go)
- [internal/watcher/diff/oauth_model_alias.go](internal/watcher/diff/oauth_model_alias.go)
- [internal/watcher/synthesizer/config.go](internal/watcher/synthesizer/config.go)
- [internal/watcher/watcher.go](internal/watcher/watcher.go)
- [sdk/cliproxy/service.go](sdk/cliproxy/service.go)
- [test/amp_management_test.go](test/amp_management_test.go)

</details>



This page details configuration entries for each supported AI provider, including API key setup, model aliasing, exclusion lists, and provider-specific options. These configurations are defined in the `Config` struct and typically loaded from `config.yaml`.

## Configuration Architecture

Provider-specific configurations serve three primary purposes: API key management for direct provider access, model name aliasing to normalize client requests, and model exclusion to restrict access to specific models. The system utilizes a synthesizer pattern to transform static configuration entries into runtime `Auth` entities.

The following diagram maps the configuration structures in `internal/config/config.go` to the synthesis logic in `internal/watcher/synthesizer/config.go`.

**Data Flow: Config to Runtime Auth**

```mermaid
graph TB
    subgraph "Config Entity Space (internal/config/config.go)"
        Config["Config struct"]
        GeminiKeyCfg["GeminiKey struct"]
        ClaudeKeyCfg["ClaudeKey struct"]
        VertexKeyCfg["VertexCompatKey struct"]
        CodexKeyCfg["CodexKey struct"]
        OpenAICompatCfg["OpenAICompatibility struct"]
    end
    
    subgraph "Logic Space (internal/watcher/synthesizer/config.go)"
        Synthesizer["ConfigSynthesizer.Synthesize()"]
        SynGemini["synthesizeGeminiKeys()"]
        SynClaude["synthesizeClaudeKeys()"]
        SynVertex["synthesizeVertexCompat()"]
        SynCodex["synthesizeCodexKeys()"]
        SynOpenAI["synthesizeOpenAICompat()"]
    end
    
    subgraph "Runtime Entity Space (sdk/cliproxy/auth/auth.go)"
        AuthEntry["coreauth.Auth struct"]
    end
    
    Config --> GeminiKeyCfg & ClaudeKeyCfg & VertexKeyCfg & CodexKeyCfg & OpenAICompatCfg
    
    GeminiKeyCfg --> SynGemini
    ClaudeKeyCfg --> SynClaude
    VertexKeyCfg --> SynVertex
    CodexKeyCfg --> SynCodex
    OpenAICompatCfg --> SynOpenAI
    
    SynGemini & SynClaude & SynVertex & SynCodex & SynOpenAI --> Synthesizer
    Synthesizer --> AuthEntry
```
**Sources:** [internal/config/config.go:27-130](), [internal/watcher/synthesizer/config.go:14-40](), [sdk/cliproxy/auth/auth.go:1-50]()

---

## Gemini API Key Configuration

Gemini API keys are configured via the `gemini-api-key` array. Each entry supports custom base URLs, proxy settings, and wildcard-based model exclusions.

### Configuration Fields
Defined in `internal/config/config.go`:
- `api-key`: The Google AI Studio API key. [internal/config/config.go:89-89]()
- `base-url`: Custom endpoint (e.g., for regional proxies). [config.example.yaml:114-114]()
- `proxy-url`: Per-credential proxy string (supports `socks5`, `http`, `direct`). [config.example.yaml:116-118]()
- `excluded-models`: List of models to hide. Supports exact matches and wildcards (e.g., `gemini-2.5-*`). [config.example.yaml:122-126]()

**Sources:** [internal/config/config.go:88-89](), [internal/watcher/synthesizer/config.go:43-88](), [config.example.yaml:110-128]()

---

## Claude API Key Configuration

Claude API keys are managed via the `claude-api-key` list. The system supports a `ClaudeHeaderDefaults` global configuration to provide fallbacks for `User-Agent` and version headers if not supplied by the client. [internal/config/config.go:101-103]()

### Configuration Fields
- `api-key`: Anthropic API key. [internal/config/config.go:98-99]()
- `models`: Array of model objects for aliasing (e.g., mapping `claude-sonnet-latest` to an upstream version). [config.example.yaml:157-159]()
- `priority`: Integer value used by the routing logic to prefer certain keys. [internal/watcher/synthesizer/config.go:110-112]()

**Sources:** [internal/config/config.go:98-103](), [internal/watcher/synthesizer/config.go:91-136](), [config.example.yaml:147-168]()

---

## OpenAI-Compatible Providers

The `openai-compatibility` section allows integration with any provider following the OpenAI API specification (e.g., DeepSeek, Groq, Local LLMs).

### Model Pool Rotation
When multiple `models` entries share the same `alias`, they form a **model pool**. The `ConfigSynthesizer` calculates a `models_hash` to track changes in these pools during synthesis. [internal/watcher/synthesizer/config.go:224-226]()

### Configuration Fields
- `name`: Identifier for the provider (used in logs and metrics). [internal/watcher/synthesizer/config.go:198-201]()
- `api-key-entries`: A list of API key objects, allowing multiple keys for a single provider base URL. [internal/watcher/synthesizer/config.go:206-209]()

**Sources:** [internal/config/config.go:105-106](), [internal/watcher/synthesizer/config.go:189-247]()

---

## Vertex AI Compatibility

The `vertex-api-key` configuration (represented by `VertexCompatKey`) is designed for third-party services that mimic Vertex AI's endpoint structure (`/publishers/google/models/{model}:streamGenerateContent`) but use simple API keys instead of Google Cloud IAM service accounts. [internal/config/vertex_compat.go:5-10]()

### Sanitization Logic
The `SanitizeVertexCompatKeys` function normalizes these entries by trimming whitespace, normalizing prefixes, and deduplicating based on the combination of `APIKey` and `BaseURL`. [internal/config/vertex_compat.go:59-98]()

**Sources:** [internal/config/vertex_compat.go:11-53](), [internal/watcher/synthesizer/config.go:250-291]()

---

## Global OAuth Model Aliasing

The `OAuthModelAlias` system provides a way to map model names across different OAuth-backed "channels" (e.g., `gemini-cli`, `claude`, `codex`). This is configured via `oauth-model-alias` in the global config. [internal/config/config.go:118-124]()

### Channel Resolution Logic
The `OAuthModelAlias` is a map where keys are channel names. The system uses a synthesizer to generate hashes for change detection during hot-reloads. [internal/watcher/diff/oauth_model_alias.go:19-35]()

**Code Entity Space: OAuth Alias Resolution**

```mermaid
graph LR
    subgraph "Input (internal/config/config.go)"
        RawAlias["OAuthModelAlias struct"]
        AliasName["Name (Upstream)"]
        AliasVal["Alias (Client)"]
        ForkFlag["Fork (Boolean)"]
    end

    subgraph "Processing (internal/watcher/diff/oauth_model_alias.go)"
        Summarizer["summarizeOAuthModelAliasList()"]
        Hasher["SHA256 Hash Generation"]
    end

    subgraph "Detection (internal/watcher/diff/oauth_model_alias.go)"
        Diff["DiffOAuthModelAliasChanges()"]
    end

    RawAlias --> Summarizer
    AliasName & AliasVal & ForkFlag --> Summarizer
    Summarizer --> Hasher
    Hasher --> Diff
```
**Sources:** [internal/config/config.go:118-124](), [internal/watcher/diff/oauth_model_alias.go:19-35]()

---

## Global Model Exclusions

The `OAuthExcludedModels` field allows for global exclusions per provider type. These are applied to all OAuth or file-backed authentication entries. [internal/config/config.go:115-116]()

### Exclusion Application
During synthesis, the `ApplyAuthExcludedModelsMeta` function is called for each generated `Auth` entry. It merges the per-credential `excluded-models` with the global `oauth-excluded-models` for that specific provider. [internal/watcher/synthesizer/config.go:84-84](), [internal/watcher/synthesizer/config.go:132-132]()

**Sources:** [internal/config/config.go:115-116](), [internal/watcher/synthesizer/config.go:22-37]()

---

# Page: Provider Integration

# Provider Integration

<details>
<summary>Relevant source files</summary>

The following files were used as context for generating this wiki page:

- [README.md](README.md)
- [README_CN.md](README_CN.md)
- [README_JA.md](README_JA.md)
- [assets/bmoplus.png](assets/bmoplus.png)
- [assets/lingtrue.png](assets/lingtrue.png)
- [internal/runtime/executor/aistudio_executor.go](internal/runtime/executor/aistudio_executor.go)
- [internal/runtime/executor/antigravity_executor.go](internal/runtime/executor/antigravity_executor.go)
- [internal/runtime/executor/claude_executor.go](internal/runtime/executor/claude_executor.go)
- [internal/runtime/executor/codex_executor.go](internal/runtime/executor/codex_executor.go)
- [internal/runtime/executor/gemini_cli_executor.go](internal/runtime/executor/gemini_cli_executor.go)
- [internal/runtime/executor/gemini_executor.go](internal/runtime/executor/gemini_executor.go)
- [internal/runtime/executor/gemini_vertex_executor.go](internal/runtime/executor/gemini_vertex_executor.go)
- [internal/runtime/executor/iflow_executor.go](internal/runtime/executor/iflow_executor.go)
- [internal/runtime/executor/openai_compat_executor.go](internal/runtime/executor/openai_compat_executor.go)
- [internal/runtime/executor/qwen_executor.go](internal/runtime/executor/qwen_executor.go)

</details>



This guide covers the setup and integration of each AI service provider supported by CLIProxyAPI. The proxy supports multiple authentication methods and provider-specific features for each service.

---

## Supported Providers

CLIProxyAPI integrates with the following AI service providers:

| Provider | Authentication | Endpoint Type | Setup Guide |
|----------|---------------|---------------|-------------|
| **Google Gemini** | API Key, OAuth | Generative Language API | [Google Gemini and Vertex AI](#6.1) |
| **Gemini CLI** | OAuth | Cloud Code Assist | [Google Gemini and Vertex AI](#6.1) |
| **Vertex AI** | Service Account, API Key | Vertex AI API | [Google Gemini and Vertex AI](#6.1) |
| **Anthropic Claude** | API Key, OAuth | Messages API | [Anthropic Claude](#6.2) |
| **OpenAI Codex** | OAuth, API Key | Responses API | [OpenAI Codex](#6.3) |
| **Qwen** | OAuth Device Flow | OpenAI-compatible | [Qwen, iFlow, and Kimi](#6.4) |
| **iFlow** | OAuth, Cookie | OpenAI-compatible | [Qwen, iFlow, and Kimi](#6.4) |
| **Kimi** | OAuth | OpenAI-compatible | [Qwen, iFlow, and Kimi](#6.4) |
| **Antigravity** | OAuth | Gemini-compatible | [Antigravity and AI Studio](#6.5) |
| **AI Studio** | WebSocket Runtime | Gemini-compatible | [Antigravity and AI Studio](#6.5) |
| **OpenAI-compatible** | API Key | OpenAI-compatible | [OpenAI-Compatible Providers](#6.6) |

**Sources**: [internal/runtime/executor/gemini_executor.go:37-43](), [internal/runtime/executor/gemini_cli_executor.go:47-50](), [internal/runtime/executor/claude_executor.go:37-41](), [internal/runtime/executor/codex_executor.go:37-41](), [internal/runtime/executor/qwen_executor.go:171-175](), [internal/runtime/executor/iflow_executor.go:34-37](), [internal/runtime/executor/antigravity_executor.go:58-61](), [internal/runtime/executor/aistudio_executor.go:26-31](), [internal/runtime/executor/openai_compat_executor.go:23-29]()

---

## Provider Executor Architecture

Each provider is implemented as a `ProviderExecutor` that handles authentication, request translation, and API communication. The system uses specific executor classes to encapsulate the logic for different upstream protocols.

**Executor System Diagram**

```mermaid
classDiagram
    class ProviderExecutor {
        <<interface>>
        +Identifier() string
        +PrepareRequest(req, auth)
        +HttpRequest(ctx, auth, req)
        +Execute(ctx, auth, req, opts)
        +ExecuteStream(ctx, auth, req, opts)
    }
    
    class GeminiExecutor["GeminiExecutor<br/>(gemini_executor.go)"]
    class GeminiCLIExecutor["GeminiCLIExecutor<br/>(gemini_cli_executor.go)"]
    class ClaudeExecutor["ClaudeExecutor<br/>(claude_executor.go)"]
    class CodexExecutor["CodexExecutor<br/>(codex_executor.go)"]
    class AntigravityExecutor["AntigravityExecutor<br/>(antigravity_executor.go)"]
    class AIStudioExecutor["AIStudioExecutor<br/>(aistudio_executor.go)"]
    class QwenExecutor["QwenExecutor<br/>(qwen_executor.go)"]
    class IFlowExecutor["IFlowExecutor<br/>(iflow_executor.go)"]
    class OpenAICompatExecutor["OpenAICompatExecutor<br/>(openai_compat_executor.go)"]
    
    ProviderExecutor <|.. GeminiExecutor
    ProviderExecutor <|.. GeminiCLIExecutor
    ProviderExecutor <|.. ClaudeExecutor
    ProviderExecutor <|.. CodexExecutor
    ProviderExecutor <|.. AntigravityExecutor
    ProviderExecutor <|.. AIStudioExecutor
    ProviderExecutor <|.. QwenExecutor
    ProviderExecutor <|.. IFlowExecutor
    ProviderExecutor <|.. OpenAICompatExecutor
```

**Sources**: [internal/runtime/executor/gemini_executor.go:40-57](), [internal/runtime/executor/gemini_cli_executor.go:48-64](), [internal/runtime/executor/claude_executor.go:39-49](), [internal/runtime/executor/codex_executor.go:39-45](), [internal/runtime/executor/antigravity_executor.go:58-72](), [internal/runtime/executor/aistudio_executor.go:27-47](), [internal/runtime/executor/qwen_executor.go:173-179](), [internal/runtime/executor/iflow_executor.go:35-43](), [internal/runtime/executor/openai_compat_executor.go:26-37]()

---

## Common Request Flow

All providers follow a unified request execution pattern managed by the runtime. The `Execute` and `ExecuteStream` methods handle the heavy lifting of payload transformation and upstream communication.

**Request Execution Sequence**

```mermaid
sequenceDiagram
    participant Client
    participant Server as "internal/api/server.go"
    participant Manager as "auth.Manager"
    participant Translator as "sdk/translator"
    participant Executor as "ProviderExecutor"
    participant Provider as "AI Provider API"
    
    Client->>Server: "POST /v1/chat/completions"
    Server->>Manager: "Execute(providers, request)"
    
    Manager->>Translator: "TranslateRequest(source, target)"
    Translator-->>Manager: "Translated payload"
    
    Manager->>Executor: "Execute(ctx, auth, req, opts)"
    Executor->>Executor: "thinking.ApplyThinking()"
    Executor->>Executor: "PrepareRequest() (Inject Auth)"
    
    Executor->>Provider: "HTTP POST to Upstream"
    Provider-->>Executor: "Response Body"
    
    Executor->>Translator: "TranslateNonStream(target, source)"
    Translator-->>Executor: "Final Response Format"
    Executor-->>Manager: "Response + usage metadata"
    Manager-->>Server: "Response"
    Server-->>Client: "HTTP 200 + body"
```

**Sources**: [internal/runtime/executor/gemini_executor.go:105-178](), [internal/runtime/executor/claude_executor.go:93-182](), [internal/runtime/executor/codex_executor.go:80-148]()

---

## Authentication Methods

CLIProxyAPI supports multiple authentication methods depending on the provider, ranging from simple API keys to complex OAuth flows.

### OAuth 2.0 Flows

Many providers use OAuth2. The proxy handles the local callback server to capture tokens during the login process.

**OAuth Provider Configuration**:
- **Gemini CLI**: Uses Google OAuth with Client ID `681255809395-oo8ft2oprdrnp9e3aqf6av3hmdib135j.apps.googleusercontent.com` [internal/runtime/executor/gemini_cli_executor.go:37]().
- **Antigravity**: Uses Client ID `1071006060591-tmhssin2h21lcre235vtolojh4g403ep.apps.googleusercontent.com` [internal/runtime/executor/antigravity_executor.go:45]().

**OAuth Flow Implementation**

```mermaid
sequenceDiagram
    participant User
    participant CLI as "sdk/auth/Authenticator"
    participant OAuth as "OAuth Provider"
    participant Store as "TokenStore"
    
    User->>CLI: "cliproxy login {provider}"
    CLI->>CLI: "startCallbackServer(port)"
    CLI-->>User: "Open browser with authURL"
    
    User->>OAuth: "Approve access"
    OAuth-->>CLI: "Redirect to localhost:port?code=..."
    
    CLI->>OAuth: "ExchangeCodeForTokens(code)"
    OAuth-->>CLI: "access_token, refresh_token"
    
    CLI->>Store: "Persist Auth metadata"
    CLI-->>User: "Login successful"
```

**Sources**: [internal/runtime/executor/gemini_cli_executor.go:34-45](), [internal/runtime/executor/antigravity_executor.go:38-51]()

### API Key and Service Account Authentication

**API Keys**:
- **Gemini**: Injects `x-goog-api-key` [internal/runtime/executor/gemini_executor.go:66]().
- **Claude**: Injects `x-api-key` or `Authorization: Bearer` depending on the host [internal/runtime/executor/claude_executor.go:62-68]().

**Vertex AI Service Account**:
Vertex AI requires a Google Service Account JSON. The system generates access tokens for requests to `https://{region}-aiplatform.googleapis.com`.

**Sources**: [internal/runtime/executor/gemini_executor.go:60-74](), [internal/runtime/executor/claude_executor.go:52-75]()

---

## Request Translation

The proxy translates requests between different API formats using the `sdk/translator` package.

### Translation Pipeline

```mermaid
flowchart LR
    A["Client Request<br/>(e.g. OpenAI)"] --> B["TranslateRequest<br/>(Source → Target)"]
    B --> C["thinking.ApplyThinking"]
    C --> D["applyPayloadConfigWithRoot"]
    D --> E["Upstream API Call"]
    
    F["Upstream Response"] --> G["TranslateNonStream<br/>(Target → Source)"]
    G --> H["Client Response"]
```

**Sources**: [internal/runtime/executor/gemini_executor.go:117-135](), [internal/runtime/executor/claude_executor.go:107-130](), [internal/runtime/executor/openai_compat_executor.go:84-109]()

---

## Provider-Specific Details

### Google Gemini and Vertex AI (6.1)
Covers the official Google Generative Language API, the Cloud Code Assist (Gemini CLI) endpoint, and enterprise Vertex AI.
- **Gemini CLI**: Uses `https://cloudcode-pa.googleapis.com` [internal/runtime/executor/gemini_cli_executor.go:35]().
For details, see [Google Gemini and Vertex AI](#6.1).

### Anthropic Claude (6.2)
Integrates with the Anthropic Messages API. Supports automatic prompt caching injection (`cache_control`) and "thinking" mode for models like Claude 3.7.
- **Thinking**: Injects thinking configuration into the translated payload via `thinking.ApplyThinking` [internal/runtime/executor/claude_executor.go:124]().
For details, see [Anthropic Claude](#6.2).

### OpenAI Codex (6.3)
Integrates with the ChatGPT `backend-api/codex/responses` endpoint. Uses OAuth tokens obtained via device flow or web login.
- **Endpoint**: `https://chatgpt.com/backend-api/codex` [internal/runtime/executor/codex_executor.go:88]().
For details, see [OpenAI Codex](#6.3).

### Qwen, iFlow, and Kimi (6.4)
Focuses on Chinese AI providers that often use OpenAI-compatible interfaces but require specialized authentication (like Qwen's 60 req/min rate limiting).
- **Qwen Rate Limit**: Implements a sliding window rate limiter [internal/runtime/executor/qwen_executor.go:47-120]().
For details, see [Qwen, iFlow, and Kimi](#6.4).

### Antigravity and AI Studio (6.5)
Covers internal Google experimental providers. AI Studio uses a unique WebSocket-based relay (`wsrelay`) to proxy requests through a browser or local agent.
- **AI Studio Relay**: Uses `relay.NonStream` and `relay.Stream` [internal/runtime/executor/aistudio_executor.go:89-209]().
For details, see [Antigravity and AI Studio](#6.5).

### OpenAI-Compatible Providers (6.6)
A generic executor for any provider following the OpenAI spec (e.g., DeepSeek, OpenRouter, Groq).
- **Configuration**: Requires a `base_url` and `api_key` in the auth attributes [internal/runtime/executor/openai_compat_executor.go:78-82]().
For details, see [OpenAI-Compatible Providers](#6.6).

---

# Page: Google Gemini and Vertex AI

# Google Gemini and Vertex AI

<details>
<summary>Relevant source files</summary>

The following files were used as context for generating this wiki page:

- [internal/api/handlers/management/auth_files.go](internal/api/handlers/management/auth_files.go)
- [internal/auth/claude/token.go](internal/auth/claude/token.go)
- [internal/auth/codex/token.go](internal/auth/codex/token.go)
- [internal/auth/gemini/gemini_token.go](internal/auth/gemini/gemini_token.go)
- [internal/auth/iflow/iflow_token.go](internal/auth/iflow/iflow_token.go)
- [internal/auth/kimi/token.go](internal/auth/kimi/token.go)
- [internal/auth/qwen/qwen_token.go](internal/auth/qwen/qwen_token.go)
- [internal/cmd/antigravity_login.go](internal/cmd/antigravity_login.go)
- [internal/config/vertex_compat.go](internal/config/vertex_compat.go)
- [internal/misc/credentials.go](internal/misc/credentials.go)
- [internal/watcher/synthesizer/config.go](internal/watcher/synthesizer/config.go)
- [sdk/auth/gemini.go](sdk/auth/gemini.go)
- [sdk/auth/interfaces.go](sdk/auth/interfaces.go)
- [sdk/auth/manager.go](sdk/auth/manager.go)
- [sdk/auth/qwen.go](sdk/auth/qwen.go)

</details>



This page documents integration with Google Gemini and Vertex AI services, including authentication methods, executor implementations, OAuth flows, and provider-specific features. CLIProxyAPI supports multiple Gemini access patterns: API key-based Generative Language API, OAuth-based Gemini CLI (Cloud Code Assist), Vertex AI with service accounts or API keys, Antigravity (internal Google service), and WebSocket-based AI Studio.

For general provider integration concepts, see [Provider Integration](). For authentication management, see [Authentication Flows](). For OAuth-specific setup across all providers, see [Provider-Specific OAuth Setup]().

---

## Authentication Methods

CLIProxyAPI supports five distinct authentication patterns for accessing Google Gemini models, each with different endpoints, capabilities, and credential requirements.

### Authentication Pattern Overview

The following diagram bridges the natural language space of authentication methods to the specific code entities (Executors and Endpoints) used in the implementation.

```mermaid
graph TB
    subgraph "Authentication Methods"
        APIKey["API Key<br/>(Generative Language API)"]
        OAuth["OAuth Bearer Token<br/>(Gemini CLI)"]
        ServiceAccount["Service Account<br/>(Vertex AI)"]
        VertexAPIKey["Vertex API Key<br/>(Vertex AI)"]
        WebSocket["WebSocket Channel<br/>(AI Studio)"]
    end
    
    subgraph "Executors (Code Space)"
        GeminiExec["GeminiExecutor<br/>internal/runtime/executor/gemini_executor.go"]
        GeminiCLIExec["GeminiCLIExecutor<br/>internal/runtime/executor/gemini_cli_executor.go"]
        VertexExec["GeminiVertexExecutor<br/>internal/runtime/executor/gemini_vertex_executor.go"]
        AntigravityExec["AntigravityExecutor<br/>internal/runtime/executor/antigravity_executor.go"]
        AIStudioExec["AIStudioExecutor<br/>internal/runtime/executor/aistudio_executor.go"]
    end
    
    subgraph "Endpoints"
        GenLangAPI["generativelanguage.googleapis.com<br/>/v1beta/models"]
        CloudCodeAPI["cloudcode-pa.googleapis.com<br/>/v1internal"]
        VertexAPI["{location}-aiplatform.googleapis.com<br/>/v1/projects/{project}/locations"]
        AntigravityAPI["cloudcode-pa.googleapis.com<br/>/v1internal (Antigravity)"]
        WSRelay["WebSocket Relay<br/>wsrelay.Manager"]
    end
    
    APIKey --> GeminiExec
    OAuth --> GeminiCLIExec
    ServiceAccount --> VertexExec
    VertexAPIKey --> VertexExec
    WebSocket --> AIStudioExec
    OAuth --> AntigravityExec
    
    GeminiExec --> GenLangAPI
    GeminiCLIExec --> CloudCodeAPI
    VertexExec --> VertexAPI
    AntigravityExec --> AntigravityAPI
    AIStudioExec --> WSRelay
```

**Sources:** [internal/api/handlers/management/auth_files.go:46-52](), [internal/auth/gemini/gemini_token.go:20-42](), [internal/watcher/synthesizer/config.go:43-88]()

### API Key Authentication (Generative Language API)

The `GeminiExecutor` uses API keys for the official Generative Language API. API keys are configured in `config.yaml` under `gemini-key` and synthesized into `Auth` entries.

| Feature | Value |
|---------|-------|
| Endpoint | `https://generativelanguage.googleapis.com` |
| API Version | `v1beta` |
| Header | `x-goog-api-key` |
| Identifier | `gemini` |

The `ConfigSynthesizer` generates these entries using `synthesizeGeminiKeys` [internal/watcher/synthesizer/config.go:43-88](). It extracts the `APIKey`, `Prefix`, `BaseURL`, and `ProxyURL` from the configuration.

**Sources:** [internal/watcher/synthesizer/config.go:43-88](), [internal/auth/gemini/gemini_token.go:20-42]()

### OAuth Bearer Token (Gemini CLI)

The `GeminiCLIExecutor` uses OAuth tokens obtained via Google Cloud Platform authentication. This pattern requires project ID association and supports multi-project configurations.

| Feature | Value |
|---------|-------|
| Endpoint | `https://cloudcode-pa.googleapis.com` |
| API Version | `v1internal` |
| OAuth Client ID | `681255809395-oo8ft2oprdrnp9e3aqf6av3hmdib135j.apps.googleusercontent.com` |
| Scopes | `cloud-platform`, `userinfo.email` |
| Identifier | `gemini-cli` |

Tokens are stored in `GeminiTokenStorage` [internal/auth/gemini/gemini_token.go:20-42](). The storage maintains compatibility with the existing auth system while adding Gemini-specific fields for managing access tokens and project information.

**Sources:** [internal/auth/gemini/gemini_token.go:20-42](), [internal/api/handlers/management/auth_files.go:50-51]()

### Service Account (Vertex AI)

The `GeminiVertexExecutor` supports Google Cloud service account credentials. Service account JSON is typically stored in auth metadata.

| Feature | Value |
|---------|-------|
| Endpoint | `https://{location}-aiplatform.googleapis.com` |
| API Version | `v1` |
| Identifier | `vertex` |

**Sources:** [internal/config/vertex_compat.go:11-40](), [internal/watcher/synthesizer/config.go:195-230]()

---

## Executor Architecture

### Gemini CLI Token Management

The `GeminiTokenStorage` struct manages the persistence of OAuth2 credentials.

| Field | Description |
|-------|-------------|
| `Token` | Raw OAuth2 token data (access/refresh) |
| `ProjectID` | Associated Google Cloud Project ID |
| `Email` | Authenticated user email |
| `Type` | Always set to `"gemini"` |

The `SaveTokenToFile` method [internal/auth/gemini/gemini_token.go:59-87]() handles the serialization, ensuring the directory structure exists and merging any additional metadata using the `misc.MergeMetadata` helper [internal/misc/credentials.go:30-61]().

**Sources:** [internal/auth/gemini/gemini_token.go:20-42](), [internal/auth/gemini/gemini_token.go:59-87](), [internal/misc/credentials.go:30-61]()

### Vertex Compatibility

CLIProxyAPI supports third-party services that use Vertex AI-style endpoint paths but authenticate with simple API keys. This is configured via `VertexCompatKey` [internal/config/vertex_compat.go:11-40]().

The `ConfigSynthesizer` processes these in `synthesizeVertexCompat` [internal/watcher/synthesizer/config.go:195-230](), generating `Auth` entries with the provider set to `vertex-compatibility`. The `SanitizeVertexCompatKeys` function [internal/config/vertex_compat.go:59-98]() ensures deduplication and normalization of these keys during configuration loading.

**Sources:** [internal/config/vertex_compat.go:11-40](), [internal/config/vertex_compat.go:59-98](), [internal/watcher/synthesizer/config.go:195-230]()

---

## OAuth Flow and Project Onboarding

### Gemini CLI Login and Onboarding

The login process for Gemini CLI accounts is managed by the `GeminiAuthenticator` [sdk/auth/gemini.go:15-73]().

```mermaid
sequenceDiagram
    participant User
    participant Auth as GeminiAuthenticator<br/>sdk/auth/gemini.go
    participant GA as GeminiAuth<br/>internal/auth/gemini
    participant Browser
    participant Google as Google OAuth
    participant Storage as GeminiTokenStorage
    
    User->>Auth: Login(ctx, cfg, opts)
    Auth->>GA: GetAuthenticatedClient(ctx, ts, cfg, loginOpts)
    GA->>Browser: Open OAuth URL
    Browser->>Google: User Authorizes
    Google-->>GA: Auth Code
    GA->>Google: Exchange Code for Tokens
    GA-->>Auth: Authenticated Client
    Auth->>Storage: Populate Token, Email, ProjectID
    Auth-->>User: Return Auth Object
```

The `Login` method [sdk/auth/gemini.go:30-73]() initializes a `GeminiTokenStorage` and uses the `internal/auth/gemini` package to perform the OAuth exchange. It then constructs a filename using `CredentialFileName` [internal/auth/gemini/gemini_token.go:93-104]() for persistence.

**Sources:** [sdk/auth/gemini.go:30-73](), [internal/auth/gemini/gemini_token.go:93-104]()

### Callback Forwarding

To facilitate OAuth flows in various environments (like WebUI mode), the system uses a `callbackForwarder` [internal/api/handlers/management/auth_files.go:54-62]().

The `startCallbackForwarder` function [internal/api/handlers/management/auth_files.go:133-191]() creates a temporary HTTP server on a specific port (e.g., `8085` for Gemini [internal/api/handlers/management/auth_files.go:48]()) that redirects incoming requests to a target base URL, preserving query parameters.

**Sources:** [internal/api/handlers/management/auth_files.go:48](), [internal/api/handlers/management/auth_files.go:133-191]()

---

## Persistence and Storage

### Token Serialization

Credentials and metadata are persisted using specific storage implementations. For Gemini, the `GeminiTokenStorage` implements `SaveTokenToFile` [internal/auth/gemini/gemini_token.go:59-87]().

| Provider | Storage Struct | Implementation Site |
|----------|----------------|---------------------|
| Gemini | `GeminiTokenStorage` | [internal/auth/gemini/gemini_token.go:20]() |
| Kimi | `KimiTokenStorage` | [internal/auth/kimi/token.go:17]() |
| Qwen | `QwenTokenStorage` | [internal/auth/qwen/qwen_token.go:18]() |
| Claude | `ClaudeTokenStorage` | [internal/auth/claude/token.go:18]() |
| Codex | `CodexTokenStorage` | [internal/auth/codex/token.go:18]() |

Each implementation uses `misc.LogSavingCredentials` [internal/misc/credentials.go:16-22]() to provide consistent logging during the persistence process.

**Sources:** [internal/auth/gemini/gemini_token.go:59-87](), [internal/auth/kimi/token.go:82-110](), [internal/auth/qwen/qwen_token.go:54-79](), [internal/misc/credentials.go:16-22]()

### Metadata Merging

The `misc.MergeMetadata` helper [internal/misc/credentials.go:30-61]() is used extensively by provider-specific storage implementations to combine struct fields with dynamic metadata before serialization. This ensures that JSON tags are respected by marshaling to a temporary map if the source is not already a map [internal/misc/credentials.go:41-48]().

**Sources:** [internal/misc/credentials.go:30-61](), [internal/auth/gemini/gemini_token.go:63-66]()

---

# Page: Anthropic Claude

# Anthropic Claude

<details>
<summary>Relevant source files</summary>

The following files were used as context for generating this wiki page:

- [internal/auth/antigravity/auth.go](internal/auth/antigravity/auth.go)
- [internal/auth/claude/anthropic_auth.go](internal/auth/claude/anthropic_auth.go)
- [internal/auth/claude/utls_transport.go](internal/auth/claude/utls_transport.go)
- [internal/auth/codex/filename.go](internal/auth/codex/filename.go)
- [internal/auth/codex/openai_auth.go](internal/auth/codex/openai_auth.go)
- [internal/auth/codex/openai_auth_test.go](internal/auth/codex/openai_auth_test.go)
- [internal/auth/gemini/gemini_auth.go](internal/auth/gemini/gemini_auth.go)
- [internal/auth/qwen/qwen_auth.go](internal/auth/qwen/qwen_auth.go)
- [internal/cmd/openai_device_login.go](internal/cmd/openai_device_login.go)
- [internal/misc/claude_code_instructions.txt](internal/misc/claude_code_instructions.txt)
- [internal/misc/oauth.go](internal/misc/oauth.go)
- [internal/runtime/executor/cloak_obfuscate.go](internal/runtime/executor/cloak_obfuscate.go)
- [internal/runtime/executor/cloak_utils.go](internal/runtime/executor/cloak_utils.go)
- [sdk/auth/antigravity.go](sdk/auth/antigravity.go)
- [sdk/auth/claude.go](sdk/auth/claude.go)
- [sdk/auth/codex.go](sdk/auth/codex.go)
- [sdk/auth/codex_device.go](sdk/auth/codex_device.go)
- [sdk/auth/iflow.go](sdk/auth/iflow.go)

</details>



This page documents Claude integration in CLIProxyAPI, covering OAuth 2.0 authentication, API key configuration, and the specialized transport layer implementation designed to support high-performance CLI tools.

## Overview

CLIProxyAPI supports Anthropic Claude through a unified interface that handles both standard API keys and modern OAuth 2.0 flows. The integration is designed to support tools like Claude Code by implementing specific TLS fingerprinting bypasses and header management.

| Feature | Implementation | Purpose |
|----------|----------|----------------|
| **OAuth 2.0** | `ClaudeAuthenticator` | Interactive login with PKCE support |
| **TLS Bypass** | `utlsRoundTripper` | Mimics Chrome fingerprint to bypass Cloudflare |
| **Antigravity** | `AntigravityAuthenticator` | GCP-based Claude routing with Project ID support |
| **Token Refresh** | `RefreshLead` | Proactive credential rotation |

**Sources:** [sdk/auth/claude.go:20-31](), [internal/auth/claude/utls_transport.go:18-29]()

## Authentication Setup

CLIProxyAPI provides an interactive login flow for Claude that manages the complexity of PKCE (Proof Key for Code Exchange) and local callback handling.

### OAuth Flow Architecture

The authentication process utilizes a local temporary server to capture the authorization code redirected from Anthropic's console.

```mermaid
sequenceDiagram
    participant CLI as "CLI/SDK Manager"
    participant Auth as "ClaudeAuthenticator<br/>sdk/auth/claude.go"
    participant Svc as "ClaudeAuth Service<br/>internal/auth/claude"
    participant Local as "OAuthServer<br/>:54545"
    participant Browser as "System Browser"
    participant Anthropic as "Anthropic Console"

    CLI->>Auth: Login(ctx, cfg, opts)
    Auth->>Svc: GeneratePKCECodes()
    Auth->>Local: Start()
    Auth->>Svc: GenerateAuthURL(state, pkce)
    Auth->>Browser: OpenURL(authURL)
    
    Browser->>Anthropic: User Authorizes
    Anthropic-->>Browser: Redirect to localhost:54545
    Browser->>Local: GET /callback?code=...
    Local-->>Auth: OAuthResult{Code}
    
    Auth->>Svc: ExchangeCodeForTokens(code, pkce)
    Svc-->>Auth: AuthBundle{AccessToken, RefreshToken}
    Auth->>Svc: CreateTokenStorage(bundle)
    Auth-->>CLI: Auth Record (JSON)
```

**Key Components:**
- **PKCE Generation:** Generates cryptographically secure `code_verifier` and `code_challenge` [sdk/auth/claude.go:54-57]().
- **State Validation:** Uses a random hex string to prevent CSRF attacks [sdk/auth/claude.go:59-62]().
- **Callback Handling:** Defaults to port `54545` for the local listener [sdk/auth/claude.go:27-28]().
- **Token Persistence:** Saves credentials to `claude-{email}.json` [sdk/auth/claude.go:203-206]().

**Sources:** [sdk/auth/claude.go:38-220](), [internal/misc/oauth.go:17-23](), [internal/auth/claude/anthropic_auth.go:81-98]()

### Manual Callback Support
If the browser cannot open automatically (e.g., in an SSH session), the system prints instructions for an SSH tunnel and provides an asynchronous prompt to manually paste the callback URL [sdk/auth/claude.go:87-101](), [sdk/auth/claude.go:155-158]().

## Transport Layer (uTLS)

To ensure compatibility and avoid detection by anti-bot measures (like Cloudflare TLS fingerprinting), CLIProxyAPI uses a specialized HTTP transport for Anthropic domains.

### Chrome Fingerprint Mimicry
The `utlsRoundTripper` uses the `refraction-networking/utls` library to mimic a Chrome browser's TLS handshake. This is critical for tools that need to appear as legitimate user agents.

```mermaid
graph TD
    subgraph "Transport_Entity_Space"
        Client["http.Client<br/>internal/auth/claude/utls_transport.go:158"]
        RT["utlsRoundTripper_struct<br/>internal/auth/claude/utls_transport.go:20"]
        ConnMap["connections_map[string]*http2.ClientConn<br/>internal/auth/claude/utls_transport.go:24"]
    end

    subgraph "Connection_Logic"
        GetConn["getOrCreateConnection<br/>internal/auth/claude/utls_transport.go:53"]
        CreateConn["createConnection<br/>internal/auth/claude/utls_transport.go:101"]
        UClient["tls.UClient(...,_HelloChrome_Auto)<br/>internal/auth/claude/utls_transport.go:108"]
    end

    Client --> RT
    RT --> GetConn
    GetConn -->|"Cache_Miss"| CreateConn
    CreateConn --> UClient
    GetConn -->|"Cache_Hit"| ConnMap
```

**Implementation Details:**
- **HTTP/2 Support:** Explicitly creates `http2.ClientConn` to ensure modern protocol performance [internal/auth/claude/utls_transport.go:116-122]().
- **Concurrency Safety:** Uses a per-host `sync.Cond` in the `pending` map to prevent "thundering herd" issues where multiple goroutines try to dial the same host simultaneously [internal/auth/claude/utls_transport.go:63-77]().
- **Proxy Integration:** Supports upstream proxies via `proxyutil.BuildDialer` [internal/auth/claude/utls_transport.go:35-41]().

**Sources:** [internal/auth/claude/utls_transport.go:1-163]()

## Antigravity Integration

The "Antigravity" provider is a specialized bridge for Claude models, often used for enterprise or research environments that require GCP project-based routing.

### Project ID Resolution
Unlike standard Claude, Antigravity requires a Google Cloud Project ID. The authenticator automatically attempts to resolve this via the `loadCodeAssist` endpoint after a successful OAuth flow.

```mermaid
graph LR
    subgraph "Code_Entity:_AntigravityAuth"
        Login["Login<br/>sdk/auth/antigravity.go:35"]
        Exch["ExchangeCodeForTokens<br/>internal/auth/antigravity/auth.go:67"]
        FetchProj["FetchProjectID<br/>internal/auth/antigravity/auth.go:155"]
    end

    subgraph "External_API"
        GCP["GCP_OAuth_Endpoint"]
        CA["loadCodeAssist_API"]
    end

    Login --> Exch
    Exch --> GCP
    Login --> FetchProj
    FetchProj --> CA
```

**Metadata Fields:**
- `project_id`: Extracted from the GCP environment via `FetchProjectID` [sdk/auth/antigravity.go:178-185]().
- `access_token` / `refresh_token`: Standard OAuth tokens returned by `ExchangeCodeForTokens` [sdk/auth/antigravity.go:190-191]().

**Sources:** [sdk/auth/antigravity.go:166-202](), [internal/auth/antigravity/auth.go:155-200]()

## Token Management

### Refresh Logic
Claude tokens have a relatively short lifespan. The system implements a proactive refresh mechanism.

- **Refresh Lead:** The `ClaudeAuthenticator` requests a refresh 4 hours before the token actually expires [sdk/auth/claude.go:34-36]().
- **Antigravity Refresh:** The `AntigravityAuthenticator` triggers a refresh 5 minutes before expiry [sdk/auth/antigravity.go:29-32]().

### Credential Storage
Tokens are stored in a standardized JSON format.
- **Claude:** `claude-{email}.json` [sdk/auth/claude.go:203]().
- **Antigravity:** Uses `antigravity.CredentialFileName(email)` to generate the filename [sdk/auth/antigravity.go:203]().

**Sources:** [sdk/auth/claude.go:30-36](), [sdk/auth/antigravity.go:203-219]()

---

# Page: OpenAI Codex

# OpenAI Codex

<details>
<summary>Relevant source files</summary>

The following files were used as context for generating this wiki page:

- [internal/auth/claude/anthropic_auth.go](internal/auth/claude/anthropic_auth.go)
- [internal/auth/codex/openai_auth.go](internal/auth/codex/openai_auth.go)
- [internal/auth/codex/openai_auth_test.go](internal/auth/codex/openai_auth_test.go)
- [internal/auth/qwen/qwen_auth.go](internal/auth/qwen/qwen_auth.go)
- [internal/cmd/openai_device_login.go](internal/cmd/openai_device_login.go)
- [internal/misc/header_utils.go](internal/misc/header_utils.go)
- [internal/runtime/executor/codex_executor_cache_test.go](internal/runtime/executor/codex_executor_cache_test.go)
- [internal/runtime/executor/codex_websockets_executor.go](internal/runtime/executor/codex_websockets_executor.go)
- [internal/runtime/executor/codex_websockets_executor_test.go](internal/runtime/executor/codex_websockets_executor_test.go)
- [internal/translator/codex/openai/chat-completions/codex_openai_request.go](internal/translator/codex/openai/chat-completions/codex_openai_request.go)
- [internal/translator/codex/openai/chat-completions/codex_openai_request_test.go](internal/translator/codex/openai/chat-completions/codex_openai_request_test.go)
- [internal/translator/codex/openai/responses/codex_openai-responses_request.go](internal/translator/codex/openai/responses/codex_openai-responses_request.go)
- [internal/translator/codex/openai/responses/codex_openai-responses_request_test.go](internal/translator/codex/openai/responses/codex_openai-responses_request_test.go)
- [internal/translator/codex/openai/responses/codex_openai-responses_response.go](internal/translator/codex/openai/responses/codex_openai-responses_response.go)
- [sdk/auth/codex_device.go](sdk/auth/codex_device.go)

</details>



This page provides a setup guide for authenticating with OpenAI Codex (ChatGPT backend API) using OAuth flows. Codex authentication enables access to GPT-5, GPT-4.1, GPT-4o, and other models available through ChatGPT subscriptions.

For the technical executor architecture, see page 3.4. For OAuth flow details across providers, see page 7.1. For credential management, see page 7.3.

## Overview

OpenAI Codex refers to ChatGPT's backend API at `https://chatgpt.com/backend-api/codex`, which provides programmatic access to ChatGPT models. Authentication uses OAuth 2.0 with two supported flows:

- **Authorization Code Flow with PKCE** (default): Opens browser for user login, suitable for desktop/development environments. [internal/auth/codex/openai_auth.go:48-68]()
- **Device Flow** (alternative): Displays user code for manual activation, suitable for headless/server environments. [sdk/auth/codex_device.go:64-126]()

Both flows obtain OAuth tokens that are stored in the `auth-dir` as JSON files and automatically refreshed by the system. [internal/auth/codex/openai_auth.go:149-165]()

**Codex Authentication Entry Points**

```mermaid
graph TB
    CLI["CLI Proxy Entry"]
    Authenticator["CodexAuthenticator<br/>(sdk/auth/codex.go)"]
    
    subgraph "OAuth Flows"
        PKCE["Authorization Code + PKCE<br/>loginWithPKCE()"]
        Device["Device Flow<br/>loginWithDeviceFlow()"]
    end
    
    subgraph "Backend Services"
        CodexAuth["codex.CodexAuth<br/>(internal/auth/codex/openai_auth.go)"]
        TokenStore["Token Store<br/>(auth-dir/codex-*.json)"]
    end
    
    CLI --> Authenticator
    Authenticator --> PKCE
    Authenticator --> Device
    
    PKCE --> CodexAuth
    Device --> CodexAuth
    
    CodexAuth --> TokenStore
```

Sources: [internal/auth/codex/openai_auth.go:33-43](), [sdk/auth/codex_device.go:64-75]()

## Account Tiers

Codex authentication provides access to models based on your ChatGPT subscription tier. The tier information is extracted from the ID token JWT claims during the token exchange. [internal/auth/codex/openai_auth.go:136-147]()

**ChatGPT Account Tiers**

| Tier | Plan Type | Filename Suffix |
|------|-----------|-----------------|
| Free | `free` | (none) |
| Team | `team` | `-team` |
| Plus | `plus` | `-plus` |

The system uses the `planType` and `AccountID` to disambiguate stored credentials for users with multiple subscriptions. [internal/auth/codex/openai_auth.go:150-157]()

Sources: [internal/auth/codex/openai_auth.go:150-157]()

## OAuth Setup: Authorization Code Flow with PKCE

The default method uses OAuth 2.0 with PKCE (Proof Key for Code Exchange). This flow opens a browser for user authentication. [internal/auth/codex/openai_auth.go:48-68]()

### Setup Steps

1. **Initiate Login**: The system generates PKCE codes (Challenge and Verifier). [internal/auth/codex/openai_auth.go:48-51]()
2. **Browser Authentication**: `CodexAuth.GenerateAuthURL` constructs the authorization URL with the `code_challenge`. [internal/auth/codex/openai_auth.go:53-67]()
3. **Token Exchange**: Upon callback, `ExchangeCodeForTokens` performs a POST request to the token endpoint with the `code_verifier`. [internal/auth/codex/openai_auth.go:80-104]()

**Authorization Code Flow with PKCE Sequence**

```mermaid
sequenceDiagram
    participant User
    participant Auth["CodexAuthenticator"]
    participant Codex["OpenAI Auth Service"]
    
    User->>Auth: Start Login
    Auth->>Codex: GenerateAuthURL(pkce)
    Auth->>User: Open Browser / Show URL
    User->>Codex: Login & Authorize
    Codex->>Auth: Redirect with ?code=...
    Auth->>Codex: ExchangeCodeForTokens(code, verifier)
    Codex-->>Auth: Access/Refresh/ID Tokens
    Auth->>User: Authentication Successful
```

Sources: [internal/auth/codex/openai_auth.go:48-104]()

## OAuth Setup: Device Flow

The Device Flow allows authentication on headless systems where a local browser is unavailable. [sdk/auth/codex_device.go:64-67]()

### Device Flow Steps

1. **Request User Code**: The client requests a device code from `https://auth.openai.com/api/accounts/deviceauth/usercode`. [sdk/auth/codex_device.go:128-141]()
2. **User Activation**: The user is instructed to visit `https://auth.openai.com/codex/device` and enter the provided code. [sdk/auth/codex_device.go:88-90]()
3. **Polling**: The client polls `https://auth.openai.com/api/accounts/deviceauth/token` until the user completes activation. [sdk/auth/codex_device.go:171-197]()
4. **Exchange**: Once activated, the service returns an `authorization_code` which is exchanged for final tokens using `ExchangeCodeForTokensWithRedirect`. [sdk/auth/codex_device.go:112-123]()

Sources: [sdk/auth/codex_device.go:27-31](), [sdk/auth/codex_device.go:64-126]()

## Token Storage and Refresh

### Auth File Persistence

Credentials are saved as JSON files containing the `AccessToken`, `RefreshToken`, and `IDToken`. [internal/auth/codex/openai_auth.go:150-157]()

### Automatic Token Refresh

The `RefreshTokens` function sends a `grant_type: refresh_token` request to OpenAI's token endpoint (`https://auth.openai.com/oauth/token`). [internal/auth/codex/openai_auth.go:171-185]()

```mermaid
graph LR
    Refresh["RefreshTokens()<br/>(internal/auth/codex/openai_auth.go)"]
    TokenURL["auth.openai.com/oauth/token"]
    Update["Update CodexTokenData"]
    
    Refresh --> TokenURL
    TokenURL --> Update
```

Sources: [internal/auth/codex/openai_auth.go:25](), [internal/auth/codex/openai_auth.go:171-190]()

## Request Translation

The system translates OpenAI-compatible requests into the format required by the Codex `/responses` API. [internal/translator/codex/openai/responses/codex_openai-responses_request.go:11-12]()

### Request Transformation (`ConvertOpenAIResponsesRequestToCodex`)

The translator applies several mutations to the raw JSON:

1. **Input Normalization**: If the input is a string, it is converted into a structured message array. [internal/translator/codex/openai/responses/codex_openai-responses_request.go:14-18]()
2. **Field Enforcement**: `stream` is forced to `true`, `store` to `false`, and `parallel_tool_calls` to `true`. [internal/translator/codex/openai/responses/codex_openai-responses_request.go:20-22]()
3. **Reasoning Support**: Adds `reasoning.encrypted_content` to the `include` array. [internal/translator/codex/openai/responses/codex_openai-responses_request.go:23]()
4. **Parameter Stripping**: Deletes unsupported fields such as `max_output_tokens`, `temperature`, `top_p`, and `user`. [internal/translator/codex/openai/responses/codex_openai-responses_request.go:25-39]()
5. **Role Conversion**: Converts `"system"` roles to `"developer"` to satisfy Codex API requirements. [internal/translator/codex/openai/responses/codex_openai-responses_request.go:42](), [internal/translator/codex/openai/responses/codex_openai-responses_request.go:68-86]()
6. **Tool Normalization**: Rewrites legacy tool names (e.g., `web_search_preview`) to stable names (e.g., `web_search`). [internal/translator/codex/openai/responses/codex_openai-responses_request.go:132-142]()

### WebSocket Execution

For improved performance and state management, the `CodexWebsocketsExecutor` can handle requests over WebSockets. [internal/runtime/executor/codex_websockets_executor.go:40-44]()

- **Beta Header**: Requests include the `OpenAI-Beta: responses_websockets=2026-02-06` header. [internal/runtime/executor/codex_websockets_executor.go:35]()
- **Message Types**: Requests are wrapped in a `response.create` type before being sent over the socket. [internal/runtime/executor/codex_websockets_executor.go:211](), [internal/runtime/executor/codex_websockets_executor_test.go:21]()

Sources: [internal/translator/codex/openai/responses/codex_openai-responses_request.go:11-46](), [internal/runtime/executor/codex_websockets_executor.go:35-49](), [internal/runtime/executor/codex_websockets_executor_test.go:16-33]()

---

# Page: Qwen, iFlow, and Kimi

# Qwen, iFlow, and Kimi

<details>
<summary>Relevant source files</summary>

The following files were used as context for generating this wiki page:

- [internal/api/handlers/management/handler.go](internal/api/handlers/management/handler.go)
- [internal/auth/iflow/cookie_helpers.go](internal/auth/iflow/cookie_helpers.go)
- [internal/auth/iflow/iflow_auth.go](internal/auth/iflow/iflow_auth.go)
- [internal/auth/kimi/kimi.go](internal/auth/kimi/kimi.go)
- [internal/cmd/antigravity_login.go](internal/cmd/antigravity_login.go)
- [internal/cmd/auth_manager.go](internal/cmd/auth_manager.go)
- [internal/cmd/iflow_cookie.go](internal/cmd/iflow_cookie.go)
- [internal/cmd/kimi_login.go](internal/cmd/kimi_login.go)
- [internal/runtime/executor/kimi_executor.go](internal/runtime/executor/kimi_executor.go)
- [internal/runtime/executor/kimi_executor_test.go](internal/runtime/executor/kimi_executor_test.go)
- [internal/runtime/executor/thinking_providers.go](internal/runtime/executor/thinking_providers.go)
- [sdk/api/management.go](sdk/api/management.go)
- [sdk/auth/gemini.go](sdk/auth/gemini.go)
- [sdk/auth/interfaces.go](sdk/auth/interfaces.go)
- [sdk/auth/kimi.go](sdk/auth/kimi.go)
- [sdk/auth/manager.go](sdk/auth/manager.go)
- [sdk/auth/qwen.go](sdk/auth/qwen.go)
- [sdk/auth/refresh_registry.go](sdk/auth/refresh_registry.go)

</details>



This page documents the provider integrations for Qwen, iFlow, and Kimi (Moonshot AI) within CLIProxyAPI. It covers their specific authentication strategies—ranging from OAuth device flows to cookie-based extraction—and their executor implementations which translate incoming requests into OpenAI-compatible payloads.

---

## Provider Summary

| Feature | Qwen | iFlow | Kimi |
|---|---|---|---|
| **Executor ID** | `"qwen"` | `"iflow"` | `"kimi"` |
| **Auth Method** | Device Flow OAuth | Auth Code / Cookie | Device Flow OAuth |
| **Upstream Format** | OpenAI `/v1/chat/...` | OpenAI `/v1/chat/...` | OpenAI `/v1/chat/...` |
| **Default Base URL** | `https://portal.qwen.ai/v1` | `https://apis.iflow.cn/v1` | `https://api.kimi.com/coding` |
| **Refresh Lead** | 3 Hours | 24 Hours | 5 Minutes |

Sources: [internal/auth/iflow/iflow_auth.go:36-42](), [internal/auth/kimi/kimi.go:33-40](), [sdk/auth/qwen.go:29-31](), [sdk/auth/refresh_registry.go:9-18]()

---

## Kimi (Moonshot AI)

Kimi integration uses the RFC 8628 OAuth2 Device Authorization Grant flow, typically used by CLI tools and IDE plugins (e.g., Kimi Code).

### Authentication Flow
The `KimiAuthenticator` (defined in `sdk/auth/kimi.go`) handles the handshake by requesting a device code and polling for the access token once the user completes the web-based authorization.

**Kimi Device Flow Sequence:**

```mermaid
sequenceDiagram
    participant "User" as U
    participant "KimiAuthenticator" as KA
    participant "DeviceFlowClient" as DFC
    participant "Kimi OAuth API" as KOA

    U->>KA: "Login(ctx, cfg, opts)"
    KA->>DFC: "RequestDeviceCode(ctx)"
    DFC->>KOA: "POST /api/oauth/device_authorization"
    KOA-->>DFC: "device_code, verification_uri_complete"
    DFC-->>KA: "DeviceCodeResponse"
    KA-->>U: "Display URL & Open Browser"
    Note over KA,DFC: Polling Started
    KA->>DFC: "WaitForAuthorization(ctx, deviceCode)"
    loop "Every 5s"
        DFC->>KOA: "POST /api/oauth/token"
        KOA-->>DFC: "authorization_pending / success"
    end
    DFC-->>KA: "KimiAuthBundle (Tokens + DeviceID)"
    KA-->>U: "Authentication successful!"
```

Sources: [internal/auth/kimi/kimi.go:24-37](), [internal/auth/kimi/kimi.go:163-202](), [internal/auth/kimi/kimi.go:205-215]()

### KimiExecutor Implementation
The `KimiExecutor` (defined in `internal/runtime/executor/kimi_executor.go`) manages request preparation, including header injection and model name normalization. It strips the `kimi-` prefix from model names before forwarding to the upstream API.

**Key Functions:**
- `PrepareRequest`: Injects `Authorization: Bearer <token>` into the request [internal/runtime/executor/kimi_executor.go:40-49]().
- `Execute`: Handles non-streaming requests, applying thinking logic via `thinking.ApplyThinking` [internal/runtime/executor/kimi_executor.go:68-102]().
- `HttpRequest`: Injects Kimi credentials into the request and executes it using a proxy-aware client [internal/runtime/executor/kimi_executor.go:52-65]().

---

## iFlow

iFlow supports two authentication methods: a standard OAuth2 Authorization Code flow and a manual Cookie-based extraction method.

### Cookie-Based Authentication
For environments where automated OAuth redirects are restricted, users can provide a `BXAuth` cookie. The `DoIFlowCookieAuth` function in `internal/cmd/iflow_cookie.go` manages this process.

**Cookie Auth Logic:**
1. `NormalizeCookie`: Validates and formats the raw cookie string [internal/auth/iflow/cookie_helpers.go:12-26]().
2. `ExtractBXAuth`: Pulls the specific session identifier needed for API calls [internal/auth/iflow/cookie_helpers.go:44-53]().
3. `CheckDuplicateBXAuth`: Prevents redundant auth files by scanning the `authDir` for existing sessions with the same `BXAuth` value [internal/auth/iflow/cookie_helpers.go:57-99]().

### iFlow Authentication Implementation

```mermaid
classDiagram
    class "IFlowAuth" {
        +AuthorizationURL(state, port)
        +ExchangeCodeForTokens(ctx, code, redirect)
        +AuthenticateWithCookie(ctx, cookie)
        +FetchUserInfo(ctx, accessToken)
    }
    class "IFlowAuthenticator" {
        +Login(ctx, cfg, opts)
        +RefreshLead() *time.Duration
    }
    class "IFlowTokenData" {
        +AccessToken string
        +RefreshToken string
        +APIKey string
        +Email string
    }
    "IFlowAuthenticator" --> "IFlowAuth" : "uses"
    "IFlowAuth" --> "IFlowTokenData" : "returns"
```

Sources: [internal/auth/iflow/iflow_auth.go:45-53](), [internal/auth/iflow/iflow_auth.go:69-83](), [internal/cmd/iflow_cookie.go:17-40]()

---

## Qwen

Qwen follows a device flow similar to Kimi. The implementation is encapsulated in `sdk/auth/qwen.go` and `internal/runtime/executor/qwen_executor.go`.

### Request Lifecycle
The `QwenExecutor` prepares requests by injecting headers and resolving credentials from the `coreauth.Auth` object.

1. **Credential Resolution**: `qwenCreds(auth)` extracts the access token and determines the target base URL (defaulting to `https://portal.qwen.ai/v1`).
2. **Payload Translation**: Translates incoming requests (e.g., Claude or Gemini format) into the standard OpenAI format required by Qwen.
3. **Device Flow Initiation**: `InitiateDeviceFlow` starts the OAuth handshake [sdk/auth/qwen.go:46-51]().
4. **Polling**: `PollForToken` waits for the user to authorize the device code [sdk/auth/qwen.go:68-71]().

---

## Code Entity Space Mapping

The following diagram bridges the management API endpoints to the internal authentication logic for these providers.

> Management API to Auth Entity Mapping

```mermaid
flowchart LR
    subgraph "Management_API_Endpoints"
        M1["/v0/management/request-qwen-token"]
        M2["/v0/management/request-iflow-token"]
        M3["/v0/management/request-kimi-token"]
    end

    subgraph "internal/api/handlers/management"
        H1["RequestQwenToken()"]
        H2["RequestIFlowToken()"]
        H3["RequestKimiToken()"]
    end

    subgraph "sdk/auth"
        A1["QwenAuthenticator"]
        A2["IFlowAuthenticator"]
        A3["KimiAuthenticator"]
    end

    M1 --> H1 --> A1
    M2 --> H2 --> A2
    M3 --> H3 --> A3
```

Sources: [internal/api/handlers/management/handler.go:37-51](), [sdk/api/management.go:14-26](), [sdk/api/management.go:55-69]()

### Refresh and Token Management
All three providers are registered in the global `refresh_registry.go`, ensuring that the `CoreManager` can automatically rotate tokens before they expire based on their specific `RefreshLead` durations.

```mermaid
flowchart TD
    subgraph "Refresh_Registry_init"
        R["sdk/auth/refresh_registry.go"]
    end

    subgraph "Authenticators"
        QA["QwenAuthenticator"]
        IA["IFlowAuthenticator"]
        KA["KimiAuthenticator"]
    end

    subgraph "Core_Logic"
        M["sdk/cliproxy/auth.Manager"]
    end

    R -->|register| QA
    R -->|register| IA
    R -->|register| KA
    M -->|calls| QA
    M -->|calls| IA
    M -->|calls| KA
```

Sources: [sdk/auth/refresh_registry.go:9-18](), [internal/cmd/auth_manager.go:13-24](), [sdk/auth/manager.go:1-20]()

---

# Page: Antigravity and AI Studio

# Antigravity and AI Studio

<details>
<summary>Relevant source files</summary>

The following files were used as context for generating this wiki page:

- [internal/auth/antigravity/auth.go](internal/auth/antigravity/auth.go)
- [internal/auth/codex/filename.go](internal/auth/codex/filename.go)
- [internal/auth/gemini/gemini_auth.go](internal/auth/gemini/gemini_auth.go)
- [internal/misc/oauth.go](internal/misc/oauth.go)
- [internal/runtime/executor/aistudio_executor.go](internal/runtime/executor/aistudio_executor.go)
- [internal/runtime/executor/antigravity_executor.go](internal/runtime/executor/antigravity_executor.go)
- [internal/runtime/executor/claude_executor.go](internal/runtime/executor/claude_executor.go)
- [internal/runtime/executor/codex_executor.go](internal/runtime/executor/codex_executor.go)
- [internal/runtime/executor/gemini_cli_executor.go](internal/runtime/executor/gemini_cli_executor.go)
- [internal/runtime/executor/gemini_executor.go](internal/runtime/executor/gemini_executor.go)
- [internal/runtime/executor/gemini_vertex_executor.go](internal/runtime/executor/gemini_vertex_executor.go)
- [internal/runtime/executor/iflow_executor.go](internal/runtime/executor/iflow_executor.go)
- [internal/runtime/executor/openai_compat_executor.go](internal/runtime/executor/openai_compat_executor.go)
- [internal/runtime/executor/qwen_executor.go](internal/runtime/executor/qwen_executor.go)
- [internal/wsrelay/http.go](internal/wsrelay/http.go)
- [internal/wsrelay/manager.go](internal/wsrelay/manager.go)
- [internal/wsrelay/message.go](internal/wsrelay/message.go)
- [internal/wsrelay/session.go](internal/wsrelay/session.go)
- [sdk/auth/antigravity.go](sdk/auth/antigravity.go)
- [sdk/auth/claude.go](sdk/auth/claude.go)
- [sdk/auth/codex.go](sdk/auth/codex.go)
- [sdk/auth/iflow.go](sdk/auth/iflow.go)

</details>



This page covers the setup and operation of two specialized Google-based providers: **Antigravity** (Google Deepmind's agentic coding assistant) and **AI Studio** (WebSocket-based multi-account provider). Both leverage Google Cloud infrastructure but use different authentication and communication mechanisms.

For general Gemini configuration, see [Google Gemini and Vertex AI](). For WebSocket relay architecture details, see [WebSocket Gateway and Runtime Auth]().

---

## Overview

**Antigravity** is Google Deepmind's advanced agentic AI coding assistant that uses OAuth authentication to access Claude and Gemini models through Google Cloud infrastructure. It provides extended thinking capabilities and signature caching for multi-turn conversations.

**AI Studio** is a WebSocket-based provider integration that enables runtime multi-account load balancing for AI Studio accounts. Unlike traditional HTTP-based executors, AI Studio routes all requests through a WebSocket relay channel, allowing dynamic provider registration without server restarts.

### Architecture Comparison

```mermaid
graph TB
    subgraph "Antigravity Flow"
        [ClientRequest] --> [AntigravityExecutor]
        [AntigravityExecutor] --> [ensureAccessToken]
        [ensureAccessToken] --> [HTTP_Request]
        [HTTP_Request] --> [cloudcode-pa.googleapis.com]
        [cloudcode-pa.googleapis.com] --> [ResponseTranslation]
    end
    
    subgraph "AI Studio Flow"
        [ClientRequest_AI] --> [AIStudioExecutor]
        [AIStudioExecutor] --> [wsrelay.Manager]
        [wsrelay.Manager] --> [WebSocketChannel]
        [WebSocketChannel] --> [RemoteAIStudioClient]
        [RemoteAIStudioClient] --> [ResponseTranslation_AI]
    end
```

**Sources:** [internal/runtime/executor/antigravity_executor.go:59-152](), [internal/runtime/executor/aistudio_executor.go:27-110]()

---

## Antigravity Provider

### Authentication Flow

Antigravity uses OAuth 2.0 with PKCE for authentication. The OAuth flow is initiated through the Management API or the TUI and uses Google's OAuth endpoints.

#### OAuth Credentials

```mermaid
graph LR
    [AntigravityAuthenticator.Login] --> [OAuthFlow_PKCE]
    [OAuthFlow_PKCE] --> [startAntigravityCallbackServer]
    [startAntigravityCallbackServer] --> [TokenStorage]
    [TokenStorage] --> [AuthMetadata]
    [AuthMetadata] --> [ensureAccessToken]
    [ensureAccessToken] --> [Auto-Refresh]
```

**Sources:** [sdk/auth/antigravity.go:20-220](), [internal/runtime/executor/antigravity_executor.go:38-52]()

#### Key Configuration Constants

| Constant | Value | Purpose |
|----------|-------|---------|
| `antigravityAuthType` | `antigravity` | Provider identifier used in `Identifier()` |
| `antigravityClientID` | `1071006060591-tmhssin2h21lcre235vtolojh4g403ep.apps.googleusercontent.com` | Google OAuth Client ID |
| `antigravityClientSecret` | `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` | Google OAuth Client Secret |
| `antigravityBaseURLProd` | `https://cloudcode-pa.googleapis.com` | Production API endpoint |
| `defaultAntigravityAgent` | `antigravity/1.19.6 darwin/arm64` | User-Agent to mimic official client |
| `refreshSkew` | `3000 * time.Second` | Token refresh lead time before expiry |

**Sources:** [internal/runtime/executor/antigravity_executor.go:38-52]()

### Model Support

Antigravity provides access to both Claude and Gemini models through Google Cloud infrastructure. The executor handles model routing and protocol translation.

#### Execute() Non-Streaming Routing

The `Execute()` method handles non-streaming requests. For Claude-based models, it may use an internal streaming approach to reassemble responses.

```mermaid
graph TD
    [AntigravityExecutor.Execute] --> [thinking.ParseSuffix]
    [thinking.ParseSuffix] --> [ModelTypeDecision]
    [ModelTypeDecision] --> [executeClaudeNonStream]
    [ModelTypeDecision] --> [StandardHTTPPOST]
    [executeClaudeNonStream] --> [TranslateRequest_StreamTrue]
    [StandardHTTPPOST] --> [TranslateRequest_StreamFalse]
```

**Sources:** [internal/runtime/executor/antigravity_executor.go:187-258](), [internal/runtime/executor/antigravity_executor.go:261-463]()

### Special Features

#### Signature Caching

Antigravity uses a signature caching mechanism to maintain conversation state for thinking models. This is managed by the `internal/cache` package.

| Function | File Path | Description |
|----------|-----------|-------------|
| `CacheSignature` | `internal/cache/signature_cache.go` | Stores a thinking signature for a specific model and text hash. |
| `GetCachedSignature` | `internal/cache/signature_cache.go` | Retrieves a cached signature to avoid re-generating thinking. |
| `HasValidSignature` | `internal/cache/signature_cache.go` | Validates if a signature meets minimum length requirements. |

**Sources:** [internal/cache/signature_cache.go:1-155]()

#### HTTP/1.1 Enforcement

To perfectly mimic official Node.js client behavior and avoid fingerprinting, the Antigravity executor forces HTTP/1.1 by disabling HTTP/2 in its transport.

```go
func cloneTransportWithHTTP11(base *http.Transport) *http.Transport {
	if base == nil {
		return nil
	}

	clone := base.Clone()
	clone.ForceAttemptHTTP2 = false
	// Wipe TLSNextProto to prevent implicit HTTP/2 upgrade.
	clone.TLSNextProto = make(map[string]func(authority string, c *tls.Conn) http.RoundTripper)
	if clone.TLSClientConfig == nil {
		clone.TLSClientConfig = &tls.Config{}
	} else {
		clone.TLSClientConfig = clone.TLSClientConfig.Clone()
	}
	// Actively advertise only HTTP/1.1 in the ALPN handshake.
	clone.TLSClientConfig.NextProtos = []string{"http/1.1"}
	return clone
}
```

**Sources:** [internal/runtime/executor/antigravity_executor.go:82-99]()

---

## AI Studio WebSocket Relay

### Architecture

AI Studio uses a WebSocket-based relay architecture. The `AIStudioExecutor` does not make direct HTTP calls to Google; instead, it forwards requests through a `wsrelay.Manager` to a connected remote client.

```mermaid
graph TB
    subgraph "CLIProxyAPI_Server"
        [AIStudioExecutor] --> [wsrelay.Manager]
        [wsrelay.Manager] --> [ChannelRegistry]
    end
    
    subgraph "WebSocket_Protocol"
        [ChannelRegistry] <--> [WebSocketConnection]
    end
    
    subgraph "Remote_Client"
        [WebSocketConnection] <--> [AIStudioClient]
        [AIStudioClient] --> [aistudio.google.com]
    end
```

**Sources:** [internal/runtime/executor/aistudio_executor.go:27-44](), [internal/wsrelay/manager.go:1-50]()

### Request Flow

#### Non-Streaming Requests

The `Execute()` method translates the incoming request (e.g., from OpenAI format) to Gemini format and wraps it in a `wsrelay.HTTPRequest` object.

```mermaid
sequenceDiagram
    participant Client
    participant Executor as AIStudioExecutor
    participant Manager as wsrelay.Manager
    participant Remote as Remote Client
    
    Client->>Executor: Execute(req)
    Executor->>Executor: translateRequest()
    Executor->>Manager: NonStream(auth.ID, wsReq)
    Manager->>Remote: Send via WebSocket
    Remote-->>Manager: HTTPResponse message
    Manager-->>Executor: wsrelay.HTTPResponse
    Executor->>Executor: TranslateNonStream()
    Executor-->>Client: Response
```

**Sources:** [internal/runtime/executor/aistudio_executor.go:113-169]()

#### Streaming Requests

Streaming requests use the `Stream()` method of the `wsrelay.Manager`, which returns a channel of events.

```mermaid
sequenceDiagram
    participant Client
    participant Executor as AIStudioExecutor
    participant Manager as wsrelay.Manager
    
    Client->>Executor: ExecuteStream(req)
    Executor->>Manager: Stream(auth.ID, wsReq)
    Manager-->>Executor: Event Channel
    loop Events
        Manager->>Executor: StreamChunk
        Executor->>Client: Translated SSE Chunk
    end
    Manager->>Executor: StreamEnd
```

**Sources:** [internal/runtime/executor/aistudio_executor.go:172-292]()

### Message Types

The WebSocket relay uses structured JSON messages defined in the `wsrelay` package to tunnel HTTP traffic.

| Message Type | Struct | Purpose |
|-------------|--------|---------|
| Request | `HTTPRequest` | Tunnels Method, URL, Headers, and Body to the client. |
| Response | `HTTPResponse` | Returns Status, Headers, and Body from the client. |
| Stream Event | `StreamEvent` | Carries chunk data or stream status updates. |

**Sources:** [internal/wsrelay/http.go:1-50](), [internal/wsrelay/message.go:1-30]()

---

## Comparison Table

| Feature | Antigravity | AI Studio |
|---------|-------------|-----------|
| **Executor Class** | `AntigravityExecutor` | `AIStudioExecutor` |
| **Auth Mechanism** | OAuth 2.0 (Google) | WebSocket Session ID |
| **Protocol** | HTTP/1.1 (Enforced) | WebSocket Relay (JSON) |
| **Primary Target** | `cloudcode-pa.googleapis.com` | `generativelanguage.googleapis.com` |
| **Translation** | `antigravity` target format | `gemini` target format |
| **Thinking Support** | Signature Caching | standard Gemini Thinking |

**Sources:** [internal/runtime/executor/antigravity_executor.go:59-131](), [internal/runtime/executor/aistudio_executor.go:27-48]()

---

# Page: OpenAI-Compatible Providers

# OpenAI-Compatible Providers

<details>
<summary>Relevant source files</summary>

The following files were used as context for generating this wiki page:

- [config.example.yaml](config.example.yaml)
- [internal/api/handlers/management/config_basic.go](internal/api/handlers/management/config_basic.go)
- [internal/api/handlers/management/config_lists.go](internal/api/handlers/management/config_lists.go)
- [internal/api/server.go](internal/api/server.go)
- [internal/config/config.go](internal/config/config.go)
- [internal/runtime/executor/aistudio_executor.go](internal/runtime/executor/aistudio_executor.go)
- [internal/runtime/executor/antigravity_executor.go](internal/runtime/executor/antigravity_executor.go)
- [internal/runtime/executor/claude_executor.go](internal/runtime/executor/claude_executor.go)
- [internal/runtime/executor/codex_executor.go](internal/runtime/executor/codex_executor.go)
- [internal/runtime/executor/gemini_cli_executor.go](internal/runtime/executor/gemini_cli_executor.go)
- [internal/runtime/executor/gemini_executor.go](internal/runtime/executor/gemini_executor.go)
- [internal/runtime/executor/gemini_vertex_executor.go](internal/runtime/executor/gemini_vertex_executor.go)
- [internal/runtime/executor/iflow_executor.go](internal/runtime/executor/iflow_executor.go)
- [internal/runtime/executor/openai_compat_executor.go](internal/runtime/executor/openai_compat_executor.go)
- [internal/runtime/executor/qwen_executor.go](internal/runtime/executor/qwen_executor.go)
- [internal/watcher/watcher.go](internal/watcher/watcher.go)
- [sdk/cliproxy/service.go](sdk/cliproxy/service.go)
- [test/amp_management_test.go](test/amp_management_test.go)

</details>



## Purpose and Scope

This page documents how to configure and use arbitrary OpenAI-compatible providers (e.g., OpenRouter, Together AI, Groq, DeepSeek, or custom local LLM endpoints) with CLIProxyAPI. These providers expose an API that mirrors OpenAI's `/v1/chat/completions` endpoint, allowing the proxy to route requests to these upstreams with minimal translation overhead while benefiting from the proxy's unified authentication and routing layers.

For configuring official providers, see: [Google Gemini and Vertex AI](), [Anthropic Claude](), [OpenAI Codex]().

---

## System Overview

The OpenAI-compatible provider system allows routing requests to any provider that implements an OpenAI-like API. The proxy handles:
- **Base URL resolution** per provider/credential.
- **Model aliasing** to map client model names to upstream names.
- **Model pools** with round-robin rotation across multiple upstream models.
- **Request translation** from any source format (Claude, Gemini, Codex) to OpenAI format.
- **Response translation** back to the source format.
- **Credential injection** (API keys, custom headers).
- **Proxy support** via per-auth HTTP transport configuration.

### Architecture and Data Flow

```mermaid
graph TB
    subgraph "Natural Language Space"
        User["User Request<br/>'gpt-4'"]
    end

    subgraph "Code Entity Space"
        Manager["Manager<br/>(sdk/cliproxy/auth/conductor.go)"]
        Config["Config<br/>(internal/config/config.go)"]
        Executor["OpenAICompatExecutor<br/>(internal/runtime/executor/openai_compat_executor.go)"]
        Translator["Translator<br/>(sdk/translator/translator.go)"]
        HTTP["ProxyAwareHTTPClient<br/>(internal/runtime/executor/http.go)"]
    end

    User --> Manager
    Manager --> Config
    Manager --> Executor
    Executor --> Translator
    Executor --> HTTP
    HTTP --> Upstream["Upstream Provider<br/>(OpenRouter/Groq)"]

    subgraph "Internal Logic"
        Pool["resolveOpenAICompatUpstreamModelPool"]
        Rotate["nextModelPoolOffset"]
    end

    Manager -.-> Pool
    Pool -.-> Rotate
```

**Sources:**
- [internal/config/config.go:105-106]()
- [internal/runtime/executor/openai_compat_executor.go:23-29]()
- [sdk/cliproxy/auth/conductor.go:394-417]()

---

## Configuration Structure

OpenAI-compatible providers are configured in `config.yaml` under the `openai-compatibility` array. Each entry defines a provider with its base URL and optional model aliases.

### Basic Configuration Schema

```yaml
openai-compatibility:
  - name: openrouter              # Provider identifier (used in auth files)
    base-url: https://openrouter.ai/api/v1
    models:
      - alias: gpt-4              # Client-visible model name
        name: openai/gpt-4        # Upstream model name
      - alias: claude-3-opus
        name: anthropic/claude-3-opus
```

### Configuration Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | string | Yes | Provider key used in auth file `compat_name` field. |
| `base-url` | string | Yes | Base URL for the provider (without `/chat/completions`). |
| `models` | array | No | Model alias mappings and pools. |
| `models[].alias` | string | Yes | Client-visible model name. |
| `models[].name` | string | Yes | Upstream model name (can be a single model or comma-separated pool). |

**Sources:**
- [internal/config/config.go:105-106]()
- [internal/config/config.go:1335-1350]() (Legacy/Reference schema)
- [config.example.yaml:182-201]()

---

## Authentication Setup

OpenAI-compatible providers use API key authentication. Create an auth file in your `auth-dir` (default `~/.cli-proxy-api`) with the following structure:

### Auth File Format (`.json`)

```json
{
  "id": "unique-auth-id",
  "provider": "openai-compatibility",
  "status": "active",
  "label": "OpenRouter Production",
  "attributes": {
    "api_key": "sk-or-v1-...",
    "compat_name": "openrouter",
    "base_url": "https://openrouter.ai/api/v1"
  }
}
```

### Auth Attribute Fields

| Field | Required | Description |
|-------|----------|-------------|
| `api_key` | Yes | Provider API key (injected as `Authorization: Bearer` header). |
| `compat_name` | Yes | Must match `name` field in `config.yaml` `openai-compatibility` entry. |
| `base_url` | No | Overrides base URL from config for this specific credential. |

**Sources:**
- [internal/runtime/executor/openai_compat_executor.go:40-54]()
- [sdk/cliproxy/auth/conductor.go:310-344]()

---

## Model Aliasing and Pools

Model aliasing allows clients to use generic model names while the proxy routes to provider-specific models. Model pools enable defining multiple upstream models for a single alias, with automatic round-robin rotation.

### Model Pool Configuration

Define multiple upstream models for load distribution or fallback:

```yaml
openai-compatibility:
  - name: multi-provider
    base-url: https://api.example.com/v1
    models:
      - alias: gpt-4
        name: provider-a/gpt-4,provider-b/gpt-4,provider-c/gpt-4
```

The `name` field contains comma-separated model names. The proxy rotates through them using round-robin logic managed by the `Manager`.

### Round-Robin Rotation Logic

When a model pool is configured, the proxy maintains per-auth, per-model rotation state to distribute requests across upstream models.

```mermaid
sequenceDiagram
    participant C as Conductor (sdk/cliproxy/auth/conductor.go)
    participant R as nextModelPoolOffset
    participant E as OpenAICompatExecutor

    C->>C: resolveOpenAICompatUpstreamModelPool
    C->>R: Request next offset for AuthID|Model
    R-->>C: Returns index (e.g., 1)
    C->>C: rotateStrings(pool, 1)
    C->>E: Execute with rotated pool[0]
```

**Sources:**
- [sdk/cliproxy/auth/conductor.go:394-417]()
- [sdk/cliproxy/auth/conductor.go:154]() (Offset Map)
- [sdk/cliproxy/auth/conductor.go:423-442]() (Rotation Logic)

---

## Implementation Details: OpenAICompatExecutor

The `OpenAICompatExecutor` implements the `ProviderExecutor` interface. It is stateless and performs the following sequence for every request:

1.  **Credential Resolution**: It resolves the `base_url` and `api_key` from the `Auth` object attributes. [internal/runtime/executor/openai_compat_executor.go:78-82]()
2.  **Translation**: It translates the incoming payload (which might be in Claude or Gemini format) into OpenAI format using `sdktranslator`. [internal/runtime/executor/openai_compat_executor.go:96-97]()
3.  **Thinking Support**: It applies user-defined thinking/reasoning parameters if requested via the model suffix (e.g., `model:gpt-4:thinking`). [internal/runtime/executor/openai_compat_executor.go:106-109]()
4.  **Header Injection**: It injects the `Authorization: Bearer <key>` header and any custom headers defined in the auth attributes. [internal/runtime/executor/openai_compat_executor.go:40-54]()
5.  **Execution**: It uses a `ProxyAwareHTTPClient` to send the request, ensuring that if a `proxy-url` is defined for that specific credential, it is respected. [internal/runtime/executor/openai_compat_executor.go:68-69]()
6.  **Response Translation**: After receiving the upstream response, it translates it back to the client's expected source format. [internal/runtime/executor/openai_compat_executor.go:173-174]()

### Streaming Support

For streaming requests, the executor uses `ExecuteStream`. It establishes a Server-Sent Events (SSE) connection with the upstream and uses a `bufio.Scanner` to process the stream line-by-line, translating each chunk before forwarding it to the client. [internal/runtime/executor/openai_compat_executor.go:179-200]()

**Sources:**
- [internal/runtime/executor/openai_compat_executor.go:23-29]() (Struct Definition)
- [internal/runtime/executor/openai_compat_executor.go:72-177]() (Execute Method)
- [internal/runtime/executor/openai_compat_executor.go:179-200]() (ExecuteStream Method)

---

## Advanced Features

### Custom Headers
Auth files can inject custom headers via the `attributes` map using the `header_` prefix. These are stripped of the prefix and injected into the upstream request by `util.ApplyCustomHeadersFromAttrs`. [internal/runtime/executor/openai_compat_executor.go:52-53]()

### Usage Tracking
The executor integrates with the `usageReporter` to track token consumption. It parses the standard OpenAI usage object from the response body and publishes it to the proxy's internal statistics engine. [internal/runtime/executor/openai_compat_executor.go:169-171]()

### Model Pool Fallback Behavior
If a model pool is defined and the first model fails with a retryable error (e.g., 500, 503, or 429), the `Conductor` will automatically attempt the next model in the pool until it succeeds or exhausts the pool. [sdk/cliproxy/auth/conductor.go:535-624]()

**Sources:**
- [internal/runtime/executor/openai_compat_executor.go:75-76]() (Usage Reporter)
- [sdk/cliproxy/auth/conductor.go:535-624]() (Retry/Fallback Logic)

---

# Page: Authentication Flows

# Authentication Flows

<details>
<summary>Relevant source files</summary>

The following files were used as context for generating this wiki page:

- [internal/api/handlers/management/auth_files.go](internal/api/handlers/management/auth_files.go)
- [internal/thinking/apply_user_defined_test.go](internal/thinking/apply_user_defined_test.go)
- [sdk/api/handlers/handlers.go](sdk/api/handlers/handlers.go)
- [sdk/cliproxy/auth/conductor.go](sdk/cliproxy/auth/conductor.go)
- [sdk/cliproxy/auth/conductor_overrides_test.go](sdk/cliproxy/auth/conductor_overrides_test.go)
- [sdk/cliproxy/auth/openai_compat_pool_test.go](sdk/cliproxy/auth/openai_compat_pool_test.go)

</details>



## Purpose and Scope

This page provides a technical deep dive into the authentication mechanisms used by CLIProxyAPI. It covers OAuth flows (PKCE, standard OAuth2, device flow), API key authentication, token storage, and credential lifecycle management including refresh and cooldown logic.

For provider-specific configuration details, see [Provider Integration](#6). For credential routing and failover strategies during request execution, see [Credential Routing and Failover](#8.1). For the authentication management API endpoints, see [Management API](#4.4).

---

## OAuth Flow Types

CLIProxyAPI implements several distinct OAuth flow patterns to accommodate different provider requirements:

| Flow Type | Providers | Characteristics | Implementation |
|-----------|-----------|-----------------|----------------|
| **PKCE** (Proof Key for Code Exchange) | Anthropic/Claude, OpenAI Codex | Browser-based flow with code challenge/verifier | [internal/auth/claude/](), [internal/auth/codex/]() |
| **Standard OAuth2** | Google Gemini, Vertex AI, Antigravity | Standard authorization code flow with offline access | [internal/auth/gemini/](), [internal/auth/antigravity/]() |
| **Device Flow** | Qwen, iFlow | Headless device authorization for limited-input environments | [internal/auth/qwen/](), [internal/auth/iflow/]() |

Each flow produces a token bundle that is persisted through the `Store` interface and registered with the `Manager` for runtime credential selection.

**Sources:** [internal/api/handlers/management/auth_files.go:45-51](), [sdk/cliproxy/auth/conductor.go:130-136]()

---

## OAuth Flow Sequence (PKCE Example)

The following diagram illustrates the interaction between the management API, the provider-specific auth logic, and the core `Manager`.

```mermaid
sequenceDiagram
    participant Client as "Client (Browser/CLI)"
    participant MgmtAPI as "management.Handler"
    participant CallbackFwd as "callbackForwarder"
    participant OAuthSvc as "ClaudeAuth Service"
    participant Provider as "Anthropic OAuth"
    participant Store as "interfaces.Store"
    participant AuthMgr as "auth.Manager"

    Client->>MgmtAPI: POST /v0/management/anthropic/token<br/>?is_webui=true
    MgmtAPI->>OAuthSvc: GeneratePKCECodes()
    OAuthSvc-->>MgmtAPI: code_verifier, code_challenge
    
    alt WebUI Mode
        MgmtAPI->>CallbackFwd: startCallbackForwarder(54545)
        CallbackFwd-->>MgmtAPI: forwarder instance
    end
    
    MgmtAPI-->>Client: {"status":"ok","url":authURL}
    
    Client->>Provider: User authenticates
    Provider->>CallbackFwd: GET /?code=xxx&state=yyy
    CallbackFwd->>MgmtAPI: Redirect to /anthropic/callback
    
    MgmtAPI->>OAuthSvc: ExchangeCodeForTokens(code, pkceCodes)
    OAuthSvc->>Provider: POST /oauth/token
    Provider-->>OAuthSvc: access_token, refresh_token
    
    MgmtAPI->>Store: Save(ctx, auth)
    MgmtAPI->>AuthMgr: Register(ctx, auth)
    
    alt WebUI Mode
        MgmtAPI->>CallbackFwd: stopCallbackForwarder()
    end
```

**Key Components:**

- **management.Handler**: Orchestrates the OAuth flow initiation and callback handling [internal/api/handlers/management/auth_files.go:240-250]().
- **callbackForwarder**: Temporary HTTP server that redirects OAuth callbacks to the management API when running in WebUI mode [internal/api/handlers/management/auth_files.go:54-58]().
- **auth.Manager**: Orchestrates auth lifecycle, selection, and execution [sdk/cliproxy/auth/conductor.go:130-166]().

**Sources:** [internal/api/handlers/management/auth_files.go:54-58](), [internal/api/handlers/management/auth_files.go:133-191](), [sdk/cliproxy/auth/conductor.go:130-166]()

---

## WebUI Callback Forwarding

When the management API is accessed from a WebUI (detected via `is_webui` query parameter [internal/api/handlers/management/auth_files.go:120-131]()), OAuth callbacks require special handling because the provider redirects to `localhost` ports.

```mermaid
graph TB
    Browser["User Browser<br/>(Remote)"]
    Provider["OAuth Provider"]
    LocalFwd["callbackForwarder<br/>127.0.0.1:PORT"]
    MgmtServer["management.Handler<br/>(Remote Server)"]
    
    Browser -->|"1. Initiates OAuth"| MgmtServer
    MgmtServer -->|"2. Returns authURL"| Browser
    Browser -->|"3. User authenticates"| Provider
    Provider -->|"4. Redirect to localhost"| LocalFwd
    LocalFwd -->|"5. Forward to MgmtServer"| MgmtServer
```

The `callbackForwarder` is a temporary HTTP server that:

1. Listens on provider-specific ports: 54545 (Anthropic), 8085 (Gemini), 1455 (Codex) [internal/api/handlers/management/auth_files.go:46-49]().
2. Accepts the OAuth callback and redirects to the management server's callback endpoint using `http.Redirect` [internal/api/handlers/management/auth_files.go:151-162]().
3. Automatically stops after the OAuth flow completes or via `stopCallbackForwarderInstance` [internal/api/handlers/management/auth_files.go:193-204]().

**Sources:** [internal/api/handlers/management/auth_files.go:46-49](), [internal/api/handlers/management/auth_files.go:120-131](), [internal/api/handlers/management/auth_files.go:151-162](), [internal/api/handlers/management/auth_files.go:193-204]()

---

## Token Refresh and Lifecycle

The `auth.Manager` orchestrates the automatic refresh of credentials using the `ProviderExecutor` interface [sdk/cliproxy/auth/conductor.go:28-43]().

```mermaid
sequenceDiagram
    participant Manager as "auth.Manager"
    participant Executor as "ProviderExecutor"
    participant Store as "interfaces.Store"

    Note over Manager: Check expiry (5s interval)
    Manager->>Executor: Refresh(ctx, auth)
    Executor->>Executor: Perform Provider OAuth Refresh
    Executor-->>Manager: Updated *Auth
    Manager->>Store: Save(ctx, updatedAuth)
    Manager->>Manager: Update memory state (mu.Lock)
```

**Refresh Parameters:**
- **Interval**: Expiry checks occur every 5 seconds (`refreshCheckInterval`) [sdk/cliproxy/auth/conductor.go:62]().
- **Concurrency**: Maximum of 16 concurrent refresh operations (`refreshMaxConcurrency`) [sdk/cliproxy/auth/conductor.go:63]().
- **Backoff**: Pending refreshes back off for 1 minute; failures back off for 5 minutes [sdk/cliproxy/auth/conductor.go:64-65]().

**Sources:** [sdk/cliproxy/auth/conductor.go:28-43](), [sdk/cliproxy/auth/conductor.go:62-65](), [sdk/cliproxy/auth/conductor.go:130-166]()

---

## Quota Cooldown Management

When a provider returns a 429 error or other rate-limiting signals, the system schedules a cooldown period to prevent further failures.

**Cooldown Logic:**
- **Result Struct**: Captures execution outcome including `RetryAfter` hints and `Success` status [sdk/cliproxy/auth/conductor.go:87-100]().
- **Backoff**: Base cooldown is 1 second (`quotaBackoffBase`), maxing out at 30 minutes (`quotaBackoffMax`) [sdk/cliproxy/auth/conductor.go:66-67]().
- **Overrides**: Cooldown can be disabled globally via `SetQuotaCooldownDisabled` or per-auth via `DisableCoolingOverride` [sdk/cliproxy/auth/conductor.go:70-84]().

**Sources:** [sdk/cliproxy/auth/conductor.go:66-67](), [sdk/cliproxy/auth/conductor.go:70-84](), [sdk/cliproxy/auth/conductor.go:87-100]()

---

## Child Pages

For detailed implementation of these topics, refer to the following sub-pages:

*   **[OAuth Flow Architecture](#7.1)**: Deep dive into PKCE, state management, and the `callbackForwarder` implementation.
*   **[Provider-Specific OAuth Setup](#7.2)**: Specific scopes, client IDs, and endpoints for Google, Anthropic, and others.
*   **[API Key and Service Account Management](#7.3)**: Handling static credentials and GCP Service Account JSON files.
*   **[Token Refresh and Lifecycle](#7.4)**: Details on the `authScheduler` and the background refresh loop.

---

# Page: OAuth Flow Architecture

# OAuth Flow Architecture

<details>
<summary>Relevant source files</summary>

The following files were used as context for generating this wiki page:

- [internal/api/handlers/management/auth_files.go](internal/api/handlers/management/auth_files.go)
- [internal/api/handlers/management/oauth_callback.go](internal/api/handlers/management/oauth_callback.go)
- [internal/api/handlers/management/oauth_sessions.go](internal/api/handlers/management/oauth_sessions.go)

</details>



## Purpose and Scope

This document describes the OAuth authentication flow architecture used across all provider integrations in CLIProxyAPI. It covers the three primary OAuth patterns implemented (PKCE, standard OAuth2, and device flow), the callback forwarding mechanism for WebUI mode, and OAuth session management infrastructure.

For provider-specific OAuth configuration details (client IDs, scopes, endpoints), see [Provider-Specific OAuth Setup](#7.2). For token refresh and lifecycle management, see [7.4 Token Refresh and Lifecycle](). For general authentication and credential management concepts, see [3.3 Authentication and Credential Management]().

---

## Supported OAuth Flow Patterns

CLIProxyAPI implements three distinct OAuth flow patterns to accommodate different provider requirements and deployment scenarios.

| Flow Pattern | Providers | Use Case | Callback Required |
|--------------|-----------|----------|-------------------|
| **PKCE** | Claude, Codex | Enhanced security for public clients | Yes |
| **Standard OAuth2** | Gemini, Antigravity, iFlow | Traditional web/mobile OAuth | Yes |
| **Device Flow** | Qwen, Kimi | Headless/CLI environments | No |

```mermaid
graph TB
    Client["Client<br/>(CLI/WebUI)"]
    
    subgraph "PKCE Flow"
        PKCE_Start["RequestAnthropicToken<br/>RequestCodexToken"]
        PKCE_Codes["GeneratePKCECodes()<br/>code_verifier<br/>code_challenge"]
        PKCE_Auth["Provider Auth URL<br/>+ state + PKCE"]
        PKCE_Callback["Callback Handler<br/>/anthropic/callback<br/>/codex/callback"]
        PKCE_Exchange["ExchangeCodeForTokens()<br/>+ code_verifier"]
    end
    
    subgraph "Standard OAuth2"
        OAuth_Start["RequestGeminiCLIToken<br/>RequestAntigravityToken<br/>RequestIFlowToken"]
        OAuth_State["Generate State<br/>CSRF Protection"]
        OAuth_Auth["oauth2.Config.AuthCodeURL()<br/>+ scopes"]
        OAuth_Callback["Callback Handler<br/>/google/callback<br/>/antigravity/callback<br/>/iflow/callback"]
        OAuth_Exchange["conf.Exchange(code)"]
    end
    
    subgraph "Device Flow"
        Device_Start["RequestQwenToken<br/>RequestKimiToken"]
        Device_Init["InitiateDeviceFlow()<br/>StartDeviceFlow()"]
        Device_URL["VerificationURIComplete<br/>device_code<br/>user_code"]
        Device_Poll["PollForToken()<br/>WaitForAuthorization()"]
    end
    
    Client --> PKCE_Start
    Client --> OAuth_Start
    Client --> Device_Start
    
    PKCE_Start --> PKCE_Codes
    PKCE_Codes --> PKCE_Auth
    PKCE_Auth --> PKCE_Callback
    PKCE_Callback --> PKCE_Exchange
    
    OAuth_Start --> OAuth_State
    OAuth_State --> OAuth_Auth
    OAuth_Auth --> OAuth_Callback
    OAuth_Callback --> OAuth_Exchange
    
    Device_Start --> Device_Init
    Device_Init --> Device_URL
    Device_URL --> Device_Poll
```

**Sources:** [internal/api/handlers/management/auth_files.go:1016-1159](), [internal/api/handlers/management/auth_files.go:1161-1418](), [internal/api/handlers/management/auth_files.go:1420-1564](), [internal/api/handlers/management/auth_files.go:1731-1785](), [internal/api/handlers/management/auth_files.go:1787-1862](), [internal/api/handlers/management/auth_files.go:1864-1976]()

---

## PKCE Flow Architecture

PKCE (Proof Key for Code Exchange, RFC 7636) provides enhanced security for public clients by binding the authorization request to the token exchange request.

### Flow Sequence

```mermaid
sequenceDiagram
    participant Client
    participant Handler as "auth_files.Handler<br/>RequestAnthropicToken()<br/>RequestCodexToken()"
    participant AuthSvc as "claude.ClaudeAuth<br/>codex.CodexAuth"
    participant State as "oauth_sessions.go<br/>oauthSessionStore"
    participant File as "Callback Wait File<br/>.oauth-{provider}-{state}.oauth"
    participant Provider as "OAuth Provider"
    participant Callback as "Callback Route<br/>/anthropic/callback<br/>/codex/callback"
    
    Client->>Handler: POST /v0/management/request_token/{provider}
    Handler->>AuthSvc: GeneratePKCECodes()
    AuthSvc-->>Handler: code_verifier, code_challenge
    Handler->>Handler: GenerateRandomState()
    Handler->>AuthSvc: GenerateAuthURL(state, pkceCodes)
    AuthSvc-->>Handler: authURL (with code_challenge)
    Handler->>State: RegisterOAuthSession(state, provider)
    Handler-->>Client: 200 OK {url, state}
    
    Note over Handler: Goroutine launched for callback wait
    
    Client->>Provider: Navigate to authURL
    Provider->>Provider: User authenticates
    Provider->>Callback: GET /callback?code=xxx&state=yyy
    Callback->>File: Write {code, state}
    
    Note over Handler: Polling wait file
    Handler->>File: Read callback data
    File-->>Handler: {code, state}
    Handler->>Handler: Validate state
    Handler->>AuthSvc: ExchangeCodeForTokens(code, pkceCodes)
    Note over AuthSvc: Sends code + code_verifier
    AuthSvc->>Provider: POST /token
    Provider-->>AuthSvc: access_token, refresh_token
    AuthSvc-->>Handler: TokenBundle
    Handler->>Handler: saveTokenRecord()
    Handler->>State: CompleteOAuthSession(state)
```

**Sources:** [internal/api/handlers/management/auth_files.go:1016-1159](), [internal/api/handlers/management/auth_files.go:1420-1564](), [internal/api/handlers/management/oauth_sessions.go:25-74]()

### PKCE Code Generation

PKCE requires generating a cryptographically random `code_verifier` and computing a `code_challenge` from it:

- **Code Verifier**: 43-128 character random string (base64url encoded)
- **Code Challenge**: `BASE64URL(SHA256(code_verifier))`
- **Challenge Method**: Always `S256` (SHA-256)

The challenge is sent during authorization, and the verifier is sent during token exchange to prove the same client initiated both requests.

**Sources:** [internal/api/handlers/management/auth_files.go:1023-1028](), [internal/api/handlers/management/auth_files.go:1427-1432]()

### Callback Wait Mechanism

For PKCE flows, the handler creates a temporary wait file and polls for callback data:

```mermaid
graph LR
    Handler["Handler Goroutine"]
    WaitFile[".oauth-{provider}-{state}.oauth<br/>in AuthDir"]
    CallbackRoute["Callback HTTP Handler<br/>/anthropic/callback"]
    
    Handler -->|"Create & poll<br/>every 500ms"| WaitFile
    CallbackRoute -->|"Write JSON<br/>{code, state, error}"| WaitFile
    WaitFile -->|"Read & delete"| Handler
```

**Wait File Location**: `{cfg.AuthDir}/.oauth-{provider}-{state}.oauth` [internal/api/handlers/management/oauth_sessions.go:257-258]()

**Timeout**: 10 minutes (defined by `oauthSessionTTL`) [internal/api/handlers/management/oauth_sessions.go:15]()

**Polling Interval**: 500ms [internal/api/handlers/management/auth_files.go:1083]()

**Data Format**:
```json
{
  "code": "authorization_code_from_provider",
  "state": "state_parameter",
  "error": "error_description_if_any"
}
```
**Sources:** [internal/api/handlers/management/auth_files.go:1073-1094](), [internal/api/handlers/management/auth_files.go:1478-1511](), [internal/api/handlers/management/oauth_sessions.go:239-272]()

---

## Standard OAuth2 Flow

Standard OAuth2 with authorization code grant is used for Gemini, Antigravity, and iFlow integrations.

### Flow Sequence

```mermaid
sequenceDiagram
    participant Client
    participant Handler as "auth_files.Handler<br/>RequestGeminiCLIToken()<br/>RequestAntigravityToken()"
    participant OAuth2 as "oauth2.Config<br/>golang.org/x/oauth2"
    participant State as "oauth_sessions.go<br/>oauthSessionStore"
    participant File as "Callback Wait File"
    participant Provider as "OAuth Provider"
    participant Callback as "Callback Route<br/>/google/callback"
    
    Client->>Handler: POST /v0/management/request_gemini_cli_token
    Handler->>Handler: Generate state (gem-{timestamp})
    Handler->>OAuth2: AuthCodeURL(state, offline, consent)
    OAuth2-->>Handler: authURL
    Handler->>State: RegisterOAuthSession(state, "gemini")
    Handler-->>Client: 200 OK {url, state}
    
    Note over Handler: Goroutine launched
    
    Client->>Provider: Navigate to authURL
    Provider->>Provider: User grants consent
    Provider->>Callback: GET /callback?code=xxx&state=yyy
    Callback->>File: Write {code, state, error}
    
    Handler->>File: Poll for callback data (5min timeout)
    File-->>Handler: {code, state}
    Handler->>Handler: Validate state
    Handler->>OAuth2: Exchange(ctx, code)
    OAuth2->>Provider: POST /token
    Provider-->>OAuth2: Token (access + refresh)
    OAuth2-->>Handler: *oauth2.Token
    Handler->>Handler: Create GeminiTokenStorage
    Handler->>Handler: Perform CLI onboarding
    Handler->>Handler: saveTokenRecord()
    Handler->>State: CompleteOAuthSession(state)
```

**Sources:** [internal/api/handlers/management/auth_files.go:1161-1418](), [internal/api/handlers/management/auth_files.go:1566-1729]()

### OAuth2 Configuration Parameters

For Gemini CLI authentication, the `oauth2.Config` is constructed as follows:

| Field | Value | Source |
|-------|-------|--------|
| `ClientID` | `geminiAuth.ClientID` | [internal/api/handlers/management/auth_files.go:1173]() |
| `ClientSecret` | `geminiAuth.ClientSecret` | [internal/api/handlers/management/auth_files.go:1174]() |
| `RedirectURL` | `http://localhost:{port}/oauth2callback` | [internal/api/handlers/management/auth_files.go:1175]() |
| `Scopes` | `geminiAuth.Scopes` | [internal/api/handlers/management/auth_files.go:1176]() |
| `Endpoint` | `google.Endpoint` | [internal/api/handlers/management/auth_files.go:1177]() |

**Additional URL Parameters**:
- `access_type=offline`: Request refresh token [internal/api/handlers/management/auth_files.go:1184]()
- `prompt=consent`: Force consent screen to ensure refresh token issuance [internal/api/handlers/management/auth_files.go:1184]()

**Sources:** [internal/api/handlers/management/auth_files.go:1173-1184]()

### Antigravity OAuth Specifics

Antigravity uses a custom OAuth implementation:

- **Authorization URL**: Built via `antigravity.BuildAuthURL(state, redirectURI)` [internal/api/handlers/management/auth_files.go:1582]()
- **Redirect URI**: `http://localhost:{antigravity.CallbackPort}/oauth-callback` [internal/api/handlers/management/auth_files.go:1571]()
- **Token Exchange**: `antigravity.ExchangeCodeForTokens(ctx, code, redirectURI)` [internal/api/handlers/management/auth_files.go:1633]()
- **User Info Fetch**: `antigravity.FetchUserInfo(ctx, accessToken)` to retrieve email [internal/api/handlers/management/auth_files.go:1641]()
- **Project ID Fetch**: `antigravity.FetchProjectID(ctx, accessToken)` for GCP project [internal/api/handlers/management/auth_files.go:1651]()

**Sources:** [internal/api/handlers/management/auth_files.go:1566-1729]()

---

## Device Flow

Device flow (RFC 8628) is designed for input-constrained devices or CLI environments where a callback URL is impractical.

### Flow Sequence

```mermaid
sequenceDiagram
    participant Client
    participant Handler as "auth_files.Handler<br/>RequestQwenToken()<br/>RequestKimiToken()"
    participant AuthSvc as "qwen.QwenAuth<br/>kimi.KimiAuth"
    participant State as "oauth_sessions.go<br/>oauthSessionStore"
    participant Provider as "OAuth Provider"
    
    Client->>Handler: POST /v0/management/request_qwen_token
    Handler->>Handler: Generate state
    Handler->>AuthSvc: InitiateDeviceFlow(ctx)<br/>StartDeviceFlow(ctx)
    AuthSvc->>Provider: POST /device/code
    Provider-->>AuthSvc: device_code, user_code,<br/>verification_uri_complete
    AuthSvc-->>Handler: DeviceFlowResponse
    Handler->>State: RegisterOAuthSession(state, provider)
    Handler-->>Client: 200 OK {url: verification_uri_complete, state}
    
    Note over Handler: Goroutine launched
    
    Client->>Client: Display verification URL to user
    
    loop Poll until authorized or timeout
        Handler->>AuthSvc: PollForToken(device_code)<br/>WaitForAuthorization(deviceFlow)
        AuthSvc->>Provider: POST /token (device_code)
        
        alt Not yet authorized
            Provider-->>AuthSvc: authorization_pending
        else Authorized
            Provider-->>AuthSvc: access_token, refresh_token
            AuthSvc-->>Handler: TokenData
        end
    end
    
    Handler->>Handler: CreateTokenStorage()
    Handler->>Handler: saveTokenRecord()
    Handler->>State: CompleteOAuthSession(state)
```

**Sources:** [internal/api/handlers/management/auth_files.go:1731-1785](), [internal/api/handlers/management/auth_files.go:1787-1862]()

### Device Flow Response Structure

The device flow initiation returns:

| Field | Description |
|-------|-------------|
| `device_code` | Unique identifier for this authorization request |
| `user_code` | Human-readable code displayed to user |
| `verification_uri` | URL where user enters the code |
| `verification_uri_complete` | Direct URL with embedded code (preferred) |
| `expires_in` | Lifetime of device_code in seconds |
| `interval` | Minimum polling interval in seconds |

For Qwen, an additional `code_verifier` is returned for enhanced security [internal/api/handlers/management/auth_files.go:1742-1749]().

**Sources:** [internal/api/handlers/management/auth_files.go:1742-1749](), [internal/api/handlers/management/auth_files.go:1798-1808]()

---

## Callback Forwarding for WebUI Mode

When the proxy is accessed via a remote WebUI, OAuth callbacks cannot reach `localhost`. The callback forwarder solves this by creating a local server that redirects callbacks to the management API endpoint.

### Architecture

```mermaid
graph TB
    Browser["Remote Browser<br/>(WebUI)"]
    LocalCallback["Local Callback Server<br/>127.0.0.1:{provider_port}"]
    MgmtAPI["Management API Endpoint<br/>127.0.0.1:{cfg.Port}/callback"]
    CallbackHandler["Callback Route Handler<br/>/anthropic/callback"]
    WaitFile["Wait File<br/>.oauth-{provider}-{state}.oauth"]
    
    Browser -->|"OAuth redirect<br/>http://localhost:{provider_port}/..."| LocalCallback
    LocalCallback -->|"HTTP 302 Redirect<br/>with query params"| MgmtAPI
    MgmtAPI --> CallbackHandler
    CallbackHandler --> WaitFile
```

**Sources:** [internal/api/handlers/management/auth_files.go:130-188]()

### Callback Forwarder Implementation

The `callbackForwarder` struct encapsulates a temporary HTTP server:

```mermaid
classDiagram
    class callbackForwarder {
        +string provider
        +http.Server server
        +chan done
    }
    
    class Handler {
        +startCallbackForwarder(port, provider, targetBase) callbackForwarder
        +stopCallbackForwarderInstance(port, forwarder)
    }
    
    Handler --> callbackForwarder : creates/manages
```

**Forwarder Lifecycle**:

1. **Start**: `startCallbackForwarder(port, provider, targetURL)` creates a listener on `127.0.0.1:{port}` via `net.Listen("tcp", addr)` [internal/api/handlers/management/auth_files.go:143-146]().
2. **Forward**: HTTP handler redirects all requests to `targetURL` with query parameters appended [internal/api/handlers/management/auth_files.go:148-159]().
3. **Stop**: `stopCallbackForwarderInstance()` performs graceful shutdown with 2-second timeout [internal/api/handlers/management/auth_files.go:203-221]().

**Sources:** [internal/api/handlers/management/auth_files.go:53-62](), [internal/api/handlers/management/auth_files.go:130-188](), [internal/api/handlers/management/auth_files.go:190-221]()

### Provider-Specific Callback Ports

Callback forwarders use provider-specific ports to avoid conflicts:

| Provider | Port | Constant |
|----------|------|----------|
| Anthropic | 54545 | `anthropicCallbackPort` [internal/api/handlers/management/auth_files.go:47]() |
| Gemini | 8085 | `geminiCallbackPort` [internal/api/handlers/management/auth_files.go:48]() |
| Codex | 1455 | `codexCallbackPort` [internal/api/handlers/management/auth_files.go:49]() |

**Sources:** [internal/api/handlers/management/auth_files.go:45-49]()

### WebUI Detection

The `is_webui` query parameter triggers callback forwarding via `isWebUIRequest(c)` [internal/api/handlers/management/auth_files.go:117-128]().

---

## OAuth Session Management

OAuth sessions track the state of in-progress authentication flows and prevent unauthorized completion.

### Session Registry

The session registry maintains a mapping of state parameters to provider names and completion status:

```mermaid
stateDiagram-v2
    [*] --> Pending: RegisterOAuthSession(state, provider)
    Pending --> Completed: CompleteOAuthSession(state)
    Pending --> Error: SetOAuthSessionError(state, message)
    Pending --> Cancelled: User cancels or goroutine returns
    Completed --> [*]
    Error --> [*]
    Cancelled --> [*]
    
    note right of Pending
        IsOAuthSessionPending(state, provider)
        returns true
    end note
    
    note right of Error
        GetOAuthSession(state)
        returns (provider, error_message, true)
    end note
```

**Sources:** [internal/api/handlers/management/oauth_sessions.go:32-191]()

### Session Operations

| Function | Purpose |
|----------|---------|
| `RegisterOAuthSession(state, provider)` | Creates pending session with TTL [internal/api/handlers/management/oauth_sessions.go:171]() |
| `IsOAuthSessionPending(state, provider)` | Checks if session is active and has no error [internal/api/handlers/management/oauth_sessions.go:189]() |
| `CompleteOAuthSession(state)` | Marks session as completed by deleting it [internal/api/handlers/management/oauth_sessions.go:175]() |
| `SetOAuthSessionError(state, message)` | Marks session as failed with an error message [internal/api/handlers/management/oauth_sessions.go:173]() |
| `ValidateOAuthState(state)` | Validates state parameter format [internal/api/handlers/management/oauth_sessions.go:193-218]() |

**Sources:** [internal/api/handlers/management/oauth_sessions.go:171-218]()

---

## State Validation and Security

### Security Measures

| Measure | Implementation | Purpose |
|---------|----------------|---------|
| **State Validation** | Compare callback state with registered session [internal/api/handlers/management/oauth_callback.go:76-88]() | Prevent CSRF attacks |
| **Timeout** | 10-minute session TTL [internal/api/handlers/management/oauth_sessions.go:15]() | Prevent session hijacking |
| **PKCE** | Code verifier binding [internal/api/handlers/management/auth_files.go:1023]() | Prevent code interception |
| **Secure Storage** | Wait files with `0o600` permissions [internal/api/handlers/management/oauth_sessions.go:268]() | Protect auth codes |

**Sources:** [internal/api/handlers/management/oauth_callback.go:76-88](), [internal/api/handlers/management/oauth_sessions.go:15-268](), [internal/api/handlers/management/auth_files.go:1023]()

### Error Handling

OAuth flows implemented in `PostOAuthCallback` validate the incoming state and session status before writing the callback file [internal/api/handlers/management/oauth_callback.go:20-100](). If a session is already marked with an error or completed, the request is rejected with `http.StatusConflict` [internal/api/handlers/management/oauth_callback.go:81-84]().

**Sources:** [internal/api/handlers/management/oauth_callback.go:20-100]()

---

## Authentication Status Polling

WebUI clients poll the `/v0/management/auth_status` endpoint to determine when OAuth flows complete. This handler checks the `oauthSessionStore` for the provided state [internal/api/handlers/management/oauth_sessions.go:181-187]().

**Sources:** [internal/api/handlers/management/oauth_sessions.go:181-187]()

---

# Page: Provider-Specific OAuth Setup

# Provider-Specific OAuth Setup

<details>
<summary>Relevant source files</summary>

The following files were used as context for generating this wiki page:

- [internal/api/handlers/management/auth_files.go](internal/api/handlers/management/auth_files.go)
- [internal/auth/claude/anthropic_auth.go](internal/auth/claude/anthropic_auth.go)
- [internal/auth/codex/openai_auth.go](internal/auth/codex/openai_auth.go)
- [internal/auth/codex/openai_auth_test.go](internal/auth/codex/openai_auth_test.go)
- [internal/auth/iflow/cookie_helpers.go](internal/auth/iflow/cookie_helpers.go)
- [internal/auth/iflow/iflow_auth.go](internal/auth/iflow/iflow_auth.go)
- [internal/auth/qwen/qwen_auth.go](internal/auth/qwen/qwen_auth.go)
- [internal/cmd/iflow_cookie.go](internal/cmd/iflow_cookie.go)
- [internal/cmd/openai_device_login.go](internal/cmd/openai_device_login.go)
- [sdk/auth/codex_device.go](sdk/auth/codex_device.go)

</details>



This page documents the OAuth configuration for each supported provider, including client IDs, OAuth scopes, redirect URIs, and special requirements. Each provider has different OAuth requirements: some use PKCE (Proof Key for Code Exchange), others use device flow, and some require post-authentication setup steps like project onboarding.

For architectural details on how OAuth flows work internally (PKCE generation, local callback servers, state validation), see page 7.1. For token refresh mechanics, see page 7.4. For the HTTP API endpoints that trigger these flows, see page 4.4.

---

## OAuth Flow Types and Configuration Summary

Each provider implements a different OAuth variant. The table below summarizes flow type, callback port, PKCE requirement, and credential file naming:

| Provider | OAuth Flow | PKCE Required | Callback Port | Redirect URI Pattern | Credential File Pattern |
|---|---|---|---|---|---|
| Gemini / Vertex | Authorization Code | No | `8085` | `http://localhost:8085/oauth2callback` | `gemini-{email}-{projectID}.json` |
| Claude (Anthropic) | Authorization Code | Yes | `54545` | `http://localhost:54545/callback` | `claude-{email}.json` |
| Codex (OpenAI) | Authorization Code or Device | Yes (code flow) | `1455` | `http://localhost:1455/auth/callback` | `codex-{email}-{planType}-{hash}.json` |
| iFlow | Authorization Code | No | `11451` | `http://localhost:11451/oauth2callback` | `iflow-{email}-{timestamp}.json` |
| Qwen | Device Flow | N/A | N/A (polling) | N/A | `qwen-{email}.json` |
| Kimi | Device Flow | N/A | N/A (polling) | N/A | `kimi-{identifier}.json` |

Callback port constants and Redirect URIs are defined within their respective auth packages:
- Claude: [internal/auth/claude/anthropic_auth.go:21-26]()
- Codex: [internal/auth/codex/openai_auth.go:23-28]()
- iFlow: [internal/auth/iflow/iflow_auth.go:40-42]()
- Management Handlers: [internal/api/handlers/management/auth_files.go:46-52]()

---

## Authentication Entry Points

Each provider supports two authentication paths:

1. **CLI flags** — Run `./cliproxyapi --{provider}-login` at startup to authenticate in the terminal.
2. **Management API** — HTTP POST to `/v0/management/auth/{provider}` to trigger authentication from a running server.

**Authentication flow routing by provider:**

```mermaid
flowchart TB
    subgraph "CLI_Entry_Points"["CLI Entry Points (cmd package)"]
        "DoLogin"["DoLogin()"]
        "DoClaudeLogin"["DoClaudeLogin()"]
        "DoCodexLogin"["DoCodexLogin()"]
        "DoIFlowLogin"["DoIFlowLogin()"]
        "DoIFlowCookieAuth"["DoIFlowCookieAuth()"]
    end

    subgraph "MGMT_Handlers"["Management API Handlers (management package)"]
        "RequestGeminiCLIToken"["RequestGeminiCLIToken()"]
        "RequestAnthropicToken"["RequestAnthropicToken()"]
        "RequestCodexToken"["RequestCodexToken()"]
        "RequestQwenToken"["RequestQwenToken()"]
        "RequestKimiToken"["RequestKimiToken()"]
    end

    subgraph "SDK_Authenticators"["SDK Authenticators (sdk/auth package)"]
        "GeminiAuthenticator"["GeminiAuthenticator"]
        "ClaudeAuthenticator"["ClaudeAuthenticator"]
        "CodexAuthenticator"["CodexAuthenticator"]
        "QwenAuthenticator"["QwenAuthenticator"]
        "IFlowAuthenticator"["IFlowAuthenticator"]
    end

    "DoLogin" --> "GeminiAuthenticator"
    "DoClaudeLogin" --> "ClaudeAuthenticator"
    "DoCodexLogin" --> "CodexAuthenticator"
    "DoIFlowLogin" --> "IFlowAuthenticator"
    "DoIFlowCookieAuth" --> "IFlowAuthenticator"

    "RequestGeminiCLIToken" --> "GeminiAuthenticator"
    "RequestAnthropicToken" --> "ClaudeAuthenticator"
    "RequestCodexToken" --> "CodexAuthenticator"
    "RequestQwenToken" --> "QwenAuthenticator"
    "RequestKimiToken" --> "KimiAuth"
```

Sources: [internal/cmd/iflow_cookie.go:16-77](), [internal/auth/iflow/iflow_auth.go:49-53](), [internal/auth/claude/anthropic_auth.go:61-67](), [internal/auth/codex/openai_auth.go:37-43]()

---

## Gemini / Vertex AI

**OAuth Configuration:**
- **Flow Type:** Authorization Code (Google OAuth2).
- **Redirect URI:** `http://localhost:8085/oauth2callback`.
- **Callback Port:** `8085` [internal/api/handlers/management/auth_files.go:48]().

**Special Requirements:**
1. **GCP Project Selection:** After OAuth completes, a GCP project must be selected or auto-discovered.
2. **API Onboarding:** Calls Google Cloud Code APIs at `https://cloudcode-pa.googleapis.com` [internal/api/handlers/management/auth_files.go:50]() to activate the project for AI Companion services.

---

## Claude (Anthropic)

**OAuth Configuration:**
- **Flow Type:** Authorization Code with PKCE.
- **Client ID:** `9d1c250a-e61b-44d9-88ed-5944d1962f5e` [internal/auth/claude/anthropic_auth.go:24]().
- **Authorization Endpoint:** `https://claude.ai/oauth/authorize` [internal/auth/claude/anthropic_auth.go:22]().
- **Token Endpoint:** `https://api.anthropic.com/v1/oauth/token` [internal/auth/claude/anthropic_auth.go:23]().
- **Redirect URI:** `http://localhost:54545/callback` [internal/auth/claude/anthropic_auth.go:25]().
- **Scopes:** `org:create_api_key user:profile user:inference` [internal/auth/claude/anthropic_auth.go:91]().

**PKCE Implementation:**
Claude uses PKCE (Proof Key for Code Exchange). The `GenerateAuthURL` function requires `PKCECodes` including `code_challenge` and `code_challenge_method` (S256) [internal/auth/claude/anthropic_auth.go:81-99](). During exchange, the `code_verifier` is sent to the token endpoint [internal/auth/claude/anthropic_auth.go:139-146]().

**Special Handling:**
The `ClaudeAuth` client uses a custom HTTP client (via `NewAnthropicHttpClient`) to bypass Cloudflare bot detection on Anthropic domains [internal/auth/claude/anthropic_auth.go:61-67]().

Sources: [internal/auth/claude/anthropic_auth.go:21-26](), [internal/auth/claude/anthropic_auth.go:81-99](), [internal/auth/claude/anthropic_auth.go:132-165]()

---

## Codex (OpenAI)

**OAuth Configuration:**
- **Flow Type:** Authorization Code with PKCE or Device Flow.
- **Client ID:** `app_EMoamEEZ73f0CkXaXp7hrann` [internal/auth/codex/openai_auth.go:26]().
- **Authorization Endpoint:** `https://auth.openai.com/oauth/authorize` [internal/auth/codex/openai_auth.go:24]().
- **Token Endpoint:** `https://auth.openai.com/oauth/token` [internal/auth/codex/openai_auth.go:25]().
- **Redirect URI:** `http://localhost:1455/auth/callback` [internal/auth/codex/openai_auth.go:27]().
- **Scopes:** `openid email profile offline_access` [internal/auth/codex/openai_auth.go:57]().

**Device Flow:**
If configured via metadata [sdk/auth/codex_device.go:57-62](), Codex uses a device flow. It requests a user code from `https://auth.openai.com/api/accounts/deviceauth/usercode` [sdk/auth/codex_device.go:27]() and polls `https://auth.openai.com/api/accounts/deviceauth/token` [sdk/auth/codex_device.go:28](). The device verification URL for users is `https://auth.openai.com/codex/device` [sdk/auth/codex_device.go:29]().

Sources: [internal/auth/codex/openai_auth.go:23-28](), [sdk/auth/codex_device.go:24-33](), [sdk/auth/codex_device.go:64-126]()

---

## iFlow

**OAuth Configuration:**
- **Flow Type:** Authorization Code.
- **Client ID:** `10009311001` [internal/auth/iflow/iflow_auth.go:31]().
- **Client Secret:** `4Z3YjXycVsQvyGF1etiNlIBB4RsqSDtW` [internal/auth/iflow/iflow_auth.go:32]().
- **Redirect URI:** `http://localhost:11451/oauth2callback` [internal/auth/iflow/iflow_auth.go:57]().

**Dual Authentication Modes:**
1. **OAuth Flow:** Standard code exchange [internal/auth/iflow/iflow_auth.go:69-83]().
2. **Cookie-Based:** Uses `AuthenticateWithCookie` to extract a `BXAuth` token from browser cookies [internal/cmd/iflow_cookie.go:56-60](). Cookies must be normalized to ensure the `BXAuth=` field is present [internal/auth/iflow/cookie_helpers.go:11-26]().

**API Key Extraction:**
iFlow authentication automatically fetches a permanent `APIKey` from `https://iflow.cn/api/oauth/getUserInfo` using the access token [internal/auth/iflow/iflow_auth.go:149-166]().

Sources: [internal/auth/iflow/iflow_auth.go:20-33](), [internal/auth/iflow/iflow_auth.go:69-83](), [internal/auth/iflow/iflow_auth.go:149-166](), [internal/cmd/iflow_cookie.go:16-77](), [internal/auth/iflow/cookie_helpers.go:11-26]()

---

## Qwen (Device Flow)

Qwen utilizes the OAuth 2.0 Device Authorization Grant.

**Configuration:**
- **Device Code Endpoint:** `https://chat.qwen.ai/api/v1/oauth2/device/code` [internal/auth/qwen/qwen_auth.go:23]().
- **Token Endpoint:** `https://chat.qwen.ai/api/v1/oauth2/token` [internal/auth/qwen/qwen_auth.go:25]().
- **Client ID:** `f0304373b74a44d2b584a3fb70ca9e56` [internal/auth/qwen/qwen_auth.go:27]().
- **Scope:** `openid profile email model.completion` [internal/auth/qwen/qwen_auth.go:29]().

**Flow Mechanics:**
The flow generates a PKCE pair (verifier and challenge) [internal/auth/qwen/qwen_auth.go:108-115](). The client then initiates the flow and polls the token endpoint until the user authorizes the request [internal/auth/qwen/qwen_auth.go:170-182]().

Sources: [internal/auth/qwen/qwen_auth.go:21-32](), [internal/auth/qwen/qwen_auth.go:108-115](), [internal/auth/qwen/qwen_auth.go:170-182]()

---

## Credential Entities and Storage

All providers utilize a unified storage structure that persists to JSON files.

**Provider-to-Code Mapping:**

```mermaid
classDiagram
    class "TokenStorage" {
        <<Interface>>
        +SaveTokenToFile(path)
        +SetMetadata(meta)
    }
    class "GeminiTokenStorage" {
        +Token any
        +ProjectID string
        +Checked bool
    }
    class "ClaudeTokenData" {
        +AccessToken string
        +RefreshToken string
        +Email string
        +Expire string
    }
    class "IFlowTokenData" {
        +AccessToken string
        +RefreshToken string
        +APIKey string
        +Email string
    }
    class "CodexTokenData" {
        +IDToken string
        +AccessToken string
        +RefreshToken string
        +AccountID string
    }
    class "QwenTokenData" {
        +AccessToken string
        +RefreshToken string
        +ResourceURL string
        +Expire string
    }

    "TokenStorage" <|.. "GeminiTokenStorage"
    "TokenStorage" <|.. "ClaudeTokenData"
    "TokenStorage" <|.. "IFlowTokenData"
    "TokenStorage" <|.. "CodexTokenData"
    "TokenStorage" <|.. "QwenTokenData"
```

Sources: [internal/auth/claude/anthropic_auth.go:194-199](), [internal/auth/iflow/iflow_auth.go:136-142](), [internal/auth/codex/openai_auth.go:150-157](), [internal/auth/qwen/qwen_auth.go:35-45]()

---

# Page: API Key and Service Account Management

# API Key and Service Account Management

<details>
<summary>Relevant source files</summary>

The following files were used as context for generating this wiki page:

- [internal/api/handlers/management/auth_files.go](internal/api/handlers/management/auth_files.go)
- [internal/auth/claude/token.go](internal/auth/claude/token.go)
- [internal/auth/codex/token.go](internal/auth/codex/token.go)
- [internal/auth/gemini/gemini_token.go](internal/auth/gemini/gemini_token.go)
- [internal/auth/iflow/iflow_token.go](internal/auth/iflow/iflow_token.go)
- [internal/auth/kimi/token.go](internal/auth/kimi/token.go)
- [internal/auth/qwen/qwen_token.go](internal/auth/qwen/qwen_token.go)
- [internal/misc/credentials.go](internal/misc/credentials.go)
- [internal/watcher/synthesizer/config_test.go](internal/watcher/synthesizer/config_test.go)
- [internal/watcher/synthesizer/context.go](internal/watcher/synthesizer/context.go)
- [internal/watcher/synthesizer/file.go](internal/watcher/synthesizer/file.go)
- [internal/watcher/synthesizer/file_test.go](internal/watcher/synthesizer/file_test.go)
- [internal/watcher/synthesizer/helpers.go](internal/watcher/synthesizer/helpers.go)
- [internal/watcher/synthesizer/helpers_test.go](internal/watcher/synthesizer/helpers_test.go)
- [internal/watcher/synthesizer/interface.go](internal/watcher/synthesizer/interface.go)
- [sdk/auth/filestore.go](sdk/auth/filestore.go)
- [sdk/cliproxy/service_excluded_models_test.go](sdk/cliproxy/service_excluded_models_test.go)

</details>



This page covers two distinct concerns that both use the word "key":

1.  **Incoming access control** — the `api-keys` list in `config.yaml` used to authenticate requests arriving at CLIProxyAPI from clients (e.g. an AI CLI tool).
2.  **Provider credentials** — the `gemini-api-key`, `claude-api-key`, `codex-api-key`, `openai-compatibility`, and `vertex-api-key` entries, along with **Service Account JSON files**, that CLIProxyAPI uses when forwarding requests to upstream AI providers.

For OAuth-based provider credentials and token refresh, see page [7.2]() and [7.4](). For the broader authentication manager and credential routing/failover, see page [3.3]() and [8.1]().

---

## Incoming Request Authentication

CLIProxyAPI can require that every API call it receives includes one of the keys listed under `api-keys` in `config.yaml`. When no keys are configured, the server allows all requests through (open access).

### Configuration

```yaml
api-keys:
  - "your-api-key-1"
  - "your-api-key-2"
```

These values are defined in `SDKConfig` inside [internal/config/config.go]() (the `APIKeys []string` field) and are loaded at startup via `LoadConfig`.

### The `config-api-key` Access Provider

The incoming-request authentication system is built around the `sdk/access` package. The concrete implementation for config-file keys lives in [internal/access/config_access/provider.go]().

**Credential locations inspected (in order):**

| Source | Header / Parameter |
| :--- | :--- |
| `authorization` | `Authorization: Bearer <key>` |
| `x-goog-api-key` | `X-Goog-Api-Key: <key>` |
| `x-api-key` | `X-Api-Key: <key>` |
| `query-key` | `?key=<key>` |
| `query-auth-token` | `?auth_token=<key>` |

The `provider` struct [internal/access/config_access/provider.go:31-35]() stores the allowed keys in a `map[string]struct{}` for O(1) lookup. The `Authenticate` method [internal/access/config_access/provider.go:55-104]() checks each credential location and returns:

*   `Result` with `Principal` = the matched key string, on success.
*   `NewInvalidCredentialError()` if a credential was supplied but not found in the set.
*   `NewNoCredentialsError()` if no credential was supplied at all.

`Register` in [internal/access/config_access/provider.go:13-29]() is called on startup and on every config reload. If `APIKeys` is empty, the provider is unregistered, making the server unauthenticated.

### The Access Manager and Middleware

**Access Manager Flow**

```mermaid
flowchart LR
    A["config.yaml\n(api-keys list)"] --> B["configaccess.Register\n(config_access/provider.go)"]
    B --> C["sdkaccess.RegisterProvider\n(sdk/access/registry.go)"]
    C --> D["sdkaccess.RegisteredProviders()"]
    D --> E["accessManager.SetProviders()\n(sdk/access/manager.go)"]
    E --> F["AuthMiddleware\n(internal/api/server.go:1030)"]
    F --> G["manager.Authenticate(ctx, req)\n(sdk/access/manager.go:45)"]
```

Sources: [internal/access/config_access/provider.go](), [sdk/access/registry.go](), [sdk/access/manager.go](), [internal/api/server.go:1030-1050]()

The `AuthMiddleware` function [internal/api/server.go:1030-1050]() is applied as Gin middleware to the `/v1` and `/v1beta` route groups. If `manager` is `nil` or has no providers, every request passes through. If `manager.Authenticate` returns an error, the middleware aborts with HTTP 401.

On success, the middleware sets two Gin context values:

*   `"apiKey"` → `result.Principal` (the matched key string)
*   `"accessProvider"` → `result.Provider`

### Hot Reload Behavior

When `config.yaml` changes, `applyAccessConfig` [internal/api/server.go:864-871]() calls `access.ApplyAccessProviders` [internal/access/reconcile.go:82-105](), which calls `configaccess.Register` with the new config and updates `accessManager.SetProviders`. This happens without restarting the server — see [3.7]() for the full hot-reload mechanism.

---

## Provider API Keys

These are credentials CLIProxyAPI uses to authenticate its own requests to upstream AI APIs. Each provider type has its own configuration structure.

### Key Types Summary

| Config Key | Go Type | Provider |
| :--- | :--- | :--- |
| `gemini-api-key` | `config.GeminiKey` | Google Gemini REST API |
| `claude-api-key` | `config.ClaudeKey` | Anthropic Claude API |
| `codex-api-key` | `config.CodexKey` | OpenAI Codex/Responses API |
| `openai-compatibility[].api-key-entries` | `config.OpenAICompatibilityAPIKey` | Any OpenAI-compatible endpoint |
| `vertex-api-key` | `config.VertexCompatKey` | Vertex AI-style API with `x-goog-api-key` |

Sources: [internal/config/config.go:85-103]()

### Common Fields

All key types share a common set of optional routing fields:

| Field | Purpose |
| :--- | :--- |
| `api-key` | The credential string sent to the upstream provider |
| `base-url` | Override the default API endpoint |
| `proxy-url` | Per-key HTTP/SOCKS5 proxy override |
| `prefix` | Namespace prefix; clients must send `prefix/model-name` to use this key |
| `priority` | Higher value = preferred when multiple credentials match |
| `models` | Optional model-to-alias mappings for this credential |
| `headers` | Extra HTTP headers injected into every request using this key |
| `excluded-models` | Models excluded from this credential |

---

## Service Account and Auth File Management

CLIProxyAPI manages complex credentials (OAuth tokens, Google Service Accounts) as `.json` files within the `auth-dir`.

### Auth File Persistence (`FileTokenStore`)

The `FileTokenStore` [sdk/auth/filestore.go:22-26]() is the primary mechanism for persisting these credentials. It handles:

*   **Saving**: `Save()` [sdk/auth/filestore.go:42-123]() writes `Auth` metadata and provider-specific tokens to disk. It handles metadata injection via the `metadataSetter` interface [sdk/auth/filestore.go:69-72]().
*   **Listing**: `List()` [sdk/auth/filestore.go:126-155]() enumerates all `.json` files in the auth directory.
*   **Reading**: `readAuthFile()` [sdk/auth/filestore.go:184-245]() unmarshals JSON and performs runtime logic, such as fetching project IDs for Gemini/Antigravity credentials if missing [sdk/auth/filestore.go:201-229]().

### Credential Synthesis (`FileSynthesizer`)

When the system scans the `auth-dir`, the `FileSynthesizer` [internal/watcher/synthesizer/file.go:20-25]() converts raw JSON files into internal `Auth` objects.

**Synthesizer Logic:**
1.  **Provider Mapping**: Converts the `"type"` field in JSON to internal provider keys (e.g., `"gemini"` -> `"gemini-cli"`) [internal/watcher/synthesizer/file.go:83-85]().
2.  **Virtual Auth Generation**: For multi-project Gemini credentials, `SynthesizeGeminiVirtualAuths` [internal/watcher/synthesizer/file.go:187-240]() creates one "Virtual Auth" per Google Cloud Project, allowing the proxy to route to specific projects using the same underlying credential.
3.  **Metadata Extraction**: Extracts `priority`, `note`, and `excluded-models` directly from the JSON file [internal/watcher/synthesizer/file.go:141-160]().

### Token Storage Implementations

Each provider implements a specific `TokenStorage` struct to handle serialization and metadata merging:

| Provider | Storage Struct | Implementation Details |
| :--- | :--- | :--- |
| **Gemini** | `GeminiTokenStorage` | Handles project IDs and user emails [internal/auth/gemini/gemini_token.go:20-42](). |
| **Claude** | `ClaudeTokenStorage` | Persists OAuth2 access/refresh tokens and ID tokens [internal/auth/claude/token.go:18-43](). |
| **Codex** | `CodexTokenStorage` | Includes `AccountID` and `id_token` for plan detection [internal/auth/codex/token.go:18-39](). |
| **Kimi** | `KimiTokenStorage` | Manages `DeviceID` for device flow authentication [internal/auth/kimi/token.go:17-36](). |
| **iFlow** | `IFlowTokenStorage` | Stores derived `APIKey` alongside OAuth cookies [internal/auth/iflow/iflow_token.go:13-28](). |

All these implementations use `misc.MergeMetadata` [internal/misc/credentials.go:30-61]() to flatten arbitrary key-value pairs into the final JSON file [internal/auth/gemini/gemini_token.go:63]().

### Management API for Auth Files

The `Handler` in [internal/api/handlers/management/auth_files.go]() provides endpoints to manage these files:

*   **`ListAuthFiles`**: [internal/api/handlers/management/auth_files.go:240-259]() Returns a list of all credentials, including their status (Active/Disabled) and last refresh timestamp [internal/api/handlers/management/auth_files.go:67-79]().
*   **`DeleteAuthFile`**: Removes the credential from disk.
*   **`UpdateAuthFile`**: Allows updating metadata like `priority` or `note` for a specific auth file.

**Auth File Lifecycle**

```mermaid
flowchart TD
    A["Auth Directory (.json files)"] -- "Watched by" --> B["FileWatcher"]
    B -- "Triggers" --> C["FileSynthesizer.Synthesize()\n(internal/watcher/synthesizer/file.go)"]
    C -- "Generates" --> D["coreauth.Auth objects"]
    D -- "Registered in" --> E["auth.Manager\n(sdk/auth/manager.go)"]
    E -- "Used by" --> F["Provider Executors"]
```

Sources: [sdk/auth/filestore.go](), [internal/watcher/synthesizer/file.go](), [internal/api/handlers/management/auth_files.go](), [internal/auth/gemini/gemini_token.go](), [internal/auth/claude/token.go](), [internal/auth/codex/token.go](), [internal/auth/kimi/token.go](), [internal/auth/iflow/iflow_token.go]()

---

## Provider-Specific Credential Handling

### Gemini and Antigravity
For Gemini and Antigravity (GCP-based), the system attempts to fetch the `project_id` during authentication. If a project ID is missing from a stored file, `readAuthFile` will attempt to backfill it using the stored access token [sdk/auth/filestore.go:217-226](). It also handles multi-project scenarios by normalizing filenames to `gemini-<email>-all.json` [internal/auth/gemini/gemini_token.go:96-98]().

### Codex
For Codex credentials, the system parses the `id_token` JWT to extract the `plan_type` (e.g., Plus, Team) [internal/watcher/synthesizer/file.go:161-169]().

### Callback Forwarding
During interactive OAuth logins (Gemini, Claude, Codex, Antigravity, iFlow), CLIProxyAPI starts a `callbackForwarder` [internal/api/handlers/management/auth_files.go:54-58]. This temporary server listens on specific ports (e.g., 8085 for Gemini [internal/api/handlers/management/auth_files.go:48]()) to capture the OAuth code and redirect the user back to the Management WebUI [internal/api/handlers/management/auth_files.go:151-162]().

**OAuth Callback Entity Mapping**

```mermaid
flowchart TD
    subgraph "Natural Language"
        U["User Browser"]
        P["Provider (Google/Anthropic)"]
    end
    subgraph "Code Entity Space"
        S["callbackForwarder\n(auth_files.go:54)"]
        H["http.HandlerFunc\n(auth_files.go:151)"]
        F["startCallbackForwarder\n(auth_files.go:133)"]
    end
    U -- "Auth Code" --> S
    S -- "Redirects via" --> H
    F -- "Initializes" --> S
```

Sources: [internal/api/handlers/management/auth_files.go](), [sdk/auth/filestore.go](), [internal/watcher/synthesizer/file.go](), [internal/auth/gemini/gemini_token.go](), [internal/misc/credentials.go]()

---

# Page: Token Refresh and Lifecycle

# Token Refresh and Lifecycle

<details>
<summary>Relevant source files</summary>

The following files were used as context for generating this wiki page:

- [internal/thinking/apply_user_defined_test.go](internal/thinking/apply_user_defined_test.go)
- [sdk/api/handlers/handlers.go](sdk/api/handlers/handlers.go)
- [sdk/cliproxy/auth/conductor.go](sdk/cliproxy/auth/conductor.go)
- [sdk/cliproxy/auth/conductor_overrides_test.go](sdk/cliproxy/auth/conductor_overrides_test.go)
- [sdk/cliproxy/auth/openai_compat_pool_test.go](sdk/cliproxy/auth/openai_compat_pool_test.go)
- [sdk/cliproxy/auth/scheduler.go](sdk/cliproxy/auth/scheduler.go)
- [sdk/cliproxy/auth/scheduler_benchmark_test.go](sdk/cliproxy/auth/scheduler_benchmark_test.go)
- [sdk/cliproxy/auth/scheduler_test.go](sdk/cliproxy/auth/scheduler_test.go)
- [sdk/cliproxy/auth/selector.go](sdk/cliproxy/auth/selector.go)
- [sdk/cliproxy/auth/selector_test.go](sdk/cliproxy/auth/selector_test.go)
- [sdk/cliproxy/auth/types.go](sdk/cliproxy/auth/types.go)

</details>



## Purpose and Scope

This page documents the token refresh mechanisms and credential lifecycle management in the CLIProxyAPI system. It covers automatic OAuth token refresh, quota cooldown scheduling, credential state transitions, and how the system maintains long-lived authentication sessions without manual intervention.

For initial OAuth flow setup, see [7.2 Provider-Specific OAuth Setup](). For credential file formats and storage, see [7.3 API Key and Service Account Management](). For credential rotation and failover during request execution, see [8.1 Credential Routing and Failover]().

---

## Token Refresh Architecture

The system implements a multi-layered token refresh architecture where each provider executor manages its own refresh logic while the `Manager` orchestrates credential state and quota cooldown.

### Token Lifecycle Data Flow

```mermaid
graph TB
    subgraph "Request Execution Layer"
        Request["Client Request"]
        Executor["ProviderExecutor<br/>Execute / ExecuteStream"]
    end
    
    subgraph "Token Refresh Layer"
        RefreshCheck["Manager.refreshSemaphore<br/>Concurrency Control"]
        RefreshMethod["ProviderExecutor.Refresh()<br/>Per-executor implementation"]
    end
    
    subgraph "Credential State Layer"
        Manager["auth.Manager<br/>Credential orchestration"]
        ResultObj["auth.Result<br/>Success/Failure/RetryAfter"]
        QuotaCooldown["QuotaState<br/>NextRecoverAt scheduling"]
    end
    
    subgraph "Persistence Layer"
        AuthMetadata["auth.Auth.Metadata map<br/>access_token, refresh_token"]
        Store["auth.Store<br/>Persist updated credentials"]
    end
    
    Request --> Executor
    Executor -->|"On Expiry"| RefreshCheck
    RefreshCheck --> RefreshMethod
    
    RefreshMethod --> AuthMetadata
    AuthMetadata --> Store
    
    Executor -->|"Produces"| ResultObj
    ResultObj -->|"429 or quota error"| QuotaCooldown
    QuotaCooldown --> Manager
    
    Manager -->|"Select next auth"| Executor
```

**Diagram: Token Refresh and Lifecycle Architecture**

The refresh process follows these stages:
1.  **Pre-request Token Check**: Each executor validates token freshness before making API calls [sdk/cliproxy/auth/conductor.go:32-35]().
2.  **Automatic Refresh**: Expired or soon-to-expire tokens trigger provider-specific refresh flows via `Refresh(ctx, auth)` [sdk/cliproxy/auth/conductor.go:36-37]().
3.  **Metadata Update**: Refreshed tokens update the `auth.Auth.Metadata` map with new credentials and timestamps [sdk/cliproxy/auth/types.go:73-74]().
4.  **State Management**: Execution results (captured in `auth.Result`) feed into quota cooldown scheduling and credential selection [sdk/cliproxy/auth/conductor.go:87-100]().
5.  **Persistence**: Updated credentials are saved to the `auth.Store` for durability across restarts [sdk/cliproxy/auth/conductor.go:131-131]().

**Sources:**
- [sdk/cliproxy/auth/conductor.go:28-43]()
- [sdk/cliproxy/auth/types.go:46-91]()
- [sdk/cliproxy/auth/conductor.go:86-100]()

---

## Executor-Level Token Refresh

Each provider executor implements the `Refresh` method from the `ProviderExecutor` interface [sdk/cliproxy/auth/conductor.go:28-43]().

### Refresh Method Interface

```mermaid
classDiagram
    class ProviderExecutor {
        <<interface>>
        +Identifier() string
        +Refresh(context.Context, *Auth) *Auth, error
        +Execute(context.Context, *Auth, Request, Options) Response, error
    }
    
    class Manager {
        -executors map[string]ProviderExecutor
        -refreshSemaphore chan struct
        +RegisterExecutor(ProviderExecutor)
    }

    class Auth {
        +ID string
        +Metadata map[string]any
        +Quota QuotaState
        +ModelStates map[string]*ModelState
    }

    Manager o-- ProviderExecutor : orchestrates
    ProviderExecutor ..> Auth : updates state
```

**Diagram: ProviderExecutor and Manager Interaction**

The `Manager` maintains a registry of executors [sdk/cliproxy/auth/conductor.go:132](). When a token needs refreshing, the `Manager` invokes the `Refresh` method of the corresponding `ProviderExecutor` [sdk/cliproxy/auth/conductor.go:36-37](). This method returns a new `Auth` pointer with updated metadata [sdk/cliproxy/auth/conductor.go:37-37]().

**Sources:**
- [sdk/cliproxy/auth/conductor.go:28-43]()
- [sdk/cliproxy/auth/conductor.go:130-166]()
- [sdk/cliproxy/auth/types.go:46-96]()

---

## Quota Cooldown Mechanism

When a credential exhausts its quota or hits rate limits (HTTP 429), the system enters a cooldown period. This is managed by the `QuotaState` within the `Auth` object [sdk/cliproxy/auth/types.go:98-108]().

### Cooldown Configuration
The system uses progressive backoff for rate limits:
*   **Base Backoff**: 1 second (`quotaBackoffBase`) [sdk/cliproxy/auth/conductor.go:66]().
*   **Max Backoff**: 30 minutes (`quotaBackoffMax`) [sdk/cliproxy/auth/conductor.go:67]().
*   **Global Toggle**: `SetQuotaCooldownDisabled` can disable cooling globally [sdk/cliproxy/auth/conductor.go:73-75]().

### Quota State Structure
The `QuotaState` tracks the recovery timeline:
*   `Exceeded`: Boolean flag indicating recent quota hit [sdk/cliproxy/auth/types.go:101]().
*   `NextRecoverAt`: Timestamp when the credential is eligible for selection again [sdk/cliproxy/auth/types.go:105]().
*   `BackoffLevel`: Progressive exponent for repeated failures [sdk/cliproxy/auth/types.go:107]().

**Sources:**
- [sdk/cliproxy/auth/types.go:99-108]()
- [sdk/cliproxy/auth/conductor.go:61-75]()

---

## Credential Selection and Availability

The `authScheduler` uses the current state of an `Auth` record to decide if it can be used for a request.

### Availability Logic
An `Auth` is considered blocked for a model if:
1.  The `Auth` is globally `Disabled` [sdk/cliproxy/auth/types.go:65]().
2.  The `Auth` is marked as `Unavailable` [sdk/cliproxy/auth/types.go:68]().
3.  The specific `ModelState` for the requested model is in cooldown (`Unavailable` is true) [sdk/cliproxy/auth/types.go:117-119]().
4.  The `QuotaState.NextRecoverAt` is in the future [sdk/cliproxy/auth/types.go:105]().

### Selector Priority
The `RoundRobinSelector` and `FillFirstSelector` group available credentials by priority [sdk/cliproxy/auth/selector.go:110-123]().
*   Higher priority values (defined in `Attributes["priority"]`) are preferred [sdk/cliproxy/auth/selector.go:114-122]().
*   If multiple credentials share the same priority, the system uses the configured strategy [sdk/cliproxy/auth/selector.go:20-30]().
*   If all credentials for a model are in cooldown, the system returns a `modelCooldownError` (HTTP 429) [sdk/cliproxy/auth/selector.go:41-97]().

**Sources:**
- [sdk/cliproxy/auth/selector.go:20-30]()
- [sdk/cliproxy/auth/selector.go:41-97]()
- [sdk/cliproxy/auth/selector.go:110-123]()
- [sdk/cliproxy/auth/types.go:109-126]()

---

## Concurrency and Performance

### Refresh Synchronization
The `Manager` limits the number of simultaneous refresh operations to prevent resource exhaustion:
*   **Max Concurrency**: 16 simultaneous refreshes (`refreshMaxConcurrency`) [sdk/cliproxy/auth/conductor.go:63]().
*   **Check Interval**: State is evaluated every 5 seconds (`refreshCheckInterval`) [sdk/cliproxy/auth/conductor.go:62]().
*   **Semaphore**: Controlled via `refreshSemaphore` channel [sdk/cliproxy/auth/conductor.go:184]().

### Model-Specific State
To avoid blocking an entire account due to a single model's rate limit, the system maintains `ModelStates` [sdk/cliproxy/auth/types.go:89-90](). This allows a credential to be "cooling" for one model while remaining "active" for another [sdk/cliproxy/auth/types.go:111-126]().

### Scheduler Rebuild
The `authScheduler` keeps an incremental view of provider/model scheduling state [sdk/cliproxy/auth/scheduler.go:34-40](). It can `rebuild` its entire state from an auth snapshot to ensure consistency [sdk/cliproxy/auth/scheduler.go:134-147]().

**Sources:**
- [sdk/cliproxy/auth/conductor.go:61-68]()
- [sdk/cliproxy/auth/types.go:89-90]()
- [sdk/cliproxy/auth/types.go:111-126]()
- [sdk/cliproxy/auth/scheduler.go:34-40]()
- [sdk/cliproxy/auth/scheduler.go:134-147]()

---

# Page: Advanced Features

# Advanced Features

<details>
<summary>Relevant source files</summary>

The following files were used as context for generating this wiki page:

- [config.example.yaml](config.example.yaml)
- [internal/api/handlers/management/config_basic.go](internal/api/handlers/management/config_basic.go)
- [internal/api/handlers/management/config_lists.go](internal/api/handlers/management/config_lists.go)
- [internal/api/server.go](internal/api/server.go)
- [internal/config/config.go](internal/config/config.go)
- [internal/thinking/apply_user_defined_test.go](internal/thinking/apply_user_defined_test.go)
- [internal/watcher/watcher.go](internal/watcher/watcher.go)
- [sdk/api/handlers/handlers.go](sdk/api/handlers/handlers.go)
- [sdk/cliproxy/auth/conductor.go](sdk/cliproxy/auth/conductor.go)
- [sdk/cliproxy/auth/conductor_overrides_test.go](sdk/cliproxy/auth/conductor_overrides_test.go)
- [sdk/cliproxy/auth/openai_compat_pool_test.go](sdk/cliproxy/auth/openai_compat_pool_test.go)
- [sdk/cliproxy/service.go](sdk/cliproxy/service.go)
- [test/amp_management_test.go](test/amp_management_test.go)

</details>



This page covers CLIProxyAPI capabilities beyond basic request proxying. It provides a structured overview of each advanced feature area and points to the detailed sub-pages where each is fully documented. For initial setup and basic configuration, see [Getting Started](#2) and the [Configuration Guide](#5). For core architectural details, see [Core Architecture](#3).

---

## Overview

The advanced features in CLIProxyAPI fall into eight areas:

| Feature Area | Summary | Detail Page |
|---|---|---|
| Credential Routing and Failover | Load-balancing, cooldowns, retry logic across multiple credentials | [Credential Routing and Failover](#8.1) |
| Model Mapping and Exclusion | Alias models, exclude models, OpenAI-compat pools, Amp fallback routing | [Model Mapping and Aliasing](#8.2) |
| Thinking and Reasoning Configuration | Budget vs Level modes, model capabilities, cross-provider conversion | [Thinking and Reasoning Configuration](#8.3) |
| Request and Response Logging | Per-request log files, rotation, error-only mode, structured output | [Request and Response Logging](#8.4) |
| Usage Statistics and Monitoring | Per-model and per-key metrics, token consumption tracking | [Usage Statistics and Monitoring](#8.5) |
| Streaming and Keep-Alive | SSE keep-alives, bootstrap retries, non-streaming keep-alive | [Streaming and Keep-Alive](#8.6) |
| WebSocket and Runtime Auth | WebSocket Gateway for AI Studio, dynamic credential registration | [WebSocket Gateway and Runtime Auth](#8.7) |
| Signature Cache and Thinking Validation | Multi-turn Claude thinking signature validation and TTL management | [Signature Cache and Multi-Turn Conversations](#8.8) |

The diagram below maps each feature area to the primary code entities that implement it.

**Diagram: Advanced Feature Areas and Primary Code Entities**

```mermaid
graph TD
    subgraph "Credential_Routing"
        A["Config\n(internal/config/config.go)"] --> B["RoundRobinSelector\n(sdk/cliproxy/auth/conductor.go)"]
        A --> C["FillFirstSelector\n(sdk/cliproxy/auth/conductor.go)"]
        D["QuotaExceeded\n(internal/config/config.go)"] --> E["SetQuotaCooldownDisabled\n(sdk/cliproxy/auth/conductor.go)"]
        F["RequestRetry / MaxRetryInterval\n(internal/config/config.go)"] --> G["Manager.SetRetryConfig\n(sdk/cliproxy/auth/conductor.go)"]
    end
    subgraph "Model_Control"
        H["OAuthModelAlias\n(internal/config/config.go)"] --> I["Manager.apiKeyModelAlias\n(sdk/cliproxy/auth/conductor.go)"]
        J["OAuthExcludedModels\n(internal/config/config.go)"] --> K["Manager.auths\n(sdk/cliproxy/auth/conductor.go)"]
        L["AmpCode\n(internal/config/config.go)"] --> M["AmpModule\n(internal/api/server.go)"]
    end
    subgraph "Observability"
        Q["LoggingToFile\n(internal/config/config.go)"] --> R["NewFileRequestLogger\n(internal/api/server.go)"]
        S["UsageStatisticsEnabled\n(internal/config/config.go)"] --> T["usage.RegisterPlugin\n(sdk/cliproxy/service.go)"]
    end
    subgraph "Transport"
        U["WebsocketAuth\n(internal/config/config.go)"] --> V["wsAuthEnabled\n(internal/api/server.go)"]
        W["keepAliveEnabled\n(internal/api/server.go)"] --> X["keepAliveHeartbeat\n(internal/api/server.go)"]
        Y["AuthUpdate\n(internal/watcher/watcher.go)"] --> Z["Service.handleAuthUpdate\n(sdk/cliproxy/service.go)"]
    end
```

Sources: [internal/config/config.go:27-130](), [internal/api/server.go:122-179](), [sdk/cliproxy/auth/conductor.go:129-191](), [sdk/cliproxy/service.go:32-92]()

---

## Credential Routing and Failover

When multiple credentials match a request, CLIProxyAPI selects an active one using the `RoutingConfig.Strategy`. Options include `"round-robin"` (default) or `"fill-first"` [internal/config/config.go:82-83](). These strategies are implemented by the `RoundRobinSelector` and `FillFirstSelector` types [sdk/cliproxy/auth/conductor.go:169-172]().

The system includes a sophisticated retry mechanism. `RequestRetry` defines attempts per credential, while `MaxRetryCredentials` limits how many different credentials are tried before returning an error [internal/config/config.go:71-75](). Credentials that hit rate limits enter a "cooldown" state, which can be globally toggled via `DisableCooling` [internal/config/config.go:68-69]().

See [Credential Routing and Failover](#8.1) for full details.

Sources: [internal/config/config.go:68-83](), [sdk/cliproxy/auth/conductor.go:141-145](), [sdk/cliproxy/auth/conductor_overrides_test.go:17-20]()

---

## Model Mapping and Aliasing

CLIProxyAPI provides flexible model name resolution across different providers:

| Mechanism | Configuration | Description |
|---|---|---|
| **Global OAuth Aliases** | `oauth-model-alias` | Maps client-requested names to upstream names for OAuth providers [internal/config/config.go:118-124](). |
| **API Key Aliases** | `models` (per-key) | Per-credential mapping for Gemini, Claude, and Codex [internal/config/config.go:122-124](). |
| **OpenAI-Compat Pools** | `openai-compatibility` | Aggregates multiple upstream models into a single logical pool with rotation [sdk/cliproxy/auth/openai_compat_pool_test.go:161-168](). |
| **Exclusion Lists** | `excluded-models` | Prevents specific models from being routed, supporting wildcards [internal/config/config.go:115-116](). |

See [Model Mapping and Aliasing](#8.2) for full details.

Sources: [internal/config/config.go:115-124](), [sdk/cliproxy/auth/conductor.go:146-152](), [config.example.yaml:119-126]()

---

## Thinking and Reasoning Configuration

For models supporting extended reasoning (like Claude 3.7 or Gemini 2.0 Thinking), CLIProxyAPI manages "thinking" parameters. This includes handling "budget" vs "level" modes and converting these parameters when proxying between different provider formats [internal/thinking/apply_user_defined_test.go:32-34]().

See [Thinking and Reasoning Configuration](#8.3) for the configuration schema and capability mapping.

---

## Request and Response Logging

The proxy supports detailed request/response logging for auditing and debugging. If `LoggingToFile` is enabled, logs are written to rotating files [internal/config/config.go:54-55]().

Retention is managed by `LogsMaxTotalSizeMB` and `ErrorLogsMaxFiles`, ensuring the disk doesn't fill up with historical logs [internal/config/config.go:57-63](). The `NewFileRequestLogger` handles the creation of these logs in the designated `logs` directory [internal/api/server.go:60-64]().

See [Request and Response Logging](#8.4) for full details.

Sources: [internal/config/config.go:54-63](), [internal/api/server.go:60-64](), [config.example.yaml:55-64]()

---

## Usage Statistics and Monitoring

When `UsageStatisticsEnabled` is true, the server tracks in-memory usage metrics including token consumption and request counts [internal/config/config.go:65-66](). This system supports external monitoring through a plugin architecture via `RegisterUsagePlugin` [sdk/cliproxy/service.go:99-101]().

See [Usage Statistics and Monitoring](#8.5) for monitoring setup and metrics definitions.

Sources: [internal/config/config.go:65-66](), [sdk/cliproxy/service.go:94-101](), [config.example.yaml:66-67]()

---

## Streaming and Keep-Alive

To maintain long-lived connections for AI responses, CLIProxyAPI implements several keep-alive mechanisms:

- **SSE Keep-Alive**: Periodically sends empty lines during streaming to prevent intermediate proxy timeouts [config.example.yaml:106-107]().
- **Non-streaming Keep-Alive**: Emits blank lines for standard HTTP responses if the generation takes a long time [config.example.yaml:102-103]().
- **Local Keep-Alive**: A dedicated endpoint (`/v1/keep-alive`) used in local management modes to ensure the proxy process stays alive as long as a client is active [internal/api/server.go:94-104]().

See [Streaming and Keep-Alive](#8.6) for implementation details.

Sources: [internal/api/server.go:94-104](), [config.example.yaml:98-109](), [sdk/api/handlers/handlers.go:144-168]()

---

## WebSocket Gateway and Runtime Auth

CLIProxyAPI includes a WebSocket gateway (`/v1/ws`) primarily used for integrating with Google AI Studio providers [sdk/cliproxy/service.go:204-220](). 

This system supports **Runtime-Only Authentication**, where credentials (like `aistudio-` channels) are registered dynamically when a WebSocket connection is established, rather than being loaded from a config file [sdk/cliproxy/service.go:222-247](). These updates are propagated via the `Watcher.DispatchRuntimeAuthUpdate` mechanism [internal/watcher/watcher.go:149-151]().

See [WebSocket Gateway and Runtime Auth](#8.7) for full details.

**Diagram: Runtime Auth Update Flow**

```mermaid
sequenceDiagram
    participant W as WebSocket Client
    participant G as wsrelay.Manager
    participant S as Service (cliproxy)
    participant M as Manager (auth)

    W->>G: Connect to /v1/ws
    G->>S: wsOnConnected(channelID)
    S->>S: Create Auth (runtime_only=true)
    S->>S: DispatchRuntimeAuthUpdate
    S->>M: handleAuthUpdate (ActionAdd)
    M->>M: Register(auth)
    Note right of M: Credential now available for routing
```

Sources: [sdk/cliproxy/service.go:204-247](), [internal/watcher/watcher.go:146-151](), [internal/config/config.go:85-86]()

---

## Signature Cache and Multi-Turn Conversations

For Claude models using the Messages API, "thinking" responses often include a unique signature. In multi-turn conversations, this signature must be cached and validated in subsequent turns to maintain context integrity. CLIProxyAPI implements a signature cache with TTL management to handle these stateful interactions automatically.

See [Signature Cache and Multi-Turn Conversations](#8.8) for cache configuration and validation logic.

---

## Hot Reload and Dynamic Updates

Most advanced features support hot-reloading without a server restart. The `Watcher` monitors `config.yaml` and the `auth-dir` for changes [internal/watcher/watcher.go:31-45](). When a change is detected, it triggers the `reloadCallback`, which updates the `Server` and `Manager` instances with the new configuration [internal/watcher/watcher.go:89-117]().

Sources: [internal/watcher/watcher.go:31-117](), [internal/api/server.go:132-138](), [sdk/cliproxy/service.go:174-202]()

---

# Page: Credential Routing and Failover

# Credential Routing and Failover

<details>
<summary>Relevant source files</summary>

The following files were used as context for generating this wiki page:

- [internal/thinking/apply_user_defined_test.go](internal/thinking/apply_user_defined_test.go)
- [sdk/api/handlers/handlers.go](sdk/api/handlers/handlers.go)
- [sdk/cliproxy/auth/conductor.go](sdk/cliproxy/auth/conductor.go)
- [sdk/cliproxy/auth/conductor_overrides_test.go](sdk/cliproxy/auth/conductor_overrides_test.go)
- [sdk/cliproxy/auth/openai_compat_pool_test.go](sdk/cliproxy/auth/openai_compat_pool_test.go)
- [sdk/cliproxy/auth/scheduler.go](sdk/cliproxy/auth/scheduler.go)
- [sdk/cliproxy/auth/scheduler_benchmark_test.go](sdk/cliproxy/auth/scheduler_benchmark_test.go)
- [sdk/cliproxy/auth/scheduler_test.go](sdk/cliproxy/auth/scheduler_test.go)
- [sdk/cliproxy/auth/selector.go](sdk/cliproxy/auth/selector.go)
- [sdk/cliproxy/auth/selector_test.go](sdk/cliproxy/auth/selector_test.go)
- [sdk/cliproxy/auth/types.go](sdk/cliproxy/auth/types.go)

</details>



## Purpose and Scope

This page documents how CLIProxyAPI selects credentials for outbound AI provider requests, how it distributes load across multiple accounts of the same provider, what happens when a request fails, and how the system tracks quota state to avoid re-routing traffic to cooling-down credentials.

The mechanism is implemented almost entirely inside the `auth` package [sdk/cliproxy/auth/conductor.go](). For how the `Manager` is initialized and wired together at startup, see [3.3](). For how OAuth tokens are refreshed before expiry, see [7.4](). For how model aliases are configured, see [8.2]().

---

## Core Participants

The three key types that implement credential routing are `Manager`, `Selector`, and `Auth`.

**Key type diagram:**

```mermaid
classDiagram
    class Manager {
        +auths map~string~Auth
        +executors map~string~ProviderExecutor
        +selector Selector
        +hook Hook
        +providerOffsets map~string~int
        +requestRetry atomic.Int32
        +maxRetryInterval atomic.Int64
        +Execute()
        +ExecuteStream()
        +ExecuteCount()
        +MarkResult()
        +SetRetryConfig()
        +SetSelector()
    }
    class Selector {
        <<interface>>
        +Pick(ctx, provider, model, opts, auths) Auth
    }
    class RoundRobinSelector {
        +cursors map~string~int
        +Pick()
    }
    class FillFirstSelector {
        +Pick()
    }
    class Auth {
        +ID string
        +Provider string
        +Prefix string
        +Disabled bool
        +Unavailable bool
        +Quota QuotaState
        +ModelStates map~string~ModelState
        +NextRetryAfter time.Time
        +Attributes map~string~string
        +Metadata map~string~any
    }
    class QuotaState {
        +Exceeded bool
        +NextRecoverAt time.Time
        +BackoffLevel int
        +Reason string
    }
    class ModelState {
        +Status Status
        +Unavailable bool
        +NextRetryAfter time.Time
        +Quota QuotaState
        +LastError Error
    }
    Manager --> Selector : "uses"
    Manager --> Auth : "manages pool"
    RoundRobinSelector ..|> Selector
    FillFirstSelector ..|> Selector
    Auth --> QuotaState : "global quota"
    Auth --> ModelState : "per-model quota"
```

Sources: [sdk/cliproxy/auth/conductor.go:130-166](), [sdk/cliproxy/auth/selector.go:20-30](), [sdk/cliproxy/auth/types.go:46-126]()

---

## Selectors

The `Selector` interface has one method: `Pick(ctx, provider, model, opts, auths) (*Auth, error)`. It receives the full filtered list of available, non-blocked auths and returns the one to use [sdk/cliproxy/auth/conductor.go:102-105]().

Two built-in implementations are provided:

| Selector | Strategy | Best for |
|---|---|---|
| `RoundRobinSelector` | Cycles through available credentials in sorted ID order | Spreading load evenly across accounts with rolling-window limits |
| `FillFirstSelector` | Always picks the first available (deterministic, lexicographic ID order) | Saturating one account before moving to the next |

`RoundRobinSelector` is the default when `NewManager` is called with a `nil` selector [sdk/cliproxy/auth/conductor.go:169-172]().

Sources: [sdk/cliproxy/auth/conductor.go:169-181](), [sdk/cliproxy/auth/selector.go:20-30](), [sdk/cliproxy/auth/selector.go:255-363]()

### Priority Buckets

Before the selector runs, `getAvailableAuths` partitions candidates by the integer `priority` attribute read from `Auth.Attributes["priority"]` [sdk/cliproxy/auth/selector.go:110-123](). Only the highest priority bucket that has at least one non-blocked credential is offered to the selector [sdk/cliproxy/auth/selector.go:235-244]().

This means:
- If all priority-10 credentials are cooling down, the system automatically falls back to priority-0 credentials [sdk/cliproxy/auth/selector.go:214-249]().
- Within the winning bucket, the selector's algorithm (round-robin or fill-first) applies normally.

Sources: [sdk/cliproxy/auth/selector.go:214-249](), [sdk/cliproxy/auth/selector.go:110-123]()

### Gemini CLI Two-Level Round-Robin

When all candidates carry a `gemini_virtual_parent` attribute, `RoundRobinSelector.Pick` applies a two-level round-robin:

1. **Outer cursor** cycles through distinct parent credential groups [sdk/cliproxy/auth/selector.go:275-285]().
2. **Inner cursor** cycles within the selected parent's project auths [sdk/cliproxy/auth/selector.go:294-313]().

If any auth in the candidate list lacks `gemini_virtual_parent`, the selector falls back to flat round-robin [sdk/cliproxy/auth/selector.go:326-351]().

Sources: [sdk/cliproxy/auth/selector.go:255-313](), [sdk/cliproxy/auth/selector.go:326-351]()

---

## Request Execution and Failover

The `Manager` orchestrates the flow from incoming API request to provider execution, handling retries across multiple credentials if errors occur.

**Execution flow diagram:**

```mermaid
flowchart TD
    A["Manager.Execute / ExecuteStream / ExecuteCount"] --> B["normalizeProviderKeys()"]
    B --> C["Manager.retrySettings()"]
    C --> D["Loop: Manager.executeMixedOnce / executeStreamMixedOnce"]
    D --> E["Manager.pickNextMixed()"]
    E --> F["authScheduler.pickMixed() / pickSingle()"]
    F --> G["Rewrite model for auth\n(prefix strip, OAuth alias, API key alias)"]
    G --> H["ProviderExecutor.Execute() / ExecuteStream()"]
    H -->|"success"| I["Manager.MarkResult(success)\nReturn response"]
    H -->|"error"| J["Manager.MarkResult(failure)\nAdd auth.ID to tried set"]
    J --> K{"isRequestInvalidError?"}
    K -->|"yes - bad request"| L["Return error immediately\n(no retry)"]
    K -->|"no"| M["continue inner loop\n(next auth for same attempt)"]
    M --> E
    E -->|"all auths exhausted"| N["Manager.shouldRetryAfterError()"]
    N -->|"retry allowed"| O["Manager.closestCooldownWait()\nManager.waitForCooldown()"]
    O --> D
    N -->|"no retry"| P["Return last error"]
```

Sources: [sdk/cliproxy/auth/conductor.go:498-588](), [sdk/cliproxy/auth/conductor.go:591-645](), [sdk/cliproxy/auth/conductor.go:703-788](), [sdk/cliproxy/auth/scheduler.go:173-232]()

### Inner Loop: Trying Each Auth

Each call to `executeMixedOnce` (and its streaming/count counterparts) builds a `tried` map keyed by `Auth.ID` [sdk/cliproxy/auth/conductor.go:594](). On each iteration, `pickNextMixed` picks the next candidate not already in `tried`. When the scheduler returns an error (no more candidates), the inner loop ends.

This means in a single attempt, **every available credential is tried before giving up or waiting**.

Sources: [sdk/cliproxy/auth/conductor.go:591-645]()

### Outer Loop: Retry with Cooldown Wait

After exhausting all candidates for an attempt, `shouldRetryAfterError` decides whether to retry:

1. `maxRetryInterval` must be non-zero (set via `SetRetryConfig`) [sdk/cliproxy/auth/conductor.go:1172-1190]().
2. The error must not be a request-invalid error (e.g., 400 Bad Request) [sdk/cliproxy/auth/conductor.go:1120-1130]().
3. `closestCooldownWait` scans all matching-provider auths and returns the minimum wait time until any of them exits cooldown [sdk/cliproxy/auth/conductor.go:1115-1170]().
4. If `wait ≤ maxRetryInterval`, the system sleeps for that duration and then retries the full inner loop.

Per-credential retry overrides are respected: each `Auth` can store a `request_retry` integer in `Auth.Metadata` to override the global retry count [sdk/cliproxy/auth/conductor_overrides_test.go:15-63]().

Sources: [sdk/cliproxy/auth/conductor.go:1172-1190](), [sdk/cliproxy/auth/conductor.go:1115-1170](), [sdk/cliproxy/auth/conductor_overrides_test.go:15-63]()

---

## Auth Blocking and Cooldown

The function `isAuthBlockedForModel` decides whether a given auth is eligible for selection. It is used by the `authScheduler` to filter candidates.

**Blocking logic decision tree:**

```mermaid
flowchart TD
    A["isAuthBlockedForModel(auth, model, now)"] --> B{"auth.Disabled\nor Status == StatusDisabled?"}
    B -->|"yes"| C["blocked: blockReasonDisabled"]
    B -->|"no"| D{"model != empty?"}
    D -->|"yes"| E{"ModelStates[model] exists?"}
    E -->|"yes, state.Status == StatusDisabled"| F["blocked: blockReasonDisabled"]
    E -->|"yes, state.Unavailable && state.NextRetryAfter.After(now)"| G{"state.Quota.Exceeded?"}
    G -->|"yes"| H["blocked: blockReasonCooldown\nnext = NextRetryAfter or Quota.NextRecoverAt"]
    G -->|"no"| I["blocked: blockReasonOther"]
    E -->|"no matching state"| J["not blocked"]
    D -->|"no model"| K{"auth.Unavailable && NextRetryAfter.After(now)?"}
    K -->|"yes, Quota.Exceeded"| L["blocked: blockReasonCooldown"]
    K -->|"yes, not quota"| M["blocked: blockReasonOther"]
    K -->|"no"| N["not blocked"]
```

Sources: [sdk/cliproxy/auth/selector.go:365-422]()

### Cooldown Error Response

When **all** candidates for a model are in `blockReasonCooldown` state, the system returns a `modelCooldownError` [sdk/cliproxy/auth/selector.go:214-233](). This error:
- Has HTTP status `429 Too Many Requests` [sdk/cliproxy/auth/selector.go:95-97]().
- Carries a `Retry-After` header with the seconds until the earliest credential recovers [sdk/cliproxy/auth/selector.go:99-108]().
- Embeds a JSON body with `code: "model_cooldown"`, `reset_time`, and `reset_seconds` [sdk/cliproxy/auth/selector.go:77-83]().

Sources: [sdk/cliproxy/auth/selector.go:41-108](), [sdk/cliproxy/auth/selector.go:214-233]()

### Per-Credential Cooldown Disable

A credential can opt out of quota cooldown entirely by setting `disable_cooling: true` in its auth file metadata. The global flag `SetQuotaCooldownDisabled(true)` disables cooldown for all credentials that do not have a per-credential override [sdk/cliproxy/auth/conductor.go:72-84]().

Sources: [sdk/cliproxy/auth/conductor.go:69-84]()

---

## Quota State and Backoff

`QuotaState` tracks progressive backoff for a credential or a per-model `ModelState` [sdk/cliproxy/auth/types.go:98-108]().

| Field | Type | Meaning |
|---|---|---|
| `Exceeded` | `bool` | Whether a quota error was recently seen |
| `NextRecoverAt` | `time.Time` | When the credential may be tried again |
| `BackoffLevel` | `int` | Exponent for the next cooldown duration |
| `Reason` | `string` | Human-readable provider description |

Cooldown constants defined in `conductor.go`:

| Constant | Value |
|---|---|
| `quotaBackoffBase` | 1 second |
| `quotaBackoffMax` | 30 minutes |
| `refreshPendingBackoff` | 1 minute |
| `refreshFailureBackoff` | 5 minutes |
| `refreshCheckInterval` | 5 seconds |

Sources: [sdk/cliproxy/auth/conductor.go:61-68](), [sdk/cliproxy/auth/types.go:98-126]()

### MarkResult

After each execution attempt, `MarkResult` is called with a `Result` struct containing:
- `AuthID` — which credential was used.
- `Success` — whether the call succeeded.
- `RetryAfter` — a provider-supplied delay hint (from 429 responses).
- `Error` — the failure details including HTTP status.

`MarkResult` updates the auth's `QuotaState` and `ModelState` accordingly and persists the updated auth [sdk/cliproxy/auth/conductor.go:623-643](). It also fires the `Hook.OnResult` callback [sdk/cliproxy/auth/conductor.go:127]().

Sources: [sdk/cliproxy/auth/conductor.go:87-100](), [sdk/cliproxy/auth/conductor.go:623-643]()

---

## Model Name Rewriting

Before the request reaches an executor, the model name may be rewritten in three steps applied in sequence:

```mermaid
flowchart LR
    A["Client model name\n(e.g. teamA/gemini-2.5-pro)"] --> B["Manager.rewriteModelForAuth()\nStrip auth.Prefix"]
    B --> C["Manager.applyOAuthModelAlias()\nOAuth alias table lookup"]
    C --> D["Manager.applyAPIKeyModelAlias()\nAPI key config alias lookup"]
    D --> E["Upstream model name\n(sent to ProviderExecutor)"]
```

1. **`rewriteModelForAuth`**: If `Auth.Prefix` is set (e.g. `"teamA"`), strips `"teamA/"` from the beginning of the model name [sdk/cliproxy/auth/conductor.go:861-875]().
2. **`applyOAuthModelAlias`**: Looks up the model in the per-channel OAuth alias table stored in `Manager.oauthModelAlias` [sdk/cliproxy/auth/conductor.go:877-897]().
3. **`applyAPIKeyModelAlias`**: Looks up the model in a per-auth-ID alias table built from `config.yaml` model entries [sdk/cliproxy/auth/conductor.go:899-923]().

Sources: [sdk/cliproxy/auth/conductor.go:861-923](), [sdk/cliproxy/auth/conductor.go:619-621]()

---

## Multi-Provider Routing

A single incoming request can be satisfied by credentials from multiple providers (e.g. both `gemini` and `claude` for the same model).

`normalizeProviderKeys` deduplicates and lowercases this list [sdk/cliproxy/auth/conductor.go:1088-1106](). `pickNextMixed` then iterates the providers (rotating the start index per model via `providerOffsets`) and calls the scheduler for each provider's credential pool [sdk/cliproxy/auth/conductor.go:499-527]().

The `tried` set spans across all providers in a single attempt, ensuring a credential is not tried twice in the same request attempt [sdk/cliproxy/auth/conductor.go:594]().

Sources: [sdk/cliproxy/auth/conductor.go:1088-1106](), [sdk/cliproxy/auth/conductor.go:499-527]()

---

## Hook Interface

`Manager` accepts a `Hook` for observing auth lifecycle events. `NoopHook` is used when no hook is supplied [sdk/cliproxy/auth/conductor.go:173-175]().

| Hook Method | When Called |
|---|---|
| `OnAuthRegistered(ctx, auth)` | A new credential is registered via `Manager.Register` |
| `OnAuthUpdated(ctx, auth)` | An existing credential changes state via `Manager.Update` |
| `OnResult(ctx, result)` | After every execution attempt, success or failure |

Sources: [sdk/cliproxy/auth/conductor.go:108-127]()

---

## Configuration Reference

| Setting | Location | Effect |
|---|---|---|
| Global retry count | `Manager.SetRetryConfig(retry, ...)` | How many outer-loop retries are allowed |
| Max retry wait | `Manager.SetRetryConfig(..., maxRetryInterval)` | Upper bound on cooldown wait before giving up |
| Per-credential retry | `Auth.Metadata["request_retry"]` | Overrides global retry count for one credential |
| Disable cooldown (global) | `SetQuotaCooldownDisabled(true)` | Skips quota cooldown for all credentials without override |
| Disable cooldown (per credential) | `Auth.Metadata["disable_cooling"]` | Overrides global cooldown flag for one credential |
| Priority | `Auth.Attributes["priority"]` | Integer; higher priority credentials are used first |
| Prefix routing | `Auth.Prefix` | Namespace prefix stripped from model names before routing |

Sources: [sdk/cliproxy/auth/conductor.go:384-397](), [sdk/cliproxy/auth/conductor.go:69-84](), [sdk/cliproxy/auth/selector.go:110-123](), [sdk/cliproxy/auth/types.go:50-54]()

---

# Page: Model Mapping and Aliasing

# Model Mapping and Aliasing

<details>
<summary>Relevant source files</summary>

The following files were used as context for generating this wiki page:

- [internal/api/modules/amp/amp.go](internal/api/modules/amp/amp.go)
- [internal/api/modules/amp/fallback_handlers.go](internal/api/modules/amp/fallback_handlers.go)
- [internal/api/modules/amp/fallback_handlers_test.go](internal/api/modules/amp/fallback_handlers_test.go)
- [internal/api/modules/amp/gemini_bridge.go](internal/api/modules/amp/gemini_bridge.go)
- [internal/api/modules/amp/gemini_bridge_test.go](internal/api/modules/amp/gemini_bridge_test.go)
- [internal/api/modules/amp/model_mapping.go](internal/api/modules/amp/model_mapping.go)
- [internal/api/modules/amp/model_mapping_test.go](internal/api/modules/amp/model_mapping_test.go)
- [internal/api/modules/amp/response_rewriter.go](internal/api/modules/amp/response_rewriter.go)
- [internal/api/modules/amp/response_rewriter_test.go](internal/api/modules/amp/response_rewriter_test.go)
- [internal/api/modules/amp/routes.go](internal/api/modules/amp/routes.go)
- [internal/api/modules/amp/routes_test.go](internal/api/modules/amp/routes_test.go)
- [internal/config/oauth_model_alias_test.go](internal/config/oauth_model_alias_test.go)
- [internal/util/claude_model.go](internal/util/claude_model.go)
- [internal/util/claude_model_test.go](internal/util/claude_model_test.go)
- [internal/watcher/diff/oauth_model_alias.go](internal/watcher/diff/oauth_model_alias.go)
- [sdk/cliproxy/auth/conductor_availability_test.go](sdk/cliproxy/auth/conductor_availability_test.go)
- [sdk/cliproxy/auth/oauth_model_alias.go](sdk/cliproxy/auth/oauth_model_alias.go)
- [sdk/cliproxy/auth/oauth_model_alias_test.go](sdk/cliproxy/auth/oauth_model_alias_test.go)
- [sdk/cliproxy/service_oauth_model_alias_test.go](sdk/cliproxy/service_oauth_model_alias_test.go)

</details>



This document details the internal systems for controlling model availability, naming, and routing in CLIProxyAPI. It covers **Model Exclusion** (restricting access per credential), **OAuth Model Aliases** (global name mapping for OAuth channels), **Per-Credential Model Aliases** (mapping in API key configs), **OpenAI-Compatible Model Pools** (load-balanced alias groups), and **Amp Model Mapping** (routing Amp CLI requests to local alternatives).

---

## 1. Overview

CLIProxyAPI implements a multi-layered mapping and aliasing architecture to decouple client-side model names from upstream provider identifiers.

| System | Scope | Primary Use Case |
| :--- | :--- | :--- |
| **Model Exclusion** | Per-Credential | Cost control, quota management, and tier-based access. |
| **OAuth Model Alias** | Per-Channel | Global renaming/forking for all OAuth-based credentials. |
| **API Key Aliases** | Per-Credential | Defining custom model IDs for specific API keys. |
| **OpenAI-Compat Pools** | Per-Auth | Grouping multiple upstream models under a single alias. |
| **Amp Model Mapping** | Amp Module | Redirecting Amp CLI requests to local providers. |

---

## 2. OAuth Model Aliases

OAuth Model Aliases provide global model name mapping for OAuth and file-backed authentication channels (e.g., `gemini-cli`, `claude`, `antigravity`). These aliases are applied during the model registration phase in the `auth.Manager`.

### Configuration and Migration
Aliases are defined in `config.yaml` under `oauth-model-alias`. The system automatically migrates legacy `oauth-model-mappings` to this new structure.

```yaml
oauth-model-alias:
  antigravity:
    - name: "rev19-uic3-1p"
      alias: "gemini-2.5-computer-use-preview"
  claude:
    - name: "claude-3-5-sonnet-20241022"
      alias: "claude-3.5-sonnet"
```

### Implementation Logic
The `auth.Manager` stores these mappings in an `atomic.Value` via the `oauthModelAlias` field [sdk/cliproxy/auth/oauth_model_alias.go:70](). When a request is executed, `applyOAuthModelAlias` resolves the upstream model name while keeping the client-visible model name unchanged for translation and response formatting [sdk/cliproxy/auth/oauth_model_alias.go:75-81]().

The system uses `compileOAuthModelAliasTable` to build a reverse lookup map (`alias` -> `original_name`) for each channel [sdk/cliproxy/auth/oauth_model_alias.go:20-56]().

**Sources**: [sdk/cliproxy/auth/oauth_model_alias.go:20-81](), [internal/config/config.go:148-156]()

---

## 3. OpenAI-Compatible Model Pools

For `openai-compatibility` providers, CLIProxyAPI supports "Model Pools." This allows a single client-facing alias to map to a list of upstream models. The `auth.Manager` performs rotation across these models for each request to balance load or handle varying rate limits.

### Data Flow and Rotation
The manager maintains state to track the rotation per authentication ID.

```mermaid
graph TD
    Request["Request (model: 'my-pool')"]
    Manager["auth.Manager.Execute()"]
    Lookup["Lookup Pool for Alias 'my-pool'"]
    Select["Select upstream model from pool"]
    Increment["Update rotation state"]
    Upstream["Execute with Upstream Model ID"]

    Request --> Manager
    Manager --> Lookup
    Lookup --> Select
    Select --> Increment
    Increment --> Upstream
```
**Diagram: OpenAI-Compatible Pool Rotation Logic**

**Sources**: [sdk/cliproxy/auth/oauth_model_alias.go:114-168]()

---

## 4. Amp Model Mapping

The Amp module (`internal/api/modules/amp`) includes a specialized `ModelMapper` to intercept requests from the Amp CLI. This system allows the proxy to satisfy requests for models not natively available in the user's local configuration by remapping them to available alternatives.

### The ModelMapper Interface
The `DefaultModelMapper` handles both exact string matches and regex-based patterns [internal/api/modules/amp/model_mapping.go:29-33]().

| Feature | Implementation | Behavior |
| :--- | :--- | :--- |
| **Exact Match** | `map[string]string` | Case-insensitive lookup [internal/api/modules/amp/model_mapping.go:69](). |
| **Regex Match** | `[]regexMapping` | Evaluated in configuration order [internal/api/modules/amp/model_mapping.go:73-80](). |
| **Thinking Suffix** | `thinking.ParseSuffix` | Preserves suffixes like `(8192)` across mappings [internal/api/modules/amp/model_mapping.go:103-105](). |

### Fallback Handler Pipeline
The `FallbackHandler` wraps standard Gin handlers. It extracts the model from the request body, resolves the mapping, and rewrites the body if a mapping is applied [internal/api/modules/amp/fallback_handlers.go:114-143](). If `forceModelMappings` is enabled in config, mappings take precedence over local API keys [internal/api/modules/amp/fallback_handlers.go:187-192]().

```mermaid
sequenceDiagram
    participant Client as Amp CLI
    participant FH as "amp.FallbackHandler"
    participant Mapper as "amp.DefaultModelMapper"
    participant Handler as Local Provider Handler
    participant Upstream as AmpCode.com (Credits)

    Client->>FH: POST /api/provider/anthropic/v1/messages (model: opus-4.5)
    FH->>Mapper: MapModel("opus-4.5")
    alt Mapping Found
        Mapper-->>FH: "claude-3.5-sonnet"
        FH->>FH: rewriteModelInRequest()
        FH->>Handler: Process with local Claude credential
    else No Mapping & No Local Provider
        FH->>Upstream: ReverseProxy.ServeHTTP() (Uses Amp Credits)
    end
```
**Diagram: Amp Fallback and Mapping Sequence**

**Sources**: [internal/api/modules/amp/model_mapping.go:19-109](), [internal/api/modules/amp/fallback_handlers.go:114-200](), [internal/api/modules/amp/amp.go:127-130]()

---

## 5. Model Exclusion System

Model exclusion prevents specific credentials from being selected for certain models. This is enforced by the `auth.Manager` during the credential selection process.

### Exclusion Logic and Hashing
To avoid unnecessary re-registrations during config updates, the system computes a hash for each credential's exclusion list. If the hash of the patterns in the configuration hasn't changed, the credential's internal state is preserved during hot-reload.

**Sources**: [internal/api/modules/amp/amp.go:180-210](), [internal/api/modules/amp/routes.go:53-59]()

---

## 6. Response Model Rewriting

When a model is aliased or mapped, the client expects the response to contain the model name it originally requested, not the internal upstream ID. The `ResponseRewriter` intercepts the response stream to perform this substitution [internal/api/modules/amp/response_rewriter.go:18-24]().

### Features
* **JSON Rewriting**: Uses `gjson` and `sjson` to replace fields like `model` or `message.model` [internal/api/modules/amp/response_rewriter.go:123-125]().
* **SSE Support**: Parses Server-Sent Events (SSE) and rewrites the `data:` chunks in real-time [internal/api/modules/amp/response_rewriter.go:93-102]().
* **Amp Compatibility**: Automatically injects empty signatures into `tool_use` or `thinking` blocks to prevent Amp TUI crashes [internal/api/modules/amp/response_rewriter.go:127-155](). It also suppresses `thinking` blocks if they appear alongside tool usage [internal/api/modules/amp/response_rewriter.go:169-208]().

```mermaid
graph LR
    Upstream["Upstream Response"]
    RW["amp.ResponseRewriter"]
    Sign["ensureAmpSignature()"]
    Think["suppressAmpThinking()"]
    Model["rewriteModelInResponse()"]
    Client["Client (Amp CLI)"]

    Upstream --> RW
    RW --> Sign
    Sign --> Think
    Think --> Model
    Model --> Client
```
**Diagram: Response Rewriting Pipeline**

**Sources**: [internal/api/modules/amp/response_rewriter.go:127-226](), [internal/api/modules/amp/response_rewriter.go:73-103]()

---

# Page: Thinking and Reasoning Configuration

# Thinking and Reasoning Configuration

<details>
<summary>Relevant source files</summary>

The following files were used as context for generating this wiki page:

- [internal/api/handlers/management/logs.go](internal/api/handlers/management/logs.go)
- [internal/logging/global_logger.go](internal/logging/global_logger.go)
- [internal/runtime/executor/payload_helpers.go](internal/runtime/executor/payload_helpers.go)
- [internal/thinking/apply.go](internal/thinking/apply.go)
- [internal/thinking/convert.go](internal/thinking/convert.go)
- [internal/thinking/provider/antigravity/apply.go](internal/thinking/provider/antigravity/apply.go)
- [internal/thinking/provider/claude/apply.go](internal/thinking/provider/claude/apply.go)
- [internal/thinking/provider/codex/apply.go](internal/thinking/provider/codex/apply.go)
- [internal/thinking/provider/gemini/apply.go](internal/thinking/provider/gemini/apply.go)
- [internal/thinking/provider/geminicli/apply.go](internal/thinking/provider/geminicli/apply.go)
- [internal/thinking/provider/kimi/apply.go](internal/thinking/provider/kimi/apply.go)
- [internal/thinking/provider/kimi/apply_test.go](internal/thinking/provider/kimi/apply_test.go)
- [internal/thinking/provider/openai/apply.go](internal/thinking/provider/openai/apply.go)
- [internal/thinking/strip.go](internal/thinking/strip.go)
- [internal/thinking/suffix.go](internal/thinking/suffix.go)
- [internal/thinking/types.go](internal/thinking/types.go)
- [internal/thinking/validate.go](internal/thinking/validate.go)
- [internal/watcher/config_reload.go](internal/watcher/config_reload.go)
- [sdk/translator/registry.go](sdk/translator/registry.go)
- [sdk/translator/registry_test.go](sdk/translator/registry_test.go)
- [test/thinking_conversion_test.go](test/thinking_conversion_test.go)

</details>



This page documents the system's extended thinking and reasoning configuration capabilities, which enable control over AI model reasoning depth and budget allocation. The thinking system provides a unified interface for configuring reasoning parameters across multiple providers (Gemini, Claude, OpenAI/Codex, iFlow, Antigravity) with automatic validation, format conversion, and model capability enforcement.

For general model configuration and selection, see **Model Registry and Selection (3.6)**. For request payload defaults and overrides, see **Payload Configuration Rules (5.4)**. For signature caching and Claude thinking block validation across conversation turns, see **Signature Cache and Thinking Validation (8.8)**.

## Overview

The thinking configuration system allows users to control how much computational budget AI models allocate to reasoning before generating responses. Different providers support different thinking mechanisms:

- **Budget-based**: Gemini, Claude, Antigravity use token budgets (e.g., 8192 tokens).
- **Level-based**: OpenAI, Codex use discrete effort levels (`minimal`, `low`, `medium`, `high`, `xhigh`).
- **Hybrid**: Some Gemini 3 models support both budgets and levels.

The system automatically converts between formats and validates configurations against model capabilities, with intelligent clamping when values are out of range.

**Configuration Methods**:
1.  **Model name suffix**: `gemini-2.5-pro(8192)` or `gpt-5.2(medium)`.
2.  **Request body JSON**: Provider-specific thinking parameters.
3.  **Default payload rules**: Configuration file defaults applied via `applyPayloadConfigWithRoot` [internal/runtime/executor/payload_helpers.go:14-152]().

Sources: [internal/thinking/apply.go:1-88](), [test/thinking_conversion_test.go:46-164](), [internal/runtime/executor/payload_helpers.go:14-152]()

## Model Thinking Capabilities

### ThinkingSupport Structure

Each model in the registry declares its thinking capabilities via the `ThinkingSupport` structure in `internal/registry`. The `detectModelCapability` function analyzes this structure to classify models [internal/thinking/validate.go:70-99]().

```go
type ThinkingSupport struct {
    Min             int      // Minimum token budget
    Max             int      // Maximum token budget
    ZeroAllowed     bool     // Whether budget=0 (disabled) is allowed
    DynamicAllowed  bool     // Whether auto/-1 (dynamic) is supported
    Levels          []string // Supported effort levels (low, medium, high, etc.)
}
```

### Model Capability Classes

The system categorizes models into four capability classes to determine how to translate thinking requests.

Title: Model Capability Mapping
```mermaid
graph TB
    subgraph "Capability Space"
        B["CapabilityBudgetOnly"]
        L["CapabilityLevelOnly"]
        H["CapabilityHybrid"]
        N["CapabilityNone"]
    end
    
    subgraph "Code Entities (internal/registry)"
        M1["ModelInfo: gemini-2.5-pro"]
        M2["ModelInfo: gpt-4.5-preview"]
        M3["ModelInfo: gemini-3-flash"]
    end

    M1 -->|Thinking.Max > 0| B
    M2 -->|Thinking.Levels != nil| L
    M3 -->|Both fields present| H
    
    subgraph "Functions"
        F1["detectModelCapability(modelInfo)"]
    end
    
    F1 -.-> B
    F1 -.-> L
    F1 -.-> H
```

Sources: [internal/thinking/validate.go:70-99](), [internal/thinking/apply.go:44-50]()

## Configuration Modes and Syntax

### ThinkingConfig Structure

The internal representation of a thinking request is stored in the `ThinkingConfig` struct.

| Mode | Description | Budget Value | Level Value |
|------|-------------|--------------|-------------|
| `ModeNone` | Thinking disabled | 0 | empty |
| `ModeBudget` | Token budget specified | > 0 | empty |
| `ModeLevel` | Effort level specified | 0 | valid level |
| `ModeAuto` | Dynamic/auto allocation | -1 | empty |

### Model Name Suffix Syntax

The system supports thinking configuration via model name suffixes. When a suffix is present, it takes priority over any thinking parameters in the request body [internal/thinking/apply.go:136-158]().

| Syntax | Mode | Example |
|--------|------|---------|
| `(none)` | None | `gemini-2.5-pro(none)` |
| `(auto)` | Auto | `gemini-2.5-pro(auto)` |
| `(low)` | Level | `gpt-5.2(low)` |
| `(8192)` | Budget | `gemini-2.5-pro(8192)` |

Sources: [internal/thinking/apply.go:109-146](), [test/thinking_conversion_test.go:46-164]()

## Validation and Normalization

The `ValidateConfig` function in `internal/thinking/validate.go` is the core engine for cross-provider compatibility.

### Validation Pipeline

Title: Thinking Configuration Data Flow
```mermaid
flowchart TD
    Start["ApplyThinking()"] --> Parse["ParseSuffix()"]
    Parse --> Lookup["registry.LookupModelInfo()"]
    Lookup --> Val["ValidateConfig()"]
    
    subgraph "Validation Logic (internal/thinking/validate.go)"
        Val --> Conv["Auto-Convert Mode<br/>(Budget <-> Level)"]
        Conv --> Clamp["clampBudget() / clampLevel()"]
        Clamp --> AutoMid["convertAutoToMidRange()"]
    end
    
    AutoMid --> App["ProviderApplier.Apply()"]

    style Val fill:none
    style Conv fill:none
    style Clamp fill:none
```

### Key Normalization Behaviors:
1.  **Auto-Conversion**: If a `ModeLevel` request is sent to a `CapabilityBudgetOnly` model, the level is converted to a budget using internal threshold mappings [internal/thinking/validate.go:72-85]().
2.  **Clamping**: If `fromSuffix` is true, strict budget validation is disabled, and values are clamped to the model's `Min`/`Max` instead of returning an error [internal/thinking/validate.go:63-67]().
3.  **Dynamic Fallback**: If `ModeAuto` is requested but `DynamicAllowed` is false, the system converts the request to a mid-range budget or `medium` level via `convertAutoToMidRange` [internal/thinking/validate.go:142-144]().

Sources: [internal/thinking/validate.go:38-165](), [internal/thinking/apply.go:168-180]()

## Provider-Specific Application

Once validated, the configuration is passed to a `ProviderApplier`. Each provider implements its own logic for JSON pathing.

| Provider | File Path | Target JSON Path |
|----------|-----------|------------------|
| **Gemini** | [internal/thinking/provider/gemini/apply.go]() | `generationConfig.thinkingConfig` |
| **Gemini CLI** | [internal/thinking/provider/geminicli/apply.go]() | `request.generationConfig.thinkingConfig` |
| **Claude** | [internal/thinking/provider/claude/apply.go]() | `thinking.type`, `thinking.budget_tokens` |
| **OpenAI** | [internal/thinking/provider/openai/apply.go]() | `reasoning_effort` |
| **Antigravity**| [internal/thinking/provider/antigravity/apply.go]()| `request.generationConfig.thinkingConfig` |

### Claude Normalization
The Claude applier includes a specific `normalizeClaudeBudget` function [internal/thinking/provider/claude/apply.go:169-195](). This ensures that `max_tokens` is always greater than `budget_tokens`, a strict requirement of the Anthropic API. If the budget exceeds `max_tokens`, the applier reduces the budget to `max_tokens - 1` [internal/thinking/provider/claude/apply.go:185-190]().

### Gemini Format Switching
Gemini appliers dynamically switch between `thinkingBudget` and `thinkingLevel` based on the model's advertised capabilities in `ModelInfo.Thinking.Levels` [internal/thinking/provider/gemini/apply.go:81-92]().

Sources: [internal/thinking/apply.go:88-106](), [internal/thinking/provider/claude/apply.go:72-165](), [internal/thinking/provider/gemini/apply.go:61-93]()

## Stripping Configuration
If a model does not support thinking (e.g., GPT-4o-mini), the system calls `StripThinkingConfig`. This function removes all thinking-related JSON keys to prevent upstream API errors from providers that reject unknown parameters [internal/thinking/apply.go:120-128]().

Sources: [internal/thinking/apply.go:120-134]()

## User-Defined Models
Models defined in the user's `config.yaml` (marked as `UserDefined=true`) bypass strict validation [internal/thinking/apply.go:44-49](). The system still attempts to apply the thinking configuration based on the requested format, but it lets the upstream provider perform the final validation [internal/thinking/apply.go:117-119]().

Sources: [internal/thinking/apply.go:35-49](), [internal/thinking/provider/openai/apply.go:42-44](), [internal/thinking/provider/claude/apply.go:73-75]()

---

# Page: Request and Response Logging

# Request and Response Logging

<details>
<summary>Relevant source files</summary>

The following files were used as context for generating this wiki page:

- [internal/api/handlers/management/logs.go](internal/api/handlers/management/logs.go)
- [internal/api/middleware/request_logging.go](internal/api/middleware/request_logging.go)
- [internal/api/middleware/response_writer.go](internal/api/middleware/response_writer.go)
- [internal/logging/gin_logger.go](internal/logging/gin_logger.go)
- [internal/logging/gin_logger_test.go](internal/logging/gin_logger_test.go)
- [internal/logging/global_logger.go](internal/logging/global_logger.go)
- [internal/logging/request_logger.go](internal/logging/request_logger.go)
- [internal/runtime/executor/logging_helpers.go](internal/runtime/executor/logging_helpers.go)
- [internal/thinking/apply.go](internal/thinking/apply.go)
- [internal/thinking/types.go](internal/thinking/types.go)
- [internal/thinking/validate.go](internal/thinking/validate.go)
- [sdk/translator/registry.go](sdk/translator/registry.go)
- [sdk/translator/registry_test.go](sdk/translator/registry_test.go)
- [test/thinking_conversion_test.go](test/thinking_conversion_test.go)

</details>



## Purpose and Scope

This document describes the logging system in CLIProxyAPI, covering application logs, detailed request/response interception, and structured output. The system provides multiple log types with configurable destinations, rotation policies, and structured output. Application logs capture service-level events (startup, configuration, errors), while the request logging system provides full-body capture for debugging and auditing, supporting both standard and streaming (Server-Sent Events) responses.

---

## Logging Architecture

The logging system consists of three primary layers: application events, raw HTTP interception, and provider-specific execution logs.

| Component | Role | Data Captured | Implementation |
|-----------|------|---------------|----------------|
| **Application Logs** | Service events | Startup, errors, debug info | `logrus` + `lumberjack` |
| **Request Logger** | HTTP Interception | Full headers, Request/Response bodies | `logging.FileRequestLogger` |
| **Upstream Logs** | Provider tracking | Retries, raw upstream payloads | `executor.logging_helpers.go` |

### Data Flow and Code Entity Mapping

The following diagram illustrates how an incoming request flows through the logging components and which code entities handle each stage.

**Diagram: Request Logging Pipeline**

```mermaid
graph TB
    subgraph "HTTP Middleware Layer"
        GIN["gin.Context"]
        RLM["middleware.RequestLoggingMiddleware"]
        RWW["middleware.ResponseWriterWrapper"]
    end
    
    subgraph "Logging Implementation"
        FRL["logging.FileRequestLogger"]
        SLW["logging.StreamingLogWriter"]
    end
    
    subgraph "Upstream Interaction"
        EXE["executor.ProviderExecutor"]
        LH["executor/logging_helpers.go"]
    end

    GIN --> RLM
    RLM --> RWW
    RWW -->|"LogRequest()"| FRL
    RWW -->|"LogStreamingRequest()"| FRL
    FRL --> SLW
    
    EXE -->|"recordAPIRequest()"| LH
    LH -->|"ginCtx.Set(apiAttemptsKey)"| GIN
    RWW -->|"Finalize()"| FRL
    FRL -->|"Write to File"| Disk["logs/requests/*.log"]
```

Sources: [internal/api/middleware/request_logging.go:24-68](), [internal/api/middleware/response_writer.go:31-44](), [internal/logging/request_logger.go:129-138](), [internal/runtime/executor/logging_helpers.go:53-97]()

---

## Application Logs

Application logs use `logrus` for structured output with a custom `LogFormatter` [internal/logging/global_logger.go:30-81](). They include timestamps, log levels, source file/line info, and a unique `request_id` generated for AI API paths.

### Request ID Tracking
The system identifies AI-related paths (e.g., `/v1/chat/completions`, `/v1/messages`) via `aiAPIPrefixes` [internal/logging/gin_logger.go:20-27]() and assigns a unique ID via `logging.GenerateRequestID()` [internal/logging/gin_logger.go:48-53](). This ID is injected into the `gin.Context` and the underlying `context.Context` [internal/logging/gin_logger.go:50-52]().

### Middleware Integration
The `GinLogrusLogger` middleware calculates request latency and logs the status code, client IP, and method [internal/logging/gin_logger.go:40-95](). If a panic occurs, `GinLogrusRecovery` captures the stack trace and logs it via `debug.Stack()` before returning a `500 Internal Server Error` [internal/logging/gin_logger.go:114-129]().

### Log Rotation
Application logs are managed by `lumberjack.Logger` for rotation [internal/logging/global_logger.go:165-171]().
- **MaxSize**: 10 MB per file [internal/logging/global_logger.go:167]().
- **Retention**: Controlled by `LogsMaxTotalSizeMB` in the configuration, which triggers a background cleaner [internal/logging/global_logger.go:148-182]().

Sources: [internal/logging/global_logger.go:30-81](), [internal/logging/gin_logger.go:19-27](), [internal/logging/gin_logger.go:40-95](), [internal/logging/gin_logger.go:114-129]()

---

## Detailed Request and Response Logging

Detailed logging captures the complete payload exchanged between the client and the proxy, as well as between the proxy and upstream providers.

### The Response Writer Wrapper
To capture response bodies without increasing latency, the system uses a `ResponseWriterWrapper` [internal/api/middleware/response_writer.go:31-44](). 

1. **Zero-Latency Writing**: Data is written to the client first via `ResponseWriter.Write(data)` [internal/api/middleware/response_writer.go:77]().
2. **Asynchronous Streaming**: For streaming responses (detected via `Content-Type`), chunks are sent to a buffered `chunkChannel` [internal/api/middleware/response_writer.go:86-89]().
3. **Background Processing**: A goroutine `processStreamingChunks` handles the actual file I/O asynchronously [internal/api/middleware/response_writer.go:175]().

### Upstream Attempt Tracking
The `executor` package tracks individual attempts made to upstream providers, capturing the exact payload sent after translation.
- `recordAPIRequest`: Stores metadata like `Upstream URL`, `HTTP Method`, and `Auth` info in the `gin.Context` [internal/runtime/executor/logging_helpers.go:53-97]().
- `recordAPIResponseMetadata`: Captures upstream status codes and headers for the current attempt [internal/runtime/executor/logging_helpers.go:99-123]().
- `appendAPIResponseChunk`: Aggregates raw chunks from the provider response for the final log file [internal/runtime/executor/logging_helpers.go:151-183]().

Sources: [internal/api/middleware/response_writer.go:71-98](), [internal/api/middleware/response_writer.go:149-180](), [internal/runtime/executor/logging_helpers.go:21-25](), [internal/runtime/executor/logging_helpers.go:53-97]()

---

## Management and Retrieval

The Management API provides endpoints to interact with logs and clean up stored files.

### Log Accumulation and Filtering
The `GetLogs` handler allows incremental log loading [internal/api/handlers/management/logs.go:26-85]().
- **Filtering**: Supports an `after` query parameter to fetch lines after a specific timestamp [internal/api/handlers/management/logs.go:67]().
- **Limiting**: Supports a `limit` parameter to prevent excessive memory usage during retrieval [internal/api/handlers/management/logs.go:61]().

### Log Deletion
The `DeleteLogs` endpoint removes all rotated log files and truncates the active `main.log` file [internal/api/handlers/management/logs.go:88-146](). It uses `os.Truncate` to clear the current log without losing the file handle [internal/api/handlers/management/logs.go:126]().

**Diagram: Log Management Interface**

```mermaid
graph LR
    subgraph "Management API"
        GL["GetLogs()"]
        DL["DeleteLogs()"]
        GRL["GetRequestLogByID()"]
    end
    
    subgraph "File System"
        MAIN["main.log"]
        ROT["main.log.1, main.log.2..."]
        REQ["requests/*.log"]
    end

    GL -->|"Read"| MAIN
    GL -->|"Read"| ROT
    DL -->|"Truncate"| MAIN
    DL -->|"Delete"| ROT
    GRL -->|"Download"| REQ
```

Sources: [internal/api/handlers/management/logs.go:26-85](), [internal/api/handlers/management/logs.go:88-146](), [internal/api/handlers/management/logs.go:214-250]()

---

## Sensitive Data Masking

To protect user privacy and security, the logging system masks sensitive information:
- **Query Parameters**: `util.MaskSensitiveQuery` is used in both application logs [internal/logging/gin_logger.go:44]() and request capture [internal/api/middleware/request_logging.go:113]().
- **Authentication**: Upstream auth details (API keys, tokens) are formatted via `formatAuthInfo` which provides a redacted representation [internal/runtime/executor/logging_helpers.go:76-78]().
- **Management Endpoints**: Requests to `/v0/management` are explicitly excluded from full-body logging to avoid leaking configuration secrets [internal/api/middleware/request_logging.go:156-158]().

Sources: [internal/logging/gin_logger.go:44](), [internal/api/middleware/request_logging.go:113](), [internal/api/middleware/request_logging.go:156-158](), [internal/runtime/executor/logging_helpers.go:76-78]()

---

# Page: Usage Statistics and Monitoring

# Usage Statistics and Monitoring

<details>
<summary>Relevant source files</summary>

The following files were used as context for generating this wiki page:

- [internal/api/handlers/management/handler.go](internal/api/handlers/management/handler.go)
- [internal/api/handlers/management/usage.go](internal/api/handlers/management/usage.go)
- [internal/auth/kimi/kimi.go](internal/auth/kimi/kimi.go)
- [internal/cmd/auth_manager.go](internal/cmd/auth_manager.go)
- [internal/cmd/kimi_login.go](internal/cmd/kimi_login.go)
- [internal/runtime/executor/kimi_executor.go](internal/runtime/executor/kimi_executor.go)
- [internal/runtime/executor/kimi_executor_test.go](internal/runtime/executor/kimi_executor_test.go)
- [internal/runtime/executor/thinking_providers.go](internal/runtime/executor/thinking_providers.go)
- [internal/runtime/executor/usage_helpers.go](internal/runtime/executor/usage_helpers.go)
- [internal/runtime/executor/usage_helpers_test.go](internal/runtime/executor/usage_helpers_test.go)
- [internal/usage/logger_plugin.go](internal/usage/logger_plugin.go)
- [internal/usage/logger_plugin_test.go](internal/usage/logger_plugin_test.go)
- [sdk/api/management.go](sdk/api/management.go)
- [sdk/auth/kimi.go](sdk/auth/kimi.go)
- [sdk/auth/refresh_registry.go](sdk/auth/refresh_registry.go)
- [sdk/cliproxy/usage/manager.go](sdk/cliproxy/usage/manager.go)

</details>



This document describes the usage statistics and monitoring features in the CLI Proxy API system, including usage tracking, token consumption monitoring, and provider health observation.

## Overview

The CLI Proxy API provides a multi-layered observability architecture designed to track AI model consumption and system health:

1.  **Usage Statistics**: Real-time aggregation of token consumption (input, output, reasoning, cached), latency, and success rates, partitioned by API key, provider, and model.
2.  **Request/Response Logging**: Detailed capture of HTTP transactions for debugging and auditing, including support for multi-attempt tracking during provider failover.
3.  **Provider Health Monitoring**: Tracking of provider-specific authentication status, token expiry, and error rates.

---

## Usage Statistics System

### Architecture

The usage system follows a decoupled architecture where the execution layer emits records to a central manager, which then dispatches them to registered plugins.

#### Code Entity Map: Usage Flow
The following diagram maps high-level usage concepts to specific code entities and data structures within the system.

```mermaid
graph TB
    subgraph "Execution Layer [internal/runtime/executor]"
        Reporter["usageReporter struct [usage_helpers.go]"]
        Parser["parseOpenAIUsage() / parseCodexUsage()"]
    end
    
    subgraph "SDK Dispatcher [sdk/cliproxy/usage]"
        Manager["Manager struct [manager.go]"]
        Record["Record struct [manager.go]"]
        Plugin["Plugin interface [manager.go]"]
    end
    
    subgraph "Aggregation Plugin [internal/usage]"
        LoggerPlugin["LoggerPlugin [logger_plugin.go]"]
        Stats["RequestStatistics [logger_plugin.go]"]
        Snapshot["StatisticsSnapshot [logger_plugin.go]"]
    end

    Reporter -- "PublishRecord()" --> Manager
    Parser -- "returns Detail" --> Reporter
    Manager -- "HandleUsage()" --> Plugin
    Plugin -- "updates" --> Stats
    Stats -- "Snapshot()" --> Snapshot
```
**Sources**: [internal/runtime/executor/usage_helpers.go:18-27](), [sdk/cliproxy/usage/manager.go:11-23](), [internal/usage/logger_plugin.go:27-29]()

### Usage Reporter Implementation

The `usageReporter` is initialized at the start of every provider request to capture metadata even if the request fails.

*   **Initialization**: Created via `newUsageReporter` which captures the `requestedAt` timestamp and resolves the `source` (e.g., email, project ID, or API key) [internal/runtime/executor/usage_helpers.go:29-43]().
*   **Source Resolution**: The `resolveUsageSource` function extracts identifying information from the `Auth` object, such as `project_id` for Vertex AI or the account email for OAuth-based providers [internal/runtime/executor/usage_helpers.go:143-185]().
*   **Token Parsing**: Provider-specific functions like `parseOpenAIUsage` and `parseCodexUsage` extract granular token counts including `ReasoningTokens` and `CachedTokens` from JSON responses [internal/runtime/executor/usage_helpers.go:187-239]().
*   **Guaranteed Delivery**: The `ensurePublished` method uses `sync.Once` to guarantee that a record is emitted exactly once per request, preventing double-counting while ensuring visibility for streaming requests that might not return token counts [internal/runtime/executor/usage_helpers.go:84-91]().
*   **Failure Tracking**: The `trackFailure` helper is typically used in `defer` blocks within executors (e.g., `KimiExecutor`) to ensure failed requests are logged with `Failed: true` [internal/runtime/executor/usage_helpers.go:53-60](), [internal/runtime/executor/kimi_executor.go:80-80]().

### In-Memory Statistics Aggregation

The `LoggerPlugin` implements the `usage.Plugin` interface to maintain high-performance, in-memory aggregates [internal/usage/logger_plugin.go:27-51]().

| Entity | Description | Code Reference |
| :--- | :--- | :--- |
| `RequestStatistics` | The primary store for global and per-API metrics. | [internal/usage/logger_plugin.go:60-74]() |
| `apiStats` | Aggregated metrics for a specific API key or source. | [internal/usage/logger_plugin.go:77-81]() |
| `RequestDetail` | Individual request metadata including latency and token breakdown. | [internal/usage/logger_plugin.go:91-98]() |
| `TokenStats` | Breakdown of input, output, reasoning, and cached tokens. | [internal/usage/logger_plugin.go:101-107]() |

**Sources**: [internal/usage/logger_plugin.go:60-107]()

---

## Management API Integration

The `management.Handler` provides endpoints to interact with the runtime statistics and monitor system health.

*   **Statistics Retrieval**: `GetUsageStatistics` returns a snapshot of the current in-memory metrics, including success and failure counts [internal/api/handlers/management/usage.go:24-33]().
*   **Persistence**: `ExportUsageStatistics` and `ImportUsageStatistics` allow for the migration or backup of statistics by serializing the `StatisticsSnapshot` [internal/api/handlers/management/usage.go:36-79]().
*   **Deduplication**: The `MergeSnapshot` function ensures that imported records are not duplicated by checking timestamps and sources [internal/usage/logger_plugin_test.go:35-96]().
*   **Security**: Management endpoints are protected by `Middleware` which enforces access control via `MANAGEMENT_PASSWORD` and implements IP-based banning after 5 failed attempts [internal/api/handlers/management/handler.go:140-204]().

---

## Provider Health and Authentication Monitoring

The system monitors the health of provider credentials through the `Auth` and `Manager` entities.

#### Code Entity Map: Auth Monitoring
This diagram illustrates how authentication status and token lifecycles are monitored.

```mermaid
graph LR
    subgraph "Auth Management [sdk/cliproxy/auth]"
        AM["Manager struct"]
        Store["Store interface"]
        Refresh["RefreshLeadProvider"]
    end

    subgraph "Provider Logic [internal/auth]"
        KimiAuth["KimiAuth [kimi.go]"]
        DeviceFlow["DeviceFlowClient [kimi.go]"]
    end

    AM -- "GetAuthStatus()" --> Store
    Refresh -- "triggers" --> KimiAuth
    KimiAuth -- "polls" --> DeviceFlow
```
**Sources**: [internal/api/handlers/management/handler.go:43-45](), [sdk/auth/refresh_registry.go:9-18](), [internal/auth/kimi/kimi.go:42-54]()

### Token Lifecycle Monitoring
*   **Refresh Thresholds**: Providers like Kimi define a `refreshThresholdSeconds` (e.g., 300 seconds) to ensure tokens are rotated before expiry [internal/auth/kimi/kimi.go:39-39]().
*   **Refresh Registry**: The `refresh_registry.go` file maps providers to their respective `RefreshLead` durations, allowing the core manager to proactively refresh credentials [sdk/auth/refresh_registry.go:1-31]().
*   **Auth Status**: The `GetAuthStatus` management endpoint allows clients to query the current state of all registered credentials, including expiry times and metadata [sdk/api/management.go:71-73]().

---

## Request and Response Logging

The system includes a file-based logging mechanism for detailed auditing, often configured via the `Handler`.

*   **Log Directory**: The management handler can be configured with a specific log directory to expose system logs via API [internal/api/handlers/management/handler.go:120-130]().
*   **Upstream Capture**: Executors record detailed metadata about upstream requests and responses using helpers like `recordAPIRequest` and `recordAPIResponseMetadata` [internal/runtime/executor/kimi_executor.go:122-132]().
*   **Error Summarization**: When upstream requests fail, the system captures and logs the error status and a summarized body for troubleshooting [internal/runtime/executor/kimi_executor.go:146-152]().

---

## Configuration Reference

Usage and monitoring features are initialized and managed through the `config.Config` and internal state:

| Key / Variable | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `statisticsEnabled` | atomic.Bool | `true` | Global toggle for in-memory aggregation. [internal/usage/logger_plugin.go:18-21]() |
| `MANAGEMENT_PASSWORD` | env string | `""` | Secret key required to access usage and health endpoints. [internal/api/handlers/management/handler.go:55-56]() |
| `attemptMaxIdleTime` | duration | `2h` | Duration before a monitored IP's failure history is purged. [internal/api/handlers/management/handler.go:34-34]() |

**Sources**: [internal/usage/logger_plugin.go:18-21](), [internal/api/handlers/management/handler.go:31-34]()

---

# Page: Streaming and Keep-Alive

# Streaming and Keep-Alive

<details>
<summary>Relevant source files</summary>

The following files were used as context for generating this wiki page:

- [internal/config/sdk_config.go](internal/config/sdk_config.go)
- [internal/runtime/executor/aistudio_executor.go](internal/runtime/executor/aistudio_executor.go)
- [internal/runtime/executor/antigravity_executor.go](internal/runtime/executor/antigravity_executor.go)
- [internal/runtime/executor/claude_executor.go](internal/runtime/executor/claude_executor.go)
- [internal/runtime/executor/codex_executor.go](internal/runtime/executor/codex_executor.go)
- [internal/runtime/executor/gemini_cli_executor.go](internal/runtime/executor/gemini_cli_executor.go)
- [internal/runtime/executor/gemini_executor.go](internal/runtime/executor/gemini_executor.go)
- [internal/runtime/executor/gemini_vertex_executor.go](internal/runtime/executor/gemini_vertex_executor.go)
- [internal/runtime/executor/iflow_executor.go](internal/runtime/executor/iflow_executor.go)
- [internal/runtime/executor/openai_compat_executor.go](internal/runtime/executor/openai_compat_executor.go)
- [internal/runtime/executor/qwen_executor.go](internal/runtime/executor/qwen_executor.go)
- [sdk/api/handlers/handlers_stream_bootstrap_test.go](sdk/api/handlers/handlers_stream_bootstrap_test.go)
- [sdk/api/handlers/header_filter.go](sdk/api/handlers/header_filter.go)
- [sdk/api/handlers/header_filter_test.go](sdk/api/handlers/header_filter_test.go)
- [sdk/api/handlers/openai/openai_responses_handlers_stream_error_test.go](sdk/api/handlers/openai/openai_responses_handlers_stream_error_test.go)
- [sdk/api/handlers/openai/openai_responses_websocket.go](sdk/api/handlers/openai/openai_responses_websocket.go)
- [sdk/api/handlers/openai/openai_responses_websocket_test.go](sdk/api/handlers/openai/openai_responses_websocket_test.go)
- [sdk/api/handlers/openai_responses_stream_error.go](sdk/api/handlers/openai_responses_stream_error.go)
- [sdk/api/handlers/openai_responses_stream_error_test.go](sdk/api/handlers/openai_responses_stream_error_test.go)
- [sdk/cliproxy/auth/conductor_executor_replace_test.go](sdk/cliproxy/auth/conductor_executor_replace_test.go)

</details>



This page covers the mechanisms CLIProxyAPI uses to maintain live connections and prevent premature timeouts during both streaming (SSE) and non-streaming AI API requests. It also documents the server-level process keep-alive endpoint used in embedded deployments.

For general HTTP request pipeline behavior, see [3.2](). For WebSocket-specific transport (Codex Responses API), see [8.7]().

---

## Overview

CLIProxyAPI manages three distinct keep-alive concerns:

| Concern | Trigger | Config key |
|---|---|---|
| SSE streaming heartbeats | Long-running streaming responses | `streaming.keepalive-seconds` |
| Streaming bootstrap retries | Transient upstream error before first byte | `streaming.bootstrap-retries` |
| Non-streaming blank-line keep-alives | Long-running non-streaming responses | `nonstream-keepalive-interval` |
| Process keep-alive endpoint | Embedded/TUI deployments | `WithKeepAliveEndpoint` server option |

**Configuration locations:**

- `streaming.keepalive-seconds` and `streaming.bootstrap-retries` map to `StreamingConfig` in [internal/config/sdk_config.go:36-45]().
- `nonstream-keepalive-interval` maps to `NonStreamKeepAliveInterval` in [internal/config/sdk_config.go:32-33]().

Sources: [internal/config/sdk_config.go:8-45](), [sdk/api/handlers/handlers.go:144-180]()

---

## SSE Streaming Keep-Alives

When a client requests a streaming response, the upstream AI provider may take many seconds to emit the first token. Reverse proxies and load balancers may close idle connections in this window. CLIProxyAPI can emit periodic SSE comment lines to keep the connection alive.

### How it works

`StreamingKeepAliveInterval` in [sdk/api/handlers/handlers.go:144-155]() reads `cfg.Streaming.KeepAliveSeconds` and returns it as a `time.Duration`. A return value of `0` disables keep-alives.

The `KeepAliveSeconds` field is defined in `StreamingConfig` ([internal/config/sdk_config.go:36-45]()). Protocol handlers use this interval to start a ticker that emits SSE comment lines (`: keep-alive\n\n`) while waiting for upstream chunks.

**Title: SSE Streaming Keep-Alive Data Flow**

```mermaid
sequenceDiagram
    participant C as "Client"
    participant H as "StreamHandler"
    participant T as "KeepAliveTicker"
    participant U as "UpstreamAI"

    C->>H: "POST /v1/chat/completions (stream=true)"
    H->>U: "ExecuteStream()"
    H->>T: "start ticker (KeepAliveSeconds)"
    loop "while waiting for first chunk"
        T-->>C: ": keep-alive\n\n"
    end
    U-->>H: "StreamChunk{Payload}"
    H->>T: "stop ticker"
    H-->>C: "data: {...}\n\n"
    U-->>H: "[DONE]"
    H-->>C: "data: [DONE]\n\n"
```

Sources: [sdk/api/handlers/handlers.go:144-155](), [internal/config/sdk_config.go:36-45]()

---

## Streaming Bootstrap Retry Logic

Some upstream auth failures manifest only after opening a streaming connection — the upstream sends an error chunk instead of data. When `streaming.bootstrap-retries` is greater than 0, CLIProxyAPI is allowed to retry the entire streaming request with a different credential, **as long as no payload bytes have been forwarded to the client yet**.

Once a single non-error chunk is written to the client, retry is no longer safe as it would produce corrupted output.

### Configuration

`StreamingBootstrapRetries` in [sdk/api/handlers/handlers.go:170-180]() reads `cfg.Streaming.BootstrapRetries`:

```go
func StreamingBootstrapRetries(cfg *config.SDKConfig) int {
	retries := defaultStreamingBootstrapRetries // 0
	if cfg != nil {
		retries = cfg.Streaming.BootstrapRetries
	}
	if retries < 0 {
		retries = 0
	}
	return retries
}
```

### Bootstrap Retry Boundary Rule

| Scenario | Retry allowed? |
|---|---|
| First chunk is an error (`StreamChunk.Err` set, no payload written) | Yes, up to `BootstrapRetries` times |
| First chunk has payload data, subsequent chunk is an error | **No** — client already received bytes |
| Error occurs on very first request (before `ExecuteStream` returns) | Yes |

This behavior is validated in [sdk/api/handlers/handlers_stream_bootstrap_test.go](). For example, `failOnceStreamExecutor` [sdk/api/handlers/handlers_stream_bootstrap_test.go:15-55]() returns an error on the first call and success on the second, allowing the handler to retry if `BootstrapRetries >= 1`. Conversely, `payloadThenErrorStreamExecutor` [sdk/api/handlers/handlers_stream_bootstrap_test.go:79-107]() sends a payload chunk before an error, which prevents retries.

**Title: Bootstrap Retry Decision Logic**

```mermaid
flowchart TD
    Start["ExecuteStreamWithAuthManager()"]
    Call["Call AuthManager.ExecuteStream()"]
    ReadChunk["Read next StreamChunk"]
    HasPayload{"Chunk has Payload?"}
    HasErr{"Chunk has Err?"}
    BytesWritten{"Any bytes\nalready sent?"}
    BootstrapLeft{"bootstrap retries\nremaining?"}
    Write["Write chunk to client\n(mark bytes_sent=true)"]
    Retry["Retry with next credential"]
    ErrorOut["Return error to client"]
    Done["Stream complete"]

    Start --> Call
    Call --> ReadChunk
    ReadChunk --> HasPayload
    HasPayload -- Yes --> Write
    Write --> ReadChunk
    HasPayload -- No --> HasErr
    HasErr -- No --> Done
    HasErr -- Yes --> BytesWritten
    BytesWritten -- Yes --> ErrorOut
    BytesWritten -- No --> BootstrapLeft
    BootstrapLeft -- Yes --> Retry
    BootstrapLeft -- No --> ErrorOut
    Retry --> Call
```

Sources: [sdk/api/handlers/handlers.go:170-180](), [sdk/api/handlers/handlers_stream_bootstrap_test.go:15-107](), [internal/config/sdk_config.go:41-45]()

---

## Non-Streaming Keep-Alive

Non-streaming requests wait for the entire upstream response before writing to the client. For complex reasoning requests this can take tens of seconds, causing proxy timeouts. When `nonstream-keepalive-interval` is set, CLIProxyAPI emits blank newlines periodically while waiting.

### Implementation: `StartNonStreamingKeepAlive`

The logic is controlled by `NonStreamingKeepAliveInterval` [sdk/api/handlers/handlers.go:157-168](), which reads the configuration value.

The handler starts a background goroutine with a `time.Ticker` that writes `"\n"` and calls `Flush()` on each tick. A stop function is returned to the caller, which must be invoked before the final JSON response is written to ensure the keep-alive goroutine has exited and no concurrent writes occur.

**Title: Non-Streaming Keep-Alive Ticker Lifecycle**

```mermaid
sequenceDiagram
    participant Handler as "RequestHandler"
    participant KA as "keepAlive goroutine"
    participant W as "gin.ResponseWriter"

    Handler->>KA: "StartNonStreamingKeepAlive() → stopFn"
    Note over KA: "ticker = time.NewTicker(interval)"
    loop "every interval"
        KA->>W: "Write(\"\\n\") + Flush()"
    end
    Handler->>KA: "stopFn() → close(stopChan)"
    KA-->>Handler: "wg.Done() (goroutine exits)"
    Handler->>W: "c.JSON(200, response)"
```

Sources: [sdk/api/handlers/handlers.go:157-168](), [internal/config/sdk_config.go:30-33]()

---

## Provider-Specific Streaming Implementation

Different executors handle streaming chunk parsing according to provider protocols:

| Executor | Protocol | Implementation |
|---|---|---|
| `AntigravityExecutor` | HTTP/1.1 SSE | [internal/runtime/executor/antigravity_executor.go:113-128]() |
| `ClaudeExecutor` | Anthropic Messages SSE | [internal/runtime/executor/claude_executor.go:163-185]() |
| `CodexExecutor` | OpenAI Responses SSE | [internal/runtime/executor/codex_executor.go:170-189]() |
| `GeminiExecutor` | Google GL SSE | [internal/runtime/executor/gemini_executor.go:144-161]() |
| `AIStudioExecutor` | WebSocket Relay | [internal/runtime/executor/aistudio_executor.go:172-209]() |

**Title: Executor Streaming Translation Map**

```mermaid
graph TD
    subgraph "Executor Layer"
        AG["AntigravityExecutor"]
        CL["ClaudeExecutor"]
        CX["CodexExecutor"]
        GE["GeminiExecutor"]
        AS["AIStudioExecutor"]
    end

    subgraph "Stream Processing"
        SSE["SSE Scanner (bufio.Scanner)"]
        WSR["WebSocket Relay (wsrelay.Manager)"]
    end

    AG --> SSE
    CL --> SSE
    CX --> SSE
    GE --> SSE
    AS --> WSR

    SSE -->|TranslateChunk| Client["Gin ResponseWriter"]
    WSR -->|TranslateChunk| Client
```

Sources: [internal/runtime/executor/antigravity_executor.go:7-23](), [internal/runtime/executor/claude_executor.go:4-18](), [internal/runtime/executor/codex_executor.go:4-11](), [internal/runtime/executor/gemini_executor.go:7-13](), [internal/runtime/executor/aistudio_executor.go:6-14]()

---

## Configuration Reference

| `config.yaml` key | Go field | Default | Effect |
|---|---|---|---|
| `streaming.keepalive-seconds` | `SDKConfig.Streaming.KeepAliveSeconds` | `0` (disabled) | SSE comment lines emitted every N seconds during streaming |
| `streaming.bootstrap-retries` | `SDKConfig.Streaming.BootstrapRetries` | `0` (disabled) | Max retries before first byte for transient upstream errors |
| `nonstream-keepalive-interval` | `SDKConfig.NonStreamKeepAliveInterval` | `0` (disabled) | Blank newlines emitted every N seconds during non-streaming waits |

Sources: [internal/config/sdk_config.go:8-45](), [sdk/api/handlers/handlers.go:144-180]()

---

# Page: WebSocket Gateway and Runtime Auth

# WebSocket Gateway and Runtime Auth

<details>
<summary>Relevant source files</summary>

The following files were used as context for generating this wiki page:

- [internal/config/sdk_config.go](internal/config/sdk_config.go)
- [internal/wsrelay/http.go](internal/wsrelay/http.go)
- [internal/wsrelay/manager.go](internal/wsrelay/manager.go)
- [internal/wsrelay/message.go](internal/wsrelay/message.go)
- [internal/wsrelay/session.go](internal/wsrelay/session.go)
- [sdk/api/handlers/handlers_stream_bootstrap_test.go](sdk/api/handlers/handlers_stream_bootstrap_test.go)
- [sdk/api/handlers/header_filter.go](sdk/api/handlers/header_filter.go)
- [sdk/api/handlers/header_filter_test.go](sdk/api/handlers/header_filter_test.go)
- [sdk/api/handlers/openai/openai_responses_websocket.go](sdk/api/handlers/openai/openai_responses_websocket.go)
- [sdk/api/handlers/openai/openai_responses_websocket_test.go](sdk/api/handlers/openai/openai_responses_websocket_test.go)
- [sdk/cliproxy/auth/conductor_executor_replace_test.go](sdk/cliproxy/auth/conductor_executor_replace_test.go)

</details>



## Purpose and Scope

This document covers the WebSocket gateway system for AI Studio providers and the runtime authentication mechanism that supports dynamically registered credentials. The WebSocket gateway enables bidirectional communication with WebSocket-based AI providers, while runtime authentication allows credentials to be registered on-demand without persistence to disk. It also covers the specialized WebSocket implementation for the OpenAI-compatible Responses API.

For OAuth authentication flows and credential lifecycle management, see [7. Authentication Flows](). For general authentication and credential management concepts, see [3.3. Authentication and Credential Management]().

---

## Overview

The WebSocket gateway serves three primary purposes:

1.  **WebSocket Provider Support**: Enables integration with AI Studio providers that communicate over WebSocket connections rather than HTTP REST APIs.
2.  **Runtime-Only Credentials**: Supports ephemeral authentication entries that exist only while a WebSocket connection is active, avoiding filesystem persistence.
3.  **Stateful Upstream Communication**: Supports the `/v1/responses` WebSocket protocol, allowing for incremental input and session pinning [sdk/api/handlers/openai/openai_responses_websocket.go:49-52]().

**Sources**: [sdk/api/handlers/openai/openai_responses_websocket.go:49-52](), [internal/wsrelay/manager.go:16-18]()

---

## Architecture Components

### WebSocket Gateway Manager

The `wsrelay.Manager` component handles the WebSocket connection lifecycle and message routing for AI Studio style providers. It maintains a map of active sessions keyed by provider name.

| Component | Type | Purpose |
| :--- | :--- | :--- |
| `Manager` | `struct` | Core WebSocket connection manager and HTTP-to-WS relay [internal/wsrelay/manager.go:18-31]() |
| `session` | `struct` | Represents a single active client connection [internal/wsrelay/session.go:36-45]() |
| `Message` | `struct` | The JSON envelope for all data exchanged over the relay [internal/wsrelay/message.go:4-8]() |

**Sources**: [internal/wsrelay/manager.go:18-31](), [internal/wsrelay/session.go:36-45](), [internal/wsrelay/message.go:4-8]()

### Message Protocol

The relay uses a specific set of message types to simulate HTTP request/response cycles over a persistent socket.

| Message Type | Code Symbol | Description |
| :--- | :--- | :--- |
| `http_request` | `MessageTypeHTTPReq` | Encapsulates method, URL, headers, and body [internal/wsrelay/message.go:12-12]() |
| `http_response` | `MessageTypeHTTPResp` | Carries non-streaming response data [internal/wsrelay/message.go:14-14]() |
| `stream_start` | `MessageTypeStreamStart` | Marks the beginning of a chunked response [internal/wsrelay/message.go:16-16]() |
| `stream_chunk` | `MessageTypeStreamChunk` | Carries a single data payload chunk [internal/wsrelay/message.go:18-18]() |
| `error` | `MessageTypeError` | Reports upstream or relay failures [internal/wsrelay/message.go:22-22]() |

**Sources**: [internal/wsrelay/message.go:10-27](), [internal/wsrelay/http.go:177-191]()

---

## Runtime Authentication System

### Runtime-Only Credential Lifecycle

Runtime authentication entries are created dynamically when WebSocket providers connect. These credentials are ephemeral and are not persisted to the storage backend.

Title: WebSocket Provider Registration Flow
```mermaid
sequenceDiagram
    participant C as WebSocket Client
    participant M as wsrelay.Manager
    participant S as session
    participant H as http.Handler
    
    C->>H: GET /v1/ws (Upgrade)
    H->>M: handleWebsocket()
    M->>M: providerFactory(r)
    M->>S: newSession(conn, provider)
    M->>M: onConnected(provider)
    Note over M, S: Session added to sessions map
    S->>S: run() loop starts
```

**Sources**: [internal/wsrelay/manager.go:114-160](), [internal/wsrelay/session.go:89-98]()

### Session Management and Heartbeats

To ensure connection health, the `session` implementation includes a heartbeat mechanism using WebSocket Ping/Pong frames.

- **Read Timeout**: 60 seconds [internal/wsrelay/session.go:14-14]().
- **Heartbeat Interval**: 30 seconds [internal/wsrelay/session.go:17-17]().
- **Write Deadline**: 10 seconds [internal/wsrelay/session.go:15-15]().

When a `session` is cleaned up (due to error or disconnect), it triggers `handleSessionClosed` in the `Manager`, which removes the provider from the active registry [internal/wsrelay/manager.go:180-193]().

**Sources**: [internal/wsrelay/session.go:13-18](), [internal/wsrelay/session.go:65-87](), [internal/wsrelay/manager.go:180-193]()

---

## Responses WebSocket Implementation

The `ResponsesWebsocket` handler in `OpenAIResponsesAPIHandler` implements a specialized protocol for stateful interactions, allowing clients to send `response.create` and `response.append` events [sdk/api/handlers/openai/openai_responses_websocket.go:49-52]().

### Request Normalization

Because some providers require full context while the WebSocket protocol allows incremental updates, the system performs "normalization" to merge new input with previous session state.

- **`normalizeResponsesWebsocketRequest`**: Merges `payload` with `lastRequest` and `lastResponseOutput` [sdk/api/handlers/openai/openai_responses_websocket.go:125-130]().
- **Stream Forcing**: The gateway forces `stream: true` on normalized requests to ensure compatibility with the gateway's event-driven architecture [sdk/api/handlers/openai/openai_responses_websocket_test.go:139-141]().

### Session Pinning

The gateway supports pinning a session to a specific authentication ID (`pinnedAuthID`). If the upstream provider supports incremental input, the handler pins the `authID` for the duration of the WebSocket session to maintain state consistency [sdk/api/handlers/openai/openai_responses_websocket.go:176-192]().

**Sources**: [sdk/api/handlers/openai/openai_responses_websocket.go:122-130](), [sdk/api/handlers/openai/openai_responses_websocket.go:176-192](), [sdk/api/handlers/openai/openai_responses_websocket_test.go:139-141]()

---

## Technical Data Flow: Request Relaying

The `wsrelay.Manager` provides both `NonStream` and `Stream` methods to interact with connected WebSocket providers as if they were standard HTTP backends.

Title: HTTP-to-WebSocket Relay Logic
```mermaid
graph TD
    subgraph "Code Entity Space"
        NS["Manager.NonStream()"]
        S["Manager.Stream()"]
        Sess["session.request()"]
        Enc["encodeRequest()"]
        Dec["decodeResponse()"]
    end

    NS --> Enc
    S --> Enc
    Enc --> Sess
    Sess -->|"MessageTypeHTTPReq"| WS["WebSocket Wire"]
    WS -->|"MessageTypeStreamChunk"| Sess
    Sess --> Dec
    Dec -->|"HTTPResponse"| NS
```

### Execution Details
1.  **Encoding**: `encodeRequest` transforms a standard `HTTPRequest` into a map containing the method, URL, headers, and body [internal/wsrelay/http.go:177-191]().
2.  **Dispatching**: `session.dispatch` routes incoming messages from the wire back to the original requestor using the message `ID` [internal/wsrelay/session.go:101-122]().
3.  **Header Filtering**: Before relaying, headers are processed via `FilterUpstreamHeaders` to remove hop-by-hop headers like `Connection`, `Keep-Alive`, and `Upgrade` [sdk/api/handlers/header_filter.go:29-49]().

**Sources**: [internal/wsrelay/http.go:39-112](), [internal/wsrelay/session.go:101-122](), [internal/wsrelay/http.go:177-191](), [sdk/api/handlers/header_filter.go:29-49]()

---

## Configuration and Constraints

### Buffer Limits
- **Read/Write Buffer**: 4096 bytes for the Responses upgrader [sdk/api/handlers/openai/openai_responses_websocket.go:41-43]().
- **Max Inbound Message**: 64 MiB for the relay manager [internal/wsrelay/session.go:16-16]().

### Header Handling
The gateway uses `FilterUpstreamHeaders` to ensure security and protocol compliance. It specifically blocks `Set-Cookie`, `Transfer-Encoding`, and `Authorization` from leaking between upstream and downstream unless explicitly configured [sdk/api/handlers/header_filter.go:10-25]().

**Sources**: [sdk/api/handlers/openai/openai_responses_websocket.go:41-43](), [internal/wsrelay/session.go:16-16](), [sdk/api/handlers/header_filter.go:10-25]()

---

# Page: Signature Cache and Multi-Turn Conversations

# Signature Cache and Multi-Turn Conversations

<details>
<summary>Relevant source files</summary>

The following files were used as context for generating this wiki page:

- [internal/cache/signature_cache.go](internal/cache/signature_cache.go)
- [internal/cache/signature_cache_test.go](internal/cache/signature_cache_test.go)
- [internal/translator/antigravity/claude/antigravity_claude_request.go](internal/translator/antigravity/claude/antigravity_claude_request.go)
- [internal/translator/antigravity/claude/antigravity_claude_request_test.go](internal/translator/antigravity/claude/antigravity_claude_request_test.go)
- [internal/translator/antigravity/claude/antigravity_claude_response.go](internal/translator/antigravity/claude/antigravity_claude_response.go)
- [internal/translator/antigravity/claude/antigravity_claude_response_test.go](internal/translator/antigravity/claude/antigravity_claude_response_test.go)

</details>



## Purpose and Scope

This page documents the signature caching system that enables multi-turn conversations with thinking blocks in Claude models. When using Claude's extended thinking capabilities (e.g., `claude-3-7-sonnet` or `claude-3-5-sonnet-20241022` with thinking enabled), the model generates signed thinking blocks that must be preserved and validated across conversation turns. The signature cache automatically manages these signatures to enable seamless multi-turn interactions.

For general thinking configuration (budget, level, hybrid modes), see [Thinking and Reasoning Configuration](8.3). For model capability metadata, see [Model Registry and Capability System](3.6). For request/response format translation, see [Request Translation System](3.5).

---

## Overview: What Are Thinking Signatures?

Thinking signatures are cryptographic tokens returned by models when generating thinking blocks. These signatures serve two purposes:

1.  **Validation**: Signatures prove that thinking content was genuinely generated by the model (not fabricated by the client).
2.  **Multi-turn continuity**: Signatures enable the model to reference previous thinking in subsequent conversation turns.

When a model generates a thinking block, it emits the thinking text first, followed by a signature in a separate event:

```
event: content_block_delta
data: {"type":"content_block_delta","index":0,"delta":{"type":"thinking_delta","thinking":"Let me analyze..."}}

event: content_block_delta
data: {"type":"content_block_delta","index":0,"delta":{"type":"signature_delta","signature":"claude#abc123..."}}
```

In subsequent conversation turns, the client must include this signature when referencing the thinking block. The signature cache automates this by:
*   Storing signatures as they arrive in responses.
*   Retrieving cached signatures when building requests based on the thinking text content.
*   Handling signature validation and expiration.

**Sources:** [internal/cache/signature_cache.go:1-196](), [internal/translator/antigravity/claude/antigravity_claude_response.go:45-46,137-153]()

---

## Signature Cache Architecture

### Data Structure and Storage

The signature cache uses a tiered storage approach to handle multiple model families (Claude, Gemini, GPT) concurrently while maintaining isolation.

```mermaid
graph TB
    subgraph "signatureCache (sync.Map)"
        ModelGroup1["Model Group: 'claude'<br/>(groupCache)"]
        ModelGroup2["Model Group: 'gemini'<br/>(groupCache)"]
        ModelGroup3["Model Group: 'gpt'<br/>(groupCache)"]
    end
    
    subgraph "groupCache"
        RWMutex["sync.RWMutex"]
        EntriesMap["entries map[string]SignatureEntry"]
    end
    
    subgraph "SignatureEntry"
        Signature["Signature: string"]
        Timestamp["Timestamp: time.Time"]
    end
    
    subgraph "Key Generation Logic"
        ThinkingText["Thinking Text"]
        SHA256["SHA256 Hash"]
        TextHash["textHash<br/>(16 hex chars)"]
    end
    
    ModelGroup1 --> EntriesMap
    ModelGroup2 --> EntriesMap
    ModelGroup3 --> EntriesMap
    
    EntriesMap --> SignatureEntry["textHash → SignatureEntry"]
    SignatureEntry --> Signature
    SignatureEntry --> Timestamp
    
    ThinkingText --> SHA256
    SHA256 --> TextHash
    TextHash --> EntriesMap
```

**Diagram: Signature Cache Data Structure**

The cache uses a two-level map structure:
1.  **Outer map**: `sync.Map` keyed by model group (resolved via `GetModelGroup` at [internal/cache/signature_cache.go:186-195]()).
2.  **Inner map**: `groupCache` with `map[string]SignatureEntry` keyed by text hash.

Each `SignatureEntry` contains:
*   `Signature`: The signature string (minimum 50 characters).
*   `Timestamp`: For TTL-based expiration (3-hour sliding window).

Text hashing uses SHA256 truncated to 16 hex characters, providing collision resistance while keeping keys compact. The hash function at [internal/cache/signature_cache.go:44-47]() handles Unicode text safely.

**Sources:** [internal/cache/signature_cache.go:11-15,31-47,49-60]()

---

### Configuration Constants

| Constant | Value | Purpose |
| :--- | :--- | :--- |
| `SignatureCacheTTL` | 3 hours | How long signatures remain valid |
| `SignatureTextHashLen` | 16 hex chars | Length of text hash keys |
| `MinValidSignatureLen` | 50 characters | Minimum length for valid signatures |
| `CacheCleanupInterval` | 10 minutes | Background cleanup frequency |

**Sources:** [internal/cache/signature_cache.go:17-29]()

---

### Cache Lifecycle and Cleanup

The cache implements **sliding expiration**: when a signature is successfully retrieved, its timestamp is refreshed at [internal/cache/signature_cache.go:161-162](), extending its lifetime by another 3 hours.

```mermaid
sequenceDiagram
    participant Client as "ConvertClaudeRequestToAntigravity"
    participant Cache as "signature_cache.go"
    participant Cleanup as "startCacheCleanup"
    
    Note over Client,Cache: Store Signature
    Client->>Cache: CacheSignature(modelName, text, sig)
    Cache->>Cache: GetModelGroup(modelName)
    Cache->>Cache: hashText(text)
    Cache->>Cache: Store SignatureEntry with time.Now()
    
    Note over Client,Cache: Retrieve Signature
    Client->>Cache: GetCachedSignature(modelName, text)
    Cache->>Cache: Check if entry exists
    alt Entry exists and not expired
        Cache->>Cache: Refresh Timestamp (sliding TTL)
        Cache-->>Client: Return signature
    else Entry expired or missing
        Cache->>Cache: Delete expired entry
        Cache-->>Client: Return "" (or Gemini sentinel)
    end
    
    Note over Cleanup: Periodic Cleanup
    Cleanup->>Cleanup: Start on first cache access
    loop Every 10 minutes
        Cleanup->>Cache: purgeExpiredCaches()
        Cache->>Cache: Delete entries older than 3h
        Cache->>Cache: Remove empty groupCache buckets
    end
```

**Diagram: Cache Lifecycle Operations**

The background cleanup goroutine starts lazily on first cache access via `cacheCleanupOnce.Do(startCacheCleanup)` at [internal/cache/signature_cache.go:52]() and runs every 10 minutes to remove stale entries.

**Sources:** [internal/cache/signature_cache.go:62-73,75-94,96-116,118-166]()

---

## Request Translation: Signature Resolution

### Signature Resolution Strategy

When translating a Claude request to Antigravity format, the system resolves thinking signatures using a three-tier strategy implemented in `ConvertClaudeRequestToAntigravity` at [internal/translator/antigravity/claude/antigravity_claude_request.go:107-149]().

```mermaid
graph TB
    Start["Thinking Block in Claude Request"]
    
    CheckCache{"GetCachedSignature()"}
    UseCache["Use Cached Signature<br/>(Most Reliable)"]
    
    CheckClient{"Client provided<br/>valid signature?"}
    ValidateClient["Validate client signature:<br/>1. Format: modelGroup#signature<br/>2. Length ≥ 50 chars<br/>3. Model group matches"]
    UseClient["Use Client Signature"]
    
    CheckModel{"Model Group<br/>is 'gemini'?"}
    DropBlock["Drop Unsigned Block<br/>(Claude requirement)"]
    UseSkip["Use skip_thought_signature_validator"]
    
    Start --> CheckCache
    CheckCache -->|Yes| UseCache
    CheckCache -->|No| CheckClient
    CheckClient -->|Yes| ValidateClient
    ValidateClient --> UseClient
    CheckClient -->|No| CheckModel
    CheckModel -->|Yes| UseSkip
    CheckModel -->|No| DropBlock
```

**Diagram: Signature Resolution Decision Tree**

1.  **Tier 1 - Cached Signature**: Always tried first (lines 107-113). It is more reliable than client-provided signatures which may be stale across sessions.
2.  **Tier 2 - Client-Provided Signature**: Extracted and validated (lines 116-129). It must follow the format `group#signature` and match the current model's group.
3.  **Tier 3 - Fallback**:
    *   If `HasValidSignature` returns true for either tier, the block is sent as a `thought` part with `thoughtSignature` (lines 150-159).
    *   If unsigned, the block is **dropped entirely** for Claude models (lines 144-148) because Claude requires assistant messages to start with valid thinking blocks when thinking is enabled.

**Sources:** [internal/translator/antigravity/claude/antigravity_claude_request.go:101-159]()

---

### Tool Use Signature Propagation

When a tool call follows a thinking block in the same message, the tool call inherits the thinking signature. This is tracked via `currentMessageThinkingSignature` at [internal/translator/antigravity/claude/antigravity_claude_request.go:134-136]().

*   If a valid signature was found for the thinking block, it is stored in the local variable.
*   Subsequent `tool_use` blocks in the same message use this signature for the `thoughtSignature` field in the Gemini CLI `functionCall` format.

**Sources:** [internal/translator/antigravity/claude/antigravity_claude_request.go:97,134-136,188-197]()

---

## Response Translation: Signature Accumulation

### Response State Machine

The response translator maintains state across streaming chunks using the `Params` struct at [internal/translator/antigravity/claude/antigravity_claude_response.go:29-51]().

```mermaid
classDiagram
    class Params {
        +bool HasFirstResponse
        +int ResponseType
        +int ResponseIndex
        +bool HasContent
        +strings.Builder CurrentThinkingText
        +map[string]string ToolNameMap
    }
    
    note for Params "ResponseType states:<br/>0 = none<br/>1 = content<br/>2 = thinking<br/>3 = function"
```

**Diagram: Response Translation State Structure**

The `CurrentThinkingText` field (line 46) accumulates thinking text as it arrives in streaming chunks.

### Streaming Signature Cache Flow

The caching logic is implemented in `ConvertAntigravityResponseToClaude` at [internal/translator/antigravity/claude/antigravity_claude_response.go:137-153]().

1.  **Accumulation**: As `thought: true` parts arrive with text, the text is appended to `params.CurrentThinkingText`.
2.  **Signature Arrival**: When a part arrives containing a `thoughtSignature`:
    *   The accumulated text is retrieved.
    *   `cache.CacheSignature(modelName, thinkingText, signature)` is called (line 142).
    *   `params.CurrentThinkingText` is reset for potential subsequent blocks (line 144).
3.  **Event Emission**: The signature is emitted to the client as a Claude `signature_delta` event.

**Sources:** [internal/translator/antigravity/claude/antigravity_claude_response.go:46,137-153,165-172]()

---

## Special Case: Gemini Skip Sentinel

For Gemini models, the cache returns a special sentinel value when no cached signature exists to allow the backend to bypass signature validation.

```mermaid
graph LR
    GetCache["GetCachedSignature()"]
    CheckExists{"Entry exists?"}
    ReturnSig["Return cached signature"]
    CheckGroup{"Model group<br/>is 'gemini'?"}
    ReturnSkip["Return 'skip_thought_signature_validator'"]
    ReturnEmpty["Return ''"]
    
    GetCache --> CheckExists
    CheckExists -->|Yes| ReturnSig
    CheckExists -->|No| CheckGroup
    CheckGroup -->|Yes| ReturnSkip
    CheckGroup -->|No| ReturnEmpty
```

**Diagram: Gemini Special Case Handling**

This sentinel approach is used in `HasValidSignature` at [internal/cache/signature_cache.go:182-184]() to treat the skip string as a valid signature specifically for the Gemini group.

**Sources:** [internal/cache/signature_cache.go:123-128,131-135,146-150,182-184]()

---

## Cache Management API

| Function | File:Lines | Purpose |
| :--- | :--- | :--- |
| `CacheSignature` | [internal/cache/signature_cache.go:98-116]() | Stores a signature for thinking text with a 3h TTL. |
| `GetCachedSignature` | [internal/cache/signature_cache.go:120-166]() | Retrieves signature; refreshes TTL on access. |
| `ClearSignatureCache` | [internal/cache/signature_cache.go:169-179]() | Clears cache for a specific model or all models. |
| `HasValidSignature` | [internal/cache/signature_cache.go:182-184]() | Validates length (min 50) and handles Gemini sentinel. |
| `GetModelGroup` | [internal/cache/signature_cache.go:186-195]() | Normalizes model names into `gpt`, `claude`, or `gemini`. |

**Sources:** [internal/cache/signature_cache.go:96-195]()

---

## Multi-Turn Conversation Flow

1.  **Turn 1 (Request)**: Client sends user prompt.
2.  **Turn 1 (Response)**: Proxy receives thinking + signature from provider via `ConvertAntigravityResponseToClaude`. Proxy caches the signature keyed by the thinking text hash and sends both to the client.
3.  **Turn 2 (Request)**: Client sends history including the Turn 1 assistant message (thinking text + signature).
4.  **Turn 2 (Translation)**: Proxy's `ConvertClaudeRequestToAntigravity` sees the thinking block. It checks the `signature_cache`.
    *   If found, it uses the cached signature.
    *   If not found, it validates the client-provided signature.
    *   It attaches the signature to the outgoing Antigravity request.
5.  **Turn 2 (Provider)**: Provider accepts the request because the thinking block is correctly signed.

**Sources:** [internal/translator/antigravity/claude/antigravity_claude_request.go:101-136](), [internal/translator/antigravity/claude/antigravity_claude_response.go:137-153]()

---

# Page: Development and Extension

# Development and Extension

<details>
<summary>Relevant source files</summary>

The following files were used as context for generating this wiki page:

- [docs/sdk-access.md](docs/sdk-access.md)
- [docs/sdk-access_CN.md](docs/sdk-access_CN.md)
- [docs/sdk-advanced.md](docs/sdk-advanced.md)
- [docs/sdk-advanced_CN.md](docs/sdk-advanced_CN.md)
- [docs/sdk-usage.md](docs/sdk-usage.md)
- [docs/sdk-usage_CN.md](docs/sdk-usage_CN.md)
- [docs/sdk-watcher.md](docs/sdk-watcher.md)
- [docs/sdk-watcher_CN.md](docs/sdk-watcher_CN.md)
- [examples/custom-provider/main.go](examples/custom-provider/main.go)
- [internal/access/config_access/provider.go](internal/access/config_access/provider.go)
- [internal/access/reconcile.go](internal/access/reconcile.go)
- [internal/translator/openai/openai/chat-completions/openai_openai_request.go](internal/translator/openai/openai/chat-completions/openai_openai_request.go)
- [sdk/access/errors.go](sdk/access/errors.go)
- [sdk/access/manager.go](sdk/access/manager.go)
- [sdk/access/registry.go](sdk/access/registry.go)
- [sdk/api/options.go](sdk/api/options.go)
- [sdk/cliproxy/builder.go](sdk/cliproxy/builder.go)
- [sdk/cliproxy/providers.go](sdk/cliproxy/providers.go)
- [sdk/cliproxy/types.go](sdk/cliproxy/types.go)
- [sdk/cliproxy/watcher.go](sdk/cliproxy/watcher.go)
- [sdk/config/config.go](sdk/config/config.go)
- [sdk/logging/request_logger.go](sdk/logging/request_logger.go)

</details>



This page provides guidance for developers who want to extend CLIProxyAPI or use it as a Go library. It covers the public SDK interfaces, extension points for custom providers and storage backends, and patterns for testing and debugging.

For information about deploying CLIProxyAPI as a service, see [Deployment Scenarios](#10). For configuration options, see [Configuration Guide](#5).

---

## Overview

CLIProxyAPI is designed as a reusable Go library with several extension points for developers. The primary extension mechanisms include:

| Extension Point | Interface/Type | Purpose |
|----------------|----------------|---------|
| **Service Builder** | `cliproxy.Builder` | Programmatic construction of the proxy service |
| **Provider Executors** | `Executor` | Custom AI provider integrations |
| **Token Storage** | `Store` | Custom credential persistence backends |
| **Request Translation** | `Translator` | Custom request/response format conversion |
| **Access Control** | `Provider` | Custom inbound authentication mechanisms |
| **Selector Strategy** | `Selector` | Custom credential selection algorithms |

Sources: [sdk/cliproxy/builder.go:21-51](), [sdk/access/registry.go:11-14](), [examples/custom-provider/main.go:67-174]()

---

## System Extension Points

The following diagram shows where developers can extend the system and which code entities to implement:

### Extension Architecture
```mermaid
graph TB
    subgraph "Application Entry Point"
        YourApp["Your Go Application"]
    end
    
    subgraph "SDK Builder Layer"
        Builder["cliproxy.NewBuilder()"]
        Service["cliproxy.Service"]
    end
    
    subgraph "Extension Interfaces"
        ProviderExec["clipexec.Executor Interface<br/>Execute(), ExecuteStream(), Refresh()"]
        StoreIface["sdkAuth.Store Interface<br/>Save(), Load(), List(), Delete()"]
        Translator["sdktr.Translator Interface<br/>TranslateRequest(), TranslateResponse()"]
        Selector["coreauth.Selector Interface<br/>Select()"]
        AccessProvider["sdkaccess.Provider Interface<br/>Authenticate()"]
    end
    
    subgraph "Built-in Implementations"
        FileStore["FileTokenStore"]
        PGStore["PostgresStore"]
        GitStore["GitTokenStore"]
        FillFirst["FillFirstSelector"]
        ConfigAuth["config-api-key"]
    end
    
    subgraph "Custom Implementations"
        CustomExec["MyExecutor"]
        CustomStore["Your Custom Store"]
        CustomTranslator["Your Custom Translator"]
        CustomSelector["Your Custom Selector"]
    end
    
    YourApp --> Builder
    Builder --> Service
    
    Service -.->|"WithCoreAuthManager()"| ProviderExec
    Service -.->|"sdkAuth.SetTokenStore()"| StoreIface
    Service -.->|"sdktr.Register()"| Translator
    Service -.->|"coreauth.Selector"| Selector
    Service -.->|"WithRequestAccessManager()"| AccessProvider
    
    ProviderExec -.->|custom| CustomExec
    
    StoreIface -.->|built-in| FileStore
    StoreIface -.->|built-in| PGStore
    StoreIface -.->|built-in| GitStore
    StoreIface -.->|custom| CustomStore
    
    Selector -.->|built-in| FillFirst
    Selector -.->|custom| CustomSelector
    
    AccessProvider -.->|built-in| ConfigAuth
    
    Translator -.->|custom| CustomTranslator
```
Sources: [sdk/cliproxy/builder.go:18-51](), [sdk/access/registry.go:11-14](), [examples/custom-provider/main.go:115-174](), [internal/access/config_access/provider.go:12-29]()

---

## Using the Go SDK

The `cliproxy` package provides a `Builder` pattern for programmatic service construction. This allows embedding CLIProxyAPI in your own applications.

### Basic Service Construction
```mermaid
sequenceDiagram
    participant App as "Your Application"
    participant Builder as "cliproxy.Builder"
    participant Service as "cliproxy.Service"
    participant CoreMgr as "coreauth.Manager"
    participant AccessMgr as "sdkaccess.Manager"
    
    App->>Builder: NewBuilder()
    App->>Builder: WithConfig(cfg)
    App->>Builder: WithConfigPath(path)
    App->>Builder: WithCoreAuthManager(core)
    App->>Builder: WithRequestAccessManager(access)
    App->>Builder: Build()
    Builder->>CoreMgr: Initialize with Selector
    Builder->>AccessMgr: SetProviders(RegisteredProviders)
    Builder->>Service: Construct service instance
    Builder-->>App: Service
    
    App->>Service: Start()
    Service-->>App: Running service
```
Sources: [sdk/cliproxy/builder.go:71-167](), [examples/custom-provider/main.go:185-207]()

For details, see [Using the Go SDK](#9.1).

---

## Creating Custom Executors

The `Executor` interface (often aliased as `clipexec.Executor`) enables integration of custom AI providers.

### Executor Interface and Usage
```mermaid
classDiagram
    class Executor {
        <<interface>>
        +Identifier() string
        +Execute(ctx, auth, req, opts) Response, error
        +ExecuteStream(ctx, auth, req, opts) *StreamResult, error
        +Refresh(ctx, auth) *Auth, error
        +CountTokens(ctx, auth, req, opts) Response, error
        +HttpRequest(ctx, auth, req) *http.Response, error
    }
    
    class MyExecutor {
        +PrepareRequest(req, auth) error
        +Execute(ctx, auth, req, opts) Response, error
    }
    
    Executor <|.. MyExecutor : implements
```
Sources: [examples/custom-provider/main.go:67-174]()

Custom executors must handle authentication injection (e.g., via `PrepareRequest` [examples/custom-provider/main.go:82-92]()), manage upstream HTTP calls, and implement streaming support. For details, see [Creating Custom Executors](#9.2).

---

## Custom Storage Backends

The `Store` interface in `sdk/auth` enables custom token persistence backends. The system automatically selects backends based on environment variables like `PGSTORE_DSN` or `GITSTORE_GIT_URL`.

| Method | Purpose |
|--------|---------|
| `Save(ctx, auth)` | Persist `Auth` object to backing storage |
| `Load(ctx, id)` | Retrieve `Auth` by ID |
| `List(ctx)` | Return all stored `Auth` objects |
| `Delete(ctx, id)` | Remove `Auth` by ID |

Sources: [sdk/cliproxy/builder.go:205-208](), [sdk/cliproxy/types.go:14-28]()

For details, see [Custom Storage Backends](#9.3).

---

## Translation System Deep Dive

The translation system converts requests and responses between different AI provider formats. Developers can register custom translators using `sdktr.Register`.

### Translation Flow
```mermaid
graph LR
    OpenAI["openai.chat Format"] --> Trans["Translator Function"]
    Trans --> Custom["myprov.chat Format"]
    
    subgraph "Registry"
        sdktr["sdktr.Register(fOpenAI, fMyProv, reqFunc, respTrans)"]
    end
```
Sources: [examples/custom-provider/main.go:51-63]()

For details, see [Translation System Deep Dive](#9.4).

---

## Testing and Debugging

CLIProxyAPI includes internal mechanisms for monitoring and debugging, such as the `Watcher` system for configuration hot-reloading and structured logging.

### Watcher and Reload Flow
```mermaid
graph TD
    File["config.yaml"] --> Watcher["Watcher Factory"]
    Watcher --> Debounce["Debounce Logic"]
    Debounce --> Reconcile["ApplyAccessProviders()"]
    Reconcile --> Manager["sdkaccess.Manager.SetProviders()"]
```
Sources: [internal/access/reconcile.go:82-105](), [sdk/cliproxy/watcher.go:11-35](), [docs/sdk-watcher.md:3-15]()

For details, see [Testing and Debugging](#9.5).

---

# Page: Using the Go SDK

# Using the Go SDK

<details>
<summary>Relevant source files</summary>

The following files were used as context for generating this wiki page:

- [docs/sdk-access.md](docs/sdk-access.md)
- [docs/sdk-access_CN.md](docs/sdk-access_CN.md)
- [docs/sdk-advanced.md](docs/sdk-advanced.md)
- [docs/sdk-advanced_CN.md](docs/sdk-advanced_CN.md)
- [docs/sdk-usage.md](docs/sdk-usage.md)
- [docs/sdk-usage_CN.md](docs/sdk-usage_CN.md)
- [docs/sdk-watcher.md](docs/sdk-watcher.md)
- [docs/sdk-watcher_CN.md](docs/sdk-watcher_CN.md)
- [examples/custom-provider/main.go](examples/custom-provider/main.go)
- [internal/access/config_access/provider.go](internal/access/config_access/provider.go)
- [internal/access/reconcile.go](internal/access/reconcile.go)
- [internal/translator/openai/openai/chat-completions/openai_openai_request.go](internal/translator/openai/openai/chat-completions/openai_openai_request.go)
- [sdk/access/errors.go](sdk/access/errors.go)
- [sdk/access/manager.go](sdk/access/manager.go)
- [sdk/access/registry.go](sdk/access/registry.go)
- [sdk/api/options.go](sdk/api/options.go)
- [sdk/cliproxy/builder.go](sdk/cliproxy/builder.go)
- [sdk/cliproxy/providers.go](sdk/cliproxy/providers.go)
- [sdk/cliproxy/types.go](sdk/cliproxy/types.go)
- [sdk/cliproxy/watcher.go](sdk/cliproxy/watcher.go)
- [sdk/config/config.go](sdk/config/config.go)
- [sdk/logging/request_logger.go](sdk/logging/request_logger.go)

</details>



The Go SDK provides a programmatic interface for embedding the CLI Proxy API service in custom applications. Instead of running the proxy as a standalone binary, you can import the `sdk/cliproxy` package and integrate the proxy functionality directly into your own Go programs.

This page covers how to use the SDK to construct and run proxy services. For implementing custom provider executors, see [Creating Custom Executors](9.2). For custom storage backends, see [Custom Storage Backends](9.3). For deeper architectural details, see [Architecture Deep Dive](9.4).

## Overview

The SDK exposes two primary patterns:

1.  **Builder Pattern** - Construct a `Service` instance using `cliproxy.NewBuilder()` with fluent configuration methods [sdk/cliproxy/builder.go:21-165]().
2.  **Service Lifecycle** - Run the service with `Service.Run(ctx)` which blocks until context cancellation or error.

The SDK manages authentication, credential selection, request routing, file watching, and HTTP server lifecycle automatically.

**Sources:** [sdk/cliproxy/builder.go:1-165]()

## Core Components

The SDK consists of three manager layers and a service orchestrator:

**SDK Component Architecture**

```mermaid
graph TB
    Builder["cliproxy.Builder<br/>sdk/cliproxy/builder.go"]
    Service["cliproxy.Service<br/>sdk/cliproxy/service.go"]
    
    subgraph "Manager Layer"
        AuthMgr["sdkAuth.Manager<br/>sdk/auth/manager.go<br/>(Token Persistence)"]
        AccessMgr["sdkaccess.Manager<br/>sdk/access/manager.go<br/>(Request Auth)"]
        CoreMgr["coreauth.Manager<br/>sdk/cliproxy/auth/manager.go<br/>(Execution)"]
    end
    
    subgraph "Provider Layer"
        TokenProvider["TokenClientProvider<br/>interface"]
        APIKeyProvider["APIKeyClientProvider<br/>interface"]
        WatcherFactory["WatcherFactory<br/>interface"]
    end
    
    subgraph "Selection Layer"
        Selector["Selector<br/>interface"]
        RoundRobin["RoundRobinSelector<br/>struct"]
        FillFirst["FillFirstSelector<br/>struct"]
    end
    
    Builder -->|"Build()"| Service
    Builder -->|"WithAuthManager()"| AuthMgr
    Builder -->|"WithRequestAccessManager()"| AccessMgr
    Builder -->|"WithCoreAuthManager()"| CoreMgr
    Builder -->|"WithTokenClientProvider()"| TokenProvider
    Builder -->|"WithAPIKeyClientProvider()"| APIKeyProvider
    Builder -->|"WithWatcherFactory()"| WatcherFactory
    
    CoreMgr --> Selector
    Selector -.implements.-> RoundRobin
    Selector -.implements.-> FillFirst
```

| Component | File Location | Responsibility |
| :--- | :--- | :--- |
| `cliproxy.Builder` | [sdk/cliproxy/builder.go:21-51]() | Fluent configuration interface for service construction |
| `cliproxy.Service` | `sdk/cliproxy/service.go` | Service orchestrator with `Run(ctx)` method |
| `sdkAuth.Manager` | `sdk/auth/manager.go` | Manages OAuth token lifecycle and persistence |
| `sdkaccess.Manager` | [sdk/access/manager.go]() | Validates incoming API key requests [sdk/access/registry.go:10-14]() |
| `coreauth.Manager` | [sdk/cliproxy/auth/manager.go]() | Selects credentials and dispatches to executors |
| `Selector` | [sdk/cliproxy/auth/selector.go]() | Credential selection strategy interface |
| `RoundRobinSelector` | [sdk/cliproxy/auth/selector.go]() | Cycles through credentials evenly |
| `FillFirstSelector` | [sdk/cliproxy/auth/selector.go]() | Exhausts first credential before moving to next [sdk/cliproxy/builder.go:214-217]() |

**Sources:** [sdk/cliproxy/builder.go:21-51](), [sdk/access/registry.go:10-14](), [sdk/cliproxy/builder.go:190-218]()

## Basic Usage Pattern

The simplest SDK integration uses `NewBuilder()` with minimal configuration:

**Service Lifecycle Sequence**

```mermaid
sequenceDiagram
    participant App as "Your Application"
    participant Builder as "cliproxy.NewBuilder()"
    participant Service as "cliproxy.Service"
    participant HTTP as "api.Server<br/>(Gin Engine)"
    
    App->>Builder: "NewBuilder()"
    App->>Builder: "WithConfig(cfg)"
    App->>Builder: "WithConfigPath(path)"
    App->>Builder: "Build()"
    Builder-->>App: "service, err"
    
    App->>Service: "Run(ctx)"
    Service->>HTTP: "Start listening on port"
    
    Note over Service,HTTP: "Service runs until<br/>context cancellation"
    
    App->>App: "signal.NotifyContext(SIGINT)"
    App->>Service: "context cancel"
    Service->>HTTP: "Graceful shutdown"
    Service-->>App: "nil or error"
```

For a minimal integration: populate a `*config.Config` (at minimum `Port` and `AuthDir`), chain `NewBuilder().WithConfig(cfg).WithConfigPath(path)`, call `Build()` to get a `*Service`, then call `Run(ctx)` to block until context cancellation or fatal error.

**Sources:** [sdk/cliproxy/builder.go:66-173](), [examples/custom-provider/main.go:175-207]()

## Builder Configuration Methods

The `Builder` provides fluent methods for customizing service components:

### Required Configuration

**Builder Method Chain**

```mermaid
graph LR
    NewBuilder["cliproxy.NewBuilder()"]
    WithConfig["WithConfig(cfg)"]
    WithConfigPath["WithConfigPath(path)"]
    Build["Build()"]
    
    NewBuilder --> WithConfig
    WithConfig --> WithConfigPath
    WithConfigPath --> Build
    Build -->|"Returns"| Service["Service, error"]
```

| Method | Parameter | Required | Description |
| :--- | :--- | :--- | :--- |
| `NewBuilder()` | - | ✓ | Creates new builder instance [sdk/cliproxy/builder.go:71-73]() |
| `WithConfig()` | `*config.Config` | ✓ | Sets application configuration [sdk/cliproxy/builder.go:82-85]() |
| `WithConfigPath()` | `string` | ✓ | Sets config file path for hot-reload [sdk/cliproxy/builder.go:94-97]() |
| `Build()` | - | ✓ | Validates and constructs service [sdk/cliproxy/builder.go:167-174]() |

**Sources:** [sdk/cliproxy/builder.go:66-174]()

### Optional Component Overrides

| Method | Parameter | Default Behavior |
| :--- | :--- | :--- |
| `WithTokenClientProvider()` | `TokenClientProvider` | `NewFileTokenClientProvider()` [sdk/cliproxy/builder.go:175-178]() |
| `WithAPIKeyClientProvider()` | `APIKeyClientProvider` | `NewAPIKeyClientProvider()` [sdk/cliproxy/builder.go:180-183]() |
| `WithWatcherFactory()` | `WatcherFactory` | `defaultWatcherFactory` [sdk/cliproxy/builder.go:185-188]() |
| `WithAuthManager()` | `*sdkAuth.Manager` | `newDefaultAuthManager()` [sdk/cliproxy/builder.go:190-193]() |
| `WithRequestAccessManager()` | `*sdkaccess.Manager` | `sdkaccess.NewManager()` [sdk/cliproxy/builder.go:195-198]() |
| `WithCoreAuthManager()` | `*coreauth.Manager` | `coreauth.NewManager(...)` [sdk/cliproxy/builder.go:203-220]() |
| `WithHooks()` | `Hooks` | Empty hooks [sdk/cliproxy/builder.go:118-121]() |

**Sources:** [sdk/cliproxy/builder.go:100-220]()

### Server Options and Hooks

| Method | Parameter | Purpose |
| :--- | :--- | :--- |
| `WithServerOptions()` | `...api.ServerOption` | Appends server configuration options [sdk/cliproxy/builder.go:142-145]() |
| `WithLocalManagementPassword()` | `string` | Configures password for localhost management requests [sdk/cliproxy/builder.go:148-154]() |
| `WithPostAuthHook()` | `coreauth.PostAuthHook` | Registers a hook called after Auth record creation [sdk/cliproxy/builder.go:158-164]() |

**Sources:** [sdk/cliproxy/builder.go:142-164]()

## Request Access Management

The SDK uses the `@sdk/access` package to handle inbound request authentication. This system chains multiple providers to validate credentials like API keys or custom tokens.

**Access Provider Reconciliation**

```mermaid
graph TD
    Config["config.yaml api-keys"]
    Manager["sdkaccess.Manager"]
    Reconcile["internal/access.ReconcileProviders"]
    Registry["sdkaccess.RegisteredProviders()"]
    
    Config -->|"Register()"| Reconcile
    Registry --> Reconcile
    Reconcile -->|"SetProviders()"| Manager
```

In the SDK, the `config-api-key` provider is registered automatically if `api-keys` are present in the configuration [internal/access/config_access/provider.go:13-29](). You can also register custom providers via `sdkaccess.RegisterProvider` [sdk/access/registry.go:30-42]().

The `ApplyAccessProviders` function in `internal/access/reconcile.go` handles the logic for updating the `Manager` when configuration changes without a restart [internal/access/reconcile.go:82-105]().

**Sources:** [sdk/access/registry.go:30-42](), [internal/access/config_access/provider.go:13-29](), [docs/sdk-access.md:25-35](), [internal/access/reconcile.go:82-105]()

## Custom Provider Integration

The SDK allows developers to implement the `Executor` interface to support proprietary or custom AI services.

**Custom Executor Flow**

```mermaid
sequenceDiagram
    participant SDK as "cliproxy.Service"
    participant Core as "coreauth.Manager"
    participant Exec as "MyExecutor (Custom)"
    
    SDK->>Core: "Execute request"
    Core->>Exec: "PrepareRequest(httpReq, auth)"
    Exec-->>Core: "Add Auth Headers"
    Core->>Exec: "Execute(ctx, auth, req, opts)"
    Exec->>Upstream: "HTTP POST /chat/completions"
    Upstream-->>Exec: "JSON Response"
    Exec-->>Core: "clipexec.Response"
    Core-->>SDK: "Final Result"
```

To integrate a custom provider:
1.  Implement the `clipexec.Executor` interface [examples/custom-provider/main.go:67-174]().
2.  Register custom translators if the provider uses a non-OpenAI format [examples/custom-provider/main.go:51-63]().
3.  Register the executor with the `coreauth.Manager` [examples/custom-provider/main.go:185-186]().
4.  Optionally register models in the global registry during `OnAfterStart` [examples/custom-provider/main.go:189-197]().

**Sources:** [examples/custom-provider/main.go:51-197]()

## Lifecycle Hooks

The `Hooks` struct provides callbacks for service lifecycle events [sdk/cliproxy/builder.go:56-64]():

| Hook | Signature | Purpose |
| :--- | :--- | :--- |
| `OnBeforeStart` | `func(*config.Config)` | Called before the service starts, allowing configuration modifications [sdk/cliproxy/builder.go:57-59]() |
| `OnAfterStart` | `func(*Service)` | Called after the service has started successfully, providing access to the service instance [sdk/cliproxy/builder.go:61-63]() |

**Sources:** [sdk/cliproxy/builder.go:56-64]()

## Hot Reloading and Watchers

The SDK supports hot-reloading of configuration and authentication tokens through a file watcher system. The `WatcherWrapper` provides an abstraction over the internal file monitoring logic [sdk/cliproxy/types.go:84-126]().

| Function | Responsibility |
| :--- | :--- |
| `WatcherFactory` | Creates a watcher for config and token changes [sdk/cliproxy/types.go:70-81]() |
| `WatcherWrapper` | Proxies start/stop and snapshot operations to the underlying watcher [sdk/cliproxy/types.go:84-126]() |
| `defaultWatcherFactory` | The default implementation using `internal/watcher` [sdk/cliproxy/watcher.go:11-35]() |

The `DispatchRuntimeAuthUpdate` method allows runtime-generated authentication updates (e.g., from WebSocket providers) to be injected into the watcher's update queue [sdk/cliproxy/types.go:121-126]().

**Sources:** [sdk/cliproxy/types.go:70-149](), [sdk/cliproxy/watcher.go:11-35](), [docs/sdk-watcher_CN.md:7-15]()

## Programmatic Client Loading

The SDK defines interfaces for loading provider clients programmatically from configuration or token storage:

*   **TokenClientProvider**: Responsible for loading token-based clients (e.g., OAuth tokens) [sdk/cliproxy/types.go:17-28]().
*   **APIKeyClientProvider**: Responsible for loading clients backed by API keys defined in `config.yaml` [sdk/cliproxy/types.go:39-50]().

The `apiKeyClientProvider` implementation uses `watcher.BuildAPIKeyClients` to parse keys for Gemini, Claude, Vertex, and OpenAI-compatible providers [sdk/cliproxy/providers.go:31-47]().

**Sources:** [sdk/cliproxy/types.go:17-50](), [sdk/cliproxy/providers.go:31-47]()

---

# Page: Creating Custom Executors

# Creating Custom Executors

<details>
<summary>Relevant source files</summary>

The following files were used as context for generating this wiki page:

- [examples/custom-provider/main.go](examples/custom-provider/main.go)
- [internal/runtime/executor/aistudio_executor.go](internal/runtime/executor/aistudio_executor.go)
- [internal/runtime/executor/antigravity_executor.go](internal/runtime/executor/antigravity_executor.go)
- [internal/runtime/executor/claude_executor.go](internal/runtime/executor/claude_executor.go)
- [internal/runtime/executor/codex_executor.go](internal/runtime/executor/codex_executor.go)
- [internal/runtime/executor/gemini_cli_executor.go](internal/runtime/executor/gemini_cli_executor.go)
- [internal/runtime/executor/gemini_executor.go](internal/runtime/executor/gemini_executor.go)
- [internal/runtime/executor/gemini_vertex_executor.go](internal/runtime/executor/gemini_vertex_executor.go)
- [internal/runtime/executor/iflow_executor.go](internal/runtime/executor/iflow_executor.go)
- [internal/runtime/executor/openai_compat_executor.go](internal/runtime/executor/openai_compat_executor.go)
- [internal/runtime/executor/qwen_executor.go](internal/runtime/executor/qwen_executor.go)
- [internal/thinking/apply_user_defined_test.go](internal/thinking/apply_user_defined_test.go)
- [internal/translator/openai/openai/chat-completions/openai_openai_request.go](internal/translator/openai/openai/chat-completions/openai_openai_request.go)
- [sdk/api/handlers/handlers.go](sdk/api/handlers/handlers.go)
- [sdk/api/options.go](sdk/api/options.go)
- [sdk/cliproxy/auth/conductor.go](sdk/cliproxy/auth/conductor.go)
- [sdk/cliproxy/auth/conductor_overrides_test.go](sdk/cliproxy/auth/conductor_overrides_test.go)
- [sdk/cliproxy/auth/openai_compat_pool_test.go](sdk/cliproxy/auth/openai_compat_pool_test.go)
- [sdk/cliproxy/providers.go](sdk/cliproxy/providers.go)
- [sdk/cliproxy/types.go](sdk/cliproxy/types.go)
- [sdk/cliproxy/watcher.go](sdk/cliproxy/watcher.go)
- [sdk/logging/request_logger.go](sdk/logging/request_logger.go)

</details>



This page explains how to implement the `ProviderExecutor` interface to add support for a new AI provider backend. It covers the interface contract, the supporting types, common patterns used by all built-in executors, and how to register a custom executor with the running service.

For context on how executors fit into the broader request pipeline, see the [Provider Executor System](#3.4) architecture page. For registering executors when embedding CLIProxyAPI as a Go library, see [Using the Go SDK](#9.1). For how requests are translated between formats before being handed to an executor, see [Translation System Deep Dive](#9.4).

---

## The ProviderExecutor Interface

Every provider backend is represented by a single interface defined in the SDK.

| Method | Responsibility |
|---|---|
| `Identifier()` | Returns the provider key string (e.g. `"gemini"`, `"claude"`). Used to look up the executor and match against `auth.Provider`. |
| `Execute()` | Handles a single non-streaming request. Translates, calls upstream, translates response, returns payload. |
| `ExecuteStream()` | Handles a streaming request. Returns a `*StreamResult` with a channel of chunks. |
| `Refresh()` | Refreshes OAuth tokens for a given auth entry. No-op for API-key-only providers. |
| `CountTokens()` | Counts tokens for a request without generating a response. |
| `HttpRequest()` | Injects credentials into a pre-built `*http.Request` and executes it. Used by proxy passthrough routes. |

Sources: [sdk/cliproxy/auth/conductor.go:28-43](), [internal/runtime/executor/gemini_executor.go:57-57](), [internal/runtime/executor/claude_executor.go:54-54](), [internal/runtime/executor/openai_compat_executor.go:37-37]()

---

## Supporting Types

**Diagram: Core Types Across Packages**

```mermaid
classDiagram
    namespace sdk_cliproxy_auth {
        class ProviderExecutor["ProviderExecutor (interface)"] {
            +Identifier() string
            +Execute()
            +ExecuteStream()
            +Refresh()
            +CountTokens()
            +HttpRequest()
        }
        class Auth {
            +ID string
            +Provider string
            +Attributes map~string~string~
            +Metadata map~string~any~
        }
        class Manager {
            +RegisterExecutor(ProviderExecutor)
        }
    }
    namespace sdk_cliproxy_executor {
        class Request {
            +Model string
            +Payload []byte
            +Metadata map~string~any~
        }
        class Options {
            +SourceFormat Format
            +Stream bool
            +OriginalRequest []byte
            +Alt string
        }
        class Response {
            +Payload []byte
            +Headers http.Header
        }
        class StreamResult {
            +Headers http.Header
            +Chunks chan StreamChunk
        }
    }
    Manager --> ProviderExecutor : "dispatches via"
    ProviderExecutor --> Auth : "receives per request"
    ProviderExecutor --> Request : "receives"
    ProviderExecutor --> Options : "receives"
    ProviderExecutor --> Response : "returns"
    ProviderExecutor --> StreamResult : "returns"
```

Sources: [sdk/cliproxy/auth/conductor.go:28-43](), [sdk/cliproxy/auth/conductor.go:130-166]()

### Auth

`Auth` carries all credential state for one account. Key fields used by executors:

| Field | Type | Purpose |
|---|---|---|
| `Attributes` | `map[string]string` | Static config values: `api_key`, `base_url`, `proxy_url` |
| `Metadata` | `map[string]any` | Mutable runtime state: `access_token`, `refresh_token`, `email` |
| `Provider` | `string` | Provider key this auth belongs to |
| `ID` | `string` | Unique identifier used for logging and usage tracking |

Sources: [internal/runtime/executor/claude_executor.go:61-71](), [internal/runtime/executor/openai_compat_executor.go:44-52]()

---

## Built-in Executors as Reference Implementations

**Diagram: Executor Implementations by File**

```mermaid
classDiagram
    class ProviderExecutor["ProviderExecutor\n(sdk/cliproxy/auth/conductor.go)"] {
        <<interface>>
    }
    class GeminiExecutor["GeminiExecutor\n(gemini_executor.go)"]
    class GeminiCLIExecutor["GeminiCLIExecutor\n(gemini_cli_executor.go)"]
    class GeminiVertexExecutor["GeminiVertexExecutor\n(gemini_vertex_executor.go)"]
    class ClaudeExecutor["ClaudeExecutor\n(claude_executor.go)"]
    class CodexExecutor["CodexExecutor\n(codex_executor.go)"]
    class AntigravityExecutor["AntigravityExecutor\n(antigravity_executor.go)"]
    class OpenAICompatExecutor["OpenAICompatExecutor\n(openai_compat_executor.go)"]
    class IFlowExecutor["IFlowExecutor\n(iflow_executor.go)"]
    class QwenExecutor["QwenExecutor\n(qwen_executor.go)"]
    class AIStudioExecutor["AIStudioExecutor\n(aistudio_executor.go)"]

    ProviderExecutor <|.. GeminiExecutor
    ProviderExecutor <|.. GeminiCLIExecutor
    ProviderExecutor <|.. GeminiVertexExecutor
    ProviderExecutor <|.. ClaudeExecutor
    ProviderExecutor <|.. CodexExecutor
    ProviderExecutor <|.. AntigravityExecutor
    ProviderExecutor <|.. OpenAICompatExecutor
    ProviderExecutor <|.. IFlowExecutor
    ProviderExecutor <|.. QwenExecutor
    ProviderExecutor <|.. AIStudioExecutor
```

Sources: [internal/runtime/executor/gemini_executor.go:40-43](), [internal/runtime/executor/claude_executor.go:40-42](), [internal/runtime/executor/codex_executor.go:39-41](), [internal/runtime/executor/antigravity_executor.go:59-61](), [internal/runtime/executor/openai_compat_executor.go:26-29](), [internal/runtime/executor/iflow_executor.go:35-37](), [internal/runtime/executor/qwen_executor.go:173-175](), [internal/runtime/executor/aistudio_executor.go:27-31](), [internal/runtime/executor/gemini_cli_executor.go:48-50](), [internal/runtime/executor/gemini_vertex_executor.go:173-175]()

---

## Implementing the Interface

### Identifier

Return a stable lowercase string that uniquely identifies your provider. This string is matched against `auth.Provider` when the manager dispatches a request.

```go
func (e *MyExecutor) Identifier() string { return "myprovider" }
```

Sources: [internal/runtime/executor/gemini_executor.go:57-57](), [internal/runtime/executor/claude_executor.go:54-54]()

---

### PrepareRequest

Inject provider credentials into an `*http.Request` that has already been constructed by the caller. Used by passthrough proxy routes.

The pattern across all built-in executors is:
1. Extract credentials from `auth.Attributes` or `auth.Metadata`.
2. Set `Authorization` (or a provider-specific header like `x-goog-api-key` or `x-api-key`).
3. Apply any custom headers from `auth.Attributes` using `util.ApplyCustomHeadersFromAttrs`.

Sources: [internal/runtime/executor/gemini_executor.go:60-74](), [internal/runtime/executor/claude_executor.go:57-80](), [internal/runtime/executor/openai_compat_executor.go:40-54]()

---

### HttpRequest

Call `PrepareRequest` then execute the request using a proxy-aware HTTP client.

```go
func (e *MyExecutor) HttpRequest(ctx context.Context, auth *cliproxyauth.Auth, req *http.Request) (*http.Response, error) {
	if req == nil {
		return nil, fmt.Errorf("executor: request is nil")
	}
	httpReq := req.WithContext(ctx)
	if err := e.PrepareRequest(httpReq, auth); err != nil {
		return nil, err
	}
	httpClient := newProxyAwareHTTPClient(ctx, e.cfg, auth, 0)
	return httpClient.Do(httpReq)
}
```

`newProxyAwareHTTPClient` is a package-level helper in `internal/runtime/executor` that creates an `*http.Client` respecting the `auth.ProxyURL` and global proxy settings.

Sources: [internal/runtime/executor/gemini_executor.go:77-90](), [internal/runtime/executor/claude_executor.go:83-96](), [internal/runtime/executor/openai_compat_executor.go:57-70]()

---

### Execute (Non-Streaming)

**Diagram: Execute Method Flow**

```mermaid
sequenceDiagram
    participant Manager
    participant Execute as "MyExecutor.Execute()"
    participant thinking as "thinking.ParseSuffix / ApplyThinking"
    participant sdktranslator as "sdktranslator.TranslateRequest"
    participant upstream as "Upstream HTTP API"
    participant translateResp as "sdktranslator.TranslateNonStream"

    Manager->>Execute: "Execute(ctx, auth, req, opts)"
    Execute->>thinking: "ParseSuffix(req.Model)"
    Execute->>Execute: "newUsageReporter(ctx, ...)"
    Execute->>sdktranslator: "TranslateRequest(from, to, baseModel, req.Payload, false)"
    Execute->>thinking: "ApplyThinking(translated, req.Model, ...)"
    Execute->>Execute: "applyPayloadConfigWithRoot(...)"
    Execute->>upstream: "http.NewRequestWithContext + httpClient.Do"
    upstream-->>Execute: "*http.Response"
    Execute->>Execute: "recordAPIResponseMetadata"
    Execute->>Execute: "reporter.publish(parseXXXUsage(data))"
    Execute->>translateResp: "TranslateNonStream(ctx, to, from, req.Model, ...)"
    translateResp-->>Execute: "translated JSON string"
    Execute-->>Manager: "cliproxyexecutor.Response{Payload}"
```

The canonical steps for a non-streaming `Execute` implementation:

1. **Reject unsupported modes early**: Check `opts.Alt` for modes like `"responses/compact"` if not implemented. [internal/runtime/executor/gemini_executor.go:106-108]()
2. **Strip thinking suffix**: Use `thinking.ParseSuffix(req.Model).ModelName` to get the actual model ID. [internal/runtime/executor/gemini_executor.go:109-109]()
3. **Set up usage reporting**: Initialize a `newUsageReporter` to track token consumption. [internal/runtime/executor/gemini_executor.go:113-114]()
4. **Translate the request**: Convert incoming payload (e.g., OpenAI format) to provider format (e.g., Gemini). [internal/runtime/executor/gemini_executor.go:117-125]()
5. **Apply thinking parameters**: Inject thinking/reasoning configuration if enabled for the model. [internal/runtime/executor/gemini_executor.go:127-130]()
6. **Apply payload config overrides**: Use `applyPayloadConfigWithRoot` to inject system prompts or parameters. [internal/runtime/executor/gemini_executor.go:134-134]()
7. **Build and execute the HTTP request**: Call `recordAPIRequest` then `httpClient.Do`. [internal/runtime/executor/gemini_executor.go:151-181]()
8. **Log response metadata**: Call `recordAPIResponseMetadata` for tracking. [internal/runtime/executor/gemini_executor.go:191-191]()
9. **Handle errors**: Detect 429/403 errors and return a `statusErr`. [internal/runtime/executor/gemini_executor.go:192-198]()
10. **Parse and publish usage**: Extract token counts and report them. [internal/runtime/executor/aistudio_executor.go:164-164]()
11. **Translate the response**: Convert provider response back to the client's expected format. [internal/runtime/executor/gemini_executor.go:203-204]()

Sources: [internal/runtime/executor/gemini_executor.go:105-210](), [internal/runtime/executor/claude_executor.go:98-228](), [internal/runtime/executor/openai_compat_executor.go:72-177]()

---

### ExecuteStream (Streaming)

`ExecuteStream` follows the same setup steps as `Execute` but returns a `StreamResult` containing a channel.

1. Check the HTTP response status **before** starting the goroutine. If the status is an error, return it immediately. [internal/runtime/executor/gemini_executor.go:281-287]()
2. Start a goroutine that reads from the response body using a `bufio.Scanner` with a large buffer (typically `streamScannerBuffer`). [internal/runtime/executor/gemini_executor.go:292-297]()
3. Send translated chunks on the channel using `sdktranslator.TranslateStream`. [internal/runtime/executor/gemini_executor.go:301-310]()
4. Call `reporter.ensurePublished(ctx)` upon completion to finalize usage tracking. [internal/runtime/executor/openai_compat_executor.go:285-285]()

Sources: [internal/runtime/executor/gemini_executor.go:212-338](), [internal/runtime/executor/openai_compat_executor.go:179-290]()

---

### CountTokens

Count tokens using the upstream API or a local tokenizer.

```go
func (e *MyExecutor) CountTokens(ctx context.Context, auth *cliproxyauth.Auth, req cliproxyexecutor.Request, opts cliproxyexecutor.Options) (resp cliproxyexecutor.Response, err error) {
    // ... setup and translation ...
    action := "countTokens"
    // ... call upstream ...
    return resp, nil
}
```

`CodexExecutor` ([internal/runtime/executor/codex_executor.go:402-436]()) implements counting locally using the `tiktoken-go` tokenizer.

Sources: [internal/runtime/executor/gemini_executor.go:340-419](), [internal/runtime/executor/codex_executor.go:402-436]()

---

### Refresh

`Refresh` is called by the `Manager`'s background loop. It must return an updated `*Auth` with new token values.

Providers using static API keys implement this as a no-op returning the original `auth`. [internal/runtime/executor/gemini_executor.go:421-423]()

OAuth providers like `AntigravityExecutor` ([internal/runtime/executor/antigravity_executor.go:846-855]()) or `ClaudeExecutor` perform the refresh flow and update `auth.Metadata`.

Sources: [internal/runtime/executor/gemini_executor.go:421-424](), [internal/runtime/executor/antigravity_executor.go:846-855]()

---

### Special Handling: Rate Limiting and Quota

Custom executors can implement specific logic for provider constraints. For example, `QwenExecutor` includes a sliding-window rate limiter to enforce a 60 requests per minute limit per credential [internal/runtime/executor/qwen_executor.go:68-120](). It also detects quota exhaustion errors (HTTP 403/429) and maps them to a cooldown period until the next day reset [internal/runtime/executor/qwen_executor.go:149-160]().

Sources: [internal/runtime/executor/qwen_executor.go:68-120](), [internal/runtime/executor/qwen_executor.go:149-160]()

---

## Registering the Executor

To register your custom executor, use the `RegisterExecutor` method on the `coreauth.Manager`.

When using the `Builder` pattern to start the service:

```go
builder := cliproxy.NewBuilder().
    WithConfig(cfg).
    WithConfigPath(path)

// If you have a custom coreManager
coreManager := coreauth.NewManager(store, selector, hook)
coreManager.RegisterExecutor(NewMyCustomExecutor(cfg))

builder.WithCoreAuthManager(coreManager).Build()
```

The `Manager` will automatically dispatch requests to your executor if the incoming request's resolved `Auth` record has a `Provider` field matching your executor's `Identifier()`.

Sources: [sdk/cliproxy/auth/conductor.go:169-191](), [sdk/cliproxy/auth/conductor.go:132-132]()

---

## Implementation Checklist

| Step | Notes |
|---|---|
| Implement `Identifier()` | Must match the `provider` string in auth JSON files. |
| Implement `PrepareRequest()` | Set headers like `Authorization` or `x-api-key`. |
| Implement `HttpRequest()` | Wrap `PrepareRequest` and execute via `httpClient.Do`. |
| Implement `Execute()` | Use `sdktranslator` for request/response conversion. |
| Implement `ExecuteStream()` | Use a goroutine and `chan StreamChunk` for SSE. |
| Implement `Refresh()` | No-op for API keys; implement OAuth refresh for tokens. |
| Register with `Manager` | Use `RegisterExecutor` during service startup. |

Sources: [internal/runtime/executor/gemini_executor.go:57-90](), [internal/runtime/executor/openai_compat_executor.go:37-70](), [sdk/cliproxy/auth/conductor.go:132-132]()

---

# Page: Custom Storage Backends

# Custom Storage Backends

<details>
<summary>Relevant source files</summary>

The following files were used as context for generating this wiki page:

- [.env.example](.env.example)
- [cmd/server/main.go](cmd/server/main.go)
- [go.mod](go.mod)
- [go.sum](go.sum)
- [internal/store/gitstore.go](internal/store/gitstore.go)
- [internal/store/objectstore.go](internal/store/objectstore.go)
- [internal/store/postgresstore.go](internal/store/postgresstore.go)
- [internal/watcher/synthesizer/config_test.go](internal/watcher/synthesizer/config_test.go)
- [internal/watcher/synthesizer/context.go](internal/watcher/synthesizer/context.go)
- [internal/watcher/synthesizer/file.go](internal/watcher/synthesizer/file.go)
- [internal/watcher/synthesizer/file_test.go](internal/watcher/synthesizer/file_test.go)
- [internal/watcher/synthesizer/helpers.go](internal/watcher/synthesizer/helpers.go)
- [internal/watcher/synthesizer/helpers_test.go](internal/watcher/synthesizer/helpers_test.go)
- [internal/watcher/synthesizer/interface.go](internal/watcher/synthesizer/interface.go)
- [sdk/auth/filestore.go](sdk/auth/filestore.go)
- [sdk/cliproxy/service_excluded_models_test.go](sdk/cliproxy/service_excluded_models_test.go)

</details>



This page explains the storage backend system used by CLIProxyAPI to persist OAuth tokens and configuration files. It covers the `Store` interface contract, the built-in remote backends (`PostgresStore`, `GitTokenStore`, `ObjectTokenStore`), the local spool pattern they share, and how to plug in a custom implementation.

For information on configuring which backend to use, see [Storage Backend Options](5.2). For how credentials are loaded and selected at request time, see [Authentication and Credential Management](3.3).

---

## Overview

All storage activity in CLIProxyAPI is routed through a single registered `TokenStore`. At startup, the server inspects environment variables to decide which concrete store to instantiate, then calls `sdkAuth.RegisterTokenStore()` to make it available to the rest of the system.

**Store selection logic:**

| Environment Variable | Backend Selected |
|---|---|
| `PGSTORE_DSN` | `PostgresStore` |
| `GITSTORE_GIT_URL` | `GitTokenStore` |
| `OBJECTSTORE_ENDPOINT` | `ObjectTokenStore` |
| *(none)* | `FileTokenStore` (default) |

> Only one backend is active at a time. PostgreSQL takes priority if multiple variables are set.

**Store selection diagram:**

```mermaid
flowchart TD
    env["Environment Variables"] --> check1{"PGSTORE_DSN\nset?"}
    check1 -->|"yes"| pg["PostgresStore\ninternal/store/postgresstore.go"]
    check1 -->|"no"| check2{"GITSTORE_GIT_URL\nset?"}
    check2 -->|"yes"| git["GitTokenStore\ninternal/store/gitstore.go"]
    check2 -->|"no"| check3{"OBJECTSTORE_ENDPOINT\nset?"}
    check3 -->|"yes"| obj["ObjectTokenStore\ninternal/store/objectstore.go"]
    check3 -->|"no"| file["FileTokenStore\nsdk/auth/filestore.go"]
    pg --> register["sdkAuth.RegisterTokenStore()"]
    git --> register
    obj --> register
    file --> register
```

Sources: `[cmd/server/main.go:179-245]()`, `[internal/store/postgresstore.go:49-54]()`, `[internal/store/gitstore.go:42-48]()`, `[internal/store/objectstore.go:55-61]()`

---

## The Store Interface

All backends satisfy the interface consumed by `sdkAuth.RegisterTokenStore()` in the `sdk/auth` package. Based on the shared method surface across all implementations, the interface requires:

| Method | Description |
|---|---|
| `Save(ctx, *Auth)` | Persists a single auth credential; returns the resolved local file path |
| `List(ctx)` | Enumerates all stored credentials from the local spool |
| `Delete(ctx, id)` | Removes a credential by ID |
| `Bootstrap(ctx, examplePath)` | Runs once at startup: creates remote tables/buckets, syncs remote→local |
| `ConfigPath()` | Returns the local spool path to `config.yaml` |
| `AuthDir()` | Returns the local spool path to the auth file directory |
| `SetBaseDir(dir)` | Hook used by some auth flows to update the working directory |

The `*Auth` type is `cliproxyauth.Auth` from `sdk/cliproxy/auth`.

**Interface-to-implementation mapping:**

```mermaid
classDiagram
    class TokenStore {
        <<interface>>
        +Save(ctx, auth) string, error
        +List(ctx) Auth[], error
        +Delete(ctx, id) error
        +Bootstrap(ctx, examplePath) error
        +ConfigPath() string
        +AuthDir() string
        +SetBaseDir(dir)
    }
    class PostgresStore {
        -db sql.DB
        -cfg PostgresStoreConfig
        -spoolRoot string
        -configPath string
        -authDir string
        +EnsureSchema(ctx) error
    }
    class GitTokenStore {
        -baseDir string
        -repoDir string
        -remote string
        +EnsureRepository() error
    }
    class ObjectTokenStore {
        -client minio.Client
        -cfg ObjectStoreConfig
        -spoolRoot string
    }
    class FileTokenStore {
        -baseDir string
    }
    TokenStore <|.. PostgresStore
    TokenStore <|.. GitTokenStore
    TokenStore <|.. ObjectTokenStore
    TokenStore <|.. FileTokenStore
```

Sources: `[internal/store/postgresstore.go:39-46]()`, `[internal/store/gitstore.go:28-38]()`, `[internal/store/objectstore.go:45-52]()`, `[sdk/auth/filestore.go:22-26]()`

---

## The Local Spool Pattern

Remote backends (PostgreSQL, Git, S3) follow a **local spool pattern**: they maintain a directory on disk that mirrors the remote state. The rest of the server (including the file watcher and synthesizers) reads and writes only to this local directory. The store is responsible for keeping the local copy in sync with the remote.

**Bootstrap (remote → local sync):**

```mermaid
sequenceDiagram
    participant main as "Service Init"
    participant store as "Store (Postgres/Git/S3)"
    participant remote as "Remote (DB/Git/S3)"
    participant spool as "Local Spool Directory"
    main->>store: Bootstrap(ctx, exampleConfigPath)
    store->>remote: Fetch config/auth records
    remote-->>store: Payloads
    store->>spool: Write config.yaml & auths/*.json
```

Sources: `[internal/store/postgresstore.go:147-158]()`, `[internal/store/gitstore.go:92-213]()`, `[internal/store/objectstore.go:142-156]()`

**Runtime (local → remote sync):**

When auth tokens are saved, the store writes the local file first, then pushes the change to the remote backend.

```mermaid
sequenceDiagram
    participant caller as "Auth Manager"
    participant store as "Store"
    participant spool as "Local Spool"
    participant remote as "Remote Backend"
    caller->>store: Save(ctx, auth)
    store->>spool: Write auth JSON to disk
    store->>remote: Upsert record (SQL/Git Push/S3 Put)
    store-->>caller: return local file path
```

Sources: `[internal/store/postgresstore.go:189-260]()`, `[internal/store/gitstore.go:216-296]()`, `[internal/store/objectstore.go:159-226]()`

---

## Built-in Backends

### File Store (Default)
The `FileTokenStore` persists credentials directly to the filesystem.
*   **Behavior:** Uses `os.WriteFile` and `os.Remove`.
*   **Metadata:** Supports `metadataSetter` interface to inject metadata before saving `[sdk/auth/filestore.go:69-77]()`.

### PostgreSQL Store
**Type:** `PostgresStore` in `internal/store/postgresstore.go`.
*   **Schema:** Manages `config_store` and `auth_store` tables `[internal/store/postgresstore.go:121-143]()`.
*   **Sync:** `syncAuthFromDatabase` mirrors JSONB rows to local `.json` files `[internal/store/postgresstore.go:154-155]()`.

### Git Store
**Type:** `GitTokenStore` in `internal/store/gitstore.go`.
*   **Persistence:** Uses `go-git` to commit and push changes on every `Save()` `[internal/store/gitstore.go:216-296]()`.
*   **Sync:** Performs `git pull` during `Bootstrap` `[internal/store/gitstore.go:179-193]()`.

### Object Store (S3-Compatible)
**Type:** `ObjectTokenStore` in `internal/store/objectstore.go`.
*   **Backend:** Uses MinIO SDK to interact with S3-compatible APIs `[internal/store/objectstore.go:98-111]()`.
*   **Persistence:** Uploads files to a specified bucket under a prefix `[internal/store/objectstore.go:222-224]()`.

---

## Synthesis and Metadata

The `FileSynthesizer` component bridges the gap between raw files in the `AuthDir` and `Auth` entities used by the runtime.

```mermaid
flowchart LR
    subgraph "Storage Layer"
        Store["Store Implementation\ninternal/store/"]
        Spool["Local Spool (Filesystem)"]
    end
    subgraph "Synthesis Layer"
        Syn["FileSynthesizer\ninternal/watcher/synthesizer/file.go"]
    end
    subgraph "Runtime Layer"
        Auth["Auth Entity\nsdk/cliproxy/auth/auth.go"]
    end
    
    Store --"Mirrors to"--> Spool
    Spool --"Read by"--> Syn
    Syn --"Synthesize()"--> Auth
```

**Synthesis Logic:**
*   `Synthesize()` iterates through `.json` files in the auth directory `[internal/watcher/synthesizer/file.go:40-59]()`.
*   `synthesizeFileAuths()` converts JSON metadata into `coreauth.Auth` objects, handling provider types and labels `[internal/watcher/synthesizer/file.go:68-139]()`.
*   **Excluded Models:** `ApplyAuthExcludedModelsMeta` merges per-account exclusions with global config and stores a hash in attributes `[internal/watcher/synthesizer/helpers.go:58-104]()`.

Sources: `[internal/watcher/synthesizer/file.go:28-183]()`, `[internal/watcher/synthesizer/helpers.go:58-104]()`

---

## Implementing a Custom Backend

To implement a custom store:

1.  **Define the Struct:** Create a type that holds necessary clients (e.g., Redis, DynamoDB).
2.  **Implement `Bootstrap`:** Ensure the remote storage is ready and sync its contents to a local spool directory.
3.  **Implement `Save`:** 
    *   Write the `auth.Metadata` to a local file in the spool.
    *   Push that content to your remote storage.
4.  **Implement `ConfigPath` and `AuthDir`:** Return the absolute paths to the mirrored files in your local spool.
5.  **Register:** Call `sdkAuth.RegisterTokenStore(yourStore)` at application startup.

Sources: `[internal/store/postgresstore.go:189-225]()`, `[sdk/auth/filestore.go:30-42]()`

---

# Page: Translation System Deep Dive

# Translation System Deep Dive

<details>
<summary>Relevant source files</summary>

The following files were used as context for generating this wiki page:

- [examples/translator/main.go](examples/translator/main.go)
- [internal/translator/antigravity/gemini/antigravity_gemini_request.go](internal/translator/antigravity/gemini/antigravity_gemini_request.go)
- [internal/translator/antigravity/gemini/antigravity_gemini_request_test.go](internal/translator/antigravity/gemini/antigravity_gemini_request_test.go)
- [internal/translator/antigravity/openai/chat-completions/antigravity_openai_request.go](internal/translator/antigravity/openai/chat-completions/antigravity_openai_request.go)
- [internal/translator/claude/gemini/claude_gemini_request.go](internal/translator/claude/gemini/claude_gemini_request.go)
- [internal/translator/claude/openai/chat-completions/claude_openai_request.go](internal/translator/claude/openai/chat-completions/claude_openai_request.go)
- [internal/translator/claude/openai/chat-completions/claude_openai_request_test.go](internal/translator/claude/openai/chat-completions/claude_openai_request_test.go)
- [internal/translator/claude/openai/responses/claude_openai-responses_request.go](internal/translator/claude/openai/responses/claude_openai-responses_request.go)
- [internal/translator/codex/claude/codex_claude_request.go](internal/translator/codex/claude/codex_claude_request.go)
- [internal/translator/codex/claude/codex_claude_request_test.go](internal/translator/codex/claude/codex_claude_request_test.go)
- [internal/translator/codex/gemini/codex_gemini_request.go](internal/translator/codex/gemini/codex_gemini_request.go)
- [internal/translator/gemini-cli/claude/gemini-cli_claude_request.go](internal/translator/gemini-cli/claude/gemini-cli_claude_request.go)
- [internal/translator/gemini-cli/gemini/gemini-cli_gemini_request.go](internal/translator/gemini-cli/gemini/gemini-cli_gemini_request.go)
- [internal/translator/gemini-cli/gemini/gemini-cli_gemini_response.go](internal/translator/gemini-cli/gemini/gemini-cli_gemini_response.go)
- [internal/translator/gemini-cli/gemini/init.go](internal/translator/gemini-cli/gemini/init.go)
- [internal/translator/gemini-cli/openai/chat-completions/gemini-cli_openai_request.go](internal/translator/gemini-cli/openai/chat-completions/gemini-cli_openai_request.go)
- [internal/translator/gemini/claude/gemini_claude_request.go](internal/translator/gemini/claude/gemini_claude_request.go)
- [internal/translator/gemini/gemini-cli/gemini_gemini-cli_request.go](internal/translator/gemini/gemini-cli/gemini_gemini-cli_request.go)
- [internal/translator/gemini/gemini/gemini_gemini_request.go](internal/translator/gemini/gemini/gemini_gemini_request.go)
- [internal/translator/gemini/gemini/gemini_gemini_request_test.go](internal/translator/gemini/gemini/gemini_gemini_request_test.go)
- [internal/translator/gemini/openai/chat-completions/gemini_openai_request.go](internal/translator/gemini/openai/chat-completions/gemini_openai_request.go)
- [internal/translator/gemini/openai/responses/gemini_openai-responses_request.go](internal/translator/gemini/openai/responses/gemini_openai-responses_request.go)
- [internal/translator/openai/claude/openai_claude_request.go](internal/translator/openai/claude/openai_claude_request.go)
- [internal/translator/openai/claude/openai_claude_request_test.go](internal/translator/openai/claude/openai_claude_request_test.go)
- [internal/translator/openai/gemini/openai_gemini_request.go](internal/translator/openai/gemini/openai_gemini_request.go)
- [sdk/translator/builtin/builtin.go](sdk/translator/builtin/builtin.go)
- [sdk/translator/formats.go](sdk/translator/formats.go)
- [sdk/translator/helpers.go](sdk/translator/helpers.go)

</details>



## Purpose and Scope

This document explains the translation system architecture that enables CLIProxyAPI to convert between different AI provider API formats. The translation system allows clients using one API format (e.g., OpenAI) to communicate with providers using different formats (e.g., Claude, Gemini, Codex), with full support for streaming, tool calls, and thinking blocks.

The system is designed to be highly efficient, using a pure functional approach to JSON transformation that avoids the overhead of Go struct marshaling.

---

## Translation Architecture

CLIProxyAPI's translation system is built on a pure functional design using `gjson` for JSON parsing and `sjson` for JSON construction. This approach enables zero-allocation transformations of large request/response payloads without defining Go structs for every API format.

### Design Principles

1.  **Pure Functions**: Translation functions are stateless and side-effect-free (except for streaming responses).
2.  **Zero-Copy JSON**: Uses `gjson`/`sjson` to manipulate JSON without marshaling to Go structs.
3.  **Bidirectional**: Supports translation in both request and response directions.
4.  **Format Agnostic**: Provider executors are decoupled from translation logic.

### Translation Function Signatures

All request translators follow this signature pattern:

`func ConvertXRequestToY(modelName string, rawJSON []byte, stream bool) []byte`
[internal/translator/gemini/openai/chat-completions/gemini_openai_request.go:29-29]()

Response translators for streaming use a stateful approach:

`func ConvertXResponseToY(ctx context.Context, modelName string, originalRequestRawJSON, requestRawJSON, rawJSON []byte, param *any) []string`

Sources: [internal/translator/gemini/openai/chat-completions/gemini_openai_request.go:29-29](), [internal/translator/claude/openai/chat-completions/claude_openai_request.go:46-46](), [internal/translator/codex/claude/codex_claude_request.go:36-36]()

---

## Request Translation Flow

```mermaid
graph TB
    Client["Client Request<br/>(OpenAI format)"]
    Protocol["Protocol Detection<br/>User-Agent/Route"]
    
    subgraph "Translation Layer"
        OAIToClaude["ConvertOpenAIRequestToClaude"]
        OAIToGemini["ConvertOpenAIRequestToGemini"]
        OAIToGeminiCLI["ConvertOpenAIRequestToGeminiCLI"]
        OAIToAntigravity["ConvertOpenAIRequestToAntigravity"]
        ClaudeToAntigravity["ConvertClaudeRequestToAntigravity"]
        GeminiToAntigravity["ConvertGeminiRequestToAntigravity"]
        ResponsesToGemini["ConvertOpenAIResponsesRequestToGemini"]
        OAIToCodex["ConvertOpenAIRequestToCodex"]
    end
    
    subgraph "Provider Executors"
        GeminiExec["GeminiExecutor<br/>Gemini API format"]
        ClaudeExec["ClaudeExecutor<br/>Claude format"]
        AntigravityExec["AntigravityExecutor<br/>Gemini CLI format"]
        CodexExec["CodexExecutor<br/>Responses API format"]
    end
    
    Client --> Protocol
    Protocol --> OAIToClaude
    Protocol --> OAIToGemini
    Protocol --> OAIToGeminiCLI
    Protocol --> OAIToAntigravity
    Protocol --> ClaudeToAntigravity
    Protocol --> GeminiToAntigravity
    Protocol --> ResponsesToGemini
    Protocol --> OAIToCodex
    
    OAIToGemini --> GeminiExec
    OAIToGeminiCLI --> AntigravityExec
    OAIToAntigravity --> AntigravityExec
    ClaudeToAntigravity --> AntigravityExec
    GeminiToAntigravity --> AntigravityExec
    ResponsesToGemini --> GeminiExec
    OAIToCodex --> CodexExec
```

**Translation Selection Matrix**

| Source Format | Target Provider | Translator Function | File Location |
| :--- | :--- | :--- | :--- |
| OpenAI Chat | Gemini | `ConvertOpenAIRequestToGemini` | [internal/translator/gemini/openai/chat-completions/gemini_openai_request.go:29]() |
| OpenAI Chat | Gemini CLI | `ConvertOpenAIRequestToGeminiCLI` | [internal/translator/gemini-cli/openai/chat-completions/gemini-cli_openai_request.go:29]() |
| OpenAI Chat | Antigravity | `ConvertOpenAIRequestToAntigravity` | [internal/translator/antigravity/openai/chat-completions/antigravity_openai_request.go:29]() |
| OpenAI Chat | Claude | `ConvertOpenAIRequestToClaude` | [internal/translator/claude/openai/chat-completions/claude_openai_request.go:46]() |
| OpenAI Chat | Codex | `ConvertOpenAIRequestToCodex` | [internal/translator/codex/openai/chat-completions/codex_openai_request.go:29]() |
| OpenAI Responses | Gemini | `ConvertOpenAIResponsesRequestToGemini` | [internal/translator/gemini/openai/responses/gemini_openai-responses_request.go:15]() |
| OpenAI Responses | Claude | `ConvertOpenAIResponsesRequestToClaude` | [internal/translator/claude/openai/responses/claude_openai-responses_request.go:34]() |
| Claude Messages | Gemini | `ConvertClaudeRequestToGemini` | [internal/translator/gemini/claude/gemini_claude_request.go:32]() |
| Claude Messages | Gemini CLI | `ConvertClaudeRequestToCLI` | [internal/translator/gemini-cli/claude/gemini-cli_claude_request.go:37]() |
| Claude Messages | OpenAI | `ConvertClaudeRequestToOpenAI` | [internal/translator/openai/claude/openai_claude_request.go:19]() |
| Claude Messages | Codex | `ConvertClaudeRequestToCodex` | [internal/translator/codex/claude/codex_claude_request.go:36]() |
| Gemini | Claude | `ConvertGeminiRequestToClaude` | [internal/translator/claude/gemini/claude_gemini_request.go:48]() |

Sources: [internal/translator/gemini/openai/chat-completions/gemini_openai_request.go:29](), [internal/translator/claude/openai/chat-completions/claude_openai_request.go:46](), [internal/translator/gemini/openai/responses/gemini_openai-responses_request.go:15](), [internal/translator/codex/claude/codex_claude_request.go:36](), [internal/translator/claude/openai/responses/claude_openai-responses_request.go:34](), [internal/translator/gemini/claude/gemini_claude_request.go:32](), [internal/translator/gemini-cli/claude/gemini-cli_claude_request.go:37](), [internal/translator/openai/claude/openai_claude_request.go:19](), [internal/translator/claude/gemini/claude_gemini_request.go:48]()

---

## Message Structure Transformations

### Role Mapping

Different API formats use different role names for the same concepts. The system normalizes these roles during translation.

| OpenAI | Claude | Gemini/CLI | Codex | Description |
| :--- | :--- | :--- | :--- | :--- |
| `system` | `system` (top-level) | `systemInstruction` | `developer` | System instructions |
| `user` | `user` | `user` | `user` | User messages |
| `assistant` | `assistant` | `model` | `assistant` | AI responses |
| `tool` | `tool_result` | `function` (role) | `function_call_output` | Tool outputs |

**OpenAI → Gemini CLI Example:**
[internal/translator/gemini-cli/openai/chat-completions/gemini-cli_openai_request.go:169-219]() handles the conversion of system and user messages into the `request.contents` array, mapping `assistant` to `model`.

**Claude → Codex Example:**
[internal/translator/codex/claude/codex_claude_request.go:82-108]() maps Claude's `assistant` role to Codex's `assistant` role, but converts `system` messages into messages with the `developer` role.

Sources: [internal/translator/gemini-cli/openai/chat-completions/gemini-cli_openai_request.go:169-219](), [internal/translator/codex/claude/codex_claude_request.go:82-108]()

### Content Structure Conversion

```mermaid
graph LR
    subgraph "OpenAI_Entity_Space"
        OAIMsg["messages (Array)"]
        OAIContent["content (String/Array)"]
        OAISystem["role: system"]
        OAITools["tools (Array)"]
    end
    
    subgraph "Gemini_Entity_Space"
        GCLIContents["contents (Array)"]
        GCLIParts["parts (Array)"]
        GCLISysInstr["systemInstruction"]
        GCLITools["tools[].functionDeclarations"]
    end
    
    subgraph "Claude_Entity_Space"
        ClaudeMsg["messages (Array)"]
        ClaudeContent["content (Array)"]
        ClaudeSystem["system (String/Array)"]
        ClaudeTools["tools (Array)"]
    end
    
    OAIMsg --> GCLIContents
    OAIContent --> GCLIParts
    OAISystem --> GCLISysInstr
    OAITools --> GCLITools
    
    ClaudeMsg --> GCLIContents
    ClaudeContent --> GCLIParts
    ClaudeSystem --> GCLISysInstr
    ClaudeTools --> GCLITools
```

Sources: [internal/translator/gemini-cli/openai/chat-completions/gemini-cli_openai_request.go:101-164](), [internal/translator/claude/openai/chat-completions/claude_openai_request.go:166-220]()

---

## Tool/Function Call Translation

### Tool Declaration Conversion

Tool definitions require field name transformations between formats. CLIProxyAPI often has to clean or restructure schemas for compatibility.

**OpenAI → Gemini:**
Maps `tools[].function.parameters` to `tools[].functionDeclarations[].parametersJsonSchema` [internal/translator/gemini/openai/chat-completions/gemini_openai_request.go:296-399](). It also removes OpenAI-specific fields like `strict`.

**Claude → Codex:**
Handles tool name shortening for Codex compatibility [internal/translator/codex/claude/codex_claude_request.go:220-263](). Claude tool names that are too long or contain invalid characters are mapped via `shortenNameIfNeeded` and `buildReverseMapFromClaudeOriginalToShort`.

**Gemini → Claude:**
Converts Gemini `functionDeclarations` to Claude `tools` [internal/translator/claude/gemini/claude_gemini_request.go:348-400](), mapping `parameters` to `input_schema`.

Sources: [internal/translator/gemini/openai/chat-completions/gemini_openai_request.go:296-399](), [internal/translator/codex/claude/codex_claude_request.go:220-263](), [internal/translator/claude/gemini/claude_gemini_request.go:348-400]()

### Tool Call and Response Mapping

```mermaid
graph TB
    subgraph "OpenAI_Code_Entities"
        OAICall["tool_calls (Array)<br/>id, function.name, function.arguments"]
        OAIResp["role: tool<br/>tool_call_id, content"]
    end
    
    subgraph "Gemini_Code_Entities"
        GCLICall["parts[].functionCall<br/>name, args"]
        GCLIResp["parts[].functionResponse<br/>name, response.result"]
    end
    
    subgraph "Claude_Code_Entities"
        ClaudeCall["type: tool_use<br/>id, name, input"]
        ClaudeResp["type: tool_result<br/>tool_use_id, content"]
    end
    
    OAICall -->|"ConvertOpenAIRequestToGemini"| GCLICall
    OAIResp -->|"ConvertOpenAIRequestToGemini"| GCLIResp
    
    ClaudeCall -->|"ConvertClaudeRequestToGemini"| GCLICall
    ClaudeResp -->|"ConvertClaudeRequestToGemini"| GCLIResp
```

Sources: [internal/translator/gemini/openai/chat-completions/gemini_openai_request.go:109-142](), [internal/translator/gemini/claude/gemini_claude_request.go:87-119]()

---

## Thinking Block Translation

### Reasoning Effort Translation

OpenAI's `reasoning_effort` parameter is mapped to provider-specific configurations like Gemini's `thinkingConfig` or Claude's `thinking` budget/adaptive settings.

**OpenAI → Gemini:**
[internal/translator/gemini/openai/chat-completions/gemini_openai_request.go:44-57]() maps `reasoning_effort` to `generationConfig.thinkingConfig`.
- `auto` → `thinkingBudget: -1`, `includeThoughts: true`
- specific levels → `thinkingLevel: effort`, `includeThoughts: true`

**OpenAI → Claude:**
[internal/translator/claude/openai/chat-completions/claude_openai_request.go:69-115]() handles both legacy budget-based thinking and new adaptive thinking for Claude 4.6.
- Adaptive models use `thinking.type: "adaptive"` and `output_config.effort`.
- Legacy models use `thinking.type: "enabled"` and `thinking.budget_tokens`.

**Claude → OpenAI:**
[internal/translator/openai/claude/openai_claude_request.go:62-96]() converts Claude's `thinking` config back to OpenAI's `reasoning_effort` using `thinking.ConvertBudgetToLevel`.

Sources: [internal/translator/gemini/openai/chat-completions/gemini_openai_request.go:44-57](), [internal/translator/claude/openai/chat-completions/claude_openai_request.go:69-115](), [internal/translator/openai/claude/openai_claude_request.go:62-96]()

---

## Special Format Handling

### OpenAI Responses API (Codex)

The Responses API (used by Codex) requires a different structure than Chat Completions. It uses a top-level `input` array of objects.

**Chat Completions → Codex:**
[internal/translator/codex/openai/chat-completions/codex_openai_request.go:113-200]() transforms standard messages into Codex `input` objects.
- `tool` role messages become `type: "function_call_output"`.
- Standard messages become `type: "message"`.
- Multimodal inputs (images, files) are mapped to `input_image` and `input_file`.

**Responses → Gemini:**
[internal/translator/gemini/openai/responses/gemini_openai-responses_request.go:38-110]() performs "normalization" on the Responses `input` array. It ensures that `function_call` items are immediately followed by their corresponding `function_call_output` items, as required by the Gemini API's sequential pairing logic.

Sources: [internal/translator/codex/openai/chat-completions/codex_openai_request.go:113-200](), [internal/translator/gemini/openai/responses/gemini_openai-responses_request.go:38-110]()

### Image and Multimodal Data

Translators handle the conversion of image formats between providers:

- **OpenAI → Gemini**: Converts `image_url` data URLs to Gemini `inline_data` [internal/translator/gemini/openai/chat-completions/gemini_openai_request.go:181-208]().
- **Claude → Gemini**: Converts Claude's `base64` source images to Gemini `inline_data` [internal/translator/gemini/claude/gemini_claude_request.go:121-135]().
- **Gemini → Claude**: Converts Gemini `inlineData` or `fileData` to Claude's base64 format [internal/translator/claude/gemini/claude_gemini_request.go:216-261]().

Sources: [internal/translator/gemini/openai/chat-completions/gemini_openai_request.go:181-208](), [internal/translator/gemini/claude/gemini_claude_request.go:121-135](), [internal/translator/claude/gemini/claude_gemini_request.go:216-261]()

---

## Key Implementation Details

### Zero-Allocation JSON Manipulation

The system relies on `gjson` for reading and `sjson` for writing JSON. This avoids the overhead of unmarshaling into Go structs.

**Example: Model and Config Setting**
[internal/translator/gemini/openai/chat-completions/gemini_openai_request.go:32-40]()
```go
out := []byte(`{"contents":[]}`)
out, _ = sjson.SetBytes(out, "model", modelName)
if genConfig := gjson.GetBytes(rawJSON, "generationConfig"); genConfig.Exists() {
    out, _ = sjson.SetRawBytes(out, "generationConfig", []byte(genConfig.Raw))
}
```

### Tool Response Consolidation

Gemini requires tool responses to be grouped within the conversation. Translators like `ConvertOpenAIRequestToGeminiCLI` [internal/translator/gemini-cli/openai/chat-completions/gemini-cli_openai_request.go:109-141]() perform a multi-pass scan of messages to build a map of tool call IDs to names and then cache the responses. This allows them to rebuild the conversation history in a format the target provider accepts.

Sources: [internal/translator/gemini/openai/chat-completions/gemini_openai_request.go:32-40](), [internal/translator/gemini-cli/openai/chat-completions/gemini-cli_openai_request.go:109-141]()

---

# Page: Testing and Debugging

# Testing and Debugging

<details>
<summary>Relevant source files</summary>

The following files were used as context for generating this wiki page:

- [internal/cache/signature_cache.go](internal/cache/signature_cache.go)
- [internal/cache/signature_cache_test.go](internal/cache/signature_cache_test.go)
- [internal/registry/model_definitions.go](internal/registry/model_definitions.go)
- [internal/registry/model_registry.go](internal/registry/model_registry.go)
- [internal/registry/model_registry_cache_test.go](internal/registry/model_registry_cache_test.go)
- [internal/registry/model_registry_hook_test.go](internal/registry/model_registry_hook_test.go)
- [internal/registry/model_registry_safety_test.go](internal/registry/model_registry_safety_test.go)
- [internal/runtime/executor/cache_helpers.go](internal/runtime/executor/cache_helpers.go)
- [internal/translator/antigravity/claude/antigravity_claude_request.go](internal/translator/antigravity/claude/antigravity_claude_request.go)
- [internal/translator/antigravity/claude/antigravity_claude_request_test.go](internal/translator/antigravity/claude/antigravity_claude_request_test.go)
- [internal/translator/antigravity/claude/antigravity_claude_response.go](internal/translator/antigravity/claude/antigravity_claude_response.go)
- [internal/translator/antigravity/claude/antigravity_claude_response_test.go](internal/translator/antigravity/claude/antigravity_claude_response_test.go)
- [sdk/cliproxy/model_registry.go](sdk/cliproxy/model_registry.go)

</details>



This page covers the testing strategies, debugging tools, and log analysis patterns used in CLIProxyAPI. It detail the integration test suite for the translation and thinking subsystems, the structured logging architecture, and workflows for diagnosing issues in the request pipeline.

---

## Running the Test Suite

Tests are standard Go tests. The codebase includes unit tests for individual components and integration-style matrix tests for complex logic like thinking budget conversions.

```sh
# Run all tests
go test ./...

# Run only the thinking end-to-end matrix
go test ./test/ -run TestThinkingE2EMatrix_Suffix -v

# Run signature cache unit tests
go test ./internal/cache/ -run TestCacheSignature -v

# Run Claude translation unit tests
go test ./internal/translator/antigravity/claude/ -v
```

### Test Suite Structure

```mermaid
graph TD
    subgraph "Test Entry Points"
        A["test/ package"] -- "Integration" --> B["thinking_conversion_test.go"]
        C["internal/translator/..."] -- "Unit" --> D["antigravity_claude_request_test.go"]
        E["internal/cache/..."] -- "Unit" --> F["signature_cache_test.go"]
    end

    subgraph "Code Entities Under Test"
        B --> G["thinking.ApplyThinking"]
        D --> H["claude.ConvertClaudeRequestToAntigravity"]
        F --> I["cache.CacheSignature"]
    end

    subgraph "Global State"
        J["registry.GetGlobalRegistry"]
        K["cache.signatureCache"]
    end

    B -.-> J
    F -.-> K
```
Sources: [test/thinking_conversion_test.go:1-50](), [internal/translator/antigravity/claude/antigravity_claude_request_test.go:1-11](), [internal/cache/signature_cache_test.go:1-10]()

---

## Translator and Thinking Testing

### Translation Unit Tests
The translation system is tested by providing raw JSON inputs and asserting the structure of the transformed output using `gjson`. For example, `TestConvertClaudeRequestToAntigravity_BasicStructure` verifies that Claude-style system prompts are correctly mapped to Gemini-style `systemInstruction` parts [internal/translator/antigravity/claude/antigravity_claude_request_test.go:11-55]().

| Test Function | Target Logic | Key Assertions |
|---|---|---|
| `TestConvertClaudeRequestToAntigravity_RoleMapping` | Role Translation | `assistant` role becomes `model` [internal/translator/antigravity/claude/antigravity_claude_request_test.go:57-74]() |
| `TestConvertClaudeRequestToAntigravity_ThinkingBlocks` | Thinking Extraction | Extracts `thought` and `thoughtSignature` [internal/translator/antigravity/claude/antigravity_claude_request_test.go:76-117]() |
| `TestConvertClaudeRequestToAntigravity_ToolDeclarations` | Tool Schema | `input_schema` renamed to `parametersJsonSchema` [internal/translator/antigravity/claude/antigravity_claude_request_test.go:154-194]() |

### Thinking Integration Matrix
The `thinking_conversion_test.go` file contains an E2E matrix that exercises the full pipeline:
1. **Registry Setup**: Registers test models with specific `ThinkingSupport` capabilities [internal/registry/model_registry.go:70-84]().
2. **Translation**: Calls `TranslateRequest` to convert formats (e.g., OpenAI to Gemini).
3. **Thinking Application**: Calls `ApplyThinking` to inject budget or level configurations.
4. **Validation**: Uses `gjson` to verify the final JSON payload matches expected provider-specific fields.

Sources: [test/thinking_conversion_test.go:28-120](), [internal/registry/model_registry_safety_test.go:8-30]()

---

## Signature Cache Debugging

The `signature_cache` is critical for Claude multi-turn conversations where thinking blocks must be signed.

### Cache Mechanics
The cache uses a `sync.Map` storing `groupCache` buckets keyed by model group (e.g., "claude", "gemini") [internal/cache/signature_cache.go:31-41]().

**Title: Signature Cache Data Flow**

```mermaid
sequenceDiagram
    participant P as "claude.Params"
    participant R as "claude.ConvertAntigravityResponseToClaude"
    participant C as "cache.signature_cache"
    
    Note over P, C: Response Streaming
    R->>P: Accumulate CurrentThinkingText
    R->>C: CacheSignature(model, text, sig)
    C->>C: hashText(text)
    C-->>C: Store in groupCache.entries
    
    Note over P, C: Subsequent Request
    participant T as "claude.ConvertClaudeRequestToAntigravity"
    T->>C: GetCachedSignature(model, text)
    C->>C: hashText(text)
    C-->>T: return signature
```
Sources: [internal/cache/signature_cache.go:98-116](), [internal/translator/antigravity/claude/antigravity_claude_response.go:218-245]()

### Debugging Cache State
- **TTL**: Signatures expire after 3 hours (`SignatureCacheTTL`) [internal/cache/signature_cache.go:19]().
- **Validation**: Signatures must be at least 50 characters long to be cached [internal/cache/signature_cache.go:25]().
- **Purge**: A background goroutine runs every 10 minutes to clean up expired entries [internal/cache/signature_cache.go:28-72]().

Tests like `TestCacheSignature_ExpirationLogic` and `TestCacheSignature_Overwrite` verify these behaviors [internal/cache/signature_cache_test.go:175-210]().

---

## Log Analysis and Troubleshooting

### Structured Field Correlation
CLIProxyAPI uses `logrus` for structured logging. Key fields to watch during debugging:

| Field | Meaning | Code Reference |
|---|---|---|
| `request_id` | Unique ID for the HTTP request | `logging.GetRequestID` |
| `provider` | The AI provider being called | `ModelInfo.Type` [internal/registry/model_registry.go:29]() |
| `model` | The specific model ID | `ModelInfo.ID` [internal/registry/model_registry.go:21]() |

### Debugging Thinking Failures
If thinking is not appearing in upstream requests:
1. Check if the model is marked as `UserDefined`. User-defined models skip capability validation [internal/registry/model_registry.go:59-62]().
2. Verify the `ThinkingSupport` metadata for the model in `internal/registry/model_definitions.go`.
3. Look for logs from `ConvertClaudeRequestToAntigravity`. If a thinking block is "unsigned" (no valid signature in cache), it is dropped to avoid Gemini API errors [internal/translator/antigravity/claude/antigravity_claude_request.go:139-148]().

### Common Troubleshooting Patterns

| Symptom | Potential Cause | Debug Step |
|---|---|---|
| 404 Model Not Found | Model not registered or client suspended | Check `GlobalModelRegistry().GetAvailableModels()` [sdk/cliproxy/model_registry.go:18]() |
| Missing Thinking | Signature mismatch or invalid budget | Verify `cache.HasValidSignature` [internal/cache/signature_cache.go:182-184]() |
| Registry Staleness | Cache not invalidated | Verify `invalidateAvailableModelsCacheLocked` calls [internal/registry/model_registry.go:154-159]() |
| Prompt Cache Miss | Codex cache expired | Check `codexCacheMap` TTL (1 hour) [internal/runtime/executor/cache_helpers.go:13-18]() |

Sources: [internal/registry/model_registry_cache_test.go:25-54](), [internal/runtime/executor/cache_helpers.go:8-18](), [internal/translator/antigravity/claude/antigravity_claude_request.go:139-152]()

---

## Model Registry Safety

The registry implements defensive cloning to prevent mutations in one request from affecting global state.

**Title: Registry Memory Safety**

```mermaid
graph LR
    subgraph "Internal State"
        M["ModelRegistration.Info"]
    end
    
    subgraph "API Access"
        L["LookupModelInfo"]
        GA["GetAvailableModels"]
    end
    
    M -- "cloneModelInfo()" --> L
    M -- "cloneModelInfo()" --> GA
    
    L --> U1["Request 1 Context"]
    GA --> U2["Request 2 Context"]
```
Sources: [internal/registry/model_definitions.go:91-101](), [internal/registry/model_registry_safety_test.go:8-30]()

Tests like `TestGetModelInfoReturnsClone` ensure that modifying a returned `ModelInfo` struct does not corrupt the source data in `globalRegistry` [internal/registry/model_registry_safety_test.go:8-30]().

Sources: [internal/registry/model_registry.go:131-147](), [internal/registry/model_registry_safety_test.go:32-57]()

---

# Page: Deployment Scenarios

# Deployment Scenarios

<details>
<summary>Relevant source files</summary>

The following files were used as context for generating this wiki page:

- [.dockerignore](.dockerignore)
- [.github/workflows/docker-image.yml](.github/workflows/docker-image.yml)
- [.github/workflows/pr-test-build.yml](.github/workflows/pr-test-build.yml)
- [.github/workflows/release.yaml](.github/workflows/release.yaml)
- [.gitignore](.gitignore)
- [.goreleaser.yml](.goreleaser.yml)
- [Dockerfile](Dockerfile)
- [LICENSE](LICENSE)
- [auths/.gitkeep](auths/.gitkeep)
- [cmd/server/main.go](cmd/server/main.go)
- [docker-build.ps1](docker-build.ps1)
- [docker-build.sh](docker-build.sh)
- [docker-compose.yml](docker-compose.yml)
- [go.mod](go.mod)
- [go.sum](go.sum)
- [internal/store/gitstore.go](internal/store/gitstore.go)
- [internal/store/postgresstore.go](internal/store/postgresstore.go)

</details>



This section covers practical deployment guides for running CLIProxyAPI in different environments and at different scales. It covers the supported deployment modes, the infrastructure components involved, and helps you select the right topology for your situation.

For configuration file settings applicable to all deployments, see [Configuration Guide](#5). For storage backend specifics, see [Storage Backend Options](#5.2). For the Go SDK-based programmatic deployment, see [Using the Go SDK](#9.1).

---

## Deployment Modes

CLIProxyAPI supports three primary deployment topologies:

| Deployment Mode | State Storage | Instances | Best For |
|---|---|---|---|
| Single-Server | Local filesystem | 1 | Personal use, small teams, local dev |
| Cloud-Native | External (PostgreSQL, Git, Object Storage) | 1 | Cloud environments, managed infra |
| High Availability | External (shared) | Multiple | Large teams, high request volume |

The choice of topology is driven primarily by two factors: **how many instances** you need to run, and **where auth credentials and usage statistics are stored**. External storage backends (PostgreSQL, Git, object storage) are required when running more than one instance, because auth tokens and configuration must be accessible to all nodes. These are activated via environment variables like `PGSTORE_DSN`, `GITSTORE_GIT_URL`, or `OBJECTSTORE_ENDPOINT`.

Sources: [cmd/server/main.go:179-210](), [.gitignore:16-19](), [docker-compose.yml:1-28]()

---

## Core Infrastructure Components

Regardless of topology, every CLIProxyAPI deployment shares the same internal components. The diagram below maps conceptual components to their concrete code-level representations.

**Diagram: CLIProxyAPI Deployment Component Map**

```mermaid
graph TD
    subgraph "Host_Orchestrator"
        cfg["config.yaml\n(CLI_PROXY_CONFIG_PATH)"]
        authdir["auths/\n(CLI_PROXY_AUTH_PATH)\n-> /root/.cli-proxy-api"]
        logdir["logs/\n(CLI_PROXY_LOG_PATH)\n-> /CLIProxyAPI/logs"]
    end

    subgraph "Container_cli-proxy-api"
        main["main() in cmd/server/main.go"]
        registry["registry.ModelRegistry"]
        authmgr["coreauth.CoreManager"]
        executor["registry.ExecutorRegistry"]
        translator["translator_registry"]
    end

    subgraph "Storage_Backends"
        localfs["FileStore\n(internal/store/filestore.go)"]
        pgstore["PostgresStore\n(internal/store/postgresstore.go)"]
        gitstore["GitTokenStore\n(internal/store/gitstore.go)"]
        objectstore["ObjectTokenStore\n(internal/store/objectstore.go)"]
    end

    cfg -->|"flag -config"| main
    authdir -->|"volume mount"| localfs
    logdir -->|"logging.SetupBaseLogger"| main

    main --> registry
    main --> authmgr
    main --> executor
    main --> translator

    authmgr --> localfs
    authmgr --> pgstore
    authmgr --> gitstore
    authmgr --> objectstore
```

Sources: [cmd/server/main.go:47-152](), [docker-compose.yml:24-27](), [.gitignore:16-19](), [internal/store/postgresstore.go:39-46]()

---

## Exposed Ports

All ports are declared in `docker-compose.yml` and exposed on the host. Different AI CLI tools connect to different ports to mimic their original provider endpoints.

| Host Port | Container Port | Protocol / Purpose |
|---|---|---|
| `8317` | `8317` | Primary API port (default, configurable via `port` in `config.yaml`) |
| `8085` | `8085` | Gemini CLI / AI Studio compatible endpoint |
| `1455` | `1455` | Claude API endpoint |
| `54545` | `54545` | Codex / OpenAI Responses endpoint |
| `51121` | `51121` | Amp CLI control plane proxy |
| `11451` | `11451` | Additional provider endpoint |

Sources: [docker-compose.yml:17-23](), [Dockerfile:29]()

---

## Volume Mounts and Path Overrides

Three directories are mounted into the container and can be overridden via environment variables before running `docker compose`.

| Environment Variable | Default Value | Mount Target in Container |
|---|---|---|
| `CLI_PROXY_CONFIG_PATH` | `./config.yaml` | `/CLIProxyAPI/config.yaml` |
| `CLI_PROXY_AUTH_PATH` | `./auths` | `/root/.cli-proxy-api` |
| `CLI_PROXY_LOG_PATH` | `./logs` | `/CLIProxyAPI/logs` |

The `auths/` directory (mounted to `/root/.cli-proxy-api`) holds OAuth token files and API key credential files managed by the storage backend. The `config.yaml` is read at startup and monitored for changes by the file watcher.

The `isCloudDeploy` variable (triggered by `DEPLOY` env) in `main.go` signals a cloud deployment mode, which can trigger different initialization logic.

Sources: [cmd/server/main.go:132-152](), [docker-compose.yml:16-27](), [.gitignore:25-26]()

---

## Deployment Scenario Comparison

The following diagram shows how the three deployment scenarios differ in their use of storage and service topology.

**Diagram: Deployment Topology Comparison**

```mermaid
graph LR
    subgraph "Single-Server_10.1"
        ss_client["AI_CLI_Client"]
        ss_proxy["cli-proxy-api\n(Docker/systemd)"]
        ss_fs["Local_auths/\nLocal_logs/"]
        ss_client --> ss_proxy
        ss_proxy --> ss_fs
    end

    subgraph "Cloud-Native_10.2"
        cn_client["AI_CLI_Client"]
        cn_proxy["cli-proxy-api\n(K8s/Cloud_Run)"]
        cn_ext["External_Storage\n(PostgresStore / ObjectTokenStore)"]
        cn_client --> cn_proxy
        cn_proxy --> cn_ext
    end

    subgraph "High_Availability_10.3"
        ha_lb["Load_Balancer"]
        ha_p1["cli-proxy-api\nNode_1"]
        ha_p2["cli-proxy-api\nNode_2"]
        ha_shared["Shared_DB\n(PostgresStore)"]
        ha_lb --> ha_p1
        ha_lb --> ha_p2
        ha_p1 --> ha_shared
        ha_p2 --> ha_shared
    end
```

Sources: [cmd/server/main.go:179-210](), [docker-compose.yml:1-28](), [internal/store/postgresstore.go:37-46]()

---

## Choosing a Deployment Scenario

Use this table to select the appropriate sub-page based on your requirements.

| Requirement | Recommended Scenario |
|---|---|
| Personal use or single developer | [Single-Server Deployment](#10.1) |
| Running in AWS/GCP/Azure with managed DB | [Cloud-Native Deployment](#10.2) |
| Multiple users, high availability needed | [High Availability and Scaling](#10.3) |
| Need to share auth tokens across instances | [High Availability and Scaling](#10.3) |
| Simplest possible setup | [Single-Server Deployment](#10.1) |
| Using PostgreSQL or object storage | [Cloud-Native Deployment](#10.2) or [High Availability and Scaling](#10.3) |

External storage backends (covered in [Storage Backend Options](#5.2)) are the key enabler for both cloud-native and HA deployments. The system uses the `DEPLOY` environment variable and specific store-related env vars (like `PGSTORE_DSN`) to determine the storage provider at runtime.

Sources: [cmd/server/main.go:132-210](), [internal/store/postgresstore.go:49-100]()

---

# Page: Single-Server Deployment

# Single-Server Deployment

<details>
<summary>Relevant source files</summary>

The following files were used as context for generating this wiki page:

- [.dockerignore](.dockerignore)
- [.gitignore](.gitignore)
- [auths/.gitkeep](auths/.gitkeep)
- [cmd/server/main.go](cmd/server/main.go)
- [docker-build.ps1](docker-build.ps1)
- [docker-build.sh](docker-build.sh)
- [docker-compose.yml](docker-compose.yml)
- [go.mod](go.mod)
- [go.sum](go.sum)
- [internal/cmd/login.go](internal/cmd/login.go)
- [internal/cmd/run.go](internal/cmd/run.go)
- [internal/store/gitstore.go](internal/store/gitstore.go)
- [internal/store/postgresstore.go](internal/store/postgresstore.go)

</details>



## Purpose and Scope

This page covers deploying CLIProxyAPI on a single machine for local development, personal use, or small-team environments. It includes installation, configuration, systemd integration, and the use of the Terminal User Interface (TUI) for local management.

For containerized cloud deployments, see [Cloud-Native Deployment](). For multi-instance setups with shared storage, see [High Availability and Scaling]().

---

## Deployment Architecture

```mermaid
graph TB
    subgraph "Single_Server_Host"
        Binary["cliproxy binary<br/>cmd/server/main.go"]
        
        subgraph "Configuration_Space"
            ConfigYAML["config.yaml"]
            EnvVars[".env file<br/>godotenv.Load"]
        end
        
        subgraph "Token_Storage_Space"
            FileStore["FileTokenStore<br/>auths/*.json"]
            PGStore["PostgresStore<br/>internal/store/postgresstore.go"]
            GitStore["GitTokenStore<br/>internal/store/gitstore.go"]
        end
        
        subgraph "Runtime_Components"
            APIServer["API Server<br/>internal/api/server.go"]
            Builder["cliproxy.Builder<br/>sdk/cliproxy/builder.go"]
            Registry["Model Registry<br/>internal/registry"]
        end
        
        subgraph "Process_Management"
            Systemd["systemd service<br/>Optional"]
            Signals["signal.NotifyContext<br/>SIGINT/SIGTERM"]
        end
    end
    
    Binary --> ConfigYAML
    Binary --> EnvVars
    Binary --> PGStore
    Binary --> GitStore
    
    Binary --> Builder
    Builder --> APIServer
    Binary --> Registry
    
    Systemd -.->|manages| Binary
    Signals -.->|graceful_shutdown| Binary
```

**Single-Server Deployment Components**

The binary runs all components in a single process. On Linux, systemd is recommended for process supervision and automatic restarts.

**Sources:** [cmd/server/main.go:56-127](), [internal/cmd/run.go:19-56](), [internal/store/postgresstore.go:39-46](), [internal/store/gitstore.go:28-38]()

---

## Installation Methods

### Binary Download

Download the pre-built binary for your platform from the releases page. The binary is typically named `cli-proxy-api` or `cli-proxy-api.exe` [ .gitignore:1-3]().

```bash
# Linux/macOS
wget https://github.com/router-for-me/CLIProxyAPI/releases/latest/download/cli-proxy-api
chmod +x cli-proxy-api
sudo mv cli-proxy-api /usr/local/bin/cliproxy

# Verify installation
cliproxy --help
```

### Building from Source

The project uses Go 1.26.0 [go.mod:1-3]().

```bash
# Clone repository
git clone https://github.com/router-for-me/CLIProxyAPI.git
cd CLIProxyAPI

# Build binary
go build -o cliproxy ./cmd/server

# Install to system path
sudo mv cliproxy /usr/local/bin/
```

**Sources:** [cmd/server/main.go:1-4](), [go.mod:1-3](), [.gitignore:1-3]()

---

## Configuration Setup

### Minimal Configuration

The server looks for `config.yaml` by default [cmd/server/main.go:92](). Minimal settings include the port and the directory for authentication credentials.

| Field | Description | Default |
|-------|-------------|---------|
| `config` | Path to configuration file | `""` (checks current dir) |
| `auths/` | Default directory for credentials | `./auths` |
| `logs/` | Directory for logs | `./logs` |

**Sources:** [cmd/server/main.go:92-93](), [.gitignore:5-11](), [.gitignore:25-26]()

---

## Token Storage Options

The storage backend is determined by environment variables at startup. CLIProxyAPI supports multiple backends for persisting provider credentials.

```mermaid
graph LR
    Main["main.go<br/>Storage Selection"]
    
    EnvCheck{"LookupEnv<br/>Check"}
    
    FileStore["FileTokenStore<br/>Default /auths"]
    PGStore["PostgresStore<br/>PGSTORE_DSN"]
    GitStore["GitTokenStore<br/>GITSTORE_GIT_URL"]
    ObjStore["ObjectTokenStore<br/>OBJECTSTORE_ENDPOINT"]
    
    Main --> EnvCheck
    
    EnvCheck -->|"PGSTORE_DSN"| PGStore
    EnvCheck -->|"OBJECTSTORE_ENDPOINT"| ObjStore
    EnvCheck -->|"GITSTORE_GIT_URL"| GitStore
    EnvCheck -->|"None"| FileStore
    
    PGStore --> Register["sdkAuth.SetTokenStore"]
    FileStore --> Register
    GitStore --> Register
    ObjStore --> Register
```

**Token Storage Selection Logic**

- **File Storage (Default):** Stores credentials as JSON files in the `auths/` directory.
- **PostgreSQL Storage:** Activated by setting `PGSTORE_DSN`. It mirrors data to a local "spool" directory to ensure file-based workflows continue to operate [internal/store/postgresstore.go:37-38]().
- **Git Storage:** Activated by `GITSTORE_GIT_URL`. It persists tokens to a git repository, handling `clone`, `pull`, `commit`, and `push` operations automatically [internal/store/gitstore.go:27-28]().

**Sources:** [cmd/server/main.go:177-220](), [internal/store/postgresstore.go:49-100](), [internal/store/gitstore.go:92-213]()

---

## Running the Server

### Server Mode Execution

The `StartService` function in `internal/cmd/run.go` orchestrates the service lifecycle using a builder pattern from the `cliproxy` SDK [internal/cmd/run.go:19-27]().

```mermaid
sequenceDiagram
    participant User
    participant main.go
    participant Builder["cliproxy.NewBuilder"]
    participant Service["cliproxy.Service"]
    participant SignalCtx["signal.NotifyContext"]
    
    User->>main.go: Execute cliproxy
    main.go->>main.go: Load .env (godotenv)
    main.go->>main.go: Init Token Store
    main.go->>Builder: NewBuilder()
    Builder->>Builder: WithConfig(cfg)
    Builder->>Builder: WithConfigPath(path)
    main.go->>SignalCtx: Setup SIGINT/SIGTERM
    main.go->>Builder: Build()
    Builder->>Service: Create service instance
    main.go->>Service: Run(ctx)
    Service->>Service: Start Gin Engine
    
    alt Signal Received
        SignalCtx->>Service: Cancel context
        Service->>Service: Graceful shutdown
        Service->>main.go: Return
    end
```

**Service Startup Flow**

**Sources:** [internal/cmd/run.go:19-56](), [cmd/server/main.go:161-166](), [cmd/server/main.go:488-493]()

---

## Systemd Integration

For production-like single-server deployments on Linux, use a systemd unit file.

### Service Unit File Example
Create `/etc/systemd/system/cliproxy.service`:

```ini
[Unit]
Description=CLIProxyAPI Server
After=network.target

[Service]
Type=simple
User=cliproxy
WorkingDirectory=/var/lib/cliproxy
ExecStart=/usr/local/bin/cliproxy -config /etc/cliproxy/config.yaml
Restart=on-failure
# Optional: load env vars for storage backends
EnvironmentFile=-/etc/cliproxy/cliproxy.env

[Install]
WantedBy=multi-user.target
```

### Signal Handling
The application uses `signal.NotifyContext` to listen for `SIGINT` (Ctrl+C) and `SIGTERM` (Systemd stop) [internal/cmd/run.go:33-34](). This ensures that when systemd stops the service, it shuts down gracefully, closing active connections and flushing logs.

**Sources:** [internal/cmd/run.go:33-44]()

---

## TUI Mode for Local Management

CLIProxyAPI includes a built-in Terminal UI for managing the server.

```mermaid
graph TB
    subgraph "TUI_Standalone_Mode"
        MainBinary["main.go<br/>-tui -standalone"]
        
        subgraph "Embedded_Server"
            LocalServer["StartServiceBackground<br/>internal/cmd/run.go"]
            KeepAlive["WithKeepAliveEndpoint<br/>internal/cmd/run.go"]
        end
        
        subgraph "TUI_Client"
            TUIApp["TUI Application<br/>internal/tui/app.go"]
            LogHook["Log Hook<br/>internal/logging"]
        end
    end
    
    MainBinary --> LocalServer
    MainBinary --> TUIApp
    
    TUIApp -.->|"Management API"| LocalServer
    LogHook -.->|"captures logs"| LocalServer
```

**TUI Standalone Architecture**

### Standalone Mode
Running `cliproxy -tui -standalone` starts an embedded server in a background goroutine and opens the TUI as the primary interface [cmd/server/main.go:95-96]().

- **Keep-Alive:** In standalone mode, if a `localPassword` is provided, the server uses a keep-alive endpoint. If the management client is idle for 10 seconds, the server shuts down automatically [internal/cmd/run.go:37-44]().
- **Background Startup:** Uses `StartServiceBackground` to run the proxy without blocking the main thread [internal/cmd/run.go:60-84]().

**Sources:** [cmd/server/main.go:95-96](), [internal/cmd/run.go:37-44](), [internal/cmd/run.go:60-84]()

---

## Local Development Setup

For developers extending the codebase on a single machine:

1. **Environment:** Use a `.env` file for local overrides. `godotenv` loads this from the working directory [cmd/server/main.go:161-166]().
2. **Docker Compose:** A `docker-compose.yml` is provided for local containerized testing, mounting `config.yaml` and `auths/` as volumes [docker-compose.yml:24-27]().
3. **Build Scripts:** Use `docker-build.sh` (Linux/macOS) or `docker-build.ps1` (Windows) to build from source with correct version metadata [docker-build.sh:138-160](), [docker-build.ps1:23-41]().
4. **Usage Stats:** The `docker-build.sh` script includes a feature to preserve usage statistics across rebuilds using the `/v0/management/usage/export` and `import` endpoints [docker-build.sh:61-96]().

**Sources:** [cmd/server/main.go:161-166](), [docker-compose.yml:24-27](), [docker-build.sh:61-96](), [docker-build.ps1:23-41]()

---

# Page: Cloud-Native Deployment

# Cloud-Native Deployment

<details>
<summary>Relevant source files</summary>

The following files were used as context for generating this wiki page:

- [.dockerignore](.dockerignore)
- [.github/workflows/docker-image.yml](.github/workflows/docker-image.yml)
- [.github/workflows/pr-test-build.yml](.github/workflows/pr-test-build.yml)
- [.github/workflows/release.yaml](.github/workflows/release.yaml)
- [.gitignore](.gitignore)
- [.goreleaser.yml](.goreleaser.yml)
- [Dockerfile](Dockerfile)
- [LICENSE](LICENSE)
- [auths/.gitkeep](auths/.gitkeep)
- [cmd/server/main.go](cmd/server/main.go)
- [docker-build.ps1](docker-build.ps1)
- [docker-build.sh](docker-build.sh)
- [docker-compose.yml](docker-compose.yml)
- [go.mod](go.mod)
- [go.sum](go.sum)
- [internal/store/gitstore.go](internal/store/gitstore.go)
- [internal/store/postgresstore.go](internal/store/postgresstore.go)

</details>



## Overview

This page covers deploying CLIProxyAPI in containerized cloud environments. Cloud-native deployment involves running the proxy in containers (Docker, Kubernetes) with externalized configuration and state, enabling horizontal scaling, zero-downtime updates, and infrastructure-as-code workflows.

Key topics covered:
- **Container deployment** with Docker and Docker Compose
- **`DEPLOY=cloud` mode** for dynamic configuration provisioning
- **External storage backends** (PostgreSQL, Git, S3-compatible object storage)
- **CI/CD and Build Metadata** for automated image generation
- **Operational considerations** for cloud environments

Related pages:
- [10.1 Single-Server Deployment]() — systemd services and local development
- [10.3 High Availability and Scaling]() — load balancing and multi-instance coordination
- [5.2 Storage Backend Options]() — detailed comparison of token storage implementations
- [5.3 Environment Variables and Overrides]() — complete environment variable reference

---

## Container Deployment Basics

CLIProxyAPI is distributed as a Docker image and can run in any OCI-compatible container runtime. The official image is built using a multi-stage `Dockerfile` and is available at `eceasy/cli-proxy-api`. [Dockerfile:1-35](), [.github/workflows/docker-image.yml:10-11]()

### Standard Container Launch

Basic container execution without external storage:

```bash
docker run -d \
  -p 8317:8317 \
  -v $(pwd)/config.yaml:/CLIProxyAPI/config.yaml \
  -v $(pwd)/auths:/root/.cli-proxy-api \
  -v $(pwd)/logs:/CLIProxyAPI/logs \
  eceasy/cli-proxy-api:latest
```

This mounts local configuration and auth directories into the container. The container writes logs to the mounted volume and reads config from the host filesystem. [Dockerfile:21-35](), [docker-compose.yml:24-27]()

### Docker Compose

The repository includes a `docker-compose.yml` that configures the service with volume mounts and environment variable pass-through. It supports variable overrides for image tags and local paths. [docker-compose.yml:1-29]()

```yaml
services:
  cli-proxy-api:
    image: ${CLI_PROXY_IMAGE:-eceasy/cli-proxy-api:latest}
    container_name: cli-proxy-api
    restart: unless-stopped
    ports:
      - "8317:8317"
    volumes:
      - ${CLI_PROXY_CONFIG_PATH:-./config.yaml}:/CLIProxyAPI/config.yaml
      - ${CLI_PROXY_AUTH_PATH:-./auths}:/root/.cli-proxy-api
      - ${CLI_PROXY_LOG_PATH:-./logs}:/CLIProxyAPI/logs
    environment:
      DEPLOY: ${DEPLOY:-}
```

Sources: [Dockerfile:1-35](), [docker-compose.yml:1-29]()

---

## Cloud Deploy Mode

Setting `DEPLOY=cloud` in the environment changes startup behavior. When this mode is active and no valid `config.yaml` is found (either locally or via the configured remote store), the server does not exit. Instead, it calls `cmd.WaitForCloudDeploy()` and blocks until an OS shutdown signal is received. [cmd/server/main.go:132-133](), [cmd/server/main.go:486-503]()

**Cloud Deploy Mode Startup Flow**

```mermaid
flowchart TD
    A["main()"] --> B{"DEPLOY == \"cloud\"?"}
    B -->|"No"| C["Normal startup path"]
    B -->|"Yes"| D["isCloudDeploy = true"]
    D --> E["Load config via active store backend"]
    E --> F{"Config file exists\nAND cfg.Port != 0?"}
    F -->|"No"| G["log: standing by for configuration\nconfigFileExists = false"]
    G --> H["cmd.WaitForCloudDeploy()\nblock on OS signal"]
    F -->|"Yes"| I["log: starting service\nconfigFileExists = true"]
    I --> J["managementasset.StartAutoUpdater()"]
    J --> K["cmd.StartService(cfg, configFilePath, password)"]
```

Sources: [cmd/server/main.go:486-570]()

The validity check considers the config file missing if:
- The file path does not exist on disk.
- The path points to a directory.
- The file exists but `cfg.Port == 0` (file is empty or unparseable). [cmd/server/main.go:490-498]()

---

## Storage Backend Selection

Exactly one token store is active at runtime. The startup code in `main()` checks environment variables in a fixed priority order and registers the selected store with `sdkAuth.RegisterTokenStore()`. Setting `PGSTORE_DSN` also sets `useGitStore = false` explicitly. [cmd/server/main.go:179-198]()

**Storage Backend Selection — Code-Level View**

```mermaid
flowchart TD
    entry["main(): lookupEnv()"] --> pgcheck{"PGSTORE_DSN set?"}
    pgcheck -->|"Yes"| pgset["usePostgresStore = true\nuseGitStore = false"]
    pgset --> pginit["store.NewPostgresStore(ctx, PostgresStoreConfig)\npgStoreInst.Bootstrap(ctx, examplePath)\nsdkAuth.RegisterTokenStore(pgStoreInst)"]
    pgcheck -->|"No"| objcheck{"OBJECTSTORE_ENDPOINT set?"}
    objcheck -->|"Yes"| objset["useObjectStore = true"]
    objset --> objinit["store.NewObjectTokenStore(ObjectStoreConfig)\nobjectStoreInst.Bootstrap(ctx, examplePath)\nsdkAuth.RegisterTokenStore(objStoreInst)"]
    objcheck -->|"No"| gitcheck{"GITSTORE_GIT_URL set?"}
    gitcheck -->|"Yes"| gitset["useGitStore = true"]
    gitset --> gitinit["store.NewGitTokenStore(url, user, password)\ngitStoreInst.EnsureRepository()\nsdkAuth.RegisterTokenStore(gitStoreInst)"]
    gitcheck -->|"No"| local["sdkAuth.RegisterTokenStore(\n  sdkAuth.NewFileTokenStore())"]
```

Sources: [cmd/server/main.go:179-453]()

| Priority | Activated by | Type |
|---|---|---|
| 1 (highest) | `PGSTORE_DSN` | `*store.PostgresStore` |
| 2 | `OBJECTSTORE_ENDPOINT` | `*store.ObjectTokenStore` |
| 3 | `GITSTORE_GIT_URL` | `*store.GitTokenStore` |
| 4 (default) | *(none)* | `sdkAuth.FileTokenStore` |

---

## PostgreSQL Backend

`PostgresStore` stores configuration YAML and auth tokens in database tables while mirroring everything to a local spool directory so the rest of the application can use standard file-based workflows. [internal/store/postgresstore.go:39-46]()

### Environment Variables

| Variable | Alias | Required | Description |
|---|---|---|---|
| `PGSTORE_DSN` | `pgstore_dsn` | Yes | PostgreSQL connection string |
| `PGSTORE_SCHEMA` | `pgstore_schema` | No | Database schema (defaults to `public`) |
| `PGSTORE_LOCAL_PATH` | `pgstore_local_path` | No | Root for local spool |

Sources: [cmd/server/main.go:179-198](), [internal/store/postgresstore.go:29-35]()

### Initialization Sequence

**`PostgresStore` Bootstrap Sequence**

```mermaid
sequenceDiagram
    participant M as "main()"
    participant PS as "PostgresStore"
    participant DB as "PostgreSQL"
    participant FS as "pgstore/ (spool)"

    M->>PS: "NewPostgresStore(ctx, PostgresStoreConfig)"
    PS->>DB: "sql.Open(pgx DSN) + PingContext()"
    M->>PS: "Bootstrap(ctx, config.example.yaml)"
    PS->>PS: "EnsureSchema()"
    PS->>DB: "CREATE TABLE IF NOT EXISTS config_store"
    PS->>DB: "CREATE TABLE IF NOT EXISTS auth_store"
    PS->>PS: "syncConfigFromDatabase()"
    PS->>DB: "SELECT content FROM config_store WHERE id='config'"
    alt "Row found"
        DB-->>PS: "config YAML string"
        PS->>FS: "WriteFile(configPath, content)"
    else "Not found"
        PS->>FS: "CopyConfigTemplate(examplePath, configPath)"
        PS->>DB: "INSERT INTO config_store (id, content)"
    end
    PS->>PS: "syncAuthFromDatabase()"
    PS->>DB: "SELECT id, content FROM auth_store"
    loop "each row"
        DB-->>PS: "auth id + JSON"
        PS->>FS: "WriteFile(authDir/id, json)"
    end
```

Sources: [internal/store/postgresstore.go:111-158](), [cmd/server/main.go:394-416]()

---

## Git Backend

`GitTokenStore` uses a remote Git repository to persist config and auth files. On every token save, the file is committed and pushed to the remote. [internal/store/gitstore.go:1-50]()

### Environment Variables

| Variable | Alias | Required | Description |
|---|---|---|---|
| `GITSTORE_GIT_URL` | `gitstore_git_url` | Yes | Remote repository URL |
| `GITSTORE_GIT_USERNAME` | `gitstore_git_username` | No | Git username |
| `GITSTORE_GIT_TOKEN` | `gitstore_git_token` | No | Personal access token |
| `GITSTORE_LOCAL_PATH` | `gitstore_local_path` | No | Local clone root |

Sources: [cmd/server/main.go:199-225]()

### Repository Layout

The store maintains a specific structure in the remote repository:
```
{GITSTORE_LOCAL_PATH}/gitstore/
├── .git/
├── auths/
│   ├── .gitkeep
│   └── *.json               ← one file per auth credential
└── config/
    ├── .gitkeep
    └── config.yaml
```

Sources: [cmd/server/main.go:214-220](), [internal/store/gitstore.go:1-50]()

---

## Object Storage Backend

`ObjectTokenStore` uses any S3-compatible service. Configuration and auth tokens are stored as objects in a single bucket. [cmd/server/main.go:275-303]()

### Environment Variables

| Variable | Alias | Required | Description |
|---|---|---|---|
| `OBJECTSTORE_ENDPOINT` | `objectstore_endpoint` | Yes | S3 endpoint URL |
| `OBJECTSTORE_ACCESS_KEY` | `objectstore_access_key` | Yes | Access key ID |
| `OBJECTSTORE_SECRET_KEY` | `objectstore_secret_key` | Yes | Secret access key |
| `OBJECTSTORE_BUCKET` | `objectstore_bucket` | Yes | Bucket name |

Sources: [cmd/server/main.go:275-303]()

### Initialization Sequence

**`ObjectTokenStore` Bootstrap Sequence**

```mermaid
sequenceDiagram
    participant M as "main()"
    participant OT as "ObjectTokenStore"
    participant S3 as "S3 Bucket"
    participant FS as "objectstore/ (mirror)"

    M->>OT: "NewObjectTokenStore(ObjectStoreConfig)"
    OT->>OT: "minio.New(endpoint, options)"
    M->>OT: "Bootstrap(ctx, config.example.yaml)"
    OT->>S3: "BucketExists(bucket)"
    alt "Bucket missing"
        OT->>S3: "MakeBucket(bucket)"
    end
    OT->>OT: "syncConfigFromBucket()"
    OT->>S3: "StatObject(config/config.yaml)"
    alt "Object found"
        OT->>S3: "GetObject(config/config.yaml)"
        OT->>FS: "WriteFile(configPath, bytes)"
    else "Not found"
        OT->>FS: "CopyConfigTemplate(examplePath, configPath)"
        OT->>S3: "PutObject(config/config.yaml, data)"
    end
    OT->>OT: "syncAuthFromBucket()"
    OT->>S3: "ListObjects(auths/)"
    loop "each object"
        OT->>S3: "GetObject(key)"
        OT->>FS: "WriteFile(authDir/rel, bytes)"
    end
```

Sources: [cmd/server/main.go:440-453]()

---

## CI/CD and Build Metadata

The project uses GitHub Actions and GoReleaser to produce container images with embedded build metadata. This metadata is injected via `-ldflags` during the build process and is used by the `buildinfo` package. [Dockerfile:11-15](), [.goreleaser.yml:17-18]()

### Versioning Logic

The version information is printed on startup:
```go
fmt.Printf("CLIProxyAPI Version: %s, Commit: %s, BuiltAt: %s\n", buildinfo.Version, buildinfo.Commit, buildinfo.BuildDate)
```
[cmd/server/main.go:57]()

### GitHub Actions Workflow

1. **Refresh models catalog**: Fetches the latest `models.json` from the remote repository before building. [.github/workflows/docker-image.yml:19-21]()
2. **Build and push**: Builds for `linux/amd64` and `linux/arm64`. [.github/workflows/docker-image.yml:34-81]()
3. **Multi-arch manifest**: Creates a combined manifest for the `latest` and version tags. [.github/workflows/docker-image.yml:105-112]()

Sources: [.github/workflows/docker-image.yml:1-148](), [.goreleaser.yml:1-43](), [cmd/server/main.go:38-57]()

---

## Local Spool Directories

Each remote backend maintains a local mirror on disk. The application's file-based internals operate against these mirrored paths.

| Backend | Spool root | Config file | Auth directory |
|---|---|---|---|
| PostgreSQL | `{PGSTORE_LOCAL_PATH}/pgstore/` | `pgstore/config/config.yaml` | `pgstore/auths/` |
| Git | `{GITSTORE_LOCAL_PATH}/gitstore/` | `gitstore/config/config.yaml` | `gitstore/auths/` |
| Object Storage | `{OBJECTSTORE_LOCAL_PATH}/objectstore/` | `objectstore/config/config.yaml` | `objectstore/auths/` |

If the `*_LOCAL_PATH` variable is not set, the fallback is the path returned by `util.WritablePath()`, or the current working directory if that is also unavailable. [cmd/server/main.go:178-225](), [internal/store/postgresstore.go:62-69]()

Sources: [cmd/server/main.go:178-225](), [internal/store/postgresstore.go:62-81]()

---

# Page: High Availability and Scaling

# High Availability and Scaling

<details>
<summary>Relevant source files</summary>

The following files were used as context for generating this wiki page:

- [.env.example](.env.example)
- [cmd/server/main.go](cmd/server/main.go)
- [go.mod](go.mod)
- [go.sum](go.sum)
- [internal/store/gitstore.go](internal/store/gitstore.go)
- [internal/store/objectstore.go](internal/store/objectstore.go)
- [internal/store/postgresstore.go](internal/store/postgresstore.go)
- [sdk/cliproxy/auth/scheduler.go](sdk/cliproxy/auth/scheduler.go)
- [sdk/cliproxy/auth/scheduler_benchmark_test.go](sdk/cliproxy/auth/scheduler_benchmark_test.go)
- [sdk/cliproxy/auth/scheduler_test.go](sdk/cliproxy/auth/scheduler_test.go)

</details>



This page explains how to deploy CLIProxyAPI in high-availability configurations with multiple instances to achieve horizontal scalability, load distribution, and fault tolerance. It covers shared storage backends (Postgres, Git, Object Store), load balancing requirements, and operational best practices for multi-instance deployments.

---

## Architecture Overview

CLIProxyAPI's architecture separates stateless request processing from stateful credential management. The system supports multiple concurrent instances when configured with shared storage backends.

### Stateless and Stateful Components

The following diagram maps high-level system components to their corresponding code entities to illustrate data flow in a multi-instance setup.

**System to Code Entity Map**

```mermaid
graph TB
    subgraph "Load_Balancer_Layer"
        LB["Load Balancer"]
    end
    
    subgraph "CLIProxyAPI_Instance"
        Server["HTTP Server<br/>cmd/server/main.go"]
        Manager["Auth Manager<br/>sdk/cliproxy/auth/conductor.go"]
        Scheduler["Auth Scheduler<br/>sdk/cliproxy/auth/scheduler.go"]
    end
    
    subgraph "Shared_Storage_Backends"
        PG["PostgresStore<br/>internal/store/postgresstore.go"]
        GitStore["GitTokenStore<br/>internal/store/gitstore.go"]
        ObjStore["ObjectTokenStore<br/>internal/store/objectstore.go"]
    end
    
    LB --> Server
    Server --> Manager
    Manager --> Scheduler
    Manager --> PG
    Manager --> GitStore
    Manager --> ObjStore
```
**Sources:** [cmd/server/main.go:133-153](), [sdk/cliproxy/auth/scheduler.go:34-40](), [internal/store/postgresstore.go:39-46]()

**Stateless Components:**
- **Request Handling:** Handled by the Gin-based server initialized in `main` [cmd/server/main.go:56-127]().
- **Scheduling Logic:** The `authScheduler` maintains local ready/blocked states but derives them from shared auth data via `rebuild` or `upsertAuth` calls [sdk/cliproxy/auth/scheduler.go:134-157]().

**Stateful Components:**
- **Credential Storage:** Managed by the `Store` interface implementations such as `PostgresStore`, `GitTokenStore`, or `ObjectTokenStore` [internal/store/postgresstore.go:39-46](), [internal/store/gitstore.go:28-38](), [internal/store/objectstore.go:45-52]().
- **OAuth Tokens:** Refreshed and persisted via the `Save` method in the respective store implementations [internal/store/postgresstore.go:189-237](), [internal/store/gitstore.go:216-225]().

---

## Shared Storage Backends

Multi-instance deployments require a shared store to synchronize `Auth` states (tokens, quotas, and model availability) across the cluster.

### PostgresStore
The `PostgresStore` provides ACID guarantees and is the recommended backend for high-concurrency production environments. It is enabled via the `PGSTORE_DSN` environment variable [cmd/server/main.go:179-182]().

- **Implementation:** Uses the `pgx` driver to manage `auth_store` and `config_store` tables [internal/store/postgresstore.go:16-24]().
- **Mirroring:** It mirrors database content to a local "spool" directory to maintain compatibility with file-based workflows [internal/store/postgresstore.go:39-44]().
- **Schema Management:** `EnsureSchema` creates the necessary tables automatically [internal/store/postgresstore.go:111-144]().

**Data Flow: Auth Persistence**
```mermaid
sequenceDiagram
    participant M as "Manager (sdk/cliproxy/auth/conductor.go)"
    participant S as "PostgresStore (internal/store/postgresstore.go)"
    participant DB as "PostgreSQL"
    participant FS as "Local Spool (auths/)"

    M->>S: Save(ctx, auth)
    S->>FS: Write JSON/Token to file
    S->>DB: UPSERT INTO auth_table (id, content)
    DB-->>S: OK
    S-->>M: Path to mirrored file
```
**Sources:** [internal/store/postgresstore.go:189-237](), [cmd/server/main.go:179-198]()

### GitStore and ObjectStore
- **GitTokenStore:** Persists tokens to a Git repository using `go-git`. It handles cloning, pulling, and pushing changes to a remote URL defined by `GITSTORE_GIT_URL` [internal/store/gitstore.go:92-213](), [cmd/server/main.go:199-202]().
- **ObjectTokenStore:** Persists tokens to S3-compatible storage using the MinIO SDK. It is enabled via `OBJECTSTORE_ENDPOINT` and related variables [internal/store/objectstore.go:55-118](), [cmd/server/main.go:222-225]().

---

## Scaling the Auth Scheduler

The `authScheduler` is responsible for selecting the best credential for a request based on priority and health.

### Scheduler Sharding and Strategy
The scheduler organizes auths into `providerScheduler` and `modelScheduler` shards [sdk/cliproxy/auth/scheduler.go:43-66](). It supports different strategies based on the configured `Selector`:
- **Round-Robin:** Distributed via `RoundRobinSelector` [sdk/cliproxy/auth/scheduler.go:19-21]().
- **Fill-First:** Prioritizes credentials until exhausted, implemented via `FillFirstSelector` [sdk/cliproxy/auth/scheduler.go:20-21]().

**Code Entity: Scheduler Structure**
```mermaid
classDiagram
    class authScheduler {
        +strategy schedulerStrategy
        +providers map[string]providerScheduler
        +pickSingle(ctx, provider, model)
    }
    class providerScheduler {
        +auths map[string]scheduledAuthMeta
        +modelShards map[string]modelScheduler
    }
    class modelScheduler {
        +entries map[string]scheduledAuth
        +readyByPriority map[int]readyBucket
        +blocked cooldownQueue
    }
    authScheduler *-- providerScheduler
    providerScheduler *-- modelScheduler
```
**Sources:** [sdk/cliproxy/auth/scheduler.go:34-66]()

### Priority and Virtual Parents
The scheduler supports advanced routing logic for scaling:
- **Priority:** Auths with higher `priority` attributes (parsed from `Auth.Attributes`) are placed in higher priority buckets and picked first [sdk/cliproxy/auth/scheduler.go:49-57](), [sdk/cliproxy/auth/scheduler_test.go:73-81]().
- **Gemini Virtual Parents:** Groups multiple project-based credentials under a single `gemini_virtual_parent` attribute to ensure fair rotation across accounts rather than just projects [sdk/cliproxy/auth/scheduler.go:82-95](), [sdk/cliproxy/auth/scheduler_test.go:154-183]().

---

## Performance and Benchmarking

The scheduler is designed for high-throughput environments. Benchmarks show efficient selection even with hundreds of credentials.

| Scenario | Operation | Scale | Implementation |
| :--- | :--- | :--- | :--- |
| **Single Provider** | `pickNext` | 1000 Auths | `BenchmarkManagerPickNext1000` |
| **Mixed Provider** | `pickNextMixed` | 500 Auths | `BenchmarkManagerPickNextMixed500` |
| **Priority Routing**| `pickNext` | 500 Auths | `BenchmarkManagerPickNextPriority500` |

**Sources:** [sdk/cliproxy/auth/scheduler_benchmark_test.go:84-177]()

---

## Failover and Cooldown Logic

High availability is further enhanced by the system's ability to fail over between credentials.

### Cooldown Management
When a credential fails (e.g., due to rate limits), it is moved to a `scheduledStateCooldown` state [sdk/cliproxy/auth/scheduler.go:28]().
- **Cooldown Queue:** Blocked auths are stored in a `cooldownQueue` ordered by their `nextRetryAt` time [sdk/cliproxy/auth/scheduler.go:97-98]().
- **Automatic Promotion:** The scheduler checks for expired cooldowns before each pick operation to reintegrate recovered credentials [sdk/cliproxy/auth/scheduler_test.go:122-152]().

### WebSocket Preference
For providers like Codex, the scheduler can be instructed to prefer credentials with `websockets: "true"` attributes when the downstream request is a WebSocket connection [sdk/cliproxy/auth/scheduler.go:181-182](), [sdk/cliproxy/auth/scheduler_test.go:185-200]().

**Sources:** [sdk/cliproxy/auth/scheduler.go:23-31](), [sdk/cliproxy/auth/scheduler.go:60-74](), [sdk/cliproxy/auth/scheduler_test.go:122-152]()

---

# Page: Glossary

# Glossary

<details>
<summary>Relevant source files</summary>

The following files were used as context for generating this wiki page:

- [README.md](README.md)
- [README_CN.md](README_CN.md)
- [README_JA.md](README_JA.md)
- [assets/bmoplus.png](assets/bmoplus.png)
- [assets/lingtrue.png](assets/lingtrue.png)
- [config.example.yaml](config.example.yaml)
- [internal/api/handlers/management/config_basic.go](internal/api/handlers/management/config_basic.go)
- [internal/api/handlers/management/config_lists.go](internal/api/handlers/management/config_lists.go)
- [internal/api/server.go](internal/api/server.go)
- [internal/cache/signature_cache.go](internal/cache/signature_cache.go)
- [internal/cache/signature_cache_test.go](internal/cache/signature_cache_test.go)
- [internal/config/config.go](internal/config/config.go)
- [internal/registry/model_definitions.go](internal/registry/model_definitions.go)
- [internal/registry/model_registry.go](internal/registry/model_registry.go)
- [internal/registry/model_registry_cache_test.go](internal/registry/model_registry_cache_test.go)
- [internal/registry/model_registry_hook_test.go](internal/registry/model_registry_hook_test.go)
- [internal/registry/model_registry_safety_test.go](internal/registry/model_registry_safety_test.go)
- [internal/runtime/executor/aistudio_executor.go](internal/runtime/executor/aistudio_executor.go)
- [internal/runtime/executor/antigravity_executor.go](internal/runtime/executor/antigravity_executor.go)
- [internal/runtime/executor/claude_executor.go](internal/runtime/executor/claude_executor.go)
- [internal/runtime/executor/codex_executor.go](internal/runtime/executor/codex_executor.go)
- [internal/runtime/executor/gemini_cli_executor.go](internal/runtime/executor/gemini_cli_executor.go)
- [internal/runtime/executor/gemini_executor.go](internal/runtime/executor/gemini_executor.go)
- [internal/runtime/executor/gemini_vertex_executor.go](internal/runtime/executor/gemini_vertex_executor.go)
- [internal/runtime/executor/iflow_executor.go](internal/runtime/executor/iflow_executor.go)
- [internal/runtime/executor/openai_compat_executor.go](internal/runtime/executor/openai_compat_executor.go)
- [internal/runtime/executor/qwen_executor.go](internal/runtime/executor/qwen_executor.go)
- [internal/thinking/apply_user_defined_test.go](internal/thinking/apply_user_defined_test.go)
- [internal/translator/antigravity/claude/antigravity_claude_request.go](internal/translator/antigravity/claude/antigravity_claude_request.go)
- [internal/translator/antigravity/claude/antigravity_claude_request_test.go](internal/translator/antigravity/claude/antigravity_claude_request_test.go)
- [internal/translator/antigravity/claude/antigravity_claude_response.go](internal/translator/antigravity/claude/antigravity_claude_response.go)
- [internal/translator/antigravity/claude/antigravity_claude_response_test.go](internal/translator/antigravity/claude/antigravity_claude_response_test.go)
- [internal/watcher/watcher.go](internal/watcher/watcher.go)
- [sdk/api/handlers/handlers.go](sdk/api/handlers/handlers.go)
- [sdk/cliproxy/auth/conductor.go](sdk/cliproxy/auth/conductor.go)
- [sdk/cliproxy/auth/conductor_overrides_test.go](sdk/cliproxy/auth/conductor_overrides_test.go)
- [sdk/cliproxy/auth/openai_compat_pool_test.go](sdk/cliproxy/auth/openai_compat_pool_test.go)
- [sdk/cliproxy/model_registry.go](sdk/cliproxy/model_registry.go)
- [sdk/cliproxy/service.go](sdk/cliproxy/service.go)
- [test/amp_management_test.go](test/amp_management_test.go)

</details>



This page provides definitions for codebase-specific terms, jargon, and abbreviations used throughout the CLIProxyAPI project. It serves as a technical reference for onboarding engineers to understand the conceptual mapping between system logic and code implementation.

## Core System Concepts

### Access Manager vs. Core Manager
The system employs a dual-layered management architecture to separate request authentication from provider credential execution.

*   **Access Manager (`sdkaccess.Manager`)**: Responsible for authenticating incoming client requests to the proxy itself. It validates the API keys or tokens provided by the user in the `Authorization` header against the configured `api-keys` in `config.yaml`.
    *   Defined in: [internal/api/server.go:139-140]()
*   **Core Manager (`coreauth.Manager`)**: Orchestrates the lifecycle of upstream AI provider credentials (e.g., Gemini OAuth tokens, Claude API keys). It handles selection, rotation, and execution of requests.
    *   Defined in: [sdk/cliproxy/auth/conductor.go:129-160]()

### Executor
A stateless component that implements the `ProviderExecutor` interface. Each executor is dedicated to a specific AI provider (e.g., `Antigravity`, `Claude`, `Codex`) and handles the low-level details of request preparation, credential injection, and network execution.

*   **Key Interface**: `ProviderExecutor` [sdk/cliproxy/auth/conductor.go:28-43]()
*   **Implementations**: 
    *   `AntigravityExecutor`: [internal/runtime/executor/antigravity_executor.go:59-61]()
    *   `ClaudeExecutor`: [internal/runtime/executor/claude_executor.go:39-41]()
    *   `CodexExecutor`: [internal/runtime/executor/codex_executor.go:39-41]()

### Selector
A strategy pattern implementation used by the `CoreManager` to pick an available `Auth` (credential) from a pool when multiple credentials satisfy a request's requirements (e.g., same provider and model).

*   **RoundRobinSelector**: Cycles through credentials to distribute load. [sdk/cliproxy/auth/conductor.go:171-171]()
*   **FillFirstSelector**: Uses the first available credential until it hits a quota/cooldown before moving to the next. [sdk/cliproxy/auth/conductor.go:195-195]()

---

## Technical Jargon & Abbreviations

| Term | Definition | Code Reference |
| :--- | :--- | :--- |
| **Auth** | A struct representing a single upstream credential (OAuth token, API key, etc.) and its metadata (status, attributes). | [sdk/cliproxy/auth/conductor.go:237-246]() |
| **Channel** | A string identifier for a provider type used in model lookups (e.g., `claude`, `gemini-cli`, `antigravity`). | [internal/registry/model_definitions.go:103-143]() |
| **Cloaking** | The process of injecting system prompts, faking user IDs, or obfuscating sensitive words to make proxy traffic appear like official client traffic. | [internal/runtime/executor/claude_executor.go:131-131]() |
| **Cooldown** | A state where a credential is temporarily disabled due to rate limits (429) or quota exhaustion. | [internal/config/config.go:68-69]() |
| **Thinking** | Refers to "Chain of Thought" or reasoning blocks in models like Claude 3.7 or Gemini. The system manages signatures and budgets for these blocks. | [internal/config/config.go:127-127]() |

---

## Data Flow: Request Translation
The following diagram illustrates how a request from a "Natural Language Space" (a user calling an OpenAI-compatible endpoint) is transformed into "Code Entity Space" (specific provider payloads).

### Request Transformation Flow
```mermaid
graph TD
    A["Client Request (OpenAI Format)"] -- "POST /v1/chat/completions" --> B["api.Server"]
    B -- "Identify Source Format" --> C["sdktranslator.TranslateRequest"]
    C -- "Target: Antigravity" --> D["claude.ConvertClaudeRequestToAntigravity"]
    D -- "Inject Thinking" --> E["thinking.ApplyThinking"]
    E -- "Execute" --> F["AntigravityExecutor.Execute"]
    F -- "Upstream" --> G["cloudcode-pa.googleapis.com"]

    subgraph "Translation Registry"
    D
    E
    end
```
**Sources:** [internal/api/server.go:122-179](), [internal/translator/antigravity/claude/antigravity_claude_request.go:38-67](), [internal/runtime/executor/antigravity_executor.go:187-200]()

---

## System Lifecycle: Hot Reloading
The `Watcher` component monitors the filesystem for changes to `config.yaml` or files in the `auth-dir`. When a change is detected, it triggers a "Hot Reload" where the `Server` and `CoreManager` update their internal state without a restart.

### Watcher and Config Update Logic
```mermaid
graph LR
    subgraph "Filesystem"
    Config["config.yaml"]
    AuthFiles["~/.cli-proxy-api/*"]
    end

    subgraph "watcher.Watcher"
    FSNotify["fsnotify.Watcher"]
    Debounce["configReloadDebounce (150ms)"]
    end

    subgraph "cliproxy.Service"
    ReloadCB["reloadCallback"]
    UpdateAuth["handleAuthUpdate"]
    end

    Config -- "Event" --> FSNotify
    AuthFiles -- "Event" --> FSNotify
    FSNotify --> Debounce
    Debounce -- "Trigger" --> ReloadCB
    Debounce -- "Update Queue" --> UpdateAuth
```
**Sources:** [internal/watcher/watcher.go:80-87](), [internal/watcher/watcher.go:90-117](), [sdk/cliproxy/service.go:174-202]()

---

## Model Registry Terms

*   **ModelInfo**: A struct containing metadata for a specific model, including its ID, token limits, and capabilities (e.g., whether it supports "thinking").
    *   Defined in: [internal/registry/model_definitions.go:10-24]()
*   **Model Mapping**: The logic that translates a client-requested model name (alias) to the actual upstream model ID supported by the provider.
    *   Logic in: [internal/config/config.go:112-113]()
*   **Thinking Signature**: A cryptographic token required by certain Google/Antigravity APIs to validate reasoning blocks. The proxy caches these to enable multi-turn conversations.
    *   Cache implementation: [internal/cache/signature_cache.go:1-30]()

### Model Lookup Diagram
```mermaid
graph TD
    Req["Request Model ID"] --> Alias["OAuthModelAlias Check"]
    Alias -- "Found" --> Upstream["Upstream Model Name"]
    Alias -- "Not Found" --> Registry["registry.LookupStaticModelInfo"]
    Registry --> Meta["ModelInfo (ID, Capabilities, etc.)"]
    Upstream --> Registry
```
**Sources:** [internal/registry/model_definitions.go:147-174](), [internal/config/config.go:118-124](), [sdk/cliproxy/auth/conductor.go:146-147]()

---

## Infrastructure Terms

*   **Commercial Mode**: A configuration flag that disables high-overhead middleware (like extensive request logging) to minimize memory usage in high-concurrency environments.
    *   Config: [internal/config/config.go:52-52]()
*   **Websocket Gateway**: A component (`wsrelay.Manager`) that manages persistent connections for providers that use WebSockets, such as AI Studio.
    *   Defined in: [sdk/cliproxy/service.go:204-220]()
*   **Usage Reporter**: An internal utility used by executors to track token consumption and success/failure rates per credential.
    *   Usage in Claude: [internal/runtime/executor/claude_executor.go:109-110]()
    *   Usage in Codex: [internal/runtime/executor/codex_executor.go:91-92]()

**Sources:** [internal/config/config.go:1-130](), [sdk/cliproxy/service.go:1-92](), [internal/runtime/executor/antigravity_executor.go:1-72](), [internal/registry/model_definitions.go:1-175]()