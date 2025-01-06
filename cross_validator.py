from dotenv import load_dotenv
from typing import List, Dict
from pydantic import BaseModel
import instructor
import json
from groq import Groq
from database_utils import retrieve_documents_by_name
load_dotenv()



class EvalModel(BaseModel):
    reason : str
    eval : bool
    

class ResponseModel(BaseModel):
    info: Dict[str, List[str]]
    doc_type: str
    summary: str

client = instructor.from_groq(Groq(), mode=instructor.Mode.JSON) 

def cross_validate(response_data: ResponseModel) -> bool:
    response_info = response_data.info
    name = response_info.get("name","")
    if name == "":
        return response_data
    db_data=retrieve_documents_by_name(response_info["name"])
    if not db_data:
        print("No data found in the database.")
        return response_data
    print(db_data)
    messages = [
          {
            "role": "system",
            "content": """You are a helpful assistant who helps in cross-verification of user data from existing database records.
            If the personal information given in the response data matches with the pre-existing database records, then it is verified.

            - Consider equivalent values that have case differences (e.g., "MALE" and "male") or minor semantic variations (e.g., "Yes" and "yes") as matching.
            - Do not check for missing fields or exact key string matches; focus only on the cross-verification of different field values between the response data and the database records.
            - Also, identify and explain any significant differences in values that lead to a false evaluation.

            Output:
            {
                reason: "The reason for the evaluation, along with appropriate information and values."
                eval: true/false
            }"""
            },
          {
              "role": "user",
              "content":f"Response Data: {response_info}\nDatabase Record: {db_data}"
          }]
    
    response = client.chat.completions.create(
        model="llama-3.1-70b-versatile",
        response_model=EvalModel,
        messages=messages,
        temperature=0.9,
        max_tokens=1000,
    )
    print(response.json())
    if json.loads(response.json())["eval"] == True:
        print("true")
        return response_data
    else:
        print("false")
        return response

    

response_data = ResponseModel(
    info={ "age": ["20"], "city": ["Mumbai"]},
    doc_type="application",
    summary="Summary of Sagar's application"
)

db_data = [
    {"info": {"name": ["Sagar"], "age": ["20"], "city": ["Mumbai"]}, "doc_type": "identity_doc", "summary": "Addhar card of Sagar"},
    {"info": {"name": ["Sagar"], "age": ["20"], "city": ["Mumbai"]}, "doc_type": "Recipt", "summary": "reciept of sagar"}
]

