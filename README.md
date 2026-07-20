# BaleAI: AI-Powered House Price Prediction & Market Analytics Platform

BaleAI is a professional, responsive, and production-ready Streamlit web application that uses a tuned XGBoost Machine Learning model to calculate high-precision residential property valuations in the Philippines. It features a modern glassmorphic UI layout inspired by Google AI Studio, Airbnb Analytics, and Airbnb design guidelines.

This application is suitable for thesis defenses, capstone presentations, and commercial deployment.

---

## 📁 Project Folder Structure

```
HPP_model/
├── app.py                      # Streamlit Main App entrypoint (Navigation Router)
├── requirements.txt            # Package dependencies
├── README.md                   # Setup & Deployment Guide
├── PH_houses_v2.csv            # Original raw listings dataset
├── House_Price_Prediction_Pipeline.ipynb  # Google Colab ML Training Notebook
│
├── assets/                     # Static graphical assets
│   ├── logo.png                # AI platform branding logo
│   └── background.png          # Minimalist modern architectural background
│
├── models/                     # Serialized machine learning models & metadata
│   ├── trained_model.pkl       # Serialized XGBoost Regressor model
│   ├── scaler.pkl              # Fitted MinMaxScaler
│   ├── encoder.pkl             # Encoded Location columns & default city values
│   ├── classifier_model.pkl    # Random Forest Classifier (Academic demo)
│   ├── model_features.pkl      # Feature column order schema
│   └── model_metadata.pkl      # Pre-calculated benchmark evaluation metrics
│
├── pages/                      # Multi-page dashboard scripts
│   ├── Dashboard.py            # Welcome page, KPIs, & pipeline workflows
│   ├── Prediction.py           # Real-time form & batch CSV predictions
│   ├── Dataset.py              # Paginated directory explorer & interactive histograms
│   ├── Model_Analytics.py      # Error scatters, residual checks, & confusion matrix
│   └── About.py                # Tech stack badges & academic developer metadata
│
└── utils/                      # Modular utility packages
    ├── preprocessing.py        # Imputations, outlier filters, & feature engineerings
    ├── predictor.py            # Single & batch inference operations & explanations
    ├── visualizations.py       # Custom styled Plotly chart generators
    └── helpers.py              # Base64 image loaders & custom CSS injections
```

---

## 🛠 Features

1. **Market Dashboard:** Renders system statistics (1,500 listing records, R² fit accuracy of 98.09%, MAE error bounds), XGBoost split weights, and end-to-end processing diagrams.
2. **Real-time Valuation Form:** Grouped collapsibles (Location, Size, Specs, Layout) with default Coordinate mapping based on the chosen city to prevent input friction.
3. **Valuation Output:** Large currency highlights, confidence meters (95% bounds), inference speed times, and a text driver explaining key pricing factors.
4. **Batch Prediction:** Upload a property CSV file using a simple template, run parallel evaluations, and download forecasted records as CSV.
5. **Session Prediction History:** Stores previous predictions in a responsive data table for comparative side-by-side analysis.
6. **Dataset Explorer:** Tabular grid with keyword search, sorting, multi-city filtering, pagination, data completeness profiles, and correlation heatmaps.
7. **Model Analytics:** Performance graphs comparing 10 regression algorithms, error distributions, learning curves, and actual vs. predicted scatters.
8. **Academic Classification Demo:** Categorizes target valuations into market tiers (Low, Medium, High) via a Random Forest Classifier to satisfy defense panels requiring confusion matrices and weighted Precision/Recall/F1 metrics.

---

## 🚀 Local Installation & Deployment Guide

### Prerequisites
Make sure you have **Python 3.8+** installed on your system.

### Step 1: Clone or Open the Directory
Open your terminal/command prompt and change directory to the project workspace:
```bash
cd path/to/HPP_model
```

### Step 2: Create a Virtual Environment (Recommended)
Create and activate a virtual environment to prevent package version conflicts:
* **Windows (PowerShell):**
  ```powershell
  python -m venv venv
  .\venv\Scripts\Activate.ps1
  ```
* **macOS / Linux:**
  ```bash
  python3 -m venv venv
  source venv/bin/activate
  ```

### Step 3: Install Required Dependencies
Install the required machine learning and plotting libraries listed in `requirements.txt`:
```bash
pip install -r requirements.txt
```

### Step 4: Run Model Training (Optional)
The pre-compiled models are already included in the `models/` directory. However, if you modify the raw `PH_houses_v2.csv` dataset, you can retrain the models and regenerate the `.pkl` files by executing:
```bash
python utils/train.py
```

### Step 5: Launch the Streamlit Web Application
Run the Streamlit server to open the application in your local browser:
```bash
streamlit run app.py
```
If it doesn't open automatically, navigate to the URL printed in the terminal (usually `http://localhost:8501`).

---

## ☁ Streamlit Cloud Deployment Instructions

Deploying ProphetAI to Streamlit Cloud is free, fast, and requires no local server setup.

### Step 1: Push Project to GitHub
1. Create a public repository on your GitHub account (e.g., `PH-House-Price-Predictor`).
2. Initialize Git, add files, commit, and push the workspace directory to your repository:
   ```bash
   git init
   git add .
   git commit -m "Initialize ProphetAI platform codebase"
   git branch -M main
   git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
   git push -u origin main
   ```

### Step 2: Connect to Streamlit Community Cloud
1. Visit the [Streamlit Community Cloud](https://share.streamlit.io/) portal.
2. Sign in with your GitHub account.
3. Click the **"New App"** button in the top right.

### Step 3: Configure Deployment Fields
1. **Repository:** Select your repository (e.g. `YOUR_USERNAME/YOUR_REPO_NAME`).
2. **Branch:** Select `main` (or `master`).
3. **Main file path:** Enter `app.py`.
4. Click **"Deploy!"**.

Streamlit will provision a container, read the `requirements.txt` file, install dependencies, compile the packages, and run the app. In 1–2 minutes, your AI platform will be live on a public URL!
