from ..models.database.session import get_session
from .base_route import APIRouter, Depends, status
from ..controllers.attendance_controller import AttendanceController
from ..schemas.attendance_schema import (
    AttendanceConfirmSchema,
    AttendanceQRSchema,
    AttendanceResponseSchema,
)
from ..auth.dependencies import require_role, get_current_user


attendance_router = APIRouter(
    prefix="/attendances",
    tags=["attendances"]
)


# ─────────────────────────────────────────
# ADMIN — listar todas as presenças
# ─────────────────────────────────────────
@attendance_router.get("/all", response_model=list[AttendanceResponseSchema])
async def get_all(
    session=Depends(get_session),
    _=Depends(require_role("admin"))
):
    controller = AttendanceController(session)
    return controller.get_all()


# ─────────────────────────────────────────
# ADMIN — presenças de um aluno específico
# ─────────────────────────────────────────
@attendance_router.get("/student/{student_id}", response_model=list[AttendanceResponseSchema])
async def get_by_student(
    student_id: str,
    session=Depends(get_session),
    _=Depends(require_role("admin"))
):
    controller = AttendanceController(session)
    return controller.get_by_student(student_id)


# ─────────────────────────────────────────
# ADMIN — detalhes de uma presença
# ─────────────────────────────────────────
@attendance_router.get("/details/{attendance_id}", response_model=AttendanceResponseSchema)
async def get_by_id(
    attendance_id: str,
    session=Depends(get_session),
    _=Depends(require_role("admin"))
):
    controller = AttendanceController(session)
    return controller.get_by_id(attendance_id)


# ─────────────────────────────────────────
# ALUNO — gerar QR de entrada (chamado no login)
# ─────────────────────────────────────────
@attendance_router.post("/qr/entry", response_model=AttendanceQRSchema, status_code=status.HTTP_201_CREATED)
async def generate_entry_qr(
    session=Depends(get_session),
    current_user=Depends(get_current_user)
):
    controller = AttendanceController(session)
    return controller.generate_entry_qr(current_user.id)


# ─────────────────────────────────────────
# ALUNO — gerar QR de saída
# ─────────────────────────────────────────
@attendance_router.post("/qr/exit", response_model=AttendanceQRSchema)
async def generate_exit_qr(
    session=Depends(get_session),
    current_user=Depends(get_current_user)
):
    controller = AttendanceController(session)
    return controller.generate_exit_qr(current_user.id)


# ─────────────────────────────────────────
# ADMIN — confirmar entrada via token do QR
# ─────────────────────────────────────────
@attendance_router.post("/confirm/entry", response_model=AttendanceResponseSchema)
async def confirm_entry(
    data: AttendanceConfirmSchema,
    session=Depends(get_session),
    _=Depends(require_role("admin"))
):
    controller = AttendanceController(session)
    return controller.confirm_entry(data)


# ─────────────────────────────────────────
# ADMIN — confirmar saída via token do QR
# ─────────────────────────────────────────
@attendance_router.post("/confirm/exit", response_model=AttendanceResponseSchema)
async def confirm_exit(
    data: AttendanceConfirmSchema,
    session=Depends(get_session),
    _=Depends(require_role("admin"))
):
    controller = AttendanceController(session)
    return controller.confirm_exit(data)