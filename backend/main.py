import os
import io
import pandas as pd
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from backend.orchestrator import EnterpriseAIAnalyst
from backend.security.anonymizer import extract_safe_schema_context, sanitize_output_text

app = FastAPI(
    title="Enterprise AI Analytics Engine API",
    description="FastAPI Backend serving Text-to-SQL execution, guardrails, and Recharts spec generation."
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

analyst_instance = EnterpriseAIAnalyst()

class QueryRequest(BaseModel):
    question: str

@app.get("/")
def health_check():
    return {"status": "healthy", "engine": "Enterprise AI Analytics Backend"}

@app.post("/api/upload")
async def upload_dataset(file: UploadFile = File(...)):
    contents = await file.read()
    filename = file.filename.lower()
    
    try:
        if filename.endswith(".csv"):
            df = pd.read_csv(io.BytesIO(contents))
        elif filename.endswith((".xlsx", ".xls")):
            df = pd.read_excel(io.BytesIO(contents))
        elif filename.endswith(".json"):
            df = pd.read_json(io.BytesIO(contents))
        elif filename.endswith((".parquet", ".pq")):
            df = pd.read_parquet(io.BytesIO(contents))
        else:
            raise HTTPException(status_code=400, detail="Unsupported file format.")
            
        analyst_instance.load_dataset(df)
        safe_schema = extract_safe_schema_context(df)
        
        return {
            "status": "success",
            "filename": file.filename,
            "rows": len(df),
            "columns": list(df.columns),
            "safe_schema_context": safe_schema
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to process dataset: {str(e)}")

@app.post("/api/query")
async def process_analytical_query(payload: QueryRequest):
    if not analyst_instance.current_metadata:
        raise HTTPException(status_code=400, detail="No active dataset registered. Upload a file first.")
        
    response = analyst_instance.process_query(payload.question)
    
    if not response["success"]:
        return {
            "success": False,
            "error": response["error"],
            "generated_sql": response.get("generated_sql", "")
        }
        
    clean_insight = sanitize_output_text(response["insight"])
    result_df = response["result_df"]
    
    return {
        "success": True,
        "insight": clean_insight,
        "generated_sql": response["generated_sql"],
        "data": result_df.to_dict(orient="records"),
        "row_count": len(result_df)
    }