# Task 01: Analyzing 2024 Facebook Political Ads: A Dual Approach with Python

## Project Description

This project analyzes a dataset of 246,745 Facebook political ads from the 2024 U.S. Presidential election. The analysis is performed twice: once using only Python's standard library and once using Pandas, to compare approaches and verify results.

The dataset contains information about ad purchases including the sponsoring organization, spend amounts, impression counts, platform targeting, candidate mentions, and topic classifications.

## Dataset

**Source:** [2024 Facebook Political Ads (Google Drive)](PASTE_YOUR_GOOGLE_DRIVE_LINK_HERE)

The dataset file is not included in this repository due to its size (46 MB). To run the scripts:

1. Download the file from the link above
2. Save it as `fb_ads_president_scored_anon.csv`
3. Place it in the root directory of this project

## How to Run

### Pure Python Script (no dependencies)
```bash
python pure_python_stats.py
```

This script uses only the standard library (csv, math, collections). No installation needed.

### Pandas Script

Install dependencies first:
```bash
pip install -r requirements.txt
```

Then run:
```bash
python pandas_stats.py
```

### Visualizations
```bash
pip install -r requirements.txt
python visualizations.py
```

Output charts are saved to the `visualizations/` folder.

## Repository Structure
```
Task_01_Descriptive_Stats/
    pure_python_stats.py       # Descriptive stats using standard library only
    pandas_stats.py            # Same analysis using Pandas
    visualizations.py          # Charts and visualizations
    FINDINGS.md                # Narrative analysis of the data
    COMPARISON.md              # Comparison of the two approaches
    README.md                  # This file
    requirements.txt           # Python dependencies
    .gitignore                 # Excludes dataset and cache files
    visualizations/            # Output charts
        top_10_spenders.png
        ads_over_time.png
        spend_distribution.png
        platform_split.png
```

## Key Findings

- The Harris campaign dominated ad volume with over 82,000 ads across two entities, while Trump's spending was spread across multiple committees and PACs.
- Ad spending is heavily right-skewed: the median spend was $49.50 while the mean was $1,062, driven by a small number of high-budget ads.
- 86.9% of ads targeted both Facebook and Instagram simultaneously.
- Ad volume increased dramatically in October 2024, peaking just days before the November 5 election.
- Donald Trump was the most mentioned candidate (78,324 mentions) despite the Harris campaign running more ads, suggesting many Harris-aligned ads focused on the opponent.

For the full analysis, see [FINDINGS.md](FINDINGS.md).

## Approach Comparison

Both scripts produce matching results across all key metrics. Notable differences include how each approach handles type detection, missing values, and standard deviation defaults. The pure Python version required explicit handling of edge cases (range dictionary parsing, missing upper bounds) that Pandas abstracts away.

For the full comparison, see [COMPARISON.md](COMPARISON.md).

## Author

Suriya Narayanan 
