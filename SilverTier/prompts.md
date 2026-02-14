This is a complete, step-by-step guide to building the **Silver Tier Digital FTE** with **Gmail, LinkedIn, and WhatsApp** capabilities.

We will strictly follow the **Silver Tier Architecture**:

1. **The Brain (Reasoning Loop):** Separating planning from acting.
2. **The Hands (Tools):** Custom scripts for Gmail, LinkedIn, and WhatsApp.
3. **The Conscience (HITL):** A strict approval workflow (Draft  Approve  Send).

### **Prerequisites**

* **Directory:** We will create a fresh folder: `Silver_Tier_FTE` (Current Direcotory).
* **Browser Tool:** We will use **Puppeteer** (via the official MCP server) instead of the Anthropic-only tool.
* **WhatsApp:** We will use `pywhatkit` (simulates a real user via WhatsApp Web).

---


#### **Step 1: Environment & Architecture Setup**

> "I am building a Silver Tier AI Employee in a new directory. Please execute the following setup:
> 1. Create a root directory named `Silver_Tier_FTE`.
> 2. Inside it, create these specific folders for the workflow:
> * `/Inbox` (For new tasks)
> * `/Plans` (For the agent's reasoning files)
> * `/Drafts` (For items waiting for my approval)
> * `/Outbox` (For approved items ready to send)
> * `/Sent` (For completed items)
> * `/Memory` (For context like `Dashboard.md` and `Company_Handbook.md`)
> 
> 
> 3. Create a `.env` template file containing placeholders for: `GMAIL_USER`, `GMAIL_APP_PASSWORD`, `LINKEDIN_USER`, `LINKEDIN_PASSWORD`.
> 4. Initialize a `package.json` file in the root (for Node.js tools) and a `requirements.txt` (for Python tools).
> 5. Create a `Company_Handbook.md` in `/Memory` that explicitly states: 'Rule #1: NEVER execute a tool directly. Always write a Plan, then write a Draft, and wait for the user to move the Draft to Outbox.'"
> 
> 

#### **Step 2: The "Hands" - Gmail & WhatsApp (Python)**

*We will build custom scripts for communication. Using Python is easier here for `pywhatkit`.*

> "Create a `tools` directory inside `Silver_Tier_FTE`. Now, generate two Python scripts inside it:
> 1. **`gmail_sender.py`**:
> * Use the `smtplib` library.
> * Function: `send_email(to, subject, body)`.
> * It must load credentials from the `.env` file.
> 
> 
> 2. **`whatsapp_sender.py`**:
> * Use the `pywhatkit` library.
> * Function: `send_whatsapp(phone_no, message)`.
> * It should verify that the `phone_no` includes the country code.
> * **Important:** Add a 15-second delay to ensure the browser tab opens before sending.
> Finally, update `requirements.txt` to include `secure-smtplib` and `pywhatkit`."

#### **Step 3: The "Eyes" - Browser & LinkedIn (MCP)**

> "I need to set up the Browser capability for the Silver Tier.
> 1. Create an `mcp_config.json` file in the root.
> 2. Configure a new MCP server named 'puppeteer'. Use the official package: `@modelcontextprotocol/server-puppeteer`.
> 3. Tell me the exact command to run to install this server (e.g., `npm install @modelcontextprotocol/server-puppeteer`).
> 4. Create a specialized instruction file `Memory/LinkedIn_SOP.md` that describes how to post on LinkedIn: 'Navigate to linkedin.com, check for login selectors, find the "Start a post" button, type the content, and click Post.'
> 5. **Constraint:** The Agent must NOT perform these actions automatically. It must only propose them in a Plan."

#### **Step 4: The "Orchestrator" (The Manager Script)**

*This is the most important part of Silver Tier. This script replaces the human clicking "Send". It watches the `/Outbox` and fires the guns.*

> "Create the core automation script named `orchestrator.py` in the root. This script acts as the 'Silver Tier Manager'.
> **Logic:**
> 1. Continuously watch the `/Outbox` folder.
> 2. When a file appears, check its filename prefix:
> * **If `EMAIL_...md**`: Parse the file for 'To:', 'Subject:', and 'Body:'. Call `tools/gmail_sender.py` to send it.
> * **If `WHATSAPP_...md**`: Parse for 'Phone:' and 'Message:'. Call `tools/whatsapp_sender.py`.
> * **If `LINKEDIN_...md**`: Use a subprocess to run a new script `tools/linkedin_poster.py` (please create this stub) that uses Playwright/Puppeteer to post the content found in the file.
> 
> 
> 3. After successful execution, move the markdown file to `/Sent` and append a log entry to `Memory/Dashboard.md`.
> 4. If an error occurs, move the file back to `/Inbox` with an error note appended."
> 
> 

#### **Step 5: The Activation (Operating Instructions)**

> "Update `Memory/Company_Handbook.md` with the final **Silver Tier Standard Operating Procedures**:
> **The Workflow:**
> 1. **Trigger:** You see a file in `/Inbox`.
> 2. **Plan:** You CREATE a file in `/Plans` named `PLAN_[TaskName].md` breaking down the steps.
> 3. **Draft:** You CREATE a file in `/Drafts`.
> * For Email: `EMAIL_[Recipient].md` (Format: TO: x, SUBJECT: y, BODY: z).
> * For WhatsApp: `WHATSAPP_[Name].md` (Format: PHONE: x, MESSAGE: y).
> * For LinkedIn: `LINKEDIN_[Topic].md` (Format: CONTENT: x).
> 4. **Wait:** You STOP. Do not execute. Tell the user: 'Draft created. Please move it to Outbox to execute.'
> **verify:** Check that you understand this by summarizing the workflow back to me."
