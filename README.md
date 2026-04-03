# Brazilian Olist E-Commerce Intelligence: End-to-End Analytics & Business Strategy Case Study
End-to-end e-commerce analytics project using the Olist dataset. Covers data cleaning, EDA, customer segmentation (RFM, CLV), cohort analysis, sales and revenue insights, market basket analysis, delivery performance, and churn prediction. Includes ML models and dashboards for business decision-making.

 Project Overview
This project is a comprehensive business analytics case study built on the Brazilian Olist e-commerce dataset. It transforms raw transactional data into strategic insights across customer behavior, operations, product performance, and revenue growth.

-Objective:
To identify key business problems, growth drivers, and actionable strategies using data.

-Problem Statement
E-commerce businesses often face challenges like:
Low customer retention
Delivery inefficiencies
Revenue concentration in few categories
Lack of customer understanding

-This project answers:
Why customers are not returning?
What drives revenue growth?
How operations affect satisfaction?
Which products truly matter?

-Tech Stack
Category	Tools
Data Extraction	MySQL
Data Processing	Python (Pandas, NumPy)
Visualization	Matplotlib, Seaborn
Modeling	Prophet (Time Series Forecasting)
Analytics	Cohort, RFM, Pareto

-- Project Workflow
Raw Data → SQL Cleaning → Python EDA → Business Analysis → ML Forecasting → Insights → Strategy

-- Dataset Overview
~100K+ Orders
Customers across Brazil
Multiple tables:
Orders
Customers
Payments
Products
Reviews

- Key Analysis & Insights
# 1. Delivery & Operations Analysis
-What was analyzed?
Delivery time trends
On-time vs delayed deliveries
Regional performance

-Key Insights
~90% deliveries are on-time
Late deliveries → significant drop in ratings (~4.2 → ~2.5)
Some states consistently show delays

-Business Insight
Delivery performance is the strongest driver of customer satisfaction

# 2. Payment Behavior Analysis
Insights
Credit cards dominate transactions
Installments widely used
Higher installments → higher order value

Business Insight
Flexible payment options increase customer spending

# 3. Customer Behavior & Segmentation
-Insights
Majority customers are one-time buyers
Very small loyal segment
- Key Problem
 Business is heavily dependent on new customers

# 4. Cohort & Retention Analysis
- Insights
Sharp drop after first purchase
Almost zero long-term retention
- Business Insight
Acquisition is strong, but retention is weak

# 5. RFM Customer Segmentation
Segments Identified:
 Champions
 Loyal Customers
 Recent Customers
 At Risk
- Insights
Very few Champions
Large number of low-value users
- Insight
Huge opportunity to convert customers into loyal users

# 6. Customer Satisfaction Analysis
- Insights
On-time delivery → high ratings
Late delivery → poor ratings
Freight cost slightly impacts satisfaction
-- Insight
Logistics > Product in driving satisfaction

# 7. Customer Lifetime Value (CLV)
- Insights
Highly skewed distribution
Few customers generate most revenue
-- Insight
Focus on high-value customers (VIP strategy)

# 8. Product & Sales Analysis
- Insights
Low price → high demand
High price → low demand
Revenue ≠ Profit
-- Insight
Pricing strategy directly impacts demand

# 9. Pareto Analysis (80/20 Rule)
- Insights
~20% categories generate ~80% revenue
Long tail contributes very little
-- Insight
 Not all products matter — focus on high-impact categories

# 10. Revenue & KPI Analysis
- Insights
Revenue growing steadily
Orders increasing
AOV remains stable
-- Insight
 Growth is driven by volume, not spending per order

# 11. Revenue Forecasting
Model:
Prophet (Time Series)
- Insights
Strong upward trend
Business expected to grow
-- Insight
Business has scalable growth potential

# Key Business Problems Identified

- Low customer retention
- Revenue concentration risk
- Delivery inefficiencies in regions

# Strategic Recommendations
# 1. Improve Retention
Loyalty programs
Personalized marketing
Re-engagement campaigns

# 2. Increase Revenue
Upselling & cross-selling
Product bundling
Target high-value customers

# 3. Optimize Operations
Improve delivery in slow regions
Reduce delays

# 4. Focus on Key Categories
Invest in top-performing categories
Reduce low-performing inventory

# Final Business Conclusion

-- Acquisition brings users
-- Retention builds business
-- Optimization drives profit

# Future Improvements
Build Streamlit Dashboard
Add churn prediction model
Deploy API for real-time insights

# Author

Sonal Verma
Aspiring Data Scientist | ML Engineer

# Final Note

This project is not just analysis —
it is a data-driven business strategy case study
