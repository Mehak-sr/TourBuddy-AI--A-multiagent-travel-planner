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
budget_inr = st.sidebar.number_input(
                "Total Budget (in INR)", 
                min_value=5000, 
                max_value=1000000, 
                value=50000, 
                step=1000
                )
num_people = st.sidebar.number_input("Number of People", min_value=1, value=1)

st.title("✨ Your AI Travel Assistant")
st.write("Plan your perfect trip with AI-powered customization.")

if st.sidebar.button("Generate Itinerary"):
    if not location:
        st.sidebar.error("Please enter a destination!")
    else:
        with st.spinner("Crafting your perfect trip..."):
            itinerary = run_travel_agent(location, days, interests, budget_inr, num_people)
            st.session_state['itinerary'] = itinerary

            if itinerary:
                
                st.download_button(
                    label="📥 Download Itinerary as Text File",
                    data=itinerary,
                    file_name="My_Travel_Plan.txt",
                    mime="text/plain"
                )
            
            # Professional Display using Expanders
            st.success("Itinerary Generated Successfully!")
            st.markdown("---")
            
            sections = itinerary.split("Day")
            st.subheader("🌍 About the Destination")
            raw_text = sections[0].replace("**", "")
            
            
            if "Current Weather:" in raw_text:
                 weather_info = raw_text.split("Current Weather:")[1].split("\n")[0]
                 st.success(f"☀️ Current Weather: {weather_info}")
                 
                 clean_about = raw_text.split("Current Weather:")[0].replace("About the Destination:", "").strip()
            else:
                 clean_about = raw_text.replace("About the Destination:", "").strip()
            
            st.write(clean_about)
            
            
            st.subheader("📅 Your Itinerary")
            for i in range(1, len(sections)):
                if i <= days:
                    content=sections[i].replace("**", "").replace("Day", "")
                    if "Budget Breakdown" in content:
                        content = content.split("Budget Breakdown")[0]
                    with st.expander(f"📅 Day {i}"):
                        st.write(content)
            st.markdown("---")
            st.subheader("Estimated Budget Breakdown")
            st.write(f"**Total People:** {num_people}")
            st.write(f"**Total Budget Set:** ₹{budget_inr}")
            st.write("---")
            st.info("Check the details below for your trip's cost breakdown:")
            st.write(itinerary.split("Budget Breakdown")[-1] if "Budget Breakdown" in itinerary else "AI is calculating your detailed breakdown...")

            sections = itinerary.split("Day")


            st.subheader("🌍 About the Destination")
            st.write(sections[0].replace("**", "")) 


            st.subheader("📅 Your Itinerary")
            for i in range(1, len(sections)):
                if i <= days: # Sirf utne din jitne user ne select kiye
                    with st.expander(f"📅 Day {i}"):
                         st.write(sections[i].replace("**", ""))

st.sidebar.info("Built with LangGraph & Groq AI")
