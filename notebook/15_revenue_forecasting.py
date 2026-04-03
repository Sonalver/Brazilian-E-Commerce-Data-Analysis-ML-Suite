import pandas as pd
import matplotlib.pyplot as plt
from sqlalchemy import create_engine
from prophet import Prophet

# -----------------------------
# DB CONNECTION
# -----------------------------
engine = create_engine(
    "mysql+pymysql://root:Sonal123@localhost:3306/olist_project"
)

print("Connected")

# -----------------------------
# LOAD DATA
# -----------------------------
query = """
SELECT * 
FROM monthly_sales_summary
ORDER BY month;
"""

df = pd.read_sql(query, engine)

# Convert date
df["month"] = pd.to_datetime(df["month"])

# Prophet format
df = df.rename(columns={
    "month": "ds",
    "revenue": "y"
})

print(df.head())

# -----------------------------
# TRAIN MODEL
# -----------------------------
model = Prophet()
model.fit(df)

# -----------------------------
# FUTURE DATA (next 6 months)
# -----------------------------
# FUTURE DATA (next 6 months)
future = model.make_future_dataframe(periods=6, freq='ME')

forecast = model.predict(future)

# -----------------------------
# PLOT FORECAST
# -----------------------------
fig1 = model.plot(forecast)
plt.title("Revenue Forecast")
plt.show()

# -----------------------------
# COMPONENTS (trend + seasonality)
# -----------------------------
fig2 = model.plot_components(forecast)
plt.show()