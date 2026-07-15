from fastapi import APIRouter, Depends, File, UploadFile, status, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.document import Document
from app.models.user import User
from app.schemas.document import DocumentResponse, DocumentListResponse, DocumentExtractResponse
from app.services.file_service import save_pdf, delete_pdf

from app.services.pdf_service import extract_text_from_pdf
from app.services.text_service import(
    combine_and_clean_pages,
    save_extracted_text,
)

router = APIRouter(prefix= "/documents", tags=["Documents"],)

@router.post("/upload", response_model=DocumentResponse, status_code= status.HTTP_201_CREATED,)

async def upload_document(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    stored_filename, filepath, file_size = await save_pdf(file)

    document = Document(
        filename = file.filename or "document.pdf",
        stored_filename = stored_filename,
        filepath=filepath,
        content_type=file.content_type or "application/pdf",
        file_size=file_size,
        owner_id=current_user.id,
    )

    try:
        db.add(document)
        db.commit()
        db.refresh(document)

    except Exception:
        db.rollback()
        raise 

    return document

@router.get("", response_model= DocumentListResponse,)

def list_documents(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    documents = (
        db.query(Document)
        .filter(Document.owner_id == current_user.id)
        .order_by(Document.uploaded_at.desc())
        .all()
    )

    return {
        "documents": documents,
        "total":  len(documents),
    }

@router.delete(
    "/{document_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_document(
    document_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    document = (
        db.query(Document)
        .filter(
            Document.id == document_id,
            Document.owner_id == current_user.id,
        )
        .first()
    )

    if document is None:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail= "Document not found",
        )
    
    delete_pdf(document.filepath)

    db.delete(document)
    db.commit()

# extract PDF text
@router.post(
    "/{document_id}/extract",
    response_model= DocumentExtractResponse,
)

def extract_document(
    document_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    document = (
        db.query(Document)
        .filter(
            Document.id == document_id,
            Document.owner_id == current_user.id,
        )
        .first()
    )

    if document is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found",
        )
    
    page_texts, page_count = extract_text_from_pdf(
        document.filepath
    )

    extracted_page_count = sum(
        1 for page_text in page_texts if page_text.strip()
    )

    cleaned_text = combine_and_clean_pages(page_texts)

    if not cleaned_text:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail=(
                "No extractable text was found."
                "The PDF may be scanned and require OCR."
            ),
        )
    
    text_path = save_extracted_text(
        document_id= document.id,
        stored_filename= document.stored_filename,
        text = cleaned_text,
    )

    requires_ocr = extracted_page_count < page_count

    return {
        "document_id": document.id,
        "filename": document.filename,
        "page_count": page_count,
        "extracted_page_count": extracted_page_count,
        "character_count": len(cleaned_text),
        "text_path": text_path,
        "text_preview": cleaned_text[:500],
        "requires_ocr": requires_ocr,  
    }