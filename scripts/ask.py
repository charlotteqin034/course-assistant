from config import EMBEDDING_MODEL, VECTOR_STORE_PATH, DB_PATH
import chromadb
from sentence_transformers import SentenceTransformer
from anthropic import Anthropic
import os
from dotenv import load_dotenv
load_dotenv()


embedder = SentenceTransformer(EMBEDDING_MODEL)
client = chromadb.PersistentClient(path=VECTOR_STORE_PATH)
collection = client.get_or_create_collection(name="course_syllabus")
llm_client = Anthropic(
    api_key=os.getenv("ANTHROPIC_API_KEY")
)

def retrieve_chunks(question, k = 4):
    question_embedding = embedder.encode([question]).tolist()
    results = collection.query(query_embeddings=question_embedding, n_results=k)
    chunks = []
    for doc, meta, dist in zip(results['documents'][0], results['metadatas'][0], results['distances'][0]):
        chunks.append({"text": doc, "metadata": meta, "distance": dist})

    return chunks


def build_prompt(question, chunks):
    context_blocks = []
    for chunk in chunks:
        source = chunk["metadata"]["course_doc"]
        text = chunk["text"]
        context_blocks.append(f"Source: {source}\nContent: {text}")

    context_text = "\n---\n".join(context_blocks)

    prompt = """You are a helpful course assistant. Answer the student's question using ONLY the information in the context below. Do not use any outside knowledge.

    Rules:
    - If the context does not contain enough information to answer, respond exactly with: "I don't have that information in my course materials."
    - Always mention which source document(s) you used to answer, in this format: (Source: filename)
    - Be concise and direct.

    Context:
    {context_text}

    Question: {question}

    Answer:"""

    return prompt

def generate_answer(prompt):
    response = llm_client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=500,
        messages=[{"role": "user", "content": prompt}]
    )
    return response.content[0].text

def ask(question):
    chunks = retrieve_chunks(question)
    prompt = build_prompt(question, chunks)
    answer = generate_answer(prompt)

    return answer

if __name__ == "__main__":
    while True:
        q = input("\nAsk something or quit(q): ")
        if q.lower() == 'q':
            break
        else: 
            print("\n" + ask(q))
