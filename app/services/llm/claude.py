"""
Claude service for interacting with Anthropic's Claude API.
"""
import os
import logging
from typing import Dict, Any, List, Optional
import anthropic
from crewai.agents.llms.anthropic import Claude as CrewClaude

from app.config import settings

logger = logging.getLogger(__name__)

# Anthropic API
ANTHROPIC_MODEL = 'claude-3-7-sonnet-20250219'
ANTHROPIC_SMALL_FAST_MODEL = 'claude-3-5-haiku-20241022'

# Amazon Bedrock
BEDROCK_ANTHROPIC_MODEL = 'us.anthropic.claude-3-7-sonnet-20250219-v1:0'
BEDROCK_ANTHROPIC_SMALL_FAST_MODEL = 'us.anthropic.claude-3-5-haiku-20241022-v1:0'

# Google Vertex AI
VERTEX_ANTHROPIC_MODEL = 'claude-3-7-sonnet@20250219'
VERTEX_ANTHROPIC_SMALL_FAST_MODEL = 'claude-3-5-haiku@20241022'

class ClaudeService:
    """
    Service for interacting with Anthropic's Claude API.
    """
    
    def __init__(self):
        """Initialize the Claude service with API credentials."""
        self.api_key = settings.ANTHROPIC_API_KEY
        self.client = anthropic.Anthropic(api_key=self.api_key)
        
    def get_completion(self, prompt: str, temperature: float = 0.2, max_tokens: int = 2000) -> str:
        """
        Get a completion from Claude for the given prompt.
        
        Args:
            prompt: The prompt to send to Claude
            temperature: Controls randomness. Values closer to 0 make the output more deterministic
            max_tokens: Maximum number of tokens to generate
            
        Returns:
            str: The completed text from Claude
        """
        logger.info("Sending prompt to Claude")
        
        try:
            response = self.client.messages.create(
                model=ANTHROPIC_MODEL,
                max_tokens=max_tokens,
                temperature=temperature,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            
            logger.info("Received response from Claude")
            return response.content[0].text
            
        except Exception as e:
            logger.error(f"Error getting completion from Claude: {str(e)}")
            return f"Error: {str(e)}"
    
    def get_structured_output(self, prompt: str, output_schema: Dict[str, Any], temperature: float = 0.1) -> Dict[str, Any]:
        """
        Get structured JSON output from Claude based on a schema.
        
        Args:
            prompt: The prompt to send to Claude
            output_schema: JSON schema defining the expected output format
            temperature: Controls randomness. Values closer to 0 make the output more deterministic
            
        Returns:
            Dict: The structured output from Claude
        """
        logger.info("Sending structured output prompt to Claude")
        
        system_prompt = f"""
        You are a helpful AI assistant that provides information in a structured format.
        Your response should be valid JSON that conforms to the following schema:
        
        {output_schema}
        
        Don't include any explanations or conversation, just output valid JSON.
        """
        
        try:
            response = self.client.messages.create(
                model=ANTHROPIC_MODEL,
                temperature=temperature,
                system=system_prompt,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            
            logger.info("Received structured response from Claude")
            
            # In a real implementation, you would parse this response as JSON
            # This is simplified for the example
            result = response.content[0].text
            
            # In a real implementation, validate the response against the schema
            return result
            
        except Exception as e:
            logger.error(f"Error getting structured output from Claude: {str(e)}")
            return {"error": str(e)}
    
    def get_llm(self, temperature: float = 0.2) -> CrewClaude:
        """
        Get a Claude LLM instance configured for use with CrewAI.
        
        Args:
            temperature: Controls randomness. Values closer to 0 make the output more deterministic
            
        Returns:
            CrewClaude: A CrewAI-compatible Claude LLM instance
        """
        return CrewClaude(
            api_key=self.api_key,
            model=ANTHROPIC_MODEL,
            temperature=temperature
        )