from langchain_groq import ChatGroq
from langchain.schema.output_parser import StrOutputParser
from utils.templates import CHAT_TEMPLATE
from config import GROQ_API_KEY

class ChatAgent:
    """
    CHAT AGENT: Provides conversational interface
    This agent handles user questions about disasters, safety, and general help
    """
    
    def __init__(self):
        # Initialize the Groq LLM for chat with current supported model
        self.llm = ChatGroq(
            groq_api_key=GROQ_API_KEY,
            model_name="llama-3.3-70b-versatile",  # Updated to current supported model
            temperature=0.7  # Higher temperature for more conversational responses
        )
        
        # Create chat chain: Template → LLM → Parser
        self.chat_chain = (
            CHAT_TEMPLATE 
            | self.llm 
            | StrOutputParser()
        )
        
        # Store conversation context
        self.context = ""
    
    def chat(self, user_question: str, additional_context: str = "") -> str:
        """
        Handle user chat messages
        
        Args:
            user_question: What the user is asking
            additional_context: Any relevant context (e.g., recent disaster info)
        
        Returns:
            AI response to the user's question
        """
        try:
            # Combine stored context with additional context
            full_context = f"{self.context}\n{additional_context}".strip()
            
            # Get response from AI
            response = self.chat_chain.invoke({
                "user_question": user_question,
                "context": full_context
            })
            
            # Update context with this conversation
            self.update_context(user_question, response)
            
            return response
            
        except Exception as e:
            return f"I'm sorry, I encountered an error: {str(e)}. Please try again."
    
    def update_context(self, user_question: str, ai_response: str):
        """
        Update conversation context for better continuity
        """
        new_context = f"User: {user_question}\nAssistant: {ai_response}\n"
        
        # Keep context manageable (last 3 exchanges)
        context_lines = self.context.split('\n')
        if len(context_lines) > 12:  # 4 lines per exchange * 3 exchanges
            context_lines = context_lines[-12:]
        
        self.context = '\n'.join(context_lines) + new_context
    
    def get_disaster_help(self, disaster_type: str) -> str:
        """
        Get specific help information for a type of disaster
        """
        disaster_help = {
            "earthquake": """
            🏠 Earthquake Safety Tips:
            • Drop, Cover, and Hold On during shaking
            • Stay away from windows and heavy objects
            • If outdoors, move away from buildings
            • After shaking stops, check for injuries and hazards
            • Be prepared for aftershocks
            """,
            "flood": """
            🌊 Flood Safety Tips:
            • Never drive through flooded roads
            • Move to higher ground immediately
            • Avoid walking in moving water
            • Stay away from downed power lines
            • Listen to emergency broadcasts for updates
            """,
            "fire": """
            🔥 Fire Safety Tips:
            • Evacuate immediately if ordered
            • Keep emergency kit ready
            • Close all windows and doors
            • Wet cloth over nose and mouth for smoke
            • Stay low to avoid smoke inhalation
            """,
            "hurricane": """
            🌀 Hurricane Safety Tips:
            • Board up windows and secure outdoor items
            • Stock up on water, food, and supplies
            • Stay indoors during the storm
            • Avoid flooded areas after the storm
            • Listen to official weather updates
            """
        }
        
        return disaster_help.get(disaster_type.lower(), 
                               "Stay safe and follow local emergency guidance.")
    
    def clear_context(self):
        """Clear conversation context"""
        self.context = ""