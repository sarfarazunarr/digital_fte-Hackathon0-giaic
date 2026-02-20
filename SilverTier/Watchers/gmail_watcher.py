import os
import time
import imaplib
import email
import logging
from datetime import datetime
from dotenv import load_dotenv

# Configuration
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load_dotenv(os.path.join(BASE_DIR, ".env"))

GMAIL_USER = os.getenv("GMAIL_USER")
GMAIL_APP_PASSWORD = os.getenv("GMAIL_APP_PASSWORD")
INBOX_DIR = os.path.join(BASE_DIR, "Inbox")
LOG_DIR = os.path.join(BASE_DIR, "Logs")

if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(os.path.join(LOG_DIR, "watchers.log")),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("GmailWatcher")

def check_gmail():
    if not GMAIL_USER or not GMAIL_APP_PASSWORD:
        logger.error("GMAIL_USER or GMAIL_APP_PASSWORD not set.")
        return

    try:
        mail = imaplib.IMAP4_SSL("imap.gmail.com")
        mail.login(GMAIL_USER, GMAIL_APP_PASSWORD)
        mail.select("inbox")

        result, data = mail.search(None, "UNSEEN")
        if result != "OK":
            logger.error("Could not search for unseen emails.")
            return

        for num in data[0].split():
            result, data = mail.fetch(num, "(RFC822)")
            if result != "OK":
                continue

            raw_email = data[0][1]
            msg = email.message_from_bytes(raw_email)
            
            subject = msg["Subject"]
            sender = msg["From"]
            date = msg["Date"]
            
            body = ""
            if msg.is_multipart():
                for part in msg.walk():
                    if part.get_content_type() == "text/plain":
                        body = part.get_payload(decode=True).decode()
                        break
            else:
                body = msg.get_payload(decode=True).decode()

            filename = f"EMAIL_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
            filepath = os.path.join(INBOX_DIR, filename)
            
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(f"# New Email from {sender}\n\n")
                f.write(f"- **Subject:** {subject}\n")
                f.write(f"- **Date:** {date}\n\n")
                f.write(f"## Content\n\n{body}\n")
            
            logger.info(f"Saved new email to Inbox: {filename}")

        mail.logout()
    except Exception as e:
        logger.error(f"Gmail check failed: {e}")

if __name__ == "__main__":
    if not os.path.exists(INBOX_DIR):
        os.makedirs(INBOX_DIR)
    
    logger.info("Gmail Watcher started. Polling every 60 seconds...")
    while True:
        check_gmail()
        time.sleep(60)
