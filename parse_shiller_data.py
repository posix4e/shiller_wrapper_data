#!/usr/bin/env python3
"""
Parse Shiller Excel files and convert to JSON/CSV formats for API
"""

import os
import json
import csv
import pandas as pd
import numpy as np
from datetime import datetime
import warnings

warnings.filterwarnings('ignore')

def parse_ie_data():
    """Parse the main ie_data.xls file containing stock market data"""
    try:
        # Read the Data sheet from ie_data.xls
        df = pd.read_excel('ie_data.xls', sheet_name='Data', header=7)

        # Clean column names
        df.columns = df.columns.str.strip()

        # Rename columns to be more API-friendly
        column_mapping = {
            'Date': 'date',
            'S&P Comp.': 'sp500',
            'P': 'sp500',  # shillerdata.com uses 'P' instead of 'S&P Comp.'
            'Dividend': 'dividend',
            'D': 'dividend',  # shillerdata.com uses 'D'
            'Earnings': 'earnings',
            'E': 'earnings',  # shillerdata.com uses 'E'
            'CPI': 'cpi',
            'Date.1': 'date_fraction',
            'Fraction': 'date_fraction',  # shillerdata.com uses 'Fraction'
            'Long Interest Rate GS10': 'long_interest_rate',
            'Rate GS10': 'long_interest_rate',  # shillerdata.com uses 'Rate GS10'
            'Real Price': 'real_price',
            'Price': 'real_price',  # shillerdata.com uses 'Price'
            'Real Dividend': 'real_dividend',
            'Real Total Return Price': 'real_total_return_price',
            'Real Earnings': 'real_earnings',
            'Real TR Scaled Earnings': 'real_tr_scaled_earnings',
            'CAPE': 'cape',
            'TR CAPE': 'tr_cape',
            'Excess CAPE Yield': 'excess_cape_yield',
            'Monthly Total Bond Returns': 'monthly_bond_returns',
            'Real Total Bond Returns': 'real_total_bond_returns',
            '10 Year Annualized Stock Real Return': 'annualized_stock_return_10y',
            '10 Year Annualized Bond Real Return': 'annualized_bond_return_10y',
            'Real 10 Year Excess Annualized Returns': 'real_excess_return_10y'
        }

        # Rename columns that exist
        df = df.rename(columns={k: v for k, v in column_mapping.items() if k in df.columns})

        # Remove rows with all NaN values first
        df = df.dropna(how='all')

        # Convert date to string format
        if 'date' in df.columns:
            # Handle the decimal date format (e.g., 1871.01 for January 1871)
            # First remove any NaN dates
            df = df[df['date'].notna()]

            df['date_str'] = df['date'].astype(str)
            df['year'] = df['date_str'].str.split('.').str[0].astype(int)
            df['month_str'] = df['date_str'].str.split('.').str[1].fillna('01')
            df['month'] = df['month_str'].str.ljust(2, '0').astype(int)
            df['date_string'] = df.apply(lambda x: f"{x['year']:04d}-{x['month']:02d}-01", axis=1)

            # Drop temporary columns
            df = df.drop(['date_str', 'month_str'], axis=1)

        # Convert NaN to None for JSON serialization
        df = df.replace({np.nan: None})

        # Create data dictionary
        data = {
            'metadata': {
                'source': 'Robert Shiller - Yale Economics',
                'last_updated': datetime.now().isoformat(),
                'description': 'U.S. Stock Market Data including S&P 500, earnings, dividends, and CAPE ratio',
                'start_date': df['date_string'].iloc[0] if 'date_string' in df.columns and len(df) > 0 else None,
                'end_date': df['date_string'].iloc[-1] if 'date_string' in df.columns and len(df) > 0 else None,
                'total_records': len(df)
            },
            'data': df.to_dict('records')
        }

        return data, df

    except Exception as e:
        print(f"Error parsing ie_data.xls: {e}")
        import traceback
        traceback.print_exc()
        return None, None

def parse_fig31_data():
    """Parse the Fig3-1.xls file containing home price data"""
    try:
        # Read the Data sheet (not 'Fig 3.1')
        df = pd.read_excel('Fig3-1.xls', sheet_name='Data', header=3)

        # Clean column names
        df.columns = df.columns.str.strip()

        # Rename columns
        column_mapping = {
            'Date': 'date',
            'Real Home Price Index': 'real_home_price_index',
            'Building Cost Index': 'building_cost_index',
            'US Population (millions)': 'us_population_millions',
            'Long Rate': 'long_rate'
        }

        # Rename columns that exist
        df = df.rename(columns={k: v for k, v in column_mapping.items() if k in df.columns})

        # Convert date to string format if it exists
        if 'date' in df.columns:
            df['year'] = df['date'].astype(int)
            df['date_string'] = df['year'].astype(str) + '-01-01'

        # Remove rows with all NaN values
        df = df.dropna(how='all')

        # Convert NaN to None for JSON serialization
        df = df.replace({np.nan: None})

        # Create data dictionary
        data = {
            'metadata': {
                'source': 'Robert Shiller - Irrational Exuberance Figure 3.1',
                'last_updated': datetime.now().isoformat(),
                'description': 'U.S. Real Home Price Index and related data since 1890',
                'start_date': df['date_string'].iloc[0] if 'date_string' in df.columns else None,
                'end_date': df['date_string'].iloc[-1] if 'date_string' in df.columns else None,
                'total_records': len(df)
            },
            'data': df.to_dict('records')
        }

        return data, df

    except Exception as e:
        print(f"Error parsing Fig3-1.xls: {e}")
        return None, None

def save_json_files(ie_data, fig31_data):
    """Save parsed data to JSON files"""
    # Create data directory
    os.makedirs('data', exist_ok=True)

    if ie_data:
        with open('data/stock_market_data.json', 'w') as f:
            json.dump(ie_data, f, indent=2)
        print("✓ Saved data/stock_market_data.json")

    if fig31_data:
        with open('data/home_price_data.json', 'w') as f:
            json.dump(fig31_data, f, indent=2)
        print("✓ Saved data/home_price_data.json")

def save_csv_files(ie_df, fig31_df):
    """Save parsed data to CSV files"""
    os.makedirs('data', exist_ok=True)

    if ie_df is not None:
        # Select important columns for CSV
        csv_columns = ['date_string', 'sp500', 'dividend', 'earnings', 'cpi', 'cape',
                      'real_price', 'real_dividend', 'real_earnings', 'long_interest_rate']
        csv_df = ie_df[[col for col in csv_columns if col in ie_df.columns]]
        csv_df.to_csv('data/stock_market_data.csv', index=False)
        print("✓ Saved data/stock_market_data.csv")

    if fig31_df is not None:
        csv_columns = ['date_string', 'real_home_price_index', 'building_cost_index',
                      'us_population_millions', 'long_rate']
        csv_df = fig31_df[[col for col in csv_columns if col in fig31_df.columns]]
        csv_df.to_csv('data/home_price_data.csv', index=False)
        print("✓ Saved data/home_price_data.csv")

def create_latest_values():
    """Create a JSON file with just the latest values for quick access"""
    latest = {}

    # Get latest stock market values
    try:
        with open('data/stock_market_data.json', 'r') as f:
            data = json.load(f)
            if data['data']:
                latest_record = data['data'][-1]
                latest['stock_market'] = {
                    'date': latest_record.get('date_string'),
                    'sp500': latest_record.get('sp500'),
                    'cape': latest_record.get('cape'),
                    'dividend_yield': latest_record.get('dividend') / latest_record.get('sp500') * 12 * 100 if latest_record.get('dividend') and latest_record.get('sp500') else None,
                    'earnings': latest_record.get('earnings'),
                    'cpi': latest_record.get('cpi')
                }
    except:
        pass

    # Get latest home price values
    try:
        with open('data/home_price_data.json', 'r') as f:
            data = json.load(f)
            if data['data']:
                latest_record = data['data'][-1]
                latest['home_prices'] = {
                    'date': latest_record.get('date_string'),
                    'real_home_price_index': latest_record.get('real_home_price_index'),
                    'building_cost_index': latest_record.get('building_cost_index'),
                    'us_population_millions': latest_record.get('us_population_millions')
                }
    except:
        pass

    latest['last_updated'] = datetime.now().isoformat()

    with open('data/latest.json', 'w') as f:
        json.dump(latest, f, indent=2)
    print("✓ Saved data/latest.json")

def main():
    """Main function to parse all data files"""
    print("Parsing Shiller data files...")

    # Parse ie_data.xls
    ie_data, ie_df = parse_ie_data()

    # Parse Fig3-1.xls
    fig31_data, fig31_df = parse_fig31_data()

    # Save JSON files
    save_json_files(ie_data, fig31_data)

    # Save CSV files
    save_csv_files(ie_df, fig31_df)

    # Create latest values file
    create_latest_values()

    print("\nData parsing complete!")

if __name__ == "__main__":
    main()