import frappe
def on_student_insert(doc, method):
    if not doc.student_applicant:
        return

    applicant = frappe.get_doc("Student Applicant", doc.student_applicant)

    # Copy Guardians (already done, not repeating here)
    if applicant.custom_student_guardian_details:
        for row in applicant.custom_student_guardian_details:
            doc.append("custom_student_guardians", {
                "custom_guardian": row.custom_guardian,
                "custom_guardian_name": row.custom_guardian_name,
                "custom_occupation": row.custom_occupation,
                "guardian_contact_no": row.guardian_contact_no
            })

    # ✅ Copy Educational Qualifications
    if applicant.custom_educational_qualifications:
        for row in applicant.custom_educational_qualifications:
            doc.append("custom_student_education_and_qualification", {
                "class_": row.class_,
                "stream": row.stream,
                "boarduniversity": row.boarduniversity,
                "marks_obtained__cgpa": row.marks_obtained__cgpa,
                "year_of_passing": row.year_of_passing,
                "certificates": row.certificates
            })
