from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routes.main_routes import main_routes

app = FastAPI()

app = FastAPI(
    title="GymFlow API",
    description="API for managing gym workouts and exercises",
    version="1.0.0"
)

app.include_router(main_routes)



app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)