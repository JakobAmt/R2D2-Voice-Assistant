import requests
from config import OPENWEATHER_API_KEY

DEFAULT_CITY = "Bekkestua"

def get_weather(city=None):
    if city is None:
        city = DEFAULT_CITY
    try:
        url = "https://api.openweathermap.org/data/2.5/weather"
        params = {
            "q": city,
            "appid": OPENWEATHER_API_KEY,
            "units": "metric",
        }
        response = requests.get(url, params=params)
        data = response.json()

        if response.status_code != 200:
            return f"I couldn't fetch the weather for {city}."

        city_name = data["name"]
        temp = round(data["main"]["temp"])
        feels_like = round(data["main"]["feels_like"])
        description = data["weather"][0]["description"]
        humidity = data["main"]["humidity"]
        wind = round(data["wind"]["speed"])

        return (
            f"Current weather in {city_name}: {description}, "
            f"{temp} degrees. "
            f"Humidity is {humidity} percent and wind speed is {wind} meters per second."
        )

    except Exception as e:
        print(f"Weather error: {e}")
        return "I had trouble fetching the weather."