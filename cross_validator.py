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
    db_data=retrieve_documents_by_name(response_info["name"])
    if not db_data:
        print("No data found in the database.")
        return response_data
    print(db_data)
    messages = [
          {
              "role": "system",
              "content" : """You are a helpful assistant who helps in cross verification of user data from exsisting database records
              
              if the personal information given in reponse data matches with pre exsisting database record then it verified  
              
              dont check missing field just cross verify diffrent field of response data from diffrent chunks of database records"""},
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
    info={"name": ["Sagar Bag"], "age": ["20"], "city": ["Mumbai"]},
    doc_type="application",
    summary="Summary of Sagar's application"
)

db_data = [
    {"info": {"name": ["Sagar"], "age": ["20"], "city": ["Mumbai"]}, "doc_type": "identity_doc", "summary": "Addhar card of Sagar"},
    {"info": {"name": ["Sagar"], "age": ["20"], "city": ["Mumbai"]}, "doc_type": "Recipt", "summary": "reciept of sagar"}
]

# cross_validate(response_data)
