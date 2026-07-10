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
    interests: str  
    budget_inr: int      
    num_people: int
    itinerary: Annotated[str, operator.add]

# 2. LLM Setup
llm = ChatGroq(model="llama-3.3-70b-versatile", api_key=GROQ_API_KEY)

# 3. Agent (Activity Planner)
def activity_planner(state: TravelState):
    prompt = f"""
    You are an expert AI Travel Planner. Your goal is to create a highly personalized trip itinerary.

    INPUT PARAMETERS:
    - Destination: {state['location']}
    - Duration: {state['days']} Days
    - Interests: {state['interests']}
    - Total Budget: {state['budget_inr']} INR
    - Number of People: {state['num_people']}

    RULES:
    1. STRICTLY focus ONLY on the destination: {state['location']}.
    2. The itinerary MUST be exactly {state['days']} days long.
    3. The budget breakdown MUST align with {state['budget_inr']} INR for {state['num_people']} people.
    4. Provide a brief 'About' section first.
    5.Include current weather for {state['location']} at the start of the 'About the Destination' section. Format: 'Current Weather: [Temp]°C [Emoji]'.

    OUTPUT FORMAT:
    - 🌍 About the Destination: [2-3 sentences]
    - 📅 Itinerary: [Day-by-day plan]
    - 💰 Budget Breakdown: [Breakdown details]
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

def run_travel_agent(location, days, interests, budget_inr, num_people): 
    thread_id = f"user_{uuid.uuid4().hex}"
    config = {"configurable": {"thread_id": thread_id}}

    initial_state = {
        "location": location,
        "days": days,
        "interests": interests,
        "budget_inr": budget_inr,    
        "num_people": num_people,    
        "itinerary": ""
    }

    result = app.invoke(initial_state, config=config)
    return result["itinerary"]
