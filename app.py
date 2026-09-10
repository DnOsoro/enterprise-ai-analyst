import os
import pandas as pd
import streamlit as st
from orchestrator import EnterpriseAIAnalyst

# Configure clean visual presentation
st.set_page_config(
    page_title="Enterprise Data Analytics Engine",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Minimal CSS adjustments for executive UI polish
st.markdown("""
    <style>
    .stApp {
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    }
    .metric-card {
        background-color: #f8f9fa;
        border: 1px solid #e9ecef;
        border-radius: 6px;
        padding: 16px;
        margin-bottom: 12px;
    }
    .metric-title {
        font-size: 0.85rem;
        color: #6c757d;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        font-weight: 600;
    }
    .metric-value {
        font-size: 1.5rem;
        font-weight: 700;
        color: #212529;
    }
    </style>
""", unsafe_allow_html=True)

# Application state initialization
if "analyst" not in st.session_state:
    st.session_state.analyst = None

if "dataset_loaded" not in st.session_state:
    st.session_state.dataset_loaded = False

if "last_response" not in st.session_state:
    st.session_state.last_response = None

# Header Block
st.title("Enterprise AI Analytics Engine")
st.caption("High-performance natural language text-to-SQL translation, safe in-memory analytics, and automated reporting.")
st.divider()

# Sidebar Setup & Controls
with st.sidebar:
    st.subheader("Data Connection & Settings")
    
    # Secure API Key Handling
    env_key = os.getenv("GEMINI_API_KEY")
    
    if env_key:
        st.success("Gemini API Key detected in system environment.")
    else:
        user_key = st.text_input(
            "Gemini API Key",
            type="password",
            placeholder="Enter API Key...",
            help="Key is kept safely in memory for the active session."
        )
        if user_key:
            os.environ["GEMINI_API_KEY"] = user_key

    uploaded_file = st.file_uploader("Upload Dataset (CSV or Parquet)", type=["csv", "parquet", "pq"])

    if uploaded_file is not None:
        try:
            if uploaded_file.name.endswith(".csv"):
                df = pd.read_csv(uploaded_file)
            else:
                df = pd.read_parquet(uploaded_file)

            st.session_state.analyst = EnterpriseAIAnalyst()
            st.session_state.analyst.load_dataset(df)
            st.session_state.dataset_loaded = True
            st.session_state.last_response = None
            st.success(f"Dataset successfully registered: {uploaded_file.name}")
        except Exception as e:
            st.error(f"Failed to load dataset: {str(e)}")

# Workspace Interface
if not st.session_state.dataset_loaded:
    st.info("No active dataset connected. Upload a CSV or Parquet file in the sidebar, or load the default enterprise sales sample dataset below.")
    
    if st.button("Load Standard Sample Dataset"):
        sample_df = pd.DataFrame([
            {'region': 'North America', 'product': 'Cloud Suite', 'revenue': 45000.0, 'deal_size': 3},
            {'region': 'Europe', 'product': 'Security Pack', 'revenue': 28000.0, 'deal_size': 2},
            {'region': 'North America', 'product': 'Security Pack', 'revenue': 62000.0, 'deal_size': 5},
            {'region': 'Asia Pacific', 'product': 'Cloud Suite', 'revenue': 89000.0, 'deal_size': 8}
        ])
        st.session_state.analyst = EnterpriseAIAnalyst()
        st.session_state.analyst.load_dataset(sample_df)
        st.session_state.dataset_loaded = True
        st.rerun()

else:
    # Metadata Overview Panel
    meta = st.session_state.analyst.current_metadata
    m_col1, m_col2, m_col3 = st.columns(3)
    
    with m_col1:
        st.markdown(f'<div class="metric-card"><div class="metric-title">Table Name</div><div class="metric-value">{meta["table_name"]}</div></div>', unsafe_allow_html=True)
    with m_col2:
        st.markdown(f'<div class="metric-card"><div class="metric-title">Row Count</div><div class="metric-value">{meta["row_count"]:,}</div></div>', unsafe_allow_html=True)
    with m_col3:
        st.markdown(f'<div class="metric-card"><div class="metric-title">Columns</div><div class="metric-value">{len(meta["columns"])}</div></div>', unsafe_allow_html=True)

    st.write("")
    
    # Query Form
    with st.form(key="query_form"):
        user_question = st.text_input("Analytical Query:", placeholder="e.g., What is the total revenue by product?")
        submit_button = st.form_submit_button(label="Run Analysis")

    if submit_button and user_question.strip():
        with st.spinner("Processing schema context, building query, and evaluating results..."):
            st.session_state.last_response = st.session_state.analyst.process_query(user_question)

    # Render Results Workspace
    response = st.session_state.last_response
    if response:
        st.divider()
        if not response["success"]:
            st.error(f"Query Pipeline Execution Failure: {response['error']}")
            if response["generated_sql"]:
                with st.expander("Attempted SQL Output"):
                    st.code(response["generated_sql"], language="sql")
        else:
            tab_insight, tab_data, tab_sql = st.tabs(["Executive Summary", "Result Dataset", "SQL Logic"])
            
            with tab_insight:
                st.subheader("Synthesis & Insight")
                st.write(response["insight"])

            with tab_data:
                st.subheader("Query Result Set")
                result_df = response["result_df"]
                st.dataframe(result_df, use_container_width=True)
                st.caption(f"Returned {len(result_df)} row(s).")

            with tab_sql:
                st.subheader("Generated DuckDB SQL Query")
                st.code(response["generated_sql"], language="sql")