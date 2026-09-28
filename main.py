"""
=============================================================================
 main.py -- Bank Transaction Analysis Project Runner
=============================================================================
 This is the main entry point for the project.
 
 It runs the complete pipeline:
   1. Data Cleaning & Preprocessing
   2. Descriptive Statistical Analysis
   3. Exploratory Data Analysis (Visualization)
   4. Power BI Data Export
   5. Auto-Launch Interactive Web Dashboard
 
 Usage:
   python main.py
=============================================================================
"""

from src.data_cleaning import main as run_cleaning
from src.analysis import main as run_analysis
from src.visualization import main as run_visualization
from src.export_powerbi import main as run_powerbi
from server import start_server


def main():
    """Run the complete Bank Transaction Analysis pipeline and launch dashboard."""
    
    print()
    print("+" + "=" * 58 + "+")
    print("|" + "  BANK TRANSACTION ANALYSIS PROJECT".center(58) + "|")
    print("|" + "  Descriptive Analytics".center(58) + "|")
    print("+" + "=" * 58 + "+")
    print()
    
    # -- PHASE 1: Data Cleaning --
    print("\n" + "#" * 60)
    print("  PHASE 1: DATA CLEANING & PREPROCESSING")
    print("#" * 60 + "\n")
    cleaned_df = run_cleaning()
    
    # -- PHASE 2: Statistical Analysis --
    print("\n" + "#" * 60)
    print("  PHASE 2: DESCRIPTIVE STATISTICAL ANALYSIS")
    print("#" * 60 + "\n")
    df, results = run_analysis()
    
    # -- PHASE 3: Visualization --
    print("\n" + "#" * 60)
    print("  PHASE 3: EXPLORATORY DATA ANALYSIS (VISUALIZATION)")
    print("#" * 60 + "\n")
    run_visualization()
    
    # -- PHASE 4: Power BI Export --
    print("\n" + "#" * 60)
    print("  PHASE 4: POWER BI DATA PREPARATION")
    print("#" * 60 + "\n")
    run_powerbi()
    
    # -- Done Processing --
    print("\n")
    print("+" + "=" * 58 + "+")
    print("|" + "  ALL DATA PROCESSING PHASES COMPLETE [OK]".center(58) + "|")
    print("|" + "".center(58) + "|")
    print("|" + "  Outputs:".center(58) + "|")
    print("|" + "  - outputs/cleaned_data.csv".center(58) + "|")
    print("|" + "  - outputs/charts/*.png".center(58) + "|")
    print("|" + "  - outputs/powerbi_data/*.csv".center(58) + "|")
    print("+" + "=" * 58 + "+")
    
    # -- PHASE 5: Launch Web Server & Auto-Open Browser --
    print("\n" + "#" * 60)
    print("  PHASE 5: LAUNCHING INTERACTIVE WEB DASHBOARD")
    print("#" * 60 + "\n")
    
    start_server(open_browser_auto=True)


if __name__ == "__main__":
    main()

