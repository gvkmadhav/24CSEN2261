#Chatgpt
import time
import logging
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

class FileSystemMonitor(FileSystemEventHandler):
    def on_created(self, event):
        logging.info(f"File created: {event.src_path}")
    
    def on_deleted(self, event):
        logging.info(f"File deleted: {event.src_path}")
    
    def on_modified(self, event):
        logging.info(f"File modified: {event.src_path}")
    
    def on_moved(self, event):
        logging.info(f"File moved: {event.src_path} -> {event.dest_path}")

def run_file_monitor(directory_to_watch):
    """Monitor the given directory for file changes."""
    event_handler = FileSystemMonitor()
    observer = Observer()
    observer.schedule(event_handler, path=directory_to_watch, recursive=True)
    
    logging.info(f"Monitoring directory: {directory_to_watch} for changes...")
    observer.start()
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        logging.info("Stopping directory monitor...")
    observer.join()

# Example usage
def main():
    directory_to_watch = './watched_directory'  # Replace with your directory path
    run_file_monitor(directory_to_watch)

if __name__ == "__main__":
    main()
