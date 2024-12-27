import fitz  # PyMuPDF
import base64
import os
import json
import requests
from ocr import image_to_text

params = {
    'models': 'quality',
    'api_user': os.getenv('API_USER'),
    'api_secret': os.getenv('API_SECRET')
}

def extract_text_and_images_info(input_path):
    file_name = os.path.basename(input_path).split('/')[-1]
    if input_path.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tiff', '.webp')):
        with open(input_path, "rb") as image_file:
            files = {'media': image_file}
            r = requests.post('https://api.sightengine.com/1.0/check.json', files=files, data=params)
            output = json.loads(r.text)
            
            if output['quality']['score'] < 0.26:
                print("Poor quality of image")
                return "Poor quality of image"
            else:
                print("quality_ok")

        with open(input_path, "rb") as image_file:
            image_bytes = image_file.read()
            image_base64 = base64.b64encode(image_bytes).decode("utf-8")
            text = image_to_text(image_base64)
            return f"{file_name}\n{text}"

    elif input_path.lower().endswith('.pdf'):
        pdf_file = fitz.open(input_path)
        all_text = f"File name: {file_name}\n"  # Initialize with the file name
        for page_index in range(len(pdf_file)):
            page = pdf_file.load_page(page_index)
            all_text += page.get_text() + "\n"
            image_list = page.get_images(full=True)
            for img in image_list:
                xref = img[0]
                base_image = pdf_file.extract_image(xref)
                image_bytes = base_image["image"]
                image_base64 = base64.b64encode(image_bytes).decode("utf-8")
                
                files = {'media': ("extracted_image", image_bytes)}
                r = requests.post('https://api.sightengine.com/1.0/check.json', files=files, data=params)
                output = json.loads(r.text)
                
                if output['quality']['score'] < 0.26:
                    return(f"Poor quality of image at page {page_index +1} ")
                                        
                else:
                    print(f"quality ok {output['quality']['score']}")
                    img_text = image_to_text(image_base64)
                    all_text += img_text + "\n"
        return all_text

    else:
        raise ValueError("Unsupported file type. Please provide a PDF or image file.")
