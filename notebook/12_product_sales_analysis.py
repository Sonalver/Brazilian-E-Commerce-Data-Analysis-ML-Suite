import pandas as pd
import matplotlib.pyplot as plt
from sqlalchemy import create_engine

# Connect to MySQL
engine = create_engine(
    "mysql+pymysql://root:Sonal123@localhost:3306/olist_project?charset=utf8mb4"
)

print("Connected for product analysis")

# --------------------------------
# 1️⃣ Top Selling Product Categories
# --------------------------------
import pandas as pd
from sqlalchemy import create_engine

# Connect to database
engine = create_engine(
    "mysql+pymysql://root:Sonal123@localhost:3306/olist_project?charset=utf8mb4"
)

print("Connected for analysis")
# Load tables
order_items = pd.read_sql(
    "SELECT order_item_id, product_id FROM olist_order_items_dataset",
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

# Fix weird BOM column name
translation.columns = translation.columns.str.replace("ï»¿", "")

# Merge products with translation
products = products.merge(
    translation,
    on="product_category_name",
    how="left"
)

# Merge with order_items
merged = order_items.merge(
    products,
    on="product_id",
    how="left"
)

# Top selling categories
top_categories = (
    merged.groupby("product_category_name_english")["order_item_id"]
    .count()
    .sort_values(ascending=False)
    .head(10)
    .reset_index(name="total_sold")
)

print("\nTop Selling Product Categories:")
print(top_categories)

# Plot
top_categories.set_index("product_category_name_english").plot(
    kind="bar",
    figsize=(10,5),
    legend=False
)

plt.title("Top 10 Selling Product Categories")
plt.ylabel("Items Sold")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
# 2️⃣ Revenue by Category
# --------------------------------
import pandas as pd
import matplotlib.pyplot as plt
from sqlalchemy import create_engine

# Connect to MySQL
engine = create_engine(
"mysql+pymysql://root:Sonal123@localhost:3306/olist_project"
)

print("Connected for product analysis")

# Load tables
order_items = pd.read_sql(
"SELECT order_item_id, product_id, price, freight_value FROM olist_order_items_dataset",
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

# Fix BOM issue
translation.columns = translation.columns.str.replace("ï»¿", "")

# Merge products with translation
products = products.merge(
translation,
on="product_category_name",
how="left"
)

# Merge order_items with products
merged = order_items.merge(
products,
on="product_id",
how="left"
)

# --------------------------------
# 2️⃣ Revenue by Category
# --------------------------------
category_revenue = (
merged.groupby("product_category_name_english")["price"]
.sum()
.sort_values(ascending=False)
.head(10)
.reset_index(name="revenue")
)

print("\nTop Categories by Revenue")
print(category_revenue)

category_revenue.set_index("product_category_name_english").plot(
kind="bar",
figsize=(10,5),
legend=False
)

plt.title("Top 10 Categories by Revenue")
plt.ylabel("Revenue")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# --------------------------------
# 3️⃣ Average Product Price by Category
# --------------------------------
avg_price = (
merged.groupby("product_category_name_english")["price"]
.mean()
.sort_values(ascending=False)
.head(10)
.reset_index(name="avg_price")
)

print("\nAverage Product Price by Category")
print(avg_price)

# --------------------------------
# 4️⃣ Top Products by Revenue
# --------------------------------
top_products = (
merged.groupby("product_id")["price"]
.sum()
.sort_values(ascending=False)
.head(10)
.reset_index(name="total_revenue")
)

print("\nTop Products by Revenue")
print(top_products)

# --------------------------------
# 5️⃣ Product Price vs Freight Cost
# --------------------------------
print("\nAverage Price vs Freight Cost")

price_vs_freight = merged[["price","freight_value"]].mean()
print(price_vs_freight)

# Scatter plot
merged.plot.scatter(
x="price",
y="freight_value",
figsize=(6,4)
)

plt.title("Product Price vs Freight Cost")
plt.tight_layout()
plt.show()

#Category Profitability Analysis
# Category Profitability
merged["profit"] = merged["price"] - merged["freight_value"]

category_profit = (
    merged.groupby("product_category_name_english")["profit"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .reset_index(name="total_profit")
)

print("\nTop Categories by Profit")
print(category_profit)

category_profit.set_index("product_category_name_english").plot(
    kind="bar",
    figsize=(10,5),
    legend=False
)

plt.title("Top 10 Product Categories by Profit")
plt.ylabel("Profit")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

#Category Shipping Burden Analysis
merged["shipping_ratio"] = merged["freight_value"] / merged["price"]

shipping_cost_analysis = (
    merged.groupby("product_category_name_english")["shipping_ratio"]
    .mean()
    .sort_values(ascending=False)
    .head(10)
    .reset_index(name="avg_shipping_ratio")
)

print("\nCategories with Highest Shipping Cost Ratio")
print(shipping_cost_analysis)

#Product Concentration (Pareto Analysis)
product_revenue = (
    merged.groupby("product_id")["price"]
    .sum()
    .sort_values(ascending=False)
    .reset_index(name="revenue")
)

product_revenue["cumulative_revenue"] = product_revenue["revenue"].cumsum()
product_revenue["revenue_share"] = (
    product_revenue["cumulative_revenue"] /
    product_revenue["revenue"].sum()
)

print("\nTop Products Revenue Distribution")
print(product_revenue.head(10))

#Product Category Demand vs Price
price_demand = (
    merged.groupby("product_category_name_english")
    .agg(avg_price=("price","mean"),
         total_sales=("order_item_id","count"))
    .reset_index()
)

print(price_demand.head())
#chart
price_demand.plot.scatter(
    x="avg_price",
    y="total_sales",
    figsize=(6,4)
)

plt.title("Price vs Demand by Category")
plt.tight_layout()
plt.show()