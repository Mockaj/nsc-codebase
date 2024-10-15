# seed_files.py
import os
import fnmatch
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session as SessionType
from models import Base, File
import sys
from typing import List, Optional

# Load environment variables
load_dotenv()

# Get database URL from environment variables
DATABASE_URL: Optional[str] = os.getenv('DATABASE_URL') or ""

if not DATABASE_URL:
    print("Please set the DATABASE_URL environment variable in your .env file.")
    sys.exit(1)

# Create the database engine
engine = create_engine(DATABASE_URL)

# Create all tables (if they don't exist)
Base.metadata.create_all(engine)

# Create a configured "Session" class
SessionLocal = sessionmaker(bind=engine)


def is_excluded(path: str, exclude_patterns: List[str]) -> bool:
    """
    Determines if a given path should be excluded based on the exclude patterns.

    Args:
        path (str): The file or directory path to check.
        exclude_patterns (List[str]): A list of patterns to exclude.

    Returns:
        bool: True if the path matches any exclude pattern, False otherwise.
    """
    for pattern in exclude_patterns:
        if fnmatch.fnmatch(path, pattern):
            return True
        if fnmatch.fnmatch(os.path.basename(path), pattern):
            return True
    return False

def main() -> None:
    """
    Main function to process files and seed the database.
    """
    # The directory to start from
    root_dir: str = '/path/to/your/codebase'  # Replace with your codebase path

    # List of patterns to exclude
    exclude_patterns: List[str] = [
        '*/node_modules/*',
        '*/.git/*',
        '*/vendor/*',
        '*/storage/*',
        '*.txt',
        '*.json',
        '*.lock',
        '*.log',
        '*.env*',
        '*.neon',
        '*.gz',
        '*.md',
        '*.png',
        '*.jpg',
        '*.jpeg',
        '*.DS_Store*',
        '*/migrations/*',
        '*/seeders/*'
    ]

    # Collect all files to process
    files_to_process: List[str] = []
    for dirpath, dirnames, filenames in os.walk(root_dir):
        dirnames[:] = [d for d in dirnames if not is_excluded(os.path.join(dirpath, d), exclude_patterns)]
        for filename in filenames:
            filepath: str = os.path.join(dirpath, filename)
            if is_excluded(filepath, exclude_patterns):
                continue
            files_to_process.append(filepath)

    total_files: int = len(files_to_process)
    print(f"Total files found: {total_files}")

    # Create a new database session
    session: SessionType = SessionLocal()

    for filepath in files_to_process:
        relative_path: str = os.path.relpath(filepath, root_dir)
        # Check if the file already exists in the database
        existing_file: File = session.query(File).filter_by(filename=relative_path).first()
        if existing_file:
            print(f"File already exists in database: {relative_path}")
            continue  # Skip already processed files
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content: str = f.read()
            # Create a new File object
            new_file: File = File(filename=relative_path, file_content=content)
            session.add(new_file)
            session.commit()
            print(f"Inserted file into database: {relative_path}")
        except Exception as e:
            session.rollback()
            print(f"Error processing {relative_path}: {e}")
            continue

    # Close the session
    session.close()

if __name__ == '__main__':
    main()