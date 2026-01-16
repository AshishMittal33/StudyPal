import os
import re
from dotenv import load_dotenv

load_dotenv()

working_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(working_dir)

CLASS_BASE_PATH = os.getenv("CLASS_BASE_PATH", "class12")

def get_chapter_list(selected_subject):
    """
    Returns chapter list for any subject using .env configuration
    """

    subject_name = selected_subject.lower()
    chapters_dir = os.path.join(
        parent_dir,
        "data",
        CLASS_BASE_PATH,
        subject_name
    )

    if not os.path.exists(chapters_dir):
        return []

    chapters = [
        f.replace(".pdf", "")
        for f in os.listdir(chapters_dir)
        if f.lower().endswith(".pdf")
    ]

    def extract_chapter_number(name):
        match = re.search(r"\d+", name)
        return int(match.group()) if match else 9999

    chapters.sort(key=extract_chapter_number)
    return chapters
