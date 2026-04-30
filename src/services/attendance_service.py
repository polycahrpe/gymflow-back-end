from ..models.repositories.attendance_repository import AttendanceRepository
from ..schemas.attendance_schema import AttendanceConfirmSchema


class AttendanceService:
    def __init__(self, session):
        self.repo = AttendanceRepository(session)

    def get_all_attendances(self):
        return self.repo.get_all()

    def get_attendances_by_student(self, student_id: str):
        return self.repo.get_by_student(student_id)

    def get_attendance_by_id(self, attendance_id: str):
        return self.repo.get_by_id(attendance_id)

    # Aluno → gera QR de entrada ao fazer login
    def generate_entry_qr(self, student_id: str):
        return self.repo.generate_entry_qr(student_id)

    # Admin → confirma entrada via token do QR
    def confirm_entry(self, data: AttendanceConfirmSchema):
        return self.repo.confirm_entry(data.token)

    # Aluno → gera QR de saída ao querer sair
    def generate_exit_qr(self, student_id: str):
        return self.repo.generate_exit_qr(student_id)

    # Admin → confirma saída via token do QR
    def confirm_exit(self, data: AttendanceConfirmSchema):
        return self.repo.confirm_exit(data.token)