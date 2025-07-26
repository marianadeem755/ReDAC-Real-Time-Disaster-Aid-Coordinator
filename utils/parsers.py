from pydantic import BaseModel, Field
from langchain.output_parsers import PydanticOutputParser
from typing import Optional

# PARSER: Structures the AI's response into organized data
# Think of this as a form that the AI must fill out correctly

class DisasterAnalysis(BaseModel):
    """Structure for disaster analysis results"""
    disaster_found: bool = Field(description="Whether a disaster was found")
    disaster_type: Optional[str] = Field(description="Type of disaster")
    severity: Optional[str] = Field(description="Severity level (Low/Medium/High)")
    description: Optional[str] = Field(description="Brief description of the disaster")
    actions: Optional[str] = Field(description="Recommended actions")

class ChatResponse(BaseModel):
    """Structure for chatbot responses"""
    response: str = Field(description="The chatbot's response")
    helpful: bool = Field(description="Whether the response is helpful")

# Create parser instances
disaster_parser = PydanticOutputParser(pydantic_object=DisasterAnalysis)
chat_parser = PydanticOutputParser(pydantic_object=ChatResponse)

# Function to parse disaster analysis text
def parse_disaster_text(text: str) -> dict:
    """
    Manual parser for disaster analysis when structured parsing fails
    This is a backup method to extract information from AI responses
    """
    result = {
        "disaster_found": False,
        "disaster_type": "Unknown",
        "severity": "Low",
        "description": "No specific information available",
        "actions": "Stay alert and follow local news"
    }
    
    lines = text.split('\n')
    for line in lines:
        line = line.strip()
        if line.startswith('DISASTER_FOUND:'):
            result["disaster_found"] = 'Yes' in line
        elif line.startswith('DISASTER_TYPE:'):
            result["disaster_type"] = line.replace('DISASTER_TYPE:', '').strip()
        elif line.startswith('SEVERITY:'):
            result["severity"] = line.replace('SEVERITY:', '').strip()
        elif line.startswith('DESCRIPTION:'):
            result["description"] = line.replace('DESCRIPTION:', '').strip()
        elif line.startswith('ACTIONS:'):
            result["actions"] = line.replace('ACTIONS:', '').strip()
    
    return result