# Copyright (c) 2025, Hopeson and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class Placements(Document):
	pass


# import frappe

# @frappe.whitelist()
# def get_student_group(student_name):
#     """Fetch the most recent Student Group for a given student."""
#     if not student_name:
#         return None

#     student_group = frappe.db.sql("""
#         SELECT parent 
#         FROM `tabStudent Group Student`
#         WHERE student = %s
#         ORDER BY creation DESC
#         LIMIT 1
#     """, (student_name,), as_dict=True)

#     return student_group[0]["parent"] if student_group else None


# @frappe.whitelist()
# def get_filtered_companies(doctype, txt, searchfield, start, page_len, filters):
#     """Get list of companies based on student's job applications."""
#     student_name = filters.get("student_name")
#     student_email = filters.get("student_email")

#     if not student_name and not student_email:
#         return []

#     return frappe.db.sql("""
#         SELECT DISTINCT jo.custom_company_name 
#         FROM `tabJob Applicant` ja
#         JOIN `tabJob Opening` jo ON ja.job_title = jo.name
#         WHERE ja.applicant_name = %s OR ja.email_id = %s
#     """, (student_name, student_email))


# @frappe.whitelist()
# def get_filtered_addresses(doctype, txt, searchfield, start, page_len, filters):
#     """Get filtered company addresses based on linked Customer in Dynamic Link."""
#     placed_company = filters.get("placed_company")

#     if not placed_company:
#         return []

#     return frappe.db.sql("""
#         SELECT name 
#         FROM `tabAddress`
#         WHERE EXISTS (
#             SELECT 1 FROM `tabDynamic Link` dl
#             WHERE dl.parent = `tabAddress`.name
#             AND dl.link_doctype = 'Customer'
#             AND dl.link_name = %s
#         )
#     """, (placed_company,))

# doc = frappe.get_doc({
#     "doctype": "Student",
#     "student_name": "John Doe",
#     # other fields
# })

# # disable link validation and unique checks manually
# doc.flags.ignore_validate = True
# doc.flags.ignore_mandatory = True
# doc.insert(ignore_permissions=True)
