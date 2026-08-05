import os
from fastapi import UploadFile
from app.core.config import settings
from app.core.exceptions import FileValidationException

def validate_uploaded_file(file: UploadFile):
    filename = file.filename or ""
    if not filename.lower().endswith(".pdf"):
        raise FileValidationException("Only PDF resumes are supported.")
    
    file.file.seek(0, os.SEEK_END)
    size = file.file.tell()
    file.file.seek(0)
    
    if size > settings.MAX_UPLOAD_SIZE:
        raise FileValidationException("File size exceeds the 5MB limit.")
    
    header = file.file.read(4)
    file.file.seek(0)
    if header != b"%PDF":
        raise FileValidationException("Invalid PDF format structure.")
