# Silver Tier AI Employee - Digital FTE

Welcome to the **Silver Tier** of your Digital FTE. This version introduces high-level reasoning, multi-channel communication (Gmail, LinkedIn, WhatsApp), and a strict Human-in-the-loop (HITL) safety workflow.

## 🚀 Key Improvements (Silver Tier)

### 1. Claude-Style Reasoning Loop
The agent no longer just summarizes files. It now **analyzes, strategizes, and proposes** actions using a dedicated reasoning loop. Every task results in a `PLAN_*.md` file detailing the agent's thought process.

### 2. Multi-Channel Watchers
- **Gmail**: Automatically monitors your inbox for new tasks.
- **LinkedIn**: Checks for notifications and business opportunities.
- **WhatsApp**: Monitors incoming messages for urgent requests.

### 3. Human-in-the-loop (HITL) Workflow
Safety first. The agent **drafts** communications but **never sends** them without your permission.
- **Drafts Folder**: Where the agent places proposed emails or posts.
- **Outbox Folder**: Where you move approved drafts to trigger execution.

### 4. Advanced Automation Tools
- **LinkedIn Poster**: Automatically posts business updates to generate sales.
- **Email MCP Server**: Provides a standardized interface for external agents to send emails.
- **Task Scheduler**: Built-in support for Windows Task Scheduler to keep everything running 24/7.

---

## 📂 Directory Structure

- `Inbox/`: Raw tasks and incoming emails/messages.
- `Plans/`: The agent's reasoning and strategy documents.
- `Drafts/`: Proposed communications (Email, LinkedIn, WhatsApp) awaiting your review.
- `Outbox/`: Move files here to authorize the agent to send/post them.
- `Sent/`: Archive of successfully executed actions.
- `Watchers/`: The "Eyes" of the system (monitoring scripts).
- `Tools/`: The "Hands" of the system (execution scripts).
- `Skills/`: Portable capability documentation for agents.

---

## 🛠️ Setup

1. **Credentials**: Copy `.env.template` to `.env` and fill in your API keys and login details.
2. **Dependencies**: Managed via `uv`. Run `uv sync` to ensure all libraries are installed.
3. **Playwright**: Run `python -m playwright install` for LinkedIn automation.

---

## 🏃 Running the System

You should run three main processes (in separate terminals or via Task Scheduler):

### 1. The Eyes (Watchers)
Choose which channels to monitor:
```powershell
uv run Watchers/gmail_watcher.py
```

### 2. The Brain (Agent Loop)
Processes the Inbox and creates Plans/Drafts:
```powershell
uv run agent_loop.py
```

### 3. The Manager (Orchestrator)
Executes approved tasks from the Outbox:
```powershell
uv run orchestrator.py
```

---

## 🧠 Agent Skills
Each capability (LinkedIn Posting, Emailing, HITL Workflow) is documented in the `Skills/` directory. Use these files to train other agents (like Claude Code or Gemini CLI) on how to interact with your Digital FTE.
