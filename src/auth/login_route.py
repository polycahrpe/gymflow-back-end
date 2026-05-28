from fastapi import APIRouter, Depends, HTTPException, status
from ..models.database.session import get_session
from ..models.repositories.user_repository import UserRepository
from ..models.repositories.student_repository import StudentRepository
from ..schemas.user_schema import UserLoginSchema
from .jwt import create_access_token

login_router = APIRouter(prefix="/auth", tags=["auth"])


@login_router.post("/login")
async def login(data: UserLoginSchema, session=Depends(get_session)):

    # 1. Tenta encontrar em users (admin, coach)
    user_repo = UserRepository(session)
    user = user_repo.get_by_email(data.email)

    if user:
        if not user_repo.verify_password(data.password, user.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Email ou password incorrectos."
            )
        if not user.ativo:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="A tua conta está desactivada. Contacta o administrador."
            )
        token = create_access_token({"sub": user.id, "role": user.role})
        return {
            "access_token": token,
            "token_type": "bearer",
            "user": {
                "id": user.id,
                "nome": user.nome,
                "email": user.email,
                "role": user.role,
                "ativo": user.ativo,
            }
        }

    # 2. Tenta encontrar em students
    student_repo = StudentRepository(session)
    student = student_repo.get_by_email(data.email)

    if student:
        if not student_repo.verify_password(data.password, student.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Email ou password incorrectos."
            )

        # Verifica se o plano expirou
        student = student_repo.verificar_expiracao(student)

        if not student.ativo:
            if student.data_fim is None:
                detail = "A tua conta ainda não foi activada. Efectua o primeiro pagamento para aceder."
            elif student.dias_restantes == 0:
                detail = "O teu plano expirou. Renova o pagamento para continuar."
            else:
                detail = "A tua conta está desactivada. Contacta o administrador."

            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=detail
            )

        # Busca todos os alunos do mesmo coach
        alunos_do_coach = student_repo.get_by_coach(student.coach_id)

        token = create_access_token({"sub": student.id, "role": "student"})
        return {
            "access_token": token,
            "token_type": "bearer",
            "user": {
                "id": student.id,
                "nome": student.nome,
                "email": student.email,
                "role": "student",
                "ativo": student.ativo,
                "genero": student.genero,
                "coach_id": student.coach_id,
                "payment_plan_id": student.payment_plan_id,
                "data_inicio": student.data_inicio,
                "data_fim": student.data_fim,
                "dias_restantes": student.dias_restantes,
                "coach": {
                    "id": student.coach.id,
                    "nome": student.coach.nome,
                    "email": student.coach.email,
                    "especialidade": student.coach.especialidade,
                    "genero": student.coach.genero,
                    "ativo": student.coach.ativo,
                    "alunos": [
                        {
                            "id": s.id,
                            "nome": s.nome,
                            "email": s.email,
                            "genero": s.genero,
                            "ativo": s.ativo,
                            "dias_restantes": s.dias_restantes,
                        }
                        for s in alunos_do_coach
                    ]
                } if student.coach else None,
                "payment_plan": {
                    "id": student.payment_plan.id,
                    "nome": student.payment_plan.nome,
                    "preco": student.payment_plan.preco,
                    "duracao_dias": student.payment_plan.duracao_dias,
                    "ativo": student.payment_plan.ativo,
                } if student.payment_plan else None,
                "pagamentos": [
                    {
                        "id": p.id,
                        "payment_plan_id": p.payment_plan_id,
                        "valor": p.valor,
                        "data_pagamento": p.data_pagamento,
                        "data_vencimento": p.data_vencimento,
                        "status": p.status,
                        "observacao": p.observacao,
                    }
                    for p in student.pagamentos
                ]
            }
        }

    # 3. Não encontrado em nenhuma tabela
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Email ou password incorrectos."
    )