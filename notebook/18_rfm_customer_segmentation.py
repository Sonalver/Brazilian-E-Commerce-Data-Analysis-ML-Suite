import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sqlalchemy import create_engine

engine = create_engine("mysql+pymysql://root:Sonal123@localhost:3306/olist_project")

#Step 1: Load Customer Revenue Data
query = """
SELECT
c.customer_unique_id,
MAX(o.order_purchase_timestamp) AS last_purchase,
COUNT(o.order_id) AS frequency,
SUM(p.payment_value) AS monetary
FROM olist_customers_dataset c
JOIN orders o ON c.customer_id = o.customer_id
JOIN order_payments p ON o.order_id = p.order_id
WHERE o.order_status='delivered'
GROUP BY c.customer_unique_id;
"""

rfm = pd.read_sql(query, engine)

#Step 2: Prepare Recency
rfm["last_purchase"] = pd.to_datetime(rfm["last_purchase"])

reference_date = rfm["last_purchase"].max()

rfm["recency"] = (reference_date - rfm["last_purchase"]).dt.days

#Step 3: Create RFM Scores
rfm["R"] = pd.qcut(rfm["recency"],4,labels=[4,3,2,1])
rfm["F"] = pd.qcut(rfm["frequency"].rank(method="first"),4,labels=[1,2,3,4])
rfm["M"] = pd.qcut(rfm["monetary"],4,labels=[1,2,3,4])

rfm["RFM_score"] = rfm["R"].astype(str) + rfm["F"].astype(str) + rfm["M"].astype(str)

print(rfm.head())

# 3. Define segment function
def segment(row):
    if row['R'] <= 2 and row['F'] >= 4 and row['M'] >= 4:
        return 'Champions'
    elif row['R'] <= 3 and row['F'] >= 3:
        return 'Loyal Customers'
    elif row['R'] <= 4:
        return 'Potential Loyalist'
    elif row['R'] >= 4 and row['F'] <= 2:
        return 'At Risk'
    else:
        return 'Others'


#Step 4: Segment Customers


rfm["segment"] = rfm.apply(segment, axis=1)

print(rfm["segment"].value_counts())

#