import duckdb
import pandas as pd
from typing import Dict, Any, Tuple
from modules.ingestion import DatasetIngestionEngine
from modules.schema_formatter import SchemaFormatter
from modules.sql_generator import SQLGenerator
from modules.guardrails import SQLGuardrails
from modules.evaluator import SQLEvaluator
from modules.insight_generator import InsightGenerator

class EnterpriseAIAnalyst:
    """
    End-to-End Orchestrator for the Enterprise AI Data Analyst.
    Handles ingestion, schema mapping, Text-to-SQL translation, security checks,
    DuckDB execution, evaluation, and natural language insight generation.
    """
    def __init__(self, model_name: str = "gemini-3.6-flash"):
        self.conn = duckdb.connect(database=":memory:")
        self.ingestion_engine = DatasetIngestionEngine(db_connection=self.conn)
        self.sql_generator = SQLGenerator(model_name=model_name)
        self.insight_generator = InsightGenerator(model_name=model_name)
        self.current_metadata = None

    def load_dataset(self, file_path_or_df) -> Dict[str, Any]:
        """
        Ingests a CSV, Parquet, or pandas DataFrame, registers it into DuckDB,
        and returns structured schema metadata.
        """
        self.current_metadata = self.ingestion_engine.register_dataset(file_path_or_df)
        return self.current_metadata

    def process_query(self, question: str) -> Dict[str, Any]:
        """
        Executes the full AI Analyst pipeline:
        NL Question -> Schema Context -> SQL Generation -> Safety Check -> Execution -> Insight Synthesis.
        """
        if not self.current_metadata:
            raise ValueError("No dataset loaded. Call load_dataset() before asking questions.")

        # 1. Format dynamic schema context for LLM
        schema_context = SchemaFormatter.format_schema_for_llm(self.current_metadata)

        # 2. Generate SQL from question
        generated_sql = self.sql_generator.generate_sql(question, schema_context)

        # 3. Security & Safety Check
        is_safe, security_msg = SQLGuardrails.validate_sql(generated_sql)
        if not is_safe:
            return {
                "success": False,
                "question": question,
                "generated_sql": generated_sql,
                "error": f"Security Guardrail Triggered: {security_msg}",
                "result_df": None,
                "insight": None
            }

        # 4. Execute SQL in DuckDB engine
        exec_success, result_or_error = self.ingestion_engine.execute_query(generated_sql)
        if not exec_success:
            return {
                "success": False,
                "question": question,
                "generated_sql": generated_sql,
                "error": f"Execution Error: {result_or_error}",
                "result_df": None,
                "insight": None
            }

        result_df = result_or_error

        # 5. Synthesize Executive Insights
        insight = self.insight_generator.generate_insight(question, generated_sql, result_df)

        return {
            "success": True,
            "question": question,
            "generated_sql": generated_sql,
            "result_df": result_df,
            "insight": insight,
            "error": None
        }


if __name__ == "__main__":
    print("EnterpriseAIAnalyst Orchestrator ready.")