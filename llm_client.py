"""
LLM Client module to query Groq, Google Gemini, and Cohere APIs.
"""

import os
from typing import Optional

# Import LLM libraries
try:
    from groq import Groq
except ImportError:
    Groq = None

try:
    import google.generativeai as genai
except ImportError:
    genai = None

try:
    import cohere
except ImportError:
    cohere = None


SYSTEM_PROMPT = """You are an expert product analyst. When given a product category query, 
provide a ranked list of the top 5 brands or products in that category, ordered by their 
prominence in AI training data and market visibility.

Format your response as a numbered list with brief reasons:
1. Brand Name - reason for ranking
2. Brand Name - reason for ranking
... and so on

Be concise and factual."""


class GroqClient:
    """Client for Groq API."""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("GROQ_API_KEY")
        if not self.api_key:
            raise ValueError("GROQ_API_KEY not found in environment variables")
        self.client = Groq(api_key=self.api_key) if Groq else None
    
    def query(self, user_query: str) -> str:
        """Query Groq API."""
        if not self.client:
            return "Groq library not installed"
        
        try:
            message = self.client.chat.completions.create(
                model="mixtral-8x7b-32768",
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": user_query}
                ],
                max_tokens=1024,
                temperature=0.7
            )
            return message.choices[0].message.content
        except Exception as e:
            return f"Error querying Groq: {str(e)}"


class GeminiClient:
    """Client for Google Gemini API."""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("GOOGLE_API_KEY")
        if not self.api_key:
            raise ValueError("GOOGLE_API_KEY not found in environment variables")
        
        if genai:
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel("gemini-pro")
        else:
            self.model = None
    
    def query(self, user_query: str) -> str:
        """Query Google Gemini API."""
        if not self.model:
            return "Google Generative AI library not installed"
        
        try:
            full_prompt = f"{SYSTEM_PROMPT}\n\nUser Query: {user_query}"
            response = self.model.generate_content(full_prompt)
            return response.text
        except Exception as e:
            return f"Error querying Gemini: {str(e)}"


class CohereClient:
    """Client for Cohere API."""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("COHERE_API_KEY")
        if not self.api_key:
            raise ValueError("COHERE_API_KEY not found in environment variables")
        
        if cohere:
            self.client = cohere.Client(api_key=self.api_key)
        else:
            self.client = None
    
    def query(self, user_query: str) -> str:
        """Query Cohere API."""
        if not self.client:
            return "Cohere library not installed"
        
        try:
            response = self.client.chat(
                model="command-r",
                message=user_query,
                preamble=SYSTEM_PROMPT
            )
            return response.text
        except Exception as e:
            return f"Error querying Cohere: {str(e)}"


def query_all_llms(user_query: str) -> dict:
    """
    Query all three LLMs in parallel and return results.
    
    Args:
        user_query (str): The product category query
    
    Returns:
        dict: Dictionary with LLM names as keys and responses as values
    """
    results = {}
    
    # Query Groq
    try:
        groq_client = GroqClient()
        results['Groq'] = groq_client.query(user_query)
    except Exception as e:
        results['Groq'] = f"Failed to initialize Groq: {str(e)}"
    
    # Query Gemini
    try:
        gemini_client = GeminiClient()
        results['Gemini'] = gemini_client.query(user_query)
    except Exception as e:
        results['Gemini'] = f"Failed to initialize Gemini: {str(e)}"
    
    # Query Cohere
    try:
        cohere_client = CohereClient()
        results['Cohere'] = cohere_client.query(user_query)
    except Exception as e:
        results['Cohere'] = f"Failed to initialize Cohere: {str(e)}"
    
    return results
