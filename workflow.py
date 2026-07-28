from typing import TypedDict
from langgraph.graph import StateGraph, END
from agent import agent

class AgentState(TypedDict):
    company: str
    research_data: str
    report: str

def research_node(state: AgentState):
    result = agent.invoke({"messages": [("user", f"Research the company {state['company']}")]})
    last_message = result["messages"][-1]
    state["research_data"] = last_message.content
    return state

def report_node(state: AgentState):
    state["report"] = f"Report for {state['company']}:\n{state['research_data']}"
    return state

workflow = StateGraph(AgentState)
workflow.add_node("research", research_node)
workflow.add_node("report", report_node)
workflow.set_entry_point("research")
workflow.add_edge("research", "report")
workflow.add_edge("report", END)

app = workflow.compile()