from flask import Flask, jsonify, render_template_string, send_from_directory
import os
import pandas as pd

app = Flask(__name__)

def ensure_data():
    if not os.path.exists('monthly_sales.csv') or not os.path.exists('forecast.csv'):
        try:
            if not os.path.exists('sales_data.csv'):
                import generate_data
                generate_data.main()
            import forecast_model
            forecast_model.build_model()
            import generate_output_images
            generate_output_images.create_images()
        except Exception as e:
            print("Error generating forecast data:", e)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Predictive Analytics: Retail Sales Forecast</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body { background-color: #0f172a; color: #f8fafc; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
        .hero { background: linear-gradient(135deg, #1e293b 0%, #334155 100%); padding: 2.5rem 0; margin-bottom: 2rem; border-bottom: 1px solid #475569; }
        .card { background-color: #1e293b; border: 1px solid #334155; border-radius: 0.75rem; color: #f8fafc; margin-bottom: 1.5rem; }
        .card-header { background-color: #0f172a; border-bottom: 1px solid #334155; font-weight: 600; color: #38bdf8; }
        .metric-value { font-size: 2rem; font-weight: bold; color: #4ade80; }
        .metric-label { font-size: 0.9rem; color: #94a3b8; }
    </style>
</head>
<body>
    <div class="hero text-center">
        <div class="container">
            <h1 class="display-5 fw-bold text-sky-400">📈 Retail Sales Forecasting</h1>
            <p class="lead text-slate-300">ARIMA Time-Series Predictive Analytics</p>
        </div>
    </div>

    <div class="container">
        <div class="row text-center mb-4">
            <div class="col-md-4">
                <div class="card p-3">
                    <div class="metric-label">Total Historical Revenue</div>
                    <div class="metric-value">${{ "{:,.2f}".format(total_hist) }}</div>
                </div>
            </div>
            <div class="col-md-4">
                <div class="card p-3">
                    <div class="metric-label">Avg Monthly Revenue</div>
                    <div class="metric-value">${{ "{:,.2f}".format(avg_monthly) }}</div>
                </div>
            </div>
            <div class="col-md-4">
                <div class="card p-3">
                    <div class="metric-label">Projected Next 12 Months</div>
                    <div class="metric-value text-emerald-400">${{ "{:,.2f}".format(expected_future) }}</div>
                </div>
            </div>
        </div>

        <div class="row">
            <div class="col-md-12">
                <div class="card">
                    <div class="card-header d-flex justify-content-between align-items-center">
                        <span>Revenue Forecast Projection (ARIMA)</span>
                        <a href="/api/forecast" class="btn btn-sm btn-outline-info" target="_blank">Raw API Data</a>
                    </div>
                    <div class="card-body text-center">
                        <img src="/output/forecast_projection.png" class="img-fluid rounded" alt="Forecast Chart" onerror="this.src='https://via.placeholder.com/800x400?text=Chart+Generating...'">
                    </div>
                </div>
            </div>
        </div>
    </div>
</body>
</html>
"""

@app.route('/')
def index():
    ensure_data()
    total_hist, avg_monthly, expected_future = 0.0, 0.0, 0.0
    if os.path.exists('monthly_sales.csv') and os.path.exists('forecast.csv'):
        hist = pd.read_csv('monthly_sales.csv')
        fc = pd.read_csv('forecast.csv')
        total_hist = hist['Revenue'].sum()
        avg_monthly = hist['Revenue'].mean()
        expected_future = fc['Forecasted_Revenue'].sum()
    return render_template_string(HTML_TEMPLATE, total_hist=total_hist, avg_monthly=avg_monthly, expected_future=expected_future)

@app.route('/api/forecast')
def api_forecast():
    ensure_data()
    if os.path.exists('forecast.csv'):
        fc = pd.read_csv('forecast.csv')
        return jsonify(fc.to_dict(orient='records'))
    return jsonify({"error": "Data not available"}), 404

@app.route('/output/<filename>')
def serve_output(filename):
    return send_from_directory('output', filename)

if __name__ == '__main__':
    ensure_data()
    app.run(debug=True, port=5000)
