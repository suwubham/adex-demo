import boto3
import uuid
from datetime import datetime
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

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

def create_table():
    try:
        table = dynamodb.create_table(
            TableName=table_name,
            KeySchema=[{"AttributeName": "id", "KeyType": "HASH"}],
            AttributeDefinitions=[{"AttributeName": "id", "AttributeType": "S"}],
            ProvisionedThroughput={"ReadCapacityUnits": 5, "WriteCapacityUnits": 5},
        )
        table.wait_until_exists()
        return table
    except dynamodb.meta.client.exceptions.ResourceInUseException:
        return dynamodb.Table(table_name)

thoughts_table = create_table()

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
