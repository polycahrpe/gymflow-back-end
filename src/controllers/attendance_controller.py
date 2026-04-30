from ..services.attendance_service import AttendanceService
from ..schemas.attendance_schema import AttendanceConfirmSchema


class AttendanceController:
    def __init__(self, session):
        self.service = AttendanceService(session)

    def get_all(self):
        return self.service.get_all_attendances()

    def get_by_student(self, student_id: str):
        return self.service.get_attendances_by_student(student_id)

    def get_by_id(self, attendance_id: str):
        return self.service.get_attendance_by_id(attendance_id)

    def generate_entry_qr(self, student_id: str):
        return self.service.generate_entry_qr(student_id)

    def confirm_entry(self, data: AttendanceConfirmSchema):
        return self.service.confirm_entry(data)

    def generate_exit_qr(self, student_id: str):
        return self.service.generate_exit_qr(student_id)

    def confirm_exit(self, data: AttendanceConfirmSchema):
        return self.service.confirm_exit(data)