"""
=============================================================================
 export_powerbi.py -- Power BI Data Preparation Module
 Bank Transaction Analysis Project
=============================================================================
 This module prepares and exports data specifically optimized for Power BI.
 It saves a unified Excel file and potentially dimension tables for Star Schema.
=============================================================================
"""

import pandas as pd
import os

# ============================================================================
# CONFIGURATION
# ============================================================================
CLEANED_DATA_PATH = os.path.join("outputs", "cleaned_data.csv")
POWERBI_DIR = os.path.join("outputs", "powerbi_data")

def main():
    print("\n" + "=" * 60)
    print("  PREPARING POWER BI DATA")
    print("=" * 60)
    
    os.makedirs(POWERBI_DIR, exist_ok=True)
    
    # Load cleaned data
    df = pd.read_csv(CLEANED_DATA_PATH, parse_dates=['Date'])
    
    # Export CSV for Power BI
    
    # Ensure derived fields required for deeper Power BI analysis (#11)
    if 'Is_Weekend' not in df.columns and 'Day of Week' in df.columns:
        df['Is_Weekend'] = df['Day of Week'].isin(['Saturday', 'Sunday']).map(
            {True: 'Weekend', False: 'Weekday'}
        )
        print("  [OK] Added derived field: Is_Weekend")
    
    csv_path = os.path.join(POWERBI_DIR, "Bank_Transactions_PowerBI.csv")
    df.to_csv(csv_path, index=False)
    
    # Let's create a Dimension Table for Date to enable time intelligence in PBI
    print("  Creating Date Dimension Table...")
    date_dim = df[['Date', 'Year', 'Month', 'Month_Name', 'Day']].drop_duplicates().sort_values('Date')
    date_dim.to_csv(os.path.join(POWERBI_DIR, "Dim_Date.csv"), index=False)
    
    print(f"\n  [OK] Power BI dataset saved: {csv_path}")
    print(f"  [OK] Dimension tables saved in: {POWERBI_DIR}/")
    print("=" * 60 + "\n")

if __name__ == "__main__":
    main()
