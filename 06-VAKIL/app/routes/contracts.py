from fastapi import APIRouter, HTTPException, UploadFile, File
import os
from config import ALLOWED_EXTENSIONS, MAX_FILE_SIZE_MB, UPLOAD_FOLDER
import uuid 
from service.document_parser import extract_text
from models import Contract

router = APIRouter(
    prefix="/contracts",
    tags=["contracts"],
)

@router.post("/upload")
async def upload_contract(
    file: UploadFile = File(...)
):
    """
    Endpoint to upload a contract for analysis.
    """
    # Logic to handle contract upload goes here
    ext = os.path.splitext(file.filename)[1]
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400, detail="Invalid file type. Allowed types are: .pdf, .docx, .txt")

    content = await file.read()
    # Here you would typically save the file to a database or storage
    # For demonstration, we'll just return the filename and size
    if len(content) > MAX_FILE_SIZE_MB * 1024 * 1024:
        raise HTTPException(status_code=400, detail=f"File size exceeds the maximum limit of {MAX_FILE_SIZE_MB} MB")

    
    return {"filename": file.filename, "size": len(content)}

    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    unique_filename = f"{uuid.uuid4().hex}{ext}"

    file_path = os.path.join(UPLOAD_FOLDER, unique_filename)
    with open(file_path, "wb") as f:
        f.write(content)
    parsed_text = extract_text(file_path)

    contract_data = Contract(
        id=uuid.uuid4().hex,
        title=file.filename,
        content=parsed_text,
        created_at="2024-01-01T00:00:00Z",  # Placeholder, replace with actual timestamp
        text_count=len(parsed_text.split()),
        page_count=0,  # Placeholder, replace with actual page count if applicable
        status="uploaded"   
    )   


