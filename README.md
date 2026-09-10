# Enterprise AI Analytics Engine

An AI-powered analytics engine that allows business users to ask questions about structured data using natural language.

The system converts business questions into SQL, validates the generated SQL against security and execution rules, runs approved queries using DuckDB, and turns the results into concise business insights.

The project demonstrates how modern data engineering, analytics engineering, and LLM capabilities can be combined into a controlled Text-to-SQL workflow.

---

## Overview

Traditional analytics workflows often require users to understand SQL or depend on analysts to answer every business question.

This project provides a controlled interface between business users and structured data.

```text
Business Question
       |
       v
   LLM / Gemini
       |
       v
   SQL Generation
       |
       v
 SQL Validation
   & Guardrails
       |
       v
 DuckDB Execution
       |
       v
 Query Results
       |
       v
 Executive Insights
