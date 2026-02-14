import pywhatkit
import re
import sys
import os
import time
from dotenv import load_dotenv

# Load environment variables relative to the project root when imported, or current dir when run directly
load_dotenv(dotenv_path=os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '.env'))

def send_whatsapp(phone_no, message):
    # Verify phone number includes country code (simple check)
    if not re.match(r"^\+\d{1,3}\d{10,}$", phone_no):
        raise ValueError("Phone number must include country code (e.g., +11234567890)")

    try:
        print(f"Sending WhatsApp message to {phone_no} in 15 seconds...", file=sys.stderr) # To stderr
        # pywhatkit.sendwhatmsg_instantly(phone_no, message, wait_time=15, tab_close=True)
        # Using sendwhatmsg for testing purposes as sendwhatmsg_instantly might not work headless
        pywhatkit.sendwhatmsg(phone_no, message, time.localtime().tm_hour, time.localtime().tm_min + 1, wait_time=15, tab_close=True)
        print(f"WhatsApp message sent successfully to {phone_no}") # To stdout
    except Exception as e:
        print(f"Error sending WhatsApp message: {e}", file=sys.stderr) # To stderr
        raise

if __name__ == '__main__':
    # When run as a script, expect arguments
    if len(sys.argv) >= 3: # phone_no, message (can be multiple words)
        phone_no = sys.argv[1]
        message = " ".join(sys.argv[2:])
        try:
            send_whatsapp(phone_no, message)
        except Exception as e:
            sys.exit(1) # Exit with error code
    else:
        print("Usage: python whatsapp_sender.py <phone_no_with_country_code> <message>", file=sys.stderr)
        sys.exit(1)
