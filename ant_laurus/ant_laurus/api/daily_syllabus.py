# import frappe

# @frappe.whitelist()
# def confirm_syllabus(student_name, dsu_name):
       

#     try:
#         # Fetch the Daily Syllabus Update document
#         dsu_doc = frappe.get_doc("Daily Syllabus Update", dsu_name)
#         student_doc=frappe.get_doc("Student", student_name)
#         student_exist = frappe.db.exists(
#             "Daily Syllabus Confirmation",
#             {
#                 "student_id": student_doc.name,  
#                 "parent": dsu_doc.name
#             }
#         )
#         if student_exist:
#             return "confirmation exist"

#         dsu_doc.append("daily_syllabus_confirmed_students", {
#             "student_id": student_doc.name,
#             "student_name": student_doc.first_name,
#             "confirmation_status": "Declared",
#             "confirmed_date": frappe.utils.now()
        
#         })

#         dsu_doc.save()
#         frappe.db.commit()

#         return "success"
#     except Exception as e:
#         frappe.log_error(frappe.get_traceback(), "Syllabus Confirmation Error")
#         retur


import frappe

@frappe.whitelist()
def confirm_syllabus(student_name, dsu_name):
    try:
        # Fetch the Daily Syllabus Update document
        dsu_doc = frappe.get_doc("Daily Syllabus Update", dsu_name)

        # Ensure syllabus is only visible if status is "Completed"
        if dsu_doc.status != "Completed":
            frappe.throw("You cannot confirm syllabus updates that are not marked as 'Completed'.")

        # Fetch the student document
        student_doc = frappe.get_doc("Student", student_name)
        
        # Check if confirmation already exists for this student and syllabus update
        student_exist = frappe.db.exists(
            "Daily Syllabus Confirmation",
            {
                "student_id": student_doc.name,
                "parent": dsu_doc.name
            }
        )
        
        if student_exist:
            return "confirmation exist"  # Avoid multiple confirmations for the same update

        # Append confirmation record
        dsu_doc.append("daily_syllabus_confirmed_students", {
            "student_id": student_doc.name,
            "student_name": student_doc.first_name,
            "confirmation_status": "Declared",
            "confirmed_date": frappe.utils.today()  # Use today's date only (YYYY-MM-DD)
        })

        # Save and commit changes
        dsu_doc.save()
        frappe.db.commit()

        return "success"
    
    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "Syllabus Confirmation Error")
        return {"error": str(e)}
    