# MCP Self-Check — Answers

---

## Conceptual

---

### 1. What problem does MCP solve, and how does it change N×M to N+M?

**The problem:** Before MCP, every AI application had to build a custom integration with every tool or data source it needed. With N AI applications and M tools, you needed N×M custom connectors. Each pair required its own protocol, authentication scheme, error handling, and maintenance surface.

**The solution:** MCP introduces a universal standard interface. Every tool builds one MCP server. Every AI application builds one MCP client. The integration count drops to N+M.

```
Before:  Claude ──── FileSystem connector
         Claude ──── Slack connector
         GPT   ──── FileSystem connector    → N×M connectors
         GPT   ──── Slack connector

After:   Claude ── MCP Client ╌╌ MCP Server ── FileSystem
         GPT    ── MCP Client ╌╌ MCP Server ── Slack        → N+M connectors
```

**The key insight:** MCP standardizes *how* context is exchanged, not *what* the AI does with it. It is the USB-C of AI tools — any compliant host connects to any compliant server, regardless of who built either.

---

### 2. What is the difference between MCP Host, Client, and Server?

These are three distinct roles. Confusing them is a common mistake.

| Role | What it is | Example |
|------|-----------|---------|
| **Host** | The AI application that orchestrates everything. Creates and manages MCP clients. | Claude Desktop, VS Code + Copilot, your custom agent app |
| **Client** | A component *inside* the host that maintains a dedicated 1:1 connection to one server. If the host connects to 3 servers, it creates 3 clients. | Created programmatically by the host |
| **Server** | A program that exposes tools, resources, and prompts. Can be local or remote — the label refers to role, not location. | A filesystem server, a database server, a web search server |

**The critical detail:** Client and Server are 1:1 per connection. The Host is the thing that holds multiple clients and coordinates them. When people say "the agent calls a tool," what actually happens is: Host instructs Client → Client sends JSON-RPC to Server → Server executes → Server responds to Client → Client returns result to Host.

---

### 3. Why does MCP use JSON-RPC 2.0 instead of REST?

**One-line answer:** REST is request-response only. JSON-RPC 2.0 is bidirectional.

**The full reason:** MCP needs the *server* to initiate messages to the *client* — not just respond to them. Two concrete cases:

1. **Sampling:** A server needs to ask the host's LLM to generate a completion. That's a server→client request, which REST cannot express without polling or webhooks.
2. **Notifications:** When a server's tool list changes, it pushes `notifications/tools/list_changed` to the client. No polling, no client re-request — the server initiates.

JSON-RPC 2.0 supports three message types that enable this:

```jsonc
// Request — expects a response (has "id")
{"jsonrpc": "2.0", "id": 1, "method": "tools/list", "params": {}}

// Response
{"jsonrpc": "2.0", "id": 1, "result": { ... }}

// Notification — fire-and-forget, no response (no "id")
{"jsonrpc": "2.0", "method": "notifications/tools/list_changed"}
```

REST would require the client to poll for changes or maintain a webhook — both worse than a persistent bidirectional channel.

---

### 4. What is the difference between STDIO and Streamable HTTP transport?

**STDIO** and **Streamable HTTP** are the two transport implementations. They define *how* JSON-RPC messages travel, not what they contain.

| | STDIO | Streamable HTTP |
|--|-------|----------------|
| **Mechanism** | stdin/stdout of a child process | HTTP POST (client→server) + optional SSE (server→client) |
| **Where server runs** | Local machine only (child process) | Anywhere — local or remote |
| **Clients per server** | One (1:1 by definition) | Many (stateless HTTP, scales horizontally) |
| **Authentication** | None needed (OS process isolation) | OAuth 2.1 required for remote servers |
| **Overhead** | Zero network overhead | Network latency + HTTP overhead |
| **Streaming** | Inherent (pipe is a stream) | SSE for server→client push |

**When to use each:**

- **STDIO** — local tools: filesystem access, local database, CLI wrappers, dev tooling. Simple, secure, no auth setup.
- **Streamable HTTP** — remote/cloud services: web search, SaaS APIs, shared company tools, multi-tenant deployments. Required when the server must serve multiple clients simultaneously.

---

### 5. What happens during the Initialization handshake? What is negotiated?

The handshake is a 3-step sequence that must complete before any other messages are valid. MCP is a stateful protocol — there is no "just call a tool" without going through this first.

**Step 1 — Client sends `initialize`:**
```json
{
  "jsonrpc": "2.0", "id": 1, "method": "initialize",
  "params": {
    "protocolVersion": "2025-06-18",
    "capabilities": { "elicitation": {} },
    "clientInfo": { "name": "my-agent", "version": "1.0.0" }
  }
}
```

**Step 2 — Server responds with its capabilities:**
```json
{
  "jsonrpc": "2.0", "id": 1,
  "result": {
    "protocolVersion": "2025-06-18",
    "capabilities": {
      "tools": { "listChanged": true },
      "resources": {}
    },
    "serverInfo": { "name": "my-mcp-server", "version": "2.0.0" }
  }
}
```

**Step 3 — Client signals ready:**
```json
{"jsonrpc": "2.0", "method": "notifications/initialized"}
```

**What gets negotiated:**
- **Protocol version** — if incompatible, the connection terminates immediately
- **Server capabilities** — which primitives the server supports (tools, resources, prompts) and whether it will send list-change notifications (`listChanged: true`)
- **Client capabilities** — which client primitives the server is allowed to use (sampling, elicitation)

If the server declares `tools.listChanged: true` but the client never declared support for it, the client can ignore those notifications. Capability negotiation makes the protocol forward-compatible.

---

## Primitives

---

### 1. What are the three server primitives and what is each used for?

Server primitives are what an MCP server exposes to clients. There are three:

**Tools — model-controlled actions**
Executable functions the LLM decides to call. Think: "do something." File writes, API calls, database queries, computations. The LLM reads the tool's JSON schema, decides when and how to call it, and uses the result.

```
tools/list  → discover available tools
tools/call  → execute a tool
```

**Resources — application-controlled data**
Read-only data sources. Think: "read something." Files, database records, API responses. Unlike tools, the *host or user* decides which resources to attach — the LLM doesn't autonomously pull resources. Identified by URI.

```
resources/list  → enumerate available resources
resources/read  → retrieve content at a URI
```

**Prompts — user-controlled templates**
Reusable prompt templates with optional parameters. Think: "frame the task." System prompts, few-shot examples, task-specific instruction sets. The *user* selects which prompt to apply.

```
prompts/list  → enumerate available prompts
prompts/get   → retrieve a prompt with arguments filled in
```

**The control axis:**
```
Tools    → model decides when to invoke  (agent autonomy)
Resources → host/user decides what to attach (application control)
Prompts   → user decides which template to use (user control)
```

---

### 2. What are the three client primitives and why would a server need them?

Client primitives are capabilities the *host* exposes to servers — things the server can request from the client side.

**Sampling — server requests an LLM completion**
The server sends `sampling/createMessage` to ask the host's LLM to generate text. The server gets LLM access without embedding a model SDK or managing API keys.

*Why a server needs this:* Enables server-side agent loops. A tool server can reason about its own output, run multi-step logic, or make decisions — all using the host's LLM — without any custom scaffolding. This was a major addition in the 2025-11-25 spec.

**Elicitation — server requests input from the user**
The server sends an elicitation request when it needs more information to proceed: confirmation before a destructive action, a missing required parameter, a clarification.

*Why a server needs this:* Without elicitation, a server that hits an ambiguous state has two bad options — fail loudly or make an assumption. Elicitation lets it ask the user directly, keeping the human in the loop for consequential decisions.

**Logging — server sends structured log messages to the client**
The server emits structured log events that the host surfaces for debugging and monitoring.

*Why a server needs this:* Servers run as isolated processes (especially with STDIO). Without a logging channel, there's no visibility into server-side behavior from the host's perspective. Logging bridges that observability gap.

---

### 3. What problem do Tasks solve? How do they change the interaction pattern?

**The problem:** Standard JSON-RPC is synchronous. The client sends a request and blocks waiting for a response. For operations that take seconds, minutes, or longer (running a build, doing a deep research query, processing a large file), the client will time out.

**How Tasks solve it — call now, fetch later:**

Without Tasks:
```
Client ──[request]──▶ Server
Client ◀──[waits 5 minutes]── Server   ← timeout risk
```

With Tasks:
```
Client ──[request]──▶ Server
Client ◀──[task handle]── Server       ← returns immediately

... client can disconnect, do other work, close laptop ...

Client ──[GET /tasks/{id}]──▶ Server
Client ◀──[status: COMPLETED, result: {...}]── Server
```

The interaction pattern shifts from **synchronous blocking** to **async with polling**. The client gets a task handle immediately and checks status when ready.

**Why this matters for agent infrastructure:** This is MCP's native session persistence mechanism. A user starts a complex agent task, closes their laptop, comes back 20 minutes later, and retrieves the result — without the host having to maintain a live connection the entire time.

**The tradeoff:** Tasks are experimental (added 2025-11-25) and introduce new attack surface. They can hide misbehavior, consume background resources, and persist across sessions. Task lifecycle management — expiry, cancellation, resource cleanup — needs explicit handling in production.

---

### 4. What is the difference between a Tool and a Resource?

| | Tool | Resource |
|--|------|----------|
| **Purpose** | Take an action | Provide data |
| **Side effects** | Yes — tools *do* things | No — read-only |
| **Who decides to use it** | The LLM (model-controlled) | The host or user (application-controlled) |
| **Identified by** | Name + JSON schema for inputs | URI |
| **Analogy** | A function call | A file attachment |

**Concrete example:**
- `read_file` as a **Tool** — the LLM autonomously decides to call it, passes a path, gets content back. Has no side effects, but the LLM controls when it runs.
- `/files/report.md` as a **Resource** — the user or host attaches it to the context. The LLM sees the content, but never "called" anything to get it.

**The practical distinction:** If you're giving the LLM the ability to autonomously pull data on demand → Tool. If you're injecting data into context that the host or user controls → Resource.

Both can return the same bytes. The difference is *who controls the invocation* and *whether there are side effects.*
