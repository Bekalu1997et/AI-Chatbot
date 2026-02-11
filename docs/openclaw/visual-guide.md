# OpenClaw Visual Study Guide

A visual reference for studying OpenClaw's architecture and components.

## 🏗️ System Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                      MESSAGING PLATFORMS                        │
│  WhatsApp │ Telegram │ Discord │ Slack │ Signal │ iMessage...  │
└────────────────────────┬────────────────────────────────────────┘
                         │
         ┌───────────────▼───────────────┐
         │    CHANNEL ADAPTERS           │
         │  - WhatsAppChannel            │
         │  - TelegramChannel            │
         │  - DiscordChannel             │
         │  - SlackChannel               │
         └───────────────┬───────────────┘
                         │
         ┌───────────────▼───────────────┐
         │      GATEWAY                  │
         │  (Control Plane)              │
         │  ┌─────────────────────────┐  │
         │  │ WebSocket Server        │  │
         │  │ ws://localhost:18789    │  │
         │  ├─────────────────────────┤  │
         │  │ Session Manager         │  │
         │  │ - Session routing       │  │
         │  │ - Context persistence   │  │
         │  ├─────────────────────────┤  │
         │  │ Authentication          │  │
         │  │ - DM pairing            │  │
         │  │ - Token/Password        │  │
         │  │ - Tailscale identity    │  │
         │  ├─────────────────────────┤  │
         │  │ Configuration           │  │
         │  └─────────────────────────┘  │
         └───────────┬───────────────────┘
                     │
     ┌───────────────┼───────────────┐
     │               │               │
     ▼               ▼               ▼
┌─────────┐   ┌──────────┐   ┌──────────┐
│  AGENT  │   │  TOOLS   │   │  NODES   │
│         │   │          │   │          │
│ Pi Agent│   │ Browser  │   │ macOS    │
│         │   │ Canvas   │   │ iOS      │
│ - AI    │   │ Cron     │   │ Android  │
│ - Tools │   │ Webhooks │   │          │
│ - Stream│   │ Skills   │   │ Camera   │
└─────────┘   └──────────┘   └──────────┘
```

## 🔄 Message Flow

```
┌──────────────┐
│ User sends   │
│ message on   │
│ WhatsApp     │
└──────┬───────┘
       │
       ▼
┌──────────────────┐
│ WhatsApp Channel │
│ receives message │
└──────┬───────────┘
       │
       ▼
┌─────────────────────┐
│ Gateway routes to   │
│ correct session     │
└──────┬──────────────┘
       │
       ▼
┌─────────────────────┐
│ Session loads       │
│ conversation context│
└──────┬──────────────┘
       │
       ▼
┌─────────────────────┐
│ Agent processes     │
│ with AI model       │
└──────┬──────────────┘
       │
       ▼
┌─────────────────────┐
│ Agent executes      │
│ tools if needed     │
└──────┬──────────────┘
       │
       ▼
┌─────────────────────┐
│ Response streams    │
│ back through        │
│ Gateway             │
└──────┬──────────────┘
       │
       ▼
┌─────────────────────┐
│ Channel sends       │
│ response to user    │
└─────────────────────┘
```

## 📊 Component Interaction Matrix

| Component | Interacts With | Communication Method | Purpose |
|-----------|----------------|---------------------|---------|
| **Channels** | Gateway | WebSocket/HTTP | Send/receive messages |
| **Gateway** | Agent | RPC | Process messages |
| **Gateway** | Nodes | WebSocket RPC | Execute device actions |
| **Gateway** | Tools | Direct calls | Execute capabilities |
| **Agent** | AI Models | API | Generate responses |
| **Agent** | Tools | Function calls | Execute tools |
| **Tools** | External APIs | HTTP/WebSocket | Fetch data/perform actions |
| **Skills** | Gateway | Registry | Register capabilities |

## 🎯 Key Subsystems Breakdown

### 1. Gateway Subsystem
```
Gateway
├── Server (WebSocket + HTTP)
├── Router (Message routing)
├── SessionManager
│   ├── Session storage (SQLite)
│   ├── Context management
│   └── Configuration
├── ChannelManager
│   ├── Channel registry
│   └── Channel lifecycle
├── AuthManager
│   ├── DM pairing
│   ├── Token auth
│   └── Tailscale identity
└── EventBus (Internal events)
```

### 2. Agent Subsystem
```
Agent (Pi)
├── ModelAdapter
│   ├── Anthropic (Claude)
│   ├── OpenAI (GPT)
│   └── Custom models
├── ToolExecutor
│   ├── Function calling
│   └── Streaming execution
├── ContextManager
│   ├── Token counting
│   ├── Pruning
│   └── Summarization
└── Failover
    ├── Retry logic
    └── Model fallback
```

### 3. Channel Subsystem
```
Channels
├── WhatsApp (Baileys)
│   ├── QR auth
│   └── Media handling
├── Telegram (grammY)
│   ├── Bot token
│   └── Inline keyboards
├── Discord (discord.js)
│   ├── Bot token
│   └── Server/channels
├── Slack (Bolt)
│   ├── OAuth
│   └── Blocks
└── ...more channels
```

### 4. Tools Subsystem
```
Tools
├── Browser
│   ├── Chrome CDP
│   └── Screenshots
├── Canvas (A2UI)
│   ├── Render
│   └── Eval
├── Cron
│   └── Scheduler
├── Webhooks
│   ├── Inbound
│   └── Outbound
└── Skills
    ├── Bundled
    ├── Managed (ClawHub)
    └── Workspace
```

### 5. Nodes Subsystem
```
Nodes
├── macOS
│   ├── system.run
│   ├── system.notify
│   ├── Canvas
│   ├── Camera
│   └── Screen record
├── iOS
│   ├── Voice Wake
│   ├── Talk Mode
│   └── Camera
└── Android
    ├── Talk Mode
    └── Camera
```

## 🔐 Security Layers

```
┌────────────────────────────────┐
│ Layer 5: Per-Session Elevated │
│ (sudo for sensitive commands)  │
└────────────────┬───────────────┘
                 │
┌────────────────▼───────────────┐
│ Layer 4: Gateway Auth          │
│ (Token/Password/Tailscale)     │
└────────────────┬───────────────┘
                 │
┌────────────────▼───────────────┐
│ Layer 3: DM Pairing            │
│ (Pairing codes for new users)  │
└────────────────┬───────────────┘
                 │
┌────────────────▼───────────────┐
│ Layer 2: Channel Allowlists    │
│ (Per-channel user filtering)   │
└────────────────┬───────────────┘
                 │
┌────────────────▼───────────────┐
│ Layer 1: Platform Auth         │
│ (WhatsApp QR, Telegram token)  │
└────────────────────────────────┘
```

## 📈 Session Lifecycle

```
┌─────────────┐
│ New Message │
└──────┬──────┘
       │
       ▼
  ┌─────────┐      No      ┌─────────────┐
  │ Session ├─────────────→│ Create      │
  │ Exists? │              │ New Session │
  └────┬────┘              └──────┬──────┘
       │ Yes                      │
       └──────────┬───────────────┘
                  │
                  ▼
         ┌────────────────┐
         │ Load Context   │
         │ from DB        │
         └────────┬───────┘
                  │
                  ▼
         ┌────────────────┐
         │ Add Message    │
         │ to Context     │
         └────────┬───────┘
                  │
                  ▼
         ┌────────────────┐
         │ Process with   │
         │ Agent          │
         └────────┬───────┘
                  │
                  ▼
         ┌────────────────┐
         │ Save Updated   │
         │ Context        │
         └────────┬───────┘
                  │
                  ▼
         ┌────────────────┐
         │ Send Response  │
         └────────┬───────┘
                  │
                  ▼
            ┌─────────┐    Yes    ┌──────────┐
            │ Prune   ├──────────→│ Compress │
            │ Needed? │           │ Context  │
            └─────────┘           └──────────┘
```

## 🛠️ Tool Execution Flow

```
Agent receives message
       │
       ▼
Analyzes available tools
       │
       ▼
Determines tool needed
       │
       ▼
┌──────────────┐
│ Tool Call    │
│ {            │
│   name: "x"  │
│   params: {} │
│ }            │
└──────┬───────┘
       │
       ▼
┌─────────────────┐
│ Execute Tool    │
│                 │
│ if (browser)    │
│   → Browser     │
│ if (canvas)     │
│   → Canvas      │
│ if (camera)     │
│   → Node        │
└──────┬──────────┘
       │
       ▼
┌─────────────────┐
│ Tool Result     │
│ {               │
│   output: "..." │
│ }               │
└──────┬──────────┘
       │
       ▼
Agent synthesizes response
       │
       ▼
Stream to user
```

## 🌍 Network Topology Options

### Option 1: Local Everything
```
┌──────────────────────┐
│  Local Machine       │
│  ┌────────────────┐  │
│  │ Gateway        │  │
│  │ Agent          │  │
│  │ Channels       │  │
│  └────────────────┘  │
│                      │
│  Access:             │
│  ws://localhost:18789│
└──────────────────────┘
```

### Option 2: Remote Gateway
```
┌──────────────────────┐       ┌──────────────────┐
│  Remote Server       │       │  Local Machine   │
│  ┌────────────────┐  │       │  ┌────────────┐  │
│  │ Gateway        │◄─┼───────┼──┤ CLI        │  │
│  │ Agent          │  │  SSH  │  │ macOS App  │  │
│  │ Channels       │  │ tunnel│  └────────────┘  │
│  └────────────────┘  │       │                  │
│                      │       │  ┌────────────┐  │
│  Public:             │       │  │ iOS Node   │  │
│  https://...         │       │  └────────────┘  │
└──────────────────────┘       └──────────────────┘
```

### Option 3: Tailscale
```
┌─────────────────────────────────┐
│     Tailscale Network           │
│                                 │
│  ┌──────────┐    ┌───────────┐ │
│  │ Gateway  │    │ Client 1  │ │
│  │ (Server) │◄───┤ (macOS)   │ │
│  └──────────┘    └───────────┘ │
│       ▲                         │
│       │          ┌───────────┐  │
│       └──────────┤ Client 2  │  │
│                  │ (Mobile)  │  │
│                  └───────────┘  │
└─────────────────────────────────┘
```

## 📚 Technology Stack Map

```
┌─────────────────────────────────────┐
│           RUNTIME                   │
│         Node.js ≥22                 │
└─────────────────┬───────────────────┘
                  │
    ┌─────────────┼─────────────┐
    │             │             │
    ▼             ▼             ▼
┌─────────┐ ┌──────────┐ ┌──────────┐
│TypeScript│ │ WebSocket│ │ SQLite   │
│  (tsx)   │ │   (ws)   │ │(better-  │
│          │ │          │ │ sqlite3) │
└─────────┘ └──────────┘ └──────────┘
    │             │             │
    └─────────────┼─────────────┘
                  │
    ┌─────────────┴─────────────┐
    │                           │
    ▼                           ▼
┌─────────┐               ┌──────────┐
│ Channel │               │    AI    │
│  SDKs   │               │  SDKs    │
│         │               │          │
│ Baileys │               │Anthropic │
│ grammY  │               │ OpenAI   │
│discord.js│              │  etc.    │
└─────────┘               └──────────┘
```

## 🎓 Learning Path

```
START HERE
    │
    ▼
┌─────────────┐
│ 1. Install  │ → openclaw onboard
└─────┬───────┘
      │
      ▼
┌─────────────┐
│ 2. Try CLI  │ → openclaw agent --message "hello"
└─────┬───────┘
      │
      ▼
┌─────────────┐
│ 3. Study    │ → Read architecture.md
│ Architecture│
└─────┬───────┘
      │
      ▼
┌─────────────┐
│ 4. Clone    │ → git clone openclaw/openclaw
│ & Build     │   pnpm install && pnpm build
└─────┬───────┘
      │
      ▼
┌─────────────┐
│ 5. Add      │ → Connect Telegram/Discord
│ Channel     │
└─────┬───────┘
      │
      ▼
┌─────────────┐
│ 6. Create   │ → Build custom skill
│ Custom Skill│
└─────┬───────┘
      │
      ▼
┌─────────────┐
│ 7. Explore  │ → Read source code
│ Codebase    │   packages/gateway/
└─────────────┘   packages/agent/
```

## 🎯 Quick Reference

| Concept | File/Directory | Description |
|---------|---------------|-------------|
| Gateway | `packages/gateway/src/server.ts` | Main server |
| Agent | `packages/agent/src/agent.ts` | AI logic |
| Channels | `packages/channels/` | Platform adapters |
| Tools | `packages/agent/src/tools/` | Capabilities |
| CLI | `packages/cli/src/commands/` | Commands |
| Config | `~/.openclaw/config.yaml` | User config |
| Sessions | `~/.openclaw/sessions.db` | Session data |

## 💡 Key Takeaways

1. **Separation of Concerns**: Gateway ≠ Agent ≠ Channels
2. **WebSocket Central**: Everything talks through Gateway WS
3. **Session-Centric**: One session = one conversation context
4. **Tool-Driven**: Agent capabilities via tools
5. **Security First**: DM pairing, auth layers, allowlists
6. **Extensible**: Skills, channels, tools are all pluggable
7. **Local-First**: Your data, your device, your control

---

**Use this guide as a visual companion to the detailed documentation!**
