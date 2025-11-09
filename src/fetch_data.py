import os
import requests
import json
from datetime import datetime

RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY")
API_HOST = "hotels-com-provider.p.rapidapi.com"  # Replace with your chosen API host

def fetch_hotels(city: str, checkin: str, checkout: str, adults: int = 2, currency="INR"):
    """Fetch hotel data for a given city and date range."""
    url = f"https://{API_HOST}/v1/hotels/search"
    headers = {
        "x-rapidapi-key": RAPIDAPI_KEY,
        "x-rapidapi-host": API_HOST
    }
    query = {
        "query": city,
        "checkin_date": checkin,
        "checkout_date": checkout,
        "adults_number": adults,
        "currency": currency
    }

    try:
        response = requests.get(url, headers=headers, params=query)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Error fetching hotel data for {city}: {e}")
        return {}

def save_data(city, data):
    os.makedirs("data", exist_ok=True)
    filename = f"data/{city}_{datetime.now().strftime('%Y-%m-%d')}.json"
    with open(filename, "w") as f:
        json.dump(data, f, indent=2)
    return filename

def run_fetch():
    cities = ["Goa", "Alibaug", "Jaipur", "Udaipur"]
    checkin = "2025-11-15"
    checkout = "2025-11-17"

    files = []
    for city in cities:
        data = fetch_hotels(city, checkin, checkout)
        if data:
            file = save_data(city, data)
            files.append(file)
    return files
