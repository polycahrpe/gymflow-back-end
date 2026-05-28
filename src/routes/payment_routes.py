from fastapi import APIRouter, Depends, status
from ..models.database.session import get_session
from ..controllers.payment_controller import PaymentController
from ..schemas.payment_schema import PaymentCreateSchema, PaymentUpdateSchema, PaymentResponseSchema
from ..auth.dependencies import require_role

payment_router = APIRouter(prefix="/payments", tags=["payments"])


@payment_router.get("/all", response_model=list[PaymentResponseSchema])
async def get_all(session=Depends(get_session), _=Depends(require_role("admin"))):
    controller = PaymentController(session)
    return controller.get_all()


@payment_router.get("/student/{student_id}", response_model=list[PaymentResponseSchema])
async def get_by_student(student_id: str, session=Depends(get_session), _=Depends(require_role("admin"))):
    controller = PaymentController(session)
    return controller.get_by_student(student_id)


@payment_router.get("/details/{payment_id}", response_model=PaymentResponseSchema)
async def get_by_id(payment_id: str, session=Depends(get_session), _=Depends(require_role("admin"))):
    controller = PaymentController(session)
    return controller.get_by_id(payment_id)


@payment_router.post("/create", response_model=PaymentResponseSchema, status_code=status.HTTP_201_CREATED)
async def create(data: PaymentCreateSchema, session=Depends(get_session), _=Depends(require_role("admin"))):
    controller = PaymentController(session)
    return controller.create(data)


@payment_router.put("/update/{payment_id}", response_model=PaymentResponseSchema)
async def update(payment_id: str, data: PaymentUpdateSchema, session=Depends(get_session), _=Depends(require_role("admin"))):
    controller = PaymentController(session)
    return controller.update(payment_id, data)


@payment_router.delete("/delete/{payment_id}", status_code=status.HTTP_200_OK)
async def delete(payment_id: str, session=Depends(get_session), _=Depends(require_role("admin"))):
    controller = PaymentController(session)
    return controller.delete(payment_id)