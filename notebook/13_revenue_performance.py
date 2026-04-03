import pandas as pd
import matplotlib.pyplot as plt
from sqlalchemy import create_engine

# -----------------------------
# DB CONNECTION
# -----------------------------
engine = create_engine(
"mysql+pymysql://root:Sonal123@localhost:3306/olist_project"
)

print("Connected to optimized database")

# -----------------------------
# CATEGORY REVENUE
# -----------------------------
query = """
SELECT * 
FROM category_revenue_summary
ORDER BY revenue DESC
LIMIT 10;
"""

top_categories = pd.read_sql(query, engine)
print("\nTop Categories:")
print(top_categories)

# Bar Chart
plt.figure(figsize=(10,6))
plt.barh(
    top_categories["product_category_name"],
    top_categories["revenue"]
)

plt.title("Top Product Categories by Revenue")
plt.xlabel("Revenue")
plt.ylabel("Category")
plt.gca().invert_yaxis()

plt.show()


# -----------------------------
# MONTHLY SALES
# -----------------------------
query = """
SELECT * 
FROM monthly_sales_summary
ORDER BY month;
"""

monthly = pd.read_sql(query, engine)

# Convert date
monthly["month"] = pd.to_datetime(monthly["month"])

print("\nMonthly Sales:")
print(monthly)

# -----------------------------
# MONTHLY TREND PLOT (FIXED)
# -----------------------------
fig, ax1 = plt.subplots(figsize=(12,6))

# Revenue (left axis)
ax1.plot(
    monthly["month"],
    monthly["revenue"],
    marker='o'
)
ax1.set_ylabel("Revenue")

# Orders (right axis)
ax2 = ax1.twinx()
ax2.plot(
    monthly["month"],
    monthly["total_orders"],
    marker='s',
    linestyle='--'
)
ax2.set_ylabel("Orders")

# Common settings
ax1.set_title("Monthly Orders & Revenue (Dual Axis)")
ax1.set_xlabel("Month")

plt.xticks(rotation=45)
plt.grid(True)
plt.tight_layout()

plt.show()



# -----------------------------
# REVENUE GROWTH %
# -----------------------------
monthly["growth_%"] = (
monthly["revenue"].pct_change() * 100
).round(2)

print("\nRevenue Growth:")
print(monthly)

# Growth Chart
plt.figure(figsize=(10,5))

plt.plot(
    monthly["month"],
    monthly["growth_%"],
    marker='o'
)

plt.axhline(0, linestyle='--')
plt.title("Revenue Growth % (MoM)")
plt.xlabel("Month")
plt.ylabel("Growth %")

plt.show()


print("\nFAST ANALYTICS COMPLETED")



