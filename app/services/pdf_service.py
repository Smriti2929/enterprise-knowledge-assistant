from pathlib import Path 

import pymupdf
from fastapi import HTTPException, status

def extract_text_from_pdf(file_path: str) -> tuple[list[str], int]:
    # extracting the texts from PDF page by page 
    # returning : tuple[list[str], int]: 
    # this gives extracted pages with their texts
    # totla no of pges

    path = Path(file_path)

    if not path.exists() or not path.is_file():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail= "PDF file not found.",
        ) 
    
    page_texts: list[str] = []

    try: 
        with pymupdf.open(path) as pdf:
            page_count = pdf.page_count

            if page_count == 0:
                raise HTTPException(
                    status_code= status.HTTP_400_BAD_REQUEST,
                    detail="The PDF contains no pages.",
                )
            
            for page in pdf:
                text = page.get_text(
                    "text",
                    sort = True,
                ).strip()

                page_texts.append(text)

    except HTTPException:
        raise

    except(
        pymupdf.FileDataError,
        RuntimeError,
        ValueError,
    ) as error:
        raise HTTPException(
            status_code= status.HTTP_400_BAD_REQUEST,
            detail="The file could not be read as a valid PDF",
        ) from error

    return page_texts, page_count            