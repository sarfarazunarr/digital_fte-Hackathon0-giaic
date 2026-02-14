# Silver Tier Digital FTE

This project implements the "Silver Tier" architecture for a digital AI employee. It provides a structured, human-in-the-loop (HITL) workflow for executing tasks related to email, WhatsApp, and LinkedIn, ensuring that no action is taken without explicit user approval.

## Core Architecture

The system is built on three core principles:

1.  **The Brain (Reasoning Loop):** The AI agent separates planning from acting. It first creates a plan of action.
2.  **The Hands (Tools):** Custom scripts (`gmail_sender.py`, `whatsapp_sender.py`, etc.) that are capable of interacting with external services.
3.  **The Conscience (HITL):** A strict Draft -> Approve -> Send workflow that enforces human oversight for every action. The AI *cannot* execute tools directly.

---

## Directory Structure

The project uses a folder-based workflow to manage tasks:

-   **/Inbox**: New tasks for the agent are placed here as markdown files.
-   **/Plans**: The agent's detailed step-by-step plans for completing a task.
-   **/Drafts**: The agent places the final, ready-to-execute action items here (e.g., the content of an email). **This is the user approval gate.**
-   **/Outbox**: The user moves files from `/Drafts` to this folder to approve and trigger their execution.
-   **/Sent**: Successfully executed items are moved here for a historical record.
-   **/Memory**: Contains long-term context, standard operating procedures (`Company_Handbook.md`, `LinkedIn_SOP.md`), and a log of all executed actions (`Dashboard.md`).
-   **/tools**: Contains the individual Python scripts that act as the "Hands" of the agent.

---

## Setup and Installation

### 1. Configure Environment Variables

In the root of the project, you will find a `.env` file. Fill in your credentials:

```plaintext
GMAIL_USER=your_gmail_username@gmail.com
GMAIL_APP_PASSWORD=your_gmail_app_password
LINKEDIN_USER=your_linkedin_username
LINKEDIN_PASSWORD=your_linkedin_password
```

**Note on `GMAIL_APP_PASSWORD`**: This is **not** your regular Gmail password. You need to generate an "App Password" from your Google Account security settings.

### 2. Install Dependencies

The project uses both Python and Node.js dependencies.

**For Python:**
Make sure you have Python installed. Then, from the project's root directory (`/Silver_Tier_FTE`), run:
```bash
pip install -r requirements.txt
```

**For Node.js (Browser Automation):**
Make sure you have Node.js and npm installed. The browser automation capabilities are provided by an MCP server.
```bash
# This was already run, but is here for reference
npm install
```

---

## How to Run the System

The core of the system is the `orchestrator.py` script, which watches the `/Outbox` folder.

To start the Digital FTE, run the following command from the `Silver_Tier_FTE` directory:

```bash
python orchestrator.py
```

The script will initialize and print a message indicating that it is watching for files. It will run continuously until you stop it (e.g., with `Ctrl+C`).

---

## The Workflow in Action

Here is the step-by-step guide to using the Silver Tier FTE:

**Step 1: Create a Task (User)**
-   Create a markdown file in the `/Inbox` directory. For example, `inbox/task1.md` with the content: "Send a welcome email to our new partner at `partner@example.com`."

**Step 2: The Agent Plans (AI)**
-   The agent (conceptually) reads the task.
-   It creates a plan file in the `/Plans` directory, e.g., `PLAN_WelcomePartnerEmail.md`, detailing how it will fulfill the request.

**Step 3: The Agent Creates a Draft (AI)**
-   Following its plan, the agent creates a structured markdown file in the `/Drafts` directory.
-   Example: `Drafts/EMAIL_partner.md`
    ```markdown
    TO: partner@example.com
    SUBJECT: A Warm Welcome!
    BODY:
    Dear Partner,

    We are delighted to have you with us.

    Best,
    The Team
    ```
-   The agent then informs you: **"Draft created. Please move it to Outbox to execute."**

**Step 4: You Approve the Task (User)**
-   Review the file `Drafts/EMAIL_partner.md`.
-   If you approve, **move the file** from the `/Drafts` folder to the `/Outbox` folder.

**Step 5: The Orchestrator Executes (System)**
-   The running `orchestrator.py` script instantly detects the new file in `/Outbox`.
-   It reads the filename (`EMAIL_...`), parses the content, and calls the appropriate tool (`tools/gmail_sender.py`).
-   **On Success:** The email is sent, the file is moved to `/Sent/EMAIL_partner.md`, and a log is added to `Memory/Dashboard.md`.
-   **On Failure:** The file is moved back to `/Inbox` as `ERROR_...EMAIL_partner.md` with an error note appended, allowing for debugging. The failure is also logged to the dashboard.

This human-in-the-loop process ensures complete control and prevents unintended actions, embodying the safety and reliability of the Silver Tier architecture.
