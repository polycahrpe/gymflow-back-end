from fastapi import APIRouter, Depends, status
from ..models.database.session import get_session
from ..controllers.attendance_controller import AttendanceController
from ..schemas.attendance_schema import (
    AttendanceMarkEntrySchema,
    AttendanceMarkExitSchema,
    AttendanceResponseSchema,
)
from ..auth.dependencies import require_role

attendance_router = APIRouter(prefix="/attendances", tags=["attendances"])


# ADMIN — listar todas as presenças
@attendance_router.get("/all", response_model=list[AttendanceResponseSchema])
async def get_all(session=Depends(get_session), _=Depends(require_role("admin"))):
    controller = AttendanceController(session)
    return controller.get_all()


# ADMIN / COACH — presenças por aluno
@attendance_router.get("/student/{student_id}", response_model=list[AttendanceResponseSchema])
async def get_by_student(student_id: str, session=Depends(get_session), _=Depends(require_role("admin", "coach"))):
    controller = AttendanceController(session)
    return controller.get_by_student(student_id)


# ADMIN / COACH — presença de hoje por aluno
@attendance_router.get("/today/{student_id}", response_model=AttendanceResponseSchema)
async def get_today(student_id: str, session=Depends(get_session), _=Depends(require_role("admin", "coach", "student"))):
    controller = AttendanceController(session)
    return controller.get_today_by_student(student_id)


# ADMIN — presença por ID
@attendance_router.get("/details/{attendance_id}", response_model=AttendanceResponseSchema)
async def get_by_id(attendance_id: str, session=Depends(get_session), _=Depends(require_role("admin"))):
    controller = AttendanceController(session)
    return controller.get_by_id(attendance_id)


# ALUNO — marcar entrada
@attendance_router.post("/entry/mark", response_model=AttendanceResponseSchema, status_code=status.HTTP_201_CREATED)
async def mark_entry(data: AttendanceMarkEntrySchema, session=Depends(get_session), _=Depends(require_role("student"))):
    controller = AttendanceController(session)
    return controller.mark_entry(data)


# ADMIN — confirmar entrada
@attendance_router.patch("/entry/confirm/{attendance_id}", response_model=AttendanceResponseSchema)
async def confirm_entry(attendance_id: str, session=Depends(get_session), _=Depends(require_role("admin"))):
    controller = AttendanceController(session)
    return controller.confirm_entry(attendance_id)


# ALUNO — marcar saída
@attendance_router.post("/exit/mark", response_model=AttendanceResponseSchema)
async def mark_exit(data: AttendanceMarkExitSchema, session=Depends(get_session), _=Depends(require_role("student"))):
    controller = AttendanceController(session)
    return controller.mark_exit(data)


# ADMIN — confirmar saída
@attendance_router.patch("/exit/confirm/{attendance_id}", response_model=AttendanceResponseSchema)
async def confirm_exit(attendance_id: str, session=Depends(get_session), _=Depends(require_role("admin"))):
    controller = AttendanceController(session)
    return controller.confirm_exit(attendance_id)