# OpenClaw Documentation

This directory contains comprehensive documentation about **OpenClaw**, a personal AI assistant framework, to help you review and study its source code, architecture, and components.

## 📚 Documentation Overview

1. **[Architecture Overview](./architecture.md)** - Core architecture, design patterns, and system components
2. **[Source Code Review](./source-code-review.md)** - Guide to navigating and understanding the OpenClaw codebase
3. **[Components & Features](./components-features.md)** - Detailed breakdown of all major components and features
4. **[Integration Guide](./integration-possibilities.md)** - How to integrate OpenClaw concepts with other projects
5. **[Visual Study Guide](./visual-guide.md)** - Diagrams, flowcharts, and visual references

## 🦞 What is OpenClaw?

**OpenClaw** is a personal AI assistant that you run on your own devices. It's designed to be:

- **Multi-channel** - Works with WhatsApp, Telegram, Slack, Discord, Google Chat, Signal, iMessage, Microsoft Teams, and more
- **Local-first** - Runs on your own infrastructure with a local control plane (Gateway)
- **Extensible** - Supports custom tools, skills, and integrations
- **Voice-enabled** - Includes Voice Wake and Talk Mode for hands-free interaction
- **Cross-platform** - Available on macOS, Linux, Windows (WSL2), iOS, and Android

## 🔗 Official Resources

- **Repository**: [github.com/openclaw/openclaw](https://github.com/openclaw/openclaw)
- **Website**: [openclaw.ai](https://openclaw.ai)
- **Documentation**: [docs.openclaw.ai](https://docs.openclaw.ai)
- **Discord**: [discord.gg/clawd](https://discord.gg/clawd)
- **License**: MIT

## 🚀 Quick Start

```bash
# Install OpenClaw globally
npm install -g openclaw@latest

# Run the onboarding wizard
openclaw onboard --install-daemon

# Start the Gateway
openclaw gateway --port 18789 --verbose

# Send a message
openclaw message send --to +1234567890 --message "Hello from OpenClaw"

# Talk to the assistant
openclaw agent --message "Ship checklist" --thinking high
```

## 🏗️ High-Level Architecture

```
WhatsApp / Telegram / Slack / Discord / etc.
               │
               ▼
┌───────────────────────────────┐
│            Gateway            │
│       (control plane)         │
│     ws://127.0.0.1:18789      │
└──────────────┬────────────────┘
               │
               ├─ Pi agent (RPC)
               ├─ CLI (openclaw …)
               ├─ WebChat UI
               ├─ macOS app
               └─ iOS / Android nodes
```

## 📖 How to Use This Documentation

1. **For Quick Visual Overview**: Start with [Visual Study Guide](./visual-guide.md)
2. **For Architecture Study**: Read [Architecture Overview](./architecture.md)
3. **For Code Deep Dive**: Follow [Source Code Review](./source-code-review.md)
4. **For Feature Understanding**: Check [Components & Features](./components-features.md)
5. **For Integration Ideas**: See [Integration Guide](./integration-possibilities.md)

## 🎯 Key Takeaways for AI Chatbot Developers

OpenClaw demonstrates several advanced patterns relevant to AI chatbot development:

1. **Multi-channel abstraction** - Unified interface for different messaging platforms
2. **Local-first architecture** - Privacy-focused design with local control
3. **Session management** - Sophisticated conversation context handling
4. **Tool/skill system** - Extensible capabilities via plugins
5. **Voice integration** - Speech recognition and synthesis
6. **Real-time communication** - WebSocket-based control plane
7. **Security model** - DM pairing, allowlists, and authentication

These concepts can inspire improvements to other chatbot projects!
