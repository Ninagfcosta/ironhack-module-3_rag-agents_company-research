# 🧩 Different Ways to Chunk Podcast and PDF

## 📌 Description
This project explores different chunking strategies for processing PDF documents and podcast transcripts using LangChain.

## 📁 Files
- `chunking_strategies.ipynb` — Main notebook with all chunking experiments
- `ethics_guidelines_for_trustworthy_ai.pdf` — PDF source document
- `The_Blueprint_For_Trustworthy_AI.m4a` — Podcast audio file

## 🔧 Setup

### 1. Install dependencies
pip install langchain langchain-community pypdf openai tiktoken python-dotenv openai-whisper

### 2. Create a .env file
OPENAI_API_KEY="your-api-key-here"

### 3. Run the notebook
Open chunking_strategies.ipynb and run all cells in order.

## ✂️ Chunking Strategies Compared

| Strategy | PDF Chunks | Podcast Chunks |
|----------|-----------|----------------|
| Fixed-Size | 174 | 19 |
| Recursive | 194 | 21 |
| Token-Based | 82 | 8 |

## ✅ Recommendations
- PDF: Recursive Character Chunking (chunk_size=1000, overlap=200)
- Podcast: Recursive Character Chunking (chunk_size=500, overlap=100)

## ⚠️ Security
Never commit your .env file! It is listed in .gitignore.
