# How to Run the AI Employee (Bronze Tier)

## Prerequisites
- [uv](https://github.com/astral-sh/uv) installed on your system.

## Setup
1. Open a terminal in the `f:\ai_dd\digital_fte\AI_Employee_Vault` directory.
2. The virtual environment and dependencies are already managed by `uv`.
## New Features (Phase 4)

### 1. System Logging
All activity from the watcher and agent is now logged to `AI_Employee_Vault/Logs/system.log`. This includes:
- File detection and movement.
- AI processing status.
- Errors and heartbeats.

### 2. Obsidian Ready
The `Documentation/Dashboard.md` and `Documentation/Company_Handbook.md` files now include YAML frontmatter. You can open the `AI_Employee_Vault` folder as an Obsidian Vault to see:
- Tagged documents.
- Automatic task tracking.
- Metadata for your AI Employee.

### 3. Formalized Skills
Check the `Skills/` directory for detailed documentation on what your agent can do. The `Document_Summarizer.md` file defines the current intelligence level of your Digital FTE.

## Running the Components

You need to run two processes simultaneously. You can do this in separate terminal windows.

### 1. File Watcher
This script monitors the `Drop_Zone` folder and moves any new files to `Needs_Action` while creating a metadata file.
```powershell
uv run filesystem_watcher.py
```

### 2. Agent Loop (Ralph Wiggum Mode)
This script processes files in `Needs_Action`, creates a plan, summarizes the content into `Dashboard.md`, and moves the file to `Done`.
```powershell
uv run agent_loop.py
```

## How to Test
1. Create a text file or drop any file into `AI_Employee_Vault/Drop_Zone`.
2. Observe the terminal for `filesystem_watcher.py` – it will detect and move the file.
3. Observe the terminal for `agent_loop.py` – it will process the file.
4. Check `AI_Employee_Vault/Documentation/Dashboard.md` for the summary.
5. Check `AI_Employee_Vault/Done` for the processed file and its metadata.
6. Check `AI_Employee_Vault/PHR` for the prompt record.
