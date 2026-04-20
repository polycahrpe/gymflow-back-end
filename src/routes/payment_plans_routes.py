from fastapi import APIRouter
from ..models.entities.payment_plans_entity import PaymentPlanCreate


payment_plans_router = APIRouter(
    prefix="/payment-plans",
    tags=["payment-plans"]
)

@payment_plans_router.get("/all")
async def get_all():
    return {
    "message": "List of all payment plans",
    "plans": [
            {"id": 1, "name": "Basic Plan", "price": 9.99},
            {"id": 2, "name": "Standard Plan", "price": 19.99},
            {"id": 3, "name": "Premium Plan", "price": 29.99}
        ]   
    } 


@payment_plans_router.get("/details/{plan_id}")
async def get_by_id(plan_id: int):
    return {"message": f"Details of payment plan with ID {plan_id}"}    


@payment_plans_router.post("/create")
async def create(plan: PaymentPlanCreate):  
    return {"message": "Payment plan created", "plan": plan}


@payment_plans_router.put("/update/{plan_id}")
async def update(plan_id: int, plan: dict):
    return {"message": f"Payment plan with ID {plan_id} updated", "plan": plan}


@payment_plans_router.delete("/delete/{plan_id}")
async def delete(plan_id: int):
    return {"message": f"Payment plan with ID {plan_id} deleted"}       


