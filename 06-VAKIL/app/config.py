from dotenv import load_dotenv
import os

load_dotenv()

MONGODB_URI = os.getenv("MONGODB_URI")

ALLOWED_EXTENSIONS = {".pdf", ".docx", ".txt"}
MAX_FILE_SIZE_MB = 10  # Maximum file size in megabytes
UPLOAD_FOLDER = os.getenv("UPLOAD_FOLDER", "uploads")  # Default upload folder if not set in .env