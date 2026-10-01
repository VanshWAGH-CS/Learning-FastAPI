from fastapi import FastAPI

from database import create_db_and_tables
from routes.orders import router as orders_router
from routes.stat import router as stats_router

app = FastAPI(
    title="DABBA Order Management API",
    version="1.0.0",
    description="A simple FastAPI service for creating, tracking, and updating orders.",
)


@app.on_event("startup")
def startup():
    create_db_and_tables()


app.include_router(orders_router)
app.include_router(stats_router)


@app.get("/")
def read_root():
    return {"message": "DABBA order management API is running", "status": "ok"}
