import pandas as pd
from sqlalchemy import create_engine
import matplotlib.pyplot as plt
#Connect to Database
engine = create_engine("mysql+pymysql://root:Sonal123@localhost:3306/olist_project")
print("Connected for analysis")

#Load Full Core Tables
customers = pd.read_sql("SELECT * FROM customers;", engine)
orders = pd.read_sql("SELECT * FROM orders;", engine)
payments = pd.read_sql("SELECT * FROM order_payments;", engine)
reviews = pd.read_sql("SELECT * FROM olist_order_reviews_dataset;", engine)
items = pd.read_sql("SELECT * FROM olist_order_items_dataset;", engine)

print("Data Loaded Successfully")

#Convert Date Columns to Datetime
date_cols = [
    "order_purchase_timestamp",
    "order_approved_at",
    "order_delivered_carrier_date",
    "order_delivered_customer_date",
    "order_estimated_delivery_date"
]

for col in date_cols:
    orders[col] = pd.to_datetime(orders[col])

reviews["review_creation_date"] = pd.to_datetime(reviews["review_creation_date"])
reviews["review_answer_timestamp"] = pd.to_datetime(reviews["review_answer_timestamp"])

print("Date columns converted")

#Filter Only Delivered Orders (Business Logic)
orders_delivered = orders[orders["order_status"] == "delivered"].copy()

print("Delivered Orders:", len(orders_delivered))

#Remove Duplicates
orders_delivered.drop_duplicates(subset=["order_id"], inplace=True)
customers.drop_duplicates(subset=["customer_id"], inplace=True)

print("Duplicates removed")

#Handle Missing Values
#Check Missing
print("Missing values in Orders:")
print(orders_delivered.isnull().sum())

#Remove Orders Without Delivery Date
orders_delivered = orders_delivered[
    orders_delivered["order_delivered_customer_date"].notna()
]

#Create Delivery Time Feature
orders_delivered["delivery_delay_days"] = (
    orders_delivered["order_delivered_customer_date"] -
    orders_delivered["order_estimated_delivery_date"]
).dt.days

#Create On-Time vs Late Column
orders_delivered["delivery_status"] = orders_delivered["delivery_delay_days"].apply(
    lambda x: "Late" if x > 0 else "On Time"
)

#Create Order Month Feature (For Trends)
orders_delivered["order_month"] = orders_delivered[
    "order_purchase_timestamp"
].dt.to_period("M")

#Merge Orders + Payments (For Revenue KPIs)
orders_payments = pd.merge(
    orders_delivered,
    payments,
    on="order_id",
    how="left"
)

print("Merged dataset ready")

#Basic Outlier Check
print("Payment Value Summary:")
print(orders_payments["payment_value"].describe())