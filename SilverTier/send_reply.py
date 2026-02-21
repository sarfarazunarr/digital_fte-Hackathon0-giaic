import os
import yagmail
from dotenv import load_dotenv

# Configuration
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(BASE_DIR, ".env"))

GMAIL_USER = os.getenv("GMAIL_USER")
GMAIL_APP_PASSWORD = os.getenv("GMAIL_APP_PASSWORD")

def send_reply(to, subject, body):
    if not GMAIL_USER or not GMAIL_APP_PASSWORD:
        print("Error: GMAIL_USER or GMAIL_APP_PASSWORD not set in .env")
        return False
    
    try:
        yag = yagmail.SMTP(GMAIL_USER, GMAIL_APP_PASSWORD)
        yag.send(to=to, subject=subject, contents=body)
        print(f"Email successfully sent to {to}")
        return True
    except Exception as e:
        print(f"Failed to send email: {str(e)}")
        return False

if __name__ == "__main__":
    reply_file = os.path.join(BASE_DIR, "Outbox", "EMAIL_REPLY_20260221_131744.md")
    if os.path.exists(reply_file):
        with open(reply_file, "r", encoding="utf-8") as f:
            lines = f.readlines()
            to = lines[0].replace("To: ", "").strip()
            subject = lines[1].replace("Subject: ", "").strip()
            body = "".join(lines[3:])
            
            if send_reply(to, subject, body):
                sent_dir = os.path.join(BASE_DIR, "Sent")
                if not os.path.exists(sent_dir):
                    os.makedirs(sent_dir)
                os.rename(reply_file, os.path.join(sent_dir, "EMAIL_REPLY_20260221_131744.md"))
    else:
        print("Reply file not found in Outbox.")
