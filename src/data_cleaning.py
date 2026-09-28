"""
=============================================================================
 data_cleaning.py -- Data Cleaning & Preprocessing Module
 Bank Transaction Analysis Project
=============================================================================
 This module handles:
   1. Loading the raw CSV dataset
   2. Inspecting data quality (shape, types, missing values, duplicates)
   3. Cleaning the Amount column (removing currency symbol)
   4. Fixing the Bank name typo (Barlcays -> Barclays)
   5. Converting Date to proper datetime format
   6. Handling missing values
   7. Fixing the Time=24 anomaly
   8. Creating derived columns (Year, Month, Age Group, Time Period, etc.)
   9. Exporting the cleaned dataset
=============================================================================
"""

import pandas as pd
import numpy as np
import os


# ============================================================================
# CONFIGURATION
# ============================================================================

# File paths
RAW_DATA_PATH = os.path.join("data", "CreditCardData.csv")
CLEANED_DATA_PATH = os.path.join("outputs", "cleaned_data.csv")


# ============================================================================
# STEP 1: LOAD THE RAW DATA
# ============================================================================

def load_data(filepath=RAW_DATA_PATH):
    """
    Load the raw CSV file into a pandas DataFrame.
    
    Parameters:
        filepath (str): Path to the CSV file
    
    Returns:
        pd.DataFrame: Raw data loaded from CSV
    """
    print("=" * 60)
    print("STEP 1: Loading Raw Data")
    print("=" * 60)
    
    df = pd.read_csv(filepath)
    print(f"  [OK] Loaded {df.shape[0]:,} rows and {df.shape[1]} columns")
    print(f"  [OK] Columns: {list(df.columns)}")
    print()
    
    return df


# ============================================================================
# STEP 2: INSPECT DATA QUALITY
# ============================================================================

def inspect_data(df):
    """
    Display a comprehensive summary of data quality.
    
    Parameters:
        df (pd.DataFrame): The DataFrame to inspect
    """
    print("=" * 60)
    print("STEP 2: Data Quality Inspection")
    print("=" * 60)
    
    # Shape
    print(f"\n  Dataset Shape: {df.shape[0]:,} rows x {df.shape[1]} columns")
    
    # Data types
    print("\n  Data Types:")
    for col in df.columns:
        print(f"    {col}: {df[col].dtype}")
    
    # Missing values
    print("\n  Missing Values:")
    total_missing = 0
    for col in df.columns:
        missing = df[col].isnull().sum()
        if missing > 0:
            pct = (missing / len(df)) * 100
            print(f"    {col}: {missing} ({pct:.2f}%)")
            total_missing += missing
    if total_missing == 0:
        print("    None found!")
    else:
        print(f"    Total missing cells: {total_missing}")
    
    # Duplicates
    print(f"\n  Duplicate Rows: {df.duplicated().sum()}")
    print(f"  Duplicate Transaction IDs: {df['Transaction ID'].duplicated().sum()}")
    
    print()


# ============================================================================
# STEP 3: CLEAN THE AMOUNT COLUMN
# ============================================================================

def clean_amount(df):
    """
    Remove the currency symbol (£) from the Amount column 
    and convert it to a numeric (float) data type.
    
    The raw data has Amount values like 'ú5', 'ú288' etc.
    The 'ú' character is a £ (pound) symbol with encoding issues.
    
    Parameters:
        df (pd.DataFrame): DataFrame with raw Amount column
    
    Returns:
        pd.DataFrame: DataFrame with cleaned numeric Amount column
    """
    print("=" * 60)
    print("STEP 3: Cleaning Amount Column")
    print("=" * 60)
    
    print(f"  Before: dtype = {df['Amount'].dtype}")
    print(f"  Sample raw values: {df['Amount'].head(5).tolist()}")
    
    # Remove all non-numeric characters (currency symbol, spaces, etc.)
    # Keep only digits and decimal point
    df['Amount'] = df['Amount'].astype(str).str.replace(r'[^\d.]', '', regex=True)
    
    # Convert to numeric
    df['Amount'] = pd.to_numeric(df['Amount'], errors='coerce')
    
    print(f"  After:  dtype = {df['Amount'].dtype}")
    print(f"  Sample cleaned values: {df['Amount'].head(5).tolist()}")
    print(f"  Range: {df['Amount'].min()} to {df['Amount'].max()}")
    print(f"  NaN after conversion: {df['Amount'].isnull().sum()}")
    print()
    
    return df


# ============================================================================
# STEP 4: FIX BANK NAME TYPO
# ============================================================================

def fix_bank_typo(df):
    """
    Fix the typo 'Barlcays' -> 'Barclays' in the Bank column.
    
    The raw data has 'Barlcays' (letters 'l' and 'c' swapped) 
    for approximately 9,993 records.
    
    Parameters:
        df (pd.DataFrame): DataFrame with raw Bank column
    
    Returns:
        pd.DataFrame: DataFrame with corrected Bank column
    """
    print("=" * 60)
    print("STEP 4: Fixing Bank Name Typo")
    print("=" * 60)
    
    # Count before fix
    print(f"  Before fix:")
    print(f"    'Barclays' count: {(df['Bank'] == 'Barclays').sum():,}")
    print(f"    'Barlcays' count: {(df['Bank'] == 'Barlcays').sum():,}")
    
    # Fix the typo
    df['Bank'] = df['Bank'].replace('Barlcays', 'Barclays')
    
    # Count after fix
    print(f"  After fix:")
    print(f"    'Barclays' count: {(df['Bank'] == 'Barclays').sum():,}")
    print(f"    Unique banks: {df['Bank'].nunique()} -> {sorted(df['Bank'].unique().tolist())}")
    print()
    
    return df


# ============================================================================
# STEP 5: CONVERT DATE TO DATETIME
# ============================================================================

def convert_date(df):
    """
    Convert the Date column from string format ('14-Oct-20') 
    to proper pandas datetime format.
    
    Parameters:
        df (pd.DataFrame): DataFrame with string Date column
    
    Returns:
        pd.DataFrame: DataFrame with datetime Date column
    """
    print("=" * 60)
    print("STEP 5: Converting Date to Datetime")
    print("=" * 60)
    
    print(f"  Before: dtype = {df['Date'].dtype}")
    print(f"  Sample: {df['Date'].head(3).tolist()}")
    
    # Convert string date to datetime
    # Format: '14-Oct-20' → day-month(abbr)-year(2digit)
    df['Date'] = pd.to_datetime(df['Date'], format='%d-%b-%y')
    
    print(f"  After:  dtype = {df['Date'].dtype}")
    print(f"  Sample: {df['Date'].head(3).tolist()}")
    print(f"  Date range: {df['Date'].min()} to {df['Date'].max()}")
    print()
    
    return df


# ============================================================================
# STEP 6: FIX TIME COLUMN ANOMALY
# ============================================================================

def fix_time_column(df):
    """
    Fix the Time=24 anomaly. In a 24-hour clock, valid hours are 0-23.
    Time=24 is treated as midnight (0).
    
    Parameters:
        df (pd.DataFrame): DataFrame with Time column
    
    Returns:
        pd.DataFrame: DataFrame with corrected Time column
    """
    print("=" * 60)
    print("STEP 6: Fixing Time Column (Time=24 -> 0)")
    print("=" * 60)
    
    count_24 = (df['Time'] == 24).sum()
    print(f"  Rows with Time=24: {count_24:,}")
    
    # Replace 24 with 0 (midnight)
    df['Time'] = df['Time'].replace(24, 0)
    
    print(f"  After fix -> Time range: {df['Time'].min()} to {df['Time'].max()}")
    print()
    
    return df


# ============================================================================
# STEP 7: HANDLE MISSING VALUES
# ============================================================================

def handle_missing_values(df):
    """
    Handle missing values in the dataset.
    
    Strategy:
    - Amount (6 missing): Fill with median amount 
      (median is preferred over mean because Amount is right-skewed)
    - Merchant Group (10 missing): Fill with 'Unknown'
      (we can't guess the merchant, so we label it honestly)
    - Shipping Address (5 missing): Fill with Country of Transaction
      (reasonable assumption: most shipping matches transaction country)
    - Gender (4 missing): Fill with mode (most frequent gender)
      (only 4 rows, impact is negligible)
    
    Parameters:
        df (pd.DataFrame): DataFrame with missing values
    
    Returns:
        pd.DataFrame: DataFrame with missing values handled
    """
    print("=" * 60)
    print("STEP 7: Handling Missing Values")
    print("=" * 60)
    
    # Check missing before
    print("  Missing values BEFORE handling:")
    for col in df.columns:
        missing = df[col].isnull().sum()
        if missing > 0:
            print(f"    {col}: {missing}")
    
    # Fill Amount with median
    median_amount = df['Amount'].median()
    df['Amount'] = df['Amount'].fillna(median_amount)
    print(f"\n  [OK] Amount: filled missing with median = {median_amount}")
    
    # Fill Merchant Group with 'Unknown'
    df['Merchant Group'] = df['Merchant Group'].fillna('Unknown')
    print(f"  [OK] Merchant Group: filled missing with 'Unknown'")
    
    # Fill Shipping Address with Country of Transaction
    df['Shipping Address'] = df['Shipping Address'].fillna(df['Country of Transaction'])
    print(f"  [OK] Shipping Address: filled missing with Country of Transaction")
    
    # Fill Gender with mode
    gender_mode = df['Gender'].mode()[0]
    df['Gender'] = df['Gender'].fillna(gender_mode)
    print(f"  [OK] Gender: filled missing with mode = '{gender_mode}'")
    
    # Verify no missing values remain
    total_missing = df.isnull().sum().sum()
    print(f"\n  Missing values AFTER handling: {total_missing}")
    print()
    
    return df


# ============================================================================
# STEP 8: CREATE DERIVED COLUMNS
# ============================================================================

def create_derived_columns(df):
    """
    Create useful derived columns for analysis:
    
    - Year: Extracted from Date
    - Month: Month number from Date
    - Month_Name: Month name (e.g., 'October')
    - Day: Day of month from Date
    - Hour: Renamed from Time for clarity
    - Time_Period: Morning/Afternoon/Evening/Night
    - Age_Group: Categorical age groups
    - Fraud_Status: Human-readable fraud label
    - Is_International: Whether transaction country differs from residence
    
    Parameters:
        df (pd.DataFrame): Cleaned DataFrame
    
    Returns:
        pd.DataFrame: DataFrame with new derived columns
    """
    print("=" * 60)
    print("STEP 8: Creating Derived Columns")
    print("=" * 60)
    
    # --- Date-based columns ---
    df['Year'] = df['Date'].dt.year
    print(f"  [OK] Year: {df['Year'].unique()}")
    
    df['Month'] = df['Date'].dt.month
    print(f"  [OK] Month: {df['Month'].unique()}")
    
    df['Month_Name'] = df['Date'].dt.strftime('%B')
    print(f"  [OK] Month_Name: {df['Month_Name'].unique()}")
    
    df['Day'] = df['Date'].dt.day
    print(f"  [OK] Day: {sorted(df['Day'].unique())}")
    
    # --- Time-based columns ---
    # Create Hour as a copy of Time (for clarity in naming)
    df['Hour'] = df['Time']
    
    # Time Period based on hour
    def get_time_period(hour):
        """Classify hour into time period."""
        if 5 <= hour < 12:
            return 'Morning'
        elif 12 <= hour < 17:
            return 'Afternoon'
        elif 17 <= hour < 21:
            return 'Evening'
        else:
            return 'Night'
    
    df['Time_Period'] = df['Hour'].apply(get_time_period)
    print(f"  [OK] Time_Period: {df['Time_Period'].value_counts().to_dict()}")
    
    # --- Age Group ---
    # Define meaningful age bins
    bins = [0, 18, 25, 35, 45, 55, 65, 100]
    labels = ['Under 18', '18-25', '26-35', '36-45', '46-55', '56-65', '65+']
    df['Age_Group'] = pd.cut(df['Age'], bins=bins, labels=labels, right=True)
    print(f"  [OK] Age_Group: {df['Age_Group'].value_counts().sort_index().to_dict()}")
    
    # --- Fraud Status ---
    df['Fraud_Status'] = df['Fraud'].map({0: 'No Fraud', 1: 'Fraud'})
    print(f"  [OK] Fraud_Status: {df['Fraud_Status'].value_counts().to_dict()}")
    
    # --- International Transaction Flag ---
    df['Is_International'] = np.where(
        df['Country of Transaction'] != df['Country of Residence'],
        'International',
        'Domestic'
    )
    print(f"  [OK] Is_International: {df['Is_International'].value_counts().to_dict()}")
    
    print(f"\n  Total columns after adding derived columns: {df.shape[1]}")
    print()
    
    return df


# ============================================================================
# STEP 9: EXPORT CLEANED DATA
# ============================================================================

def export_cleaned_data(df, filepath=CLEANED_DATA_PATH):
    """
    Export the cleaned DataFrame to a CSV file.
    
    Parameters:
        df (pd.DataFrame): Cleaned DataFrame
        filepath (str): Output file path
    """
    print("=" * 60)
    print("STEP 9: Exporting Cleaned Data")
    print("=" * 60)
    
    df.to_csv(filepath, index=False)
    
    # File size
    file_size = os.path.getsize(filepath) / (1024 * 1024)
    
    print(f"  [OK] Saved to: {filepath}")
    print(f"  [OK] File size: {file_size:.2f} MB")
    print(f"  [OK] Shape: {df.shape[0]:,} rows x {df.shape[1]} columns")
    print(f"  [OK] Columns: {list(df.columns)}")
    print()


# ============================================================================
# STEP 10: FINAL SUMMARY
# ============================================================================

def print_final_summary(df):
    """
    Print a final summary of the cleaned dataset.
    
    Parameters:
        df (pd.DataFrame): Cleaned DataFrame
    """
    print("=" * 60)
    print("FINAL SUMMARY -- Cleaned Dataset")
    print("=" * 60)
    
    print(f"\n  Total Rows: {df.shape[0]:,}")
    print(f"  Total Columns: {df.shape[1]}")
    print(f"  Missing Values: {df.isnull().sum().sum()}")
    print(f"  Duplicate Rows: {df.duplicated().sum()}")
    
    print(f"\n  Column Data Types:")
    for col in df.columns:
        print(f"    {col}: {df[col].dtype}")
    
    print(f"\n  Amount Statistics:")
    print(f"    Min:    GBP {df['Amount'].min():.0f}")
    print(f"    Max:    GBP {df['Amount'].max():.0f}")
    print(f"    Mean:   GBP {df['Amount'].mean():.2f}")
    print(f"    Median: GBP {df['Amount'].median():.0f}")
    
    print(f"\n  Date Range: {df['Date'].min().strftime('%d-%b-%Y')} to {df['Date'].max().strftime('%d-%b-%Y')}")
    print(f"  Banks: {sorted(df['Bank'].unique().tolist())}")
    print(f"  Card Types: {sorted(df['Type of Card'].unique().tolist())}")
    print(f"  Fraud Rate: {(df['Fraud'].mean() * 100):.2f}%")
    
    print("\n" + "=" * 60)
    print("DATA CLEANING COMPLETE [OK]")
    print("=" * 60)


# ============================================================================
# MAIN FUNCTION — Run All Cleaning Steps
# ============================================================================

def main():
    """
    Execute the complete data cleaning pipeline.
    
    Steps:
    1. Load raw data
    2. Inspect data quality
    3. Clean Amount column (remove currency symbol)
    4. Fix Bank name typo (Barlcays -> Barclays)
    5. Convert Date to datetime
    6. Fix Time=24 anomaly
    7. Handle missing values
    8. Create derived columns
    9. Export cleaned data
    10. Print final summary
    """
    # Step 1: Load data
    df = load_data()
    
    # Step 2: Inspect data quality
    inspect_data(df)
    
    # Step 3: Clean Amount column
    df = clean_amount(df)
    
    # Step 4: Fix Bank name typo
    df = fix_bank_typo(df)
    
    # Step 5: Convert Date to datetime
    df = convert_date(df)
    
    # Step 6: Fix Time=24
    df = fix_time_column(df)
    
    # Step 7: Handle missing values
    df = handle_missing_values(df)
    
    # Step 8: Create derived columns
    df = create_derived_columns(df)
    
    # Step 9: Export cleaned data
    export_cleaned_data(df)
    
    # Step 10: Final summary
    print_final_summary(df)
    
    return df


# Run the cleaning pipeline when this file is executed directly
if __name__ == "__main__":
    cleaned_df = main()
