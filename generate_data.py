import pandas as pd
import numpy as np
import datetime

def generate_sales_data(filename='sales_data.csv', start_year=2021, num_years=3):
    start_date = datetime.date(start_year, 1, 1)
    end_date = start_date + datetime.timedelta(days=num_years*365 - 1)
    
    dates = pd.date_range(start=start_date, end=end_date, freq='D')
    
    # We'll simulate a baseline trend and some seasonality
    np.random.seed(42)
    
    # Base daily sales starting around 500, growing slowly
    base_sales = np.linspace(500, 1000, len(dates))
    
    # Add weekly seasonality: higher on weekends
    weekly_seasonality = np.where(dates.weekday >= 5, 200, 0)
    
    # Add yearly seasonality: higher in summer and holiday season
    day_of_year = dates.dayofyear
    yearly_seasonality = 150 * np.sin(2 * np.pi * day_of_year / 365.25) + \
                         300 * np.exp(-((day_of_year - 350) / 10)**2) # Holiday bump
                         
    noise = np.random.normal(0, 50, len(dates))
    
    total_sales = base_sales + weekly_seasonality + yearly_seasonality + noise
    total_sales = np.maximum(total_sales, 0) # Ensure no negative sales
    
    data = []
    
    # Create individual transactions
    products = ['Electronics', 'Clothing', 'Home & Garden', 'Toys', 'Sports']
    
    for date, daily_total in zip(dates, total_sales):
        # Determine number of transactions for the day
        num_transactions = int(np.random.normal(50, 10))
        num_transactions = max(5, num_transactions)
        
        # Split daily total among transactions
        transaction_amounts = np.random.dirichlet(np.ones(num_transactions)) * daily_total
        
        for amt in transaction_amounts:
            data.append({
                'Date': date,
                'Transaction_ID': f"TRX_{np.random.randint(100000, 999999)}",
                'Product_Category': np.random.choice(products, p=[0.3, 0.25, 0.2, 0.1, 0.15]),
                'Revenue': round(amt, 2),
                'Units_Sold': max(1, int(amt / np.random.uniform(10, 50)))
            })
            
    df = pd.DataFrame(data)
    df.to_csv(filename, index=False)
    print(f"Successfully generated {filename} with {len(df)} records.")

if __name__ == "__main__":
    print("Generating synthetic sales data...")
    generate_sales_data()
