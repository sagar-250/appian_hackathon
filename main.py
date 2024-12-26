import streamlit as st
import requests
import json
from typing import Dict, Any
import pandas as pd
from PIL import Image
import io
import PyPDF2
import base64

st.set_page_config(layout="wide")
st.title("Document Processing App")

# Define allowed file types
ALLOWED_TYPES = ["pdf", "png", "jpg", "jpeg", "bmp", "tiff", "webp"]

def display_pdf(file):
    # Read PDF file
    try:
        base64_pdf = base64.b64encode(file.read()).decode('utf-8')
        # Embed PDF viewer
        pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="600" type="application/pdf"></iframe>'
        st.markdown(pdf_display, unsafe_allow_html=True)
        file.seek(0)  # Reset file pointer
    except Exception as e:
        st.error(f"Error displaying PDF: {str(e)}")

# File uploader with multiple file types
uploaded_file = st.file_uploader(
    "Upload your document", 
    type=ALLOWED_TYPES,
    help="Supported formats: PDF, PNG, JPG, JPEG, BMP, TIFF, WEBP"
)

if uploaded_file is not None:
    # Create tabs for organization
    file_tab, results_tab = st.tabs(["📄 File Preview", "📊 Analysis Results"])
    
    with file_tab:
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.write("### File Details")
            # Create a DataFrame for file details
            file_details = pd.DataFrame({
                "Property": ["Filename", "File size (KB)", "File type"],
                "Value": [
                    uploaded_file.name,
                    f"{uploaded_file.size / 1024:.2f}",
                    uploaded_file.type
                ]
            })
            st.dataframe(file_details, hide_index=True)
        
        with col2:
            st.write("### File Preview")
            try:
                if uploaded_file.type and "image" in uploaded_file.type:
                    image_bytes = uploaded_file.read()
                    image = Image.open(io.BytesIO(image_bytes))
                    st.image(image, caption=uploaded_file.name)
                    uploaded_file.seek(0)  # Reset file pointer
                elif uploaded_file.type == "application/pdf":
                    display_pdf(uploaded_file)
            except Exception as e:
                st.error(f"Unable to preview file: {str(e)}")
    
    with results_tab:
        st.write("### Processing document...")
        
        try:
            # Reset file pointer before sending
            uploaded_file.seek(0)
            
            # Create the files dictionary for the request
            files = {
                "file": (
                    uploaded_file.name,
                    uploaded_file.read(),  # Read file content
                    uploaded_file.type or "application/octet-stream"
                )
            }
            
            # Send the file to the FastAPI endpoint
            response = requests.post(
                "http://localhost:8000/process-document/",
                files=files
            )
            
            if response.status_code == 200:
                result = response.json()
                
                # Create columns for different types of information
                col1, col2 = st.columns([1, 1])
                
                with col1:
                    st.write("### Document Type")
                    st.info(result["doc_type"])
                    
                    st.write("### Document Summary")
                    st.write(result["summary"])
                
                with col2:
                    st.write("### Extracted Information")
                    # Convert the info dictionary to a DataFrame
                    info_data = []
                    for key, values in result["info"].items():
                        info_data.append({
                            "Field": key,
                            "Value": ", ".join(values) if isinstance(values, list) else values
                        })
                    info_df = pd.DataFrame(info_data)
                    st.dataframe(info_df, hide_index=True)
                
                # Show raw JSON with option to expand
                with st.expander("View Raw JSON Response"):
                    st.json(result)
                
            else:
                st.error(f"Error processing document: {response.status_code}")
                st.write(response.text)
                
        except requests.exceptions.ConnectionError:
            st.error("⚠️ Failed to connect to the API server. Make sure the FastAPI server is running on http://localhost:8000")
        except Exception as e:
            st.error(f"⚠️ An error occurred: {str(e)}")
            
        finally:
            # Reset file pointer after processing
            uploaded_file.seek(0)

# Add some helpful information at the bottom
st.markdown("""
---
### Notes:
- Make sure your document is clear and readable
- Maximum file size limit is determined by your server configuration
- For best results, ensure your images are properly oriented
""")