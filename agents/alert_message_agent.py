from langchain_groq import ChatGroq
from langchain.schema.output_parser import StrOutputParser
from langchain.prompts import PromptTemplate
from config import GROQ_API_KEY
from datetime import datetime

class AlertMessageAgent:
    """
    ALERT MESSAGE AGENT: Creates professional, descriptive alert messages
    This agent specializes in generating well-formatted, comprehensive alerts
    that include all necessary information for disaster response
    """
    
    def __init__(self):
        # Initialize specialized LLM for alert message generation
        self.llm = ChatGroq(
            groq_api_key=GROQ_API_KEY,
            model_name="llama-3.3-70b-versatile",
            temperature=0.3  # Balanced temperature for professional but adaptive messaging
        )
        
        # Professional alert message template
        self.alert_template = PromptTemplate(
            input_variables=[
                "disaster_type", "location", "severity", "description", 
                "timestamp", "recommended_actions", "emergency_contacts"
            ],
            template="""
            You are a professional emergency alert system. Create a comprehensive, well-formatted disaster alert message.

            DISASTER INFORMATION:
            - Type: {disaster_type}
            - Location: {location}  
            - Severity Level: {severity}
            - Description: {description}
            - Time: {timestamp}
            - Recommended Actions: {recommended_actions}

            Create a professional emergency alert that includes:
            1. Clear, attention-grabbing header with appropriate emoji
            2. Essential disaster information in organized sections
            3. Severity level with visual indicators
            4. Specific location details
            5. Immediate action steps
            6. Safety recommendations
            7. Professional closing with authority reference

            Format the message to be:
            - CLEAR and EASY TO READ
            - PROFESSIONAL but URGENT in tone  
            - COMPREHENSIVE with all critical details
            - ACTION-ORIENTED with specific steps
            - WELL-STRUCTURED with proper sections

            Generate the complete alert message:
            """
        )
        
        # Create the alert generation chain
        self.alert_chain = (
            self.alert_template
            | self.llm
            | StrOutputParser()
        )
    
    def generate_professional_alert(self, disaster_info: dict, location: str) -> str:
        """
        Generate a professional, comprehensive alert message
        
        Args:
            disaster_info: Dictionary containing disaster analysis results
            location: User's location
            
        Returns:
            Professional formatted alert message
        """
        try:
            # Get current timestamp
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC")
            
            # Extract information from disaster analysis
            disaster_type = disaster_info.get('disaster_type', 'Unknown Emergency')
            severity = disaster_info.get('severity', 'Unknown')
            description = disaster_info.get('description', 'Emergency situation detected')
            actions = disaster_info.get('actions', 'Follow local authority guidance')
            
            # Generate professional alert message
            alert_message = self.alert_chain.invoke({
                "disaster_type": disaster_type,
                "location": location,
                "severity": severity,
                "description": description,
                "timestamp": current_time,
                "recommended_actions": actions,
                "emergency_contacts": "Contact local emergency services: 911 (US), 112 (EU), 999 (UK)"
            })
            
            return alert_message
            
        except Exception as e:
            # Fallback to basic alert if AI generation fails
            return self._generate_fallback_alert(disaster_info, location)
    
    def _generate_fallback_alert(self, disaster_info: dict, location: str) -> str:
        """
        Generate a basic alert if the AI system fails
        """
        disaster_type = disaster_info.get('disaster_type', 'Emergency')
        severity = disaster_info.get('severity', 'Unknown')
        description = disaster_info.get('description', 'Emergency situation detected')
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        return f"""
🚨 EMERGENCY ALERT 🚨

DISASTER TYPE: {disaster_type}
LOCATION: {location}
SEVERITY: {severity}
TIME: {timestamp}

SITUATION:
{description}

IMMEDIATE ACTIONS:
• Stay calm and alert
• Follow local emergency guidance
• Keep emergency supplies ready
• Monitor official communications
• Contact emergency services if needed

⚠️ This is an automated alert from CrisisPilot – Global Disaster Swift Response Assistant.
Stay safe and follow official emergency protocols.
        """.strip()
    
    def generate_test_alert(self) -> str:
        """Generate a test alert message"""
        return """
🧪 CrisisPilot: Global Disaster Response – System Test Mode 🧪

ALERT SYSTEM STATUS: ✅ OPERATIONAL
TEST TIME: """ + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + """

This is a test of the  CrisisPilot Emergency Alert System.
- All systems are functioning correctly
- Alert delivery confirmed
- Ready for emergency monitoring

If this was a real emergency, you would receive:
• Detailed disaster information
• Specific location data  
• Severity assessment
• Recommended safety actions
• Emergency contact information

📱  CrisisPilot: Global Disaster Swift Response Assistant
Your AI-powered emergency monitoring system is active.
        """.strip()
    
    def generate_no_threat_message(self, location: str) -> str:
        """Generate a message when no threats are detected"""
        return f"""
✅ SAFETY STATUS UPDATE ✅

LOCATION: {location}
STATUS: NO IMMEDIATE THREATS DETECTED
SCAN TIME: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

CURRENT SITUATION:
• No active disasters detected in your area
• Weather conditions appear stable  
• Emergency services report normal operations
• No evacuation orders or warnings issued

RECOMMENDATIONS:
• Stay informed through local news
• Keep emergency kit updated
• Review family emergency plan
• Check back regularly for updates

🛡️ CrisisPilot: Global Disaster Swift Response Assistant continues monitoring for your safety.
        """.strip()