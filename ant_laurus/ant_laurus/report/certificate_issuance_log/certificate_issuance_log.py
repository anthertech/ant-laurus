import frappe
from frappe.utils import get_link_to_form

def execute(filters=None):
    columns = get_columns()
    data = get_data(filters or {})
    return columns, data

def get_columns():
    return [
    {
        "label": "<b>Student Name</b>",
        "fieldname": "student_name_link",
        "fieldtype": "HTML",
        "width": 200
    },
    {
        "label": "<b>Batch</b>",
        "fieldname": "custom_batch",
        "fieldtype": "Link",
        "options": "Student Batch Name",
        "width": 65
    },
    {
        "label": "<b>10th</b>",
        "fieldname": "tenth",
        "fieldtype": "Data",
        "width": 80
    },
    {
        "label": "<b>12th</b>",
        "fieldname": "twelfth",
        "fieldtype": "Data",
        "width": 80
    },
    {
        "label": "<b>Degree</b>",
        "fieldname": "degree",
        "fieldtype": "Data",
        "width": 120
    },
    {
        "label": "<b>PG</b>",
        "fieldname": "pg",
        "fieldtype": "Data",
        "width": 120
    },
    {
        "label": "",
        "fieldname": "spacer",
        "fieldtype": "Data",
        "width": 20
    },
    {
        "label": "<b style='color:#5819b5'>STED Council</b>",
        "fieldname": "sted",
        "fieldtype": "Data",
        "width": 120
    },
    {
        "label": "<b style='color:#5819b5'>Glocal University</b>",
        "fieldname": "glocal",
        "fieldtype": "Data",
        "width": 140
    },
    {
        "label": "<b style='color:#5819b5'>NSDC</b>",
        "fieldname": "nsdc",
        "fieldtype": "Data",
        "width": 100
    },
    {
        "label": "<b style='color:#5819b5'>American Board</b>",
        "fieldname": "american_board",
        "fieldtype": "Data",
        "width": 140
    },
]


def colorize_status(value, positive="Received", negative="Not Received", student=None, certificate_name=None):
    color = "green" if value == positive or value == "Issued" else "red"

    if value == "Not Issued" and student and certificate_name:
        log_name = frappe.db.get_value("Certificate Issuance Log", {"student": student}, "name")
        if log_name:
            url = f"/app/certificate-issuance-log/{log_name}"
        else:
            url = f"/app/certificate-issuance-log/new?student={student}"

        return f'<a href="{url}" style="color:{color};font-weight:bold">{value}</a>'

    return f'<span style="color:{color};font-weight:bold">{value}</span>'


def get_data(filters):
    conditions = "1=1"
    if filters.get("program"):
        conditions += " AND sa.program = %(program)s"
    if filters.get("custom_batch"):
        conditions += " AND sa.custom_batch = %(custom_batch)s"
    if filters.get("student"):
        conditions += " AND sa.name = %(student)s"
    if filters.get("academic_year"):
        conditions += " AND sa.academic_year = %(academic_year)s"

    query = f"""
        SELECT
            sa.name as student_applicant_id,
            CONCAT(sa.first_name, ' ', IFNULL(sa.last_name, '')) as student_name,
            sa.program,
            sa.custom_batch,
            eq.`class` as edu_class
        FROM `tabStudent Applicant` sa
        LEFT JOIN `tabEducational Qualifications` eq ON eq.parent = sa.name
        WHERE {conditions}
        ORDER BY sa.name ASC
    """
    raw_data = frappe.db.sql(query, filters, as_dict=True)

    grouped = {}
    reverse_map = {}  # Map student ID to student_applicant_id

    for row in raw_data:
        sid = row.student_applicant_id
        if sid not in grouped:
            student_id = frappe.db.get_value("Student", {"student_applicant": sid}, "name")
            if student_id:
                reverse_map[student_id] = sid
            student_name_link = (
                get_link_to_form("Student", student_id, row.student_name)
                if student_id else row.student_name
            )

            grouped[sid] = {
                "student_name_link": student_name_link,
                "program": row.program,
                "custom_batch": row.custom_batch,
                "tenth": colorize_status("Not Received"),
                "twelfth": colorize_status("Not Received"),
                "degree": colorize_status("Not Received"),
                "pg": colorize_status("Not Received"),
                "sted": colorize_status("Not Issued", "Issued", "Not Issued", student_id, "STED Council"),
                "glocal": colorize_status("Not Issued", "Issued", "Not Issued", student_id, "Glocal University"),
                "nsdc": colorize_status("Not Issued", "Issued", "Not Issued", student_id, "NSDC"),
                "american_board": colorize_status("Not Issued", "Issued", "Not Issued", student_id, "American Board")
            }

        edu_class = (row.get("edu_class") or "").strip().lower()
        if edu_class == "10th":
            grouped[sid]["tenth"] = colorize_status("Received")
        elif edu_class == "12th":
            grouped[sid]["twelfth"] = colorize_status("Received")
        elif edu_class == "degree":
            grouped[sid]["degree"] = colorize_status("Received")
        elif edu_class == "pg":
            grouped[sid]["pg"] = colorize_status("Received")

    # Fetch certificate issuance data
    all_ids = list(set(grouped.keys()))
    if all_ids:
        cert_data = frappe.db.sql(
            """
            SELECT
                cil.student,
                s.student_applicant,
                cs.certificate_name
            FROM `tabCertificate Issuance Log` cil
            LEFT JOIN `tabCertificates of Student` cs ON cs.parent = cil.name
            LEFT JOIN `tabStudent` s ON s.name = cil.student
            WHERE cil.student IN %(all_ids)s OR s.student_applicant IN %(all_ids)s
            """,
            {"all_ids": all_ids},
            as_dict=True
        )

        for cert in cert_data:
            sa_id = cert.student_applicant
            if not sa_id and cert.student:
                sa_id = reverse_map.get(cert.student)

            if not sa_id or sa_id not in grouped:
                continue

            cert_name = (cert.certificate_name or "").strip().lower()
            if cert_name == "sted council":
                grouped[sa_id]["sted"] = colorize_status("Issued", "Issued", "Not Issued")
            elif cert_name == "glocal university":
                grouped[sa_id]["glocal"] = colorize_status("Issued", "Issued", "Not Issued")
            elif cert_name == "nsdc":
                grouped[sa_id]["nsdc"] = colorize_status("Issued", "Issued", "Not Issued")
            elif cert_name == "american board":
                grouped[sa_id]["american_board"] = colorize_status("Issued", "Issued", "Not Issued")

    return list(grouped.values())
