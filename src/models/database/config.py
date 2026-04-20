"""Configuração do engine SQLAlchemy/SQLModel para o banco da aplicação."""

from sqlmodel import create_engine


engine = create_engine("sqlite:///gymflow.db", echo=True)