import os
import platform
import subprocess

def setup_windows_task():
    print("Setting up Windows Task Scheduler...")
    # Example: Create a task that runs every hour
    # schtasks /create /tn "DigitalFTE_Watcher" /tr "python f:\\ai_dd\\digital_fte\\SilverTier\\Watchers\\gmail_watcher.py" /sc hourly
    script_path = os.path.join(os.getcwd(), "Watchers", "gmail_watcher.py")
    cmd = f'schtasks /create /tn "DigitalFTE_GmailWatcher" /tr "python {script_path}" /sc minute /mo 5 /f'
    try:
        subprocess.run(cmd, shell=True, check=True)
        print("Successfully created Windows Task: DigitalFTE_GmailWatcher (every 5 mins)")
    except Exception as e:
        print(f"Failed to create task: {e}")

def setup_cron():
    print("Setting up Cron job (Linux/macOS)...")
    # Not implemented for Windows, but provided for reference
    pass

if __name__ == "__main__":
    if platform.system() == "Windows":
        setup_windows_task()
    else:
        print("Unsupported OS for auto-setup. Please add to your crontab manually.")
