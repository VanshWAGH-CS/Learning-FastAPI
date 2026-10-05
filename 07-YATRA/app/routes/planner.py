from fastapi import APIRouter, HTTPException
from app.model.model import TravelRequestModel
from services.weather_service import get_weather_data 


router = APIRouter(
    prefix="/planner", 
    tags=["Planner"],
    responses={404: {"description": "Not found"}},
)

@router.post("/", summary="Create a travel plan")
async def create_travel_plan(
    travel_request: TravelRequestModel
):
    """Agregate travel data from multiple sources and provide a unified interface for planning trips."""

    if travel_request.start_date > travel_request.end_date:
        raise HTTPException(status_code=400, detail="Start date cannot be after end date")

    trip_days = (travel_request.end_date - travel_request.start_date).days

    if trip_days <= 0:
        raise HTTPException(status_code=400, detail="Trip duration must be at least one day")

    weather_data = await get_weather_data(
        travel_request.destination,
        travel_request.start_date,
        travel_request.end_date
    )
    return {
        "message": "Travel plan created successfully",
    }

