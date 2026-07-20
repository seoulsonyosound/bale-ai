import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Clean corporate color palette
COLORS = {
    'primary': '#0D6EFD',       # Deep Blue
    'secondary': '#6C757D',     # Cool Grey
    'success': '#198754',       # Emerald Green
    'warning': '#FFC107',       # Amber Gold
    'danger': '#DC3545',        # Crimson Red
    'info': '#0DCAF0',          # Teal Blue
    'background': '#F8F9FA',    # Light Grey
    'card_bg': '#FFFFFF',       # White
    'dark': '#212529',          # Dark Slate
    'accent': '#6F42C1'         # Purple
}

def plot_feature_importance(assets):
    """
    Renders an interactive horizontal bar chart showing feature importances.
    """
    importances = assets['metadata']['feature_importances']
    features = assets['feature_names']
    
    df_imp = pd.DataFrame({
        'Feature': features,
        'Importance': importances
    }).sort_values(by='Importance', ascending=True)
    
    # Map feature names to clean labels
    clean_labels = {
        'Floor_area (sqm)': 'Floor Area (sqm)',
        'Land_area (sqm)': 'Land Area (sqm)',
        'House_Age': 'Property Age (Years)',
        'Year_Built': 'Year Built',
        'Total_Rooms': 'Total Rooms (Beds + Baths)',
        'Location_City': 'Location City',
        'Location': 'Detailed Location String',
        'Bedrooms': 'Bedrooms',
        'Bath': 'Bathrooms',
        'Latitude': 'Latitude Coordinates',
        'Longitude': 'Longitude Coordinates',
        'Is_House': 'Property Type: House',
        'Is_Condo': 'Property Type: Condo'
    }
    df_imp['Display Feature'] = df_imp['Feature'].apply(lambda x: clean_labels.get(x, x.replace('_was_missing', ' Missing Flag')))
    
    # Slice top 12 for clean layout
    df_imp = df_imp.tail(12)
    
    fig = px.bar(
        df_imp,
        x='Importance',
        y='Display Feature',
        orientation='h',
        title='Global Feature Importance (XGBoost Split Weights)',
        labels={'Importance': 'Relative Importance', 'Display Feature': 'Property Attribute'},
        color='Importance',
        color_continuous_scale='Blues'
    )
    
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_family="Inter, sans-serif",
        font_color=COLORS['dark'],
        title_font_size=16,
        xaxis=dict(showgrid=True, gridcolor='#E9ECEF'),
        yaxis=dict(showgrid=False),
        coloraxis_showscale=False,
        margin=dict(l=20, r=20, t=40, b=20),
        height=400
    )
    
    return fig

def plot_correlation_matrix(df):
    """
    Generates a correlation heatmap for numeric features.
    """
    # Select numeric features
    numeric_df = df.select_dtypes(include=[np.number]).copy()
    
    # Clean up column names for visual appeal
    clean_cols = {
        'Price (PHP)': 'Price',
        'Bedrooms': 'Bedrooms',
        'Bath': 'Bathrooms',
        'Floor_area (sqm)': 'Floor Area',
        'Land_area (sqm)': 'Land Area',
        'Longitude': 'Longitude',
        'Latitude': 'Latitude'
    }
    
    numeric_df = numeric_df.rename(columns=clean_cols)
    cols_to_keep = [col for col in clean_cols.values() if col in numeric_df.columns]
    
    if len(cols_to_keep) < 2:
        return None
        
    corr = numeric_df[cols_to_keep].corr()
    
    fig = go.Figure(data=go.Heatmap(
        z=corr.values,
        x=corr.columns,
        y=corr.columns,
        colorscale='RdBu',
        zmin=-1,
        zmax=1,
        text=np.round(corr.values, 2),
        texttemplate="%{text}",
        showscale=True
    ))
    
    fig.update_layout(
        title='Linear Correlation Heatmap',
        font_family="Inter, sans-serif",
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=20, r=20, t=40, b=20),
        height=380
    )
    
    return fig

def plot_price_gauge(pred_price, q33, q66):
    """
    Renders a Gauge chart representing the estimated price category (Low, Medium, High).
    """
    # Max bound is 3 times the upper quartile threshold for visual spacing
    max_val = float(q66 * 3)
    
    fig = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = pred_price,
        domain = {'x': [0, 1], 'y': [0, 1]},
        number = {'valueformat': ',.0f', 'suffix': ' PHP', 'font': {'size': 22, 'color': COLORS['dark']}},
        gauge = {
            'axis': {'range': [None, max_val], 'tickwidth': 1, 'tickcolor': COLORS['dark']},
            'bar': {'color': COLORS['primary']},
            'bgcolor': "white",
            'borderwidth': 2,
            'bordercolor': "#DEE2E6",
            'steps': [
                {'range': [0, q33], 'color': '#D1E7DD'},       # Low (soft green)
                {'range': [q33, q66], 'color': '#FFF3CD'},     # Medium (soft yellow)
                {'range': [q66, max_val], 'color': '#F8D7DA'}   # High (soft red)
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': pred_price
            }
        }
    ))
    
    fig.update_layout(
        title = {'text': "Estimated Price Range Profile", 'font': {'size': 14}},
        font_family="Inter, sans-serif",
        paper_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=30, r=30, t=50, b=30),
        height=250
    )
    
    return fig

def plot_confidence_meter(pred_price, lower_bound, upper_bound):
    """
    Creates a bullet chart/meter indicating prediction confidence.
    """
    margin = (upper_bound - lower_bound) / 2
    margin_pct = (margin / pred_price) * 100 if pred_price > 0 else 0
    confidence = max(50.0, min(99.0, 100.0 - margin_pct))
    
    fig = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = confidence,
        domain = {'x': [0, 1], 'y': [0, 1]},
        number = {'suffix': '%', 'font': {'size': 24, 'color': COLORS['dark']}},
        gauge = {
            'axis': {'range': [0, 100]},
            'bar': {'color': COLORS['success']},
            'steps': [
                {'range': [0, 70], 'color': "#F8D7DA"},
                {'range': [70, 90], 'color': "#FFF3CD"},
                {'range': [90, 100], 'color': "#D1E7DD"}
            ],
            'threshold': {
                'line': {'color': COLORS['success'], 'width': 4},
                'thickness': 0.75,
                'value': confidence
            }
        }
    ))
    
    fig.update_layout(
        title = {'text': "Model Prediction Confidence Score", 'font': {'size': 14}},
        font_family="Inter, sans-serif",
        paper_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=30, r=30, t=50, b=30),
        height=250
    )
    
    return fig

def plot_actual_vs_predicted(metadata):
    """
    Plots Actual vs. Predicted values.
    """
    eval_data = metadata['regression_eval']
    y_test = np.array(eval_data['y_test'])
    y_pred = np.array(eval_data['y_pred'])
    
    fig = go.Figure()
    
    # Scatter plot
    fig.add_trace(go.Scatter(
        x=y_test,
        y=y_pred,
        mode='markers',
        marker=dict(color=COLORS['primary'], opacity=0.5, size=8),
        name='Predictions'
    ))
    
    # Identity line y=x
    min_val = min(y_test.min(), y_pred.min())
    max_val = max(y_test.max(), y_pred.max())
    fig.add_trace(go.Scatter(
        x=[min_val, max_val],
        y=[min_val, max_val],
        mode='lines',
        line=dict(color=COLORS['danger'], width=2, dash='dash'),
        name='Ideal Fit (y=x)'
    ))
    
    fig.update_layout(
        title='Actual vs. Predicted House Prices',
        xaxis_title='Actual Price (PHP)',
        yaxis_title='Predicted Price (PHP)',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_family="Inter, sans-serif",
        xaxis=dict(showgrid=True, gridcolor='#E9ECEF'),
        yaxis=dict(showgrid=True, gridcolor='#E9ECEF'),
        margin=dict(l=20, r=20, t=40, b=20),
        height=380,
        showlegend=True
    )
    
    return fig

def plot_residual_scatter(metadata):
    """
    Plots residuals vs. predicted values.
    """
    eval_data = metadata['regression_eval']
    y_test = np.array(eval_data['y_test'])
    y_pred = np.array(eval_data['y_pred'])
    residuals = y_test - y_pred
    
    fig = go.Figure()
    
    # Scatter
    fig.add_trace(go.Scatter(
        x=y_pred,
        y=residuals,
        mode='markers',
        marker=dict(color=COLORS['accent'], opacity=0.5, size=8),
        name='Residuals'
    ))
    
    # Zero line
    fig.add_trace(go.Scatter(
        x=[y_pred.min(), y_pred.max()],
        y=[0, 0],
        mode='lines',
        line=dict(color=COLORS['danger'], width=2, dash='dash'),
        name='Zero Residual Line'
    ))
    
    fig.update_layout(
        title='Residuals vs. Predicted Values',
        xaxis_title='Predicted Price (PHP)',
        yaxis_title='Residual (Actual - Predicted)',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_family="Inter, sans-serif",
        xaxis=dict(showgrid=True, gridcolor='#E9ECEF'),
        yaxis=dict(showgrid=True, gridcolor='#E9ECEF'),
        margin=dict(l=20, r=20, t=40, b=20),
        height=380,
        showlegend=False
    )
    
    return fig

def plot_residual_distribution(metadata):
    """
    Plots the histogram/distribution of residuals.
    """
    eval_data = metadata['regression_eval']
    y_test = np.array(eval_data['y_test'])
    y_pred = np.array(eval_data['y_pred'])
    residuals = y_test - y_pred
    
    fig = px.histogram(
        x=residuals,
        nbins=40,
        title="Distribution of Model Prediction Residuals",
        labels={'x': 'Prediction Error (PHP)'},
        color_discrete_sequence=[COLORS['accent']]
    )
    
    # Mean line
    fig.add_vline(x=0, line_dash="dash", line_color="red", line_width=2)
    
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_family="Inter, sans-serif",
        xaxis=dict(showgrid=True, gridcolor='#E9ECEF'),
        yaxis=dict(showgrid=True, gridcolor='#E9ECEF'),
        margin=dict(l=20, r=20, t=40, b=20),
        height=380
    )
    
    return fig

def plot_target_distribution(df, col='Price (PHP)'):
    """
    Plots the distribution of the house price target variable.
    """
    fig = make_subplots(rows=1, cols=2, subplot_titles=("Raw Price (PHP) Distribution", "Log-Transformed Distribution"))
    
    prices = df[col].dropna()
    log_prices = np.log1p(prices)
    
    # Raw hist
    fig.add_trace(
        go.Histogram(x=prices, nbinsx=40, marker_color=COLORS['primary'], name='Raw Price'),
        row=1, col=1
    )
    
    # Log hist
    fig.add_trace(
        go.Histogram(x=log_prices, nbinsx=40, marker_color=COLORS['accent'], name='Log Price'),
        row=1, col=2
    )
    
    fig.update_layout(
        title_text="Target Variable Analysis (Price Profile)",
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_family="Inter, sans-serif",
        showlegend=False,
        height=350,
        margin=dict(l=20, r=20, t=60, b=20)
    )
    
    fig.update_xaxes(showgrid=True, gridcolor='#E9ECEF', row=1, col=1)
    fig.update_xaxes(showgrid=True, gridcolor='#E9ECEF', row=1, col=2)
    fig.update_yaxes(showgrid=True, gridcolor='#E9ECEF', row=1, col=1)
    fig.update_yaxes(showgrid=True, gridcolor='#E9ECEF', row=1, col=2)
    
    return fig

def plot_confusion_matrix_heatmap(classification_eval):
    """
    Generates a heatmap representation of the Confusion Matrix.
    """
    cm = np.array(classification_eval['confusion_matrix'])
    labels = classification_eval['labels']
    
    fig = go.Figure(data=go.Heatmap(
        z=cm,
        x=[f"Predicted {l}" for l in labels],
        y=[f"Actual {l}" for l in labels],
        colorscale='Greens',
        text=cm,
        texttemplate="%{text}",
        showscale=True
    ))
    
    fig.update_layout(
        title='Classifier Confusion Matrix Heatmap (Tier Allocation)',
        font_family="Inter, sans-serif",
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=20, r=20, t=40, b=20),
        height=350
    )
    
    return fig

def plot_model_comparison(metadata):
    """
    Creates a comparison chart for different regression models (hardcoded benchmarking).
    """
    # Baseline comparison data from training logs
    models = ['XGBoost', 'CatBoost', 'Extra Trees', 'Random Forest', 'Decision Tree', 'Gradient Boosting', 'LightGBM', 'Linear Regression']
    r2_scores = [0.9817, 0.9805, 0.9784, 0.9733, 0.9693, 0.9616, 0.9546, 0.7762]
    
    df_compare = pd.DataFrame({
        'Model': models,
        'R² Score': r2_scores
    }).sort_values(by='R² Score', ascending=True)
    
    fig = px.bar(
        df_compare,
        x='R² Score',
        y='Model',
        orientation='h',
        title='Benchmark Evaluation comparison (R² Test Scores)',
        color='R² Score',
        color_continuous_scale='Viridis'
    )
    
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_family="Inter, sans-serif",
        font_color=COLORS['dark'],
        title_font_size=15,
        xaxis=dict(showgrid=True, gridcolor='#E9ECEF', range=[0, 1.0]),
        yaxis=dict(showgrid=False),
        coloraxis_showscale=False,
        margin=dict(l=20, r=20, t=40, b=20),
        height=350
    )
    
    return fig
