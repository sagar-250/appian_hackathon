# Project README

## Overview

This project uses [Groq](https://groq.com/) (LLM and VLM) and [Sightengine](https://sightengine.com/) (quality check) to analyze uploaded files and provide insights through a simple UI based on [Streamlit](https://streamlit.io). Below are the steps to set up and run the project, along with a description of the user interface.

The objective of this project is to create an easy to use document verification tool. The user may upload a document (provided that it is either an image or a pdf document) and the tool will automatically evaluate the quality of the picture provided. If suitable, the tool will extract relevant information from it and categorise the same.

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
