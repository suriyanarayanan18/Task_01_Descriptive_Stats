import csv
import math
from collections import Counter

def load_data(filepath):
    #Load CSV using DictReader. Returns list of row dicts and column names.
    rows = []
    with open(filepath, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        columns = reader.fieldnames
        for row in reader:
            rows.append(row)
    return rows, columns

def is_blank(value):
    #Check if a value is missing or empty.
    return value is None or str(value).strip() == ""


def try_float(value):
    #Try converting a string to float. Returns None if it fails.
    if is_blank(value):
        return None
    try:
        return float(value)
    except ValueError:
        return None
    
def parse_range_value(value):
    # parse the range dicts in spend/impressions/audience_size columns
    # returns midpoint of lower and upper bounds
    if is_blank(value):
        return None
    val = str(value)
    if "lower_bound" not in val:
        return None
    try:
        # strip out the curly braces and quotes so we can split cleanly
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
            # some rows only have lower_bound (e.g. audience > 1M)
            return lower
        return None
    except (ValueError, IndexError):
        return None

def infer_column_type(col_values):
    # figures out if a column is range_dict, numeric, date, or categorical
    # checks a sample of 100 values to decide
    non_blank = [v for v in col_values if not is_blank(v)]
    if len(non_blank) == 0:
        return "empty"

    # only check first 100 values, no need to scan all 246k rows
    sample = non_blank[:100]

    # check for range dicts first
    range_hits = sum(1 for v in sample if "lower_bound" in str(v))
    if range_hits > len(sample) * 0.5:
        return "range_dict"

    # check for numeric
    num_hits = sum(1 for v in sample if try_float(v) is not None)
    if num_hits > len(sample) * 0.8:
        return "numeric"

    # check for dates - looking for slash-separated patterns like 10/28/2024
    date_hits = 0
    for v in sample:
        parts = str(v).strip().split("/")
        if len(parts) == 3:
            date_hits += 1
    if date_hits > len(sample) * 0.8:
        return "date"

    return "categorical"

# -- stats functions --

def compute_numeric_stats(col_values):
    #Compute count, mean, min, max, std dev, median for numeric values.
    numbers = []
    for v in col_values:
        parsed = try_float(v)
        if parsed is not None:
            numbers.append(parsed)

    if len(numbers) == 0:
        return {"count": 0, "mean": None, "min": None, "max": None,
                "std_dev": None, "median": None}

    n = len(numbers)
    mean = sum(numbers) / n
    min_val = min(numbers)
    max_val = max(numbers)

    # population standard deviation
    variance = sum((x - mean) ** 2 for x in numbers) / n
    std_dev = math.sqrt(variance)

    # median
    sorted_nums = sorted(numbers)
    mid = n // 2
    if n % 2 == 0:
        median = (sorted_nums[mid - 1] + sorted_nums[mid]) / 2
    else:
        median = sorted_nums[mid]

    return {"count": n, "mean": round(mean, 4), "min": min_val,
            "max": max_val, "std_dev": round(std_dev, 4), "median": median}


def compute_range_stats(col_values):
    #Same as numeric stats but first parses range dicts to midpoints.
    midpoints = []
    for v in col_values:
        mp = parse_range_value(v)
        if mp is not None:
            midpoints.append(mp)

    if len(midpoints) == 0:
        return {"count": 0, "mean": None, "min": None, "max": None,
                "std_dev": None, "median": None}

    n = len(midpoints)
    mean = sum(midpoints) / n
    min_val = min(midpoints)
    max_val = max(midpoints)

    variance = sum((x - mean) ** 2 for x in midpoints) / n
    std_dev = math.sqrt(variance)

    sorted_vals = sorted(midpoints)
    mid = n // 2
    if n % 2 == 0:
        median = (sorted_vals[mid - 1] + sorted_vals[mid]) / 2
    else:
        median = sorted_vals[mid]

    return {"count": n, "mean": round(mean, 4), "min": min_val,
            "max": max_val, "std_dev": round(std_dev, 4), "median": median}


def compute_categorical_stats(col_values):
    #Compute count, unique count, mode and frequency, top 5 for text columns.
    non_blank = [str(v).strip() for v in col_values if not is_blank(v)]

    if len(non_blank) == 0:
        return {"count": 0, "unique": 0, "mode": None,
                "mode_freq": 0, "top_5": []}

    freq = Counter(non_blank)
    most_common = freq.most_common(5)
    mode_val, mode_freq = most_common[0]

    return {"count": len(non_blank), "unique": len(freq),
            "mode": mode_val, "mode_freq": mode_freq, "top_5": most_common}

# -- output formatting --

def print_section(title):
    print("\n" + "=" * 65)
    print(title)
    print("=" * 65)


# -- main --

def main():
    filepath = "fb_ads_president_scored_anon.csv"

    print("Loading data...")
    rows, columns = load_data(filepath)
    print(f"Done. {len(rows)} rows loaded.\n")

    # ---- dataset overview ----
    print_section("DATASET OVERVIEW")
    print(f"Total rows:    {len(rows)}")
    print(f"Total columns: {len(columns)}")

    # missing values
    print(f"\nMissing values per column:")
    print("-" * 40)
    total_missing = 0
    for col in columns:
        missing = sum(1 for row in rows if is_blank(row.get(col, "")))
        if missing > 0:
            pct = round(missing / len(rows) * 100, 2)
            print(f"  {col}: {missing} ({pct}%)")
            total_missing += missing
    if total_missing == 0:
        print("  No missing values found.")

    # infer types
    print(f"\nInferred column types:")
    print("-" * 40)
    type_map = {}
    for col in columns:
        col_values = [row.get(col, "") for row in rows]
        col_type = infer_column_type(col_values)
        type_map[col] = col_type
        print(f"  {col}: {col_type}")

    # -- numeric columns --
    print_section("NUMERIC COLUMNS")

    for col in columns:
        col_values = [row.get(col, "") for row in rows]
        if type_map[col] == "numeric":
            stats = compute_numeric_stats(col_values)
            print(f"\n  {col}")
            print(f"    Count:    {stats['count']}")
            print(f"    Mean:     {stats['mean']}")
            print(f"    Min:      {stats['min']}")
            print(f"    Max:      {stats['max']}")
            print(f"    Std Dev:  {stats['std_dev']}")
            print(f"    Median:   {stats['median']}")

    # -- range-based columns --
    print_section("RANGE-BASED COLUMNS (spend, impressions, audience size)")
    print("  Note: these columns contain lower/upper bound ranges.")
    print("  Stats are computed on the midpoint of each range.\n")

    for col in columns:
        col_values = [row.get(col, "") for row in rows]
        if type_map[col] == "range_dict":
            stats = compute_range_stats(col_values)
            print(f"  {col}")
            print(f"    Count:    {stats['count']}")
            print(f"    Mean:     {stats['mean']}")
            print(f"    Min:      {stats['min']}")
            print(f"    Max:      {stats['max']}")
            print(f"    Std Dev:  {stats['std_dev']}")
            print(f"    Median:   {stats['median']}")
            print()

    # -- categorical and date columns --
    print_section("CATEGORICAL / TEXT COLUMNS")

    for col in columns:
        col_values = [row.get(col, "") for row in rows]
        if type_map[col] in ("categorical", "date"):
            stats = compute_categorical_stats(col_values)
            print(f"\n  {col}")
            print(f"    Count (non-null):  {stats['count']}")
            print(f"    Unique values:     {stats['unique']}")
            print(f"    Mode: {stats['mode']}")
            print(f"    Mode frequency:    {stats['mode_freq']}")
            print(f"    Top 5 values:")
            for val, freq in stats["top_5"]:
                # keep long strings readable
                if len(val) > 55:
                    val = val[:52] + "..."
                print(f"      {val}: {freq}")

    print_section("ANALYSIS COMPLETE")


if __name__ == "__main__":
    main()