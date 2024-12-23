import fitz  # PyMuPDF
import base64
from ocr import image_to_text

def extract_text_and_images_info(input_path):
    if input_path.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tiff','.webp')):
        with open(input_path, "rb") as image_file:
            image_bytes = image_file.read()
            image_base64 = base64.b64encode(image_bytes).decode("utf-8")
            return image_to_text(image_base64)
    elif input_path.lower().endswith('.pdf'):
        pdf_file = fitz.open(input_path)
        all_text = ""
        for page_index in range(len(pdf_file)):
            page = pdf_file.load_page(page_index)
            all_text += page.get_text() + "\n"
            image_list = page.get_images(full=True)
            for img in image_list:
                xref = img[0]
                base_image = pdf_file.extract_image(xref)
                image_bytes = base_image["image"]
                image_base64 = base64.b64encode(image_bytes).decode("utf-8")
                img_text = image_to_text(image_base64)
                all_text += img_text + "\n"
        return all_text
    else:
        raise ValueError("Unsupported file type. Please provide a PDF or image file.")


