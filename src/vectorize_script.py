import os
from dotenv import load_dotenv
from vectorize_book import vectorize_book_and_store_to_db, vectorize_chapters

load_dotenv()

BASE_CLASS_PATH = os.getenv("CLASS_BASE_PATH")
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DATA_DIR = os.path.join(PROJECT_ROOT, "data", BASE_CLASS_PATH)

# 🔍 auto-detect subjects
subjects = [
    d for d in os.listdir(DATA_DIR)
    if os.path.isdir(os.path.join(DATA_DIR, d))
]

print("📚 Subjects found:", subjects)

for subject in subjects:
    subject_path = f"{BASE_CLASS_PATH}/{subject}"

    print(f"\n🚀 Vectorizing subject: {subject_path}")

    vectorize_book_and_store_to_db(subject_path, "book_vector_db")
    vectorize_chapters(subject_path)
