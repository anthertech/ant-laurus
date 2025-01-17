frappe.query_reports["Student Activity Status"] = {
    filters: [
        {
            fieldname: "student",
            label: __("Student"),
            fieldtype: "Link",
            options: "Student",
            reqd: 1,
            get_query: () => {
                return {
                    filters: { enabled: 1 } // Fetch only enabled students
                };
            }
        },
        {
            fieldname: "course",
            label: __("Course"),
            fieldtype: "Link",
            options: "Course", // Assuming the course is a "Link" field linked to the "Course" DocType
            default: "20*9 Activity", // Default value for the course filter
            reqd: 0 // Course filter is not mandatory
        }
    ]
};
