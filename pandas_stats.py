import pandas as pd
def load_and_overview(filepath):
    #Load the dataset and print basic structure.
    df = pd.read_csv(filepath)

    print("=" * 65)
    print("DATASET OVERVIEW")
    print("=" * 65)
    print(f"Shape: {df.shape[0]} rows x {df.shape[1]} columns\n")

    print("Column data types:")
    print("-" * 40)
    print(df.dtypes.to_string())

    print(f"\nDataset info:")
    print("-" * 40)
    df.info()

    return df
def missing_values(df):
    #Print missing value counts and percentages.
    print("\n" + "=" * 65)
    print("MISSING VALUES")
    print("=" * 65)

    missing = df.isnull().sum()
    # only show columns that actually have missing values
    missing = missing[missing > 0]

    if len(missing) == 0:
        print("No missing values found.")
        return

    missing_pct = round(missing / len(df) * 100, 2)
    missing_df = pd.DataFrame({"count": missing, "percentage": missing_pct})
    print(missing_df.to_string())


def summary_statistics(df):
    #Generate summary stats for numeric and non-numeric columns.
    print("\n" + "=" * 65)
    print("SUMMARY STATISTICS - NUMERIC COLUMNS")
    print("=" * 65)
    print(df.describe().to_string())

    print("\n" + "=" * 65)
    print("SUMMARY STATISTICS - CATEGORICAL COLUMNS")
    print("=" * 65)
    print(df.describe(include="object").to_string())

def parse_range_column(series):
    #Parse range dict columns (spend, impressions, estimated_audience_size).
    #Extracts midpoint of lower and upper bounds.
    #If only lower_bound exists, uses that value directly.
    
    def get_midpoint(val):
        if pd.isnull(val):
            return None
        val = str(val)
        if "lower_bound" not in val:
            return None
        try:
            parts = val.replace("{", "").replace("}", "").replace("'", "")
            tokens = parts.split(",")
            lower = None
            upper = None
            for token in tokens:
                token = token.strip()
                if "lower_bound" in token:
                    lower = float(token.split(":")[1].strip())
                elif "upper_bound" in token:
                    upper = float(token.split(":")[1].strip())
            if lower is not None and upper is not None:
                return (lower + upper) / 2
            elif lower is not None:
                return lower
            return None
        except (ValueError, IndexError):
            return None

    return series.apply(get_midpoint)


def analyze_range_columns(df):
    #Parse and compute stats for the range-based columns.
    print("\n" + "=" * 65)
    print("RANGE-BASED COLUMNS (spend, impressions, audience size)")
    print("=" * 65)
    print("Note: stats computed on midpoint of each range.\n")

    range_cols = ["estimated_audience_size", "impressions", "spend"]

    for col in range_cols:
        parsed = parse_range_column(df[col])
        print(f"  {col}")
        print(f"    Count:    {parsed.count()}")
        print(f"    Mean:     {round(parsed.mean(), 4)}")
        print(f"    Min:      {parsed.min()}")
        print(f"    Max:      {parsed.max()}")
        print(f"    Std Dev:  {round(parsed.std(ddof=0), 4)}")
        print(f"    Median:   {parsed.median()}")
        print()


def analyze_categorical_columns(df):
    #Detailed analysis of categorical columns with value_counts.
    print("\n" + "=" * 65)
    print("CATEGORICAL COLUMNS - DETAILED")
    print("=" * 65)

    cat_cols = df.select_dtypes(include="object").columns

    for col in cat_cols:
        print(f"\n  {col}")
        print(f"    Count (non-null):  {df[col].count()}")
        print(f"    Unique values:     {df[col].nunique()}")
        top_5 = df[col].value_counts().head(5)
        print(f"    Top 5 values:")
        for val, freq in top_5.items():
            if len(str(val)) > 55:
                val = str(val)[:52] + "..."
            print(f"      {val}: {freq}")

def main():
    filepath = "fb_ads_president_scored_anon.csv"

    print("Loading data...")
    df = load_and_overview(filepath)

    missing_values(df)

    summary_statistics(df)

    analyze_range_columns(df)

    analyze_categorical_columns(df)

    print("\n" + "=" * 65)
    print("ANALYSIS COMPLETE")
    print("=" * 65)


if __name__ == "__main__":
    main()