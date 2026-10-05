from fastapi import FastAPI

app = FastAPI(
    title="NETRA Vision  API",
    description="NETRA Vision API is a RESTful API that provides access to the NETRA Vision platform. It allows users to perform various operations such as image analysis, object detection, and more.",
    version="1.0.0",
)

@app.get("/")
async def read_root():
    return {
        "app_name": "NETRA Vision API",
        "description": "NETRA Vision API is a RESTful API that provides access to the NETRA Vision platform. It allows users to perform various operations such as image analysis, object detection, and more.",
        "version": "1.0.0",
        "endpoints": {
            "POST /analyze": "Analyze an image and return the results.",
            "POST /analyze/batch": "Analyze a batch of images and return the results.",
            "GET /analyze" : "Get all analyzed images and their results.",
            "GET /analyze/{image_id}": "Get the analysis results for a specific image by its ID.",
        }
    }