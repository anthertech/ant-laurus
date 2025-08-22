frappe.query_reports["Student Attendance Summary"] = {
    "filters": [
        {
            "fieldname": "student_group",
            "label": "Student Group",
            "fieldtype": "Link",
            "options": "Student Group",
            "reqd": 1
        }
    ],
   
};
