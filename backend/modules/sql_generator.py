import os
import re
from typing import Optional

try:
    from google import genai
    USE_NEW_SDK = True
except ImportError:
    import google.generativeai as genai
    USE_NEW_SDK = False


class SQLGenerator:
    """
    Translates natural language questions into valid DuckDB SQL queries using Google Gemini.
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

    def generate_sql(self, question: str, schema_context: str) -> str:
        """
        Sends the question and dynamic schema context to Gemini to generate DuckDB SQL.
        """
        prompt = f"""
You are an expert SQL Data Analyst. Your task is to generate valid DuckDB SQL based on the provided dataset schema.

### Database Schema Context:
{schema_context}

### User Question:
"{question}"

### Instructions:
1. Return ONLY the raw SQL query. Do not wrap it in Markdown code blocks (e.g., no ```sql).
2. Do NOT write explanations, markdown text, or greetings.
3. Use exact column names provided in the schema context.
4. Ensure the output is a single read-only SELECT statement.

SQL Query:
"""
        if USE_NEW_SDK:
            chat = self.client.chats.create(model=self.model_name)
            response = chat.send_message(prompt)
            raw_text = response.text.strip()
        else:
            response = self.model.generate_content(prompt)
            raw_text = response.text.strip()
        
        # Clean markdown code formatting if present
        clean_sql = re.sub(r"^```(?:sql)?\s*", "", raw_text, flags=re.IGNORECASE)
        clean_sql = re.sub(r"\s*```$", "", clean_sql).strip()
        
        return clean_sql


if __name__ == "__main__":
    print("SQLGenerator module ready.")