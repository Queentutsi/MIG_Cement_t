import pandas as pd

# -----------------------------------------------------------
# LAG FEATURES
# -----------------------------------------------------------

def add_lag_features(df):
    """
    Adds lag features for cement consumption and planned pours.
    Lags are calculated per site to avoid cross-site leakage.
    """
    df = df.copy()

    # Consumption lags
    df['lag_1'] = df.groupby('site_id')['consumed_tonnes'].shift(1)
    df['lag_7'] = df.groupby('site_id')['consumed_tonnes'].shift(7)
    df['lag_14'] = df.groupby('site_id')['consumed_tonnes'].shift(14)
    df['lag_30'] = df.groupby('site_id')['consumed_tonnes'].shift(30)

    # Planned pour lags
    df['planned_lag_1'] = df.groupby('site_id')['planned_pour_tonnes'].shift(1)
    df['planned_lag_7'] = df.groupby('site_id')['planned_pour_tonnes'].shift(7)

    return df


# -----------------------------------------------------------
# ROLLING FEATURES
# -----------------------------------------------------------

def add_rolling_features(df):
    """
    Adds rolling average features for consumption.
    Rolling windows are calculated per site.
    """
    df = df.copy()

    df['roll_7'] = (
        df.groupby('site_id')['consumed_tonnes']
        .rolling(7)
        .mean()
        .reset_index(0, drop=True)
    )

    df['roll_30'] = (
        df.groupby('site_id')['consumed_tonnes']
        .rolling(30)
        .mean()
        .reset_index(0, drop=True)
    )

    df['roll_90'] = (
        df.groupby('site_id')['consumed_tonnes']
        .rolling(90)
        .mean()
        .reset_index(0, drop=True)
    )

    return df


# -----------------------------------------------------------
# SEASONAL FEATURES
# -----------------------------------------------------------

def add_seasonal_features(df):
    """
    Adds calendar-based seasonal features.
    Assumes df.index is a datetime index.
    """
    df = df.copy()

    df['month'] = df.index.month
    df['quarter'] = df.index.quarter
    df['day_of_week'] = df.index.dayofweek

    return df


# -----------------------------------------------------------
# WEATHER FEATURES
# -----------------------------------------------------------

def add_weather_features(df):
    """
    Adds lagged weather features per site.
    """
    df = df.copy()

    df['rain_lag_1'] = df.groupby('site_id')['rain_mm'].shift(1)
    df['temp_lag_1'] = df.groupby('site_id')['avg_temp_c'].shift(1)

    return df


# -----------------------------------------------------------
# BEHAVIOUR ENCODING
# -----------------------------------------------------------

def encode_behavior(df):
    """
    One-hot encodes ALL behavior categories:
    - aggressive
    - chaotic
    - conservative
    """
    df = df.copy()
    df = pd.get_dummies(df, columns=['behavior'], drop_first=False)
    return df


# -----------------------------------------------------------
# FULL PIPELINE
# -----------------------------------------------------------

def build_feature_pipeline(df):
    """
    Runs the full feature engineering pipeline.
    Returns a modelling-ready dataframe.
    """
    df = df.copy()

    df = add_lag_features(df)
    df = add_rolling_features(df)
    df = add_seasonal_features(df)
    df = add_weather_features(df)
    df = encode_behavior(df)

    return df
