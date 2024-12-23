from dotenv import load_dotenv
load_dotenv()

from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel
from typing import List
import instructor
import json
from groq import Groq
import os

# Initialize Groq client
client = Groq()

class InfoModel(BaseModel):
  info_type: str
  value : str 
class ResponseModel(BaseModel):
    info: List[InfoModel]
    doc_type: str
    summary: str 
    
client = instructor.from_groq(Groq(), mode=instructor.Mode.JSON) 
output_schema={
                  "info": [
                      {
                          "info_type": "name",
                          "value": "[extracted name]"
                      },
                      {
                          "info_type": "email",
                          "value": "[extracted email]"
                      },
                  ],
                  "doc_type": "[type of document]",
                  "summary": "[brief summary of the document content]"
              }
def classifier_summerizer(text):
  types=["Application_for_bank (for e.g. creditcard,savings accoun opening)","Identity_Document","Supporting_Financial_Document (for e.g. income statements/paystubs, tax returns)","Reciepts"]
  messages = [
          {
              "role": "system",
              "content": f"""
              Please analyze the text : {text} 
              and extract relevant information in the following structure:
              1. Identify key pieces of person information like:
                - if some field is not specified (for e.g. in bank application) dont include it
                - Names - Email addresses - Identification numbers
                - DONT PUT ANY NON PERSONAL DETAIL (OR STORE DETAIL IN RECIPT .keep store details in the summary KEY)
                - Don't put info which is censored like e.g XXXXXXXXXXXXXXXXXXXXX041 
                 
              2. For each piece of information found:
                - Classify its type (e.g., "name", "email", "phone", etc.)
                - Extract the exact value
              3. Provide a brief summary of the overall document including important details such as dates , amounts,statements address etc.
              4. Identify the type of document among the following list : {types}
              Format your response as follows:{output_schema}
              """
          }
      ]
  response = client.chat.completions.create(
        model="llama-3.1-70b-versatile",
        response_model=ResponseModel,
        messages=messages,
        temperature=0.9,
        max_tokens=1000,
    )

  return response.json()


