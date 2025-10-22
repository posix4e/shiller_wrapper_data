# Shiller Data Repository

This repository automatically downloads and tracks historical changes to Robert Shiller's stock market and economic data files.

## Data Files

- `Fig3-1.xls` - Figure 3.1 data from "Irrational Exuberance"
- `ie_data.xls` - Full dataset with stock prices, earnings, dividends, and P/E ratios since 1871

## Automated Updates

This repository uses GitHub Actions to:
- **Check for updates on every push** to main/master branch
- **Run weekly updates** every Monday at 9:00 AM UTC
- **Manual updates** can be triggered from the Actions tab

## Manual Download

To manually download the latest data:

```bash
python download_shiller_data.py
```

## Data Source

Data is sourced from Professor Robert Shiller's website:
- http://www.econ.yale.edu/~shiller/data.htm

## Usage

The Excel files contain historical U.S. stock market data including:
- S&P 500 index values
- Earnings data
- Dividend yields
- P/E ratios (including CAPE/Shiller PE)
- Interest rates
- CPI data

This data is widely used for market valuation analysis and historical research.