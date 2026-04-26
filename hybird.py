from qdrant_client import QdrantClient
from dotenv import load_dotenv
import os
import pandas as pd

dir = r"D:\Python\Projects\Community\Projects\RAG\law.json"
load_dotenv(r"D:\Python\Projects\Community\Projects\RAG\.env")

data = pd.read_json(dir)

def extract_and_store_content(contents: list):
    for i in contents:
        _type = i['type']
        title = i['title']
        content = i['content']
        is_definition = i['is_definition']

qdrant_client = QdrantClient(
    url=os.getenv("qdrant_url"), 
    api_key=os.getenv("qdrant_api"),
    cloud_inference=True
)

print(qdrant_client.get_collections())