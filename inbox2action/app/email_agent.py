from dateutil import parser
from langchain_groq import ChatGroq  # Groq client
from langgraph.graph import StateGraph
from typing import TypedDict
import json
from app.calendar_service import create_calendar_event
from app.config import GROQ_API_KEY, MODEL

# Initialize Groq LLM
llm = ChatGroq(model=MODEL, api_key=GROQ_API_KEY)


# ---- Define State ----
class EmailState(TypedDict):
    email_text: str
    summary: str
    action_items: dict
    event_id: str


# ---- Step 1: Summarize Email ----
def summarize_email(state: EmailState):
    state["summary"] = llm.invoke(
        f"Summarize this email clearly in 2-3 sentences: {state['email_text']}"
    ).content
    return state


# ---- Step 2: Extract Actions ----
from dateutil import parser  # add this import at the top of email_agent.py

def extract_actions(state: EmailState):
    response = llm.invoke(
        f"""
        Extract actionable items from the email as JSON for Google Calendar.
        Ensure datetime values are in ISO8601 format (YYYY-MM-DDTHH:MM:SS).
        Include title, description, start, and end. Only one event per email.
        Example:
        {{
          "title": "Meeting with John",
          "description": "Project discussion",
          "start": "2025-09-12T15:00:00",
          "end": "2025-09-12T16:00:00"
        }}
        
        Email: {state['email_text']}
        """
    ).content

    try:
        data = json.loads(response)

        # Parse start and end into proper ISO8601
        start_raw = data.get("start")
        end_raw = data.get("end")

        start_iso = parser.parse(start_raw).isoformat() if start_raw else None
        end_iso = parser.parse(end_raw).isoformat() if end_raw else None

        state["action_items"] = {
            "title": data.get("title", "No Title"),
            "description": data.get("description", ""),
            "start": start_iso,
            "end": end_iso,
        }

    except Exception as e:
        print("⚠️ Failed to parse LLM output:", e)
        # fallback if parsing fails
        state["action_items"] = {
            "title": "Unknown",
            "description": state.get("summary", ""),
            "start": None,
            "end": None,
        }

    return state



# ---- Step 3: Create Calendar Event ----
def create_event(state: EmailState):
    state["event_id"] = create_calendar_event(state["action_items"])
    return state


# ---- Build Workflow ----
workflow = StateGraph(EmailState)
workflow.add_node("summarize", summarize_email)
workflow.add_node("extract", extract_actions)
workflow.add_node("calendar", create_event)

workflow.add_edge("summarize", "extract")
workflow.add_edge("extract", "calendar")
workflow.set_entry_point("summarize")
workflow.set_finish_point("calendar")

agent = workflow.compile()


# ---- Public Function ----
def process_email_agent(email_text: str):
    state = {"email_text": email_text}
    result = agent.invoke(state)
    return result
