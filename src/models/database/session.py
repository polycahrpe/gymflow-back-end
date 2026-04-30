from .config import engine
from sqlalchemy.orm import sessionmaker


def get_session():
    Session = sessionmaker(bind=engine)
    session = Session()
    
    try:
        yield session
    finally:
        session.close()