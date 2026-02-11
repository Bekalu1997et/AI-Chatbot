# OpenClaw Architecture Overview

## 🏛️ Core Architecture

OpenClaw is built around a **local-first, WebSocket-based architecture** that separates concerns into distinct layers:

### 1. Gateway (Control Plane)

The **Gateway** is the heart of OpenClaw - a WebSocket server that acts as the central control plane.

**Key Responsibilities:**
- Session management and routing
- Channel connections (WhatsApp, Telegram, Slack, Discord, etc.)
- Tool and skill orchestration
- Event distribution
- Configuration management
- Authentication and security

**Default Address:** `ws://127.0.0.1:18789`

**Core Features:**
- WebSocket-based real-time communication
- RESTful API for certain operations
- Built-in web UI (Control UI + WebChat)
- Support for remote access via Tailscale or SSH tunnels

### 2. Agent Runtime (Pi Agent)

The **Pi Agent** handles the AI reasoning and tool execution.

**Characteristics:**
- RPC-based communication with the Gateway
- Supports multiple AI models (Anthropic Claude, OpenAI GPT, etc.)
- Tool streaming and block streaming
- Context management with pruning strategies
- Model failover and retry logic

**Model Support:**
- Anthropic (Claude Pro/Max) - Recommended for long context
- OpenAI (ChatGPT/Codex)
- Any model with appropriate adapters

### 3. Channels

Channels are adapters that connect the Gateway to various messaging platforms.

**Supported Channels:**
- **WhatsApp** (via Baileys library)
- **Telegram** (via grammY)
- **Slack** (via Bolt SDK)
- **Discord** (via discord.js)
- **Google Chat** (via Chat API)
- **Signal** (via signal-cli)
- **BlueBubbles** (iMessage, recommended)
- **iMessage** (legacy direct integration)
- **Microsoft Teams** (extension)
- **Matrix** (extension)
- **Zalo** and **Zalo Personal** (extension)
- **WebChat** (built-in web interface)

**Channel Abstraction:**
Each channel implements a common interface for:
- Receiving messages
- Sending messages (with chunking/streaming support)
- Typing indicators
- Presence updates
- Media handling (images, audio, video)

### 4. Nodes (Device Integration)

**Nodes** are device-specific components that provide local capabilities.

**Types of Nodes:**
- **macOS Node**: System commands, notifications, Canvas, camera, screen recording
- **iOS Node**: Canvas, Voice Wake, Talk Mode, camera, screen recording
- **Android Node**: Canvas, Talk Mode, camera, screen recording, optional SMS

**Node Capabilities:**
- `system.run` - Execute local commands (macOS only)
- `system.notify` - Show notifications
- `canvas.*` - Canvas rendering and control
- `camera.*` - Photo and video capture
- `screen.record` - Screen recording
- `location.get` - Location services

**Communication:**
Nodes communicate with the Gateway via WebSocket and can be invoked remotely using `node.invoke` RPC calls.

### 5. Tools & Skills

**Tools** are built-in capabilities:
- **Browser control** - Automated Chrome/Chromium with CDP
- **Canvas** - Visual workspace with A2UI (Agent-to-UI)
- **Cron jobs** - Scheduled tasks
- **Webhooks** - External integrations
- **Gmail Pub/Sub** - Email monitoring

**Skills** are installable extensions:
- **Bundled skills** - Shipped with OpenClaw
- **Managed skills** - From ClawHub registry
- **Workspace skills** - Custom local skills

**Skills Platform:**
- Declarative skill definitions
- Install gating and permissions
- UI integration
- Automatic discovery via ClawHub

## 🔄 Data Flow

### Inbound Message Flow

```
1. Message arrives at channel adapter
   │
2. Channel authenticates sender (DM policy check)
   │
3. Message routed to appropriate session
   │
4. Session context loaded/created
   │
5. Agent processes message with tools
   │
6. Response generated (with streaming)
   │
7. Response chunked per channel limits
   │
8. Response sent back through channel
```

### Session Model

**Session Types:**
- **Main session** - Direct 1:1 conversations
- **Group sessions** - Group chat handling with isolation
- **Agent-to-agent** - Inter-session communication

**Session Features:**
- Persistent conversation context
- Message history with pruning
- Per-session configuration (model, thinking level, etc.)
- Activation modes (mention-only or always-on for groups)
- Queue modes for sequential processing

### Group Routing

**Group Message Handling:**
- **Mention gating** - Respond only when mentioned
- **Reply tags** - Thread-based responses
- **Per-channel chunking** - Respect platform message limits
- **Activation modes** - Configurable response behavior

## 🔐 Security Architecture

### DM (Direct Message) Policy

**Default: Pairing Mode**
- Unknown senders get a pairing code
- Must approve with: `openclaw pairing approve <channel> <code>`
- Sender added to local allowlist after approval

**Alternative: Open Mode**
- Requires explicit opt-in via config
- Must include `"*"` in channel allowlist
- **Not recommended** for production

### Authentication Layers

1. **Channel-level auth** - Per-channel allowlists
2. **Gateway auth** - Token or password for WebSocket/HTTP access
3. **Tailscale integration** - Identity-based access for Serve/Funnel
4. **Elevated access** - Per-session sudo toggle for sensitive operations

### Security Best Practices

- Run `openclaw doctor` to check for misconfigurations
- Use pairing mode for DMs
- Enable Gateway authentication for remote access
- Use Tailscale Serve (not Funnel) when possible
- Review channel allowlists regularly

## 🌐 Remote Architecture

OpenClaw supports running the Gateway on a remote server (e.g., Linux instance) while clients connect from various devices.

### Remote Gateway Setup

**Gateway Host:**
- Runs the Gateway daemon
- Handles exec tool operations
- Manages channel connections
- Stores session data

**Remote Access Options:**
1. **Tailscale Serve/Funnel**
   - Automatic HTTPS
   - Tailscale identity integration
   - Public (Funnel) or tailnet-only (Serve)

2. **SSH Tunnels**
   - Manual port forwarding
   - Works with any SSH server
   - Good for development

**Client Options:**
- macOS app (connects to remote Gateway)
- CLI tools (with Gateway URL)
- WebChat (browser-based)
- Mobile nodes (iOS/Android)

**Hybrid Architecture:**
Remote Gateway + Local Nodes = Best of both worlds
- Gateway handles messaging and AI
- Nodes handle device-specific actions
- Actions routed via `node.invoke`

## 📊 Technology Stack

### Backend
- **Runtime**: Node.js (≥22 required)
- **Language**: TypeScript
- **Framework**: Custom WebSocket server + Express
- **Database**: SQLite (for persistence)
- **Build Tool**: pnpm (preferred), npm, or bun

### Frontend
- **Control UI**: React-based web interface
- **WebChat**: Browser-based chat client
- **macOS App**: Native Swift application
- **iOS/Android Apps**: Native mobile applications

### Key Libraries
- **Channel SDKs**: Baileys, grammY, Bolt, discord.js, etc.
- **AI SDKs**: Anthropic SDK, OpenAI SDK
- **Browser Control**: Chrome DevTools Protocol (CDP)
- **Voice**: ElevenLabs for TTS, platform STT

### Packaging
- **npm**: Standard distribution
- **Docker**: Container-based deployment
- **Nix**: Declarative configuration
- **Daemon**: launchd (macOS), systemd (Linux)

## 🔌 Integration Points

### Gateway WebSocket Protocol

**Key Methods:**
- `agent.send` - Send message to agent
- `sessions.list` - Get all sessions
- `sessions.patch` - Update session config
- `node.list` - Discover available nodes
- `node.invoke` - Execute node action
- `tool.invoke` - Call a tool directly

### REST API

The Gateway also exposes REST endpoints:
- `/health` - Health check
- `/api/sessions` - Session management
- `/api/messages` - Message history
- `/webchat` - WebChat UI

### Event System

**Event Types:**
- Message events (inbound/outbound)
- Presence updates
- Typing indicators
- Tool invocations
- Session state changes

## 🧩 Design Patterns

### 1. Gateway Pattern
Centralized control plane for distributed services.

### 2. Channel Adapter Pattern
Uniform interface for diverse messaging platforms.

### 3. RPC Pattern
Remote procedure calls for agent and node communication.

### 4. Plugin Architecture
Extensible skills and tools system.

### 5. Event-Driven Architecture
WebSocket-based real-time events.

### 6. Session Isolation
Each conversation has its own context and state.

### 7. Retry and Failover
Automatic retry logic and model failover.

## 🚀 Scalability Considerations

### Current Design
- Single Gateway instance
- Multi-session support
- In-memory + SQLite persistence
- Suitable for personal/small team use

### Scaling Possibilities
- Multiple Gateway instances with load balancing
- External database (PostgreSQL, MySQL)
- Redis for session state
- Message queue for channel operations
- Distributed node registry

## 📈 Performance Optimizations

1. **Streaming Responses** - Incremental message delivery
2. **Context Pruning** - Automatic cleanup of old messages
3. **Lazy Loading** - On-demand channel initialization
4. **Connection Pooling** - Reuse of HTTP/WS connections
5. **Chunking** - Efficient large message handling
6. **Caching** - Model response caching where appropriate

## 🎯 Architecture Best Practices

1. **Separation of Concerns** - Gateway, Agent, Channels, Nodes
2. **Loose Coupling** - WebSocket-based communication
3. **Security by Default** - Pairing mode, authentication
4. **Local-First** - Privacy and performance
5. **Extensibility** - Skills and tools platform
6. **Observability** - Logging and usage tracking
7. **Fail-Safe** - Graceful degradation and retries
