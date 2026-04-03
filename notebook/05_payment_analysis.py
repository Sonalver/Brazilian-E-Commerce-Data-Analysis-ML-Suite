import pandas as pd
from sqlalchemy import create_engine
import matplotlib.pyplot as plt
#Connect to Database
engine = create_engine("mysql+pymysql://root:Sonal123@localhost:3306/olist_project")
print("Connected for analysis")

#Top Payment Methods
query = """
SELECT 
payment_type,
COUNT(*) AS total_transactions
FROM order_payments
GROUP BY payment_type
ORDER BY total_transactions DESC;
"""
payment_methods = pd.read_sql(query, engine)
print(payment_methods)
#Chart
payment_methods.set_index("payment_type").plot(
    kind="bar", figsize=(8,4), legend=False
)

plt.title("Top Payment Methods")
plt.ylabel("Total Transactions")
plt.xticks(rotation=45)
plt.show()

#Payment Behavior Analysis
#Payment Method Distribution
query = """
SELECT
payment_type,
COUNT(*) AS total_transactions
FROM order_payments
GROUP BY payment_type
ORDER BY total_transactions DESC;
"""

payment_methods = pd.read_sql(query, engine)
print(payment_methods)

# Chart
payment_methods.set_index("payment_type").plot(
    kind="bar",
    figsize=(7,4),
    legend=False
)

plt.title("Payment Method Distribution")
plt.ylabel("Number of Transactions")
plt.xlabel("Payment Type")
plt.xticks(rotation=45)
plt.show()

#Revenue by Payment Method
query = """
SELECT
payment_type,
ROUND(SUM(payment_value),2) AS revenue
FROM order_payments
GROUP BY payment_type
ORDER BY revenue DESC;
"""

payment_revenue = pd.read_sql(query, engine)
print(payment_revenue)

# Chart
payment_revenue.set_index("payment_type").plot(
    kind="bar",
    figsize=(7,4),
    legend=False
)

plt.title("Revenue by Payment Method")
plt.ylabel("Revenue")
plt.xlabel("Payment Type")
plt.xticks(rotation=45)
plt.show()

#Average Payment Value by Payment Method
query = """
SELECT
payment_type,
ROUND(AVG(payment_value),2) AS avg_payment_value
FROM order_payments
GROUP BY payment_type
ORDER BY avg_payment_value DESC;
"""

avg_payment = pd.read_sql(query, engine)
print(avg_payment)

#Installment Usage Analysis
query = """
SELECT
payment_installments,
COUNT(*) AS total_transactions
FROM order_payments
GROUP BY payment_installments
ORDER BY payment_installments;
"""

installments = pd.read_sql(query, engine)
print(installments)

# Chart
installments.plot(
    x="payment_installments",
    y="total_transactions",
    kind="line",
    marker="o",
    figsize=(8,4)
)

plt.title("Installment Usage Distribution")
plt.xlabel("Number of Installments")
plt.ylabel("Transactions")
plt.show()

#Average Installments by Payment Type
query = """
SELECT
payment_type,
ROUND(AVG(payment_installments),2) AS avg_installments
FROM order_payments
GROUP BY payment_type
ORDER BY avg_installments DESC;
"""

installment_type = pd.read_sql(query, engine)
print(installment_type)

#Installments vs Order Value
query = """
SELECT
payment_installments,
ROUND(AVG(payment_value),2) AS avg_order_value
FROM order_payments
GROUP BY payment_installments
ORDER BY payment_installments;
"""

installment_value = pd.read_sql(query, engine)
print(installment_value)

# Chart
installment_value.plot(
    x="payment_installments",
    y="avg_order_value",
    kind="line",
    marker="o",
    figsize=(8,4)
)

plt.title("Installments vs Average Order Value")
plt.xlabel("Installments")
plt.ylabel("Average Order Value")
plt.show()
