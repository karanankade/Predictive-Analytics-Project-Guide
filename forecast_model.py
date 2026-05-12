import pandas as pd
import numpy as np
import pickle
import warnings
from statsmodels.tsa.arima.model import ARIMA
from sklearn.metrics import mean_squared_error, mean_absolute_error

warnings.filterwarnings("ignore")

def build_model():
    print("Loading data...")
    df = pd.read_csv('sales_data.csv')
    df['Date'] = pd.to_datetime(df['Date'])
    
    # Aggregate to monthly revenue
    print("Preprocessing data...")
    monthly_data = df.groupby(df['Date'].dt.to_period('M'))['Revenue'].sum().reset_index()
    monthly_data['Date'] = monthly_data['Date'].dt.to_timestamp()
    monthly_data.to_csv('monthly_sales.csv', index=False)
    
    # We will use the monthly revenue as our time series
    ts = monthly_data.set_index('Date')['Revenue']
    
    # Split into train and test (last 6 months for testing)
    train = ts[:-6]
    test = ts[-6:]
    
    print("Training ARIMA model...")
    # Using a simple (1,1,1) ARIMA model.
    model = ARIMA(train, order=(1, 1, 1))
    model_fit = model.fit()
    
    print("Evaluating model...")
    predictions = model_fit.forecast(steps=len(test))
    rmse = np.sqrt(mean_squared_error(test, predictions))
    mae = mean_absolute_error(test, predictions)
    print(f"Model RMSE: {rmse:.2f}")
    print(f"Model MAE: {mae:.2f}")
    
    # Retrain on full data for future forecasting
    print("Retraining on full dataset for future forecasting...")
    final_model = ARIMA(ts, order=(1, 1, 1))
    final_model_fit = final_model.fit()
    
    # Forecast next 12 months
    future_forecast = final_model_fit.forecast(steps=12)
    forecast_dates = pd.date_range(start=ts.index[-1] + pd.DateOffset(months=1), periods=12, freq='MS')
    
    forecast_df = pd.DataFrame({
        'Date': forecast_dates,
        'Forecasted_Revenue': future_forecast.values
    })
    forecast_df.to_csv('forecast.csv', index=False)
    
    # Save the model
    with open('model.pkl', 'wb') as f:
        pickle.dump(final_model_fit, f)
        
    print("Modeling pipeline complete. Artifacts saved: monthly_sales.csv, forecast.csv, model.pkl")

if __name__ == "__main__":
    build_model()
