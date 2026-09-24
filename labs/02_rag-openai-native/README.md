# RAG with OpenAI - Native Implementation

## Description
A complete RAG (Retrieval-Augmented Generation) pipeline built using OpenAI's native APIs.

## How to Run

### 1. Install dependencies
pip install openai numpy python-dotenv pypdf2 tiktoken

### 2. Set up environment variables
Create a `.env` file in the root folder:
OPENAI_API_KEY=your-api-key-here

### 3. Run the pipeline
python rag_openai_native.py

## Project Structure
- `rag_openai_native.py` — Main RAG pipeline
- `.env` — API keys (never share this file!)
- `.gitignore` — Protects sensitive files from GitHub
- `lab_summary.md` — Lab design choices

## Pipeline Steps
1. **Chunking** — Splits documents into smaller pieces
2. **Embeddings** — Converts text into vectors using OpenAI
3. **Vector Search** — Finds the most relevant chunks using cosine similarity
4. **RAG Query** — Generates answers using GPT-4o-mini with retrieved context