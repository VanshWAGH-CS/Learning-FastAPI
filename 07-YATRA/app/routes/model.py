from pydantic import BaseModel
from datetime import date

class TravelRequestModel(BaseModel):
    destination: str
    start_date: date
    end_date: date
    traveler_name: str
    traveler_email: str

class WeatherDataModel(BaseModel):
    destination: str
    start_date: date
    end_date: date
    weather_summary: str
    temperature_range: str
    rainfall_probability: float