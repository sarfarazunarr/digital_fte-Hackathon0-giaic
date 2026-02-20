import os
import time
import shutil
import logging
from datetime import datetime
from dotenv import load_dotenv
from openai import OpenAI

# Configuration
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(BASE_DIR, ".env"))

INBOX = os.path.join(BASE_DIR, "Inbox")
DRAFTS = os.path.join(BASE_DIR, "Drafts")
PLANS = os.path.join(BASE_DIR, "Plans")
LOG_DIR = os.path.join(BASE_DIR, "Logs")

# Logging Configuration
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(os.path.join(LOG_DIR, "agent.log")),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("DigitalFTE")

# API Client
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key) if api_key else None

def get_claude_style_reasoning(content):
    if not client:
        return "Reasoning loop skipped (No API Key).", "ACTION: Request Manual Review."
    
    try:
        response = client.chat.completions.create(
            model="gpt-4", # Simulate high reasoning or use 3.5 for cost
            messages=[
                {"role": "system", "content": """You are a High-Level Assistant. 
                Follow this reasoning pattern:
                1. ANALYZE: What is requested?
                2. STRATEGIZE: How to fulfill this?
                3. PROPOSE: What specific draft should be created? (EMAIL, LINKEDIN, or WHATSAPP)
                Return the reasoning in Markdown plan format and the proposed ACTION separately."""},
                {"role": "user", "content": content}
            ]
        )
        return response.choices[0].message.content, "ACTION: Draft CREATED"
    except Exception as e:
        return f"Reasoning failed: {e}", "ACTION: Manual check required."

def process_inbox():
    if not os.path.exists(INBOX):
        return

    files = [f for f in os.listdir(INBOX) if os.path.isfile(os.path.join(INBOX, f))]
    for filename in files:
        logger.info(f"New incoming task: {filename}")
        src_path = os.path.join(INBOX, filename)
        
        with open(src_path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
        
        # 1. Claude Reasoning Loop
        reasoning, action = get_claude_style_reasoning(content)
        
        # 2. Create Plan.md
        plan_filename = f"PLAN_{filename}.md"
        with open(os.path.join(PLANS, plan_filename), "w", encoding="utf-8") as f:
            f.write(f"# Reasoning Plan for {filename}\n\n")
            f.write(reasoning)
        
        # 3. Create Draft based on content
        draft_filename = f"DRAFT_{filename}.md"
        if "EMAIL" in content.upper() or "MAIL" in content.upper():
            draft_filename = f"EMAIL_{filename}.md"
        elif "LINKEDIN" in content.upper():
            draft_filename = f"LINKEDIN_{filename}.md"
        
        with open(os.path.join(DRAFTS, draft_filename), "w", encoding="utf-8") as f:
            f.write(content) # Or structured draft
            
        logger.info(f"Reasoning complete for {filename}. Draft created at {draft_filename}. Awaiting user approval.")
        
        # Move processed inbox file to avoid re-processing or archive
        # shutil.move(src_path, os.path.join(BASE_DIR, "Archive", filename)) 
        # For now, we delete or rename
        os.rename(src_path, src_path + ".processed")

if __name__ == "__main__":
    for folder in [INBOX, DRAFTS, PLANS]:
        if not os.path.exists(folder):
            os.makedirs(folder)

    logger.info("Silver Tier Agent Loop started. Monitoring Inbox...")
    while True:
        process_inbox()
        time.sleep(10)
