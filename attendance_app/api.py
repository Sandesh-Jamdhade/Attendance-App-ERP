import frappe
from frappe.utils import nowdate

@frappe.whitelist()
def mark_attendance(employee, status):

    if not employee:
        return "Employee required"

    today = nowdate()

    # Check if already marked
    exists = frappe.db.exists("Attendance", {
        "employee": employee,
        "attendance_date": today
    })

    if exists:
        return "Already marked"

    doc = frappe.get_doc({
        "doctype": "Attendance",
        "employee": employee,
        "status": status,
        "attendance_date": today
    })

    doc.insert()
    return "Attendance Marked Successfully"
