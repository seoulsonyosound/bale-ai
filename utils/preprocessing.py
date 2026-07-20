import os
import re
import numpy as np
import pandas as pd
from sklearn.preprocessing import LabelEncoder

def clean_target_price(df, target_col='Price (PHP)'):
    """
    Cleans target price column: removes commas, spaces, and casts to numeric.
    """
    df = df.copy()
    if target_col in df.columns:
        df[target_col] = df[target_col].astype(str).str.replace(',', '').str.replace(' ', '')
        df[target_col] = pd.to_numeric(df[target_col], errors='coerce')
        # Drop rows where target price is missing for training
        df = df.dropna(subset=[target_col])
    return df

def parse_numeric_columns(df, cols=['Bedrooms', 'Bath', 'Floor_area (sqm)', 'Land_area (sqm)', 'Latitude', 'Longitude']):
    """
    Parses columns to numeric types, coercing invalid values to NaN.
    """
    df = df.copy()
    for col in cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
    return df

def impute_missing_values(df, num_cols, cat_cols, medians=None, modes=None, is_training=True):
    """
    Imputes missing values.
    During training, fits medians/modes and tracks missing flags.
    During inference, applies the fitted medians/modes and missing flags.
    """
    df = df.copy()
    fitted_medians = medians if medians is not None else {}
    fitted_modes = modes if modes is not None else {}
    
    # Track missing flags
    for col in num_cols:
        flag_col = f'{col}_was_missing'
        if is_training:
            if df[col].isnull().any():
                df[flag_col] = df[col].isnull().astype(int)
            else:
                df[flag_col] = 0
        else:
            # For inference, if the flag column is in the schema, populate it
            df[flag_col] = df[col].isnull().astype(int)
            
    # Impute numerical columns
    for col in num_cols:
        if is_training:
            median_val = df[col].median()
            # Fallback if all values are NaN
            if pd.isnull(median_val):
                median_val = 0.0
            fitted_medians[col] = median_val
        df[col] = df[col].fillna(fitted_medians.get(col, 0.0))
        
    # Impute categorical columns
    for col in cat_cols:
        if is_training:
            if df[col].isnull().all():
                mode_val = "Unknown"
            else:
                mode_val = df[col].mode()[0]
            fitted_modes[col] = mode_val
        df[col] = df[col].fillna(fitted_modes.get(col, "Unknown"))
        
    if is_training:
        return df, fitted_medians, fitted_modes
    return df

def remove_outliers_zscore(df, columns=['Price (PHP)', 'Floor_area (sqm)', 'Land_area (sqm)'], threshold=3.0):
    """
    Removes outliers using the Z-score method.
    """
    df = df.copy()
    outliers_idx = []
    for col in columns:
        if col in df.columns:
            col_mean = df[col].mean()
            col_std = df[col].std()
            if col_std == 0:
                continue
            z_scores = (df[col] - col_mean) / col_std
            outliers = df.index[z_scores.abs() > threshold].tolist()
            outliers_idx.extend(outliers)
    
    outliers_idx = list(set(outliers_idx))
    df = df.drop(index=outliers_idx).reset_index(drop=True)
    return df, len(outliers_idx)

def extract_house_year(text):
    """
    Regex function to extract year built from text between 1950 and 2026.
    """
    if pd.isnull(text):
        return np.nan
    # Find all 4-digit numbers in the range 1950 - 2026
    years = re.findall(r'\b(19\d{2}|20[0-2]\d)\b', str(text))
    if years:
        years = [int(y) for y in years if 1950 <= int(y) <= 2026]
        if years:
            return min(years)
    return np.nan

def engineer_features(df, is_training=True, median_year=2015):
    """
    Applies feature engineering: Total_Rooms, Age, Condo/House tags, City.
    """
    df = df.copy()
    
    # 1. Total Rooms
    if 'Bedrooms' in df.columns and 'Bath' in df.columns:
        df['Total_Rooms'] = df['Bedrooms'] + df['Bath']
    else:
        df['Total_Rooms'] = 3.0 # Default fallback
        
    # 2. Extract Year Built
    if 'Description' in df.columns:
        df['Year_Built'] = df['Description'].apply(extract_house_year)
    else:
        df['Year_Built'] = np.nan
        
    if is_training:
        med_yr = df['Year_Built'].median()
        if pd.isnull(med_yr):
            med_yr = 2015
        median_year = med_yr
        df['Year_Built_was_missing'] = df['Year_Built'].isnull().astype(int)
    else:
        df['Year_Built_was_missing'] = df['Year_Built'].isnull().astype(int)
        
    df['Year_Built'] = df['Year_Built'].fillna(median_year)
    df['House_Age'] = 2026.0 - df['Year_Built']
    
    # 3. Property Tags (Is_Condo, Is_House)
    # We apply this to description column
    if 'Description' in df.columns:
        desc_str = df['Description'].astype(str).str.lower()
        if 'Link' in df.columns:
            desc_str += " " + df['Link'].astype(str).str.lower()
        
        df['Is_Condo'] = desc_str.apply(lambda x: 1 if any(kw in x for kw in ['condo', 'unit', 'residences', 'apartment', 'studio']) else 0)
        df['Is_House'] = desc_str.apply(lambda x: 1 if any(kw in x for kw in ['house', 'townhouse', 'villa', 'cara', 'greta', 'ella', 'criselle', 'arielle', 'ezabelle']) else 0)
    else:
        df['Is_Condo'] = 0
        df['Is_House'] = 1
        
    # 4. Extract City
    if 'Location' in df.columns:
        df['Location_City'] = df['Location'].apply(lambda x: str(x).split(',')[-1].strip() if pd.notnull(x) else 'Unknown')
    else:
        df['Location_City'] = 'Unknown'
        
    # 5. Price per sqm floor (For EDA only)
    if 'Price (PHP)' in df.columns and 'Floor_area (sqm)' in df.columns:
        df['Price_per_sqm_floor'] = df['Price (PHP)'] / df['Floor_area (sqm)']
        
    if is_training:
        return df, median_year
    return df
