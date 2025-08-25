# Copyright (c) 2025, Hopeson and contributors
# For license information, please see license.txt

import frappe
import calendar
from datetime import datetime

def execute(filters=None):
    filters = filters or {}
    student_group = filters.get('student_group')
    if not student_group:
        return [], []

    # Get students in the group
    students = frappe.db.sql("""
        SELECT s.name, s.student_name
        FROM `tabStudent` s
        JOIN `tabStudent Group Student` sgs ON sgs.student = s.name
        WHERE sgs.parent = %s
    """, student_group, as_dict=True)
    if not students:
        return [], []

    student_ids = [s.name for s in students]

    # Get min and max attendance dates
    date_range = frappe.db.sql("""
        SELECT MIN(`date`) as min_date, MAX(`date`) as max_date
        FROM `tabStudent Attendance`
        WHERE student IN %(students)s
    """, {'students': tuple(student_ids)}, as_dict=True)

    if not date_range or not date_range[0]['min_date']:
        return [], []

    min_date = date_range[0]['min_date']
    max_date = date_range[0]['max_date']

    # Month-year iterator
    def month_year_iter(start_date, end_date):
        y, m = start_date.year, start_date.month
        end_y, end_m = end_date.year, end_date.month
        while (y, m) <= (end_y, end_m):
            yield y, m
            if m == 12:
                y += 1
                m = 1
            else:
                m += 1

    months = []
    for y, m in month_year_iter(min_date, max_date):
        months.append(f"{calendar.month_abbr[m]} {y}")

    # Attendance data structure
    attendance_data = {
        s.name: {
            month: {'working_days': 0, 'present': 0, 'absent_or_leave': 0} for month in months
        } for s in students
    }

    # Fetch attendance grouped by month and status
    attendance_records = frappe.db.sql("""
        SELECT student, DATE_FORMAT(`date`, '%%Y-%%m') as month_ym, status, COUNT(*) as count
        FROM `tabStudent Attendance`
        WHERE student IN %(students)s
        GROUP BY student, month_ym, status
    """, {'students': tuple(student_ids)}, as_dict=True)

    # Map YYYY-MM to Month Name
    month_ym_to_month_name = {
        f"{y}-{m:02d}": f"{calendar.month_abbr[m]} {y}" for y, m in month_year_iter(min_date, max_date)
    }

    # Fill attendance_data
    for record in attendance_records:
        student = record.student
        month = month_ym_to_month_name.get(record.month_ym)
        if month and month in attendance_data[student]:
            attendance_data[student][month]['working_days'] += record.count
            if record.status == 'Present':
                attendance_data[student][month]['present'] += record.count
            elif record.status in ('Absent', 'On Leave'):
                attendance_data[student][month]['absent_or_leave'] += record.count

    # Columns
    columns = [
        "Student ID:Link/Student:120",
        "Student Name::140"
    ]

    for month in months:
        # Month on first line, WD|P|A on second line
        columns.append(f"{month}\nWD | P | A:Data:120")

    # Updated column headers (removed WD and A/L)
    columns.append("Total Working Days:Int:120")
    columns.append("Total Absent/Leave:Int:120")

    # Result rows
    result = []
    for student in students:
        row = [student.name, student.student_name]
        total_working_days = 0
        total_absent_leave = 0
        for month in months:
            data = attendance_data[student.name][month]
            row.append(f"{data['working_days']}    |  {data['present']}  |  {data['absent_or_leave']}")
            total_working_days += data['working_days']
            total_absent_leave += data['absent_or_leave']
        row.append(total_working_days)
        row.append(total_absent_leave)
        result.append(row)

    return columns, result


