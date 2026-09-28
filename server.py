"""
=============================================================================
 server.py -- Flask API Server for Bank Transaction Analysis
=============================================================================
 This server provides REST API endpoints for the frontend:
   - /api/filter-options  → Returns unique values for each filter dropdown
   - /api/analyze         → Accepts filters, returns statistics + insights
   - /api/overall-stats   → Returns overall dataset statistics

 Usage:
   python server.py
   → Starts Flask server at http://localhost:5000
   → Frontend at http://localhost:5000/
=============================================================================
"""

from flask import Flask, request, jsonify, send_from_directory, send_file
import pandas as pd
import numpy as np
import os
import json
import webbrowser
import threading

from src.insight_engine import compute_segment_statistics, generate_key_insights, generate_suggestions, analyze_and_generate


# ============================================================================
# APP SETUP
# ============================================================================

app = Flask(__name__, static_folder='frontend', static_url_path='')

CLEANED_DATA_PATH = os.path.join("outputs", "cleaned_data.csv")
CHARTS_DIR = os.path.join("outputs", "charts")

# Load cleaned data ONCE at startup (100K rows, ~17MB)
print("Loading cleaned dataset...")
DF = pd.read_csv(CLEANED_DATA_PATH, parse_dates=['Date'])
print(f"  [OK] Loaded {len(DF):,} rows x {DF.shape[1]} columns")

# Pre-compute overall statistics once
print("Computing overall statistics...")
OVERALL_STATS = compute_segment_statistics(DF)
OVERALL_INSIGHTS = generate_key_insights(OVERALL_STATS)
OVERALL_SUGGESTIONS = generate_suggestions(OVERALL_STATS)
print("  [OK] Overall statistics computed")


# ============================================================================
# HELPER: Apply filters to dataframe
# ============================================================================

def apply_filters(df, filters):
    """
    Apply user-selected filters to the DataFrame.
    
    Parameters:
        df (pd.DataFrame): The full dataset
        filters (dict): Filter selections from frontend
    
    Returns:
        pd.DataFrame: Filtered subset
    """
    filtered = df
    
    # Categorical filters
    filter_map = {
        'bank': 'Bank',
        'card_type': 'Type of Card',
        'entry_mode': 'Entry Mode',
        'txn_type': 'Type of Transaction',
        'merchant_group': 'Merchant Group',
        'country': 'Country of Transaction',
        'gender': 'Gender',
        'age_group': 'Age_Group',
        'fraud_status': 'Fraud_Status',
    }
    
    for filter_key, column_name in filter_map.items():
        value = filters.get(filter_key, 'All')
        if value and value != 'All' and value != '':
            if isinstance(value, list):
                filtered = filtered[filtered[column_name].isin(value)]
            else:
                filtered = filtered[filtered[column_name] == value]
    
    # Date range filter
    date_from = filters.get('date_from', '')
    date_to = filters.get('date_to', '')
    
    if date_from and date_from != '':
        try:
            filtered = filtered[filtered['Date'] >= pd.to_datetime(date_from)]
        except:
            pass
    
    if date_to and date_to != '':
        try:
            filtered = filtered[filtered['Date'] <= pd.to_datetime(date_to)]
        except:
            pass
    
    return filtered


# ============================================================================
# ROUTES: Static Files
# ============================================================================

@app.route('/')
def serve_index():
    return send_from_directory('frontend', 'index.html')

@app.route('/charts/<path:filename>')
def serve_chart(filename):
    return send_from_directory(CHARTS_DIR, filename)

@app.route('/outputs/charts/<path:filename>')
def serve_output_chart(filename):
    return send_from_directory(CHARTS_DIR, filename)


# ============================================================================
# API: Filter Options
# ============================================================================

@app.route('/api/filter-options', methods=['GET'])
def get_filter_options():
    """Return unique/distinct values for each filter dropdown."""
    options = {
        'banks': sorted(DF['Bank'].unique().tolist()),
        'card_types': sorted(DF['Type of Card'].unique().tolist()),
        'entry_modes': sorted(DF['Entry Mode'].unique().tolist()),
        'txn_types': sorted(DF['Type of Transaction'].unique().tolist()),
        'merchant_groups': sorted(DF['Merchant Group'].unique().tolist()),
        'countries': sorted(DF['Country of Transaction'].unique().tolist()),
        'genders': [{'value': 'M', 'label': 'Male'}, {'value': 'F', 'label': 'Female'}],
        'age_groups': ['Under 18', '18-25', '26-35', '36-45', '46-55', '56-65', '65+'],
        'fraud_statuses': sorted(DF['Fraud_Status'].unique().tolist()),
        'date_min': str(DF['Date'].min().date()),
        'date_max': str(DF['Date'].max().date()),
    }
    return jsonify(options)


# ============================================================================
# API: Overall Statistics
# ============================================================================

@app.route('/api/overall-stats', methods=['GET'])
def get_overall_stats():
    """Return pre-computed overall dataset statistics."""
    return jsonify({
        'statistics': OVERALL_STATS,
        'insights': OVERALL_INSIGHTS,
        'suggestions': OVERALL_SUGGESTIONS
    })


# ============================================================================
# API: Custom Analysis (with filters)
# ============================================================================

@app.route('/api/analyze', methods=['POST'])
def analyze():
    """
    Accept filters from frontend, apply them, compute statistics,
    generate insights and suggestions, then return everything.
    """
    filters = request.get_json() or {}
    
    # Apply filters to the dataset
    filtered_df = apply_filters(DF, filters)
    
    # No results check
    if len(filtered_df) == 0:
        return jsonify({
            'statistics': None,
            'insights': ["No transactions found for the selected criteria."],
            'suggestions': ["Try adjusting your filters to include more transactions."],
            'chart_data': None,
            'num_results': 0
        })
    
    # Run analysis with overall comparison
    result = analyze_and_generate(filtered_df, DF)
    
    # Build chart data for dynamic frontend charts
    chart_data = build_chart_data(filtered_df)
    
    result['chart_data'] = chart_data
    result['num_results'] = len(filtered_df)
    
    return jsonify(result)


# ============================================================================
# HELPER: Build Chart Data for Frontend
# ============================================================================

def build_chart_data(df):
    """
    Build JSON-serializable chart data for the frontend to render.
    """
    charts = {}
    
    # 1. Transaction amount distribution (histogram buckets)
    amounts = df['Amount'].dropna()
    if len(amounts) > 0:
        hist, bin_edges = np.histogram(amounts, bins=20)
        charts['amount_distribution'] = {
            'labels': [f"£{bin_edges[i]:,.0f}-{bin_edges[i+1]:,.0f}" for i in range(len(hist))],
            'values': hist.tolist()
        }
    
    # 2. Day of week distribution
    if 'Day of Week' in df.columns:
        day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        day_counts = df['Day of Week'].value_counts().reindex(day_order).fillna(0)
        charts['day_of_week'] = {
            'labels': day_counts.index.tolist(),
            'values': day_counts.values.astype(int).tolist()
        }
    
    # 3. Hourly distribution
    if 'Hour' in df.columns:
        hour_counts = df['Hour'].value_counts().sort_index()
        # Ensure all 24 hours are represented
        full_hours = pd.Series(0, index=range(24))
        full_hours.update(hour_counts)
        charts['hourly'] = {
            'labels': [f"{h}:00" for h in range(24)],
            'values': full_hours.values.astype(int).tolist()
        }
    
    # 4. Time period distribution
    if 'Time_Period' in df.columns:
        period_order = ['Morning', 'Afternoon', 'Evening', 'Night']
        period_counts = df['Time_Period'].value_counts().reindex(period_order).fillna(0)
        charts['time_period'] = {
            'labels': period_counts.index.tolist(),
            'values': period_counts.values.astype(int).tolist()
        }
    
    # 5. Card type distribution
    if 'Type of Card' in df.columns:
        card_counts = df['Type of Card'].value_counts()
        charts['card_type'] = {
            'labels': card_counts.index.tolist(),
            'values': card_counts.values.astype(int).tolist()
        }
    
    # 6. Merchant group distribution
    if 'Merchant Group' in df.columns:
        merchant_counts = df['Merchant Group'].value_counts()
        charts['merchant'] = {
            'labels': merchant_counts.index.tolist(),
            'values': merchant_counts.values.astype(int).tolist()
        }
    
    # 7. Transaction type distribution
    if 'Type of Transaction' in df.columns:
        txn_counts = df['Type of Transaction'].value_counts()
        charts['txn_type'] = {
            'labels': txn_counts.index.tolist(),
            'values': txn_counts.values.astype(int).tolist()
        }
    
    # 8. Transaction trend (by date)
    if 'Date' in df.columns and len(df) > 0:
        date_counts = df.groupby(df['Date'].dt.strftime('%Y-%m-%d')).size()
        date_counts = date_counts.sort_index()
        charts['trend'] = {
            'labels': date_counts.index.tolist(),
            'values': date_counts.values.astype(int).tolist()
        }
    
    return charts


# ============================================================================
# CHECK: Ensure Power BI data has derived fields (Requirement #11)
# ============================================================================

def ensure_powerbi_derived_fields():
    """
    Check and ensure the Power BI export has all required derived fields.
    Only adds fields if they aren't already present.
    """
    powerbi_path = os.path.join("outputs", "powerbi_data", "Bank_Transactions_PowerBI.csv")
    if not os.path.exists(powerbi_path):
        return
    
    pbi_df = pd.read_csv(powerbi_path, parse_dates=['Date'])
    changed = False
    
    required_fields = {
        'Year': lambda df: df['Date'].dt.year,
        'Month': lambda df: df['Date'].dt.month,
        'Month_Name': lambda df: df['Date'].dt.strftime('%B'),
        'Hour': lambda df: df['Time'],
        'Time_Period': lambda df: df['Hour'].apply(
            lambda h: 'Morning' if 5 <= h < 12 else ('Afternoon' if 12 <= h < 17 else ('Evening' if 17 <= h < 21 else 'Night'))
        ),
        'Age_Group': None,  # Complex, skip if missing (should exist)
        'Is_Weekend': lambda df: df['Day of Week'].isin(['Saturday', 'Sunday']).map({True: 'Weekend', False: 'Weekday'}),
        'Fraud_Status': lambda df: df['Fraud'].map({0: 'No Fraud', 1: 'Fraud'}),
    }
    
    for field_name, create_fn in required_fields.items():
        if field_name not in pbi_df.columns and create_fn is not None:
            try:
                pbi_df[field_name] = create_fn(pbi_df)
                changed = True
                print(f"  [PowerBI] Added derived field: {field_name}")
            except Exception as e:
                print(f"  [PowerBI] Could not add {field_name}: {e}")
    
    if changed:
        pbi_df.to_csv(powerbi_path, index=False)
        print("  [PowerBI] Updated export with new derived fields")


# ============================================================================
# MAIN / SERVER LAUNCHER
# ============================================================================

def start_server(host='0.0.0.0', port=5000, open_browser_auto=True):
    """
    Ensure derived fields are created, launch Flask API server,
    and automatically open the dashboard in the default browser.
    """
    ensure_powerbi_derived_fields()
    
    url = f"http://localhost:{port}"
    print("\n" + "=" * 60)
    print("  SERVER READY")
    print(f"  Dashboard available at: {url}")
    print("=" * 60 + "\n")
    
    if open_browser_auto and os.environ.get("WERKZEUG_RUN_MAIN") != "true":
        print(f"  [Auto-Open] Opening {url} in your default browser...\n")
        threading.Timer(1.2, lambda: webbrowser.open(url)).start()
        
    try:
        app.run(host=host, port=port, debug=False)
    except OSError as e:
        print(f"\n  [INFO] Server already running or port {port} is active.")
        print(f"  [Auto-Open] Opening existing dashboard at {url}...\n")
        webbrowser.open(url)


if __name__ == '__main__':
    start_server(open_browser_auto=True)
