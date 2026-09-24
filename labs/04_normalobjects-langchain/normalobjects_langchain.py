import os
import random
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage
from langgraph.prebuilt import create_react_agent
from typing import Dict

load_dotenv()

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)

@tool
def consult_demogorgon(complaint: str) -> str:
    """Get the Demogorgon's perspective on a complaint about the Upside Down.
    
    Args:
        complaint: The complaint about the Upside Down
    Returns:
        The Demogorgon's perspective (creative and possibly chaotic)
    """
    responses = [
        f"The Demogorgon tilts its head. It seems confused by '{complaint}'. Perhaps the issue is that you're thinking in three dimensions?",
        f"The Demogorgon makes a sound that might be agreement. Things work differently in the Upside Down's time.",
        f"The Demogorgon appears to be eating something. Maybe consistency isn't a priority there?"
    ]
    return random.choice(responses)

@tool
def check_hawkins_records(query: str) -> str:
    """Search Hawkins historical records for information.
    
    Args:
        query: What to search for in the records
    Returns:
        Information from Hawkins historical records
    """
    records = {
        "portal": "Records show portals have opened on various dates with no clear pattern. Weather, electromagnetic activity, and unknown factors seem involved.",
        "monsters": "Historical records indicate creatures from the Upside Down behave differently based on environmental factors and time of day.",
        "psychics": "Records show that psychic abilities vary greatly. Some individuals can move objects but not see the future.",
        "electricity": "Hawkins has a history of electrical anomalies connected to the Upside Down and electromagnetic fields."
    }
    for key, value in records.items():
        if key in query.lower():
            return value
    return f"Records don't contain specific information about '{query}', but many unexplained events have occurred in Hawkins."

@tool
def cast_interdimensional_spell(problem: str, creativity_level: str = "medium") -> str:
    """Suggest a creative interdimensional spell to fix a problem.
    
    Args:
        problem: The problem to solve
        creativity_level: How creative to be (low, medium, high)
    Returns:
        A creative spell or solution suggestion
    """
    creativity_multiplier = {"low": 1, "medium": 2, "high": 3}[creativity_level]
    spells = [
        f"Try chanting 'Becma Becma Becma' three times while holding a Walkman. This might recalibrate the interdimensional frequencies related to: {problem}",
        f"Create a salt circle and place a compass in the center. The magnetic anomalies might help stabilize: {problem}",
        f"Play 'Running Up That Hill' backwards at the exact location of the issue. The temporal resonance could fix: {problem}",
        f"Gather three items: a lighter, a compass, and something personal. Arrange them in a triangle while thinking about: {problem}.",
    ]
    selected = random.sample(spells, min(creativity_multiplier, len(spells)))
    return "\n".join(selected)

@tool
def gather_party_wisdom(question: str) -> str:
    """Ask the D&D party (Mike, Dustin, Lucas, Will) for their collective wisdom.
    
    Args:
        question: The question or problem to ask the party about
    Returns:
        The party's collective wisdom and suggestions
    """
    party_responses = {
        "portal": "Mike: 'Portals usually open near strong emotional events.' Dustin: 'They follow patterns related to the Mind Flayer's activity.'",
        "monsters": "Lucas: 'Demogorgons are territorial but opportunistic.' Will: 'They sense fear and strong emotions.'",
        "psychics": "Mike: 'El's powers are connected to her emotional state.' Dustin: 'Limited by her physical and mental energy.'",
        "electricity": "Lucas: 'The Upside Down interferes with electrical systems.' Dustin: 'It creates strange connections, like a feedback loop.'"
    }
    for key, response in party_responses.items():
        if key in question.lower():
            return response
    return "The party huddles. Mike: 'This is tough.' Dustin: 'We need more info.' Lucas: 'Let's think.' Will: 'Maybe consult other sources?'"

tools = [
    consult_demogorgon,
    check_hawkins_records,
    cast_interdimensional_spell,
    gather_party_wisdom
]

print(f"Created {len(tools)} creative tools:")
for t in tools:
    print(f"  - {t.name}: {t.description[:60]}...")

system_prompt = """You are Becma, the creative AI agent of the Downside-Up Complaint Bureau.
Your job is to handle complaints about the Normal Objects universe creatively.

You have access to these tools:
- consult_demogorgon: Get the Demogorgon's perspective
- check_hawkins_records: Search historical records
- cast_interdimensional_spell: Suggest creative magical solutions
- gather_party_wisdom: Ask the D&D party for advice

Always use at least 2 different tools when handling a complaint.
Be entertaining, imaginative, and thorough!"""

agent_executor = create_react_agent(llm, tools, prompt=system_prompt)

print("\nAgent created successfully!")

complaints = [
    "Why do demogorgons sometimes eat people and sometimes don't?",
    "The portal opens on different days—is there a schedule?",
    "Why can some psychics see the Upside Down and others can't?",
    "Why do creatures and power lines react so strangely together?",
]

def handle_complaint(complaint: str) -> str:
    print(f"\n{'='*60}")
    print(f"COMPLAINT: {complaint}")
    print(f"{'='*60}\n")
    result = agent_executor.invoke({"messages": [HumanMessage(content=complaint)]})
    final_response = result["messages"][-1].content
    return final_response

print("\nTesting agent with sample complaints...\n")
responses = []
for complaint in complaints[:3]:
    response = handle_complaint(complaint)
    responses.append(response)
    print(f"\nRESPONSE: {response}\n")

class ToolUsageTracker:
    def __init__(self):
        self.usage_count = {t.name: 0 for t in tools}
        self.tool_sequences = []
    
    def track_usage(self, tool_name: str):
        if tool_name in self.usage_count:
            self.usage_count[tool_name] += 1
            self.tool_sequences.append(tool_name)
    
    def get_statistics(self) -> Dict:
        return {
            "total_tool_calls": sum(self.usage_count.values()),
            "tool_counts": self.usage_count,
            "most_used": max(self.usage_count.items(), key=lambda x: x[1])[0] if self.usage_count else None,
            "tool_sequences": self.tool_sequences
        }

tracker = ToolUsageTracker()

for complaint_response in responses:
    if "demogorgon" in complaint_response.lower():
        tracker.track_usage("consult_demogorgon")
    if "record" in complaint_response.lower() or "hawkins" in complaint_response.lower():
        tracker.track_usage("check_hawkins_records")
    if "spell" in complaint_response.lower() or "chant" in complaint_response.lower():
        tracker.track_usage("cast_interdimensional_spell")
    if "mike" in complaint_response.lower() or "dustin" in complaint_response.lower():
        tracker.track_usage("gather_party_wisdom")

print("\n=== Tool Usage Analysis ===")
stats = tracker.get_statistics()
print(f"Total tool calls: {stats['total_tool_calls']}")
print(f"Tool usage counts: {stats['tool_counts']}")
print(f"Most used tool: {stats['most_used']}")
print(f"\nTool sequence examples:")
for i in range(min(3, len(stats['tool_sequences']))):
    print(f"  Sequence {i+1}: {' -> '.join(stats['tool_sequences'][i:i+3])}")

print("\n=== Agent Demo Complete! ===")