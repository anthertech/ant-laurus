frappe.query_reports["Placements Report"] = {
    filters: [
        {
            fieldname: "academic_year",
            label: __("Academic Year"),
            fieldtype: "Link",
            options: "Academic Year",
            reqd: 0,
            on_change: function() {
                // Reset Student Group when Academic Year changes
                frappe.query_report.set_filter_value('student_batch', null);
                frappe.query_report.refresh();
            }
        },
        {
            fieldname: "student_batch",
            label: __("Student Batch"),
            fieldtype: "Link",
            options: "Student Group",
            get_query: function() {
                let academic_year = frappe.query_report.get_filter_value("academic_year");
                if (academic_year) {
                    return {
                        filters: { "academic_year": academic_year } // Fetch only student groups from the selected academic year
                    };
                }
            },
            on_change: function() {
                frappe.query_report.refresh();
            }
        },
        {
            fieldname: "placement_type",
            label: __("Placement Type"),
            fieldtype: "Select",
            options: ["", "Campus Placement", "Self-Placed"],
            on_change: function() {
                frappe.query_report.refresh();
            }
        },
        {
            fieldname: "placed_company",
            label: __("Placed Company"),
            fieldtype: "Link",
            options: "Customer",
            get_query: function() {
                return {
                    filters: { "customer_type": "Placement" } 
                };
            },
            on_change: function() {
                frappe.query_report.refresh();
            }
        }
    ]
};
