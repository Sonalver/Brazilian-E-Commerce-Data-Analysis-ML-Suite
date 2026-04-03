import pandas as pd
import matplotlib.pyplot as plt
from sqlalchemy import create_engine

engine = create_engine("mysql+pymysql://root:Sonal123@localhost:3306/olist_project")

#Total Revenue
query = """
SELECT ROUND(SUM(payment_value),2) AS total_revenue
FROM order_payments;
"""

print(pd.read_sql(query, engine))

#Total Revenue (Delivered Orders Only)
query = """
SELECT 
    ROUND(SUM(p.payment_value),2) AS total_revenue
FROM orders o
JOIN order_payments p 
    ON o.order_id = p.order_id
WHERE o.order_status = 'delivered';
"""

total_revenue = pd.read_sql(query, engine)
print("Total Revenue:")
print(total_revenue)

#Total orders
query = "SELECT COUNT(*) AS total_orders FROM orders;"
print(pd.read_sql(query, engine))

#Total Orders (Delivered)
query = """
SELECT COUNT(*) AS total_orders
FROM orders
WHERE order_status = 'delivered';
"""

total_orders = pd.read_sql(query, engine)
print("Total Delivered Orders:")
print(total_orders)

# Monthly Order Trend
query = """
SELECT 
DATE_FORMAT(order_purchase_timestamp,'%%Y-%%m') AS month,
COUNT(order_id) AS total_orders
FROM orders
GROUP BY month
ORDER BY month;
"""

monthly_orders = pd.read_sql(query, engine)

print(monthly_orders)

#chart
import matplotlib.pyplot as plt

plt.figure(figsize=(12,6))

plt.plot(
    monthly_orders["month"],
    monthly_orders["total_orders"],
    marker='o'
)

plt.title("Monthly Order Trend", fontsize=14)
plt.xlabel("Month")
plt.ylabel("Total Orders")
plt.xticks(rotation=45)
plt.grid(True)

plt.tight_layout()
plt.show()

#Month-wise Revenue Trend
query = """
SELECT 
DATE_FORMAT(o.order_purchase_timestamp,'%%Y-%%m') AS month,
ROUND(SUM(p.payment_value),2) AS revenue
FROM orders o
JOIN order_payments p 
ON o.order_id = p.order_id
WHERE o.order_status = 'delivered'
GROUP BY month
ORDER BY month;
"""

monthly_revenue = pd.read_sql(query, engine)

print("Month-wise Revenue:")
print(monthly_revenue)

##Convert Month Column → Datetime
monthly_revenue["month"] = pd.to_datetime(monthly_revenue["month"])

#Visualization
import matplotlib.pyplot as plt

plt.figure(figsize=(12,6))

plt.plot(
    monthly_revenue["month"],
    monthly_revenue["revenue"],
    marker='o'
)

plt.title("Month-wise Revenue Trend", fontsize=14)
plt.xlabel("Month")
plt.ylabel("Revenue")
plt.xticks(rotation=45)
plt.grid(True)

plt.tight_layout()
plt.show()

#Revenue Growth %
monthly_revenue["revenue_growth_%"] = (
    monthly_revenue["revenue"].pct_change() * 100
).round(2)

print(monthly_revenue)

#Monthly Orders + Revenue Together
query = """
SELECT 
DATE_FORMAT(o.order_purchase_timestamp,'%%Y-%%m') AS month,
COUNT(DISTINCT o.order_id) AS total_orders,
ROUND(SUM(p.payment_value),2) AS revenue
FROM orders o
JOIN order_payments p 
ON o.order_id = p.order_id
WHERE o.order_status = 'delivered'
GROUP BY month
ORDER BY month;
"""

monthly_trend = pd.read_sql(query, engine)

print(monthly_trend)
#monthly_trend["month"] = pd.to_datetime(monthly_trend["month"])
monthly_trend["month"] = pd.to_datetime(monthly_trend["month"])

#Dual-Axis Visualization
import matplotlib.pyplot as plt

fig, ax1 = plt.subplots(figsize=(12,6))

# Orders line
ax1.plot(
    monthly_trend["month"],
    monthly_trend["total_orders"],
    marker='o',
    label="Total Orders"
)
ax1.set_ylabel("Total Orders")

# Revenue line
ax2 = ax1.twinx()
ax2.plot(
    monthly_trend["month"],
    monthly_trend["revenue"],
    marker='s',
    linestyle='--',
    label="Revenue"
)
ax2.set_ylabel("Revenue")

# Title & formatting
plt.title("Monthly Orders vs Revenue Trend", fontsize=14)
ax1.set_xlabel("Month")
ax1.tick_params(axis='x', rotation=45)

fig.tight_layout()
lines_1, labels_1 = ax1.get_legend_handles_labels()
lines_2, labels_2 = ax2.get_legend_handles_labels()
ax1.legend(lines_1 + lines_2, labels_1 + labels_2, loc="upper left")

plt.show()

##Average Order Value (AOV)
query = """
SELECT 
ROUND(
SUM(p.payment_value) / COUNT(DISTINCT o.order_id)
,2) AS AOV
FROM orders o
JOIN order_payments p ON o.order_id = p.order_id
WHERE o.order_status = 'delivered';
"""
pd.read_sql(query, engine)

#multi-chart layout:Orders,Revenue and AOV
query = """
SELECT 
DATE_FORMAT(o.order_purchase_timestamp,'%%Y-%%m') AS month,
COUNT(DISTINCT o.order_id) AS total_orders,
ROUND(SUM(p.payment_value),2) AS revenue
FROM orders o
JOIN order_payments p 
ON o.order_id = p.order_id
WHERE o.order_status = 'delivered'
GROUP BY month
ORDER BY month;
"""

monthly_kpi = pd.read_sql(query, engine)
#Create AOV + Convert Month
monthly_kpi["month"] = pd.to_datetime(monthly_kpi["month"])

monthly_kpi["AOV"] = (
    monthly_kpi["revenue"] / monthly_kpi["total_orders"]
).round(2)

print(monthly_kpi)
#Multi-Chart Dashboard Layout
import matplotlib.pyplot as plt

fig, axes = plt.subplots(3, 1, figsize=(12,12), sharex=True)

# 📦 Orders
axes[0].plot(
    monthly_kpi["month"],
    monthly_kpi["total_orders"],
    marker='o'
)
axes[0].set_title("Monthly Orders")
axes[0].set_ylabel("Orders")
axes[0].grid(True)

#Revenue
axes[1].plot(
    monthly_kpi["month"],
    monthly_kpi["revenue"],
    marker='o'
)
axes[1].set_title("Monthly Revenue")
axes[1].set_ylabel("Revenue")
axes[1].grid(True)

#AOV
axes[2].plot(
    monthly_kpi["month"],
    monthly_kpi["AOV"],
    marker='o'
)
axes[2].set_title("Average Order Value (AOV)")
axes[2].set_ylabel("AOV")
axes[2].set_xlabel("Month")
axes[2].grid(True)

plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

#Use Your Monthly KPI Data
monthly_kpi = pd.read_sql(query, engine)

#Prepare Data
monthly_kpi["month"] = pd.to_datetime(monthly_kpi["month"])

monthly_kpi["AOV"] = (
    monthly_kpi["revenue"] / monthly_kpi["total_orders"]
).round(2)

#Calculate Growth %
monthly_kpi["order_growth_%"] = monthly_kpi["total_orders"].pct_change() * 100
monthly_kpi["revenue_growth_%"] = monthly_kpi["revenue"].pct_change() * 100
monthly_kpi["AOV_growth_%"] = monthly_kpi["AOV"].pct_change() * 100

monthly_kpi = monthly_kpi.round(2)

print(monthly_kpi)

#Get Latest Month Growth (For KPI Cards)
latest = monthly_kpi.iloc[-1]

order_growth = latest["order_growth_%"]
revenue_growth = latest["revenue_growth_%"]
AOV_growth = latest["AOV_growth_%"]

#Format with Arrows
def format_growth(value):
    arrow = "▲" if value > 0 else "▼"
    return f"{arrow} {abs(value):.2f}%"

print("Order Growth:", format_growth(order_growth))
print("Revenue Growth:", format_growth(revenue_growth))
print("AOV Growth:", format_growth(AOV_growth))

#Growth Trend Chart
plt.figure(figsize=(12,6))

plt.plot(monthly_kpi["month"], monthly_kpi["revenue_growth_%"], marker='o')

plt.axhline(0, linestyle='--')

plt.title("Month-over-Month Revenue Growth %")
plt.ylabel("Growth %")
plt.xticks(rotation=45)
plt.grid(True)

plt.show()

