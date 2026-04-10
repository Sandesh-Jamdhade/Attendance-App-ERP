from hrms.hr.doctype.attendance.attendance import Attendance

class CustomAttendance(Attendance):

    def validate(self):
        # Disable ERP validation
        pass