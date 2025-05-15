// Copyright (c) 2025, Hopeson and contributors
// For license information, please see license.txt

frappe.query_reports["Certificate Issuance Log"] = {
    "filters": [
        {
            "fieldname": "program",
            "label": "Program",
            "fieldtype": "Link",
            "options": "Program",
            "width": 180
        },
        {
            "fieldname": "custom_batch",
            "label": "Batch",
            "fieldtype": "Link",
            "options": "Student Batch Name",
            "width": 180
        },
        {
            "fieldname": "student",
            "label": "Student",
            "fieldtype": "Link",
            "options": "Student Applicant",
            "width": 180
        } ,
		{
            "fieldname": "academic_year",
			"label": "Academic Year",
            "fieldtype": "Link",
            "options": "Academic Year",
            "width": 180
        }
    ]
};
