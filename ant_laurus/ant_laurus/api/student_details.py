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

    # Copy Educational Qualifications
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

    # Copy Aadhaar fields (single-value fields)
    doc.custom_aadhaar_no = applicant.custom_addhaar
    doc.custom_adhaar_front_ = applicant.custom_addhaar_copy
    doc.custom_adhaar_back = applicant.custom_addhaar_copy_back_side


def on_student_applicant_update(doc, method):
    # Find student(s) with this applicant linked
    students = frappe.get_all("Student", filters={"student_applicant": doc.name})

    for student in students:
        student_doc = frappe.get_doc("Student", student.name)
        
        # Clear existing educational qualifications in Student doc
        student_doc.set("custom_student_education_and_qualification", [])
        
        # Copy updated qualifications from Student Applicant to Student
        if doc.custom_educational_qualifications:
            for row in doc.custom_educational_qualifications:
                student_doc.append("custom_student_education_and_qualification", {
                    "class_": getattr(row, "class_", ""),
                    "stream": getattr(row, "stream", ""),
                    "boarduniversity": getattr(row, "boarduniversity", ""),
                    "marks_obtained__cgpa": getattr(row, "marks_obtained__cgpa", None),
                    "certificates": getattr(row, "certificates", ""),
                })

        
        student_doc.save()
