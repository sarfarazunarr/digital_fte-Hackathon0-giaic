# How to Run the AI Employee (Bronze Tier)

## Prerequisites
- [uv](https://github.com/astral-sh/uv) installed on your system.

## Setup
1. Open a terminal in the `f:\ai_dd\digital_fte\AI_Employee_Vault` directory.
2. The virtual environment and dependencies are already managed by `uv`.




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
4. Check `AI_Employee_Vault/Dashboard.md` for the summary.
5. Check `AI_Employee_Vault/Done` for the processed file and its metadata.
6. Check `AI_Employee_Vault/PHR` for the prompt record.
