from .base_repository import HTTPException, status, Session
from ..entities.workout_plan_entity import WorkoutPlanEntity
from ..entities.workout_exercise_entity import WorkoutExerciseEntity
from ..entities.student_entity import StudentEntity
from ...schemas.workout_plan_schema import WorkoutPlanCreateSchema, WorkoutPlanUpdateSchema


class WorkoutPlanRepository:
    def __init__(self, my_session: Session):
        self.session = my_session

    # ─────────────────────────────────────────
    # GET ALL
    # ─────────────────────────────────────────
    def get_all(self):
        return self.session.query(WorkoutPlanEntity).all()

    # ─────────────────────────────────────────
    # GET BY ID
    # ─────────────────────────────────────────
    def get_by_id(self, id: str):
        plan = self.session.query(WorkoutPlanEntity).filter(
            WorkoutPlanEntity.id == id
        ).first()

        if not plan:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Ficha de treino não encontrada."
            )

        return plan

    # ─────────────────────────────────────────
    # GET BY STUDENT
    # ─────────────────────────────────────────
    def get_by_student(self, student_id: str):
        return self.session.query(WorkoutPlanEntity).filter(
            WorkoutPlanEntity.student_id == student_id
        ).all()

    # ─────────────────────────────────────────
    # GET BY COACH
    # ─────────────────────────────────────────
    def get_by_coach(self, coach_id: str):
        return self.session.query(WorkoutPlanEntity).filter(
            WorkoutPlanEntity.coach_id == coach_id
        ).all()

    # ─────────────────────────────────────────
    # CREATE
    # ─────────────────────────────────────────
    def create(self, coach_id: str, data: WorkoutPlanCreateSchema):
        student = self.session.query(StudentEntity).filter(
            StudentEntity.id == data.student_id
        ).first()

        if not student:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Aluno não encontrado."
            )

        plan = WorkoutPlanEntity(
            student_id=data.student_id,
            coach_id=coach_id,
            titulo=data.titulo,
        )

        plan.exercicios = [
            WorkoutExerciseEntity(
                dia_semana=ex.dia_semana,
                nome=ex.nome,
                series=ex.series,
                repeticoes=ex.repeticoes,
                carga=ex.carga,
            )
            for ex in data.exercicios
        ]

        self.session.add(plan)
        self.session.commit()
        self.session.refresh(plan)

        return plan

    # ─────────────────────────────────────────
    # UPDATE
    # ─────────────────────────────────────────
    def update(self, id: str, data: WorkoutPlanUpdateSchema):
        plan = self.get_by_id(id)

        if data.titulo is not None:
            plan.titulo = data.titulo
        if data.ativo is not None:
            plan.ativo = data.ativo

        if data.exercicios is not None:
            plan.exercicios = [
                WorkoutExerciseEntity(
                    dia_semana=ex.dia_semana,
                    nome=ex.nome,
                    series=ex.series,
                    repeticoes=ex.repeticoes,
                    carga=ex.carga,
                )
                for ex in data.exercicios
            ]

        self.session.commit()
        self.session.refresh(plan)

        return plan

    # ─────────────────────────────────────────
    # DELETE
    # ─────────────────────────────────────────
    def delete(self, id: str):
        plan = self.get_by_id(id)

        self.session.delete(plan)
        self.session.commit()

        return {"detail": "Ficha de treino eliminada com sucesso."}