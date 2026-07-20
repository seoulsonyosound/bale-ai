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
        html, body, input, button, select, textarea, h1, h2, h3, h4, h5, h6 {
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

        /* ── Sidebar shell ──────────────────────────────────────────── */
        [data-testid="stSidebar"] {
            background-color: #FFFFFF;
            border-right: 1px solid #E2E8F0;
        }

        /* st.logo() header row – give it enough height for the bigger logo */
        [data-testid="stSidebarHeader"] {
            min-height: 72px !important;
            align-items: center !important;
            padding: 8px 12px !important;
        }

        /* st.logo() image – bigger, contained, rounded */
        [data-testid="stSidebarHeader"] img {
            width: 62px !important;
            height: 62px !important;
            object-fit: contain !important;
            border-radius: 8px !important;
        }

        /* Brand overlay: pulled up via negative margin to sit inline with logo */
        .brand-overlay {
            margin-top: -66px;        /* pull up into the header row */
            margin-left: 74px;        /* clear the logo width + gap */
            padding-bottom: 4px;
            position: relative;
            z-index: 999;
            line-height: 1.25;
        }
        .brand-name {
            font-size: 15px;
            font-weight: 700;
            color: #0F172A;
            letter-spacing: -0.2px;
        }
        .brand-sub {
            font-size: 9px;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 1.4px;
            color: #1E9B8A;
            margin-top: 2px;
        }

        /* Divider below brand area */
        .brand-divider {
            border: none;
            border-top: 1px solid #E2E8F0;
            margin: 10px 0 18px 0;
        }

        /* Sidebar content – no extra top padding (brand overlay handles spacing) */
        [data-testid="stSidebarContent"] {
            padding-top: 0px !important;
        }


        /* Navigation label */
        .nav-label {
            font-size: 10px;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 1px;
            color: #94A3B8;
            margin-bottom: 8px;
            padding-left: 4px;
        }

        /* ── Sidebar navigation radio pills ──────────────────────────── */
        /* Hide the auto-generated label above the radio group */
        [data-testid="stSidebar"] [data-testid="stRadio"] > label {
            display: none !important;
        }
        /* Each option row */
        [data-testid="stSidebar"] [data-testid="stRadio"] > div > label {
            display: flex !important;
            align-items: center !important;
            padding: 9px 14px !important;
            border-radius: 8px !important;
            margin-bottom: 3px !important;
            font-size: 14px !important;
            font-weight: 500 !important;
            color: #475569 !important;
            cursor: pointer !important;
            transition: background 0.15s ease, color 0.15s ease !important;
            border-left: 3px solid transparent !important;
        }
        [data-testid="stSidebar"] [data-testid="stRadio"] > div > label:hover {
            background: #F1F5F9 !important;
            color: #0F172A !important;
        }
        /* Hide the native radio circle / SVG marker */
        [data-testid="stSidebar"] [data-testid="stRadio"] > div > label > span:first-child {
            display: none !important;
        }
        /* Active / selected item */
        [data-testid="stSidebar"] [data-testid="stRadio"] > div > label[data-checked="true"],
        [data-testid="stSidebar"] [data-testid="stRadio"] > div > label:has(input:checked) {
            background: rgba(13, 110, 253, 0.07) !important;
            color: #0D6EFD !important;
            font-weight: 600 !important;
            border-left: 3px solid #0D6EFD !important;
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
    Places the BaleAI logo inline with the sidebar collapse arrows via st.logo().
    Then injects a brand-overlay div (pulled up via negative margin) so that
    'BaleAI' and 'REAL ESTATE INTELLIGENCE' sit on the same row as the logo.
    """
    assets_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets")
    logo_path = os.path.join(assets_dir, "logo.png")

    # Place logo in the native sidebar header row (same row as the << button)
    if os.path.exists(logo_path):
        st.logo(logo_path)

    # Brand text overlay – negative margin pulls it up into the header row,
    # left margin clears the logo image so text sits right next to it.
    st.sidebar.markdown(
        '<div class="brand-overlay">'
        '<div class="brand-name">BaleAI</div>'
        '<div class="brand-sub">Real Estate Intelligence</div>'
        '</div>'
        '<hr class="brand-divider">',
        unsafe_allow_html=True,
    )

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
