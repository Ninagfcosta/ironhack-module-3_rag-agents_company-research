from dotenv import load_dotenv
load_dotenv()

from langgraph.prebuilt import create_react_agent
from langchain_openai import ChatOpenAI
from tools import web_search, get_news, get_financial_data

llm = ChatOpenAI(model="gpt-4o-mini")

agent = create_react_agent(llm, tools=[web_search, get_news, get_financial_data])