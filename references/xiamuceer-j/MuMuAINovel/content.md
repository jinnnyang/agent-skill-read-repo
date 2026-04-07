# Page: Overview

# Overview

<details>
<summary>Relevant source files</summary>

The following files were used as context for generating this wiki page:

- [README.md](README.md)
- [backend/.env.example](backend/.env.example)
- [frontend/package-lock.json](frontend/package-lock.json)
- [frontend/package.json](frontend/package.json)
- [frontend/src/pages/ProjectList.tsx](frontend/src/pages/ProjectList.tsx)
- [images/1-1.png](images/1-1.png)
- [images/1.png](images/1.png)
- [images/2-1.png](images/2-1.png)
- [images/2.png](images/2.png)
- [images/3-1.png](images/3-1.png)
- [images/3.png](images/3.png)
- [images/4-1.png](images/4-1.png)
- [images/4.png](images/4.png)

</details>



## Purpose and Scope

This document provides a high-level introduction to the MuMuAINovel system, covering its purpose, core capabilities, and architectural foundations. It serves as the starting point for understanding the codebase and should be read before diving into specific subsystems.

MuMuAINovel is an AI-powered novel creation assistant designed to help authors move from initial inspiration to a completed manuscript through a structured, AI-guided workflow. It orchestrates complex interactions between Large Language Models (LLMs), character relationship mapping, and plot analysis.

**Sources:** [README.md:1-15](), [README.md:110-127]()

## What is MuMuAINovel

MuMuAINovel is a full-stack application that transforms the novel-writing process into a collaborative experience between the author and AI. Unlike simple text editors, it maintains a deep understanding of the story's "World State," including character arcs, organizational hierarchies, and plot threads.

The application consists of:
- **FastAPI backend**: A high-performance Python backend serving REST APIs and real-time Server-Sent Events (SSE) for streaming AI responses.
- **React frontend**: A modern, responsive interface built with TypeScript, Ant Design, and specialized components for visualization (e.g., relationship graphs).
- **PostgreSQL Database**: A production-grade database ensuring data integrity and multi-user isolation.
- **AI Abstraction Layer**: A unified service for interacting with OpenAI, Gemini, Claude, and custom model providers.

**Key Features:**
- **Intelligent Wizard**: Automated generation of world-building, characters, and outlines [README.md:70]().
- **Inspiration Mode**: A conversational interface for brainstorming story ideas [README.md:114]().
- **Character Management**: Visual tools for managing character relationships and organizational structures [README.md:71]().
- **Plot Analysis**: AI-driven analysis of chapter logic and foreshadowing tracking [README.md:120-124]().
- **Multi-tenant Architecture**: Secure data isolation using PostgreSQL schemas and user-based filtering [README.md:75]().

**Sources:** [README.md:67-77](), [backend/.env.example:10-15]()

## System Components

The following diagram bridges the Natural Language concepts (like "Novel Projects") to the Code Entity space (like `Project` models and `api/projects.py` routes).

**System Component Map**
```mermaid
graph TB
    subgraph "Frontend [frontend/src/]"
        App["App.tsx<br/>Router & Auth Guard"]
        ProjectList["pages/ProjectList.tsx<br/>Dashboard"]
        ProjectWizard["pages/ProjectWizardNew.tsx<br/>SSE Wizard"]
        Inspiration["pages/Inspiration.tsx<br/>Brainstorming UI"]
        
        subgraph "State & Services"
            Store["store/index.ts<br/>Zustand Store"]
            ProjectAPI["services/api/projectApi.ts"]
            WizardAPI["services/api/wizardStreamApi.ts"]
        end
    end
    
    subgraph "Backend [backend/app/]"
        Main["main.py<br/>FastAPI Entry"]
        
        subgraph "API Routers [api/]"
            AuthRoute["api/auth.py<br/>/api/auth"]
            WizardRoute["api/wizard_stream.py<br/>/api/wizard-stream"]
            ProjectRoute["api/projects.py<br/>/api/projects"]
            ChapterRoute["api/chapters.py<br/>/api/chapters"]
        end
        
        subgraph "Core Services [services/]"
            AIService["services/ai_service.py<br/>LLM Abstraction"]
            PromptService["services/prompt_service.py<br/>Template Engine"]
            CharacterService["services/auto_character_service.py"]
        end
        
        subgraph "Data Layer"
            DB["database.py<br/>get_db() Dependency"]
            Models["models/*.py<br/>SQLAlchemy Entities"]
        end
    end
    
    subgraph "External"
        Postgres[("PostgreSQL<br/>mumuai_novel DB")]
        LLMs["AI Providers<br/>OpenAI/Gemini/Claude"]
    end
    
    ProjectList --> ProjectAPI
    ProjectWizard --> WizardAPI
    WizardAPI --> WizardRoute
    ProjectAPI --> ProjectRoute
    
    WizardRoute --> AIService
    ChapterRoute --> AIService
    AIService --> LLMs
    
    ProjectRoute --> DB
    DB --> Postgres
    DB -.-> Models
```
**Sources:** [frontend/src/pages/ProjectList.tsx:55-81](), [backend/.env.example:22-29](), [README.md:191-197]()

## Core Data Model

MuMuAINovel uses a structured relational model to maintain story consistency. The relationship between a project, its characters, and its chapters is central to the system's ability to provide context to the AI.

**Entity Relationship Overview**
```mermaid
erDiagram
    USER ||--o{ PROJECT : "owns"
    PROJECT ||--o{ CHARACTER : "contains"
    PROJECT ||--o{ CHAPTER : "contains"
    PROJECT ||--o{ OUTLINE : "has"
    CHARACTER ||--o{ CHARACTER_RELATIONSHIP : "source"
    CHARACTER ||--o{ CHARACTER_RELATIONSHIP : "target"
    CHAPTER ||--o{ CHAPTER_ANALYSIS : "analyzed_by"
    
    PROJECT {
        string id PK
        string title
        string theme
        string genre
        json world_data
    }
    
    CHARACTER {
        string id PK
        string name
        string personality
        boolean is_organization
    }
    
    CHAPTER {
        string id PK
        int chapter_number
        string content
        string summary
    }
```
**Sources:** [README.md:67-77](), [backend/.env.example:22-25]()

## AI Integration Architecture

The system uses a sophisticated abstraction layer to handle various AI providers and streaming responses. This allows the frontend to receive real-time updates while the backend manages prompt construction and model-specific logic.

| Component | Code Entity | Role |
|-----------|-------------|------|
| **Service Layer** | `AIService` | Handles API calls to OpenAI, Gemini, and Claude; manages retries and JSON parsing. |
| **Prompt Factory** | `PromptService` | Injects project context (world-building, characters) into pre-defined templates. |
| **Streaming** | `wizard_stream.py` | Implements FastAPI `EventSourceResponse` for real-time content delivery. |
| **Provider Config** | `.env` | Defines `DEFAULT_AI_PROVIDER` and API keys for global or per-user use. |

**Natural Language to Code Mapping**
```mermaid
graph LR
    subgraph "Natural Language Space"
        Concept1["'Write Chapter 1'"]
        Concept2["'Create a Villain'"]
    end
    
    subgraph "Code Entity Space"
        Route1["api/chapters.py<br/>generate_chapter()"]
        Route2["api/wizard_stream.py<br/>generate_characters()"]
        
        Svc["services/ai_service.py<br/>AIService.generate_text_stream()"]
        Prompt["services/prompt_service.py<br/>get_chapter_prompt()"]
    end
    
    Concept1 --> Route1
    Concept2 --> Route2
    Route1 --> Prompt
    Route2 --> Prompt
    Prompt --> Svc
    Svc --> Provider["OpenAI/Claude/Gemini"]
```
**Sources:** [backend/.env.example:61-70](), [backend/app/main.py](), [frontend/package.json:12-30]()

## Technology Stack

### Backend
- **FastAPI**: Asynchronous web framework for high-concurrency SSE streaming [README.md:7]().
- **PostgreSQL**: Production-grade relational database for multi-user data isolation [README.md:75]().
- **SQLAlchemy**: Async ORM for database interactions.
- **Pydantic**: Data validation and settings management [backend/.env.example:10-15]().

### Frontend
- **React (Vite)**: Frontend framework and build tool [frontend/package.json:25,43]().
- **Ant Design**: UI component library for the dashboard and editor [frontend/package.json:20]().
- **Zustand**: Lightweight state management for project and chapter data [frontend/package.json:29]().
- **React Flow (@xyflow/react)**: Used for visualizing character relationships and plot maps [frontend/package.json:19]().

### Deployment
- **Docker & Docker Compose**: Containerized deployment for easy setup [README.md:176-197]().
- **Nginx**: Typically used as a reverse proxy for the FastAPI/React combined container.

**Sources:** [README.md:5-9](), [frontend/package.json:1-30](), [backend/.env.example:1-25]()

---

# Page: Getting Started

# Getting Started

<details>
<summary>Relevant source files</summary>

The following files were used as context for generating this wiki page:

- [.dockerignore](.dockerignore)
- [.gitignore](.gitignore)
- [Dockerfile](Dockerfile)
- [README.md](README.md)
- [backend/.env.example](backend/.env.example)
- [backend/app/schemas/import_export.py](backend/app/schemas/import_export.py)
- [backend/app/services/import_export_service.py](backend/app/services/import_export_service.py)
- [backend/app/services/memory_service.py](backend/app/services/memory_service.py)
- [docker-compose.yml](docker-compose.yml)
- [frontend/package-lock.json](frontend/package-lock.json)
- [frontend/package.json](frontend/package.json)

</details>



This page provides a quick start guide for setting up and running MuMuAINovel. It covers the prerequisites, deployment options, initial configuration, and verification steps needed to get the system operational.

For detailed deployment instructions, see [Installation and Deployment](#2.1). For comprehensive configuration options, see [Configuration](#2.2). For authentication setup, see [Authentication Setup](#2.3).

## Purpose and Scope

This guide walks through the minimal steps required to:
- Deploy MuMuAINovel using Docker Compose.
- Configure essential settings (database, AI provider, authentication).
- Verify the system is running correctly.
- Access the application and create your first project.

The guide assumes use of Docker Compose for deployment, which is the recommended approach for both development and production environments.

---

## Prerequisites

Before starting, ensure you have the following:

| Requirement | Description | Notes |
|------------|-------------|-------|
| **Docker** | Docker Engine 20.10+ | Required for containerized deployment [README.md:173]() |
| **Docker Compose** | Version 2.0+ | Included with Docker Desktop [README.md:173]() |
| **AI API Key** | At least one LLM provider | OpenAI, Gemini, or Claude [README.md:174]() |
| **Port Availability** | Port 8000 (web) and 5432 (database) | Configurable in `.env` [backend/.env.example:13-25]() |
| **Hardware** | 2 Core CPU / 2GB RAM | Minimum requirements for personal use [README.md:136-141]() |

**Sources**: [README.md:134-175](), [backend/.env.example:13-25]()

---

## Quick Start Workflow

The following diagram illustrates the complete workflow from repository clone to first project creation:

### Deployment and Initialization Workflow

```mermaid
graph TB
    Start["User: Clone Repository"]
    
    subgraph "Phase 1: Setup Files"
        Clone["git clone MuMuAINovel"]
        CopyEnv["cp backend/.env.example .env"]
        EditEnv["Edit .env<br/>- POSTGRES_PASSWORD<br/>- OPENAI_API_KEY<br/>- LOCAL_AUTH_USERNAME/PASSWORD"]
        VerifyFiles["Verify Files Exist:<br/>- .env<br/>- docker-compose.yml<br/>- backend/scripts/init_postgres.sql"]
    end
    
    subgraph "Phase 2: Docker Deployment"
        Pull["docker pull mumujie/mumuainovel:latest<br/>(Recommended for beginners)"]
        Up["docker-compose up -d<br/>Starts services:<br/>- postgres<br/>- mumuainovel"]
        WaitDB["postgres: Run init_postgres.sql<br/>Install extensions"]
        WaitApp["mumuainovel: Run entrypoint.sh<br/>Execute migrations"]
        Ready["Services Ready<br/>postgres:5432<br/>mumuainovel:8000"]
    end
    
    subgraph "Phase 3: Verification"
        CheckLogs["docker-compose logs -f<br/>Check for Uvicorn startup"]
        CheckHealth["Check http://localhost:8000/health<br/>Healthcheck defined in Dockerfile"]
        AccessUI["Open http://localhost:8000<br/>Login page loads"]
    end
    
    subgraph "Phase 4: First Use"
        Login["Login with LOCAL_AUTH credentials<br/>Defined in .env"]
        ConfigAPI["Navigate to Settings<br/>Test AI connection"]
        CreateProject["Create first project:<br/>- Wizard Mode<br/>- Inspiration Mode"]
    end
    
    Start --> Clone
    Clone --> CopyEnv
    CopyEnv --> EditEnv
    EditEnv --> VerifyFiles
    VerifyFiles --> Pull
    Pull --> Up
    Up --> WaitDB
    Up --> WaitApp
    WaitDB --> Ready
    WaitApp --> Ready
    Ready --> CheckLogs
    CheckLogs --> CheckHealth
    CheckHealth --> AccessUI
    AccessUI --> Login
    Login --> ConfigAPI
    ConfigAPI --> CreateProject
```

**Sources**: [README.md:178-197](), [README.md:207-212](), [Dockerfile:119-123]()

---

## Docker Compose Services

MuMuAINovel uses a two-container architecture managed by Docker Compose.

### Service Architecture Diagram

```mermaid
graph TB
    subgraph "Host System"
        EnvFile[".env file<br/>Shared configuration"]
        LogsDir["./logs/<br/>Application logs"]
        DataDir["postgres_data<br/>DB persistence"]
        InitScript["backend/scripts/init_postgres.sql<br/>DB Initialization"]
    end
    
    subgraph "Docker Compose Services"
        subgraph "mumuainovel-postgres [postgres:18-alpine]"
            PG["PostgreSQL Server<br/>Port: 5432"]
            PGEnv["Env Variables:<br/>- POSTGRES_DB<br/>- POSTGRES_USER<br/>- POSTGRES_PASSWORD"]
        end
        
        subgraph "mumuainovel [mumujie/mumuainovel:latest]"
            App["FastAPI Backend<br/>Port: 8000"]
            Static["React Frontend<br/>Served as static files"]
            Embed["Embedding Model<br/>paraphrase-multilingual-MiniLM-L12-v2"]
        end
    end
    
    subgraph "External AI Providers"
        OpenAI["OpenAI API"]
        Gemini["Gemini API"]
        Claude["Claude API"]
    end
    
    EnvFile -.-> PGEnv
    EnvFile -.-> App
    InitScript -.-> PG
    DataDir --- PG
    LogsDir --- App
    
    App -->|"DATABASE_URL"| PG
    App --> OpenAI
    App --> Gemini
    App --> Claude
    
    User["User Browser<br/>http://localhost:8000"] --> App
```

**Sources**: [docker-compose.yml:2-132](), [Dockerfile:82-84]()

---

## Essential Configuration Files

### Configuration File Structure

```mermaid
graph TB
    subgraph "Configuration Entities"
        EnvExample["backend/.env.example<br/>Template file"]
        Env[".env<br/>Active configuration"]
        Compose["docker-compose.yml<br/>Container orchestration"]
        InitSQL["backend/scripts/init_postgres.sql<br/>PostgreSQL init script"]
    end
    
    subgraph "Key Config Groups in .env"
        DB_CFG["Database:<br/>POSTGRES_USER<br/>POSTGRES_PASSWORD<br/>DATABASE_URL"]
        AI_CFG["AI Service:<br/>OPENAI_API_KEY<br/>DEFAULT_MODEL<br/>DEFAULT_AI_PROVIDER"]
        AUTH_CFG["Auth:<br/>LOCAL_AUTH_ENABLED<br/>LOCAL_AUTH_USERNAME<br/>LOCAL_AUTH_PASSWORD"]
        SESSION_CFG["Session:<br/>SESSION_EXPIRE_MINUTES"]
    end
    
    EnvExample -- "Manual Copy" --> Env
    Env -- "Loaded by" --> Compose
    Env -- "Provides" --> DB_CFG
    Env -- "Provides" --> AI_CFG
    Env -- "Provides" --> AUTH_CFG
    Env -- "Provides" --> SESSION_CFG
    InitSQL -- "Mounted to" --> Compose
```

**Sources**: [backend/.env.example:1-125](), [docker-compose.yml:11-13]()

---

## Configuration Categories

### Required Configuration (Minimum to Start)

| Category | Variables | Purpose | Example |
|----------|-----------|---------|---------|
| **Database** | `POSTGRES_PASSWORD` | PostgreSQL connection security | `123456` [backend/.env.example:24]() |
| **AI Provider** | `OPENAI_API_KEY` | Primary LLM access | `sk-...` [backend/.env.example:62]() |
| **Default AI** | `DEFAULT_AI_PROVIDER` | Fallback provider | `openai` [backend/.env.example:66]() |
| **Authentication** | `LOCAL_AUTH_PASSWORD` | Default login password | `admin123` [backend/.env.example:87]() |

### Optional Configuration (Performance and Features)

| Category | Variables | Purpose | Default |
|----------|-----------|---------|---------|
| **Connection Pool** | `DATABASE_POOL_SIZE` | Database concurrency | `30` [docker-compose.yml:84]() |
| **LinuxDO OAuth** | `LINUXDO_CLIENT_ID` | Social login integration | `11111` [backend/.env.example:74]() |
| **Session** | `SESSION_EXPIRE_MINUTES` | Session lifetime | `120` [backend/.env.example:93]() |
| **Prompt Workshop** | `WORKSHOP_MODE` | Community prompt sharing | `client` [backend/.env.example:118]() |

---

## Deployment Steps

### Step 1: Clone Repository
```bash
git clone https://github.com/xiamuceer-j/MuMuAINovel.git
cd MuMuAINovel
```

### Step 2: Configure Environment
```bash
# Copy template
cp backend/.env.example .env

# Edit .env with your favorite editor (e.g., nano, vim)
# Ensure POSTGRES_PASSWORD and OPENAI_API_KEY are set
```

### Step 3: Start Services
```bash
# Using the recommended Docker Hub image
docker-compose up -d
```

### Step 4: Verify Deployment
```bash
# Check if containers are healthy
docker-compose ps

# Check logs for the backend startup
docker-compose logs -f mumuainovel
```

**Sources**: [README.md:178-197](), [docker-compose.yml:124-129]()

---

## Service Health Check Flow

```mermaid
sequenceDiagram
    participant User as "User"
    participant Compose as "docker-compose"
    participant PG as "mumuainovel-postgres"
    participant App as "mumuainovel"
    
    User->>Compose: docker-compose up -d
    Compose->>PG: Start Container
    Compose->>App: Start Container (Depends on PG healthy)
    
    Note over PG: Running init_postgres.sql
    PG->>PG: Healthcheck (pg_isready)
    PG-->>Compose: Healthy
    
    Note over App: Running entrypoint.sh
    App->>App: Wait for DB (nc -z postgres 5432)
    App->>App: Run Alembic Migrations
    App->>App: Start Uvicorn (Port 8000)
    
    App->>App: Healthcheck (curl /health)
    App-->>Compose: Healthy
    
    User->>App: Access http://localhost:8000
    App-->>User: Serve React Frontend
```

**Sources**: [docker-compose.yml:17-22](), [docker-compose.yml:124-129](), [Dockerfile:123]()

---

## First-Time Setup Tasks

### 1. Access the Application
Open your browser and navigate to: `http://localhost:8000`.

### 2. Login
Use the credentials defined in your `.env` file:
- **Username**: Value of `LOCAL_AUTH_USERNAME` (default: `admin`) [backend/.env.example:86]()
- **Password**: Value of `LOCAL_AUTH_PASSWORD` (default: `admin123`) [backend/.env.example:87]()

### 3. Configure API Settings
Navigate to the **Settings** page within the application to:
- Add or update API keys for OpenAI, Gemini, or Claude.
- Test the connection to ensure the backend can reach the AI providers.
- Select the default model for generation tasks.

### 4. Create Your First Project
You can start creating via:
- **Wizard Mode**: A structured flow for generating world-building, characters, and outlines [README.md:70]().
- **Inspiration Mode**: A conversational AI interface to brainstorm story ideas [README.md:114]().

---

## Data Persistence and Backup

MuMuAINovel persists data using Docker volumes and local directories.

| Data Type | Location | Notes |
|-----------|----------|-------|
| **Database** | `postgres_data` (Volume) | PostgreSQL data files [docker-compose.yml:134]() |
| **Logs** | `./logs` (Host Dir) | Application runtime logs [docker-compose.yml:64]() |
| **Covers** | `./storage/generated_covers` | AI generated book covers [docker-compose.yml:65]() |
| **Vector DB** | `data/chroma_db` | Semantic memory storage [backend/app/services/memory_service.py:88]() |

**Sources**: [docker-compose.yml:133-135](), [backend/app/services/memory_service.py:88-92]()

---

## Next Steps

After completing the getting started guide:

1. **Detailed Configuration**: See [Configuration](#2.2) for comprehensive environment variable documentation.
2. **Authentication Options**: See [Authentication Setup](#2.3) for LinuxDO OAuth configuration.
3. **Architecture Overview**: See [System Architecture](#3.1) to understand the system design.
4. **Importing Data**: Use `ImportExportService` to migrate projects from other instances [backend/app/services/import_export_service.py:48]().

---

# Page: Installation and Deployment

# Installation and Deployment

<details>
<summary>Relevant source files</summary>

The following files were used as context for generating this wiki page:

- [.dockerignore](.dockerignore)
- [.gitignore](.gitignore)
- [Dockerfile](Dockerfile)
- [backend/app/schemas/import_export.py](backend/app/schemas/import_export.py)
- [backend/app/services/import_export_service.py](backend/app/services/import_export_service.py)
- [backend/app/services/memory_service.py](backend/app/services/memory_service.py)
- [backend/scripts/entrypoint.sh](backend/scripts/entrypoint.sh)
- [docker-compose.yml](docker-compose.yml)

</details>



This page provides complete instructions for deploying MuMuAINovel in a production or development environment using Docker. It covers the containerized deployment process, service orchestration, database initialization, and essential operational commands.

For detailed environment variable configuration, see [Configuration](#2.2). For authentication setup (local accounts and LinuxDO OAuth), see [Authentication Setup](#2.3). For local development without Docker, see [Development Workflow](#9.2).

---

## Purpose and Scope

This document guides you through deploying MuMuAINovel using Docker Compose, which is the recommended deployment method for both production and development environments. The deployment includes:

- **PostgreSQL 18** database with vector extensions.
- **FastAPI backend** application with embedded frontend.
- **Automatic database initialization** and Alembic migrations.
- **Volume management** for data persistence and model caching.
- **Health checking** and service dependencies.

**Sources**: [docker-compose.yml:1-141](), [Dockerfile:1-123]()

---

## Prerequisites

Before deploying MuMuAINovel, ensure the following requirements are met:

| Requirement | Version | Purpose |
|------------|---------|---------|
| Docker | 20.10+ | Container runtime |
| Docker Compose | 2.0+ | Service orchestration |
| Available Memory | 2GB+ | Application and database |
| Storage | 5GB+ | Database, logs, and models |
| AI Service API Key | N/A | OpenAI, Gemini, or Claude |

**Supported AI Providers**:
- OpenAI (GPT-4, GPT-4o-mini, etc.)
- Google Gemini
- Anthropic Claude
- Any OpenAI-compatible API endpoint

**Sources**: [docker-compose.yml:96-107](), [Dockerfile:119-120]()

---

## Quick Start with Docker Compose

### Deployment Architecture

```mermaid
graph TB
    subgraph "Host System"
        DockerEngine["Docker Engine"]
        
        subgraph "Docker Network: ai-story-network"
            PostgresContainer["[postgres]<br/>Image: postgres:18-alpine<br/>Port: 5432"]
            AppContainer["[mumuainovel]<br/>Image: mumujie/mumuainovel:latest<br/>Port: 8000"]
        end
        
        subgraph "Volumes (Host-Mounted)"
            PostgresData["postgres_data<br/>/var/lib/postgresql"]
            LogsDir["./logs<br/>/app/logs"]
            EnvFile[".env<br/>/app/.env"]
            CoversDir["./storage/generated_covers<br/>/app/storage/generated_covers"]
        end
        
        subgraph "Network Ports"
            Port8000["Host:8000 → Container:8000"]
        end
    end
    
    subgraph "External Services"
        Browser["Web Browser<br/>http://localhost:8000"]
        AIProviders["AI Services<br/>OpenAI/Gemini/Claude"]
        LinuxDO["LinuxDO OAuth<br/>(optional)"]
    end
    
    DockerEngine --> PostgresContainer
    DockerEngine --> AppContainer
    
    PostgresContainer --> PostgresData
    AppContainer --> LogsDir
    AppContainer --> EnvFile
    AppContainer --> CoversDir
    
    AppContainer --> Port8000
    Port8000 --> Browser
    
    AppContainer -- "SQLAlchemy AsyncSession" --> PostgresContainer
    AppContainer -- "AIService" --> AIProviders
    AppContainer -- "OAuthService" --> LinuxDO
    
    EnvFile -. "Settings" .-> AppContainer
```

**Sources**: [docker-compose.yml:1-141](), [Dockerfile:102-106]()

---

### Step 1: Clone the Repository

```bash
git clone https://github.com/xiamuceer-j/MuMuAINovel.git
cd MuMuAINovel
```

---

### Step 2: Configure Environment Variables

Copy the example environment file and edit it with your configuration:

```bash
cp .env.example .env
```

**Minimal Required Configuration**:

```bash
# PostgreSQL Database
POSTGRES_PASSWORD=your_secure_password
DATABASE_URL=postgresql+asyncpg://mumuai:your_secure_password@postgres:5432/mumuai_novel

# AI Service (at least one required)
OPENAI_API_KEY=sk-your-openai-key-here
DEFAULT_AI_PROVIDER=openai
DEFAULT_MODEL=gpt-4o-mini

# Local Authentication
LOCAL_AUTH_ENABLED=true
LOCAL_AUTH_USERNAME=admin
LOCAL_AUTH_PASSWORD=your_secure_password
```

**Sources**: [docker-compose.yml:6-15](), [docker-compose.yml:76-81](), [docker-compose.yml:97-104]()

---

### Step 3: Verify Required Files

Ensure these files exist before starting:

```
MuMuAINovel/
├── .env                                    # Required: Environment configuration
├── docker-compose.yml                      # Required: Service orchestration
└── backend/
    └── scripts/
        ├── init_postgres.sql              # Required: Database initialization
        └── entrypoint.sh                  # Required: Startup logic
```

The initialization script `init_postgres.sql` is automatically mounted to `/docker-entrypoint-initdb.d/init.sql` and executed on first database startup.

**Sources**: [docker-compose.yml:13-13](), [Dockerfile:96-96]()

---

### Step 4: Start Services

```bash
docker-compose up -d
```

This command:
1. Creates the `ai-story-network` bridge network. [docker-compose.yml:138-139]()
2. Starts the `postgres` container and waits for the `pg_isready` healthcheck. [docker-compose.yml:17-21]()
3. Starts the `mumuainovel` container. [docker-compose.yml:52-57]()
4. Runs the `entrypoint.sh` script inside the app container to wait for DB and run Alembic migrations. [backend/scripts/entrypoint.sh:37-84]()

---

### Step 5: Verify Deployment

```bash
# Check service status
docker-compose ps

# View logs (follow mode)
docker-compose logs -f mumuainovel
```

**Expected Output**:
- `mumuainovel` container: `✅ 数据库迁移成功` and `Uvicorn running on http://0.0.0.0:8000`. [backend/scripts/entrypoint.sh:79-97]()

---

## Service Architecture

### Docker Build Process

MuMuAINovel uses a multi-stage Dockerfile to minimize image size and handle complex dependencies.

```mermaid
graph TD
    subgraph "Stage 1: frontend-builder"
        NPM["npm install"] --> Build["npm run build"]
        Build --> Dist["/frontend/dist"]
    end
    
    subgraph "Stage 2: final-image"
        Base["python:3.11-slim"] --> SysDeps["apt-get install gcc/psql-client"]
        SysDeps --> PyDeps["pip install requirements.txt"]
        PyDeps --> ModelDL["Pre-download Embedding Model"]
        ModelDL --> CopyCode["Copy backend/"]
        Dist -- "COPY --from" --> Static["/app/static"]
        CopyCode --> Entry["ENTRYPOINT entrypoint.sh"]
    end
```

**Key Build Steps**:
- **Embedding Model**: The model `sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2` is pre-downloaded during build to `SENTENCE_TRANSFORMERS_HOME` (/app/embedding) to support offline runtime. [Dockerfile:74-85]()
- **Frontend Integration**: Vite is configured to output to `dist`, which is then copied to `/app/static` in the final image. [Dockerfile:31-35](), [Dockerfile:91-91]()
- **Offline Mode**: Environment variables `TRANSFORMERS_OFFLINE=1` and `HF_HUB_OFFLINE=1` are set to prevent runtime network calls for models. [Dockerfile:114-116]()

**Sources**: [Dockerfile:8-35](), [Dockerfile:38-123](), [backend/app/services/memory_service.py:18-67]()

---

## Database Initialization and Migration

### entrypoint.sh Workflow

The `entrypoint.sh` script is the orchestrator for the application container's startup phase.

1.  **Wait for DB**: Uses `nc -z` and `psql` to verify the PostgreSQL service is fully ready. [backend/scripts/entrypoint.sh:37-65]()
2.  **Alembic Migration**: Executes `alembic upgrade head` to ensure the schema is up to date before the app starts. [backend/scripts/entrypoint.sh:77-77]()
3.  **Start Uvicorn**: Launches the FastAPI application using `exec uvicorn`. [backend/scripts/entrypoint.sh:92-97]()

### Import/Export Service

The system includes a robust `ImportExportService` for project portability.

- **Supported Versions**: "1.0.0", "1.1.0". [backend/app/services/import_export_service.py:44-45]()
- **Export Scope**: Includes Projects, Chapters, Characters, Outlines, Relationships, Organizations, Writing Styles, Careers, and Story Memories. [backend/app/services/import_export_service.py:163-180]()
- **Data Model**: Uses `ProjectExportData` Pydantic model to structure the JSON output. [backend/app/schemas/import_export.py:208-223]()

**Sources**: [backend/app/services/import_export_service.py:41-183](), [backend/app/schemas/import_export.py:1-223]()

---

## Connection Pool Configuration

The application uses an optimized PostgreSQL connection pool configured via environment variables in `docker-compose.yml`.

| Variable | Default | Purpose |
|----------|---------|---------|
| `DATABASE_POOL_SIZE` | 30 | Base connections in the pool |
| `DATABASE_MAX_OVERFLOW` | 20 | Additional connections allowed during peaks |
| `DATABASE_POOL_TIMEOUT` | 60 | Seconds to wait for a connection |
| `DATABASE_POOL_RECYCLE` | 1800 | Seconds before recycling a connection |
| `DATABASE_POOL_PRE_PING` | True | Verify connection health before use |

**Sources**: [docker-compose.yml:84-89]()

---

## Vector Memory Setup (ChromaDB)

The system utilizes `MemoryService` for long-term semantic memory, backed by **ChromaDB**.

- **Storage**: Persisted at `data/chroma_db` (or `/app/data/chroma_db` in container). [backend/app/services/memory_service.py:88-92]()
- **Model Path Logic**: The service checks multiple paths (PyInstaller `_MEIPASS`, `_internal`, or dev paths) to locate the `sentence-transformers` model. [backend/app/services/memory_service.py:20-67]()
- **Offline Loading**: If `TRANSFORMERS_OFFLINE` is set, it strictly loads from the local cache folder. [backend/app/services/memory_service.py:106-114]()

**Sources**: [backend/app/services/memory_service.py:69-180]()

---

## Common Operations

### Updating the Deployment
To update to the latest version while preserving data:
```bash
docker-compose pull
docker-compose up -d
```
The `entrypoint.sh` will automatically run `alembic upgrade head` to apply any new database schema changes. [backend/scripts/entrypoint.sh:77-77]()

### Data Persistence
MuMuAINovel persists data in the following locations:
- **PostgreSQL**: `postgres_data` volume. [docker-compose.yml:134-135]()
- **Covers**: `./storage/generated_covers` on host. [docker-compose.yml:65-65]()
- **Logs**: `./logs` on host. [docker-compose.yml:64-64]()

**Sources**: [docker-compose.yml:63-66](), [docker-compose.yml:11-13]()

---

# Page: Configuration

# Configuration

<details>
<summary>Relevant source files</summary>

The following files were used as context for generating this wiki page:

- [README.md](README.md)
- [backend/.env.example](backend/.env.example)
- [backend/app/api/auth.py](backend/app/api/auth.py)
- [backend/app/config.py](backend/app/config.py)
- [backend/app/models/settings.py](backend/app/models/settings.py)
- [backend/requirements.txt](backend/requirements.txt)
- [frontend/package-lock.json](frontend/package-lock.json)
- [frontend/package.json](frontend/package.json)

</details>



This page provides detailed documentation for configuring MuMuAINovel through environment variables, AI provider setup, and user-specific settings. Configuration occurs at two levels: system-wide defaults defined in `.env` files, and per-user settings stored in the database.

For information about deploying the application, see [Installation and Deployment](#2.1). For configuring authentication providers, see [Authentication Setup](#2.3). For runtime AI provider configuration through the UI, see [MCP Plugin System](#5.3).

## Configuration Architecture

MuMuAINovel uses a two-tier configuration system managed by the `Settings` class in `backend/app/config.py`. It leverages `pydantic-settings` for type-safe environment variable parsing and validation.

### Configuration Hierarchy Diagram

```mermaid
graph TB
    subgraph "Configuration Sources"
        EnvFile[".env File<br/>System Defaults"]
        EnvVars["Environment Variables<br/>(Docker/Shell)"]
    end
    
    subgraph "Application Layer"
        ConfigModule["config.py<br/>Settings Class<br/>(Pydantic BaseSettings)"]
        AppSettings["settings<br/>Global Instance"]
    end
    
    subgraph "Database Layer"
        SettingsTable["settings Table<br/>Per-User Records"]
        GlobalDB["_global_users_ DB<br/>Admin Settings"]
    end
    
    subgraph "Runtime"
        UserSettings["User-Specific Settings<br/>(API Provider, Model, etc)"]
        AIService["AIService Instance<br/>Per Request"]
    end
    
    EnvFile --> ConfigModule
    EnvVars --> ConfigModule
    ConfigModule --> AppSettings
    
    AppSettings --> SettingsTable
    AppSettings --> AIService
    
    GlobalDB -- "SMTP/Auth Overrides" --> AppSettings
    SettingsTable --> UserSettings
    UserSettings --> AIService
    
    note1["Priority:<br/>1. User DB Settings<br/>2. Admin Global Settings<br/>3. .env File<br/>4. Code Defaults"]
    
    style SettingsTable fill:#f9f9f9
    style UserSettings fill:#f9f9f9
    style AIService fill:#e8e8e8
```

**Sources:** [backend/app/config.py:24-138](), [backend/app/models/settings.py:8-47](), [backend/app/api/auth.py:125-168]()

### Configuration Loading Flow

The application initializes a global `settings` instance from `backend/app/config.py` during startup. For authentication and system emails, it additionally checks the global database for administrator-defined overrides.

```mermaid
sequenceDiagram
    participant App as "FastAPI Application"
    participant Config as "app.config.settings"
    participant DB as "PostgreSQL / SQLite"
    participant AuthAPI as "auth.py<br/>_get_auth_runtime_settings()"
    
    Note over App,Config: Application Startup
    App->>Config: Load .env + Environment Variables
    Config->>Config: Validate with Pydantic BaseSettings
    Config-->>App: Global settings Instance
    
    Note over AuthAPI,DB: Runtime Auth/SMTP Config
    AuthAPI->>DB: SELECT Settings FROM settings JOIN users WHERE is_admin=True
    alt Admin Settings Found
        DB-->>AuthAPI: Custom SMTP/Auth Config
        AuthAPI->>AuthAPI: Update runtime dict with DB values
    else No Admin Settings
        DB-->>AuthAPI: None
        AuthAPI->>AuthAPI: Use .env defaults from settings
    end
    AuthAPI-->>App: Final Runtime Configuration
```

**Sources:** [backend/app/config.py:130-138](), [backend/app/api/auth.py:125-168](), [backend/app/models/settings.py:29-43]()

## Environment Variables

All environment variables are defined in the `.env` file at the project root. The `backend/.env.example` file provides a template for these values.

### Required Configuration

| Variable | Description | Default/Example |
|----------|-------------|---------|
| `DATABASE_URL` | SQLAlchemy connection string | `postgresql+asyncpg://mumuai:123456@postgres:5432/mumuai_novel` |
| `OPENAI_API_KEY` | Primary AI service key | `your_openai_api_key_here` |
| `LOCAL_AUTH_PASSWORD` | Default admin password | `admin123` |

**Sources:** [backend/.env.example:28-87](), [backend/app/config.py:19-22]()

### Database and Connection Pool

MuMuAINovel is optimized for high concurrency (80-150 users) through specific PostgreSQL connection pool parameters defined in `backend/app/config.py`.

| Variable | Default | Description |
|----------|---------|-------------|
| `DATABASE_POOL_SIZE` | `50` | Core number of persistent connections in the pool. |
| `DATABASE_MAX_OVERFLOW` | `30` | Maximum number of connections allowed beyond `pool_size`. |
| `DATABASE_POOL_TIMEOUT` | `90` | Seconds to wait before throwing an error when no connections are available. |
| `DATABASE_POOL_RECYCLE` | `1800` | Seconds after which a connection is automatically recycled (30 mins). |
| `DATABASE_POOL_PRE_PING` | `True` | Checks connection validity before use to prevent stale connection errors. |

**Sources:** [backend/app/config.py:47-53](), [README.md:154-162]()

### AI Service Configuration

The system supports multiple providers. Defaults are set in `.env` but can be overridden by users in the UI.

#### Default Provider Settings
```bash
DEFAULT_AI_PROVIDER=openai
DEFAULT_MODEL=gpt-4o-mini
DEFAULT_TEMPERATURE=0.7
DEFAULT_MAX_TOKENS=32000
```

#### Provider-Specific Keys
- `OPENAI_API_KEY` / `OPENAI_BASE_URL`
- `GEMINI_API_KEY` / `GEMINI_BASE_URL`
- `ANTHROPIC_API_KEY` / `ANTHROPIC_BASE_URL`

**Sources:** [backend/.env.example:61-70](), [backend/app/config.py:70-79]()

### SMTP and Email Configuration

System emails for registration and verification are configured via SMTP. Administrators can override these via the system settings UI, which updates the `settings` table.

| Variable | Default | Description |
|----------|---------|-------------|
| `SMTP_HOST` | `smtp.qq.com` | SMTP server address. |
| `SMTP_PORT` | `465` | SMTP server port. |
| `SMTP_USE_SSL` | `True` | Whether to use SSL for connection. |
| `EMAIL_AUTH_ENABLED` | `True` | Enables email-based login/registration. |
| `EMAIL_VERIFICATION_CODE_TTL_MINUTES` | `10` | Expiration time for email codes. |

**Sources:** [backend/.env.example:98-111](), [backend/app/models/settings.py:29-43](), [backend/app/config.py:110-123]()

## User Settings System

### Settings Data Model

The `Settings` class in `backend/app/models/settings.py` represents the `settings` table. This table stores both per-user AI preferences and global system configurations (when `user_id` belongs to an admin).

| Field | Type | Description |
|-------|------|-------------|
| `user_id` | `String` | Unique identifier for the user (indexed). |
| `api_provider` | `String` | Selected AI provider (e.g., "openai", "gemini"). |
| `api_key` | `String` | Encrypted/Stored API key for the user. |
| `llm_model` | `String` | Specific model name (e.g., "gpt-4"). |
| `temperature` | `Float` | Sampling temperature (0.0 to 2.0). |
| `cover_enabled` | `Boolean` | Whether AI book cover generation is active. |

**Sources:** [backend/app/models/settings.py:12-47]()

### Configuration Persistence Logic

When a user logs in or makes a request, the system retrieves their specific configuration. If no record exists, it defaults to the values provided in the system-wide `.env` file.

```mermaid
graph LR
    User["User Request"] --> Auth["AuthMiddleware"]
    Auth --> GetID["Get user_id"]
    GetID --> QueryDB["SELECT FROM settings WHERE user_id = :uid"]
    QueryDB -- "Record Found" --> Apply["Apply User Settings"]
    QueryDB -- "Not Found" --> Env["Load Defaults from config.settings"]
    Apply --> AIService["Initialize AIService"]
    Env --> AIService
```

**Sources:** [backend/app/api/auth.py:171-181](), [backend/app/config.py:130-134](), [backend/app/models/settings.py:13-20]()

## Prompt Workshop Configuration

The Prompt Workshop (`提示词工坊`) can operate in two modes defined by `WORKSHOP_MODE`:

1.  **Client Mode (`client`)**: The default mode for local deployments. It connects to a central cloud server (`WORKSHOP_CLOUD_URL`) to fetch community prompts.
2.  **Server Mode (`server`)**: Used only for the central authority (e.g., `mumuverse.space`).

Each instance generates a unique `INSTANCE_ID` stored in `.instance_id` to identify itself to the workshop cloud.

**Sources:** [backend/app/config.py:125-181](), [backend/.env.example:114-124]()

## Logging Configuration

MuMuAINovel uses a rotating file logger for production stability.

| Variable | Default | Description |
|----------|---------|-------------|
| `LOG_LEVEL` | `INFO` | Logging threshold (DEBUG, INFO, WARNING, ERROR). |
| `LOG_TO_FILE` | `True` | Enables persistence to disk. |
| `LOG_MAX_BYTES` | `10485760` | Max size per log file (10MB). |
| `LOG_BACKUP_COUNT` | `30` | Number of old log files to keep. |

**Sources:** [backend/.env.example:39-43](), [backend/app/config.py:34-39]()

---

# Page: Authentication Setup

# Authentication Setup

<details>
<summary>Relevant source files</summary>

The following files were used as context for generating this wiki page:

- [backend/app/api/admin.py](backend/app/api/admin.py)
- [backend/app/api/auth.py](backend/app/api/auth.py)
- [backend/app/api/users.py](backend/app/api/users.py)
- [backend/app/config.py](backend/app/config.py)
- [backend/app/middleware/auth_middleware.py](backend/app/middleware/auth_middleware.py)
- [backend/app/models/settings.py](backend/app/models/settings.py)
- [backend/app/services/oauth_service.py](backend/app/services/oauth_service.py)
- [backend/requirements.txt](backend/requirements.txt)
- [frontend/src/components/UserMenu.tsx](frontend/src/components/UserMenu.tsx)
- [frontend/src/pages/Login.tsx](frontend/src/pages/Login.tsx)
- [frontend/src/pages/UserManagement.tsx](frontend/src/pages/UserManagement.tsx)

</details>



## Purpose and Scope

This page provides a technical guide to configuring authentication in MuMuAINovel. The system implements a multi-tier authentication architecture supporting **Local Username/Password**, **Email Verification Code (Login/Register)**, and **LinuxDO OAuth2**. It details the session management logic, database-backed user models, and the `AuthMiddleware` responsible for request validation and multi-user data isolation.

---

## Authentication System Overview

MuMuAINovel utilizes a flexible authentication stack managed by `user_manager.py` and `auth.py`. User identities are persisted in a PostgreSQL global users table, and sessions are maintained via secure cookies.

### Key Components
- **Local Auth**: Traditional credential-based access defined in environment variables.
- **Email Auth**: Passwordless login and registration using SMTP-based verification codes.
- **OAuth2**: Integration with LinuxDO for third-party identity provider support.
- **Middleware**: `AuthMiddleware` extracts identity from cookies or headers and injects it into `request.state`.

### Code-to-Entity Mapping
| System Concept | Code Entity | File Path |
|:---|:---|:---|
| **User Data Model** | `class User(Base)` | [backend/app/models/user.py:10-45]() |
| **Auth Controller** | `router = APIRouter(prefix="/auth")` | [backend/app/api/auth.py:36-36]() |
| **OAuth Service** | `class LinuxDOOAuthService` | [backend/app/services/oauth_service.py:10-10]() |
| **Identity Injection** | `class AuthMiddleware` | [backend/app/middleware/auth_middleware.py:13-13]() |
| **Password Logic** | `class PasswordManager` | [backend/app/user_password.py]() |

```mermaid
graph TB
    subgraph "Frontend Space"
        Login["Login.tsx Component"]
        UserMenu["UserMenu.tsx Component"]
    end

    subgraph "Backend API Space"
        AuthRouter["auth.py Router"]
        AdminRouter["admin.py Router"]
    end

    subgraph "Logic & Data Space"
        UserManager["user_manager.py"]
        PasswordMgr["user_password.py"]
        OAuthSvc["LinuxDOOAuthService"]
        UserModel["UserModel (PostgreSQL)"]
    end

    Login -- "POST /api/auth/login" --> AuthRouter
    AuthRouter -- "verify" --> PasswordMgr
    AuthRouter -- "fetch/create" --> UserManager
    UserManager -- "persist" --> UserModel
    
    Login -- "OAuth Flow" --> OAuthSvc
    UserMenu -- "GET /api/users/current" --> AuthRouter
    
    AdminRouter -- "CRUD Users" --> UserManager
```
**Sources**: [backend/app/api/auth.py:36-40](), [backend/app/models/user.py:10-45](), [frontend/src/pages/Login.tsx:30-30]()

---

## Configuration Reference

Authentication behavior is governed by `Settings` in `backend/app/config.py`. These values are typically sourced from the `.env` file.

### Core Settings
| Parameter | Default | Description |
|:---|:---|:---|
| `LOCAL_AUTH_ENABLED` | `True` | Enables username/password login |
| `EMAIL_AUTH_ENABLED` | `True` | Enables email verification code login |
| `LINUXDO_CLIENT_ID` | `None` | OAuth Client ID |
| `SESSION_EXPIRE_MINUTES` | `120` | Session duration (2 hours) |
| `SMTP_HOST` | `smtp.qq.com` | Host for sending verification emails |

**Sources**: [backend/app/config.py:84-123]()

---

## Authentication Methods

### 1. Local Authentication
Local auth uses credentials defined in `.env` or created by administrators.
- **Implementation**: The `auth.py` router validates input against the `password_manager`.
- **Admin Users**: The `INITIAL_ADMIN_LINUXDO_ID` can be used to bootstrap the first administrative account.

### 2. Email Verification & Registration
Supports passwordless entry and user self-registration.
- **Flow**: User requests code -> `email_service` sends SMTP mail -> Code stored in `_email_verification_storage` -> User submits code to `/api/auth/email-login`.
- **TTL**: Codes expire based on `EMAIL_VERIFICATION_CODE_TTL_MINUTES` (default 10).

### 3. LinuxDO OAuth2
A full OAuth2 Authorization Code flow.
- **State Storage**: CSRF protection using `_state_storage` in `auth.py`.
- **Callback**: Handled at `/api/auth/callback`, which exchanges the `code` for an `access_token` and fetches profile data via `USERINFO_URL`.

```mermaid
sequenceDiagram
    participant U as User (Browser)
    participant BE as auth.py
    participant OA as LinuxDOOAuthService
    participant LDO as LinuxDO Server

    U->>BE: GET /api/auth/linuxdo
    BE->>OA: generate_state()
    BE->>OA: get_authorization_url(state)
    BE-->>U: Redirect to LinuxDO
    U->>LDO: Authorize
    LDO-->>U: Redirect to /callback?code=xxx
    U->>BE: GET /api/auth/callback
    BE->>OA: get_access_token(code)
    OA->>LDO: POST /oauth2/token
    LDO-->>OA: access_token
    BE->>OA: get_user_info(access_token)
    OA->>LDO: GET /api/user
    LDO-->>OA: {id, username, avatar}
    BE->>BE: create_or_update_user()
    BE-->>U: Set Cookie & Redirect
```
**Sources**: [backend/app/api/auth.py:38-45](), [backend/app/services/oauth_service.py:44-105]()

---

## Session Management & Middleware

### AuthMiddleware Logic
The `AuthMiddleware` executes for every request to populate `request.state`.
1. **Proxy Check**: Checks `X-Instance-ID` for Prompt Workshop requests.
2. **Cookie Extraction**: Reads `user_id` from browser cookies.
3. **Trust Validation**: If `user.trust_level == -1`, the user is treated as unauthorized (banned).
4. **Injection**: Attaches `user_id`, `user` object, and `is_admin` flag to the request state.

### Multi-User Isolation
MuMuAINovel enforces data isolation by using the injected `request.state.user_id` in database dependencies. All project and chapter queries are filtered by this ID to ensure users only access their own data.

```mermaid
graph LR
    subgraph "Request Processing"
        Req["Incoming Request"]
        Mid["AuthMiddleware"]
        Dep["get_db Dependency"]
        Route["API Route Logic"]
    end

    subgraph "Code Entities"
        State["request.state.user_id"]
        Engine["Database Engine"]
    end

    Req --> Mid
    Mid -- "Verify Cookie" --> State
    State --> Dep
    Dep -- "Filter by user_id" --> Engine
    Engine --> Route
```
**Sources**: [backend/app/middleware/auth_middleware.py:16-77](), [backend/app/api/users.py:13-25]()

---

## Administrative User Management

Administrators can manage the user lifecycle through the `UserManagement.tsx` interface and associated `/admin` endpoints.

### Capabilities:
- **User Creation**: `adminApi.createUser` allows manual account provisioning with auto-generated passwords.
- **Status Toggling**: Disabling a user (setting `trust_level` to `-1`) immediately revokes access via middleware.
- **Password Resets**: Admins can force-reset passwords to the default `username@666` pattern.
- **Permission Escalation**: Granting or revoking `is_admin` status.

**Key Functions**:
- `handleToggleStatus`: Calls `adminApi.toggleUserStatus`.
- `handleResetPassword`: Calls `adminApi.resetPassword`.
- `check_admin`: FastAPI dependency ensuring only privileged users access these routes.

**Sources**: [frontend/src/pages/UserManagement.tsx:146-255](), [backend/app/api/admin.py:76-121]()

---

# Page: Architecture

# Architecture

<details>
<summary>Relevant source files</summary>

The following files were used as context for generating this wiki page:

- [README.md](README.md)
- [backend/.env.example](backend/.env.example)
- [backend/app/database.py](backend/app/database.py)
- [backend/app/main.py](backend/app/main.py)
- [backend/app/models/__init__.py](backend/app/models/__init__.py)
- [frontend/package-lock.json](frontend/package-lock.json)
- [frontend/package.json](frontend/package.json)
- [frontend/src/App.tsx](frontend/src/App.tsx)
- [frontend/src/pages/ProjectDetail.tsx](frontend/src/pages/ProjectDetail.tsx)
- [frontend/src/pages/WritingStyles.tsx](frontend/src/pages/WritingStyles.tsx)

</details>



## Purpose and Scope

This document provides a comprehensive overview of the MuMuAINovel system architecture, describing the overall structure, component organization, and key architectural patterns that enable AI-powered novel creation. It explains how the frontend, backend, database, and external services interact to deliver the application's functionality.

For detailed information about specific architectural layers, see:
- Frontend structure and components: [Frontend Architecture](#3.2)
- Backend services and API design: [Backend Architecture](#3.3)
- Multi-user database isolation strategy: [Database Architecture](#3.4)
- Entity relationships and data schemas: [Data Model](#3.5)

For deployment and configuration details, see [Installation and Deployment](#2.1) and [Configuration](#2.2).

## System Overview

MuMuAINovel employs a three-tier architecture with strict separation between presentation (React SPA frontend), business logic (FastAPI backend with service layer), and data persistence (PostgreSQL for relational data, ChromaDB for vector embeddings). The system is designed for Docker Compose deployment with separate containers for application and database services, supporting 80-150 concurrent users with multi-tenant data isolation at the application layer.

### Technology Stack Summary

| Layer | Technologies | Key Files |
|-------|-------------|-----------|
| **Frontend** | React 18.3, TypeScript 5.9, Ant Design 5.27, Zustand 5.0, Axios | [frontend/src/App.tsx:1-75](), [frontend/package.json:1-45]() |
| **Backend** | FastAPI 0.109, SQLAlchemy 2.x (async), Python 3.11, asyncpg | [backend/app/main.py:1-210](), [README.md:6-7]() |
| **Database** | PostgreSQL 18 with connection pooling, ChromaDB for vectors | [backend/app/database.py:1-200](), [README.md:219-268]() |
| **AI Services** | OpenAI SDK, Google Gemini, Anthropic Claude, httpx pooling | [backend/app/services/ai_service.py:40-42](), [backend/.env.example:61-70]() |
| **Specialized Services** | PlotAnalyzer, MemoryService, MCP Registry, PromptService | [backend/app/main.py:15-16](), [backend/app/models/__init__.py:1-50]() |
| **Deployment** | Docker Compose (multi-container), uvicorn ASGI server | [README.md:176-204](), [backend/app/main.py:203-210]() |

Sources: [README.md:1-10](), [backend/.env.example:10-15](), [frontend/package.json:12-30](), [backend/app/main.py:128-160]()

## High-Level Architecture

The following diagram shows the major architectural layers and how they communicate:

### Diagram: System Layers and Communication Paths

```mermaid
graph TB
    subgraph Client["Client Layer"]
        Browser["Web Browser"]
        ReactApp["React Application<br/>frontend/src/App.tsx"]
    end
    
    subgraph Backend["Backend Container - FastAPI"]
        subgraph API["API Router Layer - app/api/"]
            AuthAPI["auth.py<br/>/api/auth"]
            ProjectAPI["projects.py<br/>/api/projects"]
            WizardAPI["wizard_stream.py<br/>/api/wizard-stream"]
            OutlineAPI["outlines.py<br/>/api/outlines"]
            ChapterAPI["chapters.py<br/>/api/chapters"]
            CharacterAPI["characters.py<br/>/api/characters"]
            SettingsAPI["settings.py<br/>/api/settings"]
            InspirationAPI["inspiration.py<br/>/api/inspiration"]
        end
        
        subgraph Services["Service Layer - app/services/"]
            AIService["ai_service.py<br/>AIService"]
            PromptService["prompt_service.py<br/>PromptService"]
            PlotAnalyzer["plot_analyzer.py<br/>PlotAnalyzer"]
            MemoryService["memory_service.py<br/>MemoryService"]
            MCPClient["mcp.py<br/>mcp_client"]
            OAuthService["oauth_service.py<br/>LinuxDO OAuth"]
        end
        
        Database["database.py<br/>get_db()<br/>shared_postgres engine"]
    end
    
    subgraph Data["Data Layer - Docker Volumes"]
        PostgresDB[("PostgreSQL Container<br/>postgres:18-alpine<br/>Port 5432")]
        ChromaDB[("ChromaDB Storage<br/>./chroma_data")]
        Covers["./storage/generated_covers"]
    end
    
    subgraph External["External Services"]
        OpenAI["OpenAI API"]
        Gemini["Google Gemini API"]
        Claude["Anthropic Claude API"]
        LinuxDO["LinuxDO OAuth"]
    end
    
    Browser --> ReactApp
    ReactApp -->|"REST/SSE"| AuthAPI
    ReactApp -->|"REST/SSE"| ProjectAPI
    ReactApp -->|"SSE"| WizardAPI
    ReactApp -->|"REST/SSE"| OutlineAPI
    ReactApp -->|"REST/SSE"| ChapterAPI
    ReactApp -->|"REST"| CharacterAPI
    ReactApp -->|"REST"| SettingsAPI
    
    WizardAPI --> AIService
    OutlineAPI --> AIService
    ChapterAPI --> AIService
    ChapterAPI --> PlotAnalyzer
    InspirationAPI --> AIService
    
    AIService --> OpenAI
    AIService --> Gemini
    AIService --> Claude
    AIService --> MCPClient
    
    AuthAPI --> OAuthService
    OAuthService --> LinuxDO
    
    API --> Database
    Database --> PostgresDB
    MemoryService --> ChromaDB
```

Sources: [backend/app/main.py:128-160](), [backend/app/database.py:45-142](), [backend/.env.example:61-78](), [frontend/src/App.tsx:43-73]()

## Key Architectural Patterns

### 1. Application-Level Multi-Tenant Data Isolation

The system uses a single shared PostgreSQL database with application-level data isolation. All queries automatically filter by `user_id` through SQLAlchemy, ensuring complete data separation between users.

**Shared Connection Pool Architecture:**
- Single `shared_postgres` engine serves all users in PostgreSQL mode [backend/app/database.py:57-59]().
- Connection pool configuration: `pool_size` (default 30), `max_overflow` (default 20) [backend/app/database.py:107-118]().
- `pool_pre_ping=True` validates connections before use [backend/app/database.py:99]().
- SQLite support includes WAL mode for better concurrency [backend/app/database.py:124-138]().

**User Isolation Mechanism:**
1. `AuthMiddleware` extracts `user_id` from session/token and sets `request.state.user_id` [backend/app/main.py:82]().
2. `get_db()` dependency reads `request.state.user_id` and injects it into session context [backend/app/database.py:150-155]().
3. All models include a `user_id` field for row-level isolation [backend/app/database.py:48]().

**Session Statistics and Monitoring:**
The system tracks connection health with `_session_stats` [backend/app/database.py:35-42]():
- `active`: Currently active sessions (warning threshold: >10) [backend/app/main.py:124]().
- `generator_exits`: SSE disconnections tracking [backend/app/database.py:177-178]().

Sources: [backend/app/database.py:1-200](), [backend/app/main.py:108-125](), [backend/.env.example:22-34]()

### 2. AI Provider Abstraction with MCP Integration

The `AIService` provides a unified interface for multiple AI providers, abstracting differences in API formats and streaming mechanisms.

**Provider Support:**
- **OpenAI**: Configured via `OPENAI_API_KEY` and `OPENAI_BASE_URL` [backend/.env.example:62-63]().
- **Google Gemini & Anthropic Claude**: Supported as mainstream models [README.md:69]().
- **MCP (Model Context Protocol)**: Integrated via `mcp_client` to allow AI to use external tools [backend/app/main.py:15-38]().

**Resource Management:**
- `cleanup_http_clients()` ensures proper shutdown of AI connection pools [backend/app/main.py:41-42]().
- `lifespan` manager handles registration and cleanup of MCP status sync [backend/app/main.py:27-48]().

Sources: [backend/app/main.py:15-42](), [backend/.env.example:61-70](), [README.md:69-70]()

### 3. Server-Sent Events (SSE) for Real-Time Progress

All long-running AI generation operations (World Building, Chapter Generation, etc.) use SSE to stream progress updates to the client.

**Implementation Pattern:**
- `wizard_stream.router` handles multi-step project creation [backend/app/main.py:144]().
- `chapters.router` provides streaming chapter generation [backend/app/main.py:149]().
- `_session_stats` explicitly tracks `generator_exits` to handle SSE disconnects without leaking database connections [backend/app/database.py:177-185]().

Sources: [backend/app/main.py:144-149](), [backend/app/database.py:176-186]()

### Diagram: Request Flow Through Backend Stack

This diagram shows a typical AI generation request flowing through the backend, using actual code identifiers:

```mermaid
sequenceDiagram
    participant Client as "React Frontend<br/>chapterApi.ts"
    participant Route as "chapters.py<br/>generate_chapter()"
    participant Auth as "auth_middleware.py<br/>AuthMiddleware"
    participant DB as "database.py<br/>get_db()"
    participant AI as "ai_service.py<br/>AIService"
    participant MCP as "mcp.py<br/>mcp_client"
    participant Postgres as "PostgreSQL<br/>mumuai_novel DB"
    
    Client->>Route: "POST /api/chapters/generate"
    Route->>Auth: "Process Request"
    Auth-->>Route: "Set request.state.user_id"
    
    Route->>DB: "get_db(request)"
    DB->>Postgres: "Checkout Connection"
    DB-->>Route: "AsyncSession"
    
    Route->>AI: "generate_text_stream()"
    AI->>MCP: "Check available tools"
    
    loop "Streaming"
        AI-->>Route: "Yield Content Chunk"
        Route-->>Client: "SSE Event"
    end
    
    Route->>Postgres: "UPDATE chapters SET content=..."
    Postgres-->>Route: "Commit"
    Route-->>Client: "SSE Done"
```

Sources: [backend/app/main.py:82](), [backend/app/database.py:145-165](), [backend/app/main.py:27-42](), [backend/app/database.py:172-186]()

## Component Interaction Patterns

### Frontend State and Routing

The frontend uses **React Router** for navigation and **Zustand** for global state management.

- **Protected Routes**: `ProtectedRoute` component ensures users are authenticated before accessing project data [frontend/src/App.tsx:27, 47]().
- **State Sync Hooks**: `useCharacterSync`, `useOutlineSync`, and `useChapterSync` coordinate data fetching between the API and the global store [frontend/src/pages/ProjectDetail.tsx:24, 78-80]().
- **Theme Management**: `useThemeMode` supports Light, Dark, and System modes across the application [frontend/src/pages/ProjectDetail.tsx:27, 44-49]().

Sources: [frontend/src/App.tsx:37-74](), [frontend/src/pages/ProjectDetail.tsx:66-110](), [frontend/package.json:28-29]()

### Project Detail Navigation

The `ProjectDetail` component serves as a layout parent for project-specific features, using a sidebar menu to navigate between world settings, characters, outlines, and chapters [frontend/src/pages/ProjectDetail.tsx:115-188]().

| Menu Item | Target Component | Purpose |
|-----------|------------------|---------|
| World Setting | `WorldSetting` | Configure story background [frontend/src/App.tsx:58]() |
| Characters | `Characters` | Manage character profiles [frontend/src/App.tsx:61]() |
| Outline | `Outline` | Structure story plot [frontend/src/App.tsx:60]() |
| Chapters | `Chapters` | Write and generate content [frontend/src/App.tsx:65]() |
| Writing Styles | `WritingStyles` | Customize AI tone [frontend/src/App.tsx:68]() |

Sources: [frontend/src/App.tsx:56-72](), [frontend/src/pages/ProjectDetail.tsx:115-188]()

## Scalability and Performance Characteristics

### Connection Management
The system is optimized for high concurrency by using `asyncpg` for asynchronous PostgreSQL communication and `NullPool` with WAL mode for SQLite [backend/app/database.py:73-82, 124-138]().

### Hardware Requirements
- **Minimum**: 2 Core CPU, 2GB RAM [README.md:140-141]().
- **High Concurrency (80-150 users)**: 8 Core CPU, 16GB RAM [README.md:158-159]().
- **Embedding Storage**: Approximately 400MB disk space for models [README.md:164]().

### Deployment Structure
The application is containerized using Docker, with volumes for:
- `./logs`: Application logs [README.md:278]().
- `./storage/generated_covers`: AI-generated book covers [README.md:280]().
- `postgres_data`: Persistent relational data [README.md:229]().

Sources: [README.md:134-168](), [README.md:218-300](), [backend/app/database.py:84-118]()

## Summary

MuMuAINovel's architecture balances simplicity with production-grade features:
- **FastAPI** provides a high-performance asynchronous backend.
- **React & Ant Design** deliver a responsive, feature-rich writing interface.
- **SQLAlchemy** ensures data integrity and multi-user isolation.
- **SSE & MCP** enable sophisticated, real-time AI interactions.

The system is designed to be easily extensible, allowing developers to add new AI providers or specialized writing tools within the established service-oriented framework.

---

# Page: System Architecture

# System Architecture

<details>
<summary>Relevant source files</summary>

The following files were used as context for generating this wiki page:

- [README.md](README.md)
- [backend/.env.example](backend/.env.example)
- [backend/app/api/auth.py](backend/app/api/auth.py)
- [backend/app/config.py](backend/app/config.py)
- [backend/app/main.py](backend/app/main.py)
- [backend/app/models/settings.py](backend/app/models/settings.py)
- [backend/requirements.txt](backend/requirements.txt)
- [frontend/package-lock.json](frontend/package-lock.json)
- [frontend/package.json](frontend/package.json)
- [frontend/src/App.tsx](frontend/src/App.tsx)
- [frontend/src/pages/ProjectDetail.tsx](frontend/src/pages/ProjectDetail.tsx)
- [frontend/src/pages/WritingStyles.tsx](frontend/src/pages/WritingStyles.tsx)

</details>



## Purpose and Scope

This document describes the overall architecture of MuMuAINovel, a web-based AI-powered novel creation assistant. It covers the system's major components, their interactions, deployment strategy, and integration with external services.

For detailed information about specific architectural layers, see:
- Frontend component structure and state management: [3.2]()
- Backend API organization and service patterns: [3.3]()
- Multi-user database session management: [3.4]()
- Entity-relationship data model: [3.5]()

## System Overview

MuMuAINovel follows a three-tier architecture with clear separation between the client layer, application layer, and data layer. The system is typically deployed as two Docker containers: one for the FastAPI application (which serves the pre-built React frontend) and one for the PostgreSQL database. A ChromaDB vector database runs within the application container for semantic memory storage.

### High-Level System Layers

```mermaid
graph TB
    subgraph ClientLayer["Client Layer (frontend/)"]
        Browser["Web Browser (React SPA)"]
    end
    
    subgraph AppContainer["Application Container - mumuainovel"]
        subgraph FastAPIApp["FastAPI Application (app.main:app)"]
            StaticMount["StaticFiles mount<br/>/assets/ & /generated-assets/"]
            APIRoutes["API Routers<br/>app.include_router()"]
        end
        
        subgraph APILayer["backend/app/api/"]
            AuthAPI["auth.py (OAuth & Local)"]
            ProjectsAPI["projects.py"]
            ChaptersAPI["chapters.py"]
            OutlinesAPI["outlines.py"]
            CharactersAPI["characters.py"]
            SettingsAPI["settings.py"]
            WizardStreamAPI["wizard_stream.py (SSE)"]
            InspirationAPI["inspiration.py"]
            MCPPluginsAPI["mcp_plugins.py"]
        end
        
        subgraph ServiceLayer["backend/app/services/"]
            AIService["ai_service.py (LLM Abstraction)"]
            PromptService["prompt_service.py (Templates)"]
            PlotAnalyzer["plot_analyzer.py (Analysis)"]
            MemoryService["memory_service.py (RAG)"]
            EmailService["email_service.py (SMTP)"]
        end
        
        subgraph DatabaseLayer["backend/app/"]
            DatabasePy["database.py (get_db dependency)"]
            ModelsPy["models/ (SQLAlchemy ORM)"]
        end
        
        subgraph VectorDB["Vector Storage"]
            ChromaDB["ChromaDB (chromadb==1.3.2)"]
        end
        
        subgraph MCPSystem["MCP System"]
            mcp_client["mcp/client.py (Context Protocol)"]
        end
    end
    
    subgraph DBContainer["Database Container - postgres"]
        PostgreSQL["PostgreSQL 18<br/>Connection Pool: database_pool_size=50"]
    end
    
    subgraph ExternalServices["External Services"]
        OpenAIAPI["OpenAI API"]
        GeminiAPI["Google Gemini API"]
        ClaudeAPI["Anthropic Claude API"]
        LinuxDOOAuth["LinuxDO OAuth (connect.linux.do)"]
        SMTPServer["SMTP Server (e.g. smtp.qq.com)"]
    end
    
    Browser -->|"HTTP :8000"| StaticMount
    Browser -->|"REST + SSE"| APIRoutes
    
    APIRoutes --> APILayer
    APILayer --> ServiceLayer
    ServiceLayer --> AIService
    AIService --> ExternalServices
    
    AuthAPI --> LinuxDOOAuth
    AuthAPI --> EmailService
    EmailService --> SMTPServer
    
    APILayer --> DatabasePy
    DatabasePy --> PostgreSQL
    MemoryService --> ChromaDB
```

**Sources:** [backend/app/main.py:1-210](), [backend/app/api/auth.py:36-168](), [backend/app/database.py:1-50](), [README.md:218-268](), [backend/requirements.txt:1-39]()

## Application Layer Architecture

The application layer consists of a FastAPI backend that serves both the React frontend (as static files) and provides REST/SSE APIs for dynamic operations. The backend follows a layered service pattern with API routers delegating to specialized services.

### Backend Service Structure

```mermaid
graph TB
    subgraph MainApp["backend/app/main.py"]
        AppInstance["app = FastAPI()"]
        Middleware["AuthMiddleware<br/>RequestIDMiddleware"]
        Lifespan["@asynccontextmanager lifespan"]
    end
    
    subgraph APILayer["API Layer - backend/app/api/"]
        AuthAPI["auth.py (Login/Register)"]
        ProjectsAPI["projects.py"]
        ChaptersAPI["chapters.py"]
        SettingsAPI["settings.py"]
        WizardAPI["wizard_stream.py (SSE)"]
        WorkshopAPI["prompt_workshop.py"]
    end
    
    subgraph CoreServices["Core Service Layer - backend/app/services/"]
        AIService["ai_service.py<br/>- generate_text_stream()<br/>- generate_text_with_mcp()"]
        PromptService["prompt_service.py<br/>- Template management"]
        PlotAnalyzer["plot_analyzer.py<br/>- Narrative extraction"]
        MemoryService["memory_service.py<br/>- Vector search"]
        EmailService["email_service.py<br/>- Verification codes"]
    end
    
    subgraph DatabaseLayer["Database Layer"]
        DatabasePy["database.py<br/>- get_db(request)<br/>- shared_postgres engine"]
        ModelsDir["models/<br/>User, Project, Chapter,<br/>Settings, WritingStyle"]
    end
    
    subgraph ConfigLayer["Configuration"]
        SettingsClass["config.py: Settings<br/>- database_pool_size=50<br/>- database_max_overflow=30"]
        EnvFile[".env"]
    end
    
    AppInstance --> Middleware
    AppInstance --> APILayer
    APILayer --> CoreServices
    CoreServices --> DatabasePy
    DatabasePy --> ModelsDir
    DatabasePy --> SettingsClass
    SettingsClass --> EnvFile
```

**Key Services:**

| Service | Responsibility | Key Methods |
|---------|---------------|-------------|
| `AIService` | LLM provider abstraction, streaming, MCP integration | `generate_text()`, `generate_text_stream()`, `generate_text_with_mcp()` |
| `PromptService` | Template management, user customization | `get_template()`, 20+ template methods |
| `PlotAnalyzer` | Chapter narrative analysis, memory extraction | `analyze_chapter()`, `extract_memories()` |
| `MemoryService` | Semantic memory storage and retrieval | `add_memory()`, `search_memories()` |
| `EmailService` | SMTP communication for registration and verification | `send_verification_code()`, `send_email()` |

**Sources:** [backend/app/main.py:128-160](), [backend/app/services/ai_service.py:1-100](), [backend/app/config.py:44-68](), [backend/app/database.py:1-50](), [backend/app/api/auth.py:23-39]()

## Communication Patterns

MuMuAINovel uses two primary communication patterns between the frontend and backend:

### REST API Communication

Standard HTTP REST endpoints handle CRUD operations. These use JSON request/response payloads with standard HTTP methods.

| Endpoint Pattern | Module | Primary Operations |
|-----------------|---------|-------------------|
| `/api/auth/*` | [backend/app/api/auth.py]() | OAuth, Local login, Email registration |
| `/api/projects/*` | [backend/app/api/projects.py]() | Project CRUD, export/import |
| `/api/chapters/*` | [backend/app/api/chapters.py]() | Chapter management, batch generation |
| `/api/settings/*` | [backend/app/api/settings.py]() | API key presets, model configuration |
| `/api/writing-styles/*` | [backend/app/api/writing_styles.py]() | Style management |
| `/api/prompt-workshop/*` | [backend/app/api/prompt_workshop.py]() | Template sharing (Client/Server modes) |

### Server-Sent Events (SSE) Streaming

For long-running AI generation, the system uses SSE via the `EventSource` pattern to provide real-time progress updates.

#### SSE Generation Flow

```mermaid
sequenceDiagram
    participant FE as "React Frontend"
    participant API as "wizard_stream.py / chapters.py"
    participant AI as "AIService"
    participant Provider as "LLM Provider (OpenAI/Claude)"
    
    FE->>API: "POST /api/wizard-stream/world-building"
    API->>AI: "generate_text_stream(prompt)"
    loop "Streaming Chunks"
        AI->>Provider: "httpx stream request"
        Provider-->>AI: "Chunk data"
        AI-->>API: "yield chunk"
        API-->>FE: "data: {type:'progress', chunk:'...'}"
    end
    API-->>FE: "data: {type:'result', data:{...}}"
    API-->>FE: "data: {type:'done'}"
```

**Sources:** [backend/app/api/wizard_stream.py:1-50](), [backend/app/services/ai_service.py:1-100](), [backend/app/main.py:144-150]()

## Deployment Architecture

MuMuAINovel is optimized for Docker deployment, supporting both SQLite and PostgreSQL.

### Docker Container Structure

```mermaid
graph TB
    subgraph Host["Host System"]
        Port8000[":8000"]
        EnvFile[".env"]
        LogVol["./logs/"]
    end
    
    subgraph AppContainer["Container: mumuainovel"]
        Uvicorn["Uvicorn (app.main:app)"]
        FastAPI["FastAPI Backend"]
        ReactStatic["React Static Build (frontend/dist)"]
        Storage["/app/storage/generated_covers/"]
    end
    
    subgraph DBContainer["Container: mumuainovel-postgres"]
        Postgres["PostgreSQL 18 Alpine"]
        DataVol["/var/lib/postgresql/data"]
    end
    
    Port8000 --> Uvicorn
    Uvicorn --> FastAPI
    FastAPI --> ReactStatic
    FastAPI -->|AsyncPG| Postgres
    EnvFile --> FastAPI
    LogVol --> FastAPI
```

**Key architectural decisions:**
1. **Production-grade Pooling**: PostgreSQL pool is tuned for 80-150 users with `database_pool_size=50` and `database_max_overflow=30` [backend/app/config.py:48-49]().
2. **Static Asset Serving**: FastAPI mounts `/assets` and `/generated-assets/covers` for performance [backend/app/main.py:166-167]().
3. **Health Monitoring**: A dedicated `/health/db-sessions` endpoint monitors for connection leaks [backend/app/main.py:108-125]().

**Sources:** [docker-compose.yml:218-295](), [backend/app/config.py:44-68](), [backend/app/main.py:161-190]()

## Multi-Tenant Data Isolation

Isolation is implemented at the application layer using a shared database with `user_id` filtering.

| Aspect | Implementation | Code Reference |
|--------|---------------|----------------|
| **Authentication** | `AuthMiddleware` extracts user ID from session cookies | [backend/app/middleware/auth_middleware.py]() |
| **Database** | `get_db` dependency provides an `AsyncSession` scoped to the request | [backend/app/database.py]() |
| **Data Filter** | Queries filter by `user_id` (e.g., `Settings.user_id`) | [backend/app/models/settings.py:13]() |
| **Vector DB** | ChromaDB collections are partitioned by user ID | [backend/app/services/memory_service.py]() |

**Sources:** [backend/app/database.py:1-50](), [backend/app/models/settings.py:13](), [backend/app/middleware/auth_middleware.py:1-50]()

## Technology Stack Summary

### Backend Stack
- **Framework**: FastAPI [backend/requirements.txt:2]()
- **ORM**: SQLAlchemy 2.0 [backend/requirements.txt:7]()
- **Database**: PostgreSQL (via asyncpg) or SQLite [backend/requirements.txt:8-11]()
- **AI Services**: OpenAI, Anthropic, Gemini [backend/requirements.txt:18-22]()
- **Vector DB**: ChromaDB [backend/requirements.txt:30]()

### Frontend Stack
- **Framework**: React 18.3 [frontend/package.json:25]()
- **Build Tool**: Vite 7.1 [frontend/package.json:43]()
- **State**: Zustand 5.0 [frontend/package.json:29]()
- **UI Components**: Ant Design 5.27 [frontend/package.json:20]()
- **Styling**: CSS-in-JS (Ant Design) [frontend/package.json:53]()

**Sources:** [backend/requirements.txt:1-39](), [frontend/package.json:1-45]()

---

# Page: Frontend Architecture

# Frontend Architecture

<details>
<summary>Relevant source files</summary>

The following files were used as context for generating this wiki page:

- [backend/app/main.py](backend/app/main.py)
- [frontend/src/App.tsx](frontend/src/App.tsx)
- [frontend/src/components/AppFooter.tsx](frontend/src/components/AppFooter.tsx)
- [frontend/src/components/ChangelogModal.tsx](frontend/src/components/ChangelogModal.tsx)
- [frontend/src/components/ThemeSwitch.tsx](frontend/src/components/ThemeSwitch.tsx)
- [frontend/src/config/version.ts](frontend/src/config/version.ts)
- [frontend/src/main.tsx](frontend/src/main.tsx)
- [frontend/src/pages/ProjectDetail.tsx](frontend/src/pages/ProjectDetail.tsx)
- [frontend/src/pages/WritingStyles.tsx](frontend/src/pages/WritingStyles.tsx)
- [frontend/src/services/api.ts](frontend/src/services/api.ts)
- [frontend/src/services/changelogService.ts](frontend/src/services/changelogService.ts)
- [frontend/src/services/versionService.ts](frontend/src/services/versionService.ts)
- [frontend/src/theme/ThemeProvider.tsx](frontend/src/theme/ThemeProvider.tsx)
- [frontend/src/theme/themeConfig.ts](frontend/src/theme/themeConfig.ts)
- [frontend/src/theme/themeContext.ts](frontend/src/theme/themeContext.ts)
- [frontend/src/theme/themeStorage.ts](frontend/src/theme/themeStorage.ts)
- [frontend/src/theme/useThemeMode.ts](frontend/src/theme/useThemeMode.ts)
- [frontend/src/types/index.ts](frontend/src/types/index.ts)
- [frontend/vite.config.ts](frontend/vite.config.ts)

</details>



## Purpose and Scope

This document describes the architecture of the React-based frontend application for MuMuAINovel. The frontend is a Single Page Application (SPA) built with React 18, TypeScript, and Ant Design. It follows a modular architecture centered around state management with Zustand and real-time communication via Server-Sent Events (SSE) for AI generation tasks.

---

## Technology Stack

The frontend utilizes a modern web stack optimized for developer experience and performance:

| Technology | Version | Purpose |
|------------|---------|---------|
| React | 18.3.1 | Core UI library [frontend/vite.config.ts:29]() |
| TypeScript | ~5.6.2 | Static typing and interface definitions [frontend/src/types/index.ts:1-12]() |
| Ant Design | 5.22.2 | UI component library [frontend/src/App.tsx:3]() |
| Zustand | 5.0.1 | Global state management [frontend/src/store/index.ts]() |
| Axios | 1.7.7 | HTTP client for REST APIs [frontend/src/services/api.ts:1]() |
| Vite | 5.4.10 | Build tool and development server [frontend/vite.config.ts:1]() |

Sources: [frontend/vite.config.ts:27-38](), [frontend/src/types/index.ts:1-61]()

---

## Application Initialization

### Entry Point and Theme Provider
The application initializes in `main.tsx`, wrapping the `App` component with a custom `ThemeProvider`. This provider manages dark/light mode transitions using the Browser's `matchMedia` API and the `startViewTransition` API for smooth visual updates.

- **Theme Logic**: Supports `light`, `dark`, and `system` modes [frontend/src/theme/ThemeProvider.tsx:9-18]().
- **Ant Design Integration**: Uses `ConfigProvider` to inject localized Chinese (`zhCN`) settings and custom theme tokens [frontend/src/theme/ThemeProvider.tsx:144-150]().

Sources: [frontend/src/main.tsx:8-14](), [frontend/src/theme/ThemeProvider.tsx:35-155]()

---

## Routing Architecture

The application uses `react-router-dom` (v6) to manage navigation. Routes are split between public authentication pages and protected application content.

### Route Entity Mapping

```mermaid
graph TD
    subgraph "Public Space"
        Login["/login (Login.tsx)"]
        Callback["/auth/callback (AuthCallback.tsx)"]
    end

    subgraph "Protected Space (ProtectedRoute.tsx)"
        Dashboard["/ (ProjectList.tsx)"]
        Wizard["/wizard (ProjectWizardNew.tsx)"]
        Inspiration["/inspiration (Inspiration.tsx)"]
        Settings["/settings (Settings.tsx)"]
        
        subgraph "Project Workspace (ProjectDetail.tsx)"
            World["world-setting"]
            Outline["outline"]
            Chars["characters"]
            Chaps["chapters"]
            Analysis["chapter-analysis"]
            Styles["writing-styles"]
        end
    end

    App["App.tsx"] --> Login
    App --> Dashboard
    Dashboard --> Wizard
    Dashboard --> Inspiration
    Dashboard --> ProjectDetail
    ProjectDetail --> World
    ProjectDetail --> Outline
    ProjectDetail --> Chaps
```

### Route Table and Components

| Path Pattern | Component | Logic |
|--------------|-----------|-------|
| `/login` | `Login` | Handles local, email, and LinuxDO OAuth login [frontend/src/App.tsx:44]() |
| `/wizard` | `ProjectWizardNew` | Multi-step AI-guided project creation [frontend/src/App.tsx:49]() |
| `/project/:projectId` | `ProjectDetail` | Layout container with sidebar navigation [frontend/src/App.tsx:56]() |
| `.../outline` | `Outline` | Story structure management [frontend/src/App.tsx:60]() |
| `.../chapters` | `Chapters` | Content editor and AI generation [frontend/src/App.tsx:65]() |
| `.../chapter-analysis`| `ChapterAnalysis` | Plot and memory extraction UI [frontend/src/App.tsx:66]() |

Sources: [frontend/src/App.tsx:43-73](), [frontend/src/pages/ProjectDetail.tsx:115-188]()

---

## State Management

MuMuAINovel uses **Zustand** for centralized state management. Instead of a single monolithic store, the system uses a combined store approach (via `useStore`) to manage different domain entities.

### Store Organization and Data Flow

```mermaid
graph LR
    subgraph "Zustand Store (useStore)"
        ProjectState["currentProject"]
        OutlineState["outlines[]"]
        CharacterState["characters[]"]
        ChapterState["chapters[]"]
    end

    subgraph "Synchronization Hooks"
        SyncOutline["useOutlineSync()"]
        SyncChar["useCharacterSync()"]
        SyncChap["useChapterSync()"]
    end

    API["api.ts (Axios)"] --> SyncOutline
    SyncOutline --> OutlineState
    ProjectDetail["ProjectDetail.tsx"] --> SyncOutline
    ProjectDetail --> SyncChar
    ProjectDetail --> SyncChap
```

**Key Patterns:**
- **Automatic Sync**: `ProjectDetail` utilizes custom hooks (`useCharacterSync`, `useOutlineSync`, `useChapterSync`) to fetch data automatically when a `projectId` is present in the URL [frontend/src/pages/ProjectDetail.tsx:78-80]().
- **Global Loading**: A central `loading` state in the store manages UI spinners across pages [frontend/src/pages/ProjectDetail.tsx:85-99]().

Sources: [frontend/src/pages/ProjectDetail.tsx:66-110](), [frontend/src/store/index.ts]()

---

## API Service Layer

The frontend communicates with the backend via a centralized Axios instance in `api.ts`.

### Axios Configuration
- **Base URL**: Prefixed with `/api` [frontend/src/services/api.ts:69]().
- **Interceptors**: 
    - **Request**: Injects credentials for session-based auth [frontend/src/services/api.ts:74]().
    - **Response**: Centralized error handling for 401 (redirect to login), 422 (validation errors), and 500 (server errors) [frontend/src/services/api.ts:86-150]().

### Service Modules
The API is organized into functional objects:
- `authApi`: Session management and OAuth [frontend/src/services/api.ts:152-198]().
- `projectApi`: CRUD for novel projects [frontend/src/services/api.ts:254-285]().
- `writingStyleApi`: Management of AI prose styles [frontend/src/pages/WritingStyles.tsx:26]().
- `ssePost`: A utility for handling Server-Sent Events, used for streaming AI responses [frontend/src/services/api.ts:3]().

Sources: [frontend/src/services/api.ts:68-150](), [frontend/src/pages/WritingStyles.tsx:88-155]()

---

## Key UI Components and Patterns

### 1. Global Footer and Versioning
The `AppFooter` component displays the current version, build time, and update status. It polls a GitHub-based badge API to notify users of new releases [frontend/src/components/AppFooter.tsx:23-39]().

### 2. Writing Style Management
The `WritingStyles` page allows users to define "Custom" or use "Preset" styles.
- **Implementation**: Styles are filtered by `project_id`. Users can set a "Default" style which the backend then applies to all AI generation tasks for that project [frontend/src/pages/WritingStyles.tsx:62-86]().
- **UI**: Uses a responsive `Row`/`Col` grid with Ant Design `Card` components [frontend/src/pages/WritingStyles.tsx:201-220]().

### 3. Changelog Integration
A `ChangelogModal` fetches commit-based updates from the backend, grouping them by date and type (feature, fix, refactor) using the `groupChangelogByDate` utility [frontend/src/components/ChangelogModal.tsx:53-79]().

Sources: [frontend/src/components/AppFooter.tsx:51-143](), [frontend/src/pages/WritingStyles.tsx:170-245](), [frontend/src/components/ChangelogModal.tsx:105-125]()

---

## Build and Optimization

The project uses Vite for bundling, with specific optimizations for large dependencies:

- **Code Splitting**: Large libraries are split into separate chunks to improve initial load time:
    - `vendor-antd`: Ant Design components [frontend/vite.config.ts:31]().
    - `vendor-react`: React core libraries [frontend/vite.config.ts:29]().
    - `vendor-utils`: Axios, Zustand, and Dayjs [frontend/vite.config.ts:33]().
- **Static Asset Handling**: The build output is directed to `../backend/static`, allowing the FastAPI backend to serve the frontend in production [frontend/vite.config.ts:22]().

Sources: [frontend/vite.config.ts:21-41]()

---

# Page: Backend Architecture

# Backend Architecture

<details>
<summary>Relevant source files</summary>

The following files were used as context for generating this wiki page:

- [backend/app/api/admin.py](backend/app/api/admin.py)
- [backend/app/api/auth.py](backend/app/api/auth.py)
- [backend/app/api/users.py](backend/app/api/users.py)
- [backend/app/config.py](backend/app/config.py)
- [backend/app/main.py](backend/app/main.py)
- [backend/app/middleware/auth_middleware.py](backend/app/middleware/auth_middleware.py)
- [backend/app/models/settings.py](backend/app/models/settings.py)
- [backend/requirements.txt](backend/requirements.txt)
- [frontend/src/App.tsx](frontend/src/App.tsx)
- [frontend/src/components/UserMenu.tsx](frontend/src/components/UserMenu.tsx)
- [frontend/src/pages/ProjectDetail.tsx](frontend/src/pages/ProjectDetail.tsx)
- [frontend/src/pages/WritingStyles.tsx](frontend/src/pages/WritingStyles.tsx)

</details>



## Purpose and Scope

This document describes the FastAPI backend architecture of MuMuAINovel, including the API layer structure, service layer design, dependency injection patterns, and request handling flow. The backend is built on **FastAPI 0.121.0** [backend/requirements.txt:2-2]() and utilizes **SQLAlchemy 2.0** [backend/requirements.txt:7-7]() with **asyncpg** [backend/requirements.txt:8-8]() for asynchronous PostgreSQL interactions.

---

## Directory Structure

The backend follows a layered architecture pattern with clear separation of concerns:

```
backend/
├── app/
│   ├── main.py                    # FastAPI application entry point
│   ├── config.py                  # Configuration management (Pydantic Settings)
│   ├── database.py                # PostgreSQL session and pool management
│   ├── logger.py                  # Structured logging configuration
│   ├── api/                       # API route handlers (Controllers)
│   │   ├── auth.py                # OAuth2 and Local Authentication
│   │   ├── users.py               # User profile and permission management
│   │   ├── admin.py               # Administrative user management
│   │   ├── projects.py            # Project CRUD and metadata
│   │   ├── chapters.py            # Chapter generation and editing
│   │   ├── outlines.py            # Outline management and expansion
│   │   ├── characters.py          # Character and relationship CRUD
│   │   ├── writing_styles.py      # Writing style management
│   │   ├── wizard_stream.py       # SSE-based project creation wizard
│   │   ├── inspiration.py         # Conversational AI-guided creation
│   │   └── ...                    # Other domain-specific routers
│   ├── services/                  # Business logic layer
│   │   ├── ai_service.py          # Multi-provider AI abstraction (OpenAI/Anthropic/Gemini)
│   │   ├── prompt_service.py      # Prompt template management
│   │   ├── email_service.py       # SMTP integration for registration
│   │   └── ...                    # Domain services
│   ├── models/                    # SQLAlchemy ORM models
│   │   ├── user.py                # User and Account models
│   │   ├── settings.py            # User-specific AI and System settings
│   │   └── ...                    # Domain models
│   ├── middleware/                # Request/response middleware
│   │   ├── auth_middleware.py     # Cookie/Header based authentication
│   │   └── request_id.py          # Request tracing middleware
│   └── utils/                     # Utility modules
│       └── sse_response.py        # SSE response helpers
└── requirements.txt               # Python dependencies
```

**Sources**: [backend/app/main.py:1-160](), [backend/app/config.py:24-133](), [backend/app/api/auth.py:36-39]()

---

## Application Entry Point

### FastAPI Application Structure

The main FastAPI application is defined in `backend/app/main.py` [backend/app/main.py:50-55](). It configures routing, middleware, and application lifecycles.

**Key Application Setup Diagram**

```mermaid
graph TB
    Main["main.py<br/>FastAPI(lifespan=lifespan)"]
    
    subgraph "Lifespan Management"
        Start["lifespan() start"]
        Sync["register_status_sync()<br/>MCP Status"]
        Stop["lifespan() stop"]
        CleanupAI["cleanup_http_clients()<br/>AI Service"]
        CloseDB["close_db()<br/>Database"]
    end
    
    subgraph "Router Registration"
        AuthRouter["auth.py<br/>prefix=/api/auth"]
        UserRouter["users.py<br/>prefix=/api/users"]
        AdminRouter["admin.py<br/>prefix=/api/admin"]
        WizardRouter["wizard_stream.py<br/>prefix=/api/wizard-stream"]
        ProjectRouter["projects.py<br/>prefix=/api/projects"]
    end
    
    subgraph "Middleware Stack"
        RID["RequestIDMiddleware"]
        AuthM["AuthMiddleware"]
        CORS["CORSMiddleware"]
    end
    
    Main --> Start
    Start --> Sync
    Main --> RID
    RID --> AuthM
    AuthM --> CORS
    CORS --> AuthRouter
    CORS --> UserRouter
    CORS --> AdminRouter
    CORS --> WizardRouter
    CORS --> ProjectRouter
    
    Stop --> CleanupAI
    Stop --> CloseDB
```

The `lifespan` context manager handles critical startup and shutdown tasks, such as cleaning up the `AIService` HTTP client pool and closing database connections [backend/app/main.py:28-48]().

**Sources**: [backend/app/main.py:28-48](), [backend/app/main.py:81-99](), [backend/app/main.py:137-160]()

---

## API Layer Architecture

### Router Organization

The API layer is organized into feature-based routers mounted under the `/api` prefix [backend/app/main.py:137-160]().

| Router | File | Primary Purpose |
|--------|------|----------------|
| **Auth** | `auth.py` | Handles LinuxDO OAuth2, Local Login, and Email verification [backend/app/api/auth.py:36-39]() |
| **Users** | `users.py` | Current user info and basic user management [backend/app/api/users.py:10-10]() |
| **Admin** | `admin.py` | Advanced user management, permission toggling, and password resets [backend/app/api/admin.py:19-19]() |
| **Settings** | `settings.py` | Manages user-specific API keys, models, and SMTP configuration [backend/app/models/settings.py:8-43]() |
| **Writing Styles** | `writing_styles.py` | Project-specific and global writing style management [frontend/src/pages/WritingStyles.tsx:67-70]() |

### Authentication and Authorization

The backend supports a hybrid authentication model implemented in `AuthMiddleware` [backend/app/middleware/auth_middleware.py:13-14]().

1.  **Local/OAuth Session**: Uses a `user_id` cookie to identify the user [backend/app/middleware/auth_middleware.py:50-50]().
2.  **Proxy Requests**: Supports the "Prompt Workshop" feature by accepting `X-Instance-ID` and `X-User-ID` headers for cross-instance communication [backend/app/middleware/auth_middleware.py:24-38]().
3.  **Trust Levels**: Users with a `trust_level` of `-1` are automatically blocked from accessing the system [backend/app/middleware/auth_middleware.py:55-61]().

**Sources**: [backend/app/middleware/auth_middleware.py:13-79](), [backend/app/api/users.py:13-26]()

---

## Dependency Injection Pattern

### Database Session Injection

The system utilizes a shared PostgreSQL connection pool configured for high concurrency (up to 200 concurrent users) [backend/app/config.py:47-53]().

**Database Injection Flow**

```mermaid
graph TB
    subgraph "database.py"
        GetDB["get_db()<br/>AsyncGenerator[AsyncSession]"]
        Pool["Connection Pool<br/>size=50, max_overflow=30"]
    end
    
    subgraph "auth_middleware.py"
        Extract["Extract user_id from Cookie"]
        Inject["request.state.user = UserDTO"]
    end
    
    subgraph "API Endpoint"
        Handler["@router.get('/current')<br/>async def get_user(<br/>  db: AsyncSession = Depends(get_db),<br/>  user: User = Depends(require_login)<br/>)"]
    end
    
    Extract --> Inject
    Inject --> Handler
    Pool --> GetDB
    GetDB --> Handler
```

The `Settings` model is unique per user, identified by `user_id` [backend/app/models/settings.py:13-13](), ensuring that AI configurations and SMTP settings remain isolated between users.

**Sources**: [backend/app/database.py:108-126](), [backend/app/config.py:48-53](), [backend/app/models/settings.py:8-43]()

---

## Service Layer Design

### AI Service Abstraction

The `AIService` manages interactions with multiple LLM providers. It maintains an internal HTTP client pool to optimize performance for streaming responses [backend/app/main.py:41-42]().

**AI Service Lifecycle**

```mermaid
graph LR
    subgraph "AIService (ai_service.py)"
        Stream["generate_text_stream()"]
        Pool["_http_client_pool"]
    end
    
    subgraph "Lifespan (main.py)"
        Cleanup["cleanup_http_clients()"]
    end
    
    Stream --> Pool
    Cleanup --> Pool
```

### Prompt Template System

The system manages 20+ system prompt templates. The `PromptService` handles fallback logic where user-defined templates in the `prompt_templates` table can override system defaults.

**Sources**: [backend/app/main.py:41-42](), [backend/app/api/main.py:156-156]()

---

## Configuration Management

The backend uses `pydantic-settings` to manage environment variables from a `.env` file [backend/app/config.py:24-133]().

| Category | Key Settings | Purpose |
|----------|--------------|---------|
| **Database** | `database_url`, `database_pool_size` | PostgreSQL connection and pooling [backend/app/config.py:45-48]() |
| **Auth** | `LOCAL_AUTH_ENABLED`, `LINUXDO_CLIENT_ID` | Authentication provider toggles [backend/app/config.py:85-101]() |
| **SMTP** | `SMTP_HOST`, `SMTP_PORT`, `SMTP_PASSWORD` | Email verification for registration [backend/app/config.py:112-115]() |
| **Workshop** | `WORKSHOP_MODE`, `WORKSHOP_CLOUD_URL` | Prompt Workshop federation settings [backend/app/config.py:126-127]() |

**Sources**: [backend/app/config.py:24-133](), [backend/app/api/auth.py:125-168]()

---

## Request Processing Flow

### Standard API Flow

1.  **Middleware**: `RequestIDMiddleware` assigns a trace ID; `AuthMiddleware` populates `request.state.user` [backend/app/main.py:81-82]().
2.  **Dependency Resolution**: `get_db` provides a scoped SQLAlchemy session [backend/app/database.py:108-126]().
3.  **Router**: Validates request body using Pydantic schemas.
4.  **Service**: Executes business logic (e.g., calling AI via `AIService`).
5.  **Response**: Returns JSON or SSE stream.

### Error Handling

Global exception handlers in `main.py` capture `RequestValidationError` for 422 errors and generic `Exception` for 500 errors, ensuring consistent JSON error responses [backend/app/main.py:57-79]().

**Sources**: [backend/app/main.py:57-79](), [backend/app/middleware/auth_middleware.py:16-79]()

---

# Page: Database Architecture

# Database Architecture

<details>
<summary>Relevant source files</summary>

The following files were used as context for generating this wiki page:

- [backend/alembic-postgres.ini](backend/alembic-postgres.ini)
- [backend/alembic-sqlite.ini](backend/alembic-sqlite.ini)
- [backend/alembic/README](backend/alembic/README)
- [backend/alembic/postgres/.gitkeep](backend/alembic/postgres/.gitkeep)
- [backend/alembic/postgres/env.py](backend/alembic/postgres/env.py)
- [backend/alembic/postgres/script.py.mako](backend/alembic/postgres/script.py.mako)
- [backend/app/database.py](backend/app/database.py)
- [backend/app/models/__init__.py](backend/app/models/__init__.py)
- [backend/scripts/init_postgres.sql](backend/scripts/init_postgres.sql)
- [backend/scripts/setup_postgres.py](backend/scripts/setup_postgres.py)

</details>



This document describes the database connection management, connection pooling strategy, multi-user data isolation, session lifecycle, and health monitoring systems in MuMuAINovel. The system supports both **PostgreSQL** (production) and **SQLite** (development) with SQLAlchemy async for data persistence, implementing application-level multi-user isolation through a shared connection pool architecture.

For information about the data models and their relationships, see [Data Model](#3.5). For backend session management details, see [Database Session Management](#7.2). For authentication and user isolation, see [User Authentication and Authorization](#7.3).

---

## Overview

MuMuAINovel employs a **shared database** architecture where all users access the same database instance through a single connection pool. Data isolation is enforced at the **application layer** through `user_id` filtering in SQLAlchemy queries, rather than using separate database instances per user. This design maximizes connection efficiency while maintaining security boundaries.

The architecture supports **80-150 concurrent users** when using PostgreSQL, with a connection pool configuration of 50 core connections plus 30 overflow connections. Health monitoring tracks session lifecycle, connection pool usage, and potential leaks.

**Sources:** [backend/app/database.py:1-556](), [backend/app/models/__init__.py:1-50]()

---

## Connection Pool Architecture

### Shared Engine Model

The system uses a single `AsyncEngine` instance shared by all users, cached with the key `"shared_postgres"`. This approach maximizes connection reuse and simplifies connection management.

```mermaid
graph TB
    subgraph "Request Layer"
        Req1["Request (user_id='alice')"]
        Req2["Request (user_id='bob')"]
        Req3["Request (user_id='charlie')"]
    end
    
    subgraph "Engine Cache (_engine_cache)"
        CacheKey["cache_key = 'shared_postgres'"]
        SharedEngine["AsyncEngine instance<br/>(created by create_async_engine)"]
    end
    
    subgraph "Connection Pool (PostgreSQL)"
        PoolConfig["Pool Configuration:<br/>pool_size=50<br/>max_overflow=30<br/>pool_timeout=90s<br/>pool_recycle=1800s<br/>pool_pre_ping=True<br/>pool_use_lifo=True"]
        
        CoreConns["Core Connections (50)"]
        OverflowConns["Overflow Connections (30)"]
        TotalCap["Total Capacity: 80 connections"]
    end
    
    subgraph "PostgreSQL Server"
        PG["PostgreSQL Database<br/>application_name='MuMuAINovel'<br/>jit='off'<br/>statement_cache_size=500"]
    end
    
    Req1 --> CacheKey
    Req2 --> CacheKey
    Req3 --> CacheKey
    
    CacheKey --> SharedEngine
    SharedEngine --> PoolConfig
    PoolConfig --> CoreConns
    PoolConfig --> OverflowConns
    CoreConns --> TotalCap
    OverflowConns --> TotalCap
    
    TotalCap --> PG
```

**Sources:** [backend/app/database.py:45-142](), [backend/app/config.py:43-67]()

### Engine Creation and Caching

The `get_engine()` function implements thread-safe engine creation with caching:

```mermaid
sequenceDiagram
    participant Req as "Request Handler"
    participant GetEngine as "get_engine(user_id)"
    participant Cache as "_engine_cache dict"
    participant Lock as "_cache_lock"
    participant Factory as "create_async_engine"
    
    Req->>GetEngine: get_engine(user_id)
    GetEngine->>Cache: Check cache_key='shared_postgres'
    
    alt Engine exists in cache
        Cache-->>GetEngine: Return cached engine
        GetEngine-->>Req: engine
    else Engine not cached
        GetEngine->>Lock: async with _cache_lock
        Lock->>GetEngine: Acquired lock
        GetEngine->>Cache: Double-check cache
        
        alt Still not in cache
            GetEngine->>Factory: create_async_engine(DATABASE_URL, **engine_args)
            Factory-->>GetEngine: AsyncEngine instance
            GetEngine->>Cache: _engine_cache['shared_postgres'] = engine
            Cache-->>GetEngine: engine
        end
        
        GetEngine->>Lock: Release lock
        GetEngine-->>Req: engine
    end
```

**Key Implementation Details:**

| Parameter | Value | Purpose |
|-----------|-------|---------|
| `pool_size` | 50 | Core connections maintained in pool (PostgreSQL) |
| `max_overflow` | 30 | Additional connections when pool exhausted (PostgreSQL) |
| `pool_timeout` | 90s | Max wait time for connection availability |
| `pool_recycle` | 1800s | Recycle connections after 30 minutes |
| `pool_pre_ping` | `True` | Test connection validity before use |
| `pool_use_lifo` | `True` | LIFO strategy for better connection reuse |
| `pool_reset_on_return` | `"rollback"` | Auto-rollback on connection return |

**Sources:** [backend/app/database.py:45-142](), [backend/app/config.py:46-57]()

---

## Multi-User Data Isolation

### Application-Level Filtering

All database tables containing user data include a `user_id` column. The system enforces data isolation by automatically filtering queries based on the authenticated user's ID, extracted from `request.state.user_id`.

```mermaid
graph TB
    subgraph "Authentication Layer"
        AuthMiddleware["AuthMiddleware<br/>(auth_routes.py)"]
        RequestState["request.state.user_id<br/>(set by middleware)"]
    end
    
    subgraph "Database Dependency"
        GetDB["get_db(request)<br/>(database.py:145-224)"]
        UserIDExtract["user_id = getattr(request.state, 'user_id')"]
        GetEngineCall["engine = await get_engine(user_id)"]
        SessionFactory["AsyncSessionLocal = async_sessionmaker(engine)"]
    end
    
    subgraph "Database Tables"
        Projects["projects table<br/>(user_id='alice')"]
        Chapters["chapters table<br/>(user_id='alice')"]
        Characters["characters table<br/>(user_id='alice')"]
        Outlines["outlines table<br/>(user_id='alice')"]
        
        ProjectsB["projects table<br/>(user_id='bob')"]
        ChaptersB["chapters table<br/>(user_id='bob')"]
    end
    
    subgraph "SQLAlchemy Query Layer"
        QueryFilter["SELECT * FROM projects<br/>WHERE user_id = 'alice'"]
    end
    
    subgraph "Shared Data"
        WritingStyles["writing_styles table<br/>(user_id IS NULL)<br/>Global Presets"]
        RelTypes["relationship_types table<br/>(user_id IS NULL)<br/>Global Types"]
    end
    
    AuthMiddleware --> RequestState
    RequestState --> GetDB
    GetDB --> UserIDExtract
    UserIDExtract --> GetEngineCall
    GetEngineCall --> SessionFactory
    
    SessionFactory --> QueryFilter
    QueryFilter --> Projects
    QueryFilter --> Chapters
    QueryFilter --> Characters
    QueryFilter --> Outlines
    
    QueryFilter -.does not access.-> ProjectsB
    QueryFilter -.does not access.-> ChaptersB
    
    QueryFilter -.reads global data.-> WritingStyles
    QueryFilter -.reads global data.-> RelTypes
```

**Sources:** [backend/app/database.py:145-154](), [backend/app/database.py:226-344]()

### Global Shared Data

Some data is globally shared across all users using `user_id=NULL`:

| Data Type | Table | Initialization Function | Usage |
|-----------|-------|------------------------|-------|
| Writing Style Presets | `writing_styles` | `_init_global_writing_styles()` | Preset styles like "natural", "classical", "modern" |
| Relationship Types | `relationship_types` | `_init_relationship_types()` | Preset relationships like "父亲", "朋友", "敌人" |

These global presets are inserted once during database initialization and are read-only for all users.

**Sources:** [backend/app/database.py:226-287](), [backend/app/database.py:291-344]()

---

## Session Lifecycle Management

### get_db() Dependency

The `get_db()` function is a FastAPI dependency that manages the complete session lifecycle for each request:

```mermaid
sequenceDiagram
    participant Endpoint as "API Endpoint"
    participant GetDB as "get_db(request)"
    participant Stats as "_session_stats dict"
    participant SessionFactory as "AsyncSessionLocal"
    participant Session as "AsyncSession instance"
    
    Endpoint->>GetDB: Inject dependency
    GetDB->>GetDB: user_id = request.state.user_id
    
    alt user_id is None
        GetDB-->>Endpoint: HTTPException 401
    end
    
    GetDB->>GetDB: engine = await get_engine(user_id)
    GetDB->>SessionFactory: Create AsyncSessionLocal
    GetDB->>Session: session = AsyncSessionLocal()
    
    GetDB->>Stats: _session_stats['created'] += 1
    GetDB->>Stats: _session_stats['active'] += 1
    GetDB->>GetDB: Log session creation
    
    GetDB-->>Endpoint: yield session
    
    Note over Endpoint: Endpoint uses session<br/>for database operations
    
    alt GeneratorExit (SSE disconnect)
        GetDB->>Stats: _session_stats['generator_exits'] += 1
        GetDB->>Session: if in_transaction: rollback()
        GetDB->>GetDB: Log GeneratorExit
    else Exception during request
        GetDB->>Stats: _session_stats['errors'] += 1
        GetDB->>Session: if in_transaction: rollback()
        GetDB->>GetDB: Log exception
    end
    
    GetDB->>Session: Check if in_transaction
    
    alt Transaction still active
        GetDB->>Session: await session.rollback()
        GetDB->>GetDB: Log warning (uncommitted transaction)
    end
    
    GetDB->>Session: await session.close()
    GetDB->>Stats: _session_stats['closed'] += 1
    GetDB->>Stats: _session_stats['active'] -= 1
    GetDB->>GetDB: Check leak thresholds
    
    alt active > leak_threshold
        GetDB->>GetDB: Log critical alert
    else active > max_active
        GetDB->>GetDB: Log warning
    end
```

**Sources:** [backend/app/database.py:145-224]()

---

## Database Health Monitoring

### get_database_stats() Function

The `get_database_stats()` function provides comprehensive monitoring data, including session metrics and pool utilization.

```mermaid
graph TB
    subgraph "Statistics Collection"
        GetStats["get_database_stats()"]
        
        subgraph "Session Metrics"
            SessionCreated["created: total sessions"]
            SessionClosed["closed: total closed"]
            SessionActive["active: current active"]
            SessionErrors["errors: error count"]
            SessionGenExit["generator_exits: SSE disconnects"]
        end
        
        subgraph "Pool Metrics"
            PoolSize["size: current pool size"]
            CheckedIn["checked_in: available connections"]
            CheckedOut["checked_out: in-use connections"]
            Overflow["overflow: overflow connections"]
            UsagePercent["usage_percent: utilization %"]
        end
        
        subgraph "Health Assessment"
            Status["status: healthy/warning/critical"]
            Warnings["warnings: list of warnings"]
            Errors["errors: list of errors"]
            ErrorRate["error_rate: percentage"]
        end
    end
    
    subgraph "Health Checks"
        Check1["active > leak_threshold<br/>→ status = critical"]
        Check2["active > max_active<br/>→ status = warning"]
        Check3["usage_percent > 95%<br/>→ status = critical"]
        Check4["usage_percent > 90%<br/>→ status = warning"]
        Check5["error_rate > 5%<br/>→ status = warning"]
    end
    
    GetStats --> SessionCreated
    GetStats --> SessionClosed
    GetStats --> SessionActive
    GetStats --> SessionErrors
    GetStats --> SessionGenExit
    
    GetStats --> PoolSize
    GetStats --> CheckedIn
    GetStats --> CheckedOut
    GetStats --> Overflow
    GetStats --> UsagePercent
    
    SessionActive --> Check1
    SessionActive --> Check2
    UsagePercent --> Check3
    UsagePercent --> Check4
    SessionErrors --> Check5
    
    Check1 --> Status
    Check2 --> Status
    Check3 --> Status
    Check4 --> Status
    Check5 --> Status
    
    Status --> Warnings
    Status --> Errors
    Status --> ErrorRate
```

**Leak Detection Thresholds:**

| Threshold | Value | Action |
|-----------|-------|--------|
| `database_session_max_active` | 50 | Log warning |
| `database_session_leak_threshold` | 100 | Log critical alert |

**Sources:** [backend/app/database.py:382-473](), [backend/app/config.py:59-61]()

---

## Database Initialization and Migrations

### init_db() Workflow

The `init_db()` function handles table creation and the insertion of preset data (relationship types and writing styles) during system setup.

**Sources:** [backend/app/database.py:347-366](), [backend/app/database.py:226-344]()

### Alembic Migration Profiles

The system maintains independent migration profiles for PostgreSQL and SQLite to handle dialect-specific differences like `JSON` vs `TEXT` mapping and `ALTER TABLE` capabilities.

| Profile | Config File | Script Location | Batch Mode |
|---------|-------------|-----------------|------------|
| PostgreSQL | `alembic-postgres.ini` | `alembic/postgres` | `False` |
| SQLite | `alembic-sqlite.ini` | `alembic/sqlite` | `True` |

**Sources:** [backend/alembic-postgres.ini:1-13](), [backend/alembic-sqlite.ini:1-13](), [backend/alembic/README:1-145]()

### Manual Setup Scripts

For PostgreSQL environments, a manual setup script is provided to automate database and user creation.

| Script | Purpose |
|--------|---------|
| `backend/scripts/setup_postgres.py` | Python script to create DB, User, and Grant Privileges |
| `backend/scripts/init_postgres.sql` | SQL script to enable extensions (`uuid-ossp`, `pg_trgm`) |

**Sources:** [backend/scripts/setup_postgres.py:50-214](), [backend/scripts/init_postgres.sql:1-22]()

---

## Performance and Resilience

### Connection Pool Configuration

The connection pool is optimized for production high-concurrency scenarios:

**PostgreSQL Optimized Parameters:**
- `pool_size=50`: Core connections.
- `max_overflow=30`: Burst capacity.
- `pool_timeout=90s`: Wait time for connections.
- `pool_recycle=1800s`: Prevents stale connections.

**SQLite Optimization (WAL Mode):**
When using SQLite, the system automatically enables **Write-Ahead Logging (WAL)** mode to improve read/write concurrency.

```python
# SQLite WAL Mode Configuration
cursor.execute("PRAGMA journal_mode=WAL")
cursor.execute("PRAGMA synchronous=NORMAL")
cursor.execute("PRAGMA busy_timeout=30000") # 30s timeout
```

**Sources:** [backend/app/database.py:95-106](), [backend/app/database.py:124-141]()

### Special Handling: GeneratorExit

SSE streaming endpoints (used for AI generation) can disconnect mid-stream. The `get_db` dependency handles this by:
1. Catching `GeneratorExit`.
2. Incrementing the `generator_exits` statistic.
3. Rolling back any active transaction to prevent partial data corruption.
4. Ensuring the session is closed.

**Sources:** [backend/app/database.py:176-185]()

---

# Page: Data Model

# Data Model

<details>
<summary>Relevant source files</summary>

The following files were used as context for generating this wiki page:

- [backend/app/models/chapter.py](backend/app/models/chapter.py)
- [backend/app/models/project.py](backend/app/models/project.py)
- [backend/app/models/regeneration_task.py](backend/app/models/regeneration_task.py)
- [backend/app/models/relationship.py](backend/app/models/relationship.py)
- [backend/app/models/user.py](backend/app/models/user.py)
- [backend/app/schemas/project.py](backend/app/schemas/project.py)
- [backend/app/schemas/regeneration.py](backend/app/schemas/regeneration.py)
- [backend/app/schemas/relationship.py](backend/app/schemas/relationship.py)
- [frontend/src/services/api.ts](frontend/src/services/api.ts)
- [frontend/src/types/index.ts](frontend/src/types/index.ts)

</details>



## Purpose and Scope

This document describes the data model used in MuMuAINovel, including all database entities, their relationships, and the multi-user data isolation strategy. It covers the structure of Projects, Chapters, Outlines, Characters, and supporting entities that store AI generation history and user preferences.

For database session management and connection pooling, see [Database Architecture](#3.4). For API endpoints that interact with these entities, see [API Reference](#8).

---

## Multi-User Data Isolation Strategy

MuMuAINovel uses **PostgreSQL with application-level data isolation**. All users share a single PostgreSQL database with a unified connection pool, and data isolation is enforced through `user_id` filtering at the application layer.

### Shared Database Architecture

```mermaid
graph TB
    subgraph "All_Users"
        UserA["User A"]
        UserB["User B"]
        UserN["User N"]
    end
    
    subgraph "Shared_Engine_Layer"
        SharedEngine["shared_postgres_engine<br/>cache_key: 'shared_postgres'"]
        ConnectionPool["SQLAlchemy_QueuePool<br/>pool_size: 50<br/>max_overflow: 30"]
    end
    
    subgraph "PostgreSQL_Database"
        Projects["projects_table<br/>user_id_column"]
        Chapters["chapters_table<br/>user_id_column"]
        Characters["characters_table<br/>user_id_column"]
        Outlines["outlines_table<br/>user_id_column"]
    end
    
    UserA --> SharedEngine
    UserB --> SharedEngine
    UserN --> SharedEngine
    
    SharedEngine --> ConnectionPool
    ConnectionPool --> Projects
    ConnectionPool --> Chapters
    ConnectionPool --> Characters
    ConnectionPool --> Outlines
```

**Sources:** [backend/app/models/user.py:9-22](), [backend/app/models/project.py:8-44]()

---

### Application-Level Data Isolation

Data isolation is enforced through SQLAlchemy query filtering. The `user_id` is a primary filter for all business entities including `Project`, `Chapter`, and `Character`.

Some entities like `RelationshipType` use `user_id = NULL` or are system-wide to indicate globally shared data.

**Sources:** [backend/app/models/project.py:13-13](), [backend/app/models/relationship.py:12-20](), [backend/app/models/user.py:13-13]()

---

## Core Entities

### User Entity

The `User` entity stores basic authentication and profile information.

```mermaid
erDiagram
    User {
        string user_id PK "linuxdo_{id} or local_{id}"
        string username "Unique username"
        string display_name "Display name"
        string avatar_url "Avatar link"
        int trust_level "LinuxDO trust level"
        boolean is_admin "Admin flag"
        string linuxdo_id "OAuth ID"
        datetime created_at "Creation time"
        datetime last_login "Last login time"
    }
    UserPassword {
        string user_id PK "FK to User"
        string password_hash "SHA256 hash"
        boolean has_custom_password "Flag"
    }
```

**Sources:** [backend/app/models/user.py:9-47]()

---

### Project Entity

The `Project` entity represents a novel project and serves as the root container for all related data.

#### Project Fields

```mermaid
erDiagram
    Project {
        string id PK "UUID"
        string user_id "Owner ID"
        string title "Title"
        string description "Description"
        string theme "Theme"
        string genre "Genre"
        int target_words "Target"
        int current_words "Calculated"
        string status "planning/writing/etc"
        string wizard_status "incomplete/completed"
        int wizard_step "0-4"
        string outline_mode "one-to-one/one-to-many"
        string world_time_period "World Building"
        string world_location "World Building"
        string world_atmosphere "World Building"
        string world_rules "World Building"
        int chapter_count "Config"
        string narrative_perspective "Config"
        string cover_status "none/generating/ready/failed"
    }
```

The `outline_mode` field is critical; it determines whether an outline entry maps to exactly one chapter (`one-to-one`) or multiple chapters (`one-to-many`) [backend/app/models/project.py:23-23]().

**Sources:** [backend/app/models/project.py:8-58](), [frontend/src/types/index.ts:155-181]()

---

### Chapter Entity

The `Chapter` entity stores chapter content and supports **one-to-many outline expansion** through the `expansion_plan` field.

#### Chapter Fields and Constraints

```mermaid
erDiagram
    Chapter {
        string id PK "UUID"
        string project_id FK "FK to Project"
        int chapter_number "Global sequence"
        string title "Title"
        string content "Text"
        string summary "AI Summary"
        int word_count "Calculated"
        string status "draft/completed"
        string outline_id FK "FK to Outline"
        int sub_index "Sub-index for outline"
        text expansion_plan "JSON structure"
    }
```

**Key Fields:**
- `outline_id`: Links the chapter to its parent outline [backend/app/models/chapter.py:22-22]().
- `sub_index`: Used in `one-to-many` mode to order multiple chapters belonging to the same outline [backend/app/models/chapter.py:23-23]().
- `expansion_plan`: Stores JSON data including `key_events`, `character_focus`, and `scenes` used by the AI to generate content [backend/app/models/chapter.py:26-26]().

**Sources:** [backend/app/models/chapter.py:8-32](), [frontend/src/types/index.ts:311-326]()

---

### Outline Entity

The `Outline` entity represents the high-level story structure.

```mermaid
erDiagram
    Outline {
        string id PK "UUID"
        string project_id FK "FK to Project"
        string title "Outline Title"
        string content "Description"
        string structure "Optional JSON"
        int order_index "Sequence"
    }
    Outline ||--o{ Chapter : "contains"
```

In `one-to-many` mode, one `Outline` record serves as the source for multiple `Chapter` records.

**Sources:** [frontend/src/types/index.ts:248-258]()

---

### Character and Organization Entities

MuMuAINovel uses a unified `Character` model where organizations are specialized character entities.

```mermaid
erDiagram
    Character {
        string id PK "UUID"
        string project_id FK "FK to Project"
        string name "Name"
        boolean is_organization "Type flag"
        string role_type "protagonist/antagonist"
        string personality "Traits"
        string background "History"
    }
    Organization {
        string id PK "UUID"
        string character_id FK "Unique FK to Character"
        string parent_org_id FK "Self-referential FK"
        int level "Hierarchy level"
        int power_level "0-100"
        string location "Base"
        string motto "Slogan"
    }
    OrganizationMember {
        string id PK "UUID"
        string organization_id FK "FK to Organization"
        string character_id FK "FK to Character"
        string position "Job title"
        int rank "Numeric rank"
        int loyalty "0-100"
    }
```

**Key Implementation Details:**
- `Organization` records have a `unique=True` relationship with a `Character` record [backend/app/models/relationship.py:64-64]().
- `CharacterRelationship` defines directed links between characters with an `intimacy_level` ranging from -100 to 100 [backend/app/models/relationship.py:41-41]().

**Sources:** [backend/app/models/relationship.py:59-116](), [backend/app/schemas/relationship.py:93-200](), [frontend/src/types/index.ts:276-309]()

---

## Relationship Metadata

### RelationshipType Entity

This entity defines the "vocabulary" of relationships available in the system.

| Category | Description |
|----------|-------------|
| `family` | Kinship ties (e.g., Father, Sister) |
| `social` | Friendship and community ties |
| `hostile` | Rivalries and enemies |
| `professional` | Work-related ties (e.g., Mentor, Subordinate) |

**Sources:** [backend/app/models/relationship.py:8-22](), [backend/app/schemas/relationship.py:9-20]()

---

## Task and History Entities

### RegenerationTask Entity

Tracks the status of chapter content regeneration requests.

```mermaid
erDiagram
    RegenerationTask {
        string id PK "UUID"
        string chapter_id FK "Target Chapter"
        string status "pending/running/completed/failed"
        text modification_instructions "Combined AI prompt"
        text original_content "Backup"
        text regenerated_content "Result"
        int version_number "Version"
    }
```

**Sources:** [backend/app/models/regeneration_task.py:8-50](), [backend/app/schemas/regeneration.py:41-65]()

---

### Story Memory and Analysis

MuMuAINovel stores semantic analysis of chapters to maintain long-term consistency.

- **`PlotAnalysis`**: Stores structured JSON data about chapter hooks, foreshadowing, and conflicts.
- **`StoryMemory`**: Individual memory units extracted from analysis, often linked to vector IDs in ChromaDB for semantic retrieval.

**Sources:** [backend/app/models/regeneration_task.py:15-15](), [frontend/src/services/api.ts:58-61]()

---

## Complete Entity Relationship Diagram (Code Space)

This diagram maps the backend SQLAlchemy models to their functional relationships.

```mermaid
erDiagram
    "User" ||--o{ "Project" : "owns"
    "Project" ||--o{ "Outline" : "has_structure"
    "Project" ||--o{ "Chapter" : "contains"
    "Project" ||--o{ "Character" : "includes"
    "Outline" ||--o{ "Chapter" : "expands_into"
    "Character" ||--o{ "CharacterRelationship" : "from"
    "Character" ||--o{ "CharacterRelationship" : "to"
    "Character" ||--o| "Organization" : "is_represented_by"
    "Organization" ||--o{ "OrganizationMember" : "has"
    "Character" ||--o{ "OrganizationMember" : "belongs_to"
    "Chapter" ||--o{ "RegenerationTask" : "tracks_edits"
    "RelationshipType" ||--o{ "CharacterRelationship" : "defines"

    "Project" {
        string id
        string user_id
        string outline_mode
    }
    "Chapter" {
        string id
        string outline_id
        text expansion_plan
    }
    "Character" {
        string id
        boolean is_organization
    }
```

**Sources:** [backend/app/models/project.py:8-44](), [backend/app/models/chapter.py:8-32](), [backend/app/models/relationship.py:25-116]()

---

# Page: Core Features

# Core Features

<details>
<summary>Relevant source files</summary>

The following files were used as context for generating this wiki page:

- [backend/app/main.py](backend/app/main.py)
- [frontend/src/App.tsx](frontend/src/App.tsx)
- [frontend/src/pages/ProjectDetail.tsx](frontend/src/pages/ProjectDetail.tsx)
- [frontend/src/pages/ProjectList.tsx](frontend/src/pages/ProjectList.tsx)
- [frontend/src/pages/WritingStyles.tsx](frontend/src/pages/WritingStyles.tsx)

</details>



This document provides a comprehensive overview of MuMuAINovel's core features and workflows. It describes the major functional capabilities of the system and how they integrate to support AI-assisted novel creation from initial concept through completed chapters.

For detailed API specifications, see [API Reference](#8). For AI integration details including prompt engineering and streaming, see [AI Integration](#5). For frontend component implementation, see [Frontend Guide](#6).

## Overview

MuMuAINovel provides several primary feature areas that work together to support the complete novel writing workflow:

| Feature | Primary Purpose | Key Components |
|---------|----------------|----------------|
| **Project Creation Wizard** | Guided AI-assisted project initialization | `wizard_stream.py`, `ProjectWizardNew.tsx` |
| **Inspiration Mode** | Conversational AI-assisted project creation | `inspiration.py`, `Inspiration.tsx` |
| **Outline Management** | Story structure planning and expansion | `outlines.py`, `Outline.tsx` |
| **Chapter Writing** | AI-generated chapter content with context awareness | `chapters.py`, `Chapters.tsx` |
| **Chapter Analysis** | Plot memory extraction and semantic storage | `PlotAnalyzer`, `ChapterAnalysis.tsx` |
| **Character Management** | Profiles, relationships, and organizations | `characters.py`, `Characters.tsx`, `Relationships.tsx` |
| **Writing Styles** | Customizable AI writing style presets | `WritingStyle` model, `WritingStyles.tsx` |

These features share common infrastructure including the `AIService` abstraction layer [backend/app/services/ai_service.py:20-50](), `PromptService` template system [backend/app/services/prompt_service.py:10-30](), and per-user SQLite databases managed by `database.py` [backend/app/database.py:15-40]().

## Feature Architecture

### Feature-to-Code Mapping

```mermaid
graph TB
    subgraph "Feature Layer"
        ProjectWizard["Project Creation Wizard"]
        InspirationMode["Inspiration Mode"]
        OutlineMgmt["Outline Management"]
        ChapterWrite["Chapter Writing"]
        ChapterAnalysis["Chapter Analysis System"]
        CharacterMgmt["Character & Relationship Management"]
        StyleMgmt["Writing Styles"]
    end
    
    subgraph "Frontend Components (frontend/src/pages/)"
        WizardUI["ProjectWizardNew.tsx"]
        InspirationUI["Inspiration.tsx"]
        OutlineUI["Outline.tsx"]
        ChapterUI["Chapters.tsx"]
        AnalysisUI["ChapterAnalysis.tsx"]
        CharacterUI["Characters.tsx<br/>Relationships.tsx<br/>Organizations.tsx"]
        StyleUI["WritingStyles.tsx"]
    end
    
    subgraph "Backend API Routes (backend/app/api/)"
        WizardAPI["wizard_stream.py<br/>/api/wizard-stream/*"]
        InspirationAPI["inspiration.py<br/>/api/inspiration/*"]
        OutlineAPI["outlines.py<br/>/api/outlines/*"]
        ChapterAPI["chapters.py<br/>/api/chapters/*"]
        CharacterAPI["characters.py<br/>/api/characters/*<br/>/api/relationships/*<br/>/api/organizations/*"]
        ProjectAPI["projects.py<br/>/api/projects/*"]
    end
    
    subgraph "Service Layer (backend/app/services/)"
        AIServiceLayer["ai_service.py<br/>AIService class"]
        PromptServiceLayer["prompt_service.py<br/>PromptService class"]
        PlotAnalyzerLayer["plot_analyzer.py<br/>PlotAnalyzer class"]
    end
    
    subgraph "Data Models (backend/app/models/)"
        ProjectModel["project.py<br/>Project"]
        OutlineModel["outline.py<br/>Outline"]
        ChapterModel["chapter.py<br/>Chapter"]
        CharacterModel["character.py<br/>Character<br/>CharacterRelationship<br/>Organization"]
        StyleModel["writing_style.py<br/>WritingStyle"]
        MemoryModel["memory.py<br/>Memory"]
    end
    
    ProjectWizard --> WizardUI
    InspirationMode --> InspirationUI
    OutlineMgmt --> OutlineUI
    ChapterWrite --> ChapterUI
    ChapterAnalysis --> AnalysisUI
    CharacterMgmt --> CharacterUI
    StyleMgmt --> StyleUI
    
    WizardUI --> WizardAPI
    InspirationUI --> InspirationAPI
    OutlineUI --> OutlineAPI
    ChapterUI --> ChapterAPI
    AnalysisUI --> ChapterAPI
    CharacterUI --> CharacterAPI
    StyleUI --> ProjectAPI
    
    WizardAPI --> AIServiceLayer
    InspirationAPI --> AIServiceLayer
    OutlineAPI --> AIServiceLayer
    ChapterAPI --> AIServiceLayer
    
    AIServiceLayer --> PromptServiceLayer
    ChapterAPI --> PlotAnalyzerLayer
    PlotAnalyzerLayer --> MemoryModel
    
    WizardAPI --> ProjectModel
    WizardAPI --> CharacterModel
    OutlineAPI --> OutlineModel
    ChapterAPI --> ChapterModel
    CharacterAPI --> CharacterModel
    ProjectAPI --> StyleModel
```

**Sources:** [backend/app/main.py:128-160](), [frontend/src/App.tsx:32-75](), [backend/app/services/ai_service.py:20-40](), [backend/app/services/plot_analyzer.py:15-30]()

### Feature Interaction Flow

```mermaid
sequenceDiagram
    participant User
    participant Wizard as "Project Wizard<br/>(wizard_stream.py)"
    participant Outline as "Outline Mgmt<br/>(outlines.py)"
    participant Chapter as "Chapter Writing<br/>(chapters.py)"
    participant Analyzer as "Plot Analyzer<br/>(plot_analyzer.py)"
    participant AI as "AIService"
    participant DB as "SQLite & ChromaDB"
    
    Note over User,DB: Complete Novel Creation Flow
    
    User->>Wizard: "Start wizard (step 0-3)"
    Wizard->>AI: "generate_world_building()"
    AI-->>Wizard: "World data (SSE stream)"
    Wizard->>DB: "Save to Project.world_*"
    
    Wizard->>AI: "generate_characters()"
    AI-->>Wizard: "Character list (SSE stream)"
    Wizard->>DB: "Save to Character table"
    
    User->>Outline: "Generate Expansion Plan"
    Outline->>AI: "generate_expansion_plan()"
    AI-->>Outline: "Scene breakdowns"
    Outline->>DB: "Save to Outline structure"
    
    User->>Chapter: "Generate chapter 1"
    Chapter->>AI: "generate_chapter(outline, characters)"
    AI-->>Chapter: "Chapter content (SSE stream)"
    Chapter->>DB: "Save to Chapter table"
    
    Chapter->>Analyzer: "Analyze Chapter 1"
    Analyzer->>AI: "extract_memories()"
    AI-->>Analyzer: "Plot points & character arcs"
    Analyzer->>DB: "Store in ChromaDB (Vector)"
    
    User->>Chapter: "Generate chapter 2"
    Chapter->>Analyzer: "query_relevant_memories()"
    Analyzer-->>Chapter: "Context from Chapter 1"
    Chapter->>AI: "generate_chapter(context, outline)"
    AI-->>Chapter: "Chapter 2 content"
    Chapter->>DB: "Save to Chapter table"
```

**Sources:** [backend/app/api/wizard_stream.py:20-60](), [backend/app/api/chapters.py:110-140](), [backend/app/services/plot_analyzer.py:40-80](), [backend/app/api/outlines.py:200-240]()

## Feature Details

### Project Creation Wizard
The wizard provides a 4-step guided process for initializing novel projects with AI assistance. It uses Server-Sent Events (SSE) to stream generation for world-building, characters, and initial outlines.
For details, see [Project Creation Wizard](#4.1).

**Sources:** [backend/app/api/wizard_stream.py:1-50](), [frontend/src/pages/ProjectWizardNew.tsx:1-100]()

### Inspiration Mode
A conversational alternative to the structured wizard. It allows users to iterate on ideas through a step-by-step dialogue with the AI, generating multiple options for themes, settings, and plots before finalizing a project.
For details, see [Inspiration Mode](#4.2).

**Sources:** [backend/app/api/inspiration.py:10-40](), [frontend/src/pages/Inspiration.tsx:1-50]()

### Outline Management
Supports the full lifecycle of story planning, including initial generation, manual CRUD operations, and reordering. It features two modes: one-to-one (simple chapter summaries) and one-to-many (detailed expansion).
For details, see [Outline Management](#4.3).

**Sources:** [backend/app/api/outlines.py:1-100](), [frontend/src/pages/Outline.tsx:1-100]()

### Outline Expansion System
The expansion system takes a high-level outline and breaks it down into a detailed "Expansion Plan." This plan includes scene-by-scene breakdowns, character appearances, and specific plot beats to guide precise chapter generation.
For details, see [Outline Expansion System](#4.4).

**Sources:** [backend/app/api/outlines.py:230-300](), [frontend/src/api/outline.ts:40-60]()

### Chapter Writing
The core generation engine for novel content. It supports streaming generation, batch generation for multiple chapters, and smart context building that incorporates world settings, characters, and previous plot points.
For details, see [Chapter Writing](#4.5).

**Sources:** [backend/app/api/chapters.py:100-250](), [frontend/src/pages/Chapters.tsx:1-150]()

### Chapter Analysis System
Powered by the `PlotAnalyzer`, this system automatically extracts key plot points, character developments, and "memories" from generated chapters. These are stored in a semantic vector database (ChromaDB) to maintain long-term narrative consistency.
For details, see [Chapter Analysis System](#4.6).

**Sources:** [backend/app/services/plot_analyzer.py:1-100](), [frontend/src/pages/ChapterAnalysis.tsx:1-80]()

### Character and Relationship Management
A comprehensive database for story actors. It manages detailed character profiles, complex multi-way relationships, and organizational hierarchies. It also features an auto-introduction system to track when characters first appear.
For details, see [Character and Relationship Management](#4.7).

**Sources:** [backend/app/api/characters.py:1-150](), [frontend/src/pages/Characters.tsx:1-100](), [frontend/src/pages/Relationships.tsx:1-50]()

### Writing Styles
Allows users to control the "voice" of the AI. It includes preset styles (e.g., Epic, Modern, Humorous) and allows for custom style creation by defining specific prompt instructions that are injected into the generation process.
For details, see [Writing Styles](#4.8).

**Sources:** [backend/app/models/writing_style.py:1-60](), [frontend/src/pages/WritingStyles.tsx:1-100]()

---

# Page: Project Creation Wizard

# Project Creation Wizard

<details>
<summary>Relevant source files</summary>

The following files were used as context for generating this wiki page:

- [backend/app/api/inspiration.py](backend/app/api/inspiration.py)
- [backend/app/api/wizard_stream.py](backend/app/api/wizard_stream.py)
- [backend/app/services/plot_expansion_service.py](backend/app/services/plot_expansion_service.py)
- [backend/app/services/prompt_service.py](backend/app/services/prompt_service.py)
- [frontend/src/components/AIProjectGenerator.tsx](frontend/src/components/AIProjectGenerator.tsx)
- [frontend/src/components/SSEProgressModal.tsx](frontend/src/components/SSEProgressModal.tsx)
- [frontend/src/pages/Inspiration.tsx](frontend/src/pages/Inspiration.tsx)
- [frontend/src/pages/ProjectWizardNew.tsx](frontend/src/pages/ProjectWizardNew.tsx)
- [frontend/src/pages/WorldSetting.tsx](frontend/src/pages/WorldSetting.tsx)

</details>



## Purpose and Scope

The Project Creation Wizard provides a structured interface for creating new novel projects with AI-guided generation of world-building, characters, and outlines. Users fill out a form with basic project information (title, description, theme, genre, etc.), and the system automatically generates a complete project setup through three sequential phases using Server-Sent Events (SSE) for real-time progress updates.

This document covers the **structured form-based wizard** (`/wizard` route). For the alternative conversational AI-assisted creation mode, see [Inspiration Mode](4.2). For details on outline generation and expansion, see [Outline Management](4.3) and [Outline Expansion System](4.4).

**Sources**: [frontend/src/pages/ProjectWizardNew.tsx:1-388](), [backend/app/api/wizard_stream.py:1-26]()

---

## System Architecture

### Component Overview

The wizard architecture bridges the React frontend components with FastAPI backend generators through a specialized SSE streaming layer.

```mermaid
graph TB
    subgraph "Frontend Components"
        WizardForm["ProjectWizardNew<br/>(Form Page)"]
        AIGenerator["AIProjectGenerator<br/>(Orchestrator)"]
        ProgressModal["SSEProgressModal<br/>(Progress Display)"]
        SSEClient["wizardStreamApi<br/>(SSE Client)"]
    end
    
    subgraph "Backend API Routes"
        WorldRoute["/wizard-stream/world-building<br/>POST"]
        CharRoute["/wizard-stream/characters<br/>POST"]
        OutlineRoute["/wizard-stream/complete-outline<br/>POST"]
    end
    
    subgraph "Backend Generators"
        WorldGen["world_building_generator()<br/>AsyncGenerator"]
        CharGen["characters_generator()<br/>AsyncGenerator"]
        OutlineGen["complete_outline_generator()<br/>AsyncGenerator"]
    end
    
    subgraph "Core Services"
        AIService["AIService<br/>generate_text_stream()"]
        PromptService["PromptService<br/>get_template()"]
    end
    
    subgraph "Data Layer"
        DB[(PostgreSQL)]
        Project["Project<br/>wizard_step"]
        Character["Character"]
        Outline["Outline"]
    end
    
    WizardForm -->|1. Submit Form| AIGenerator
    AIGenerator -->|2. Call SSE APIs| SSEClient
    SSEClient -->|3. HTTP SSE| WorldRoute
    SSEClient -->|4. HTTP SSE| CharRoute
    SSEClient -->|5. HTTP SSE| OutlineRoute
    
    WorldRoute --> WorldGen
    CharRoute --> CharGen
    OutlineRoute --> OutlineGen
    
    WorldGen --> PromptService
    WorldGen --> AIService
    CharGen --> PromptService
    CharGen --> AIService
    OutlineGen --> PromptService
    OutlineGen --> AIService
    
    WorldGen -->|Save| Project
    CharGen -->|Save| Character
    OutlineGen -->|Save| Outline
    
    Project --> DB
    Character --> DB
    Outline --> DB
    
    AIGenerator -->|6. Display Progress| ProgressModal
```

**Sources**: [frontend/src/pages/ProjectWizardNew.tsx:16-103](), [backend/app/api/wizard_stream.py:25-287](), [frontend/src/components/AIProjectGenerator.tsx:1-54]()

### Key Code Entities

| Component | File | Key Entities | Responsibility |
|-----------|------|-------------|----------------|
| **Frontend Form** | `ProjectWizardNew.tsx` | `ProjectWizardNew`, `GenerationConfig` | Collect user input, validate form [frontend/src/pages/ProjectWizardNew.tsx:16-119]() |
| **Generation Orchestrator** | `AIProjectGenerator.tsx` | `AIProjectGenerator`, `GenerationSteps` | Coordinate three-phase workflow [frontend/src/components/AIProjectGenerator.tsx:48-73]() |
| **SSE Client** | `api.ts` | `wizardStreamApi` | Handle SSE connections, parse events [frontend/src/components/AIProjectGenerator.tsx:5-5]() |
| **Backend Router** | `wizard_stream.py` | `router`, `@router.post()` | Define SSE endpoints [backend/app/api/wizard_stream.py:25-25]() |
| **World Generator** | `wizard_stream.py` | `world_building_generator()` | Phase 1: Generate world settings [backend/app/api/wizard_stream.py:29-33]() |
| **Character Generator** | `wizard_stream.py` | `characters_generator()` | Phase 2: Generate characters [backend/app/api/wizard_stream.py:289-293]() |
| **Outline Generator** | `wizard_stream.py` | `complete_outline_generator()` | Phase 3: Generate outlines [backend/app/api/wizard_stream.py:861-865]() |
| **SSE Progress UI** | `SSEProgressModal.tsx` | `SSEProgressModal` | Unified progress display component [frontend/src/components/SSEProgressModal.tsx:20-29]() |

**Sources**: [frontend/src/pages/ProjectWizardNew.tsx:1-119](), [frontend/src/components/AIProjectGenerator.tsx:1-73](), [backend/app/api/wizard_stream.py:1-865]()

---

## Three-Phase Generation Workflow

### Workflow Sequence

The generation follows a strict sequence: World -> Characters -> Outline. Each phase updates the `wizard_step` in the database to support resumption.

```mermaid
sequenceDiagram
    participant User
    participant Form as ProjectWizardNew
    participant Gen as AIProjectGenerator
    participant SSE as wizardStreamApi
    participant API as wizard_stream.py
    participant AI as AIService
    participant DB as PostgreSQL
    
    rect rgb(240, 248, 255)
        Note over User,DB: Phase 1: World Building
        User->>Form: Fill form & submit
        Form->>Gen: GenerationConfig
        Gen->>SSE: generateWorldBuildingStream()
        SSE->>API: POST /wizard-stream/world-building
        
        API->>AI: PromptService.get_template("WORLD_BUILDING")
        API->>AI: generate_text_stream(world_prompt)
        
        loop Streaming
            AI-->>API: Content chunks
            API-->>SSE: SSE events (progress, chunk)
            SSE-->>Gen: onProgress(), onResult()
        end
        
        API->>DB: INSERT Project (wizard_step=1)
        API-->>SSE: Result with project_id
    end
    
    rect rgb(240, 255, 240)
        Note over User,DB: Phase 2: Characters
        Gen->>SSE: generateCharactersStream()
        SSE->>API: POST /wizard-stream/characters
        
        API->>AI: generate_text_stream(batch_prompt)
        AI-->>API: Character JSON
        
        API->>DB: INSERT Characters + Relationships
        API->>DB: UPDATE Project (wizard_step=2)
        API-->>SSE: Result with characters[]
    end
    
    rect rgb(255, 248, 240)
        Note over User,DB: Phase 3: Outline
        Gen->>SSE: generateCompleteOutlineStream()
        SSE->>API: POST /wizard-stream/complete-outline
        
        API->>AI: generate_text_stream(outline_prompt)
        AI-->>API: Outline JSON
        API->>DB: INSERT Outline
        
        API->>DB: UPDATE Project (wizard_step=3)
        API-->>SSE: Result with outlines[]
        Gen->>User: Navigate to /project/:id
    end
```

**Sources**: [frontend/src/components/AIProjectGenerator.tsx:106-183](), [backend/app/api/wizard_stream.py:29-255](), [backend/app/api/wizard_stream.py:289-858](), [backend/app/api/wizard_stream.py:861-1529]()

### Phase Progression Table

| Phase | Route | Generator Function | Progress Range | Database Changes | `wizard_step` |
|-------|-------|-------------------|----------------|-----------------|-------------|
| **World Building** | `/wizard-stream/world-building` | `world_building_generator()` | 0-33% | Create `Project`, set world fields [backend/app/api/wizard_stream.py:238-241]() | 0 → 1 |
| **Characters** | `/wizard-stream/characters` | `characters_generator()` | 33-66% | Create `Character`, `Relationship`, `Organization` [backend/app/api/wizard_stream.py:806-810]() | 1 → 2 |
| **Outline** | `/wizard-stream/complete-outline` | `complete_outline_generator()` | 66-100% | Create `Outline`, optionally `Chapter` [backend/app/api/wizard_stream.py:1471-1475]() | 2 → 3 |

**Sources**: [backend/app/api/wizard_stream.py:29-1529](), [frontend/src/components/AIProjectGenerator.tsx:150-175]()

---

## Frontend Implementation

### ProjectWizardNew Component

The entry point is a form-based page that collects project metadata using Ant Design components.

**Key Form Fields**:
- **outline_mode**: `'one-to-one' | 'one-to-many'` - Determines if outlines are 1:1 with chapters or expanded later [frontend/src/pages/ProjectWizardNew.tsx:189-249]().
- **genre**: `Select mode="tags"` - Allows multiple genre tags [frontend/src/pages/ProjectWizardNew.tsx:163-186]().
- **character_count**: `InputNumber` - Number of characters to generate [frontend/src/pages/ProjectWizardNew.tsx:251-262]().

**Sources**: [frontend/src/pages/ProjectWizardNew.tsx:107-319]()

### AIProjectGenerator Component

The orchestrator component manages the three-phase workflow with state tracking and localStorage persistence.

**State Management**:
```typescript
interface GenerationSteps {
  worldBuilding: GenerationStep;  // 'pending' | 'processing' | 'completed' | 'error'
  careers: GenerationStep;
  characters: GenerationStep;
  outline: GenerationStep;
}
```
[frontend/src/components/AIProjectGenerator.tsx:33-38]()

**Key Methods**:
- `handleAutoGenerate()`: Starts a new project generation [frontend/src/components/AIProjectGenerator.tsx:308-315]().
- `handleResumeGenerate()`: Resumes incomplete projects by checking `wizard_step` [frontend/src/components/AIProjectGenerator.tsx:120-192]().
- `saveProgress()`: Persists `project_id` and `GenerationConfig` to `localStorage` [frontend/src/components/AIProjectGenerator.tsx:88-96]().

**Sources**: [frontend/src/components/AIProjectGenerator.tsx:48-192]()

---

## Backend Generator Implementation

### World Building Generator

**Function**: `world_building_generator()` [backend/app/api/wizard_stream.py:29-33]()

The generator uses the `WORLD_BUILDING` prompt template which follows the **RTCO (Role, Task, Constraints, Output)** framework.

1. **Prompt Construction**: Fetches template and formats it with user input (title, theme, genre, description) [backend/app/api/wizard_stream.py:65-72]().
2. **Streaming**: Calls `user_ai_service.generate_text_stream()` [backend/app/api/wizard_stream.py:103-108]().
3. **JSON Cleaning**: Uses `_clean_json_response()` to strip markdown markers before parsing [backend/app/api/wizard_stream.py:156-160]().
4. **Data Model**: Saves results into `Project` model fields: `world_time_period`, `world_location`, `world_atmosphere`, `world_rules` [backend/app/api/wizard_stream.py:238-241]().

**Sources**: [backend/app/api/wizard_stream.py:29-269](), [backend/app/services/prompt_service.py:77-191]()

### Characters Generator

**Function**: `characters_generator()` [backend/app/api/wizard_stream.py:289-293]()

Generates characters and organizations in batches (default size 3) to manage context window and reliability.

1. **Batch Loop**: Iterates until `character_count` is reached [backend/app/api/wizard_stream.py:384-386]().
2. **Relationship Network**: Uses `CHARACTERS_BATCH_GENERATION` template which requires AI to link new characters to existing ones in the batch [backend/app/services/prompt_service.py:193-317]().
3. **Validation**: Strictly validates that the returned JSON array matches the requested batch size [backend/app/api/wizard_stream.py:534-540]().
4. **Relationship Storage**: Creates `CharacterRelationship` and `OrganizationMember` records after entities are flushed to the DB [backend/app/api/wizard_stream.py:719-798]().

**Sources**: [backend/app/api/wizard_stream.py:289-858](), [backend/app/services/prompt_service.py:193-317]()

### Complete Outline Generator

**Function**: `complete_outline_generator()` [backend/app/api/wizard_stream.py:861-865]()

Generates the initial narrative structure.

1. **Prompt Construction**: Includes the generated world-view and character list to ensure narrative consistency [backend/app/api/wizard_stream.py:1003-1015]().
2. **Outline Mode Logic**: 
   - If `one-to-one`, it creates a `Chapter` for every `Outline` [backend/app/api/wizard_stream.py:1416-1430]().
   - If `one-to-many`, it only creates `Outline` nodes [backend/app/api/wizard_stream.py:1432-1433]().

**Sources**: [backend/app/api/wizard_stream.py:861-1529](), [backend/app/services/prompt_service.py:319-354]()

---

## Error Handling and Retry

### SSE Progress Modal

The `SSEProgressModal` provides visual feedback during the long-running generation process. It displays a progress bar, status messages, and an optional cancel button [frontend/src/components/SSEProgressModal.tsx:20-29]().

### Smart Retry

The `AIProjectGenerator` includes logic to resume from the last failed step. If a project creation fails during the "Characters" phase, the user can trigger a retry that skips "World Building" (already saved in DB) and restarts from the character generation step [frontend/src/components/AIProjectGenerator.tsx:150-175]().

**Sources**: [frontend/src/components/SSEProgressModal.tsx:1-151](), [frontend/src/components/AIProjectGenerator.tsx:120-192]()

---

# Page: Inspiration Mode

# Inspiration Mode

<details>
<summary>Relevant source files</summary>

The following files were used as context for generating this wiki page:

- [backend/app/api/inspiration.py](backend/app/api/inspiration.py)
- [backend/app/services/plot_expansion_service.py](backend/app/services/plot_expansion_service.py)
- [frontend/src/components/AIProjectGenerator.tsx](frontend/src/components/AIProjectGenerator.tsx)
- [frontend/src/components/SSEProgressModal.tsx](frontend/src/components/SSEProgressModal.tsx)
- [frontend/src/pages/Inspiration.tsx](frontend/src/pages/Inspiration.tsx)
- [frontend/src/pages/ProjectWizardNew.tsx](frontend/src/pages/ProjectWizardNew.tsx)

</details>



This document describes the Inspiration Mode feature, a conversational AI-guided project creation workflow that uses a chat-style interface to collect project information through step-by-step dialogue.

**Scope**: This page covers the conversational project creation interface, AI-powered option generation, conversation caching, and the integration with the project generation pipeline. For the structured form-based project creation, see [Project Creation Wizard](4.1). Both modes share the same `AIProjectGenerator` component for the final generation phase.

---

## Overview

Inspiration Mode provides an alternative project creation workflow that guides users through a natural conversation. Unlike the wizard's structured forms, this mode:

- Presents one question at a time in a chat interface.
- AI generates 3-6 contextual options at each step using the `inspirationApi`.
- Users can select options or input custom values via a `TextArea`.
- Conversation state persists in `localStorage` for 24 hours.
- Supports automatic retry on AI generation failures with a `max_retries` limit of 3.
- Eventually delegates to the same `AIProjectGenerator` used by the wizard.

**Key difference from Project Wizard**: The wizard collects all information upfront in a single form, while Inspiration Mode builds context progressively through conversation, making the AI suggestions more relevant at each step.

---

## Architecture Overview

The following diagram shows the high-level architecture and data flow between the React frontend and FastAPI backend.

### System Interaction Diagram

```mermaid
graph TB
    subgraph "Frontend - Inspiration.tsx"
        ChatUI["Chat Interface<br/>(Messages + Options)"]
        StateManager["StateManager<br/>(currentStep, wizardData)"]
        CacheManager["CacheManager<br/>(localStorage: CACHE_KEY)"]
    end
    
    subgraph "Backend - inspiration.py"
        GenerateOptionsEndpoint["/inspiration/generate-options"]
        TemplateSystem["Prompt Template System<br/>(INSPIRATION_TITLE_SYSTEM, etc.)"]
        ValidationLayer["validate_options_response()"]
        RetryMechanism["Retry Logic<br/>(max_retries=3)"]
    end
    
    subgraph "AI Service Layer"
        AIService["AIService<br/>(generate_text_stream)"]
        PromptService["PromptService<br/>(get_template)"]
    end
    
    subgraph "Shared Generation"
        AIProjectGenerator["AIProjectGenerator<br/>(Shared Component)"]
    end
    
    ChatUI --> StateManager
    StateManager --> CacheManager
    StateManager -->|inspirationApi.generateOptions| GenerateOptionsEndpoint
    
    GenerateOptionsEndpoint --> TemplateSystem
    GenerateOptionsEndpoint --> ValidationLayer
    GenerateOptionsEndpoint --> RetryMechanism
    
    TemplateSystem --> PromptService
    RetryMechanism --> AIService
    ValidationLayer -->|Valid| StateManager
    ValidationLayer -->|Invalid| RetryMechanism
    
    StateManager -->|Confirm Creation| AIProjectGenerator
```

**Sources**: [frontend/src/pages/Inspiration.tsx:5-50](), [backend/app/api/inspiration.py:13-25](), [frontend/src/components/AIProjectGenerator.tsx:48-54]()

---

## Conversation Step Flow

The conversation progresses through a fixed sequence of steps defined in the `Step` type, collecting project information incrementally.

```mermaid
graph LR
    Idea["idea<br/>(Initial concept)"]
    Title["title<br/>(Book name)<br/>temp=0.8"]
    Description["description<br/>(Synopsis)<br/>temp=0.65"]
    Theme["theme<br/>(Theme)<br/>temp=0.55"]
    Genre["genre<br/>(Types)<br/>temp=0.45"]
    Perspective["perspective<br/>(Narrative POV)"]
    OutlineMode["outline_mode<br/>(1-to-1 or 1-to-N)"]
    Confirm["confirm<br/>(Review)"]
    Generating["generating<br/>(AIProjectGenerator)"]
    Complete["complete<br/>(Navigate)"]
    
    Idea -->|AI generates titles| Title
    Title -->|AI generates descriptions| Description
    Description -->|AI generates themes| Theme
    Theme -->|AI generates genres| Genre
    Genre -->|Predefined| Perspective
    Perspective -->|Predefined| OutlineMode
    OutlineMode -->|Summary| Confirm
    Confirm -->|Confirm| Generating
    Generating -->|Success| Complete
```

**Temperature Strategy**: The backend `TEMPERATURE_SETTINGS` map defines a decreasing temperature from 0.8 (creative titles) to 0.45 (specific genres) to maintain consistency with previously selected values.

**Sources**: [frontend/src/pages/Inspiration.tsx:11-11](), [backend/app/api/inspiration.py:18-23]()

---

## Data Model

### Message Interface
The `Message` interface defines the structure of each chat bubble in the UI.

```typescript
interface Message {
  type: 'ai' | 'user';
  content: string;
  options?: string[];
  isMultiSelect?: boolean;
  optionsDisabled?: boolean; // Marks options as used
  canRefine?: boolean;      // Supports multi-turn refinement
  step?: Step;              // Tracks step for feedback
}
```
**Sources**: [frontend/src/pages/Inspiration.tsx:13-21]()

### WizardData and Cache
The `WizardData` interface stores the accumulated project configuration, while `CacheData` wraps it for persistent storage.

```typescript
interface WizardData {
  title: string;
  description: string;
  theme: string;
  genre: string[];
  narrative_perspective: string;
  outline_mode: 'one-to-one' | 'one-to-many';
}

interface CacheData {
  messages: Message[];
  currentStep: Step;
  wizardData: Partial<WizardData>;
  initialIdea: string;
  selectedOptions: string[];
  timestamp: number;
}
```
**Sources**: [frontend/src/pages/Inspiration.tsx:23-44]()

---

## Cache Management Implementation

Caching is handled via `localStorage` with a 24-hour expiry (`CACHE_EXPIRY`).

| Function | Logic |
| :--- | :--- |
| `saveToCache` | Saves current state if `currentStep` is not 'generating' or 'complete'. |
| `restoreFromCache` | Validates `timestamp` against `CACHE_EXPIRY` before restoring state. |
| `clearCache` | Removes `CACHE_KEY` from `localStorage`. |

**Auto-save Trigger**: A `useEffect` hook monitors state changes and executes a debounced `saveToCache` every 500ms.

**Sources**: [frontend/src/pages/Inspiration.tsx:47-49](), [frontend/src/pages/Inspiration.tsx:117-188](), [frontend/src/pages/Inspiration.tsx:201-210]()

---

## Backend Implementation

### API Endpoint: `/inspiration/generate-options`

This endpoint (`router.post("/generate-options")`) is the core of the conversational intelligence. It performs the following steps:

1.  **Template Mapping**: Maps the current `step` to specific prompt keys (e.g., `INSPIRATION_TITLE_SYSTEM` and `INSPIRATION_TITLE_USER`).
2.  **Prompt Formatting**: Uses `PromptService.get_template` and formats it with existing `context` (previous selections).
3.  **AI Invocation**: Calls `ai_service.generate_text_stream` with the step-specific temperature.
4.  **Response Cleaning**: Uses `ai_service._clean_json_response` to handle potential Markdown artifacts in AI output.
5.  **Validation**: `validate_options_response` ensures the AI returned a valid JSON array with 3-10 options.

**Sources**: [backend/app/api/inspiration.py:69-172](), [backend/app/api/inspiration.py:26-66]()

### Validation Thresholds
- **Options Count**: Minimum 3, Maximum 10.
- **Option Length**: Maximum 500 characters.
- **Genre Constraints**: Tags must be between 2-10 characters.

**Sources**: [backend/app/api/inspiration.py:44-64]()

---

## Integration with Project Generation

Once the conversation reaches the `confirm` step and the user selects "确认创建", the `Inspiration` component mounts the `AIProjectGenerator`.

### Transition Logic

```mermaid
sequenceDiagram
    participant I as Inspiration.tsx
    participant A as AIProjectGenerator.tsx
    participant W as wizardStreamApi
    
    I->>I: clearCache()
    I->>I: setGenerationConfig(wizardData)
    I->>A: Render <AIProjectGenerator config={...} />
    A->>W: generateWorldBuildingStream()
    W-->>A: SSE Stream (World Data)
    A->>W: generateCharactersStream()
    W-->>A: SSE Stream (Characters)
    A->>W: generateOutlineStream()
    W-->>A: SSE Stream (Outline)
    A->>I: onComplete(projectId)
```

**Sources**: [frontend/src/pages/Inspiration.tsx:420-451](), [frontend/src/components/AIProjectGenerator.tsx:198-230]()

### Shared Component Usage
The `AIProjectGenerator` accepts a `storagePrefix` prop (set to `'inspiration'` here) to isolate its own generation progress in `localStorage` from the standard Wizard mode.

**Sources**: [frontend/src/components/AIProjectGenerator.tsx:22-29](), [frontend/src/components/AIProjectGenerator.tsx:81-85]()

---

## Error Handling and Recovery

### Retry Mechanism
The backend includes a `max_retries = 3` loop. If validation fails, it appends a warning to the `system_prompt` emphasizing the JSON format for the next attempt. If all retries fail, it returns a fallback response allowing manual input.

**Sources**: [backend/app/api/inspiration.py:95-144](), [backend/app/api/inspiration.py:181-185]()

### Frontend Recovery
The frontend tracks `lastFailedRequest`. If an error occurs, the UI displays a "重新生成" (Retry) button which calls `handleRetry`, re-invoking the API with the saved context.

**Sources**: [frontend/src/pages/Inspiration.tsx:96-99](), [frontend/src/pages/Inspiration.tsx:230-249]()

---

# Page: Outline Management

# Outline Management

<details>
<summary>Relevant source files</summary>

The following files were used as context for generating this wiki page:

- [backend/app/api/outlines.py](backend/app/api/outlines.py)
- [backend/app/schemas/outline.py](backend/app/schemas/outline.py)
- [frontend/src/pages/Outline.tsx](frontend/src/pages/Outline.tsx)
- [frontend/src/services/api.ts](frontend/src/services/api.ts)
- [frontend/src/types/index.ts](frontend/src/types/index.ts)

</details>



## Purpose and Scope

This document covers the Outline Management subsystem, which handles the creation, editing, AI-assisted generation, and expansion of story outlines. The system supports two distinct operational modes:

- **One-to-One Mode** (Traditional): Each outline corresponds to exactly one chapter.
- **One-to-Many Mode** (Expansion): Each outline serves as a plot summary that can be expanded into multiple detailed chapters.

Outlines define the high-level structure of a novel project. In one-to-many mode, they act as logical containers for a sequence of events that the `PlotExpansionService` later breaks down into specific chapter plans.

For information about AI-generated chapter prose, see [Chapter Writing (4.5)](). For outline expansion logic, see [Outline Expansion System (4.4)](). For project-level settings, see [Project Creation Wizard (4.1)]().

---

## Data Model and Relationships

The `Outline` entity represents a high-level structural element. Its relationship with the `Chapter` entity is governed by the project's `outline_mode`.

### Dual-Mode Relationship Architecture

```mermaid
erDiagram
    "Project" ||--|{ "Outline" : "has"
    "Project" ||--|{ "Chapter" : "has"
    "Project" {
        string id PK
        string outline_mode "one-to-one | one-to-many"
    }
    
    "Outline" {
        string id PK
        string project_id FK
        int order_index
        string title
        string content
        json structure "Parsed AI data"
    }
    
    "Chapter" {
        string id PK
        string project_id FK
        string outline_id FK "Nullable"
        int chapter_number
        int sub_index
        string status "pending | writing | completed"
    }
    
    "Outline" ||--o{ "Chapter" : "one-to-many: references outline_id"
    "Outline" ||--o| "Chapter" : "one-to-one: matched by order_index"
```

**Sources**: [backend/app/models/outline.py:1-30](), [backend/app/models/chapter.py:1-40](), [backend/app/api/outlines.py:75-87]()

### Implementation Details by Mode

| Feature | One-to-One Mode | One-to-Many Mode |
| :--- | :--- | :--- |
| **Chapter Creation** | Auto-created during `create_outline` [backend/app/api/outlines.py:75-87]() | Created via Expansion System [backend/app/api/outlines.py:1181-1201]() |
| **Mapping Key** | `Outline.order_index` == `Chapter.chapter_number` | `Chapter.outline_id` FK |
| **Syncing** | Updates to Outline title/content sync to Chapter [backend/app/api/outlines.py:237-256]() | Chapters are independent plans [backend/app/api/outlines.py:200-235]() |
| **`outline_id` FK** | Usually `NULL` | Required for association |

**Sources**: [backend/app/api/outlines.py:58-91](), [backend/app/api/outlines.py:193-260]()

---

## Outline CRUD Operations

### API Structure

The `router` in `backend/app/api/outlines.py` handles the lifecycle of outline entities.

```mermaid
graph TD
    subgraph "Frontend: Outline.tsx"
        UI["Outline Component"]
        Sync["useOutlineSync() Hook"]
    end

    subgraph "Backend: outlines.py"
        GET["GET /outlines"]
        POST["POST /outlines"]
        PUT["PUT /outlines/{id}"]
        DELETE["DELETE /outlines/{id}"]
    end

    UI --> Sync
    Sync --> GET
    Sync --> POST
    POST -->|"one-to-one"| AC["Auto-create Chapter"]
    Sync --> PUT
    Sync --> DELETE
```

**Sources**: [backend/app/api/outlines.py:39-40](), [frontend/src/pages/Outline.tsx:172-176]()

### Optimized List Retrieval
The `get_outlines` endpoint [backend/app/api/outlines.py:94-158]() performs a "Deep Parse" of the `structure` JSON field. It extracts `title` and `summary` from the JSON to ensure the UI has the most up-to-date AI-generated fields without extra frontend processing. It also performs a batch query to check `has_chapters` status for each outline to avoid N+1 query issues in the frontend [backend/app/api/outlines.py:119-132]().

### Update Logic
When updating an outline via `update_outline` [backend/app/api/outlines.py:193-260](), the system:
1. Updates the `Outline` record.
2. Synchronizes the `structure` JSON field with the new `title` and `content` [backend/app/api/outlines.py:220-235]().
3. In `one-to-one` mode, it locates the corresponding `Chapter` (by `order_index`) and updates its title and summary [backend/app/api/outlines.py:237-256]().

**Sources**: [backend/app/api/outlines.py:94-158](), [backend/app/api/outlines.py:193-260]()

---

## AI Generation and Continuation

The system provides streaming generation via Server-Sent Events (SSE). It supports three primary modes: `new` (fresh start), `continue` (append to existing), and `auto` (intelligent selection).

### Generation Logic Flow

```mermaid
sequenceDiagram
    participant FE as "Outline.tsx (SSEPostClient)"
    participant BE as "outlines.py (generate_outline_stream)"
    participant AI as "AIService"
    participant MCP as "MCPToolService"
    participant DB as "SQLite (get_db)"

    FE->>BE: POST /generate-stream (mode="continue")
    BE->>DB: Load Project & Existing Outlines
    BE->>BE: build_smart_outline_context()
    
    alt Character Prediction Enabled
        BE->>AI: Predict new characters needed?
        AI-->>BE: Predicted Characters JSON
        BE-->>FE: SSE event: "character_confirmation_required"
        Note over FE: User confirms characters in Modal
    end

    loop Batch Processing (5 chapters/batch)
        BE->>MCP: Get reference materials (if enabled)
        BE->>AI: generate_text (Prompt + Context)
        AI-->>BE: JSON Outline Batch
        BE->>DB: _save_outlines()
        BE-->>FE: SSE event: "progress"
    end
    
    BE-->>FE: SSE event: "result"
```

**Sources**: [backend/app/api/outlines.py:1451-1480](), [backend/app/api/outlines.py:1944-2010](), [frontend/src/utils/sseClient.ts]()

### Smart Context Building
To handle large projects, `build_smart_outline_context` [backend/app/api/outlines.py:643-726]() implements a sampling strategy:
- **Story Skeleton**: Includes every 50th outline for long-range context [backend/app/api/outlines.py:683-694]().
- **Recent Summary**: Includes the last 20 outlines with titles and partial summaries [backend/app/api/outlines.py:696-707]().
- **Recent Detail**: Includes the full content of the last 2 outlines [backend/app/api/outlines.py:709-715]().

**Sources**: [backend/app/api/outlines.py:643-726]()

### Character Prediction and Confirmation
During continuation, the `auto_character_service` analyzes the plot direction to see if new characters should be introduced [backend/app/api/outlines.py:1614-1640]().
- If the AI suggests new characters, the backend yields a `character_confirmation_required` event [backend/app/api/outlines.py:1648-1658]().
- The frontend `Outline.tsx` catches this, pauses the generation, and displays a confirmation modal [frontend/src/pages/Outline.tsx:270-283]().
- Once confirmed, the characters are created, and the generation resumes [frontend/src/pages/Outline.tsx:1595-1650]().

**Sources**: [backend/app/api/outlines.py:1614-1658](), [frontend/src/pages/Outline.tsx:270-283]()

---

## Outline Expansion (One-to-Many)

The expansion system transforms a single `Outline` into multiple `ChapterPlanItem` objects.

### Expansion Strategies
Users can select strategies that influence the `PlotExpansionService` [backend/app/schemas/outline.py:95-103]():
- `balanced`: Even distribution of plot points.
- `climax`: Focuses more chapters on high-tension events.
- `detail`: Maximizes world-building and character interaction details.

### The Expansion Preview Flow
1. **Request**: `POST /outlines/{id}/expand-stream` [backend/app/api/outlines.py:2013-2161]().
2. **AI Generation**: AI returns a list of chapter plans containing `plot_summary`, `key_events`, `scenes`, and `emotional_tone` [backend/app/schemas/outline.py:81-93]().
3. **Preview**: The frontend displays these plans in the `ExpansionPlanEditor` [frontend/src/pages/Outline.tsx:1095-1189]().
4. **Commit**: Upon user confirmation, `create-chapters-from-plans` [backend/app/api/outlines.py:2262-2308]() is called to persist the `Chapter` records.

**Sources**: [backend/app/api/outlines.py:2013-2161](), [backend/app/api/outlines.py:2262-2308](), [backend/app/schemas/outline.py:81-113]()

---

## Technical Components Summary

### Backend Classes and Models
| Symbol | File | Role |
| :--- | :--- | :--- |
| `Outline` | [backend/app/models/outline.py:10-30]() | Database model for story outlines. |
| `OutlineGenerateRequest` | [backend/app/schemas/outline.py:45-65]() | Pydantic schema for AI generation parameters. |
| `ChapterPlanItem` | [backend/app/schemas/outline.py:81-93]() | Schema for a single chapter's detailed expansion plan. |
| `WizardProgressTracker` | [backend/app/utils/sse_response.py]() | Tracks and emits SSE progress percentages. |

### Frontend Functions
| Symbol | File | Role |
| :--- | :--- | :--- |
| `parseOutlineStructure` | [frontend/src/pages/Outline.tsx:98-106]() | Safely parses the `structure` JSON from the backend. |
| `handleGenerateOutline` | [frontend/src/pages/Outline.tsx:223-300]() | Initiates the SSE connection for outline generation. |
| `handleConfirmBatchCreate` | [frontend/src/pages/Outline.tsx:1535-1593]() | Finalizes batch chapter creation from expanded plans. |

**Sources**: [backend/app/models/outline.py](), [backend/app/schemas/outline.py](), [frontend/src/pages/Outline.tsx]()

---

# Page: Outline Expansion System

# Outline Expansion System

<details>
<summary>Relevant source files</summary>

The following files were used as context for generating this wiki page:

- [backend/app/api/inspiration.py](backend/app/api/inspiration.py)
- [backend/app/api/outlines.py](backend/app/api/outlines.py)
- [backend/app/schemas/outline.py](backend/app/schemas/outline.py)
- [backend/app/services/plot_expansion_service.py](backend/app/services/plot_expansion_service.py)
- [frontend/src/components/AIProjectGenerator.tsx](frontend/src/components/AIProjectGenerator.tsx)
- [frontend/src/components/SSEProgressModal.tsx](frontend/src/components/SSEProgressModal.tsx)
- [frontend/src/pages/Inspiration.tsx](frontend/src/pages/Inspiration.tsx)
- [frontend/src/pages/Outline.tsx](frontend/src/pages/Outline.tsx)
- [frontend/src/pages/ProjectWizardNew.tsx](frontend/src/pages/ProjectWizardNew.tsx)

</details>



## Purpose and Scope

The Outline Expansion System enables users to transform high-level outlines into detailed, multi-chapter content in projects using the **one-to-many** outline mode. Instead of each outline corresponding to a single chapter (one-to-one mode), this system allows a single outline to be expanded into 1–10 detailed chapters with specific plot elements, character focus, emotional tones, and scene breakdowns.

This system implements a **two-phase workflow**: first, AI generates chapter plans with preview capability via Server-Sent Events (SSE); second, after user confirmation, chapters are created in the database. The expansion process supports batch generation for large expansions (>5 chapters) and enforces sequential expansion to maintain chapter numbering consistency.

Sources: [backend/app/models/project.py:15-30](), [backend/app/schemas/outline.py:95-125](), [backend/app/services/plot_expansion_service.py:24-36]()

---

## System Architecture

The expansion system bridges the gap between high-level plot nodes and individual chapter records.

### Logic Flow and Code Entities

```mermaid
graph TB
    subgraph "Frontend - Outline.tsx"
        UI["Outline List UI"]
        ExpandBtn["Expand Button<br/>(handleExpandOutline)"]
        ConfigForm["Expansion Form<br/>target_chapter_count<br/>expansion_strategy"]
        SSEModal["SSEProgressModal"]
        PreviewModal["Expansion Preview Modal"]
        ConfirmBtn["Confirm Button<br/>(handleConfirmExpansion)"]
    end
    
    subgraph "Backend API - outlines.py"
        ExpandStream["/api/outlines/{outline_id}/expand-stream<br/>(SSE Endpoint)"]
        CreateChaptersAPI["/api/outlines/{outline_id}/create-chapters<br/>(POST)"]
    end
    
    subgraph "Service Layer - plot_expansion_service.py"
        PlotExpansionService["PlotExpansionService"]
        AnalyzeMethod["analyze_outline_for_chapters()"]
        BatchMethod["_generate_chapters_in_batches()"]
        SingleBatch["_generate_chapters_single_batch()"]
        ContextMethod["_get_outline_context()"]
    end
    
    subgraph "AI Integration"
        AIService["AIService"]
        PromptService["PromptService<br/>OUTLINE_EXPAND_SINGLE<br/>OUTLINE_EXPAND_MULTI"]
    end
    
    subgraph "Database Models"
        OutlineTable[("Outline Model<br/>structure: JSON string")]
        ChapterTable[("Chapter Model<br/>expansion_plan: JSON string")]
    end
    
    UI --> ExpandBtn
    ExpandBtn --> ConfigForm
    ConfigForm -->|SSE Request| ExpandStream
    ExpandStream --> PlotExpansionService
    PlotExpansionService --> AnalyzeMethod
    AnalyzeMethod --> BatchMethod
    AnalyzeMethod --> SingleBatch
    SingleBatch --> AIService
    BatchMethod --> AIService
    AIService --> PromptService
    
    ExpandStream -->|Stream Progress| SSEModal
    ExpandStream -->|Return Plans| PreviewModal
    PreviewModal --> ConfirmBtn
    ConfirmBtn --> CreateChaptersAPI
    CreateChaptersAPI --> ChapterTable
    
    AnalyzeMethod --> OutlineTable
```

Sources: [backend/app/api/outlines.py:1200-1250](), [backend/app/services/plot_expansion_service.py:18-84](), [frontend/src/pages/Outline.tsx:628-812]()

---

## Two-Phase Workflow

The expansion process follows a strict two-phase pattern to allow user review before committing records to the database.

### Phase 1: Generate and Preview (SSE)

1. **Trigger**: User clicks "Expand" on an outline card in `Outline.tsx`.
2. **Configuration**: User selects `target_chapter_count` (1-10) and `expansion_strategy` (`balanced`, `climax`, or `detail`).
3. **SSE Stream**: The frontend uses `SSEPostClient` to connect to `/api/outlines/{outline_id}/expand-stream`.
4. **Service Logic**: `PlotExpansionService.analyze_outline_for_chapters` determines if it needs single-batch or multi-batch generation based on `batch_size` (default 5).
5. **Real-time Feedback**: `SSEProgressModal` displays progress updates (0-100%) as the AI processes chapters.
6. **Preview**: Once complete, a JSON array of `ChapterPlanItem` is returned and displayed in a preview modal.

Sources: [backend/app/api/outlines.py:1335-1481](), [backend/app/services/plot_expansion_service.py:24-84](), [frontend/src/pages/Outline.tsx:730-810]()

### Phase 2: Confirm and Create

1. **Review**: The user reviews the AI-generated titles, summaries, and key events in the `Expansion Preview Modal`.
2. **Submission**: User clicks "Confirm and Create", sending the plan array to `/api/outlines/{outline_id}/create-chapters`.
3. **Record Creation**: The backend creates multiple `Chapter` entries.
    - `chapter_number` is calculated based on previous outlines to maintain global order.
    - `sub_index` tracks the order within the specific outline expansion.
    - The original plan is saved in the `expansion_plan` column.
4. **Renumbering**: The system automatically calls `_renumber_subsequent_chapters` to shift the numbering of any existing chapters that appear later in the novel.

Sources: [backend/app/api/outlines.py:1483-1549](), [backend/app/services/plot_expansion_service.py:352-453](), [frontend/src/pages/Outline.tsx:1082-1139]()

---

## Core Service: PlotExpansionService

The `PlotExpansionService` is responsible for the heavy lifting of contextual AI generation.

### Batch Generation Logic

To maintain quality and avoid token limits for large expansions (e.g., 10 chapters), the service splits the request:

| Feature | Single Batch (≤5) | Multi-Batch (>5) |
| :--- | :--- | :--- |
| **Function** | `_generate_chapters_single_batch` | `_generate_chapters_in_batches` |
| **Context** | Previous/Next outline summaries | Previous/Next outlines + summaries of previous batches |
| **Prompt** | `OUTLINE_EXPAND_SINGLE` | `OUTLINE_EXPAND_MULTI` |

Sources: [backend/app/services/plot_expansion_service.py:85-260]()

### Contextual Awareness

The service calls `_get_outline_context` to fetch the content of the outline immediately preceding and following the current one. This ensures that the expanded chapters bridge the narrative gap correctly.

```python
# Context Retrieval Example
prev_outline = await db.execute(
    select(Outline).where(Outline.order_index < outline.order_index).order_by(Outline.order_index.desc())
)
```

Sources: [backend/app/services/plot_expansion_service.py:455-492]()

---

## Data Models and Schemas

### ChapterPlanItem (Pydantic)
This schema defines the structure returned by the AI and used for the preview.

```python
class ChapterPlanItem(BaseModel):
    sub_index: int
    title: str
    plot_summary: str
    key_events: list[str]
    character_focus: list[str]
    emotional_tone: str
    narrative_goal: str
    conflict_type: str
    estimated_words: int = 3000
    scenes: Optional[list[str]] = None
```

Sources: [backend/app/schemas/outline.py:81-93]()

### Chapter (SQLAlchemy)
The database model stores the expanded plan for use during the actual writing phase.

| Column | Type | Description |
| :--- | :--- | :--- |
| `outline_id` | String (FK) | Links the chapter to the source outline |
| `chapter_number` | Integer | Global sequence number in the book |
| `sub_index` | Integer | Local sequence (e.g., Chapter 1.2) |
| `expansion_plan` | Text (JSON) | Stores the `ChapterPlanItem` data |

Sources: [backend/app/models/chapter.py:10-40]()

---

## Frontend Preview and Interaction

The `Outline.tsx` component manages the state for the preview and the sequential expansion check.

### Sequential Expansion Enforcement
The system prevents "gaps" in the story. Before expanding Outline N, it checks if Outline N-1 has already been expanded.

```typescript
// Frontend check in handleExpandOutline
for (const prevOutline of previousOutlines) {
  if (!outlineExpandStatus[prevOutline.id]) {
    message.warning(`请先按顺序展开：${prevOutline.title}`);
    return;
  }
}
```

Sources: [frontend/src/pages/Outline.tsx:633-684]()

### Preview Modal Features
- **Tabbed Navigation**: Users can click through the generated chapters.
- **Scene Breakdown**: If `enable_scene_analysis` was checked, the modal displays specific locations and character purposes for each scene.
- **Batch Mode**: In `BatchOutlineExpansionRequest`, multiple outlines can be queued for expansion at once, with the results displayed in a consolidated view.

Sources: [frontend/src/pages/Outline.tsx:897-1080](), [backend/app/schemas/outline.py:116-128]()

---

## API Reference Summary

| Endpoint | Method | Purpose |
| :--- | :--- | :--- |
| `/outlines/{id}/expand-stream` | POST | SSE stream for AI plan generation |
| `/outlines/{id}/create-chapters` | POST | Persists previewed plans to Chapter table |
| `/outlines/batch-expand` | POST | Batch expansion for multiple outlines |
| `/outlines/{id}/chapters` | GET | Retrieves existing chapters for an outline |

Sources: [backend/app/api/outlines.py:1335-1613]()

---

# Page: Chapter Writing

# Chapter Writing

<details>
<summary>Relevant source files</summary>

The following files were used as context for generating this wiki page:

- [backend/app/api/chapters.py](backend/app/api/chapters.py)
- [backend/app/schemas/chapter.py](backend/app/schemas/chapter.py)
- [frontend/src/components/ExpansionPlanEditor.tsx](frontend/src/components/ExpansionPlanEditor.tsx)
- [frontend/src/pages/Chapters.tsx](frontend/src/pages/Chapters.tsx)
- [frontend/src/services/api.ts](frontend/src/services/api.ts)
- [frontend/src/store/hooks.ts](frontend/src/store/hooks.ts)
- [frontend/src/types/index.ts](frontend/src/types/index.ts)

</details>



## Purpose and Scope

This document describes the chapter writing functionality in MuMuAINovel, which enables users to generate and manage novel chapter content using AI assistance. The chapter writing system enforces sequential generation (chapters must be created in order), gathers extensive context from the project's world-building, characters, and outlines, and streams AI-generated content in real-time using Server-Sent Events (SSE).

For information about creating the initial project structure and outlines, see **4.1 Project Creation Wizard** and **4.3 Outline Management**. For details about configuring AI providers and models, see **5.4 AI Provider Configuration**. For the prompt templates used in chapter generation, see **5.2 Prompt System**.

---

## Chapter Data Model

The `Chapter` entity represents a single chapter of a novel project. Each chapter is tied to a specific project and must have a sequential chapter number.

**Key Attributes:**
- `id`: Unique identifier (UUID)
- `project_id`: Foreign key to the parent Project
- `chapter_number`: Sequential integer (1, 2, 3...)
- `title`: Chapter title
- `content`: Full chapter text content
- `word_count`: Automatically calculated character count
- `status`: Chapter status (draft, completed, etc.)
- `summary`: Optional chapter summary
- `outline_id`: Reference to the parent outline node
- `expansion_plan`: JSON string containing detailed scene breakdowns (used in one-to-many mode)

**Sources:** [backend/app/models/chapter.py:1-40](), [backend/app/schemas/chapter.py:7-18]()

---

## Chapter CRUD Operations

The chapter management API provides standard CRUD operations with automatic word count tracking and project-level synchronization.

### API Endpoints

| Method | Endpoint | Purpose | Key Behavior |
|--------|----------|---------|--------------|
| POST | `/chapters` | Create new chapter | Validates project access, calculates word count, updates `Project.current_words` |
| GET | `/chapters/project/{project_id}` | List all chapters in project | Returns chapters ordered by `chapter_number` with outline metadata |
| GET | `/chapters/{chapter_id}` | Get chapter details | Returns single chapter data with linked outline title |
| PUT | `/chapters/{chapter_id}` | Update chapter | Recalculates word count, updates project statistics, clears analysis if content is wiped |
| DELETE | `/chapters/{chapter_id}` | Delete chapter | Decrements `Project.current_words`, removes associated memories |

### Word Count Management

All chapter operations automatically maintain word count integrity:
1. **On Creation**: Word count is calculated as `len(chapter.content)` and added to `Project.current_words` [backend/app/api/chapters.py:88-98]().
2. **On Update**: The difference between old and new word count is applied to the project total [backend/app/api/chapters.py:305-310]().
3. **On Deletion**: Chapter's word count is subtracted from the project total [backend/app/api/chapters.py:343-345]().

**Sources:** [backend/app/api/chapters.py:77-351]()

---

## Sequential Generation Prerequisite System

The chapter writing system enforces strict sequential generation: **Chapter N cannot be generated until all chapters 1 through N-1 are complete with content**.

### Prerequisite Check Logic

```mermaid
flowchart TD
    Start["check_prerequisites(chapter)"] --> IsFirst{"chapter_number == 1?"}
    IsFirst -->|Yes| Allow["Return: can_generate=True"]
    IsFirst -->|No| QueryPrev["Query all chapters where<br/>chapter_number < current"]
    QueryPrev --> CheckContent{"All previous chapters<br/>have non-empty content?"}
    CheckContent -->|Yes| Allow
    CheckContent -->|No| Deny["Return: can_generate=False<br/>error: '需要先完成前置章节：第X章'"]
```

**Sources:** [backend/app/api/chapters.py:1014-1051]()

---

## AI-Assisted Content Generation

The core chapter writing feature is the `POST /chapters/{chapter_id}/generate-stream` endpoint, which generates complete chapter content using AI with extensive contextual awareness.

### Chapter Generation Flow

```mermaid
sequenceDiagram
    participant FE as "frontend/src/pages/Chapters.tsx"
    participant API as "backend/app/api/chapters.py:generate_chapter_content_stream"
    participant DB as "SQLAlchemy AsyncSession"
    participant Context as "app.services.chapter_context_service"
    participant AI as "app.services.ai_service:AIService"
    participant BG as "FastAPI BackgroundTasks"

    FE->>API: POST /chapters/{id}/generate-stream
    API->>DB: check_prerequisites()
    API->>Context: build_smart_chapter_context()
    Context-->>API: Story Skeleton + Relevant History
    
    alt MCP Enabled
        API->>AI: generate_text_with_mcp()
        AI-->>API: Reference materials
    end
    
    API->>AI: generate_text_stream(prompt)
    
    loop Streaming
        AI-->>API: Content chunk
        API-->>FE: SSE Event: type=content
    end
    
    API->>DB: Update Chapter content & word_count
    API->>DB: Create GenerationHistory
    API->>BG: add_task(analyze_chapter_background)
    API-->>FE: SSE Event: type=done
```

**Sources:** [backend/app/api/chapters.py:974-1554]()

---

## Smart Context Building

MuMuAINovel uses an intelligent context building strategy to maintain narrative consistency across long novels without exceeding LLM token limits.

### Context Components

The `build_smart_chapter_context` function implements a 4-tier strategy:

| Tier | Component | Implementation | Purpose |
|------|-----------|----------------|---------|
| 1 | **Story Skeleton** | Samples every 50th chapter (title + summary) | Long-term arc consistency |
| 2 | **Relevant History** | Semantic search via `memory_service` for 15 chapters | Thematic/Plot relevance |
| 3 | **Recent Summary** | Last 30 chapters (200 chars each) | Medium-term continuity |
| 4 | **Recent Full** | Last 3 chapters (full content) | Immediate narrative flow |

**Sources:** [backend/app/api/chapters.py:446-636](), [backend/app/services/memory_service.py]()

---

## Outline Mode Differentiation

Generation logic adapts based on the project's `outline_mode` [backend/app/api/chapters.py:1277-1317]():

### 1. One-to-One Mode
- **Logic**: Each outline node corresponds to exactly one chapter.
- **Context**: Uses `outline.content` directly.
- **Instruction**: "本章采用一对一模式...请充分展开大纲中的情节."

### 2. One-to-Many Mode (Expansion Plan)
- **Logic**: One outline node is expanded into multiple chapters via `ExpansionPlan`.
- **Context**: Prioritizes `expansion_plan` JSON data (summary, key_events, scenes).
- **Instruction**: "本章采用细纲模式...请严格遵循上述详细规划."

**Sources:** [backend/app/api/chapters.py:1277-1317](), [frontend/src/components/ExpansionPlanEditor.tsx]()

---

## Batch Chapter Generation

For large-scale writing, the system provides a `BatchGenerationTask` system that handles sequential generation of multiple chapters in the background.

### Batch Execution Logic

```mermaid
flowchart TD
    Task["BatchGenerationTask"] --> Loop["For chapter in chapter_ids"]
    Loop --> Prereq["Check Prerequisites"]
    Prereq -->|Pass| Gen["Generate Single Chapter"]
    Gen -->|Success| Analyze{"enable_analysis?"}
    Analyze -->|Yes| SyncAnalysis["Run analyze_chapter_background()"]
    SyncAnalysis --> Next["Next Chapter"]
    Gen -->|Fail| Retry{"retry < max_retries?"}
    Retry -->|Yes| Gen
    Retry -->|No| FailTask["Mark Batch Failed"]
```

**Sources:** [backend/app/api/chapters.py:2188-2385](), [backend/app/models/batch_generation_task.py]()

---

## Post-Generation Analysis Pipeline

Every successful generation triggers the `PlotAnalyzer` to extract memories and update the semantic database.

1. **Extraction**: AI identifies `hooks`, `foreshadows`, `plot_points`, and `character_events` from the new text.
2. **PostgreSQL Storage**: Saves to `PlotAnalysis` and `StoryMemory` tables.
3. **Vector Storage**: Syncs memories to **ChromaDB** for future semantic context building.

**Sources:** [backend/app/api/chapters.py:684-972](), [backend/app/services/plot_analyzer.py]()

---

## SSE Event Reference

The frontend `Chapters.tsx` component listens for the following SSE event types during generation:

| Event Type | Payload Data | Purpose |
|------------|--------------|---------|
| `start` | Message | Signals start of process |
| `progress` | `progress` (0-100), `message` | UI progress bar updates |
| `content` | `content` (string chunk) | Real-time text appending |
| `done` | `word_count`, `analysis_task_id` | Finalizes UI state and triggers analysis polling |
| `error` | `error` (string) | Displays error notification |

**Sources:** [backend/app/api/chapters.py:1345-1437](), [frontend/src/pages/Chapters.tsx:116-165]()

---

# Page: Chapter Analysis System

# Chapter Analysis System

<details>
<summary>Relevant source files</summary>

The following files were used as context for generating this wiki page:

- [backend/app/api/foreshadows.py](backend/app/api/foreshadows.py)
- [backend/app/api/memories.py](backend/app/api/memories.py)
- [backend/app/models/foreshadow.py](backend/app/models/foreshadow.py)
- [backend/app/schemas/foreshadow.py](backend/app/schemas/foreshadow.py)
- [backend/app/services/chapter_context_service.py](backend/app/services/chapter_context_service.py)
- [backend/app/services/chapter_regenerator.py](backend/app/services/chapter_regenerator.py)
- [backend/app/services/foreshadow_service.py](backend/app/services/foreshadow_service.py)
- [backend/app/services/plot_analyzer.py](backend/app/services/plot_analyzer.py)
- [frontend/src/components/AnnotatedText.tsx](frontend/src/components/AnnotatedText.tsx)
- [frontend/src/components/ChapterAnalysis.tsx](frontend/src/components/ChapterAnalysis.tsx)
- [frontend/src/components/ChapterContentComparison.tsx](frontend/src/components/ChapterContentComparison.tsx)
- [frontend/src/components/ChapterRegenerationModal.tsx](frontend/src/components/ChapterRegenerationModal.tsx)
- [frontend/src/components/CharacterCareerCard.tsx](frontend/src/components/CharacterCareerCard.tsx)
- [frontend/src/pages/ChapterAnalysis.tsx](frontend/src/pages/ChapterAnalysis.tsx)

</details>



## Purpose and Scope

The Chapter Analysis System automatically analyzes completed chapter content to extract narrative elements such as hooks, foreshadows, plot points, character states, and conflicts. These extracted elements are stored as semantic memories in a vector database (ChromaDB), enabling intelligent context retrieval for future chapter generation. The system operates through the `PlotAnalyzer` service and can be triggered manually or automatically after chapter generation.

For information about chapter generation itself, see [Chapter Writing](4.5). For details on how extracted memories are used during generation, see the smart context building mechanism in [Chapter Writing](4.5).

---

## System Overview

The Chapter Analysis System consists of three primary components:

1.  **PlotAnalyzer Service**: The core engine that uses AI to perform structural and narrative analysis of chapter text [backend/app/services/plot_analyzer.py:18-29]().
2.  **Foreshadow Service**: Manages the lifecycle of plot plants and payoffs, ensuring consistent tracking across chapters [backend/app/services/foreshadow_service.py:49-51]().
3.  **Memory & Vector Storage**: Persists extracted elements in PostgreSQL (`StoryMemory`) and ChromaDB for semantic search [backend/app/api/memories.py:149-177]().

**Sources:** [backend/app/services/plot_analyzer.py:1-443](), [backend/app/services/foreshadow_service.py:1-228](), [backend/app/api/memories.py:23-182]()

---

## Analysis Pipeline Architecture

The following diagram illustrates the flow from raw chapter text to structured semantic storage.

### Data Flow: Text to Semantic Memory

```mermaid
graph TB
    subgraph "Input Layer"
        Chapter["Chapter Entity<br/>models/chapter.py"]
        Content["Chapter Content<br/>(up to 8000 chars)"]
    end
    
    subgraph "Analysis Engine [PlotAnalyzer]"
        Trigger["analyze_chapter()<br/>plot_analyzer.py:31"]
        AI["AIService.generate_text_stream<br/>(temp=0.3)"]
        Retry["Retry Logic<br/>(max_retries=3)"]
        Parse["_parse_analysis_response()<br/>plot_analyzer.py:140"]
    end
    
    subgraph "Extraction Logic"
        MemExtract["extract_memories_from_analysis()<br/>plot_analyzer.py:146"]
        PosMatch["_find_text_position()<br/>plot_analyzer.py:329"]
    end
    
    subgraph "Persistence [PostgreSQL]"
        PlotAnalysis["PlotAnalysis Record<br/>models/memory.py"]
        StoryMemory["StoryMemory Record<br/>models/memory.py"]
        Foreshadow["Foreshadow Record<br/>models/foreshadow.py"]
    end
    
    subgraph "Vector Storage [ChromaDB]"
        Vector["memory_service.add_memory()<br/>Vector ID = Memory ID"]
    end

    Chapter --> Content
    Content --> Trigger
    Trigger --> AI
    AI --> Retry
    Retry --> Parse
    Parse --> MemExtract
    MemExtract --> PosMatch
    
    MemExtract --> PlotAnalysis
    MemExtract --> StoryMemory
    MemExtract --> Foreshadow
    StoryMemory --> Vector

    style Trigger fill:#f9f9f9
    style MemExtract fill:#f9f9f9
    style Vector fill:#f9f9f9
```

**Sources:** [backend/app/services/plot_analyzer.py:31-148](), [backend/app/api/memories.py:98-179](), [backend/app/services/plot_analyzer.py:146-327]()

---

## Core Components

### PlotAnalyzer Service

The `PlotAnalyzer` class is the primary service responsible for analyzing chapter content using AI. It is initialized with an `AIService` instance and provides methods for analysis, memory extraction, and summary generation.

| Method | Purpose | Key Parameters | Returns |
| :--- | :--- | :--- | :--- |
| `analyze_chapter` | Analyzes chapter content using AI with low temperature (0.3) for consistent JSON output [backend/app/services/plot_analyzer.py:31-148]() | `chapter_number`, `title`, `content`, `existing_foreshadows` | `Dict[str, Any]` containing hooks, foreshadows, plot_points, etc. |
| `extract_memories_from_analysis` | Converts analysis results into memory records with text positions [backend/app/services/plot_analyzer.py:146-327]() | `analysis`, `chapter_id`, `chapter_number` | `List[Dict[str, Any]]` of memory objects |
| `_find_text_position` | Locates keyword positions in full text using exact, cleaned, and fuzzy matching [backend/app/services/plot_analyzer.py:329-372]() | `full_text`, `keyword` | `(position, length)` tuple |
| `generate_analysis_summary` | Generates human-readable analysis report [backend/app/services/plot_analyzer.py:374-432]() | `analysis_result` | Formatted string |

**Sources:** [backend/app/services/plot_analyzer.py:18-433]()

### Foreshadow Management

The system tracks "Foreshadows" (伏笔) through their lifecycle: `pending` -> `planted` -> `resolved`.

*   **Stable ID Generation**: Uses `generate_stable_foreshadow_id` (hash of chapter ID and content) to prevent duplicate entries when re-analyzing the same chapter [backend/app/services/foreshadow_service.py:22-46]().
*   **Automatic Matching**: During analysis, existing "planted" foreshadows are passed to the AI to check for "resolved" (payoff) matches in the current chapter [backend/app/api/memories.py:75-92]().

**Sources:** [backend/app/services/foreshadow_service.py:22-46](), [backend/app/api/memories.py:75-92](), [backend/app/schemas/foreshadow.py:8-14]()

---

## Chapter Regeneration with Feedback

The analysis system directly feeds into the `ChapterRegenerator`, allowing users to improve chapters based on AI-detected issues.

### Regeneration Workflow

```mermaid
sequenceDiagram
    participant UI as "ChapterAnalysis UI"
    participant Modal as "ChapterRegenerationModal"
    participant Service as "ChapterRegenerator"
    participant AI as "AIService"

    UI->>Modal: Open with suggestions
    Modal->>Modal: User selects suggestions &<br/>adds custom instructions
    Modal->>Service: POST /regenerate-stream
    Service->>Service: _build_modification_instructions()<br/>plot_regenerator.py:110
    Service->>AI: generate_text_stream()
    AI-->>Modal: SSE Chunks
    Modal->>UI: Show Content Comparison
```

**Key Features:**
*   **Modification Source**: Users can choose between "custom", "analysis_suggestions", or "mixed" modes [frontend/src/components/ChapterRegenerationModal.tsx:65]().
*   **Preservation Config**: Options to `preserve_structure`, `preserve_dialogues`, or `preserve_character_traits` during rewrite [backend/app/schemas/regeneration.py:8](), [backend/app/services/chapter_regenerator.py:157-177]().
*   **Focus Areas**: Target specific improvements like `pacing`, `emotion`, `description`, `dialogue`, or `conflict` [backend/app/services/chapter_regenerator.py:141-154]().

**Sources:** [backend/app/services/chapter_regenerator.py:15-108](), [frontend/src/components/ChapterRegenerationModal.tsx:94-210]()

---

## Frontend Visualization

The system provides a rich UI for exploring the results of the analysis.

### Annotated Text Component
The `AnnotatedText` component maps memory positions back onto the chapter text, allowing users to hover over highlighted sections to see the underlying "Hook" or "Foreshadow" [frontend/src/components/AnnotatedText.tsx:48-58]().

*   **Type Icons**: Hook (🎣), Foreshadow (🌟), Plot Point (💎), Character Event (👤) [frontend/src/components/AnnotatedText.tsx:40-45]().
*   **Smart Segmentation**: Handles overlapping annotations by splitting text into minimal segments [frontend/src/components/AnnotatedText.tsx:112-195]().

### Content Comparison
After regeneration, the `ChapterContentComparison` component uses `react-diff-viewer-continued` to show a side-by-side diff between the original and AI-improved versions [frontend/src/components/ChapterContentComparison.tsx:188-223]().

**Sources:** [frontend/src/components/AnnotatedText.tsx:1-207](), [frontend/src/components/ChapterContentComparison.tsx:18-227]()

---

## Analysis Task Management

Background analysis is tracked via the `AnalysisTask` status in the frontend to provide real-time feedback.

| Status | UI Representation | Logic |
| :--- | :--- | :--- |
| `pending` | Clock Icon | Task is in the queue |
| `running` | Spin / Progress Bar | AI is currently processing [frontend/src/components/ChapterAnalysis.tsx:197-198]() |
| `completed` | Check Circle | Results are ready to fetch [frontend/src/components/ChapterAnalysis.tsx:199-200]() |
| `failed` | Close Circle | Error message displayed [frontend/src/components/ChapterAnalysis.tsx:201-202]() |

**Sources:** [frontend/src/components/ChapterAnalysis.tsx:80-162](), [frontend/src/components/ChapterAnalysis.tsx:191-206]()

---

## Integration with Smart Context (RTCO)

Extracted memories are the backbone of the **RTCO (Recent, Theme, Character, Outline)** context framework used during chapter generation.

*   **P2 - Reference Information**: Relevant memories are retrieved from ChromaDB based on the current chapter's outline (similarity > 0.6) and injected into the generation prompt [backend/app/services/chapter_context_service.py:23-31]().
*   **Foreshadow Reminders**: Active foreshadows that need to be "planted" or "resolved" in the current chapter are automatically included [backend/app/services/chapter_context_service.py:142]().

**Sources:** [backend/app/services/chapter_context_service.py:23-127](), [backend/app/services/chapter_context_service.py:132-220]()

---

# Page: Character and Relationship Management

# Character and Relationship Management

<details>
<summary>Relevant source files</summary>

The following files were used as context for generating this wiki page:

- [backend/app/api/careers.py](backend/app/api/careers.py)
- [backend/app/api/characters.py](backend/app/api/characters.py)
- [backend/app/api/organizations.py](backend/app/api/organizations.py)
- [backend/app/api/relationships.py](backend/app/api/relationships.py)
- [backend/app/api/writing_styles.py](backend/app/api/writing_styles.py)
- [backend/app/models/character.py](backend/app/models/character.py)
- [backend/app/schemas/character.py](backend/app/schemas/character.py)
- [backend/app/services/auto_character_service.py](backend/app/services/auto_character_service.py)
- [backend/app/services/auto_organization_service.py](backend/app/services/auto_organization_service.py)
- [backend/app/services/character_state_update_service.py](backend/app/services/character_state_update_service.py)
- [backend/app/utils/sse_response.py](backend/app/utils/sse_response.py)
- [frontend/pnpm-lock.yaml](frontend/pnpm-lock.yaml)
- [frontend/src/components/CharacterCard.tsx](frontend/src/components/CharacterCard.tsx)
- [frontend/src/pages/Careers.tsx](frontend/src/pages/Careers.tsx)
- [frontend/src/pages/Characters.tsx](frontend/src/pages/Characters.tsx)
- [frontend/src/pages/Organizations.tsx](frontend/src/pages/Organizations.tsx)
- [frontend/src/pages/RelationshipGraph.tsx](frontend/src/pages/RelationshipGraph.tsx)
- [frontend/src/pages/Relationships.tsx](frontend/src/pages/Relationships.tsx)
- [frontend/src/utils/sseClient.ts](frontend/src/utils/sseClient.ts)

</details>



## Purpose and Scope

This page documents the character and relationship management system in MuMuAINovel. The system provides a dual-nature character model where entities can represent both individual characters and organizations, a sophisticated relationship tracking system, a hierarchical organization membership system, and an integrated career (profession) system. It also details the `AutoCharacterService` which handles predictive character introduction during story expansion.

---

## Character and Organization Data Model

### Unified Character Entity
The system uses a unified `Character` model [backend/app/models/character.py]() that represents both individual characters and organizations via the `is_organization` flag.

| Field | Type | Description |
|-------|------|-------------|
| `id` | String (UUID) | Primary key. |
| `is_organization` | Boolean | If `True`, the entity is an organization. |
| `role_type` | String | protagonist, supporting, antagonist. [backend/app/schemas/character.py:31]() |
| `main_career_id` | String (FK) | References the primary `Career`. [backend/app/schemas/character.py:48]() |
| `main_career_stage`| Integer | Current level in the main career. |
| `sub_careers` | JSON String | List of secondary careers and stages. [backend/app/schemas/character.py:50]() |
| `status` | String | active, deceased, missing, retired. [backend/app/schemas/character.py:100]() |

### Organization Extension
When `is_organization` is `True`, a record in the `Organization` table [backend/app/models/relationship.py:11]() stores metadata:
*   **Power Level**: Influence rating (0-100). [backend/app/schemas/character.py:42]()
*   **Location**: Physical headquarters.
*   **Motto**: Organizational slogan.

**Diagram: Character and Organization Logic Space**

```mermaid
graph LR
    subgraph "Code Entity Space (SQLAlchemy Models)"
        C["Character (app.models.character)"]
        O["Organization (app.models.relationship)"]
        OM["OrganizationMember (app.models.relationship)"]
        CR["CharacterCareer (app.models.career)"]
    end

    subgraph "Natural Language Space (AI Generation)"
        AI_C["'Character Description'"]
        AI_O["'Sect/Guild Details'"]
        AI_M["'Member Ranks'"]
    end

    AI_C -->|is_organization=false| C
    AI_O -->|is_organization=true| C
    C -->|1:1 Optional| O
    O -->|1:N| OM
    C -->|1:N| CR
    
    C -- "character_id" --> O
    O -- "organization_id" --> OM
```
Sources: [backend/app/models/character.py](), [backend/app/models/relationship.py:11-30](), [backend/app/schemas/character.py:24-51]()

---

## Relationship Management System

### CharacterRelationship Model
Captures directed relationships between characters (A → B). Relationships can be asymmetric (e.g., A loves B, B hates A).

*   **Intimacy Level**: 0-100 score. [backend/app/api/relationships.py:124]()
*   **Relationship Name**: Custom label (e.g., "师徒", "仇人").
*   **Source**: "ai", "manual", or "auto". [backend/app/api/relationships.py:193]()

### Organization Membership
The `OrganizationMember` model [backend/app/models/relationship.py:133]() manages the many-to-many relationship between characters and organizations.
*   **Position**: Role title (e.g., "Elder", "Sect Leader"). [backend/app/api/organizations.py:230]()
*   **Rank**: Numeric hierarchy level (higher is more senior). [backend/app/api/organizations.py:97]()
*   **Loyalty**: Member's commitment to the organization (0-100).

**Diagram: Relationship Graph Data Flow**

```mermaid
sequenceDiagram
    participant UI as Relationships.tsx
    participant API as relationships.py (get_relationship_graph)
    participant DB as SQLite/PostgreSQL
    
    UI->>API: GET /api/relationships/graph/{project_id}
    API->>DB: select(Character)
    API->>DB: select(CharacterRelationship)
    API->>DB: select(OrganizationMember) JOIN Organization
    DB-->>API: Row Data
    API->>API: Map to RelationshipGraphNode & RelationshipGraphLink
    API-->>UI: RelationshipGraphData (JSON)
    Note right of UI: Rendered via @xyflow/react in RelationshipGraph.tsx
```
Sources: [backend/app/api/relationships.py:77-157](), [frontend/src/pages/RelationshipGraph.tsx:13-23]()

---

## Career (Profession) System

MuMuAINovel features a structured career system where characters progress through "Stages" (阶).

*   **Career Types**: `main` (primary cultivation/job) and `sub` (secondary skills like alchemy). [backend/app/api/careers.py:87-90]()
*   **Stages**: Defined as a JSON list containing level, name, and description. [backend/app/api/careers.py:66]()
*   **AI Generation**: The system can generate a complete career system for a world context via SSE. [backend/app/api/careers.py:158-175]()

---

## Auto-Character Introduction System

The `AutoCharacterService` [backend/app/services/auto_character_service.py:17]() automatically identifies when a plot expansion requires new characters and generates them to fit the existing context.

### Predictive Analysis Workflow
1.  **Analyze Needs**: Uses `AUTO_CHARACTER_ANALYSIS` prompt to check if the current plot stage (e.g., "High Tide") requires new actors. [backend/app/services/auto_character_service.py:218]()
2.  **Generate Details**: Uses `AUTO_CHARACTER_GENERATION` to create full character profiles, ensuring career stages do not exceed world maximums. [backend/app/services/auto_character_service.py:87-108]()
3.  **Database Sync**: Matches AI-suggested career names against existing `Career` records to link IDs. [backend/app/services/auto_character_service.py:156-173]()

### Hallucination Cleanup
The service includes a cleanup phase to ensure that relationships generated by the AI do not point to non-existent entities within the batch. [backend/app/services/auto_character_service.py:407-445]()

---

## Implementation Details: Character API

The character API [backend/app/api/characters.py]() provides enriched data by aggregating information from multiple tables.

### Enriched Character Retrieval
When fetching character lists, the backend dynamically builds summaries for the frontend:
*   **Relationships Summary**: Concatenates all `CharacterRelationship` records into a readable string (e.g., "与张三：师徒"). [backend/app/api/characters.py:34-80]()
*   **Organization Summary**: Serializes `OrganizationMember` lists into JSON for the UI. [backend/app/api/characters.py:83-117]()
*   **Career Resolution**: Parses `sub_careers` JSON and links `main_career_id`. [backend/app/api/characters.py:174-176]()

### Streaming Generation (SSE)
Character and organization generation use Server-Sent Events to provide real-time progress.
*   **Endpoint**: `/api/characters/generate-stream` [backend/app/api/characters.py:255]()
*   **Tracker**: Uses `WizardProgressTracker` to send percentage updates. [backend/app/api/characters.py:269]()

**Table: Character Management API Reference**

| Method | Route | Description |
|--------|-------|-------------|
| GET | `/api/characters` | List all characters with relationship/org summaries. [backend/app/api/characters.py:120]() |
| POST | `/api/characters/generate-stream` | SSE endpoint for AI character batch generation. [backend/app/api/characters.py:255]() |
| POST | `/api/organizations/generate-stream` | SSE endpoint for AI organization generation. [backend/app/api/organizations.py:330]() |
| GET | `/api/relationships/graph/{project_id}` | Returns nodes/links for graph visualization. [backend/app/api/relationships.py:77]() |
| PUT | `/api/organizations/members/{member_id}` | Update member rank/loyalty. [backend/app/api/organizations.py:284]() |

Sources: [backend/app/api/characters.py:34-194](), [backend/app/api/organizations.py:32-330](), [backend/app/api/relationships.py:77-157]()

---

# Page: Writing Styles

# Writing Styles

<details>
<summary>Relevant source files</summary>

The following files were used as context for generating this wiki page:

- [backend/app/api/careers.py](backend/app/api/careers.py)
- [backend/app/api/writing_styles.py](backend/app/api/writing_styles.py)
- [backend/app/main.py](backend/app/main.py)
- [backend/app/models/writing_style.py](backend/app/models/writing_style.py)
- [backend/app/schemas/writing_style.py](backend/app/schemas/writing_style.py)
- [frontend/src/App.tsx](frontend/src/App.tsx)
- [frontend/src/pages/Careers.tsx](frontend/src/pages/Careers.tsx)
- [frontend/src/pages/ProjectDetail.tsx](frontend/src/pages/ProjectDetail.tsx)
- [frontend/src/pages/WritingStyles.tsx](frontend/src/pages/WritingStyles.tsx)

</details>



## Purpose and Scope

The Writing Styles system in MuMuAINovel allows users to define and apply specific narrative tones, linguistic patterns, and structural preferences to AI-generated content. This feature ensures stylistic consistency across a novel's chapters by injecting specialized instructions into the prompt engineering pipeline. The system supports both global presets (e.g., "Classical", "Modern") and user-defined custom styles stored in the database.

**Sources:** [backend/app/models/writing_style.py:7-20](), [backend/app/api/writing_styles.py:1-21]()

---

## System Architecture

The writing style architecture is split between a centralized database for persistence and a logic layer within the prompt service for application.

### Style Management and Application Flow

The following diagram illustrates how a style moves from the database/preset definition through the backend API and into the AI generation prompt.

```mermaid
graph TD
    subgraph "Frontend Space"
        WS_Page["WritingStyles.tsx"]
        Store["useStore (currentProject)"]
    end

    subgraph "Backend Code Entities"
        WS_Router["writing_styles.py (APIRouter)"]
        WS_Model["WritingStyle (SQLAlchemy Model)"]
        PDS_Model["ProjectDefaultStyle (SQLAlchemy Model)"]
        PromptService["PromptService (Logic Layer)"]
    end

    subgraph "Data Storage"
        DB[("PostgreSQL / SQLite")]
    end

    WS_Page -- "GET /api/writing-styles/project/{id}" --> WS_Router
    WS_Router -- "query" --> WS_Model
    WS_Router -- "check default" --> PDS_Model
    DB --- WS_Model
    
    Store -- "projectId + styleId" --> Gen_API["/api/chapters/generate"]
    Gen_API -- "calls" --> PromptService
    PromptService -- "appends prompt_content" --> AI_Request["AIService.generate_text_stream"]
```

**Sources:** [frontend/src/pages/WritingStyles.tsx:25-34](), [backend/app/api/writing_styles.py:202-213](), [backend/app/models/writing_style.py:7-21](), [backend/app/main.py:152-152]()

---

## Data Models and Schema

Styles are categorized into two types: **Preset** (global, provided by the system) and **Custom** (user-created).

### WritingStyle Model
The `WritingStyle` model [backend/app/models/writing_style.py:7-21]() serves as the primary entity:
- `user_id`: If `NULL`, the style is a global preset available to everyone [backend/app/models/writing_style.py:12-12]().
- `style_type`: Distinguished as `preset` or `custom` [backend/app/models/writing_style.py:14-14]().
- `prompt_content`: The actual text instructions sent to the LLM [backend/app/models/writing_style.py:17-17]().

### Project Default Styles
The system tracks which style is the "active" default for a specific project via the `ProjectDefaultStyle` model [backend/app/api/writing_styles.py:10-10](). This allows the UI to highlight the selected style and the backend to automatically apply it during batch generation.

| Field | Type | Description |
|-------|------|-------------|
| `name` | String | Display name (e.g., "Cyberpunk Noir") |
| `preset_id` | String | Unique identifier for system presets (e.g., "natural") |
| `prompt_content`| Text | The specific LLM instructions |
| `is_default` | Boolean | (Schema only) Indicates if it's the project's active style |

**Sources:** [backend/app/schemas/writing_style.py:7-50](), [backend/app/models/writing_style.py:7-21]()

---

## Writing Style Application

Styles are applied by the backend during the prompt construction phase for chapter generation.

### Code Entity Association

This diagram maps the natural language concept of "Applying a Style" to the specific backend functions and database fields involved.

```mermaid
graph LR
    subgraph "Natural Language Concept"
        Selection["User selects 'Classical' style"]
        Instruction["'Use elegant, rhythmic language'"]
    end

    subgraph "Code Entity Space"
        API_Route["writing_styles.py: get_project_styles()"]
        Model_Field["WritingStyle.prompt_content"]
        Logic_Func["PromptService.format_prompt()"]
    end

    Selection --> API_Route
    API_Route --> Model_Field
    Instruction --> Model_Field
    Model_Field -- "Injected into" --> Logic_Func
```

**Sources:** [backend/app/api/writing_styles.py:202-233](), [backend/app/models/writing_style.py:17-17]()

### Application Logic
When generating a chapter, the backend retrieves the `prompt_content`. This content is appended to the system prompt to override the default "neutral" AI writing behavior. 

1. **Retrieval**: The API fetches the style linked to the project [backend/app/api/writing_styles.py:202-233]().
2. **Injection**: The `prompt_content` is merged with project metadata (world-building, characters) and the specific chapter outline.
3. **Execution**: The final prompt is sent to the configured AI provider via the `AIService`.

---

## User Interface and Interaction

The `WritingStyles` page [frontend/src/pages/WritingStyles.tsx:32-40]() provides the management interface.

### Key Frontend Functions
- `loadStyles`: Fetches combined list of presets and user-custom styles [frontend/src/pages/WritingStyles.tsx:62-86]().
- `handleSetDefault`: Persists the project-style association via `writingStyleApi.setDefaultStyle` [frontend/src/pages/WritingStyles.tsx:142-155]().
- `handleCreate`: Allows users to define new `prompt_content` for personalized narrative voices [frontend/src/pages/WritingStyles.tsx:88-105]().

### UI Components
The interface uses an Ant Design `Card` grid [frontend/src/pages/WritingStyles.tsx:201-218](). Cards for the currently active project style are highlighted with a primary color border [frontend/src/pages/WritingStyles.tsx:226-226]() and a `StarFilled` icon [frontend/src/pages/WritingStyles.tsx:241-241]().

**Sources:** [frontend/src/pages/WritingStyles.tsx:1-241](), [frontend/src/App.tsx:68-68]()

---

## Preset Styles Reference

The system includes several built-in presets (stored in the database with `user_id = NULL`). Common presets include:

| Preset ID | Style Name | Intended Use |
|-----------|------------|--------------|
| `natural` | 自然流畅 | General fiction, conversational and easy to read. |
| `classical`| 古典优雅 | Wuxia, historical, or high fantasy with formal prose. |
| `modern`  | 现代简约 | Thrillers, urban fiction, or fast-paced action. |
| `vivid`   | 生动形象 | Descriptive works focusing on sensory details. |

**Sources:** [backend/app/api/writing_styles.py:32-63](), [backend/app/models/writing_style.py:12-12]()

---

# Page: AI Integration

# AI Integration

<details>
<summary>Relevant source files</summary>

The following files were used as context for generating this wiki page:

- [backend/app/api/wizard_stream.py](backend/app/api/wizard_stream.py)
- [backend/app/services/ai_service.py](backend/app/services/ai_service.py)
- [backend/app/services/prompt_service.py](backend/app/services/prompt_service.py)

</details>



This page documents how AI services are integrated throughout MuMuAINovel. It covers the core `AIService` abstraction layer, provider management, connection pooling, streaming architecture, and error handling patterns. For specific sub-topics, see:
- Provider configuration and API key management: [AI Provider Configuration](#5.4)
- Prompt template system: [Prompt System](#5.2)
- MCP plugin architecture: [MCP Plugin System](#5.3)
- SSE streaming implementation details: [Server-Sent Events (SSE) for Streaming](#5.5)

The AI integration layer serves as the foundation for all AI-powered features in the system, including world building, character generation, outline creation, and chapter writing.

---

## Core Architecture Overview

The AI integration is built around the `AIService` class, which provides a unified interface to multiple LLM providers while handling connection pooling, rate limiting, retry logic, and format validation.

### AIService Class Structure

```mermaid
classDiagram
    class AIService {
        +api_provider: str
        +default_model: str
        +user_id: str
        +db_session: AsyncSession
        -enable_mcp: bool
        -_openai_provider: OpenAIProvider
        -_anthropic_provider: AnthropicProvider
        -_gemini_provider: GeminiProvider
        +generate_text(prompt, provider, model) Dict
        +generate_text_stream(prompt, provider, model) AsyncGenerator
        +generate_text_with_mcp(prompt, mcp_max_rounds) Dict
        +call_with_json_retry(prompt, max_retries) Dict|List
        -_get_provider(provider) BaseAIProvider
        -_clean_json_response(text) str
        -_add_json_format_hint(original_prompt, failed_response) str
    }
    
    class BaseAIProvider {
        <<interface>>
        +generate_text()
        +generate_text_stream()
    }
    
    class OpenAIProvider {
        -client: OpenAIClient
    }
    
    class OpenAIClient {
        -api_key: str
        -base_url: str
        -http_client: httpx.AsyncClient
    }
    
    AIService --> OpenAIProvider
    AIService --> AnthropicProvider
    AIService --> GeminiProvider
    OpenAIProvider --|> BaseAIProvider
    OpenAIProvider --> OpenAIClient
```

**Sources:** [backend/app/services/ai_service.py:37-125](), [backend/app/services/ai_service.py:156-165]()

---

## Provider Abstraction Layer

The `AIService` class abstracts away provider-specific implementation details using a Provider pattern. It standardizes naming via `normalize_provider` and routes requests to specific implementations like `OpenAIProvider` or `GeminiProvider`.

### Provider Initialization Flow

```mermaid
sequenceDiagram
    participant App as "Application/User"
    participant AIS as "AIService.__init__"
    participant Norm as "normalize_provider"
    participant OAI as "OpenAIProvider"
    participant OAC as "OpenAIClient"
    
    App->>AIS: Initialize(api_provider, api_key, ...)
    AIS->>Norm: normalize_provider("mumu")
    Norm-->>AIS: "openai"
    
    alt Provider is OpenAI
        AIS->>OAC: Initialize(api_key, base_url, config)
        Note over OAC: Uses global httpx client pool
        OAC-->>AIS: client_instance
        AIS->>OAI: Initialize(client_instance)
        OAI-->>AIS: _openai_provider
    end
    
    Note over AIS: ✅ AIService ready
```

**Sources:** [backend/app/services/ai_service.py:30-34](), [backend/app/services/ai_service.py:88-125]()

---

## HTTP Client Pooling Architecture

To optimize performance, the system implements global HTTP client pooling via `cleanup_all_clients` and provider-specific client classes (e.g., `OpenAIClient`, `AnthropicClient`).

### Connection Pool Management

| Component | Code Entity | Purpose |
|-----------|--------------|---------|
| **Pool Manager** | `cleanup_all_clients` | Manages lifecycle of underlying `httpx.AsyncClient` instances |
| **Config** | `AIClientConfig` | Defines timeout and retry parameters for all clients |
| **Default Config** | `default_config` | 60s timeout, 3 max retries, exponential backoff |
| **Provider Logic** | `BaseAIProvider` | Abstract base for provider-specific API call logic |

**Sources:** [backend/app/services/ai_service.py:17-25](), [backend/app/services/ai_config.py:12-45]()

---

## Generation Methods

The `AIService` provides multiple generation methods tailored for different reliability and interactivity requirements:

### Method Comparison

| Method | Return Type | Streaming | Use Case |
|--------|------------|-----------|----------|
| `generate_text()` | `Dict[str, Any]` | No | Standard one-off generation |
| `generate_text_stream()` | `AsyncGenerator[str, None]` | Yes | Real-time chapter writing and world building |
| `generate_text_with_mcp()` | `Dict[str, Any]` | No | Tool-augmented generation (web search, file access) |
| `call_with_json_retry()` | `Dict \| List` | No | Strict structured data generation (Characters, Outlines) |

**Sources:** [backend/app/services/ai_service.py:194-230](), [backend/app/services/ai_service.py:232-269](), [backend/app/services/ai_service.py:271-337]()

---

## Streaming Architecture

The streaming implementation uses `AsyncGenerator` to yield text chunks as they arrive from the provider. This is heavily utilized in the Project Wizard and Chapter Generation.

### Streaming Generation Flow

```mermaid
sequenceDiagram
    participant API as "wizard_stream.py"
    participant AIS as "AIService.generate_text_stream"
    participant Prov as "OpenAIProvider"
    participant Client as "OpenAIClient"
    participant Remote as "LLM API"
    
    API->>AIS: generate_text_stream(prompt, model)
    AIS->>Prov: generate_text_stream(prompt, model, ...)
    Prov->>Client: stream_chat(messages, ...)
    Client->>Remote: POST /v1/chat/completions (stream=true)
    
    loop Chunks
        Remote-->>Client: data: {"choices": [{"delta": {"content": "..."}}]}
        Client-->>Prov: yield chunk
        Prov-->>AIS: yield chunk
        AIS-->>API: yield chunk
        Note over API: Send via SSE to Frontend
    end
```

**Key Implementation Details:**
- **Cleaning:** `_clean_json_response` is used to strip markdown artifacts like ` ```json ` from AI output [backend/app/services/ai_service.py:339-366]().
- **Progress Tracking:** The `WizardProgressTracker` in `wizard_stream.py` manages percentage updates and heartbeats during the stream [backend/app/api/wizard_stream.py:37-42]().

**Sources:** [backend/app/services/ai_service.py:232-269](), [backend/app/api/wizard_stream.py:103-128]()

---

## JSON Retry Mechanism

MuMuAINovel relies on structured JSON for its data models. The `call_with_json_retry` method ensures that even if an AI model produces malformed JSON, the system attempts to fix it or retries with a corrective prompt.

### JSON Correction Logic

1. **Extraction:** Uses `_clean_json_response` to find the first `{` or `[` and the last matching bracket [backend/app/services/ai_service.py:339-366]().
2. **Validation:** Attempts `json.loads()`.
3. **Retry:** If parsing fails, it appends a "format hint" explaining the error and the expected JSON structure to the next prompt [backend/app/services/ai_service.py:381-413]().

**Sources:** [backend/app/services/ai_service.py:271-337](), [backend/app/services/ai_service.py:339-366]()

---

## MCP Tool Integration

The Model Context Protocol (MCP) integration allows the AI to perform external actions. This is managed via the `enable_mcp` flag and the `generate_text_with_mcp` method.

### MCP Integration Flow

```mermaid
graph TB
    subgraph "AIService"
        MCP_Check{"enable_mcp == True?"}
        LoadTools["_load_mcp_tools()"]
        CallAI["Provider.generate_text(tools=...)"]
    end
    
    subgraph "MCP System"
        PluginRegistry["MCPPlugin Registry"]
        ToolExecution["Tool Executor"]
    end
    
    MCP_Check -->|Yes| LoadTools
    LoadTools --> PluginRegistry
    CallAI -->|Tool Call| ToolExecution
    ToolExecution -->|Results| CallAI
```

**Sources:** [backend/app/services/ai_service.py:37-72](), [backend/app/services/ai_service.py:271-337]()

---

## Writing Style Integration

AI generation is further customized through the `WritingStyleManager`, which injects specific stylistic requirements into the base prompts before they are sent to the `AIService`.

### Style Application Pattern

The `WritingStyleManager.apply_style_to_prompt` method takes a base prompt and a `style_content` string, combining them to ensure the AI follows specific prose guidelines [backend/app/services/prompt_service.py:6-22]().

**Sources:** [backend/app/services/prompt_service.py:6-22]()

---

# Page: AI Service Architecture

# AI Service Architecture

<details>
<summary>Relevant source files</summary>

The following files were used as context for generating this wiki page:

- [backend/app/logger.py](backend/app/logger.py)
- [backend/app/services/ai_clients/anthropic_client.py](backend/app/services/ai_clients/anthropic_client.py)
- [backend/app/services/ai_clients/gemini_client.py](backend/app/services/ai_clients/gemini_client.py)
- [backend/app/services/ai_clients/openai_client.py](backend/app/services/ai_clients/openai_client.py)
- [backend/app/services/ai_metrics.py](backend/app/services/ai_metrics.py)
- [backend/app/services/ai_providers/anthropic_provider.py](backend/app/services/ai_providers/anthropic_provider.py)
- [backend/app/services/ai_providers/gemini_provider.py](backend/app/services/ai_providers/gemini_provider.py)
- [backend/app/services/ai_providers/openai_provider.py](backend/app/services/ai_providers/openai_provider.py)
- [backend/app/services/ai_service.py](backend/app/services/ai_service.py)

</details>



## Purpose and Scope

This document describes the `AIService` architecture, which provides a unified abstraction layer for interacting with multiple Large Language Model (LLM) providers including OpenAI, Anthropic, and Google Gemini. The `AIService` class handles provider switching, HTTP connection pooling via `httpx.AsyncClient`, request metrics tracking, JSON response parsing with automatic retry, and integration with the Model Context Protocol (MCP) for tool calling.

**Sources:** [backend/app/services/ai_service.py:1-7]()

---

## AIService Class Structure

The `AIService` class is the central component that encapsulates all AI provider interactions. It maintains provider-specific adapter instances (`OpenAIProvider`, `AnthropicProvider`, `GeminiProvider`) and routes requests based on the standardized `api_provider` name.

### Class Initialization and Provider Mapping

```mermaid
graph TB
    Init["AIService.__init__()"]
    
    subgraph "Configuration Resolution"
        UserSettings["User Settings<br/>(api_provider, api_key, api_base_url)"]
        GlobalSettings["Global Settings<br/>(app_settings)"]
        FinalConfig["Final AIClientConfig"]
    end
    
    subgraph "Provider Initialization"
        OpenAIInit["OpenAIClient + OpenAIProvider"]
        AnthropicInit["AnthropicClient + AnthropicProvider"]
        GeminiInit["GeminiClient + GeminiProvider"]
    end
    
    subgraph "Standardization"
        Normalize["normalize_provider()<br/>(mumu -> openai)"]
    end
    
    Init --> UserSettings
    UserSettings --> FinalConfig
    GlobalSettings --> FinalConfig
    
    FinalConfig --> Normalize
    Normalize --> OpenAIInit
    Normalize --> AnthropicInit
    Normalize --> GeminiInit
    
    OpenAIInit --> P1["self._openai_provider"]
    AnthropicInit --> P2["self._anthropic_provider"]
    GeminiInit --> P3["self._gemini_provider"]
```

**Provider Normalization**
The system uses `normalize_provider` to map internal aliases like `mumu` to standard provider names like `openai` [backend/app/services/ai_service.py:30-34]().

**Sources:** [backend/app/services/ai_service.py:74-125]()

---

## HTTP Client Pooling and Client Layer

Unlike direct SDK usage for all providers, the architecture uses custom client classes (`OpenAIClient`, `GeminiClient`) that wrap `httpx.AsyncClient` to implement pooling and timeout logic.

### Client Configuration and Pooling

| Parameter | Source | Default Value | Purpose |
|-----------|--------|---------------|---------|
| `connect_timeout` | `AIClientConfig` | 10.0s | Max time to establish connection |
| `read_timeout` | `AIClientConfig` | 60.0s | Max time to receive response |
| `pool_timeout` | `AIClientConfig` | 10.0s | Max time to acquire connection from pool |

**Implementation Details:**
- **OpenAI:** Uses `BaseAIClient` which manages a shared `httpx.AsyncClient` with retry logic [backend/app/services/ai_clients/openai_client.py:11-12]().
- **Gemini:** Manages its own `httpx.AsyncClient` instance per client [backend/app/services/ai_clients/gemini_client.py:18-25]().
- **Anthropic:** Uses the official `AsyncAnthropic` SDK [backend/app/services/ai_clients/anthropic_client.py:20]().

**Cleanup:**
The system provides a `cleanup_http_clients` function (aliased from `cleanup_all_clients`) to ensure all underlying `httpx` connections are closed on server shutdown [backend/app/services/ai_service.py:25]().

**Sources:** [backend/app/services/ai_clients/gemini_client.py:13-25](), [backend/app/services/ai_service.py:107-125]()

---

## Provider Abstraction Layer

The `AIService` class provides a unified interface that transparently routes requests to the appropriate provider.

### Text Generation Methods

```mermaid
graph TB
    subgraph "Public API Methods"
        GenerateText["generate_text()<br/>(non-streaming)"]
        GenerateStream["generate_text_stream()<br/>(streaming)"]
        JSONRetry["call_with_json_retry()<br/>(with auto-retry)"]
    end
    
    subgraph "Provider Logic"
        GetProvider["_get_provider()"]
        Metrics["_build_call_metrics()"]
    end
    
    subgraph "Provider Implementations"
        OA["OpenAIProvider"]
        AN["AnthropicProvider"]
        GE["GeminiProvider"]
    end
    
    GenerateText --> GetProvider
    GenerateStream --> GetProvider
    
    GetProvider --> OA
    GetProvider --> AN
    GetProvider --> GE
    
    OA --> Metrics
    AN --> Metrics
    GE --> Metrics
```

**Metrics Tracking**
Every AI call generates an `AICallMetrics` object that tracks:
- `ttft_ms`: Time to first token (for streaming) [backend/app/services/ai_metrics.py:102]().
- `duration_ms`: Total request duration [backend/app/services/ai_metrics.py:114]().
- `usage`: Token consumption (prompt, completion, total) [backend/app/services/ai_metrics.py:94]().
- `success`: Boolean status of the call [backend/app/services/ai_metrics.py:88]().

**Sources:** [backend/app/services/ai_service.py:156-187](), [backend/app/services/ai_metrics.py:72-125]()

---

## JSON Retry and Cleaning Mechanism

The system implements a robust JSON handling layer to ensure structured data (like outlines or character profiles) is correctly parsed even if the LLM includes conversational filler or markdown.

### JSON Cleaning Process

The `clean_json_response` utility (imported in `ai_service.py`) performs the following:
1. Strips markdown code blocks (e.g., ` ```json ... ``` `).
2. Extracts the first valid JSON object `{...}` or array `[...]` found in the text.
3. Removes trailing commas or other common LLM syntax errors.

**Sources:** [backend/app/services/ai_service.py:22]()

### call_with_json_retry Flow

This method wraps the standard generation with an error-correction loop. If `parse_json` fails, it re-prompts the AI with a "format hint" that includes the previous error and explicit JSON rules.

```mermaid
sequenceDiagram
    participant App as Application Logic
    participant Service as AIService
    participant AI as LLM Provider
    
    App->>Service: call_with_json_retry(prompt)
    Service->>AI: generate_text(prompt)
    AI-->>Service: "Here is your JSON: ```json {...}```"
    Service->>Service: clean_json_response()
    Service->>Service: parse_json()
    
    alt Parse Success
        Service-->>App: Parsed Object
    else Parse Failure (Attempt 1)
        Service->>Service: Build Error Hint Prompt
        Service->>AI: generate_text(Hint + Original)
        AI-->>Service: "{...}"
        Service->>Service: parse_json()
        Service-->>App: Parsed Object
    end
```

**Sources:** [backend/app/services/ai_service.py:22](), [backend/app/services/ai_service.py:110-125]()

---

## MCP Tool Calling Architecture

The `AIService` supports the Model Context Protocol (MCP) for dynamic tool discovery and execution.

### MCP Lifecycle in AIService

1. **Discovery:** When `AIService` is initialized with a `user_id` and `db_session`, it checks for enabled MCP plugins [backend/app/services/ai_service.py:50-54]().
2. **Caching:** Available tools are cached in `_cached_tools` to avoid redundant database lookups during multi-turn conversations [backend/app/services/ai_service.py:100]().
3. **Execution:**
    - **Streaming:** Providers (e.g., `OpenAIProvider`) buffer `tool_calls` from the stream [backend/app/services/ai_providers/openai_provider.py:62-76]().
    - **Resolution:** Once the stream ends, `batch_call_tools` is executed via the `mcp_client` [backend/app/services/ai_providers/openai_provider.py:83-86]().
    - **Injection:** Tool results are formatted into a `tool_context` and injected into a recursive AI call to generate the final answer [backend/app/services/ai_providers/openai_provider.py:88-91]().

**Sources:** [backend/app/services/ai_service.py:37-72](), [backend/app/services/ai_providers/openai_provider.py:58-102]()

---

## Provider Implementation Comparison

| Feature | OpenAI | Anthropic | Gemini |
|---------|--------|-----------|--------|
| **Client** | `OpenAIClient` (httpx) | `AnthropicClient` (SDK) | `GeminiClient` (httpx) |
| **Stream Support** | `data: ` SSE parsing | SDK Native Stream | `alt=sse` Query Param |
| **Tool Format** | OpenAI Tools JSON | Anthropic Content Blocks | Gemini Function Declarations |
| **Tool Conversion** | Native | Native | `_convert_tools_to_gemini` |

**Gemini Tool Conversion:**
The `GeminiClient` specifically converts OpenAI-formatted tools by stripping `$schema` and `additionalProperties` fields which are unsupported by the Google Generative Language API [backend/app/services/ai_clients/gemini_client.py:27-45]().

**Sources:** [backend/app/services/ai_clients/openai_client.py:11-35](), [backend/app/services/ai_clients/anthropic_client.py:12-21](), [backend/app/services/ai_clients/gemini_client.py:10-45]()

---

# Page: Prompt System

# Prompt System

<details>
<summary>Relevant source files</summary>

The following files were used as context for generating this wiki page:

- [backend/app/api/prompt_templates.py](backend/app/api/prompt_templates.py)
- [backend/app/api/wizard_stream.py](backend/app/api/wizard_stream.py)
- [backend/app/schemas/prompt_template.py](backend/app/schemas/prompt_template.py)
- [backend/app/services/prompt_service.py](backend/app/services/prompt_service.py)
- [frontend/src/pages/MCPPlugins.tsx](frontend/src/pages/MCPPlugins.tsx)
- [frontend/src/pages/PromptTemplates.tsx](frontend/src/pages/PromptTemplates.tsx)

</details>



## Purpose and Scope

The Prompt System in MuMuAINovel is a sophisticated orchestration layer that manages over 20 specialized AI instructions. It is designed to bridge the gap between high-level creative intent and structured machine-readable output. The system handles template management, user-level customization, context-aware variable injection, and strict JSON enforcement to ensure that AI-generated content—ranging from world-building to chapter text—remains consistent and parseable.

---

## System Architecture

The prompt system is primarily managed by the `PromptService` class [backend/app/services/prompt_service.py:25-27](). It operates as a centralized repository for system-default templates while providing a fallback mechanism that allows users to override any prompt with their own custom versions.

### Core Components and Data Flow

```mermaid
graph TD
    subgraph "Frontend Layer"
        PTPage["PromptTemplates.tsx"]
        Editor["Template Editor"]
    end

    subgraph "Backend Service Layer"
        PS["PromptService"]
        WSM["WritingStyleManager"]
        DB["PostgreSQL (PromptTemplate Table)"]
    end

    subgraph "AI Integration"
        AIS["AIService"]
        LLM["LLM Provider (OpenAI/Claude/etc.)"]
    end

    PTPage -->|CRUD| PS
    Editor -->|Save| DB
    PS -->|1. Fetch Template| DB
    PS -->|2. Fallback to System| PS
    PS -->|3. Inject Context| PS
    PS -->|4. Apply Style| WSM
    PS -->|5. Final Prompt| AIS
    AIS -->|Generate| LLM
```

**Sources:** [backend/app/services/prompt_service.py:25-75](), [frontend/src/pages/PromptTemplates.tsx:57-125](), [backend/app/api/prompt_templates.py:82-152]()

---

## Template Management and Customization

MuMuAINovel supports a multi-tier template management strategy. Every generation task in the system (World Building, Character Generation, etc.) has a unique `template_key`.

### Fallback Logic

When a service requests a prompt, the system follows a specific resolution order:
1. **User Customization**: Check the `prompt_templates` table for a record matching the `user_id` and `template_key` where `is_active` is true [backend/app/api/prompt_templates.py:190-201]().
2. **System Default**: If no user record exists, the system retrieves the hardcoded constant from the `PromptService` class [backend/app/services/prompt_service.py:75-665]().

### Data Model: PromptTemplate

The `PromptTemplate` model stores these overrides:

| Field | Type | Description |
|-------|------|-------------|
| `template_key` | String | Unique identifier (e.g., `WORLD_BUILDING`) |
| `template_name` | String | Display name for the UI |
| `template_content` | Text | The actual prompt string with `{placeholders}` |
| `is_system_default` | Boolean | Flag indicating if it's a factory setting |
| `parameters` | JSON | Metadata about available variables |

**Sources:** [backend/app/models/prompt_template.py:1-25](), [backend/app/schemas/prompt_template.py:7-42]()

---

## RTCO Framework and Prompt Design

MuMuAINovel utilizes the **RTCO (Role, Task, Context, Output)** framework for its V2 prompts to maximize LLM adherence to complex instructions.

### 1. World Building (`WORLD_BUILDING`)
Generates the foundational "bible" of the story.
- **Task**: Create a JSON object with `time_period`, `location`, `atmosphere`, and `rules` [backend/app/services/prompt_service.py:132-176]().
- **Constraints**: Enforces genre-specific logic (e.g., avoiding "apocalyptic" themes in modern romance) [backend/app/services/prompt_service.py:104-130]().

### 2. Batch Character Generation (`CHARACTERS_BATCH_GENERATION`)
Generates multiple entities and their relationships simultaneously.
- **Entity Types**: Protagonists, supporting characters, and high-influence organizations [backend/app/services/prompt_service.py:205-210]().
- **Relationship Integrity**: Includes a "no-hallucination" constraint where relationships can only reference characters within the same generated batch [backend/app/services/prompt_service.py:300-305]().

### 3. Outline and Expansion (`OUTLINE_CREATE`, `PLOT_EXPANSION_V2`)
Handles the transition from a high-level summary to a detailed chapter-by-chapter plan.
- **Expansion Logic**: Breaks a single outline point into a detailed `expansion_plan` containing multiple scenes, character motivations, and emotional beats [backend/app/services/prompt_service.py:320-390]().

**Sources:** [backend/app/services/prompt_service.py:78-317]()

---

## Context Injection and Style Application

The system dynamically builds the prompt by injecting database entities into templates.

### Writing Style Manager
The `WritingStyleManager` class [backend/app/services/prompt_service.py:6-23]() appends specific stylistic requirements to the base prompt.

```python
# Implementation of style application
@staticmethod
def apply_style_to_prompt(base_prompt: str, style_content: str) -> str:
    return f"{base_prompt}\n\n{style_content}\n\n请直接输出章节正文内容..."
```

### Context Mapping (Natural Language to Code)

The following diagram illustrates how database models are transformed into the "Context" section of an AI prompt.

```mermaid
graph LR
    subgraph "Code Entity Space (SQLAlchemy Models)"
        M_Project["Project Model"]
        M_Char["Character Model"]
        M_Out["Outline Model"]
        M_Style["WritingStyle Model"]
    end

    subgraph "Natural Language Space (AI Prompt)"
        P_Info["【项目信息】<br/>title, genre, theme"]
        P_World["【世界观信息】<br/>time_period, rules"]
        P_Chars["【角色列表】<br/>name, personality, traits"]
        P_Style["【写作风格】<br/>narrative voice instructions"]
    end

    M_Project -->|mapped via| P_Info
    M_Project -->|mapped via| P_World
    M_Char -->|serialized to| P_Chars
    M_Style -->|appended as| P_Style
```

**Sources:** [backend/app/services/prompt_service.py:10-22](), [backend/app/api/wizard_stream.py:65-72]()

---

## Technical Implementation of SSE Generation

The `wizard_stream.py` module demonstrates how prompts are utilized in a streaming context.

1. **Template Retrieval**: Calls `PromptService.get_template("WORLD_BUILDING", user_id, db)` [backend/app/api/wizard_stream.py:65]().
2. **Formatting**: Uses `PromptService.format_prompt()` to inject user inputs like `title` and `theme` [backend/app/api/wizard_stream.py:66-72]().
3. **Execution**: The formatted string is passed to `user_ai_service.generate_text_stream()` [backend/app/api/wizard_stream.py:103-108]().
4. **JSON Cleaning**: Since LLMs often include markdown backticks, the system uses `_clean_json_response()` before parsing the result into a Python dictionary [backend/app/api/wizard_stream.py:156-160]().

### Prompt Parameter Reference (Partial)

| Template Key | Parameters | Role |
|--------------|------------|------|
| `WORLD_BUILDING` | `title`, `genre`, `theme`, `description` | Sets the global setting |
| `CHAPTER_GENERATION` | `outline`, `characters`, `previous_content` | Generates narrative text |
| `NOVEL_COVER` | `title`, `genre`, `theme`, `description` | Generates DALL-E/Midjourney prompts |

**Sources:** [backend/app/services/prompt_service.py:50-73](), [backend/app/api/wizard_stream.py:45-72]()

---

# Page: MCP Plugin System

# MCP Plugin System

<details>
<summary>Relevant source files</summary>

The following files were used as context for generating this wiki page:

- [backend/app/api/mcp_plugins.py](backend/app/api/mcp_plugins.py)
- [backend/app/api/prompt_templates.py](backend/app/api/prompt_templates.py)
- [backend/app/mcp/config.py](backend/app/mcp/config.py)
- [backend/app/mcp/facade.py](backend/app/mcp/facade.py)
- [backend/app/mcp/status_sync.py](backend/app/mcp/status_sync.py)
- [backend/app/schemas/prompt_template.py](backend/app/schemas/prompt_template.py)
- [backend/app/services/json_helper.py](backend/app/services/json_helper.py)
- [backend/app/services/mcp_test_service.py](backend/app/services/mcp_test_service.py)
- [frontend/src/pages/MCPPlugins.tsx](frontend/src/pages/MCPPlugins.tsx)
- [frontend/src/pages/PromptTemplates.tsx](frontend/src/pages/PromptTemplates.tsx)

</details>



The MCP (Model Context Protocol) Plugin System enables external tool integration with the AI generation pipeline. This system allows the AI to query reference materials, call APIs, and access external data sources during content generation, enhancing the quality and accuracy of generated novels.

For information about the core AI service architecture, see [AI Service Architecture](#5.1). For details on how MCP integrates with the prompt system, see [Prompt System](#5.2).

---

## Purpose and Scope

The MCP Plugin System provides:

- **Plugin Management**: Registration, configuration, and lifecycle management of HTTP, SSE, and Streamable HTTP MCP servers [backend/app/mcp/facade.py:63-72]().
- **Tool Discovery**: Automatic detection of available tools from MCP servers using the Model Context Protocol [backend/app/mcp/facade.py:302-332]().
- **AI Integration**: Seamless tool calling during AI text generation via Function Calling [backend/app/services/mcp_test_service.py:192-211]().
- **Testing Framework**: Connection testing and AI-driven tool validation [backend/app/services/mcp_test_service.py:121-137]().
- **Multi-User Isolation**: Per-user plugin configurations with separate MCP client instances [backend/app/mcp/facade.py:179-181]().

This document covers the plugin architecture, tool calling workflow, testing mechanisms, and integration points with the AI generation system.

**Sources**: [backend/app/mcp/facade.py:1-46](), [backend/app/services/mcp_test_service.py:1-25]()

---

## System Architecture

The MCP Plugin System is centered around the `MCPClientFacade`, which acts as a unified entry point for all MCP operations [backend/app/mcp/facade.py:146-163]().

### High-Level Architecture

```mermaid
graph TB
    subgraph "Frontend Layer [frontend/src/pages/MCPPlugins.tsx]"
        SettingsUI["MCPPluginsPage<br/>Plugin Management"]
        TestButton["handleTestPlugin()"]
    end
    
    subgraph "API Layer [backend/app/api/mcp_plugins.py]"
        MCPRouter["/mcp/plugins<br/>list_plugins() / create_plugin()"]
        TestEndpoint["/test_plugin<br/>test_plugin()"]
        ToolsEndpoint["/{plugin_id}/tools<br/>get_plugin_tools()"]
    end
    
    subgraph "Service Layer"
        MCPFacade["MCPClientFacade [backend/app/mcp/facade.py]<br/>Unified Entry Point"]
        MCPTestService["MCPTestService [backend/app/services/mcp_test_service.py]<br/>AI-Driven Testing"]
        StatusSync["status_sync [backend/app/mcp/status_sync.py]<br/>DB State Sync"]
    end
    
    subgraph "MCP Clients"
        SSEClient["sse_client<br/>Server-Sent Events"]
        StreamHTTP["streamablehttp_client<br/>HTTP Stream"]
    end
    
    subgraph "Database"
        MCPPluginTable[("MCPPlugin Table<br/>models/mcp_plugin.py")]
    end
    
    SettingsUI -->|mcpPluginApi| MCPRouter
    MCPRouter --> MCPFacade
    MCPRouter --> MCPTestService
    
    MCPTestService -->|test_connection()| MCPFacade
    MCPFacade --> SSEClient
    MCPFacade --> StreamHTTP
    
    MCPFacade -->|StatusCallback| StatusSync
    StatusSync -->|Async Update| MCPPluginTable
```

**Sources**: [backend/app/mcp/facade.py:146-201](), [backend/app/api/mcp_plugins.py:30-140](), [backend/app/mcp/status_sync.py:1-15]()

---

## Plugin Types and Configuration

The system supports various HTTP-based MCP protocols. Configuration is often handled via a standard MCP JSON format in the frontend [frontend/src/pages/MCPPlugins.tsx:195-204]().

### Plugin Type Comparison

| Feature | HTTP / Streamable HTTP | SSE (Server-Sent Events) |
|---------|-----------------------|--------------------------|
| **Communication** | REST / Streaming HTTP | Persistent Event Stream |
| **Client Class** | `streamablehttp_client` | `sse_client` |
| **Required Fields** | `server_url`, `headers` | `server_url`, `headers` |
| **Typical Use** | Fast API-based tools | Long-running stateful tools |

### Data Model

The `MCPPlugin` configuration is managed through the `MCPPluginConfig` dataclass in the backend [backend/app/mcp/facade.py:64-72]().

**Key Configuration Fields**:
- `user_id`: For multi-user isolation [backend/app/mcp/facade.py:66]().
- `plugin_name`: Unique identifier for the session key [backend/app/mcp/facade.py:202-204]().
- `url`: The endpoint of the MCP server [backend/app/mcp/facade.py:68]().
- `plugin_type`: One of `streamable_http`, `sse`, or `http` [backend/app/mcp/facade.py:69]().

**Sources**: [backend/app/mcp/facade.py:64-72](), [backend/app/mcp/config.py:7-39]()

---

## Tool Discovery Mechanism

The `MCPClientFacade` handles tool discovery by communicating with the remote server and caching the results to improve performance [backend/app/mcp/facade.py:184-186]().

### Discovery Workflow

```mermaid
sequenceDiagram
    participant UI as MCPPluginsPage
    participant API as mcp_plugins.py
    participant Facade as MCPClientFacade
    participant Session as ClientSession
    participant Server as Remote MCP Server
    
    UI->>API: GET /mcp/plugins/{id}/tools
    API->>Facade: get_tools(user_id, plugin_name)
    
    Facade->>Facade: Check _tool_cache
    alt Cache Miss
        Facade->>Session: session.list_tools()
        Session->>Server: [MCP Protocol] listTools
        Server-->>Session: { tools: [...] }
        Session-->>Facade: List[Tool]
        Facade->>Facade: Update _tool_cache
    end
    
    Facade-->>API: List[Tool]
    API-->>UI: Return tools to frontend
```

### Tool Format Conversion

To integrate with LLMs, MCP tools are converted to the OpenAI Function Calling format using `format_tools_for_openai()` [backend/app/mcp/facade.py:382-414]().

**Conversion Logic**:
- `name`: Prefixed with the plugin name (e.g., `plugin_name__tool_name`) to avoid collisions [backend/app/mcp/facade.py:404]().
- `description`: Mapping the MCP tool description [backend/app/mcp/facade.py:407]().
- `parameters`: Mapping the `inputSchema` from MCP to OpenAI `parameters` [backend/app/mcp/facade.py:408]().

**Sources**: [backend/app/mcp/facade.py:382-414](), [backend/app/services/mcp_test_service.py:192-196]()

---

## Integration with AI Generation

The system uses `AIService` to bridge the gap between user prompts and MCP tools.

### Tool Calling Workflow

1. **Discovery**: `AIService` retrieves enabled tools for the user [backend/app/api/mcp_plugins.py:140-164]().
2. **Formatting**: Tools are converted to OpenAI format [backend/app/mcp/facade.py:382]().
3. **LLM Interaction**: The LLM is called with `tools` and `tool_choice="auto"` [backend/app/services/mcp_test_service.py:206-211]().
4. **Execution**: If the LLM returns `tool_calls`, the `MCPClientFacade` executes them via `call_tool()` [backend/app/mcp/facade.py:334-380]().

**Sources**: [backend/app/mcp/facade.py:334-380](), [backend/app/services/mcp_test_service.py:206-215]()

---

## Testing System

The `MCPTestService` provides sophisticated validation including "AI-Driven Testing" where an AI model is used to generate valid test arguments for the plugin's tools [backend/app/services/mcp_test_service.py:121-137]().

### AI-Driven Testing Flow

```mermaid
graph TD
    subgraph "Test Logic [backend/app/services/mcp_test_service.py]"
        Start[test_plugin_with_ai] --> Conn[test_plugin_connection]
        Conn --> GetTools[mcp_client.get_tools]
        GetTools --> AISetup[create_user_ai_service]
        AISetup --> Prompt[prompt_service.get_mcp_tool_test_prompts]
        Prompt --> AICall[ai_service.generate_text with tools]
        AICall --> Exec[mcp_client.call_tool]
        Exec --> Result[Return MCPTestResult]
    end
```

**Sources**: [backend/app/services/mcp_test_service.py:121-295](), [backend/app/mcp/facade.py:72-100]()

---

## Plugin Management and Safety

### Configuration Consistency Check
The frontend monitors for changes in the global AI model configuration (e.g., changing from GPT-4 to a model that might not support Function Calling). If a change is detected, it automatically disables all MCP plugins to prevent errors [frontend/src/pages/MCPPlugins.tsx:116-143]().

### Status Synchronization
The system uses a background worker and an `asyncio.Queue` to synchronize in-memory plugin status (e.g., `active`, `degraded`, `error`) to the database without blocking the main request thread [backend/app/mcp/status_sync.py:21-37]().

### Multi-User Isolation
Isolation is enforced via the `SessionInfo` structure and unique keys generated from `user_id` and `plugin_name` [backend/app/mcp/facade.py:76-88]().
- **User Locks**: Fine-grained `asyncio.Lock` per user ensures that one user's slow MCP server doesn't block another user [backend/app/mcp/facade.py:206-211]().
- **Session Expiry**: Inactive sessions are cleaned up automatically based on `CLEANUP_INTERVAL_SECONDS` [backend/app/mcp/facade.py:231-241]().

**Sources**: [frontend/src/pages/MCPPlugins.tsx:116-143](), [backend/app/mcp/status_sync.py:67-88](), [backend/app/mcp/facade.py:179-181](), [backend/app/mcp/config.py:11-13]()

---

# Page: AI Provider Configuration

# AI Provider Configuration

<details>
<summary>Relevant source files</summary>

The following files were used as context for generating this wiki page:

- [backend/app/api/settings.py](backend/app/api/settings.py)
- [backend/app/logger.py](backend/app/logger.py)
- [backend/app/schemas/settings.py](backend/app/schemas/settings.py)
- [backend/app/services/ai_clients/anthropic_client.py](backend/app/services/ai_clients/anthropic_client.py)
- [backend/app/services/ai_clients/gemini_client.py](backend/app/services/ai_clients/gemini_client.py)
- [backend/app/services/ai_clients/openai_client.py](backend/app/services/ai_clients/openai_client.py)
- [backend/app/services/ai_metrics.py](backend/app/services/ai_metrics.py)
- [backend/app/services/ai_providers/anthropic_provider.py](backend/app/services/ai_providers/anthropic_provider.py)
- [backend/app/services/ai_providers/gemini_provider.py](backend/app/services/ai_providers/gemini_provider.py)
- [backend/app/services/ai_providers/openai_provider.py](backend/app/services/ai_providers/openai_provider.py)
- [frontend/src/pages/Settings.tsx](frontend/src/pages/Settings.tsx)

</details>



## Purpose and Scope

This document describes how users configure AI provider settings in MuMuAINovel, including API keys, base URLs, model selection, and generation parameters. These settings control how the application interacts with external AI services (OpenAI, Anthropic Claude, Google Gemini) for content generation.

The system supports a multi-provider architecture where users can maintain global settings or create "API Presets" to quickly switch between different models and providers.

---

## Configuration Data Model

The system uses a `Settings` entity to store per-user AI provider configuration. Each user maintains their own independent settings in the database, enabling multi-tenant configuration isolation.

### Settings Schema

```mermaid
classDiagram
    class Settings {
        +string id PK
        +string user_id UK
        +string api_provider
        +string api_key
        +string api_base_url
        +string llm_model
        +float temperature
        +int max_tokens
        +string system_prompt
        +string preferences
        +datetime created_at
        +datetime updated_at
    }
    
    class SettingsBase {
        +Optional~string~ api_provider = "openai"
        +Optional~string~ api_key = None
        +Optional~string~ api_base_url = None
        +Optional~string~ llm_model = "gpt-4"
        +Optional~float~ temperature = 0.7
        +Optional~int~ max_tokens = 2000
        +Optional~string~ system_prompt = None
    }
    
    class SettingsResponse {
        <<inherits SettingsBase>>
        +string id
        +string user_id
        +datetime created_at
        +datetime updated_at
    }
    
    SettingsBase <|-- SettingsResponse
```

**Sources:** [backend/app/schemas/settings.py:7-44](), [backend/app/models/settings.py:1-30]()

---

## Configuration Parameters

### API Provider

The `api_provider` field determines which AI service backend to use. The system currently supports:

| Provider | Value | Default Base URL | Implementation Class |
|----------|-------|------------------|----------------------|
| OpenAI | `openai` | `https://api.openai.com/v1` | `OpenAIProvider` |
| Anthropic Claude | `anthropic` | `https://api.anthropic.com` | `AnthropicProvider` |
| Google Gemini | `gemini` | `https://generativelanguage.googleapis.com/v1beta` | `GeminiProvider` |

**Sources:** [backend/app/services/ai_service.py:27-30](), [backend/app/services/ai_clients/openai_client.py:11-12](), [backend/app/services/ai_clients/gemini_client.py:10-15]()

### API Key and Base URL

- **API Key**: Required for authentication. Stored per user.
- **Base URL**: Allows customization for proxies or regional endpoints. For Gemini, the API key is typically passed as a query parameter (`?key=...`), while OpenAI and Anthropic use `Authorization` headers.

**Sources:** [backend/app/services/ai_clients/openai_client.py:14-18](), [backend/app/services/ai_clients/gemini_client.py:57-58]()

### Model and Parameters

- **LLM Model**: The specific model identifier (e.g., `gpt-4o`, `claude-3-5-sonnet-20240620`, `gemini-1.5-pro`).
- **Temperature**: Controls randomness (0.0 to 2.0). Default is 0.7.
- **Max Tokens**: Limits response length. Default is 2000.
- **System Prompt**: A global system-level instruction prepended to all AI requests for the user.

**Sources:** [backend/app/schemas/settings.py:11-17](), [frontend/src/pages/Settings.tsx:114-121]()

---

## API Key Presets

MuMuAINovel allows users to save multiple configurations as "Presets". This is useful for switching between a "Fast" model (like GPT-4o-mini) and a "High Quality" model (like Claude 3.5 Opus) without re-entering API keys.

### Preset Logic Flow

```mermaid
sequenceDiagram
    participant User
    participant Frontend as SettingsPage.tsx
    participant Backend as settings.py
    participant DB as SQLite (Settings/Presets)

    User->>Frontend: Select "Presets" Tab
    Frontend->>Backend: GET /settings/presets
    Backend->>DB: SELECT * FROM api_key_presets
    DB-->>Frontend: List of Presets
    
    User->>Frontend: Click "Activate" on Preset
    Frontend->>Backend: POST /settings/presets/{id}/activate
    Backend->>DB: Update active_preset_id
    Backend->>DB: Sync Preset Config -> Main Settings
    Backend-->>User: Success (Settings Updated)
```

**Sources:** [frontend/src/pages/Settings.tsx:46-54](), [backend/app/api/settings.py:348-385](), [backend/app/schemas/settings.py:89-143]()

---

## Connection Testing

Before saving settings, users can test the connection to ensure the API key and Base URL are valid.

### Test Workflow

1. **Frontend**: Collects current form values and sends to `/settings/test`.
2. **Backend**: Creates a temporary `AIService` instance using the provided credentials.
3. **Execution**: Sends a minimal "Hello" prompt to the provider.
4. **Metrics**: Captures response time, token usage, and any error details.

```mermaid
flowchart TD
    subgraph "Frontend"
        Btn["Click 'Test Connection'"]
        UI_Res["Show Result/Error/Suggestions"]
    end

    subgraph "Backend (/settings/test)"
        CreateSvc["create_user_ai_service()"]
        CallAI["ai_service.generate('Hello')"]
        CatchErr["Catch Provider Errors"]
    end

    Btn --> CreateSvc
    CreateSvc --> CallAI
    CallAI -->|Success| UI_Res
    CallAI -->|Failure| CatchErr
    CatchErr -->|Format Suggestions| UI_Res
```

**Sources:** [frontend/src/pages/Settings.tsx:210-255](), [backend/app/api/settings.py:293-345]()

---

## Provider Implementation Details

### OpenAI Implementation
Uses standard `chat/completions` endpoint. Supports tool calls and streaming.
**Sources:** [backend/app/services/ai_clients/openai_client.py:11-87]()

### Anthropic Implementation
Uses the Anthropic Python SDK (`AsyncAnthropic`). Handles system prompts via a specific `system` parameter rather than a message role.
**Sources:** [backend/app/services/ai_clients/anthropic_client.py:12-74]()

### Gemini Implementation
Uses the Google Generative AI REST API. Requires converting OpenAI-style messages/tools to Gemini's `contents` and `functionDeclarations` format.
**Sources:** [backend/app/services/ai_clients/gemini_client.py:10-115]()

---

## Summary of Configuration Flow

```mermaid
graph TB
    subgraph "Natural Language Space"
        UserIntent["'I want to use Claude 3.5 Sonnet'"]
    end

    subgraph "Code Entity Space"
        UI["Settings.tsx Form"]
        Schema["SettingsUpdate (Pydantic)"]
        Service["AIService (Factory)"]
        Client["AnthropicClient"]
    end

    UserIntent -->|Inputs Key/Model| UI
    UI -->|Validates| Schema
    Schema -->|Dependency Injection| Service
    Service -->|Instantiates| Client
    Client -->|REST API| ExternalAI["Anthropic API"]
```

**Sources:** [frontend/src/pages/Settings.tsx:130-150](), [backend/app/api/settings.py:101-159](), [backend/app/services/ai_service.py:27-30]()

---

# Page: Server-Sent Events (SSE) for Streaming

# Server-Sent Events (SSE) for Streaming

<details>
<summary>Relevant source files</summary>

The following files were used as context for generating this wiki page:

- [backend/app/api/chapters.py](backend/app/api/chapters.py)
- [backend/app/api/inspiration.py](backend/app/api/inspiration.py)
- [backend/app/schemas/chapter.py](backend/app/schemas/chapter.py)
- [backend/app/services/auto_character_service.py](backend/app/services/auto_character_service.py)
- [backend/app/services/auto_organization_service.py](backend/app/services/auto_organization_service.py)
- [backend/app/services/plot_expansion_service.py](backend/app/services/plot_expansion_service.py)
- [backend/app/utils/sse_response.py](backend/app/utils/sse_response.py)
- [frontend/src/components/AIProjectGenerator.tsx](frontend/src/components/AIProjectGenerator.tsx)
- [frontend/src/components/ExpansionPlanEditor.tsx](frontend/src/components/ExpansionPlanEditor.tsx)
- [frontend/src/components/SSEProgressModal.tsx](frontend/src/components/SSEProgressModal.tsx)
- [frontend/src/pages/Chapters.tsx](frontend/src/pages/Chapters.tsx)
- [frontend/src/pages/Inspiration.tsx](frontend/src/pages/Inspiration.tsx)
- [frontend/src/pages/ProjectWizardNew.tsx](frontend/src/pages/ProjectWizardNew.tsx)
- [frontend/src/store/hooks.ts](frontend/src/store/hooks.ts)
- [frontend/src/utils/sseClient.ts](frontend/src/utils/sseClient.ts)

</details>



This page provides technical details on the Server-Sent Events (SSE) implementation in MuMuAINovel. SSE is the primary mechanism for real-time AI generation, progress tracking, and long-running background tasks, ensuring a responsive user experience during intensive AI operations.

## SSE Architecture Overview

MuMuAINovel utilizes a hybrid "POST-to-Stream" pattern. While standard SSE uses `GET` requests, the system implements a custom `SSEPostClient` that uses the `fetch` API to send complex JSON configurations via `POST` and then processes the response body as a stream of events. This allows sending detailed generation parameters (e.g., character lists, plot requirements) that would exceed URL length limits.

### System-to-Code Mapping

The following diagram bridges the high-level streaming concepts to specific backend and frontend entities.

**Streaming Data Flow**
```mermaid
graph TD
    subgraph "Frontend (React)"
        A["SSEPostClient"] -->|"POST /api/.../stream"| B["SSEProgressModal"]
        A -->|"onChunk callback"| C["Chapters.tsx / Outline.tsx"]
    end

    subgraph "Backend (FastAPI)"
        D["APIRouter (e.g., chapters.py)"] -->|"create_sse_response"| E["SSEResponse (sse_response.py)"]
        E -->|"yields"| F["Async Generator Functions"]
    end

    subgraph "AI & Data Layer"
        F -->|"calls"| G["AIService (ai_service.py)"]
        F -->|"commits"| H["AsyncSession (SQLAlchemy)"]
    end

    style A stroke-width:2px
    style D stroke-width:2px
    style G stroke-width:2px
```
Sources: [backend/app/utils/sse_response.py:1-20](), [frontend/src/utils/sseClient.ts:125-140](), [backend/app/api/chapters.py:974-985]()

---

## Backend Implementation

### SSEResponse Utility
The `SSEResponse` class in `backend/app/utils/sse_response.py` standardizes the event format sent to the client. It wraps data into a specific JSON structure recognized by the frontend.

| Event Type | Method | Payload Key | Purpose |
| :--- | :--- | :--- | :--- |
| `progress` | `send_progress` | `progress`, `message` | Updates UI progress bars and status text. |
| `chunk` | `send_chunk` | `content` | Incremental text fragments from the LLM. |
| `result` | `send_result` | `data` | Final structured data (e.g., a created Project ID). |
| `error` | `send_error` | `error`, `code` | Reports failures and stops the stream. |
| `done` | `send_done` | N/A | Signals successful completion of the generator. |

Sources: [backend/app/utils/sse_response.py:23-110]()

### Async Generator Pattern
All streaming endpoints utilize Python `AsyncGenerator` to yield events. This prevents blocking the event loop during long AI calls.

**Chapter Generation Example:**
In `backend/app/api/chapters.py`, the `generate_chapter_stream` function (invoked via `POST /chapters/{chapter_id}/generate-stream`) follows this lifecycle:
1. **Context Building**: Uses `OneToManyContextBuilder` or `OneToOneContextBuilder` to gather project background [backend/app/api/chapters.py:14-17]().
2. **AI Stream**: Calls `ai_service.generate_text_stream` [backend/app/api/chapters.py:1020-1030]().
3. **Chunking**: Yields `SSEResponse.send_chunk(chunk)` as text arrives.
4. **Finalization**: Saves the accumulated content to the `Chapter` model and commits the transaction [backend/app/api/chapters.py:1060-1075]().

---

## Frontend Implementation

### SSEPostClient
The frontend uses a custom client located in `frontend/src/utils/sseClient.ts`. Unlike the native `EventSource`, this client supports `POST` bodies and `AbortController` for cancelling generations.

**Key Logic:**
- **Connection**: Uses `fetch` with a `POST` method [frontend/src/utils/sseClient.ts:149-155]().
- **Reading**: Uses a `ReadableStreamDefaultReader` to process chunks of bytes [frontend/src/utils/sseClient.ts:162-170]().
- **Buffering**: Accumulates partial lines and splits by `\n\n` to handle the SSE protocol format [frontend/src/utils/sseClient.ts:179-182]().

Sources: [frontend/src/utils/sseClient.ts:125-214]()

### UI Integration
Components like `Chapters.tsx` and `Outline.tsx` use the `SSEProgressModal` to display real-time feedback.

```mermaid
sequenceDiagram
    participant UI as Chapters.tsx
    participant Client as SSEPostClient
    participant Modal as SSEProgressModal
    participant API as FastAPI Backend

    UI->>Client: connect(url, data)
    Client->>API: POST /generate-stream
    API-->>Client: data: {"type": "progress", "progress": 10}
    Client->>Modal: updateProgress(10)
    API-->>Client: data: {"type": "chunk", "content": "Once upon..."}
    Client->>UI: onChunk("Once upon...")
    API-->>Client: data: {"type": "done"}
    Client->>UI: onComplete()
    UI->>Modal: close()
```
Sources: [frontend/src/pages/Chapters.tsx:96-114](), [frontend/src/utils/sseClient.ts:217-250]()

---

## Specialized Streaming Workflows

### 1. Wizard and Inspiration Mode
The `ProjectWizardNew` and `Inspiration` pages use SSE to handle multi-step generation (World Building -> Characters -> Outline).
- **Step-by-step Options**: `Inspiration.tsx` calls `/inspiration/generate-options` which returns structured JSON options via a stream [backend/app/api/inspiration.py:69-75]().
- **Progressive Persistence**: The backend commits each step to the database as it completes, allowing users to resume if the connection drops [frontend/src/components/AIProjectGenerator.tsx:88-96]().

### 2. Batch Generation
The system supports generating up to 20 chapters in a single stream.
- **Task Tracking**: Uses `BatchGenerationTask` to maintain state [backend/app/api/chapters.py:28]().
- **Sequential Streaming**: The generator yields progress for the entire batch while streaming content for the "current" chapter [backend/app/api/chapters.py:126-140]().

### 3. Transaction Management & Error Handling
To ensure data integrity, the backend uses a `db_committed` flag. If the client disconnects (`GeneratorExit`) before the final `db.commit()`, the transaction is rolled back.

```python
# Pattern used in backend/app/api/wizard_stream.py
db_committed = False
try:
    # ... generation logic ...
    await db.commit()
    db_committed = True
    yield await SSEResponse.send_done()
except Exception as e:
    if not db_committed:
        await db.rollback()
    yield await SSEResponse.send_error(str(e))
```
Sources: [backend/app/api/chapters.py:65-74](), [backend/app/utils/sse_response.py:115-130]()

---

## Performance and Reliability

### Heartbeat Mechanism
To prevent proxies (like Nginx) from closing "idle" connections during long AI thinking periods, the backend sends periodic heartbeats.
- **Implementation**: `SSEResponse.send_heartbeat()` sends a comment or a timestamp event [backend/app/utils/sse_response.py:132-138]().
- **Client Side**: The `SSEPostClient` ignores heartbeat types but the activity keeps the TCP connection alive.

### Buffer Management
On the frontend, `SSEPostClient` maintains an `accumulatedContent` string. This is useful for components that need the full result at the end of the stream without managing state for every individual chunk [frontend/src/utils/sseClient.ts:130-131]().

Sources: [frontend/src/utils/sseClient.ts:231-236](), [backend/app/utils/sse_response.py:140-150]()

---

# Page: Frontend Guide

# Frontend Guide

<details>
<summary>Relevant source files</summary>

The following files were used as context for generating this wiki page:

- [backend/app/main.py](backend/app/main.py)
- [frontend/src/App.tsx](frontend/src/App.tsx)
- [frontend/src/pages/ProjectDetail.tsx](frontend/src/pages/ProjectDetail.tsx)
- [frontend/src/pages/WritingStyles.tsx](frontend/src/pages/WritingStyles.tsx)
- [frontend/src/services/api.ts](frontend/src/services/api.ts)
- [frontend/src/types/index.ts](frontend/src/types/index.ts)

</details>



## Overview

This document provides a comprehensive overview of the MuMuAINovel React frontend application. The frontend is a single-page application (SPA) built with React 18, TypeScript, and Ant Design 5.x, communicating with the FastAPI backend via REST APIs and Server-Sent Events (SSE) for streaming AI generation.

**Key Architectural Characteristics:**

- **Component-Based Architecture:** Modular React components organized by feature [frontend/src/App.tsx:2-26]().
- **Type-Safe Development:** Full TypeScript coverage with shared interfaces matching backend schemas [frontend/src/types/index.ts:1-300]().
- **Lightweight State Management:** Zustand for global state management with minimal boilerplate [frontend/src/store/index.ts]().
- **Real-Time Streaming:** Custom SSE client integration for live AI generation progress [frontend/src/utils/sseClient.ts]().
- **Protected Routing:** React Router with authentication guards [frontend/src/components/ProtectedRoute.tsx]().
- **Modular API Layer:** Service objects for clean backend integration using Axios [frontend/src/services/api.ts:152-250]().

For detailed information on specific subsystems, see:

- **[Routing and Navigation](#6.1)** - React Router configuration and protected routes.
- **[API Client Layer](#6.2)** - Axios-based API services and error handling.
- **[State Management](#6.3)** - Zustand stores and synchronization hooks.
- **[Wizard and Inspiration Interfaces](#6.4)** - Project creation workflows.
- **[Chapter Interface](#6.5)** - Chapter writing and generation UI.
- **[Outline Interface](#6.6)** - Outline management and expansion UI.
- **[Expansion Plan Editor](#6.7)** - Chapter planning interface.
- **[Settings Interface](#6.8)** - AI provider and API key configuration UI.

**Sources:** [frontend/src/App.tsx:1-80](), [frontend/src/services/api.ts:1-150](), [frontend/src/types/index.ts:1-250]()

## Technology Stack

The frontend is built with the following core technologies:

| Technology | Version | Purpose | Key Files |
|------------|---------|---------|-----------|
| **React** | 18.x | UI component library | [frontend/src/App.tsx]() |
| **TypeScript** | 5.x | Type-safe JavaScript | [frontend/src/types/index.ts]() |
| **Ant Design** | 5.x | UI component framework | [frontend/src/App.tsx:3-23]() |
| **React Router** | 6.x | Client-side routing | [frontend/src/App.tsx:1]() |
| **Zustand** | 4.x | State management | [frontend/src/store/index.ts]() |
| **Axios** | 1.x | HTTP client | [frontend/src/services/api.ts:1-75]() |

**Sources:** [frontend/src/App.tsx:1-30](), [frontend/src/services/api.ts:68-75]()

## Directory Structure

The frontend follows a feature-organized structure with clear separation of concerns:

```
frontend/
├── src/
│   ├── App.tsx                     # Root component with BrowserRouter
│   ├── pages/                      # Page-level route components
│   │   ├── Login.tsx               # Auth entry [frontend/src/pages/Login.tsx]()
│   │   ├── ProjectList.tsx         # Dashboard [frontend/src/pages/ProjectList.tsx]()
│   │   ├── ProjectWizardNew.tsx    # Guided creation [frontend/src/pages/ProjectWizardNew.tsx]()
│   │   ├── Inspiration.tsx         # Conversational mode [frontend/src/pages/Inspiration.tsx]()
│   │   ├── ProjectDetail.tsx       # Layout for project routes [frontend/src/pages/ProjectDetail.tsx]()
│   │   ├── Chapters.tsx            # Chapter management [frontend/src/pages/Chapters.tsx]()
│   │   └── WritingStyles.tsx       # Style management [frontend/src/pages/WritingStyles.tsx]()
│   ├── components/                 # Reusable UI components
│   │   ├── ProtectedRoute.tsx      # Auth guard [frontend/src/components/ProtectedRoute.tsx]()
│   │   └── SpringFestival.tsx      # Seasonal UI [frontend/src/components/SpringFestival.tsx]()
│   ├── services/                   # API client layer
│   │   └── api.ts                  # Central API definitions [frontend/src/services/api.ts]()
│   ├── store/                      # Zustand state management
│   │   ├── index.ts                # Main store [frontend/src/store/index.ts]()
│   │   └── hooks.ts                # Sync hooks [frontend/src/store/hooks.ts]()
│   └── types/                      # TS definitions [frontend/src/types/index.ts]()
```

**Sources:** [frontend/src/App.tsx:2-30](), [frontend/src/pages/ProjectDetail.tsx:115-188]()

## Frontend Architecture Diagram

### System Entity Mapping

This diagram bridges the Natural Language concepts to the specific Code Entities used in the frontend implementation.

```mermaid
graph TD
    subgraph "Natural Language Space"
        User["Writer"]
        Project["Novel Project"]
        Chapter["Story Chapter"]
        AI["AI Assistant"]
    end

    subgraph "Code Entity Space (Frontend)"
        Auth["authApi / ProtectedRoute"]
        P_Store["useStore / currentProject"]
        C_Page["Chapters.tsx / ChapterReader.tsx"]
        SSE["ssePost / SSEClientOptions"]
        API["api (AxiosInstance)"]
    end

    User --> Auth
    Project --> P_Store
    Chapter --> C_Page
    AI --> SSE
    SSE --> API
    API --> Auth
```

**Sources:** [frontend/src/services/api.ts:68-150](), [frontend/src/App.tsx:43-73](), [frontend/src/store/index.ts]()

### Navigation and Data Flow

```mermaid
graph TB
    subgraph Browser["Browser Environment"]
        LocalStorage["localStorage<br/>- sidebarCollapsed"]
    end
    
    subgraph ReactApp["React Application (App.tsx)"]
        Routes["Routes"]
        
        subgraph Public["Public"]
            Login["Login.tsx"]
        end
        
        subgraph Protected["Protected (ProtectedRoute)"]
            Dashboard["ProjectList.tsx"]
            Wizard["ProjectWizardNew.tsx"]
            Detail["ProjectDetail.tsx (Parent)"]
            
            subgraph Nested["Project Sub-pages"]
                World["WorldSetting.tsx"]
                Outline["Outline.tsx"]
                Chars["Characters.tsx"]
                Chaps["Chapters.tsx"]
                Styles["WritingStyles.tsx"]
            end
        end
    end
    
    subgraph Services["Services & State"]
        Store["useStore (Zustand)"]
        SyncHooks["useChapterSync / useOutlineSync"]
        APILayer["api.ts (Axios)"]
    end

    Login --> LocalStorage
    Dashboard --> Store
    Detail --> SyncHooks
    SyncHooks --> APILayer
    APILayer --> Store
    Detail --> Nested
```

**Sources:** [frontend/src/App.tsx:43-73](), [frontend/src/pages/ProjectDetail.tsx:78-110](), [frontend/src/services/api.ts:152-230]()

## Routing Overview

The application uses React Router v6 with nested routes and authentication protection. The configuration is defined in `App.tsx` [frontend/src/App.tsx:43-73]().

### Key Routes

| Path | Component | Description |
|------|-----------|-------------|
| `/login` | `Login` | Auth entry point [frontend/src/App.tsx:44]() |
| `/projects` | `ProjectList` | Main dashboard [frontend/src/App.tsx:48]() |
| `/wizard` | `ProjectWizardNew` | Guided project setup [frontend/src/App.tsx:49]() |
| `/project/:projectId` | `ProjectDetail` | Parent layout for project content [frontend/src/App.tsx:56]() |
| `.../chapters` | `Chapters` | Chapter management sub-page [frontend/src/App.tsx:65]() |
| `.../writing-styles`| `WritingStyles` | Style management sub-page [frontend/src/App.tsx:68]() |

For details on navigation flow and guards, see **[Routing and Navigation](#6.1)**.

**Sources:** [frontend/src/App.tsx:43-73]()

## State Management and Data Sync

The frontend utilizes **Zustand** for global state and custom hooks for synchronizing data with the backend.

- **`useStore`**: Central store for projects, current project context, and loading states [frontend/src/store/index.ts]().
- **Synchronization Hooks**: Specialized hooks like `useCharacterSync`, `useOutlineSync`, and `useChapterSync` handle the fetching and store updates for specific project domains [frontend/src/pages/ProjectDetail.tsx:78-80]().
- **Initialization**: `ProjectDetail` orchestrates the initial data load when a project is selected, calling `refreshOutlines`, `refreshCharacters`, and `refreshChapters` in parallel [frontend/src/pages/ProjectDetail.tsx:82-105]().

For details, see **[State Management](#6.3)**.

**Sources:** [frontend/src/pages/ProjectDetail.tsx:66-110](), [frontend/src/store/index.ts]()

## API and Communication

The API layer is built on **Axios** with interceptors for global error handling and authentication status monitoring [frontend/src/services/api.ts:86-150]().

- **Auth Interceptor**: Detects `401 Unauthorized` responses and redirects to `/login` [frontend/src/services/api.ts:101-117]().
- **Streaming (SSE)**: Uses `ssePost` for real-time AI content generation, such as world building and chapter writing [frontend/src/services/api.ts:3]().
- **Service Objects**: Grouped API calls (e.g., `authApi`, `projectApi`, `writingStyleApi`) provide a clean interface for components [frontend/src/services/api.ts:152-250]().

For details, see **[API Client Layer](#6.2)**.

**Sources:** [frontend/src/services/api.ts:1-150]()

## Core Feature Interfaces

The frontend is divided into several specialized interfaces:

- **Creation Interfaces**: `ProjectWizardNew` and `Inspiration` provide structured and conversational paths to start new projects. For details, see **[Wizard and Inspiration Interfaces](#6.4)**.
- **Content Management**: `Chapters` and `Outline` manage the core story structure. `Chapters` supports batch generation and analysis [frontend/src/pages/Chapters.tsx](). For details, see **[Chapter Interface](#6.5)** and **[Outline Interface](#6.6)**.
- **Writing Tools**: `WritingStyles` allows users to define custom AI prompts for specific prose styles [frontend/src/pages/WritingStyles.tsx:88-105](). For details, see **[Settings Interface](#6.8)**.

**Sources:** [frontend/src/pages/ProjectDetail.tsx:115-188](), [frontend/src/pages/WritingStyles.tsx:32-60]()

---

# Page: Routing and Navigation

# Routing and Navigation

<details>
<summary>Relevant source files</summary>

The following files were used as context for generating this wiki page:

- [backend/app/main.py](backend/app/main.py)
- [frontend/src/App.tsx](frontend/src/App.tsx)
- [frontend/src/components/AnnouncementModal.tsx](frontend/src/components/AnnouncementModal.tsx)
- [frontend/src/index.css](frontend/src/index.css)
- [frontend/src/pages/AuthCallback.tsx](frontend/src/pages/AuthCallback.tsx)
- [frontend/src/pages/ProjectDetail.tsx](frontend/src/pages/ProjectDetail.tsx)
- [frontend/src/pages/WritingStyles.tsx](frontend/src/pages/WritingStyles.tsx)

</details>



## Purpose and Scope

This document describes the frontend routing architecture in MuMuAINovel, including route configuration, authentication protection, and navigation patterns. The routing system uses React Router v6 to manage client-side navigation between different views of the application.

For information about state management during navigation, see [State Management](6.3). For details on the authentication mechanism that protects routes, see [User Authentication and Authorization](7.3).

## Route Configuration Overview

The application uses a centralized route configuration defined in `App.tsx`. All routes are managed by a `BrowserRouter` component with future compatibility flags enabled.

**Route Hierarchy Diagram**

```mermaid
graph TB
    BrowserRouter["BrowserRouter<br/>(with v7 future flags)"]
    
    subgraph "Public Routes"
        LoginRoute["/login → Login"]
        CallbackRoute["/auth/callback → AuthCallback"]
    end
    
    subgraph "Protected Top-Level Routes"
        RootRoute["/ → ProjectList"]
        ProjectsRoute["/projects → ProjectList"]
        WizardRoute["/wizard → ProjectWizardNew"]
        InspirationRoute["/inspiration → Inspiration"]
        SettingsRoute["/settings → Settings"]
        PromptTemplatesRoute["/prompt-templates → PromptTemplates"]
        MCPPluginsRoute["/mcp-plugins → MCPPlugins"]
        UserManagementRoute["/user-management → UserManagement"]
        ChapterReaderRoute["/chapters/:chapterId/reader → ChapterReader"]
    end
    
    subgraph "Protected Nested Routes"
        ProjectRoute["/project/:projectId → ProjectDetail"]
        
        subgraph "Nested Under ProjectDetail"
            IndexRedirect["index → Navigate to sponsor"]
            WorldRoute["world-setting → WorldSetting"]
            CareersRoute["careers → Careers"]
            OutlineRoute["outline → Outline"]
            CharactersRoute["characters → Characters"]
            RelationshipsRoute["relationships → Relationships"]
            RelGraphRoute["relationships-graph → RelationshipGraph"]
            OrganizationsRoute["organizations → Organizations"]
            ChaptersRoute["chapters → Chapters"]
            ChapterAnalysisRoute["chapter-analysis → ChapterAnalysis"]
            ForeshadowsRoute["foreshadows → Foreshadows"]
            StylesRoute["writing-styles → WritingStyles"]
            WorkshopRoute["prompt-workshop → PromptWorkshop"]
            SponsorRoute["sponsor → Sponsor"]
        end
    end
    
    BrowserRouter --> LoginRoute
    BrowserRouter --> CallbackRoute
    BrowserRouter --> RootRoute
    BrowserRouter --> ProjectsRoute
    BrowserRouter --> WizardRoute
    BrowserRouter --> InspirationRoute
    BrowserRouter --> SettingsRoute
    BrowserRouter --> PromptTemplatesRoute
    BrowserRouter --> MCPPluginsRoute
    BrowserRouter --> UserManagementRoute
    BrowserRouter --> ChapterReaderRoute
    BrowserRouter --> ProjectRoute
    
    ProjectRoute --> IndexRedirect
    ProjectRoute --> WorldRoute
    ProjectRoute --> CareersRoute
    ProjectRoute --> OutlineRoute
    ProjectRoute --> CharactersRoute
    ProjectRoute --> RelationshipsRoute
    ProjectRoute --> RelGraphRoute
    ProjectRoute --> OrganizationsRoute
    ProjectRoute --> ChaptersRoute
    ProjectRoute --> ChapterAnalysisRoute
    ProjectRoute --> ForeshadowsRoute
    ProjectRoute --> StylesRoute
    ProjectRoute --> WorkshopRoute
    ProjectRoute --> SponsorRoute
```

Sources: [frontend/src/App.tsx:32-77]()

## Public Routes

The application defines two public routes that do not require authentication:

| Route | Component | Purpose |
|-------|-----------|---------|
| `/login` | `Login` | User authentication entry point (local or OAuth) [frontend/src/App.tsx:44]() |
| `/auth/callback` | `AuthCallback` | OAuth callback handler for LinuxDO integration [frontend/src/App.tsx:45]() |

The `AuthCallback` component handles the post-login logic, including checking for first-time login via cookies to trigger password initialization [frontend/src/AuthCallback.tsx:31-55]().

Sources: [frontend/src/App.tsx:44-45](), [frontend/src/pages/AuthCallback.tsx:27-88]()

## Protected Routes and Authentication Guard

All application features except login are protected by the `ProtectedRoute` component, which wraps routes requiring authentication. The component checks for valid authentication state before rendering child components.

**Protected Route Structure**

```mermaid
graph LR
    Route["Route Definition"]
    ProtectedRoute["ProtectedRoute<br/>Component"]
    AuthCheck{"User<br/>Authenticated?"}
    PageComponent["Page Component<br/>(ProjectList, Settings, etc.)"]
    LoginRedirect["Redirect to /login"]
    
    Route --> ProtectedRoute
    ProtectedRoute --> AuthCheck
    AuthCheck -->|Yes| PageComponent
    AuthCheck -->|No| LoginRedirect
```

The `ProtectedRoute` wrapper is applied to all internal dashboard and project management routes [frontend/src/App.tsx:47-56]().

Sources: [frontend/src/App.tsx:27](), [frontend/src/App.tsx:47-56]()

## Nested Project Routes

The `/project/:projectId` route uses React Router's nested routing feature. The `ProjectDetail` component acts as a layout container with an `<Outlet />` to render specific project modules [frontend/src/pages/ProjectDetail.tsx:2]().

**Project Detail Navigation Mapping**

| Nested Path | Component | Purpose |
|-------------|-----------|---------|
| index | `Navigate` (to `sponsor`) | Default redirect when accessing project root [frontend/src/App.tsx:57]() |
| `world-setting` | `WorldSetting` | Project world-building and background [frontend/src/App.tsx:58]() |
| `careers` | `Careers` | Character profession and power system management [frontend/src/App.tsx:59]() |
| `outline` | `Outline` | Story outlines and expansion plans [frontend/src/App.tsx:60]() |
| `characters` | `Characters` | Detailed character profiles [frontend/src/App.tsx:61]() |
| `relationships` | `Relationships` | Character relationship list [frontend/src/App.tsx:62]() |
| `relationships-graph` | `RelationshipGraph` | Visual relationship network [frontend/src/App.tsx:63]() |
| `organizations` | `Organizations` | Faction and group management [frontend/src/App.tsx:64]() |
| `chapters` | `Chapters` | Chapter management and AI generation [frontend/src/App.tsx:65]() |
| `chapter-analysis` | `ChapterAnalysis` | Plot analysis and memory extraction [frontend/src/App.tsx:66]() |
| `foreshadows` | `Foreshadows` | Tracking plot seeds and payoffs [frontend/src/App.tsx:67]() |
| `writing-styles` | `WritingStyles` | Custom AI writing style configuration [frontend/src/App.tsx:68]() |
| `prompt-workshop` | `PromptWorkshop` | Prompt testing and refinement [frontend/src/App.tsx:69]() |
| `sponsor` | `Sponsor` | Support information [frontend/src/App.tsx:70]() |

### Data Synchronization on Navigation

When navigating to a project-specific route, the `ProjectDetail` component triggers a global data refresh for that project's context, including characters, outlines, and chapters [frontend/src/pages/ProjectDetail.tsx:82-110]().

Sources: [frontend/src/App.tsx:56-72](), [frontend/src/pages/ProjectDetail.tsx:115-188]()

## BrowserRouter Configuration

The `BrowserRouter` component is configured with React Router v7 future flags to ensure forward compatibility:

```typescript
<BrowserRouter
  future={{
    v7_startTransition: true,
    v7_relativeSplatPath: true,
  }}
>
```

| Flag | Purpose |
|------|---------|
| `v7_startTransition` | Enables React Transition API for smoother navigation transitions [frontend/src/App.tsx:39]() |
| `v7_relativeSplatPath` | Standardizes path resolution for splat routes [frontend/src/App.tsx:40]() |

Sources: [frontend/src/App.tsx:37-41]()

## Navigation Patterns

**Route-to-Component Mapping**

The following diagram shows how specific code entities are associated with URL paths:

```mermaid
graph LR
    subgraph "URL Paths"
        P1["/projects"]
        P2["/wizard"]
        P3["/project/:projectId/outline"]
        P4["/project/:projectId/chapters"]
        P5["/chapters/:chapterId/reader"]
    end
    
    subgraph "React Components"
        C1["ProjectList.tsx"]
        C2["ProjectWizardNew.tsx"]
        C3["Outline.tsx"]
        C4["Chapters.tsx"]
        C5["ChapterReader.tsx"]
    end
    
    P1 --- C1
    P2 --- C2
    P3 --- C3
    P4 --- C4
    P5 --- C5
```

### Programmatic Navigation

Components utilize the `useNavigate` hook for flow control. For example, in `AuthCallback`, users are redirected based on session state or stored redirect paths [frontend/src/pages/AuthCallback.tsx:61-73]().

### Sidebar Navigation

The project sidebar in `ProjectDetail.tsx` dynamically generates navigation links using the `Link` component. It supports both a full layout and a collapsed state for mobile responsiveness [frontend/src/pages/ProjectDetail.tsx:115-233]().

Sources: [frontend/src/pages/ProjectDetail.tsx:35-41](), [frontend/src/pages/AuthCallback.tsx:8-10]()

## Backend Route Handling

While the frontend is a Single Page Application (SPA), the backend `main.py` provides a catch-all route to serve `index.html` for all non-API paths, enabling direct browser navigation to deep links [backend/app/main.py:169-189]().

```python
@app.get("/{full_path:path}")
async def serve_spa(full_path: str):
    # Logic to return static index.html for SPA routing
```

Sources: [backend/app/main.py:169-189]()

---

# Page: API Client Layer

# API Client Layer

<details>
<summary>Relevant source files</summary>

The following files were used as context for generating this wiki page:

- [frontend/src/services/api.ts](frontend/src/services/api.ts)
- [frontend/src/types/index.ts](frontend/src/types/index.ts)

</details>



## Purpose and Scope

The API Client Layer provides a centralized, type-safe interface for all HTTP communication between the React frontend and the FastAPI backend. This layer abstracts REST API calls and Server-Sent Events (SSE) streaming, handling authentication, error management, and response transformation automatically.

For information about SSE streaming implementation details, see [Server-Sent Events (SSE) for Streaming](#5.5). For state management integration with API data, see [State Management](#6.3). For backend API endpoint specifications, see [API Reference](#8).

**Sources**: [frontend/src/services/api.ts:1-772]()

---

## Core Architecture

The API client is built on an axios instance configured with global settings for `baseURL`, `timeout`, `credentials`, and `headers`. All API communication flows through this central instance, enabling consistent request/response handling.

### Axios Instance Configuration

The base axios instance is configured at [frontend/src/services/api.ts:68-75]():

| Configuration | Value | Purpose |
|--------------|-------|---------|
| `baseURL` | `/api` | Base path for all API requests |
| `timeout` | `120000` (120s) | Maximum request duration for AI generation |
| `headers.Content-Type` | `application/json` | Default content type |
| `withCredentials` | `true` | Include cookies for session-based authentication |

**Sources**: [frontend/src/services/api.ts:68-75]()

---

### API Client Architecture Diagram

```mermaid
graph TB
    subgraph "React Components"
        Pages["Pages<br/>(ProjectList, Chapters, etc.)"]
        Hooks["Custom Hooks<br/>(useChapterSync, useProjectSync)"]
    end
    
    subgraph "API Client Layer - api.ts"
        AxiosInstance["axios.create()<br/>baseURL: /api<br/>timeout: 120s<br/>withCredentials: true"]
        
        subgraph "Interceptors"
            RequestInterceptor["Request Interceptor<br/>lines 77-84"]
            ResponseInterceptor["Response Interceptor<br/>lines 86-150"]
        end
        
        subgraph "Service Objects"
            AuthApi["authApi<br/>lines 152-198"]
            UserApi["userApi<br/>lines 200-219"]
            SettingsApi["settingsApi<br/>lines 221-304"]
            ProjectApi["projectApi<br/>lines 306-386"]
            OutlineApi["outlineApi<br/>lines 388-513"]
            CharacterApi["characterApi<br/>lines 515-560"]
            ChapterApi["chapterApi<br/>lines 562-604"]
            WritingStyleApi["writingStyleApi<br/>lines 606-640"]
            PolishApi["polishApi<br/>lines 642-648"]
            InspirationApi["inspirationApi<br/>lines 649-679"]
            WizardStreamApi["wizardStreamApi<br/>lines 684-777"]
            McpPluginApi["mcpPluginApi<br/>lines 779-820"]
            AdminApi["adminApi<br/>lines 823-878"]
        end
    end
    
    subgraph "SSE Client"
        SseClient["sseClient.ssePost()<br/>utils/sseClient"]
    end
    
    subgraph "Backend API"
        FastAPI["FastAPI Routers<br/>/api/auth<br/>/api/projects<br/>/api/chapters<br/>..."]
    end
    
    Pages --> Hooks
    Hooks --> AuthApi
    Hooks --> ProjectApi
    Hooks --> ChapterApi
    Hooks --> OutlineApi
    
    AuthApi --> AxiosInstance
    UserApi --> AxiosInstance
    SettingsApi --> AxiosInstance
    ProjectApi --> AxiosInstance
    OutlineApi --> AxiosInstance
    CharacterApi --> AxiosInstance
    ChapterApi --> AxiosInstance
    WritingStyleApi --> AxiosInstance
    PolishApi --> AxiosInstance
    InspirationApi --> AxiosInstance
    AdminApi --> AxiosInstance
    
    WizardStreamApi --> SseClient
    
    AxiosInstance --> RequestInterceptor
    RequestInterceptor --> FastAPI
    FastAPI --> ResponseInterceptor
    ResponseInterceptor --> AxiosInstance
    
    SseClient --> FastAPI
```

**Sources**: [frontend/src/services/api.ts:68-878](), [frontend/src/types/index.ts:1-294]()

---

## Request and Response Interceptors

Interceptors provide a centralized mechanism for request preprocessing and response transformation/error handling.

### Request Interceptor

The request interceptor [frontend/src/services/api.ts:77-84]() is currently minimal, primarily serving as an extension point for future authentication token injection or request logging.

### Response Interceptor

The response interceptor [frontend/src/services/api.ts:86-150]() handles two critical functions:

1. **Automatic data extraction**: Returns `response.data` directly, simplifying API usage.
2. **Comprehensive error handling**: Transforms HTTP errors into user-friendly messages and handles session expiration.

**Sources**: [frontend/src/services/api.ts:77-150]()

---

### Error Handling Flow

```mermaid
graph TB
    Response["HTTP Response"]
    
    Success{"Status 2xx?"}
    
    ExtractData["Extract response.data<br/>line 88"]
    
    ErrorHandler{"Error Type?"}
    
    ResponseError{"Has response?"}
    
    StatusHandler{"HTTP Status?"}
    
    Status400["400: Bad Request<br/>请求参数错误<br/>lines 98-100"]
    Status401["401: Unauthorized<br/>redirect to /login<br/>lines 101-117"]
    Status403["403: Forbidden<br/>没有权限访问<br/>lines 118-120"]
    Status404["404: Not Found<br/>请求的资源不存在<br/>lines 121-123"]
    Status422["422: Validation Error<br/>请求参数验证失败<br/>lines 124-129"]
    Status500["500: Server Error<br/>服务器内部错误<br/>lines 130-132"]
    Status503["503: Service Unavailable<br/>服务暂时不可用<br/>lines 133-135"]
    StatusOther["Other Status<br/>Extract detail/message<br/>lines 136-138"]
    
    NetworkError["Network Error<br/>网络错误，请检查网络连接<br/>lines 139-140"]
    
    OtherError["Other Error<br/>Extract error.message<br/>lines 141-143"]
    
    ShowMessage["message.error()<br/>Display error<br/>line 145"]
    
    LogError["console.error()<br/>Log details<br/>line 146"]
    
    RejectPromise["Promise.reject(error)<br/>line 148"]
    
    Response --> Success
    Success -->|Yes| ExtractData
    Success -->|No| ErrorHandler
    
    ErrorHandler --> ResponseError
    ResponseError -->|Yes| StatusHandler
    ResponseError -->|No<br/>Has request?| NetworkError
    ResponseError -->|No<br/>No request| OtherError
    
    StatusHandler -->|400| Status400
    StatusHandler -->|401| Status401
    StatusHandler -->|403| Status403
    StatusHandler -->|404| Status404
    StatusHandler -->|422| Status422
    StatusHandler -->|500| Status500
    StatusHandler -->|503| Status503
    StatusHandler -->|Other| StatusOther
    
    Status400 --> ShowMessage
    Status401 --> ShowMessage
    Status403 --> ShowMessage
    Status404 --> ShowMessage
    Status422 --> ShowMessage
    Status500 --> ShowMessage
    Status503 --> ShowMessage
    StatusOther --> ShowMessage
    NetworkError --> ShowMessage
    OtherError --> ShowMessage
    
    ShowMessage --> LogError
    LogError --> RejectPromise
```

**Key Error Handling Features**:
- **Automatic 401 redirect**: [frontend/src/services/api.ts:113-115]() redirects to `/login` on unauthorized access if the user is not already on the login page.
- **Detailed validation errors**: [frontend/src/services/api.ts:124-129]() logs validation details from FastAPI's 422 responses.
- **User-friendly messages**: Extracts `detail` or `message` fields from backend error responses.
- **Automatic error display**: Uses Ant Design's `message.error()` for immediate UI feedback [frontend/src/services/api.ts:145]().

**Sources**: [frontend/src/services/api.ts:86-150]()

---

## Service Objects Organization

The API client exports specialized service objects, each encapsulating related endpoints. This organization promotes maintainability and discoverability.

### Service Objects Structure

```mermaid
graph LR
    subgraph "Authentication & User Management"
        AuthApi["authApi<br/>12 methods"]
        UserApi["userApi<br/>6 methods"]
        AdminApi["adminApi<br/>6 methods"]
    end
    
    subgraph "Configuration"
        SettingsApi["settingsApi<br/>13 methods"]
        WritingStyleApi["writingStyleApi<br/>8 methods"]
    end
    
    subgraph "Project Management"
        ProjectApi["projectApi<br/>9 methods"]
        OutlineApi["outlineApi<br/>12 methods"]
        ChapterApi["chapterApi<br/>7 methods"]
        CharacterApi["characterApi<br/>6 methods"]
    end
    
    subgraph "AI Services"
        WizardStreamApi["wizardStreamApi<br/>6 methods (SSE)"]
        InspirationApi["inspirationApi<br/>2 methods"]
        PolishApi["polishApi<br/>2 methods"]
    end
    
    subgraph "Plugin System"
        McpPluginApi["mcpPluginApi<br/>10 methods"]
    end
```

**Sources**: [frontend/src/services/api.ts:152-878]()

---

### Complete Service Method Reference

| Service | Methods | Purpose |
|---------|---------|---------|
| **authApi** | `getAuthConfig`, `localLogin`, `emailLogin`, `getLinuxDOAuthUrl`, `getCurrentUser`, `refreshSession`, `logout` | Authentication and session management [frontend/src/services/api.ts:152-198]() |
| **userApi** | `getCurrentUser`, `listUsers`, `setAdmin`, `deleteUser`, `getUser`, `resetPassword` | User profile management [frontend/src/services/api.ts:200-219]() |
| **settingsApi** | `getSettings`, `saveSettings`, `getAvailableModels`, `testApiConnection`, `getPresets`, `activatePreset` | API key and LLM configuration management [frontend/src/services/api.ts:221-304]() |
| **projectApi** | `getProjects`, `getProject`, `createProject`, `updateProject`, `deleteProject`, `exportProject`, `importProject` | Project CRUD and import/export [frontend/src/services/api.ts:306-386]() |
| **outlineApi** | `getOutlines`, `createOutline`, `updateOutline`, `reorderOutlines`, `generateOutline`, `expandOutline`, `batchExpandOutlines` | Outline management and AI expansion [frontend/src/services/api.ts:388-513]() |
| **characterApi** | `getCharacters`, `getCharacter`, `createCharacter`, `updateCharacter`, `deleteCharacter`, `generateCharacter` | Character CRUD and AI generation [frontend/src/services/api.ts:515-560]() |
| **chapterApi** | `getChapters`, `getChapter`, `createChapter`, `updateChapter`, `deleteChapter`, `checkCanGenerate` | Chapter management and generation [frontend/src/services/api.ts:562-604]() |
| **writingStyleApi** | `getPresetStyles`, `getUserStyles`, `createStyle`, `updateStyle`, `setDefaultStyle` | Writing style configuration [frontend/src/services/api.ts:606-640]() |
| **wizardStreamApi** | `generateWorldBuildingStream`, `generateCharactersStream`, `generateCompleteOutlineStream` | SSE-based wizard generation [frontend/src/services/api.ts:684-777]() |
| **mcpPluginApi** | `getPlugins`, `createPlugin`, `updatePlugin`, `testPlugin`, `getPluginTools`, `callTool` | MCP plugin management [frontend/src/services/api.ts:779-820]() |

**Sources**: [frontend/src/services/api.ts:152-820]()

---

## Type Safety with TypeScript

All API methods are fully typed using TypeScript interfaces defined in [frontend/src/types/index.ts](). The axios instance is configured with generic types that enforce type safety at compile time.

### Type Flow Diagram

```mermaid
graph TB
    subgraph "Type Definitions - types/index.ts"
        RequestTypes["Request Types<br/>ProjectCreate [line 183]<br/>ChapterUpdate [line 373]<br/>OutlineExpansionRequest [line 309]"]
        ResponseTypes["Response Types<br/>Project [line 155]<br/>Chapter [line 343]<br/>OutlineExpansionResponse [line 315]"]
    end
    
    subgraph "API Client - services/api.ts"
        ApiMethod["API Method<br/>api.get&lt;unknown, ResponseType&gt;<br/>api.post&lt;unknown, ResponseType&gt;"]
    end
    
    subgraph "React Components"
        HookUsage["Custom Hook<br/>const data = await projectApi.getProject(id)"]
        TypedData["Typed Data<br/>data: Project"]
    end
    
    RequestTypes --> ApiMethod
    ResponseTypes --> ApiMethod
    ApiMethod --> HookUsage
    HookUsage --> TypedData
```

**Key Type Safety Examples**:
- **Project Operations**: Uses `Project` [frontend/src/types/index.ts:155](), `ProjectCreate` [frontend/src/types/index.ts:183](), and `ProjectUpdate` [frontend/src/types/index.ts:198]().
- **Outline Operations**: Uses `Outline` [frontend/src/types/index.ts:248](), `OutlineCreate` [frontend/src/types/index.ts:260](), and `OutlineUpdate` [frontend/src/types/index.ts:268]().
- **Settings**: Uses `Settings` [frontend/src/types/index.ts:74]() and `SettingsUpdate` [frontend/src/types/index.ts:94]().

**Sources**: [frontend/src/services/api.ts:152-878](), [frontend/src/types/index.ts:1-733]()

---

## SSE Integration

The `wizardStreamApi` service object integrates with the SSE client for real-time AI generation streaming. Unlike regular REST APIs, SSE methods use the `ssePost()` function from [frontend/src/utils/sseClient.ts]().

### SSE Method Pattern

All `wizardStreamApi` methods follow a consistent pattern [frontend/src/services/api.ts:684-777]():

```typescript
generateWorldBuildingStream: (
  data: { /* request parameters */ },
  options?: SSEClientOptions  // Callbacks for progress/complete/error
) => ssePost<WorldBuildingResponse>(
  '/api/wizard-stream/world-building',
  data,
  options
)
```

**SSE Methods**:
- `generateWorldBuildingStream` [frontend/src/services/api.ts:684-698]()
- `generateCharactersStream` [frontend/src/services/api.ts:700-714]()
- `generateCompleteOutlineStream` [frontend/src/services/api.ts:716-730]()
- `updateWorldBuildingStream` [frontend/src/services/api.ts:732-746]()
- `regenerateWorldBuildingStream` [frontend/src/services/api.ts:748-762]()

**Sources**: [frontend/src/services/api.ts:684-762](), [frontend/src/utils/sseClient.ts:1-50]()

---

## Special Request Handling

### File Upload and Download

#### File Upload (FormData)

[frontend/src/services/api.ts:357-370]() and [frontend/src/services/api.ts:373-385]() demonstrate `FormData` handling for project import:

```typescript
validateImportFile: (file: File) => {
  const formData = new FormData();
  formData.append('file', file);
  return api.post<unknown, BookImportPreview>('/projects/validate-import', formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
  });
}
```

#### File Download (Blob)

[frontend/src/services/api.ts:323-354]() demonstrates blob handling for project export. It uses a raw `axios` instance to bypass the default response interceptor that extracts `.data`, allowing access to headers for filename extraction.

**Key Steps**:
1. Request with `responseType: 'blob'`.
2. Extract filename from `content-disposition` header.
3. Create a temporary `ObjectURL` and trigger a programmatic click on an `<a>` element.
4. Revoke the URL to free memory.

**Sources**: [frontend/src/services/api.ts:323-385]()

---

## Integration with Frontend Architecture

### Component to Backend Data Flow

```mermaid
sequenceDiagram
    participant Component as "React Component<br/>(Chapters.tsx)"
    participant Hook as "Custom Hook<br/>(useChapterSync)"
    participant Store as "Zustand Store"
    participant Api as "API Client<br/>(chapterApi)"
    participant Interceptor as "Response Interceptor"
    participant Backend as "FastAPI Backend"
    
    Component->>Hook: useEffect(() => sync())
    Hook->>Api: chapterApi.getChapters(projectId)
    Api->>Interceptor: Request
    Interceptor->>Backend: GET /api/chapters/project/{id}
    Backend-->>Interceptor: 200 OK { data: [...] }
    Interceptor-->>Api: Extract response.data [line 88]
    
    alt Error Response
        Backend-->>Interceptor: 4xx/5xx Error
        Interceptor->>Interceptor: Parse error status [lines 97-138]
        Interceptor->>Interceptor: message.error(errorMsg) [line 145]
        Interceptor-->>Api: Promise.reject(error) [line 148]
        Api-->>Hook: throw error
        Hook->>Hook: Handle error locally
    end
    
    Api-->>Hook: chapters: Chapter[]
    Hook->>Store: setChapters(chapters)
    Store-->>Component: Re-render with new data
```

**Sources**: [frontend/src/services/api.ts:86-150]()

---

# Page: State Management

# State Management

<details>
<summary>Relevant source files</summary>

The following files were used as context for generating this wiki page:

- [backend/app/api/chapters.py](backend/app/api/chapters.py)
- [backend/app/schemas/chapter.py](backend/app/schemas/chapter.py)
- [frontend/src/components/ExpansionPlanEditor.tsx](frontend/src/components/ExpansionPlanEditor.tsx)
- [frontend/src/pages/Chapters.tsx](frontend/src/pages/Chapters.tsx)
- [frontend/src/pages/ProjectList.tsx](frontend/src/pages/ProjectList.tsx)
- [frontend/src/store/hooks.ts](frontend/src/store/hooks.ts)

</details>



This document describes the frontend state management architecture in MuMuAINovel. The system uses **Zustand** for global state management and custom hooks to synchronize state with the backend APIs. For information about backend data persistence, see [Database Architecture](3.4). For API communication patterns, see [SSE Streaming Implementation](7.4).

## Overview

The frontend maintains global state for:
- User projects list
- Current project details
- Story outlines
- Chapters
- Characters and relationships
- Loading states

State is managed through:
1. **Zustand Store**: Central state container located in `frontend/src/store/index.ts`.
2. **Custom Sync Hooks**: Hooks like `useProjectSync` and `useOutlineSync` that bridge API calls and state updates.
3. **Component Consumption**: React components access state via the `useStore` hook.

---

## Zustand Store Architecture

The application uses Zustand for lightweight, hook-based state management. The store is structured as a single global state object with typed interfaces.

### Store Structure

The following diagram illustrates the relationship between the Zustand store, custom sync hooks, and page components.

**Diagram: Frontend State Flow Architecture**
```mermaid
graph TB
    subgraph ZustandStore["Zustand Store (store/index.ts)"]
        StoreInterface["Store Interface"]
        
        subgraph StateSlices["State Slices"]
            Projects["projects: Project[]"]
            CurrentProject["currentProject: Project | null"]
            Outlines["outlines: Outline[]"]
            Chapters["chapters: Chapter[]"]
            Characters["characters: Character[]"]
            Loading["loading: boolean"]
        end
        
        subgraph Actions["Actions (Setters)"]
            SetProjects["setProjects(projects)"]
            AddProject["addProject(project)"]
            UpdateProject["updateProject(id, project)"]
            RemoveProject["removeProject(id)"]
            SetOutlines["setOutlines(outlines)"]
            AddOutline["addOutline(outline)"]
            UpdateOutline["updateOutline(id, outline)"]
            RemoveOutline["removeOutline(id)"]
            SetChapters["setChapters(chapters)"]
            AddChapter["addChapter(chapter)"]
            UpdateChapter["updateChapter(id, chapter)"]
            RemoveChapter["removeChapter(id)"]
            SetCharacters["setCharacters(characters)"]
            AddCharacter["addCharacter(character)"]
            RemoveCharacter["removeCharacter(id)"]
            SetLoading["setLoading(loading)"]
        end
    end
    
    subgraph CustomHooks["Custom Hooks (store/hooks.ts)"]
        UseProjectSync["useProjectSync"]
        UseOutlineSync["useOutlineSync"]
        UseChapterSync["useChapterSync"]
        UseCharacterSync["useCharacterSync"]
    end
    
    subgraph Components["Page Components"]
        ProjectPages["ProjectList.tsx"]
        OutlinePages["Outline.tsx"]
        ChapterPages["Chapters.tsx"]
    end
    
    ProjectPages -->|"useStore()"| Projects
    ProjectPages -->|"useStore()"| Loading
    OutlinePages -->|"useStore()"| CurrentProject
    OutlinePages -->|"useStore()"| Outlines
    ChapterPages -->|"useStore()"| Chapters
    
    UseProjectSync -->|"updates"| SetProjects
    UseProjectSync -->|"updates"| AddProject
    UseProjectSync -->|"updates"| UpdateProject
    UseProjectSync -->|"updates"| RemoveProject
    
    UseOutlineSync -->|"updates"| SetOutlines
    UseOutlineSync -->|"updates"| AddOutline
    UseOutlineSync -->|"updates"| UpdateOutline
    UseOutlineSync -->|"updates"| RemoveOutline
    
    UseChapterSync -->|"updates"| SetChapters
    UseChapterSync -->|"updates"| AddChapter
    UseChapterSync -->|"updates"| UpdateChapter
    UseChapterSync -->|"updates"| RemoveChapter
    
    UseCharacterSync -->|"updates"| SetCharacters
    UseCharacterSync -->|"updates"| AddCharacter
    UseCharacterSync -->|"updates"| RemoveCharacter
    
    ProjectPages -->|"uses"| UseProjectSync
    OutlinePages -->|"uses"| UseOutlineSync
    ChapterPages -->|"uses"| UseChapterSync
```

**Store State Schema**

| State Property | Type | Description |
|---|---|---|
| `projects` | `Project[]` | List of all user projects |
| `currentProject` | `Project \| null` | Currently selected project for detail view |
| `outlines` | `Outline[]` | Story outline items for current project |
| `chapters` | `Chapter[]` | Chapter content for current project |
| `characters` | `Character[]` | Characters for current project |
| `loading` | `boolean` | Global loading indicator |

**Sources**: [frontend/src/store/hooks.ts:30-30](), [frontend/src/store/hooks.ts:96-96](), [frontend/src/store/hooks.ts:149-149](), [frontend/src/store/hooks.ts:229-229]()

---

## Custom Sync Hooks Pattern

Custom hooks encapsulate the logic for syncing backend data with the Zustand store. They provide a clean API for components to trigger data operations without directly managing API calls or state updates.

### Hook Architecture

**Diagram: Data Synchronization Flow**
```mermaid
graph LR
    Component["Component<br/>(ProjectList.tsx)"]
    Hook["Custom Hook<br/>(useProjectSync)"]
    API["API Service<br/>(services/api.ts)"]
    Store["Zustand Store"]
    Backend["Backend API<br/>(api/chapters.py)"]
    
    Component -->|"1. Call hook function<br/>refreshProjects()"| Hook
    Hook -->|"2. HTTP Request"| API
    API -->|"3. REST/SSE"| Backend
    Backend -->|"4. Response data"| API
    API -->|"5. Return data"| Hook
    Hook -->|"6. setProjects(data)"| Store
    Store -->|"7. Trigger re-render"| Component
```

### useProjectSync Hook

The `useProjectSync` hook manages project-level operations. Components call hook methods, which handle API communication and state synchronization [frontend/src/store/hooks.ts:29-90]().

**Hook Implementation**
The hook extracts store setters and wraps them with API calls [frontend/src/store/hooks.ts:30-30]():
```typescript
const { setProjects, setLoading, addProject, updateProject, removeProject } = useStore();
```

| Method | Description | API Endpoint | State Updates |
|---|---|---|---|
| `refreshProjects()` | Fetches all projects from API | `GET /api/projects` | Calls `setProjects()` [frontend/src/store/hooks.ts:33-47]() |
| `createProject(data)` | Creates new project | `POST /api/projects` | Calls `addProject()` [frontend/src/store/hooks.ts:50-59]() |
| `updateProject(id, data)` | Updates project details | `PUT /api/projects/{id}` | Calls `updateProject()` [frontend/src/store/hooks.ts:62-71]() |
| `deleteProject(id)` | Deletes project | `DELETE /api/projects/{id}` | Calls `removeProject()` [frontend/src/store/hooks.ts:74-82]() |

**Sources**: [frontend/src/store/hooks.ts:29-90](), [frontend/src/pages/ProjectList.tsx:79-79]()

---

### useChapterSync Hook

The `useChapterSync` hook manages chapter CRUD operations and provides SSE-based streaming generation [frontend/src/store/hooks.ts:228-408]().

**Hook Implementation**
```typescript
const { currentProject, setChapters, addChapter, updateChapter, removeChapter } = useStore();
```

**SSE Streaming Generation Implementation**
The `generateChapterContentStream` method uses the native `fetch` API to handle Server-Sent Events (SSE) for real-time content generation [frontend/src/store/hooks.ts:284-399]().

| Message Type | Action |
|---|---|
| `start` | Initialize progress callback [frontend/src/store/hooks.ts:347-350]() |
| `content` | Accumulate content and trigger `onProgress` callback [frontend/src/store/hooks.ts:358-361]() |
| `done` | Trigger 100% progress and call `refreshChapters()` [frontend/src/store/hooks.ts:370-374]() |
| `error` | Throw error to interrupt generation [frontend/src/store/hooks.ts:366-368]() |

**Sources**: [frontend/src/store/hooks.ts:228-408](), [frontend/src/pages/Chapters.tsx:5-5]()

---

### useOutlineSync Hook

The `useOutlineSync` hook manages outline CRUD operations and AI generation [frontend/src/store/hooks.ts:148-223]().

| Method | Description | API Endpoint | State Updates |
|---|---|---|---|
| `refreshOutlines(projectId?)` | Fetches outlines for project | `GET /api/outlines/project/{id}` | Calls `setOutlines()` [frontend/src/store/hooks.ts:152-166]() |
| `generateOutlines(data)` | AI generates multiple outlines | `POST /api/outlines/generate` | Calls `addOutline()` for each item [frontend/src/store/hooks.ts:204-214]() |

**Sources**: [frontend/src/store/hooks.ts:148-223]()

---

### useCharacterSync Hook

The `useCharacterSync` hook manages character CRUD operations and AI generation [frontend/src/store/hooks.ts:95-143]().

| Method | Description | API Endpoint | State Updates |
|---|---|---|---|
| `refreshCharacters(projectId?)` | Fetches characters for project | `GET /api/characters/project/{id}` | Calls `setCharacters()` [frontend/src/store/hooks.ts:99-113]() |
| `generateCharacter(data)` | AI generates single character | `POST /api/characters/generate` | Calls `addCharacter()` [frontend/src/store/hooks.ts:127-136]() |

**Sources**: [frontend/src/store/hooks.ts:95-143]()

---

## State Consumption in Components

Components consume state by calling the `useStore` hook, which returns the current state and triggers re-renders when state changes.

### Local vs Global State
The application uses a hybrid approach:
- **Global State**: Managed via Zustand for data shared across pages (e.g., `projects`, `chapters`) [frontend/src/pages/Chapters.tsx:49-49]().
- **Local State**: Managed via `useState` for UI-only concerns (e.g., modal visibility, form inputs) [frontend/src/pages/Chapters.tsx:52-58]().

**ExpansionPlanEditor Example**
The `ExpansionPlanEditor` component demonstrates loading character data locally for selection while saving the final plan via a parent-provided callback [frontend/src/components/ExpansionPlanEditor.tsx:39-70]().

```typescript
const loadCharacters = useCallback(async () => {
  try {
    setLoadingCharacters(true);
    const response = await characterApi.getCharacters(projectId);
    // ... logic to extract characters from response
    setAvailableCharacters(chars);
  } catch (error) {
    message.error('加载角色列表失败');
  } finally {
    setLoadingCharacters(false);
  }
}, [projectId]);
```

**Sources**: [frontend/src/components/ExpansionPlanEditor.tsx:39-70](), [frontend/src/pages/Chapters.tsx:49-58]()

---

## State Update Flow Diagrams

### Standard CRUD Operation Flow
**Diagram: Delete Project Flow**
```mermaid
sequenceDiagram
    participant C as ProjectList.tsx
    participant H as useProjectSync
    participant A as projectApi (services/api.ts)
    participant B as Backend (FastAPI)
    participant S as Zustand Store
    
    C->>C: User clicks delete button
    C->>H: deleteProject(id)
    H->>A: projectApi.deleteProject(id)
    A->>B: DELETE /api/projects/{id}
    B-->>A: 200 OK
    A-->>H: Success response
    H->>S: removeProject(id)
    Note over S: Store filters projects array
    S-->>C: Zustand triggers re-render
```

**Sources**: [frontend/src/store/hooks.ts:74-82](), [frontend/src/pages/ProjectList.tsx:147-168]()

### Chapter Generation Sync Flow
**Diagram: Chapter Streaming Flow**
```mermaid
sequenceDiagram
    participant C as Chapters.tsx
    participant H as useChapterSync
    participant F as fetch (Native)
    participant B as Backend SSE (api/chapters.py)
    participant S as Zustand Store
    
    C->>H: generateChapterContentStream(id, onProgress)
    H->>F: POST /api/chapters/{id}/generate-stream
    F->>B: Start SSE
    loop Stream
        B-->>F: data: {"type": "content", "content": "..."}
        F->>H: Decode
        H->>C: onProgress(text)
    end
    B-->>F: data: {"type": "done"}
    F->>H: Complete
    H->>H: refreshChapters()
    H->>S: setChapters(data)
    S-->>C: Update UI
```

**Sources**: [frontend/src/store/hooks.ts:284-399](), [backend/app/api/chapters.py:62-62]()

---

## Code Entity Reference Map

| Code Entity | Purpose | Source File |
|---|---|---|
| `useStore` | Central Zustand hook | [frontend/src/store/index.ts]() |
| `useProjectSync` | Project data synchronization | [frontend/src/store/hooks.ts:29-90]() |
| `useChapterSync` | Chapter data synchronization and SSE | [frontend/src/store/hooks.ts:228-408]() |
| `useOutlineSync` | Outline data synchronization | [frontend/src/store/hooks.ts:148-223]() |
| `useCharacterSync` | Character data synchronization | [frontend/src/store/hooks.ts:95-143]() |
| `ChapterCreate` | Pydantic model for chapter creation | [backend/app/schemas/chapter.py:20-31]() |
| `ChapterResponse` | Pydantic model for chapter API response | [backend/app/schemas/chapter.py:43-61]() |
| `ExpansionPlanUpdate` | Model for chapter planning updates | [backend/app/schemas/chapter.py:175-185]() |

**Sources**: [frontend/src/store/hooks.ts:1-408](), [backend/app/schemas/chapter.py:1-200]()

---

# Page: Wizard and Inspiration Interfaces

# Wizard and Inspiration Interfaces

<details>
<summary>Relevant source files</summary>

The following files were used as context for generating this wiki page:

- [backend/app/api/inspiration.py](backend/app/api/inspiration.py)
- [backend/app/services/plot_expansion_service.py](backend/app/services/plot_expansion_service.py)
- [frontend/src/components/AIProjectGenerator.tsx](frontend/src/components/AIProjectGenerator.tsx)
- [frontend/src/components/SSEProgressModal.tsx](frontend/src/components/SSEProgressModal.tsx)
- [frontend/src/pages/Inspiration.tsx](frontend/src/pages/Inspiration.tsx)
- [frontend/src/pages/ProjectWizardNew.tsx](frontend/src/pages/ProjectWizardNew.tsx)

</details>



This document describes the two frontend interfaces for creating new novel projects: **ProjectWizardNew** (traditional form-based wizard) and **Inspiration** (conversational AI-guided mode). Both interfaces collect project parameters and orchestrate multi-step AI generation through a shared `AIProjectGenerator` component.

---

## Overview

The system provides two distinct user experiences for project creation, both culminating in the same multi-phase generation pipeline (world-building → careers → characters → outline):

| Interface | Component | Route | User Experience | Caching Strategy |
|-----------|-----------|-------|----------------|------------------|
| **Wizard** | `ProjectWizardNew` | `/wizard` | Form-based parameter collection | Resume via URL parameter |
| **Inspiration** | `Inspiration` | `/inspiration` | Conversational step-by-step guidance | LocalStorage-based conversation cache |

Both interfaces delegate generation to `AIProjectGenerator`, which manages SSE streaming, progress tracking, and error recovery.

**Sources:** [frontend/src/pages/ProjectWizardNew.tsx:16-103](), [frontend/src/pages/Inspiration.tsx:51-104]()

---

## Wizard Flow Architecture

### Diagram: ProjectWizardNew Component Flow

```mermaid
graph TB
    subgraph "ProjectWizardNew [frontend/src/pages/ProjectWizardNew.tsx]"
        FormStep["Form Step<br/>(currentStep: 'form')"]
        FormComponent["Ant Design Form<br/>- title<br/>- description<br/>- theme<br/>- genre[]<br/>- narrative_perspective<br/>- target_words<br/>- character_count<br/>- outline_mode"]
        
        GeneratingStep["Generating Step<br/>(currentStep: 'generating')"]
        
        GenConfig["GenerationConfig<br/>[frontend/src/components/AIProjectGenerator.tsx]"]
        
        AIGen["AIProjectGenerator<br/>Component"]
    end
    
    subgraph "URL Parameters"
        URLCheck["searchParams.get('project_id')"]
        ResumeFlow["handleResumeGeneration()"]
    end
    
    subgraph "State Management"
        LocalState["Local State:<br/>- currentStep: 'form' | 'generating'<br/>- generationConfig<br/>- resumeProjectId"]
    end
    
    FormComponent -->|"form.onFinish"| FormValidation["Form Validation"]
    FormValidation -->|"handleAutoGenerate()"| GenConfig
    GenConfig --> GeneratingStep
    GeneratingStep --> AIGen
    
    URLCheck -->|"if project_id exists"| ResumeFlow
    ResumeFlow -->|"Fetch project data"| GenConfig
    
    AIGen -->|"onComplete(projectId)"| Complete["Navigate to<br/>/project/:projectId"]
    AIGen -->|"onBack()"| FormStep
    
    LocalState -.->|"stores"| FormStep
    LocalState -.->|"stores"| GeneratingStep
```

**Sources:** [frontend/src/pages/ProjectWizardNew.tsx:16-103](), [frontend/src/pages/ProjectWizardNew.tsx:105-319]()

### Form Configuration

The wizard renders an Ant Design `Form` with the following fields:

| Field | Name | Type | Validation | Default |
|-------|------|------|------------|---------|
| Title | `title` | `Input` | Required | - |
| Description | `description` | `TextArea` | Required, maxLength: 300 | - |
| Theme | `theme` | `TextArea` | Required, maxLength: 500 | - |
| Genre | `genre` | `Select` (tags mode) | Required | `['玄幻']` |
| Outline Mode | `outline_mode` | `Radio.Group` | Required | `'one-to-one'` |
| Character Count | `character_count` | `InputNumber` | Required, min: 3, max: 20 | `5` |
| Target Words | `target_words` | `InputNumber` | Required, min: 10000 | `100000` |

The outline mode field uses interactive `Card` components that highlight on selection [frontend/src/pages/ProjectWizardNew.tsx:192-248](). The two modes are:
- `'one-to-one'` - Traditional mode (one outline per chapter).
- `'one-to-many'` - Refinement mode (one outline expands to multiple chapters) [frontend/src/pages/ProjectWizardNew.tsx:216-231]().

**Sources:** [frontend/src/pages/ProjectWizardNew.tsx:116-249]()

### Resume Functionality

The wizard supports resuming interrupted generation via URL parameters:

1. URL check: `searchParams.get('project_id')` [frontend/src/pages/ProjectWizardNew.tsx:38-44]().
2. Fetch project data: `fetch('/api/projects/${projectId}')` [frontend/src/pages/ProjectWizardNew.tsx:47-55]().
3. Reconstruct `GenerationConfig` from project metadata [frontend/src/pages/ProjectWizardNew.tsx:57-66]().
4. Pass `resumeProjectId` to `AIProjectGenerator` [frontend/src/pages/ProjectWizardNew.tsx:68-69]().

**Sources:** [frontend/src/pages/ProjectWizardNew.tsx:36-75]()

---

## Inspiration Flow Architecture

### Diagram: Inspiration Conversational State Machine

```mermaid
stateDiagram-v2
    [*] --> idea: Initial greeting
    
    idea --> title: handleSendMessage()<br/>inspirationApi.generateOptions('title')
    
    title --> description: handleSelectOption()<br/>or handleCustomInput()<br/>generateOptions('description')
    
    description --> theme: generateOptions('theme')
    
    theme --> genre: generateOptions('genre')
    
    genre --> perspective: handleConfirmGenres()<br/>(multi-select)
    
    perspective --> outline_mode: Fixed options
    
    outline_mode --> confirm: Show summary
    
    confirm --> generating: '✅ 确认创建'<br/>clearCache()<br/>setGenerationConfig()
    confirm --> idea: '🔄 重新开始'<br/>handleRestart()
    
    generating --> complete: AIProjectGenerator<br/>onComplete()
    
    complete --> [*]
    
    note right of idea
        Step type: 'idea' | 'title' | 
        'description' | 'theme' | 'genre' | 
        'perspective' | 'outline_mode' | 
        'confirm' | 'generating' | 'complete'
    end note
```

**Sources:** [frontend/src/pages/Inspiration.tsx:11-12](), [frontend/src/pages/Inspiration.tsx:254-665]()

### Conversational Message Flow

The Inspiration interface maintains a `messages` array with a structured message format:

```typescript
interface Message {
  type: 'ai' | 'user';
  content: string;
  options?: string[];
  isMultiSelect?: boolean;
  optionsDisabled?: boolean;
  canRefine?: boolean;
  step?: Step;
}
```

**Key functions:**

- **handleSendMessage()** [frontend/src/pages/Inspiration.tsx:254-314]() - Processes user text input, calls backend API for next step.
- **handleSelectOption()** [frontend/src/pages/Inspiration.tsx:316-483]() - Handles option selection, manages multi-select for genres.
- **handleRetry()** [frontend/src/pages/Inspiration.tsx:230-249]() - Re-triggers the last failed step using `lastFailedRequest`.
- **generateNextStep()** [frontend/src/pages/Inspiration.tsx:560-665]() - Orchestrates transition between conversation stages.

**Sources:** [frontend/src/pages/Inspiration.tsx:13-21](), [frontend/src/pages/Inspiration.tsx:254-665]()

### Backend Integration (Inspiration API)

Each step calls the Inspiration API to generate options with automatic retries on the backend:

- **Endpoint**: `POST /inspiration/generate-options` [backend/app/api/inspiration.py:69-75]().
- **Validation**: Ensures AI returns at least 3 and at most 10 options [backend/app/api/inspiration.py:26-58]().
- **Temperature Strategy**: Temperature decreases as steps progress (Title: 0.8 → Genre: 0.45) to maintain consistency with previous choices [backend/app/api/inspiration.py:18-23]().

**Sources:** [backend/app/api/inspiration.py:18-203]()

---

## Caching and State Persistence

### Inspiration Conversation Cache

The Inspiration interface implements caching to preserve conversation progress across refreshes:

**Cache Data Structure:**

```typescript
interface CacheData {
  messages: Message[];
  currentStep: Step;
  wizardData: Partial<WizardData>;
  initialIdea: string;
  selectedOptions: string[];
  lastFailedRequest: { ... } | null;
  timestamp: number;
}
```

**Cache Management Functions:**

| Function | Purpose | Trigger |
|----------|---------|---------|
| `saveToCache()` [frontend/src/pages/Inspiration.tsx:117-144]() | Saves state to localStorage | Debounced on state change (500ms) |
| `restoreFromCache()` [frontend/src/pages/Inspiration.tsx:147-188]() | Restores cached state | Component mount |
| `clearCache()` [frontend/src/pages/Inspiration.tsx:107-114]() | Removes cache | Generation starts or manual restart |

**Cache Key and Expiry:**
- Key: `'inspiration_conversation_cache'` [frontend/src/pages/Inspiration.tsx:47]().
- Expiry: 24 hours (86400000ms) [frontend/src/pages/Inspiration.tsx:49]().

**Sources:** [frontend/src/pages/Inspiration.tsx:33-50](), [frontend/src/pages/Inspiration.tsx:107-210]()

---

## AIProjectGenerator Component

### Diagram: Generation Pipeline and State Management

```mermaid
graph TB
    subgraph "AIProjectGenerator Props"
        Config["GenerationConfig:<br/>- title, description, theme<br/>- genre, narrative_perspective<br/>- target_words, chapter_count<br/>- character_count, outline_mode"]
        StoragePrefix["storagePrefix:<br/>'wizard' | 'inspiration'"]
        ResumeID["resumeProjectId?: string"]
    end
    
    subgraph "Generation States"
        GenSteps["GenerationSteps:<br/>- worldBuilding: GenerationStep<br/>- careers: GenerationStep<br/>- characters: GenerationStep<br/>- outline: GenerationStep"]
        
        Progress["Progress State:<br/>- progress: 0-100<br/>- progressMessage: string<br/>- errorDetails: string"]
    end
    
    subgraph "Generation Flow"
        Init["useEffect on mount"]
        CheckResume{"resumeProjectId?"}
        
        NewFlow["handleAutoGenerate()"]
        ResumeFlow["handleResumeGenerate()"]
        
        World["wizardStreamApi<br/>.generateWorldBuildingStream()"]
        Careers["wizardStreamApi<br/>.generateCareersStream()"]
        Chars["wizardStreamApi<br/>.generateCharactersStream()"]
        Outline["wizardStreamApi<br/>.generateCompleteOutlineStream()"]
        
        Complete["onComplete(projectId)<br/>navigate to project"]
    end
    
    Config --> Init
    Init --> CheckResume
    CheckResume -->|"No"| NewFlow
    CheckResume -->|"Yes"| ResumeFlow
    
    NewFlow --> World
    ResumeFlow --> CheckStep{"Check wizard_step"}
    
    CheckStep -->|"0"| World
    CheckStep -->|"1"| Careers
    CheckStep -->|"2"| Chars
    CheckStep -->|"3"| Outline
    
    World -->|"Success"| Careers
    Careers -->|"Success"| Chars
    Chars -->|"Success"| Outline
    Outline -->|"Success"| Complete
```

**Sources:** [frontend/src/components/AIProjectGenerator.tsx:33-103](), [frontend/src/components/AIProjectGenerator.tsx:106-192]()

### Generation Step States

The component tracks four distinct phases:
1. **World Building**: 0-20% progress [frontend/src/components/AIProjectGenerator.tsx:336]().
2. **Careers**: 20-40% progress [frontend/src/components/AIProjectGenerator.tsx:361]().
3. **Characters**: 40-70% progress [frontend/src/components/AIProjectGenerator.tsx:386]().
4. **Outline**: 70-100% progress [frontend/src/components/AIProjectGenerator.tsx:418]().

**SSE Streaming Integration:**
Each phase uses `wizardStreamApi` to handle SSE events. Results are stored in the database at each step, updating the project's `wizard_step` (0-4) to allow for recovery [frontend/src/components/AIProjectGenerator.tsx:137-140]().

**Sources:** [frontend/src/components/AIProjectGenerator.tsx:31-38](), [frontend/src/components/AIProjectGenerator.tsx:323-437]()

---

## UI Components and Integration

### SSE Progress Modal

The `SSEProgressModal` provides a unified loading interface for long-running generation tasks:
- **Progress Bar**: Displays percentage and a gradient background [frontend/src/components/SSEProgressModal.tsx:72-92]().
- **Status Message**: Displays real-time updates from the SSE stream [frontend/src/components/SSEProgressModal.tsx:109-118]().
- **Cancel Button**: Optional button to stop the task [frontend/src/components/SSEProgressModal.tsx:131-145]().

**Sources:** [frontend/src/components/SSEProgressModal.tsx:5-149]()

### Code Entity Reference Table

| Entity | Type | Purpose | Location |
|--------|------|---------|----------|
| `ProjectWizardNew` | Component | Form-based creation | [frontend/src/pages/ProjectWizardNew.tsx:16]() |
| `Inspiration` | Component | Conversational creation | [frontend/src/pages/Inspiration.tsx:51]() |
| `AIProjectGenerator` | Component | Shared SSE pipeline | [frontend/src/components/AIProjectGenerator.tsx:48]() |
| `SSEProgressModal` | Component | Unified progress UI | [frontend/src/components/SSEProgressModal.tsx:20]() |
| `inspirationApi` | API Service | Conversational options | [frontend/src/pages/Inspiration.tsx:5]() |
| `wizardStreamApi` | API Service | Multi-step SSE generation | [frontend/src/components/AIProjectGenerator.tsx:5]() |

**Sources:** [frontend/src/pages/ProjectWizardNew.tsx:16](), [frontend/src/pages/Inspiration.tsx:51](), [frontend/src/components/AIProjectGenerator.tsx:48](), [frontend/src/components/SSEProgressModal.tsx:20]()

---

# Page: Chapter Interface

# Chapter Interface

<details>
<summary>Relevant source files</summary>

The following files were used as context for generating this wiki page:

- [backend/app/api/chapters.py](backend/app/api/chapters.py)
- [backend/app/schemas/chapter.py](backend/app/schemas/chapter.py)
- [frontend/src/components/AnnotatedText.tsx](frontend/src/components/AnnotatedText.tsx)
- [frontend/src/components/ChapterAnalysis.tsx](frontend/src/components/ChapterAnalysis.tsx)
- [frontend/src/components/ChapterContentComparison.tsx](frontend/src/components/ChapterContentComparison.tsx)
- [frontend/src/components/ChapterReader.tsx](frontend/src/components/ChapterReader.tsx)
- [frontend/src/components/ChapterRegenerationModal.tsx](frontend/src/components/ChapterRegenerationModal.tsx)
- [frontend/src/components/CharacterCareerCard.tsx](frontend/src/components/CharacterCareerCard.tsx)
- [frontend/src/components/ExpansionPlanEditor.tsx](frontend/src/components/ExpansionPlanEditor.tsx)
- [frontend/src/components/PartialRegenerateModal.tsx](frontend/src/components/PartialRegenerateModal.tsx)
- [frontend/src/components/PartialRegenerateToolbar.tsx](frontend/src/components/PartialRegenerateToolbar.tsx)
- [frontend/src/pages/ChapterAnalysis.tsx](frontend/src/pages/ChapterAnalysis.tsx)
- [frontend/src/pages/Chapters.tsx](frontend/src/pages/Chapters.tsx)
- [frontend/src/store/hooks.ts](frontend/src/store/hooks.ts)

</details>



## Purpose and Scope

The Chapter Interface is the primary page component for managing and creating novel chapters within a project. It provides comprehensive chapter management including listing, editing metadata and content, AI-powered content generation (both single and batch), chapter analysis integration, and expansion plan editing. The interface adapts to the project's outline mode (one-to-one or one-to-many) to display chapters in different organizational structures.

For information about the backend chapter APIs that this interface calls, see [Chapter APIs](). For details on the AI generation services, see [AI Service Architecture](). For expansion plan editing functionality, see [Expansion Plan Editor](). For chapter analysis features, see [Chapter Analysis System]().

**Sources**: [frontend/src/pages/Chapters.tsx:1-123](), [backend/app/api/chapters.py:1-62]()

---

## Component Architecture

### Component Structure

The `Chapters` component is located at [frontend/src/pages/Chapters.tsx:48-2469]() and serves as the main container for all chapter-related functionality. It integrates multiple child components and manages complex state for chapter operations.

**Component Hierarchy Diagram**

```mermaid
graph TB
    Chapters["Chapters Component<br/>(pages/Chapters.tsx)"]
    
    subgraph "State Management"
        ZustandStore["Zustand Store<br/>currentProject, chapters"]
        ChapterSync["useChapterSync Hook<br/>refreshChapters, updateChapter"]
        LocalState["Local State<br/>modals, forms, progress"]
    end
    
    subgraph "Display Components"
        List["Ant Design List<br/>Chapter Items"]
        Collapse["Ant Design Collapse<br/>Grouped by Outline"]
        Reader["ChapterReader<br/>Full Screen Reading"]
    end
    
    subgraph "Modal Components"
        MetadataModal["Modal: Edit Metadata<br/>title, status"]
        EditorModal["Modal: Edit Content<br/>TextArea + AI Generate"]
        BatchModal["Modal: Batch Generate<br/>Configuration Form"]
        RegenModal["ChapterRegenerationModal<br/>AI Rewrite"]
        PartialRegen["PartialRegenerateModal<br/>Selected Text Rewrite"]
    end
    
    subgraph "Analysis & Planning"
        Analysis["ChapterAnalysis<br/>Plot & Memory View"]
        PlanEditor["ExpansionPlanEditor<br/>Plan Details"]
        Annotated["AnnotatedText<br/>Highlighted Memory Hooks"]
    end
    
    Chapters --> ZustandStore
    Chapters --> ChapterSync
    Chapters --> LocalState
    
    Chapters --> List
    Chapters --> Collapse
    Chapters --> Reader
    
    Chapters --> MetadataModal
    Chapters --> EditorModal
    Chapters --> BatchModal
    Chapters --> RegenModal
    Chapters --> PartialRegen
    
    Chapters --> Analysis
    Chapters --> PlanEditor
    Chapters --> Annotated
```

**Sources**: [frontend/src/pages/Chapters.tsx:1-115](), [frontend/src/store/hooks.ts:228-246]()

---

### Key State Variables

The component manages extensive state for different operations:

| State Category | Variables | Purpose | Lines |
|----------------|-----------|---------|-------|
| **Modal Visibility** | `isModalOpen`, `isEditorOpen`, `batchGenerateVisible`, `planEditorVisible`, `analysisVisible` | Control visibility of different modals | [frontend/src/pages/Chapters.tsx:52-68]() |
| **Generation State** | `isGenerating`, `isContinuing`, `batchGenerating` | Track AI generation operations | [frontend/src/pages/Chapters.tsx:54-102]() |
| **Selection State** | `selectedStyleId`, `selectedModel`, `batchSelectedModel` | User selections for AI generation | [frontend/src/pages/Chapters.tsx:61-66]() |
| **Progress Tracking** | `singleChapterProgress`, `batchProgress`, `analysisTasksMap` | Track generation and analysis progress | [frontend/src/pages/Chapters.tsx:97-113]() |
| **Partial Rewrite** | `selectedTextForRegenerate`, `selectionStartPosition` | Metadata for selective text regeneration | [frontend/src/pages/Chapters.tsx:91-93]() |

**Sources**: [frontend/src/pages/Chapters.tsx:50-115]()

---

## AI Content Generation & Regeneration

### Partial Text Regeneration

A key feature of the interface is the ability to rewrite specific sections of a chapter. When a user selects text in the editor, a floating toolbar appears [frontend/src/pages/Chapters.tsx:126-160]().

**Partial Rewrite Flow**
```mermaid
sequenceDiagram
    participant User
    participant Toolbar as "PartialRegenerateToolbar"
    participant Modal as "PartialRegenerateModal"
    participant SSE as "ssePost"
    participant API as "Backend API"

    User->>User: Selects >10 chars in Editor
    Toolbar->>User: Appears at selection position
    User->>Toolbar: Click "AI重写"
    Modal->>User: Prompt for rewrite instructions
    User->>Modal: Submit instructions
    Modal->>SSE: Call /api/chapters/{id}/partial-regenerate
    SSE->>API: POST with selection_start/end
    API-->>SSE: Stream new content chunks
    SSE-->>Modal: Update preview
    Modal->>User: Show Diff Comparison
```

**Sources**: [frontend/src/pages/Chapters.tsx:126-174](), [frontend/src/components/PartialRegenerateToolbar.tsx:16-84]()

---

### Chapter Analysis & Comparison

The system integrates a "Chapter Analysis" suite that extracts plot hooks and story memories. After generation or manual editing, users can compare versions using `ChapterContentComparison` [frontend/src/components/ChapterContentComparison.tsx:18-28]().

**Key Functions**:
- **Status Polling**: `fetchAnalysisStatus` checks if the AI has finished extracting memories [frontend/src/components/ChapterAnalysis.tsx:80-122]().
- **Visual Annotation**: `AnnotatedText` highlights plot points and foreshadowing directly in the chapter content using different colors for hooks, foreshadows, and character events [frontend/src/components/AnnotatedText.tsx:51-67]().
- **Version Application**: `handleApply` in the comparison modal updates the database via `PUT /api/chapters/{chapterId}` and immediately triggers a new analysis task [frontend/src/components/ChapterContentComparison.tsx:38-88]().

**Sources**: [frontend/src/components/ChapterAnalysis.tsx:80-162](), [frontend/src/components/AnnotatedText.tsx:51-67](), [frontend/src/components/ChapterContentComparison.tsx:38-88]()

---

## Batch Generation

Batch generation allows creating multiple chapter contents sequentially. The interface manages this through a dedicated modal and polling mechanism.

**Batch Generation Logic**
```mermaid
graph TD
    "BatchForm[BatchGenerateRequest]" --> "POST /api/chapters/project/{id}/batch-generate"
    "POST /api/chapters/project/{id}/batch-generate" --> "TaskID[BatchTaskId]"
    "TaskID[BatchTaskId]" --> "startBatchPolling[setInterval 2s]"
    "startBatchPolling[setInterval 2s]" --> "GET /api/chapters/batch-generate/{taskId}/status"
    "GET /api/chapters/batch-generate/{taskId}/status" --> "UpdateUI[Update batchProgress state]"
    "UpdateUI[Update batchProgress state]" --> "CheckStatus{Status Final?}"
    "CheckStatus{Status Final?}" -- "No" --> "startBatchPolling[setInterval 2s]"
    "CheckStatus{Status Final?}" -- "Yes" --> "StopPolling[clearInterval]"
```

**Sources**: [frontend/src/pages/Chapters.tsx:692-766](), [backend/app/api/chapters.py:126-167]()

---

## Chapter Data Models

The interface interacts with the backend using Pydantic schemas for type safety.

| Schema | Purpose | Key Fields |
|--------|---------|------------|
| `ChapterCreate` | Creating new chapters manually | `project_id`, `title`, `chapter_number`, `outline_id` |
| `ChapterUpdate` | Saving content or status | `title`, `content`, `summary`, `status` |
| `ChapterGenerateRequest` | AI generation parameters | `style_id`, `target_word_count`, `model`, `narrative_perspective` |
| `ExpansionPlanUpdate` | Saving chapter scene plans | `key_events`, `character_focus`, `scenes`, `emotional_tone` |

**Sources**: [backend/app/schemas/chapter.py:20-42](), [backend/app/schemas/chapter.py:112-124](), [backend/app/schemas/chapter.py:175-195]()

---

## Component Lifecycle Summary

**Component Flow Diagram**

```mermaid
graph TD
    Mount["Component Mount"]
    
    LoadData["Load Data:<br/>- refreshChapters<br/>- loadWritingStyles<br/>- loadAnalysisTasks<br/>- checkAndRestoreBatchTask"]
    
    Display["Render Display:<br/>One-to-one vs One-to-many"]
    
    subgraph "Editor Interactions"
        TextSelect["Text Selection Detection<br/>(handleTextSelection)"]
        AIGen["SSE Content Generation<br/>(generateChapterContentStream)"]
        ManualEdit["Manual TextArea Input"]
    end
    
    subgraph "Modals & Views"
        Reader["ChapterReader<br/>(Navigation: Prev/Next)"]
        Analysis["ChapterAnalysis<br/>(Status Polling)"]
        Plan["ExpansionPlanEditor<br/>(Scene Breakdown)"]
    end
    
    Refresh["Refresh Data via useChapterSync"]
    
    Mount --> LoadData
    LoadData --> Display
    Display --> EditorInteractions
    Display --> ModalsViews
    EditorInteractions --> Refresh
    ModalsViews --> Refresh
    Refresh --> Display
```

**Sources**: [frontend/src/pages/Chapters.tsx:81-123](), [frontend/src/pages/Chapters.tsx:126-160](), [frontend/src/store/hooks.ts:232-246]()

---

# Page: Outline Interface

# Outline Interface

<details>
<summary>Relevant source files</summary>

The following files were used as context for generating this wiki page:

- [backend/app/api/outlines.py](backend/app/api/outlines.py)
- [backend/app/schemas/outline.py](backend/app/schemas/outline.py)
- [frontend/src/pages/Outline.tsx](frontend/src/pages/Outline.tsx)

</details>



## Purpose and Scope

The Outline Interface (`Outline.tsx`) is the frontend page component responsible for managing story outlines within a project. It provides a UI for creating, editing, and deleting outlines, AI-powered generation and continuation of outlines, expansion of high-level outlines into detailed chapter plans, and intelligent character prediction with user confirmation workflows.

The interface supports two distinct operational modes:
1.  **One-to-One (1→1)**: Each outline entry directly corresponds to a single chapter.
2.  **One-to-Many (1→N)**: A high-level outline (volume/arc) is expanded into multiple detailed chapter plans.

**Sources**: [frontend/src/pages/Outline.tsx:1-25](), [backend/app/api/outlines.py:58-91]()

---

## Component Architecture

### Component Structure

The `Outline` component is a complex page that manages multiple workflows through state and modal dialogs. The component structure follows this hierarchy:

```mermaid
graph TB
    Outline["Outline Component<br/>(Outline.tsx)"]
    
    subgraph "State Management"
        Store["useStore()<br/>- currentProject<br/>- outlines<br/>- setCurrentProject"]
        Hooks["useOutlineSync()<br/>- refreshOutlines()<br/>- updateOutline()<br/>- deleteOutline()"]
        LocalState["Local State<br/>- isGenerating<br/>- isExpanding<br/>- sseProgress<br/>- outlineContentExpandStatus<br/>- cachedBatchExpansionResponse"]
    end
    
    subgraph "Forms"
        EditForm["editForm<br/>Form.useForm()"]
        GenerateForm["generateForm<br/>Form.useForm()"]
        ExpansionForm["expansionForm<br/>Form.useForm()"]
        BatchExpansionForm["batchExpansionForm<br/>Form.useForm()"]
        ManualCreateForm["manualCreateForm<br/>Form.useForm()"]
    end
    
    subgraph "Modals"
        SSEModal["SSEProgressModal<br/>SSE progress display"]
        CharacterModal["Character Confirmation<br/>renderCharacterConfirmModal()"]
        ExpansionPreview["Expansion Preview<br/>showExpansionPreview()"]
        BatchPreview["Batch Preview<br/>batchPreviewVisible"]
        EditModal["Edit Modal<br/>modalApi.confirm()"]
    end
    
    Outline --> Store
    Outline --> Hooks
    Outline --> LocalState
    Outline --> Forms
    Outline --> Modals
```

**Sources**: [frontend/src/pages/Outline.tsx:121-155](), [frontend/src/pages/Outline.tsx:172-176]()

---

### Data Models and Parsing

The frontend interacts with structured JSON data stored in the `structure` field of the `Outline` model.

| Entity | Code Identifier | Description |
| :--- | :--- | :--- |
| **Outline Schema** | `OutlineResponse` | The Pydantic model returned by the backend. |
| **Structure Data** | `OutlineStructureData` | Interface for parsing the JSON `structure` field. |
| **Character Entry** | `CharacterEntry` | Unified format for characters/organizations within an outline. |
| **Chapter Plan** | `ChapterPlanItem` | Schema for AI-generated chapter plans during expansion. |

The component uses `parseOutlineStructure` to safely decode the backend's JSON strings and `parseCharacterEntries` to handle legacy string arrays versus new object-based character definitions.

**Sources**: [frontend/src/pages/Outline.tsx:42-106](), [backend/app/schemas/outline.py:30-43](), [backend/app/schemas/outline.py:81-93]()

---

## Outline Generation Workflow

### Generation Flow with Character Confirmation

The outline generation process includes a character prediction and confirmation mechanism when using "Continue" (续写) mode:

```mermaid
sequenceDiagram
    participant User
    participant UI["Outline.tsx"]
    participant SSE["SSEPostClient"]
    participant API["/api/outlines/generate-stream"]
    participant CharModal["Character Confirmation Modal"]
    
    User->>UI: Submit GenerateForm
    UI->>SSE: connect(apiUrl, requestData)
    SSE->>API: POST OutlineGenerateRequest
    
    alt Character Confirmation Required
        API-->>SSE: event: character_confirmation_required
        SSE->>UI: onCharacterConfirmation(data)
        UI->>CharModal: setCharacterConfirmVisible(true)
        User->>CharModal: Select characters & confirm
        CharModal->>UI: handleConfirmCharacters()
        UI->>SSE: Reconnect with confirmed_characters
        SSE->>API: POST with character data
    end
    
    loop Progress
        API-->>SSE: event: progress
        SSE->>UI: setSSEProgress(n)
    end
    
    API-->>SSE: event: result (Outlines)
    SSE->>UI: refreshOutlines()
```

**Sources**: [frontend/src/pages/Outline.tsx:12-25](), [frontend/src/pages/Outline.tsx:1595-1715](), [backend/app/schemas/outline.py:45-66]()

---

## Outline Expansion System

### One-to-Many Expansion

Expansion converts a high-level volume/arc into multiple detailed chapter plans. The backend `PlotExpansionService` performs the heavy lifting, while the frontend provides a two-step confirmation UI.

1.  **Expansion Request**: User specifies `target_chapter_count` and `expansion_strategy` (balanced, climax, or detail).
2.  **Preview**: The system displays generated `ChapterPlanItem` objects in a tabbed interface.
3.  **Confirmation**: User clicks "确认并创建章节", triggering `createChaptersFromPlans` which persists the chapters to the database.

```mermaid
graph LR
    subgraph "Frontend UI"
        Btn["BranchesOutlined Button"]
        Form["ExpansionForm"]
        Preview["showExpansionPreview()"]
    end
    
    subgraph "Backend Services"
        ExpSrv["PlotExpansionService"]
        OutAPI["/api/outlines/{id}/expand-stream"]
        PlanAPI["/api/outlines/create-chapters-from-plans"]
    end
    
    Btn --> Form
    Form --> OutAPI
    OutAPI --> ExpSrv
    ExpSrv --"Stream Plans"--> Preview
    Preview --"User Confirm"--> PlanAPI
```

**Sources**: [frontend/src/pages/Outline.tsx:629-812](), [backend/app/api/outlines.py:1222-1344](), [backend/app/schemas/outline.py:95-115]()

---

## UI Components and Features

### Content Management
*   **Expandable Cards**: The UI uses `outlineContentExpandStatus` to toggle the visibility of full outline summaries, preventing long lists from becoming unreadable.
*   **Scene Breakdown**: If an outline contains structured scene data, it is rendered in a collapsible section showing locations and participating characters.
*   **Search and Pagination**: Supports keyword filtering via `outlineSearchKeyword` and server-side pagination through `outlinePage` and `outlinePageSize`.

**Sources**: [frontend/src/pages/Outline.tsx:137-141](), [frontend/src/pages/Outline.tsx:167-169](), [backend/app/api/outlines.py:94-158]()

### Batch Operations
The "Batch Expansion" feature allows users to process multiple outlines at once.
*   **Request**: `BatchOutlineExpansionRequest` includes `outline_ids` and `chapters_per_outline`.
*   **Response**: `BatchOutlineExpansionResponse` provides results for all successful expansions and a list of `skipped_outlines` (e.g., those already expanded).
*   **Preview**: A specialized three-panel layout for reviewing large volumes of generated content before committing to the database.

**Sources**: [frontend/src/pages/Outline.tsx:1346-1520](), [backend/app/schemas/outline.py:116-135]()

---

## Technical Implementation Details

### Backend Data Enrichment
The backend `get_outlines` endpoint (in `outlines.py`) performs "on-the-fly" enrichment of outline objects. It parses the JSON `structure` field and populates the `title` and `content` fields dynamically if they are missing or outdated in the primary columns. It also performs a batch query to determine `has_chapters` status to avoid N+1 query problems on the frontend.

**Sources**: [backend/app/api/outlines.py:119-158]()

### Manual Creation Logic
When manually creating an outline via `manualCreateForm`, the system automatically calculates the next `order_index`. If the project is in `one-to-one` mode, the backend `create_outline` function automatically generates a corresponding `Chapter` record with status `pending`.

**Sources**: [frontend/src/pages/Outline.tsx:525-626](), [backend/app/api/outlines.py:74-87]()

---

# Page: Expansion Plan Editor

# Expansion Plan Editor

<details>
<summary>Relevant source files</summary>

The following files were used as context for generating this wiki page:

- [backend/app/api/chapters.py](backend/app/api/chapters.py)
- [backend/app/schemas/chapter.py](backend/app/schemas/chapter.py)
- [frontend/src/components/ExpansionPlanEditor.tsx](frontend/src/components/ExpansionPlanEditor.tsx)
- [frontend/src/pages/Chapters.tsx](frontend/src/pages/Chapters.tsx)
- [frontend/src/store/hooks.ts](frontend/src/store/hooks.ts)

</details>



## Purpose and Scope

The Expansion Plan Editor is a specialized frontend component used to manage detailed chapter plans before they are committed as full chapters. It allows authors to refine AI-generated plot structures, ensuring that key events, character involvement, and narrative goals align with the project's creative direction. This document details the `ExpansionPlanEditor` component, its data models, and its integration with the chapter generation workflow.

For the high-level workflow, see [Outline Expansion System](#4.4). For the data structures, see [Data Model](#3.5).

**Sources:** [frontend/src/components/ExpansionPlanEditor.tsx:9-25](), [backend/app/schemas/chapter.py:168-200]()

## Component Architecture

The `ExpansionPlanEditor` is a React functional component utilizing Ant Design's `Modal` and `Form` systems. It acts as a bridge between raw AI suggestions and the final chapter configuration stored in the database.

### Component Structure and Data Flow

```mermaid
graph TD
    subgraph "ExpansionPlanEditor (React Component)"
        FormInstance["Form.useForm()"]
        LocalState["Local State:<br/>keyEvents (string[])<br/>characters (string[])<br/>availableCharacters (Character[])"]
        
        subgraph "UI Sections"
            Overview["Section: Overview<br/>Summary (TextArea)"]
            DetailDivider["Divider: 详细规划"]
            Details["Section: Detailed Planning<br/>Key Events (Tag Input)<br/>Character Focus (Select)<br/>Emotional Tone (Input)<br/>Conflict Type (Input)<br/>Est. Words (InputNumber)<br/>Narrative Goal (TextArea)"]
        end
        
        Validation["Validation Logic:<br/>validateFields()<br/>Check empty tags"]
    end

    subgraph "External Integration"
        API_Char["characterApi.getCharacters()"]
        Parent_Save["onSave(updatedPlan)"]
        Store["Project Store (projectId)"]
    end

    Store -->|projectId| API_Char
    API_Char -->|Character List| LocalState
    LocalState -->|Options| Details
    FormInstance -->|Initial Values| Overview
    FormInstance -->|Initial Values| Details
    
    UserInteraction["User Input"] --> Overview
    UserInteraction --> Details
    
    Details --> Validation
    Validation -->|Success| Parent_Save
```

**Sources:** [frontend/src/components/ExpansionPlanEditor.tsx:26-36](), [frontend/src/components/ExpansionPlanEditor.tsx:179-202](), [frontend/src/components/ExpansionPlanEditor.tsx:205-346]()

### Props Interface

| Prop | Type | Description |
|------|------|-------------|
| `visible` | `boolean` | Controls modal visibility. |
| `planData` | `ExpansionPlanData \| null` | The AI-generated plan data to be edited. |
| `chapterSummary` | `string \| null` | The high-level summary for the chapter. |
| `projectId` | `string` | Used to fetch valid characters for selection. |
| `onSave` | `(data) => Promise<void>` | Callback to persist the edited plan. |
| `onCancel` | `() => void` | Callback to close the editor without saving. |

**Sources:** [frontend/src/components/ExpansionPlanEditor.tsx:9-25]()

## Data Model

The editor operates on the `ExpansionPlanUpdate` schema, which encapsulates the "blueprint" for a chapter.

### Schema Definition

| Field | Code Entity | Type | Description |
|-------|-------------|------|-------------|
| Summary | `summary` | `Optional[str]` | High-level plot summary. |
| Key Events | `key_events` | `List[str]` | Specific plot points to cover. |
| Characters | `character_focus` | `List[str]` | Characters featured in this chapter. |
| Tone | `emotional_tone` | `str` | Predominant mood (e.g., "Tense"). |
| Conflict | `conflict_type` | `str` | Primary driver (e.g., "Internal"). |
| Words | `estimated_words` | `int` | Target length (500 - 10,000). |
| Goal | `narrative_goal` | `str` | Purpose of the chapter in the story. |

**Sources:** [backend/app/schemas/chapter.py:175-185](), [frontend/src/components/ExpansionPlanEditor.tsx:134-143]()

## Key Implementation Details

### Character Integration
The component fetches the project's character list to ensure that the `character_focus` field uses established names rather than hallucinated ones.

```mermaid
sequenceDiagram
    participant Editor as ExpansionPlanEditor
    participant API as characterApi (frontend)
    participant Backend as ChapterRouter (backend)
    
    Editor->>API: getCharacters(projectId)
    API->>Backend: GET /api/characters/project/{id}
    Backend-->>API: List[Character]
    API-->>Editor: setAvailableCharacters(chars)
    Note over Editor: Filter options to exclude<br/>already selected tags
```

**Sources:** [frontend/src/components/ExpansionPlanEditor.tsx:39-70](), [frontend/src/store/hooks.ts:99-113]()

### Tag-Based Input Management
For `key_events` and `character_focus`, the editor uses a tag system.
- **Key Events:** Managed via `handleAddKeyEvent` which pushes strings to a local state array. [frontend/src/components/ExpansionPlanEditor.tsx:102-107]()
- **Character Focus:** Managed via an Ant Design `Select` component that filters out characters already present in the `characters` state array. [frontend/src/components/ExpansionPlanEditor.tsx:260-267]()

### Validation Logic
Before calling `onSave`, the component performs manual validation beyond standard form rules:
1. **Key Events:** Must have at least one entry.
2. **Characters:** Must have at least one entry.
3. **Form Fields:** Must pass Pydantic-aligned constraints (e.g., `estimated_words` range).

**Sources:** [frontend/src/components/ExpansionPlanEditor.tsx:120-132](), [backend/app/schemas/chapter.py:183-183]()

## Integration with Chapter Workflow

The editor is a critical step in the "One-to-Many" expansion flow.

1. **Generation:** The backend `OneToManyContextBuilder` generates several `expansion_plan` objects. [backend/app/api/chapters.py:14-17]()
2. **Review:** The frontend displays these in the `Outline` or `Chapters` page. [frontend/src/pages/Chapters.tsx:84-87]()
3. **Editing:** Clicking "Edit" opens the `ExpansionPlanEditor`.
4. **Persistence:** The `onSave` function updates the `expansion_plan` field (stored as a JSON string) in the `Chapter` model. [backend/app/schemas/chapter.py:30-30](), [backend/app/schemas/chapter.py:55-55]()

### Data Persistence Mapping

| Frontend State | Backend Model | Storage Format |
|----------------|---------------|----------------|
| `values.summary` | `Chapter.summary` | String |
| `updatedPlan` | `Chapter.expansion_plan` | JSON String |

**Sources:** [frontend/src/components/ExpansionPlanEditor.tsx:134-145](), [backend/app/models/chapter.py:18-30]() (referenced by schema usage in [backend/app/schemas/chapter.py:43-59]())

## User Interface Layout

The modal is divided into two logical sections:

1.  **Overview Section:** Contains the `summary` field, providing the broad context for the chapter. [frontend/src/components/ExpansionPlanEditor.tsx:189-200]()
2.  **Detailed Planning Section:** Separated by a `<Divider>`, containing granular controls for events, characters, and stylistic parameters. [frontend/src/components/ExpansionPlanEditor.tsx:202-344]()

The footer contains a primary "Save" button that triggers `handleSubmit`, which manages the `loading` state during the asynchronous `onSave` operation. [frontend/src/components/ExpansionPlanEditor.tsx:115-153]()

---

# Page: Settings Interface

# Settings Interface

<details>
<summary>Relevant source files</summary>

The following files were used as context for generating this wiki page:

- [backend/app/api/settings.py](backend/app/api/settings.py)
- [backend/app/schemas/settings.py](backend/app/schemas/settings.py)
- [frontend/src/pages/Settings.tsx](frontend/src/pages/Settings.tsx)
- [frontend/src/pages/SystemSettings.tsx](frontend/src/pages/SystemSettings.tsx)

</details>



## Purpose and Scope

The Settings Interface provides the frontend UI layer for managing user-specific AI configuration, including API keys, provider selection, model parameters, and reusable configuration presets. This page documents the `SettingsPage` component, the backend `settings` router, and the data flow between them. It also covers the system-level SMTP configuration accessible only to administrators.

For architectural details on how these settings are consumed, see [AI Service Architecture](5.1). For provider-specific setup, see [AI Provider Configuration](5.4).

---

## Settings Data Model

The system manages active settings, reusable presets, and system-level SMTP configurations.

### Core Settings and Presets
The `Settings` model stores the user's current active AI configuration. If a user has no saved settings, the system defaults to values defined in the `.env` file via `read_env_defaults` [backend/app/api/settings.py:42-51]().

[backend/app/schemas/settings.py:7-23]()
```python
class SettingsBase(BaseModel):
    api_provider: Optional[str] = Field(default="openai")
    api_key: Optional[str] = Field(default=None)
    api_base_url: Optional[str] = Field(default=None)
    llm_model: Optional[str] = Field(default="gpt-4")
    temperature: Optional[float] = Field(default=0.7)
    max_tokens: Optional[int] = Field(default=2000)
    system_prompt: Optional[str] = Field(default=None)
    cover_enabled: Optional[bool] = Field(default=False)
```

### API Key Presets
Presets allow users to save multiple configurations and switch between them. Activating a preset copies its `APIKeyPresetConfig` into the main `Settings` record [backend/app/schemas/settings.py:89-112]().

### System SMTP Settings
Administrators can configure global mail settings for user registration and verification [backend/app/schemas/settings.py:46-62]().

**Sources:** [backend/app/schemas/settings.py:7-143](), [backend/app/api/settings.py:42-51]()

---

## Component Architecture

The interface is split into two primary pages: `SettingsPage` for general users and `SystemSettingsPage` for administrators.

### Settings UI Logic Flow
The `SettingsPage` component manages complex state including model discovery and connection testing.

```mermaid
graph TD
    subgraph "SettingsPage.tsx Component"
        Init["useEffect: loadSettings()"]
        TabState["activeTab: 'current' | 'presets'"]
        FormState["AntD Form Instance"]
        TestState["testingApi / testResult"]
    end

    subgraph "Data Fetching"
        GetS["settingsApi.getSettings()"]
        GetP["settingsApi.getPresets()"]
        GetM["settingsApi.getAvailableModels()"]
    end

    subgraph "Backend API (app/api/settings.py)"
        S_Route["GET /settings"]
        P_Route["GET /settings/presets"]
        T_Route["POST /settings/test"]
    end

    Init --> GetS
    TabState -- "onTabChange" --> GetP
    FormState -- "onProviderChange" --> GetM
    TestState -- "onTestClick" --> T_Route

    GetS --> S_Route
    GetP --> P_Route
    GetM --> S_Route
```

**Sources:** [frontend/src/pages/Settings.tsx:13-61](), [backend/app/api/settings.py:32-160]()

---

## Implementation Details

### Settings Loading and Defaults
When a user accesses the settings, the backend first checks for a record in the `Settings` table. If missing, it performs an "auto-sync" from environment variables [backend/app/api/settings.py:176-189]().

[frontend/src/pages/Settings.tsx:86-128]()
In the frontend, `loadSettings` populates the form. It identifies "default" settings (those not yet modified by the user) by checking if the ID is `'0'` [frontend/src/pages/Settings.tsx:101-107]().

### Model Discovery
The interface dynamically fetches available models when a provider or API key is changed. This is handled by `getAvailableModels` which proxies the request through the backend to the LLM provider's metadata endpoints [frontend/src/pages/Settings.tsx:23-26]().

### MCP Plugin Integration
Saving settings triggers a check for Model Context Protocol (MCP) consistency. If the AI provider or model changes, the frontend clears the `mcp_verified_config` cache and may prompt the user to re-verify plugins [frontend/src/pages/Settings.tsx:130-185]().

**Sources:** [frontend/src/pages/Settings.tsx:86-185](), [backend/app/api/settings.py:162-192]()

---

## Connection Testing and Validation

The system provides robust testing for both LLM connections and Cover Image APIs.

### LLM Connectivity Test
The `testApiConnection` method [frontend/src/services/api.ts:191-203]() calls the backend's test endpoint, which attempts a minimal chat completion to verify credentials and latency [backend/app/api/settings.py:195-205]().

### Cover API Test
The `test_cover_settings` endpoint validates image generation providers (like OpenAI DALL-E or Stability) [backend/app/api/settings.py:195-205]().

```mermaid
sequenceDiagram
    participant UI as SettingsPage (Frontend)
    participant API as settingsApi (Axios)
    participant BE as settings.py (FastAPI)
    participant AI as AIService (Backend Service)

    UI->>API: testApiConnection(config)
    API->>BE: POST /settings/test
    BE->>AI: create_temp_service()
    AI->>AI: test_connection()
    AI-->>BE: TestResult (success, latency, preview)
    BE-->>API: JSON Response
    API-->>UI: setTestResult(data)
    UI->>UI: setShowTestResult(true)
```

**Sources:** [frontend/src/pages/Settings.tsx:27-44](), [backend/app/api/settings.py:195-210]()

---

## Administrative System Settings

The `SystemSettingsPage` is restricted to users where `is_admin` is true [frontend/src/pages/SystemSettings.tsx:118-124]().

### SMTP Configuration
This interface manages the `SystemSMTPSettings` which are stored on the administrator's settings record but applied globally for system emails [backend/app/api/settings.py:68-98]().

Key features include:
- **Provider Presets**: Quick configuration for common providers like QQ Mail [frontend/src/pages/SystemSettings.tsx:10-16]().
- **Live Testing**: The `handleTest` function allows sending a test email to verify SMTP credentials before saving [frontend/src/pages/SystemSettings.tsx:87-108]().
- **Auth Toggles**: Enable/disable email-based registration and set verification code TTL [backend/app/schemas/settings.py:59-62]().

**Sources:** [frontend/src/pages/SystemSettings.tsx:18-157](), [backend/app/api/settings.py:61-65]()

---

## API Preset Workflow

The preset system enables rapid switching between different AI models or providers (e.g., switching from "Creative GPT-4" to "Fast Claude-3-Haiku").

### Activation Logic
When a preset is activated via `activatePreset(presetId)` [frontend/src/services/api.ts:218-219](), the backend:
1. Locates the preset by ID.
2. Updates the user's primary `Settings` record with the preset's `config` values.
3. Sets `is_active` to true for the chosen preset and false for others.

### Creation from Current
Users can capture their current form state as a new preset using `createPresetFromCurrent` [frontend/src/services/api.ts:235-238](), which simplifies the workflow of "tweaking then saving" configurations.

**Sources:** [frontend/src/services/api.ts:205-239](), [backend/app/schemas/settings.py:114-143]()

---

# Page: Backend Guide

# Backend Guide

<details>
<summary>Relevant source files</summary>

The following files were used as context for generating this wiki page:

- [backend/app/database.py](backend/app/database.py)
- [backend/app/main.py](backend/app/main.py)
- [backend/app/models/__init__.py](backend/app/models/__init__.py)
- [frontend/src/App.tsx](frontend/src/App.tsx)
- [frontend/src/pages/ProjectDetail.tsx](frontend/src/pages/ProjectDetail.tsx)
- [frontend/src/pages/WritingStyles.tsx](frontend/src/pages/WritingStyles.tsx)

</details>



## Purpose and Scope

This document provides a comprehensive overview of the FastAPI backend architecture, including application structure, service layer design, API organization, and core implementation patterns. It covers how the backend components work together to provide multi-user data isolation, AI content generation, and real-time streaming updates.

For detailed information on specific aspects:
- API endpoint documentation: see [API Reference](#8)
- Database session management details: see [Database Session Management](#7.2)
- Authentication implementation: see [User Authentication and Authorization](#7.3)
- SSE streaming patterns: see [SSE Streaming Implementation](#7.4)

---

## Backend Architecture Overview

The backend is built with **FastAPI** and follows a layered architecture pattern with clear separation between API routes, business logic services, and data access. The system supports multiple users with data isolation and integrates with multiple AI providers through a unified abstraction layer.

### Core Components

| Component | Location | Purpose |
|-----------|----------|---------|
| Application Entry | `backend/app/main.py` | FastAPI app initialization, middleware setup, route registration [backend/app/main.py:1-210]() |
| Configuration | `backend/app/config.py` | Environment variable management and settings validation |
| API Routes | `backend/app/api/` | REST and SSE endpoints organized by domain [backend/app/main.py:128-160]() |
| Database | `backend/app/database.py` | Multi-user session management and connection pooling [backend/app/database.py:1-210]() |
| Models | `backend/app/models/` | SQLAlchemy ORM models [backend/app/models/__init__.py:1-50]() |
| Middleware | `backend/app/middleware/` | CORS, authentication, and request ID tracking [backend/app/main.py:81-99]() |

### Backend Module Structure

```mermaid
graph TB
    subgraph "backend/app/"
        Main["main.py<br/>FastAPI(lifespan=lifespan)"]
        
        subgraph "API Layer (api/)"
            Auth["auth.py"]
            Projects["projects.py"]
            Chapters["chapters.py"]
            Outlines["outlines.py"]
            WizardStream["wizard_stream.py"]
            Inspiration["inspiration.py"]
        end
        
        subgraph "Services"
            AIService["ai_service.py"]
            MCPClient["mcp.py<br/>mcp_client"]
        end
        
        subgraph "Data Layer"
            Database["database.py<br/>get_db dependency"]
            Models["models/<br/>SQLAlchemy Base"]
        end
        
        subgraph "Infrastructure"
            Middleware["middleware/<br/>AuthMiddleware"]
            Logger["logger.py"]
        end
    end
    
    Main --> Auth
    Main --> Projects
    Main --> Chapters
    Main --> Outlines
    Main --> WizardStream
    Main --> Middleware
    
    Projects --> Database
    Chapters --> AIService
    WizardStream --> AIService
    
    Database --> Models
    Main --> MCPClient
```

**Sources:** [backend/app/main.py:128-160](), [backend/app/database.py:1-25](), [backend/app/main.py:28-48]()

---

## Application Entry Point

The FastAPI application is initialized in `main.py`, which serves as the central orchestration point.

### FastAPI Application Setup

The application uses a **lifespan context manager** for startup and shutdown operations, handles CORS configuration, and registers all API routers.

**Key initialization steps:**

1. **Logging Setup** - Initialized via `setup_logging` using configuration settings [backend/app/main.py:17-23]().
2. **Lifespan management** - Handles MCP status synchronization, cleanup of HTTP client pools, and closing database connections [backend/app/main.py:28-48]().
3. **Middleware registration** - Includes `RequestIDMiddleware` and `AuthMiddleware` [backend/app/main.py:81-82]().
4. **Global Exception Handlers** - Custom handlers for `RequestValidationError` and general `Exception` to return structured JSON responses [backend/app/main.py:57-79]().
5. **Static file serving** - Mounts directories for `/assets` and `/generated-assets/covers` to serve the frontend and AI-generated content [backend/app/main.py:161-189]().

### Application Lifecycle

```mermaid
sequenceDiagram
    participant OS
    participant main as main.py
    participant DB as database.py
    participant AI as ai_service.py
    participant MCP as mcp.py

    OS->>main: uvicorn startup
    main->>main: lifespan start
    main->>MCP: register_status_sync()
    
    Note over main: Application Running
    
    OS->>main: Shutdown signal
    main->>main: lifespan end
    main->>MCP: mcp_client.cleanup()
    main->>AI: cleanup_http_clients()
    main->>DB: close_db()
    main-->>OS: Process Exit
```

**Sources:** [backend/app/main.py:28-48](), [backend/app/main.py:203-210]()

---

## API Layer Organization

The API layer is organized into domain-specific routers. Each router handles a specific area of functionality and follows consistent patterns for dependency injection.

### Router Structure

| Router | Path Prefix | Key Features |
|--------|-------------|--------------|
| `auth.py` | `/api/auth` | Login and OAuth callback handling [backend/app/main.py:137]() |
| `projects.py` | `/api/projects` | Project lifecycle and covers [backend/app/main.py:142-143]() |
| `chapters.py` | `/api/chapters` | CRUD and batch generation tasks [backend/app/main.py:149]() |
| `wizard_stream.py` | `/api/wizard-stream` | SSE streaming for project creation [backend/app/main.py:144]() |
| `mcp_plugins.py` | `/api/mcp-plugins` | Model Context Protocol integration [backend/app/main.py:155]() |

### Request Flow Through Backend

```mermaid
sequenceDiagram
    participant Client
    participant Auth as AuthMiddleware
    participant Router
    participant DB as get_db
    participant AI as AIService

    Client->>Auth: Request + Cookie/Header
    Auth->>Auth: Extract user_id
    Auth->>Router: Forward with state.user_id
    
    Router->>DB: Request session
    DB->>DB: get_engine(user_id)
    DB-->>Router: AsyncSession
    
    alt AI Generation
        Router->>AI: generate_text_stream()
        AI-->>Router: Chunk yield
        Router-->>Client: SSE Event
    else Standard Query
        Router->>DB: commit()
        Router-->>Client: JSON Response
    end
```

**Sources:** [backend/app/database.py:145-163](), [backend/app/main.py:81-82](), [backend/app/main.py:108-126]()

---

## Database Architecture

The backend implements a flexible database layer supporting both **PostgreSQL** and **SQLite**. It uses a shared engine approach for PostgreSQL while providing data isolation via a `user_id` field on all core models.

### Multi-User Data Isolation

The `get_db` dependency retrieves the `user_id` from the request state (populated by `AuthMiddleware`) and provides a scoped `AsyncSession` [backend/app/database.py:145-163]().

**Key Database Features:**
- **Engine Caching**: Engines are cached in `_engine_cache` to optimize connection reuse [backend/app/database.py:28-32]().
- **PostgreSQL Connection Pool**: Configurable via `pool_size`, `max_overflow`, and `pool_recycle` settings [backend/app/database.py:95-105]().
- **SQLite Concurrency**: When using SQLite, the system automatically enables **WAL (Write-Ahead Logging)** mode to support concurrent read/write operations [backend/app/database.py:124-138]().
- **Session Monitoring**: The `_session_stats` dictionary tracks created, active, and closed sessions to detect potential connection leaks [backend/app/database.py:35-42]().

For detailed session lifecycle and transaction management, see [Database Session Management](#7.2).

**Sources:** [backend/app/database.py:1-143](), [backend/app/main.py:108-126]()

---

## Middleware and Request Processing

### Authentication Middleware
The `AuthMiddleware` is responsible for extracting identity information from incoming requests and attaching it to the `request.state.user_id` for use by downstream dependencies like `get_db` [backend/app/main.py:82]().

### CORS Configuration
In debug mode, the backend allows all origins. In production, it restricts access to origins defined in `config_settings.cors_origins` [backend/app/main.py:84-99]().

### Health and Monitoring
The backend provides a specialized endpoint at `/health/db-sessions` that returns real-time statistics on database connection usage, including active session counts and SSE disconnection counts (`generator_exits`) [backend/app/main.py:108-126]().

---

## Summary

The FastAPI backend architecture provides:

✅ **Modular Routing** - Domain-driven endpoint organization.  
✅ **Hybrid Database Support** - Optimized for both PostgreSQL and SQLite with WAL mode.  
✅ **Lifecycle Management** - Clean startup/shutdown of AI clients and MCP plugins.  
✅ **Resource Monitoring** - Built-in session tracking to prevent leaks.  
✅ **Multi-User Security** - Isolation enforced at the database session level.

For implementation details of specific subsystems:
- API endpoints: [API Reference](#8)
- Database transactions: [Database Session Management](#7.2)
- Authentication flows: [User Authentication and Authorization](#7.3)
- SSE implementation: [SSE Streaming Implementation](#7.4)

**Sources:** [backend/app/main.py:1-210](), [backend/app/database.py:1-190]()

---

# Page: API Structure

# API Structure

<details>
<summary>Relevant source files</summary>

The following files were used as context for generating this wiki page:

- [backend/app/api/common.py](backend/app/api/common.py)
- [backend/app/main.py](backend/app/main.py)
- [frontend/src/App.tsx](frontend/src/App.tsx)
- [frontend/src/pages/ProjectDetail.tsx](frontend/src/pages/ProjectDetail.tsx)
- [frontend/src/pages/WritingStyles.tsx](frontend/src/pages/WritingStyles.tsx)

</details>



## Purpose and Scope

This document describes the organization and architectural patterns of the FastAPI backend API layer, including route organization, middleware stack, dependency injection, error handling, and response patterns. The backend is designed to handle both standard RESTful JSON requests and long-running AI generation tasks via Server-Sent Events (SSE).

---

## Router Organization

The backend API is organized into modular routers, each responsible for a specific domain of functionality. All API route modules are located in `backend/app/api/`.

### API Module Structure

The following diagram maps the logical API domains to their corresponding code entities and registration points.

```mermaid
graph TB
    subgraph "Code Entity Space (backend/app/api/)"
        WizardStream["wizard_stream.py<br/>Router: /wizard-stream"]
        Projects["projects.py<br/>Router: /projects"]
        Chapters["chapters.py<br/>Router: /chapters"]
        Outlines["outlines.py<br/>Router: /outlines"]
        Characters["characters.py<br/>Router: /characters"]
        Settings["settings.py<br/>Router: /settings"]
        Auth["auth.py<br/>Router: /auth"]
        McpPlugins["mcp_plugins.py<br/>Router: /mcp-plugins"]
    end
    
    MainApp["backend/app/main.py<br/>FastAPI(app)"]
    
    MainApp -- "app.include_router(auth.router, prefix='/api')" --> Auth
    MainApp -- "app.include_router(projects.router, prefix='/api')" --> Projects
    MainApp -- "app.include_router(chapters.router, prefix='/api')" --> Chapters
    MainApp -- "app.include_router(wizard_stream.router, prefix='/api')" --> WizardStream
    MainApp -- "app.include_router(mcp_plugins.router, prefix='/api')" --> McpPlugins
    
    style MainApp stroke-width:2px
```

**Sources:** [backend/app/main.py:128-160](), [backend/app/api/wizard_stream.py:23]()

### Router Declaration Pattern

Each API module follows a consistent pattern for declaring routers using FastAPI's `APIRouter`. Routers are then imported and included in the main application instance in `backend/app/main.py`.

| Module | Prefix (at include) | Primary Purpose |
|--------|--------|-----------------|
| `auth.py` | `/api` | Authentication and OAuth (LinuxDO) |
| `projects.py` | `/api` | Project CRUD and metadata management |
| `wizard_stream.py` | `/api` | SSE-based AI project creation wizard |
| `chapters.py` | `/api` | Chapter generation, batching, and analysis |
| `outlines.py` | `/api` | Outline CRUD and expansion logic |
| `characters.py` | `/api` | Character, organization, and relationship management |
| `mcp_plugins.py` | `/api` | Model Context Protocol (MCP) tool management |
| `settings.py` | `/api` | User AI provider and model configuration |

**Sources:** [backend/app/main.py:137-159](), [backend/app/api/wizard_stream.py:23]()

---

## Middleware Stack

The application uses a stack of middlewares to handle cross-cutting concerns before requests reach the route handlers.

| Middleware | Implementation | Purpose |
|------------|----------------|---------|
| `RequestIDMiddleware` | [backend/app/middleware/request_id.py]() | Injects a unique UUID into every request for tracing. |
| `AuthMiddleware` | [backend/app/middleware/auth_middleware.py]() | Validates sessions/tokens and populates `request.state.user_id`. |
| `CORSMiddleware` | `fastapi.middleware.cors` | Handles Cross-Origin Resource Sharing based on `config_settings.cors_origins`. |

**Sources:** [backend/app/main.py:81-99]()

---

## Dependency Injection System

The API layer uses FastAPI's `Depends` system to inject shared resources like database sessions and AI services.

### Dependency Flow Architecture

The following diagram shows how high-level route handlers interact with lower-level services through the dependency injection system.

```mermaid
graph TB
    subgraph "Natural Language Space"
        Req["Incoming Request"]
        Logic["Business Logic"]
    end

    subgraph "Code Entity Space"
        Handler["Route Handler<br/>(e.g., generate_world_building_stream)"]
        GetDB["get_db()<br/>(Dependency Provider)"]
        GetAI["get_user_ai_service()<br/>(Dependency Provider)"]
        VerifyAccess["verify_project_access_from_request()"]
        
        Handler -- "Depends(get_db)" --> GetDB
        Handler -- "Depends(get_user_ai_service)" --> GetAI
        Logic -- "Calls" --> VerifyAccess
    end

    Req --> Handler
    Handler --> Logic
    VerifyAccess -- "Uses" --> GetDB
```

**Sources:** [backend/app/api/common.py:75-98](), [backend/app/api/wizard_stream.py:191-196]()

### Core Dependencies

*   **`get_db`**: Yields an `AsyncSession` for the current user. It manages per-user SQLite connection pools to ensure data isolation. [backend/app/main.py:11-11]().
*   **`get_user_ai_service`**: Returns an `AIService` instance pre-configured with the user's specific API keys and model preferences.
*   **`verify_project_access_from_request`**: A common utility that checks if the `user_id` in the request state has permission to access the requested `project_id`. [backend/app/api/common.py:75-84]().

---

## Response Patterns

### Standard JSON Responses
Used for CRUD operations. These return Pydantic models serialized to JSON.
**Sources:** [backend/app/main.py:61-67]()

### Server-Sent Events (SSE)
Used for AI generation. The backend uses a custom `SSEResponse` utility to stream progress, content chunks, and final results.
*   **Content-Type**: `text/event-stream`
*   **Event Types**: `progress`, `chunk`, `result`, `error`, `heartbeat`, `done`.

**Sources:** [backend/app/api/wizard_stream.py:27-40](), [backend/app/main.py:118-119]()

---

## Exception Handling

The application defines global exception handlers in `backend/app/main.py` to ensure consistent error responses.

### Validation Errors
`RequestValidationError` is caught to return a `422 Unprocessable Entity` status with a detailed error list.
**Sources:** [backend/app/main.py:57-67]()

### Global Exception Handler
All unhandled exceptions are caught by a global handler. In debug mode, it returns the full stack trace; in production, it returns a generic "Server Internal Error" message.
**Sources:** [backend/app/main.py:69-79]()

### SSE Error Handling
Inside streaming generators, exceptions must be caught manually to send an `error` event before the connection closes, as standard FastAPI exception handlers cannot modify a response that has already started streaming.

```python
try:
    # generation logic
except Exception as e:
    yield await SSEResponse.send_error(str(e))
```
**Sources:** [backend/app/api/wizard_stream.py:182-188]()

---

## Application Lifespan

The `lifespan` async context manager handles application startup and shutdown tasks:
1.  **Startup**: Registers MCP status synchronization. [backend/app/main.py:31-31]().
2.  **Shutdown**:
    *   Cleans up the MCP client. [backend/app/main.py:38-38]().
    *   Cleans up the AI Service HTTP client pool. [backend/app/main.py:41-42]().
    *   Closes all active database connections. [backend/app/main.py:45-45]().

**Sources:** [backend/app/main.py:27-48]()

---

# Page: Database Session Management

# Database Session Management

<details>
<summary>Relevant source files</summary>

The following files were used as context for generating this wiki page:

- [backend/app/database.py](backend/app/database.py)
- [backend/app/models/__init__.py](backend/app/models/__init__.py)
- [backend/scripts/init_postgres.sql](backend/scripts/init_postgres.sql)

</details>



## Purpose and Scope

This document details the database session management system in MuMuAINovel's backend, specifically covering how database connections and sessions are created, managed, and monitored throughout request lifecycles. The system uses a shared connection pool architecture with application-level data isolation to support multiple concurrent users efficiently.

For information about the overall database architecture and multi-user data isolation strategy, see [Database Architecture](#3.4). For authentication and user context setup, see [User Authentication and Authorization](#7.3). For API endpoint structure and middleware, see [7.1 API Structure]().

**Sources:** [backend/app/database.py:1-42](), [backend/app/database.py:145-155]()

---

## Core Architecture

### Shared Engine Model

MuMuAINovel uses a **single shared PostgreSQL engine** for all users rather than per-user database instances. This design provides several benefits:

- **Connection Pool Efficiency**: One large pool serves all users, maximizing connection reuse. [backend/app/database.py:56-59]()
- **Resource Optimization**: Configurable core connections and overflow connections support high concurrency. [backend/app/database.py:107-118]()
- **Simplified Management**: No need to create/destroy engines per user. [backend/app/database.py:45-55]()
- **Cost Effective**: Single database instance reduces infrastructure costs.

Data isolation is enforced at the **application layer** through automatic `user_id` filtering on all queries, not at the database level. [backend/app/database.py:48-48]()

**Sources:** [backend/app/database.py:45-142](), [backend/app/config.py:46-62]()

---

## Session Dependency Function

### The `get_db` Dependency

The `get_db` function is the primary FastAPI dependency for obtaining database sessions. It integrates with the request lifecycle and user authentication system. [backend/app/database.py:145-150]()

**Key Responsibilities:**
1. Extract `user_id` from `request.state` (set by `AuthMiddleware`). [backend/app/database.py:150-150]()
2. Obtain shared engine via `get_engine(user_id)`. [backend/app/database.py:155-155]()
3. Create session-scoped `AsyncSession` instance using `async_sessionmaker`. [backend/app/database.py:157-163]()
4. Track session statistics for monitoring. [backend/app/database.py:166-168]()
5. Handle cleanup and transaction rollbacks in `finally` block. [backend/app/database.py:196-224]()

**Sources:** [backend/app/database.py:145-225]()

### Request Integration Flow

```mermaid
sequenceDiagram
    participant Client
    participant AuthMiddleware
    participant Router as "FastAPI Router"
    participant GetDB as "get_db(request)"
    participant Engine as "shared_postgres Engine"
    participant Session as "AsyncSession"
    participant Handler as "Endpoint Handler"

    Client->>AuthMiddleware: "HTTP Request with JWT"
    AuthMiddleware->>AuthMiddleware: "Validate JWT/Session"
    AuthMiddleware->>AuthMiddleware: "Extract user_id"
    AuthMiddleware->>Router: "request.state.user_id = 'xxx'"
    
    Router->>GetDB: "Dependency injection"
    GetDB->>GetDB: "user_id = request.state.user_id"
    
    alt No user_id
        GetDB-->>Router: "HTTPException(401)"
    end
    
    GetDB->>Engine: "get_engine(user_id)"
    Engine-->>GetDB: "shared engine instance"
    
    GetDB->>Session: "AsyncSessionLocal()"
    GetDB->>GetDB: "_session_stats[created] += 1"
    GetDB->>GetDB: "_session_stats[active] += 1"
    GetDB->>Handler: "yield session"
    
    Handler->>Session: "Query operations (e.g. Project, Chapter)"
    Session-->>Handler: "Results"
    
    Handler-->>GetDB: "Return/Exception"
    
    GetDB->>GetDB: "Handle exceptions"
    GetDB->>Session: "rollback() if in_transaction()"
    GetDB->>Session: "close()"
    GetDB->>GetDB: "_session_stats[closed] += 1"
    GetDB->>GetDB: "_session_stats[active] -= 1"
    
    GetDB-->>Router: "Session cleaned up"
```

**Sources:** [backend/app/database.py:145-225](), [backend/app/models/__init__.py:1-25]()

---

## Connection Pool Configuration

### PostgreSQL Pool Parameters

The connection pool is configured via `settings` in `app/config.py` for high-concurrency scenarios:

| Parameter | Purpose | Code Reference |
|-----------|---------|----------------|
| `pool_size` | Core persistent connections always available | [backend/app/database.py:96-96]() |
| `max_overflow` | Additional connections created under load | [backend/app/database.py:97-97]() |
| `pool_timeout` | Max wait time to acquire connection | [backend/app/database.py:98-98]() |
| `pool_recycle` | Recycle connections (default 1800s) | [backend/app/database.py:100-100]() |
| `pool_pre_ping` | Test connection validity before use | [backend/app/database.py:99-99]() |
| `pool_use_lifo` | Reuse recently-used connections | [backend/app/database.py:101-101]() |

**Sources:** [backend/app/database.py:95-118]()

### Engine Creation and Caching

```mermaid
graph TB
    subgraph "Engine Cache Strategy"
        GetEngine["get_engine(user_id)"]
        CacheCheck{"'shared_postgres' in<br/>_engine_cache?"}
        ReturnCached["Return cached engine"]
        
        AcquireLock["Acquire _cache_lock"]
        DoubleCheck{"Double-check<br/>cache after lock"}
        CreateEngine["create_async_engine()"]
        ConfigurePool["Configure pool parameters<br/>from app.config.settings"]
        StoreCache["_engine_cache['shared_postgres'] = engine"]
        ReturnNew["Return new engine"]
    end
    
    GetEngine --> CacheCheck
    CacheCheck -->|Yes| ReturnCached
    CacheCheck -->|No| AcquireLock
    AcquireLock --> DoubleCheck
    DoubleCheck -->|Still missing| CreateEngine
    DoubleCheck -->|Now exists| ReturnCached
    CreateEngine --> ConfigurePool
    ConfigurePool --> StoreCache
    StoreCache --> ReturnNew
```

**Key Implementation Details:**

1. **Cache Key**: Always `"shared_postgres"` regardless of `user_id` to enforce sharing. [backend/app/database.py:57-57]()
2. **Thread Safety**: Uses `asyncio.Lock` (`_cache_lock`) to prevent race conditions during engine creation. [backend/app/database.py:32-32, 61-61]()
3. **Double-Check Pattern**: Re-checks cache after acquiring lock to avoid duplicate engine creation. [backend/app/database.py:62-62]()
4. **Lazy Initialization**: Engine created on first database access, not at startup. [backend/app/database.py:45-55]()

**Sources:** [backend/app/database.py:27-32, 45-142]()

### SQLite Fallback Support

For development or single-user deployments, the system supports SQLite with specialized handling:

- Uses `NullPool` (no connection pooling). [backend/app/database.py:74-74, 127-127]()
- Enables **WAL mode** (Write-Ahead Logging) for better read-write concurrency via SQLAlchemy events. [backend/app/database.py:129-136]()
- Sets `busy_timeout=30000` (30 seconds) to handle locks. [backend/app/database.py:135-135]()

**Sources:** [backend/app/database.py:64-141]()

---

## Session Lifecycle Management

### Session Creation

When a session is created through `get_db`, the following steps occur:

1. **User ID Validation**: Checks `request.state.user_id` is not `None`, else raises 401. [backend/app/database.py:150-153]()
2. **Engine Retrieval**: Calls `get_engine(user_id)` to get shared engine. [backend/app/database.py:155-155]()
3. **Session Factory**: Creates `async_sessionmaker` with `expire_on_commit=False`. [backend/app/database.py:157-161]()
4. **Session Instantiation**: Calls `AsyncSessionLocal()` to create session. [backend/app/database.py:163-163]()
5. **Statistics Update**: Increments `_session_stats["created"]` and `_session_stats["active"]`. [backend/app/database.py:167-168]()

**Sources:** [backend/app/database.py:145-171]()

### Exception Handling

The `get_db` function implements comprehensive exception handling:

#### 1. GeneratorExit Exception
Occurs when SSE connections (Server-Sent Events) are prematurely closed (e.g., user navigates away). The system rolls back any active transactions. [backend/app/database.py:176-185]()

#### 2. General Exceptions
Application or database errors trigger a rollback and log the error before propagating the exception. [backend/app/database.py:186-195]()

#### 3. Finally Block Cleanup
**Always executes** to ensure resources are released:
- Check for uncommitted transactions and rollback with warning. [backend/app/database.py:198-204]()
- Close session (`await session.close()`). [backend/app/database.py:207-207]()
- Update statistics (`closed += 1`, `active -= 1`). [backend/app/database.py:210-211]()
- Check against leak thresholds. [backend/app/database.py:213-217]()

**Sources:** [backend/app/database.py:172-225]()

---

## Monitoring and Health Checks

### Session Statistics Tracking

The system maintains real-time statistics in the `_session_stats` dictionary. [backend/app/database.py:35-42]()

| Metric | Description |
|--------|-------------|
| `created` | Total sessions created since startup |
| `closed` | Total sessions properly closed |
| `active` | Currently active sessions |
| `errors` | Errors during session lifecycle |
| `generator_exits` | SSE disconnections |

**Leak Detection Logic:**
If `active` sessions exceed thresholds (default 50 for warning, 100 for critical), the system logs alerts. [backend/app/database.py:213-217]()

**Sources:** [backend/app/database.py:34-42, 210-217]()

### Health Check Function

The `check_database_health()` function performs live connection testing:

1. Obtain engine. [backend/app/database.py:488-488]()
2. Create temporary session. [backend/app/database.py:494-494]()
3. Execute `SELECT 1` query. [backend/app/database.py:495-495]()
4. Check connection pool status (PostgreSQL only). [backend/app/database.py:504-517]()
5. Return health status with warnings if pool usage is high. [backend/app/database.py:519-541]()

**Sources:** [backend/app/database.py:476-541]()

---

## Best Practices

### For Endpoint Developers

1. **Always use `Depends(get_db)`**: Never create sessions manually in routers. [backend/app/database.py:145-149]()
2. **Commit explicitly**: Use `await db.commit()` when making changes to models like `Project`, `Chapter`, or `Character`.
3. **Let exceptions propagate**: Don't catch database errors silently; let `get_db` handle cleanup and rollback. [backend/app/database.py:186-195]()
4. **Avoid long-lived sessions**: Complete database work within single request; don't store sessions in global state.

**Sources:** [backend/app/database.py:145-225](), [backend/app/models/__init__.py:1-25]()

### For SSE Streaming Endpoints

Special considerations for Server-Sent Events (SSE) endpoints:

1. **Expect GeneratorExit**: Client disconnections are normal; system handles them gracefully. [backend/app/database.py:176-178]()
2. **Rollback on Disconnect**: The system automatically rolls back transactions if a stream is cut. [backend/app/database.py:179-182]()
3. **Monitor `generator_exits`**: High counts may indicate network instability or UI issues. [backend/app/database.py:178-178]()

**Sources:** [backend/app/database.py:176-185]()

---

# Page: User Authentication and Authorization

# User Authentication and Authorization

<details>
<summary>Relevant source files</summary>

The following files were used as context for generating this wiki page:

- [backend/app/api/admin.py](backend/app/api/admin.py)
- [backend/app/api/users.py](backend/app/api/users.py)
- [backend/app/middleware/auth_middleware.py](backend/app/middleware/auth_middleware.py)
- [backend/app/services/oauth_service.py](backend/app/services/oauth_service.py)
- [frontend/src/components/UserMenu.tsx](frontend/src/components/UserMenu.tsx)
- [frontend/src/pages/Login.tsx](frontend/src/pages/Login.tsx)
- [frontend/src/pages/UserManagement.tsx](frontend/src/pages/UserManagement.tsx)

</details>



## Purpose and Scope

This document describes the authentication and authorization mechanisms in MuMuAINovel. It covers:

- **Authentication methods**: Local username/password authentication, Email-based auth, and LinuxDO OAuth2 integration.
- **AuthMiddleware**: User identity extraction, request state management, and support for proxy requests.
- **Session management**: Token-based sessions and persistent user state.
- **User Management**: Administrative interfaces for user lifecycle, password resets, and trust levels.
- **Multi-user data isolation**: Application-level data segregation in the shared PostgreSQL database.

For information about database connection management and session lifecycle, see [7.2](). For details on API endpoint structure, see [7.1](). For frontend routing configuration, see [6.1]().

---

## Authentication Architecture Overview

The system employs a multi-layered authentication strategy. The backend `AuthMiddleware` acts as the primary gatekeeper, while the frontend `Login.tsx` manages the various entry points for user identification.

### Authentication Flow Diagram

```mermaid
graph TB
    subgraph "Client Layer"
        [Browser]
        ["Login.tsx"]
        ["AuthCallback.tsx"]
    end
    
    subgraph "Frontend Authentication"
        ["ProtectedRoute.tsx"]
        ["authApi" service]
        [LocalStorage]
    end
    
    subgraph "Backend Middleware Stack"
        ["AuthMiddleware" backend/app/middleware/auth_middleware.py]
        ["user_manager" backend/app/user_manager.py]
    end
    
    subgraph "Authentication Providers"
        ["LocalAuth" username/password]
        ["EmailAuth" OTP verification]
        ["LinuxDOOAuthService" backend/app/services/oauth_service.py]
    end
    
    subgraph "Database Layer"
        ["User Table" backend/app/models/user.py]
        ["PostgreSQL" DB]
    end
    
    [Browser] --> ["Login.tsx"]
    ["Login.tsx"] --> ["LocalAuth"]
    ["Login.tsx"] --> ["EmailAuth"]
    ["Login.tsx"] --> ["LinuxDOOAuthService"]
    
    ["LinuxDOOAuthService"] --> ["AuthCallback.tsx"]
    
    ["LocalAuth"] --> ["AuthMiddleware"]
    ["EmailAuth"] --> ["AuthMiddleware"]
    ["AuthCallback.tsx"] --> ["AuthMiddleware"]
    
    ["AuthMiddleware"] --> ["user_manager"]
    ["user_manager"] --> ["User Table"]
    ["User Table"] --> [PostgreSQL]
    
    ["authApi"] -.-> ["AuthMiddleware"]
    ["ProtectedRoute.tsx"] -.-> ["authApi"]
```

**Sources**: [backend/app/middleware/auth_middleware.py:13-43](), [frontend/src/pages/Login.tsx:171-201](), [backend/app/services/oauth_service.py:10-17]()

---

## Authentication Methods

MuMuAINovel supports three primary authentication methods, configurable via the `AuthConfig` interface [frontend/src/pages/Login.tsx:37-42]().

### 1. Local Authentication
Uses standard username and password credentials. The frontend `handleLocalLogin` function calls `authApi.localLogin` [frontend/src/pages/Login.tsx:171-183]().

### 2. Email Authentication
Supports both login and registration via email verification codes (OTP).
- **Login**: `handleEmailLogin` sends an email and code to the backend [frontend/src/pages/Login.tsx:185-200]().
- **Registration**: Users can register with an email, code, and password [frontend/src/pages/Login.tsx:54-60]().
- **Password Reset**: Users can reset forgotten passwords using email verification [frontend/src/pages/Login.tsx:62-67]().

### 3. LinuxDO OAuth2 Integration
Provides social authentication through the LinuxDO platform.
- **Service**: Managed by `LinuxDOOAuthService` [backend/app/services/oauth_service.py:10-152]().
- **Endpoints**: Uses `AUTHORIZE_URL` (`/oauth2/authorize`), `TOKEN_URL` (`/oauth2/token`), and `USERINFO_URL` (`/api/user`) [backend/app/services/oauth_service.py:14-16]().
- **User Creation**: Automatically creates or updates local user records from LinuxDO profiles via `user_manager.create_or_update_from_linuxdo` [backend/app/api/admin.py:135-141]().

---

## AuthMiddleware Implementation

The `AuthMiddleware` [backend/app/middleware/auth_middleware.py:13-80]() is responsible for extracting identity from every incoming request and injecting it into `request.state`.

### Identity Extraction Logic

1. **Proxy Request Detection**: It checks for `X-Instance-ID` and `X-User-ID` headers to support "Prompt Workshop" proxy requests [backend/app/middleware/auth_middleware.py:24-39]().
2. **Cookie Authentication**: For standard requests, it retrieves the `user_id` from the `user_id` cookie [backend/app/middleware/auth_middleware.py:50]().
3. **User Validation**: It fetches the user via `user_manager.get_user(user_id)` [backend/app/middleware/auth_middleware.py:53]().
4. **Trust Level Enforcement**: If a user's `trust_level` is set to `-1`, they are treated as disabled and access is denied [backend/app/middleware/auth_middleware.py:55-61]().
5. **State Injection**: Successful authentication populates `request.state.user_id`, `request.state.user`, and `request.state.is_admin` [backend/app/middleware/auth_middleware.py:64-66]().

**Sources**: [backend/app/middleware/auth_middleware.py:13-80]()

---

## Authorization and Admin Privileges

The system uses a combination of trust levels and an explicit `is_admin` flag to control access.

### Permission Dependencies
Backend routes use FastAPI dependencies to enforce access control:
- `require_login`: Ensures `request.state.user` exists [backend/app/api/users.py:13-17]().
- `require_admin` / `check_admin`: Ensures the user is logged in AND `is_admin` is true [backend/app/api/users.py:20-25](), [backend/app/api/admin.py:76-86]().

### User Management Capabilities
The `UserManagement.tsx` component [frontend/src/pages/UserManagement.tsx:58-300]() provides an interface for administrators to:
- **List Users**: Fetch all users with status, trust level, and last login [frontend/src/pages/UserManagement.tsx:146-157]().
- **Create Users**: Manually add users and generate initial passwords [frontend/src/pages/UserManagement.tsx:173-203]().
- **Toggle Status**: Enable or disable accounts (sets `trust_level` to `-1`) [frontend/src/pages/UserManagement.tsx:240-252]().
- **Reset Passwords**: Reset a user's password to a default or specified value [backend/app/api/users.py:134-183]().
- **Modify Trust Levels**: Adjust `trust_level` (0-9) which can be used for feature gating [backend/app/api/admin.py:38]().

### Multi-User Data Isolation
Data isolation is maintained by filtering database queries using the `user_id` injected by `AuthMiddleware`.
- **Database Sessions**: `get_db` relies on `request.state.user_id` to provide a context-aware session [backend/app/database.py:145-224]().
- **Admin Bypass**: Admin APIs (e.g., `get_users`) explicitly use the `user_manager` to aggregate data across users for management purposes [backend/app/api/admin.py:90-115]().

---

## Session Management

Sessions are managed via HTTP-only cookies and the `authApi` service.

| Feature | Implementation |
| :--- | :--- |
| **Login** | `authApi.localLogin` or `authApi.emailLogin` sets the session [frontend/src/pages/Login.tsx:171-200](). |
| **Logout** | `authApi.logout` clears the session and redirects to `/login` [frontend/src/components/UserMenu.tsx:40-49](). |
| **Persistence** | User info is loaded on mount via `authApi.getCurrentUser` [frontend/src/components/UserMenu.tsx:31-38](). |
| **Password Change** | Users can update their own passwords via `authApi.setPassword` [frontend/src/components/UserMenu.tsx:59-73](). |

### Identity Flow in Code

```mermaid
sequenceDiagram
    participant B as Browser
    participant M as AuthMiddleware
    participant UM as user_manager
    participant R as Route Handler
    
    B->>M: Request with Cookie: user_id=...
    M->>UM: get_user(user_id)
    UM-->>M: User Object (is_admin=True)
    M->>M: Set request.state.user = User
    M->>R: Proceed to Handler
    R->>R: Depends(require_admin)
    Note over R: Check request.state.is_admin
    R-->>B: 200 OK / Data
```

**Sources**: [backend/app/middleware/auth_middleware.py:44-77](), [backend/app/api/users.py:20-25](), [frontend/src/components/UserMenu.tsx:75-119]()

---

# Page: SSE Streaming Implementation

# SSE Streaming Implementation

<details>
<summary>Relevant source files</summary>

The following files were used as context for generating this wiki page:

- [backend/app/api/chapters.py](backend/app/api/chapters.py)
- [backend/app/schemas/chapter.py](backend/app/schemas/chapter.py)
- [backend/app/services/auto_character_service.py](backend/app/services/auto_character_service.py)
- [backend/app/services/auto_organization_service.py](backend/app/services/auto_organization_service.py)
- [backend/app/utils/sse_response.py](backend/app/utils/sse_response.py)
- [frontend/src/components/ExpansionPlanEditor.tsx](frontend/src/components/ExpansionPlanEditor.tsx)
- [frontend/src/pages/Chapters.tsx](frontend/src/pages/Chapters.tsx)
- [frontend/src/store/hooks.ts](frontend/src/store/hooks.ts)
- [frontend/src/utils/sseClient.ts](frontend/src/utils/sseClient.ts)

</details>



## Purpose and Scope

This document details the Server-Sent Events (SSE) streaming architecture used throughout MuMuAINovel to deliver real-time AI generation progress to the frontend. SSE enables long-running AI operations—such as world-building, character generation, outline creation, and chapter expansion—to stream progress updates, content chunks, and results without timeout issues.

The implementation covers standardized backend response utilities, async generator patterns for FastAPI, transaction management during streaming, and a custom frontend client for handling POST-based SSE.

---

## SSE Response Format

MuMuAINovel uses a standardized SSE message format defined in the `SSEResponse` utility class. All SSE events follow the Server-Sent Events specification with `event:` and `data:` fields.

### Message Types

| Event Type | Purpose | Data Format |
|------------|---------|-------------|
| `progress` | Progress updates with percentage | `{"message": str, "progress": int, "status": str, "word_count": int}` |
| `chunk` | Streaming content fragments | `{"content": str}` |
| `result` | Final generation result | `{...}` (varies by endpoint) |
| `error` | Error notification | `{"message": str, "code": int}` |
| `done` | Stream completion signal | `{}` |

### SSEResponse Utility Class

The backend provides helper methods for generating standardized SSE messages in `backend/app/utils/sse_response.py`.

```python
# backend/app/utils/sse_response.py
class SSEResponse:
    @staticmethod
    async def send_progress(message: str, progress: int, status: str = "info", word_count: int = None) -> str:
        # Returns formatted "data: {...}\n\n" string
```

The system also includes a `WizardProgressTracker` to manage standardized progress stages:
*   `INIT`: 0-5% [backend/app/utils/sse_response.py:41]()
*   `LOADING`: 5-15% [backend/app/utils/sse_response.py:42]()
*   `PREPARING`: 15-20% [backend/app/utils/sse_response.py:43]()
*   `GENERATING`: 20-85% [backend/app/utils/sse_response.py:44]()
*   `PARSING`: 85-92% [backend/app/utils/sse_response.py:45]()
*   `SAVING`: 92-98% [backend/app/utils/sse_response.py:46]()
*   `COMPLETE`: 100% [backend/app/utils/sse_response.py:47]()

**Sources:** [backend/app/utils/sse_response.py:1-210]()

---

## Backend SSE Implementation

### Async Generator Pattern

SSE endpoints are implemented as async generators that yield SSE-formatted strings. FastAPI's `StreamingResponse` handles the delivery.

**SSE Data Flow (Code Entity Space)**

```mermaid
graph TB
    subgraph "Frontend (React)"
        C["SSEPostClient (sseClient.ts)"]
    end

    subgraph "Backend (FastAPI)"
        R["Router (chapters.py / outlines.py)"]
        G["Async Generator Function"]
        T["WizardProgressTracker (sse_response.py)"]
        AI["AIService (ai_service.py)"]
    end

    C -->|"POST Request"| R
    R -->|"calls"| G
    G -->|"yield tracker.start()"| T
    G -->|"async for chunk in AI.generate_text_stream()"| AI
    AI -->>|"yields chunk"| G
    G -->>|"yield SSEResponse.send_chunk()"| C
    G -->|"db.commit()"| DB[("SQLite (SQLAlchemy)")]
```

**Sources:** [backend/app/utils/sse_response.py:51-65](), [backend/app/api/chapters.py:60](), [backend/app/services/ai_service.py:52]()

### Core Generator Structure

All SSE generators follow a robust pattern to handle database integrity:

1.  **Initialization:** Define a `db_committed` flag as `False`. [backend/app/api/chapters.py:65]() (Contextual pattern used in wizard and chapter generation).
2.  **Streaming Phase:** Use `async for` to consume chunks from `AIService`.
3.  **Progress Updates:** Use `WizardProgressTracker` to send periodic updates. [backend/app/utils/sse_response.py:124-163]()
4.  **Finalization:** Perform database operations, commit, and set `db_committed = True`.
5.  **Cleanup:** Use a `finally` block or `except GeneratorExit` to rollback if the client disconnects before the commit.

---

## Transaction Management in SSE

SSE streams present challenges because the connection can be interrupted at any time. MuMuAINovel uses a per-user lock and careful commit logic.

### User-Level Locking

For SQLite stability during async operations, the backend implements a `db_write_locks` dictionary.

```python
# backend/app/api/chapters.py
db_write_locks: dict[str, Lock] = {}

async def get_db_write_lock(user_id: str) -> Lock:
    if user_id not in db_write_locks:
        db_write_locks[user_id] = Lock()
    return db_write_locks[user_id]
```

**Sources:** [backend/app/api/chapters.py:65-74]()

### Transaction Lifecycle

```mermaid
sequenceDiagram
    participant FE as "SSEPostClient (Frontend)"
    participant BE as "FastAPI Endpoint"
    participant AI as "AIService"
    participant DB as "SQLAlchemy Session"

    FE->>BE: POST /api/chapters/generate
    BE->>BE: Acquire user Lock()
    BE->>DB: Start Transaction
    BE->>AI: generate_text_stream()
    loop Stream Content
        AI-->>BE: chunk
        BE-->>FE: SSE: chunk + progress
    end
    BE->>DB: db.add(Chapter)
    BE->>DB: db.commit()
    BE-->>FE: SSE: result + done
    BE->>BE: Release Lock()
    Note over BE,DB: If FE disconnects early, rollback() occurs in except block
```

**Sources:** [backend/app/api/chapters.py:69-74](), [backend/app/utils/sse_response.py:208-210]()

---

## Frontend SSE Client Implementation

### SSEPostClient Class

Since standard browser `EventSource` only supports GET requests, the frontend implements `SSEPostClient` using the `fetch` API and `ReadableStream`.

**Key Methods:**
*   `connect()`: Initiates the fetch request and starts reading the stream. [frontend/src/utils/sseClient.ts:139-143]()
*   `handleMessage()`: Dispatches events based on the `type` field (progress, chunk, result, error, done). [frontend/src/utils/sseClient.ts:216-258]()

**Sources:** [frontend/src/utils/sseClient.ts:125-260]()

### UI Integration (Chapters.tsx)

The `Chapters` component uses these clients to manage chapter generation and batch operations.

```typescript
// frontend/src/pages/Chapters.tsx
// Single chapter generation progress
const [singleChapterProgress, setSingleChapterProgress] = useState(0);
const [singleChapterProgressMessage, setSingleChapterProgressMessage] = useState('');

// Batch generation status
const [batchProgress, setBatchProgress] = useState<{
  status: string;
  total: number;
  completed: number;
  current_chapter_number: number | null;
} | null>(null);
```

**Sources:** [frontend/src/pages/Chapters.tsx:96-113]()

---

## Complex Workflows

### Auto-Character and Organization Prediction

When generating outlines, the system can predict and automatically create missing characters or organizations. This uses specialized services:
*   `AutoCharacterService`: Generates character details based on plot context and project rules. [backend/app/services/auto_character_service.py:17-132]()
*   `AutoOrganizationService`: Generates organization details and member relationships. [backend/app/services/auto_organization_service.py:17-111]()

These services are often invoked within an SSE stream to provide immediate feedback as new entities are "discovered" by the AI.

### Batch Generation Progress

Batch operations (like generating 10 chapters at once) use a polling or SSE mechanism to track sub-tasks.
*   `BatchGenerateRequest`: Specifies count, style, and model. [backend/app/schemas/chapter.py:126-141]()
*   `BatchGenerateStatusResponse`: Tracks `total`, `completed`, and `current_retry_count`. [backend/app/schemas/chapter.py:151-166]()

**Sources:** [backend/app/schemas/chapter.py:126-166](), [backend/app/services/auto_character_service.py:17-50](), [backend/app/services/auto_organization_service.py:17-61]()

---

## Summary of Key Entities

| Code Entity | File Path | Role |
|:---|:---|:---|
| `SSEResponse` | `backend/app/utils/sse_response.py` | Low-level SSE string formatting |
| `WizardProgressTracker` | `backend/app/utils/sse_response.py` | High-level progress stage management |
| `SSEPostClient` | `frontend/src/utils/sseClient.ts` | Frontend fetch-based SSE consumer |
| `ChapterGenerateRequest` | `backend/app/schemas/chapter.py` | Schema for SSE generation inputs |
| `db_write_locks` | `backend/app/api/chapters.py` | Concurrency control for SQLite writes |

**Sources:** [backend/app/utils/sse_response.py:51](), [frontend/src/utils/sseClient.ts:125](), [backend/app/schemas/chapter.py:112](), [backend/app/api/chapters.py:65]()

---

# Page: API Reference

# API Reference

<details>
<summary>Relevant source files</summary>

The following files were used as context for generating this wiki page:

- [frontend/src/services/api.ts](frontend/src/services/api.ts)
- [frontend/src/types/index.ts](frontend/src/types/index.ts)

</details>



## Purpose and Scope

This document provides a complete reference for all REST and Server-Sent Events (SSE) endpoints in the MuMuAINovel backend API. It covers endpoint specifications, authentication requirements, request/response formats, and common patterns used throughout the API.

For detailed implementation patterns of specific features, see:
- Authentication implementation details: [User Authentication and Authorization](#7.3)
- SSE streaming implementation: [SSE Streaming Implementation](#7.4)
- AI provider integration: [AI Service Architecture](#5.1)
- Database session management: [Database Session Management](#7.2)

For detailed documentation of each endpoint category, see the child pages:
- [Wizard Stream APIs](#8.1) — Document `/wizard-stream` endpoints for world-building, character generation, and outline generation with SSE.
- [Outline APIs](#8.2) — Document outline CRUD endpoints, generation, expansion, character prediction, and reordering.
- [Chapter APIs](#8.3) — Document chapter CRUD endpoints, AI generation, batch generation, analysis, and regeneration.
- [Character and Relationship APIs](#8.4) — Document character CRUD endpoints, relationship management, organization APIs, and auto-character services.
- [Project APIs](#8.5) — Document project CRUD endpoints, export/import functionality, and project statistics.
- [Settings and Configuration APIs](#8.6) — Document settings endpoints, API key preset management, model discovery, and connection testing.
- [Inspiration APIs](#8.7) — Document inspiration mode endpoints for step-by-step AI-guided option generation.

---

## API Architecture Overview

The MuMuAINovel backend is built with FastAPI and exposes a RESTful API with additional SSE streaming endpoints for long-running AI generation operations. All API routes are organized under the `/api` prefix [frontend/src/services/api.ts:69-69]().

### Base URL Structure

```
http://localhost:8000/api/{resource}/{operation}
```

- **Base URL**: `http://localhost:8000` (configurable via environment variables)
- **API Prefix**: `/api` [frontend/src/services/api.ts:69-69]()
- **Resources**: `auth`, `projects`, `chapters`, `outlines`, `characters`, `settings`, `wizard-stream`, `inspiration`

### Route Organization

The frontend interacts with these routes through specialized API objects defined in `frontend/src/services/api.ts`:

| API Object | Resource Path | Primary Responsibility |
|--------|-----------|----------------------|
| `authApi` | `/auth` | Login (Local/Email/LinuxDO), session management, password status [frontend/src/services/api.ts:152-198]() |
| `projectApi` | `/projects` | Project CRUD, statistics, export/import [frontend/src/services/api.ts:323-388]() |
| `chapterApi` | `/chapters` | Chapter CRUD, AI generation, batch analysis [frontend/src/services/api.ts:517-640]() |
| `outlineApi` | `/outlines` | Outline CRUD, expansion, reordering, character prediction [frontend/src/services/api.ts:430-515]() |
| `characterApi` | `/characters` | Character/organization CRUD, relationships [frontend/src/services/api.ts:390-428]() |
| `settingsApi` | `/settings` | User AI provider configuration and model discovery [frontend/src/services/api.ts:221-252]() |
| `wizardApi` | `/wizard-stream` | SSE endpoints for structured project creation [frontend/src/services/api.ts:286-321]() |
| `inspirationApi` | `/inspiration` | Step-by-step conversational AI guidance [frontend/src/services/api.ts:654-672]() |

**Sources**: [frontend/src/services/api.ts:152-672](), [frontend/src/types/index.ts]()

---

## API Route Structure Diagram

This diagram maps the logical API resources to their respective frontend service implementations and backend router logic.

```mermaid
graph TB
    subgraph "Frontend API Layer (api.ts)"
        Axios["axios instance (baseURL: /api)"]
        
        subgraph "Service Objects"
            AuthSvc["authApi"]
            ProjSvc["projectApi"]
            ChapSvc["chapterApi"]
            OutSvc["outlineApi"]
            CharSvc["characterApi"]
            SetSvc["settingsApi"]
            WizSvc["wizardApi (SSE)"]
            InspSvc["inspirationApi"]
        end
    end
    
    subgraph "Backend FastAPI Routers"
        AuthRouter["/auth"]
        ProjRouter["/projects"]
        ChapRouter["/chapters"]
        OutRouter["/outlines"]
        CharRouter["/characters"]
        SetRouter["/settings"]
        WizRouter["/wizard-stream"]
        InspRouter["/inspiration"]
    end
    
    Axios --> AuthSvc & ProjSvc & ChapSvc & OutSvc & CharSvc & SetSvc & WizSvc & InspSvc
    
    AuthSvc --> AuthRouter
    ProjSvc --> ProjRouter
    ChapSvc --> ChapRouter
    OutSvc --> OutRouter
    CharSvc --> CharRouter
    SetSvc --> SetRouter
    WizSvc --> WizRouter
    InspSvc --> InspRouter
```

**Sources**: [frontend/src/services/api.ts:68-75](), [frontend/src/services/api.ts:152-672]()

---

## Authentication and Authorization

### Authentication Methods

MuMuAINovel supports multiple authentication methods [frontend/src/services/api.ts:153-158]():

1. **Local Account Login**: Traditional username/password [frontend/src/services/api.ts:160-161]().
2. **Email Login/Register**: Verification code based auth with SMTP support [frontend/src/services/api.ts:166-177]().
3. **LinuxDO OAuth**: Third-party OAuth2 integration [frontend/src/services/api.ts:178-178]().

### Session Management

- **Persistence**: Sessions are managed via cookies (`withCredentials: true`) [frontend/src/services/api.ts:74-74]().
- **Interceptors**: The API client automatically handles 401 Unauthorized errors by redirecting to `/login` [frontend/src/services/api.ts:101-117]().
- **Data Isolation**: Each user session is associated with a unique `user_id`, which the backend uses to route requests to the correct user-specific SQLite database [frontend/src/types/index.ts:74-76]().

---

## Common Patterns

### Request/Response Format

The system uses standard HTTP status codes to communicate request results [frontend/src/services/api.ts:97-138]():

| Status Code | Meaning | Frontend Handling |
|-------------|---------|-------------------|
| 200/201 | Success | Returns `response.data` [frontend/src/services/api.ts:87-89]() |
| 401 | Unauthorized | Redirects to `/login` [frontend/src/services/api.ts:113-115]() |
| 422 | Validation Error | Logs validation details and shows error message [frontend/src/services/api.ts:124-129]() |
| 500 | Server Error | Shows "服务器内部错误" (Internal Server Error) [frontend/src/services/api.ts:130-132]() |

### SSE Streaming Pattern

For long-running AI operations (like chapter generation or world-building), the API uses Server-Sent Events (SSE) via the `ssePost` utility [frontend/src/services/api.ts:3-3]().

```mermaid
sequenceDiagram
    participant UI as Frontend Component
    participant SSE as sseClient (ssePost)
    participant API as Backend SSE Endpoint
    
    UI->>SSE: Call ssePost(url, data, options)
    SSE->>API: POST request with streaming headers
    
    loop Stream Events
        API-->>SSE: event: progress (text chunk)
        SSE->>UI: onMessage(chunk)
    end
    
    API-->>SSE: event: result (JSON data)
    SSE->>UI: onSuccess(parsedData)
    
    API-->>SSE: event: error
    SSE->>UI: onError(error)
```

**Sources**: [frontend/src/utils/sseClient.ts](), [frontend/src/services/api.ts:286-321]()

---

## Data Model Reference

The API operates on several core entities defined in `frontend/src/types/index.ts`.

| Entity | Description | Key Fields |
|--------|-------------|------------|
| `Project` | The root container for a story [frontend/src/types/index.ts:155-181](). | `id`, `title`, `outline_mode`, `wizard_status` |
| `Outline` | Structural components (chapters/arcs) [frontend/src/types/index.ts:248-258](). | `id`, `project_id`, `content`, `order_index` |
| `Chapter` | The actual narrative text [frontend/src/types/index.ts:316-333](). | `id`, `project_id`, `content`, `chapter_number` |
| `Character` | Entities within the story [frontend/src/types/index.ts:276-302](). | `id`, `name`, `is_organization`, `role_type` |
| `Settings` | AI provider and model configurations [frontend/src/types/index.ts:74-92](). | `api_provider`, `api_key`, `llm_model` |

**Sources**: [frontend/src/types/index.ts]()

---

## Summary of Endpoint Groups

For detailed documentation, please refer to the specific child pages:

- **[Wizard Stream APIs](#8.1)**: Handles `world-building`, `characters`, and `outline` generation steps using SSE.
- **[Outline APIs](#8.2)**: Manages story structure, including expansion from "one-to-one" to "one-to-many" modes.
- **[Chapter APIs](#8.3)**: Handles narrative content, including batch analysis and smart regeneration.
- **[Character and Relationship APIs](#8.4)**: Manages the "Dramatis Personae" and organizational hierarchies.
- **[Project APIs](#8.5)**: High-level management, including full project export and import.
- **[Settings and Configuration APIs](#8.6)**: Manages LLM provider keys, writing styles, and MCP plugins.
- **[Inspiration APIs](#8.7)**: Provides a conversational interface for generating creative options.

**Sources**: [frontend/src/services/api.ts:152-672]()

---

# Page: Wizard Stream APIs

# Wizard Stream APIs

<details>
<summary>Relevant source files</summary>

The following files were used as context for generating this wiki page:

- [backend/app/api/wizard_stream.py](backend/app/api/wizard_stream.py)
- [backend/app/services/prompt_service.py](backend/app/services/prompt_service.py)

</details>



## Purpose and Scope

The Wizard Stream APIs provide Server-Sent Events (SSE) streaming endpoints for the project creation wizard workflow. These APIs handle long-running AI content generation operations that would otherwise timeout with standard HTTP responses. Each wizard step (world building, character creation, outline generation) uses streaming to provide real-time progress updates, heartbeats, and intermediate results to the frontend.

For the overall wizard workflow and UI components, see [Project Creation Wizard](). For the AI service integration details, see [AI Service Architecture](). For SSE implementation patterns on the backend, see [SSE Streaming Implementation]().

**Sources:** [backend/app/api/wizard_stream.py:1-26]()

---

## API Endpoint Overview

All endpoints in this module are mounted under the `/wizard-stream` prefix and use SSE for streaming responses via async generators.

| Endpoint | Method | Purpose | Generator Function |
|----------|--------|---------|-------------------|
| `/wizard-stream/world-building` | POST | Generate world setting from basic project info | `world_building_generator()` |
| `/wizard-stream/characters` | POST | Batch generate characters and organizations | `characters_generator()` |
| `/wizard-stream/outline` | POST | Generate 5-chapter opening outline | `outline_generator()` |
| `/wizard-stream/world-building/{project_id}` | POST | Update world building fields manually | `update_world_building_generator()` |
| `/wizard-stream/world-building/{project_id}/regenerate` | POST | Regenerate world building via AI | `regenerate_world_building_generator()` |
| `/wizard-stream/cleanup/{project_id}` | POST | Delete project and all related wizard data | `cleanup_wizard_data_generator()` |

**Sources:** [backend/app/api/wizard_stream.py:25](), [backend/app/api/wizard_stream.py:191-201](), [backend/app/api/wizard_stream.py:718-727](), [backend/app/api/wizard_stream.py:984-993](), [backend/app/api/wizard_stream.py:1058-1074](), [backend/app/api/wizard_stream.py:1197-1212](), [backend/app/api/wizard_stream.py:1297-1306]()

---

## Generator Pattern and SSE Lifecycle

All wizard stream endpoints follow a consistent async generator pattern that yields SSE-formatted messages throughout the operation lifecycle.

### Wizard Stream Generator Lifecycle

```mermaid
sequenceDiagram
    participant Client as "Frontend EventSource"
    participant Router as "FastAPI Route Handler"
    participant Generator as "Async Generator Function"
    participant Tracker as "WizardProgressTracker"
    participant AIService as "AIService"
    participant DB as "AsyncSession"
    
    Client->>Router: POST /wizard-stream/* (request body)
    Router->>Generator: Call generator(data, db, ai_service)
    Router->>Client: Return SSEResponse (StreamingResponse)
    
    Note over Generator: Start transaction
    Generator->>Tracker: tracker.start()
    Tracker-->>Client: event: start
    
    Generator->>AIService: generate_text_stream(prompt)
    
    loop AI Streaming
        AIService-->>Generator: yield chunk
        Generator->>Tracker: tracker.generating_chunk(chunk)
        Tracker-->>Client: event: chunk (content)
        Generator->>Tracker: tracker.generating(progress_info)
        Tracker-->>Client: event: progress (%)
        Note over Generator: Every 20 chunks
        Generator->>Tracker: tracker.heartbeat()
        Tracker-->>Client: event: heartbeat
    end
    
    Generator->>Generator: Parse & Clean JSON
    Generator->>DB: Create/Update models
    Generator->>DB: commit()
    
    Generator->>Tracker: tracker.result(data)
    Tracker-->>Client: event: result (final data)
    Generator->>Tracker: tracker.done()
    Tracker-->>Client: event: done (end stream)
    
    Note over Generator: Close generator
    Router-->>Client: Close SSE connection
```

**Sources:** [backend/app/api/wizard_stream.py:29-189](), [backend/app/utils/sse_response.py:1-120]()

### Progress Tracking Helper

The `WizardProgressTracker` class from `app.utils.sse_response` provides standardized message formatting for the wizard workflow:

| Method | Event Type | Purpose |
|--------|-----------|---------|
| `start()` | `start` | Initialize the wizard step stream |
| `preparing(msg)` | `preparing` | Report pre-generation tasks (e.g., loading prompts) |
| `generating(...)` | `generating` | Report generation stats (chars, retries, total) |
| `generating_chunk(text)` | `chunk` | Send AI-generated text fragment |
| `parsing(msg)` | `parsing` | Report JSON parsing and data cleaning phase |
| `saving(msg)` | `saving` | Report database persistence phase |
| `result(data)` | `result` | Send final structured result data |
| `done()` | `done` | Signal stream completion |

**Sources:** [backend/app/api/wizard_stream.py:22](), [backend/app/api/wizard_stream.py:38](), [backend/app/api/wizard_stream.py:42](), [backend/app/api/wizard_stream.py:113](), [backend/app/api/wizard_stream.py:149]()

---

## World Building Generation

The world building generator creates the foundational setting for a new project based on metadata like title, theme, and genre.

### Endpoint: POST /wizard-stream/world-building

**Request Body:**
```typescript
{
  title: string;
  description: string;
  theme: string;
  genre: string;
  narrative_perspective?: string;
  target_words?: number;
  chapter_count?: number;
  character_count?: number;
  outline_mode?: "one-to-one" | "one-to-many";
  provider?: string;
  model?: string;
}
```

**Sources:** [backend/app/api/wizard_stream.py:44-56]()

### World Building Data Flow

```mermaid
graph TB
    Request["POST /world-building<br/>{title, theme, genre}"]
    Generator["world_building_generator()"]
    PromptService["PromptService.get_template('WORLD_BUILDING')"]
    AIService["user_ai_service.<br/>generate_text_stream()"]
    Parser["AIService._clean_json_response()"]
    ProjectModel["Project Model<br/>(create new)"]
    StyleModel["ProjectDefaultStyle<br/>(set first preset)"]
    Response["SSE: result event<br/>{project_id, world_data}"]
    
    Request-->Generator
    Generator-->PromptService
    PromptService-->AIService
    AIService-->Parser
    Parser-->ProjectModel
    ProjectModel-->StyleModel
    StyleModel-->Response
```

**Sources:** [backend/app/api/wizard_stream.py:29-189](), [backend/app/services/prompt_service.py:77-191]()

### Implementation Details

1. **Validation**: Checks required fields (title, description, theme, genre) [backend/app/api/wizard_stream.py:59-61]().
2. **Prompt Generation**: Uses the RTCO framework template `WORLD_BUILDING` [backend/app/services/prompt_service.py:78-191]().
3. **AI Streaming**: Implements a retry mechanism (`MAX_WORLD_RETRIES = 3`) for empty or invalid AI responses [backend/app/api/wizard_stream.py:80-146]().
4. **JSON Cleaning**: Uses `user_ai_service._clean_json_response()` to handle markdown and formatting issues [backend/app/api/wizard_stream.py:156]().
5. **Project Creation**: Stores the four core world fields: `time_period`, `location`, `atmosphere`, and `rules` [backend/app/api/wizard_stream.py:171-174]().
6. **Style Assignment**: Automatically assigns the first available global `WritingStyle` as the project's default [backend/app/api/wizard_stream.py:139-158]().

---

## Character Batch Generation

The character generator creates multiple character and organization entities in batches (default size 3) to ensure quality and avoid context window limitations.

### Endpoint: POST /wizard-stream/characters

**Request Body:**
```typescript
{
  project_id: string;
  count?: number;           // Total entities to generate
  world_context?: {
    time_period: string;
    location: string;
    atmosphere: string;
    rules: string;
  };
  requirements?: string;
}
```

**Sources:** [backend/app/api/wizard_stream.py:204-222]()

### Character Generation Architecture

```mermaid
graph TB
    subgraph "Batch Processing (BATCH_SIZE=3)"
        BatchLoop["For each batch"]
        RetryLoop["Retry Loop (3 times)"]
        PromptGen["PromptService.format_prompt(<br/>'CHARACTERS_BATCH_GENERATION')"]
        AIStream["AIService.generate_text_stream()"]
        CleanJSON["AIService._clean_json_response()"]
    end
    
    subgraph "Data Cleaning & Linking"
        BuildEntitySet["Collect all valid names"]
        CleanRels["Filter hallucinated relationships"]
        CleanOrgMems["Filter hallucinated organizations"]
    end
    
    subgraph "Database Persistence"
        CreateChars["Phase 1: Character records"]
        CreateOrgs["Phase 2: Organization records"]
        CreateRels["Phase 3: CharacterRelationship"]
        CreateMembers["Phase 4: OrganizationMember"]
    end
    
    BatchLoop-->RetryLoop
    RetryLoop-->PromptGen
    PromptGen-->AIStream
    AIStream-->CleanJSON
    CleanJSON-->BuildEntitySet
    BuildEntitySet-->CleanRels
    CleanRels-->CleanOrgMems
    CleanOrgMems-->CreateChars
    CreateChars-->CreateOrgs
    CreateOrgs-->CreateRels
    CreateRels-->CreateMembers
```

**Sources:** [backend/app/api/wizard_stream.py:236-716](), [backend/app/services/prompt_service.py:193-317]()

### Hallucination Cleaning Logic

To prevent foreign key violations, the generator implements strict cleaning:
1. **Valid Entity Set**: A set of all names generated in the current session is maintained [backend/app/api/wizard_stream.py:403-412]().
2. **Relationship Filtering**: The `relationships_array` is filtered to only include targets present in the valid entity set [backend/app/api/wizard_stream.py:418-428]().
3. **Membership Filtering**: `organization_memberships` are filtered to ensure the organization exists in the generated batch [backend/app/api/wizard_stream.py:431-441]().

---

## Outline Generation

The outline generator creates a fixed 5-chapter opening for the project, establishing the initial plot and conflict.

### Endpoint: POST /wizard-stream/outline

**Behavior:**
- Generates 5 `Outline` records with `order_index` 1-5 [backend/app/api/wizard_stream.py:925-942]().
- Creates 5 corresponding `Chapter` records with `status="draft"` [backend/app/api/wizard_stream.py:934-941]().
- Uses the `OUTLINE_CREATE` template which focuses on "opening chapters" rather than a full story arc [backend/app/services/prompt_service.py:320-334]().
- Updates the project `wizard_status` to `"completed"` upon success [backend/app/api/wizard_stream.py:948]().

**Sources:** [backend/app/api/wizard_stream.py:730-982](), [backend/app/services/prompt_service.py:320-385]()

---

## Transaction and Error Management

### Transaction Rollback Pattern

All wizard stream generators implement a manual transaction management pattern to handle the unique requirements of long-running SSE connections.

```python
db_committed = False
try:
    # ... logic ...
    await db.commit()
    db_committed = True
except Exception as e:
    if not db_committed:
        await db.rollback()
    yield await tracker.error(str(e))
```

**Sources:** [backend/app/api/wizard_stream.py:35-40](), [backend/app/api/wizard_stream.py:176-188]()

### Key Model Integrations

| Model | Creation Step | Purpose |
|-------|---------------|---------|
| `Project` | World Building | Core project container [backend/app/models/project.py]() |
| `Character` | Characters | Individual entities [backend/app/models/character.py]() |
| `Organization` | Characters | Groups/Factions [backend/app/models/relationship.py]() |
| `CharacterRelationship` | Characters | Social/Conflict links [backend/app/models/relationship.py]() |
| `Outline` | Outline | Chapter plot summaries [backend/app/models/outline.py]() |
| `Chapter` | Outline | Actual writing containers [backend/app/models/chapter.py]() |

**Sources:** [backend/app/api/wizard_stream.py:10-17]()

---

# Page: Outline APIs

# Outline APIs

<details>
<summary>Relevant source files</summary>

The following files were used as context for generating this wiki page:

- [backend/app/api/outlines.py](backend/app/api/outlines.py)
- [backend/app/schemas/outline.py](backend/app/schemas/outline.py)
- [frontend/src/pages/Outline.tsx](frontend/src/pages/Outline.tsx)
- [frontend/src/services/api.ts](frontend/src/services/api.ts)
- [frontend/src/types/index.ts](frontend/src/types/index.ts)

</details>



This document provides comprehensive reference documentation for all outline-related API endpoints in the MuMuAINovel system. Outlines represent high-level story structures that can be created manually, generated by AI, or expanded into detailed chapters.

**Scope**: This page covers the `/api/outlines` router including CRUD operations, AI generation (both streaming and non-streaming), outline expansion, character prediction, and reordering. For chapter-related endpoints, see [Chapter APIs](8.3). For the AI generation wizard, see [Wizard Stream APIs](8.1).

---

## Endpoint Overview

The outline API router is implemented in [backend/app/api/outlines.py:39-41]() and provides the following categories of endpoints:

| Endpoint | Method | Purpose | Streaming |
|----------|--------|---------|-----------|
| `/outlines` | POST | Create a single outline manually | No |
| `/outlines` | GET | List all outlines for a project | No |
| `/outlines/project/{project_id}` | GET | List outlines (path parameter variant) | No |
| `/outlines/{outline_id}` | GET | Get outline details | No |
| `/outlines/{outline_id}` | PUT | Update outline | No |
| `/outlines/{outline_id}` | DELETE | Delete outline and associated chapters | No |
| `/outlines/generate-stream` | POST | AI generate/continue outlines | Yes (SSE) |
| `/outlines/predict-characters` | POST | Predict characters needed for continuation | No |
| `/outlines/{outline_id}/expand-stream` | POST | Expand single outline to multiple chapters | Yes (SSE) |
| `/outlines/batch-expand-stream` | POST | Batch expand multiple outlines | Yes (SSE) |
| `/outlines/create-chapters-from-plans` | POST | Create chapters from generated plans | No |

**Sources**: [backend/app/api/outlines.py:39-41](), [backend/app/api/outlines.py:58-59](), [backend/app/api/outlines.py:94-95](), [backend/app/api/outlines.py:193-194](), [backend/app/api/outlines.py:262-263]()

---

## Data Models

### Outline Schema

The `Outline` model represents a high-level story structure:

```python
class Outline(Base):
    __tablename__ = "outlines"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    project_id = Column(String, ForeignKey("projects.id", ondelete="CASCADE"), nullable=False)
    title = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    structure = Column(Text, nullable=True) # JSON string with extended metadata
    order_index = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
```

The `order_index` field determines the sequential position. In **one-to-one mode**, this corresponds to the chapter number. In **one-to-many mode**, this represents the "volume" or "arc" number.

**Sources**: [backend/app/models/outline.py:10-23](), [backend/app/api/outlines.py:75-87]()

### Request/Response Schemas

Key schemas defined in [backend/app/schemas/outline.py:7-147]():

| Schema | Purpose |
|--------|---------|
| `OutlineCreate` | Create outline request [backend/app/schemas/outline.py:13-20]() |
| `OutlineUpdate` | Update outline request [backend/app/schemas/outline.py:22-28]() |
| `OutlineResponse` | Single outline response with `has_chapters` [backend/app/schemas/outline.py:30-42]() |
| `OutlineGenerateRequest` | AI generation parameters including `mode` [backend/app/schemas/outline.py:45-65]() |
| `OutlineExpansionRequest` | Strategy and target count for expansion [backend/app/schemas/outline.py:95-103]() |
| `ChapterPlanItem` | Structure for a single expanded chapter plan [backend/app/schemas/outline.py:81-93]() |

**Sources**: [backend/app/schemas/outline.py:7-147]()

---

## CRUD Operations

### Create Outline

**Endpoint**: `POST /outlines`

**Behavior**:
- Creates outline record in database.
- **One-to-one mode**: Automatically creates a corresponding `Chapter` with `chapter_number = order_index` and `sub_index = 1` [backend/app/api/outlines.py:75-87]().
- **One-to-many mode**: Only creates the outline record; user must use expansion APIs to create chapters.

**Sources**: [backend/app/api/outlines.py:58-91]()

### Get Outlines (Optimized)

**Endpoint**: `GET /outlines?project_id={id}`

**Implementation Detail**:
The backend performs a batch query on the `chapters` table to determine which outlines have already been expanded, attaching a dynamic `has_chapters` boolean to each item to prevent N+1 frontend requests [backend/app/api/outlines.py:119-137](). It also parses the `structure` JSON field to populate `title` and `content` if they are missing or stored within the structure [backend/app/api/outlines.py:139-152]().

**Sources**: [backend/app/api/outlines.py:94-158]()

### Update and Delete

- **Update**: `PUT /outlines/{outline_id}`. Syncs changes to the `structure` field and, in one-to-one mode, updates the associated chapter title [backend/app/api/outlines.py:193-256]().
- **Delete**: `DELETE /outlines/{outline_id}`. Deletes the outline and its associated chapters. It automatically reorders subsequent outlines by decrementing their `order_index` [backend/app/api/outlines.py:262-362]().

---

## AI Generation and Continuation

### Generation Modes

The `/outlines/generate-stream` endpoint (SSE) supports:
- `new`: Deletes existing outlines and generates a fresh set based on project theme [backend/app/schemas/outline.py:60]().
- `continue`: Appends new outlines to the existing story, using smart context building to maintain consistency [backend/app/schemas/outline.py:60]().

### Smart Context Building
To handle long stories, `_build_smart_outline_context` builds a prompt containing:
1. **Skeleton**: Titles of every 50th outline for long-term structure [backend/app/api/outlines.py:679-688]().
2. **Recent Summaries**: Titles and snippets of the last 20 outlines [backend/app/api/outlines.py:692-702]().
3. **Immediate Context**: Full content of the last 2 outlines [backend/app/api/outlines.py:706-714]().

**Sources**: [backend/app/api/outlines.py:643-726]()

### Character Prediction and Confirmation
When continuing a story, the AI can predict if new characters are needed.
- If `enable_auto_characters` is true and new characters are detected, the API sends a `character_confirmation_required` SSE event [backend/app/api/outlines.py:1649-1658]().
- The frontend `Outline.tsx` intercepts this and shows a modal for the user to approve or edit the new characters before proceeding [frontend/src/pages/Outline.tsx:1717-1854]().

---

## Outline Expansion (One-to-Many)

This system allows a single outline (an arc) to be broken down into detailed chapter plans.

### Expansion Logic Flow

```mermaid
graph TD
    A["OutlineExpansionRequest"] --> B["PlotExpansionService.analyze_outline_for_chapters"]
    B --> C["Generate ChapterPlanItems (JSON)"]
    C --> D["SSE Stream to Frontend"]
    D --> E["User Reviews Plans in ExpansionPlanEditor"]
    E --> F["POST /create-chapters-from-plans"]
    F --> G["Database: Create Chapter records"]
```

**Key Entities**:
- `PlotExpansionService`: Orchestrates the AI calls to split plot points into scenes and chapters [backend/app/api/outlines.py:32]().
- `ChapterPlanItem`: Contains `plot_summary`, `key_events`, `character_focus`, and `scenes` [backend/app/schemas/outline.py:81-93]().

**Sources**: [backend/app/api/outlines.py:2013-2162](), [backend/app/schemas/outline.py:81-113]()

---

## Code Mapping: Natural Language to Code Entity

This diagram bridges user actions in the UI to specific backend logic and data models.

```mermaid
graph LR
    subgraph "User Action Space"
        UA1["'Generate Outlines' Button"]
        UA2["'Expand' Icon on Card"]
        UA3["Drag and Drop Reorder"]
    end

    subgraph "Code Entity Space"
        direction TB
        CE1["SSEPostClient (frontend)"]
        CE2["outline_router.generate_stream (backend)"]
        CE3["PlotExpansionService (backend)"]
        CE4["outline_router.reorder_outlines (backend)"]
        CE5["Outline (SQLAlchemy Model)"]
        CE6["ChapterPlanItem (Pydantic)"]
    end

    UA1 -- "calls" --> CE1
    CE1 -- "POST /generate-stream" --> CE2
    UA2 -- "triggers" --> CE3
    CE3 -- "returns" --> CE6
    UA3 -- "PUT /reorder" --> CE4
    CE2 -- "writes to" --> CE5
    CE4 -- "updates" --> CE5
```

**Sources**: [frontend/src/pages/Outline.tsx:210-308](), [backend/app/api/outlines.py:1944-2010](), [backend/app/api/outlines.py:2013-2162](), [backend/app/models/outline.py:10-23]()

---

## Reordering Logic

Outlines can be reordered via `PUT /outlines/reorder`. The backend takes a list of IDs in the desired order and updates the `order_index` for each. In **one-to-one mode**, it also updates the `chapter_number` of the corresponding chapters to ensure the narrative sequence remains synchronized [backend/app/api/outlines.py:1137-1202]().

```mermaid
sequenceDiagram
    participant FE as Frontend (Outline.tsx)
    participant BE as Backend (outlines.py)
    participant DB as PostgreSQL (outlines table)

    FE->>BE: PUT /outlines/reorder {outline_ids: [id3, id1, id2]}
    BE->>DB: SELECT * FROM outlines WHERE id IN [...]
    loop For each ID in new order
        BE->>DB: UPDATE outline SET order_index = current_loop_index
        opt one-to-one mode
            BE->>DB: UPDATE chapter SET chapter_number = current_loop_index WHERE ...
        end
    end
    BE->>DB: commit()
    BE-->>FE: 200 OK
```

**Sources**: [backend/app/api/outlines.py:1137-1202](), [frontend/src/services/api.ts:250-255]()

---

# Page: Chapter APIs

# Chapter APIs

<details>
<summary>Relevant source files</summary>

The following files were used as context for generating this wiki page:

- [backend/app/api/chapters.py](backend/app/api/chapters.py)
- [backend/app/schemas/chapter.py](backend/app/schemas/chapter.py)
- [frontend/src/components/ExpansionPlanEditor.tsx](frontend/src/components/ExpansionPlanEditor.tsx)
- [frontend/src/pages/Chapters.tsx](frontend/src/pages/Chapters.tsx)
- [frontend/src/services/api.ts](frontend/src/services/api.ts)
- [frontend/src/store/hooks.ts](frontend/src/store/hooks.ts)
- [frontend/src/types/index.ts](frontend/src/types/index.ts)

</details>



## Purpose and Scope

This page documents the REST API endpoints defined in [backend/app/api/chapters.py:1-62]() for managing chapters in novel projects. These endpoints handle CRUD operations, AI-powered chapter generation with streaming support, batch generation tasks, and the automated plot analysis system.

The chapter system integrates deeply with the `PlotAnalyzer` for memory extraction [backend/app/api/chapters.py:54](), the `ChapterRegenerator` for partial rewriting [backend/app/api/chapters.py:57](), and various context builders for one-to-one or one-to-many outline modes [backend/app/api/chapters.py:14-17]().

**Sources:** [backend/app/api/chapters.py:1-63]()

---

## API Router Configuration

The chapter API is mounted at the `/chapters` prefix. It utilizes a per-user global database write lock `db_write_locks` to protect SQLite concurrent write operations during intensive tasks like batch generation.

```python
router = APIRouter(prefix="/chapters", tags=["章节管理"])
db_write_locks: dict[str, Lock] = {}
```

**Sources:** [backend/app/api/chapters.py:62-74]()

---

## Endpoint Overview

### API Endpoints Summary

| HTTP Method | Endpoint Path | Purpose | Response Model |
|------------|---------------|---------|----------------|
| POST | `/chapters` | Create new chapter | `ChapterResponse` |
| GET | `/chapters/project/{project_id}` | List chapters with outline info | `ChapterListResponse` |
| GET | `/chapters/{chapter_id}` | Get single chapter details | `ChapterResponse` |
| PUT | `/chapters/{chapter_id}` | Update content/expansion plan | `ChapterResponse` |
| DELETE | `/chapters/{chapter_id}` | Delete chapter & update word count | `{"message": str}` |
| POST | `/chapters/{chapter_id}/generate-stream` | AI generate chapter (SSE) | `StreamingResponse` |
| POST | `/chapters/batch-generate` | Start batch generation task | `BatchGenerateResponse` |
| POST | `/chapters/{chapter_id}/analyze` | Trigger plot analysis | `AnalysisTaskStatusResponse` |
| POST | `/chapters/{chapter_id}/regenerate-partial` | Partial text rewriting (SSE) | `StreamingResponse` |

**Sources:** [backend/app/api/chapters.py:77-172](), [backend/app/api/chapters.py:251-1100]()

---

## CRUD Operations

### Create Chapter

**Endpoint:** `POST /chapters`

Creates a new chapter record. It automatically calculates `word_count` and increments the project's `current_words` counter [backend/app/api/chapters.py:89-98]().

**Sources:** [backend/app/api/chapters.py:77-102]()

### List Project Chapters

**Endpoint:** `GET /chapters/project/{project_id}`

Retrieves all chapters ordered by `chapter_number`. This endpoint performs a join-like operation by mapping `Outline` titles and order indices to the chapter objects [backend/app/api/chapters.py:131-166]().

**Sources:** [backend/app/api/chapters.py:105-169]()

### Update Chapter and Expansion Plan

**Endpoint:** `PUT /chapters/{chapter_id}`

Updates chapter metadata or content. If the `content` is updated, it recalculates the word count delta and updates the `Project.current_words` accordingly [backend/app/api/chapters.py:270-282](). This endpoint also handles updating the `expansion_plan` JSON field [backend/app/api/chapters.py:285-288]().

**Sources:** [backend/app/api/chapters.py:251-305]()

---

## AI Generation Architecture

### Diagram: Chapter Generation System Mapping

This diagram associates the natural language concepts of "Chapter Writing" with the specific backend service entities and frontend components.

```mermaid
graph LR
    subgraph "Frontend Space (React)"
        UI["Chapters.tsx"]
        Editor["ExpansionPlanEditor.tsx"]
        Reader["ChapterReader.tsx"]
    end

    subgraph "Code Entity Space (FastAPI/Services)"
        API["api/chapters.py"]
        Ctx1["OneToOneContextBuilder"]
        Ctx2["OneToManyContextBuilder"]
        AI["AIService"]
        Regen["ChapterRegenerator"]
    end

    subgraph "Data Space (SQL/Chroma)"
        DB[("SQLite: Chapter Table")]
        Mem[("ChromaDB: StoryMemory")]
    end

    UI -- "POST /generate-stream" --> API
    Editor -- "PUT /chapters/{id}/plan" --> API
    API -- "build_context()" --> Ctx2
    Ctx2 -- "query_memory()" --> Mem
    API -- "stream_text()" --> AI
    AI -- "UPDATE" --> DB
```

**Sources:** [backend/app/api/chapters.py:14-17](), [frontend/src/pages/Chapters.tsx:48-115](), [frontend/src/components/ExpansionPlanEditor.tsx:18-25]()

---

## Sequential Generation and Context

The system utilizes `OneToManyContextBuilder` or `OneToOneContextBuilder` to assemble the prompt.

### Context Strategy

The context building process [backend/app/api/chapters.py:550-620]() involves:
1.  **Project Info:** Theme, genre, and world-building rules.
2.  **Character Profiles:** Detailed traits and relationships [backend/app/api/chapters.py:568-575]().
3.  **Outline Context:** The specific plot points for the current chapter.
4.  **Story Memory:** Semantic retrieval of past events from `ChromaDB` via `memory_service` [backend/app/api/chapters.py:55]().
5.  **Expansion Plan:** If the chapter has a detailed plan (scenes, events), it is prioritized in the prompt [backend/app/schemas/chapter.py:175-185]().

**Sources:** [backend/app/api/chapters.py:520-650](), [backend/app/services/chapter_context_service.py]()

---

## Plot Analysis System

Every generated chapter can be analyzed to update the "Story Memory."

### Analysis Workflow

1.  **Trigger:** User clicks "Analyze" or it's triggered automatically after generation.
2.  **Task Creation:** An `AnalysisTask` is created in the DB with status `pending` [backend/app/api/chapters.py:1225-1235]().
3.  **Background Processing:** `PlotAnalyzer.analyze_chapter` is called via `BackgroundTasks` [backend/app/api/chapters.py:1247]().
4.  **Memory Extraction:** The analyzer extracts key plot points, character status changes, and foreshadowing.
5.  **Storage:** Data is saved to `PlotAnalysis` (SQL) and `StoryMemory` (Vector DB) [backend/app/api/chapters.py:27]().

**Sources:** [backend/app/api/chapters.py:1210-1255](), [backend/app/services/plot_analyzer.py]()

---

## Batch Generation

The batch generation system allows generating up to 20 chapters sequentially.

### Implementation Logic

```mermaid
flowchart TD
    Start["POST /batch-generate"] --> Lock["Acquire db_write_lock"]
    Lock --> Task["Create BatchGenerationTask (SQL)"]
    Task --> Loop["For each chapter in range"]
    Loop --> Gen["Generate content via AIService"]
    Gen --> Save["Save Chapter & Update Project Word Count"]
    Save --> Analyze["Optional: Trigger Background Analysis"]
    Analyze --> Next{"More chapters?"}
    Next -->|Yes| Loop
    Next -->|No| Finish["Set task status = completed"]
    Finish --> Unlock["Release Lock"]
```

**Sources:** [backend/app/api/chapters.py:1360-1450](), [backend/app/schemas/chapter.py:126-142]()

---

## Partial Regeneration

Users can highlight text in the frontend and request a partial rewrite.

**Endpoint:** `POST /chapters/{chapter_id}/regenerate-partial`

-   **Input:** Original text, selected text, and a rewrite instruction (e.g., "make it more dramatic") [backend/app/schemas/chapter.py:45-51]().
-   **Service:** `ChapterRegenerator` processes the request using the surrounding text as context to maintain stylistic consistency [backend/app/api/chapters.py:57]().
-   **Streaming:** Returns an SSE stream of the new text segment [backend/app/api/chapters.py:1650-1700]().

**Sources:** [backend/app/api/chapters.py:1634-1710](), [frontend/src/pages/Chapters.tsx:88-95]()

---

## Frontend Integration

The `Chapters.tsx` page manages the UI for these APIs.

### Key Components

-   **SSEProgressModal:** Displays real-time progress for batch generation or long single-chapter tasks [frontend/src/pages/Chapters.tsx:12]().
-   **ExpansionPlanEditor:** A modal for editing the `expansion_plan` JSON structure before generation [frontend/src/components/ExpansionPlanEditor.tsx:18-25]().
-   **useChapterSync:** A custom hook that wraps `chapterApi` calls and synchronizes the local Zustand store [frontend/src/store/hooks.ts:228-255]().

**Sources:** [frontend/src/pages/Chapters.tsx:1-15](), [frontend/src/store/hooks.ts:228-260]()

---

# Page: Character and Relationship APIs

# Character and Relationship APIs

<details>
<summary>Relevant source files</summary>

The following files were used as context for generating this wiki page:

- [backend/app/api/characters.py](backend/app/api/characters.py)
- [backend/app/api/organizations.py](backend/app/api/organizations.py)
- [backend/app/api/relationships.py](backend/app/api/relationships.py)
- [backend/app/schemas/character.py](backend/app/schemas/character.py)
- [frontend/pnpm-lock.yaml](frontend/pnpm-lock.yaml)
- [frontend/src/pages/Characters.tsx](frontend/src/pages/Characters.tsx)
- [frontend/src/pages/Organizations.tsx](frontend/src/pages/Organizations.tsx)
- [frontend/src/pages/RelationshipGraph.tsx](frontend/src/pages/RelationshipGraph.tsx)
- [frontend/src/pages/Relationships.tsx](frontend/src/pages/Relationships.tsx)
- [frontend/src/services/api.ts](frontend/src/services/api.ts)
- [frontend/src/types/index.ts](frontend/src/types/index.ts)

</details>



This page documents the Character and Relationship APIs, covering character CRUD operations, organization management, relationship tracking, and AI-assisted generation services. These APIs manage the complex social ecosystem of a novel project, including individual actors, hierarchical organizations, and interpersonal connections.

## Overview

The character management system is split into three primary functional areas:

| Area | Purpose | Key File |
|------|---------|----------|
| **Character Management** | Core CRUD for individual and organizational entities. | [backend/app/api/characters.py]() |
| **Relationship Tracking** | Interpersonal connections, intimacy levels, and graph data. | [backend/app/api/relationships.py]() |
| **Organization Hierarchy** | Managing memberships, ranks, and organizational attributes. | [backend/app/api/organizations.py]() |

Characters are unified entities in the database; an organization is a `Character` record with `is_organization=True`, linked to specialized details in the `Organization` table.

Sources: [backend/app/api/characters.py:11-14](), [backend/app/api/organizations.py:11-13]()

---

## Character CRUD and AI Generation

### Data Flow: Character Retrieval
When fetching characters, the backend enriches the base model with relationship summaries and organizational details.

```mermaid
graph TD
    A["GET /api/characters"] --> B["verify_project_access"]
    B --> C["Query Character Table"]
    C --> D["_build_relationships_summary"]
    C --> E["_build_org_members_summary (if org)"]
    D --> F["Query CharacterRelationship"]
    E --> G["Query Organization & Members"]
    F --> H["Enriched CharacterResponse"]
    G --> H
```

**Key Implementation Details:**
- **Relationship Summary**: `_build_relationships_summary` constructs a human-readable string (e.g., "与张三：朋友；与李四：敌人") by querying the `CharacterRelationship` table. [backend/app/api/characters.py:34-80]()
- **Organization Summary**: `_build_org_members_summary` returns a JSON string array of members and their positions. [backend/app/api/characters.py:83-117]()

### AI-Assisted Generation
Characters can be generated via a streaming SSE endpoint that supports Model Context Protocol (MCP) for external knowledge retrieval.

- **Endpoint**: `POST /api/characters/generate-stream`
- **Implementation**: Uses `SSEPostClient` on the frontend and `AIService` on the backend to stream character profiles based on project context. [frontend/src/pages/Characters.tsx:161-187](), [backend/app/api/characters.py:246-302]()

Sources: [backend/app/api/characters.py:120-194](), [frontend/src/services/api.ts:258-272]()

---

## Relationship Management

The relationship system tracks bidirectional links between characters with metadata like `intimacy_level` and `status`.

### Relationship Graph Data Structure
The API provides a specialized graph endpoint for visual mapping (used by `RelationshipGraph.tsx`).

```mermaid
classDiagram
    class RelationshipGraphData {
        nodes: RelationshipGraphNode[]
        links: RelationshipGraphLink[]
    }
    class RelationshipGraphNode {
        id: string
        name: string
        type: string
        role_type: string
        avatar: string
    }
    class RelationshipGraphLink {
        source: string
        target: string
        relationship: string
        intimacy: number
        status: string
    }
```

**Data Aggregation Logic:**
1. Fetches all `Character` records as nodes. [backend/app/api/relationships.py:94-109]()
2. Fetches `CharacterRelationship` records as interpersonal links. [backend/app/api/relationships.py:112-128]()
3. Fetches `OrganizationMember` records and converts them into "Organization -> Member" links. [backend/app/api/relationships.py:132-151]()

Sources: [backend/app/api/relationships.py:77-157](), [frontend/src/pages/RelationshipGraph.tsx:27-46]()

---

## Organization and Membership

Organizations represent collective entities. They are managed through a dedicated router that handles both the entity's attributes and its membership list.

### Organization Entity Architecture

```mermaid
graph LR
    subgraph "Character Space"
        C["Character (is_organization=True)"]
    end
    subgraph "Organization Space"
        O["Organization Table"]
        M["OrganizationMember Table"]
    end
    C --- O
    O --- M
    M --- C2["Character (Member)"]
```

### Key Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/organizations/project/{id}` | Lists all organizations with member counts and power levels. [backend/app/api/organizations.py:46-89]() |
| `POST` | `/api/organizations/{id}/members` | Adds a character to an organization with a specific `position` and `rank`. [backend/app/api/organizations.py:231-274]() |
| `PUT` | `/api/organizations/members/{id}` | Updates member loyalty, contribution, or status. [backend/app/api/organizations.py:313-345]() |

**Automatic Counters**: Adding a member via the API automatically increments the `member_count` on the `Organization` record. [backend/app/api/organizations.py:266]()

Sources: [backend/app/api/organizations.py:114-155](), [frontend/src/pages/Organizations.tsx:121-135]()

---

## Technical Implementation Details

### Frontend Service Integration
The `api.ts` file defines `characterApi` and `relationshipApi` which wrap axios calls.

- **Character Sync**: The `useCharacterSync` hook (used in `Characters.tsx`) manages local state updates after API calls to ensure UI consistency. [frontend/src/pages/Characters.tsx:117-120]()
- **SSE Client**: Character generation uses `SSEPostClient` to handle the asynchronous stream of JSON chunks from the backend. [frontend/src/utils/sseClient.ts]() (referenced in [frontend/src/pages/Characters.tsx:11]())

### Schema Validation
The system uses Pydantic models to strictly enforce data types for character and relationship operations.

- **CharacterBase**: Defines core fields like `role_type` (protagonist/supporting/antagonist). [backend/app/schemas/character.py:7-21]()
- **CharacterResponse**: Includes computed fields like `power_level` (from the Organization table) and `main_career_id`. [backend/app/schemas/character.py:80-107]()

Sources: [frontend/src/services/api.ts:258-305](), [backend/app/schemas/character.py:1-123]()

---

## Relationship Types and Categories

The system supports categorized relationship types (Family, Social, Hostile, Professional) which influence the visual representation in the graph.

| Category | UI Color (Frontend) | Example Types |
|----------|---------------------|---------------|
| `family` | Magenta | Parent, Sibling |
| `social` | Blue | Friend, Acquaintance |
| `hostile`| Red | Rival, Enemy |
| `professional` | Cyan | Colleague, Mentor |

Sources: [frontend/src/pages/Relationships.tsx:199-207](), [frontend/src/pages/RelationshipGraph.tsx:105-115]()

---

# Page: Project APIs

# Project APIs

<details>
<summary>Relevant source files</summary>

The following files were used as context for generating this wiki page:

- [backend/app/api/book_import.py](backend/app/api/book_import.py)
- [backend/app/api/projects.py](backend/app/api/projects.py)
- [backend/app/schemas/book_import.py](backend/app/schemas/book_import.py)
- [backend/app/schemas/import_export.py](backend/app/schemas/import_export.py)
- [backend/app/services/book_import_service.py](backend/app/services/book_import_service.py)
- [backend/app/services/import_export_service.py](backend/app/services/import_export_service.py)
- [backend/app/services/txt_parser_service.py](backend/app/services/txt_parser_service.py)
- [docker-compose.yml](docker-compose.yml)
- [frontend/src/pages/BookImport.tsx](frontend/src/pages/BookImport.tsx)
- [frontend/src/services/api.ts](frontend/src/services/api.ts)
- [frontend/src/types/index.ts](frontend/src/types/index.ts)

</details>



This page documents the REST API endpoints for project management, including CRUD operations, export/import functionality, data validation, and the specialized "Book Import" (拆书) system. These endpoints handle the core project entity lifecycle and bulk data ingestion.

For project creation using AI wizards, see [Wizard Stream APIs](#8.1). For project-related content like outlines, chapters, and characters, see [Outline APIs](#8.2), [Chapter APIs](#8.3), and [Character and Relationship APIs](#8.4).

---

## Overview

The Project APIs provide endpoints for managing novel projects, which serve as the top-level container for all content (world-building, characters, outlines, chapters). Each project includes metadata (title, theme, genre), status tracking (planning, writing, revising, completed), word count statistics, and configuration (outline mode, narrative perspective).

The system also includes a sophisticated **Book Import Service** (`BookImportService`) that allows users to upload existing TXT files. It uses a rule-based parser (`TxtParserService`) to split text into chapters and an AI-driven pipeline to reconstruct project metadata, world-building, and character systems from the imported text.

**API Entity Mapping**

```mermaid
graph TD
    subgraph "Natural Language Space (UI/Concepts)"
        UI_Project["Project Dashboard"]
        UI_Import["Book Import (拆书)"]
        UI_Export["JSON Export/Import"]
    end

    subgraph "Code Entity Space (Backend/Frontend)"
        Router_Proj["backend/app/api/projects.py"]
        Router_Import["backend/app/api/book_import.py"]
        Service_Import["BookImportService<br/>(backend/app/services/book_import_service.py)"]
        Service_Parser["TxtParserService<br/>(backend/app/services/txt_parser_service.py)"]
        Model_Project["Project Model<br/>(backend/app/models/project.py)"]
        Export_Service["ImportExportService<br/>(backend/app/services/import_export_service.py)"]
    end

    UI_Project --> Router_Proj
    UI_Import --> Router_Import
    Router_Import --> Service_Import
    Service_Import --> Service_Parser
    Router_Proj --> Export_Service
    Export_Service --> Model_Project
```

**Sources**: [backend/app/api/projects.py:42](), [backend/app/api/book_import.py:23](), [backend/app/services/book_import_service.py:82](), [backend/app/services/import_export_service.py:41]()

---

## CRUD Operations

### List Projects
Retrieves all projects belonging to the authenticated user, ordered by most recently updated.

**Endpoint**: `GET /api/projects`
**Frontend API**: `projectApi.getProjects()` [frontend/src/services/api.ts:242]()

**Implementation**:
The backend uses `select(Project).where(Project.user_id == user_id)` to ensure strict data isolation. It returns a `ProjectListResponse` containing the total count and a list of project objects.
[backend/app/api/projects.py:79-111]()

### Create Project
Creates a new project for the authenticated user.

**Endpoint**: `POST /api/projects`
**Frontend API**: `projectApi.createProject(data: ProjectCreate)` [frontend/src/services/api.ts:246]()

**Data Model**:
- `title`: Required string.
- `outline_mode`: `'one-to-one'` or `'one-to-many'`. Default is `'one-to-many'`.
[frontend/src/types/index.ts:183-196]()

### Update & Delete Project
Standard lifecycle operations. Deleting a project triggers a cascade of deletions for all associated chapters, outlines, characters, and AI analysis history.
[backend/app/api/projects.py:156-215]()

---

## Project Export & Import

The `ImportExportService` handles full project backups in JSON format. This is distinct from the "Book Import" feature as it preserves all AI-generated metadata, writing styles, and career systems.

**Export Options**:
Users can choose to include or exclude:
- Generation History (`include_generation_history`)
- Writing Styles (`include_writing_styles`)
- Career Systems (`include_careers`)
- Story Memories (`include_memories`)
- Plot Analysis (`include_plot_analysis`)
[backend/app/schemas/import_export.py:7-14]()

**Data Flow for Export**:
1. `ImportExportService.export_project` fetches the `Project` record.
2. It sequentially calls private methods like `_export_chapters`, `_export_characters`, and `_export_outlines`.
3. It bundles all data into a `ProjectExportData` schema (Version 1.1.0).
[backend/app/services/import_export_service.py:48-183]()

---

## Book Import (拆书) System

The "Book Import" system allows users to bootstrap a project from a raw TXT file. It follows a multi-stage pipeline: **Upload -> Parse -> Preview -> AI Reconstruction**.

**System Data Flow**

```mermaid
sequenceDiagram
    participant FE as "BookImport.tsx"
    participant API as "api/book_import.py"
    participant Service as "BookImportService"
    participant Parser as "TxtParserService"
    participant AI as "AIService"

    FE->>API: POST /tasks (Upload TXT)
    API->>Service: create_task()
    Service->>Parser: decode_bytes() & split_chapters()
    Parser-->>Service: List of Chapters
    Service-->>FE: task_id (Status: pending)

    Note over FE, Service: FE polls /tasks/{id} until status="completed"

    FE->>API: GET /tasks/{id}/preview
    API-->>FE: ProjectSuggestion + Chapters + Outlines

    FE->>API: POST /tasks/{id}/apply-stream (SSE)
    Service->>AI: Generate World-building
    AI-->>FE: SSE: progress (25%)
    Service->>AI: Generate Careers
    AI-->>FE: SSE: progress (50%)
    Service->>AI: Generate Characters
    AI-->>FE: SSE: progress (100%)
    Service-->>FE: SSE: result (project_id)
```

### 1. TXT Parsing (`TxtParserService`)
The parser uses a "Rule-First" approach:
- **Encoding**: Attempts `utf-8`, `gb18030`, `gbk` before falling back to `utf-8(ignore)`. [backend/app/services/txt_parser_service.py:21-37]()
- **Chapter Splitting**: Uses `STRONG_CHAPTER_PATTERNS` (e.g., `第...章`, `Chapter \d`) to identify boundaries. [backend/app/services/txt_parser_service.py:15-19]()
- **Fallback**: If no headings are found, it performs a fixed-window split (3000-5000 characters) at punctuation boundaries. [backend/app/services/txt_parser_service.py:135-168]()

### 2. Task Management
Import tasks are managed in-memory within the `BookImportService`.
- **Create Task**: `POST /api/book-import/tasks`. [backend/app/api/book_import.py:29-64]()
- **Cancel Task**: `DELETE /api/book-import/tasks/{task_id}`. [backend/app/api/book_import.py:104-110]()

### 3. AI Reconstruction (SSE Apply)
When a user "applies" an import, the system doesn't just save text; it uses SSE (`apply_book_import_stream`) to provide real-time feedback while AI analyzes the text to rebuild the project structure.
- **World-building**: AI infers time period, location, and rules from the first 10 chapters.
- **Career System**: AI extracts power levels or professional systems.
- **Character Extraction**: AI identifies main characters and their relationships.
[backend/app/services/book_import_service.py:199-230](), [backend/app/api/book_import.py:113-187]()

---

## Project Statistics

Project statistics are primarily handled via the `ProjectResponse` schema, which includes calculated fields.

| Field | Source / Implementation |
| :--- | :--- |
| `current_words` | Sum of `word_count` from all chapters in the project. [frontend/src/types/index.ts:162]() |
| `chapter_count` | Count of `Chapter` records associated with the project ID. [frontend/src/types/index.ts:171]() |
| `character_count` | Count of `Character` records associated with the project ID. [frontend/src/types/index.ts:173]() |

The `ImportExportService` also provides an overview of entity counts during the export/import validation phase.
[backend/app/services/import_export_service.py:101-124]()

**Sources**:
- `backend/app/api/projects.py` (CRUD & Export endpoints)
- `backend/app/api/book_import.py` (Import task endpoints)
- `backend/app/services/import_export_service.py` (JSON data handling)
- `backend/app/services/book_import_service.py` (TXT to Project pipeline)
- `backend/app/services/txt_parser_service.py` (Text processing logic)
- `frontend/src/services/api.ts` (Frontend client methods)
- `frontend/src/types/index.ts` (Data structures)

---

# Page: Settings and Configuration APIs

# Settings and Configuration APIs

<details>
<summary>Relevant source files</summary>

The following files were used as context for generating this wiki page:

- [backend/app/api/settings.py](backend/app/api/settings.py)
- [backend/app/schemas/settings.py](backend/app/schemas/settings.py)
- [frontend/src/pages/Settings.tsx](frontend/src/pages/Settings.tsx)
- [frontend/src/services/api.ts](frontend/src/services/api.ts)
- [frontend/src/types/index.ts](frontend/src/types/index.ts)

</details>



## Purpose and Scope

This page documents the REST API endpoints for managing user settings, AI provider configurations, and system-level SMTP settings. The Settings APIs enable users to configure AI service credentials (OpenAI, Gemini, Claude), manage multiple API key presets for rapid switching, discover available models, and test connections. It also covers administrative configuration for email services.

For backend implementation details of AI providers, see [AI Provider Configuration](#5.4). For the frontend implementation, see [Settings Interface](#6.8).

---

## Data Models

### Settings Model

The `Settings` model stores the active AI and image generation configuration for a user. Each user has one active settings record. If no record exists, the system dynamically generates one from `.env` defaults [backend/app/api/settings.py:162-192]().

| Field | Type | Description |
|-------|------|-------------|
| `id` | string (UUID) | Unique identifier |
| `user_id` | string | Owner user ID (multi-user isolation) |
| `api_provider` | string | AI provider: `openai`, `gemini`, or `anthropic` |
| `api_key` | string | API key for the provider |
| `api_base_url` | string | Custom API base URL (optional) |
| `llm_model` | string | Model identifier (e.g., `gpt-4o`) |
| `temperature` | float | Sampling temperature (0.0-2.0) |
| `max_tokens` | int | Maximum tokens per generation |
| `system_prompt` | string | Global system prompt applied to all AI calls |
| `cover_enabled` | boolean | Whether AI cover generation is enabled |
| `cover_api_provider`| string | Provider for image generation (e.g., `dalle`) |
| `preferences` | string (JSON) | Additional user preferences |

**Sources:** [frontend/src/types/index.ts:74-92](), [backend/app/schemas/settings.py:7-24]()

### API Key Preset Model

The `APIKeyPreset` model allows users to save named configurations for quick switching.

| Field | Type | Description |
|-------|------|-------------|
| `id` | string (UUID) | Unique identifier |
| `name` | string | User-friendly preset name |
| `description` | string | Optional preset description |
| `is_active` | boolean | Whether this preset matches current active settings |
| `config` | APIKeyPresetConfig | Configuration object (Provider, Key, Model, etc.) |

**Sources:** [frontend/src/types/index.ts:111-146](), [backend/app/schemas/settings.py:89-112]()

---

## Settings CRUD Operations

### Get Current Settings
Retrieves active settings. If the user has never saved settings, the backend reads from `.env` via `read_env_defaults` and persists them to the database for that user [backend/app/api/settings.py:42-51, 177-189]().

**Endpoint:** `GET /api/settings`
**Response:** `Settings` object

### Save/Update Settings
Updates the user's active configuration.
**Endpoint:** `POST /api/settings` or `PUT /api/settings`
**Note:** Saving settings triggers a check for MCP (Model Context Protocol) plugins. If the provider or model changes, the frontend clears the `mcp_verified_config` cache [frontend/src/pages/Settings.tsx:130-176]().

### Delete Settings
Reverts the user to system defaults by deleting their specific settings record.
**Endpoint:** `DELETE /api/settings`

**Sources:** [frontend/src/services/api.ts:221-230](), [backend/app/api/settings.py:162-192]()

---

## Model Discovery and Testing

### Get Available Models
Fetches a list of models supported by the provider using the provided credentials.
**Endpoint:** `GET /api/settings/models`
**Query Params:** `api_key`, `api_base_url`, `provider`
**Implementation:** Calls `AIService.get_available_models` [frontend/src/services/api.ts:232-233]().

### Test API Connection
Validates credentials by performing a lightweight "ping" to the AI provider.
**Endpoint:** `POST /api/settings/test`
**Response:** Includes `success`, `response_time_ms`, and `response_preview` [frontend/src/pages/Settings.tsx:28-36]().

### Test Cover API
Validates image generation settings (e.g., DALL-E).
**Endpoint:** `POST /api/settings/cover/test`
**Implementation:** Routes through `cover_generation_service.test_cover_settings` [backend/app/api/settings.py:195-209]().

---

## API Key Preset Management

The system supports a workflow for managing multiple configurations.

```mermaid
sequenceDiagram
    participant User as "User"
    participant API as "settingsApi"
    participant DB as "PostgreSQL (Settings/Presets)"
    participant AI as "AI Provider"

    User->>API: "List Presets (GET /settings/presets)"
    API->>DB: "SELECT * FROM api_key_presets WHERE user_id = ?"
    DB-->>User: "Return Presets List"

    User->>API: "Test Preset (POST /presets/{id}/test)"
    API->>AI: "Validate credentials"
    AI-->>User: "Success/Failure Result"

    User->>API: "Activate Preset (POST /presets/{id}/activate)"
    API->>DB: "UPDATE settings SET ... FROM preset.config"
    DB-->>User: "Settings Updated"
```

**Sources:** [frontend/src/services/api.ts:241-274](), [backend/app/api/settings.py:270-350]()

---

## Administrative & SMTP Configuration

System-level email settings are managed by administrators and stored on the admin's settings record [backend/app/api/settings.py:68-98]().

### SMTP Management
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/settings/smtp` | `GET` | Get system SMTP config (Admin only) |
| `/api/settings/smtp` | `PUT` | Update SMTP config (Admin only) |
| `/api/settings/smtp/test` | `POST` | Send test email to `to_email` |

**Implementation:** Uses `email_service` to validate SMTP connectivity [backend/app/api/settings.py:433-460]().

**Sources:** [backend/app/api/settings.py:388-460](), [backend/app/schemas/settings.py:46-86]()

---

## Implementation Architecture

The following diagram bridges the frontend UI state to the backend service logic.

```mermaid
graph TD
    subgraph "Frontend: SettingsPage.tsx"
        UI_State["React State:<br/>presets, activePresetId"]
        Form_Hooks["Form.useForm()"]
        Event_Bus["eventBus.emit(SETTINGS_UPDATED)"]
    end

    subgraph "Backend: settings.py"
        Route_Get["get_settings()"]
        Route_Test["test_api_connection()"]
        Dep_User["get_user_ai_service()"]
    end

    subgraph "Service Layer"
        AIService["AIService (LLM Logic)"]
        CoverService["CoverGenerationService"]
        EmailService["EmailService (SMTP)"]
    end

    UI_State -->|API Call| Route_Get
    Form_Hooks -->|POST| Route_Test
    Route_Test --> AIService
    Dep_User -->|Loads| AIService
    Route_Get -->|Read .env if empty| read_env_defaults["read_env_defaults()"]
    
    style AIService fill:#f9f9f9
    style EmailService fill:#f9f9f9
```

**Key Code Entities:**
- `get_user_ai_service`: Dependency that dynamically creates an `AIService` instance based on the user's stored database settings and active MCP plugins [backend/app/api/settings.py:101-159]().
- `create_user_ai_service_with_mcp`: Factory function that integrates MCP tools into the user's AI session [backend/app/api/settings.py:148-159]().
- `settingsApi`: Frontend axios wrapper for all configuration endpoints [frontend/src/services/api.ts:221-274]().

**Sources:** [backend/app/api/settings.py:101-159](), [frontend/src/services/api.ts:221-274](), [frontend/src/pages/Settings.tsx:13-128]()

---

# Page: Inspiration APIs

# Inspiration APIs

<details>
<summary>Relevant source files</summary>

The following files were used as context for generating this wiki page:

- [backend/app/api/inspiration.py](backend/app/api/inspiration.py)
- [backend/app/services/plot_expansion_service.py](backend/app/services/plot_expansion_service.py)
- [frontend/src/components/AIProjectGenerator.tsx](frontend/src/components/AIProjectGenerator.tsx)
- [frontend/src/components/SSEProgressModal.tsx](frontend/src/components/SSEProgressModal.tsx)
- [frontend/src/pages/Inspiration.tsx](frontend/src/pages/Inspiration.tsx)
- [frontend/src/pages/ProjectWizardNew.tsx](frontend/src/pages/ProjectWizardNew.tsx)
- [frontend/src/services/api.ts](frontend/src/services/api.ts)
- [frontend/src/types/index.ts](frontend/src/types/index.ts)

</details>



## Purpose and Scope

This document describes the Inspiration Mode APIs, which provide step-by-step AI-guided project creation through conversational interaction. These endpoints generate contextual options at each stage of project setup (title, description, theme, genre) and support intelligent auto-completion of missing information.

For the frontend implementation of Inspiration Mode, see [6.4 Wizard and Inspiration Interfaces](). For the streaming wizard APIs that handle world-building and batch generation, see [8.1 Wizard Stream APIs]().

**Sources:** [backend/app/api/inspiration.py:1-318]()

---

## API Overview

The Inspiration API provides two primary endpoints for interactive project creation defined in the `inspiration` router:

| Endpoint | Method | Purpose | Retry Support |
|----------|--------|---------|---------------|
| `/api/inspiration/generate-options` | POST | Generate AI-suggested options for current step | Yes (3 attempts) |
| `/api/inspiration/quick-generate` | POST | Auto-complete all missing project fields | No |

Both endpoints use the user's configured AI service settings (via `get_user_ai_service` dependency) and support custom prompt templates through `PromptService`.

**Sources:** [backend/app/api/inspiration.py:13-14](), [backend/app/api/inspiration.py:69-75](), [backend/app/api/inspiration.py:225-230]()

---

## Endpoint: Generate Options

### Request Flow

The following diagram illustrates the interaction between the frontend `Inspiration.tsx` component and the backend `inspiration.py` logic.

```mermaid
sequenceDiagram
    participant Client as "frontend/src/pages/Inspiration.tsx"
    participant API as "backend/app/api/inspiration.py"
    participant Validator as "validate_options_response"
    participant AIService as "backend/app/services/ai_service.py"
    participant PromptService as "backend/app/services/prompt_service.py"
    
    Client->>API: POST /generate-options (step, context)
    
    loop "Retry up to 3 times (max_retries)"
        API->>PromptService: get_template(system_key/user_key, user_id, db)
        PromptService-->>API: Template string
        
        API->>API: Format with context (initial_idea, title, etc.)
        Note over API: Uses TEMPERATURE_SETTINGS[step]
        
        API->>AIService: generate_text_stream(prompt, system_prompt, temperature)
        AIService-->>API: accumulated_text (JSON string)
        
        API->>AIService: _clean_json_response(content)
        AIService-->>API: Sanitized JSON
        
        API->>API: json.loads()
        
        API->>Validator: validate_options_response(result, step)
        
        alt "Validation Success"
            Validator-->>API: (True, "")
            API-->>Client: {"prompt": "...", "options": [...]}
        else "Validation Failed"
            Validator-->>API: (False, error_msg)
            Note over API: Continue retry loop with warning in prompt
        end
    end
    
    alt "All Retries Failed"
        API-->>Client: {"error": "...", "options": ["让AI重新生成", "我自己输入"]}
    end
```

**Sources:** [backend/app/api/inspiration.py:69-222](), [frontend/src/pages/Inspiration.tsx:230-264]()

---

### Request Schema

The request is handled by the `generate_options` function.

```typescript
// frontend/src/services/api.ts
POST /api/inspiration/generate-options
{
    "step": "title" | "description" | "theme" | "genre",
    "context": {
        "initial_idea": "...",
        "title": "...",         
        "description": "...",   
        "theme": "...",         
        "genre": ["..."]        
    }
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `step` | string | Yes | Current generation step: `title`, `description`, `theme`, or `genre`. |
| `context` | object | Yes | Previously collected information. `initial_idea` is mapped from user's first input. |

**Sources:** [backend/app/api/inspiration.py:79-93](), [backend/app/api/inspiration.py:131-136]()

---

### Response Schema

#### Success Response
Returned when `validate_options_response` passes.

```json
{
    "prompt": "请从以下书名中选择一个，或自己创作：",
    "options": [
        "星河尽头的守望者",
        "时空裂痕",
        "最后的机械师",
        "虚拟之城",
        "量子迷雾",
        "深空遗产"
    ]
}
```

#### Error Response (After Retries)
Returned if `max_retries` (3) is reached without a valid JSON response.

```json
{
    "error": "AI生成格式错误，已自动重试3次，请手动重试或自己输入",
    "prompt": "请为【title】提供内容：",
    "options": ["让AI重新生成", "我自己输入"]
}
```

**Sources:** [backend/app/api/inspiration.py:181-203](), [backend/app/api/inspiration.py:26-66]()

---

### Template Mapping

The API uses distinct system and user templates for each step, retrieved via `PromptService.get_template`.

| Step | Template Keys (System, User) | Description |
|------|------------------------------|-------------|
| `title` | `INSPIRATION_TITLE_SYSTEM`, `_USER` | Creative title suggestions. |
| `description` | `INSPIRATION_DESCRIPTION_SYSTEM`, `_USER` | Detailed synopsis based on title. |
| `theme` | `INSPIRATION_THEME_SYSTEM`, `_USER` | Core thematic elements. |
| `genre` | `INSPIRATION_GENRE_SYSTEM`, `_USER` | Concise genre tags (2-10 characters). |

**Sources:** [backend/app/api/inspiration.py:109-114](), [backend/app/api/inspiration.py:127-128]()

---

### Temperature Configuration Strategy

The `TEMPERATURE_SETTINGS` constant defines a **progressive temperature decay** strategy to ensure consistency as the project structure solidifies.

```python
TEMPERATURE_SETTINGS = {
    "title": 0.8,        # High creativity for naming
    "description": 0.65, # Moderate constraints for plot
    "theme": 0.55,       # Higher consistency for themes
    "genre": 0.45        # Low randomness for classification
}
```

**Sources:** [backend/app/api/inspiration.py:18-23](), [backend/app/api/inspiration.py:148-156]()

---

## Validation and Retry Logic

### Validation Rules

The `validate_options_response` function enforces strict requirements to prevent frontend UI breakage.

```mermaid
graph TB
    Input["AI Response JSON"]
    
    Check1{"'options' field exists?"}
    Check2{"Is options a list?"}
    Check3{"3 to 10 items?"}
    Check4{"All items strings?"}
    Check5{"All non-empty?"}
    Check6{"Length < 500 chars?"}
    Check7{"Is 'genre' step?"}
    Check8{"Tags 2-10 chars?"}
    
    Pass["✅ Validation Pass"]
    Fail["❌ Validation Fail<br/>Trigger Retry"]
    
    Input --> Check1
    Check1 -- No --> Fail
    Check1 -- Yes --> Check2
    Check2 -- No --> Fail
    Check2 -- Yes --> Check3
    Check3 -- No --> Fail
    Check3 -- Yes --> Check4
    Check4 -- No --> Fail
    Check4 -- Yes --> Check5
    Check5 -- No --> Fail
    Check5 -- Yes --> Check6
    Check6 -- No --> Fail
    Check6 -- Yes --> Check7
    Check7 -- No --> Pass
    Check7 -- Yes --> Check8
    Check8 -- No --> Fail
    Check8 -- Yes --> Pass
```

**Sources:** [backend/app/api/inspiration.py:26-66]()

---

### Retry Mechanism

On each retry, the system appends a warning to the `system_prompt` to correct the LLM's behavior:

```python
if attempt > 0:
    system_prompt += f"\n\n⚠️ 这是第{attempt + 1}次生成，请务必严格按照JSON格式返回，确保options数组包含6个有效选项！"
```

**Sources:** [backend/app/api/inspiration.py:143-144]()

---

## Endpoint: Quick Generate

The `quick_generate` endpoint provides auto-completion for partially filled project data, used when a user wants the AI to "fill in the blanks".

### Request/Response Flow

```mermaid
sequenceDiagram
    participant Client as "frontend/src/pages/Inspiration.tsx"
    participant API as "backend/app/api/inspiration.py"
    participant Prompt as "backend/app/services/prompt_service.py"
    participant AI as "backend/app/services/ai_service.py"
    
    Client->>API: POST /quick-generate (partial data)
    
    API->>API: Construct 'existing_info' summary
    API->>Prompt: get_template("INSPIRATION_QUICK_COMPLETE", user_id, db)
    Prompt-->>API: Template
    
    API->>AI: generate_text_stream(prompt, temperature=0.7)
    AI-->>API: JSON content
    
    API->>AI: _clean_json_response()
    API->>API: json.loads()
    
    API->>API: Merge: User Input > AI Output
    Note right of API: result.get('title') or data.get('title')
    
    API-->>Client: Full Project Object
```

**Sources:** [backend/app/api/inspiration.py:225-318]()

---

### Field Precedence

The logic ensures that if a user has already provided a field, the AI's suggestion for that specific field is discarded in favor of the user's input.

```python
final_result = {
    "title": data.get("title") or result.get("title", ""),
    "description": data.get("description") or result.get("description", ""),
    "theme": data.get("theme") or result.get("theme", ""),
    "genre": data.get("genre") or result.get("genre", [])
}
```

**Sources:** [backend/app/api/inspiration.py:299-308]()

---

## Frontend Integration

### Inspiration.tsx Component

The `Inspiration` page manages a conversational state machine.

*   **Caching:** Uses `localStorage` with `CACHE_KEY` (`inspiration_conversation_cache`) to save `messages`, `currentStep`, and `wizardData`.
*   **API Calls:** Invokes `inspirationApi.generateOptions` and `inspirationApi.quickGenerate`.
*   **Transition:** Once all data is collected, it transitions to the `AIProjectGenerator` component to create the actual database entities (World, Characters, Outline).

**Sources:** [frontend/src/pages/Inspiration.tsx:47-53](), [frontend/src/pages/Inspiration.tsx:117-144](), [frontend/src/pages/Inspiration.tsx:230-264]()

### SSE Progress Tracking

While the Inspiration APIs themselves are standard REST (POST), the final project creation triggered after the conversation uses the `wizardStreamApi` which implements Server-Sent Events (SSE).

*   **Component:** `AIProjectGenerator.tsx`
*   **UI:** `SSEProgressModal.tsx` displays the progress percentage and current status message (e.g., "正在生成世界观...").

**Sources:** [frontend/src/components/AIProjectGenerator.tsx:64-73](), [frontend/src/components/SSEProgressModal.tsx:20-29]()

---

## Implementation Notes

### AI Service Dependency
Both endpoints utilize the `get_user_ai_service` dependency, which ensures that the AI provider (OpenAI, Gemini, etc.) and model settings are scoped to the current user's configuration.

**Sources:** [backend/app/api/inspiration.py:9](), [backend/app/api/inspiration.py:74]()

### JSON Sanitization
The system uses `AIService._clean_json_response` to strip markdown code blocks (e.g., ` ```json ... ``` `) that LLMs often include, ensuring `json.loads` does not fail on non-JSON text.

**Sources:** [backend/app/api/inspiration.py:167-169](), [backend/app/api/inspiration.py:294-296]()

---

# Page: Development

# Development

<details>
<summary>Relevant source files</summary>

The following files were used as context for generating this wiki page:

- [README.md](README.md)
- [backend/.env.example](backend/.env.example)
- [frontend/package-lock.json](frontend/package-lock.json)
- [frontend/package.json](frontend/package.json)
- [frontend/src/components/AppFooter.tsx](frontend/src/components/AppFooter.tsx)
- [frontend/src/components/ChangelogModal.tsx](frontend/src/components/ChangelogModal.tsx)
- [frontend/src/config/version.ts](frontend/src/config/version.ts)
- [frontend/src/services/changelogService.ts](frontend/src/services/changelogService.ts)
- [frontend/src/services/versionService.ts](frontend/src/services/versionService.ts)
- [frontend/vite.config.ts](frontend/vite.config.ts)

</details>



This page provides essential information for developers who want to contribute to, extend, or customize MuMuAINovel. It covers the development environment setup, codebase organization, and common development workflows.

For detailed information on specific development topics:
- Project file and directory organization: see [Project Structure](#9.1)
- Setting up local environment and testing: see [Development Workflow](#9.2)
- Extending AI provider support: see [Adding New AI Providers](#9.3)
- Modifying prompt templates: see [Creating Custom Prompts](#9.4)

## Prerequisites

MuMuAINovel requires the following tools for local development:

| Tool | Version | Purpose |
|------|---------|---------|
| Python | 3.11+ | Backend runtime |
| Node.js | 18+ | Frontend build tooling |
| PostgreSQL | 15+ | Production-grade database |
| Docker | Latest | Containerized deployment and testing |

Additional requirements:
- At least one AI provider API key (OpenAI, Gemini, or Claude) [README.md:174-174]()
- Basic understanding of FastAPI (Python) and React (TypeScript)

Sources: [README.md:6-9](), [README.md:134-162]()

## Development Architecture Overview

### Local Development Server Configuration

The diagram below shows how the development servers interact during local development:

```mermaid
graph TB
    subgraph "Development Host"
        subgraph "Frontend Dev Server (Vite)"
            FrontDev["npm run dev<br/>Port 5173<br/>Hot Module Replacement"]
            ViteProxy["Vite Proxy Config<br/>vite.config.ts"]
        end
        
        subgraph "Backend Dev Server (Uvicorn)"
            BackDev["uvicorn app.main:app<br/>Port 8000<br/>--reload flag"]
            MainApp["app.main:app<br/>FastAPI Application"]
            APIRoutes["API Routes<br/>/api/*"]
        end
        
        subgraph "Infrastructure"
            Postgres["PostgreSQL DB<br/>Port 5432"]
            EnvFile[".env file<br/>API keys & config"]
            LogsDir["logs/app.log<br/>Application logs"]
        end
        
        Browser["Browser<br/>localhost:5173"]
    end
    
    Browser -->|"HTTP Requests"| FrontDev
    FrontDev -->|"API Proxy<br/>/api/*"| ViteProxy
    ViteProxy -->|"Forward to<br/>localhost:8000"| BackDev
    
    BackDev --> MainApp
    MainApp --> APIRoutes
    MainApp --> Postgres
    
    BackDev -.Watches.-> EnvFile
    BackDev --> LogsDir
```

**Key Points:**
- **Frontend:** Uses Vite for fast development and HMR [frontend/package.json:7-7]().
- **Backend:** Uses FastAPI with Uvicorn. The `--reload` flag is recommended for local dev.
- **Proxy:** `vite.config.ts` handles proxying `/api` and `/generated-assets` to the backend [frontend/vite.config.ts:42-53]().
- **Database:** Defaults to PostgreSQL for production parity, though SQLite is supported for simple tests [backend/.env.example:22-34]().

Sources: [frontend/package.json:7-7](), [frontend/vite.config.ts:42-53](), [backend/.env.example:22-34]()

### Development Entry Points

```mermaid
graph LR
    subgraph "Backend Entry Points"
        MainPy["backend/app/main.py<br/>FastAPI() app creation"]
        ConfigPy["backend/app/config.py<br/>Settings class"]
        DatabasePy["backend/app/database.py<br/>get_db dependency"]
    end
    
    subgraph "Frontend Entry Points"
        PackageJson["frontend/package.json<br/>Scripts & Dependencies"]
        MainTSX["frontend/src/main.tsx<br/>React root render"]
        AppTSX["frontend/src/App.tsx<br/>Route definitions"]
        StoreTSX["frontend/src/store/useStore.ts<br/>Zustand store"]
    end
    
    MainPy -->|"Loads"| ConfigPy
    MainPy -->|"Uses"| DatabasePy
    
    PackageJson -->|"Runs"| MainTSX
    MainTSX -->|"Renders"| AppTSX
    AppTSX -->|"Accesses"| StoreTSX
```

Sources: [frontend/package.json:6-11](), [frontend/src/config/version.ts:8-29]()

## Quick Start for Development

### Backend Setup

1. **Clone repository and navigate to backend:**
```bash
git clone https://github.com/xiamuceer-j/MuMuAINovel.git
cd MuMuAINovel/backend
```

2. **Configure environment:**
```bash
cp .env.example .env
# Edit .env file with your API keys and database credentials
```

3. **Database Initialization:**
Ensure PostgreSQL is running and execute the initialization script [README.md:202-202]().
```bash
# Script location: backend/scripts/init_postgres.sql
```

4. **Start development server (Docker recommended):**
```bash
docker-compose up -d
```

Sources: [README.md:176-197](), [backend/.env.example:1-5]()

### Frontend Setup

1. **Navigate to frontend directory:**
```bash
cd frontend
```

2. **Install dependencies:**
```bash
npm install
```

3. **Start development server:**
```bash
npm run dev
```

The frontend will be available at `http://localhost:5173`, proxying requests to the backend at `http://localhost:8000` [frontend/vite.config.ts:42-53]().

Sources: [frontend/package.json:7-7](), [frontend/vite.config.ts:42-53]()

## Core Technology Stack

### Backend Dependencies
The backend is built on **FastAPI** [README.md:7-7](). It uses **SQLAlchemy** for ORM and **Pydantic** for data validation and settings management [backend/.env.example:10-14](). AI integrations are handled via official SDKs for OpenAI, Google (Gemini), and Anthropic (Claude).

### Frontend Dependencies
The frontend is a **React** application [README.md:8-8]() using **TypeScript** [frontend/package.json:41-41]().

| Category | Library | Usage |
|----------|---------|-------|
| UI Components | `antd` | Main component library [frontend/package.json:20-20]() |
| State Management | `zustand` | Global application state [frontend/package.json:29-29]() |
| Routing | `react-router-dom` | Navigation and URL management [frontend/package.json:28-28]() |
| HTTP Client | `axios` | Backend API communication [frontend/package.json:21-21]() |
| Visualization | `@xyflow/react` | Relationship and logic graphs [frontend/package.json:19-19]() |

Sources: [frontend/package.json:12-45](), [README.md:5-9]()

## Versioning and Updates

The project follows semantic versioning [frontend/src/config/version.ts:3-5]().
- **Version Source:** The version is defined in `frontend/package.json` [frontend/package.json:4-4]() and injected into the app during build [frontend/vite.config.ts:15-20]().
- **Update Checks:** The `versionService` checks against GitHub releases using the shields.io API [frontend/src/services/versionService.ts:32-40]().
- **Changelog:** Automatically generated from GitHub commits via `changelogService` [frontend/src/services/changelogService.ts:202-205]().

Sources: [frontend/src/config/version.ts:8-29](), [frontend/src/services/versionService.ts:32-40](), [frontend/src/services/changelogService.ts:153-174]()

## Next Steps

For more detailed information on development topics:

- **Understanding the codebase structure:** See [Project Structure](#9.1) for detailed directory layout and file responsibilities.
- **Setting up your local environment:** See [Development Workflow](#9.2) for step-by-step setup and testing procedures.
- **Extending AI capabilities:** See [Adding New AI Providers](#9.3) for integrating new LLM services.
- **Customizing content generation:** See [Creating Custom Prompts](#9.4) for modifying prompt templates.

Sources: [README.md:13-13]()

---

# Page: Project Structure

# Project Structure

<details>
<summary>Relevant source files</summary>

The following files were used as context for generating this wiki page:

- [README.md](README.md)
- [backend/.env.example](backend/.env.example)
- [backend/app/api/auth.py](backend/app/api/auth.py)
- [backend/app/config.py](backend/app/config.py)
- [backend/app/models/settings.py](backend/app/models/settings.py)
- [backend/requirements.txt](backend/requirements.txt)
- [frontend/package-lock.json](frontend/package-lock.json)
- [frontend/package.json](frontend/package.json)
- [frontend/src/components/AppFooter.tsx](frontend/src/components/AppFooter.tsx)
- [frontend/src/components/ChangelogModal.tsx](frontend/src/components/ChangelogModal.tsx)
- [frontend/src/config/version.ts](frontend/src/config/version.ts)
- [frontend/src/services/changelogService.ts](frontend/src/services/changelogService.ts)
- [frontend/src/services/versionService.ts](frontend/src/services/versionService.ts)
- [frontend/vite.config.ts](frontend/vite.config.ts)

</details>



## Purpose and Scope

This document describes the directory organization, file naming conventions, and module responsibilities within the MuMuAINovel codebase. It serves as a reference for developers who need to locate specific functionality or add new features to the project.

MuMuAINovel is a full-stack application utilizing a **FastAPI** backend and a **React (Vite)** frontend. The project is designed for containerized deployment using Docker and supports high-concurrency scenarios with optimized PostgreSQL connection pooling and semantic memory storage via ChromaDB.

---

## Repository Root Organization

The repository follows a monorepo structure with clearly separated frontend and backend codebases, containerization configuration, and data persistence directories.

### Root Directory Structure

```text
MuMuAINovel/
├── backend/                 # FastAPI backend application
├── frontend/                # React TypeScript frontend
├── postgres_data/           # PostgreSQL database files (Docker volume)
├── logs/                    # Application logs
├── docker-compose.yml       # Docker Compose configuration
├── Dockerfile              # Multi-stage build (frontend + backend)
├── README.md               # Project documentation
└── LICENSE                 # GNU GPL v3 license
```

**Directory Diagram: Repository Root**

```mermaid
graph TB
    Root["MuMuAINovel/"]
    
    Root --> Backend["backend/<br/>(FastAPI Server)"]
    Root --> Frontend["frontend/<br/>(React App)"]
    Root --> PostgresData["postgres_data/<br/>(PostgreSQL Data)"]
    Root --> Logs["logs/<br/>(App Logs)"]
    Root --> Docker["docker-compose.yml"]
    Root --> Dockerfile["Dockerfile"]
    Root --> Readme["README.md"]
    
    Backend --> BackendApp["app/"]
    Backend --> BackendStatic["static/<br/>(Built Frontend)"]
    Backend --> BackendScripts["scripts/"]
    Backend --> Requirements["requirements.txt"]
    Backend --> EnvExample[".env.example"]
    
    Frontend --> FrontendSrc["src/"]
    Frontend --> Package["package.json"]
    Frontend --> ViteConfig["vite.config.ts"]
    
    PostgresData --> PGDB["PostgreSQL Database"]
    Logs --> AppLogs["app.log"]
```

**Sources:** [README.md:179-197](), [README.md:218-280]()

---

## Backend Directory Structure

The backend follows a layered architecture with clear separation between API routes, business logic, data models, and infrastructure concerns.

### Backend Application Layout

```text
backend/
├── app/
│   ├── main.py                  # FastAPI app entry point
│   ├── config.py                # Pydantic Settings & Instance ID logic
│   ├── database.py              # PostgreSQL connection & pooling
│   ├── user_manager.py          # User DTO and management logic
│   ├── user_password.py         # Password hashing and validation
│   ├── logger.py                # Logging configuration
│   │
│   ├── api/                     # API route handlers
│   │   ├── auth.py              # OAuth2 & Local Auth endpoints
│   │   ├── projects.py          # Project CRUD
│   │   ├── chapters.py          # Chapter management
│   │   ├── wizard_stream.py     # SSE generation endpoints
│   │   └── ...
│   │
│   ├── models/                  # SQLAlchemy ORM models
│   │   ├── user.py              # User model
│   │   ├── settings.py          # Settings model (API keys, SMTP)
│   │   └── ...
│   │
│   ├── services/                # Business logic layer
│   │   ├── ai_service.py        # AI provider abstraction
│   │   ├── email_service.py     # SMTP integration
│   │   ├── oauth_service.py     # LinuxDO OAuth integration
│   │   └── ...
│   │
│   └── middleware/              # Custom middleware
│       └── auth_middleware.py   # Request authentication
│
├── scripts/                     # Database initialization scripts
│   └── init_postgres.sql        # PostgreSQL extensions setup
│
├── static/                      # Pre-built frontend files (Vite output)
├── requirements.txt             # Python dependencies
└── .env.example                 # Environment variable template
```

**Backend Module Hierarchy Diagram**

```mermaid
graph TB
    MainPy["main.py<br/>(FastAPI App)"]
    AuthMW["auth_middleware.py<br/>(AuthMiddleware)"]
    
    subgraph "API Layer"
        AuthAPI["api/auth.py<br/>(Router: /auth)"]
        ProjAPI["api/projects.py<br/>(Router: /projects)"]
    end
    
    subgraph "Service Layer"
        AIService["ai_service.py<br/>(AIService)"]
        EmailService["email_service.py<br/>(EmailService)"]
        OAuthService["oauth_service.py<br/>(LinuxDOOAuthService)"]
    end
    
    subgraph "Data & Config"
        ConfigPy["config.py<br/>(Settings)"]
        DBPy["database.py<br/>(get_engine)"]
        Models["models/<br/>(SQLAlchemy)"]
    end
    
    MainPy --> AuthMW
    AuthMW --> AuthAPI
    AuthMW --> ProjAPI
    
    AuthAPI --> OAuthService
    AuthAPI --> EmailService
    AuthAPI --> DBPy
    
    ProjAPI --> AIService
    AIService --> ConfigPy
    DBPy --> Models
```

**Sources:** [backend/app/config.py:24-134](), [backend/app/api/auth.py:36-40](), [backend/app/models/settings.py:8-53]()

---

## Frontend Directory Structure

The frontend uses a component-based React architecture with Vite as the build tool and Ant Design for the UI.

### Frontend Application Layout

```text
frontend/
├── src/
│   ├── App.tsx                  # Root component & Routing
│   ├── main.tsx                 # Entry point
│   │
│   ├── components/              # UI Components
│   │   ├── AppFooter.tsx        # Version & Update display
│   │   ├── ChangelogModal.tsx   # GitHub commit history viewer
│   │   └── ...
│   │
│   ├── services/                # API clients
│   │   ├── versionService.ts    # Version checking via shields.io
│   │   ├── changelogService.ts  # GitHub API integration
│   │   └── ...
│   │
│   ├── config/                  # Frontend configuration
│   │   └── version.ts           # Project metadata
│   │
│   ├── store/                   # Zustand state stores
│   └── types/                   # TypeScript definitions
│
├── package.json                 # Dependencies & Scripts
├── vite.config.ts              # Vite & Rollup configuration
└── index.html
```

**Frontend Component Architecture Diagram**

```mermaid
graph TB
    AppTsx["App.tsx"]
    
    subgraph "Components"
        Footer["AppFooter.tsx<br/>(Version Display)"]
        Changelog["ChangelogModal.tsx<br/>(Timeline)"]
    end
    
    subgraph "Services"
        VerSvc["versionService.ts<br/>(checkLatestVersion)"]
        ChgSvc["changelogService.ts<br/>(fetchChangelog)"]
    end
    
    subgraph "Config & State"
        VerCfg["version.ts<br/>(VERSION_INFO)"]
        Store["Zustand Store"]
    end
    
    AppTsx --> Footer
    Footer --> VerSvc
    Footer --> Changelog
    Changelog --> ChgSvc
    VerSvc --> VerCfg
```

**Sources:** [frontend/package.json:12-30](), [frontend/vite.config.ts:21-41](), [frontend/src/components/AppFooter.tsx:14-20]()

---

## Key File Responsibilities

### Backend Infrastructure

| File | Path | Responsibility |
| :--- | :--- | :--- |
| **Global Config** | `backend/app/config.py` | Manages `Settings` via Pydantic. Handles `INSTANCE_ID` generation for the Prompt Workshop [backend/app/config.py:145-175](). |
| **Database** | `backend/app/database.py` | Manages SQLAlchemy engines and connection pooling [backend/app/config.py:47-53](). |
| **Auth API** | `backend/app/api/auth.py` | Implements LinuxDO OAuth2, local login, and email verification [backend/app/api/auth.py:1-36](). |
| **Settings Model** | `backend/app/models/settings.py` | Defines the `Settings` table, storing AI keys, SMTP configs, and user preferences [backend/app/models/settings.py:8-46](). |

### Frontend Infrastructure

| File | Path | Responsibility |
| :--- | :--- | :--- |
| **Build Config** | `frontend/vite.config.ts` | Configures code splitting via `manualChunks` (separating `vendor-antd`, `vendor-react`, etc.) [frontend/vite.config.ts:27-38](). |
| **Version Service** | `frontend/src/services/versionService.ts` | Checks for updates using shields.io Badge API to avoid CORS issues [frontend/src/services/versionService.ts:32-50](). |
| **Footer** | `frontend/src/components/AppFooter.tsx` | Displays version info, update badges, and links to GitHub/Sponsorship [frontend/src/components/AppFooter.tsx:145-202](). |
| **Changelog** | `frontend/src/components/ChangelogModal.tsx` | Renders a `Timeline` of project updates grouped by date [frontend/src/components/ChangelogModal.tsx:106-194](). |

---

## Data Persistence and Configuration

### Database Organization
The project primarily uses **PostgreSQL**.
- **Relational Data**: Managed via SQLAlchemy ORM in `backend/app/models/`.
- **Initialization**: `init_postgres.sql` sets up necessary extensions like `vector` for semantic search [README.md:202]().
- **Pooling**: Optimized for 150-200 concurrent users with `database_pool_size: 50` and `database_max_overflow: 30` [backend/app/config.py:47-49]().

### Configuration Flow
1. **Environment Variables**: Defined in `.env` (based on `.env.example`).
2. **Pydantic Settings**: Loaded into the `Settings` class in `backend/app/config.py` [backend/app/config.py:24-134]().
3. **Runtime Overrides**: Admin-defined settings in the database (e.g., SMTP, AI keys) override `.env` defaults for authentication workflows [backend/app/api/auth.py:125-168]().

**Sources:** [backend/.env.example:1-125](), [backend/app/config.py:17-67](), [backend/requirements.txt:6-15]()

---

# Page: Development Workflow

# Development Workflow

<details>
<summary>Relevant source files</summary>

The following files were used as context for generating this wiki page:

- [.dockerignore](.dockerignore)
- [.github/workflows/docker-build.yml](.github/workflows/docker-build.yml)
- [.gitignore](.gitignore)
- [Dockerfile](Dockerfile)
- [README.md](README.md)
- [backend/.env.example](backend/.env.example)
- [backend/app/services/email_service.py](backend/app/services/email_service.py)
- [backend/app/services/memory_service.py](backend/app/services/memory_service.py)
- [frontend/package-lock.json](frontend/package-lock.json)
- [frontend/package.json](frontend/package.json)

</details>



This page provides a comprehensive guide for developers who want to contribute to MuMuAINovel or extend its functionality. It covers setting up a local development environment, running development servers with hot reload, debugging techniques, and common development workflows.

---

## Prerequisites

Before starting development, ensure you have the following tools installed:

| Tool | Version | Purpose |
|------|---------|---------|
| Python | 3.11 | Backend runtime [README.md:6]() |
| Node.js | 22+ | Frontend build tools [Dockerfile:8]() |
| npm | Latest | Frontend package manager [frontend/package.json:7]() |
| PostgreSQL | 18+ | Production-grade database [README.md:220]() |
| Git | Any | Version control |

Sources: [README.md:6-9](), [Dockerfile:8-38](), [frontend/package.json:1-11]()

---

## Environment Setup

### Initial Repository Setup

```bash
# Clone the repository
git clone https://github.com/xiamuceer-j/MuMuAINovel.git
cd MuMuAINovel

# Create a development branch
git checkout -b feature/your-feature-name
```

### Backend Development Setup

#### 1. Python Virtual Environment

```bash
cd backend

# Create virtual environment
python -m venv .venv

# Activate virtual environment
# On Linux/Mac:
source .venv/bin/activate
# On Windows:
.venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

#### 2. Environment Configuration

The backend relies on a `.env` file for configuration. Use the provided example as a template.

```bash
# Copy example configuration
cp .env.example .env
```

**Key Development Settings in `.env`**:
- `DEBUG=true`: Enables detailed error messages [backend/.env.example:14]().
- `DATABASE_URL`: Connection string for PostgreSQL [backend/.env.example:28]().
- `LOCAL_AUTH_ENABLED=true`: Allows quick testing without OAuth [backend/.env.example:85]().
- `SENTENCE_TRANSFORMERS_HOME`: Directory for embedding models [backend/app/services/memory_service.py:74]().

#### 3. Embedding Model Setup

MuMuAINovel uses `paraphrase-multilingual-MiniLM-L12-v2` for semantic search and chapter analysis [backend/app/services/memory_service.py:173]().

- **Development Mode**: The system looks for models in `backend/embedding/` [backend/app/services/memory_service.py:58]().
- **Offline Mode**: Set `TRANSFORMERS_OFFLINE=1` if models are pre-downloaded [Dockerfile:114]().

Sources: [backend/.env.example:1-125](), [backend/app/services/memory_service.py:13-85](), [Dockerfile:70-85]()

---

### Frontend Development Setup

The frontend is built with React 18 and Vite [frontend/package.json:25,43]().

```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

Sources: [frontend/package.json:1-45](), [Dockerfile:15-26]()

---

### Database Setup

#### Option 1: Docker PostgreSQL (Recommended)

```bash
# Start PostgreSQL container
docker-compose up -d postgres

# Initialize extensions and schema
# The init_postgres.sql script runs automatically on first start
```

#### Option 2: Local PostgreSQL Installation

If running locally, ensure the user has permissions and the database exists as defined in `.env` [backend/.env.example:22-25]().

Sources: [README.md:219-268](), [backend/.env.example:21-25]()

---

## Development Environment Diagram

The following diagram bridges the "Natural Language Space" of development tasks to the "Code Entity Space" of specific files and services.

```mermaid
graph TB
    subgraph "Developer_Machine"
        subgraph "Backend_Runtime"
            Main["app/main.py"]
            Env[".env"]
            DB_Pool["AsyncSession (get_db)"]
            AI_Svc["AIService"]
            Mem_Svc["MemoryService"]
        end
        
        subgraph "Frontend_Runtime"
            Vite["Vite Dev Server (Port 5173)"]
            Zustand["Zustand Store"]
            Axios["Axios API Client"]
        end
        
        subgraph "Data_Storage"
            Postgres["PostgreSQL (Port 5432)"]
            Chroma["ChromaDB (data/chroma_db)"]
            Logs["logs/app.log"]
        end
    end

    Vite -- "Proxy /api" --> Main
    Main -- "Reads" --> Env
    Main -- "Dependency" --> DB_Pool
    DB_Pool -- "Connects" --> Postgres
    AI_Svc -- "Prompts" --> Main
    Mem_Svc -- "Embeddings" --> Chroma
    Main -- "Writes" --> Logs
    Axios -- "Requests" --> Main
    Zustand -- "Manages" --> Axios
```

Sources: [backend/app/services/memory_service.py:88-92](), [backend/.env.example:21-43](), [frontend/package.json:19-29]()

---

## Running Development Servers

### Backend Server with Hot Reload

Start the FastAPI application using `uvicorn`. The `--reload` flag ensures the server restarts when code changes.

```bash
cd backend
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

- **Port**: Defaults to `8000` [backend/.env.example:13]().
- **Logging**: Logs are written to `logs/app.log` if `LOG_TO_FILE` is true [backend/.env.example:40-41]().

### Frontend Development Server

Vite provides Hot Module Replacement (HMR) for a fast development loop.

```bash
cd frontend
npm run dev
```

- **Default URL**: `http://localhost:5173`
- **Proxy Configuration**: Vite is configured to proxy `/api` requests to the backend [Dockerfile:32]().

Sources: [frontend/package.json:6-11](), [backend/.env.example:10-15](), [Dockerfile:109-111]()

---

## Development Workflow Diagram

This diagram illustrates the data flow from code changes to browser updates.

```mermaid
sequenceDiagram
    participant Dev as "Developer"
    participant FS as "File System"
    participant BE as "FastAPI (Uvicorn)"
    participant FE as "React (Vite)"
    participant DB as "PostgreSQL"

    Dev->>FS: Edit backend/app/api/chapters.py
    FS->>BE: Watcher detects change
    BE->>BE: Reload Application
    Note over BE: Preserves Connection Pool

    Dev->>FS: Edit frontend/src/pages/Chapters.tsx
    FS->>FE: HMR Trigger
    FE->>Dev: Update UI in Browser

    Dev->>FE: Click 'Generate Chapter'
    FE->>BE: POST /api/chapters/generate
    BE->>DB: get_db() -> Session
    DB-->>BE: Chapter Data
    BE-->>FE: SSE Stream (Text Chunks)
```

Sources: [backend/app/services/memory_service.py:75-84](), [frontend/package.json:7](), [README.md:193-197]()

---

## Debugging and Tools

### Backend Debugging

1.  **Swagger UI**: Accessible at `http://localhost:8000/docs`. Use this to test individual endpoints without the frontend.
2.  **Logging**: Use the centralized logger.
    ```python
    from app.logger import get_logger
    logger = get_logger(__name__)
    logger.info("Debugging value: %s", value)
    ```
3.  **Database Inspection**: Use `postgresql-client` to query the dev database directly [Dockerfile:56]().

### Frontend Debugging

1.  **React DevTools**: Inspect the component hierarchy and props.
2.  **Network Tab**: Monitor Server-Sent Events (SSE) for real-time AI generation progress.
3.  **Zustand DevTools**: Monitor global state changes in the browser.

### Vector Memory Debugging

If chapter analysis or semantic search fails, check the `MemoryService` initialization logs. It will report the exact path where it searches for the embedding model [backend/app/services/memory_service.py:44,61]().

Sources: [backend/app/services/memory_service.py:102-107](), [backend/app/logger.py:1-11](), [Dockerfile:54-58]()

---

## Common Development Tasks

### 1. Adding a New API Route
- Define the router in `backend/app/api/`.
- Include the router in `backend/app/main.py`.
- Update the frontend `Axios` service in `frontend/src/services/`.

### 2. Modifying Database Schema
- MuMuAINovel uses `SQLAlchemy` for ORM.
- For production-ready changes, use `Alembic` migrations located in `backend/alembic/` [Dockerfile:93-95]().
- Run migrations using `python scripts/migrate.py` [Dockerfile:97]().

### 3. Testing AI Integration
- Configure a provider in `.env` (e.g., `OPENAI_API_KEY`) [backend/.env.example:62]().
- Use the `AIService` to send prompts and handle streaming responses.

Sources: [Dockerfile:93-100](), [backend/.env.example:58-70](), [backend/app/services/memory_service.py:1-11]()

---

# Page: Adding New AI Providers

# Adding New AI Providers

<details>
<summary>Relevant source files</summary>

The following files were used as context for generating this wiki page:

- [backend/app/logger.py](backend/app/logger.py)
- [backend/app/services/ai_clients/anthropic_client.py](backend/app/services/ai_clients/anthropic_client.py)
- [backend/app/services/ai_clients/gemini_client.py](backend/app/services/ai_clients/gemini_client.py)
- [backend/app/services/ai_clients/openai_client.py](backend/app/services/ai_clients/openai_client.py)
- [backend/app/services/ai_metrics.py](backend/app/services/ai_metrics.py)
- [backend/app/services/ai_providers/anthropic_provider.py](backend/app/services/ai_providers/anthropic_provider.py)
- [backend/app/services/ai_providers/gemini_provider.py](backend/app/services/ai_providers/gemini_provider.py)
- [backend/app/services/ai_providers/openai_provider.py](backend/app/services/ai_providers/openai_provider.py)
- [backend/app/services/ai_service.py](backend/app/services/ai_service.py)

</details>



## Purpose and Scope

This document provides a step-by-step guide for developers integrating new LLM providers into the `AIService` architecture. It covers implementing provider-specific clients, integrating them into the unified service layer, and supporting advanced features like Server-Sent Events (SSE) streaming and Model Context Protocol (MCP) tool calling.

---

## System Architecture

The `AIService` class acts as a central dispatcher. It abstracts the complexities of different provider APIs (OpenAI, Anthropic, Gemini) into a common interface used by the rest of the application.

### AI Provider Class Hierarchy

```mermaid
classDiagram
    class BaseAIProvider {
        <<interface>>
        +generate(prompt, model, ...) Dict
        +generate_stream(prompt, model, ...) AsyncGenerator
    }
    class OpenAIProvider {
        -client: OpenAIClient
        +generate()
        +generate_stream()
    }
    class AnthropicProvider {
        -client: AnthropicClient
        +generate()
        +generate_stream()
    }
    class GeminiProvider {
        -client: GeminiClient
        +generate()
        +generate_stream()
    }
    class AIService {
        -providers: Dict
        +generate_text()
        +generate_text_stream()
    }

    BaseAIProvider <|-- OpenAIProvider
    BaseAIProvider <|-- AnthropicProvider
    BaseAIProvider <|-- GeminiProvider
    AIService o-- BaseAIProvider : manages
```

**Sources**: [backend/app/services/ai_service.py:18-21](), [backend/app/services/ai_providers/base_provider.py:1-20]()

---

## Step 1: Implement the Low-Level Client

Each provider requires a client in `backend/app/services/ai_clients/` to handle raw HTTP requests, headers, and payload formatting.

### Implementation Requirements
1. **Initialization**: Accept `api_key`, `base_url`, and `AIClientConfig` [backend/app/services/ai_clients/openai_client.py:11-13]().
2. **Request Logic**: Use `httpx.AsyncClient` for non-blocking I/O [backend/app/services/ai_clients/gemini_client.py:18-25]().
3. **Payload Mapping**: Convert the system's internal message format to the provider's specific schema [backend/app/services/ai_clients/openai_client.py:20-51]().

### Example: Gemini Client Mapping
The Gemini client converts standard OpenAI-style messages to Google's `contents` format:
```python
# backend/app/services/ai_clients/gemini_client.py
contents = []
for msg in messages:
    role = "user" if msg["role"] == "user" else "model"
    contents.append({"role": role, "parts": [{"text": msg["content"]}]})
```
**Sources**: [backend/app/services/ai_clients/gemini_client.py:59-62]()

---

## Step 2: Implement the Provider Wrapper

The Provider class (located in `backend/app/services/ai_providers/`) wraps the client and implements the `BaseAIProvider` interface. This layer is responsible for high-level logic like MCP tool result injection.

### Data Flow: Natural Language to Code Entities

```mermaid
graph TD
    subgraph "Natural Language Space"
        UserPrompt["'Write a story about a cat'"]
        SystemPrompt["'You are a novelist'"]
    end

    subgraph "Code Entity Space"
        AIService["AIService.generate_text()"]
        Provider["OpenAIProvider.generate()"]
        Client["OpenAIClient.chat_completion()"]
        Metrics["AICallMetrics"]
        
        AIService -- "dispatches to" --> Provider
        Provider -- "calls" --> Client
        Client -- "returns JSON" --> Provider
        Provider -- "records usage" --> Metrics
    end

    UserPrompt --> AIService
    SystemPrompt --> AIService
```

**Sources**: [backend/app/services/ai_service.py:156-165](), [backend/app/services/ai_providers/openai_provider.py:17-39]()

---

## Step 3: Integrate into AIService

To make the new provider available to the application, you must register it in the `AIService` constructor and dispatcher.

### 3.1 Registration in `__init__`
Initialize the provider instance if the API key is present.
```python
# backend/app/services/ai_service.py
if self.api_provider == "new_provider" and api_key:
    client = NewProviderClient(api_key, api_base_url, self.config)
    self._new_provider = NewProvider(client)
```
**Sources**: [backend/app/services/ai_service.py:107-124]()

### 3.2 Dispatcher Update
Update `_get_provider` to return the new instance based on the provider string.
```python
# backend/app/services/ai_service.py
def _get_provider(self, provider: Optional[str] = None) -> BaseAIProvider:
    p = normalize_provider(provider or self.api_provider)
    # ... existing checks ...
    if p == "new_provider" and self._new_provider:
        return self._new_provider
    raise ValueError(f"Provider {p} 未初始化")
```
**Sources**: [backend/app/services/ai_service.py:156-165]()

---

## Step 4: Supporting Advanced Features

### 4.1 SSE Streaming
Providers must implement `generate_stream` using an `AsyncGenerator`. This method should yield text chunks or usage dictionaries.

| Feature | Implementation Detail |
| :--- | :--- |
| **Text Chunks** | Yielded as raw strings [backend/app/services/ai_providers/openai_provider.py:108-109]() |
| **Usage Info** | Yielded as `{"usage": {...}}` for metrics tracking [backend/app/services/ai_providers/openai_provider.py:104-105]() |
| **Finish Reason** | Yielded as `{"finish_reason": "...", "done": True}` [backend/app/services/ai_providers/openai_provider.py:100-101]() |

### 4.2 MCP Tool Calling
If the provider supports tools, the `generate_stream` method should:
1. Buffer `tool_calls` from the stream [backend/app/services/ai_providers/anthropic_provider.py:55-69]().
2. Execute tools via `mcp_client.batch_call_tools` upon stream completion [backend/app/services/ai_providers/anthropic_provider.py:77-80]().
3. Inject tool results into a new prompt and recurse to get the final answer [backend/app/services/ai_providers/anthropic_provider.py:82-92]().

### Metrics Integration
Every AI call must be wrapped with `AICallMetrics` to track latency, token usage, and success rates.

```mermaid
sequenceDiagram
    participant S as AIService
    participant M as AICallMetrics
    participant P as BaseAIProvider
    
    S->+M: init(model, provider, prompt_len)
    S->+P: generate()
    P-->>-S: result (content, usage)
    S->+M: finish(success, response_len, usage)
    S->+S: _log_call_metrics(metrics)
```

**Sources**: [backend/app/services/ai_service.py:167-191](), [backend/app/services/ai_metrics.py:72-102]()

---

## Step 5: Verification Checklist

1. **Connection Test**: Ensure the provider responds to a simple prompt.
2. **Streaming Test**: Verify that `generate_text_stream` yields chunks incrementally.
3. **JSON Extraction**: Verify that `call_with_json_retry` works with the new provider's output format [backend/app/services/ai_service.py:1090-1171]().
4. **Metrics Verification**: Check logs to ensure `TokenUsage` and `duration_ms` are correctly recorded [backend/app/services/ai_metrics.py:130-163]().

**Sources**: [backend/app/services/ai_service.py:1015-1088](), [backend/app/logger.py:143-150]()

---

# Page: Creating Custom Prompts

# Creating Custom Prompts

<details>
<summary>Relevant source files</summary>

The following files were used as context for generating this wiki page:

- [backend/app/api/prompt_templates.py](backend/app/api/prompt_templates.py)
- [backend/app/api/prompt_workshop.py](backend/app/api/prompt_workshop.py)
- [backend/app/api/wizard_stream.py](backend/app/api/wizard_stream.py)
- [backend/app/schemas/prompt_template.py](backend/app/schemas/prompt_template.py)
- [backend/app/services/prompt_service.py](backend/app/services/prompt_service.py)
- [backend/app/services/workshop_client.py](backend/app/services/workshop_client.py)
- [frontend/src/pages/MCPPlugins.tsx](frontend/src/pages/MCPPlugins.tsx)
- [frontend/src/pages/PromptTemplates.tsx](frontend/src/pages/PromptTemplates.tsx)
- [frontend/src/pages/PromptWorkshop.tsx](frontend/src/pages/PromptWorkshop.tsx)

</details>



This document explains how to add new prompt templates and modify existing ones in the Prompt system. The system has evolved into a robust infrastructure supporting both static templates and dynamic, user-customizable templates managed via the database and a dedicated "Prompt Workshop" for community sharing.

## Purpose and Scope

This guide covers:
- The architecture of the `PromptService` and the new database-driven template system.
- The **RTCO (Role-Task-Context-Output)** framework used for high-quality prompt engineering.
- Adding and modifying prompt templates via code and the UI.
- The **Prompt Workshop** system for importing/exporting and sharing templates.
- Writing style management and application.

---

## Prompt System Architecture

The prompt system consists of a multi-layer architecture that bridges static code-defined templates with user-defined overrides stored in the database.

### Logic Flow and Entity Space

```mermaid
graph TD
    subgraph "Natural Language Space"
        UserReq["User Intent (e.g., 'Generate Chapter')"]
        StyleReq["Writing Style (e.g., 'Classical')"]
    end

    subgraph "Code Entity Space (Backend)"
        API["app.api.wizard_stream.py"]
        PS["app.services.prompt_service.PromptService"]
        WSM["app.services.prompt_service.WritingStyleManager"]
        DB_Model["app.models.prompt_template.PromptTemplate"]
    end

    subgraph "Data Storage"
        SQLite["SQLite / DB"]
        SystemTemplates["Hardcoded Constants in PromptService"]
    end

    UserReq --> API
    API --> PS
    PS -- "1. Check DB for User Override" --> DB_Model
    DB_Model -- "2. Fallback if not found" --> SystemTemplates
    StyleReq --> WSM
    WSM --> PS
    PS -- "Final Formatted String" --> AIService["app.services.ai_service.AIService"]
```

**Sources:** [backend/app/services/prompt_service.py:25-75](), [backend/app/api/wizard_stream.py:63-72](), [backend/app/api/prompt_templates.py:98-131]()

---

## RTCO Framework Implementation

MuMuAINovel uses the **RTCO (Role, Task, Context, Output)** framework for its V2 prompts to ensure maximum instruction following and structural integrity.

### Template Components
Most system templates (like `WORLD_BUILDING` or `OUTLINE_CREATE`) are structured with XML-like tags for clear separation:

| Tag | Purpose | Example from Code |
| :--- | :--- | :--- |
| `<system>` | Defines the AI's persona/role. | `你是资深的世界观设计师...` [backend/app/services/prompt_service.py:78-80]() |
| `<task>` | Defines the specific mission. | `为小说《{title}》构建完整的世界观设定。` [backend/app/services/prompt_service.py:82-91]() |
| `<input>` / `<worldview>` | Contextual data (P0 priority). | `{title}`, `{theme}`, `{genre}`, `{description}` [backend/app/services/prompt_service.py:93-99]() |
| `<output>` | Strict JSON format and constraints. | `生成包含以下四个字段的JSON对象...` [backend/app/services/prompt_service.py:132-176]() |

**Sources:** [backend/app/services/prompt_service.py:77-191](), [backend/app/services/prompt_service.py:193-317]()

---

## Managing Templates via UI

Users can customize prompts without touching code through the **Prompt Templates** and **Prompt Workshop** interfaces.

### Prompt Templates (Local Customization)
The `PromptTemplates.tsx` page allows users to edit the 20+ system templates. 
- **Path:** `/api/prompt-templates`
- **Logic:** When a user saves a template, it is stored in the `prompt_templates` table with `is_system_default=False`. The `PromptService.get_template_with_fallback` method will then prioritize this record over the hardcoded constant. [backend/app/api/prompt_templates.py:204-245]()

### Prompt Workshop (Community)
The Workshop allows users to download community-curated prompts or share their own.
- **Client/Server Mode:** Controlled by `settings.WORKSHOP_MODE`. [backend/app/services/workshop_client.py:18-20]()
- **Import Flow:** Downloading a workshop item creates a local `WritingStyle` record. [frontend/src/pages/PromptWorkshop.tsx:195-208]()

**Sources:** [frontend/src/pages/PromptTemplates.tsx:96-125](), [backend/app/api/prompt_workshop.py:150-177](), [backend/app/services/workshop_client.py:106-116]()

---

## Writing Style System

Writing styles are appended to the end of base prompts to influence the "flavor" of the text.

### Style Application
The `WritingStyleManager` handles the combination of the base prompt and the style requirements.

```python
@staticmethod
def apply_style_to_prompt(base_prompt: str, style_content: str) -> str:
    """将写作风格应用到基础提示词中"""
    return f"{base_prompt}\n\n{style_content}\n\n请直接输出章节正文内容，不要包含章节标题和其他说明文字。"
```

**Sources:** [backend/app/services/prompt_service.py:9-22]()

### Preset vs. Custom Styles
1. **Presets:** Hardcoded in `WritingStyleManager.PRESET_STYLES` (e.g., Natural, Classical). [backend/app/services/prompt_service.py:25-83]()
2. **Custom:** Stored in the `writing_styles` table, created by users or imported from the Workshop. [backend/app/api/prompt_workshop.py:11-12]()

---

## Adding a New System Prompt (Developer Guide)

### 1. Define the Constant
Add the RTCO-structured string to `PromptService` in `backend/app/services/prompt_service.py`.

### 2. Add Helper Logic
Implement a builder method that handles variable injection and database lookups.

```python
@classmethod
async def build_custom_task_prompt(cls, project: Any, user_id: str, db: AsyncSession) -> str:
    # 1. Fetch template (DB or Code)
    template = await cls.get_template_with_fallback("CUSTOM_TASK_KEY", user_id, db)
    
    # 2. Format with project data
    return template.format(
        title=project.title,
        theme=project.theme,
        # ... other vars
    )
```

**Sources:** [backend/app/services/prompt_service.py:49-73]()

### 3. Handle JSON Cleaning
When using prompts that return JSON, always use the `AIService._clean_json_response` method in the API layer to strip markdown markers (e.g., ` ```json `) before parsing.

```python
# Inside an API generator
cleaned_text = user_ai_service._clean_json_response(accumulated_text)
data = json.loads(cleaned_text)
```

**Sources:** [backend/app/api/wizard_stream.py:155-162]()

---

## Summary of Key Entities

| Component | File Path | Role |
| :--- | :--- | :--- |
| **PromptService** | `backend/app/services/prompt_service.py` | Central logic for template retrieval and formatting. |
| **PromptWorkshopItem** | `backend/app/models/prompt_workshop.py` | DB model for community-shared prompts. |
| **PromptTemplates UI** | `frontend/src/pages/PromptTemplates.tsx` | Local editor for system prompts. |
| **Workshop API** | `backend/app/api/prompt_workshop.py` | Endpoints for cloud prompt synchronization. |
| **SSE Tracker** | `backend/app/utils/sse_response.py` | Manages progress reporting during prompt generation. |

**Sources:** [backend/app/services/prompt_service.py:1-25](), [backend/app/api/prompt_workshop.py:1-21](), [frontend/src/pages/PromptTemplates.tsx:36-55]()

---

# Page: Troubleshooting

# Troubleshooting

<details>
<summary>Relevant source files</summary>

The following files were used as context for generating this wiki page:

- [backend/app/api/settings.py](backend/app/api/settings.py)
- [backend/app/database.py](backend/app/database.py)
- [backend/app/models/__init__.py](backend/app/models/__init__.py)
- [backend/app/schemas/settings.py](backend/app/schemas/settings.py)
- [backend/app/services/ai_service.py](backend/app/services/ai_service.py)
- [backend/scripts/setup_postgres.py](backend/scripts/setup_postgres.py)
- [frontend/src/pages/Settings.tsx](frontend/src/pages/Settings.tsx)

</details>



This page documents common issues encountered when deploying, configuring, and using MuMuAINovel, along with their diagnostic steps and solutions. It covers problems related to deployment, database connections, AI provider integration, authentication, streaming operations, and performance.

---

## Deployment Issues

### Docker Container Won't Start

**Symptoms:**
- Container exits immediately after starting.
- `docker-compose up` shows error messages.
- Container status shows "Exited (1)".

**Diagnostic Steps:**
```bash
# Check container logs
docker-compose logs ai-story

# Check container status
docker-compose ps
```

**Common Causes and Solutions:**

| Issue | Cause | Solution |
|-------|-------|----------|
| Missing `.env` file | Configuration file not mounted | Create `.env` from `.env.example` [README.md:118-183](). |
| Port conflict | Port 8000 already in use | Change host port mapping in `docker-compose.yml` [README.md:268-272](). |
| Volume mount errors | Directory permissions | Ensure `./data` and `./logs` exist and are writable. |

**Sources:** [README.md:118-183](), [README.md:268-272]()

---

## Configuration and AI Issues

### AI Provider API Key Errors

**Symptoms:**
- Error message: "API key not configured" or "Invalid API key".
- Project wizard fails at Step 1 (world building).

**AI Configuration Flow:**

The `AIService` acts as a unified interface, initializing specific provider clients (OpenAI, Anthropic, Gemini) based on the user's configuration stored in the database or `.env` defaults.

Title: AI Service Initialization and Provider Routing
```mermaid
graph TD
    subgraph "Configuration Source"
        ENV[".env / app_settings"]
        DB["Settings Table<br/>(user_id)"]
    end

    subgraph "Backend Entity: AIService"
        Init["AIService.__init__<br/>[app/services/ai_service.py:74-125]"]
        GetProv["_get_provider()<br/>[app/services/ai_service.py:156-165]"]
    end

    subgraph "Provider Clients"
        OAI["OpenAIProvider<br/>(OpenAIClient)"]
        ANT["AnthropicProvider<br/>(AnthropicClient)"]
        GEM["GeminiProvider<br/>(GeminiClient)"]
    end

    ENV --> Init
    DB --> Init
    Init --> GetProv
    GetProv -->|"provider=='openai'"| OAI
    GetProv -->|"provider=='anthropic'"| ANT
    GetProv -->|"provider=='gemini'"| GEM
```

**Solution:**
1. **Verify API Key Format:** Ensure keys start correctly (e.g., `sk-` for OpenAI).
2. **Check Base URL:** Proxies must include `/v1` suffix usually [README.md:273-336]().
3. **Model Names:** Ensure model strings match provider requirements (e.g., `gpt-4o-mini` vs `gpt-4o`) [README.md:338-346]().

**Sources:** [backend/app/services/ai_service.py:74-165](), [README.md:273-346]()

### API Key Presets and Active Configuration

**Symptoms:**
- Settings page shows "Config changed, preset deactivated".
- Testing a preset fails while the current config works.

**Implementation Detail:**
The frontend `Settings.tsx` tracks `activePresetId`. If a user manually edits and saves the current configuration, the backend automatically cancels the active preset to prevent inconsistency [frontend/src/pages/Settings.tsx:161-171]().

**Sources:** [frontend/src/pages/Settings.tsx:161-171](), [backend/app/api/settings.py:162-192]()

---

## Database Issues

### Session Connection Leaks

**Symptoms:**
- Error: "Too many connections" or "Connection pool exhausted".
- Log shows warning: "活跃会话数过多" (Too many active sessions).

**PostgreSQL Session Lifecycle:**
The `get_db` dependency manages the lifecycle. A common failure point is Server-Sent Events (SSE) where a user disconnects, triggering a `GeneratorExit` [backend/app/database.py:176-185]().

Title: Database Session Management and Cleanup
```mermaid
sequenceDiagram
    participant Req as "FastAPI Request"
    participant GDB as "get_db() Dependency<br/>[app/database.py:145]"
    participant Ses as "AsyncSession<br/>(SQLAlchemy)"
    participant Pool as "PostgreSQL Connection Pool"

    Req->>GDB: Request Session
    GDB->>Pool: Acquire Connection
    GDB->>Ses: Create Session
    Note over GDB: _session_stats['active']++
    GDB-->>Req: yield session
    
    alt Normal Completion
        Req->>GDB: Request Finished
        GDB->>Ses: close()
    else SSE Disconnect (GeneratorExit)
        Req--xGDB: Connection Closed
        GDB->>Ses: rollback() if in_transaction
        GDB->>Ses: close()
        Note over GDB: _session_stats['generator_exits']++
    end
    
    GDB->>Pool: Release Connection
    Note over GDB: _session_stats['active']--
```

**Diagnostic Thresholds:**
- **Warning:** 50 active sessions [backend/app/config.py:59-61]().
- **Critical:** 100 active sessions (Leak threshold) [backend/app/config.py:59-61]().

**Sources:** [backend/app/database.py:145-224](), [backend/app/config.py:59-61]()

### PostgreSQL Connection Failures

**Symptoms:**
- Error: "could not connect to server: Connection refused".
- Application fails to start.

**Database Configuration:**
The system uses a shared engine for PostgreSQL but implements data isolation via `user_id` columns in every table [backend/app/database.py:45-142]().

**Checklist:**
1. **DATABASE_URL:** Must use `postgresql+asyncpg://` [backend/.env.example:27-28]().
2. **Container Networking:** Use the service name (e.g., `postgres`) as the host, not `localhost`.
3. **Pool Settings:** Default `pool_size` is 30 with `max_overflow` of 20 [backend/app/config.py:46-58]().

**Sources:** [backend/app/database.py:45-142](), [backend/app/config.py:46-58](), [backend/.env.example:27-28]()

---

## Authentication Issues

### Local vs. OAuth Failures

**Symptoms:**
- "用户名或密码错误" (Invalid username/password).
- LinuxDO login redirects to an error page.

**Authentication Logic:**
- **Local Auth:** Compares against `LOCAL_AUTH_USERNAME` and `LOCAL_AUTH_PASSWORD` in `.env` [README.md:328-332]().
- **OAuth:** Requires `LINUXDO_CLIENT_ID`, `LINUXDO_CLIENT_SECRET`, and a **matching** `LINUXDO_REDIRECT_URI` [README.md:322-327]().

**Redirect URI Requirement:**
The URI in the LinuxDO dashboard must exactly match the `.env` value (usually `http://domain:port/api/auth/callback`).

**Sources:** [README.md:322-332](), [backend/app/api/settings.py:54-65]()

---

## Performance and Resource Limits

### Memory Usage

**Symptoms:**
- Container killed by OOM (Out of Memory).
- Slow performance under concurrent load.

**Resource Components:**
- **FastAPI/Python:** ~200-500MB.
- **PostgreSQL Pool:** 50 connections (configured) [backend/app/database.py:107-118]().
- **Embeddings/ChromaDB:** ~400-600MB when active.

**Optimization:**
- Set `DATABASE_POOL_SIZE` and `DATABASE_MAX_OVERFLOW` according to available RAM [backend/app/config.py:46-58]().
- Use `pool_recycle` (default 1800s) to prevent stale connections from hogging resources [backend/app/database.py:99-100]().

**Sources:** [backend/app/database.py:45-142](), [backend/app/config.py:46-58]()

---

## Logging and Monitoring

### Health Endpoint

The system provides a health check that includes detailed database statistics [backend/app/database.py:382-473]().

**Monitoring Statistics:**
- `checked_out`: Connections currently in use.
- `overflow`: Connections created beyond `pool_size`.
- `active`: Current application-level sessions.

**Diagnostic Commands:**
```bash
# View session stats in logs
docker-compose logs ai-story | grep "会话"

# View pool usage
docker-compose logs ai-story | grep "pool_size"
```

**Sources:** [backend/app/database.py:382-473](), [backend/app/database.py:163-170]()

---

# Page: License

# License

<details>
<summary>Relevant source files</summary>

The following files were used as context for generating this wiki page:

- [LICENSE](LICENSE)

</details>



This document describes the software license governing the MuMuAINovel project, the rights granted to users and developers, and the obligations that must be followed when using, modifying, or distributing the software.

---

## Overview

MuMuAINovel is licensed under the **GNU General Public License version 3** (GPL-3.0). The complete license text is located in [LICENSE:1-675](). This is a strong copyleft license that ensures the software remains free and open source.

### License File Location

```
LICENSE                    # Full GNU GPL v3 text [LICENSE:1-675]
```

**Sources:** [LICENSE:1-675]()

---

## Key License Provisions

The GNU GPL v3 grants four essential freedoms to all users:

| Freedom | Description | GPL v3 Section |
|---------|-------------|----------------|
| **Freedom 0** | Run the program for any purpose | Section 2 [LICENSE:154-162]() |
| **Freedom 1** | Study and modify the source code | Sections 1, 2 [LICENSE:112-162]() |
| **Freedom 2** | Redistribute copies | Section 4 [LICENSE:195-207]() |
| **Freedom 3** | Distribute modified versions | Section 5 [LICENSE:208-244]() |

### Core Principles

The license is built on the following principles as stated in the Preamble [LICENSE:8-67]():

1. **Free Software**: "Free" refers to freedom, not price [LICENSE:22-27]()
2. **Copyleft**: Modifications must also be licensed under GPL v3 [LICENSE:222-228]()
3. **Source Availability**: "Corresponding Source" code must be accessible [LICENSE:134-152]()
4. **No Additional Restrictions**: Cannot impose further limitations on recipients [LICENSE:388-405]()

**Sources:** [LICENSE:1-70](), [LICENSE:112-162](), [LICENSE:195-244](), [LICENSE:388-405]()

---

## License Scope Diagram

The following diagram shows which components of the MuMuAINovel system are covered by the GPL v3 license versus external dependencies and user data:

```mermaid
graph TB
    subgraph "GPL_v3_Licensed_Components"
        [Backend_App] --> [API_Routers]
        [Backend_App] --> [AI_Services]
        [Frontend_App] --> [React_Components]
        [Frontend_App] --> [API_Client]
        [Docker_Config]
    end
    
    subgraph "User_Generated_Content_Not_Covered"
        [User_DB]
        [Novel_Text]
        [App_Logs]
    end
    
    subgraph "Third_Party_Dependencies_Separate_Licenses"
        [FastAPI_SQLAlchemy]
        [React_AntDesign]
        [AI_Provider_APIs]
    end
    
    [Backend_App] -. "Uses" .-> [FastAPI_SQLAlchemy]
    [Frontend_App] -. "Uses" .-> [React_AntDesign]
    [Backend_App] -. "Calls" .-> [AI_Provider_APIs]
    
    [Backend_App] -. "Creates" .-> [User_DB]
    [Backend_App] -. "Writes" .-> [App_Logs]
```

**Sources:** [LICENSE:1-675]()

---

## User Rights

### What You Can Do

As a user of MuMuAINovel under GPL v3, you have the following rights as defined in [LICENSE:154-207]():

1. **Use the Software**: Run MuMuAINovel for any purpose, commercial or personal [LICENSE:154-158]().
2. **Access Source Code**: The "Corresponding Source" is the preferred form for making modifications [LICENSE:112-114]().
3. **Modify the Software**: Create "modified versions" based on the original [LICENSE:84-88]().
4. **Redistribute**: Convey verbatim copies or modified versions [LICENSE:195-244]().
5. **No Warranty**: The software is provided "AS IS" without warranty [LICENSE:591-599]().

### Content Ownership

**Important**: The GPL v3 only applies to the MuMuAINovel software itself. Content you create using the software (novels, characters, outlines, etc.) belongs to you and is not subject to GPL v3 licensing requirements as stated in [LICENSE:159-162]():

> "The output from running a covered work is covered by this License only if the output, given its content, constitutes a covered work."

User-generated novels are not "covered works" and remain under your copyright.

**Sources:** [LICENSE:84-114](), [LICENSE:154-207](), [LICENSE:591-599]()

---

## Developer Obligations

### Compliance Decision Tree

This diagram maps the legal requirements of the GPL v3 [LICENSE:195-296]() to development actions.

```mermaid
flowchart TD
    [Start] --> [Modifying_or_Distributing?]
    
    [Modifying_or_Distributing?] -->| "No - Use Only" | [No_Obligations]
    [Modifying_or_Distributing?] -->| "Yes" | [Distributing_to_Others?]
    
    [Distributing_to_Others?] -->| "No - Private" | [Private_Use_Section_2]
    
    [Distributing_to_Others?] -->| "Yes" | [Distribution_Type]
    
    [Distribution_Type] -->| "Binary_Form" | [Binary_Reqs_Section_6]
    [Distribution_Type] -->| "Source_Form" | [Source_Reqs_Section_5]
    
    [Binary_Reqs_Section_6] --> [Copyleft_Effect]
    [Source_Reqs_Section_5] --> [Copyleft_Effect]
    
    [Copyleft_Effect] --> [Adding_Proprietary_Code?]
    
    [Adding_Proprietary_Code?] -->| "Yes" | [License_Violation_Section_10]
    [Adding_Proprietary_Code?] -->| "No" | [Compliant_Distribution]
```

**Sources:** [LICENSE:154-177](), [LICENSE:195-207](), [LICENSE:208-244](), [LICENSE:245-296]()

---

## Modification and Distribution Requirements

### If You Modify the Code

When modifying MuMuAINovel, you must comply with Section 5 [LICENSE:208-234]():

| Requirement | Description | Code Implementation |
|-------------|-------------|---------|
| **Mark Changes** | Prominently notice modifications | [LICENSE:211-213]() |
| **License Notice** | State the code is GPL v3 licensed | [LICENSE:214-216]() |
| **Copyleft** | License entire work under GPL v3 | [LICENSE:222-228]() |
| **Copyright Notice** | Maintain existing copyright notices | [LICENSE:196-197]() |

### If You Distribute Modified Code

Distribution (conveying) triggers additional obligations per Section 4 [LICENSE:195-207]() and Section 6 [LICENSE:245-296]():

```mermaid
graph LR
    [Modified_Code] --> [Include_Source_Section_6]
    [Modified_Code] --> [Include_LICENSE_File]
    [Modified_Code] --> [Document_Modifications]
    [Modified_Code] --> [Maintain_Notices]
    [Modified_Code] --> [No_Extra_Restrictions]
    
    [Include_Source_Section_6] --> [Compliant_Conveying]
    [Include_LICENSE_File] --> [Compliant_Conveying]
    [Document_Modifications] --> [Compliant_Conveying]
    [Maintain_Notices] --> [Compliant_Conveying]
    [No_Extra_Restrictions] --> [Compliant_Conveying]
```

**Sources:** [LICENSE:195-207](), [LICENSE:208-244](), [LICENSE:245-296]()

---

## Common Use Cases

### Case 1: Running MuMuAINovel for Personal Use

**Scenario**: You deploy MuMuAINovel using Docker and use it to write novels.

**Obligations**: None. You can use the software freely without any licensing obligations.

**Reference**: [LICENSE:159-162]()

---

### Case 2: Deploying as a Service

**Scenario**: You host MuMuAINovel on a server and let others access it via web interface.

**GPL v3 Position**: Mere interaction with a user through a computer network, with no transfer of a copy, is not conveying [LICENSE:100-101]().

**Important**: If you modify the code, you are not required to release your modifications unless you also distribute the software itself. However, consider AGPL compatibility mentioned in Section 13 [LICENSE:552-561]() if combining with AGPL code.

**Reference**: [LICENSE:99-101](), [LICENSE:552-561]()

---

### Case 3: Forking and Distributing Modified Version

**Scenario**: You fork MuMuAINovel, add custom features, and distribute your version.

**Obligations**:
1. License your entire work under GPL v3 [LICENSE:222-228]().
2. Provide complete source code to recipients [LICENSE:245-250]().
3. Include the GPL v3 license text [LICENSE:1-675]().
4. Document your modifications prominently [LICENSE:211-213]().
5. Maintain all copyright notices from the original [LICENSE:196-197]().

**Reference**: [LICENSE:208-234]()

---

### Case 4: Integrating into Proprietary Software

**Scenario**: You want to include MuMuAINovel code in a closed-source commercial product.

**Answer**: **Not permitted** under GPL v3. 

The copyleft nature of GPL v3 means any work that includes GPL-licensed code must also be licensed under GPL v3 [LICENSE:222-228]():

> "You must license the entire work, as a whole, under this License to anyone who comes into possession of a copy."

**Reference**: [LICENSE:222-228](), [LICENSE:669-674]()

---

## Component-Specific License Notes

### Third-Party Dependencies

MuMuAINovel uses libraries with compatible licenses. MIT-licensed dependencies can be combined with GPL v3 code per Section 7 [LICENSE:345-359]().

| Component | License Type | Compatibility |
|-----------|--------------|---------------|
| FastAPI | MIT | Compatible ✓ |
| SQLAlchemy | MIT | Compatible ✓ |
| React | MIT | Compatible ✓ |
| Ant Design | MIT | Compatible ✓ |

**Note**: External AI API services (OpenAI, Gemini, Claude) are accessed via network calls and are not included in the GPL licensing scope.

**Sources:** [LICENSE:345-405]()

---

## Warranty Disclaimer

MuMuAINovel is provided **without warranty** as explicitly stated in Sections 15 and 16 [LICENSE:589-619]():

### Key Points

1. **NO WARRANTY**: The software is provided "AS IS" [LICENSE:595-599]().
2. **NO LIABILITY**: Developers are not liable for damages [LICENSE:605-619]().
3. **NO GUARANTEE**: No guarantee of fitness for any purpose [LICENSE:595-599]().

**Sources:** [LICENSE:589-619]()

---

## How to Comply

### For End Users

1. No action required - use the software freely [LICENSE:154-158]().
2. Your generated content belongs to you [LICENSE:159-162]().

### For Distributors (Modified Versions)

**Checklist**:

- [ ] Include complete source code [LICENSE:245-250]()
- [ ] Include [LICENSE:1-675]() file
- [ ] Add copyright notices for your modifications [LICENSE:211-213]()
- [ ] Document all changes made [LICENSE:211-213]()
- [ ] License entire work under GPL v3 [LICENSE:222-228]()
- [ ] Do not add additional restrictions [LICENSE:388-405]()

**Sources:** [LICENSE:195-244](), [LICENSE:623-675]()

---

# Page: Glossary

# Glossary

<details>
<summary>Relevant source files</summary>

The following files were used as context for generating this wiki page:

- [README.md](README.md)
- [backend/.env.example](backend/.env.example)
- [backend/app/api/chapters.py](backend/app/api/chapters.py)
- [backend/app/api/foreshadows.py](backend/app/api/foreshadows.py)
- [backend/app/api/mcp_plugins.py](backend/app/api/mcp_plugins.py)
- [backend/app/api/outlines.py](backend/app/api/outlines.py)
- [backend/app/api/wizard_stream.py](backend/app/api/wizard_stream.py)
- [backend/app/mcp/facade.py](backend/app/mcp/facade.py)
- [backend/app/mcp/status_sync.py](backend/app/mcp/status_sync.py)
- [backend/app/models/foreshadow.py](backend/app/models/foreshadow.py)
- [backend/app/schemas/chapter.py](backend/app/schemas/chapter.py)
- [backend/app/schemas/foreshadow.py](backend/app/schemas/foreshadow.py)
- [backend/app/schemas/outline.py](backend/app/schemas/outline.py)
- [backend/app/services/chapter_context_service.py](backend/app/services/chapter_context_service.py)
- [backend/app/services/chapter_regenerator.py](backend/app/services/chapter_regenerator.py)
- [backend/app/services/foreshadow_service.py](backend/app/services/foreshadow_service.py)
- [backend/app/services/json_helper.py](backend/app/services/json_helper.py)
- [backend/app/services/mcp_test_service.py](backend/app/services/mcp_test_service.py)
- [backend/app/services/plot_analyzer.py](backend/app/services/plot_analyzer.py)
- [backend/app/services/prompt_service.py](backend/app/services/prompt_service.py)
- [frontend/package-lock.json](frontend/package-lock.json)
- [frontend/package.json](frontend/package.json)
- [frontend/src/components/ExpansionPlanEditor.tsx](frontend/src/components/ExpansionPlanEditor.tsx)
- [frontend/src/pages/Chapters.tsx](frontend/src/pages/Chapters.tsx)
- [frontend/src/pages/Outline.tsx](frontend/src/pages/Outline.tsx)
- [frontend/src/services/api.ts](frontend/src/services/api.ts)
- [frontend/src/store/hooks.ts](frontend/src/store/hooks.ts)
- [frontend/src/types/index.ts](frontend/src/types/index.ts)

</details>



This glossary defines technical terms, architectural patterns, and domain-specific jargon used within the MuMuAINovel codebase. It serves as a reference for onboarding engineers to understand the mapping between natural language features and their underlying code implementations.

## 1. Core Architectural Patterns

### Outline Modes (大纲模式)
The system supports two distinct workflows for transforming high-level plot points into chapter content, governed by the `outline_mode` field in the `Project` model [backend/app/models/project.py]().

| Term | Code Entity | Description |
|:---|:---|:---|
| **One-to-One** | `one-to-one` | A legacy or simple mode where one `Outline` entity maps directly to exactly one `Chapter`. Creating an outline automatically triggers chapter stub creation [backend/app/api/outlines.py:75-87](). |
| **One-to-Many** | `one-to-many` | The advanced workflow where one high-level `Outline` (e.g., "The Hero's Journey Begins") is expanded into multiple detailed `Chapters` via an intermediate `ExpansionPlan` [backend/app/services/chapter_context_service.py:15-16](). |

### Context Building (上下文构建)
To maintain narrative consistency, the system dynamically gathers project metadata, character details, and previous plot points before calling an LLM.

**Context Construction Flow**
```mermaid
graph TD
    A["Request: Generate Chapter"] --> B["ContextBuilder Selection"]
    B -- "Project.outline_mode == 'one-to-many'" --> C["OneToManyContextBuilder"]
    B -- "Project.outline_mode == 'one-to-one'" --> D["OneToOneContextBuilder"]
    C --> E["Fetch StoryMemory & PlotAnalysis"]
    D --> E
    E --> F["Format via PromptService"]
    F --> G["AIService.generate_text_stream"]
```
*Sources: [backend/app/services/chapter_context_service.py:14-17](), [backend/app/api/chapters.py:14-17]()*

---

## 2. AI & Prompt Subsystem

### RTCO Framework
A proprietary prompting structure used in `PromptService` [backend/app/services/prompt_service.py:75-78]() to ensure structured and reliable LLM outputs.
*   **R (Role):** System role definition (e.g., "Senior World Designer").
*   **T (Task):** Specific creative objective.
*   **C (Constraints):** Formatting and content taboos.
*   **O (Output):** Strict JSON schema requirements.

### SSE (Server-Sent Events)
The primary protocol for real-time AI interactions. Unlike standard REST, it allows the backend to "push" incremental updates (tokens, progress percentages) to the frontend [backend/app/utils/sse_response.py]().

*   **WizardProgressTracker:** A utility class used in stream generators to send standardized progress updates (e.g., `preparing`, `generating`, `parsing`) to the UI [backend/app/api/wizard_stream.py:38]().
*   **SSEPostClient:** The frontend utility in `sseClient.ts` that handles the `EventSource`-like behavior over POST requests [frontend/src/utils/sseClient.ts]().

### MCP (Model Context Protocol)
An integration layer that allows the LLM to call external "tools" or plugins during generation.
*   **MCPPlugin:** Database model storing configuration for external tool servers [backend/app/api/mcp_plugins.py]().
*   **Tool Discovery:** The system dynamically queries MCP servers to find available functions the AI can invoke [backend/app/services/mcp_test_service.py]().

---

## 3. Narrative Domain Terms

### Expansion Plan (章节规划)
In `one-to-many` mode, the `ExpansionPlan` acts as a bridge between a vague outline and concrete chapters. It contains a `scenes` array, `key_events`, and `character_involved` [frontend/src/pages/Outline.tsx:81-96]().

### Plot Analyzer & Story Memory
The "Long-term Memory" system of the novel.
*   **PlotAnalyzer:** Extracts semantic meaning from written chapters [backend/app/services/plot_analyzer.py]().
*   **StoryMemory:** Stores extracted plot points, character states, and world changes to prevent AI "hallucinations" about past events [backend/app/models/memory.py:27]().

### Foreshadowing (伏笔管理)
A specialized service for tracking unresolved plot threads.
*   **Foreshadow:** A model representing a "hook" planted in a chapter that needs to be "resolved" later [backend/app/models/foreshadow.py]().
*   **ForeshadowService:** Analyzes text to detect when a foreshadowing element is introduced or closed [backend/app/services/foreshadow_service.py]().

---

## 4. Technical Components Mapping

### From Feature to Code Entity

| Feature Name (CN) | Technical Term | Primary Code Files |
|:---|:---|:---|
| **项目向导** | Project Wizard | `wizard_stream.py`, `ProjectWizardNew.tsx` |
| **灵感模式** | Inspiration Mode | `Inspiration.tsx`, `inspiration.py` |
| **提示词工坊** | Prompt Workshop | `PromptWorkshop.tsx`, `prompt_service.py` |
| **拆书功能** | Book Import / Dissection | `BookImport.tsx`, `book_import_service.py` |
| **写作风格** | Writing Styles | `WritingStyleManager`, `writing_style.py` |

### Data Flow: AI Generation to Database
This diagram illustrates how a "Generate" request moves through the system.

```mermaid
sequenceDiagram
    participant UI as "Chapters.tsx"
    participant API as "api/chapters.py"
    participant AS as "AIService"
    participant PS as "PromptService"
    participant DB as "PostgreSQL (AsyncSession)"

    UI->>API: POST /generate (SSE)
    API->>PS: build_prompt(context)
    PS-->>API: Formatted Prompt (RTCO)
    API->>AS: generate_text_stream()
    loop Token Streaming
        AS-->>API: text_chunk
        API-->>UI: data: {"content": "..."}
    end
    API->>DB: update Chapter(content, word_count)
    DB-->>API: Commit Transaction
    API-->>UI: event: finish
```
*Sources: [backend/app/api/chapters.py:77-102](), [backend/app/services/ai_service.py](), [frontend/src/pages/Chapters.tsx:96-113]()*

---

## 5. Database & State Terms

### Connection Pool (连接池)
The system uses `SQLAlchemy` with `asyncpg`. Configuration parameters like `DATABASE_POOL_SIZE` and `DATABASE_MAX_OVERFLOW` in the `.env` file control how many concurrent database connections are maintained [backend/.env.example:294-295]().

### User Isolation (多用户隔离)
Every API request is intercepted by `AuthMiddleware`. The `user_id` is extracted from the session and used in every query (e.g., `where(Project.user_id == user_id)`) to ensure users cannot see each other's novels [backend/app/api/common.py:13]().

### Sync Hooks
Custom React hooks in `frontend/src/store/hooks.ts` that encapsulate the logic for fetching data and updating the `Zustand` global store.
*   **useChapterSync:** Handles fetching chapter lists and updating the local state when a chapter is edited [frontend/src/store/hooks.ts]().
*   **useOutlineSync:** Manages the state of the plot structure [frontend/src/pages/Outline.tsx:172-176]().

*Sources: [backend/app/database.py](), [backend/app/api/common.py](), [frontend/src/store/hooks.ts]()*