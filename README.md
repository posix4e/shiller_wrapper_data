# Shiller Data Repository

This repository automatically downloads Robert Shiller's stock market and economic data and publishes it to GitHub Pages. The data files are NOT tracked in git history - only the code is versioned.

## Data Files

The following files are generated and published to GitHub Pages:
- `Fig3-1.xls` - Figure 3.1 data from "Irrational Exuberance"
- `ie_data.xls` - Full dataset with stock prices, earnings, dividends, and P/E ratios since 1871
- JSON and CSV versions of the data

## Automated Updates

This repository uses GitHub Actions to:
- **Run weekly updates** every Monday at 9:00 AM UTC
- **Manual updates** can be triggered from the Actions tab
- **Deploy directly to GitHub Pages** without committing data files to git

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

This data is widely used for market valuation analysis and historical research.# Trigger Pages rebuild
