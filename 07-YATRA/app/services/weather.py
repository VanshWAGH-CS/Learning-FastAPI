from datetime import datetime
from models import WeatherDataModel
import httpx
from services.cache import get_cache, set_cache


async def fetch_weather_data(destination: str, start_date: str, end_date: str) -> list[WeatherDataModel]:
    cache_key = f"{destination}_{start_date}_{end_date}"
    cached_data = get_cache(cache_key)
    if cached_data:
        return [WeatherDataModel(**item) for item in cached_data]

    """
    Fetch weather data for the given destination and date range.
    """
    try:
        start_dt = datetime.strptime(start_date, "%Y-%m-%d")
        end_dt = datetime.strptime(end_date, "%Y-%m-%d")
    except ValueError as exc:
        raise ValueError("Dates must be in YYYY-MM-DD format") from exc

    days = (end_dt - start_dt).days + 1

    async with httpx.AsyncClient() as client:
        response = await client.get(
            "https://api.weatherapi.com/v1/forecast.json",
            params={
                "key": "YOUR_API_KEY",
                "q": destination,
                "days": days,
            },
            timeout=10.0,
        )
        if response.status_code != 200:
            raise Exception("Failed to fetch weather data")
        data = response.json()

    weather_data_list: list[WeatherDataModel] = []
    for day in data["forecast"]["forecastday"]:
        weather_data = WeatherDataModel(
            destination=destination,
            start_date=datetime.strptime(day["date"], "%Y-%m-%d").date(),
            end_date=datetime.strptime(day["date"], "%Y-%m-%d").date(),
            weather_summary=day["day"]["condition"]["text"],
            temperature_range=f"{day['day']['mintemp_c']}°C - {day['day']['maxtemp_c']}°C",
            rainfall_probability=day["day"]["daily_chance_of_rain"],
        )
        weather_data_list.append(weather_data)

    # Cache the fetched weather data
    set_cache(cache_key, [weather.dict() for weather in weather_data_list])
    # Cache the fetched data; this code runs only on a cache miss.
    return weather_data_list
  