import pandas as pd
from sqlalchemy import create_engine
import matplotlib.pyplot as plt
#Connect to Database
engine = create_engine("mysql+pymysql://root:Sonal123@localhost:3306/olist_project")
print("Connected for analysis")

#Check Current Database
query = "SHOW TABLES;"
tables = pd.read_sql(query, engine)

#List All Tables
tables = pd.read_sql("SHOW TABLES;", engine)
print("Tables in database:")
print(tables)

print(pd.read_sql("SELECT DATABASE();", engine))
print(pd.read_sql("SHOW TABLES;", engine))

#Row count of each table
print("Total customers:")
print(pd.read_sql("SELECT COUNT(*) FROM customers;", engine))

print("Total orders:")
print(pd.read_sql("SELECT COUNT(*) FROM orders;", engine))

print("Total payments:")
print(pd.read_sql("SELECT COUNT(*) FROM order_payments;", engine))

#Preview first 5 rows
customers = pd.read_sql("SELECT * FROM customers LIMIT 5;", engine)
print("Customers sample:")
print(customers)

orders = pd.read_sql("SELECT * FROM orders LIMIT 5;", engine)
print("Orders sample:")
print(orders)

payments = pd.read_sql("SELECT * FROM order_payments LIMIT 5;", engine)
print("Payments sample:")
print(payments)

#Check column names
print("Customers columns:", customers.columns)
print("Orders columns:", orders.columns)
print("Payments columns:", payments.columns)

#Check Order Status Distribution
query = """
SELECT order_status, COUNT(*) AS total
FROM orders
GROUP BY order_status;
"""
print(pd.read_sql(query, engine))

#Check missing values
print("Missing values in customers:")
print(customers.isnull().sum())

print("Missing values in orders:")
print(orders.isnull().sum())

#check reviews
reviews = pd.read_sql("SELECT * FROM olist_order_reviews_dataset;", engine)
print("Missing values in Reviews:")
print(reviews.isnull().sum())

#Check unique values
print("Unique order status:")
print(pd.read_sql("SELECT DISTINCT order_status FROM orders;", engine))

#Check duplicates
query = """
SELECT order_id, COUNT(*) AS duplicate_count
FROM orders
GROUP BY order_id
HAVING COUNT(*) > 1;
"""
duplicates = pd.read_sql(query, engine)

print("Duplicate Orders:")
print(duplicates)

#Basic Date Range Check
query = """
SELECT 
MIN(order_purchase_timestamp) AS first_order,
MAX(order_purchase_timestamp) AS last_order
FROM orders;
"""
print(pd.read_sql(query, engine))

numeric_orders = orders.select_dtypes(include=['int64', 'float64'])
numeric_payments = payments.select_dtypes(include=['int64','float64'])

#shape
print("Orders dataset shape:", orders.shape)
print("Payments dataset shape:", payments.shape)

#Descriptive Statistics (Numerical Columns)
print("\nDescriptive Statistics (Orders Dataset):")
print(orders.describe())

print("\nDescriptive Statistics (Payments Dataset):")
print(payments.describe())

#Descriptive Statistics for Categorical Columns
print("\nDescriptive Statistics (Orders Dataset):")
print(orders.describe())

print("\nDescriptive Statistics (Payments Dataset):")
print(payments.describe())

#Descriptive Statistics (Numerical Columns)
print("\nDescriptive Statistics (Orders Dataset):")
print(orders.describe())

print("\nDescriptive Statistics (Payments Dataset):")
print(payments.describe())

#Skewness
print("\nSkewness (Orders Dataset)")
print(numeric_orders.skew())

print("\nSkewness (Payments Dataset)")
print(numeric_payments.skew())

#Kurtosis
print("\nKurtosis (Orders Dataset)")
print(numeric_orders.kurtosis())

print("\nKurtosis (Payments Dataset)")
print(numeric_payments.kurtosis())