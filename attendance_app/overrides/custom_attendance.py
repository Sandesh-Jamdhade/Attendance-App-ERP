from hrms.hr.doctype.attendance.attendance import Attendance
import frappe

class CustomAttendance(Attendance):

    def validate(self):
        if self.flags.ignore_validate:
            return
        # Skip all duplicate/overlap checks, only run other validations
        self.validate_attendance_date()  # keep date validation

    def validate_duplicate_record(self):
        # Completely disabled - handled in api.py
        pass

    def get_duplicate_attendance_record(self):
        # Return None so validate_duplicate_record never throws
        return None

    def validate_overlapping_shift_attendance(self):
        # Disabled
        pass

    def get_overlapping_shift_attendance(self):
        return {}