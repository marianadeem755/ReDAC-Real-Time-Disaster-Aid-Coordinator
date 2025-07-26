import streamlit as st
import time
from agents.news_agent import NewsAgent
from agents.alert_agent import AlertAgent
from agents.chat_agent import ChatAgent
from agents.alert_message_agent import AlertMessageAgent

# Configure Streamlit page
st.set_page_config(
    page_title="ReDAC - Real-Time Disaster Aid Coordinator",
    page_icon="🚨",
    layout="wide"
)

# Initialize session state
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'last_analysis' not in st.session_state:
    st.session_state.last_analysis = None
if 'chat_key' not in st.session_state:
    st.session_state.chat_key = 0

# Initialize agents
@st.cache_resource
def initialize_agents():
    """Initialize all agents (cached to avoid reinitializing)"""
    return {
        'news': NewsAgent(),
        'alert': AlertAgent(),
        'chat': ChatAgent(),
        'message': AlertMessageAgent()
    }

agents = initialize_agents()

# Main UI
st.title("🚨 ReDAC - Real-Time Disaster Aid Coordinator")
st.markdown("*Your AI-powered disaster monitoring and alert system*")

# Sidebar for configuration
st.sidebar.header("⚙️ Configuration")

# User location input
user_location = st.sidebar.text_input(
    "📍 Your Location", 
    placeholder="e.g., New York, California, London",
    help="Enter your city, state, or region"
)

# Alert platform display (Discord only as requested)
st.sidebar.markdown("📢 **Alert Platform:** Discord")

# Test alert button
if st.sidebar.button("🧪 Test Alert System"):
    if user_location:
        with st.sidebar:
            with st.spinner("Testing alert system..."):
                success = agents['alert'].send_test_alert()
                if success:
                    st.success("✅ Alert system working!")
                else:
                    st.error("❌ Alert system not configured. Check your webhook URL.")
    else:
        st.sidebar.error("Please enter your location first.")

# Main content area
col1, col2 = st.columns([2, 1])

with col1:
    st.header("📰 Disaster Monitoring")
    
    if st.button("🔍 Check for Disasters", type="primary"):
        if not user_location:
            st.error("Please enter your location in the sidebar first.")
        else:
            with st.spinner(f"Searching for disasters near {user_location}..."):
                # Step 1: Fetch news
                news_articles = agents['news'].search_disaster_news(user_location)
                
                if news_articles:
                    # Step 2: Format news for analysis
                    news_data = agents['news'].format_news_for_analysis(news_articles)
                    
                    # Step 3: Analyze and potentially send alerts
                    result = agents['alert'].analyze_and_alert(news_data, user_location)
                    
                    # Store result for chat context
                    st.session_state.last_analysis = result
                    
                    # Display results
                    if result['analysis']['disaster_found']:
                        st.error("🚨 **DISASTER ALERT!**")
                        
                        col_a, col_b = st.columns(2)
                        with col_a:
                            st.metric("Disaster Type", result['analysis']['disaster_type'])
                            st.metric("Severity", result['analysis']['severity'])
                        with col_b:
                            st.metric("Alert Sent", "✅ Yes" if result['alert_sent'] else "❌ Failed")
                        
                        st.write("**Description:**", result['analysis']['description'])
                        st.write("**Recommended Actions:**", result['analysis']['actions'])
                        
                        # Show the professional alert message
                        if result.get('alert_message'):
                            st.subheader("📢 Alert Message Sent:")
                            st.text_area("Professional Alert", result['alert_message'], height=200, key="alert_display")
                        
                        if result['alert_sent']:
                            st.success("Professional alert sent to Discord!")
                        else:
                            st.warning("Alert could not be sent. Check your Discord webhook configuration.")
                    
                    else:
                        st.success("✅ No immediate disasters detected in your area.")
                        st.info("Stay alert and check back regularly for updates.")
                        
                        # Show the "all clear" message that was sent
                        if result.get('alert_message'):
                            st.subheader("📢 Status Update Sent:")
                            st.text_area("Safety Status", result['alert_message'], height=150, key="status_display")
                    
                    # Show news articles
                    with st.expander("📰 View News Articles"):
                        for i, article in enumerate(news_articles, 1):
                            st.write(f"**{i}. {article['title']}**")
                            st.write(article['snippet'])
                            st.write(f"*Source: {article['source']} | {article['date']}*")
                            if article['link'] and not article['link'].startswith('https://example.com'):
                                st.write(f"[Read more]({article['link']})")
                            st.divider()
                
                else:
                    st.info("No recent news found for your location. This might be good news!")

with col2:
    st.header("💬 Chat Assistant")
    
    # Display chat history
    chat_container = st.container()
    with chat_container:
        for message in st.session_state.chat_history:
            if message['role'] == 'user':
                st.write(f"**You:** {message['content']}")
            else:
                st.write(f"**ReDAC:** {message['content']}")
    
    # Chat input - FIXED: Using form to prevent infinite loop
    with st.form("chat_form", clear_on_submit=True):
        user_message = st.text_input("Ask me about disasters, safety tips, or anything else:")
        submitted = st.form_submit_button("Send")
        
        if submitted and user_message:
            # Add user message to history
            st.session_state.chat_history.append({
                'role': 'user',
                'content': user_message
            })
            
            # Prepare context from last analysis
            context = ""
            if st.session_state.last_analysis:
                analysis = st.session_state.last_analysis['analysis']
                if analysis.get('disaster_found'):
                    context = f"Recent disaster analysis for {user_location}: {analysis.get('disaster_type', 'Unknown')} - {analysis.get('description', 'No description')}"
            
            # Get AI response
            with st.spinner("Thinking..."):
                response = agents['chat'].chat(user_message, context)
            
            # Add AI response to history
            st.session_state.chat_history.append({
                'role': 'assistant',
                'content': response
            })
            
            # FIXED: Use rerun only when necessary, not after every message
            if len(st.session_state.chat_history) > 20:  # Clear old messages
                st.session_state.chat_history = st.session_state.chat_history[-10:]
            
            if len(st.session_state.chat_history) > 20:
                st.session_state.chat_history = st.session_state.chat_history[-10:]

    # Clear chat button
    # if st.button("🗑️ Clear Chat"):
    #     st.session_state.chat_history = []
    #     agents['chat'].clear_context()
    #     st.rerun()

# Footer information
st.divider()
st.markdown("### 🔧 How ReDAC Works")

with st.expander("Click to learn about the technology"):
    st.markdown("""
    **ReDAC uses several AI components working together:**
    
    1. **News Agent** 🕵️ - Searches for disaster-related news using Serper API (with DuckDuckGo backup)
    2. **Alert Agent** 🚨 - Analyzes news with Groq AI and sends alerts via Discord
    3. **Chat Agent** 💬 - Provides conversational help and safety information
    4. **Alert Message Agent** 📝 - Creates professional, comprehensive alert messages
    
    **LangChain Components Used:**
    - **Templates**: Pre-written instructions for the AI
    - **Parsers**: Structure AI responses into organized data  
    - **Chains**: Connect templates → AI → parsers in sequence
    - **Runnables**: Modern way to execute LangChain components
    """)

# Configuration help
# with st.expander("⚙️ Setup Instructions"):
#     st.markdown("""
#     **To set up ReDAC, you need:**
    
#     1. **Create a .env file** with these API keys:
#     ```
#     GROQ_API_KEY=your_groq_api_key_here
#     SERPER_API_KEY=your_serper_api_key_here  
#     DISCORD_WEBHOOK_URL=your_discord_webhook_url_here
#     ```
    
#     2. **Get API Keys (All Free!):**
#     - **Groq API**: Visit console.groq.com → Create account → Get API key
#     - **Serper API**: Visit serper.dev → Sign up → Get API key (100 free searches/month)
#     - **Discord Webhook**: Create Discord server → Channel settings → Integrations → Webhooks
    
#     3. **Install Dependencies:**
#     ```bash
#     pip install -r requirements.txt
#     ```
    
#     4. **Run the App:**
#     ```bash
#     streamlit run app.py
#     ```
#     """)

# Status indicators
st.sidebar.divider()
st.sidebar.header("🔌 System Status")

# Check API keys
import os
if os.getenv("GROQ_API_KEY"):
    st.sidebar.success("✅ Groq AI Connected")
else:
    st.sidebar.error("❌ Groq AI Not Configured")

if os.getenv("SERPER_API_KEY"):
    st.sidebar.success("✅ Serper News Connected") 
else:
    st.sidebar.warning("⚠️ Using Mock News Data")

if os.getenv("DISCORD_WEBHOOK_URL"):
    st.sidebar.success("✅ Discord Alerts Ready")
else:
    st.sidebar.error("❌ Discord Not Configured")

# Show current configuration
st.sidebar.info(f"📍 **Current Location:** {user_location if user_location else 'Not set'}")