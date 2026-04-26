from sentence_transformers import SentenceTransformer
import torch
from pyvi import ViTokenizer
import json

# Download from the 🤗 Hub
model = SentenceTransformer("huyydangg/DEk21_hcmute_embedding")

# Define query (câu hỏi pháp luật) và docs (điều luật)
query = "Điều kiện để kết hôn hợp pháp là gì?"
docs = [
    "Điều 8 Bộ luật Dân sự 2015 quy định về quyền và nghĩa vụ của công dân trong quan hệ gia đình.",
    "Điều 18 Luật Hôn nhân và gia đình 2014 quy định về độ tuổi kết hôn của nam và nữ.",
    "Điều 14 Bộ luật Dân sự 2015 quy định về quyền và nghĩa vụ của cá nhân khi tham gia hợp đồng.",
    "Điều 27 Luật Hôn nhân và gia đình 2014 quy định về các trường hợp không được kết hôn.",
    "Điều 51 Luật Hôn nhân và gia đình 2014 quy định về việc kết hôn giữa công dân Việt Nam và người nước ngoài."
]

# Tách từ cho query
segmented_query = ViTokenizer.tokenize(query)

# Tách từ cho từng dòng văn bản
segmented_docs = [ViTokenizer.tokenize(doc) for doc in docs]

# Encode query and documents
query_embedding = model.encode([segmented_query])
doc_embeddings = model.encode(segmented_docs)
similarities = torch.nn.functional.cosine_similarity(
    torch.tensor(query_embedding), torch.tensor(doc_embeddings)
).flatten()

# Sort documents by cosine similarity
sorted_indices = torch.argsort(similarities, descending=True)
sorted_docs = [docs[idx] for idx in sorted_indices]
sorted_scores = [similarities[idx].item() for idx in sorted_indices]

# Print sorted documents with their cosine scores
for doc, score in zip(sorted_docs, sorted_scores):
    print(f"Document: {doc} - Cosine Similarity: {score:.4f}")
