
from PyPDF2 import PdfReader
from docx import Document
import os

def extract_text_from_pdf(file_path: str) -> str:
    """
    Extract text from a PDF file.

    Args:
        file_path (str): The path to the PDF file.
    """
    text = ""
    with open(file_path, 'rb') as f:
        reader = PdfReader(f)
        for page in reader.pages:
            text += page.extract_text() + "\n"
    return text


def extract_text_from_txt(file_path: str) -> str:
    """
    Extract text from a .txt file.

    Args:
        file_path (str): The path to the .txt file.
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()

def extract_text_from_docx(file_path: str) -> str:
    """
    Extract text from a .docx file.

    Args:
        file_path (str): The path to the .docx file.
    """
    
    doc = Document(file_path)
    return "\n".join([para.text for para in doc.paragraphs])    


def extract_text(file_path: str) -> str:
    """
    Extract text from a file based on its extension.

    Args:
        file_path (str): The path to the file.
    """
    ext = os.path.splitext(file_path)[1].lower()
    if ext == ".pdf":
        return extract_text_from_pdf(file_path)
    elif ext == ".docx":
        return extract_text_from_docx(file_path)
    elif ext == ".txt":
        return extract_text_from_txt(file_path)
    else:
        raise ValueError(f"Unsupported file extension: {ext}")