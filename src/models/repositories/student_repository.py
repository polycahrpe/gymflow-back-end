from .base_repository import HTTPException, status, Session
from ..entities.student_entity import StudentEntity
from ..entities.coach_entity import CoachEntity
from ..entities.payment_plans_entity import PaymentPlanEntity
from ...schemas.student_schema import StudentCreateSchema
import bcrypt


class StudentRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_by_email(self, email: str):
        return self.session.query(StudentEntity).filter(StudentEntity.email == email).first()

    def get_by_id(self, id: str):
        student = self.session.query(StudentEntity).filter(StudentEntity.id == id).first()
        if not student:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Aluno não encontrado."
            )
        return student

    def get_all(self):
        return self.session.query(StudentEntity).all()

    def get_by_coach(self, coach_id: str):
        return self.session.query(StudentEntity).filter(StudentEntity.coach_id == coach_id).all()

    def hash_password(self, password: str) -> str:
        return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

    def verify_password(self, plain: str, hashed: str) -> bool:
        return bcrypt.checkpw(plain.encode("utf-8"), hashed.encode("utf-8"))

    def create(self, data: StudentCreateSchema) -> StudentEntity:

        # Verifica se o email já existe
        if self.get_by_email(data.email):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Já existe um aluno com este email."
            )

        # Verifica se o coach existe
        coach = self.session.query(CoachEntity).filter(CoachEntity.id == data.coach_id).first()
        if not coach:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Treinador não encontrado."
            )

        # Verifica se o plano de pagamento existe
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
            ativo=False
        )

        self.session.add(student)
        self.session.commit()
        self.session.refresh(student)
        return student

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