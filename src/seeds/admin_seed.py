import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv
load_dotenv()

from sqlalchemy.orm import sessionmaker
from src.models.database.config import engine
from src.models.repositories.user_repository import UserRepository
from src.schemas.user_schema import UserCreateSchema, UserRole

def seed_admin():
    Session = sessionmaker(bind=engine)
    session = Session()
    repo = UserRepository(session)

    try:
        admin = UserCreateSchema(
            nome="Admin GymFlow",
            email="admin@gymflow.com",
            password="Admin@1234",
            role=UserRole.admin
        )
        user = repo.create(admin)
        print(f"✅ Admin criado com sucesso: {user.email}")

    except Exception as e:
        print(f"❌ Erro ao criar admin: {e}")

    finally:
        session.close()

if __name__ == "__main__":
    seed_admin()


# python -m src.seeds.admin_seed - comando para criar o admin no banco de dados.