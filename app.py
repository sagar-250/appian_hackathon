from fastapi import FastAPI, File, UploadFile, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, List
import uvicorn
from database_utils import upload_to_database
from cross_validator import cross_validate
import cross_validator
from extracter import extract_text_and_images_info
from classifier import classifier_summerizer
import classifier
from process_text import process
import tempfile
import json
import os
import mimetypes
import shutil
from pathlib import Path
from adhaar_verification import visual_verification,Validate_aadhaar_num

app = FastAPI(title="Document Processing API")


ALLOWED_MIMETYPES = {
    'application/pdf',
    'image/png',
    'image/jpeg',
    'image/bmp',
    'image/tiff',
    'image/webp'
}

class ResponseModel(BaseModel):
    info: Dict[str, list]
    doc_type: str
    summary: str

def get_file_extension(filename: str) -> str:
    """Get the file extension from the filename."""
    return os.path.splitext(filename)[1].lower()

def sanitize_filename(filename: str) -> str:
    """Sanitize the filename to prevent directory traversal attacks."""
    return os.path.basename(filename)

@app.post("/process-document/", response_model=ResponseModel)
async def process_document(file: UploadFile = File(...)):
    # Check file type
    content_type = file.content_type or mimetypes.guess_type(file.filename)[0]
    if content_type not in ALLOWED_MIMETYPES:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid file type. Allowed types are: PDF and common image formats"
        )
    
    
    with tempfile.TemporaryDirectory() as temp_dir:
        safe_filename = sanitize_filename(file.filename)
        temp_file_path = os.path.join(temp_dir, safe_filename)
        
        try:
         
            with open(temp_file_path, 'wb') as temp_file:
                shutil.copyfileobj(file.file, temp_file)
            
           
            extracted_text = extract_text_and_images_info(temp_file_path)
            if "Poor quality of image" in extracted_text:
                raise Exception(extracted_text)
            cleaned_text = process(extracted_text)
            extracted_data = classifier_summerizer(cleaned_text)
            verification = cross_validate(extracted_data)
            if isinstance(verification, classifier.ResponseModel):
                print("cross verification done")
                if "Aadhaar" in verification.info.keys():
                    visual_eval=visual_verification(temp_file_path)
                    # number_eval=Validate_aadhaar_num(verification.info["Aadhaar"])
                    # if visual_eval and number_eval         
                    if visual_eval:        
                        upload_to_database(verification)
                        print("visual verification done")
                        return json.loads(verification.json())
                    else:
                        raise ValueError("Verification failed in visual and number algorithm check of Aadhaar")
                else:
                    upload_to_database(verification)
                    return json.loads(verification.json())
            else:
                raise ValueError(verification.json())

        except ValueError as ve:
            raise HTTPException(
                status_code=400,
                detail=f"Cross verification failed: {str(ve)}"
            )
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Quality issue: {str(e)}"
            )
        
        finally:
            
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
