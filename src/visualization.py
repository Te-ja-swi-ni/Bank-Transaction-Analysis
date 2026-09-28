"""
=============================================================================
 visualization.py -- Exploratory Data Analysis (EDA) Visualization Module
 Bank Transaction Analysis Project
=============================================================================
 This module creates all charts and visualizations using:
   - Matplotlib: Line charts, bar charts, histograms, pie charts
   - Seaborn: Distribution plots, box plots, heatmaps, count plots
 
 All charts are saved to outputs/charts/ directory.
=============================================================================
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import seaborn as sns
import os


# ============================================================================
# CONFIGURATION
# ============================================================================

CLEANED_DATA_PATH = os.path.join("outputs", "cleaned_data.csv")
CHARTS_DIR = os.path.join("outputs", "charts")

# Visual style settings
sns.set_theme(style="whitegrid", palette="deep")
plt.rcParams['figure.figsize'] = (10, 6)
plt.rcParams['figure.dpi'] = 150
plt.rcParams['font.size'] = 11
plt.rcParams['axes.titlesize'] = 14
plt.rcParams['axes.labelsize'] = 12


def save_chart(fig, filename):
    """Save chart to the charts directory."""
    filepath = os.path.join(CHARTS_DIR, filename)
    fig.savefig(filepath, bbox_inches='tight', facecolor='white')
    plt.close(fig)
    print(f"  [OK] Saved: {filepath}")


# ============================================================================
# LOAD DATA
# ============================================================================

def load_cleaned_data(filepath=CLEANED_DATA_PATH):
    """Load the cleaned dataset."""
    df = pd.read_csv(filepath, parse_dates=['Date'])
    print(f"Loaded cleaned data: {df.shape[0]:,} rows x {df.shape[1]} columns\n")
    return df


# ============================================================================
# 1. TRANSACTION AMOUNT DISTRIBUTION
# ============================================================================

def plot_amount_distribution(df):
    """Histogram + KDE of transaction amounts."""
    print("  Creating: Amount Distribution...")
    
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    
    # Histogram
    axes[0].hist(df['Amount'], bins=40, color='#3498db', edgecolor='white', alpha=0.8)
    axes[0].set_title('Distribution of Transaction Amounts')
    axes[0].set_xlabel('Amount (£)')
    axes[0].set_ylabel('Frequency')
    
    # Box plot
    sns.boxplot(x=df['Amount'], ax=axes[1], color='#2ecc71')
    axes[1].set_title('Box Plot of Transaction Amounts')
    axes[1].set_xlabel('Amount (£)')
    
    fig.suptitle('Transaction Amount Analysis', fontsize=16, fontweight='bold', y=1.02)
    fig.tight_layout()
    save_chart(fig, '01_amount_distribution.png')


# ============================================================================
# 2. TRANSACTIONS BY DAY OF WEEK
# ============================================================================

def plot_day_of_week(df):
    """Bar chart of transactions by day of week."""
    print("  Creating: Day of Week Analysis...")
    
    day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    day_counts = df['Day of Week'].value_counts().reindex(day_order).dropna()
    
    fig, ax = plt.subplots(figsize=(10, 6))
    bars = ax.bar(day_counts.index, day_counts.values, color='#9b59b6', edgecolor='white')
    
    # Add value labels on bars
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{int(height):,}', ha='center', va='bottom', fontweight='bold')
    
    ax.set_title('Transactions by Day of Week', fontsize=14, fontweight='bold')
    ax.set_xlabel('Day of Week')
    ax.set_ylabel('Number of Transactions')
    ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f'{int(x):,}'))
    
    fig.tight_layout()
    save_chart(fig, '02_day_of_week.png')


# ============================================================================
# 3. HOURLY TRANSACTION PATTERN
# ============================================================================

def plot_hourly_pattern(df):
    """Line chart of transactions by hour."""
    print("  Creating: Hourly Transaction Pattern...")
    
    hour_counts = df['Hour'].value_counts().sort_index()
    
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(hour_counts.index, hour_counts.values, marker='o', linewidth=2,
            color='#e74c3c', markersize=6, markerfacecolor='white', markeredgewidth=2)
    ax.fill_between(hour_counts.index, hour_counts.values, alpha=0.15, color='#e74c3c')
    
    ax.set_title('Transaction Volume by Hour of Day', fontsize=14, fontweight='bold')
    ax.set_xlabel('Hour (24-hour format)')
    ax.set_ylabel('Number of Transactions')
    ax.set_xticks(range(0, 24))
    ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f'{int(x):,}'))
    ax.grid(True, alpha=0.3)
    
    fig.tight_layout()
    save_chart(fig, '03_hourly_pattern.png')


# ============================================================================
# 4. TRANSACTIONS BY TIME PERIOD
# ============================================================================

def plot_time_period(df):
    """Pie chart of transactions by time period."""
    print("  Creating: Time Period Distribution...")
    
    period_order = ['Morning', 'Afternoon', 'Evening', 'Night']
    period_counts = df['Time_Period'].value_counts().reindex(period_order)
    colors = ['#f39c12', '#e74c3c', '#9b59b6', '#2c3e50']
    
    fig, ax = plt.subplots(figsize=(8, 8))
    wedges, texts, autotexts = ax.pie(
        period_counts.values,
        labels=period_counts.index,
        autopct='%1.1f%%',
        colors=colors,
        startangle=90,
        explode=(0.02, 0.02, 0.02, 0.02),
        shadow=True
    )
    
    for text in autotexts:
        text.set_fontweight('bold')
        text.set_fontsize(12)
    
    ax.set_title('Transactions by Time Period', fontsize=14, fontweight='bold')
    
    fig.tight_layout()
    save_chart(fig, '04_time_period.png')


# ============================================================================
# 5. CARD TYPE ANALYSIS
# ============================================================================

def plot_card_analysis(df):
    """Card type and entry mode comparison."""
    print("  Creating: Card Type Analysis...")
    
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    
    # Card type count
    card_counts = df['Type of Card'].value_counts()
    bars1 = axes[0].bar(card_counts.index, card_counts.values,
                         color=['#3498db', '#e74c3c'], edgecolor='white')
    for bar in bars1:
        height = bar.get_height()
        axes[0].text(bar.get_x() + bar.get_width()/2., height,
                     f'{int(height):,}', ha='center', va='bottom', fontweight='bold')
    axes[0].set_title('Transaction Count by Card Type')
    axes[0].set_ylabel('Number of Transactions')
    
    # Entry mode count
    entry_counts = df['Entry Mode'].value_counts()
    bars2 = axes[1].bar(entry_counts.index, entry_counts.values,
                         color=['#2ecc71', '#f39c12', '#9b59b6'], edgecolor='white')
    for bar in bars2:
        height = bar.get_height()
        axes[1].text(bar.get_x() + bar.get_width()/2., height,
                     f'{int(height):,}', ha='center', va='bottom', fontweight='bold')
    axes[1].set_title('Transaction Count by Entry Mode')
    axes[1].set_ylabel('Number of Transactions')
    
    fig.suptitle('Card & Entry Mode Analysis', fontsize=16, fontweight='bold', y=1.02)
    fig.tight_layout()
    save_chart(fig, '05_card_analysis.png')


# ============================================================================
# 6. TRANSACTION TYPE ANALYSIS
# ============================================================================

def plot_transaction_type(df):
    """Transaction type frequency and average amount."""
    print("  Creating: Transaction Type Analysis...")
    
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    
    # Count
    type_counts = df['Type of Transaction'].value_counts()
    bars = axes[0].bar(type_counts.index, type_counts.values,
                        color=['#1abc9c', '#3498db', '#e67e22'], edgecolor='white')
    for bar in bars:
        height = bar.get_height()
        axes[0].text(bar.get_x() + bar.get_width()/2., height,
                     f'{int(height):,}', ha='center', va='bottom', fontweight='bold')
    axes[0].set_title('Transaction Count by Type')
    axes[0].set_ylabel('Number of Transactions')
    
    # Average amount
    type_avg = df.groupby('Type of Transaction')['Amount'].mean().sort_values(ascending=False)
    bars2 = axes[1].bar(type_avg.index, type_avg.values,
                         color=['#1abc9c', '#3498db', '#e67e22'], edgecolor='white')
    for bar in bars2:
        height = bar.get_height()
        axes[1].text(bar.get_x() + bar.get_width()/2., height,
                     f'£{height:,.0f}', ha='center', va='bottom', fontweight='bold')
    axes[1].set_title('Average Amount by Transaction Type')
    axes[1].set_ylabel('Average Amount (£)')
    
    fig.suptitle('Transaction Type Analysis', fontsize=16, fontweight='bold', y=1.02)
    fig.tight_layout()
    save_chart(fig, '06_transaction_type.png')


# ============================================================================
# 7. MERCHANT GROUP ANALYSIS
# ============================================================================

def plot_merchant_analysis(df):
    """Merchant group horizontal bar and average amount."""
    print("  Creating: Merchant Group Analysis...")
    
    fig, axes = plt.subplots(1, 2, figsize=(14, 7))
    
    # Transaction count by merchant
    merchant_counts = df['Merchant Group'].value_counts().sort_values()
    colors = sns.color_palette('viridis', len(merchant_counts))
    axes[0].barh(merchant_counts.index, merchant_counts.values, color=colors, edgecolor='white')
    axes[0].set_title('Transaction Count by Merchant Group')
    axes[0].set_xlabel('Number of Transactions')
    
    # Average amount by merchant
    merchant_avg = df.groupby('Merchant Group')['Amount'].mean().sort_values()
    axes[1].barh(merchant_avg.index, merchant_avg.values, color=colors, edgecolor='white')
    axes[1].set_title('Average Amount by Merchant Group')
    axes[1].set_xlabel('Average Amount (£)')
    
    fig.suptitle('Merchant Group Analysis', fontsize=16, fontweight='bold', y=1.02)
    fig.tight_layout()
    save_chart(fig, '07_merchant_analysis.png')


# ============================================================================
# 8. BANK ANALYSIS
# ============================================================================

def plot_bank_analysis(df):
    """Bank-wise transaction analysis."""
    print("  Creating: Bank Analysis...")
    
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    
    # Count by bank
    bank_counts = df['Bank'].value_counts()
    colors = sns.color_palette('Set2', len(bank_counts))
    bars = axes[0].bar(bank_counts.index, bank_counts.values, color=colors, edgecolor='white')
    for bar in bars:
        height = bar.get_height()
        axes[0].text(bar.get_x() + bar.get_width()/2., height,
                     f'{int(height):,}', ha='center', va='bottom', fontsize=8, fontweight='bold')
    axes[0].set_title('Transaction Count by Bank')
    axes[0].set_ylabel('Number of Transactions')
    axes[0].tick_params(axis='x', rotation=45)
    
    # Average amount by bank
    bank_avg = df.groupby('Bank')['Amount'].mean().sort_values(ascending=False)
    bars2 = axes[1].bar(bank_avg.index, bank_avg.values, color=colors, edgecolor='white')
    for bar in bars2:
        height = bar.get_height()
        axes[1].text(bar.get_x() + bar.get_width()/2., height,
                     f'£{height:,.0f}', ha='center', va='bottom', fontsize=8, fontweight='bold')
    axes[1].set_title('Average Amount by Bank')
    axes[1].set_ylabel('Average Amount (£)')
    axes[1].tick_params(axis='x', rotation=45)
    
    fig.suptitle('Bank Analysis', fontsize=16, fontweight='bold', y=1.02)
    fig.tight_layout()
    save_chart(fig, '08_bank_analysis.png')


# ============================================================================
# 9. GEOGRAPHICAL ANALYSIS
# ============================================================================

def plot_geographical_analysis(df):
    """Country-wise transaction analysis."""
    print("  Creating: Geographical Analysis...")
    
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    
    # Transaction count by country
    country_counts = df['Country of Transaction'].value_counts()
    colors = ['#2ecc71', '#3498db', '#e74c3c', '#f39c12', '#9b59b6']
    bars = axes[0].bar(country_counts.index, country_counts.values, color=colors, edgecolor='white')
    for bar in bars:
        height = bar.get_height()
        axes[0].text(bar.get_x() + bar.get_width()/2., height,
                     f'{int(height):,}', ha='center', va='bottom', fontsize=9, fontweight='bold')
    axes[0].set_title('Transaction Count by Country')
    axes[0].set_ylabel('Number of Transactions')
    axes[0].tick_params(axis='x', rotation=30)
    
    # Domestic vs International
    intl_counts = df['Is_International'].value_counts()
    axes[1].pie(intl_counts.values, labels=intl_counts.index,
                autopct='%1.1f%%', colors=['#2ecc71', '#e74c3c'],
                startangle=90, shadow=True,
                textprops={'fontweight': 'bold'})
    axes[1].set_title('Domestic vs International Transactions')
    
    fig.suptitle('Geographical Analysis', fontsize=16, fontweight='bold', y=1.02)
    fig.tight_layout()
    save_chart(fig, '09_geographical_analysis.png')


# ============================================================================
# 10. CUSTOMER ANALYSIS (AGE + GENDER)
# ============================================================================

def plot_customer_analysis(df):
    """Age group and gender analysis."""
    print("  Creating: Customer Analysis...")
    
    fig, axes = plt.subplots(2, 2, figsize=(18, 16))
    fig.subplots_adjust(hspace=0.35, wspace=0.30)
    
    # Age group bar chart
    age_order = ['Under 18', '18-25', '26-35', '36-45', '46-55', '56-65', '65+']
    age_counts = df['Age_Group'].value_counts().reindex(age_order)
    colors_age = sns.color_palette('coolwarm', len(age_order))
    bars = axes[0, 0].bar(age_counts.index, age_counts.values, color=colors_age, edgecolor='white')
    for bar in bars:
        height = bar.get_height()
        axes[0, 0].text(bar.get_x() + bar.get_width()/2., height,
                        f'{int(height):,}', ha='center', va='bottom', fontsize=10, fontweight='bold')
    axes[0, 0].set_title('Transactions by Age Group', fontsize=14, fontweight='bold')
    axes[0, 0].set_ylabel('Count')
    axes[0, 0].tick_params(axis='x', rotation=30)
    
    # Average amount by age group
    age_avg = df.groupby('Age_Group', observed=True)['Amount'].mean().reindex(age_order)
    bars2 = axes[0, 1].bar(age_avg.index, age_avg.values, color=colors_age, edgecolor='white')
    for bar in bars2:
        height = bar.get_height()
        axes[0, 1].text(bar.get_x() + bar.get_width()/2., height,
                        f'£{height:,.0f}', ha='center', va='bottom', fontsize=10, fontweight='bold')
    axes[0, 1].set_title('Average Amount by Age Group', fontsize=14, fontweight='bold')
    axes[0, 1].set_ylabel('Average Amount (£)')
    axes[0, 1].tick_params(axis='x', rotation=30)
    
    # Gender count
    gender_counts = df['Gender'].value_counts()
    axes[1, 0].pie(gender_counts.values,
                    labels=['Male', 'Female'],
                    autopct='%1.1f%%',
                    colors=['#3498db', '#e74c3c'],
                    startangle=90, shadow=True,
                    textprops={'fontweight': 'bold', 'fontsize': 13})
    axes[1, 0].set_title('Transactions by Gender', fontsize=14, fontweight='bold', pad=15)
    
    # Age distribution by gender
    sns.histplot(data=df, x='Age', hue='Gender', kde=True, ax=axes[1, 1],
                 palette={'M': '#3498db', 'F': '#e74c3c'}, alpha=0.5, bins=30)
    axes[1, 1].set_title('Age Distribution by Gender', fontsize=14, fontweight='bold')
    axes[1, 1].set_xlabel('Age')
    axes[1, 1].set_ylabel('Frequency')
    
    fig.suptitle('Customer Activity Analysis', fontsize=18, fontweight='bold', y=1.01)
    fig.tight_layout(rect=[0, 0, 1, 0.97])
    save_chart(fig, '10_customer_analysis.png')


# ============================================================================
# 11. FRAUD ANALYSIS
# ============================================================================

def plot_fraud_analysis(df):
    """Descriptive fraud visualizations."""
    print("  Creating: Fraud Analysis...")
    
    fig, axes = plt.subplots(2, 2, figsize=(18, 16))
    fig.subplots_adjust(hspace=0.35, wspace=0.30)
    
    # Fraud vs Non-Fraud pie
    fraud_counts = df['Fraud_Status'].value_counts()
    axes[0, 0].pie(fraud_counts.values,
                    labels=fraud_counts.index,
                    autopct='%1.1f%%',
                    colors=['#2ecc71', '#e74c3c'],
                    startangle=90, shadow=True, explode=(0, 0.05),
                    textprops={'fontweight': 'bold', 'fontsize': 13})
    axes[0, 0].set_title('Fraud vs Non-Fraud', fontsize=14, fontweight='bold', pad=15)
    
    # Fraud by transaction type
    fraud_type = df[df['Fraud'] == 1]['Type of Transaction'].value_counts()
    bars = axes[0, 1].bar(fraud_type.index, fraud_type.values,
                           color=['#e74c3c', '#f39c12', '#9b59b6'], edgecolor='white')
    for bar in bars:
        height = bar.get_height()
        axes[0, 1].text(bar.get_x() + bar.get_width()/2., height,
                        f'{int(height):,}', ha='center', va='bottom', fontsize=11, fontweight='bold')
    axes[0, 1].set_title('Fraud Count by Transaction Type', fontsize=14, fontweight='bold')
    axes[0, 1].set_ylabel('Fraud Count')
    
    # Fraud by merchant group
    fraud_merchant = df[df['Fraud'] == 1]['Merchant Group'].value_counts().sort_values()
    colors_m = sns.color_palette('Reds_r', len(fraud_merchant))
    axes[1, 0].barh(fraud_merchant.index, fraud_merchant.values, color=colors_m, edgecolor='white')
    axes[1, 0].set_title('Fraud Count by Merchant Group', fontsize=14, fontweight='bold')
    axes[1, 0].set_xlabel('Fraud Count')
    
    # Fraud rate by country
    fraud_rate_country = df.groupby('Country of Transaction')['Fraud'].mean() * 100
    fraud_rate_country = fraud_rate_country.sort_values(ascending=False)
    bars2 = axes[1, 1].bar(fraud_rate_country.index, fraud_rate_country.values,
                            color='#e74c3c', edgecolor='white', alpha=0.8)
    for bar in bars2:
        height = bar.get_height()
        axes[1, 1].text(bar.get_x() + bar.get_width()/2., height,
                        f'{height:.1f}%', ha='center', va='bottom', fontsize=11, fontweight='bold')
    axes[1, 1].set_title('Fraud Rate by Country', fontsize=14, fontweight='bold')
    axes[1, 1].set_ylabel('Fraud Rate (%)')
    axes[1, 1].tick_params(axis='x', rotation=30)
    
    fig.suptitle('Fraud Analysis (Descriptive)', fontsize=18, fontweight='bold', y=1.01)
    fig.tight_layout(rect=[0, 0, 1, 0.97])
    save_chart(fig, '11_fraud_analysis.png')


# ============================================================================
# 12. CORRELATION HEATMAP
# ============================================================================

def plot_heatmap(df):
    """Heatmap of correlations between numeric columns."""
    print("  Creating: Correlation Heatmap...")
    
    numeric_cols = df[['Amount', 'Time', 'Age', 'Fraud']].copy()
    corr_matrix = numeric_cols.corr()
    
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.heatmap(corr_matrix, annot=True, cmap='RdYlBu_r', center=0,
                linewidths=1, fmt='.3f', ax=ax,
                square=True, cbar_kws={'shrink': 0.8})
    ax.set_title('Correlation Heatmap (Numeric Variables)', fontsize=14, fontweight='bold')
    
    fig.tight_layout()
    save_chart(fig, '12_correlation_heatmap.png')


# ============================================================================
# 13. AMOUNT BY CARD TYPE (BOX PLOT)
# ============================================================================

def plot_amount_by_card_boxplot(df):
    """Box plot of Amount by Card Type and Transaction Type."""
    print("  Creating: Amount Box Plots...")
    
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    
    # By card type
    sns.boxplot(data=df, x='Type of Card', y='Amount', ax=axes[0],
                palette=['#3498db', '#e74c3c'], hue='Type of Card', legend=False)
    axes[0].set_title('Amount Distribution by Card Type')
    axes[0].set_ylabel('Amount (£)')
    
    # By transaction type
    sns.boxplot(data=df, x='Type of Transaction', y='Amount', ax=axes[1],
                palette=['#1abc9c', '#3498db', '#e67e22'], hue='Type of Transaction', legend=False)
    axes[1].set_title('Amount Distribution by Transaction Type')
    axes[1].set_ylabel('Amount (£)')
    
    fig.suptitle('Amount Distribution Comparisons', fontsize=16, fontweight='bold', y=1.02)
    fig.tight_layout()
    save_chart(fig, '13_amount_boxplots.png')


# ============================================================================
# MAIN -- Generate All Visualizations
# ============================================================================

def main():
    """Generate all EDA visualizations."""
    
    print("=" * 60)
    print("  GENERATING ALL VISUALIZATIONS")
    print("=" * 60)
    print()
    
    # Create charts directory if not exists
    os.makedirs(CHARTS_DIR, exist_ok=True)
    
    # Load data
    df = load_cleaned_data()
    
    # Generate all charts
    plot_amount_distribution(df)
    plot_day_of_week(df)
    plot_hourly_pattern(df)
    plot_time_period(df)
    plot_card_analysis(df)
    plot_transaction_type(df)
    plot_merchant_analysis(df)
    plot_bank_analysis(df)
    plot_geographical_analysis(df)
    plot_customer_analysis(df)
    plot_fraud_analysis(df)
    plot_heatmap(df)
    plot_amount_by_card_boxplot(df)
    
    print()
    print("=" * 60)
    print(f"  ALL {13} CHARTS GENERATED SUCCESSFULLY [OK]")
    print(f"  Saved to: {CHARTS_DIR}/")
    print("=" * 60)


if __name__ == "__main__":
    main()
