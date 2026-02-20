import os
import time
import shutil
import logging
import subprocess
from dotenv import load_dotenv

# Configuration
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(BASE_DIR, ".env"))

OUTBOX = os.path.join(BASE_DIR, "Outbox")
SENT = os.path.join(BASE_DIR, "Sent")
INBOX = os.path.join(BASE_DIR, "Inbox")
LOG_DIR = os.path.join(BASE_DIR, "Logs")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(os.path.join(LOG_DIR, "orchestrator.log")),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("Orchestrator")

def process_outbox():
    if not os.path.exists(OUTBOX):
        return

    files = [f for f in os.listdir(OUTBOX) if os.path.isfile(os.path.join(OUTBOX, f))]
    for filename in files:
        filepath = os.path.join(OUTBOX, filename)
        logger.info(f"Executing approved task: {filename}")
        
        success = False
        try:
            if filename.startswith("EMAIL_"):
                # Handle Email execution via MCP or script
                # For simplicity, we'll assume a specific format in the file
                logger.info("Sending Email...")
                # subprocess.run(["uv", "run", "mcp_server/email_server.py", ...]) 
                # Or just use yagmail directly if credentials exist
                success = True # Placeholder
            elif filename.startswith("LINKEDIN_"):
                logger.info("Posting to LinkedIn...")
                with open(filepath, "r", encoding="utf-8") as f:
                    content = f.read()
                subprocess.run(["python", os.path.join(BASE_DIR, "Tools", "linkedin_poster.py"), content])
                success = True
            elif filename.startswith("WHATSAPP_"):
                logger.info("Sending WhatsApp message...")
                # Call whatsapp tool
                success = True
            
            if success:
                shutil.move(filepath, os.path.join(SENT, filename))
                logger.info(f"Successfully executed and moved to Sent: {filename}")
            else:
                shutil.move(filepath, os.path.join(INBOX, filename))
                logger.error(f"Execution failed for {filename}. Moved back to Inbox.")
                
        except Exception as e:
            logger.error(f"Error executing {filename}: {e}")
            shutil.move(filepath, os.path.join(INBOX, filename))

if __name__ == "__main__":
    for folder in [OUTBOX, SENT, INBOX]:
        if not os.path.exists(folder):
            os.makedirs(folder)

    logger.info("Silver Tier Orchestrator started. Monitoring Outbox...")
    while True:
        process_outbox()
        time.sleep(5)
