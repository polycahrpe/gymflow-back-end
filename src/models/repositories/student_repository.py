from .base_repository import HTTPException, status, Session
from .access_code_repository import AccessCodeRepository
from sqlalchemy.orm import joinedload
from ..entities.student_entity import StudentEntity
from ..entities.coach_entity import CoachEntity
from ..entities.payment_plans_entity import PaymentPlanEntity
from ...schemas.student_schema import StudentCreateSchema, StudentUpdateSchema
import bcrypt


class StudentRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_by_email(self, email: str):
        return self.session.query(StudentEntity).filter(StudentEntity.email == email).first()

    def get_by_id(self, id: str):
        student = (
            self.session.query(StudentEntity)
            .options(
                joinedload(StudentEntity.coach),
                joinedload(StudentEntity.payment_plan)
            )
            .filter(StudentEntity.id == id)
            .first()
        )
        if not student:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Aluno não encontrado."
            )
        return student

    def get_all(self):
        return (
            self.session.query(StudentEntity)
            .options(
                joinedload(StudentEntity.coach),
                joinedload(StudentEntity.payment_plan)
            )
            .all()
        )

    def get_by_coach(self, coach_id: str):
        return (
            self.session.query(StudentEntity)
            .options(
                joinedload(StudentEntity.coach),
                joinedload(StudentEntity.payment_plan)
            )
            .filter(StudentEntity.coach_id == coach_id)
            .all()
        )

    def hash_password(self, password: str) -> str:
        return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

    def verify_password(self, plain: str, hashed: str) -> bool:
        return bcrypt.checkpw(plain.encode("utf-8"), hashed.encode("utf-8"))

    # ─────────────────────────────────────────
    # CREATE — valida código de acesso
    # ─────────────────────────────────────────
    def create(self, data: StudentCreateSchema) -> StudentEntity:
        # Valida e consome o código de acesso
        AccessCodeRepository(self.session).validate_and_consume(data.access_code)

        if self.get_by_email(data.email):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Já existe um aluno com este email."
            )

        coach = self.session.query(CoachEntity).filter(CoachEntity.id == data.coach_id).first()
        if not coach:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Treinador não encontrado."
            )

        plan = self.session.query(PaymentPlanEntity).filter(PaymentPlanEntity.id == data.payment_plan_id).first()
        if not plan:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Plano de pagamento não encontrado."
            )

        student = StudentEntity(
            nome=data.nome,
            email=data.email,
            password=self.hash_password(data.password),
            genero=data.genero,
            coach_id=data.coach_id,
            payment_plan_id=data.payment_plan_id,
            ativo=True,  # activo directamente após código válido
        )

        self.session.add(student)
        self.session.commit()
        self.session.refresh(student)
        return student

    # ─────────────────────────────────────────
    # UPDATE
    # ─────────────────────────────────────────
    def update(self, id: str, data: StudentUpdateSchema) -> StudentEntity:
        student = self.get_by_id(id)

        if data.nome is not None:
            student.nome = data.nome
        if data.genero is not None:
            student.genero = data.genero
        if data.coach_id is not None:
            coach = self.session.query(CoachEntity).filter(CoachEntity.id == data.coach_id).first()
            if not coach:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Treinador não encontrado."
                )
            student.coach_id = data.coach_id
        if data.payment_plan_id is not None:
            plan = self.session.query(PaymentPlanEntity).filter(PaymentPlanEntity.id == data.payment_plan_id).first()
            if not plan:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Plano de pagamento não encontrado."
                )
            student.payment_plan_id = data.payment_plan_id

        self.session.commit()
        self.session.refresh(student)
        return student

    # ─────────────────────────────────────────
    # ACTIVATE BY ID (admin)
    # ─────────────────────────────────────────
    def activate(self, id: str) -> StudentEntity:
        student = self.get_by_id(id)

        if student.ativo:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Aluno já está activo."
            )

        student.ativo = True
        self.session.commit()
        self.session.refresh(student)
        return student

    # ─────────────────────────────────────────
    # DEACTIVATE BY ID (admin)
    # ─────────────────────────────────────────
    def deactivate(self, id: str) -> StudentEntity:
        student = self.get_by_id(id)

        if not student.ativo:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Aluno já está inactivo."
            )

        student.ativo = False
        self.session.commit()
        self.session.refresh(student)
        return student

    # ─────────────────────────────────────────
    # DELETE
    # ─────────────────────────────────────────
    def delete(self, id: str) -> dict:
        student = self.get_by_id(id)
        self.session.delete(student)
        self.session.commit()
        return {"detail": "Conta do aluno eliminada com sucesso."}