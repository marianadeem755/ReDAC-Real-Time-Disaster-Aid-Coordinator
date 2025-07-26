from langchain_groq import ChatGroq
from langchain.schema.runnable import RunnablePassthrough
from langchain.schema.output_parser import StrOutputParser
from utils.templates import NEWS_ANALYSIS_TEMPLATE
from utils.parsers import parse_disaster_text
from utils.alert_sender import AlertSender
from agents.alert_message_agent import AlertMessageAgent
from config import GROQ_API_KEY

class AlertAgent:
    """
    ALERT AGENT: Analyzes news and sends professional alerts
    This agent uses LangChain to process news and determine if alerts are needed
    """
    
    def __init__(self):
        # Initialize the Groq LLM (Large Language Model) with current supported model
        self.llm = ChatGroq(
            groq_api_key=GROQ_API_KEY,
            model_name="llama-3.3-70b-versatile",  # Updated to current supported model
            temperature=0.1  # Low temperature for consistent results
        )
        
        # Initialize alert sender and message generator
        self.alert_sender = AlertSender()
        self.message_agent = AlertMessageAgent()
        
        # Create a CHAIN: Template → LLM → Parser
        # This is like a pipeline that processes data step by step
        self.analysis_chain = (
            NEWS_ANALYSIS_TEMPLATE 
            | self.llm 
            | StrOutputParser()
        )
    
    def analyze_and_alert(self, news_data: str, user_location: str) -> dict:
        """
        Main method: Analyze news and send professional alerts if needed
        
        Steps:
        1. Use AI to analyze news data
        2. Parse the results
        3. If disaster found, generate professional alert message
        4. Send alert via configured platform
        
        Returns:
            Dictionary with analysis results and alert status
        """
        try:
            # Step 1: Analyze news using AI
            analysis_result = self.analysis_chain.invoke({
                "news_data": news_data,
                "user_location": user_location
            })
            
            # Step 2: Parse the analysis result
            parsed_result = parse_disaster_text(analysis_result)
            
            # Step 3: Generate and send alert if disaster found
            alert_sent = False
            alert_message = ""
            
            if parsed_result["disaster_found"]:
                # Generate professional alert message using dedicated agent
                alert_message = self.message_agent.generate_professional_alert(
                    parsed_result, user_location
                )
                
                # Send the professional alert
                alert_sent = self.alert_sender.send_alert(alert_message)
            else:
                # Send "all clear" message
                alert_message = self.message_agent.generate_no_threat_message(user_location)
                alert_sent = self.alert_sender.send_alert(alert_message)
            
            return {
                "analysis": parsed_result,
                "alert_sent": alert_sent,
                "alert_message": alert_message,
                "raw_analysis": analysis_result
            }
            
        except Exception as e:
            print(f"Error in analyze_and_alert: {e}")
            return {
                "analysis": {
                    "disaster_found": False,
                    "error": str(e)
                },
                "alert_sent": False,
                "alert_message": "",
                "raw_analysis": ""
            }
    
    def send_test_alert(self) -> bool:
        """Send a professional test alert to verify the system is working"""
        test_message = self.message_agent.generate_test_alert()
        return self.alert_sender.send_alert(test_message)
    
    def send_custom_alert(self, message: str) -> bool:
        """Send a custom alert message"""
        return self.alert_sender.send_alert(message)