
# MIG_cement_TeamB

📘 **Midlands Infrastructure Group — MIG Cement Demand Forecasting Project**

This project is based on cement operations data from **Midlands Infrastructure Group (MIG)** — a Tier‑1 UK civil engineering company that runs 25–40 active construction sites. Cement is a critical material for them, but demand is very unpredictable because of weather, pour schedules, and inventory issues.  

The goal of this project is to help MIG forecast cement demand better so they can reduce waste, avoid stockouts, and plan more efficiently.

---

## 🏗️ Project Overview

MIG currently struggles with:

- Running out of cement at the wrong time  
- Overstocking and wasting material  
- Paying extra for emergency deliveries  
- Using spreadsheets instead of proper forecasting  
- Not having visibility across all sites  

This project aims to build a cement demand forecasting system using:

- Historical consumption  
- Planned pour schedules  
- Inventory levels  
- Weather (rain + temperature)  
- Site behaviour patterns  

The final goal is to produce:

- A forecasting model (8‑week horizon)  
- A dashboard (Plotly Dash)  
- Inventory optimisation logic  
- A deployable pipeline (AWS)

---

## 🎯 Project Objectives

- **MAPE ≤ 15%** for cement demand forecasting  
- **≥ 98% pour readiness** (no stockouts)  
- **20% improvement** in silo utilisation  
- **30% reduction** in cement write‑offs  
- A dashboard that operations managers can actually use  

---

## 📂 Repository Structure

```
MIG_cement_TeamB/
│
├── Notebooks/
│   ├── EDA.ipynb
│   └── Cleaning.ipynb
│
├── data/
│   └── MIG_Cement_Records.db
│
├── src/
│   ├── cleaning.py
│   ├── feature_engineering.py
│   ├── model_training.py
│   └── forecasting_pipeline.py
│
├── dashboard/
│   └── app.py
│
└── README.md
```

---

## 📊 Data Dictionary  

### **Operations Table**

| Column | Description |
|--------|-------------|
| **date** | Date of operation (daily granularity) |
| **site_id** | Unique ID of construction site |
| **cement_type** | Type of cement (CEM_I, CEM_II, CEM_III) |
| **planned_pour_tonnes** | Planned cement pour for that day |
| **consumed_tonnes** | Actual cement used |
| **opening_inventory_tonnes** | Inventory at start of day |
| **deliveries_tonnes** | Cement delivered that day |
| **closing_inventory_tonnes** | Inventory at end of day |
| **rain_mm** | Rainfall in millimetres |
| **avg_temp_c** | Average temperature in °C |
| **silo_capacity** | Maximum silo capacity at that site |

---

### **Sites Table**

| Column | Description |
|--------|-------------|
| **site_id** | Site identifier |
| **region** | Geographic region (North, South, East, West) |
| **silo_capacity** | Capacity of silo at that site |
| **behavior** | Behaviour pattern (aggressive, conservative, chaotic) |

---

### **CementTypes Table**

| Column | Description |
|--------|-------------|
| **cement_type** | Cement type code (CEM_I, CEM_II, CEM_III) |

---

## 🔧 Workflow (Step‑by‑Step)

### **1. Data Ingestion & Cleaning**
- Load SQLite tables into pandas  
- Convert date column  
- Standardise IDs (site_id, cement_type)  
- Validate join keys  
- Check categorical columns  
- Validate inventory logic  
- Merge tables into one dataset  

---

### **2. Exploratory Data Analysis (EDA)**
- Plot consumption trends  
- Compare sites  
- Look at weather impact  
- Check seasonality  
- Identify outliers  
- Understand behaviour patterns  

---

### **3. Feature Engineering**
- Lag features (1‑day, 7‑day, 14‑day)  
- Rolling averages  
- Weather‑adjusted pour indicators  
- Inventory turnover  
- One‑hot encoding for region, behaviour, cement_type  

---

## 🤖 Model Development

The aim is to build and compare **five models**:

1. Baseline model** (mean or last value)  
2. Linear Regression**  
3. Random Forest Regressor**  
4. XGBoost / Gradient Boosting**  
5. Time‑series model** (Prophet, ARIMA and SARIMAX)  

Models will be evaluated using:

- RMSE  
- MAE  
- MAPE  

## 📦 Inventory Simulation

Using the forecast:

```
closing_inventory = opening_inventory + deliveries - consumed
```

The aim is to simulate:

- Future silo levels  
- Reorder points  
- Lead times  
- Stockout risk  


## 📊 Dashboard (Plotly Dash)

The dashboard will show:

- Forecasts  
- Inventory projections  
- Reorder alerts  
- Site‑level drill‑downs  


## 🚀 Deployment

1. Save best model as `model.pkl`  
2. Build a FastAPI prediction service  
3. Containerise with Docker  
4. Deploy to AWS  
5. Add monitoring and retraining triggers  


## Preocess to cleaning the dataset. 
#### 🧹 Data Cleaning & Validation Summary

I started by pulling three raw tables straight from the SQLite database: "Operations", "Sites", and "CementTypes". From there, I built a full cleaning pipeline that turned messy, real‑world construction data into a reliable, analysis‑ready dataset.

First, 

### ✔ Structural Cleaning
- Converted all dates into proper `datetime` format  
- Standardised `site_id` and `cement_type` values  
- Ensured all numeric fields were correctly typed  
- Verified join keys across tables (no missing sites or cement types)

### ✔ Inventory Logic Validation
The raw data included daily opening inventory, deliveries, consumption, and closing inventory.  
I validated the core inventory equation:

///closing_inventory = opening_inventory + deliveries - consumed///

Every mismatch was identified, investigated, and corrected using a tolerance‑based comparison to handle floating‑point precision.  
The result: "0 remaining mismatches" — full inventory consistency across all 32,880 rows.

### ✔ Merging & Redundancy Removal
After cleaning, I merged the three tables into one unified dataset.  
Pandas created duplicate silo capacity columns (`_x` and `_y`) during the merge, so I removed the redundant version and kept the correct one from the Sites table.

I also dropped temporary validation columns like `inventory_match` to keep the final dataset tidy.

### ✔ Final Dataset
The cleaned, merged dataset now contains:
- Daily operational metrics  
- Weather conditions  
- Site metadata  
- Fully validated inventory values  
There were no no duplicates, missing values, redundant columns, and inconsistencies. Just a clean, trustworthy dataset ready for EDA, feature engineering, and forecasting.




