"""
TMDB EDA — Load, Merge, Clean, Explore & Plot
Loads all 5 tables from movies.db, merges into one DataFrame, then runs
exploratory analysis with visualisations for the workshop.
"""

import sqlite3
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
from pathlib import Path

sns.set_theme(style="whitegrid", palette="muted", font_scale=1.1)
Path("plots").mkdir(exist_ok=True)

DB = "movies.db"

# ── 1. Load all tables ───────────────────────────────────────────────
conn = sqlite3.connect(DB)

df_movies       = pd.read_sql("SELECT * FROM movies", conn)
df_genres       = pd.read_sql("SELECT * FROM genres", conn)
df_movie_genres = pd.read_sql("SELECT * FROM movie_genres", conn)
df_cast         = pd.read_sql("SELECT * FROM cast", conn)
df_directors    = pd.read_sql("SELECT * FROM directors", conn)

conn.close()

print("Tables loaded:")
for name, d in [("movies", df_movies), ("genres", df_genres),
                ("movie_genres", df_movie_genres), ("cast", df_cast),
                ("directors", df_directors)]:
    print(f"  {name:<15} {d.shape}")

# ── 2. Aggregate genres & cast per movie ─────────────────────────────
genres_agg = (
    df_movie_genres.groupby("movie_id")["genre_name"]
    .agg(lambda x: ", ".join(sorted(x)))
    .reset_index()
    .rename(columns={"genre_name": "genres"})
)

cast_agg = (
    df_cast.sort_values(["movie_id", "billing_order"])
    .groupby("movie_id")["actor_name"]
    .agg(lambda x: ", ".join(x))
    .reset_index()
    .rename(columns={"actor_name": "top_cast"})
)

directors_slim = df_directors[["movie_id", "director_name"]].copy()

# ── 3. Merge into one big DataFrame ──────────────────────────────────
df = (
    df_movies
    .merge(genres_agg, on="movie_id", how="left")
    .merge(cast_agg, on="movie_id", how="left")
    .merge(directors_slim, on="movie_id", how="left")
)

# ── 4. Clean: replace 0 with NaN for budget/revenue ─────────────────
df["budget"]  = df["budget"].replace(0, np.nan)
df["revenue"] = df["revenue"].replace(0, np.nan)

# Derived columns
df["profit"]     = df["revenue"] - df["budget"]
df["roi"]        = (df["profit"] / df["budget"]) * 100  # ROI as percentage
df["decade"]     = (df["release_year"] // 10 * 10).astype("Int64")

print(f"\nMerged DataFrame: {df.shape}")
print(f"Columns: {df.columns.tolist()}")
print(f"\nNull counts in key columns:")
for col in ["budget", "revenue", "runtime", "director_name", "genres", "top_cast"]:
    print(f"  {col:<20} {df[col].isna().sum()}")

# ── Helper to save plots ─────────────────────────────────────────────
def savefig(name):
    plt.tight_layout()
    plt.savefig(f"plots/{name}.png", dpi=150, bbox_inches="tight")
    print(f"  Saved plots/{name}.png")
    plt.close()

# ══════════════════════════════════════════════════════════════════════
# EDA PLOTS
# ══════════════════════════════════════════════════════════════════════

# ── Q1: Which genres have the most movies? ───────────────────────────
print("\nQ1: Genre distribution")
genre_counts = df_movie_genres["genre_name"].value_counts()

fig, ax = plt.subplots(figsize=(10, 6))
genre_counts.plot.barh(ax=ax, color=sns.color_palette("viridis", len(genre_counts)))
ax.set_xlabel("Number of Movies")
ax.set_title("Movies per Genre")
ax.invert_yaxis()
savefig("01_genre_distribution")

# ── Q2: Budget vs Revenue — does spending more earn more? ────────────
print("Q2: Budget vs Revenue scatter")
fin = df.dropna(subset=["budget", "revenue"])

fig, ax = plt.subplots(figsize=(10, 7))
scatter = ax.scatter(fin["budget"] / 1e6, fin["revenue"] / 1e6,
                     alpha=0.4, c=fin["vote_average"], cmap="RdYlGn", s=20)
ax.plot([0, fin["budget"].max() / 1e6], [0, fin["budget"].max() / 1e6],
        "r--", alpha=0.5, label="Break-even line")
ax.set_xlabel("Budget ($M)")
ax.set_ylabel("Revenue ($M)")
ax.set_title("Budget vs Revenue (color = rating)")
plt.colorbar(scatter, label="Vote Average")
ax.legend()
savefig("02_budget_vs_revenue")

# ── Q3: Rating distribution ──────────────────────────────────────────
print("Q3: Rating distribution")
fig, ax = plt.subplots(figsize=(10, 5))
ax.hist(df["vote_average"].dropna(), bins=40, edgecolor="white", color="#4C72B0")
ax.axvline(df["vote_average"].mean(), color="red", linestyle="--", label=f"Mean: {df['vote_average'].mean():.1f}")
ax.set_xlabel("Vote Average")
ax.set_ylabel("Count")
ax.set_title("Distribution of Movie Ratings")
ax.legend()
savefig("03_rating_distribution")

# ── Q4: Revenue by genre (box plot) ──────────────────────────────────
print("Q4: Revenue by genre")
genre_rev = df_movie_genres.merge(df[["movie_id", "revenue"]], on="movie_id")
genre_rev = genre_rev.dropna(subset=["revenue"])

top_genres = genre_rev["genre_name"].value_counts().head(10).index
genre_rev_top = genre_rev[genre_rev["genre_name"].isin(top_genres)]

fig, ax = plt.subplots(figsize=(12, 6))
order = genre_rev_top.groupby("genre_name")["revenue"].median().sort_values(ascending=False).index
sns.boxplot(data=genre_rev_top, x="genre_name", y="revenue", order=order, ax=ax, showfliers=False)
ax.set_ylabel("Revenue ($)")
ax.set_xlabel("")
ax.set_title("Revenue Distribution by Genre (top 10, outliers hidden)")
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x/1e6:.0f}M"))
plt.xticks(rotation=45, ha="right")
savefig("04_revenue_by_genre")

# ── Q5: How has average runtime changed over decades? ────────────────
print("Q5: Runtime over decades")
decade_runtime = df.dropna(subset=["decade", "runtime"]).groupby("decade")["runtime"].mean()

fig, ax = plt.subplots(figsize=(10, 5))
decade_runtime.plot(kind="bar", ax=ax, color="#55A868", edgecolor="white")
ax.set_ylabel("Average Runtime (min)")
ax.set_xlabel("Decade")
ax.set_title("Average Movie Runtime by Decade")
ax.set_xticklabels([str(int(x)) for x in decade_runtime.index], rotation=0)
savefig("05_runtime_by_decade")

# ── Q6: Franchise vs Standalone ──────────────────────────────────────
print("Q6: Franchise vs Standalone")
fran = df.dropna(subset=["revenue"])
fran["type"] = fran["is_franchise"].map({1: "Franchise", 0: "Standalone"})

fig, axes = plt.subplots(1, 2, figsize=(14, 5))

sns.boxplot(data=fran, x="type", y="revenue", ax=axes[0], showfliers=False)
axes[0].set_title("Revenue: Franchise vs Standalone")
axes[0].yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x/1e6:.0f}M"))
axes[0].set_xlabel("")

sns.boxplot(data=fran, x="type", y="vote_average", ax=axes[1], showfliers=False)
axes[1].set_title("Rating: Franchise vs Standalone")
axes[1].set_xlabel("")
savefig("06_franchise_vs_standalone")

# ── Q7: Best month to release a movie? ───────────────────────────────
print("Q7: Best release month")
monthly = df.dropna(subset=["release_month", "revenue"]).groupby("release_month").agg(
    avg_revenue=("revenue", "mean"),
    movie_count=("movie_id", "count"),
).reset_index()
month_names = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]

fig, ax1 = plt.subplots(figsize=(10, 5))
ax1.bar(monthly["release_month"], monthly["avg_revenue"] / 1e6, color="#4C72B0", alpha=0.7, label="Avg Revenue")
ax1.set_ylabel("Avg Revenue ($M)")
ax1.set_xlabel("Release Month")
ax1.set_xticks(range(1, 13))
ax1.set_xticklabels(month_names)
ax1.set_title("Average Revenue & Movie Count by Release Month")

ax2 = ax1.twinx()
ax2.plot(monthly["release_month"], monthly["movie_count"], "o-", color="#C44E52", label="Movie Count")
ax2.set_ylabel("Number of Movies")

lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1 + lines2, labels1 + labels2, loc="upper left")
savefig("07_best_release_month")

# ── Q8: Top 15 directors by avg rating (min 3 films) ────────────────
print("Q8: Top directors by rating")
dir_stats = (
    df.dropna(subset=["director_name"])
    .groupby("director_name")
    .agg(films=("movie_id", "count"), avg_rating=("vote_average", "mean"))
    .query("films >= 3")
    .sort_values("avg_rating", ascending=False)
    .head(15)
)

fig, ax = plt.subplots(figsize=(10, 6))
ax.barh(dir_stats.index, dir_stats["avg_rating"], color=sns.color_palette("coolwarm", len(dir_stats)))
ax.set_xlabel("Average Rating")
ax.set_title("Top 15 Directors by Avg Rating (min 3 films)")
ax.invert_yaxis()
for i, (val, films) in enumerate(zip(dir_stats["avg_rating"], dir_stats["films"])):
    ax.text(val + 0.05, i, f"{val:.1f} ({films} films)", va="center", fontsize=9)
savefig("08_top_directors_rating")

# ── Q9: Most appearing actors ────────────────────────────────────────
print("Q9: Most appearing actors")
actor_counts = df_cast["actor_name"].value_counts().head(20)

fig, ax = plt.subplots(figsize=(10, 6))
actor_counts.plot.barh(ax=ax, color=sns.color_palette("magma", len(actor_counts)))
ax.set_xlabel("Number of Movies (in top-5 billing)")
ax.set_title("Top 20 Most Appearing Actors")
ax.invert_yaxis()
savefig("09_top_actors")

# ── Q10: Correlation heatmap of numeric columns ─────────────────────
print("Q10: Correlation heatmap")
numeric_cols = ["budget", "revenue", "runtime", "vote_average", "vote_count", "popularity", "profit", "roi"]
corr = df[numeric_cols].corr()

fig, ax = plt.subplots(figsize=(10, 8))
sns.heatmap(corr, annot=True, fmt=".2f", cmap="RdBu_r", center=0, ax=ax, square=True)
ax.set_title("Correlation Heatmap of Numeric Features")
savefig("10_correlation_heatmap")

# ── Q11: Movies per year trend ───────────────────────────────────────
print("Q11: Movies per year")
yearly = df.dropna(subset=["release_year"])
yearly = yearly[yearly["release_year"].between(1970, 2025)]
year_counts = yearly.groupby("release_year").size()

fig, ax = plt.subplots(figsize=(12, 5))
ax.fill_between(year_counts.index, year_counts.values, alpha=0.3, color="#4C72B0")
ax.plot(year_counts.index, year_counts.values, color="#4C72B0", linewidth=2)
ax.set_xlabel("Year")
ax.set_ylabel("Number of Movies")
ax.set_title("Movies in Dataset per Year (1970–2025)")
savefig("11_movies_per_year")

# ── Q12: ROI — which low-budget films earned the most? ───────────────
print("Q12: Top ROI movies")
roi_df = df.dropna(subset=["roi", "budget"]).query("budget > 1e6").nlargest(15, "roi")

fig, ax = plt.subplots(figsize=(12, 6))
bars = ax.barh(roi_df["title"], roi_df["roi"], color=sns.color_palette("YlOrRd_r", len(roi_df)))
ax.set_xlabel("ROI (%)")
ax.set_title("Top 15 Movies by ROI (budget > $1M)")
ax.invert_yaxis()
for i, (val, bud) in enumerate(zip(roi_df["roi"], roi_df["budget"])):
    ax.text(val + 50, i, f"{val:,.0f}% (${bud/1e6:.0f}M budget)", va="center", fontsize=8)
savefig("12_top_roi_movies")

# ── Summary stats ────────────────────────────────────────────────────
print("\n" + "=" * 60)
print("SUMMARY STATISTICS")
print("=" * 60)
print(f"Total movies:          {len(df):,}")
print(f"With budget data:      {df['budget'].notna().sum():,}")
print(f"With revenue data:     {df['revenue'].notna().sum():,}")
print(f"Year range:            {df['release_year'].min():.0f} – {df['release_year'].max():.0f}")
print(f"Avg rating:            {df['vote_average'].mean():.2f}")
print(f"Avg runtime:           {df['runtime'].mean():.0f} min")
print(f"Franchise movies:      {df['is_franchise'].sum():,} ({df['is_franchise'].mean()*100:.1f}%)")
print(f"Unique directors:      {df['director_name'].nunique():,}")
print(f"Unique actors:         {df_cast['actor_name'].nunique():,}")
print(f"\nAll 12 plots saved to plots/ folder.")
print("Done!")
