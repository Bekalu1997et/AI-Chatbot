# OpenClaw Components & Features

A comprehensive breakdown of all major components, features, and capabilities in OpenClaw.

## 🎯 Core Components

### 1. Gateway (Control Plane)

The Gateway is the central nervous system of OpenClaw.

**Capabilities:**
- WebSocket server for real-time communication
- HTTP/HTTPS server for web UI and REST API
- Session management and persistence
- Channel orchestration
- Configuration management
- Authentication and authorization
- Event distribution
- Logging and monitoring

**Configuration Options:**
```yaml
gateway:
  port: 18789
  bind: loopback  # or 0.0.0.0
  verbose: true
  
  auth:
    mode: password  # or token, or off
    password: "your-secure-password"
    allowTailscale: true
  
  tailscale:
    mode: serve  # or funnel, or off
    resetOnExit: true
```

**Key Features:**
- **Auto-discovery** - Nodes advertise capabilities
- **Hot reload** - Config changes without restart
- **Health checks** - Built-in diagnostics
- **Usage tracking** - Per-session metrics
- **Backup/restore** - Session data management

### 2. Agent (AI Core)

The Pi Agent handles all AI reasoning and decision-making.

**Features:**
- **Multi-model support** - Claude, GPT-4, GPT-5.2, custom models
- **Tool execution** - Function calling with streaming
- **Context management** - Automatic pruning and summarization
- **Thinking levels** - Variable reasoning depth (off to xhigh)
- **Model failover** - Automatic fallback on errors
- **Cost tracking** - Token usage and cost estimation

**Thinking Levels:**
- `off` - No extended reasoning
- `minimal` - Basic chain-of-thought
- `low` - Light reasoning
- `medium` - Balanced (default)
- `high` - Deep reasoning
- `xhigh` - Maximum reasoning (GPT-5.2/Codex only)

**Configuration:**
```yaml
agent:
  model: claude-3-7-sonnet-20250219  # or gpt-4, gpt-5.2, etc.
  thinkingLevel: medium
  maxTokens: 4096
  temperature: 0.7
  
  failover:
    enabled: true
    fallbackModels:
      - gpt-4-turbo
      - claude-3-5-sonnet
```

### 3. Channels

Messaging platform integrations.

#### WhatsApp (via Baileys)

**Features:**
- QR code authentication
- Send/receive text, media, reactions
- Group support
- Status updates
- Typing indicators
- Read receipts

**Setup:**
```typescript
channels:
  whatsapp:
    enabled: true
    dm:
      policy: pairing  # or open
      allowFrom: []
```

#### Telegram (via grammY)

**Features:**
- Bot token authentication
- Rich media support (photos, videos, documents)
- Inline keyboards
- Custom keyboards
- Group and channel support
- Webhook or polling mode

#### Discord (via discord.js)

**Features:**
- Bot token authentication
- Server/channel support
- Thread support
- Slash commands
- Embeds and reactions
- Voice channel presence

#### Slack (via Bolt)

**Features:**
- OAuth or bot token
- Workspace integration
- Thread support
- Blocks and attachments
- Interactive components
- App Home

#### Signal (via signal-cli)

**Features:**
- Linked device support
- End-to-end encryption
- Group support
- Media attachments
- Read receipts

#### BlueBubbles (iMessage - Recommended)

**Features:**
- iMessage via BlueBubbles server
- Send/receive messages
- Group chats
- Rich media
- Reactions and effects

#### Google Chat

**Features:**
- Workspace integration
- Space support
- Cards and widgets
- Thread support
- Rich text formatting

#### Microsoft Teams

**Features:**
- Bot framework integration
- Team and channel support
- Adaptive cards
- Meeting integration
- Tabs and messaging extensions

### 4. Nodes (Device Capabilities)

#### macOS Node

**System Commands (`system.run`):**
```typescript
// Execute local commands
await node.invoke('system.run', {
  command: 'ls -la',
  timeout: 5000
});
```

**Notifications (`system.notify`):**
```typescript
await node.invoke('system.notify', {
  title: 'Alert',
  message: 'Task completed',
  sound: true
});
```

**Canvas:**
- Render visual content
- A2UI (Agent-to-UI) interface
- Screenshots and snapshots

**Camera:**
- Photo capture
- Video recording
- Configurable resolution

**Screen Recording:**
- Capture screen activity
- Region selection
- Quality settings

#### iOS Node

**Features:**
- Canvas rendering
- Voice Wake (always-on listening)
- Talk Mode (hands-free conversation)
- Camera access
- Screen recording
- Bonjour device discovery

**Voice Wake:**
```typescript
voiceWake:
  enabled: true
  wakeWord: "Hey Claw"
  language: en-US
  sensitivity: medium
```

#### Android Node

**Features:**
- Canvas support
- Talk Mode
- Camera integration
- Screen recording
- Optional SMS access

### 5. Tools

#### Browser Control

**Capabilities:**
- Launch Chrome/Chromium
- Navigate to URLs
- Take screenshots
- Execute JavaScript
- Fill forms
- Upload files
- Download files
- Manage browser profiles

**Usage:**
```typescript
// Browser tool in action
tools:
  browser:
    enabled: true
    executablePath: /path/to/chrome
    headless: false
    profiles:
      - name: default
        path: ~/.openclaw/browser-profiles/default
```

**Example Commands:**
- "Open google.com and search for AI news"
- "Screenshot the current page"
- "Fill out the form with my details"

#### Canvas (A2UI)

**Agent-to-UI Interface:**
- Dynamic UI generation
- Real-time updates
- Interactive components
- Custom layouts

**Canvas Operations:**
```typescript
// Push content to Canvas
await canvas.push({
  type: 'markdown',
  content: '# Hello World'
});

// Reset Canvas
await canvas.reset();

// Evaluate JavaScript
await canvas.eval('document.body.style.background = "blue"');

// Take snapshot
const snapshot = await canvas.snapshot();
```

#### Node Actions

**Available Operations:**
- `camera.snap` - Take photo
- `camera.record` - Record video
- `screen.record` - Record screen
- `location.get` - Get GPS coordinates
- `system.run` - Execute command (macOS only)
- `system.notify` - Show notification

### 6. Skills Platform

#### Skill Types

**1. Bundled Skills**
- Shipped with OpenClaw
- Always available
- Core functionality

**2. Managed Skills**
- From ClawHub registry
- Vetted and maintained
- Auto-updates

**3. Workspace Skills**
- Local custom skills
- Project-specific
- Full control

#### Skill Structure

```typescript
// skill.json
{
  "name": "weather",
  "version": "1.0.0",
  "description": "Get weather information",
  "author": "OpenClaw Team",
  "tools": [
    {
      "name": "getWeather",
      "description": "Get current weather for a location",
      "parameters": {
        "type": "object",
        "properties": {
          "location": {
            "type": "string",
            "description": "City name or coordinates"
          }
        },
        "required": ["location"]
      }
    }
  ],
  "permissions": ["network"],
  "dependencies": {}
}
```

**Skill Installation:**
```bash
# From ClawHub
openclaw skills install weather

# From local directory
openclaw skills install ./my-skill

# List installed skills
openclaw skills list
```

### 7. Automation

#### Cron Jobs

**Schedule Tasks:**
```yaml
cron:
  - name: morning-briefing
    schedule: "0 8 * * *"  # 8 AM daily
    action:
      type: agent
      message: "Give me my morning briefing"
      sendTo: whatsapp:+1234567890
  
  - name: backup
    schedule: "0 0 * * 0"  # Weekly
    action:
      type: system
      command: openclaw backup
```

#### Webhooks

**Inbound Webhooks:**
```yaml
webhooks:
  - name: github-pr
    path: /webhooks/github
    auth:
      type: token
      token: ${GITHUB_WEBHOOK_SECRET}
    handler: skills/github-webhook
```

**Outbound Webhooks:**
Send notifications to external services on events.

#### Gmail Pub/Sub

**Email Monitoring:**
```yaml
gmail:
  enabled: true
  credentials: ~/.openclaw/gmail-credentials.json
  filters:
    - from: boss@company.com
      action: notify
      message: "New email from boss"
```

## 🎨 User Interface Components

### Control UI

**Features:**
- Gateway status dashboard
- Session browser
- Channel management
- Skill registry
- Configuration editor
- Log viewer

**Access:** `http://localhost:18789/control`

### WebChat

**Features:**
- Browser-based chat interface
- Message history
- Media upload
- Voice input (browser-supported)
- Typing indicators
- Read receipts

**Access:** `http://localhost:18789/webchat`

### macOS App

**Features:**
- Menu bar integration
- Quick access controls
- Voice Wake toggle
- Talk Mode overlay
- Gateway connection manager
- Debug tools

**Install:**
```bash
# Via Homebrew
brew install --cask openclaw

# Or download from releases
```

### Mobile Apps (iOS/Android)

**Features:**
- Canvas rendering
- Voice input/output
- Camera integration
- Screen recording
- Push notifications
- Background operation

## 🔐 Security Features

### DM Policy

**Pairing Mode (Default):**
```typescript
channels:
  telegram:
    dm:
      policy: pairing
      allowFrom: []  # Allowlist populated via pairing
```

**Pairing Flow:**
1. Unknown sender messages the bot
2. Bot responds with pairing code
3. Owner approves: `openclaw pairing approve telegram CODE`
4. Sender added to allowlist
5. Conversation proceeds normally

**Open Mode (Not Recommended):**
```typescript
channels:
  telegram:
    dm:
      policy: open
      allowFrom: ["*"]  # Allow all
```

### Gateway Authentication

**Password Mode:**
```yaml
gateway:
  auth:
    mode: password
    password: "secure-password-here"
```

**Token Mode:**
```yaml
gateway:
  auth:
    mode: token
    tokens:
      - "token-abc123"
      - "token-def456"
```

**Tailscale Identity:**
```yaml
gateway:
  auth:
    mode: tailscale
    allowTailscale: true
```

### Elevated Access

**Per-Session Sudo Toggle:**
```bash
# In chat
/elevated on   # Enable sudo for this session
/elevated off  # Disable sudo for this session
```

**Configuration:**
```yaml
gateway:
  elevated:
    enabled: true
    allowFrom:
      - whatsapp:+1234567890
      - telegram:@username
```

## 📊 Monitoring & Observability

### Logging

**Log Levels:**
- `error` - Errors only
- `warn` - Warnings and errors
- `info` - Informational messages (default)
- `debug` - Debug information
- `trace` - Verbose tracing

**Configuration:**
```yaml
logging:
  level: info
  outputs:
    - console
    - file: ~/.openclaw/logs/gateway.log
```

### Usage Tracking

**Metrics Collected:**
- Message counts (inbound/outbound)
- Token usage per model
- Cost estimates
- Tool invocations
- Error rates
- Response times

**Per-Message Footer:**
```
/usage full   # Show detailed usage
/usage tokens # Show token count only
/usage off    # Hide usage info
```

### Health Checks

**Gateway Doctor:**
```bash
openclaw doctor

# Checks:
# - Gateway connectivity
# - Channel status
# - Database integrity
# - Configuration issues
# - Security misconfigurations
# - Disk space
# - Memory usage
```

## 🌐 Networking Features

### Tailscale Integration

**Serve Mode (Tailnet-Only):**
```yaml
gateway:
  tailscale:
    mode: serve
    resetOnExit: true
```

**Funnel Mode (Public):**
```yaml
gateway:
  tailscale:
    mode: funnel
    resetOnExit: false
  auth:
    mode: password  # Required for Funnel
    password: "secure-password"
```

### SSH Tunnels

**Remote Gateway Access:**
```bash
# Forward local port to remote Gateway
ssh -L 18789:localhost:18789 user@remote-server

# Connect CLI to remote Gateway
openclaw agent --gateway ws://localhost:18789
```

### Reverse Proxy

**nginx Example:**
```nginx
server {
  listen 443 ssl;
  server_name openclaw.example.com;
  
  location / {
    proxy_pass http://127.0.0.1:18789;
    proxy_http_version 1.1;
    proxy_set_header Upgrade $http_upgrade;
    proxy_set_header Connection "upgrade";
    proxy_set_header Host $host;
  }
}
```

## 🔄 Session Management

### Session Commands

**In-Chat Commands:**
- `/status` - Show session info
- `/new` or `/reset` - Start fresh session
- `/compact` - Compress context (summarize old messages)
- `/think <level>` - Change thinking level
- `/verbose on|off` - Toggle verbose output
- `/usage <mode>` - Configure usage display

**Group Commands (Owner-Only):**
- `/restart` - Restart Gateway
- `/activation mention|always` - Set activation mode

### Session Configuration

**Per-Session Settings:**
```typescript
interface SessionConfig {
  model: string;              // AI model
  thinkingLevel: ThinkingLevel;
  verboseLevel: number;
  sendPolicy: SendPolicy;     // How to send responses
  groupActivation: 'mention' | 'always';
  elevated: boolean;          // Sudo access
}
```

**Update Via API:**
```typescript
await gateway.sessions.patch(sessionId, {
  model: 'claude-3-7-sonnet',
  thinkingLevel: 'high'
});
```

### Agent-to-Agent Communication

**Session Tools:**
- `sessions_list` - List all active sessions
- `sessions_history` - Get conversation history
- `sessions_send` - Send message to another session

**Example Use Case:**
```
User → Session A: "Ask Session B to research topic X"
Session A uses sessions_send → Session B
Session B responds → Session A
Session A → User: "Here's what Session B found"
```

## 🎭 Advanced Features

### Voice Integration

**Voice Wake:**
- Always-on listening
- Custom wake words
- Multi-language support
- Sensitivity adjustment

**Talk Mode:**
- Continuous conversation
- Push-to-talk option
- Auto speech-to-text
- Text-to-speech responses
- ElevenLabs integration

### Canvas & A2UI

**Use Cases:**
- Data visualization
- Interactive dashboards
- Form generation
- Custom UI components
- Real-time updates

**Canvas API:**
```typescript
// Agent can control Canvas
canvas.push({ type: 'html', content: '<h1>Hello</h1>' });
canvas.reset();
canvas.eval('window.alert("Hi")');
```

### Multi-Agent Routing

**Route Different Channels to Different Agents:**
```yaml
routing:
  - from: whatsapp:+1234567890
    agent: personal-agent
    workspace: ~/openclaw/personal
  
  - from: slack:work-team
    agent: work-agent
    workspace: ~/openclaw/work
  
  - from: discord:community-server
    agent: community-agent
    workspace: ~/openclaw/community
```

## 📦 Deployment Options

### NPM (Global Install)

```bash
npm install -g openclaw@latest
openclaw onboard --install-daemon
```

### Docker

```bash
docker run -d \
  -p 18789:18789 \
  -v ~/.openclaw:/root/.openclaw \
  openclaw/openclaw:latest
```

### Nix

```nix
{
  services.openclaw = {
    enable = true;
    port = 18789;
    config = {
      channels.telegram.enabled = true;
      # ...
    };
  };
}
```

### systemd (Linux)

```ini
[Unit]
Description=OpenClaw Gateway
After=network.target

[Service]
Type=simple
User=openclaw
ExecStart=/usr/local/bin/openclaw gateway
Restart=always

[Install]
WantedBy=multi-user.target
```

### launchd (macOS)

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" ...>
<plist version="1.0">
<dict>
  <key>Label</key>
  <string>ai.openclaw.gateway</string>
  <key>ProgramArguments</key>
  <array>
    <string>/usr/local/bin/openclaw</string>
    <string>gateway</string>
  </array>
  <key>RunAtLoad</key>
  <true/>
  <key>KeepAlive</key>
  <true/>
</dict>
</plist>
```

## 🎯 Best Practices

1. **Start with pairing mode** - Security first
2. **Use Tailscale Serve** - For remote access (not Funnel)
3. **Enable authentication** - Always for remote Gateway
4. **Regular backups** - Session data is valuable
5. **Monitor usage** - Watch token consumption
6. **Update regularly** - Stay current with releases
7. **Run doctor** - Periodic health checks
8. **Review logs** - Catch issues early
9. **Test channels** - Verify connectivity
10. **Document config** - Keep notes on customizations
