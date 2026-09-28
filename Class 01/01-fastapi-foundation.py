from fastapi import FastAPI
from fastapi import Request
import uvicorn

app = FastAPI(

    title="Swiggy Order Service",
    description=(
        "This is a sample FastAPI application that demonstrates the use of FastAPI for building a simple web service. "
        "The application provides a single endpoint that returns a greeting message. "
    ),
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)

@app.get("/")  # decorator
def read_root():
    """Root endpoint that returns a greeting message. -- Healthy and simple."""

    #Fast api converts this dictionary to JSON automatically
    return {"message": "Welcome to the Swiggy Order Service!", "status": "healthy"}


@app.get("/about")
def about():
    """About endpoint that provides information about the service."""

    return {
        "service": "Swiggy Order Service",
        "version": "1.0.0",
        "description": "This service handles order processing for Swiggy.",
    }


@app.get("/orders")
def get_orders():
    """List of orders"""
    return {"orders": [
        {"id0": 1, "item": "Butter Chicken", "Status": "Delivered"},
        {"id1": 2, "item": "Paneer Tikka", "Status": "In Progress"},
        {"id2": 3, "item": "Veg Biryani", "Status": "Pending"},


    ]}

@app.get("/orders/status")
def get_order_status(order_id: int):
    """Get the status of a specific order by its ID."""
    # In a real application, you would fetch this from a database
    orders = {
        1: "Delivered",
        2: "In Progress",
        3: "Pending"
    }
    status = orders.get(order_id, "Order not found")
    return {"order_id": order_id, "status": status}


@app.get("/debug/request-info")
async def request_info(request: Request):
    """Inspects the raw request object"""
    return {
        "method": request.method,
        "url": str(request.url),
        "headers": dict(request.headers),
        "client": request.client.host if request.client else None,
    }


@app.get(
    "/orders/activate",
    summary="Get the status of a specific order by its ID.",
    description=(
        "This endpoint allows you to activate an order by providing its ID. "
        "In a real application, this would trigger the order processing logic."
    ),
    tags=["orders"],
    response_description="List of orders with their statuses.",
    deprecated=False,

)

def activate_order(order_id: int):
    """Activate an order by its ID."""
    # In a real application, you would implement the activation logic here
    return {"order_id": order_id, "status": "Activated"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
