import os
import json
import uuid
from dotenv import load_dotenv
from qdrant_client import QdrantClient
from qdrant_client.http import models
from sentence_transformers import SentenceTransformer
from pyvi import ViTokenizer

# Load environment variables
load_dotenv()
QDRANT_URL = os.getenv("qdrant_url")
QDRANT_API_KEY = os.getenv("qdrant_api")

# Initialize Qdrant Client
client = QdrantClient(
    url=QDRANT_URL,
    api_key=QDRANT_API_KEY,
)

# Load Embedding Model
print("Loading model...")
model = SentenceTransformer("huyydangg/DEk21_hcmute_embedding")
vector_size = model.get_sentence_embedding_dimension()

# Create Collection if it doesn't exist
COLLECTION_NAME = "law_embedding"
if not client.collection_exists(COLLECTION_NAME):
    print(f"Creating collection: {COLLECTION_NAME}")
    client.create_collection(
        collection_name=COLLECTION_NAME,
        vectors_config=models.VectorParams(
            size=vector_size,
            distance=models.Distance.COSINE
        )
    )

# Load Data from JSON
print("Loading data...")
with open("law.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# Process and Upload Data
points = []
print("Processing and generating embeddings...")

for doc in data:
    url = doc.get("url", "")
    short_title = doc.get("short_title", "")
    full_title = doc.get("full_title", "")
    
    for layer in doc.get("content_layers", []):
        layer_title = layer.get("title", "")
        layer_content_list = layer.get("content", [])
        
        # Combine title and content into one paragraph for embedding
        text_to_embed = layer_title + " " + " ".join(layer_content_list)
        
        # Tokenize using pyvi
        segmented_text = ViTokenizer.tokenize(text_to_embed)
        
        # Generate embedding and convert to standard Python list
        embedding = model.encode(segmented_text).tolist()
        
        # Generate UUID5 using NAMESPACE_DNS and the required string format
        point_id = str(uuid.uuid5(uuid.NAMESPACE_DNS, short_title + layer_title))
        
        # Construct the payload
        payload = {
            "url": url,
            "short_title": short_title,
            "full_title": full_title,
            "data": {
                "type": layer.get("type", ""),
                "title": layer_title,
                "content": layer_content_list,
                "is_definition": layer.get("is_definition", False)
            }
        }
        
        # Create the point for Qdrant
        point = models.PointStruct(
            id=point_id,
            vector=embedding,
            payload=payload
        )
        points.append(point)

# Upload to Qdrant in batches to prevent memory/timeout issues
print(f"Uploading {len(points)} points to Qdrant...")
BATCH_SIZE = 100
for i in range(0, len(points), BATCH_SIZE):
    batch = points[i:i + BATCH_SIZE]
    client.upsert(
        collection_name=COLLECTION_NAME,
        points=batch
    )