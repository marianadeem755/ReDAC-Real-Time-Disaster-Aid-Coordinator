from langchain.prompts import PromptTemplate

# TEMPLATE: Instructions for the AI (like a fill-in-the-blank form)
# This template tells the AI how to analyze news for disasters

NEWS_ANALYSIS_TEMPLATE = PromptTemplate(
    input_variables=["news_data", "user_location"],
    template="""
    You are a disaster monitoring AI assistant. Analyze the following news data and determine if there are any disasters or emergencies relevant to the user's location.

    User Location: {user_location}
    News Data: {news_data}

    Please analyze and respond with:
    1. Is there any disaster/emergency near the user's location? (Yes/No)
    2. Type of disaster (if any)
    3. Severity level (Low/Medium/High)
    4. Brief description
    5. Recommended actions

    Format your response as:
    DISASTER_FOUND: [Yes/No]
    DISASTER_TYPE: [type]
    SEVERITY: [level]
    DESCRIPTION: [brief description]
    ACTIONS: [recommended actions]
    """
)

# TEMPLATE: For generating alert messages
ALERT_TEMPLATE = PromptTemplate(
    input_variables=["disaster_type", "location", "severity", "description"],
    template="""
    🚨 DISASTER ALERT 🚨
    
    Type: {disaster_type}
    Location: {location}
    Severity: {severity}
    
    Description: {description}
    
    Stay safe and follow local authorities' guidance!
    """
)

# TEMPLATE: For chatbot responses
CHAT_TEMPLATE = PromptTemplate(
    input_variables=["user_question", "context"],
    template="""
    You are a helpful disaster response assistant. Answer the user's question based on the context provided.
    
    Context: {context}
    User Question: {user_question}
    
    Provide a helpful, clear, and supportive response. If you don't have enough information, suggest where they might find more help.
    
    Response:
    """
)