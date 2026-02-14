import os
import time
import shutil
from datetime import datetime
from dotenv import load_dotenv
from openai import OpenAI

# Configuration - Relative to script location
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(BASE_DIR, ".env"))

# Check for API Key
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    print("Warning: OPENAI_API_KEY not found in .env file. Falling back to simple summarization.")
    client = None
else:
    client = OpenAI(api_key=api_key)

NEEDS_ACTION = os.path.join(BASE_DIR, "Needs_Action")
DONE = os.path.join(BASE_DIR, "Done")
PLANS = os.path.join(BASE_DIR, "Plans")
DASHBOARD = os.path.join(BASE_DIR, "Dashboard.md")
PHR = os.path.join(BASE_DIR, "PHR")

def get_ai_summary(content):
    if not client:
        return content[:200] + ("..." if len(content) > 200 else "")
    
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful AI employee. Summarize the following document content concisely."},
                {"role": "user", "content": content}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"AI Summarization failed: {e}")
        return content[:200] + ("..." if len(content) > 200 else "")

def process_tasks():
    if not os.path.exists(NEEDS_ACTION):
        return False

    files = [f for f in os.listdir(NEEDS_ACTION) if not f.startswith("FILE_") and os.path.isfile(os.path.join(NEEDS_ACTION, f))]
    
    if not files:
        return False

    for filename in files:
        print(f"Processing: {filename}")
        src_path = os.path.join(NEEDS_ACTION, filename)
        
        # 1. Read content
        try:
            with open(src_path, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
        except Exception as e:
            content = f"Could not read content: {e}"

        # 2. Generate Plan
        plan_filename = f"PLAN_{filename}.md"
        plan_path = os.path.join(PLANS, plan_filename)
        with open(plan_path, "w", encoding="utf-8") as f:
            f.write(f"# Plan for {filename}\n\n")
            f.write(f"Task: AI Summarization of {filename}\n")
            f.write(f"Execution: Use OpenAI to summarize and append to Dashboard.md.\n")
        
        # 3. Execute (Summarize into Dashboard)
        summary = get_ai_summary(content)
        with open(DASHBOARD, "a", encoding="utf-8") as f:
            f.write(f"\n### {filename} (Processed at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')})\n")
            f.write(f"**Summary:** {summary}\n")
            f.write(f"**Original Location:** {src_path}\n")

        # 4. Record prompt in PHR
        record_filename = f"RECORD_{datetime.now().strftime('%Y%H%M%S')}_{filename}.md"
        record_path = os.path.join(PHR, record_filename)
        with open(record_path, "w", encoding="utf-8") as f:
            f.write(f"# Prompt Record\n")
            f.write(f"- **File:** {filename}\n")
            f.write(f"- **Timestamp:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"- **Action:** AI Summarization\n")

        # 5. Move to Done
        dest_path = os.path.join(DONE, filename)
        shutil.move(src_path, dest_path)
        
        # Also move the metadata file if it exists
        meta_file = f"FILE_{filename}.md"
        meta_src = os.path.join(NEEDS_ACTION, meta_file)
        if os.path.exists(meta_src):
            shutil.move(meta_src, os.path.join(DONE, meta_file))

        print(f"Successfully processed {filename}")

    return True

if __name__ == "__main__":
    for folder in [NEEDS_ACTION, DONE, PLANS, PHR]:
        if not os.path.exists(folder):
            os.makedirs(folder)

    print("Agent Loop (Ralph Wiggum Mode) started. Monitoring Needs_Action...")
    print(f"Directory: {NEEDS_ACTION}")
    
    try:
        while True:
            processed = process_tasks()
            if not processed:
                # Polling interval with minor heartbeat
                time.sleep(5)
                # print(".", end="", flush=True) # Optional heartbeat
            else:
                print("Tasks processed, checking for more...")
    except KeyboardInterrupt:
        print("\nAgent Loop stopped.")
