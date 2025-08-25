// Copyright (c) 2025, Hopeson and contributors
// For license information, please see license.txt

frappe.query_reports["Syllabus Updation Report"] = {
    filters: [
        {
            fieldname: "course",
            label: __("Course"),
            fieldtype: "Link",
            options: "Course",
            reqd: 0,
            // No need to filter based on 'enabled' since all courses are active
            get_query: function() {
                return {};  // No additional filtering needed
            }
        },
        {
            fieldname: "student",
            label: __("Student"),
            fieldtype: "Link",
            options: "Student",
            reqd: 0,
        },
    ],
    onload: function(report) {
        // Ensures that filters are applied to the backend on load
        report.page.add_inner_button(__('Refresh'), function() {
            report.refresh();
        });
    }
};





