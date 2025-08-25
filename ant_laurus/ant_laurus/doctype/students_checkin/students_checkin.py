# Copyright (c) 2025, Hopeson and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class StudentsCheckin(Document):
	pass


import frappe
from frappe import _
from frappe.utils import cint
	
@frappe.whitelist()
def add_log_based_on_student_field(
    employee_field_value,
    timestamp,
    device_id=None,
    log_type=None,
    skip_auto_attendance=0,
    employee_fieldname="custom_student_attendance_device_id_biometricrf_tag_id"
):
	
	if not employee_field_value or not timestamp:
		frappe.throw(_("'student_field_value' and 'timestamp' are required."))
	student = frappe.db.get_value(
		"Student",
		{employee_fieldname: employee_field_value},
		["name", "student_name", employee_fieldname],
		as_dict=True
	)

	if not student:
		frappe.throw(
			_("No Student found for the given field value. '{}': {}").format(
				employee_fieldname, employee_field_value
			)
		)
	doc = frappe.new_doc("Students Checkin")
	doc.students = student.name
	doc.student_name = student.student_name
	doc.time = timestamp
	doc.device_id = device_id
	doc.log_type = log_type
	if cint(skip_auto_attendance) == 1:
		doc.skip_auto_attendance = 1
	doc.insert()

	return doc