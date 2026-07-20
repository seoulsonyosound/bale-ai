import os
import time
import joblib
import numpy as np
import pandas as pd

def load_model_assets():
    """
    Loads all model assets from the models directory.
    Normally cached in streamlit using @st.cache_resource
    """
    models_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "models")
    
    reg_model = joblib.load(os.path.join(models_dir, 'trained_model.pkl'))
    scaler = joblib.load(os.path.join(models_dir, 'scaler.pkl'))
    encoder_bundle = joblib.load(os.path.join(models_dir, 'encoder.pkl'))
    feature_names = joblib.load(os.path.join(models_dir, 'model_features.pkl'))
    clf_model = joblib.load(os.path.join(models_dir, 'classifier_model.pkl'))
    metadata = joblib.load(os.path.join(models_dir, 'model_metadata.pkl'))
    
    return {
        'reg_model': reg_model,
        'scaler': scaler,
        'encoder_bundle': encoder_bundle,
        'feature_names': feature_names,
        'features': feature_names,
        'clf_model': clf_model,
        'metadata': metadata
    }

def predict_single_house(assets, floor_area, land_area, bedrooms, bath, location_city, year_built, property_type):
    """
    Preprocesses user input parameters, scales them, and runs inference.
    Returns: predicted price (PHP), lower bound, upper bound, prediction time (ms), and property class.
    """
    start_time = time.time()
    
    encoder_bundle = assets['encoder_bundle']
    feature_names = assets['feature_names']
    scaler = assets['scaler']
    reg_model = assets['reg_model']
    clf_model = assets['clf_model']
    metadata = assets['metadata']
    
    # 1. Resolve Location, Lat, Long from city defaults
    city_defaults = encoder_bundle['city_defaults']
    if location_city in city_defaults:
        defaults = city_defaults[location_city]
    else:
        defaults = city_defaults['Global_Default']
        
    lat = defaults['Latitude']
    lon = defaults['Longitude']
    location = defaults['Location']
    
    # Property flags
    is_condo = 1 if property_type == "Condo" else 0
    is_house = 1 if property_type == "House" else 0
    
    # 2. Build input dictionary matching training features order
    input_data = {col: 0.0 for col in feature_names}
    
    # Base numeric variables
    input_data['Bedrooms'] = float(bedrooms)
    input_data['Bath'] = float(bath)
    input_data['Floor_area (sqm)'] = float(floor_area)
    input_data['Land_area (sqm)'] = float(land_area)
    input_data['Latitude'] = float(lat)
    input_data['Longitude'] = float(lon)
    
    # Missing value flags - assume user input is complete, so flags are 0
    input_data['Bedrooms_was_missing'] = 0
    input_data['Bath_was_missing'] = 0
    input_data['Floor_area (sqm)_was_missing'] = 0
    input_data['Land_area (sqm)_was_missing'] = 0
    input_data['Latitude_was_missing'] = 0
    
    # Engineered variables
    input_data['Total_Rooms'] = float(bedrooms) + float(bath)
    input_data['Year_Built'] = float(year_built)
    input_data['Year_Built_was_missing'] = 0
    input_data['House_Age'] = 2026.0 - float(year_built)
    input_data['Is_Condo'] = is_condo
    input_data['Is_House'] = is_house
    
    # Encoding categorical variables
    label_encoders = encoder_bundle['label_encoders']
    
    # Encode Location
    le_loc = label_encoders['Location']
    try:
        input_data['Location'] = le_loc.transform([location])[0]
    except ValueError:
        # Unseen category fallback (use mode index)
        input_data['Location'] = 0
        
    # Encode Location_City
    le_city = label_encoders['Location_City']
    try:
        input_data['Location_City'] = le_city.transform([location_city])[0]
    except ValueError:
        input_data['Location_City'] = 0
        
    # 3. Construct DataFrame matching original feature structure
    input_df = pd.DataFrame([input_data])
    input_df = input_df[feature_names]
    
    # 4. Scale features
    input_scaled = scaler.transform(input_df)
    
    # 5. Predict Price
    pred_price = reg_model.predict(input_scaled)[0]
    # Ensure price is not negative
    pred_price = max(0.0, float(pred_price))
    
    # 6. Predict Category (Classifier)
    pred_class = clf_model.predict(input_scaled)[0]
    
    # 7. Confidence Bounds
    # Margins based on regression evaluation RMSE
    rmse = metadata['regression_eval']['RMSE']
    # Calculate a 95% prediction interval (using 1.96 * RMSE / sqrt(5) as a proxy for prediction interval width)
    margin = 1.96 * (rmse / np.sqrt(5))
    lower_bound = max(0.0, pred_price - margin)
    upper_bound = pred_price + margin
    
    prediction_time_ms = (time.time() - start_time) * 1000
    
    return {
        'price': pred_price,
        'lower_bound': lower_bound,
        'upper_bound': upper_bound,
        'class': pred_class,
        'time_ms': prediction_time_ms,
        'features_df': input_df
    }

def explain_prediction_insights(assets, features_df):
    """
    Generates structured textual explanation of how features influenced prediction.
    Compares the inputs with the dataset medians.
    """
    encoder_bundle = assets['encoder_bundle']
    metadata = assets['metadata']
    importances = metadata['feature_importances']
    feature_names = assets['feature_names']
    
    # Convert importances list to a dictionary
    imp_dict = dict(zip(feature_names, importances))
    
    # Medians dictionary
    medians = encoder_bundle['medians']
    
    insights = []
    
    # Floor Area
    floor_area = features_df.iloc[0]['Floor_area (sqm)']
    median_floor = medians.get('Floor_area (sqm)', 120.0)
    if floor_area > median_floor:
        diff_pct = ((floor_area - median_floor) / median_floor) * 100
        insights.append({
            'feature': 'Floor Area',
            'value': f"{floor_area:,.1f} sqm",
            'impact': 'Positive (Strong)',
            'explanation': f"Floor area is {diff_pct:.1f}% larger than the market median ({median_floor:.1f} sqm), which significantly increases the valuation."
        })
    else:
        diff_pct = ((median_floor - floor_area) / median_floor) * 100
        insights.append({
            'feature': 'Floor Area',
            'value': f"{floor_area:,.1f} sqm",
            'impact': 'Negative (Moderate)',
            'explanation': f"Floor area is {diff_pct:.1f}% smaller than the market median ({median_floor:.1f} sqm), limiting the overall valuation of the property."
        })
        
    # Rooms count
    rooms = features_df.iloc[0]['Total_Rooms']
    median_rooms = medians.get('Bedrooms', 3.0) + medians.get('Bath', 2.0)
    if rooms > median_rooms:
        insights.append({
            'feature': 'Room Count',
            'value': f"{int(rooms)} rooms",
            'impact': 'Positive',
            'explanation': f"The property has {int(rooms)} total rooms, which is above the typical standard room count of {int(median_rooms)}."
        })
        
    # Age
    age = features_df.iloc[0]['House_Age']
    median_age = 2026.0 - encoder_bundle['median_year']
    if age < median_age:
        insights.append({
            'feature': 'Property Age',
            'value': f"{int(age)} years old",
            'impact': 'Positive (Moderate)',
            'explanation': f"At {int(age)} years old, the property is newer than the typical market standard ({int(median_age)} years old), offering a premium."
        })
    else:
        insights.append({
            'feature': 'Property Age',
            'value': f"{int(age)} years old",
            'impact': 'Negative (Subtle)',
            'explanation': f"The property is older than the market median ({int(median_age)} years old), which might introduce depreciation discounts."
        })
        
    # Land Area
    land_area = features_df.iloc[0]['Land_area (sqm)']
    median_land = medians.get('Land_area (sqm)', 150.0)
    if land_area > median_land:
        diff_pct = ((land_area - median_land) / median_land) * 100
        insights.append({
            'feature': 'Land Area',
            'value': f"{land_area:,.1f} sqm",
            'impact': 'Positive (Moderate)',
            'explanation': f"Land area is {diff_pct:.1f}% larger than the median land area ({median_land:.1f} sqm), giving additional ground value."
        })
        
    # Sort insights based on XGBoost feature importance weights
    # Map feature names to display names
    display_mapping = {
        'Floor_area (sqm)': 'Floor Area',
        'Total_Rooms': 'Room Count',
        'House_Age': 'Property Age',
        'Land_area (sqm)': 'Land Area'
    }
    
    # Calculate a score based on importance weight for sorting
    for insight in insights:
        mapped_key = [k for k, v in display_mapping.items() if v == insight['feature']]
        weight = imp_dict.get(mapped_key[0], 0.01) if mapped_key else 0.01
        insight['weight'] = weight
        
    insights = sorted(insights, key=lambda x: x['weight'], reverse=True)
    return insights

def predict_batch_csv(assets, uploaded_file):
    """
    Loads batch CSV file, performs necessary missing value imputation,
    feature engineering, and category encoding, then runs predictions.
    Returns: A tuple (original_df_with_predictions, success_count, error_message).
    """
    try:
        df = pd.read_csv(uploaded_file)
        df_original = df.copy()
        
        # Verify minimum required columns exist
        required_cols = ['Bedrooms', 'Bath', 'Floor_area (sqm)', 'Land_area (sqm)', 'Location_City', 'Year_Built']
        missing_req = [col for col in required_cols if col not in df.columns]
        
        if missing_req:
            # Try to map alternative names
            mapping = {
                'bedroom': 'Bedrooms', 'bedrooms': 'Bedrooms',
                'bathroom': 'Bath', 'bath': 'Bath', 'bathrooms': 'Bath',
                'floor': 'Floor_area (sqm)', 'floor_area': 'Floor_area (sqm)',
                'land': 'Land_area (sqm)', 'land_area': 'Land_area (sqm)',
                'city': 'Location_City', 'location': 'Location_City',
                'year': 'Year_Built', 'built': 'Year_Built'
            }
            renamed = {}
            for col in df.columns:
                lower = col.lower().strip()
                if lower in mapping:
                    renamed[col] = mapping[lower]
            df = df.rename(columns=renamed)
            
            # Recheck
            missing_req = [col for col in required_cols if col not in df.columns]
            if missing_req:
                return None, 0, f"Missing required columns in CSV: {missing_req}. Please check the template format."
        
        # Preprocessing setup
        encoder_bundle = assets['encoder_bundle']
        feature_names = assets['feature_names']
        scaler = assets['scaler']
        reg_model = assets['reg_model']
        clf_model = assets['clf_model']
        
        city_defaults = encoder_bundle['city_defaults']
        medians = encoder_bundle['medians']
        modes = encoder_bundle['modes']
        
        # Fill missing values and engineering
        df_processed = df.copy()
        
        # Ensure numerical types
        for col in ['Bedrooms', 'Bath', 'Floor_area (sqm)', 'Land_area (sqm)', 'Year_Built']:
            df_processed[col] = pd.to_numeric(df_processed[col], errors='coerce')
            
        # Parse missing values
        num_cols = ['Bedrooms', 'Bath', 'Floor_area (sqm)', 'Land_area (sqm)']
        for col in num_cols:
            df_processed[f'{col}_was_missing'] = df_processed[col].isnull().astype(int)
            df_processed[col] = df_processed[col].fillna(medians.get(col, 120.0))
            
        # Fill Location and Coordinates based on Location_City
        df_processed['Latitude'] = df_processed['Location_City'].apply(
            lambda x: city_defaults.get(x, city_defaults['Global_Default'])['Latitude']
        )
        df_processed['Longitude'] = df_processed['Location_City'].apply(
            lambda x: city_defaults.get(x, city_defaults['Global_Default'])['Longitude']
        )
        df_processed['Location'] = df_processed['Location_City'].apply(
            lambda x: city_defaults.get(x, city_defaults['Global_Default'])['Location']
        )
        df_processed['Latitude_was_missing'] = 0
        
        # Feature Engineering
        df_processed['Total_Rooms'] = df_processed['Bedrooms'] + df_processed['Bath']
        df_processed['Year_Built_was_missing'] = df_processed['Year_Built'].isnull().astype(int)
        df_processed['Year_Built'] = df_processed['Year_Built'].fillna(encoder_bundle['median_year'])
        df_processed['House_Age'] = 2026.0 - df_processed['Year_Built']
        
        # Property tags: Check if property_type is supplied
        if 'property_type' in df_processed.columns:
            df_processed['Is_Condo'] = df_processed['property_type'].apply(lambda x: 1 if str(x).lower().strip() == 'condo' else 0)
            df_processed['Is_House'] = df_processed['property_type'].apply(lambda x: 1 if str(x).lower().strip() == 'house' else 0)
        elif 'Description' in df_processed.columns:
            desc_str = df_processed['Description'].astype(str).str.lower()
            df_processed['Is_Condo'] = desc_str.apply(lambda x: 1 if any(kw in x for kw in ['condo', 'unit', 'residences']) else 0)
            df_processed['Is_House'] = desc_str.apply(lambda x: 1 if any(kw in x for kw in ['house', 'townhouse', 'villa']) else 0)
        else:
            df_processed['Is_Condo'] = 0
            df_processed['Is_House'] = 1
            
        # Categorical Encoding
        label_encoders = encoder_bundle['label_encoders']
        
        # Encode Location
        le_loc = label_encoders['Location']
        df_processed['Location'] = df_processed['Location'].apply(
            lambda x: le_loc.transform([x])[0] if x in le_loc.classes_ else 0
        )
        
        # Encode Location_City
        le_city = label_encoders['Location_City']
        df_processed['Location_City'] = df_processed['Location_City'].apply(
            lambda x: le_city.transform([x])[0] if x in le_city.classes_ else 0
        )
        
        # Convert booleans
        for col in df_processed.columns:
            if df_processed[col].dtype == 'bool':
                df_processed[col] = df_processed[col].astype(int)
                
        # Sub-select and order columns
        X_batch = df_processed[feature_names]
        
        # Scale
        X_batch_scaled = scaler.transform(X_batch)
        
        # Predict
        preds = reg_model.predict(X_batch_scaled)
        preds = np.clip(preds, 0.0, None)
        
        pred_classes = clf_model.predict(X_batch_scaled)
        
        # Add to original DataFrame for display and download
        df_original['Predicted Price (PHP)'] = preds
        df_original['Property Market Tier'] = pred_classes
        
        return df_original, len(df_original), ""
        
    except Exception as e:
        return None, 0, f"Error processing batch prediction: {str(e)}"
