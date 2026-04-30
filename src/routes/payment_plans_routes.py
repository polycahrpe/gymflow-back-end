from ..models.database.session import get_session
from .base_route import APIRouter, Depends, status
from ..controllers.payment_plans_controller import PaymentPlansController
from ..schemas.payment_plans_schema import (
    PaymentPlansCreateSchema,
    PaymentPlansUpdateSchema,
    PaymentPlansGetSchema,
    PaymentPlansResponseSchema,
)
from ..auth.dependencies import require_role


payment_plans_router = APIRouter(
    prefix="/payment-plans",
    tags=["payment-plans"]
)


@payment_plans_router.get("/all", response_model=list[PaymentPlansResponseSchema])
async def get_all(
                    session=Depends(get_session),
                ):
    
    controller = PaymentPlansController(session)
    return controller.get_all()


@payment_plans_router.get("/details/{plan_id}", response_model=PaymentPlansGetSchema)
async def get_by_id(
                        plan_id: str, 
                        session=Depends(get_session),
                    ):
    
    controller = PaymentPlansController(session)
    return controller.get_by_id(plan_id)


@payment_plans_router.post("/create", response_model=PaymentPlansResponseSchema, status_code=status.HTTP_201_CREATED)
async def create(
                    data: PaymentPlansCreateSchema, 
                    session=Depends(get_session),
                    _=Depends(require_role("admin"))
                ):
    
    controller = PaymentPlansController(session)
    return controller.create(data)


@payment_plans_router.put("/update/{plan_id}", response_model=PaymentPlansResponseSchema)
async def update(
                    plan_id: str, 
                    data: PaymentPlansUpdateSchema, 
                    session=Depends(get_session),
                    _=Depends(require_role("admin"))
                ):
    
    controller = PaymentPlansController(session)
    return controller.update(plan_id, data)


@payment_plans_router.delete("/delete/{plan_id}", status_code=status.HTTP_200_OK)
async def delete(
                    plan_id: str, 
                    session=Depends(get_session),
                    _=Depends(require_role("admin"))
                ):
    
    controller = PaymentPlansController(session)
    return controller.delete(plan_id)