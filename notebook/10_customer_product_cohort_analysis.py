import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sqlalchemy import create_engine

# -----------------------------
# DB CONNECTION
# -----------------------------
engine = create_engine(
    "mysql+pymysql://root:Sonal123@localhost:3306/olist_project?charset=utf8mb4"
)

print("Connected for analysis")

# -----------------------------
# LOAD DATA
# -----------------------------
customers = pd.read_sql(
    "SELECT customer_id, customer_unique_id FROM olist_customers_dataset",
    engine
)

orders = pd.read_sql(
    "SELECT order_id, customer_id, order_purchase_timestamp FROM orders",
    engine
)

order_items = pd.read_sql(
    "SELECT order_id, product_id FROM olist_order_items_dataset",
    engine
)

products = pd.read_sql(
    "SELECT product_id, product_category_name FROM olist_products_dataset",
    engine
)

translation = pd.read_sql(
    "SELECT * FROM product_category_name_translation",
    engine
)

# Fix encoding issue
translation.columns = translation.columns.str.replace("ï»¿", "")

# -----------------------------
# MERGE DATA
# -----------------------------
merged = orders.merge(customers, on="customer_id", how="left")

merged = merged.merge(order_items, on="order_id", how="left")

merged = merged.merge(products, on="product_id", how="left")

merged = merged.merge(
    translation,
    on="product_category_name",
    how="left"
)

print("Data merged successfully")

# -----------------------------
# DATE PROCESSING
# -----------------------------
merged["order_purchase_timestamp"] = pd.to_datetime(
    merged["order_purchase_timestamp"]
)

merged["order_month"] = merged["order_purchase_timestamp"].dt.to_period("M")

# -----------------------------
# COHORT CREATION
# -----------------------------
merged["cohort_month"] = merged.groupby(
    "customer_unique_id"
)["order_month"].transform("min")

# Convert to string for plotting
merged["order_month"] = merged["order_month"].astype(str)
merged["cohort_month"] = merged["cohort_month"].astype(str)

# -----------------------------
# COHORT MATRIX
# -----------------------------
cohort_data = (
    merged.groupby(["cohort_month", "order_month"])
    ["customer_unique_id"]
    .nunique()
    .reset_index()
)

cohort_matrix = cohort_data.pivot(
    index="cohort_month",
    columns="order_month",
    values="customer_unique_id"
)

print("\nCohort Matrix:")
print(cohort_matrix)

# -----------------------------
# RETENTION CALCULATION
# -----------------------------
cohort_size = cohort_matrix.iloc[:, 0]

retention = cohort_matrix.divide(cohort_size, axis=0)

print("\nRetention Matrix:")
print(retention)

# -----------------------------
# HEATMAP VISUALIZATION
# -----------------------------
plt.figure(figsize=(12, 7))

sns.heatmap(
    retention,
    annot=True,
    fmt=".0%",
    cmap="Blues",
    linewidths=0.5
)

plt.title("Customer Retention Cohort Analysis")
plt.ylabel("Cohort Month")
plt.xlabel("Months After First Purchase")

plt.tight_layout()
plt.show()

# -----------------------------
# RETENTION TREND
# -----------------------------
retention.mean().plot(figsize=(10,5), marker='o')

plt.title("Average Retention Over Time")
plt.xlabel("Months")
plt.ylabel("Retention Rate")

plt.grid(True)
plt.show()

# -----------------------------
# CHURN ANALYSIS
# -----------------------------
churn = 1 - retention

print("\nChurn Matrix:")
print(churn)

# -----------------------------
# BUSINESS INSIGHTS
# -----------------------------
print("\nINSIGHTS:")
print("1. First month retention is always 100% (new users).")
print("2. Retention drops after first purchase → users are not returning.")
print("3. Strong retention in early months = good onboarding.")
print("4. Rapid drop = need re-engagement strategies (offers, email marketing).")

print("\nCOHORT ANALYSIS COMPLETED")