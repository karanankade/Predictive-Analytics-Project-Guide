# 📈 Predictive Analytics: Retail Sales Forecasting

A end-to-end Predictive Analytics project featuring daily data generation with realistic trend/seasonality components, an **ARIMA Time-Series Forecasting Model**, model persistence, and an interactive **Streamlit Web Dashboard**.

---

## 📌 Features

- **Synthetic Daily Sales Generator (`generate_data.py`)**:
  - Generates 3 years of daily transaction-level sales data (`sales_data.csv`).
  - Models complex patterns including baseline growth trends, weekly seasonality (weekend peaks), and yearly seasonality (holiday bumps).
- **Time-Series Modeling Pipeline (`forecast_model.py`)**:
  - Aggregates daily transactions into monthly revenue totals (`monthly_sales.csv`).
  - Splits data into training and test sets (evaluating on the last 6 months).
  - Trains an **ARIMA(1, 1, 1)** model and calculates performance metrics (**RMSE** and **MAE**).
  - Retrains on the complete dataset to project revenue 12 months into the future (`forecast.csv`).
  - Serializes the trained ARIMA model object (`model.pkl`).
- **Interactive Dark-Themed Dashboard (`dashboard.py`)**:
  - Built with **Streamlit** for real-time visualization.
  - Features KPI metric cards: Total Historical Revenue, Average Monthly Revenue, and Projected Next 12 Months Revenue.
  - Interactive plot showing seamless transition from historical actuals to forecasted revenue.
  - Key business insights section for executive decision-making.

---

## 🛠️ Tech Stack

- **Language**: Python 3.8+
- **Web Framework**: `streamlit`
- **Time-Series Modeling**: `statsmodels` (ARIMA)
- **Machine Learning Metrics**: `scikit-learn`
- **Data Manipulation & Plotting**: `pandas`, `numpy`, `matplotlib`

---

## 📁 Directory Structure

```text
Predictive Analytics Project Guide/
├── generate_data.py            # Generates synthetic daily sales transactions (sales_data.csv)
├── forecast_model.py           # Aggregates data, trains ARIMA model, exports forecasts & model.pkl
├── dashboard.py                # Streamlit web application for interactive forecasting
├── sales_data.csv              # Synthetic multi-year daily transaction dataset (~2.2 MB)
├── monthly_sales.csv           # Monthly aggregated historical sales data
├── forecast.csv                # 12-month future revenue predictions
├── model.pkl                   # Saved ARIMA model binary
├── requirements.txt            # Python dependency list
├── output/                     # Saved charts & visualization snapshots
└── README.md                   # Project documentation
```

---

## 🚀 Quick Start Guide

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Generate Daily Sales Data
```bash
python generate_data.py
```
*Output*: Creates `sales_data.csv` with simulated multi-year transactions.

### 3. Build & Evaluate Forecast Model
```bash
python forecast_model.py
```
*Output*:
- Aggregates data to `monthly_sales.csv`.
- Trains ARIMA model and prints RMSE / MAE metrics.
- Generates 12-month forecast in `forecast.csv` and saves model binary to `model.pkl`.

### 4. Launch Interactive Streamlit Dashboard
```bash
streamlit run dashboard.py
```
*Access*: Open your browser at `http://localhost:8501`.

---

## 📊 Business Value & Insights

- **Inventory Planning**: Helps retail managers anticipate seasonal demand surges and prepare stock levels accordingly.
- **Financial Projections**: Provides executive teams with data-backed revenue projections for budget allocation and forecasting.
- **Model Evaluation**: Uses quantitative regression metrics (RMSE/MAE) to validate prediction confidence before deployment.

---
