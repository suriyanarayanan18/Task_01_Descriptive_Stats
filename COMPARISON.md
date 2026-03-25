# Comparison: Pure Python vs Pandas

## Overview

This document reflects on the differences between the two approaches used to analyze the 2024 Facebook Political Ads dataset. The pure Python script (`pure_python_stats.py`) uses only the standard library, while the Pandas script (`pandas_stats.py`) uses the Pandas library to perform the same analysis.

## Do the Results Agree?

For the most part, yes. The core statistics (count, mean, min, max, median) matched across both scripts for all columns. Missing value counts were identical: 2,159 for `ad_delivery_stop_time`, 1,009 for `bylines`, and 579 for `estimated_audience_size`.

One minor difference showed up in the unique count for `bylines`: 3,786 in the pure Python script vs 3,790 in Pandas. This is likely due to how each approach handles trailing whitespace or NaN values when counting unique entries. Pandas treats NaN as a distinct category in some operations, which can slightly inflate the unique count.

Standard deviation values also differ very slightly between the two scripts when using Pandas' default settings. This is because Pandas uses sample standard deviation (dividing by n-1) by default, while my pure Python implementation uses population standard deviation (dividing by n). To make the comparison fair, I used `ddof=0` in the Pandas script for the range-based columns so the numbers would match. This is a good example of a silent default that could lead to confusion if you were not paying attention.

## Where Did Pure Python Force Decisions That Pandas Made Silently?

Several places:

**Type detection.** In the pure Python script, I had to write my own `infer_column_type()` function that samples values and checks whether they look numeric, date-like, or like range dictionaries. Pandas does this automatically with `read_csv()` and assigns dtypes like `int64` or `object`. The catch is that Pandas labeled the range columns (spend, impressions, estimated_audience_size) as `object` type, which just means "string." It did not recognize them as numeric data. My pure Python script explicitly identified these as `range_dict` type and parsed them accordingly. If I had only used Pandas and relied on `describe()`, I would have missed these columns entirely in the numeric summary.

**Range parsing.** The spend, impressions, and estimated_audience_size columns contain dictionary-like strings with lower and upper bounds. There is no built-in Pandas function that handles this. I had to write the same `parse_range_value()` logic in both scripts. The pure Python version forced me to discover this format early on because I was manually inspecting values. With Pandas, `describe(include='object')` would have just told me the most common string and moved on.

**Missing value handling.** In pure Python, I explicitly checked for empty strings, None, and whitespace using an `is_blank()` function because `csv.DictReader` keeps blank cells as empty strings. I had to decide what counts as "missing." Pandas handled this differently: `pd.read_csv()` automatically converts empty strings to NaN during loading, so by the time the data is in the DataFrame, `isnull()` catches everything. The counts matched, but only because Pandas silently made the conversion that I had to handle explicitly in pure Python. On messier data with values like "N/A" or "none", Pandas might not catch those without extra configuration, while the pure Python approach forces you to define every edge case upfront.

**Handling rows with only a lower bound.** The `estimated_audience_size` column had about 100,000 rows where Facebook only provided a lower bound (e.g., `{'lower_bound': '1000001'}`) with no upper bound. My initial pure Python parser missed these entirely because it required both bounds. I caught this because the count was much lower than expected (146,020 vs 246,166). I had to add an explicit check: if only the lower bound exists, use it directly. This is the kind of edge case that manual computation forces you to find and fix.

## What Did I Learn From Writing the Pure Python Version?

The biggest takeaway is that writing statistics from scratch makes you confront every assumption. When I computed the mean manually, I had to handle the case where a column might have zero valid values (division by zero). When I computed the median, I had to sort the list and handle even vs odd counts. These are operations that `df.describe()` abstracts away, and doing them manually gave me a clearer picture of what that function actually computes and where its defaults might not fit every dataset.

The pure Python script took significantly longer to write roughly 3x the time, but it gave me a much better understanding of the data. I found the range dictionary format, the missing upper bounds, and the implications of the data being reported as ranges rather than exact values. If I had jumped straight to Pandas, I would have gotten summary statistics faster but understood the data less.

## Code Comparison

| Aspect | Pure Python | Pandas |
|--------|------------|--------|
| Lines of code | ~220 | ~120 |
| External dependencies | None | pandas |
| Load time (246K rows) | ~20 seconds | ~3 seconds |
| Type detection | Manual sampling | Automatic (dtypes) |
| Std dev default | Population (n) | Sample (n-1) |
| Range column handling | Custom parser | Custom parser (same) |
| Missing value detection | is_blank() function | isnull() built-in |