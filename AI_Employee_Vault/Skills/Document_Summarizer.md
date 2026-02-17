# Document Summarizer Skill

## Purpose
Intelligently summarize any document dropped into the vault to provide a quick overview in the Dashboard.

## Pre-requisites
- OpenAI API Key configured in `.env`
- File must be in a readable text format (txt, md, logic etc.)

## Execution Flow
1. **Trigger**: New file detected in `Needs_Action` by the `agent_loop.py`.
2. **Analysis**: Read the entire content of the file.
3. **AI Processing**:
   - Send content to GPT-3.5-Turbo.
   - Request a concise summary highlighting key points.
4. **Output**:
   - Append the summary to `Dashboard.md` with a timestamp.
   - Record the operation in `PHR/` (Prompt History Record).
5. **Log**: Record success or failure in `Logs/system.log`.
6. **Cleanup**: Move the original file and metadata to `Done/`.

## Quality Guidelines
- Summary should not exceed 200 words.
- Maintain a professional and objective tone.
- Flag any sensitive information (e.g., payments) as per `Company_Handbook.md`.
