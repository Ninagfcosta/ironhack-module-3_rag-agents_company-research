# NormalObjects - Creative Complaint Handler (LangChain)

## Description
A creative AI agent that handles complaints about the Normal Objects universe using LangChain's tool-calling framework. The agent uses tools creatively to provide entertaining solutions.

## How to Run

### 1. Install dependencies
pip install langchain langchain-openai langgraph python-dotenv

### 2. Create a .env file with your API key
OPENAI_API_KEY=your-key-here

### 3. Run the script
python normalobjects_langchain.py

## Files
- `normalobjects_langchain.py` - Main agent code with all tools
- `lab_summary.md` - Lab summary and analysis
- `.gitignore` - Hides the .env file from GitHub

## Tools Created
- consult_demogorgon - Gets the Demogorgon's perspective
- check_hawkins_records - Searches Hawkins historical records
- cast_interdimensional_spell - Suggests creative magical solutions
- gather_party_wisdom - Asks the D&D party for advice