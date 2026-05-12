import pandas as pd
import matplotlib.pyplot as plt
import os

def create_images():
    # Create the output directory
    os.makedirs('output', exist_ok=True)
    
    # Load data
    historical = pd.read_csv('monthly_sales.csv')
    historical['Date'] = pd.to_datetime(historical['Date'])
    
    forecast = pd.read_csv('forecast.csv')
    forecast['Date'] = pd.to_datetime(forecast['Date'])
    
    # Plot 1: Historical Revenue Trend
    plt.figure(figsize=(10, 5))
    plt.plot(historical['Date'], historical['Revenue'], color='#1f77b4', marker='o')
    plt.title('Historical Monthly Revenue')
    plt.xlabel('Date')
    plt.ylabel('Revenue ($)')
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.tight_layout()
    plt.savefig('output/historical_revenue.png')
    plt.close()
    
    # Plot 2: Historical vs Forecast
    plt.figure(figsize=(12, 6))
    plt.plot(historical['Date'], historical['Revenue'], label='Historical', color='#1f77b4', marker='o')
    
    # Connect the forecast line to the end of historical
    last_hist_date = historical['Date'].iloc[-1]
    last_hist_val = historical['Revenue'].iloc[-1]
    
    forecast_dates = [last_hist_date] + forecast['Date'].tolist()
    forecast_vals = [last_hist_val] + forecast['Forecasted_Revenue'].tolist()
    
    plt.plot(forecast_dates, forecast_vals, label='Forecast (Next 12 Months)', color='#ff7f0e', linestyle='--', marker='s')
    
    plt.title('Revenue Forecast Projection (ARIMA)')
    plt.xlabel('Date')
    plt.ylabel('Revenue ($)')
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.tight_layout()
    plt.savefig('output/forecast_projection.png')
    plt.close()

if __name__ == "__main__":
    create_images()
    print("Output images saved to 'output' folder.")
