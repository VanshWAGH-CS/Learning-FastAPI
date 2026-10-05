from fastapi import FastAPI

from routes.planner import router as planner_router

app = FastAPI(
    title="The Yatra planner API",
    description="Aggregate travel data from multiple sources and provide a unified interface for planning trips.",
    version="1.0.0",
)




@app.get("/", tags=["Root"])
async def root():
    return {
        "app": "The Yatra planner API",
        "version": "1.0.0",
        "endpoint": {
            "POST/plan": "Create a travel plan",
            "GET/plan/stream": "Stream travel plan updates",
            "GET/plan/cache-stats": "Get cache statistics",
            "DELETE/plan/cache": "Clear cache"
        }
    }

app.include_router(planner_router)  