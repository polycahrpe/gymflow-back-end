from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .auth.login_route import login_router
from .routes.coach_routes import coach_router
from .routes.student_routes import student_router
from .routes.payment_routes import payment_router
from .routes.presence_routes import presence_router
from .routes.training_routes import training_router
from .routes.payment_plans_routes import payment_plans_router

app = FastAPI()

app = FastAPI(
    title="GymFlow API",
    description="API for managing gym workouts and exercises",
    version="1.0.0"
)

app.include_router(login_router)
app.include_router(coach_router)
app.include_router(student_router)
app.include_router(payment_router)
app.include_router(presence_router)
app.include_router(training_router)
app.include_router(payment_plans_router)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)