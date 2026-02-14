import os
import time
import re
import shutil
import subprocess
import sys
from datetime import datetime
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Add the 'tools' directory to sys.path to allow direct imports
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
TOOLS_DIR = os.path.join(PROJECT_ROOT, 'tools')
sys.path.insert(0, TOOLS_DIR)

try:
    from gmail_sender import send_email
    from whatsapp_sender import send_whatsapp
    from linkedin_poster import post_to_linkedin
except ImportError as e:
    print(f"Error importing sender modules: {e}. Make sure they are in the 'tools' directory and dependencies are installed.", file=sys.stderr)
    sys.exit(1)


OUTBOX_DIR = os.path.join(PROJECT_ROOT, 'Outbox')
INBOX_DIR = os.path.join(PROJECT_ROOT, 'Inbox')
SENT_DIR = os.path.join(PROJECT_ROOT, 'Sent')
MEMORY_DIR = os.path.join(PROJECT_ROOT, 'Memory')
DASHBOARD_PATH = os.path.join(MEMORY_DIR, 'Dashboard.md')


def log_to_dashboard(entry):
    """Appends a log entry to the Dashboard.md file."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(DASHBOARD_PATH, 'a') as f:
        f.write(f"- [{timestamp}] {entry}\n")
    print(f"Logged to Dashboard: {entry}")

def parse_markdown_file(filepath):
    """Parses a markdown file for key-value pairs."""
    content = {}
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    current_key = None
    buffer = []

    for line in lines:
        line = line.strip()
        if not line:
            continue

        match = re.match(r"^(TO|SUBJECT|BODY|PHONE|MESSAGE|CONTENT):\s*(.*)", line, re.IGNORECASE)
        if match:
            # If we were buffering content for a previous key, save it
            if current_key and buffer:
                content[current_key] = "\n".join(buffer).strip()
                buffer = []

            key = match.group(1).upper()
            value = match.group(2).strip()
            content[key] = value # Initial value
            current_key = key
        elif current_key:
            # Continue buffering for the current key
            buffer.append(line)
        else:
            # If no key is set yet, assume it's part of a generic 'CONTENT'
            buffer.append(line)

    # Save any remaining buffered content
    if current_key and buffer:
        content[current_key] = "\n".join(buffer).strip()
    elif buffer and 'CONTENT' not in content: # If there's unkeyed content
        content['CONTENT'] = "\n".join(buffer).strip()
    elif buffer and 'CONTENT' in content: # Append if content key already exists
        content['CONTENT'] += "\n" + "\n".join(buffer).strip()


    return content

def process_file(filepath):
    """Processes a file from the Outbox based on its prefix."""
    filename = os.path.basename(filepath)
    print(f"Processing file: {filename}")

    try:
        if filename.startswith('EMAIL_') and filename.endswith('.md'):
            data = parse_markdown_file(filepath)
            to_email = data.get('TO')
            subject = data.get('SUBJECT')
            body = data.get('BODY')

            if not all([to_email, subject, body]):
                raise ValueError(f"Missing required fields for email in {filename}: To, Subject, Body")

            send_email(to_email, subject, body)
            log_entry = f"Sent email '{subject}' to {to_email} from {filename}"

        elif filename.startswith('WHATSAPP_') and filename.endswith('.md'):
            data = parse_markdown_file(filepath)
            phone_no = data.get('PHONE')
            message = data.get('MESSAGE')

            if not all([phone_no, message]):
                raise ValueError(f"Missing required fields for WhatsApp in {filename}: Phone, Message")

            send_whatsapp(phone_no, message)
            log_entry = f"Sent WhatsApp message to {phone_no} from {filename}"

        elif filename.startswith('LINKEDIN_') and filename.endswith('.md'):
            data = parse_markdown_file(filepath)
            content = data.get('CONTENT')

            if not content:
                raise ValueError(f"Missing content for LinkedIn post in {filename}")

            post_to_linkedin(content)
            log_entry = f"Posted to LinkedIn from {filename}"

        else:
            raise ValueError(f"Unknown file type or format: {filename}")

        # If successful, move to Sent and log
        shutil.move(filepath, os.path.join(SENT_DIR, filename))
        log_to_dashboard(log_entry)
        print(f"Successfully processed {filename}. Moved to {SENT_DIR}")

    except Exception as e:
        error_message = f"Error processing {filename}: {e}"
        print(error_message)
        # On error, move back to Inbox and append error note
        error_filename = f"ERROR_{datetime.now().strftime('%Y%m%d%H%M%S')}_{filename}"
        new_inbox_path = os.path.join(INBOX_DIR, error_filename)
        shutil.move(filepath, new_inbox_path)
        with open(new_inbox_path, 'a') as f:
            f.write(f"\n\n--- ERROR ---\n{error_message}\n")
        log_to_dashboard(f"Failed to process {filename}. Moved to Inbox as {error_filename}. Error: {e}")
        print(f"Failed to process {filename}. Moved to {INBOX_DIR} as {error_filename}")


class OutboxEventHandler(FileSystemEventHandler):
    """Handles file system events in the Outbox directory."""
    def on_created(self, event):
        if not event.is_directory and event.src_path.endswith('.md'):
            print(f"New file detected in Outbox: {event.src_path}")
            # Give a small delay to ensure the file is fully written
            time.sleep(1)
            process_file(event.src_path)

def start_orchestrator():
    """Starts the file system observer for the Outbox."""
    print(f"Starting Orchestrator. Watching for files in: {OUTBOX_DIR}")
    if not os.path.exists(OUTBOX_DIR):
        os.makedirs(OUTBOX_DIR) # Ensure Outbox exists

    # Ensure other necessary directories exist
    os.makedirs(INBOX_DIR, exist_ok=True)
    os.makedirs(SENT_DIR, exist_ok=True)
    os.makedirs(MEMORY_DIR, exist_ok=True)

    event_handler = OutboxEventHandler()
    observer = Observer()
    observer.schedule(event_handler, OUTBOX_DIR, recursive=False)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
    print("Orchestrator stopped.")

if __name__ == "__main__":
    start_orchestrator()
