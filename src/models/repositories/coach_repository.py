from .base_repository import HTTPException, status, Session
from ..entities.coach_entity import CoachEntity
from ...schemas.coach_schema import CoachCreateSchema
import bcrypt


class CoachRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_by_email(self, email: str):
        return self.session.query(CoachEntity).filter(CoachEntity.email == email).first()

    def get_by_id(self, id: str):
        coach = self.session.query(CoachEntity).filter(CoachEntity.id == id).first()
        if not coach:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Coach não encontrado."
            )
        return coach

    def get_all(self):
        return self.session.query(CoachEntity).all()

    def hash_password(self, password: str) -> str:
        return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

    def verify_password(self, plain: str, hashed: str) -> bool:
        return bcrypt.checkpw(plain.encode("utf-8"), hashed.encode("utf-8"))

    def create(self, data: CoachCreateSchema) -> CoachEntity:
        existing = self.get_by_email(data.email)
        if existing:
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
            ativo=False
        )

        self.session.add(coach)
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