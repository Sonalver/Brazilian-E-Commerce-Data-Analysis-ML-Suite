import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sqlalchemy import create_engine

engine = create_engine("mysql+pymysql://root:Sonal123@localhost:3306/olist_project")

#Step 1: Calculate Average Revenue per Customer
query = """
SELECT
c.customer_unique_id,
COUNT(o.order_id) AS total_orders,
SUM(p.payment_value) AS total_revenue
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
JOIN order_payments p ON o.order_id = p.order_id
WHERE o.order_status='delivered'
GROUP BY c.customer_unique_id;
"""

clv = pd.read_sql(query, engine)

#Step 2: Calculate CLV Metrics
avg_order_value = clv["total_revenue"].sum() / clv["total_orders"].sum()

purchase_frequency = clv["total_orders"].sum() / len(clv)

customer_value = avg_order_value * purchase_frequency

print("Average Order Value:", avg_order_value)
print("Purchase Frequency:", purchase_frequency)
print("Estimated Customer Lifetime Value:", customer_value)

#Step 3: CLV Distribution
clv["clv_estimate"] = clv["total_revenue"]

clv["clv_estimate"].plot(kind="hist", bins=30, figsize=(8,4))

plt.title("Customer Lifetime Value Distribution")
plt.xlabel("CLV")
plt.show()
