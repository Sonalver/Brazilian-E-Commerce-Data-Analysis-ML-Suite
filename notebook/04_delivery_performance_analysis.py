import pandas as pd
from sqlalchemy import create_engine
import matplotlib.pyplot as plt
#Connect to Database
engine = create_engine("mysql+pymysql://root:Sonal123@localhost:3306/olist_project")
print("Connected for analysis")

engine = create_engine(
"mysql+pymysql://root:Sonal123@localhost:3306/olist_project?charset=utf8mb4"
)
#Average Delivery Time (Customer Perspective)
query = """
SELECT 
ROUND(AVG(DATEDIFF(order_delivered_customer_date, order_purchase_timestamp)),2)
AS avg_delivery_days
FROM orders
WHERE order_status = 'delivered';
"""
pd.read_sql(query, engine)

#Shipping Time (Seller → Carrier Handover Speed)
query = """
SELECT 
ROUND(AVG(DATEDIFF(order_delivered_carrier_date, order_purchase_timestamp)),2)
AS avg_shipping_days
FROM orders
WHERE order_status = 'delivered';
"""
pd.read_sql(query, engine)

#Carrier Delivery Time (Logistics Performance)
query = """
SELECT 
ROUND(AVG(DATEDIFF(order_delivered_customer_date, order_delivered_carrier_date)),2)
AS avg_carrier_delivery_days
FROM orders
WHERE order_status = 'delivered';
"""
pd.read_sql(query, engine)

#Early / On-Time / Late Deliveries
query = """
SELECT 
CASE 
WHEN order_delivered_customer_date < order_estimated_delivery_date THEN 'Early'
WHEN order_delivered_customer_date = order_estimated_delivery_date THEN 'On Time'
ELSE 'Late'
END AS delivery_status,
COUNT(*) AS total_orders
FROM orders
WHERE order_status = 'delivered'
GROUP BY delivery_status;
"""
delivery_status = pd.read_sql(query, engine)
print(delivery_status)
#Chart
delivery_status.set_index("delivery_status").plot(
    kind="bar", figsize=(7,4), legend=False
)
plt.title("Delivery Performance")
plt.ylabel("Total Orders")
plt.xticks(rotation=0)
plt.show()

#Late Delivery Rate
query = """
SELECT 
ROUND(
SUM(CASE 
WHEN order_delivered_customer_date > order_estimated_delivery_date 
THEN 1 ELSE 0 END)
/ COUNT(*) * 100,2
) AS late_delivery_rate
FROM orders
WHERE order_status = 'delivered';
"""
pd.read_sql(query, engine)

#State-Wise Average Delivery Time
query = """
SELECT 
c.customer_state,
ROUND(AVG(DATEDIFF(o.order_delivered_customer_date, 
o.order_purchase_timestamp)),2) AS avg_delivery_days
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id
WHERE o.order_status = 'delivered'
GROUP BY c.customer_state
ORDER BY avg_delivery_days;
"""
state_delivery = pd.read_sql(query, engine)
print(state_delivery)

#Monthly Delivery Time Trend
query = """
SELECT 
DATE_FORMAT(order_purchase_timestamp,'%%Y-%%m') AS month,
ROUND(AVG(DATEDIFF(order_delivered_customer_date, 
order_purchase_timestamp)),2) AS avg_delivery_days
FROM orders
WHERE order_status = 'delivered'
GROUP BY month
ORDER BY month;
"""
monthly_delivery = pd.read_sql(query, engine)
print(monthly_delivery)
#Chart
monthly_delivery.plot(
    x="month", y="avg_delivery_days",
    kind="line", marker='o', figsize=(10,5)
)

plt.title("Monthly Avg Delivery Time")
plt.xticks(rotation=45)
plt.show()

#Delivery delay distribution
query = """
SELECT 
DATEDIFF(order_delivered_customer_date, order_estimated_delivery_date) 
AS delay_days,
COUNT(*) AS total_orders
FROM orders
WHERE order_status = 'delivered'
GROUP BY delay_days
ORDER BY delay_days;
"""

delay_distribution = pd.read_sql(query, engine)
print(delay_distribution.head())
# Chart
delay_distribution.plot(
    x="delay_days",
    y="total_orders",
    kind="bar",
    figsize=(10,5)
)
plt.title("Delivery Delay Distribution")
plt.xlabel("Delay Days (Negative = Early)")
plt.ylabel("Number of Orders")
plt.show()

#State-wise late delivery rate
query = """
SELECT 
c.customer_state,

ROUND(
SUM(CASE 
WHEN o.order_delivered_customer_date > o.order_estimated_delivery_date
THEN 1 ELSE 0 END) / COUNT(*) * 100,2
) AS late_delivery_rate

FROM orders o
JOIN customers c 
ON o.customer_id = c.customer_id

WHERE o.order_status = 'delivered'

GROUP BY c.customer_state
ORDER BY late_delivery_rate DESC;
"""

state_late = pd.read_sql(query, engine)

print(state_late)
# Chart
state_late.plot(
    x="customer_state",
    y="late_delivery_rate",
    kind="bar",
    figsize=(10,5)
)

plt.title("Late Delivery Rate by State")
plt.ylabel("Late Delivery %")
plt.xticks(rotation=45)
plt.show()

#Seller processing time
query = """
SELECT 
ROUND(AVG(
DATEDIFF(order_delivered_carrier_date, order_purchase_timestamp)
),2) AS avg_seller_processing_days

FROM orders
WHERE order_status = 'delivered';
"""

seller_processing = pd.read_sql(query, engine)

print("Average Seller Processing Time:")
print(seller_processing)

#Estimated vs actual delivery time
query = """
SELECT 

ROUND(
AVG(DATEDIFF(order_estimated_delivery_date, order_purchase_timestamp)),2
) AS estimated_days,

ROUND(
AVG(DATEDIFF(order_delivered_customer_date, order_purchase_timestamp)),2
) AS actual_days

FROM orders
WHERE order_status = 'delivered';
"""

delivery_compare = pd.read_sql(query, engine)

print("Estimated vs Actual Delivery Time")
print(delivery_compare)

#Monthly late delivery trend
query = """
SELECT 

DATE_FORMAT(order_purchase_timestamp,'%%Y-%%m') AS month,

ROUND(
SUM(CASE 
WHEN order_delivered_customer_date > order_estimated_delivery_date
THEN 1 ELSE 0 END) / COUNT(*) * 100,2
) AS late_delivery_rate

FROM orders
WHERE order_status = 'delivered'

GROUP BY month
ORDER BY month;
"""

monthly_late = pd.read_sql(query, engine)
print(monthly_late)

# Chart
monthly_late.plot(
    x="month",
    y="late_delivery_rate",
    kind="line",
    marker='o',
    figsize=(10,5)
)

plt.title("Monthly Late Delivery Trend")
plt.xlabel("Month")
plt.ylabel("Late Delivery %")
plt.xticks(rotation=45)
plt.show()