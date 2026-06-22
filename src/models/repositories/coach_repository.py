from .base_repository import HTTPException, status, Session
from sqlalchemy.orm import joinedload
from ..entities.coach_entity import CoachEntity
from ..entities.coach_experiencia_entity import CoachExperienciaEntity
from ..entities.student_entity import StudentEntity
from .access_code_repository import AccessCodeRepository
from ...schemas.coach_schema import CoachCreateSchema, CoachUpdateSchema
import bcrypt


class CoachRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_by_email(self, email: str):
        return self.session.query(CoachEntity).filter(CoachEntity.email == email).first()

    def get_by_id(self, id: str):
        coach = (
            self.session.query(CoachEntity)
            .options(joinedload(CoachEntity.students))
            .filter(CoachEntity.id == id)
            .first()
        )
        if not coach:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Coach não encontrado."
            )
        return coach

    def get_all(self):
        return (
            self.session.query(CoachEntity)
            .options(joinedload(CoachEntity.students))
            .all()
        )

    def hash_password(self, password: str) -> str:
        return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

    def verify_password(self, plain: str, hashed: str) -> bool:
        return bcrypt.checkpw(plain.encode("utf-8"), hashed.encode("utf-8"))

    def create(self, data: CoachCreateSchema) -> CoachEntity:
        AccessCodeRepository(self.session).validate_and_consume(data.access_code)

        if self.get_by_email(data.email):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Já existe um coach com este email."
            )

        coach = CoachEntity(
            nome=data.nome,
            email=data.email,
            password=self.hash_password(data.password),
            especialidade=data.especialidade,
            genero=data.genero,
            ativo=False,
        )

        coach.experiencias = [
            CoachExperienciaEntity(nome=e.value)
            for e in data.experiencias
        ]

        self.session.add(coach)
        self.session.commit()
        self.session.refresh(coach)
        return coach

    def update(self, id: str, data: CoachUpdateSchema) -> CoachEntity:
        coach = self.get_by_id(id)

        if data.nome is not None:
            coach.nome = data.nome
        if data.especialidade is not None:
            coach.especialidade = data.especialidade
        if data.genero is not None:
            coach.genero = data.genero
        if data.experiencias is not None:
            coach.experiencias = [
                CoachExperienciaEntity(nome=e.value)
                for e in data.experiencias
            ]

        self.session.commit()
        self.session.refresh(coach)
        return coach

    def activate(self, id: str) -> CoachEntity:
        coach = self.get_by_id(id)
        if coach.ativo:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Coach já está activo."
            )
        coach.ativo = True
        self.session.commit()
        self.session.refresh(coach)
        return coach

    def deactivate(self, id: str) -> CoachEntity:
        coach = self.get_by_id(id)
        if not coach.ativo:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Coach já está inactivo."
            )
        coach.ativo = False
        self.session.commit()
        self.session.refresh(coach)
        return coach

    def delete(self, id: str) -> dict:
        coach = self.get_by_id(id)
        self.session.delete(coach)
        self.session.commit()
        return {"detail": "Coach eliminado com sucesso."}