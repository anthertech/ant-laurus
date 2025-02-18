// Copyright (c) 2025, Hopeson and contributors
// For license information, please see license.txt

// frappe.ui.form.on("Certificate Issuance Log", {
// 	refresh(frm) {

// 	},
// });




frappe.ui.form.on("Certificate Issuance Log", {
    student: function(frm) {
        if (frm.doc.student) {
            frappe.call({
                method: "ant_laurus.ant_laurus.doctype.certificate_issuance_log.certificate_issuance_log.get_student_group_details",
                args: {
                    student: frm.doc.student
                },
                callback: function(response) {
                    if (response.message) {
                        frm.set_value("academic_year", response.message.academic_year);
                        frm.set_value("student_batch", response.message.student_batch);
                    } else {
                        frappe.msgprint("No Student Group found for this student.");
                        frm.set_value("academic_year", "");
                        frm.set_value("student_batch", "");
                    }
                }
            });
        }
    }
});

