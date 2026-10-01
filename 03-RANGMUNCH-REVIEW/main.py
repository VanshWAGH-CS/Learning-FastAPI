from contextlib import asynccontextmanager
from fastapi import FastAPI
from databse import table, get_session, create_tables
from routes.reviews import router as reviews_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_tables()  # Create tables when the application starts
    print("Tables created successfully.")
    yield
    #shutdown and cleanups
    print("Application shutdown. Cleanup done.")

app = FastAPI(
    title="RangMunch Review API",
    description="An API for managing reviews of RangMunch plays.",
    lifespan=lifespan
)

app.include_router(reviews_router)

app.get("/")
def root():
    return {"message": "Welcome to the RangMunch Review API!"}