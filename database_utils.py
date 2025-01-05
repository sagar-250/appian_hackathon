from pymongo import MongoClient
from pydantic import BaseModel
from typing import Dict, List
from classifier import ResponseModel

def upload_to_database(response_data: ResponseModel):
    try:
        client = MongoClient("mongodb://localhost:27017")
        db = client["extract_info"]
        collection = db["appian"]
        data_to_insert = response_data.dict()
        result = collection.insert_one(data_to_insert)
        print(f"Document inserted with ID: {result.inserted_id}")
        return result.inserted_id
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
    finally:
        client.close()
        
def retrieve_documents_by_name(name: str) -> List[Dict]:
    client = MongoClient('mongodb://localhost:27017/')
    db = client['extract_info']
    collection = db['appian']
    query = {'info.name': name}
    documents = collection.find(query)
    return list(documents)



