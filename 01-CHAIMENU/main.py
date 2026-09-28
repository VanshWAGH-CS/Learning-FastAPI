from fastapi import FastAPI, Query, HTTPException
from models import MenuItem, MenuResponse
from data import menu_item

app = FastAPI(
    title="Chai Menu API",
    description="An API for managing a menu of chai (tea) items.",
)

@app.get("/")
def root():
    return {"message": "Welcome to the Chai Menu API!"}

@app.get("/menu", response_model=MenuResponse)
def get_menu(category: str | None = Query(None, description="Filter by chai, snack or combo")):
    if category:
        filtered = [item for item in menu_item if item["category"].lower() == category.lower()]
        if not filtered:
            raise HTTPException(status_code=404, detail=f"No items found in category '{category}'")
    else:
        filtered = menu_item

    return MenuResponse(
        status="success",
        count=len(filtered),
        items=filtered
    )


@app.get("/menu/{item_id}", response_model=MenuItem)
def get_item(item_id: int):
    for item in menu_item:
        if(item["id"] == item_id):
            return item
    raise HTTPException(status_code=404, detail=f"Item with id {item_id} not found")

