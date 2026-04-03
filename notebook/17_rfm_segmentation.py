from sqlalchemy import create_engine
import pandas as pd

# DB CONNECTION
# -----------------------------
engine = create_engine(
    "mysql+pymysql://root:Sonal123@localhost:3306/olist_project"
)
# Load RFM table
rfm = pd.read_sql("SELECT * FROM rfm_summary", engine)

# -----------------------------
# Create RFM Scores (1–4)
# -----------------------------
rfm['r_score'] = pd.qcut(rfm['recency'], 4, labels=[4,3,2,1])
rfm['f_score'] = pd.qcut(rfm['frequency'].rank(method="first"), 4, labels=[1,2,3,4])
rfm['m_score'] = pd.qcut(rfm['monetary'], 4, labels=[1,2,3,4])

# Combine score
rfm['rfm_score'] = (
    rfm['r_score'].astype(str) +
    rfm['f_score'].astype(str) +
    rfm['m_score'].astype(str)
)

# -----------------------------
# Customer Segments
# -----------------------------
def segment(row):
    if row['r_score'] == 4 and row['f_score'] == 4:
        return 'Champions'
    elif row['r_score'] >= 3 and row['f_score'] >= 3:
        return 'Loyal Customers'
    elif row['r_score'] >= 3:
        return 'Recent Customers'
    elif row['f_score'] >= 3:
        return 'Frequent Customers'
    else:
        return 'At Risk'

rfm['segment'] = rfm.apply(segment, axis=1)

print(rfm.head())