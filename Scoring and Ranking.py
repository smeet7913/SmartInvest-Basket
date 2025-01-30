import pandas as pd
import numpy as np

# Scoring functions (unchanged)
def score_revenue_growth(value):
    """Score revenue growth based on predefined thresholds."""
    if pd.isna(value) or value == '-':
        return 0
    elif value > 20:
        return 10
    elif value > 10:
        return 8
    elif value > 5:
        return 6
    elif value > 1:
        return 4
    else:
        return 2

def score_eps_growth(value):
    """Score EPS growth based on predefined thresholds."""
    if pd.isna(value) or value == '-':
        return 0
    elif value > 25:
        return 10
    elif value > 15:
        return 8
    elif value > 5:
        return 6
    elif value > 0:
        return 4
    else:
        return 1

def score_rsi(value):
    """Score RSI based on predefined thresholds."""
    if pd.isna(value) or value == '-':
        return 0
    elif 30 <= value <= 50:
        return 10
    elif 50 < value <= 70:
        return 8
    else:
        return 4

def score_analyst_target_price(current_price, analyst_target_price):
    """Score analyst target price based on potential upside."""
    if pd.isna(current_price) or pd.isna(analyst_target_price) or current_price == '-' or analyst_target_price == '-':
        return 0
    potential_upside = (analyst_target_price - current_price) / current_price * 100
    if potential_upside > 30:
        return 10
    elif potential_upside > 20:
        return 8
    elif potential_upside > 10:
        return 6
    elif potential_upside > 0:
        return 4
    else:
        return 2

def score_beta(value):
    """Score Beta based on predefined thresholds."""
    if pd.isna(value) or value == '-':
        return 0
    elif 0.8 <= value <= 1.2:
        return 10
    elif 0.5 <= value < 0.8:
        return 8
    elif 1.2 < value <= 1.5:
        return 6
    else:
        return 4

def score_profit_margin(value):
    """Score profit margin based on predefined thresholds."""
    if pd.isna(value) or value == '-':
        return 0
    elif value > 25:
        return 10
    elif value > 18:
        return 8
    elif value > 12:
        return 6
    elif value > 5:
        return 4
    else:
        return 2

def score_ebitda_margin(value):
    """Score EBITDA margin based on predefined thresholds."""
    if pd.isna(value) or value == '-':
        return 0
    elif value > 25:
        return 10
    elif value > 18:
        return 8
    elif value > 12:
        return 6
    elif value > 5:
        return 4
    else:
        return 2

def score_roe(value):
    """Score Return on Equity (ROE) based on predefined thresholds."""
    if pd.isna(value) or value == '-':
        return 0
    elif value > 25:
        return 10
    elif value > 15:
        return 8
    elif value > 10:
        return 6
    elif value > 5:
        return 4
    else:
        return 2

def score_debt_equity(value):
    """Score Debt/Equity ratio based on predefined thresholds."""
    if pd.isna(value) or value == '-':
        return 0
    elif value < 0.5:
        return 10
    elif value <= 1:
        return 8
    elif value <= 1.5:
        return 6
    elif value <= 2:
        return 4
    else:
        return 2

def score_roa(value):
    """Score Return on Assets (ROA) based on predefined thresholds."""
    if pd.isna(value) or value == '-':
        return 0
    elif value > 10:
        return 10
    elif value > 7:
        return 8
    elif value > 4:
        return 6
    elif value > 1:
        return 4
    else:
        return 2

# Function to preprocess percentage values (unchanged)
def preprocess_percentage_columns(data, columns):
    """Preprocess percentage columns by removing '%' and converting to float."""
    for col in columns:
        if col in data.columns:
            data[col] = data[col].replace('-', np.nan, regex=True)
            data[col] = data[col].replace('%', '', regex=True).astype(float)
    return data

# Main function to process stock data
def process_stock_data_csv(input_file, output_file):
    """Process stock data, calculate scores, and save the results."""
    try:
        data = pd.read_csv(input_file)
    except Exception as e:
        print(f"Error reading the input file: {e}")
        return

    # Preprocess percentage columns
    percentage_columns = [
        'Profit Margin', 'EBITDA Margin', 'Return on Equity (ROE)',
        'Return on Assets (ROA)', 'Revenue Growth (YoY)', 'EPS Growth'
    ]
    data = preprocess_percentage_columns(data, percentage_columns)

    # Convert numeric columns
    for col in data.columns:
        if col not in ['Stock Symbol', 'Theme']:
            data[col] = pd.to_numeric(data[col], errors='coerce')

    # Apply scoring logic
    data['Revenue Growth (YoY) Score'] = data['Revenue Growth (YoY)'].apply(score_revenue_growth)
    data['EPS Growth Score'] = data['EPS Growth'].apply(score_eps_growth)
    data['RSI Score'] = data['RSI'].apply(score_rsi)
    data['Analyst Target Price Score'] = data.apply(
        lambda row: score_analyst_target_price(row['Current Price'], row['Analyst Target Price']), axis=1
    )
    data['Beta Score'] = data['Beta'].apply(score_beta)
    data['Profit Margin Score'] = data['Profit Margin'].apply(score_profit_margin)
    data['EBITDA Margin Score'] = data['EBITDA Margin'].apply(score_ebitda_margin)
    data['Return on Equity (ROE) Score'] = data['Return on Equity (ROE)'].apply(score_roe)
    data['Debt/Equity Ratio Score'] = data['Debt / Equity'].apply(score_debt_equity)
    data['Return on Assets (ROA) Score'] = data['Return on Assets (ROA)'].apply(score_roa)

    # Define weights for scoring
    weights = {
        'Revenue Growth (YoY) Score': 0.15,
        'EPS Growth Score': 0.15,
        'RSI Score': 0.1,
        'Analyst Target Price Score': 0.1,
        'Beta Score': 0.05,
        'Profit Margin Score': 0.1,
        'EBITDA Margin Score': 0.1,
        'Return on Equity (ROE) Score': 0.1,
        'Debt/Equity Ratio Score': 0.05,
        'Return on Assets (ROA) Score': 0.1
    }

    # Calculate total score
    data['Total Score'] = sum([data[col] * weight for col, weight in weights.items()])

    # Rank the stocks with unique ranks
    data['Rank'] = data['Total Score'].rank(ascending=False, method='min')

    # Adjust ranks to ensure uniqueness
    data['Rank'] = data['Rank'] + data.groupby('Rank').cumcount()

    # Save to the same CSV file (overwrite)
    try:
        data.to_csv(output_file, index=False)
        print(f"Processed data saved to {output_file}")
    except Exception as e:
        print(f"Error writing to output file: {e}")

    # Display ranked stock symbols
    ranked_stocks = data[['Stock Symbol', 'Rank']].sort_values(by='Rank')
    print("\nRanked Stock Symbols:")
    print(ranked_stocks.to_string(index=False))

# Example usage
process_stock_data_csv("Midcap.csv", "Midcap.csv")