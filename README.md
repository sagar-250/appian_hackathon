# Project README

## Overview

This project uses [Groq](https://groq.com/) (LLM and VLM) and [Sightengine](https://sightengine.com/) (quality check) to analyze uploaded files and provide insights through a simple UI based on [Streamlit](https://streamlit.io). Below are the steps to set up and run the project, along with a description of the user interface.

This project is an easy-to-use document verification tool designed to process and analyze uploaded documents. The tool supports both image and PDF files, evaluating their quality, extracting context, cleaning the data, and generating classifications and summaries.

## Working Architecture

1. **Document Upload**
   - Users can upload documents in either **image** (JPEG, PNG, etc.) or **PDF** format.

2. **Document Quality Evaluation**
   - The tool automatically assesses the quality of the uploaded document to determine if it is suitable for processing (e.g., resolution, clarity).

3. **Context Extraction**
   - **For images**: The image is passed directly to a **Vision Language Model (VLM)** to extract contextual information.
   - **For PDFs**: The document is broken down into its text and image components:
     - Text is extracted separately.
     - Images are processed through the VLM.
     - The extracted text and image summaries are combined before proceeding with further processing.

4. **Data Cleaning**
   - The extracted context is then sent through a **data processor** that cleans the content, removing unnecessary information and ensuring accuracy.

5. **Classification ,Summarization & Extraction**
   - The cleaned data is processed by a **classifier** that categorizes the document and generates a summary of the key points and information and extracts personal info.


Our goal is to extend the capabilities of this tool to perform document verification and authentication as well.This would ensure that all documents uploaded to the system are not only processed for quality and categorization but are also confirmed to be legitimate. By incorporating these additional capabilities, the tool will provide a more robust solution for managing and validating documents effectively


---

## Setup Instructions

1. Add the following keys to your ```.env``` file:

   ```
   GROQ_API_KEY=<your_groq_api_key>
   API_USER=<your_api_user>
   API_SECRET=<your_api_secret>
   ```
   

3. Run the backend server by executing:

   ```
   python app.py
   ```
   

   This will start the model endpoint.

5. Launch the Streamlit app using the following command:

   ```
   streamlit run main.py
   ```
   

---

## User Interface

### File Upload and Preview

The UI allows users to upload files and preview them before analysis
![image](https://github.com/user-attachments/assets/4bdae180-d2b0-4dae-8f69-85df3d10a7c5)


### Analysis Output

After running the analysis, the results are displayed in a structured format
![image](https://github.com/user-attachments/assets/2d7dd46e-2ab3-4ecc-b4ed-b76f488f5c9e)



---

## Notes

- Ensure that the .env file is properly configured before running the app.
- Both the backend (app.py) and frontend (main.py) must be running for the full functionality of the app.
