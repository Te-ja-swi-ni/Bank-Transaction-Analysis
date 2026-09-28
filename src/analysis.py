"""
=============================================================================
 analysis.py -- Descriptive Statistical Analysis Module
 Bank Transaction Analysis Project
=============================================================================
 This module performs all descriptive statistical analyses:
   1. Transaction Analysis (count, total, mean, median, std, min, max)
   2. Time Analysis (day of week, hourly, time period)
   3. Card Analysis (card type, entry mode)
   4. Transaction Type Analysis
   5. Merchant Group Analysis
   6. Bank Analysis
   7. Geographical Analysis
   8. Customer Activity Analysis (age group, gender)
   9. Fraud Analysis (descriptive only, no prediction)
=============================================================================
"""

import pandas as pd
import numpy as np
import os


# ============================================================================
# CONFIGURATION
# ============================================================================

CLEANED_DATA_PATH = os.path.join("outputs", "cleaned_data.csv")


# ============================================================================
# LOAD CLEANED DATA
# ============================================================================

def load_cleaned_data(filepath=CLEANED_DATA_PATH):
    """Load the cleaned dataset."""
    df = pd.read_csv(filepath, parse_dates=['Date'])
    print(f"Loaded cleaned data: {df.shape[0]:,} rows x {df.shape[1]} columns\n")
    return df


# ============================================================================
# 1. TRANSACTION ANALYSIS
# ============================================================================

def transaction_analysis(df):
    """
    Overall transaction statistics.
    Answers: How many transactions? Total amount? Average? Median? Std Dev?
    """
    print("=" * 60)
    print("1. TRANSACTION ANALYSIS")
    print("=" * 60)
    
    stats = {
        'Total Transactions': len(df),
        'Total Amount (GBP)': df['Amount'].sum(),
        'Average Amount (GBP)': round(df['Amount'].mean(), 2),
        'Median Amount (GBP)': df['Amount'].median(),
        'Min Amount (GBP)': df['Amount'].min(),
        'Max Amount (GBP)': df['Amount'].max(),
        'Std Deviation (GBP)': round(df['Amount'].std(), 2),
    }
    
    for key, value in stats.items():
        print(f"  {key}: {value:,.2f}" if isinstance(value, float) else f"  {key}: {value:,}")
    
    print()
    return stats


# ============================================================================
# 2. TIME ANALYSIS
# ============================================================================

def time_analysis(df):
    """
    Time-based transaction analysis.
    Answers: Which day/hour/time-period has the most transactions?
    """
    print("=" * 60)
    print("2. TIME ANALYSIS")
    print("=" * 60)
    
    # Day of Week analysis
    print("\n  Transactions by Day of Week:")
    day_counts = df['Day of Week'].value_counts()
    for day, count in day_counts.items():
        print(f"    {day}: {count:,}")
    
    # Hourly analysis
    print("\n  Top 5 Busiest Hours:")
    hour_counts = df['Hour'].value_counts().head(5)
    for hour, count in hour_counts.items():
        print(f"    {hour}:00 -- {count:,} transactions")
    
    # Time Period analysis
    print("\n  Transactions by Time Period:")
    period_counts = df['Time_Period'].value_counts()
    for period, count in period_counts.items():
        pct = (count / len(df)) * 100
        print(f"    {period}: {count:,} ({pct:.1f}%)")
    
    # Date-wise analysis
    print("\n  Transactions by Date:")
    date_counts = df['Date'].dt.strftime('%d-%b-%Y').value_counts()
    for date, count in date_counts.items():
        print(f"    {date}: {count:,}")
    
    print()
    return {
        'day_counts': day_counts,
        'hour_counts': df['Hour'].value_counts().sort_index(),
        'period_counts': period_counts,
        'date_counts': date_counts
    }


# ============================================================================
# 3. CARD ANALYSIS
# ============================================================================

def card_analysis(df):
    """
    Card type and entry mode analysis.
    Answers: Which card type is most used? Which entry mode is most common?
    """
    print("=" * 60)
    print("3. CARD ANALYSIS")
    print("=" * 60)
    
    # Card type frequency
    print("\n  Transactions by Card Type:")
    card_counts = df['Type of Card'].value_counts()
    for card, count in card_counts.items():
        pct = (count / len(df)) * 100
        print(f"    {card}: {count:,} ({pct:.1f}%)")
    
    # Card type total amount
    print("\n  Total Amount by Card Type:")
    card_total = df.groupby('Type of Card')['Amount'].sum()
    for card, total in card_total.items():
        print(f"    {card}: GBP {total:,.0f}")
    
    # Card type average amount
    print("\n  Average Amount by Card Type:")
    card_avg = df.groupby('Type of Card')['Amount'].mean()
    for card, avg in card_avg.items():
        print(f"    {card}: GBP {avg:,.2f}")
    
    # Entry mode frequency
    print("\n  Transactions by Entry Mode:")
    entry_counts = df['Entry Mode'].value_counts()
    for mode, count in entry_counts.items():
        pct = (count / len(df)) * 100
        print(f"    {mode}: {count:,} ({pct:.1f}%)")
    
    print()
    return {
        'card_counts': card_counts,
        'card_total': card_total,
        'card_avg': card_avg,
        'entry_counts': entry_counts
    }


# ============================================================================
# 4. TRANSACTION TYPE ANALYSIS
# ============================================================================

def transaction_type_analysis(df):
    """
    Analysis by transaction type (Online, ATM, POS).
    """
    print("=" * 60)
    print("4. TRANSACTION TYPE ANALYSIS")
    print("=" * 60)
    
    # Frequency
    print("\n  Transaction Type Frequency:")
    type_counts = df['Type of Transaction'].value_counts()
    for t, count in type_counts.items():
        pct = (count / len(df)) * 100
        print(f"    {t}: {count:,} ({pct:.1f}%)")
    
    # Total amount
    print("\n  Total Amount by Transaction Type:")
    type_total = df.groupby('Type of Transaction')['Amount'].sum()
    for t, total in type_total.items():
        print(f"    {t}: GBP {total:,.0f}")
    
    # Average amount
    print("\n  Average Amount by Transaction Type:")
    type_avg = df.groupby('Type of Transaction')['Amount'].mean()
    for t, avg in type_avg.items():
        print(f"    {t}: GBP {avg:,.2f}")
    
    print()
    return {
        'type_counts': type_counts,
        'type_total': type_total,
        'type_avg': type_avg
    }


# ============================================================================
# 5. MERCHANT GROUP ANALYSIS
# ============================================================================

def merchant_analysis(df):
    """
    Analysis by merchant group.
    """
    print("=" * 60)
    print("5. MERCHANT GROUP ANALYSIS")
    print("=" * 60)
    
    # Frequency
    print("\n  Transactions by Merchant Group:")
    merchant_counts = df['Merchant Group'].value_counts()
    for m, count in merchant_counts.items():
        print(f"    {m}: {count:,}")
    
    # Total amount
    print("\n  Total Amount by Merchant Group:")
    merchant_total = df.groupby('Merchant Group')['Amount'].sum().sort_values(ascending=False)
    for m, total in merchant_total.items():
        print(f"    {m}: GBP {total:,.0f}")
    
    # Average amount
    print("\n  Average Amount by Merchant Group:")
    merchant_avg = df.groupby('Merchant Group')['Amount'].mean().sort_values(ascending=False)
    for m, avg in merchant_avg.items():
        print(f"    {m}: GBP {avg:,.2f}")
    
    print()
    return {
        'merchant_counts': merchant_counts,
        'merchant_total': merchant_total,
        'merchant_avg': merchant_avg
    }


# ============================================================================
# 6. BANK ANALYSIS
# ============================================================================

def bank_analysis(df):
    """
    Analysis by bank.
    """
    print("=" * 60)
    print("6. BANK ANALYSIS")
    print("=" * 60)
    
    # Frequency
    print("\n  Transactions by Bank:")
    bank_counts = df['Bank'].value_counts()
    for b, count in bank_counts.items():
        print(f"    {b}: {count:,}")
    
    # Total amount
    print("\n  Total Amount by Bank:")
    bank_total = df.groupby('Bank')['Amount'].sum().sort_values(ascending=False)
    for b, total in bank_total.items():
        print(f"    {b}: GBP {total:,.0f}")
    
    # Average amount
    print("\n  Average Amount by Bank:")
    bank_avg = df.groupby('Bank')['Amount'].mean().sort_values(ascending=False)
    for b, avg in bank_avg.items():
        print(f"    {b}: GBP {avg:,.2f}")
    
    print()
    return {
        'bank_counts': bank_counts,
        'bank_total': bank_total,
        'bank_avg': bank_avg
    }


# ============================================================================
# 7. GEOGRAPHICAL ANALYSIS
# ============================================================================

def geographical_analysis(df):
    """
    Country-wise transaction analysis.
    """
    print("=" * 60)
    print("7. GEOGRAPHICAL ANALYSIS")
    print("=" * 60)
    
    # Transaction volume by country
    print("\n  Transactions by Country:")
    country_counts = df['Country of Transaction'].value_counts()
    for c, count in country_counts.items():
        pct = (count / len(df)) * 100
        print(f"    {c}: {count:,} ({pct:.1f}%)")
    
    # Total amount by country
    print("\n  Total Amount by Country:")
    country_total = df.groupby('Country of Transaction')['Amount'].sum().sort_values(ascending=False)
    for c, total in country_total.items():
        print(f"    {c}: GBP {total:,.0f}")
    
    # Average amount by country
    print("\n  Average Amount by Country:")
    country_avg = df.groupby('Country of Transaction')['Amount'].mean().sort_values(ascending=False)
    for c, avg in country_avg.items():
        print(f"    {c}: GBP {avg:,.2f}")
    
    # International vs Domestic
    print("\n  Domestic vs International:")
    intl_counts = df['Is_International'].value_counts()
    for t, count in intl_counts.items():
        pct = (count / len(df)) * 100
        print(f"    {t}: {count:,} ({pct:.1f}%)")
    
    print()
    return {
        'country_counts': country_counts,
        'country_total': country_total,
        'country_avg': country_avg,
        'intl_counts': intl_counts
    }


# ============================================================================
# 8. CUSTOMER ACTIVITY ANALYSIS
# ============================================================================

def customer_analysis(df):
    """
    Analysis by age group and gender.
    """
    print("=" * 60)
    print("8. CUSTOMER ACTIVITY ANALYSIS")
    print("=" * 60)
    
    # Age group frequency
    print("\n  Transactions by Age Group:")
    age_counts = df['Age_Group'].value_counts().sort_index()
    for grp, count in age_counts.items():
        pct = (count / len(df)) * 100
        print(f"    {grp}: {count:,} ({pct:.1f}%)")
    
    # Age group average amount
    print("\n  Average Amount by Age Group:")
    age_avg = df.groupby('Age_Group', observed=True)['Amount'].mean()
    for grp, avg in age_avg.items():
        print(f"    {grp}: GBP {avg:,.2f}")
    
    # Gender frequency
    print("\n  Transactions by Gender:")
    gender_counts = df['Gender'].value_counts()
    for g, count in gender_counts.items():
        pct = (count / len(df)) * 100
        label = 'Male' if g == 'M' else 'Female'
        print(f"    {label} ({g}): {count:,} ({pct:.1f}%)")
    
    # Gender average amount
    print("\n  Average Amount by Gender:")
    gender_avg = df.groupby('Gender')['Amount'].mean()
    for g, avg in gender_avg.items():
        label = 'Male' if g == 'M' else 'Female'
        print(f"    {label}: GBP {avg:,.2f}")
    
    print()
    return {
        'age_counts': age_counts,
        'age_avg': age_avg,
        'gender_counts': gender_counts,
        'gender_avg': gender_avg
    }


# ============================================================================
# 9. FRAUD ANALYSIS (DESCRIPTIVE ONLY)
# ============================================================================

def fraud_analysis(df):
    """
    Descriptive fraud analysis.
    NOTE: This is NOT a fraud prediction model -- only descriptive statistics.
    """
    print("=" * 60)
    print("9. FRAUD ANALYSIS (Descriptive)")
    print("=" * 60)
    
    # Overall fraud stats
    total = len(df)
    fraud_count = df['Fraud'].sum()
    non_fraud_count = total - fraud_count
    fraud_pct = (fraud_count / total) * 100
    
    print(f"\n  Fraud vs Non-Fraud:")
    print(f"    Non-Fraud: {non_fraud_count:,} ({100 - fraud_pct:.2f}%)")
    print(f"    Fraud:     {fraud_count:,} ({fraud_pct:.2f}%)")
    
    # Average amount: fraud vs non-fraud
    fraud_df = df[df['Fraud'] == 1]
    non_fraud_df = df[df['Fraud'] == 0]
    
    print(f"\n  Average Transaction Amount:")
    print(f"    Non-Fraud: GBP {non_fraud_df['Amount'].mean():.2f}")
    print(f"    Fraud:     GBP {fraud_df['Amount'].mean():.2f}")
    
    # Fraud by transaction type
    print(f"\n  Fraud by Transaction Type:")
    fraud_by_type = fraud_df['Type of Transaction'].value_counts()
    for t, count in fraud_by_type.items():
        type_total = df[df['Type of Transaction'] == t].shape[0]
        pct = (count / type_total) * 100
        print(f"    {t}: {count:,} frauds ({pct:.2f}% of {t} transactions)")
    
    # Fraud by merchant group
    print(f"\n  Fraud by Merchant Group:")
    fraud_by_merchant = fraud_df['Merchant Group'].value_counts()
    for m, count in fraud_by_merchant.items():
        print(f"    {m}: {count:,}")
    
    # Fraud by country
    print(f"\n  Fraud by Country:")
    fraud_by_country = fraud_df['Country of Transaction'].value_counts()
    for c, count in fraud_by_country.items():
        country_total = df[df['Country of Transaction'] == c].shape[0]
        pct = (count / country_total) * 100
        print(f"    {c}: {count:,} ({pct:.2f}% fraud rate)")
    
    # Fraud by card type
    print(f"\n  Fraud by Card Type:")
    fraud_by_card = fraud_df['Type of Card'].value_counts()
    for card, count in fraud_by_card.items():
        card_total = df[df['Type of Card'] == card].shape[0]
        pct = (count / card_total) * 100
        print(f"    {card}: {count:,} ({pct:.2f}% fraud rate)")
    
    print()
    return {
        'fraud_count': fraud_count,
        'non_fraud_count': non_fraud_count,
        'fraud_pct': fraud_pct,
        'fraud_by_type': fraud_by_type,
        'fraud_by_merchant': fraud_by_merchant,
        'fraud_by_country': fraud_by_country
    }


# ============================================================================
# MAIN -- Run All Analyses
# ============================================================================

def main():
    """Run the complete descriptive analysis pipeline."""
    
    print("\n" + "=" * 60)
    print("  BANK TRANSACTION ANALYSIS -- DESCRIPTIVE STATISTICS")
    print("=" * 60 + "\n")
    
    # Load cleaned data
    df = load_cleaned_data()
    
    # Run all analyses
    results = {}
    results['transaction'] = transaction_analysis(df)
    results['time'] = time_analysis(df)
    results['card'] = card_analysis(df)
    results['transaction_type'] = transaction_type_analysis(df)
    results['merchant'] = merchant_analysis(df)
    results['bank'] = bank_analysis(df)
    results['geographical'] = geographical_analysis(df)
    results['customer'] = customer_analysis(df)
    results['fraud'] = fraud_analysis(df)
    
    print("=" * 60)
    print("  ALL ANALYSES COMPLETE [OK]")
    print("=" * 60)
    
    return df, results


if __name__ == "__main__":
    df, results = main()
