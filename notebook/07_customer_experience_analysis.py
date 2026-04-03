import pandas as pd
import matplotlib.pyplot as plt
from sqlalchemy import create_engine

engine = create_engine("mysql+pymysql://root:Sonal123@localhost:3306/olist_project")

#Average Review Score
query = """
SELECT ROUND(AVG(review_score),2) AS avg_review_score
FROM olist_order_reviews_dataset;
"""
avg_review = pd.read_sql(query, engine)

print("Average Review Score")
print(avg_review)

#Review Score Distribution
query = """
SELECT review_score, COUNT(*) AS total_reviews
FROM olist_order_reviews_dataset
GROUP BY review_score
ORDER BY review_score;
"""

review_dist = pd.read_sql(query, engine)
print(review_dist)
#Chart
review_dist.set_index("review_score").plot(
    kind="bar",
    figsize=(7,4),
    legend=False
)
plt.title("Review Score Distribution")
plt.ylabel("Total Reviews")
plt.xlabel("Review Score")
plt.show()

#Delivery Time vs Review Score
query = """
SELECT
r.review_score,
ROUND(AVG(DATEDIFF(o.order_delivered_customer_date,
o.order_purchase_timestamp)),2) AS avg_delivery_days
FROM orders o
JOIN olist_order_reviews_dataset r
ON o.order_id = r.order_id
WHERE o.order_status = 'delivered'
GROUP BY r.review_score
ORDER BY r.review_score;
"""

delivery_vs_review = pd.read_sql(query, engine)
print(delivery_vs_review)
#Chart
delivery_vs_review.plot(
    x="review_score",
    y="avg_delivery_days",
    kind="bar",
    figsize=(7,4),
    legend=False
)
plt.title("Delivery Time vs Review Score")
plt.ylabel("Average Delivery Days")
plt.xlabel("Review Score")
plt.show()

#Delivery Delay Impact
query = """
SELECT
    ROUND(AVG(DATEDIFF(
        o.order_delivered_customer_date,
        o.order_estimated_delivery_date
    )),2) AS avg_delay,
    ROUND(AVG(r.review_score),2) AS avg_review
FROM orders o
JOIN olist_order_reviews_dataset r
    ON o.order_id = r.order_id
WHERE o.order_status = 'delivered'
AND o.order_delivered_customer_date IS NOT NULL;
"""

pd.read_sql(query, engine)

#On-Time vs Late Delivery
query = """
SELECT
CASE
    WHEN o.order_delivered_customer_date <= o.order_estimated_delivery_date
         THEN 'On Time'
    ELSE 'Late'
END AS delivery_status,

ROUND(AVG(r.review_score),2) AS avg_review

FROM orders o
JOIN olist_order_reviews_dataset r
ON o.order_id = r.order_id

WHERE o.order_status = 'delivered'
GROUP BY delivery_status;
"""

delivery_driver = pd.read_sql(query, engine)
delivery_driver.plot(x="delivery_status", y="avg_review", kind="bar", legend=False)
plt.title("On-Time vs Late Delivery Impact")
plt.show()

# Revenue by Review Score
query = """
SELECT
    r.review_score,
    ROUND(SUM(p.payment_value), 2) AS revenue
FROM olist_order_reviews_dataset r
JOIN orders o
    ON r.order_id = o.order_id
JOIN order_payments p
    ON o.order_id = p.order_id
GROUP BY r.review_score
ORDER BY r.review_score;
"""

revenue_review = pd.read_sql(query, engine)
print(revenue_review)
#chart
revenue_review.plot(
    x="review_score",
    y="revenue",
    kind="bar",
    figsize=(7,4),
    legend=False
)

plt.title("Revenue by Review Score")
plt.xlabel("Review Score")
plt.ylabel("Revenue")
plt.show()

#State-wise Average Review Score
query = """
SELECT
    c.customer_state,
    ROUND(AVG(r.review_score), 2) AS avg_review
FROM customers c
JOIN orders o
    ON c.customer_id = o.customer_id
JOIN olist_order_reviews_dataset r
    ON o.order_id = r.order_id
GROUP BY c.customer_state
ORDER BY avg_review DESC;
"""

state_review = pd.read_sql(query, engine)
print(state_review)
#chart
state_review.head(10).plot(
    x="customer_state",
    y="avg_review",
    kind="bar",
    figsize=(10,5),
    legend=False
)

plt.title("Top 10 States by Average Review Score")
plt.xlabel("State")
plt.ylabel("Average Review Score")
plt.show()

#Freight Cost vs Review Score
query = """
SELECT
CASE
    WHEN freight_value < 10 THEN 'Low Freight'
    WHEN freight_value BETWEEN 10 AND 20 THEN 'Medium Freight'
    ELSE 'High Freight'
END AS freight_range,

ROUND(AVG(r.review_score),2) AS avg_review

FROM olist_order_items_dataset oi
JOIN orders o ON oi.order_id = o.order_id
JOIN olist_order_reviews_dataset r ON o.order_id = r.order_id

GROUP BY freight_range;
"""

freight_driver = pd.read_sql(query, engine)
freight_driver.plot(x="freight_range", y="avg_review", kind="bar", legend=False)
plt.title("Freight Cost Impact on Satisfaction")
plt.show()

#Order Value Impact
query = """
SELECT
CASE
    WHEN payment_value < 50 THEN 'Low Value'
    WHEN payment_value BETWEEN 50 AND 150 THEN 'Medium Value'
    ELSE 'High Value'
END AS order_value_segment,

ROUND(AVG(r.review_score),2) AS avg_review

FROM order_payments p
JOIN orders o ON p.order_id = o.order_id
JOIN olist_order_reviews_dataset r ON o.order_id = r.order_id

GROUP BY order_value_segment;
"""

value_driver = pd.read_sql(query, engine)
value_driver.plot(x="order_value_segment", y="avg_review", kind="bar", legend=False)
plt.title("Order Value vs Satisfaction")
plt.show()

#Product Category Impact
query = """
SELECT
    p.product_category_name AS product_category,
    ROUND(AVG(r.review_score), 2) AS avg_review,
    COUNT(*) AS total_orders

FROM olist_order_items_dataset oi

JOIN olist_products_dataset p
    ON oi.product_id = p.product_id

JOIN orders o
    ON oi.order_id = o.order_id

JOIN olist_order_reviews_dataset r
    ON o.order_id = r.order_id

WHERE o.order_status = 'delivered'
AND p.product_category_name IS NOT NULL

GROUP BY p.product_category_name
ORDER BY avg_review DESC
LIMIT 10;
"""

category_driver = pd.read_sql(query, engine)
print("\nTop Categories by Satisfaction\n", category_driver)

category_driver.plot(
    x="product_category",
    y="avg_review",
    kind="bar",
    figsize=(10,5),
    legend=False
)
plt.title("Top Product Categories by Customer Satisfaction")
plt.xticks(rotation=45)
plt.show()

#On-Time vs Late Delivery Impact on Reviews
query = """
SELECT
CASE
WHEN o.order_delivered_customer_date > o.order_estimated_delivery_date
THEN 'Late'
ELSE 'On Time'
END AS delivery_status,
ROUND(AVG(r.review_score),2) AS avg_review_score
FROM orders o
JOIN olist_order_reviews_dataset r
ON o.order_id = r.order_id
WHERE o.order_status='delivered'
GROUP BY delivery_status;
"""

on_time_vs_late = pd.read_sql(query, engine)
print(on_time_vs_late)
#Chart
on_time_vs_late.set_index("delivery_status").plot(
    kind="bar",
    legend=False,
    figsize=(6,4)
)
plt.title("Customer Satisfaction: On-Time vs Late Delivery")
plt.ylabel("Average Review Score")
plt.xticks(rotation=0)
plt.show()

#Late Delivery → 1-Star Review Contribution
query = """
SELECT
CASE
WHEN o.order_delivered_customer_date > o.order_estimated_delivery_date
THEN 'Late'
ELSE 'On Time'
END AS delivery_status,
COUNT(*) AS one_star_reviews
FROM orders o
JOIN olist_order_reviews_dataset r
ON o.order_id = r.order_id
WHERE r.review_score = 1
AND o.order_status = 'delivered'
GROUP BY delivery_status;
"""

one_star = pd.read_sql(query, engine)
print(one_star)
# 1-Star Contribution Chart
one_star.set_index("delivery_status")["one_star_reviews"].plot(
    kind="bar", figsize=(6,4), legend=False
)
plt.title("Late Delivery Contribution to 1-Star Reviews")
plt.ylabel("Number of 1-Star Reviews")
plt.xticks(rotation=0)
plt.show()

# Contribution %
one_star["contribution_%"] = (
    one_star["one_star_reviews"] /
    one_star["one_star_reviews"].sum() * 100
).round(2)

print(one_star)

# Revenue Impact of Delivery Performance

query = """
SELECT
    CASE
        WHEN o.order_delivered_customer_date > o.order_estimated_delivery_date
            THEN 'Late'
        ELSE 'On Time'
    END AS delivery_status,
    ROUND(SUM(p.payment_value), 2) AS revenue
FROM orders o
JOIN olist_order_reviews_dataset r
    ON o.order_id = r.order_id
JOIN order_payments p
    ON o.order_id = p.order_id
WHERE o.order_status = 'delivered'
  AND o.order_delivered_customer_date IS NOT NULL
GROUP BY delivery_status;
"""

revenue_impact = pd.read_sql(query, engine)
print(revenue_impact)
# Revenue Chart
revenue_impact.set_index("delivery_status")["revenue"].plot(
    kind="bar", figsize=(6,4), legend=False
)
plt.title("Revenue: On-Time vs Late Deliveries")
plt.ylabel("Revenue")
plt.xticks(rotation=0)
plt.show()

#Average Delivery Delay for Low Reviews
query = """
SELECT
ROUND(AVG(
DATEDIFF(o.order_delivered_customer_date,
o.order_estimated_delivery_date)
),2) AS avg_delay_days
FROM orders o
JOIN olist_order_reviews_dataset r
ON o.order_id = r.order_id
WHERE r.review_score <= 2
AND o.order_delivered_customer_date > o.order_estimated_delivery_date;
"""

delay_low_reviews = pd.read_sql(query, engine)
print(delay_low_reviews)

#Delivery Time Buckets vs Review Score
query = """
SELECT
CASE
WHEN DATEDIFF(o.order_delivered_customer_date,
o.order_purchase_timestamp) <= 3 THEN '0-3 days'
WHEN DATEDIFF(o.order_delivered_customer_date,
o.order_purchase_timestamp) <= 7 THEN '4-7 days'
WHEN DATEDIFF(o.order_delivered_customer_date,
o.order_purchase_timestamp) <= 14 THEN '8-14 days'
ELSE '15+ days'
END AS delivery_speed,
ROUND(AVG(r.review_score),2) AS avg_review
FROM orders o
JOIN olist_order_reviews_dataset r
ON o.order_id = r.order_id
WHERE o.order_status='delivered'
GROUP BY delivery_speed
ORDER BY avg_review DESC;
"""

delivery_bucket = pd.read_sql(query, engine)
print(delivery_bucket)

#State-wise Customer Satisfaction
query = """
SELECT
c.customer_state,
ROUND(AVG(r.review_score),2) AS avg_review
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
JOIN olist_order_reviews_dataset r
ON o.order_id = r.order_id
GROUP BY c.customer_state
ORDER BY avg_review DESC;
"""

state_review = pd.read_sql(query, engine)
print(state_review)

#Monthly Customer Satisfaction Trend
query = """
SELECT
DATE_FORMAT(o.order_purchase_timestamp,'%%Y-%%m') AS month,
ROUND(AVG(r.review_score),2) AS avg_review
FROM orders o
JOIN olist_order_reviews_dataset r
ON o.order_id = r.order_id
GROUP BY month
ORDER BY month;
"""

monthly_review = pd.read_sql(query, engine)
print(monthly_review)
#Chart
monthly_review.plot(
    x="month",
    y="avg_review",
    kind="line",
    marker="o",
    figsize=(10,5)
)

plt.title("Monthly Customer Satisfaction Trend")
plt.ylabel("Average Review Score")
plt.xticks(rotation=45)
plt.show()