from typing import TypedDict, Annotated, List
import os
from dotenv import load_dotenv

from langgraph.prebuilt import ToolNode
from langgraph.graph import StateGraph, START, END


load_dotenv()

from langgraph.checkpoint.memory import MemorySaver

from langchain_core.messages import (
    AnyMessage,
    HumanMessage,
    AIMessage,
    SystemMessage,
)

"""def get_database_url():
    database_url = os.getenv("DATABASE_URL")

    if not database_url:
        raise ValueError(
            "DATABASE_URL is missing. Please add your Render PostgreSQL External Database URL to .env"
        )

    if "sslmode=" not in database_url:
        separator = "&" if "?" in database_url else "?"
        database_url = f"{database_url}{separator}sslmode=require"

    return database_url"""

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
import operator
from langchain_groq import ChatGroq
from langgraph.graph import StateGraph, END

# 1. State Define karein 
class TravelState(TypedDict):
    location: str
    days: int
    interests: str  # User interest (e.g., "Adventure, Food")
    itinerary: Annotated[str, operator.add]

# 2. LLM Setup
llm = ChatGroq(model="llama-3.3-70b-versatile", api_key=GROQ_API_KEY)

# 3. Agent (Activity Planner)
def activity_planner(state: TravelState):
    prompt = f"""
    You are a professional travel planner. 
    1. FIRST, provide a detailed 'About' section (2-3 sentences) about {state['location']}. 
   Cover its vibe, culture, and key highlights.
   2. THEN, provide a day-by-day itinerary for {state['days']} days based on {state['interests']}.
   Format each day as 'Day 1', 'Day 2', etc.
   """
    response = llm.invoke(prompt)
    return {"itinerary": response.content}

# 4. Workflow
workflow = StateGraph(TravelState)
workflow.add_node("planner", activity_planner)
workflow.set_entry_point("planner")
workflow.add_edge("planner", END)



#DATABASE_URL = get_database_url()
def get_checkpointer():
    
    checkpointer = MemorySaver()
    return checkpointer


checkpointer = get_checkpointer()
app = workflow.compile(checkpointer=checkpointer)
# 5. Function to run in Streamlit
import uuid

def run_travel_agent(location, days, interests):
    config = {"configurable": {"thread_id": "unique_thread_id"}} # Ya unique ID use karein
    initial_state = {"location": location, "days": days, "interests": interests}
    result = app.invoke(initial_state, config=config)
    return result["itinerary"]
