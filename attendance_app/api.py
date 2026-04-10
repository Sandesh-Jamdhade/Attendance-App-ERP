import frappe
from frappe.utils import nowdate, now_datetime, get_time

@frappe.whitelist()
def mark_attendance(employee, status):

    if not employee:
        return "Employee required"

    today = nowdate()
    current_time = now_datetime()

    time_obj = get_time(current_time)

    # Late logic
    if time_obj > get_time("10:00:00") and status == "Present":
        status = "Half Day"

    # if already marked
    exists = frappe.db.exists("Attendance", {
        "employee": employee,
        "attendance_date": today
    })

    if exists:
        frappe.db.sql("""
            UPDATE `tabAttendance`
            SET status=%s, in_time=%s
            WHERE name=%s
        """, (status, current_time, exists))
        return f"Attendance updated to {status}"
    
    doc = frappe.get_doc({
        "doctype": "Attendance",
        "employee": employee,
        "status": status,
        "attendance_date": today,
        "in_time": current_time
    })

    doc.insert(ignore_permissions=True, ignore_validate=True)

    return f"Attendance marked at {current_time} with status {status}"

def disable_attendance_validation(doc, method):
    return