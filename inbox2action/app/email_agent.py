from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph
from typing import TypedDict
import json
from inbox2action.app.google_calendar_service import create_calendar_event

llm = ChatOpenAI(model="gpt-4o")

class EmailState(TypedDict):
    email_text: str
    summary: str
    action_items: dict
    event_id: str

def summarize_email(state: EmailState):
    state["summary"] = llm.predict(f"Summarize this email: {state['email_text']}")
    return state

def extract_actions(state: EmailState):
    response = llm.predict(
        f"Extract actionable items in JSON format for a calendar event:\n\n{state['email_text']}"
    )
    try:
        state["action_items"] = json.loads(response)
    except:
        state["action_items"] = {"title": "Unknown", "date": None, "time": None}
    return state

def create_event(state: EmailState):
    state["event_id"] = create_calendar_event(state["action_items"])
    return state

workflow = StateGraph(EmailState)
workflow.add_node("summarize", summarize_email)
workflow.add_node("extract", extract_actions)
workflow.add_node("calendar", create_event)

workflow.add_edge("summarize", "extract")
workflow.add_edge("extract", "calendar")
workflow.set_entry_point("summarize")
workflow.set_finish_point("calendar")

agent = workflow.compile()

def process_email_agent(email_text: str):
    state = {"email_text": email_text}
    result = agent.invoke(state)
    return result
