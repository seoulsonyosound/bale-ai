import streamlit as st
import pandas as pd
import numpy as np
import os
from utils.visualizations import plot_correlation_matrix

def show_dataset(assets):
    """
    Renders the Dataset Explorer page, displaying clean metadata and a searchable listing table.
    """
    st.markdown("<h1 style='margin-bottom:5px;'>Dataset Explorer</h1>", unsafe_allow_html=True)
    st.markdown("<p style='font-size:16px; color:#6C757D; margin-bottom:25px;'>Search, sort, filter, and inspect the raw PH Houses listing records.</p>", unsafe_allow_html=True)

    # Load dataset
    csv_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "PH_houses_v2.csv")
    if not os.path.exists(csv_path):
        st.error("Dataset 'PH_houses_v2.csv' not found.")
        return

    try:
        df = pd.read_csv(csv_path)
    except Exception as e:
        st.error(f"Error loading dataset: {e}")
        return

    # Parse dataset for display: replace string 'na' with NaN
    df_clean = df.copy()
    df_clean = df_clean.replace('na', np.nan)
    
    # Render basic info about the dataset
    # Render basic info about the dataset
    with st.container(border=True):
        st.markdown("<h3 style='margin-top:0; color:#0F172A; font-size:18px;'>Dataset Overview</h3>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Records", f"{len(df_clean):,}")
        with col2:
            st.metric("Features Available", f"{len(df_clean.columns)}")
        with col3:
            st.metric("Unique Locations", f"{df_clean['Location'].dropna().nunique():,}")

    # Cleaning price for correlation plot and search filters
    if 'Price (PHP)' in df_clean.columns:
        df_clean['Price_cleaned'] = df_clean['Price (PHP)'].astype(str).str.replace(',', '').str.replace(' ', '')
        df_clean['Price_cleaned'] = pd.to_numeric(df_clean['Price_cleaned'], errors='coerce')
        
    # Clean other numeric columns
    for col in ['Bedrooms', 'Bath', 'Floor_area (sqm)', 'Land_area (sqm)', 'Latitude', 'Longitude']:
        if col in df_clean.columns:
            df_clean[col] = pd.to_numeric(df_clean[col], errors='coerce')

    # Filtering Section
    st.markdown("<h3 style='margin-bottom:15px; font-size:18px;'>Filter Dataset</h3>", unsafe_allow_html=True)
    
    col_filter1, col_filter2, col_filter3 = st.columns(3)
    
    with col_filter1:
        search_query = st.text_input("Search Description", "", help="Search listing description by keyword")
        
    with col_filter2:
        # Get location list
        locations = sorted(list(df_clean['Location'].dropna().unique()))
        selected_location = st.selectbox("Location Filter", ["All Locations"] + locations)
        
    with col_filter3:
        # Price range
        min_price = float(df_clean['Price_cleaned'].min()) if 'Price_cleaned' in df_clean.columns and not df_clean['Price_cleaned'].isnull().all() else 0.0
        max_price = float(df_clean['Price_cleaned'].max()) if 'Price_cleaned' in df_clean.columns and not df_clean['Price_cleaned'].isnull().all() else 100000000.0
        
        # Format values
        price_range = st.slider(
            "Price Range (PHP)",
            min_value=min_price,
            max_value=max_price,
            value=(min_price, max_price),
            step=100000.0,
            format="₱%,.0f"
        )

    # Filter operations
    filtered_df = df_clean.copy()
    if search_query:
        filtered_df = filtered_df[filtered_df['Description'].astype(str).str.contains(search_query, case=False, na=False)]
    if selected_location != "All Locations":
        filtered_df = filtered_df[filtered_df['Location'] == selected_location]
        
    if 'Price_cleaned' in filtered_df.columns:
        filtered_df = filtered_df[
            (filtered_df['Price_cleaned'] >= price_range[0]) & 
            (filtered_df['Price_cleaned'] <= price_range[1])
        ]
        
    # Drop intermediate cleaned column for display
    display_df = filtered_df.drop(columns=['Price_cleaned'], errors='ignore')

    # Display Table
    st.markdown(f"<p style='font-size:14px; color:#6C757D;'>Displaying {len(display_df):,} matching listings.</p>", unsafe_allow_html=True)
    st.dataframe(display_df, use_container_width=True)

    # Double columns: Completeness & Heatmap
    st.markdown("<hr style='margin:25px 0;'>", unsafe_allow_html=True)
    
    col_comp, col_heat = st.columns([0.45, 0.55])
    
    with col_comp:
        st.markdown("<h3 style='font-size:18px;'>Data Completeness Profile</h3>", unsafe_allow_html=True)
        # Compute missing percents (treat 'na' as missing as they were replaced above)
        missing_df = df_clean.drop(columns=['Price_cleaned'], errors='ignore').isnull().mean() * 100
        completeness_df = pd.DataFrame({
            "Attribute": missing_df.index,
            "Completeness (%)": 100 - missing_df.values
        }).sort_values(by="Completeness (%)", ascending=False)
        
        st.dataframe(
            completeness_df.style.format({"Completeness (%)": "{:.2f}%"})
                                .background_gradient(cmap="Blues", subset=["Completeness (%)"]),
            use_container_width=True
        )
        
    with col_heat:
        st.markdown("<h3 style='font-size:18px;'>Correlation Analysis</h3>", unsafe_allow_html=True)
        fig_corr = plot_correlation_matrix(filtered_df)
        if fig_corr is not None:
            st.plotly_chart(fig_corr, use_container_width=True)
        else:
            st.info("Not enough numeric data to display correlation matrix.")
