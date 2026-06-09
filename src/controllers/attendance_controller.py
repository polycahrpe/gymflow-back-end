from ..services.attendance_service import AttendanceService
from ..schemas.attendance_schema import AttendanceMarkEntrySchema, AttendanceMarkExitSchema


class AttendanceController:
    def __init__(self, session):
        self.service = AttendanceService(session)

    def get_all(self):
        return self.service.get_all_attendances()

    def get_by_student(self, student_id: str):
        return self.service.get_attendances_by_student(student_id)

    def get_today_by_student(self, student_id: str):
        return self.service.get_today_by_student(student_id)

    def get_by_id(self, attendance_id: str):
        return self.service.get_attendance_by_id(attendance_id)

    def mark_entry(self, data: AttendanceMarkEntrySchema):
        return self.service.mark_entry(data)

    def confirm_entry(self, attendance_id: str):
        return self.service.confirm_entry(attendance_id)

    def mark_exit(self, data: AttendanceMarkExitSchema):
        return self.service.mark_exit(data)

    def confirm_exit(self, attendance_id: str):
        return self.service.confirm_exit(attendance_id)