from sentence_transformers import SentenceTransformer
import chromadb
import json

model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
client = chromadb.PersistenClient(path="./db/vector_store")
collection = client.get_or_create_collection(name="course_syllabus")

chunk_dir = "/Users/charlotte/Documents/GitHub/course-assistant/data/processed/chunks"
chunks_with_metadata = []

for file in chunk_dir.iterdir():
    with open(file, 'r', encoding="utf-8") as f:
        chunks = json.load(f)

    chunk_dict = {
        "id": "",
        "text": "",
        "metadata": {}
    }
    metadata = {
        "course": "",
        "doc_type": "",
        "chunk_index": 0
    }
    for i, c in enumerate(chunks):
        chunk_dict['id'] = f"{file}_chunk_{i}"
        chunk_dict['text'] = c
        metadata["course_doc"] = file
        metadata["chunk_index"] = i
        chunk_dict['metadata'] = metadata

        chunks_with_metadata.append(chunk_dict)
        
    

documents = [c["text"] for c in chunks_with_metadata]
metadatas = [c["metadata"] for c in chunks_with_metadata]
ids = [c["id"] for c in chunks_with_metadata]

embeddings = model.encode(documents).tolist()
collection.upsert(documents=documents, embeddings=embeddings, metadata=metadata, ids=ids)

