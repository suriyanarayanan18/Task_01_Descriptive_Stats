import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import seaborn as sns
from collections import Counter

# set a clean style
sns.set_style("whitegrid")

# load data
print("Loading data...")
df = pd.read_csv("fb_ads_president_scored_anon.csv")
print(f"Loaded {len(df)} rows.")

# ---- Chart 1: Top 10 spenders by ad count ----
print("Creating Chart 1: Top 10 spenders...")

top_spenders = df["bylines"].value_counts().head(10)

fig, ax = plt.subplots(figsize=(10, 6))
bars = ax.barh(top_spenders.index[::-1], top_spenders.values[::-1], color="steelblue")

# add count labels on each bar
for bar in bars:
    width = bar.get_width()
    ax.text(width + 200, bar.get_y() + bar.get_height()/2,
            f"{int(width):,}", va="center", fontsize=9)

ax.set_xlabel("Number of Ads")
ax.set_title("Top 10 Organizations by Ad Count", fontsize=14, fontweight="bold")
ax.xaxis.set_major_formatter(ticker.FuncFormatter(lambda x, p: format(int(x), ",")))
plt.tight_layout()
plt.savefig("visualizations/top_10_spenders.png", dpi=150)
plt.close()
print("  Saved: visualizations/top_10_spenders.png")

# ---- Chart 2: Ad volume over time ----
print("Creating Chart 2: Ad volume over time...")

# convert to datetime and count ads per day
df["ad_creation_date"] = pd.to_datetime(df["ad_creation_time"], format="%m/%d/%Y")
ads_per_day = df.groupby("ad_creation_date").size()

fig, ax = plt.subplots(figsize=(12, 5))
ax.plot(ads_per_day.index, ads_per_day.values, color="steelblue", linewidth=1.2)

# mark election day
election_day = pd.Timestamp("2024-11-05")
ax.axvline(x=election_day, color="red", linestyle="--", alpha=0.7, label="Election Day (Nov 5)")

# mark debate dates
debate_1 = pd.Timestamp("2024-06-27")  # Biden-Trump debate
debate_2 = pd.Timestamp("2024-09-10")  # Harris-Trump debate
ax.axvline(x=debate_1, color="orange", linestyle="--", alpha=0.5, label="Biden-Trump Debate (Jun 27)")
ax.axvline(x=debate_2, color="green", linestyle="--", alpha=0.5, label="Harris-Trump Debate (Sep 10)")

ax.set_xlabel("Date")
ax.set_ylabel("Number of Ads Created")
ax.set_title("Daily Ad Volume Over the 2024 Election Cycle", fontsize=14, fontweight="bold")
ax.legend(fontsize=9)
plt.tight_layout()
plt.savefig("visualizations/ads_over_time.png", dpi=150)
plt.close()
print("  Saved: visualizations/ads_over_time.png")

# ---- Chart 3: Spend distribution ----
print("Creating Chart 3: Spend distribution...")

def get_spend_midpoint(val):
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

spend_values = df["spend"].apply(get_spend_midpoint).dropna()

fig, ax = plt.subplots(figsize=(10, 5))
# cap at $10,000 to see the distribution clearly (most ads are under this)
spend_capped = spend_values[spend_values <= 10000]
ax.hist(spend_capped, bins=50, color="steelblue", edgecolor="white")

ax.set_xlabel("Estimated Spend ($)")
ax.set_ylabel("Number of Ads")
ax.set_title("Distribution of Ad Spend (capped at $10,000)", fontsize=14, fontweight="bold")
ax.xaxis.set_major_formatter(ticker.FuncFormatter(lambda x, p: f"${int(x):,}"))
plt.tight_layout()
plt.savefig("visualizations/spend_distribution.png", dpi=150)
plt.close()
print("  Saved: visualizations/spend_distribution.png")

# ---- Chart 4: Platform breakdown ----
print("Creating Chart 4: Platform breakdown...")

platform_counts = df["publisher_platforms"].value_counts()

# simplify the labels
label_map = {}
for val in platform_counts.index:
    if "facebook" in val and "instagram" in val and "audience_network" not in val:
        label_map[val] = "Facebook + Instagram"
    elif val == "['facebook']":
        label_map[val] = "Facebook only"
    elif val == "['instagram']":
        label_map[val] = "Instagram only"
    else:
        label_map[val] = "Other"

simplified = {}
for val, count in platform_counts.items():
    label = label_map.get(val, "Other")
    simplified[label] = simplified.get(label, 0) + count

# sort by count
sorted_platforms = sorted(simplified.items(), key=lambda x: x[1])
labels = [item[0] for item in sorted_platforms]
sizes = [item[1] for item in sorted_platforms]

fig, ax = plt.subplots(figsize=(10, 5))
bars = ax.barh(labels, sizes, color="steelblue")

for bar in bars:
    width = bar.get_width()
    pct = width / len(df) * 100
    ax.text(width + 500, bar.get_y() + bar.get_height()/2,
            f"{int(width):,} ({pct:.1f}%)", va="center", fontsize=9)

ax.set_xlabel("Number of Ads")
ax.set_title("Ad Distribution by Platform", fontsize=14, fontweight="bold")
ax.xaxis.set_major_formatter(ticker.FuncFormatter(lambda x, p: format(int(x), ",")))
plt.tight_layout()
plt.savefig("visualizations/platform_split.png", dpi=150)
plt.close()
print("  Saved: visualizations/platform_split.png")