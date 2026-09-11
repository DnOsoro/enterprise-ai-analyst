import os
import duckdb
import pandas as pd
from typing import Dict, Any, Tuple, Union

class DatasetIngestionEngine:
    """
    Handles loading CSV, Parquet, or pandas DataFrames into an in-memory DuckDB database
    and extracts metadata required for dynamic schema formatting.
    """
    def __init__(self, db_connection: duckdb.DuckDBPyConnection = None):
        self.conn = db_connection or duckdb.connect(database=":memory:")

    def register_dataset(self, data_input: Union[str, pd.DataFrame], table_name: str = "uploaded_dataset") -> Dict[str, Any]:
        """
        Registers a file path (CSV/Parquet) or pandas DataFrame into DuckDB and extracts schema metadata.
        """
        if isinstance(data_input, pd.DataFrame):
            df = data_input
        elif isinstance(data_input, str):
            if not os.path.exists(data_input):
                raise FileNotFoundError(f"File not found: {data_input}")
            
            ext = os.path.splitext(data_input)[1].lower()
            if ext == ".csv":
                df = pd.read_csv(data_input)
            elif ext in [".parquet", ".pq"]:
                df = pd.read_parquet(data_input)
            else:
                raise ValueError(f"Unsupported file format: {ext}")
        else:
            raise TypeError("data_input must be a file path string or a pandas DataFrame.")

        # Register DataFrame in DuckDB
        self.conn.register(table_name, df)

        # Extract schema metadata
        schema_df = self.conn.execute(f"DESCRIBE {table_name}").df()
        row_count = self.conn.execute(f"SELECT COUNT(*) FROM {table_name}").fetchone()[0]

        columns_meta = []
        for _, row in schema_df.iterrows():
            col_name = row["column_name"]
            data_type = row["column_type"]
            
            # Fetch sample values
            sample_query = f"SELECT DISTINCT \"{col_name}\" FROM {table_name} WHERE \"{col_name}\" IS NOT NULL LIMIT 3"
            samples = [str(val[0]) for val in self.conn.execute(sample_query).fetchall()]
            
            columns_meta.append({
                "column_name": col_name,
                "data_type": data_type,
                "samples": samples
            })

        return {
            "table_name": table_name,
            "row_count": row_count,
            "columns": columns_meta
        }

    def execute_query(self, sql_query: str) -> Tuple[bool, Union[pd.DataFrame, str]]:
        """
        Executes a SQL query in DuckDB and returns (success_flag, DataFrame_or_error_message).
        """
        try:
            result_df = self.conn.execute(sql_query).df()
            return True, result_df
        except Exception as e:
            return False, str(e)


if __name__ == "__main__":
    print("DatasetIngestionEngine ready.")