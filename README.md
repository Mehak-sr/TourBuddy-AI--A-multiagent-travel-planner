🚀 TourBuddy: AI-Powered Personalized Travel Planner
TourBuddy is an intelligent, agent-based travel itinerary generator that creates highly customized, day-by-day travel plans. Unlike static search engines, TourBuddy uses LLMs and state-graph orchestration to tailor recommendations based on specific user interests like adventure, culinary experiences, or historical exploration.

🛠️ Tech Stack
Core Language: Python

AI Orchestration: LangGraph, LangChain

LLM Engine: Llama-3.3-70b (via Groq API)

Frontend: Streamlit

State Management: PostgreSQL

Deployment: Streamlit Cloud

✨ Key Features
Smart AI Itinerary Generation: Powered by multi-agent travel planning to create personalized travel schedules.

Real-time Weather Updates: Fetches live weather information for your chosen destination so you can plan your day accordingly.

Dynamic Budget Breakdown: Provides a clear estimation of your trip expenses to help you manage your finances efficiently.

Seamless Export: Easily download your customized travel itinerary as a text file for offline access.

🚀 How to Run Locally
1. Clone the repository:

Bash
'''git clone https://github.com/Mehak-sr/TourBuddy-AI--A-multiagent-travel-planner.git
cd TourBuddy-AI--A-multiagent-travel-planner'''

2. Install dependencies:

Bash
'''pip install -r requirements.txt'''

3. Set up Environment Variables:
Create a .env file in the project root and add your Groq API Key:

Plaintext
'''GROQ_API_KEY=your_groq_api_key_here'''

4. Run the application:

Bash
'''streamlit run ui2.py'''

📈 Deployment
This project is deployed on Streamlit Cloud for global accessibility.
[https://tourbuddy-ai--a-multiagent-travel-planner-maihgwapplngk62wc8gp.streamlit.app/]
