from typing import TypedDict, Annotated, List
import os
from dotenv import load_dotenv

from langgraph.prebuilt import ToolNode
from langgraph.graph import StateGraph, START, END

import psycopg
from psycopg.rows import dict_row

from langgraph.checkpoint.postgres import PostgresSaver

load_dotenv()

from langchain_core.messages import (
    AnyMessage,
    HumanMessage,
    AIMessage,
    SystemMessage,
)

def get_database_url():
    database_url = os.getenv("DATABASE_URL")

    if not database_url:
        raise ValueError(
            "DATABASE_URL is missing. Please add your Render PostgreSQL External Database URL to .env"
        )

    if "sslmode=" not in database_url:
        separator = "&" if "?" in database_url else "?"
        database_url = f"{database_url}{separator}sslmode=require"

    return database_url

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
    Create a {state['days']}-day itinerary for {state['location']}.
    Focus specifically on these interests: {state['interests']}.
    Make it detailed, engaging, and provide a day-by-day plan.
    """
    response = llm.invoke(prompt)
    return {"itinerary": response.content}

# 4. Workflow
workflow = StateGraph(TravelState)
workflow.add_node("planner", activity_planner)
workflow.set_entry_point("planner")
workflow.add_edge("planner", END)



DATABASE_URL = get_database_url()
def get_checkpointer():
    
    conn = psycopg.connect(DATABASE_URL, autocommit=True)
    checkpointer = PostgresSaver(conn)
    checkpointer.setup()
    return checkpointer


checkpointer = get_checkpointer()
app = workflow.compile(checkpointer=checkpointer)

# 5. Function to run in Streamlit
import uuid

def run_travel_agent(location, days, interests):
    thread_id = f"user_{uuid.uuid4().hex}"
    
    # Config setup
    config = {"configurable": {"thread_id": thread_id}}
    
    # Initial state
    initial_state = {
        "location": location,
        "days": days,
        "interests": interests,
        "itinerary": ""
    }
    
    result = app.invoke(initial_state, config=config)
    
    return result["itinerary"]