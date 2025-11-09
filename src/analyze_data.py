import os
import json
import pandas as pd
from datetime import datetime, timedelta
from prophet import Prophet

def get_recent_files(days=120):
    files = []
    cutoff = datetime.now() - timedelta(days=days)
    for f in os.listdir("data"):
        try:
            date_str = f.split("_")[-1].split(".")[0]
            file_date = datetime.strptime(date_str, "%Y-%m-%d")
            if file_date >= cutoff:
                files.append(os.path.join("data", f))
        except:
            continue
    return sorted(files)

def parse_prices(files):
    price_data = {}
    for f in files:
        date_str = f.split("_")[-1].split(".")[0]
        with open(f) as fp:
            content = json.load(fp)
            hotels = content.get("searchResults", {}).get("results", [])
            for h in hotels:
                name = h.get("name")
                price = h.get("ratePlan", {}).get("price", {}).get("exactCurrent")
                if name and price:
                    price_data.setdefault(name, []).append({"date": date_str, "price": price})
    return price_data

def forecast_prices(price_series, future_days=60):
    df = pd.DataFrame(price_series)
    df["ds"] = pd.to_datetime(df["date"])
    df["y"] = df["price"]
    df = df[["ds", "y"]]

    if len(df) < 10:
        return df["y"].mean()

    m = Prophet(daily_seasonality=True, yearly_seasonality=True)
    m.fit(df)
    future = m.make_future_dataframe(periods=future_days)
    forecast = m.predict(future)
    return forecast.iloc[-future_days:]["yhat"].mean()

def find_deals(price_data, discount_threshold=0.6):
    deals = []
    for name, records in price_data.items():
        if len(records) < 3:
            continue
        current_price = records[-1]["price"]
        predicted_future = forecast_prices(records)
        ratio = current_price / predicted_future
        if ratio <= discount_threshold:
            deals.append({
                "hotel": name,
                "current_price": round(current_price, 2),
                "expected_price": round(predicted_future, 2),
                "discount_ratio": round(ratio, 2)
            })
    return deals

def run_analysis():
    files = get_recent_files()
    price_data = parse_prices(files)
    deals = find_deals(price_data)
    return deals
