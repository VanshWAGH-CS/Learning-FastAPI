from fastapi import FastAPI
from database import init_db
from routes.contracts import router as contracts_router


app = FastAPI(
    title="Vakeel Contracts API",
    description="AI Powered legal contracts anaylysis and generation",
    version="1.0.0",
)

@app.on_event("startup")
async def startup_event():
    init_db() # Initialize the database and create indexes

@app.get("/")
async def root():
    return {
        "app": "Vakeel Contracts API",
        "version": "1.0.0",
        "endpoints": {
            "POST /contracts/upload": "Upload a contract for analysis",
            "GET /contracts/": "Retrieve a list of uploaded contracts",
            "GET /contracts/{id}": "Retrieve details of a specific contract",
            "POST /analysis/{contract_id}": "Analyze a contract using AI",
            "GET /analysis/{analysis_id}": "Analyze a contract using AI",
            "GET /analysis/contract/{contract_id}": "Retrieve analysis results for a specific contract",
        }
    }

app.include_router(contracts_router)