import os
from typing import Optional, Any
import pandas as pd

try:
    from google import genai
    USE_NEW_SDK = True
except ImportError:
    import google.generativeai as genai
    USE_NEW_SDK = False


class InsightGenerator:
    """
    Synthesizes raw SQL query execution results into concise, executive-level
    business insights using Google Gemini.
    """
    def __init__(self, api_key: Optional[str] = None, model_name: str = "gemini-3.6-flash"):
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY environment variable is missing.")
        
        self.model_name = model_name
        if USE_NEW_SDK:
            self.client = genai.Client(api_key=self.api_key)
        else:
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel(self.model_name)

    def generate_insight(self, question: str, sql_query: str, query_result: Any) -> str:
        """
        Generates narrative insights based on user question and SQL query results.
        """
        if isinstance(query_result, pd.DataFrame):
            result_str = query_result.to_markdown(index=False)
        else:
            result_str = str(query_result)

        prompt = f"""
You are a Lead Business Intelligence Analyst presenting findings to executive leadership.

### User Question:
"{question}"

### SQL Executed:
`{sql_query}`

### Query Results:
{result_str}

### Instructions:
1. Provide a direct, concise answer in 1-2 sentences.
2. Summarize key numeric highlights or takeaways.
3. Keep the tone professional, clear, and actionable. Avoid meta-commentary or repeating raw system details unnecessarily.

Executive Summary:
"""
        if USE_NEW_SDK:
            chat = self.client.chats.create(model=self.model_name)
            response = chat.send_message(prompt)
            return response.text.strip()
        else:
            response = self.model.generate_content(prompt)
            return response.text.strip()


if __name__ == "__main__":
    print("InsightGenerator module ready.")