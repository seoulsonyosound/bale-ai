import streamlit as st


def show_about(assets):
    """
    Renders the About Page detailing project parameters, technologies, and metadata.
    """
    st.markdown("<h1 style='margin-bottom:5px;'>About Project</h1>", unsafe_allow_html=True)
    st.markdown(
        "<p style='font-size:16px; color:#6C757D; margin-bottom:25px;'>"
        "Technical architecture briefings, machine learning pipelines, and developer metadata.</p>",
        unsafe_allow_html=True,
    )

    # ── Project Overview card ─────────────────────────────────────────────────
    st.markdown(
        """
        <div class="glass-card">
            <h3 style="margin-top:0; color:#0F172A;">Project Overview &amp; Objectives</h3>
            <p style="line-height:1.6; font-size:14px; color:#495057;">
                The pricing and valuation of residential estates in urban environments is frequently
                complicated by speculative listings, geographic density, and highly unstructured
                property description postings.
                <b>BaleAI</b> addresses this valuation discrepancy by processing historical housing
                listings in metropolitan areas using a high-precision, tuned ensemble regressor.
            </p>
            <p style="line-height:1.6; font-size:14px; color:#495057; font-weight:600; margin-bottom:8px;">
                Core Objectives:
            </p>
            <ol style="line-height:1.6; font-size:14px; color:#495057; padding-left:20px; margin-top:0;">
                <li style="margin-bottom:6px;">
                    <b>Valuation Precision:</b> Implement a regression pipeline matching raw listings
                    with transaction-grade pricing estimates (R&sup2; accuracy of <b>98.09%</b>).
                </li>
                <li style="margin-bottom:6px;">
                    <b>Feature Extraction:</b> Automate regex patterns and spatial mappings to convert
                    description texts and coordinates into structured indicators.
                </li>
                <li style="margin-bottom:6px;">
                    <b>Academic Integrity:</b> Align the project with capstone requirements by
                    establishing a multi-class pricing category demo backed by confusion matrices.
                </li>
                <li style="margin-bottom:6px;">
                    <b>Production Architecture:</b> Deploy a modular codebase capable of low-latency
                    local execution and seamless cloud integration.
                </li>
            </ol>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ── 2-Column layout ───────────────────────────────────────────────────────
    col_flow, col_tech = st.columns([0.65, 0.35])

    with col_flow:
        st.markdown(
            """
            <div class="glass-card" style="height:480px; overflow-y:auto;">
                <h3 style="margin-top:0; color:#0F172A;">Machine Learning Lifecycle</h3>
                <p style="font-size:14px; color:#495057; margin-bottom:12px;">
                    Our processing workflow strictly avoids data leakage and ensures maximum generalizability:
                </p>
                <ul style="line-height:1.6; font-size:13.5px; color:#495057; padding-left:20px;">
                    <li style="margin-bottom:8px;"><b>Data Ingestion:</b> Read text and tabular features.
                        Maps &lsquo;na&rsquo; string patterns to standard NaN null definitions.</li>
                    <li style="margin-bottom:8px;"><b>Preprocessing &amp; Cleaning:</b> Strip formatting
                        commas from targets, convert numeric variables, and remove duplicate rows.</li>
                    <li style="margin-bottom:8px;"><b>Imputation:</b> Imputes numerical fields with
                        train-set medians and categoricals with modes, adding binary missing flags.</li>
                    <li style="margin-bottom:8px;"><b>Outlier Trimming:</b> Applies Z-score filtering
                        (|Z|&nbsp;&gt;&nbsp;3.0) to trim anomalous listings without dropping valid
                        high-value homes.</li>
                    <li style="margin-bottom:8px;"><b>Feature Engineering:</b> Computes property age,
                        sums room counts, tags Condo vs. House indicators, and extracts municipal cities
                        from locations.</li>
                    <li style="margin-bottom:8px;"><b>Categorical Encoding:</b> Applies Label Encoding to
                        Location classes to retain structure without high-dimensional one-hot expansion.</li>
                    <li style="margin-bottom:8px;"><b>Scaling:</b> Fits a MinMax mapping to compress
                        features within a standard interval [0,&nbsp;1].</li>
                    <li style="margin-bottom:8px;"><b>XGBoost Regression:</b> Runs predictions via
                        decision trees with gradient boosting, yielding standard deviation margins.</li>
                </ul>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col_tech:
        tech_stack = [
            ("Python 3.12",    "Core programming runtime"),
            ("Streamlit 1.35", "Interactive UI frontend"),
            ("XGBoost",        "Boosting regressor engine"),
            ("Scikit-Learn",   "Scaler, Encoder, & Evaluators"),
            ("Pandas",         "Data cleaning & manipulations"),
            ("NumPy",          "Mathematical operations"),
            ("Plotly",         "Interactive graphics & charts"),
            ("Joblib",         "Pickle model serialization"),
            ("Google Colab",   "Initial model exploration"),
        ]

        # Build badge HTML using plain string concatenation (no f-string)
        # to avoid curly-brace conflicts with CSS values like rgba(...)
        badge_style = (
            "background:rgba(13,110,253,0.06);"
            "padding:8px 12px;"
            "border-radius:6px;"
            "border-left:3px solid #0D6EFD;"
            "margin-bottom:8px;"
        )
        name_style  = "font-weight:600; font-size:13px; color:#0F172A;"
        desc_style  = "font-size:11px; color:#6C757D; margin-top:2px;"

        badges_html = ""
        for name, desc in tech_stack:
            badges_html += (
                '<div style="' + badge_style + '">'
                '<div style="' + name_style + '">' + name + '</div>'
                '<div style="' + desc_style + '">' + desc + '</div>'
                '</div>'
            )

        card_style = (
            "background:#FFFFFF;"
            "border-radius:12px;"
            "border:1px solid #E2E8F0;"
            "padding:20px;"
            "box-shadow:0 1px 3px rgba(0,0,0,0.05);"
            "height:480px;"
            "overflow-y:auto;"
        )
        heading_style = (
            "margin-top:0;"
            "margin-bottom:16px;"
            "color:#0F172A;"
            "font-size:16px;"
            "font-family:Inter,sans-serif;"
        )

        tech_html = (
            '<div style="' + card_style + '">'
            '<h3 style="' + heading_style + '">Technologies Used</h3>'
            + badges_html +
            '</div>'
        )
        st.markdown(tech_html, unsafe_allow_html=True)

    # ── Developer Section ─────────────────────────────────────────────────────
    st.markdown(
        """
        <div class="glass-card">
            <h3 style="margin-top:0; color:#0F172A;">Developer Metadata</h3>
            <p style="line-height:1.6; font-size:14px; color:#495057;">
                This House Price Prediction application was developed as a project in
                <b>Image Processing and Machine Learning Life Cycle Workshop</b>.
            </p>
            <ul style="line-height:1.9; font-size:14px; color:#495057; padding-left:20px; margin-top:12px;">
                <li style="margin-bottom:4px;">
                    <b>Developers:</b> Theeanna Jether D. Alejos, Stephany Ann Dela Pe&ntilde;a, Graciella Pastoral
                </li>
                <li style="margin-bottom:4px;"><b>Section:</b> BSIT 4A</li>
                <li style="margin-bottom:4px;"><b>Institution:</b> University of the Assumption</li>
                <li style="margin-bottom:4px;"><b>Date:</b> July 21, 2026</li>
            </ul>
        </div>
        """,
        unsafe_allow_html=True,
    )
