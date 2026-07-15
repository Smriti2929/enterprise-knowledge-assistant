from datetime import datetime
from pydantic import BaseModel

class DocumentResponse(BaseModel):
    id: int
    filename: str
    stored_filename: str 
    content_type: str
    file_size: int
    uploaded_at: datetime
    owner_id: int

    model_config = {
        "from_attributes": True
    }

class DocumentListResponse(BaseModel):
    documents: list[DocumentResponse]
    total: int

class DocumentExtractResponse(BaseModel):
    document_id: int
    filename: str
    page_count: int
    extracted_page_count: int
    character_count: int
    text_path: str
    text_preview: str
    requires_ocr: bool

    