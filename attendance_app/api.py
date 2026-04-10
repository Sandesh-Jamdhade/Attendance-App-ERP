import frappe
from frappe.utils import nowdate, now_datetime, get_time

@frappe.whitelist()
def mark_attendance(employee, status):

    if not employee:
        return "Employee required"

    today = nowdate()
    current_time = now_datetime()
    time_obj = get_time(current_time)

    if time_obj > get_time("10:00:00") and status == "Present":
        status = "Half Day"

    # Check excluding cancelled records
    exists = frappe.db.exists("Attendance", {
        "employee": employee,
        "attendance_date": today,
        "docstatus": ["!=", 2]
    })

    if exists:
        doc = frappe.get_doc("Attendance", exists)

        if "HR Manager" not in frappe.get_roles():
            return "Only HR can modify attendance"

        doc.status = status
        doc.in_time = current_time
        doc.flags.ignore_validate = True
        doc.save(ignore_permissions=True)

        return f"Attendance corrected to {status}"

    # Use SQL insert with duplicate protection instead of frappe.get_doc
    try:
        doc = frappe.get_doc({
            "doctype": "Attendance",
            "employee": employee,
            "status": status,
            "attendance_date": today,
            "in_time": current_time
        })
        doc.flags.ignore_validate = True
        doc.insert(ignore_permissions=True)
        frappe.db.commit()  # Commit immediately to release lock
        return f"Attendance marked as {status}"

    except frappe.DuplicateEntryError:
        #  Specific exception, not broad Exception
        existing = frappe.db.get_value("Attendance", {
            "employee": employee,
            "attendance_date": today,
            "docstatus": ["!=", 2]
        }, "name")

        if existing:
            frappe.db.set_value("Attendance", existing, "status", status)
            return f"Attendance updated to {status}"

        return "Error marking attendance"
    
@frappe.whitelist()
def mark_bulk_attendance(data):
    import json
    data = json.loads(data)
    
    employee = data.get("employee")
    status = data.get("status")
    unmarked_days = data.get("unmarked_days", [])
    today = nowdate()
    current_time = now_datetime()

    if not employee or not unmarked_days:
        return "Invalid data"

    marked = 0
    for date in unmarked_days:
        exists = frappe.db.exists("Attendance", {
            "employee": employee,
            "attendance_date": date,
            "docstatus": ["!=", 2]
        })

        if exists:
            continue  # Skip already marked days

        try:
            doc = frappe.get_doc({
                "doctype": "Attendance",
                "employee": employee,
                "status": status,
                "attendance_date": today,
                "in_time": current_time
            })
            doc.flags.ignore_validate = True
            doc.flags.ignore_mandatory = True  
            doc.insert(ignore_permissions=True, ignore_mandatory=True)
            frappe.db.commit()
            marked += 1
        except frappe.DuplicateEntryError:
            continue

    return f"Attendance marked for {marked} day(s)"