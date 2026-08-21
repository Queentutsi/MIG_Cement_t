import pandas as pd
from fastapi import FastAPI

app = FastAPI()

# Load data once at startup
dashboard_df = pd.read_csv("MIG_dashboard_inventory_forecast.csv")
dashboard_df["date"] = pd.to_datetime(dashboard_df["date"])

def compute_kpis(df_site):
    stockout_days = (df_site["closing_inventory_sim"] <= 0).sum()
    total_days = len(df_site)
    stockout_pct = (stockout_days / total_days) * 100 if total_days > 0 else 0

    reorder_count = df_site["reorder_alert"].sum()

    utilisation_pct = (
        (df_site["closing_inventory_sim"] / df_site["silo_capacity"]).mean() * 100
        if total_days > 0 else 0
    )

    return stockout_pct, reorder_count, utilisation_pct

@app.get("/forecast/{site_id}")
def get_forecast(site_id: str):
    df_site = dashboard_df[dashboard_df["site_id"] == site_id]

    if df_site.empty:
        return {"error": "Invalid site_id or no data"}

    stockout_pct, reorder_count, utilisation_pct = compute_kpis(df_site)

    # Convert time series to JSON‑friendly format
    forecast_data = {
        "date": df_site["date"].dt.strftime("%Y-%m-%d").tolist(),
        "ensemble": df_site["ensemble"].tolist(),
        "sarimax": df_site["sarimax"].tolist(),
        "xgboost": df_site["xgboost"].tolist(),
        "random_forest": df_site["random_forest"].tolist(),
        "closing_inventory_sim": df_site["closing_inventory_sim"].tolist(),
        "silo_capacity": df_site["silo_capacity"].tolist()
    }

    kpis = {
        "stockout_pct": stockout_pct,
        "reorder_count": int(reorder_count),
        "utilisation_pct": utilisation_pct
    }

    return {
        "site_id": site_id,
        "forecast": forecast_data,
        "kpis": kpis
    }
