from pathlib import Path
from uuid import uuid4
from fastapi import HTTPException, UploadFile, status

from app.core.config import settings

def validate_pdf(file: UploadFile) -> None:
    if file.content_type not in settings.ALLOWED_FILE_TYPES:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Only PDF files allowed",)
    
def generate_unique_filename(original_filename:str) -> str:
    file_extension = Path(original_filename).suffix.lower()

    return f"{uuid4().hex}{file_extension}"

async def save_pdf(file: UploadFile)-> tuple[str, str, int]:
    validate_pdf(file)

    upload_directory = Path(settings.UPLOAD_DIR)
    upload_directory.mkdir(parents=True, exist_ok= True)

    stored_filename = generate_unique_filename(
        file.filename or "document.pdf"
    )    

    file_path = upload_directory / stored_filename

    file_content = await file.read()

    file_size = len(file_content)

    if file_size == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail= "The uploaded PDF is empty",
        )
    
    if file_size > settings.MAX_FILE_SIZE:
        raise HTTPException(
            status_code=status.HTTP_413_CONTENT_TOO_LARGE,
            detail= "The uploaded PDF exceeds the limit"
        )
    
    try:
        file_path.write_bytes(file_content)
    except OSError as error:
        raise HTTPException(
            status_code= status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail= "The PDF could not be saved",
        )from error
    finally:
        await file.close()

    return stored_filename, str(file_path), file_size

def delete_pdf(file_path: str) -> None:
    path = Path(file_path)

    try:
        if path.exists() and path.is_file():
            path.unlink()
    except OSError as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="The PDF could not be deleted.",
        ) from error           