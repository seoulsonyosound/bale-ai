import streamlit as st
import os
import sys

import importlib

# Ensure utils and pages directories are in sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

# Force reload utility and page modules to prevent stale cached bytecodes in Streamlit
import utils.predictor
import utils.visualizations
import utils.helpers
import utils.preprocessing
import pages.Dashboard
import pages.Prediction
import pages.Dataset
import pages.Model_Analytics
import pages.About

importlib.reload(utils.predictor)
importlib.reload(utils.visualizations)
importlib.reload(utils.helpers)
importlib.reload(utils.preprocessing)
importlib.reload(pages.Dashboard)
importlib.reload(pages.Prediction)
importlib.reload(pages.Dataset)
importlib.reload(pages.Model_Analytics)
importlib.reload(pages.About)

# Import layout and UI helpers
from utils.helpers import load_custom_css, render_sidebar_header
from utils.predictor import load_model_assets

def main():
    # Set page layout config
    st.set_page_config(
        page_title="BaleAI | House Price Prediction",
        page_icon=None,
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Load custom CSS styles
    load_custom_css()
    
    # Render sidebar branding header
    render_sidebar_header()
    
    # Pre-load machine learning model and metadata (cached resource)
    try:
        assets = load_model_assets()
        st.session_state['ml_assets'] = assets
    except Exception as e:
        st.sidebar.error(f"Error loading models: {e}")
        st.error("Failed to load machine learning models. Please run 'utils/train.py' to generate the pickle assets.")
        return

    # Navigation menu
    st.sidebar.markdown("<p style='font-size:12px; font-weight:600; color:#6C757D; text-transform:uppercase; letter-spacing:0.5px; margin-bottom:5px;'>Navigation</p>", unsafe_allow_html=True)
    
    navigation_options = {
        "Dashboard": "dashboard",
        "Predict House Price": "prediction",
        "Dataset Explorer": "dataset",
        "Model Analytics": "analytics",
        "About": "about"
    }
    
    # Navigation selection
    selected_option = st.sidebar.radio(
        label="Menu Navigation",
        options=list(navigation_options.keys()),
        label_visibility="collapsed"
    )
    
    page_key = navigation_options[selected_option]
    
    # Initialize history session states
    if 'prediction_history' not in st.session_state:
        st.session_state['prediction_history'] = []
        
    # Render the active page
    if page_key == "dashboard":
        from pages.Dashboard import show_dashboard
        show_dashboard(assets)
    elif page_key == "prediction":
        from pages.Prediction import show_prediction
        show_prediction(assets)
    elif page_key == "dataset":
        from pages.Dataset import show_dataset
        show_dataset(assets)
    elif page_key == "analytics":
        from pages.Model_Analytics import show_analytics
        show_analytics(assets)
    elif page_key == "about":
        from pages.About import show_about
        show_about(assets)

if __name__ == "__main__":
    main()
