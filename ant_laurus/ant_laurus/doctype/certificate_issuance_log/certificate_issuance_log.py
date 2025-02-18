# Copyright (c) 2025, Hopeson and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class CertificateIssuanceLog(Document):
	pass

import frappe

@frappe.whitelist()
def get_student_group_details(student):
    """
    Fetches the academic_year and batch for the given student
    from the Student Group if the student exists in the Student Group Student child table.
    """
    student_group = frappe.db.sql("""
        SELECT sg.academic_year, sg.batch 
        FROM `tabStudent Group` sg
        JOIN `tabStudent Group Student` sgs ON sg.name = sgs.parent
        WHERE sgs.student = %s
        LIMIT 1
    """, (student), as_dict=True)

    if student_group:
        return {
            "academic_year": student_group[0].academic_year,
            "student_batch": student_group[0].batch
        }
    else:
        return None
