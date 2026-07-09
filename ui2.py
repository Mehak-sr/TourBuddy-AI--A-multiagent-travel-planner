import streamlit as st
from backend2 import run_travel_agent

# Page Config
st.set_page_config(page_title="TourBuddy AI", page_icon="🌍", layout="wide")

# Custom CSS for Professional Look
st.markdown("""
    <style>
    .main {background-color: #f5f7f9;}
    .stButton>button {width: 100%; border-radius: 5px; height: 3em; background-color: #007BFF; color: white;}
    .css-1544g2n {padding: 2rem;}
    </style>
    """, unsafe_allow_html=True)

# Sidebar UI
st.sidebar.title("🌍 TourBuddy Settings")
location = st.sidebar.text_input("Destination City", placeholder="e.g., Dubai")
days = st.sidebar.slider("Number of Days", 1, 10, 3)
interests = st.sidebar.multiselect("Select Interests", 
    ["Adventure", "Food", "History", "Nature", "Luxury", "Budget"])

st.title("✨ Your AI Travel Assistant")
st.write("Plan your perfect trip with AI-powered customization.")

if st.sidebar.button("Generate Itinerary"):
    if not location:
        st.sidebar.error("Please enter a destination!")
    else:
        with st.spinner("Crafting your perfect trip..."):
            itinerary = run_travel_agent(location, days, ", ".join(interests))

            if itinerary:
                st.balloons()
            
            # Professional Display using Expanders
            st.success("Itinerary Generated Successfully!")
            st.markdown("---")
            
            # Splitting output by Day (Assumes LLM provides it day-wise)
            days_list = itinerary.split("Day")
            for i, day_content in enumerate(days_list):
                if day_content.strip():
                    with st.expander(f"🗓️ Day {i}", expanded=(i==1)):
                        st.write(day_content)

st.sidebar.info("Built with LangGraph & Groq AI")