from extracter import extract_text_and_images_info
from classifier import classifier_summerizer
from process_text import process
extracted_text=extract_text_and_images_info("samples\Sagar's_recipt.pdf")
print(extracted_text)
cleaned_text=process(extracted_text)

result=classifier_summerizer(cleaned_text)
print(result)