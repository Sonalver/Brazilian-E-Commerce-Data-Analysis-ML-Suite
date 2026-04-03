import pandas as pd
from sqlalchemy import create_engine
import matplotlib.pyplot as plt

# Connect to DB
engine = create_engine("mysql+pymysql://root:Sonal123@localhost:3306/olist_project")


# 2. Load Aggregated Data (from DB)
# -----------------------------
query = """
SELECT
    product_category_name,
    revenue
FROM category_revenue_summary
ORDER BY revenue DESC
"""

df = pd.read_sql(query, engine)

# -----------------------------
# 3. Load Translation CSV (FIX BOM here)
# -----------------------------
translation_df = pd.read_csv("C:/Users/sonal/olist_sql_project/data/product_category_name_translation.csv",
    encoding="utf-8-sig"
)

# Clean column names (extra safety)
translation_df.columns = translation_df.columns.str.strip()

# -----------------------------
# 4. Merge (Python instead of SQL)
# -----------------------------
df = df.merge(
    translation_df,
    on="product_category_name",
    how="left"
)

# -----------------------------
# 5. Clean Category Names
# -----------------------------
df["category"] = df["product_category_name_english"].fillna("Unknown")
df["category"] = df["category"].str.replace("_", " ")

# -----------------------------
# 6. Pareto Calculation
# -----------------------------
df["cumulative_revenue"] = df["revenue"].cumsum()
total_revenue = df["revenue"].sum()

df["cumulative_percentage"] = df["cumulative_revenue"] / total_revenue

# Top 80%
top_80 = df[df["cumulative_percentage"] <= 0.8]

# -----------------------------
# 7. Visualization (Professional Pareto Chart)
# -----------------------------
fig, ax1 = plt.subplots(figsize=(14,7))

# Bar chart
ax1.bar(df["category"], df["revenue"])
ax1.set_ylabel("Revenue")
ax1.set_xlabel("Product Category")
ax1.set_xticklabels(df["category"], rotation=90)

# Cumulative line
ax2 = ax1.twinx()
ax2.plot(df["cumulative_percentage"].values)
ax2.set_ylabel("Cumulative Percentage")

# 80% line
ax2.axhline(y=0.8, linestyle="--")

plt.title("Pareto Analysis - Revenue Contribution by Category")
plt.tight_layout()
plt.show()

# -----------------------------
# 8. Business Insights
# -----------------------------
print("\n--- BUSINESS INSIGHTS ---\n")

print(f"Total Categories: {len(df)}")
print(f"Top {len(top_80)} categories contribute ~80% of revenue")

print("\nTop 5 Revenue-Driving Categories:")
for cat in top_80["category"].head(5):
    print(f"- {cat}")

print("\nInsight:")
print("A small number of product categories drive the majority of revenue.")
print("Focus marketing, inventory, and pricing strategies on these categories.")