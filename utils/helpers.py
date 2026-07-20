import streamlit as st
import os
import base64

def get_base64_encoded_image(img_path):
    """
    Reads an image from path and returns its base64 encoding.
    """
    if os.path.exists(img_path):
        with open(img_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode()
    return ""

def load_custom_css():
    """
    Injects custom CSS to style the Streamlit application.
    Enforces a sleek, formal, and premium corporate style.
    """
    custom_style = """
    <style>
        /* Import premium typography */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
        
        [data-testid="stAppViewContainer"] {
            background-color: #F8F9FA;
        }
        
        /* Apply font and global clean layout */
        html, body, [class*="css"], [class*="st-"] {
            font-family: 'Inter', sans-serif !important;
        }
        
        /* Formal, Sleek Card Containers */
        .glass-card {
            background: #FFFFFF;
            border-radius: 12px;
            border: 1px solid #E2E8F0;
            padding: 24px;
            box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.05), 0 1px 2px 0 rgba(0, 0, 0, 0.03);
            margin-bottom: 20px;
            transition: all 0.2s ease;
        }
        .glass-card:hover {
            transform: translateY(-1px);
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.03);
            border-color: #CBD5E1;
        }
        
        /* Custom Stats Grid Cards */
        .metric-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
            gap: 16px;
            margin-bottom: 24px;
        }
        
        .stat-card {
            background: #FFFFFF;
            border-radius: 10px;
            border: 1px solid #E2E8F0;
            padding: 20px;
            box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
            text-align: center;
            transition: all 0.2s ease;
        }
        
        .stat-card:hover {
            background: #FAFAFA;
            border-color: #CBD5E1;
            transform: translateY(-1px);
        }
        
        .stat-value {
            font-size: 26px;
            font-weight: 700;
            color: #0F172A;
            margin-bottom: 4px;
        }
        
        .stat-label {
            font-size: 13px;
            font-weight: 600;
            color: #475569;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        
        .stat-desc {
            font-size: 11px;
            color: #64748B;
            margin-top: 6px;
        }
        
        /* Formal Corporate Button Styling */
        .stButton>button {
            background: #0F172A !important;
            color: white !important;
            border: none !important;
            padding: 10px 24px !important;
            border-radius: 6px !important;
            font-weight: 500 !important;
            box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.05) !important;
            transition: all 0.2s ease !important;
            width: 100%;
        }
        
        .stButton>button:hover {
            background: #1E293B !important;
            transform: translateY(-1px);
        }
        
        .stButton>button:active {
            transform: translateY(1px);
        }
        
        /* Reset button design */
        div[data-testid="stFormSubmitButton"] + div button, 
        .secondary-btn button {
            background: transparent !important;
            color: #334155 !important;
            border: 1px solid #E2E8F0 !important;
            box-shadow: none !important;
        }
        
        .secondary-btn button:hover {
            background: #F8FAFC !important;
            border-color: #CBD5E1 !important;
            color: #0F172A !important;
        }
        
        /* Custom side header logo */
        .logo-container {
            display: flex;
            align-items: center;
            padding: 10px 0 20px 0;
            border-bottom: 1px solid #E2E8F0;
            margin-bottom: 20px;
        }
        
        .logo-img {
            width: 44px;
            height: 44px;
            border-radius: 6px;
            margin-right: 12px;
            object-fit: cover;
        }
        
        .logo-title {
            font-size: 18px;
            font-weight: 700;
            color: #0F172A;
            line-height: 1.2;
        }
        
        .logo-subtitle {
            font-size: 11px;
            color: #64748B;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        
        /* Sticky sidebar tabs styling tweaks */
        [data-testid="stSidebar"] {
            background-color: #FFFFFF;
            border-right: 1px solid #E2E8F0;
        }
        
        /* Modern scrollbars */
        ::-webkit-scrollbar {
            width: 6px;
            height: 6px;
        }
        ::-webkit-scrollbar-track {
            background: transparent;
        }
        ::-webkit-scrollbar-thumb {
            background: #CBD5E1;
            border-radius: 3px;
        }
        ::-webkit-scrollbar-thumb:hover {
            background: #94A3B8;
        }
        
        /* Form sections grouping */
        .form-section {
            background: #F8FAFC;
            border-radius: 8px;
            border: 1px solid #E2E8F0;
            padding: 16px;
            margin-bottom: 12px;
        }
        
        /* Prediction Highlight Cards */
        .price-card {
            background: #0F172A;
            border-radius: 12px;
            padding: 24px;
            color: white;
            text-align: center;
            border: 1px solid #1E293B;
            margin-bottom: 20px;
        }
        .price-label {
            font-size: 13px;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 1px;
            color: #94A3B8;
        }
        .price-val {
            font-size: 32px;
            font-weight: 700;
            margin: 8px 0;
            letter-spacing: -0.5px;
            color: #FFFFFF;
        }
        .price-range {
            font-size: 13px;
            color: #CBD5E1;
            font-weight: 400;
        }
    </style>
    """
    st.markdown(custom_style, unsafe_allow_html=True)

def render_sidebar_header():
    """
    Renders the company logo and branding in the sidebar.
    """
    assets_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets")
    logo_encoded = get_base64_encoded_image(os.path.join(assets_dir, "logo.png"))
    
    if logo_encoded:
        logo_html = f"""
        <div class="logo-container">
            <img class="logo-img" src="data:image/png;base64,{logo_encoded}">
            <div>
                <div class="logo-title">BaleAI</div>
                <div class="logo-subtitle">Real Estate Intelligence</div>
            </div>
        </div>
        """
    else:
        logo_html = """
        <div class="logo-container">
            <div class="logo-img" style="background:#0F172A; display:flex; align-items:center; justify-content:center; color:white; font-weight:bold; font-size:20px;">B</div>
            <div>
                <div class="logo-title">BaleAI</div>
                <div class="logo-subtitle">Real Estate Intelligence</div>
            </div>
        </div>
        """
    st.sidebar.markdown(logo_html, unsafe_allow_html=True)

def draw_metric_card(title, value, description, key_suffix=""):
    """
    Draws a single statistics card using clean styled HTML.
    """
    card_html = f"""
    <div class="stat-card">
        <div class="stat-value">{value}</div>
        <div class="stat-label">{title}</div>
        <div class="stat-desc">{description}</div>
    </div>
    """
    st.markdown(card_html, unsafe_allow_html=True)

def draw_price_result_card(price, low, high):
    """
    Draws the hero pricing outcome display block.
    """
    card_html = f"""
    <div class="price-card">
        <div class="price-label">Estimated House Valuation</div>
        <div class="price-val">₱{price:,.2f} PHP</div>
        <div class="price-range">95% Valuation Bounds: ₱{low:,.2f} to ₱{high:,.2f} PHP</div>
    </div>
    """
    st.markdown(card_html, unsafe_allow_html=True)
