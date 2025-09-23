import frappe
import io
import base64
from pypdf import PdfMerger
from PIL import Image
import os
import tempfile


@frappe.whitelist()
def download_all_files(docname, doctype):
    # Get the Student document to read student_applicant value
    student_doc = frappe.get_doc(doctype, docname)
    student_applicant_name = getattr(student_doc, "student_applicant", None)

    # Get all files attached directly to Student
    student_files = frappe.get_all("File", filters={
        "attached_to_doctype": doctype,
        "attached_to_name": docname
    }, fields=["file_url", "file_name", "attached_to_field"])

    # Get files attached to the student_applicant, if present
    applicant_files = []
    if student_applicant_name:
        applicant_files = frappe.get_all("File", filters={
            "attached_to_doctype": "Student Applicant",
            "attached_to_name": student_applicant_name
        }, fields=["file_url", "file_name", "attached_to_field"])

    # Get child table records linked to Student
    child_records = frappe.get_all("Educational Qualifications", filters={
        "parent": docname
    }, fields=["name"], order_by="idx asc")

    child_files = []
    for child in child_records:
        files = frappe.get_all("File", filters={
            "attached_to_doctype": "Educational Qualifications",
            "attached_to_name": child.name,
            "attached_to_field": "certificates"
        }, fields=["file_url", "file_name", "attached_to_field"], order_by="creation asc")
        child_files.extend(files)

    # Combine all files: student + applicant + child table
    all_files = student_files + applicant_files + child_files

    if not all_files:
        frappe.throw("No files attached to this record.")

    # Priority sorting function as before
    def file_priority(f):
        field = f.get("attached_to_field", "")
        # Hardcoded field priority
        if field == "image":
            return 0
        elif field == "custom_adhaar_front_":
            return 1
        elif field == "custom_adhaar_back":
            return 2
        elif field == "certificates":
            return 3
        return 4  # All other fields last


    all_files_sorted = sorted(all_files, key=file_priority)

    # Merge logic unchanged
    merger = PdfMerger()
    temp_pdfs = []

    for f in all_files_sorted:
        file_url = f["file_url"]

        if file_url.startswith("/private/"):
            relative_path = file_url[len("/private/"):]
            file_path = frappe.get_site_path("private", relative_path)
        elif file_url.startswith("/files/"):
            relative_path = file_url[len("/files/"):]
            file_path = frappe.get_site_path("public", "files", relative_path)
        else:
            relative_path = file_url.lstrip("/")
            file_path = frappe.get_site_path("public", relative_path)

        if not os.path.exists(file_path):
            frappe.log_error(f"File not found at path: {file_path}", "download_all_files missing_file")
            continue

        ext = os.path.splitext(file_path)[1].lower()

        if ext == ".pdf":
            merger.append(file_path)
        elif ext in [".png", ".jpg", ".jpeg"]:
            img = Image.open(file_path).convert("RGB")
            temp_pdf_fd, temp_pdf_path = tempfile.mkstemp(suffix=".pdf")
            os.close(temp_pdf_fd)
            img.save(temp_pdf_path)
            merger.append(temp_pdf_path)
            temp_pdfs.append(temp_pdf_path)

    if not merger.pages:
        frappe.throw("No PDF or image files attached to this record.")

    output = io.BytesIO()
    merger.write(output)
    merger.close()
    output.seek(0)

    for temp_pdf in temp_pdfs:
        try:
            os.remove(temp_pdf)
        except Exception as e:
            frappe.log_error(f"Error deleting temp pdf {temp_pdf}: {str(e)}", "download_all_files cleanup")

    encoded_pdf = base64.b64encode(output.read()).decode('utf-8')

    return {"pdf_base64": encoded_pdf}
