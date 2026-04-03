import pandas as pd
import matplotlib.pyplot as plt
from sqlalchemy import create_engine


# Database connection
engine = create_engine("mysql+pymysql://root:Sonal123@localhost:3306/olist_project")

#Total Customers
query = """
SELECT COUNT(DISTINCT customer_unique_id) AS total_customers
FROM customers;
"""
total_customers = pd.read_sql(query, engine)
print("Total Customers:")
print(total_customers)

#Customers by State
query = """
SELECT
customer_state,
COUNT(DISTINCT customer_unique_id) AS total_customers
FROM customers
GROUP BY customer_state
ORDER BY total_customers DESC;
"""
customers_state = pd.read_sql(query, engine)
print(customers_state)
#chart
customers_state.head(10).set_index("customer_state").plot(
    kind="bar", figsize=(8,4), legend=False
)

plt.title("Top 10 States by Number of Customers")
plt.ylabel("Customers")
plt.xticks(rotation=45)
plt.show()

#Repeat Purchase Rate
query = """
SELECT
ROUND(
SUM(CASE WHEN order_count > 1 THEN 1 ELSE 0 END)*100.0
/ COUNT(*),2
) AS repeat_purchase_rate
FROM (
SELECT
c.customer_unique_id,
COUNT(o.order_id) AS order_count
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
WHERE o.order_status='delivered'
GROUP BY c.customer_unique_id
) t;
"""
repeat_rate = pd.read_sql(query, engine)
print("Repeat Purchase Rate:")
print(repeat_rate)

#Orders per Customer
query = """
SELECT
c.customer_unique_id,
COUNT(o.order_id) AS total_orders
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
WHERE o.order_status='delivered'
GROUP BY c.customer_unique_id
ORDER BY total_orders DESC
LIMIT 10;
"""
top_customers = pd.read_sql(query, engine)
print(top_customers)

#Revenue per Customer
query = """
SELECT
c.customer_unique_id,
ROUND(SUM(p.payment_value),2) AS customer_revenue
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
JOIN order_payments p ON o.order_id = p.order_id
WHERE o.order_status='delivered'
GROUP BY c.customer_unique_id
ORDER BY customer_revenue DESC
LIMIT 10;
"""
top_revenue_customers = pd.read_sql(query, engine)
print(top_revenue_customers)

#Average Revenue per Customer (ARPU)
query = """
SELECT
ROUND(SUM(p.payment_value) /
COUNT(DISTINCT c.customer_unique_id),2) AS avg_revenue_per_customer
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
JOIN order_payments p ON o.order_id = p.order_id
WHERE o.order_status='delivered';
"""
arpu = pd.read_sql(query, engine)
print("Average Revenue per Customer:")
print(arpu)

#New Customers by Month
query = """
SELECT
DATE_FORMAT(o.order_purchase_timestamp,'%%Y-%%m') AS month,
COUNT(DISTINCT c.customer_unique_id) AS new_customers
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
WHERE o.order_status='delivered'
GROUP BY month
ORDER BY month;
"""
monthly_customers = pd.read_sql(query, engine)
print(monthly_customers)
#Chart
plt.figure(figsize=(10,5))

plt.plot(
    monthly_customers["month"],
    monthly_customers["new_customers"],
    marker='o'
)

plt.title("New Customers by Month")
plt.xlabel("Month")
plt.ylabel("Customers")
plt.xticks(rotation=45)
plt.grid(True)

plt.show()


#Customer Lifetime Value (CLV)
# Customer Lifetime Value
query = """
SELECT
c.customer_unique_id,
ROUND(SUM(p.payment_value),2) AS lifetime_value,
COUNT(DISTINCT o.order_id) AS total_orders
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
JOIN order_payments p ON o.order_id = p.order_id
WHERE o.order_status='delivered'
GROUP BY c.customer_unique_id
ORDER BY lifetime_value DESC
LIMIT 10;
"""

clv = pd.read_sql(query, engine)

print("\nTop Customers by Lifetime Value")
print(clv)

clv.set_index("customer_unique_id").plot(
    kind="bar", figsize=(8,4), legend=False
)

plt.title("Top Customers by Lifetime Value")
plt.ylabel("Revenue")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

#Customer Retention Rate
query = """
SELECT
ROUND(
COUNT(DISTINCT CASE WHEN order_count > 1 THEN customer_unique_id END)
/ COUNT(DISTINCT customer_unique_id) * 100,2
) AS retention_rate
FROM (
SELECT
c.customer_unique_id,
COUNT(o.order_id) AS order_count
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.customer_unique_id
) t;
"""

retention = pd.read_sql(query, engine)

print("\nCustomer Retention Rate (%)")
print(retention)

#Revenue by State (Pareto Insight)
query = """
SELECT
c.customer_state,
ROUND(SUM(p.payment_value),2) AS revenue
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
JOIN order_payments p ON o.order_id = p.order_id
WHERE o.order_status='delivered'
GROUP BY c.customer_state
ORDER BY revenue DESC;
"""

state_revenue = pd.read_sql(query, engine)

print("\nRevenue by State")
print(state_revenue)

state_revenue.head(10).set_index("customer_state").plot(
    kind="bar", figsize=(8,4), legend=False
)

plt.title("Top States by Revenue")
plt.ylabel("Revenue")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

#Average Orders per Customer
query = """
SELECT
ROUND(
COUNT(o.order_id) /
COUNT(DISTINCT c.customer_unique_id),2
) AS avg_orders_per_customer
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
WHERE o.order_status='delivered';
"""

avg_orders = pd.read_sql(query, engine)

print("\nAverage Orders per Customer")
print(avg_orders)

#Customer Segmentation
query = """
SELECT
CASE
WHEN order_count = 1 THEN 'One-time'
WHEN order_count BETWEEN 2 AND 5 THEN 'Occasional'
ELSE 'Loyal'
END AS customer_type,
COUNT(*) AS total_customers
FROM (
SELECT
c.customer_unique_id,
COUNT(o.order_id) AS order_count
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.customer_unique_id
) t
GROUP BY customer_type;
"""

segments = pd.read_sql(query, engine)

print("\nCustomer Segmentation")
print(segments)

segments.set_index("customer_type").plot(
    kind="bar", figsize=(6,4), legend=False
)

plt.title("Customer Segmentation")
plt.ylabel("Customers")
plt.xticks(rotation=0)
plt.tight_layout()
plt.show()