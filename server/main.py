import boto3
import uuid
from datetime import datetime
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import os
import sys

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

dynamodb = boto3.resource("dynamodb", region_name="us-east-1")
table_name = "Thoughts"

try:
    thoughts_table = dynamodb.Table(table_name)
    thoughts_table.table_status  
    print("Connected to existing table:", table_name)
except dynamodb.meta.client.exceptions.ResourceNotFoundException:
    print(f"Error: Table '{table_name}' does not exist.")
    sys.exit(1)  
except Exception as e:
    print(f"Unexpected error: {e}")
    sys.exit(1)  


class Thought(BaseModel):
    text: str

@app.post("/thoughts/")
def create_thought(thought: Thought):
    thought_id = str(uuid.uuid4())
    timestamp = datetime.utcnow().isoformat()  

    thoughts_table.put_item(Item={"id": thought_id, "text": thought.text, "timestamp": timestamp})
    return {"id": thought_id, "message": "Thought shared!", "timestamp": timestamp}

@app.get("/thoughts/")
def get_all_thoughts():
    response = thoughts_table.scan()
    return response.get("Items", [])

@app.post("/deleteall")
def delete_all_thoughts():
    response = thoughts_table.scan()
    items = response.get("Items", [])
    for item in items:
        thoughts_table.delete_item(Key={"id": item["id"]})
    return {"message": "All thoughts deleted!"}
