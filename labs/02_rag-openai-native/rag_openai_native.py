import os
import numpy as np
from openai import OpenAI
from dotenv import load_dotenv
from typing import List

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def chunk_text(text: str, chunk_size: int = 500, overlap: int = 50) -> List[str]:
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start += chunk_size - overlap
    return chunks


def get_embeddings_batch(texts: List[str], model: str = "text-embedding-3-small", batch_size: int = 100) -> List[List[float]]:
    all_embeddings = []
    for i in range(0, len(texts), batch_size):
        batch = texts[i:i + batch_size]
        response = client.embeddings.create(model=model, input=batch)
        batch_embeddings = [item.embedding for item in response.data]
        all_embeddings.extend(batch_embeddings)
        print(f"Processed {min(i + batch_size, len(texts))}/{len(texts)} chunks")
    return all_embeddings


def cosine_similarity(vec1: List[float], vec2: List[float]) -> float:
    v1 = np.array(vec1)
    v2 = np.array(vec2)
    return np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))


def search_similar_chunks(query: str, chunks: List[str], chunk_embeddings: List[List[float]], top_k: int = 3) -> List[str]:
    query_embedding = client.embeddings.create(
        model="text-embedding-3-small",
        input=query
    ).data[0].embedding
    similarities = [cosine_similarity(query_embedding, emb) for emb in chunk_embeddings]
    top_indices = np.argsort(similarities)[-top_k:][::-1]
    return [chunks[i] for i in top_indices]


def rag_query(question: str, chunks: List[str], chunk_embeddings: List[List[float]]) -> str:
    relevant_chunks = search_similar_chunks(question, chunks, chunk_embeddings)
    context = "\n\n".join([f"Source {i+1}:\n{chunk}" for i, chunk in enumerate(relevant_chunks)])
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant. Answer questions based only on the provided context. Always cite which source you used (Source 1, Source 2, etc)."
            },
            {
                "role": "user",
                "content": f"Context:\n{context}\n\nQuestion: {question}"
            }
        ]
    )
    return response.choices[0].message.content


if __name__ == "__main__":

    sample_document = """
    Artificial intelligence (AI) is intelligence demonstrated by machines.
    Machine learning is a subset of AI that learns from data automatically.
    Deep learning uses neural networks with many layers to learn complex patterns.
    Natural language processing (NLP) helps computers understand human language.
    Large language models like GPT are trained on massive amounts of text data.
    RAG stands for Retrieval-Augmented Generation. It combines search with AI generation.
    Embeddings are numerical representations of text that capture semantic meaning.
    Vector databases store embeddings and allow fast similarity search.
    OpenAI provides APIs for embeddings and chat completions.
    The cosine similarity measures how similar two vectors are in direction.
    """

    print("Step 1: Chunking document...")
    chunks = chunk_text(sample_document, chunk_size=200, overlap=30)
    print(f"Created {len(chunks)} chunks\n")

    print("Step 2: Generating embeddings...")
    embeddings = get_embeddings_batch(chunks)
    print(f"Generated {len(embeddings)} embeddings\n")

    print("Step 3 & 4: Running RAG queries...\n")
    questions = [
        "What is RAG and how does it work?",
        "What are embeddings?",
        "How does machine learning relate to AI?"
    ]

    for question in questions:
        print(f"Question: {question}")
        answer = rag_query(question, chunks, embeddings)
        print(f"Answer: {answer}")
        print("-" * 50)