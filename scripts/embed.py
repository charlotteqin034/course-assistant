from sentence_transformers import SentenceTransformer
import chromadb
import json
from pathlib import Path

model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
client = chromadb.PersistentClient(path="./db/vector_store")
collection = client.get_or_create_collection(name="course_syllabus")


chunk_dir = Path("/Users/charlotte/Documents/GitHub/course-assistant/data/processed/chunks")
chunks_with_metadata = []
course_names = ["201", "270", "304", "352"]

for i, file in enumerate(chunk_dir.iterdir()):
    with open(file, 'r', encoding="utf-8") as f:
        chunks = json.load(f)
    
    for j, c in enumerate(chunks):
        chunk_dict = {
            "id": "",
            "text": "",
            "metadata": {}
        }
        metadata = {
            "course_doc": "",
            "doc_type": "syllabus",
            "chunk_index": 0
        }
        
        chunk_dict['id'] = f"{course_names[i]}_chunk_{j}"
        chunk_dict['text'] = c
        metadata["course_doc"] = course_names[i]
        metadata["chunk_index"] = j
        chunk_dict['metadata'] = metadata

        chunks_with_metadata.append(chunk_dict)
        
    

documents = [c["text"] for c in chunks_with_metadata]
metadatas = [c["metadata"] for c in chunks_with_metadata]
ids = [c["id"] for c in chunks_with_metadata]

embeddings = model.encode(documents).tolist()
collection.upsert(documents=documents, embeddings=embeddings, metadatas=metadatas, ids=ids)

