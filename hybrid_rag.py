import os
import json
import uuid
from dotenv import load_dotenv
from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer
from pyvi import ViTokenizer
import bm25s

load_dotenv()
QDRANT_URL = os.getenv("qdrant_url")
QDRANT_API_KEY = os.getenv("qdrant_api")

client = QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY)
collection_name = "law_embedding"
model = SentenceTransformer("huyydangg/DEk21_hcmute_embedding")

print("Building BM25 Index...")
with open(r"D:\Python\Projects\Community\Law\data\law.json", "r", encoding="utf-8") as f:
    data = json.load(f)

corpus_texts = []
corpus_ids = []
payload_map = {} # To easily fetch data later

for doc in data:
    short_title = doc.get("short_title", "")
    for layer in doc.get("content_layers", []):
        layer_title = layer.get("title", "")
        content = " ".join(layer.get("content", []))
        text_to_index = f"{short_title} - {layer_title}. {content}"
        
        point_id = str(uuid.uuid5(uuid.NAMESPACE_DNS, short_title + layer_title))
        
        corpus_texts.append(text_to_index)
        corpus_ids.append(point_id)
        payload_map[point_id] = {
            "title": layer_title,
            "text": text_to_index
        }

tokenized_corpus = [ViTokenizer.tokenize(text) for text in corpus_texts]
bm25_tokens = bm25s.tokenize(tokenized_corpus)

retriever = bm25s.BM25()
retriever.index(bm25_tokens)

def hybrid_search(query, top_k=3):
    # Segment query
    segmented_query = ViTokenizer.tokenize(query)
    
    bm25_query_tokens = bm25s.tokenize([segmented_query])
    bm25_results, bm25_scores = retriever.retrieve(bm25_query_tokens, k=top_k * 2)
    
    # Extract IDs
    lexical_ids = [corpus_ids[i] for i in bm25_results[0]]
    
    query_vector = model.encode([segmented_query])[0].tolist()
    
    # Use query_points for the newer Qdrant API
    response = client.query_points(
        collection_name=collection_name,
        query=query_vector,
        limit=top_k * 2
    )
    qdrant_results = response.points
    
    vector_ids = [res.id for res in qdrant_results]
    
    # Combine score + RRF
    combined_scores = {}
    k = 60
    
    # Calculate Lexical RRF scores
    for rank, doc_id in enumerate(lexical_ids):
        rrf_score = 1 / (k + rank + 1)
        # Apply 30% weight
        combined_scores[doc_id] = combined_scores.get(doc_id, 0.0) + (rrf_score * 0.3)
        
    # Calculate Vector RRF scores
    for rank, doc_id in enumerate(vector_ids):
        rrf_score = 1 / (k + rank + 1)
        # Apply 70% weight
        combined_scores[doc_id] = combined_scores.get(doc_id, 0.0) + (rrf_score * 0.7)
        
    sorted_results = sorted(combined_scores.items(), key=lambda x: x[1], reverse=True)
    
    final_top_k = sorted_results[:top_k]
    
    print(f"Results for: '{query}'")
    for rank, (doc_id, score) in enumerate(final_top_k):
        doc_info = payload_map.get(doc_id, {})
        print(f"{rank + 1}. Score: {score:.4f} | Title: {doc_info.get('title')}")

if __name__ == "__main__":
    test_query = "Điều 1 trong Thông tư 06/2026/TT-BVHTTDL là gì?"
    hybrid_search(test_query, top_k=3)