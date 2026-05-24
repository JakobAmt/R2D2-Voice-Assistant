import requests
from config import OPENWEATHER_API_KEY, WEATHER_CITY, WEATHER_UNITS

def get_weather():
    try:
        url = "https://api.openweathermap.org/data/2.5/weather"
        params = {
            "q": WEATHER_CITY,
            "appid": OPENWEATHER_API_KEY,
            "units": WEATHER_UNITS,
        }
        response = requests.get(url, params=params)
        data = response.json()

        if response.status_code != 200:
            return "I couldn't fetch the weather right now."

        city = data["name"]
        temp = round(data["main"]["temp"])
        feels_like = round(data["main"]["feels_like"])
        description = data["weather"][0]["description"]
        humidity = data["main"]["humidity"]
        wind = round(data["wind"]["speed"])

        return (
            f"Current weather in {city}: {description}, "
            f"{temp} degrees with a feels like of {feels_like}. "
            f"Humidity is {humidity} percent and wind speed is {wind} meters per second."
        )

    except Exception as e:
        print(f"Weather error: {e}")
        return "I had trouble fetching the weather."