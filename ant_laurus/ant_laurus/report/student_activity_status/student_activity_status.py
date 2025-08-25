import frappe
from frappe import _

def execute(filters=None):
    """
    Main function for generating the student-specific assessment report.
    """
    validate_filters(filters)

    # Fetch columns dynamically based on criteria
    columns = get_columns(filters)

    # Fetch data for the selected student grouped by date
    data = get_student_assessment_data(filters, columns)

    return columns, data

def validate_filters(filters):
    """
    Validates the input filters to ensure 'student' is provided.
    """
    if not filters or not filters.get("student"):
        frappe.throw(_("Please select a student to generate the report."))

def get_columns(filters):
    """
    Dynamically generate columns based on assessment criteria.
    """
    columns = [
        {"fieldname": "date", "label": _("Date"), "fieldtype": "Date", "width": 120}
    ]

    # Fetch unique assessment criteria for the student
    student = filters.get("student")
    criteria_list = frappe.db.sql("""
        SELECT DISTINCT ar_detail.assessment_criteria
        FROM `tabAssessment Result Detail` ar_detail
        INNER JOIN `tabAssessment Result` ar
        ON ar.name = ar_detail.parent
        WHERE ar.student = %s AND ar.docstatus = 1
        ORDER BY ar_detail.assessment_criteria ASC
    """, student, as_dict=True)

    for criteria in criteria_list:
        columns.append({
            "fieldname": frappe.scrub(criteria.assessment_criteria),
            "label": criteria.assessment_criteria,
            "fieldtype": "Data",
            "width": 150
        })

    # Add "Pending in a Day" and "Completed in a Day" columns
    columns.append({"fieldname": "pending", "label": _("Pending in a Day"), "fieldtype": "Int", "width": 100})
    columns.append({"fieldname": "completed", "label": _("Completed in a Day"), "fieldtype": "Int", "width": 100})

    return columns

def get_student_assessment_data(filters, columns):
    """
    Fetch all assessment results for the selected student grouped by date.
    """
    student = filters.get("student")
    course = filters.get("course")  # Get the course filter value

    # Fetch assessment results grouped by date and criterion
    results = frappe.db.sql("""
    SELECT ap.schedule_date AS date, ar_detail.assessment_criteria, ar_detail.grade
    FROM `tabAssessment Result Detail` ar_detail
    INNER JOIN `tabAssessment Result` ar ON ar.name = ar_detail.parent
    INNER JOIN `tabAssessment Plan` ap ON ap.name = ar.assessment_plan
    WHERE ar.student = %s
    AND (%s IS NULL OR ar.course = %s)
    AND ar.docstatus = 1
    ORDER BY ap.schedule_date ASC
""", (student, course, course), as_dict=True)


    # Prepare data grouped by date and criteria
    grouped_data = {}

    for row in results:
        date = row.date
        if date not in grouped_data:
            grouped_data[date] = {"date": date, "pending": 0, "completed": 0}

        criteria_key = frappe.scrub(row.assessment_criteria)

        # Initialize count for each criterion
        if criteria_key not in grouped_data[date]:
            grouped_data[date][criteria_key] = None  # Use None to represent no data yet

        # Count the status of the grade
        if row.grade == "Completed":  # Grade is "Completed"
            grouped_data[date]["completed"] += 1
            grouped_data[date][criteria_key] = "<span style='color: #4CAF50; font-size: 18px;'>✅</span>"  # Set parrot green tick mark with larger font
        else:  # Grade is "Not Completed"
            grouped_data[date]["pending"] += 1
            if grouped_data[date][criteria_key] is None:  # If no data yet, set it to cross mark
                grouped_data[date][criteria_key] = "<span style='color: red; font-size: 18px; font-weight: bolder;'>❌</span>"  # Set bolder red cross mark with larger font

    # Convert grouped data to a list
    data = list(grouped_data.values())

    return data
