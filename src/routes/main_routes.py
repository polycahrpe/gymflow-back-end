from fastapi import APIRouter

from .payment_plans_routes import payment_plans_router
from .coach_routes import coach_router
from .student_routes import student_router
from ..auth.login_route import login_router
from .payment_route import payment_router
from .attendance_route import attendance_router
from .access_code_routes import access_code_router

main_routes = APIRouter()


main_routes.include_router(login_router)
main_routes.include_router(coach_router)
main_routes.include_router(student_router)
main_routes.include_router(payment_router)
main_routes.include_router(attendance_router)
main_routes.include_router(access_code_router)
main_routes.include_router(payment_plans_router)