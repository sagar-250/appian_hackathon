from fastapi import FastAPI, File, UploadFile, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, List
import uvicorn
from extracter import extract_text_and_images_info
from classifier import classifier_summerizer
from process_text import process
import tempfile
import json
import os
import mimetypes
import shutil
from pathlib import Path

app = FastAPI(title="Document Processing API")

# Define allowed file types
ALLOWED_MIMETYPES = {
    'application/pdf',
    'image/png',
    'image/jpeg',
    'image/bmp',
    'image/tiff',
    'image/webp'
}

class DocumentResponse(BaseModel):
    info: Dict[str, list]
    doc_type: str
    summary: str

def get_file_extension(filename: str) -> str:
    """Get the file extension from the filename."""
    return os.path.splitext(filename)[1].lower()

def sanitize_filename(filename: str) -> str:
    """Sanitize the filename to prevent directory traversal attacks."""
    return os.path.basename(filename)

@app.post("/process-document/", response_model=DocumentResponse)
async def process_document(file: UploadFile = File(...)):
    # Check file type
    content_type = file.content_type or mimetypes.guess_type(file.filename)[0]
    if content_type not in ALLOWED_MIMETYPES:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid file type. Allowed types are: PDF and common image formats"
        )
    
    # Create a temporary directory
    with tempfile.TemporaryDirectory() as temp_dir:
        # Sanitize and preserve original filename
        safe_filename = sanitize_filename(file.filename)
        temp_file_path = os.path.join(temp_dir, safe_filename)
        
        try:
            # Save the file with its original name in the temporary directory
            with open(temp_file_path, 'wb') as temp_file:
                shutil.copyfileobj(file.file, temp_file)
            
            # Process the document
            extracted_text = extract_text_and_images_info(temp_file_path)
            cleaned_text = process(extracted_text)
            result = classifier_summerizer(cleaned_text)
            print(result)
            return json.loads(result)

        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Error processing document: {str(e)}"
            )
        
        finally:
            # The temporary directory and its contents will be automatically cleaned up
            file.file.close()

@app.get("/supported-formats/")
async def get_supported_formats():
    """Return list of supported file formats"""
    return {
        "supported_formats": [
            "PDF (.pdf)",
            "PNG (.png)",
            "JPEG (.jpg, .jpeg)",
            "BMP (.bmp)",
            "TIFF (.tiff)",
            "WebP (.webp)"
        ]
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)