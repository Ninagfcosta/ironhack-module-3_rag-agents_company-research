import os
import requests
from langchain.tools import tool
from tavily import TavilyClient

tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

@tool
def web_search(query: str) -> str:
    """Searches the web for general company information."""
    results = tavily.search(query=query, max_results=3)
    return str(results)

@tool
def get_news(company: str) -> str:
    """Fetches recent news about a company."""
    url = f"https://newsapi.org/v2/everything?q={company}&apiKey={os.getenv('NEWSAPI_KEY')}"
    response = requests.get(url)
    articles = response.json().get("articles", [])[:3]
    return str([a["title"] for a in articles])

@tool
def get_financial_data(symbol: str) -> str:
    """Fetches basic financial data for a stock symbol."""
    url = f"https://www.alphavantage.co/query?function=OVERVIEW&symbol={symbol}&apikey={os.getenv('ALPHAVANTAGE_KEY')}"
    response = requests.get(url)
    return str(response.json())