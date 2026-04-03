import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sqlalchemy import create_engine

# Connect to MySQL
engine = create_engine(
    "mysql+pymysql://root:Sonal123@localhost:3306/olist_project"
)

print("Connected for cohort analysis")

# Load tables
customers = pd.read_sql(
    "SELECT customer_id, customer_unique_id FROM customers",
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

# Fix BOM issue in translation table
translation.columns = translation.columns.str.replace("ï»¿", "")

# Merge products with category translation
products = products.merge(
    translation,
    on="product_category_name",
    how="left"
)

# Merge orders with customers
orders_customers = orders.merge(
    customers,
    on="customer_id",
    how="left"
)

# Merge order items with products
orders_products = order_items.merge(
    products,
    on="product_id",
    how="left"
)

# Final merge
merged = orders_customers.merge(
    orders_products,
    on="order_id",
    how="left"
)

# Convert to datetime
merged["order_purchase_timestamp"] = pd.to_datetime(
    merged["order_purchase_timestamp"]
)

# Create month column
merged["order_month"] = merged["order_purchase_timestamp"].dt.to_period("M")

# Find first purchase month (cohort)
merged["cohort_month"] = merged.groupby(
    "customer_unique_id"
)["order_month"].transform("min")

# Cohort grouping
cohort_data = (
    merged.groupby(["cohort_month", "order_month"])["customer_unique_id"]
    .nunique()
    .reset_index()
)

# Pivot table
cohort_matrix = cohort_data.pivot(
    index="cohort_month",
    columns="order_month",
    values="customer_unique_id"
)

# Calculate retention
cohort_size = cohort_matrix.iloc[:, 0]

retention = cohort_matrix.divide(cohort_size, axis=0)

print("\nCustomer Cohort Retention Matrix")
print(retention)

# Heatmap visualization
plt.figure(figsize=(10,6))

sns.heatmap(
    retention,
    annot=True,
    fmt=".0%",
    cmap="Blues"
)

plt.title("Customer Retention Cohort Analysis")
plt.tight_layout()
plt.show()