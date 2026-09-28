# Bank Transaction Analysis

## Project Overview
A descriptive analytics project that processes **100,000 historical bank/card transaction records** using Python and presents insights through an interactive Power BI dashboard.

## Technologies Used
| Technology | Purpose |
|------------|---------|
| **Python** | Core programming language |
| **Pandas** | Data loading, cleaning, transformation, aggregation |
| **NumPy** | Numerical/statistical calculations |
| **Matplotlib** | Line charts, bar charts, histograms, pie charts |
| **Seaborn** | Distribution plots, box plots, heatmaps |
| **Power BI** | Interactive dashboard for final presentation |

## Project Structure
```
Bank-Transaction-Analysis/
│
├── data/
│   └── CreditCardData.csv          # Raw dataset (100,000 records)
│
├── src/
│   ├── __init__.py
│   ├── data_cleaning.py             # Data cleaning & preprocessing
│   ├── analysis.py                  # Descriptive statistical analysis
│   └── visualization.py             # EDA charts (Matplotlib + Seaborn)
│
├── outputs/
│   ├── cleaned_data.csv             # Cleaned dataset (generated)
│   ├── charts/                      # All visualization charts (generated)
│   └── powerbi_data/                # Aggregated data for Power BI
│
├── main.py                          # Main project runner
├── server.py                        # Flask API server
├── requirements.txt                 # Python dependencies
└── README.md                        # This file
```

## How to Run

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Run the Complete Pipeline
```bash
python main.py
```

This will:
1. Clean and preprocess the raw data → `outputs/cleaned_data.csv`
2. Perform all descriptive statistical analyses (printed to console)
3. Generate 13 visualization charts → `outputs/charts/`

### Step 3: Run Individual Modules
```bash
# Run only data cleaning
python -m src.data_cleaning

# Run only statistical analysis
python -m src.analysis

# Run only visualizations
python -m src.visualization
```

## Dataset Summary
- **100,000** transaction records across **4 days** (Oct 13–16, 2020)
- **16 columns**: Transaction ID, Date, Day of Week, Time, Card Type, Entry Mode, Amount, Transaction Type, Merchant Group, Country, Shipping Address, Residence, Gender, Age, Bank, Fraud
- **5 countries**: United Kingdom, USA, Russia, China, India
- **7 banks**: Barclays, Monzo, RBS, Metro, Halifax, Lloyds, HSBC
- **Fraud rate**: ~7.2%

## Analysis Categories
1. Transaction Analysis (totals, averages, frequency)
2. Time Analysis (hourly, daily patterns)
3. Card Analysis (Visa vs MasterCard, entry modes)
4. Transaction Type Analysis (Online, ATM, POS)
5. Merchant Group Analysis (top categories)
6. Bank Analysis (transaction volume & value)
7. Geographical Analysis (country comparisons)
8. Customer Activity (age groups, gender)
9. Fraud Analysis (descriptive statistics only)

## Author
College Project — IBM 7th Semester
