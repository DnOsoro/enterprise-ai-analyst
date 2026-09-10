# Enterprise AI Analytics Engine

An enterprise-ready Data Analytics platform that translates natural language business questions into precise, read-only SQL queries, executes them in-memory, and synthesizes executive insights.

Built using Python 3.12, DuckDB, Google Gemini (`gemini-3.6-flash`), and Streamlit.

---

## Architectural Overview

The system operates on a decoupled modular architecture designed for high security, data privacy, and sub-second analytical queries:

1. **Dataset Ingestion Engine (`modules/ingestion.py`)**  
   Accepts CSV or Parquet inputs and registers them directly into an in-memory DuckDB instance without persistent file writes.

2. **Schema Metadata Formatter (`modules/schema_formatter.py`)**  
   Dynamically extracts table names, column data types, and sample non-null records to feed precise schema context into the LLM.

3. **Text-to-SQL Generator (`modules/sql_generator.py`)**  
   Uses Google Gemini (`gemini-3.6-flash`) to generate strict, dialect-aware DuckDB SQL queries without wrapping code blocks.

4. **Security & SQL Guardrails (`modules/guardrails.py`)**  
   Validates generated SQL before execution to ensure only read-only `SELECT` statements run, blocking any structural changes (`DROP`, `DELETE`, `INSERT`, `UPDATE`).

5. **Executive Insight Synthesizer (`modules/insight_generator.py`)**  
   Translates raw SQL query result sets back into concise, 1-2 sentence executive business summaries.

6. **Unified Orchestration Engine (`orchestrator.py`)**  
   Coordinates end-to-end data flow between ingestion, validation, execution, and presentation layers.

---

## System Workflow
