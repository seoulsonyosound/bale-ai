import streamlit as st
from utils.helpers import draw_metric_card
from utils.visualizations import plot_feature_importance

def show_dashboard(assets):
    """
    Renders the welcome dashboard landing page.
    """
    st.markdown("<h1 style='margin-bottom:5px;'>Market Dashboard</h1>", unsafe_allow_html=True)
    st.markdown("<p style='font-size:16px; color:#6C757D; margin-bottom:25px;'>BaleAI House Price Prediction and Valuation System</p>", unsafe_allow_html=True)
    
    # 1. Quick Statistics Cards in a responsive grid
    st.markdown("<h3 style='margin-bottom:15px; font-size:18px;'>Valuation Engine Statistics</h3>", unsafe_allow_html=True)
    
    # Load metadata values
    metadata = assets['metadata']
    reg_eval = metadata['regression_eval']
    
    col1, col2, col3, col4, col5, col6 = st.columns(6)
    with col1:
        draw_metric_card("Records", f"{metadata['raw_stats']['num_records_raw']:,}", "Total listing samples")
    with col2:
        draw_metric_card("Features", f"{metadata['raw_stats']['num_features_raw']}", "Input variables used")
    with col3:
        draw_metric_card("Core Model", "XGBoost", "Tuned regression trees")
    with col4:
        draw_metric_card("R² Score", f"{reg_eval['R2']*100:.2f}%", "Model accuracy fit")
    with col5:
        draw_metric_card("RMSE", f"₱{reg_eval['RMSE']/1e6:.2f}M", "Std prediction error")
    with col6:
        draw_metric_card("MAE", f"₱{reg_eval['MAE']/1e3:.0f}K", "Mean absolute error")
        
    st.markdown("<div style='margin-top: 15px;'></div>", unsafe_allow_html=True)
    
    # 2. Main content split layout
    left_col, right_col = st.columns([1.15, 0.85])
    
    with left_col:
        st.markdown("""
        <div class="glass-card" style="height: 480px; overflow: auto;">
            <h3 style="margin-top:0; color:#0F172A;">BaleAI Model Summary</h3>
            <p style="line-height:1.6; font-size:14px; color:#495057;">
                This enterprise-grade AI system is trained on vetted residential properties within the Philippines. The workflow implements robust data cleanup processes (removing commas, missing labels, and duplicate posts), handles null inputs via robust median/mode imputation, and filters outlier records via Z-scores to prevent high-end speculative listings from skewing baseline valuations.
            </p>
            <p style="line-height:1.6; font-size:14px; color:#495057;">
                <b>Feature Engineering Highlights:</b> We extract geographical indicators, age depreciation metrics, and property indicators (Condo vs. House) directly from raw description tags and location vectors.
            </p>
            <p style="line-height:1.6; font-size:14px; color:#495057;">
                <b>Modeling Benchmark:</b> The pipeline evaluated 10 standard algorithms, comparing Linear Regressors, Tree Ensembles, and Boosting models. The <b>XGBoost Regressor</b> outperformed all other algorithms, registering an outstanding test R² of <b>98.09%</b> and a Mean Absolute Percentage Error (MAPE) of <b>9.46%</b>.
            </p>
            <div style="background-color:rgba(15,23,42,0.05); padding: 12px 16px; border-radius: 8px; border-left: 4px solid #0F172A; font-size:13px; color:#334155; margin-top:15px;">
                <b>Inference Ready:</b> Predictions incorporate simulated 95% confidence intervals based on testing residuals, enabling risk assessments for mortgage and acquisition pricing.
            </div>
        </div>
        """, unsafe_allow_html=True)
        
    with right_col:
        fig_imp = plot_feature_importance(assets)
        st.plotly_chart(fig_imp, use_container_width=True)
        
    # 3. Workflow Diagram
    st.markdown("<h3 style='margin-top:20px; margin-bottom:15px; font-size:18px;'>End-to-End Prediction Workflow</h3>", unsafe_allow_html=True)
    
    workflow_html = (
        '<div class="glass-card" style="padding: 30px;">'
        '<div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap: 20px;">'
        '<!-- Step 1 -->'
        '<div style="flex:1; min-width: 180px; text-align:center; position:relative;">'
        '<div style="width:50px; height:50px; border-radius:50%; background:#E9ECEF; display:flex; align-items:center; justify-content:center; margin: 0 auto 12px auto; font-weight:700; color:#0D6EFD; border: 2px solid #0D6EFD;">1</div>'
        '<div style="font-weight:600; font-size:14px; margin-bottom:5px; color:#212529;">Data Ingestion</div>'
        '<div style="font-size:11px; color:#6C757D;">PH Houses dataset cleaned and parsed (strings, targets, coordinate bounds)</div>'
        '</div>'
        '<div style="font-size: 20px; color: #CED4DA; font-weight:bold;">&rarr;</div>'
        '<!-- Step 2 -->'
        '<div style="flex:1; min-width: 180px; text-align:center; position:relative;">'
        '<div style="width:50px; height:50px; border-radius:50%; background:#E9ECEF; display:flex; align-items:center; justify-content:center; margin: 0 auto 12px auto; font-weight:700; color:#0D6EFD; border: 2px solid #0D6EFD;">2</div>'
        '<div style="font-weight:600; font-size:14px; margin-bottom:5px; color:#212529;">Feature Engineering</div>'
        '<div style="font-size:11px; color:#6C757D;">Property age, condo flags, total rooms, and city attributes engineered</div>'
        '</div>'
        '<div style="font-size: 20px; color: #CED4DA; font-weight:bold;">&rarr;</div>'
        '<!-- Step 3 -->'
        '<div style="flex:1; min-width: 180px; text-align:center;">'
        '<div style="width:50px; height:50px; border-radius:50%; background:#E9ECEF; display:flex; align-items:center; justify-content:center; margin: 0 auto 12px auto; font-weight:700; color:#0D6EFD; border: 2px solid #0D6EFD;">3</div>'
        '<div style="font-weight:600; font-size:14px; margin-bottom:5px; color:#212529;">Encoding & Scaling</div>'
        '<div style="font-size:11px; color:#6C757D;">Label encoding for high-cardinality locations, scaling via MinMax mapping</div>'
        '</div>'
        '<div style="font-size: 20px; color: #CED4DA; font-weight:bold;">&rarr;</div>'
        '<!-- Step 4 -->'
        '<div style="flex:1; min-width: 180px; text-align:center;">'
        '<div style="width:50px; height:50px; border-radius:50%; background:#E9ECEF; display:flex; align-items:center; justify-content:center; margin: 0 auto 12px auto; font-weight:700; color:#0D6EFD; border: 2px solid #0D6EFD;">4</div>'
        '<div style="font-weight:600; font-size:14px; margin-bottom:5px; color:#212529;">XGBoost Inference</div>'
        '<div style="font-weight:700; font-size:14px; margin-bottom:5px; color:#198754;">98.09% R&sup2; Model</div>'
        '<div style="font-size:11px; color:#6C757D;">Inference checks, error confidence bounds & target categorization applied</div>'
        '</div>'
        '</div>'
        '</div>'
    )
    st.markdown(workflow_html, unsafe_allow_html=True)
