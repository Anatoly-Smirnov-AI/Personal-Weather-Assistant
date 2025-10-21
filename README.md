# Personal Weather Assistant

I built this project to practice working with APIs and integrate AI into a practical everyday tool.  
A simple AI-powered weather assistant that combines live data from **OpenWeatherMap** with smart analysis from the **Groq API**.  
It provides short weather summaries, activity suggestions, and travel comparisons — all from the command line.

---

## Features

- **Single-city mode:**  
  Get the current temperature, humidity, wind speed, and a short description of the weather.  
  The assistant then suggests 3 realistic activities suited for the day.

- **Travel mode:**  
  Enter two cities separated by a comma to compare their weather.  
  In this mode, the assistant compares key weather data, tells which city is better to visit, and even suggests what to pack.  
  It also shows a short 3-day forecast for the destination.

---

## Example usage

**1️⃣ Single city**

Enter city name (or two cities separated by comma for travel comparison): Zagreb

Weather summary for Zagreb
Temperature: 15°C
Humidity: 60%
Wind speed: 3.4 m/s
Conditions: Clear sky

Activity Recommendations:

Take a walk by the river

Visit a local market

Enjoy a coffee outside


**2️⃣ Travel comparison**

Enter city name (or two cities separated by comma for travel comparison): Zagreb, Split

Travel Weather Comparison: Zagreb vs Split
Zagreb: 12°C, 68% humidity, 2.1 m/s wind
Split: 18°C, 72% humidity, 1.8 m/s wind

Travel Recommendation:
Split is warmer and ideal for outdoor walks, while Zagreb is better for cozy indoor spots.

3-Day Forecast for Destination:
2025-10-22: 18°C, scattered clouds
2025-10-23: 17°C, light rain
2025-10-24: 19°C, clear sky

Suggested Packing List:

Light jacket

Sunglasses

Comfortable shoes

Small backpack

Portable charger


---

## Installation

1. **Clone or download** the project folder.  
2. Inside the main folder, create a file called `.env` and add your API keys:

OPENWEATHER_API_KEY=your_openweather_api_key_here
grok_api=your_groq_api_key_here

3. Install the required Python packages:
pip install requests python-dotenv groq

4. Run the assistant:
python weather_summary.py


---

## Built with
- **Language:** Python  
- **APIs:** OpenWeatherMap (for weather data), Groq (for LLM analysis)  
- **Environment:** CLI app  

---

## Useful info
- The `.env` file should never be shared publicly.  
- Use `.env.example` as a template to create your own configuration.  
- Free tiers of both APIs are sufficient for testing.

---

## Author
Created by **Anatoly Smirnov**, developed while learning API integration.  
This was my first project that combines API data and AI logic.  
I built it step by step to learn how APIs and Python can work together.
