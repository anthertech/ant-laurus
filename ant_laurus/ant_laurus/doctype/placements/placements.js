// Copyright (c) 2025, Hopeson and contributors
// For license information, please see license.txt


frappe.ui.form.on('Placements', {
    student_name: function(frm) {
        if (frm.doc.student_name) {
            // Fetch Student Applicant from Student
            frappe.call({
                method: 'frappe.client.get_value',
                args: {
                    doctype: 'Student',
                    filters: { name: frm.doc.student_name },
                    fieldname: ['student_applicant']
                },
                callback: function(response) {
                    let student_applicant = response.message?.student_applicant;
                    if (student_applicant) {
                        frappe.call({
                            method: 'frappe.client.get_value',
                            args: {
                                doctype: 'Student Applicant',
                                filters: { name: student_applicant },
                                fieldname: ['academic_year', 'city']
                            },
                            callback: function(response) {
                                if (response.message) {
                                    frm.set_value('academic_year', response.message.academic_year);
                                    frm.set_value('student_location', response.message.city);
                                }
                            }
                        });
                    }
                }
            });

            // Fetch Student Group
            frappe.call({
                method: 'ant_laurus.ant_laurus.doctype.placements.placements.get_student_group',
                args: { student_name: frm.doc.student_name },
                callback: function(response) {
                    if (response.message) {
                        frm.set_value('student_batch', response.message);
                    } else {
                        frappe.msgprint(__('No Student Group found for this student.'));
                        frm.set_value('student_batch', '');
                    }
                }
            });
        }
    },

    setup: function(frm) {
        // Filter Company Location based on Placed Company
        frm.set_query('company_location', function() {
            if (!frm.doc.placed_company) {
                frappe.msgprint(__('Please select a Placed Company first.'));
                return {};
            }
            return {
                query: "ant_laurus.ant_laurus.doctype.placements.placements.get_filtered_addresses",
                filters: { placed_company: frm.doc.placed_company }
            };
        });
    },

    placement_type: function(frm) {
        let hidden = frm.doc.placement_type === "Self-Placed" ? 1 : 0;
        frm.set_df_property("job_applicant_id", "hidden", hidden);
        frm.set_df_property("payment_history", "hidden", hidden);
    }
});





