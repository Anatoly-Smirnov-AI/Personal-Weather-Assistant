# Personal Weather Assistant

> Version 1.4 — travel-by-date (DD-MM), smart year handling.

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

- **Input validation:**  
  Handles misspelled or unknown city names gracefully and shows a clear message instead of crashing.

- **Travel-by-date (optional):**  
  When two cities are provided, you can also enter a date (DD-MM) to compare the forecast for that day (up to 5 days ahead). If no date is entered, the app compares current conditions.

- **European date format (DD-MM) with smart year handling:**  
  If the chosen date has already passed this year, the app automatically shifts it to the next year. (OpenWeatherMap provides forecast data for ~5 days ahead, so the date must fall within that window.)


---

## Example usage

**1️⃣ Single city with date (DD-MM)**

Enter city name (or two cities separated by comma for travel comparison): Zagreb  
Optional date (DD-MM) for forecast, press Enter for today: 22-10

Weather forecast for Zagreb on 2025-10-22  
Temperature: 16°C  
Humidity: 64%  
Wind speed: 2.8 m/s  
Conditions: Scattered clouds

Activity Recommendations:
- Take a short city walk
- Visit a museum or gallery
- Enjoy a coffee indoors


**2️⃣ Travel comparison with a specific date (DD-MM)**

Enter city name (or two cities separated by comma for travel comparison): Zagreb, Moscow  
Optional date (DD-MM) for forecast, press Enter for current comparison: 23-10

Travel Weather Comparison: Zagreb vs Moscow  
Zagreb: 13.2°C, 88% humidity, 1.1 m/s wind  
Moscow: 6.0°C, 89% humidity, 0.3 m/s wind

Travel Recommendation:
Zagreb is milder and better for outdoor plans on that date; Moscow is notably colder.

3-Day Forecast for Destination:
2025-10-21: 4.8°C, overcast clouds  
2025-10-22: 5.1°C, light rain  
2025-10-23: 6.0°C, overcast clouds

Suggested Packing List:
- Light waterproof jacket  
- Comfortable walking shoes  
- Compact umbrella  
- Warm layer for evenings  
- Small daypack


**3️⃣ Handling typos**

Enter city name (or two cities separated by comma for travel comparison): Zaagreb

City not found. Please check the spelling and try again.


---

## Installation

1. **Clone or download** the project folder.  
2. Inside the main folder, create a file called `.env` and add your API keys:

# .env
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
- **Version:** 1.4 (travel-by-date, DD-MM input, smart year handling)

---

## Useful info
- The `.env` file should never be shared publicly.  
- Use `.env.example` as a template to create your own configuration.  
```markdown
- You can copy `.env.example` → `.env` and fill in your own API keys.
- Free tiers of both APIs are sufficient for testing.
- The app validates city names and shows a friendly error if a city is not found.
- Date input uses the European format `DD-MM`. The app automatically adjusts the year if the date has already passed this year.
- Forecast data is limited to ~5 days ahead by the OpenWeatherMap free API. Pick dates within this window.

---

## Author
Created by **Anatoly Smirnov**, developed while learning API integration.  
This was my first project that combines API data and AI logic.  
I built it step by step to learn how APIs and Python can work together.
