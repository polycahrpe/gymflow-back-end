from .base_repository import HTTPException, status, Session
from datetime import datetime, timedelta, date
from ..entities.attendance_entity import AttendanceEntity, AttendanceStatus


QR_EXPIRY_MINUTES = 30


class AttendanceRepository:
    def __init__(self, my_session: Session):
        self.session = my_session

    # ─────────────────────────────────────────
    # GET ALL
    # ─────────────────────────────────────────
    def get_all(self):
        return self.session.query(AttendanceEntity).all()

    # ─────────────────────────────────────────
    # GET ALL BY STUDENT
    # ─────────────────────────────────────────
    def get_by_student(self, student_id: str):
        return self.session.query(AttendanceEntity).filter(
            AttendanceEntity.student_id == student_id
        ).all()

    # ─────────────────────────────────────────
    # GET BY ID
    # ─────────────────────────────────────────
    def get_by_id(self, id: str):
        attendance = self.session.query(AttendanceEntity).filter(
            AttendanceEntity.id == id
        ).first()

        if not attendance:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Presença não encontrada."
            )

        return attendance

    # ─────────────────────────────────────────
    # GET BY TOKEN
    # ─────────────────────────────────────────
    def get_by_token(self, token: str):
        attendance = self.session.query(AttendanceEntity).filter(
            AttendanceEntity.token == token
        ).first()

        if not attendance:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="QR code inválido."
            )

        return attendance

    # ─────────────────────────────────────────
    # GERAR QR DE ENTRADA
    # Chamado quando o aluno faz login
    # ─────────────────────────────────────────
    def generate_entry_qr(self, student_id: str):
        # Verifica se já existe uma presença aberta hoje
        hoje = date.today()
        existente = self.session.query(AttendanceEntity).filter(
            AttendanceEntity.student_id == student_id,
            AttendanceEntity.data == hoje,
            AttendanceEntity.status.in_([
                AttendanceStatus.pendente_entrada,
                AttendanceStatus.presente,
                AttendanceStatus.pendente_saida,
            ])
        ).first()

        if existente:
            # Renova o token se já expirou
            if existente.token_expira_em < datetime.now():
                from uuid import uuid4
                existente.token = str(uuid4())
                existente.token_expira_em = datetime.now() + timedelta(minutes=QR_EXPIRY_MINUTES)
                self.session.commit()
                self.session.refresh(existente)
            return existente

        attendance = AttendanceEntity(
            student_id=student_id,
            data=hoje,
            token_expira_em=datetime.now() + timedelta(minutes=QR_EXPIRY_MINUTES),
            status=AttendanceStatus.pendente_entrada,
        )

        self.session.add(attendance)
        self.session.commit()
        self.session.refresh(attendance)

        return attendance

    # ─────────────────────────────────────────
    # CONFIRMAR ENTRADA (admin)
    # ─────────────────────────────────────────
    def confirm_entry(self, token: str):
        attendance = self.get_by_token(token)

        if attendance.status != AttendanceStatus.pendente_entrada:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Este QR code não é válido para confirmar entrada."
            )

        if attendance.token_expira_em < datetime.now():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="QR code expirado. O aluno deve gerar um novo."
            )

        agora = datetime.now()
        attendance.status = AttendanceStatus.presente
        attendance.hora_entrada = agora.time()
        attendance.confirmado_entrada_em = agora

        self.session.commit()
        self.session.refresh(attendance)

        return attendance

    # ─────────────────────────────────────────
    # GERAR QR DE SAÍDA
    # Chamado quando o aluno quer sair
    # ─────────────────────────────────────────
    def generate_exit_qr(self, student_id: str):
        hoje = date.today()
        attendance = self.session.query(AttendanceEntity).filter(
            AttendanceEntity.student_id == student_id,
            AttendanceEntity.data == hoje,
            AttendanceEntity.status == AttendanceStatus.presente,
        ).first()

        if not attendance:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Nenhuma entrada confirmada hoje. Não é possível gerar QR de saída."
            )

        from uuid import uuid4
        attendance.token = str(uuid4())
        attendance.token_expira_em = datetime.now() + timedelta(minutes=QR_EXPIRY_MINUTES)
        attendance.status = AttendanceStatus.pendente_saida

        self.session.commit()
        self.session.refresh(attendance)

        return attendance

    # ─────────────────────────────────────────
    # CONFIRMAR SAÍDA (admin)
    # ─────────────────────────────────────────
    def confirm_exit(self, token: str):
        attendance = self.get_by_token(token)

        if attendance.status != AttendanceStatus.pendente_saida:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Este QR code não é válido para confirmar saída."
            )

        if attendance.token_expira_em < datetime.now():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="QR code expirado. O aluno deve gerar um novo."
            )

        agora = datetime.now()
        attendance.status = AttendanceStatus.saiu
        attendance.hora_saida = agora.time()
        attendance.confirmado_saida_em = agora

        self.session.commit()
        self.session.refresh(attendance)

        return attendance