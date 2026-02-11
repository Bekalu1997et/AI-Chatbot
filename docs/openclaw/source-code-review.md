# OpenClaw Source Code Review Guide

This guide helps you navigate and understand the OpenClaw codebase structure, key files, and code organization.

## 📁 Repository Structure

```
openclaw/
│
├── packages/               # Monorepo packages
│   ├── gateway/           # Gateway control plane
│   ├── agent/             # Pi agent runtime
│   ├── channels/          # Channel adapters
│   ├── cli/               # Command-line interface
│   ├── web/               # Web UI components
│   ├── shared/            # Shared utilities and types
│   └── nodes/             # Node implementations
│
├── apps/                  # Application builds
│   ├── macos/            # macOS native app
│   ├── ios/              # iOS app
│   └── android/          # Android app
│
├── docs/                  # Documentation
├── scripts/              # Build and deployment scripts
├── tests/                # Test suites
└── config/               # Configuration files
```

## 🔍 Key Packages Deep Dive

### 1. Gateway Package (`packages/gateway/`)

**Purpose:** Core control plane and WebSocket server

**Key Files:**
- `src/server.ts` - Main Gateway server setup
- `src/websocket.ts` - WebSocket handler and protocol
- `src/router.ts` - Message routing logic
- `src/sessions/` - Session management
- `src/channels/` - Channel integration layer
- `src/config.ts` - Configuration management
- `src/database/` - SQLite persistence layer
- `src/auth/` - Authentication and security

**Important Concepts:**

```typescript
// Example: Session routing
interface Session {
  id: string;
  channelId: string;
  peerId: string;
  context: Message[];
  config: SessionConfig;
  state: SessionState;
}

// Gateway manages sessions and routes messages
class Gateway {
  sessions: Map<string, Session>;
  channels: Map<string, ChannelAdapter>;
  
  async handleInboundMessage(msg: InboundMessage) {
    const session = await this.getOrCreateSession(msg);
    const response = await this.agent.process(session, msg);
    await this.sendResponse(msg.channelId, response);
  }
}
```

**Key Functions to Study:**
1. `startGateway()` - Initialization sequence
2. `handleWebSocketConnection()` - Client connection handling
3. `routeMessage()` - Message routing logic
4. `createSession()` - Session initialization
5. `authenticateRequest()` - Security checks

### 2. Agent Package (`packages/agent/`)

**Purpose:** AI reasoning and tool execution

**Key Files:**
- `src/agent.ts` - Main agent implementation
- `src/tools/` - Tool definitions and handlers
- `src/models/` - AI model adapters
- `src/context.ts` - Context management
- `src/streaming.ts` - Response streaming
- `src/failover.ts` - Model failover logic

**Important Patterns:**

```typescript
// Agent with tool execution
class PiAgent {
  async process(session: Session, message: Message): Promise<Response> {
    // 1. Build context from session history
    const context = this.buildContext(session);
    
    // 2. Call AI model with tools
    const response = await this.model.generate({
      context,
      tools: this.availableTools,
      streaming: true
    });
    
    // 3. Execute tool calls
    if (response.toolCalls) {
      for (const call of response.toolCalls) {
        await this.executeTool(call);
      }
    }
    
    // 4. Return final response
    return response;
  }
}
```

**Key Concepts:**
- **Tool Definitions** - JSON schemas for tools
- **Streaming** - Incremental response delivery
- **Context Windows** - Managing token limits
- **Failover** - Handling model failures

### 3. Channels Package (`packages/channels/`)

**Purpose:** Messaging platform adapters

**Structure:**
```
channels/
├── whatsapp/         # WhatsApp via Baileys
├── telegram/         # Telegram via grammY
├── discord/          # Discord via discord.js
├── slack/            # Slack via Bolt
├── signal/           # Signal via signal-cli
├── imessage/         # iMessage (legacy)
├── bluebubbles/      # iMessage via BlueBubbles
└── base/             # Base channel interface
```

**Channel Interface:**

```typescript
interface ChannelAdapter {
  id: string;
  type: ChannelType;
  
  // Connection management
  connect(): Promise<void>;
  disconnect(): Promise<void>;
  
  // Message handling
  sendMessage(to: string, content: MessageContent): Promise<void>;
  onMessage(handler: MessageHandler): void;
  
  // Features
  sendTyping?(to: string): Promise<void>;
  sendPresence?(to: string, status: PresenceStatus): Promise<void>;
  uploadMedia?(file: Buffer, type: MediaType): Promise<string>;
}
```

**Example: WhatsApp Channel**

```typescript
class WhatsAppChannel implements ChannelAdapter {
  private socket: WASocket;
  
  async connect() {
    // Initialize Baileys socket
    this.socket = makeWASocket({
      auth: this.authState,
      printQRInTerminal: true
    });
    
    // Register message handler
    this.socket.ev.on('messages.upsert', this.handleMessage);
  }
  
  async sendMessage(to: string, content: MessageContent) {
    await this.socket.sendMessage(to, {
      text: content.text,
      // Handle media, formatting, etc.
    });
  }
}
```

### 4. CLI Package (`packages/cli/`)

**Purpose:** Command-line interface

**Key Commands:**
- `openclaw gateway` - Start Gateway
- `openclaw agent` - Talk to agent
- `openclaw onboard` - Setup wizard
- `openclaw doctor` - Health check
- `openclaw pairing` - Manage pairings
- `openclaw message` - Send messages

**CLI Architecture:**

```typescript
// Command structure (using a framework like Commander.js)
program
  .command('gateway')
  .option('--port <port>', 'Gateway port')
  .option('--verbose', 'Verbose logging')
  .action(async (options) => {
    const gateway = new Gateway(options);
    await gateway.start();
  });
```

### 5. Web Package (`packages/web/`)

**Purpose:** Browser-based interfaces

**Components:**
- `control-ui/` - Gateway management dashboard
- `webchat/` - Chat interface
- `components/` - Shared React components

**Technology:**
- React for UI
- WebSocket for real-time updates
- Tailwind CSS for styling

### 6. Shared Package (`packages/shared/`)

**Purpose:** Common utilities and types

**Key Modules:**
- `types/` - TypeScript type definitions
- `utils/` - Helper functions
- `constants/` - Shared constants
- `validators/` - Input validation
- `logger/` - Logging utilities

**Important Types:**

```typescript
// Message types
interface Message {
  id: string;
  role: 'user' | 'assistant' | 'system';
  content: string;
  timestamp: Date;
  metadata?: Record<string, any>;
}

// Channel types
type ChannelType = 
  | 'whatsapp' 
  | 'telegram' 
  | 'discord' 
  | 'slack' 
  | 'signal'
  | 'imessage'
  | 'bluebubbles'
  | 'webchat';

// Tool types
interface Tool {
  name: string;
  description: string;
  parameters: ToolParameters;
  handler: ToolHandler;
}
```

## 🔬 Code Study Path

### For Beginners

1. **Start with CLI** (`packages/cli/`)
   - Simple entry point
   - See how commands work
   - Understand user workflows

2. **Study Channels** (`packages/channels/base/`)
   - Review the base interface
   - Pick one channel (e.g., Telegram) to study
   - Understand message flow

3. **Explore Gateway** (`packages/gateway/server.ts`)
   - Main server initialization
   - WebSocket handling basics
   - Simple message routing

### For Intermediate

4. **Session Management** (`packages/gateway/sessions/`)
   - How sessions are created and managed
   - Context persistence
   - Configuration handling

5. **Agent Logic** (`packages/agent/agent.ts`)
   - AI model integration
   - Tool execution
   - Response generation

6. **Tools System** (`packages/agent/tools/`)
   - How tools are defined
   - Tool execution lifecycle
   - Built-in tools vs. skills

### For Advanced

7. **WebSocket Protocol** (`packages/gateway/websocket.ts`)
   - RPC implementation
   - Event handling
   - Client synchronization

8. **Node System** (`packages/nodes/`)
   - Device capabilities
   - Remote invocation
   - Permission handling

9. **Skills Platform** (`packages/gateway/skills/`)
   - Skill loading and validation
   - ClawHub integration
   - Security model

## 🧪 Testing Strategy

### Test Structure

```
tests/
├── unit/              # Unit tests for individual modules
├── integration/       # Integration tests for components
├── e2e/              # End-to-end tests
└── fixtures/         # Test data and mocks
```

### Key Test Files

- `tests/unit/gateway/router.test.ts` - Routing logic tests
- `tests/unit/agent/tools.test.ts` - Tool execution tests
- `tests/integration/channels/` - Channel integration tests
- `tests/e2e/flows/` - Complete user flow tests

### Testing Tools

- **Jest** - Test framework
- **ts-jest** - TypeScript support
- **supertest** - HTTP testing
- **ws** - WebSocket testing
- **Mock libraries** - For AI models, channels, etc.

## 🔧 Build and Development

### Development Setup

```bash
# Clone repository
git clone https://github.com/openclaw/openclaw.git
cd openclaw

# Install dependencies
pnpm install

# Build packages
pnpm build

# Run in development mode (with auto-reload)
pnpm gateway:watch

# Run tests
pnpm test

# Run linter
pnpm lint
```

### Build Scripts

**Key npm scripts:**
- `build` - Build all packages
- `dev` - Development mode with watch
- `test` - Run test suite
- `lint` - Code linting
- `clean` - Clean build artifacts
- `ui:build` - Build web UI

### TypeScript Configuration

The project uses a monorepo TypeScript setup with:
- Strict mode enabled
- Path aliases for clean imports
- Project references for build optimization

Example `tsconfig.json`:
```json
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "commonjs",
    "strict": true,
    "esModuleInterop": true,
    "resolveJsonModule": true,
    "paths": {
      "@openclaw/gateway": ["packages/gateway/src"],
      "@openclaw/agent": ["packages/agent/src"],
      "@openclaw/shared": ["packages/shared/src"]
    }
  }
}
```

## 📝 Code Style Guidelines

### TypeScript Best Practices

1. **Use strict types** - Avoid `any`
2. **Prefer interfaces** - For object shapes
3. **Use enums** - For fixed sets of values
4. **Async/await** - Over promise chains
5. **Error handling** - Try/catch with specific error types

### Naming Conventions

- **Files**: `kebab-case.ts`
- **Classes**: `PascalCase`
- **Functions**: `camelCase`
- **Constants**: `UPPER_SNAKE_CASE`
- **Interfaces**: `PascalCase` (with `I` prefix optional)
- **Types**: `PascalCase`

### Code Organization

```typescript
// 1. Imports (grouped by source)
import { Gateway } from '@openclaw/gateway';
import { PiAgent } from '@openclaw/agent';
import type { Session } from '@openclaw/shared';

// 2. Constants
const DEFAULT_PORT = 18789;

// 3. Types/Interfaces
interface GatewayConfig {
  port: number;
  verbose: boolean;
}

// 4. Main logic
class GatewayServer {
  // Implementation
}

// 5. Exports
export { GatewayServer };
```

## 🔍 Debugging Tips

### Gateway Debugging

```bash
# Start with verbose logging
openclaw gateway --verbose

# Enable debug logs
DEBUG=openclaw:* openclaw gateway

# Check Gateway status
openclaw doctor
```

### Agent Debugging

```typescript
// Add logging to agent calls
this.logger.debug('Processing message', { sessionId, messageId });

// Enable tool call tracing
config.agent.traceTools = true;
```

### Channel Debugging

```typescript
// Log channel events
channel.on('message', (msg) => {
  console.log('Received:', msg);
});

channel.on('error', (err) => {
  console.error('Channel error:', err);
});
```

## 🎯 Key Areas for Custom Development

### 1. Custom Channels
Add new messaging platform support by implementing `ChannelAdapter`.

### 2. Custom Tools
Extend agent capabilities with new tool definitions.

### 3. Custom Skills
Create workspace skills for specific use cases.

### 4. Custom UI
Build new web interfaces using the Gateway WebSocket API.

### 5. Custom Nodes
Add support for new device types and capabilities.

## 📚 Further Reading

### Important Files to Review

1. `packages/gateway/src/server.ts` - Gateway initialization
2. `packages/agent/src/agent.ts` - Agent core logic
3. `packages/channels/base/adapter.ts` - Channel interface
4. `packages/shared/src/types/` - Core type definitions
5. `packages/cli/src/commands/` - CLI commands

### External Dependencies

**Key libraries to understand:**
- **Baileys** - WhatsApp Web API
- **grammY** - Telegram bot framework
- **discord.js** - Discord API wrapper
- **@slack/bolt** - Slack app framework
- **ws** - WebSocket library
- **express** - HTTP server
- **better-sqlite3** - SQLite interface

## 💡 Pro Tips

1. **Use TypeScript Language Server** - For code navigation
2. **Read tests first** - They show intended usage
3. **Follow the data flow** - From channel → gateway → agent → response
4. **Start small** - Modify existing features before adding new ones
5. **Use debugger** - VS Code debugging works great with TypeScript
6. **Join Discord** - Ask questions to the community
7. **Read commit history** - Learn from past changes
8. **Check issues** - See common problems and solutions

## 🚀 Contributing

When contributing to OpenClaw:

1. Fork the repository
2. Create a feature branch
3. Write tests for new features
4. Follow existing code style
5. Update documentation
6. Submit a pull request

Refer to the project's `CONTRIBUTING.md` for detailed guidelines.
