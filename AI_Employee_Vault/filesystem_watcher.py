import os
import time
import shutil
from datetime import datetime
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Configuration - Relative to script location
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DROP_ZONE = os.path.join(BASE_DIR, "Drop_Zone")
NEEDS_ACTION = os.path.join(BASE_DIR, "Needs_Action")

class WatcherHandler(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory:
            filename = os.path.basename(event.src_path)
            print(f"Detected new file: {filename}")
            
            # Wait a moment to ensure file is fully written
            time.sleep(1)
            
            src_path = event.src_path
            dest_path = os.path.join(NEEDS_ACTION, filename)
            
            try:
                # Move the file
                shutil.move(src_path, dest_path)
                print(f"Moved {filename} to {NEEDS_ACTION}")
                
                # Create metadata MD file
                metadata_filename = f"FILE_{filename}.md"
                metadata_path = os.path.join(NEEDS_ACTION, metadata_filename)
                
                with open(metadata_path, "w", encoding="utf-8") as f:
                    f.write(f"# Metadata for {filename}\n\n")
                    f.write(f"- **Original Name:** {filename}\n")
                    f.write(f"- **Timestamp:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                    f.write(f"- **Status:** pending\n")
                
                print(f"Created metadata file: {metadata_filename}")
                
            except Exception as e:
                print(f"Error processing {filename}: {e}")

def scan_existing_files():
    print(f"Scanning for existing files in {DROP_ZONE}...")
    for filename in os.listdir(DROP_ZONE):
        src_path = os.path.join(DROP_ZONE, filename)
        if os.path.isfile(src_path):
            print(f"Found existing file: {filename}")
            # Manually trigger the move logic
            dest_path = os.path.join(NEEDS_ACTION, filename)
            try:
                shutil.move(src_path, dest_path)
                print(f"Moved {filename} to {NEEDS_ACTION}")
                
                metadata_filename = f"FILE_{filename}.md"
                metadata_path = os.path.join(NEEDS_ACTION, metadata_filename)
                with open(metadata_path, "w", encoding="utf-8") as f:
                    f.write(f"# Metadata for {filename}\n\n")
                    f.write(f"- **Original Name:** {filename}\n")
                    f.write(f"- **Timestamp:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                    f.write(f"- **Status:** pending\n")
            except Exception as e:
                print(f"Error moving existing file {filename}: {e}")

if __name__ == "__main__":
    if not os.path.exists(DROP_ZONE):
        os.makedirs(DROP_ZONE)
    if not os.path.exists(NEEDS_ACTION):
        os.makedirs(NEEDS_ACTION)

    # Scan for files that are already there
    scan_existing_files()

    event_handler = WatcherHandler()
    observer = Observer()
    observer.schedule(event_handler, DROP_ZONE, recursive=False)
    
    print(f"Watching folder: {DROP_ZONE}")
    observer.start()
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
