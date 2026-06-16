import os
import datetime
from typing import TypedDict, List
from dotenv import load_dotenv
from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage

load_dotenv()

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

# ──────────────────────────────────────────
# STATE
# ──────────────────────────────────────────
class ComplaintState(TypedDict):
    complaint: str
    category: str
    is_valid: bool
    investigation: str
    resolution: str
    effectiveness: str
    status: str
    workflow_path: List[str]
    rejection_reason: str


# ──────────────────────────────────────────
# NODE 1 — INTAKE
# ──────────────────────────────────────────
def intake_node(state: ComplaintState) -> ComplaintState:
    """Step 1: Intake - Parse and categorize the complaint"""
    print("\n[INTAKE] Processing complaint...")

    complaint = state["complaint"]

    categorization_prompt = f"""Categorize this Downside Up complaint into one of these categories:
- portal: Issues with portal timing, location, or behavior
- monster: Issues with creature behavior (demogorgons, etc.)
- psychic: Issues with psychic abilities or limitations
- environmental: Issues with electricity, weather, or physical environment
- other: Anything else

Complaint: {complaint}

Respond with ONLY the category name (portal, monster, psychic, environmental, or other)."""

    response = llm.invoke([HumanMessage(content=categorization_prompt)])
    category = response.content.strip().lower()

    new_state = {
        **state,
        "category": category,
        "workflow_path": state.get("workflow_path", []) + ["intake"],
        "status": "intake"
    }

    print(f"[INTAKE] Categorized as: {category}")
    return new_state


# ──────────────────────────────────────────
# NODE 2 — VALIDATE
# ──────────────────────────────────────────
def validate_node(state: ComplaintState) -> ComplaintState:
    """Step 2: Validate - Check if complaint meets the rules"""
    print("\n[VALIDATE] Validating complaint...")

    complaint = state["complaint"]
    category = state["category"]

    validation_prompt = f"""You are validating a Downside Up complaint.

Category: {category}
Complaint: {complaint}

Validation rules:
- portal: must reference specific location or timing anomalies
- monster: must describe creature behavior or interactions
- psychic: must reference specific ability limitations or malfunctions
- environmental: must have connection to electricity, weather, or observable phenomena
- other: ALWAYS mark as INVALID for automatic escalation

Does this complaint meet the validation rules for its category?
Respond with ONLY: VALID or INVALID, then a pipe | then a brief reason.
Example: VALID | References specific portal timing anomaly"""

    response = llm.invoke([HumanMessage(content=validation_prompt)])
    result = response.content.strip()

    is_valid = result.startswith("VALID")
    reason = result.split("|")[1].strip() if "|" in result else result

    new_state = {
        **state,
        "is_valid": is_valid,
        "rejection_reason": "" if is_valid else reason,
        "workflow_path": state.get("workflow_path", []) + ["validate"],
        "status": "validate"
    }

    print(f"[VALIDATE] Valid: {is_valid} | Reason: {reason}")
    return new_state


# ──────────────────────────────────────────
# NODE 3 — INVESTIGATE
# ──────────────────────────────────────────
def investigate_node(state: ComplaintState) -> ComplaintState:
    """Step 3: Investigate - Gather evidence and document findings"""
    print("\n[INVESTIGATE] Investigating...")

    complaint = state["complaint"]
    category = state["category"]

    investigation_prompt = f"""You are an investigator at the Downside Up Complaint Bureau.

Complaint category: {category}
Complaint: {complaint}

Investigation rules for {category}:
- portal: investigate temporal patterns, location consistency, environmental factors
- monster: gather behavioral data, interaction patterns, environmental triggers
- psychic: document ability specifications, tested limitations, contextual factors
- environmental: analyze power line activity, atmospheric conditions, anomaly correlation

Provide a documented investigation report (2-3 sentences) with specific findings and evidence."""

    response = llm.invoke([HumanMessage(content=investigation_prompt)])

    new_state = {
        **state,
        "investigation": response.content.strip(),
        "workflow_path": state.get("workflow_path", []) + ["investigate"],
        "status": "investigate"
    }

    print(f"[INVESTIGATE] Report: {response.content.strip()[:80]}...")
    return new_state


# ──────────────────────────────────────────
# NODE 4 — RESOLVE
# ──────────────────────────────────────────
def resolve_node(state: ComplaintState) -> ComplaintState:
    """Step 4: Resolve - Apply a specific resolution"""
    print("\n[RESOLVE] Creating resolution...")

    resolution_prompt = f"""You are resolving a Downside Up complaint using Bloyce's Protocol.

Category: {state['category']}
Complaint: {state['complaint']}
Investigation findings: {state['investigation']}

Resolution rules:
- Must be specific to the complaint type
- Must reference established Downside Up procedures or protocols
- Environmental or monster complaints may require escalation to specialized teams
- Must include a predicted effectiveness rating: high, medium, or low

Provide:
1. A specific resolution (2-3 sentences)
2. Effectiveness rating on its own line starting with EFFECTIVENESS:

Example format:
Apply Protocol Delta-7 to monitor portal timing. Coordinate with the Portal Division.
EFFECTIVENESS: high"""

    response = llm.invoke([HumanMessage(content=resolution_prompt)])
    content = response.content.strip()

    effectiveness = "medium"
    resolution_text = content
    for line in content.split("\n"):
        if line.strip().startswith("EFFECTIVENESS:"):
            effectiveness = line.replace("EFFECTIVENESS:", "").strip().lower()
            resolution_text = content.replace(line, "").strip()
            break

    new_state = {
        **state,
        "resolution": resolution_text,
        "effectiveness": effectiveness,
        "workflow_path": state.get("workflow_path", []) + ["resolve"],
        "status": "resolve"
    }

    print(f"[RESOLVE] Effectiveness: {effectiveness}")
    return new_state


# ──────────────────────────────────────────
# NODE 5 — CLOSE
# ──────────────────────────────────────────
def close_node(state: ComplaintState) -> ComplaintState:
    """Step 5: Close - Confirm resolution, log everything"""
    print("\n[CLOSE] Closing complaint...")

    timestamp = datetime.datetime.now().isoformat()
    follow_up = " [30-DAY FOLLOW-UP REQUIRED]" if state.get("effectiveness") == "low" else ""

    closure_log = (
        f"CLOSED | Category: {state['category']} | "
        f"Resolution: Applied | Outcome: Resolved | "
        f"Timestamp: {timestamp}{follow_up}"
    )

    new_state = {
        **state,
        "workflow_path": state.get("workflow_path", []) + ["close"],
        "status": "closed",
        "resolution": state.get("resolution", "") + f"\n\n[CLOSURE LOG] {closure_log}"
    }

    print(f"[CLOSE] {closure_log}")
    return new_state


# ──────────────────────────────────────────
# NODE — REJECT
# ──────────────────────────────────────────
def reject_node(state: ComplaintState) -> ComplaintState:
    """Rejection node - For invalid or insufficient complaints"""
    print("\n[REJECT] Complaint rejected...")

    timestamp = datetime.datetime.now().isoformat()

    new_state = {
        **state,
        "workflow_path": state.get("workflow_path", []) + ["reject"],
        "status": "rejected",
        "resolution": f"REJECTED: {state.get('rejection_reason', 'Insufficient detail')} | Timestamp: {timestamp}"
    }

    print(f"[REJECT] Reason: {state.get('rejection_reason')}")
    return new_state


# ──────────────────────────────────────────
# ROUTING FUNCTION
# ──────────────────────────────────────────
def routing_function(state: ComplaintState) -> str:
    if state.get("is_valid"):
        return "investigate"
    else:
        return "reject"


# ──────────────────────────────────────────
# BUILD THE GRAPH
# ──────────────────────────────────────────
workflow = StateGraph(ComplaintState)

workflow.add_node("intake", intake_node)
workflow.add_node("validate", validate_node)
workflow.add_node("investigate", investigate_node)
workflow.add_node("resolve", resolve_node)
workflow.add_node("close", close_node)
workflow.add_node("reject", reject_node)

workflow.set_entry_point("intake")

workflow.add_edge("intake", "validate")

workflow.add_conditional_edges(
    "validate",
    routing_function,
    {
        "investigate": "investigate",
        "reject": "reject"
    }
)

workflow.add_edge("investigate", "resolve")
workflow.add_edge("resolve", "close")
workflow.add_edge("close", END)
workflow.add_edge("reject", END)

app = workflow.compile()


# ──────────────────────────────────────────
# VISUALIZE WORKFLOW PATH
# ──────────────────────────────────────────
def visualize_workflow_path(result: dict, complaint_num: int):
    print(f"\n{'='*60}")
    print(f"COMPLAINT #{complaint_num} WORKFLOW SUMMARY")
    print(f"{'='*60}")
    print(f"Complaint  : {result.get('complaint', '')[:70]}...")
    print(f"Category   : {result.get('category', 'N/A')}")
    print(f"Status     : {result.get('status', 'N/A')}")
    path = result.get("workflow_path", [])
    print(f"Path       : {' → '.join(path)}")
    if result.get("effectiveness"):
        print(f"Effectiveness: {result.get('effectiveness')}")
    print(f"Resolution :\n{result.get('resolution', 'N/A')}")
    print(f"{'='*60}\n")


# ──────────────────────────────────────────
# TEST COMPLAINTS
# ──────────────────────────────────────────
test_complaints = [
    "The Downside Up portal opens at different times each day. How do I predict when?",
    "Demogorgons sometimes work together and sometimes fight. What's their deal?",
    "El can move things with her mind but can't lift heavy rocks. Why?",
    "Why do creatures and power lines react so strangely together?",
    "This is not a valid complaint about something random"
]

print("\nTesting workflow with sample complaints...\n")

for i, complaint in enumerate(test_complaints, 1):
    print(f"\n{'#'*60}")
    print(f"PROCESSING COMPLAINT #{i}")
    print(f"{'#'*60}")

    initial_state = {
        "complaint": complaint,
        "category": "",
        "is_valid": False,
        "investigation": "",
        "resolution": "",
        "effectiveness": "",
        "status": "pending",
        "workflow_path": [],
        "rejection_reason": ""
    }

    result = app.invoke(initial_state)
    visualize_workflow_path(result, i)