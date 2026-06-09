from ..models.repositories.attendance_repository import AttendanceRepository
from ..schemas.attendance_schema import AttendanceMarkEntrySchema, AttendanceMarkExitSchema


class AttendanceService:
    def __init__(self, session):
        self.repo = AttendanceRepository(session)

    def get_all_attendances(self):
        return self.repo.get_all()

    def get_attendances_by_student(self, student_id: str):
        return self.repo.get_by_student(student_id)

    def get_today_by_student(self, student_id: str):
        return self.repo.get_today_by_student(student_id)

    def get_attendance_by_id(self, attendance_id: str):
        return self.repo.get_by_id(attendance_id)

    def mark_entry(self, data: AttendanceMarkEntrySchema):
        return self.repo.mark_entry(data)

    def confirm_entry(self, attendance_id: str):
        return self.repo.confirm_entry(attendance_id)

    def mark_exit(self, data: AttendanceMarkExitSchema):
        return self.repo.mark_exit(data)

    def confirm_exit(self, attendance_id: str):
        return self.repo.confirm_exit(attendance_id)