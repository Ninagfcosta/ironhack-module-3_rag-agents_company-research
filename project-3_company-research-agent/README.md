# Company Research Agent

An autonomous AI agent that researches companies and generates reports,
using web search, news, and financial data APIs.

## What it does
- Searches the web for company information
- Fetches recent news
- Gets financial data
- Generates a written report
- Runs automatically through N8N

## Sample reports
See the `sample_reports/` folder for example outputs (Tesla, Apple, Adidas).

## How to run
1. Activate the virtual environment: `source venv/bin/activate`
2. Copy `.env.example` to `.env` and add your own API keys
3. Run the ingestion script: `python3 ingest.py`
4. Start the API server: `python3 api.py`
5. Open N8N and trigger the workflow

## Tech Stack
- LangChain + LangGraph (ReAct agent)
- Pinecone (RAG)
- Flask (API)
- N8N (automation)