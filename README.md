# Relevance Scoring and Rerankers Lab

## How to Run

### 1. Install dependencies
pip install openai numpy python-dotenv cohere sentence-transformers pypdf2 tiktoken jupyter

### 2. Set up environment variables
Create a `.env` file:
OPENAI_API_KEY=your-openai-key
COHERE_API_KEY=your-cohere-key

### 3. Run the notebook
jupyter notebook relevance_scoring_rerankers.ipynb

## Project Structure
- `relevance_scoring_rerankers.ipynb` — Main notebook with full implementation
- `.env` — API keys (never share this!)
- `.gitignore` — Protects sensitive files
- `lab_summary.md` — Design choices summary

## Pipeline
1. Load documents with metadata
2. Chunk and generate embeddings
3. Basic vector search (baseline)
4. Rerank with Cohere
5. Compare results before/after reranking