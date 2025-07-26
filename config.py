import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# API Keys (you need to set these in your .env file)
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
SERPER_API_KEY = os.getenv("SERPER_API_KEY")  # Optional: for enhanced search
DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")  # For Discord alerts

# Debug prints (remove these after testing)
print(f"🔑 Groq API Key loaded: {'✅ Yes' if GROQ_API_KEY else '❌ No'}")
print(f"🔑 Serper API Key loaded: {'✅ Yes' if SERPER_API_KEY else '❌ No'}")  
print(f"🔑 Discord Webhook loaded: {'✅ Yes' if DISCORD_WEBHOOK_URL else '❌ No'}")

# Disaster keywords to search for
DISASTER_KEYWORDS = [
    "earthquake", "flood", "hurricane", "tornado", "wildfire", 
    "tsunami", "cyclone", "landslide", "emergency", "disaster",
    "evacuation", "rescue", "relief", "aid"
]

# News API endpoint (using free Serper API)
NEWS_API_URL = "https://google.serper.dev/news"