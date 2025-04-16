import frappe
from frappe.utils import now_datetime
from frappe import _

@frappe.whitelist(allow_guest=True)
def add_student_log_based_on_id(student_id, timestamp=None, device_id=None, log_type="IN"):
    """
    This function receives biometric data and logs a Student Checkin in ERPNext.
    :param student_id: biometric ID of the student (maps to student_biometric_id field in Student DocType)
    :param timestamp: datetime of the checkin (optional, defaults to now)
    :param device_id: device identifier from which checkin was made
    :param log_type: IN or OUT
    """
    timestamp = timestamp or now_datetime()

    # Match the biometric ID to a student
    student = frappe.db.get_value("Student", {"student_biometric_id": student_id}, "name")

    if not student:
        frappe.throw(_("Student not found for ID: {0}").format(student_id))

    # Avoid duplicate check-ins for the same timestamp
    existing = frappe.db.exists("Student Checkin", {
        "student": student,
        "time": timestamp
    })
    if existing:
        return {
            "message": {
                "name": existing,
                "info": "Duplicate Checkin Skipped"
            }
        }

    # Create new Student Checkin
    doc = frappe.get_doc({
        "doctype": "Student Checkin",
        "student": student,
        "time": timestamp,
        "log_type": log_type,
        "device_id": device_id
    })
    doc.insert(ignore_permissions=True)
    frappe.db.commit()

    return {
        "message": {
            "name": doc.name,
            "info": "Student Checkin Created"
        }
    }
