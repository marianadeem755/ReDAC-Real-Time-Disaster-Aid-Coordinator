import streamlit as st
import time
import os
from agents.news_agent import NewsAgent
from agents.alert_agent import AlertAgent
from agents.chat_agent import ChatAgent
from agents.alert_message_agent import AlertMessageAgent

# Configure Streamlit page
st.set_page_config(
    page_title="CrisisPilot: Global Disaster Swift Response Assistant",
    page_icon="🚨",
    layout="wide"
)

# Your exact styling with black text fix
st.markdown("""
<style>
    /* Main app background with gradient */
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 25%, #f093fb 50%, #f5576c 75%, #4facfe 100%);
        background-size: 400% 400%;
        animation: gradientShift 15s ease infinite;
    }
    
    /* Animated gradient keyframes */
    @keyframes gradientShift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    /* Main content container with semi-transparent background */
    .main .block-container {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 2rem;
        margin-top: 1rem;
        box-shadow: 0 8px 32px rgba(31, 38, 135, 0.37);
        border: 1px solid rgba(255, 255, 255, 0.18);
    }
    
    /* Sidebar styling with gradient background */
    .css-1d391kg, .css-1cypcdb, .sidebar .sidebar-content, section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #ff9a9e 0%, #fecfef 50%, #fecfef 100%) !important;
        backdrop-filter: blur(10px);
        border-radius: 0 20px 20px 0;
        border-right: 2px solid rgba(255, 255, 255, 0.3);
    }
    
    /* Sidebar text styling for better readability - BLACK TEXT */
    .sidebar .sidebar-content, section[data-testid="stSidebar"] * {
        color: #000000 !important;
    }
    
    .sidebar .sidebar-content h1, 
    .sidebar .sidebar-content h2, 
    .sidebar .sidebar-content h3,
    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3 {
        color: #000000 !important;
        text-shadow: 1px 1px 2px rgba(255,255,255,0.5);
    }
    
    /* Make buttons more vibrant */
    .stButton > button {
        background: linear-gradient(45deg, #FF6B6B, #4ECDC4, #45B7D1, #96CEB4) !important;
        background-size: 300% 300%;
        animation: gradientShift 3s ease infinite;
        color: white !important;
        border: none !important;
        border-radius: 25px !important;
        padding: 12px 24px !important;
        font-weight: bold !important;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2) !important;
        transition: all 0.3s ease !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(0,0,0,0.3) !important;
    }
    
    /* Enhanced main title with glassmorphism effect */
    .main-title {
        background: rgba(255, 255, 255, 0.25) !important;
        backdrop-filter: blur(10px) !important;
        -webkit-backdrop-filter: blur(10px) !important;
        border: 1px solid rgba(255, 255, 255, 0.18) !important;
        padding: 30px !important;
        border-radius: 20px !important;
        color: white !important;
        text-align: center !important;
        margin-bottom: 30px !important;
        box-shadow: 0 8px 32px rgba(31, 38, 135, 0.37) !important;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3) !important;
    }
    
    /* Alert boxes with glassmorphism */
    .alert-danger {
        background: rgba(255, 107, 107, 0.8) !important;
        backdrop-filter: blur(10px) !important;
        color: white !important;
        padding: 20px !important;
        border-radius: 15px !important;
        margin: 15px 0 !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        box-shadow: 0 4px 16px rgba(255, 107, 107, 0.3) !important;
    }
    
    .alert-success {
        background: rgba(0, 210, 211, 0.8) !important;
        backdrop-filter: blur(10px) !important;
        color: white !important;
        padding: 20px !important;
        border-radius: 15px !important;
        margin: 15px 0 !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        box-shadow: 0 4px 16px rgba(0, 210, 211, 0.3) !important;
    }
    
    /* Style metrics and other elements */
    div[data-testid="metric-container"] {
        background: rgba(255, 255, 255, 0.1) !important;
        backdrop-filter: blur(10px) !important;
        border: 1px solid rgba(255, 255, 255, 0.18) !important;
        padding: 1rem !important;
        border-radius: 15px !important;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1) !important;
    }
    
    /* Text areas and inputs styling */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea {
        background: rgba(255, 255, 255, 0.9) !important;
        border: 1px solid rgba(255, 255, 255, 0.3) !important;
        border-radius: 10px !important;
        backdrop-filter: blur(5px) !important;
        color: #000000 !important;
    }
    
    /* Expander styling */
    .streamlit-expanderHeader {
        background: rgba(255, 255, 255, 0.1) !important;
        backdrop-filter: blur(10px) !important;
        border-radius: 10px !important;
        border: 1px solid rgba(255, 255, 255, 0.18) !important;
    }
    
    /* Status badges enhancement */
    .status-badge {
        display: inline-block;
        padding: 8px 16px;
        border-radius: 20px;
        font-weight: bold;
        margin: 2px;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    }
    
    /* Make sure main content text is readable */
    .stMarkdown, .stText {
        color: white !important;
        text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.5) !important;
    }
    
    /* Chat messages styling */
    .chat-message {
        background: rgba(0, 0, 0, 0.7) !important;
        color: white !important;
        padding: 10px !important;
        border-radius: 10px !important;
        margin: 5px 0 !important;
    }
    
    /* Tabs styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 24px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: rgba(255, 255, 255, 0.2);
        border-radius: 15px;
        color: white !important;
        font-weight: bold;
        padding: 10px 20px;
    }
    
    .stTabs [aria-selected="true"] {
        background: rgba(255, 255, 255, 0.4) !important;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state - Simplified without auto-alert features
def initialize_session_state():
    """Initialize session state variables properly"""
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    if 'last_analysis' not in st.session_state:
        st.session_state.last_analysis = None
    if 'chat_input_key' not in st.session_state:
        st.session_state.chat_input_key = 0
    if 'processing_chat' not in st.session_state:
        st.session_state.processing_chat = False
    # REMOVED: auto_safety_generated, emergency_mode, sos_button_clicked, pending_response

# Initialize session state
initialize_session_state()

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
st.markdown("""
<div class="main-title">
    <h1>🚨 CrisisPilot: Global Disaster Swift Response Assistant</h1>
    <p>An AI-powered assistant for real-time disaster detection and response — accelerating relief, reducing impact, and saving lives through smart alerts and coordination.</p>
</div>
""", unsafe_allow_html=True)

# Sidebar
st.sidebar.header("🔮 System Portal")
user_location = st.sidebar.text_input(
    "📍Enter Your Location Here:", 
    placeholder="e.g., New York, California, London",
    help="Enter your city, state, or region"
)

# Discord-only configuration
st.sidebar.info("📢 **Alert Platform:** Discord")
st.sidebar.markdown("*Instant notifications via Discord webhook*")

if st.sidebar.button("🔔Trigger Discord Alert"):
    if user_location:
        with st.sidebar:
            with st.spinner("Testing Discord alert system..."):
                success = agents['alert'].send_test_alert()
                if success:
                    st.success("✅ Discord alert system working!")
                else:
                    st.error("❌ Discord webhook not configured.")
    else:
        st.sidebar.error("Please enter your location first.")

# Main content with tabs
tab1, tab2, tab3, tab4 = st.tabs(["🚨 Disaster Monitor", "💬CrisisPilot: Command Chat Center", "🛡️Smart Survival Guide", "📊🔧Emergency Action Toolkit"])

with tab1:
    st.header("📰📡CrisisPilot: Global Threat Monitor")
    
    if st.button("🔍 Check for Disasters", type="primary"):
        if not user_location:
            st.error("Please enter your location in the sidebar first.")
        else:
            with st.spinner(f"Searching for disasters near {user_location}..."):
                news_articles = agents['news'].search_disaster_news(user_location)
                
                if news_articles:
                    news_data = agents['news'].format_news_for_analysis(news_articles)
                    result = agents['alert'].analyze_and_alert(news_data, user_location)
                    st.session_state.last_analysis = result
                    
                    if result['analysis']['disaster_found']:
                        st.error("🚨 **DISASTER ALERT!**")
                        
                        col_a, col_b = st.columns(2)
                        with col_a:
                            st.metric("Disaster Type", result['analysis']['disaster_type'])
                            st.metric("Severity", result['analysis']['severity'])
                        with col_b:
                            st.metric("Discord Alert", "✅ Sent" if result['alert_sent'] else "❌ Failed")
                            st.metric("Location", f"📍 {user_location}")
                        
                        st.write("**Description:**", result['analysis']['description'])
                        st.write("**Recommended Actions:**", result['analysis']['actions'])
                        
                        if result.get('alert_message'):
                            st.subheader("📢 Discord Alert Message Sent:")
                            st.text_area("Professional Alert", result['alert_message'], height=200, key="alert_display")
                    else:
                        st.success("✅ No immediate disasters detected in your area.")
                        st.info("Stay alert and check back regularly for updates.")
                    
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

with tab2:
    st.header("💬 AI Disaster Assistant")
    
    # REMOVED: All automatic alert activation logic and emergency mode detection
    # Chat now works in normal mode only, without auto-triggering emergency responses
    
    # Simple status indicator without emergency mode
    if st.session_state.last_analysis and st.session_state.last_analysis['analysis'].get('disaster_found'):
        disaster_info = st.session_state.last_analysis['analysis']
        st.info(f"ℹ️ **Disaster Information Available:** {disaster_info.get('disaster_type', 'Unknown')} detected in your area. You can ask me specific questions about safety measures.")
    else:
        st.info("🟢 **Ready to Help** - Ask me about disaster preparedness, safety tips, or emergency information.")
    
    # Display chat history with simplified styling
    if st.session_state.chat_history:
        st.subheader("💬 Conversation History")
        
        for i, message in enumerate(st.session_state.chat_history):
            if message['role'] == 'user':
                st.markdown(f'<div class="chat-message" style="background: rgba(0, 123, 255, 0.7);">**👤 You:** {message["content"]}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="chat-message" style="background: rgba(0, 200, 0, 0.7);">**🤖 CrisisPilot:** {message["content"]}</div>', unsafe_allow_html=True)
    else:
        st.info("👋 Hello! I'm your AI disaster assistant. Ask me about disasters, safety tips, or emergency preparedness.")
    
    # Simplified chat input without emergency context
    with st.form(key="chat_form", clear_on_submit=True):
        user_message = st.text_input(
            "Ask me anything about disaster safety and emergency preparedness:", 
            key=f"chat_input_{st.session_state.chat_input_key}",
            placeholder="Ask about disaster preparedness, safety tips, or emergency planning...",
            help="💡 Tip: Ask about specific disasters like 'earthquake safety' or 'flood preparation'"
        )
        submit_button = st.form_submit_button("Send 💬", type="primary")
        
        if submit_button and user_message.strip():
            # Prevent double processing
            if not st.session_state.processing_chat:
                st.session_state.processing_chat = True
                
                # Add user message
                st.session_state.chat_history.append({
                    'role': 'user',
                    'content': user_message
                })
                
                # Simple context preparation (optional disaster info if available)
                context = ""
                if st.session_state.last_analysis:
                    analysis = st.session_state.last_analysis['analysis']
                    if analysis.get('disaster_found'):
                        context = f"""
                        Available disaster information for reference:
                        Type: {analysis.get('disaster_type', 'Unknown')}
                        Severity: {analysis.get('severity', 'Unknown')}
                        Location: {user_location}
                        Description: {analysis.get('description', 'No description')}
                        """
                
                # Get AI response using regular chat method
                with st.spinner("🤔 Preparing response..."):
                    try:
                        response = agents['chat'].chat(user_message, context)
                        
                        # Add AI response
                        st.session_state.chat_history.append({
                            'role': 'assistant',
                            'content': response
                        })
                    except Exception as e:
                        error_msg = "I apologize, but I'm having trouble processing your request right now. Please try again."
                        st.error(f"Sorry, I encountered an error: {str(e)}")
                        st.session_state.chat_history.append({
                            'role': 'assistant',
                            'content': error_msg
                        })
                
                # Reset processing flag and increment key
                st.session_state.processing_chat = False
                st.session_state.chat_input_key += 1
                
                # Rerun to show the new messages
                st.rerun()

with tab3:
    st.header("🆘 CrisisPilot: Life-Saving Instructions")
    
    disaster_type = st.selectbox(
        "Select Disaster Type:", 
        ["Earthquake", "Flood", "Fire", "Hurricane", "Tornado", "Tsunami"],
        help="Choose a disaster type to get specific safety information"
    )
    
    if disaster_type:
        with st.spinner("Loading safety information..."):
            safety_info = agents['chat'].get_disaster_help(disaster_type.lower())
            st.markdown(safety_info)
    
    # Emergency contacts section
    st.subheader("🚨 Emergency Contacts")
    st.info("""
    **Universal Emergency Numbers:**
    - 🚨 Emergency Services: 911 (US), 112 (EU), 999 (UK)
    - 🚒 Fire Department: Local emergency number
    - 🚑 Medical Emergency: Local emergency number
    - 👮 Police: Local emergency number
    
    **Important:** Always call local emergency services first in case of immediate danger.
    """)

with tab4:
    st.header("📊 Emergency Preparedness Toolkit")
    
    # Emergency preparedness checklist
    st.subheader("✅ Emergency Preparedness Checklist")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🧰Survival SmartKit: Essentials Checklist")
        emergency_kit_items = [
            "Water (1 gallon per person per day for 3 days)",
            "Non-perishable food (3-day supply)",
            "Battery-powered or hand crank radio",
            "Flashlight and extra batteries",
            "First aid kit",
            "Whistle for signaling help",
            "Dust masks and plastic sheeting",
            "Moist towelettes and garbage bags",
            "Wrench or pliers to turn off utilities",
            "Manual can opener",
            "Local maps",
            "Cell phone with chargers and backup battery"
        ]
        
        selected_items = []
        for item in emergency_kit_items:
            if st.checkbox(item, key=f"kit_{item[:20]}"):
                selected_items.append(item)
        
        progress = len(selected_items) / len(emergency_kit_items)
        st.progress(progress, text=f"Kit Completion: {int(progress * 100)}%")
    
    with col2:
        st.markdown("### 🏠📦Crisis-Ready Home Setup")
        home_prep_items = [
            "Create family emergency plan",
            "Identify safe spots in each room",
            "Know how to turn off water, gas, electricity",
            "Install smoke alarms on every level",
            "Check fire extinguisher annually",
            "Secure heavy furniture to walls",
            "Store emergency supplies in accessible location",
            "Keep important documents in waterproof container",
            "Practice evacuation routes",
            "Establish out-of-area contact person"
        ]
        
        selected_home_items = []
        for item in home_prep_items:
            if st.checkbox(item, key=f"home_{item[:20]}"):
                selected_home_items.append(item)
        
        home_progress = len(selected_home_items) / len(home_prep_items)
        st.progress(home_progress, text=f"Home Preparedness: {int(home_progress * 100)}%")
    
    st.divider()
    
    # Family emergency plan generator
    st.subheader("👨‍👩‍👧‍👦 Family Emergency Plan Builder")
    
    with st.expander("Create Your Family Emergency Plan"):
        family_size = st.number_input("Number of family members:", min_value=1, max_value=20, value=4)
        
        st.write("**Family Members Information:**")
        family_members = []
        for i in range(int(family_size)):
            col_name, col_age, col_needs = st.columns([2, 1, 2])
            with col_name:
                name = st.text_input(f"Member {i+1} Name:", key=f"name_{i}")
            with col_age:
                age = st.number_input(f"Age:", min_value=0, max_value=120, key=f"age_{i}")
            with col_needs:
                special_needs = st.text_input(f"Special Needs/Medications:", key=f"needs_{i}")
            
            if name:
                family_members.append({
                    'name': name,
                    'age': age,
                    'special_needs': special_needs
                })
        
        st.write("**Meeting Points:**")
        col_local, col_regional = st.columns(2)
        with col_local:
            local_meeting_point = st.text_input("Local meeting point (near your home):")
        with col_regional:
            regional_meeting_point = st.text_input("Regional meeting point (outside your area):")
        
        st.write("**Emergency Contacts:**")
        col_contact1, col_contact2 = st.columns(2)
        with col_contact1:
            emergency_contact_1 = st.text_input("Primary emergency contact:")
            emergency_phone_1 = st.text_input("Primary contact phone:")
        with col_contact2:
            emergency_contact_2 = st.text_input("Secondary emergency contact:")
            emergency_phone_2 = st.text_input("Secondary contact phone:")
        
        if st.button("Generate Family Emergency Plan", type="primary"):
            if family_members and local_meeting_point:
                plan = f"""
# Family Emergency Plan

## Family Members:
{chr(10).join([f"- {member['name']} (Age: {member['age']}) - Special needs: {member['special_needs'] or 'None'}" for member in family_members])}

## Meeting Points:
- **Local:** {local_meeting_point}
- **Regional:** {regional_meeting_point}

## Emergency Contacts:
- **Primary:** {emergency_contact_1} - {emergency_phone_1}
- **Secondary:** {emergency_contact_2} - {emergency_phone_2}

## Important Phone Numbers:
- Emergency Services: 911
- Local Police: [Fill in local number]
- Fire Department: [Fill in local number]
- Hospital: [Fill in local hospital]
- Poison Control: 1-800-222-1222

## Emergency Kit Locations:
- Primary: [Specify location in home]
- Vehicle: [Specify vehicle kit location]
- Workplace: [Specify workplace kit]

## Evacuation Routes:
- Primary route: [Fill in primary evacuation route]
- Alternative route: [Fill in alternative route]

## Utility Shut-offs:
- Water main: [Location]
- Gas valve: [Location]
- Electrical panel: [Location]

## Important Documents Location:
[Specify where important documents are stored]

## Pet Emergency Plan:
[Include pet carriers, food, medications, veterinarian contact]

---
*Print this plan and keep copies in your emergency kit, car, and workplace.*
                """
                
                st.markdown("### 📄 Your Family Emergency Plan")
                st.text_area("Emergency Plan (Copy and save this):", value=plan, height=400)
                st.success("✅ Emergency plan generated! Print and distribute copies to all family members.")
            else:
                st.error("Please fill in at least family member information and local meeting point.")
    
    st.divider()
    
    # Risk assessment tool
    st.subheader("🎯 Personal Risk Assessment")
    
    with st.expander("Assess Your Disaster Risks"):
        st.write("Based on your location and circumstances, identify potential risks:")
        
        location_input = st.text_input("Your specific location (city, state):", value=user_location if user_location else "")
        
        risk_types = {
            "Natural Disasters": ["Earthquake", "Flood", "Hurricane", "Tornado", "Wildfire", "Winter Storm", "Tsunami"],
            "Infrastructure": ["Power Outage", "Water Contamination", "Gas Leak", "Building Collapse"],
            "Security": ["Civil Unrest", "Terrorism", "Cyber Attack"],
            "Health": ["Pandemic", "Chemical Spill", "Nuclear Incident"]
        }
        
        user_risks = {}
        for category, risks in risk_types.items():
            st.write(f"**{category}:**")
            cols = st.columns(3)
            for i, risk in enumerate(risks):
                with cols[i % 3]:
                    risk_level = st.selectbox(
                        risk,
                        ["Low", "Medium", "High", "Very High"],
                        key=f"risk_{risk}",
                        index=0
                    )
                    user_risks[risk] = risk_level
        
        if st.button("Generate Risk Assessment Report"):
            high_risks = [risk for risk, level in user_risks.items() if level in ["High", "Very High"]]
            medium_risks = [risk for risk, level in user_risks.items() if level == "Medium"]
            
            st.markdown("### 📊 Your Risk Assessment Results")
            
            if high_risks:
                st.error(f"🔴 **High Priority Risks:** {', '.join(high_risks)}")
                st.write("**Recommended Actions:**")
                st.write("- Prioritize emergency planning for these risks")
                st.write("- Ensure you have specific supplies and plans for these scenarios")
                st.write("- Consider additional insurance coverage")
                st.write("- Stay informed about early warning systems")
            
            if medium_risks:
                st.warning(f"🟡 **Medium Priority Risks:** {', '.join(medium_risks)}")
                st.write("**Recommended Actions:**")
                st.write("- Include these risks in your general emergency planning")
                st.write("- Stay informed about prevention measures")
            
            st.info("💡 **Next Steps:** Focus your emergency preparedness efforts on your highest-risk scenarios first.")
    
    st.divider()
    
    # Resources and links
    st.subheader("🔗 Helpful Resources")
    
    col_res1, col_res2, col_res3 = st.columns(3)
    
    with col_res1:
        st.markdown("""
        ### 🏛️ Government Resources
        - [Ready.gov](https://www.ready.gov) - Official preparedness guide
        - [FEMA](https://www.fema.gov) - Federal emergency management
        - [Red Cross](https://www.redcross.org) - Disaster relief and preparedness
        - [Weather.gov](https://www.weather.gov) - National weather alerts
        """)
    
    with col_res2:
        st.markdown("""
        ### 📱 Essential Apps
        - FEMA App - Disaster alerts and tips
        - Red Cross Emergency App - First aid and alerts
        - Weather Radio - NOAA weather alerts
        - Zello Walkie Talkie - Communication backup
        """)
    
    with col_res3:
        st.markdown("""
        ### 📚 Additional Resources
        - Local emergency management office
        - Community emergency response teams (CERT)
        - Ham radio clubs for communication
        - First aid and CPR training courses
        """)

# Footer
st.divider()
st.markdown("### 🔧 How CrisisPilot Works")

with st.expander("Click to learn about the technology"):
    st.markdown("""
    **CrisisPilot uses several AI components working together:**
    
    1. **News Agent** 🕵️ - Searches for disaster-related news using Serper API
    2. **Alert Agent** 🚨 - Analyzes news with Groq AI and sends alerts to Discord
    3. **Chat Agent** 💬 - Provides conversational help and safety information
    4. **Alert Message Agent** 📝 - Creates professional, comprehensive alert messages
    
    **Discord Integration:**
    - 📱 Instant notifications via Discord webhooks
    - 🔔 Professional alert formatting
    - 🚨 Real-time disaster notifications
    - 💬 Community-friendly messaging
    """)

# Sidebar status
st.sidebar.divider()
st.sidebar.header("🔌 System Status")

# Check API configurations
if os.getenv("GROQ_API_KEY"):
    st.sidebar.markdown('<div class="status-badge" style="background: rgba(0, 210, 211, 0.8);">✅ Groq AI Connected</div>', unsafe_allow_html=True)
else:
    st.sidebar.markdown('<div class="status-badge" style="background: rgba(255, 107, 107, 0.8);">❌ Groq AI Not Configured</div>', unsafe_allow_html=True)

if os.getenv("SERPER_API_KEY"):
    st.sidebar.markdown('<div class="status-badge" style="background: rgba(0, 210, 211, 0.8);">✅ Serper News Connected</div>', unsafe_allow_html=True)
else:
    st.sidebar.markdown('<div class="status-badge" style="background: rgba(254, 202, 87, 0.8);">⚠️ Using Mock News Data</div>', unsafe_allow_html=True)

# Discord status indicator
if os.getenv("DISCORD_WEBHOOK_URL"):
    st.sidebar.markdown('<div class="status-badge" style="background: rgba(0, 210, 211, 0.8);">✅ Discord Ready</div>', unsafe_allow_html=True)
else:
    st.sidebar.markdown('<div class="status-badge" style="background: rgba(255, 107, 107, 0.8);">❌ Discord Not Configured</div>', unsafe_allow_html=True)

st.sidebar.info(f"📍 **Current Location:** {user_location if user_location else 'Not set'}")
st.sidebar.info("📢 🔔Powered by **Discord** for Instant Alerts")

# Session info
st.sidebar.divider()
st.sidebar.header("📊 Session Info")
st.sidebar.info(f"Chat Messages: {len(st.session_state.chat_history)}")
st.sidebar.info(f"Last Analysis: {'✅ Done' if st.session_state.last_analysis else '❌ None'}")
