import os
import requests
from datetime import datetime
from dotenv import load_dotenv
from groq import Groq

# === Load API keys from .env ===
load_dotenv()
API_KEY = os.getenv("OPENWEATHER_API_KEY")
GROQ_KEY = os.getenv("grok_api")
groq_client = Groq(api_key=GROQ_KEY)

print("=" * 50)
print("🌤  Personal Weather Assistant v1.4")
print("=" * 50)

# === User input ===
city_input = input("Enter city name (or two cities separated by comma for travel comparison): ").strip()

# === Detect mode ===
if "," in city_input:
    cities = [c.strip() for c in city_input.split(",")]
    if len(cities) == 2:
        city1, city2 = cities
        travel_mode = True
    else:
        print("Please enter exactly two cities separated by a comma.")
        exit()
else:
    city = city_input or "Zagreb"
    travel_mode = False

# === Helper function for forecast ===
def get_forecast_for_date(city, date_str):
    forecast_url = f"https://api.openweathermap.org/data/2.5/forecast?q={city}&units=metric&appid={API_KEY}&lang=en"
    forecast_data = requests.get(forecast_url).json()
    if forecast_data.get("cod") != "200":
        return None

    for entry in forecast_data["list"]:
        if entry["dt_txt"].startswith(date_str):
            temp = entry["main"]["temp"]
            humidity = entry["main"]["humidity"]
            wind = entry["wind"]["speed"]
            desc = entry["weather"][0]["description"]
            return {"temp": temp, "humidity": humidity, "wind": wind, "desc": desc}
    return None

# === Single City Mode ===
if not travel_mode:
    # Validate city first
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&appid={API_KEY}&lang=en"
    response = requests.get(url)
    data = response.json()

    if data.get("cod") != 200:
        print("City not found. Please check the spelling and try again.")
        exit()

    # Ask for optional date
    date_input = input("Optional date (DD-MM) for forecast, press Enter for today: ").strip()

    adjusted_year = False
    if date_input:
        try:
            now = datetime.now()
            day, month = map(int, date_input.split("-"))
            forecast_date = datetime(now.year, month, day)
            if forecast_date < now:
                forecast_date = forecast_date.replace(year=now.year + 1)
                adjusted_year = True
            date_input = forecast_date.strftime("%Y-%m-%d")
        except ValueError:
            print("Invalid date format. Please use DD-MM (e.g., 23-10).")
            exit()

    if adjusted_year:
        print("(Note: Date automatically adjusted to next year.)")

    # === Forecast for that date ===
    if date_input:
        forecast = get_forecast_for_date(city, date_input)
        if not forecast:
            print("No forecast found for that date. Please check the range (max 5 days ahead).")
            exit()

        print()
        print("=" * 50)
        print(f"Weather forecast for {city.capitalize()} on {date_input}")
        print("-" * 50)
        print(f"Temperature: {forecast['temp']}°C")
        print(f"Humidity: {forecast['humidity']}%")
        print(f"Wind speed: {forecast['wind']} m/s")
        print(f"Conditions: {forecast['desc'].capitalize()}")
        print("=" * 50)

        prompt = (
            f"Weather forecast for {city.capitalize()} on {date_input}: "
            f"{forecast['desc']}, {forecast['temp']}°C, humidity {forecast['humidity']}%, wind {forecast['wind']} m/s.\n"
            "Suggest 3 short, realistic activities for that day (no clothing advice)."
        )

    else:
        # === Current weather ===
        name = data["name"]
        temp = data["main"]["temp"]
        humidity = data["main"]["humidity"]
        wind = data["wind"]["speed"]
        desc = data["weather"][0]["description"]

        print()
        print("=" * 50)
        print(f"Weather summary for {name}")
        print("-" * 50)
        print(f"Temperature: {temp}°C")
        print(f"Humidity: {humidity}%")
        print(f"Wind speed: {wind} m/s")
        print(f"Conditions: {desc.capitalize()}")
        print("=" * 50)

        prompt = (
            f"Current weather in {name}: {desc}, {temp}°C, humidity {humidity}%, wind {wind} m/s.\n"
            "Suggest 3 short, realistic activities based on this weather (no clothing advice)."
        )

    # === AI-generated activities ===
    response = groq_client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
    )

    activities = response.choices[0].message.content.strip()
    print("\n>>> Activity Recommendations <<<")
    print("-" * 50)
    print(activities)
    print("-" * 50)
    print()

# === Travel Assistant Mode ===
if travel_mode:
    date_input = input("Optional date (DD-MM) for forecast, press Enter for current comparison: ").strip()

    # Convert date if provided
    forecast_mode = False
    if date_input:
        try:
            now = datetime.now()
            day, month = map(int, date_input.split("-"))
            forecast_date = datetime(now.year, month, day)
            if forecast_date < now:
                forecast_date = forecast_date.replace(year=now.year + 1)
            date_input = forecast_date.strftime("%Y-%m-%d")
            forecast_mode = True
        except ValueError:
            print("Invalid date format. Please use DD-MM (e.g., 23-10).")
            exit()

    # === Fetch data ===
    if forecast_mode:
        data1 = get_forecast_for_date(city1, date_input)
        data2 = get_forecast_for_date(city2, date_input)
        if not data1 or not data2:
            print("No forecast available for one or both cities. Try a closer date (within 5 days).")
            exit()
        name1, name2 = city1.capitalize(), city2.capitalize()
    else:
        url1 = f"https://api.openweathermap.org/data/2.5/weather?q={city1}&units=metric&appid={API_KEY}&lang=en"
        url2 = f"https://api.openweathermap.org/data/2.5/weather?q={city2}&units=metric&appid={API_KEY}&lang=en"
        data1 = requests.get(url1).json()
        data2 = requests.get(url2).json()

        if data1.get("cod") != 200 or data2.get("cod") != 200:
            print("One or both cities not found. Please check spelling.")
            exit()

        name1, temp1, hum1, wind1 = data1["name"], data1["main"]["temp"], data1["main"]["humidity"], data1["wind"]["speed"]
        name2, temp2, hum2, wind2 = data2["name"], data2["main"]["temp"], data2["main"]["humidity"], data2["wind"]["speed"]
        data1 = {"temp": temp1, "humidity": hum1, "wind": wind1}
        data2 = {"temp": temp2, "humidity": hum2, "wind": wind2}

    # === Print comparison ===
    print(f"\n{'=' * 50}")
    print(f"Travel Weather Comparison: {city1.capitalize()} vs {city2.capitalize()}")
    print("-" * 50)
    print(f"{city1.capitalize()}: {data1['temp']}°C, {data1['humidity']}% humidity, {data1['wind']} m/s wind")
    print(f"{city2.capitalize()}: {data2['temp']}°C, {data2['humidity']}% humidity, {data2['wind']} m/s wind")

    diff_temp = round(data2["temp"] - data1["temp"], 1)
    diff_hum = data2["humidity"] - data1["humidity"]
    print(f"\nTemperature difference: {diff_temp}°C")
    print(f"Humidity difference: {diff_hum}%")
    print("=" * 50)

    # === AI Travel Recommendation ===
    prompt = (
        f"Compare weather for travel between {city1} ({data1['temp']}°C, {data1['humidity']}% humidity, {data1['wind']} m/s wind) "
        f"and {city2} ({data2['temp']}°C, {data2['humidity']}% humidity, {data2['wind']} m/s wind). "
        "Give a short, realistic travel recommendation: which city is better to visit and why."
    )

    response = groq_client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
    )

    advice = response.choices[0].message.content.strip()
    print("\n>>> Travel Recommendation <<<")
    print("-" * 50)
    print(advice)
    print("-" * 50)

    # === 3-Day Forecast for Destination ===
    print("\n>>> 3-Day Forecast for Destination <<<")
    print("-" * 50)

    forecast_url = f"https://api.openweathermap.org/data/2.5/forecast?q={city2}&units=metric&appid={API_KEY}&lang=en"
    forecast_data = requests.get(forecast_url).json()

    shown_dates = set()
    for entry in forecast_data["list"]:
        date = entry["dt_txt"].split(" ")[0]
        if date not in shown_dates:
            desc_day = entry["weather"][0]["description"]
            temp_day = entry["main"]["temp"]
            print(f"{date}: {temp_day}°C, {desc_day}")
            shown_dates.add(date)
        if len(shown_dates) >= 3:
            break
    print("-" * 50)

    # === Packing List (short AI suggestion) ===
    pack_prompt = (
        f"You are helping a traveler going from {city1.capitalize()} to {city2.capitalize()}. "
        f"Destination weather: {desc_day}, {data2['temp']}°C, humidity {data2['humidity']}%, wind {data2['wind']} m/s. "
        "Suggest 4–5 short, practical items to pack for this trip."
    )

    pack_response = groq_client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": pack_prompt}],
    )

    packing_list = pack_response.choices[0].message.content.strip()
    print("\n>>> Suggested Packing List <<<")
    print("-" * 50)
    print(packing_list)
    print("-" * 50)
    print()
