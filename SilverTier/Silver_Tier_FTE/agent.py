
import os
import time
import json
import openai
from dotenv import load_dotenv
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# --- Configuration ---
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

INBOX_PATH = "Inbox"
PLANS_PATH = "Plans"
DRAFTS_PATH = "Drafts"
MEMORY_PATH = "Memory"

# --- LLM Prompt ---
SYSTEM_PROMPT = """
You are "Silver Tier FTE", a digital AI employee. Your task is to read user requests from the Inbox, understand them, and prepare a draft for action. You must strictly follow the provided workflow and formatting rules.

**Workflow:**
1.  **Read the Task:** A user will provide a task in a markdown file.
2.  **Consult Your Memory:** Review the provided context from the /Memory folder (Company Handbook, SOPs, etc.) to align your response with company policy.
3.  **Formulate a Plan:** Detail the steps you will take to complete the task.
4.  **Create a Draft:** Generate the final content for execution (e.g., an email or a LinkedIn post). The draft must be in a structured format with a specific filename.

**Output Format:**
You MUST respond with a single JSON object. Do not add any text before or after the JSON.
The JSON object must have the following structure:
{
  "plan": "A step-by-step plan for how you will approach the task. This will be saved in the /Plans folder.",
  "draft_filename": "The name for the draft file. It MUST start with 'EMAIL_', 'WHATSAPP_', or 'LINKEDIN_'. For example: 'EMAIL_to_alex.doe.md' or 'LINKEDIN_announcement.md'.",
  "draft_content": "The full, ready-to-execute content of the draft. For emails, this must be in the format 'TO: ...
SUBJECT: ...
BODY: ...'. For other types, just the content is sufficient."
}

**Example Email Draft Content:**
"TO: user@example.com
SUBJECT: Hello
BODY:
This is the body of the email."
"""

class Agent:
    def __init__(self):
        self.client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    def get_memory_context(self):
        """Reads all files in the Memory folder to provide context to the LLM."""
        context = ""
        for filename in os.listdir(MEMORY_PATH):
            filepath = os.path.join(MEMORY_PATH, filename)
            if os.path.isfile(filepath):
                with open(filepath, 'r', encoding='utf-8') as f:
                    context += f"--- Content from {filename} ---" + f.read()
        return context

    def process_task(self, task_path):
        """Processes a single task file from the Inbox."""
        print(f"Processing new task: {task_path}")
        try:
            with open(task_path, 'r', encoding='utf-8') as f:
                task_content = f.read()

            memory_context = self.get_memory_context()
            
            prompt = f"""
            {memory_context}
            --- User Task ---
            {task_content}
            """

            response = self.client.chat.completions.create(
                model="gpt-4-turbo", # Or your preferred model
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": prompt}
                ],
                response_format={"type": "json_object"}
            )

            response_data = json.loads(response.choices[0].message.content)
            
            plan = response_data.get("plan")
            draft_filename = response_data.get("draft_filename")
            draft_content = response_data.get("draft_content")

            if not all([plan, draft_filename, draft_content]):
                raise ValueError("LLM response was missing required fields.")

            # Create Plan file
            plan_filename = f"PLAN_{os.path.basename(task_path)}"
            with open(os.path.join(PLANS_PATH, plan_filename), 'w', encoding='utf-8') as f:
                f.write(plan)

            # Create Draft file
            with open(os.path.join(DRAFTS_PATH, draft_filename), 'w', encoding='utf-8') as f:
                f.write(draft_content)

            # Move processed task out of Inbox
            os.remove(task_path)

            print(f">>> Draft created: {os.path.join(DRAFTS_PATH, draft_filename)}")
            print("Please review the draft. If you approve, move it to the /Outbox folder to be sent.")

        except Exception as e:
            print(f"Error processing task {task_path}: {e}")
            # Optionally move the file to an error folder
            error_folder = "Inbox/Errors"
            if not os.path.exists(error_folder):
                os.makedirs(error_folder)
            os.rename(task_path, os.path.join(error_folder, os.path.basename(task_path)))


class InboxWatcher(FileSystemEventHandler):
    def __init__(self, agent):
        self.agent = agent

    def on_created(self, event):
        if not event.is_directory and not os.path.basename(event.src_path).startswith("ERROR_"):
            # Wait a moment to ensure file write is complete
            time.sleep(1)
            self.agent.process_task(event.src_path)

if __name__ == "__main__":
    print("Initializing Silver Tier FTE Agent...")
    
    if not os.getenv("OPENAI_API_KEY"):
        print("""
--- IMPORTANT ---
OPENAI_API_KEY environment variable not found.
Please create a file named '.env' in this directory and add the following line:
OPENAI_API_KEY='your_openai_api_key'
""")
    else:
        agent = Agent()
        observer = Observer()
        observer.schedule(InboxWatcher(agent), INBOX_PATH, recursive=False)
        observer.start()
        print(f"Agent started. Watching for new tasks in '{INBOX_PATH}'...")
        print("Press Ctrl+C to stop.")
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            observer.stop()
        observer.join()
        print("Agent stopped.")
