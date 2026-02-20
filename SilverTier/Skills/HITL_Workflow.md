# Skill: Human-in-the-loop (HITL) Workflow

## Description
Ensures all sensitive actions (Email, LinkedIn, WhatsApp) are approved by a human before execution.

## Workflow
1. **Inbox**: Raw task enters.
2. **Reasoning**: Agent creates a `Plan.md` in `Plans/`.
3. **Draft**: Agent creates a `DRAFT_*.md` in `Drafts/`.
4. **Approval**: YOU (the human) review the draft.
5. **Execution**: Move the draft to `Outbox/` to send/post.
6. **Confirmation**: Orchestrator moves item to `Sent/`.

## Benefit
Prevents accidental or incorrect AI-generated communication.
