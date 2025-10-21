import os
import requests
from dotenv import load_dotenv
from groq import Groq

# === Load API keys from .env ===
load_dotenv()
API_KEY = os.getenv("OPENWEATHER_API_KEY")
GROQ_KEY = os.getenv("grok_api")
groq_client = Groq(api_key=GROQ_KEY)

print("=" * 50)
print("🌤  Personal Weather Assistant v1.0")
print("=" * 50)

# === User input ===
city_input = input("Enter city name (or two cities separated by comma for travel comparison): ")

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

# === Single City Mode ===
if not travel_mode:
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&appid={API_KEY}&lang=en"
    response = requests.get(url)
    data = response.json()

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

    # === Activity Recommender ===
    prompt = (
        f"Current weather in {name}: {desc}, {temp}°C, humidity {humidity}%, wind {wind} m/s.\n"
        "Suggest 3 short, realistic activities someone could do today based on this weather. "
        "Avoid clothing advice, focus on fun or practical ideas."
    )

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
    url1 = f"https://api.openweathermap.org/data/2.5/weather?q={city1}&units=metric&appid={API_KEY}&lang=en"
    url2 = f"https://api.openweathermap.org/data/2.5/weather?q={city2}&units=metric&appid={API_KEY}&lang=en"

    data1 = requests.get(url1).json()
    data2 = requests.get(url2).json()

    name1, temp1, hum1, wind1 = data1["name"], data1["main"]["temp"], data1["main"]["humidity"], data1["wind"]["speed"]
    name2, temp2, hum2, wind2 = data2["name"], data2["main"]["temp"], data2["main"]["humidity"], data2["wind"]["speed"]

    print(f"\n{'=' * 50}")
    print(f"Travel Weather Comparison: {name1} vs {name2}")
    print("-" * 50)
    print(f"{name1}: {temp1}°C, {hum1}% humidity, {wind1} m/s wind")
    print(f"{name2}: {temp2}°C, {hum2}% humidity, {wind2} m/s wind")

    diff_temp = round(temp2 - temp1, 1)
    diff_hum = hum2 - hum1
    print(f"\nTemperature difference: {diff_temp}°C")
    print(f"Humidity difference: {diff_hum}%")
    print("=" * 50)

    # === AI Travel Recommendation ===
    prompt = (
        f"Compare weather for travel: {name1} ({temp1}°C, {hum1}% humidity, {wind1} m/s wind) "
        f"and {name2} ({temp2}°C, {hum2}% humidity, {wind2} m/s wind). "
        "Give a short, realistic travel recommendation: which city is better to visit now and why."
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
        f"You are helping a traveler going from {name1} to {name2}. "
        f"Destination weather: {desc_day}, {temp2}°C, humidity {hum2}%, wind {wind2} m/s. "
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

    exit()
