import os
import sys

# Ensure current directory is in path
sys.path.append(os.getcwd())

from Watchers.gmail_watcher import check_gmail

print("Checking Gmail...")
check_gmail()
print("Done checking Gmail.")
