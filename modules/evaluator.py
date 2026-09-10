import time
import pandas as pd
from typing import Dict, Any, Tuple, Optional

class SQLEvaluator:
    """
    Unified Evaluation Engine for evaluating LLM-generated SQL against ground truth.
    Supports both PostgreSQL and DuckDB connections.
    """
    def __init__(self, db_connection: Any, engine_type: str = "duckdb"):
        self.conn = db_connection
        self.engine_type = engine_type.lower()

    def execute_query(self, query: str) -> Tuple[bool, Optional[pd.DataFrame], Optional[str], float]:
        start_time = time.perf_counter()
        try:
            if self.engine_type == "postgres":
                df = pd.read_sql(query, self.conn)
            elif self.engine_type == "duckdb":
                df = self.conn.execute(query).df()
            else:
                raise ValueError(f"Unsupported engine type: {self.engine_type}")
            
            elapsed_time = time.perf_counter() - start_time
            return True, df, None, round(elapsed_time, 4)
        except Exception as e:
            elapsed_time = time.perf_counter() - start_time
            return False, None, str(e), round(elapsed_time, 4)

    def compare_dataframes(self, df_generated: pd.DataFrame, df_truth: pd.DataFrame) -> bool:
        if df_generated is None or df_truth is None:
            return False

        if df_generated.shape != df_truth.shape:
            return False

        try:
            df_gen_sorted = df_generated.copy()
            df_truth_sorted = df_truth.copy()
            
            df_gen_sorted.columns = [f"col_{i}" for i in range(df_gen_sorted.shape[1])]
            df_truth_sorted.columns = [f"col_{i}" for i in range(df_truth_sorted.shape[1])]

            pd.testing.assert_frame_equal(
                df_gen_sorted, 
                df_truth_sorted, 
                check_dtype=False, 
                check_exact=False, 
                atol=1e-3
            )
            return True
        except AssertionError:
            return False

    def evaluate_sample(self, question: str, generated_sql: str, ground_truth_sql: str) -> Dict[str, Any]:
        truth_ok, truth_df, truth_err, truth_time = self.execute_query(ground_truth_sql)
        if not truth_ok:
            return {
                "question": question,
                "status": "ERROR_IN_GROUND_TRUTH",
                "error": truth_err,
                "exact_match": False,
                "generated_exec_time": 0.0
            }

        gen_ok, gen_df, gen_err, gen_time = self.execute_query(generated_sql)
        if not gen_ok:
            return {
                "question": question,
                "status": "GENERATED_SQL_SYNTAX_ERROR",
                "error": gen_err,
                "exact_match": False,
                "generated_exec_time": gen_time
            }

        is_match = self.compare_dataframes(gen_df, truth_df)

        return {
            "question": question,
            "status": "SUCCESS" if is_match else "RESULT_MISMATCH",
            "exact_match": is_match,
            "generated_exec_time": gen_time,
            "truth_exec_time": truth_time,
            "error": None
        }

if __name__ == "__main__":
    print("SQLEvaluator module ready.")