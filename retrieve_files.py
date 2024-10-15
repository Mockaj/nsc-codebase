# retrieve_files.py
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session as SessionType
from models import File
import sys
from typing import List, Dict

# Load environment variables
load_dotenv()

# Get database URL from environment variables
DATABASE_URL: str = os.getenv('DATABASE_URL') or ""

if not DATABASE_URL:
    print("Please set the DATABASE_URL environment variable in your .env file.")
    sys.exit(1)

# Create the database engine
engine = create_engine(DATABASE_URL)

# Create a configured "Session" class
SessionLocal = sessionmaker(bind=engine)

def get_file_contents(relative_paths: List[str]) -> Dict[str, str]:
    """
    Retrieves the file contents for the given list of relative file paths.

    Args:
        relative_paths (List[str]): A list of relative file paths.

    Returns:
        Dict[str, str]: A dictionary mapping filenames to their contents.
    """
    # Create a new database session
    session: SessionType = SessionLocal()

    try:
        # Query the database for files with filenames in the provided list
        files = session.query(File).filter(File.filename.in_(relative_paths)).all()

        # Create a dictionary mapping filename to file_content
        file_contents: Dict[str, str] = {file.filename: file.file_content for file in files}

        # Identify files that were not found
        not_found_files: set = set(relative_paths) - set(file_contents.keys())
        if not_found_files:
            print(f"The following files were not found in the database: {not_found_files}")

        return file_contents
    finally:
        # Close the session
        session.close()

def main() -> None:
    """
    Example usage of the get_file_contents function.
    """
    # Example list of relative file paths
    relative_paths: List[str] = [
        'src/main.py',
        'src/utils/helpers.py',
        'nonexistent_file.py'  # This file does not exist in the database
    ]

    file_contents: Dict[str, str] = get_file_contents(relative_paths)

    for filename, content in file_contents.items():
        print(f"Filename: {filename}")
        print("Content:")
        print(content)
        print("-" * 40)

if __name__ == '__main__':
    main()