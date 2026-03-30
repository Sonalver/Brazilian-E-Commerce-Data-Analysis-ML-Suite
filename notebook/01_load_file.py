# Import required libraries
import pandas as pd
from sqlalchemy import create_engine

# Create connection between Python and MySQL database
# mysql+pymysql://<username>:<password>@<host>:<port>/<database_name>
engine = create_engine("mysql+pymysql://root:Sonal123@localhost:3306/olist_project")

print("Connected successfully!")

## Load CSV files from local system into pandas DataFrames
customers = pd.read_csv("C:/Users/sonal/olist_sql_project/data/olist_customers_dataset.csv")
orders = pd.read_csv("C:/Users/sonal/olist_sql_project/data/olist_orders_dataset.csv")
payments = pd.read_csv("C:/Users/sonal/olist_sql_project/data/olist_order_payments_dataset.csv")
products = pd.read_csv("C:/Users/sonal/olist_sql_project/data/olist_products_dataset.csv")
translation = pd.read_csv("C:/Users/sonal/olist_sql_project/data/product_category_name_translation.csv")


# Preview the first 5 rows
print(customers.head())
print(orders.head())

#Upload the data into MySQL
customers.to_sql("customers", engine, if_exists="replace", index=False)
orders.to_sql("orders", engine, if_exists="replace", index=False)
payments.to_sql("order_payments", engine, if_exists="replace", index=False)

print(" Data uploaded to MySQL!")
