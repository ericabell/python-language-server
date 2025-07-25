# Phase 1: Understanding LSP Fundamentals

## Learning Goals
- Language Server Protocol architecture and communication model
- JSON-RPC 2.0 messaging format and structure
- Client-server relationship and lifecycle management
- Core LSP capabilities and their purposes
- Understanding requests, responses, and notifications

## Mini-Projects
1. **JSON-RPC Message Parser**: Build a simple function that can parse and validate JSON-RPC 2.0 messages
2. **Echo Server**: Create a basic server that echoes back any message it receives
3. **LSP Message Validator**: Build a validator that checks if messages conform to LSP message structure

## Implementation Goals
1. **Basic Server Setup**: Create a minimal LSP server that can start and respond to initialization
2. **Message Handling**: Implement JSON-RPC message parsing and response generation
3. **Lifecycle Management**: Handle initialize, initialized, and shutdown requests
4. **Capability Negotiation**: Implement basic client-server capability exchange

## Progress Tracking
- [ ] Completed pre-reading materials
- [ ] Built JSON-RPC Message Parser
- [ ] Built Echo Server
- [ ] Built LSP Message Validator
- [ ] Implemented basic server setup
- [ ] Implemented message handling
- [ ] Implemented lifecycle management
- [ ] Implemented capability negotiation
- [ ] Passed all knowledge checks

## Knowledge Checks
- [ ] Explain the difference between notifications and requests in LSP
- [ ] Describe what happens during the server initialization handshake
- [ ] Build a sequence diagram showing the initialization flow
- [ ] Implement a simple ping-pong test between client and server

## Notes
Started reading https://code.visualstudio.com/api/language-extensions/language-server-extension-guide

It seems pretty clear why LSP was created - to solve the problem of multiple editors and multiple languages in a scalable way. The LSP can just be off running in another process, doing it's thing. The editor asks different questions about the code, and that's it. Seems like having an LSP hooked into Claude Code would provide excellent power and better editing capabilities for Claude Code.

A bit disappointing that this page says I need to be familiar with VS Code Extension API - but I don't think that's a problem since my goal isn't to write a VS Code extension.

The first interesting feature a language server usually implements is validation of documents.

But there is more to language servers. They can provide code completion, Find All References, or Go To Definition.

To create a high-quality Language Server, we need to build a good test suite covering its functionalities.

I understand the basic client-server relationship, although maybe not specific details for an LSP - but I think that will become clearer as I move along.

I kind of understand the flow of an LSP session. Seems like there are some document-sync things that happen, and then the server gets a request for something like a completion to happen and replies back. Maybe need more details here?

Moving on to: https://www.jsonrpc.org/specification and focusing on the examples section.

JSON-RPC seems pretty straightfoward. requests, responses, and notifications are pretty easy to understand.

A request will require and id and a response, while a notification has no id and will receive no response.

I don't know that I found much about the initialization handshake... the spec doc mentions handshake in two places, but neither of those explains how the handshake actually works? Also, it's not clear if this is a VS Code extension thing or a JSON-RPC thing. It's probably a VS Code extension thing.

I googled the handshake and found this note:
The VS Code extension initialization handshake refers to the sequence of events and communication that occurs when a VS Code extension is activated and starts running within the VS Code environment. This process ensures the extension is properly loaded, its resources are available, and it can interact with the VS Code API.

What was most interesting or surprising:
Nothing that surprised me. Interesting that the JSON-RPC is so simple, but also seems kinda dangerous in that a server could receive any request to execute something and not really know where it came from or any kind of auth process...

Concepts that seem unclear:
See above in my notes I made as I was reading.

---

## Teacher Feedback & Comments

**Excellent work on your notes! You've grasped the core concepts really well. Let me clarify a few key points:**

### ✅ The Initialization Handshake IS Part of LSP (Not VS Code Specific!)

You found information about VS Code extensions, but the **LSP initialization handshake is actually part of the Language Server Protocol itself**. Here's the actual LSP flow from the official specification:

**The LSP Initialization Sequence:**
1. **Client → Server**: `initialize` request (with client capabilities)
2. **Server → Client**: `InitializeResult` response (with server capabilities) 
3. **Client → Server**: `initialized` notification (signals client is ready)
4. **Now both sides can send normal LSP requests/notifications**

This is the "handshake" - it's how client and server negotiate what features they both support!

### Your Security Observation is Spot-On! 
You're absolutely right that JSON-RPC seems "dangerous" without auth. In practice, LSP servers typically run in trusted environments (same machine, trusted processes), but you're thinking like a good developer about security implications.

### Your Understanding is Excellent
- ✅ You get why LSP was created (N×M problem)
- ✅ You understand requests vs notifications 
- ✅ You see the value for Claude Code integration
- ✅ You grasp that document sync and features like completion are the core value

### Ready for Your First Mini-Project?

Let's build a **JSON-RPC Message Parser**! This will solidify your understanding and give you a foundation for everything else.

**Mini-Project 1: JSON-RPC Message Parser**

Create a Python function that can:
1. Parse a JSON string into a JSON-RPC message
2. Validate it has the required fields (`jsonrpc`, `method`, etc.)
3. Determine if it's a request, response, or notification
4. Return a structured result or error

Want to tackle this? I'll guide you through it step by step, and we can test it with real LSP messages!

