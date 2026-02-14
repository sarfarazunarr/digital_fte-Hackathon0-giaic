import smtplib
import os
import sys
from dotenv import load_dotenv

# Load environment variables relative to the project root when imported, or current dir when run directly
load_dotenv(dotenv_path=os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '.env'))

def send_email(to_email, subject, body):
    gmail_user = os.getenv('GMAIL_USER')
    gmail_app_password = os.getenv('GMAIL_APP_PASSWORD')

    if not gmail_user or not gmail_app_password:
        raise ValueError("GMAIL_USER and GMAIL_APP_PASSWORD must be set in the .env file")

    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        server.login(gmail_user, gmail_app_password)
        message = f"Subject: {subject}\n\n{body}"
        server.sendmail(gmail_user, to_email, message)
        server.close()
        print(f"Email sent successfully to {to_email}") # This will go to stdout for subprocess to capture
    except Exception as e:
        print(f"Error sending email: {e}", file=sys.stderr) # Send errors to stderr
        raise

if __name__ == '__main__':
    # When run as a script, expect arguments
    if len(sys.argv) == 4:
        to_email = sys.argv[1]
        subject = sys.argv[2]
        body = sys.argv[3]
        try:
            send_email(to_email, subject, body)
        except Exception as e:
            sys.exit(1) # Exit with error code
    else:
        print("Usage: python gmail_sender.py <to_email> <subject> <body>", file=sys.stderr)
        sys.exit(1)
