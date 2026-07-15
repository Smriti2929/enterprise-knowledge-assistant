import re
from pathlib import Path
from fastapi import HTTPException, status
from app.core.config import settings

def clean_page_text(text: str) -> str:
    #  Perform basic cleanup while preserving paragraph boundaries.

    if not text:
        return ""
    
    # Normalise Windows and old Mac line endings.
    text = text.replace("\r\n", "\n").replace("\r", "\n")

    #Remove unnecessary spaces and tabs
    text = re.sub(r"[\t]+", " ", text)

    #remove spaces surrounding line breaks
    text = re.sub(r" *\n *", "\n", text)

    # Limit excessive blank lines to one paragraph break.
    text = re.sub(r"\n{3,}", "\n\n", text)

    return text.strip()

def combine_and_clean_pages(page_texts: list[str]) -> str:
    # Clean each page and combine pages with traceable page markers.
    cleaned_pages: list[str] = []

    for page_number, page_text in enumerate(page_texts, start=1):
        cleaned_text = clean_page_text(page_text)

        if cleaned_text:
            cleaned_pages.append(
                f"---Page {page_number} ---\n{cleaned_text}"
            )

    return "\n\n".join(cleaned_pages).strip()   



# Temporary text storage     

def save_extracted_text(
        document_id: int,
        stored_filename: str,
        text: str,
) -> str:
    
    # save extracted text temporarily as a utf-8 .txt file

    output_directory = Path(settings.EXTRACTED_TEXT_DIR)
    output_directory.mkdir(
        parents= True,
        exist_ok= True,
    )

    filename_stem = Path(stored_filename).stem
    output_filename = f"{document_id}_{filename_stem}.txt"
    output_path = output_directory / output_filename

    try:
        output_path.write_text(
            text,
            encoding= "utf-8",
        )
    except OSError as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail= "The extracted text could not be stored",
        ) from error
    return str(output_path)

def delete_extracted_text(text_path: str) -> None:
    path = Path(text_path)

    try:
        if path.exists() and path.is_file():
            path.unlink()
    except OSError as error:
        raise HTTPException(
            status_code= status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail= "The extracted text could not be selected",
        ) from error       