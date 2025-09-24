import frappe
import io
import base64
from pypdf import PdfMerger
from PIL import Image
import os
import tempfile

@frappe.whitelist()
def download_all_files(docname, doctype):
    student_doc = frappe.get_doc(doctype, docname)
    student_applicant_name = getattr(student_doc, "student_applicant", None)

    # Helper to get files
    def get_files(dt, dn, field_filters=None):
        filters = {"attached_to_doctype": dt, "attached_to_name": dn}
        if field_filters:
            filters.update(field_filters)
        return frappe.get_all("File", filters=filters, fields=["file_url", "file_name", "attached_to_field"], order_by="creation asc")

    # 1. Get files from student and student applicant
    student_files = get_files(doctype, docname)
    applicant_files = get_files("Student Applicant", student_applicant_name) if student_applicant_name else []

    # 2. Get child table files
    child_files = []
    child_records = frappe.get_all("Educational Qualifications", filters={"parent": docname}, fields=["name"], order_by="idx asc")
    for child in child_records:
        child_files.extend(get_files("Educational Qualifications", child.name, {"attached_to_field": "certificates"}))

    # 3. Combine all files
    all_files = applicant_files + student_files + child_files  # Applicant first for priority

    if not all_files:
        frappe.throw("No files attached to this record.")

    # 4. Deduplicate and prioritize
    seen_fields = set()
    final_files = []

    field_aliases = {
        "image": ["image"],
        "custom_adhaar_front_": ["custom_adhaar_front_", "custom_addhaar_copy"],
        "custom_adhaar_back": ["custom_adhaar_back", "custom_addhaar_copy_back_side"],
        "certificates": ["certificates"]
    }

    def get_field_type(f):
        for key, aliases in field_aliases.items():
            if f.get("attached_to_field") in aliases:
                return key
        return "other"

    # Priority: only one for image and Aadhaar
    for priority_field in ["image", "custom_adhaar_front_", "custom_adhaar_back"]:
        for f in all_files:
            f_type = get_field_type(f)
            if f_type == priority_field and f_type not in seen_fields:
                final_files.append(f)
                seen_fields.add(f_type)
                break  # Only one file per priority type

    # Add all certificates from student applicant
    for f in applicant_files:
        if get_field_type(f) == "certificates":
            final_files.append(f)

    # Add remaining files not yet added (excluding duplicates of priority and certificates)
    for f in all_files:
        f_type = get_field_type(f)
        if f_type not in seen_fields and f_type != "certificates":
            final_files.append(f)
            seen_fields.add(f_type)

    # 5. Merge PDFs and images
    merger = PdfMerger()
    temp_pdfs = []

    for f in final_files:
        file_url = f["file_url"]
        if file_url.startswith("/private/"):
            file_path = frappe.get_site_path("private", file_url[len("/private/"):])
        elif file_url.startswith("/files/"):
            file_path = frappe.get_site_path("public", "files", file_url[len("/files/"):])
        else:
            file_path = frappe.get_site_path("public", file_url.lstrip("/"))

        if not os.path.exists(file_path):
            frappe.log_error(f"File not found: {file_path}", "download_all_files")
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
