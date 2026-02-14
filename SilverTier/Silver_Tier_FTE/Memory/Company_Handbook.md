# Silver Tier Standard Operating Procedures

**The Workflow:**
1.  **Trigger:** You see a file in `/Inbox`.
2.  **Plan:** You CREATE a file in `/Plans` named `PLAN_[TaskName].md` breaking down the steps.
3.  **Draft:** You CREATE a file in `/Drafts`.
    *   For Email: `EMAIL_[Recipient].md` (Format: TO: x, SUBJECT: y, BODY: z).
    *   For WhatsApp: `WHATSAPP_[Name].md` (Format: PHONE: x, MESSAGE: y).
    *   For LinkedIn: `LINKEDIN_[Topic].md` (Format: CONTENT: x).
4.  **Wait:** You STOP. Do not execute. Tell the user: 'Draft created. Please move it to Outbox to execute.'

---
Rule #1: NEVER execute a tool directly. Always write a Plan, then write a Draft, and wait for the user to move the Draft to Outbox.
