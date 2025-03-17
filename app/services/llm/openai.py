"""
OpenAI service for interacting with OpenAI's API.
"""
import os
import logging
from typing import Dict, Any, List, Optional
import openai
from crewai.agents.llms.openai import OpenAI as CrewOpenAI

from app.config import settings

logger = logging.getLogger(__name__)

class OpenAIService:
    """
    Service for interacting with OpenAI's API.
    """
    
    def __init__(self):
        """Initialize the OpenAI service with API credentials."""
        self.api_key = settings.OPENAI_API_KEY
        self.client = openai.OpenAI(api_key=self.api_key)
        
    def get_completion(self, prompt: str, model: str = "gpt-4-turbo", temperature: float = 0.2, max_tokens: int = 2000) -> str:
        """
        Get a completion from OpenAI for the given prompt.
        
        Args:
            prompt: The prompt to send to OpenAI
            model: The OpenAI model to use
            temperature: Controls randomness. Values closer to 0 make the output more deterministic
            max_tokens: Maximum number of tokens to generate
            
        Returns:
            str: The completed text from OpenAI
        """
        logger.info(f"Sending prompt to OpenAI using model {model}")
        
        try:
            response = self.client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": prompt}
                ],
                temperature=temperature,
                max_tokens=max_tokens
            )
            
            logger.info("Received response from OpenAI")
            return response.choices[0].message.content
            
        except Exception as e:
            logger.error(f"Error getting completion from OpenAI: {str(e)}")
            return f"Error: {str(e)}"
    
    def get_structured_output(self, prompt: str, output_schema: Dict[str, Any], model: str = "gpt-4-turbo", temperature: float = 0.1) -> Dict[str, Any]:
        """
        Get structured JSON output from OpenAI based on a schema.
        
        Args:
            prompt: The prompt to send to OpenAI
            output_schema: JSON schema defining the expected output format
            model: The OpenAI model to use
            temperature: Controls randomness. Values closer to 0 make the output more deterministic
            
        Returns:
            Dict: The structured output from OpenAI
        """
        logger.info(f"Sending structured output prompt to OpenAI using model {model}")
        
        system_prompt = f"""
        You are a helpful AI assistant that provides information in a structured format.
        Your response should be valid JSON that conforms to the following schema:
        
        {output_schema}
        
        Don't include any explanations or conversation, just output valid JSON.
        """
        
        try:
            response = self.client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt}
                ],
                temperature=temperature
            )
            
            logger.info("Received structured response from OpenAI")
            
            # In a real implementation, you would parse this response as JSON
            # This is simplified for the example
            result = response.choices[0].message.content
            
            # In a real implementation, validate the response against the schema
            return result
            
        except Exception as e:
            logger.error(f"Error getting structured output from OpenAI: {str(e)}")
            return {"error": str(e)}
    
    def get_llm(self, model: str = "gpt-4-turbo", temperature: float = 0.2) -> CrewOpenAI:
        """
        Get an OpenAI LLM instance configured for use with CrewAI.
        
        Args:
            model: The OpenAI model to use
            temperature: Controls randomness. Values closer to 0 make the output more deterministic
            
        Returns:
            CrewOpenAI: A CrewAI-compatible OpenAI LLM instance
        """
        return CrewOpenAI(
            api_key=self.api_key,
            model=model,
            temperature=temperature
        )
