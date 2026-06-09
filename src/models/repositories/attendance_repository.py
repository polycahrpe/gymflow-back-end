from .base_repository import HTTPException, status, Session
from datetime import datetime, date
from sqlalchemy.orm import joinedload
from ..entities.attendance_entity import AttendanceEntity, AttendanceStatus
from ..entities.student_entity import StudentEntity
from ...schemas.attendance_schema import AttendanceMarkEntrySchema, AttendanceMarkExitSchema


class AttendanceRepository:
    def __init__(self, my_session: Session):
        self.session = my_session

    def get_all(self):
        return (
            self.session.query(AttendanceEntity)
            .options(joinedload(AttendanceEntity.student))
            .order_by(AttendanceEntity.data.desc())
            .all()
        )

    def get_by_student(self, student_id: str):
        return (
            self.session.query(AttendanceEntity)
            .options(joinedload(AttendanceEntity.student))
            .filter(AttendanceEntity.student_id == student_id)
            .order_by(AttendanceEntity.data.desc())
            .all()
        )

    def get_today_by_student(self, student_id: str):
        return (
            self.session.query(AttendanceEntity)
            .options(joinedload(AttendanceEntity.student))
            .filter(
                AttendanceEntity.student_id == student_id,
                AttendanceEntity.data == date.today()
            )
            .first()
        )

    def get_by_id(self, id: str):
        attendance = (
            self.session.query(AttendanceEntity)
            .options(joinedload(AttendanceEntity.student))
            .filter(AttendanceEntity.id == id)
            .first()
        )
        if not attendance:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Presença não encontrada."
            )
        return attendance

    def mark_entry(self, data: AttendanceMarkEntrySchema):
        existente = self.get_today_by_student(data.student_id)
        if existente:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Já marcaste presença hoje."
            )

        attendance = AttendanceEntity(
            student_id=data.student_id,
            data=data.data,
            hora_entrada=data.hora_entrada,
            status=AttendanceStatus.pendente_entrada,
        )

        self.session.add(attendance)
        self.session.commit()
        self.session.refresh(attendance)
        return self.get_by_id(attendance.id)

    def confirm_entry(self, attendance_id: str):
        attendance = self.get_by_id(attendance_id)

        if attendance.status != AttendanceStatus.pendente_entrada:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Esta presença não está pendente de confirmação de entrada."
            )

        attendance.status = AttendanceStatus.presente
        attendance.confirmado_entrada_em = datetime.now()

        self.session.commit()
        self.session.refresh(attendance)
        return self.get_by_id(attendance.id)

    def mark_exit(self, data: AttendanceMarkExitSchema):
        attendance = self.get_today_by_student(data.student_id)

        if not attendance:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Não tens nenhuma entrada registada hoje."
            )

        if attendance.status != AttendanceStatus.presente:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="A tua entrada ainda não foi confirmada pelo admin."
            )

        attendance.hora_saida = data.hora_saida
        attendance.status = AttendanceStatus.pendente_saida

        self.session.commit()
        self.session.refresh(attendance)
        return self.get_by_id(attendance.id)

    def confirm_exit(self, attendance_id: str):
        attendance = self.get_by_id(attendance_id)

        if attendance.status != AttendanceStatus.pendente_saida:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Esta presença não está pendente de confirmação de saída."
            )

        attendance.status = AttendanceStatus.saiu
        attendance.confirmado_saida_em = datetime.now()

        self.session.commit()
        self.session.refresh(attendance)
        return self.get_by_id(attendance.id)