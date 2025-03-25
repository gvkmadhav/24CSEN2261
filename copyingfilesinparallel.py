#Chat gpt
import os
import shutil
import threading
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

class FileCopyError(Exception):
    """Custom exception for file copy errors."""
    pass

class FileCopier:
    def __init__(self, source_dir, destination_dir, max_threads=4):
        self.source_dir = Path(source_dir)
        self.destination_dir = Path(destination_dir)
        self.max_threads = max_threads
        self.files_to_copy = []

    def validate_directories(self):
        """Validate if source and destination directories exist."""
        if not self.source_dir.exists() or not self.source_dir.is_dir():
            raise FileCopyError(f"Source directory {self.source_dir} does not exist or is not a directory.")
        if not self.destination_dir.exists():
            os.makedirs(self.destination_dir)
            logging.info(f"Created destination directory: {self.destination_dir}")
    
    def get_files_to_copy(self):
        """Get all files in the source directory to copy."""
        self.files_to_copy = [file for file in self.source_dir.iterdir() if file.is_file()]
        logging.info(f"Found {len(self.files_to_copy)} files to copy.")
    
    def copy_file(self, file_path):
        """Copy a single file to the destination directory."""
        try:
            dest_path = self.destination_dir / file_path.name
            shutil.copy(file_path, dest_path)
            logging.info(f"Successfully copied {file_path.name} to {self.destination_dir}")
        except Exception as e:
            logging.error(f"Failed to copy {file_path.name}: {e}")
            raise FileCopyError(f"Error copying {file_path.name}: {e}")

    def copy_files_concurrently(self):
        """Copy files concurrently using threading."""
        threads = []
        for file in self.files_to_copy:
            thread = threading.Thread(target=self.copy_file, args=(file,))
            threads.append(thread)
            thread.start()

        # Wait for all threads to complete
        for thread in threads:
            thread.join()

    def run(self):
        """Run the file copying process."""
        try:
            self.validate_directories()
            self.get_files_to_copy()
            self.copy_files_concurrently()
            logging.info("File copy operation completed successfully.")
        except FileCopyError as e:
            logging.error(f"File copy operation failed: {e}")
        except Exception as e:
            logging.error(f"Unexpected error: {e}")

# Example usage
def main():
    source_directory = 'source_folder'  # Replace with your source directory path
    destination_directory = 'destination_folder'  # Replace with your destination directory path

    copier = FileCopier(source_directory, destination_directory)
    copier.run()

if __name__ == "__main__":
    main()
