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
    
    def emergency_chat(self, user_question: str, emergency_context: str = "") -> str:
        """
        Handle emergency chat messages - SIMPLIFIED VERSION
        """
        try:
            # Create emergency-focused question using regular chat method
            emergency_question = f"""
🚨 EMERGENCY SITUATION 🚨

Context: {emergency_context}

User's Emergency Question: {user_question}

Please provide immediate emergency safety guidance with:
1. Immediate actions to take RIGHT NOW
2. Safety measures and protection steps
3. Emergency supplies needed
4. What to avoid for safety
5. When to evacuate or seek help

Focus on life-saving information and be specific and actionable.
"""
            
            # Use the regular chat method with emergency context
            response = self.chat(emergency_question, "EMERGENCY MODE ACTIVATED")
            
            # Add emergency formatting
            return f"🚨 **EMERGENCY RESPONSE** 🚨\n\n{response}"
            
        except Exception as e:
            # Detailed fallback response
            return f"""
🚨 **EMERGENCY SAFETY GUIDANCE** 🚨

**Your Question:** {user_question}

**🏠 SHELTER SAFETY & IMMEDIATE PROTECTION:**

**1. SECURE YOUR IMMEDIATE AREA:**
• Move to the safest room (interior room, lowest floor if possible)
• Stay away from windows, glass, and heavy objects that could fall
• Have a sturdy table or desk nearby for cover if needed
• Keep clear pathways to exits

**2. GATHER EMERGENCY SUPPLIES NOW:**
• Flashlight and extra batteries (avoid candles)
• Battery-powered or hand-crank radio
• First aid kit and any medications you need
• Water - at least 1 gallon per person per day for 3 days
• Non-perishable food for at least 3 days
• Cell phone with chargers and backup battery
• Important documents in waterproof container
• Cash in small bills

**3. IMMEDIATE PROTECTION MEASURES:**
• Wear sturdy shoes and protective clothing
• Know where your gas shut-off valve is located
• Keep fire extinguisher accessible
• Have face masks ready (N95 if available)
• Know your evacuation routes

**4. COMMUNICATION & SAFETY:**
• Establish an out-of-area contact person
• Keep emergency numbers readily available
• Have a family meeting place planned
• Listen to official emergency broadcasts
• Follow evacuation orders immediately if given

**⚠️ CALL 911 IMMEDIATELY IF:**
• You are in immediate physical danger
• Someone is seriously injured
• You smell gas or see downed power lines
• You see fire or flooding approaching

**🚨 EVACUATION PRIORITY:**
If authorities order evacuation, leave IMMEDIATELY. Take your emergency kit and go to designated safe areas.

Error details: {str(e)}
            """
    
    def get_emergency_response(self, disaster_type: str, safety_context: str) -> str:
        """
        Generate immediate emergency response when disaster is first detected - SIMPLIFIED
        """
        try:
            # Create comprehensive emergency activation prompt
            activation_prompt = f"""
🚨 DISASTER EMERGENCY DETECTED 🚨

Disaster Type: {disaster_type}
Context: {safety_context}

Provide a comprehensive emergency response guide that includes:

1. IMMEDIATE ACTIONS people should take RIGHT NOW
2. SAFETY PRIORITIES and life-saving measures  
3. SHELTER and PROTECTION guidance
4. EVACUATION procedures if needed
5. EMERGENCY SUPPLIES checklist
6. COMMUNICATION steps
7. What to AVOID for safety

Make this detailed, actionable, and focused on immediate safety.
Use clear formatting with numbers and bullet points.
This could save lives - be thorough and specific.
"""
            
            # Use regular chat method
            response = self.chat(activation_prompt, "DISASTER EMERGENCY ACTIVATION")
            
            return f"🚨 **{disaster_type.upper()} EMERGENCY PROTOCOL ACTIVATED** 🚨\n\n{response}"
            
        except Exception as e:
            # Return disaster-specific fallback guidance
            return self._get_disaster_fallback(disaster_type, str(e))
    
    def _get_disaster_fallback(self, disaster_type: str, error_msg: str) -> str:
        """Provide fallback emergency guidance when AI fails"""
        
        disaster_guides = {
            "earthquake": """
🚨 **EARTHQUAKE EMERGENCY PROTOCOL** 🚨

**IMMEDIATE ACTIONS (RIGHT NOW):**
1. **DROP** to hands and knees immediately
2. **TAKE COVER** under sturdy desk/table or against interior wall  
3. **HOLD ON** and protect your head and neck with arms
4. Stay where you are until shaking completely stops
5. Count to 60 after shaking stops before moving

**AFTER SHAKING STOPS:**
• Check yourself and others for injuries
• Look for hazards: gas leaks, electrical damage, structural damage  
• Be ready for aftershocks (can be as strong as main quake)
• Use stairs only - NEVER elevators
• Stay out of damaged buildings
• Turn off gas if you smell leaks

**EMERGENCY SUPPLIES TO GATHER:**
• Water, food, flashlight, battery radio, first aid kit
• Sturdy shoes and work gloves
• Important documents and cash
• Fire extinguisher and gas shut-off wrench

**WHAT TO AVOID:**
• Don't run outside during shaking
• Don't stand in doorways  
• Don't use elevators
• Don't light matches if you smell gas
• Don't use phone unless emergency
            """,
            
            "flood": """
🚨 **FLOOD EMERGENCY PROTOCOL** 🚨

**IMMEDIATE ACTIONS (RIGHT NOW):**
1. Move to higher ground IMMEDIATELY - don't wait
2. If evacuation is ordered, LEAVE NOW
3. Never drive through flooded roads
4. Avoid walking in moving water (6 inches can knock you down)
5. Stay away from downed power lines

**EVACUATION PRIORITIES:**
• Take your emergency kit and important documents
• Follow designated evacuation routes to higher ground
• Help elderly/disabled neighbors if safe to do so
• Don't return until authorities say it's completely safe
• If trapped, get to highest floor and signal for help

**FLOOD WATER DANGERS:**
• Contains sewage, chemicals, and dangerous debris
• May be electrically charged from downed power lines
• Can hide holes, objects, and washouts
• Moves faster and is deeper than it appears

**EMERGENCY SUPPLIES:**
• Water purification tablets, food, radio, flashlight
• Waterproof containers for documents
• Life jackets or flotation devices if available
• Cell phone in waterproof case

**WHAT TO AVOID:**  
• Never drive through flooded streets ("Turn Around, Don't Drown")
• Don't walk in flowing water
• Don't touch electrical equipment if standing in water
• Don't drink flood water
            """,
            
            "fire": """  
🚨 **FIRE EMERGENCY PROTOCOL** 🚨

**IMMEDIATE ACTIONS (RIGHT NOW):**
1. If evacuation is ordered, LEAVE IMMEDIATELY
2. Grab your pre-packed emergency "Go Bag"
3. Close all doors and windows behind you (don't lock)
4. Follow multiple evacuation routes away from fire
5. Call 911 from safe location to report your status

**EVACUATION PROCEDURES:**
• Don't delay to gather belongings - GO NOW
• Stay low if there's smoke (crawl if necessary)
• Feel doors before opening (hot door = don't open)
• Use wet cloth over nose and mouth
• Meet at designated family meeting place

**SMOKE PROTECTION:**
• Stay indoors with windows/doors closed if not evacuating
• Use air conditioning on recirculate mode
• Create "clean room" with minimal air leaks
• Use N95 masks when going outside
• Monitor air quality reports

**EMERGENCY SUPPLIES:**
• Go-bag with 3 days supplies ready at all times
• Important documents in fireproof container
• N95 masks for smoke protection
• Battery radio for evacuation updates

**WHAT TO AVOID:**
• Don't delay evacuation to save belongings
• Don't use elevators during fire emergency
• Don't go back into evacuated areas
• Don't open doors that feel hot
• Don't use generators or grills indoors
            """
        }
        
        # Get specific guidance or generic emergency response
        guide = disaster_guides.get(disaster_type.lower(), f"""
🚨 **{disaster_type.upper()} EMERGENCY PROTOCOL** 🚨

**IMMEDIATE ACTIONS:**
• Follow all official emergency guidance immediately
• Evacuate if ordered by authorities - don't delay
• Monitor emergency broadcasts continuously
• Keep emergency supplies ready and accessible
• Stay in communication with family/friends

**GENERAL EMERGENCY PRIORITIES:**
• Life safety is the top priority
• Follow evacuation orders immediately
• Keep emergency communication devices charged
• Have multiple evacuation routes planned
• Help neighbors if safe to do so

**EMERGENCY SUPPLIES:**
• Water: 1 gallon per person per day for 3+ days
• Food: 3+ days of non-perishable food
• Battery radio and flashlight with extra batteries
• First aid kit and prescription medications
• Important documents and cash
• Cell phone chargers and backup batteries

**STAY INFORMED:**
• Monitor official emergency broadcasts
• Follow local emergency management social media
• Listen to weather radio for updates
• Keep communication devices charged
• Have backup communication methods ready
        """)
        
        return f"{guide}\n\n**System Error:** {error_msg}\n**Contact local emergency services for immediate assistance: 911**"
    
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