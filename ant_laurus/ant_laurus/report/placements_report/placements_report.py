import frappe
from frappe import _

def execute(filters=None):
    columns = get_columns()
    data = get_data(filters)

    return columns, data

def get_columns():
    return [
        {"fieldname": "student_id", "label": _("""<b>Student ID</b>"""), "fieldtype": "Link", "options": "Student", "width": 50},
        {"fieldname": "student_full_name", "label": _("""<b>Student  Name</b>"""), "fieldtype": "Data", "width": 160},
        {"fieldname": "student_batch", "label": _("""<b>Student Batch</b>"""), "fieldtype": "Link", "options": "Student Group", "width": 110},
        {"fieldname": "placement_type", "label": _("""<b>Placement Type</b>"""), "fieldtype": "Select", "width": 150},
        {"fieldname": "placed_company", "label": _("""<b>Placed Company</b>"""), "fieldtype": "Link", "options": "Customer", "width": 150},
        {"fieldname": "joined_date", "label": _("""<b>Joined Date</b>"""), "fieldtype": "Date", "width": 100},
        {"fieldname": "employment_type", "label": _("""<b>Employment Type</b>"""), "fieldtype": "Data", "width": 120},
        {"fieldname": "designation", "label": _("""<b>Designation</b>"""), "fieldtype": "Data", "width": 150},
        {"fieldname": "current_status", "label": _("""<b>Current Status</b>"""), "fieldtype": "Data", "width": 90},
		{"fieldname": "company_location", "label": _("""<b>Company Location</b>"""), "fieldtype": "Link", "options": "Address", "width": 150}

    ]


def get_data(filters):
    if not filters.get("academic_year"):
        frappe.throw(_("Please select an Academic Year"))

    conditions = ["sg.academic_year = %(academic_year)s"]
    values = {"academic_year": filters["academic_year"]}

    if filters.get("placed_company"):
        conditions.append("p.placed_company = %(placed_company)s")
        values["placed_company"] = filters["placed_company"]

    if filters.get("student_batch"):
        conditions.append("p.student_batch = %(student_batch)s")
        values["student_batch"] = filters["student_batch"]

    if filters.get("placement_type"):
        conditions.append("p.placement_type = %(placement_type)s")
        values["placement_type"] = filters["placement_type"]

    where_clause = " AND ".join(conditions)

    return frappe.db.sql(f"""
        SELECT 
            s.name AS student_id,  
            s.student_name AS student_full_name,  
            p.student_batch, 
            p.placement_type, 
            p.placed_company, 
            p.joined_date, 
            p.employment_type, 
            p.designation, 
            p.current_status,
			p.company_location
        FROM `tabPlacements` p
        LEFT JOIN `tabStudent` s ON p.student_name = s.name
        LEFT JOIN `tabStudent Group` sg ON p.student_batch = sg.name
        WHERE {where_clause}
        ORDER BY p.joined_date DESC
    """, values, as_dict=True)
