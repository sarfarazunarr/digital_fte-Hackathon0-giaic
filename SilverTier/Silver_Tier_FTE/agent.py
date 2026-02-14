
import os
import time
import asyncio
import json
from typing import Annotated
from pydantic import BaseModel, Field
from agents import Agent, Runner, function_tool
from dotenv import load_dotenv
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import sys

# --- Configuration ---
load_dotenv()

# Add tools directory to path to import skill modules
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'tools'))

INBOX_PATH = "Inbox"
PLANS_PATH = "Plans"
DRAFTS_PATH = "Drafts"
MEMORY_PATH = "Memory"
SENT_PATH = "Sent"
OUTBOX_PATH = "Outbox"

# --- Agent Tools for Creating Drafts ---

@function_tool
def create_email_draft(
    recipient: Annotated[str, "The email address of the recipient."],
    subject: Annotated[str, "The subject line of the email."],
    body: Annotated[str, "The content of the email body."],
    task_filename: Annotated[str, "The original filename of the task in the Inbox."]
):
    """
    Creates a draft email file in the /Drafts directory.
    Use this tool when the user's request is to send an email.
    The draft will be named EMAIL_[recipient].md.
    """
    draft_content = f"TO: {recipient}\nSUBJECT: {subject}\nBODY:\n{body}"
    draft_filename = f"EMAIL_{recipient.split('@')[0]}.md"
    draft_filepath = os.path.join(DRAFTS_PATH, draft_filename)
    with open(draft_filepath, 'w', encoding='utf-8') as f:
        f.write(draft_content)
    
    plan_content = f"Created draft for task '{task_filename}'.\n"
    plan_content += f"Draft file: {draft_filepath}\n"
    plan_content += f"Content:\n{draft_content}"
    
    return f"Email draft for {recipient} created at {draft_filepath}. Please ask the user to review and move it to the Outbox."

@function_tool
def create_whatsapp_draft(
    phone_number: Annotated[str, "The recipient's phone number, including the country code (e.g., +11234567890)."],
    message: Annotated[str, "The content of the WhatsApp message."],
    task_filename: Annotated[str, "The original filename of the task in the Inbox."]
):
    """
    Creates a draft WhatsApp message file in the /Drafts directory.
    Use this tool when the user's request is to send a WhatsApp message.
    The draft will be named WHATSAPP_[phone_number].md.
    """
    draft_content = f"PHONE: {phone_number}\nMESSAGE: {message}"
    # Sanitize phone number for filename
    safe_phone_number = "".join(filter(str.isalnum, phone_number))
    draft_filename = f"WHATSAPP_{safe_phone_number}.md"
    draft_filepath = os.path.join(DRAFTS_PATH, draft_filename)
    with open(draft_filepath, 'w', encoding='utf-8') as f:
        f.write(draft_content)
        
    plan_content = f"Created draft for task '{task_filename}'.\n"
    plan_content += f"Draft file: {draft_filepath}\n"
    plan_content += f"Content:\n{draft_content}"

    return f"WhatsApp draft for {phone_number} created at {draft_filepath}. Please ask the user to review and move it to the Outbox."

@function_tool
def create_linkedin_draft(
    content: Annotated[str, "The content of the LinkedIn post."],
    topic: Annotated[str, "A short, file-safe topic for the post, used for the filename."],
    task_filename: Annotated[str, "The original filename of the task in the Inbox."]
):
    """
    Creates a draft LinkedIn post file in the /Drafts directory.
    Use this tool when the user's request is to post on LinkedIn.
    The draft will be named LINKEDIN_[topic].md.
    """
    draft_content = f"CONTENT: {content}"
    draft_filename = f"LINKEDIN_{topic}.md"
    draft_filepath = os.path.join(DRAFTS_PATH, draft_filename)
    with open(draft_filepath, 'w', encoding='utf-8') as f:
        f.write(draft_content)

    plan_content = f"Created draft for task '{task_filename}'.\\n"
    plan_content += f"Draft file: {draft_filepath}\\n"
    plan_content += f"Content:\\n{draft_content}"

    return f"LinkedIn draft about '{topic}' created at {draft_filepath}. Please ask the user to review and move it to the Outbox."

# --- LLM Prompt ---
SYSTEM_PROMPT = """
You are "Silver Tier FTE", a digital AI employee. Your purpose is to process tasks from the `/Inbox` folder and prepare drafts for human approval. You NEVER execute actions directly.

**Your Workflow:**
1.  **Analyze the Task:** A user provides a task in a markdown file. You will be given its content.
2.  **Consult Your Memory:** You have been provided with Standard Operating Procedures (SOPs) from the `/Memory` folder. You must follow these rules. The most important rule is that you ONLY create drafts. You DO NOT have tools to send emails, post to social media, or send messages directly.
3.  **Select a Tool:** Based on the task, you must choose one of your available tools: `create_email_draft`, `create_whatsapp_draft`, or `create_linkedin_draft`.
4.  **Execute Tool:** Call the chosen tool with all the required parameters extracted from the user's task.
5.  **Confirm:** Your final output will be the confirmation message from the tool you used. You will then wait for the next task.
"""

# --- Agent Definition ---
def get_memory_context():
    """Reads all files in the Memory folder to provide context to the LLM."""
    context = ""
    for filename in os.listdir(MEMORY_PATH):
        filepath = os.path.join(MEMORY_PATH, filename)
        if os.path.isfile(filepath):
            with open(filepath, 'r', encoding='utf-8') as f:
                context += f"--- Content from {filename} ---\\n{f.read()}\\n"
    return context

class FTEAgent:
    def __init__(self):
        self.agent = Agent(
            name="Silver Tier FTE",
            instructions=SYSTEM_PROMPT,
            tools=[create_email_draft, create_whatsapp_draft, create_linkedin_draft],
        )

    async def process_task(self, task_path):
        """Processes a single task file from the Inbox using the openai-agents SDK."""
        print(f"Processing new task: {task_path}")
        task_filename = os.path.basename(task_path)
        try:
            with open(task_path, 'r', encoding='utf-8') as f:
                task_content = f.read()

            memory_context = get_memory_context()

            prompt = f"""
            {memory_context}
            --- User Task from '{task_filename}' ---
            {task_content}

            You must pass the original task filename '{task_filename}' to the 'task_filename' parameter of whichever tool you call.
            """

            # Let the agent handle the prompt
            result = await Runner.run(self.agent, prompt)
            
            final_output = result.final_output if result.final_output else "No output from agent."
            
            print(f"Agent execution finished for task: {task_filename}")
            print(f"Agent response: {final_output}")

            # Create a plan file from the agent's thoughts and tool calls
            plan_filename = f"PLAN_{task_filename}.log"
            plan_filepath = os.path.join(PLANS_PATH, plan_filename)
            with open(plan_filepath, 'w', encoding='utf-8') as f:
                # Log the full conversation trace for debugging and planning records
                f.write("--- Conversation Trace ---\n")
                for item in result.to_input_list():
                    f.write(json.dumps(item, indent=2) + "\n")
                f.write("\n--- Final Output ---\n")
                f.write(str(final_output))

            # Move the original task to the Sent folder to mark it as processed
            sent_filepath = os.path.join(SENT_PATH, task_filename)
            os.rename(task_path, sent_filepath)

            print(f">>> Task '{task_filename}' processed, draft created, and task moved to Sent.")
            print(f"Plan and agent thoughts logged to: {plan_filepath}")
            print(final_output) # Display the final confirmation to the user

        except Exception as e:
            print(f"Error processing task {task_path}: {e}")
            error_folder = os.path.join(INBOX_PATH, "Errors")
            if not os.path.exists(error_folder):
                os.makedirs(error_folder)
            try:
                os.rename(task_path, os.path.join(error_folder, task_filename))
            except FileExistsError:
                os.remove(os.path.join(error_folder, task_filename))
                os.rename(task_path, os.path.join(error_folder, task_filename))

# --- File System Watcher ---
class InboxWatcher(FileSystemEventHandler):
    def __init__(self, agent, loop):
        self.agent = agent
        self.loop = loop
        self.processing = set()

    def on_created(self, event):
        if not event.is_directory and event.src_path not in self.processing and "ERROR_" not in event.src_path:
            self.processing.add(event.src_path)
            print(f"File creation detected: {event.src_path}")
            # Wait a moment to ensure file write is complete
            time.sleep(1)
            try:
                # Schedule the async task to run in the event loop
                asyncio.run_coroutine_threadsafe(self.agent.process_task(event.src_path), self.loop)
            finally:
                # The task is running, but we can allow the watcher to pick up new files.
                # The `processing` set prevents re-processing the same file.
                # We will remove it after the async task is truly done if needed, but for now this is ok.
                # In a more robust system, a callback would handle this.
                pass

def ensure_folders_exist():
    for folder in [INBOX_PATH, PLANS_PATH, DRAFTS_PATH, MEMORY_PATH, SENT_PATH, OUTBOX_PATH]:
        if not os.path.exists(folder):
            print(f"Creating folder: {folder}")
            os.makedirs(folder)

async def amain(agent):
    """The main async function to run the agent and file watcher."""
    loop = asyncio.get_running_loop()
    
    observer = Observer()
    observer.schedule(InboxWatcher(agent, loop), INBOX_PATH, recursive=False)
    observer.start()
    
    print(f"Agent started. Watching for new tasks in '{INBOX_PATH}'...")
    print("Press Ctrl+C to stop.")
    
    try:
        # Keep the main coroutine alive to process tasks
        while True:
            await asyncio.sleep(1)
    finally:
        print("Stopping observer...")
        observer.stop()
        observer.join()
        print("Observer stopped.")

def main():
    """Sets up the environment and runs the async main function."""
    print("Initializing Silver Tier FTE Agent...")
    ensure_folders_exist()

    if not os.getenv("OPENAI_API_KEY"):
        print("\\n--- IMPORTANT ---\\nOPENAI_API_KEY environment variable not found.\\nPlease create a .env file and add: OPENAI_API_KEY='your_key'\\n")
        return

    agent = FTEAgent()
    
    try:
        asyncio.run(amain(agent))
    except KeyboardInterrupt:
        print("\nAgent stopped by user.")


if __name__ == "__main__":
    main()
