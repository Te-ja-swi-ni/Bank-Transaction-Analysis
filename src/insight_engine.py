"""
=============================================================================
 insight_engine.py -- Insight & Suggestion Generation Engine
 Bank Transaction Analysis Project
=============================================================================
 This module takes calculated statistics from a filtered (or full) dataset
 and generates:
   1. Key Insights   -- human-readable observations about the data
   2. Data-Driven Suggestions -- analytical highlights based on patterns
   3. Supporting statistics

 Architecture:
   analyze_selection(filters)
        → calculated statistics
        → insight_engine
        → insights + suggestions
        → frontend

 IMPORTANT: This is a DESCRIPTIVE ANALYTICS module.
 NO predictions, NO ML, NO forecasting.
=============================================================================
"""

import pandas as pd
import numpy as np


# ============================================================================
# CORE STATISTICS CALCULATOR
# ============================================================================

def compute_segment_statistics(df, overall_df=None):
    """
    Compute comprehensive descriptive statistics for a given DataFrame segment.
    
    Parameters:
        df (pd.DataFrame): The filtered/segment DataFrame
        overall_df (pd.DataFrame): The full dataset for comparison (optional)
    
    Returns:
        dict: Comprehensive statistics dictionary
    """
    if df is None or len(df) == 0:
        return None
    
    stats = {}
    
    # --- Basic Transaction Stats ---
    stats['num_transactions'] = int(len(df))
    stats['total_amount'] = round(float(df['Amount'].sum()), 2)
    stats['avg_amount'] = round(float(df['Amount'].mean()), 2)
    stats['median_amount'] = round(float(df['Amount'].median()), 2)
    stats['min_amount'] = round(float(df['Amount'].min()), 2)
    stats['max_amount'] = round(float(df['Amount'].max()), 2)
    stats['std_amount'] = round(float(df['Amount'].std()), 2) if len(df) > 1 else 0.0
    stats['variance_amount'] = round(float(df['Amount'].var()), 2) if len(df) > 1 else 0.0
    
    # Quartiles & Percentiles
    stats['q1_amount'] = round(float(df['Amount'].quantile(0.25)), 2)
    stats['q3_amount'] = round(float(df['Amount'].quantile(0.75)), 2)
    stats['iqr_amount'] = round(stats['q3_amount'] - stats['q1_amount'], 2)
    stats['p10_amount'] = round(float(df['Amount'].quantile(0.10)), 2)
    stats['p90_amount'] = round(float(df['Amount'].quantile(0.90)), 2)
    
    # Outlier boundaries (IQR method)
    lower_bound = stats['q1_amount'] - 1.5 * stats['iqr_amount']
    upper_bound = stats['q3_amount'] + 1.5 * stats['iqr_amount']
    outliers = df[(df['Amount'] < lower_bound) | (df['Amount'] > upper_bound)]
    stats['outlier_count'] = int(len(outliers))
    stats['outlier_pct'] = round((len(outliers) / len(df)) * 100, 2) if len(df) > 0 else 0.0
    
    # Mode (most common transaction amount)
    mode_val = df['Amount'].mode()
    stats['mode_amount'] = round(float(mode_val.iloc[0]), 2) if len(mode_val) > 0 else None
    
    # --- Time-Based Stats ---
    if 'Day of Week' in df.columns:
        day_counts = df['Day of Week'].value_counts()
        stats['most_active_day'] = str(day_counts.index[0])
        stats['most_active_day_count'] = int(day_counts.iloc[0])
        stats['day_distribution'] = {str(k): int(v) for k, v in day_counts.items()}
    
    if 'Hour' in df.columns:
        hour_counts = df['Hour'].value_counts()
        stats['peak_hour'] = int(hour_counts.index[0])
        stats['peak_hour_count'] = int(hour_counts.iloc[0])
        stats['hour_distribution'] = {int(k): int(v) for k, v in hour_counts.sort_index().items()}
    
    if 'Time_Period' in df.columns:
        period_counts = df['Time_Period'].value_counts()
        stats['peak_time_period'] = str(period_counts.index[0])
        stats['peak_time_period_count'] = int(period_counts.iloc[0])
        stats['peak_time_period_pct'] = round((period_counts.iloc[0] / len(df)) * 100, 1)
        stats['time_period_distribution'] = {str(k): int(v) for k, v in period_counts.items()}
    
    # --- Card Stats ---
    if 'Type of Card' in df.columns:
        card_counts = df['Type of Card'].value_counts()
        stats['most_used_card'] = str(card_counts.index[0])
        stats['most_used_card_count'] = int(card_counts.iloc[0])
        stats['most_used_card_pct'] = round((card_counts.iloc[0] / len(df)) * 100, 1)
        stats['card_distribution'] = {str(k): int(v) for k, v in card_counts.items()}
    
    # --- Entry Mode Stats ---
    if 'Entry Mode' in df.columns:
        entry_counts = df['Entry Mode'].value_counts()
        stats['most_common_entry_mode'] = str(entry_counts.index[0])
        stats['most_common_entry_mode_count'] = int(entry_counts.iloc[0])
        stats['most_common_entry_mode_pct'] = round((entry_counts.iloc[0] / len(df)) * 100, 1)
        stats['entry_mode_distribution'] = {str(k): int(v) for k, v in entry_counts.items()}
    
    # --- Transaction Type Stats ---
    if 'Type of Transaction' in df.columns:
        txn_counts = df['Type of Transaction'].value_counts()
        stats['most_common_txn_type'] = str(txn_counts.index[0])
        stats['most_common_txn_type_count'] = int(txn_counts.iloc[0])
        stats['most_common_txn_type_pct'] = round((txn_counts.iloc[0] / len(df)) * 100, 1)
        stats['txn_type_distribution'] = {str(k): int(v) for k, v in txn_counts.items()}
    
    # --- Merchant Stats ---
    if 'Merchant Group' in df.columns:
        merchant_counts = df['Merchant Group'].value_counts()
        stats['top_merchant'] = str(merchant_counts.index[0])
        stats['top_merchant_count'] = int(merchant_counts.iloc[0])
        stats['top_merchant_pct'] = round((merchant_counts.iloc[0] / len(df)) * 100, 1)
        stats['merchant_distribution'] = {str(k): int(v) for k, v in merchant_counts.items()}
        
        # Merchant amount analysis
        merchant_amount = df.groupby('Merchant Group')['Amount'].sum().sort_values(ascending=False)
        stats['top_merchant_by_amount'] = str(merchant_amount.index[0])
        stats['top_merchant_amount'] = round(float(merchant_amount.iloc[0]), 2)
        stats['top_merchant_amount_pct'] = round((merchant_amount.iloc[0] / stats['total_amount']) * 100, 1)
    
    # --- Country Stats ---
    if 'Country of Transaction' in df.columns:
        country_counts = df['Country of Transaction'].value_counts()
        stats['top_country'] = str(country_counts.index[0])
        stats['top_country_count'] = int(country_counts.iloc[0])
        stats['top_country_pct'] = round((country_counts.iloc[0] / len(df)) * 100, 1)
        stats['country_distribution'] = {str(k): int(v) for k, v in country_counts.items()}
    
    # --- Bank Stats ---
    if 'Bank' in df.columns:
        bank_counts = df['Bank'].value_counts()
        stats['top_bank'] = str(bank_counts.index[0])
        stats['top_bank_count'] = int(bank_counts.iloc[0])
        stats['bank_distribution'] = {str(k): int(v) for k, v in bank_counts.items()}
    
    # --- Gender Stats ---
    if 'Gender' in df.columns:
        gender_counts = df['Gender'].value_counts()
        stats['gender_distribution'] = {str(k): int(v) for k, v in gender_counts.items()}
        stats['dominant_gender'] = 'Male' if gender_counts.get('M', 0) > gender_counts.get('F', 0) else 'Female'
    
    # --- Age Stats ---
    if 'Age_Group' in df.columns:
        age_counts = df['Age_Group'].value_counts()
        stats['top_age_group'] = str(age_counts.index[0])
        stats['age_distribution'] = {str(k): int(v) for k, v in age_counts.items()}
    
    if 'Age' in df.columns:
        stats['avg_age'] = round(float(df['Age'].mean()), 1)
        stats['median_age'] = round(float(df['Age'].median()), 1)
    
    # --- Fraud Stats ---
    if 'Fraud' in df.columns:
        fraud_count = int(df['Fraud'].sum())
        stats['fraud_count'] = fraud_count
        stats['fraud_pct'] = round((fraud_count / len(df)) * 100, 2) if len(df) > 0 else 0.0
    
    # --- Overall comparison stats (if available) ---
    if overall_df is not None and len(overall_df) > 0:
        stats['overall_avg_amount'] = round(float(overall_df['Amount'].mean()), 2)
        stats['overall_median_amount'] = round(float(overall_df['Amount'].median()), 2)
        stats['overall_total'] = int(len(overall_df))
        stats['segment_pct_of_total'] = round((len(df) / len(overall_df)) * 100, 2)
        if 'Fraud' in overall_df.columns:
            stats['overall_fraud_pct'] = round((overall_df['Fraud'].sum() / len(overall_df)) * 100, 2)
        
        # Comparison ratios
        stats['avg_amount_vs_overall'] = round(stats['avg_amount'] / stats['overall_avg_amount'], 2) if stats['overall_avg_amount'] > 0 else 1.0
    
    return stats


# ============================================================================
# KEY INSIGHTS GENERATOR
# ============================================================================

def generate_key_insights(stats):
    """
    Generate human-readable key insights based on computed statistics.
    
    Parameters:
        stats (dict): The statistics dictionary from compute_segment_statistics
    
    Returns:
        list: List of insight strings
    """
    if stats is None:
        return ["No data available for the selected criteria."]
    
    insights = []
    
    # 1. Most active day
    if 'most_active_day' in stats:
        insights.append(
            f"{stats['most_active_day']} has the highest transaction frequency "
            f"with {stats['most_active_day_count']:,} transactions in the selected segment."
        )
    
    # 2. Average vs overall comparison
    if 'avg_amount_vs_overall' in stats:
        ratio = stats['avg_amount_vs_overall']
        if ratio > 1.15:
            pct_higher = round((ratio - 1) * 100, 1)
            insights.append(
                f"The selected segment has an average transaction amount (£{stats['avg_amount']:,.2f}) "
                f"that is {pct_higher}% higher than the overall dataset average (£{stats['overall_avg_amount']:,.2f})."
            )
        elif ratio < 0.85:
            pct_lower = round((1 - ratio) * 100, 1)
            insights.append(
                f"The selected segment has an average transaction amount (£{stats['avg_amount']:,.2f}) "
                f"that is {pct_lower}% lower than the overall dataset average (£{stats['overall_avg_amount']:,.2f})."
            )
        else:
            insights.append(
                f"The average transaction amount (£{stats['avg_amount']:,.2f}) is in line with "
                f"the overall dataset average (£{stats['overall_avg_amount']:,.2f})."
            )
    
    # 3. Peak time period
    if 'peak_time_period' in stats:
        insights.append(
            f"{stats['peak_time_period']} is the most active transaction period, "
            f"accounting for {stats['peak_time_period_pct']}% of transactions."
        )
    
    # 4. Top merchant
    if 'top_merchant' in stats:
        insights.append(
            f"{stats['top_merchant']} is the dominant merchant group, "
            f"representing {stats['top_merchant_pct']}% of transactions in the selected segment."
        )
    
    # 5. Card type
    if 'most_used_card' in stats:
        insights.append(
            f"{stats['most_used_card']} is the most frequently used card type "
            f"({stats['most_used_card_pct']}% of transactions)."
        )
    
    # 6. Peak hour
    if 'peak_hour' in stats:
        hour_label = f"{stats['peak_hour']}:00"
        insights.append(
            f"Peak transaction activity occurs at {hour_label} "
            f"with {stats['peak_hour_count']:,} transactions."
        )
    
    # 7. Fraud percentage
    if 'fraud_pct' in stats:
        if stats['fraud_pct'] > 0:
            insights.append(
                f"The fraud rate in the selected segment is {stats['fraud_pct']}%"
                f" ({stats['fraud_count']:,} flagged transactions)."
            )
        else:
            insights.append("No fraudulent transactions were found in the selected segment.")
    
    # 8. Transaction type
    if 'most_common_txn_type' in stats:
        insights.append(
            f"{stats['most_common_txn_type']} is the most common transaction type "
            f"({stats['most_common_txn_type_pct']}%)."
        )
    
    # 9. Entry mode
    if 'most_common_entry_mode' in stats:
        insights.append(
            f"{stats['most_common_entry_mode']} is the most common entry mode "
            f"({stats['most_common_entry_mode_pct']}% of transactions)."
        )
    
    # 10. Outlier info
    if 'outlier_count' in stats and stats['outlier_count'] > 0:
        insights.append(
            f"There are {stats['outlier_count']:,} outlier transactions ({stats['outlier_pct']}%) "
            f"based on the IQR method (amounts outside £{stats['q1_amount'] - 1.5 * stats['iqr_amount']:,.2f} – "
            f"£{stats['q3_amount'] + 1.5 * stats['iqr_amount']:,.2f})."
        )
    
    # 11. Amount spread
    if stats.get('std_amount', 0) > 0:
        cv = round(stats['std_amount'] / stats['avg_amount'] * 100, 1) if stats['avg_amount'] > 0 else 0
        if cv > 100:
            insights.append(
                f"Transaction amounts show very high variability (CV: {cv}%), "
                f"indicating a wide spread from £{stats['min_amount']:,.2f} to £{stats['max_amount']:,.2f}."
            )
    
    return insights


# ============================================================================
# DATA-DRIVEN SUGGESTIONS GENERATOR
# ============================================================================

def generate_suggestions(stats):
    """
    Generate data-driven suggestions based on observed patterns.
    
    IMPORTANT: These are descriptive observations, NOT predictions.
    
    Parameters:
        stats (dict): The statistics dictionary from compute_segment_statistics
    
    Returns:
        list: List of suggestion strings
    """
    if stats is None:
        return ["No data available to generate suggestions."]
    
    suggestions = []
    
    # 1. Time concentration check
    if 'time_period_distribution' in stats and 'peak_time_period' in stats:
        if stats['peak_time_period_pct'] > 35:
            suggestions.append(
                f"Transaction activity is concentrated in the {stats['peak_time_period']} period "
                f"({stats['peak_time_period_pct']}%). This indicates a strong time-based usage pattern "
                f"in the selected segment."
            )
    
    # 2. Merchant group dominance
    if 'top_merchant_amount_pct' in stats:
        if stats['top_merchant_amount_pct'] > 25:
            suggestions.append(
                f"{stats['top_merchant_by_amount']} contributes {stats['top_merchant_amount_pct']}% "
                f"of the total transaction value (£{stats['top_merchant_amount']:,.2f}). "
                f"This merchant group has a disproportionate share of transaction volume."
            )
    
    # 3. Average amount vs overall
    if 'avg_amount_vs_overall' in stats:
        ratio = stats['avg_amount_vs_overall']
        if ratio > 1.3:
            suggestions.append(
                f"The selected segment has a significantly higher average transaction "
                f"(£{stats['avg_amount']:,.2f} vs overall £{stats['overall_avg_amount']:,.2f}). "
                f"This segment tends toward higher-value transactions."
            )
        elif ratio < 0.7:
            suggestions.append(
                f"The selected segment has a notably lower average transaction "
                f"(£{stats['avg_amount']:,.2f} vs overall £{stats['overall_avg_amount']:,.2f}). "
                f"This segment is characterized by smaller, more frequent transactions."
            )
    
    # 4. Day with unusually high activity
    if 'day_distribution' in stats:
        day_vals = list(stats['day_distribution'].values())
        if len(day_vals) > 1:
            avg_day_count = sum(day_vals) / len(day_vals)
            max_day_count = max(day_vals)
            if max_day_count > avg_day_count * 1.2:
                suggestions.append(
                    f"{stats['most_active_day']} has notably higher activity than the average day "
                    f"({stats['most_active_day_count']:,} vs avg {avg_day_count:,.0f}). "
                    f"This day may represent a recurring behavioural pattern."
                )
    
    # 5. Transaction type dominance
    if 'most_common_txn_type_pct' in stats:
        if stats['most_common_txn_type_pct'] > 50:
            suggestions.append(
                f"{stats['most_common_txn_type']} transactions dominate this segment "
                f"at {stats['most_common_txn_type_pct']}%. "
                f"The segment shows a strong preference for this transaction method."
            )
    
    # 6. Fraud rate comparison
    if 'fraud_pct' in stats and 'overall_fraud_pct' in stats:
        diff = stats['fraud_pct'] - stats['overall_fraud_pct']
        if diff > 3:
            suggestions.append(
                f"The fraud rate in this segment ({stats['fraud_pct']}%) is notably higher "
                f"than the overall dataset ({stats['overall_fraud_pct']}%). "
                f"This segment shows an elevated fraud incidence that warrants attention."
            )
        elif diff < -3:
            suggestions.append(
                f"The fraud rate in this segment ({stats['fraud_pct']}%) is notably lower "
                f"than the overall dataset ({stats['overall_fraud_pct']}%). "
                f"This segment exhibits a comparatively lower fraud risk profile."
            )
    
    # 7. Segment size context
    if 'segment_pct_of_total' in stats:
        pct = stats['segment_pct_of_total']
        if pct < 1:
            suggestions.append(
                f"This segment represents only {pct}% of the total dataset "
                f"({stats['num_transactions']:,} out of {stats['overall_total']:,} transactions). "
                f"Insights derived from this small segment should be interpreted with caution."
            )
        elif pct > 50:
            suggestions.append(
                f"This segment represents {pct}% of the total dataset. "
                f"It captures the majority of transaction activity and its patterns "
                f"closely reflect overall trends."
            )
    
    # 8. High variability warning
    if stats.get('std_amount', 0) > 0 and stats.get('avg_amount', 0) > 0:
        cv = stats['std_amount'] / stats['avg_amount']
        if cv > 2:
            suggestions.append(
                f"Transaction amounts in this segment exhibit extremely high variability "
                f"(standard deviation £{stats['std_amount']:,.2f} vs mean £{stats['avg_amount']:,.2f}). "
                f"The median (£{stats['median_amount']:,.2f}) may be a more representative "
                f"measure of typical transaction size."
            )
    
    # 9. Country concentration
    if 'top_country_pct' in stats:
        if stats['top_country_pct'] > 80:
            suggestions.append(
                f"{stats['top_country']} accounts for {stats['top_country_pct']}% of transactions "
                f"in this segment, indicating a highly domestic transaction profile."
            )
    
    # 10. Outlier significance
    if 'outlier_pct' in stats and stats['outlier_pct'] > 10:
        suggestions.append(
            f"{stats['outlier_pct']}% of transactions in this segment are outliers by amount. "
            f"These high- or low-value transactions may significantly skew aggregate metrics "
            f"like the mean."
        )
    
    if not suggestions:
        suggestions.append(
            "The selected segment's patterns are largely consistent with the overall dataset. "
            "No significant deviations were observed."
        )
    
    return suggestions


# ============================================================================
# MAIN ORCHESTRATOR
# ============================================================================

def analyze_and_generate(df, overall_df=None):
    """
    Main orchestrator that computes statistics, generates insights and suggestions.
    
    Parameters:
        df (pd.DataFrame): Filtered segment
        overall_df (pd.DataFrame): Full dataset for comparison
    
    Returns:
        dict: {
            'statistics': {...},
            'insights': [...],
            'suggestions': [...]
        }
    """
    stats = compute_segment_statistics(df, overall_df)
    
    if stats is None:
        return {
            'statistics': None,
            'insights': ["No transactions found for the selected criteria."],
            'suggestions': ["Try adjusting your filters to include more transactions."]
        }
    
    insights = generate_key_insights(stats)
    suggestions = generate_suggestions(stats)
    
    return {
        'statistics': stats,
        'insights': insights,
        'suggestions': suggestions
    }
