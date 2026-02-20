import os
import yagmail
from dotenv import load_dotenv
from fastmcp import FastMCP

# Configuration
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load_dotenv(os.path.join(BASE_DIR, ".env"))

GMAIL_USER = os.getenv("GMAIL_USER")
GMAIL_APP_PASSWORD = os.getenv("GMAIL_APP_PASSWORD")

mcp = FastMCP("Email Service")

@mcp.tool()
def send_email(to: str, subject: str, body: str) -> str:
    \"\"\"
    Sends an email using Gmail SMTP.
    Requires GMAIL_USER and GMAIL_APP_PASSWORD in .env.
    \"\"\"
    if not GMAIL_USER or not GMAIL_APP_PASSWORD:
        return "Error: GMAIL_USER or GMAIL_APP_PASSWORD not set in .env"
    
    try:
        yag = yagmail.SMTP(GMAIL_USER, GMAIL_APP_PASSWORD)
        yag.send(to=to, subject=subject, contents=body)
        return f"Email successfully sent to {to}"
    except Exception as e:
        return f"Failed to send email: {str(e)}"

if __name__ == "__main__":
    mcp.run()
