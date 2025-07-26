# Sidebar - Updated with Discord Server Instructions
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

# Discord Server Invitation Section
st.sidebar.divider()
st.sidebar.header("🔗 Join Our Discord Server")

st.sidebar.markdown("""
To receive real-time alerts and interact with the CrisisPilot community:

1. **Click the invite link below:**
   👉 [Join CrisisPilot Discord Server](https://discord.gg/your-invite-code)

2. **Log in** to your Discord account (if not already).

3. **Accept the invitation** and you'll be added to the server.

4. **Navigate** to the **#alerts** or **#general** channel to see updates.

> 🔒 **Note**: If the invite expires or you get an error, contact the project maintainer for a new link.
""")

# Optional: Add a more prominent button-style link
if st.sidebar.button("🎮 Join Discord Community", type="secondary", help="Click to join our Discord server"):
    st.sidebar.markdown("""
    **Discord Invite Link:**
    https://discord.gg/your-invite-code
    """)
    st.sidebar.info("Copy the link above and paste it in your browser to join!")

# Discord community status indicator
st.sidebar.markdown("""
<div style="text-align: center; padding: 10px; background: rgba(114, 137, 218, 0.2); border-radius: 10px; margin: 10px 0;">
    <strong>🎮 Discord Community</strong><br>
    <small>Join for alerts & support</small>
</div>
""", unsafe_allow_html=True)

# System Status Section (keeping your existing code)
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
