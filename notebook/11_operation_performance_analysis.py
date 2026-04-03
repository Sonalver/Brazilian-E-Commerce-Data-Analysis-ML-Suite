import pandas as pd
import matplotlib.pyplot as plt
from sqlalchemy import create_engine

engine = create_engine("mysql+pymysql://root:Sonal123@localhost:3306/olist_project")

#Order Status Distribution
query = """
SELECT order_status, COUNT(*) AS total_orders
FROM orders
GROUP BY order_status
ORDER BY total_orders DESC;
"""
order_status = pd.read_sql(query, engine)

print("Order Status Distribution:")
print(order_status)

#Cancellation Rate
query = """
SELECT 
ROUND(
SUM(CASE WHEN order_status = 'canceled' THEN 1 ELSE 0 END)
/
COUNT(*) * 100, 2
) AS cancellation_rate
FROM orders;
"""
cancellation_rate = pd.read_sql(query, engine)

print("Cancellation Rate (%):")
print(cancellation_rate)

#Delivery Success Rate
query = """
SELECT 
ROUND(
SUM(CASE WHEN order_status = 'delivered' THEN 1 ELSE 0 END)
/
COUNT(*) * 100, 2
) AS delivery_success_rate
FROM orders;
"""
delivery_rate = pd.read_sql(query, engine)

print("Delivery Success Rate (%):")
print(delivery_rate)

#Visualize Order Status
order_status.set_index("order_status").plot(
    kind="bar",
    figsize=(8,5),
    legend=False
)

plt.title("Order Status Distribution")
plt.ylabel("Total Orders")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

#On-Time Delivery Rate
query = """
SELECT
CASE
WHEN order_delivered_customer_date > order_estimated_delivery_date
THEN 'Late'
ELSE 'On Time'
END AS delivery_status,
COUNT(*) AS total_orders
FROM orders
WHERE order_status='delivered'
GROUP BY delivery_status;
"""

delivery_status = pd.read_sql(query, engine)
print(delivery_status)
#Chart
delivery_status.set_index("delivery_status").plot(
    kind="bar",
    figsize=(6,4),
    legend=False
)

plt.title("On-Time vs Late Deliveries")
plt.ylabel("Number of Orders")
plt.xticks(rotation=0)
plt.tight_layout()
plt.show()

#Average Delivery Time
query = """
SELECT
ROUND(AVG(
DATEDIFF(order_delivered_customer_date,
order_purchase_timestamp)
),2) AS avg_delivery_days
FROM orders
WHERE order_status='delivered';
"""

avg_delivery_time = pd.read_sql(query, engine)
print("Average Delivery Time (Days)")
print(avg_delivery_time)

#Average Delivery Delay
query = """
SELECT
ROUND(AVG(
DATEDIFF(order_delivered_customer_date,
order_estimated_delivery_date)
),2) AS avg_delay_days
FROM orders
WHERE order_status='delivered'
AND order_delivered_customer_date > order_estimated_delivery_date;
"""

delay = pd.read_sql(query, engine)
print("Average Delay for Late Deliveries")
print(delay)

#On-Time vs Delayed Orders
query = """
SELECT 
CASE 
WHEN order_delivered_customer_date <= order_estimated_delivery_date 
THEN 'On Time'
ELSE 'Delayed'
END AS delivery_status,
COUNT(*) AS total_orders
FROM orders
WHERE order_status = 'delivered'
GROUP BY delivery_status;
"""
delivery_status = pd.read_sql(query, engine)

print("On-Time vs Delayed Orders:")
print(delivery_status)

#Visualization
delivery_status.set_index("delivery_status").plot(
    kind="bar",
    legend=False,
    figsize=(6,4)
)

plt.title("On-Time vs Delayed Deliveries")
plt.ylabel("Total Orders")
plt.xticks(rotation=0)
plt.tight_layout()
plt.show()

#Impact on Revenue
query = """
SELECT 
CASE 
WHEN o.order_delivered_customer_date <= o.order_estimated_delivery_date 
THEN 'On Time'
ELSE 'Delayed'
END AS delivery_status,
ROUND(SUM(p.payment_value),2) AS revenue
FROM orders o
JOIN order_payments p 
ON o.order_id = p.order_id
WHERE o.order_status = 'delivered'
GROUP BY delivery_status;
"""
revenue_impact = pd.read_sql(query, engine)

print("Revenue Impact by Delivery Performance:")
print(revenue_impact)

#Chart for Revenue Impact
revenue_impact.set_index("delivery_status").plot(
    kind="bar",
    legend=False,
    figsize=(6,4)
)

plt.title("Revenue: On-Time vs Delayed")
plt.ylabel("Revenue")
plt.xticks(rotation=0)
plt.tight_layout()
plt.show()

#Order Fulfillment Time
query = """
SELECT
ROUND(AVG(
DATEDIFF(order_delivered_carrier_date,
order_purchase_timestamp)
),2) AS avg_fulfillment_days
FROM orders
WHERE order_status='delivered'
AND order_delivered_carrier_date IS NOT NULL;
"""

fulfillment = pd.read_sql(query, engine)
print("Average Fulfillment Time")
print(fulfillment)

#Freight Cost per Order
query = """
SELECT
ROUND(AVG(freight_value),2) AS avg_freight_cost
FROM olist_order_items_dataset;
"""

freight = pd.read_sql(query, engine)
print("Average Freight Cost")
print(freight)

#Freight Cost vs Product Price
query = """
SELECT
ROUND(AVG(price),2) AS avg_product_price,
ROUND(AVG(freight_value),2) AS avg_freight_cost
FROM olist_order_items_dataset;
"""

cost_comparison = pd.read_sql(query, engine)
print(cost_comparison)

#Top States with Highest Delivery Time
query = """
SELECT
c.customer_state,
ROUND(AVG(
DATEDIFF(o.order_delivered_customer_date,
o.order_purchase_timestamp)
),2) AS avg_delivery_days
FROM orders o
JOIN customers c
ON o.customer_id = c.customer_id
WHERE o.order_status='delivered'
GROUP BY c.customer_state
ORDER BY avg_delivery_days DESC
LIMIT 10;
"""

slow_states = pd.read_sql(query, engine)
print(slow_states)
#Chart
slow_states.set_index("customer_state").plot(
    kind="bar",
    figsize=(8,4),
    legend=False
)

plt.title("States with Slowest Deliveries")
plt.ylabel("Avg Delivery Days")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

#Delivery Performance vs Customer Reviews
query = """
SELECT
CASE
WHEN o.order_delivered_customer_date > o.order_estimated_delivery_date
THEN 'Late'
ELSE 'On Time'
END AS delivery_status,
ROUND(AVG(r.review_score),2) AS avg_review
FROM orders o
JOIN olist_order_reviews_dataset r
ON o.order_id = r.order_id
WHERE o.order_status='delivered'
GROUP BY delivery_status;
"""

delivery_review = pd.read_sql(query, engine)
print(delivery_review)

#Freight Cost Ratio
query = """
SELECT
ROUND(AVG(freight_value / price) * 100,2) AS freight_percentage
FROM olist_order_items_dataset;
"""

freight_ratio = pd.read_sql(query, engine)

print("Freight Cost as % of Product Price")
print(freight_ratio)

#Add Monthly Delivery Trend
query = """
SELECT
DATE_FORMAT(order_purchase_timestamp,'%%Y-%%m') AS month,
ROUND(AVG(DATEDIFF(order_delivered_customer_date,
order_purchase_timestamp)),2) AS avg_delivery_days
FROM orders
WHERE order_status='delivered'
GROUP BY month
ORDER BY month;
"""

monthly_delivery = pd.read_sql(query, engine)

monthly_delivery.plot(
x="month",
y="avg_delivery_days",
kind="line",
marker="o",
figsize=(10,5)
)

plt.title("Monthly Delivery Time Trend")
plt.ylabel("Days")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()