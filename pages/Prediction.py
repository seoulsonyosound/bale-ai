import streamlit as st
import time
import pandas as pd
import numpy as np
from utils.helpers import draw_price_result_card
from utils.predictor import predict_single_house, explain_prediction_insights, predict_batch_csv
from utils.visualizations import plot_price_gauge, plot_confidence_meter

def show_prediction(assets):
    """
    Renders the Predict House Price page, supporting single-property form and batch upload.
    """
    st.markdown("<h1 style='margin-bottom:5px;'>House Price Valuation</h1>", unsafe_allow_html=True)
    st.markdown("<p style='font-size:16px; color:#6C757D; margin-bottom:25px;'>Run real-time valuation estimates or batch predict listings via CSV upload.</p>", unsafe_allow_html=True)
    
    # Create Tabs for Single vs Batch Prediction
    tab_single, tab_batch = st.tabs(["Single Property Valuation", "Batch Prediction (CSV)"])
    
    encoder_bundle = assets['encoder_bundle']
    city_defaults = encoder_bundle['city_defaults']
    metadata = assets['metadata']
    q33 = metadata['classification_eval']['q33']
    q66 = metadata['classification_eval']['q66']
    
    # Extract cities list
    cities = sorted([c for c in city_defaults.keys() if c != 'Global_Default'])
    
    # ------------------ TAB 1: SINGLE PROPERTY ------------------
    with tab_single:
        left_col, right_col = st.columns([0.45, 0.55])
        
        with left_col:
            st.markdown("<h3 style='font-size:18px;'>Property Specifications Form</h3>", unsafe_allow_html=True)
            
            # Using Streamlit form to group inputs and prevent page reloading on widget changes
            with st.form("valuation_form"):
                
                # Section 1: Location
                with st.expander("Location Details", expanded=True):
                    location_city = st.selectbox(
                        "City/Municipality",
                        options=cities,
                        index=cities.index("Pasig") if "Pasig" in cities else 0,
                        help="Select the specific city in the Philippines where the property is located."
                    )
                
                # Section 2: Specifications
                with st.expander("Building & Land Areas", expanded=True):
                    floor_area = st.number_input(
                        "Floor Area (sqm)",
                        min_value=10.0,
                        max_value=1000.0,
                        value=120.0,
                        step=5.0,
                        help="Total structural indoor floor area in square meters."
                    )
                    land_area = st.number_input(
                        "Land Area (sqm)",
                        min_value=0.0,
                        max_value=2000.0,
                        value=150.0,
                        step=10.0,
                        help="Total lot land area in square meters. Set to 0 if Condo/No lot land."
                    )
                
                # Section 3: House Layout
                with st.expander("Layout & Age", expanded=True):
                    c1, c2 = st.columns(2)
                    with c1:
                        bedrooms = st.slider("Bedrooms", min_value=1, max_value=10, value=3)
                    with c2:
                        bathrooms = st.slider("Bathrooms (Bath)", min_value=1, max_value=10, value=2)
                        
                    year_built = st.number_input(
                        "Year Built",
                        min_value=1950,
                        max_value=2026,
                        value=2018,
                        step=1,
                        help="The year construction was completed. Used to compute age depreciation."
                    )
                    
                    property_type = st.selectbox(
                        "Property Type",
                        options=["House", "Condo"],
                        index=0,
                        help="House/Townhouse vs. High-rise Condominium Unit."
                    )
                
                # Form Action Buttons
                st.markdown("<div style='margin-top:15px;'></div>", unsafe_allow_html=True)
                submit_btn = st.form_submit_button("Estimate Valuation Price")
                
        with right_col:
            st.markdown("<h3 style='font-size:18px;'>Valuation Report Output</h3>", unsafe_allow_html=True)
            
            if submit_btn:
                # 1. Prediction run
                with st.spinner("Analyzing market indices & processing property parameters..."):
                    # Add artificial delay to give a professional computational feel
                    time.sleep(0.6)
                    
                    result = predict_single_house(
                        assets=assets,
                        floor_area=floor_area,
                        land_area=land_area,
                        bedrooms=bedrooms,
                        bath=bathrooms,
                        location_city=location_city,
                        year_built=year_built,
                        property_type=property_type
                    )
                    
                # 2. Extract values
                price = result['price']
                low = result['lower_bound']
                high = result['upper_bound']
                tier = result['class']
                time_ms = result['time_ms']
                features_df = result['features_df']
                
                st.toast("Property valuation compiled successfully!")
                st.balloons()
                
                # 3. Draw Hero Card
                draw_price_result_card(price, low, high)
                
                # 4. Indicators Grid
                ind_col1, ind_col2 = st.columns(2)
                with ind_col1:
                    st.plotly_chart(plot_price_gauge(price, q33, q66), use_container_width=True)
                with ind_col2:
                    st.plotly_chart(plot_confidence_meter(price, low, high), use_container_width=True)
                    
                # 5. Core parameters
                st.markdown(f"""
                <div class="glass-card" style="padding:15px 20px; font-size:13px; color:#495057; line-height:1.6;">
                    <b>Model Used:</b> XGBoost Regressor | <b>Inference Speed:</b> {time_ms:.1f} ms<br>
                    <b>Estimated Market Tier:</b> <span style="font-weight:700; color:#0F172A;">{tier} Market Tier</span>
                </div>
                """, unsafe_allow_html=True)
                
                # 6. Feature insights
                st.markdown("<h4 style='font-size:16px; margin-top:20px; margin-bottom:10px;'>Valuation Key Drivers</h4>", unsafe_allow_html=True)
                insights = explain_prediction_insights(assets, features_df)
                
                for insight in insights:
                    impact_color = "#198754" if "Positive" in insight['impact'] else "#DC3545"
                    st.markdown(f"""
                    <div style="background-color:rgba(255,255,255,0.7); border-radius:8px; padding:10px 15px; border-left:4px solid {impact_color}; margin-bottom:10px; font-size:13px; box-shadow:0 2px 8px rgba(0,0,0,0.02);">
                        <span style="font-weight:600; color:#212529;">{insight['feature']}: {insight['value']}</span> 
                        <span style="color:{impact_color}; font-weight:700; font-size:11px; float:right;">{insight['impact']}</span>
                        <div style="color:#6C757D; margin-top:4px;">{insight['explanation']}</div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                # 7. Add to Session prediction history
                st.session_state['prediction_history'].append({
                    "Timestamp": pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "City": location_city,
                    "Type": property_type,
                    "Floor Area (sqm)": floor_area,
                    "Land Area (sqm)": land_area,
                    "Bedrooms": bedrooms,
                    "Bathrooms": bathrooms,
                    "Year Built": year_built,
                    "Estimated Price": price,
                    "Confidence Interval": f"₱{low:,.0f} - ₱{high:,.0f}"
                })
                
                # 8. Export Single Valuation as CSV
                val_df = pd.DataFrame([{
                    "City": location_city,
                    "Type": property_type,
                    "Floor Area (sqm)": floor_area,
                    "Land Area (sqm)": land_area,
                    "Bedrooms": bedrooms,
                    "Bathrooms": bathrooms,
                    "Year Built": year_built,
                    "Estimated Price (PHP)": price,
                    "Lower Bound (PHP)": low,
                    "Upper Bound (PHP)": high,
                    "Market Tier": tier
                }])
                csv_data = val_df.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="Download Valuation Report (CSV)",
                    data=csv_data,
                    file_name=f"valuation_{location_city}_{property_type}.csv",
                    mime="text/csv"
                )
            else:
                st.markdown("""
                <div style="background-color:rgba(255,255,255,0.5); border-radius:12px; border:2px dashed #CED4DA; height:320px; display:flex; align-items:center; justify-content:center; flex-direction:column; text-align:center; padding:20px; color:#6C757D;">
                    <div style="font-size:24px; font-weight:600; color:#94A3B8; margin-bottom:15px;">BaleAI</div>
                    <div style="font-weight:600; font-size:15px; color:#495057;">Waiting for input parameters...</div>
                    <div style="font-size:12px; max-width:280px; margin-top:5px;">Fill out the specifications form and click "Estimate Valuation Price" to compile predictions.</div>
                </div>
                """, unsafe_allow_html=True)
                
    # ------------------ TAB 2: BATCH PREDICTION ------------------
    with tab_batch:
        st.markdown("<h3 style='font-size:18px;'>Batch Upload Interface</h3>", unsafe_allow_html=True)
        st.markdown("""
            Upload a CSV containing multiple property records to run batch pricing estimates. 
            The system will automatically run missing value checks, location mapping, and scaling.
        """)
        
        # 1. Download CSV Template
        template_df = pd.DataFrame([{
            'Floor_area (sqm)': 120.0,
            'Land_area (sqm)': 150.0,
            'Bedrooms': 3,
            'Bath': 2,
            'Location_City': 'Pasig',
            'Year_Built': 2018,
            'property_type': 'House'
        }, {
            'Floor_area (sqm)': 85.0,
            'Land_area (sqm)': 0.0,
            'Bedrooms': 2,
            'Bath': 1,
            'Location_City': 'Makati',
            'Year_Built': 2020,
            'property_type': 'Condo'
        }])
        template_csv = template_df.to_csv(index=False).encode('utf-8')
        
        st.download_button(
            label="Download CSV Upload Template",
            data=template_csv,
            file_name="baleai_batch_template.csv",
            mime="text/csv"
        )
        
        st.markdown("<div style='margin-top:15px;'></div>", unsafe_allow_html=True)
        
        # 2. Upload file
        uploaded_file = st.file_uploader("Upload Property Listings CSV File", type=["csv"])
        
        if uploaded_file is not None:
            with st.spinner("Processing batch upload and compiling forecasts..."):
                time.sleep(1.0)
                pred_df, success_count, err_msg = predict_batch_csv(assets, uploaded_file)
                
            if err_msg:
                st.error(err_msg)
            else:
                st.success(f"Batch inference complete! Successfully forecast prices for {success_count} property listings.")
                
                # Render preview table
                # Format predicted price for preview display
                df_disp = pred_df.copy()
                df_disp['Predicted Price (PHP)'] = df_disp['Predicted Price (PHP)'].apply(lambda x: f"₱{x:,.2f}")
                st.dataframe(df_disp.head(20), use_container_width=True)
                
                # Download button for predicted CSV
                output_csv = pred_df.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="Download Forecasted Predictions CSV",
                    data=output_csv,
                    file_name="forecasted_batch_valuations.csv",
                    mime="text/csv"
                )
                
    # ------------------ PREDICTION HISTORY SECTION ------------------
    st.markdown("<h3 style='margin-top:30px; font-size:18px;'>Prediction History (Current Session)</h3>", unsafe_allow_html=True)
    history = st.session_state['prediction_history']
    
    if len(history) > 0:
        hist_df = pd.DataFrame(history)
        
        # Display nicely formatted dataframe
        hist_df_disp = hist_df.copy()
        hist_df_disp['Estimated Price'] = hist_df_disp['Estimated Price'].apply(lambda x: f"₱{x:,.2f}")
        st.dataframe(hist_df_disp.iloc[::-1], use_container_width=True) # Reverse to show latest first
        
        c1, c2 = st.columns([0.15, 0.85])
        with c1:
            if st.button("Clear History", key="clear_hist"):
                st.session_state['prediction_history'] = []
                st.rerun()
    else:
        st.markdown("""
        <div style="background-color:rgba(0,0,0,0.02); border-radius:8px; border:1px solid rgba(0,0,0,0.05); padding:15px; text-align:center; color:#6C757D; font-size:13px;">
            No valuations executed in the current session. Run a prediction to populate history.
        </div>
        """, unsafe_allow_html=True)
