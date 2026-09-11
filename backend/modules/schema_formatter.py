from typing import Dict, Any

class SchemaFormatter:
    """
    Formats schema metadata discovered by DatasetIngestionEngine into a clean,
    structured text representation optimized for LLM prompt injection.
    """
    
    @staticmethod
    def format_schema_for_llm(metadata: Dict[str, Any], dialect: str = "DuckDB") -> str:
        """
        Converts raw schema metadata dictionary into a standard prompt string.
        """
        if not metadata or "table_name" not in metadata:
            return "No valid schema provided."

        table_name = metadata["table_name"]
        row_count = metadata.get("row_count", "Unknown")
        columns = metadata.get("columns", [])

        schema_lines = [
            f"Target SQL Dialect: {dialect}",
            f"Table Name: {table_name}",
            f"Total Rows: {row_count}",
            "Columns & Data Types:"
        ]

        for col in columns:
            name = col.get("column_name")
            dtype = col.get("data_type")
            samples = col.get("samples", [])
            sample_str = ", ".join([f"'{s}'" for s in samples]) if samples else "N/A"
            
            schema_lines.append(f"  - {name} ({dtype}) | Example values: [{sample_str}]")

        return "\n".join(schema_lines)


if __name__ == "__main__":
    print("SchemaFormatter module ready.")