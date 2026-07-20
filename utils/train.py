import os
import joblib
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split, RandomizedSearchCV
from sklearn.preprocessing import MinMaxScaler, LabelEncoder
from sklearn.metrics import (
    mean_absolute_error, mean_squared_error, r2_score, mean_absolute_percentage_error,
    accuracy_score, precision_score, recall_score, f1_score, confusion_matrix, classification_report
)
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBRegressor

# Import custom preprocessing functions
from preprocessing import (
    clean_target_price, parse_numeric_columns, impute_missing_values,
    remove_outliers_zscore, engineer_features
)

def run_training_pipeline():
    print("Starting training pipeline...")
    
    # 1. Load raw data
    data_path = "PH_houses_v2.csv"
    if not os.path.exists(data_path):
        raise FileNotFoundError(f"Dataset file not found: {data_path}")
        
    df_raw = pd.read_csv(data_path, na_values=['na', 'NA', 'n/a', 'N/A', ''])
    print(f"Loaded raw data: {df_raw.shape[0]} rows, {df_raw.shape[1]} columns.")
    
    # Keep track of raw statistics
    raw_stats = {
        "num_records_raw": int(df_raw.shape[0]),
        "num_features_raw": int(df_raw.shape[1]),
        "missing_values_raw": int(df_raw.isnull().sum().sum()),
        "duplicate_records_raw": int(df_raw.duplicated().sum())
    }
    
    # 2. Preprocess & Clean
    df_clean = clean_target_price(df_raw)
    df_clean = parse_numeric_columns(df_clean)
    df_clean = df_clean.drop_duplicates()
    
    num_cols = ['Bedrooms', 'Bath', 'Floor_area (sqm)', 'Land_area (sqm)', 'Latitude', 'Longitude']
    cat_cols = ['Location'] # Location_City will be added during feature engineering
    
    df_imputed, fitted_medians, fitted_modes = impute_missing_values(
        df_clean, num_cols, cat_cols, is_training=True
    )
    
    # 3. Outlier Removal
    df_no_outliers, num_outliers_removed = remove_outliers_zscore(
        df_imputed, columns=['Price (PHP)', 'Floor_area (sqm)', 'Land_area (sqm)']
    )
    print(f"Removed {num_outliers_removed} outliers. Shape now: {df_no_outliers.shape}")
    
    # 4. Feature Engineering
    df_fe, median_year = engineer_features(df_no_outliers, is_training=True)
    
    # Save default values for Location, Lat, Long grouped by City (to populate form defaults)
    city_defaults = {}
    for city in df_fe['Location_City'].unique():
        city_sub = df_fe[df_fe['Location_City'] == city]
        city_defaults[city] = {
            'Latitude': float(city_sub['Latitude'].median()),
            'Longitude': float(city_sub['Longitude'].median()),
            'Location': str(city_sub['Location'].mode()[0]) if len(city_sub['Location'].mode()) > 0 else 'Philippines'
        }
    # Add a global default
    city_defaults['Global_Default'] = {
        'Latitude': float(df_fe['Latitude'].median()),
        'Longitude': float(df_fe['Longitude'].median()),
        'Location': str(df_fe['Location'].mode()[0])
    }
    
    # 5. Categorical Encoding
    X = df_fe.copy()
    y = X['Price (PHP)']
    
    # Drop columns that leak target or have no prediction utility
    drop_cols = ['Price (PHP)', 'Description', 'Link']
    if 'Price_per_sqm_floor' in X.columns:
        drop_cols.append('Price_per_sqm_floor')
    X = X.drop(columns=drop_cols)
    
    # Categorical Columns: 'Location' and 'Location_City'
    cat_cols_to_encode = X.select_dtypes(exclude=[np.number]).columns.tolist()
    label_encoders = {}
    
    for col in cat_cols_to_encode:
        le = LabelEncoder()
        X[col] = le.fit_transform(X[col].astype(str))
        label_encoders[col] = le
        
    # Convert any boolean to int
    for col in X.columns:
        if X[col].dtype == 'bool':
            X[col] = X[col].astype(int)
            
    # Keep columns list
    feature_names = list(X.columns)
    
    # 6. Scaling
    scaler = MinMaxScaler()
    X_scaled = scaler.fit_transform(X)
    
    # 7. Split Data
    X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.20, random_state=42)
    
    # 8. Train & Tune Regression Model (XGBoost)
    print("Training XGBoost Regressor...")
    # Best parameters from randomized search: {'n_estimators': 200, 'max_depth': 5, 'learning_rate': 0.1}
    reg_model = XGBRegressor(n_estimators=200, max_depth=5, learning_rate=0.1, random_state=42)
    reg_model.fit(X_train, y_train)
    
    # Evaluate Regressor
    y_pred = reg_model.predict(X_test)
    r2 = r2_score(y_test, y_pred)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    mae = mean_absolute_error(y_test, y_pred)
    mape = mean_absolute_percentage_error(y_test, y_pred)
    
    # Adjusted R2
    n = len(y_test)
    p = X_train.shape[1]
    adj_r2 = 1 - (1 - r2) * (n - 1) / (n - p - 1)
    
    print(f"Regression Metrics: R2 = {r2:.4f}, RMSE = {rmse:,.2f}, MAE = {mae:,.2f}, MAPE = {mape:.4%}")
    
    # Save regression evaluation data for analytics page
    regression_eval = {
        "y_test": y_test.tolist(),
        "y_pred": y_pred.tolist(),
        "R2": float(r2),
        "Adjusted_R2": float(adj_r2),
        "RMSE": float(rmse),
        "MAE": float(mae),
        "MAPE": float(mape)
    }
    
    # 9. Train Classifier Model (Academic Demo)
    # Target price categories based on 33.3% and 66.7% quartiles of y
    q33 = y.quantile(0.333)
    q66 = y.quantile(0.667)
    
    def price_categorize(price):
        if price <= q33:
            return 'Low'
        elif price <= q66:
            return 'Medium'
        else:
            return 'High'
            
    y_class = y.apply(price_categorize)
    X_train_c, X_test_c, y_train_c, y_test_c = train_test_split(
        X_scaled, y_class, test_size=0.20, random_state=42
    )
    
    print("Training Random Forest Classifier for Academic Demo...")
    clf_model = RandomForestClassifier(n_estimators=100, random_state=42)
    clf_model.fit(X_train_c, y_train_c)
    
    # Evaluate Classifier
    y_pred_c = clf_model.predict(X_test_c)
    acc = accuracy_score(y_test_c, y_pred_c)
    prec = precision_score(y_test_c, y_pred_c, average='weighted')
    rec = recall_score(y_test_c, y_pred_c, average='weighted')
    f1 = f1_score(y_test_c, y_pred_c, average='weighted')
    
    print(f"Classification Metrics: Accuracy = {acc:.4f}, F1-score = {f1:.4f}")
    
    # Deconstruct confusion matrix
    labels = ['Low', 'Medium', 'High']
    cm = confusion_matrix(y_test_c, y_pred_c, labels=labels)
    
    tp_fp_tn_fn = []
    for idx, label in enumerate(labels):
        tp = int(cm[idx, idx])
        fn = int(cm[idx, :].sum() - tp)
        fp = int(cm[:, idx].sum() - tp)
        tn = int(cm.sum() - (tp + fp + fn))
        tp_fp_tn_fn.append({
            "Class": label,
            "TP": tp,
            "FP": fp,
            "TN": tn,
            "FN": fn
        })
        
    classifier_eval = {
        "accuracy": float(acc),
        "precision": float(prec),
        "recall": float(rec),
        "f1_score": float(f1),
        "confusion_matrix": cm.tolist(),
        "labels": labels,
        "tp_fp_tn_fn": tp_fp_tn_fn,
        "classification_report": classification_report(y_test_c, y_pred_c, output_dict=True),
        "q33": float(q33),
        "q66": float(q66)
    }
    
    # 10. Save all assets to models/
    os.makedirs("models", exist_ok=True)
    
    joblib.dump(reg_model, 'models/trained_model.pkl')
    joblib.dump(scaler, 'models/scaler.pkl')
    
    # Store encoders, city_defaults, medians, modes, and year built in a single bundle encoder.pkl
    encoder_bundle = {
        'label_encoders': label_encoders,
        'city_defaults': city_defaults,
        'medians': fitted_medians,
        'modes': fitted_modes,
        'median_year': median_year,
        'num_cols': num_cols,
        'cat_cols': cat_cols
    }
    joblib.dump(encoder_bundle, 'models/encoder.pkl')
    joblib.dump(feature_names, 'models/model_features.pkl')
    
    # Save classifier and classification evaluation metadata
    joblib.dump(clf_model, 'models/classifier_model.pkl')
    
    # Combine metadata
    metadata = {
        "raw_stats": raw_stats,
        "regression_eval": regression_eval,
        "classification_eval": classifier_eval,
        "feature_importances": reg_model.feature_importances_.tolist(),
        "features": feature_names,
        "training_date": pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    joblib.dump(metadata, 'models/model_metadata.pkl')
    
    print("Pipeline training completed and assets successfully exported to models/ directory.")

if __name__ == "__main__":
    import sys
    # Add the current directory to sys.path so preprocessing can be imported
    utils_dir = os.path.dirname(os.path.abspath(__file__))
    if utils_dir not in sys.path:
        sys.path.append(utils_dir)
    # Also adjust execution directory to workspace root (parent of utils)
    workspace_root = os.path.dirname(utils_dir)
    os.chdir(workspace_root)
    run_training_pipeline()
