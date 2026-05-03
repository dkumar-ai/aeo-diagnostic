import os
from typing import Optional

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
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("GROQ_API_KEY")
        if not self.api_key:
            raise ValueError("GROQ_API_KEY not found in environment variables")
        self.client = Groq(api_key=self.api_key) if Groq else None

    def query(self, user_query: str) -> str:
        if not self.client:
            return "Groq library not installed"
        try:
            message = self.client.chat.completions.create(
                model="llama-3.3-70b-versatile",
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
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY not found in environment variables")
        if genai:
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel("gemini-2.0-flash")
        else:
            self.model = None

    def query(self, user_query: str) -> str:
        if not self.model:
            return "Google Generative AI library not installed"
        try:
            full_prompt = f"{SYSTEM_PROMPT}\n\nUser Query: {user_query}"
            response = self.model.generate_content(full_prompt)
            return response.text
        except Exception as e:
            return f"Error querying Gemini: {str(e)}"


class CohereClient:
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("COHERE_API_KEY")
        if not self.api_key:
            raise ValueError("COHERE_API_KEY not found in environment variables")
        if cohere:
            self.client = cohere.ClientV2(api_key=self.api_key)
        else:
            self.client = None

    def query(self, user_query: str) -> str:
        if not self.client:
            return "Cohere library not installed"
        try:
            response = self.client.chat(
                model="command-a-03-2025",
                messages=[
                    {"role": "user", "content": SYSTEM_PROMPT + "\n\n" + user_query}
                ]
            )
            return response.message.content[0].text
        except Exception as e:
            return f"Error querying Cohere: {str(e)}"


def query_all_llms(user_query: str) -> dict:
    results = {}

    try:
        groq_client = GroqClient()
        results['Groq'] = groq_client.query(user_query)
    except Exception as e:
        results['Groq'] = f"Failed to initialize Groq: {str(e)}"

    try:
        gemini_client = GeminiClient()
        results['Gemini'] = gemini_client.query(user_query)
    except Exception as e:
        results['Gemini'] = f"Failed to initialize Gemini: {str(e)}"

    try:
        cohere_client = CohereClient()
        results['Cohere'] = cohere_client.query(user_query)
    except Exception as e:
        results['Cohere'] = f"Failed to initialize Cohere: {str(e)}"

    return results
