import requests
from functools import lru_cache

@lru_cache(maxsize=32)
def get_current_weather(city_name: str, api_key: str) -> str:
    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city_name,
        "appid": api_key,
        "units": "metric",
        "lang": "en"
    }

    try:
        response = requests.get(url, params=params, timeout=8)
        data = response.json()

        if response.status_code == 404 or str(data.get("cod")) == "404":
            return f"Sorry, I couldn't find weather data for '{city_name}'. Please check the spelling."

        if response.status_code != 200:
            return "Weather service is temporarily unavailable. Please try again later."

        main = data["main"]
        weather = data["weather"][0]
        wind = data.get("wind", {})
        sys = data.get("sys", {})

        city = data.get("name", city_name)
        country = sys.get("country", "")
        temp = main["temp"]
        feels_like = main.get("feels_like", temp)
        humidity = main["humidity"]
        description = weather["description"].capitalize()
        wind_speed = wind.get("speed", 0)

        return (
            f"📍 {city}, {country}\n"
            f"🌡️ Temperature: {temp}°C (feels like {feels_like}°C)\n"
            f"☁️ Condition: {description}\n"
            f"💧 Humidity: {humidity}%\n"
            f"💨 Wind: {wind_speed} m/s"
        )

    except requests.exceptions.Timeout:
        return "The weather service took too long to respond. Please try again."
    except requests.exceptions.RequestException:
        return "Network error while fetching weather data."
    except Exception:
        return "Something went wrong while getting the weather."


def get_forecast(city_name: str, api_key: str, days: int = 5) -> str:
    url = "https://api.openweathermap.org/data/2.5/forecast"
    params = {
        "q": city_name,
        "appid": api_key,
        "units": "metric",
        "lang": "en"
    }

    try:
        response = requests.get(url, params=params, timeout=8)
        data = response.json()

        if response.status_code == 404 or str(data.get("cod")) == "404":
            return f"Sorry, I couldn't find forecast data for '{city_name}'."

        if response.status_code != 200:
            return "Forecast service is temporarily unavailable."

        city = data["city"]["name"]
        country = data["city"].get("country", "")
        forecast_list = data["list"]

        # Group by day (prefer midday entries)
        daily = {}
        for entry in forecast_list:
            date = entry["dt_txt"].split(" ")[0]
            time = entry["dt_txt"].split(" ")[1]
            if date not in daily and time.startswith("12"):
                daily[date] = entry
            elif date not in daily:
                daily[date] = entry

        lines = [f"📅 5-Day Forecast for {city}, {country}:\n"]
        count = 0
        for date, entry in daily.items():
            if count >= days:
                break
            temp = entry["main"]["temp"]
            desc = entry["weather"][0]["description"].capitalize()
            lines.append(f"• {date}: {temp}°C, {desc}")
            count += 1

        return "\n".join(lines)

    except requests.exceptions.RequestException:
        return "Network error while fetching the forecast."
    except Exception:
        return "Something went wrong while getting the forecast."