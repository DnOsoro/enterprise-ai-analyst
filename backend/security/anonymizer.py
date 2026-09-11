import re
import pandas as pd

def extract_safe_schema_context(df: pd.DataFrame) -> str:
    """
    Enforces privacy rule: Sends ONLY the first 3 rows of a dataset 
    to the external LLM to prevent data exposure.
    """
    sample_df = df.head(3)
    schema_info = []
    
    for col in df.columns:
        samples = sample_df[col].tolist()
        clean_samples = [re.sub(r'[\w\.-]+@[\w\.-]+\.\w+', '[REDACTED_EMAIL]', str(s)) for s in samples]
        schema_info.append(f"Column: '{col}' ({df[col].dtype}) | Sample Values (Max 3): {clean_samples}")
        
    return "\n".join(schema_info)

def sanitize_output_text(text: str) -> str:
    """
    Sanitizes LLM outputs against HTML/JS injection (XSS attacks) and redacts PII.
    """
    clean_text = re.sub(r'<script.*?>.*?</script>', '[BLOCKED_SCRIPT]', text, flags=re.DOTALL)
    clean_text = re.sub(r'[\w\.-]+@[\w\.-]+\.\w+', '[REDACTED_EMAIL]', clean_text)
    clean_text = re.sub(r'\b\d{3}[-.\s]?\d{3}[-.\s]?\d{4}\b', '[REDACTED_PHONE]', clean_text)
    return clean_text