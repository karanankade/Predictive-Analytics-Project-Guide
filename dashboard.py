import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Set page configuration
st.set_page_config(page_title="Retail Sales Forecast", page_icon="📈", layout="wide")

# Custom CSS for better aesthetics
st.markdown("""
<style>
    .metric-card {
        background-color: #1e1e1e;
        border-radius: 10px;
        padding: 20px;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.5);
        text-align: center;
        color: white;
    }
    .metric-value {
        font-size: 2rem;
        font-weight: bold;
        color: #4CAF50;
    }
    .metric-label {
        font-size: 1rem;
        color: #aaaaaa;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    try:
        historical = pd.read_csv('monthly_sales.csv')
        historical['Date'] = pd.to_datetime(historical['Date'])
        
        forecast = pd.read_csv('forecast.csv')
        forecast['Date'] = pd.to_datetime(forecast['Date'])
        return historical, forecast
    except FileNotFoundError:
        return None, None

st.title("📈 Predictive Analytics: Retail Sales Forecasting")
st.markdown("This dashboard presents the historical sales performance and the 12-month projected revenue using an ARIMA Time-Series forecasting model.")

historical, forecast = load_data()

if historical is None:
    st.error("Data files not found. Please run the data generation and modeling pipeline first.")
else:
    # Key Metrics
    total_historical = historical['Revenue'].sum()
    avg_monthly = historical['Revenue'].mean()
    expected_future = forecast['Forecasted_Revenue'].sum()
    
    # Layout for metrics
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Total Historical Revenue</div>
            <div class="metric-value">${total_historical:,.2f}</div>
        </div>
        """, unsafe_allow_html=True)
        
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Avg Monthly Revenue</div>
            <div class="metric-value">${avg_monthly:,.2f}</div>
        </div>
        """, unsafe_allow_html=True)
        
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Projected Next 12 Months</div>
            <div class="metric-value">${expected_future:,.2f}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    
    # Visualizations
    st.subheader("Historical vs Forecasted Revenue Trend")
    
    fig, ax = plt.subplots(figsize=(12, 6))
    
    # Plot historical
    ax.plot(historical['Date'], historical['Revenue'], label='Historical Actuals', marker='o', color='#1f77b4', linewidth=2)
    
    # Plot forecast
    # We want the forecast line to connect with the last historical point
    last_hist_date = historical['Date'].iloc[-1]
    last_hist_val = historical['Revenue'].iloc[-1]
    
    forecast_dates = [last_hist_date] + forecast['Date'].tolist()
    forecast_vals = [last_hist_val] + forecast['Forecasted_Revenue'].tolist()
    
    ax.plot(forecast_dates, forecast_vals, label='Forecasted (ARIMA)', marker='s', color='#ff7f0e', linestyle='--', linewidth=2)
    
    ax.set_title("Revenue Over Time", fontsize=14, pad=15)
    ax.set_xlabel("Date", fontsize=12)
    ax.set_ylabel("Revenue ($)", fontsize=12)
    ax.grid(True, linestyle='--', alpha=0.6)
    ax.legend(fontsize=11)
    
    # Formatting y-axis as currency
    fmt = '${x:,.0f}'
    tick = plt.FuncFormatter(lambda x, pos: fmt.format(x=x))
    ax.yaxis.set_major_formatter(tick)
    
    st.pyplot(fig)
    
    st.markdown("---")
    
    # Business Insights section
    st.subheader("🧠 Key Business Insights")
    st.markdown("""
    Based on the predictive model:
    - **Demand Trend:** The model captures the underlying steady growth and seasonal fluctuations in the historical data, projecting a continued upward trajectory.
    - **Revenue Forecast:** Over the next 12 months, the expected total revenue is approximately **${:,.2f}**.
    - **Opportunities:** Consider aligning marketing campaigns with historical seasonal peaks to maximize returns. The forecast provides a baseline for inventory planning.
    """.format(expected_future))
