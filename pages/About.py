import streamlit as st

def show_about(assets):
    """
    Renders the About Page detailing project parameters, technologies, and metadata.
    """
    st.markdown("<h1 style='margin-bottom:5px;'>About Project</h1>", unsafe_allow_html=True)
    st.markdown("<p style='font-size:16px; color:#6C757D; margin-bottom:25px;'>Technical architecture briefings, machine learning pipelines, and developer metadata.</p>", unsafe_allow_html=True)
    
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    st.markdown("<h3>Project Overview & Objectives</h3>", unsafe_allow_html=True)
    st.markdown("""
    The pricing and valuation of residential estates in urban environments is frequently complicated by speculative listings, geographic density, 
    and highly unstructured property description postings. 
    <b>BaleAI</b> addresses this valuation discrepancy by processing historical housing listings in metropolitan areas using a high-precision, 
    tuned ensemble regressor.
    
    <b>Core Objectives:</b>
    1. <b>Valuation Precision:</b> Implement a regression pipeline matching raw listings with transaction-grade pricing estimates (R² accuracy of <b>98.09%</b>).
    2. <b>Feature Extraction:</b> Automate regex patterns and spatial mappings to convert description texts and coordinates into structured indicators.
    3. <b>Academic Integrity:</b> Align the project with capstone requirements by establishing a multi-class pricing category demo backed by confusion matrices.
    4. <b>Production Architecture:</b> Deploy a modular codebase capable of low-latency local execution and seamless cloud integration.
    """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
    
    # 2-Column: Workflow vs Technologies
    col_flow, col_tech = st.columns([0.65, 0.35])
    
    with col_flow:
        st.markdown("<div class='glass-card' style='height: 480px;'>", unsafe_allow_html=True)
        st.markdown("<h3>Machine Learning Lifecycle</h3>", unsafe_allow_html=True)
        st.markdown("""
        Our processing workflow strictly avoids data leakage and ensures maximum generalizability:
        * <b>Data Ingestion:</b> Read text and tabular features. Maps 'na' string patterns to standard NaN null definitions.
        * <b>Preprocessing & Cleaning:</b> Strip formatting commas from targets, convert numeric variables, and remove duplicate rows.
        * <b>Imputation:</b> Imputes numerical fields with train-set medians and categoricals with modes, adding binary missing flags.
        * <b>Outlier Trimming:</b> Applies Z-score filtering (|Z| > 3.0) to trim anomalous/speculative pricing listings without dropping valid high-value homes.
        * <b>Feature Engineering:</b> Computes property age, sums room counts, tags Condo vs. House indicators, and extracts municipal cities from locations.
        * <b>Categorical Encoding:</b> Applies Label Encoding to Location classes to retain structure without high-dimensional one-hot expansion.
        * <b>Scaling:</b> Fits a MinMax mapping to compress features within a standard interval [0, 1].
        * <b>XGBoost Regression:</b> Runs predictions via decision trees with gradient boosting, yielding standard deviation margins.
        """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
        
    with col_tech:
        st.markdown("<div class='glass-card' style='height: 480px;'>", unsafe_allow_html=True)
        st.markdown("<h3>Technologies Used</h3>", unsafe_allow_html=True)
        
        # Draw tech badges
        tech_stack = [
            ("Python 3.12", "Core programming runtime"),
            ("Streamlit 1.35", "Interactive UI frontend"),
            ("XGBoost", "Boosting regressor engine"),
            ("Scikit-Learn", "Scaler, Encoder, & Evaluators"),
            ("Pandas", "Data cleaning & manipulations"),
            ("NumPy", "Mathematical operations"),
            ("Plotly", "Interactive graphics & charts"),
            ("Joblib", "Pickle model serialization"),
            ("Google Colab", "Initial model exploration")
        ]
        
        for tech, desc in tech_stack:
            st.markdown(f"""
            <div style="background-color:rgba(13,110,253,0.05); padding: 8px 12px; border-radius: 6px; border-left: 3px solid #0D6EFD; margin-bottom:8px; font-size:12.5px;">
                <span style="font-weight:600; color:#212529;">{tech}</span>
                <div style="font-size:10px; color:#6C757D; margin-top:2px;">{desc}</div>
            </div>
            """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
        
    # Developer Section
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    st.markdown("<h3>Developer Metadata</h3>", unsafe_allow_html=True)
    st.markdown("""
    This House Price Prediction application was developed as a Capstone / Thesis Research Project.
    
    * <b>Institution:</b> CG Seminar Advanced Machine Learning Lab
    * <b>Academic Track:</b> Artificial Intelligence & Full Stack Engineering
    * <b>Supervising Panel:</b> Senior Data Science Research Board
    * <b>Academic Support:</b> support@baleai.example.com
    """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
