# Copyright (c) 2025, Hopeson and contributors
# For license information, please see license.txt

import frappe

def execute(filters=None):
    if not filters:
        filters = {}

    columns = get_columns()
    data = get_data(filters)

    return columns, data

def get_columns():
    return [
        {"label": "Student Name", "fieldname": "student_name", "fieldtype": "Data", "width": 150},
        {"label": "Student Group", "fieldname": "student_group", "fieldtype": "Link", "options": "Student Group", "width": 150},
        {"label": "Course", "fieldname": "course", "fieldtype": "Link", "options": "Course", "width": 250},
        {"label": "Topic", "fieldname": "topic", "fieldtype": "Link", "options": "Topic", "width": 350},
        {"label": "Confirmation Status", "fieldname": "confirmation_status", "fieldtype": "Data", "width": 150},
        {"label": "Confirmed Date", "fieldname": "confirmed_date", "fieldtype": "Date", "width": 120},
    ]

def get_data(filters):
    # Ensure that the 'student' filter is provided, if not, handle accordingly
    if 'student' not in filters:
        frappe.throw("Please select student to view Report.")

    conditions = []

    if filters.get("student_group"):
        conditions.append("d.student_group = %(student_group)s")
    if filters.get("course"):
        conditions.append("d.course = %(course)s")
    if filters.get("student"):
        conditions.append("s.name = %(student)s")

    condition_string = " AND ".join(conditions)

    query = f"""
        SELECT
            s.student_name AS student_name,
            d.student_group AS student_group,
            d.course AS course,
            d.topic AS topic,
            IFNULL(c.student_name, 'Not Declared') AS confirmation_status,
            IFNULL(c.confirmed_date, NULL) AS confirmed_date
        FROM
            `tabDaily Syllabus Update` d
        LEFT JOIN
            `tabDaily Syllabus Confirmation` c ON c.parent = d.name AND c.student_id = %(student)s
        INNER JOIN
            `tabStudent Group Student` sgs ON sgs.parent = d.student_group
        INNER JOIN
            `tabStudent` s ON sgs.student = s.name
        WHERE
            {condition_string if condition_string else "1=1"}
            AND d.status = 'Completed'
    """

    # Fetch results
    result = frappe.db.sql(query, filters, as_dict=True)

    # Format confirmation_status for better visual presentation
    for row in result:
        if row.get('confirmation_status') != 'Not Declared':
            row['confirmation_status'] = '<span style="font-weight: bold; color: green;">Declared</span>'
        else:
            row['confirmation_status'] = '<span style="color: red;">Not Declared</span>'

    return result




      