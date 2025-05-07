import frappe
from datetime import datetime

@frappe.whitelist()
def check_in_out_attendance_scheduler():
    today = frappe.utils.nowdate()

    # 1. Get all active Student Groups
    active_student_groups = frappe.get_all('Student Group', filters={'disabled': 0}, fields=['name'])

    for group in active_student_groups:
        group_name = group.name

        # 🚨 Check if this group has any class scheduled today
        has_class_today = frappe.db.exists('Course Schedule', {
            'student_group': group_name,
            'schedule_date': today
        })

        if not has_class_today:
            continue  # ⛔ Skip groups with no scheduled class

        # 2. Get students in each group
        students = frappe.get_all('Student Group Student', filters={'parent': group_name}, fields=['student'])

        for student in students:
            student_id = student.student

            # 3. Skip if student already has attendance
            existing_attendance = frappe.get_value('Student Attendance', {
                'student': student_id,
                'date': today
            })

            if existing_attendance:
                continue

            # 4. Fetch check-ins for today
            checkins = frappe.get_all('Students Checkin', filters={
                'students': student_id,
                'time': ['between', [f'{today} 00:00:00', f'{today} 23:59:59']]
            }, fields=['log_type', 'time'], order_by='time asc')

            if not checkins:
                create_attendance(student_id, group_name, today, 'Absent')
                continue

            in_times = [c['time'] for c in checkins if c['log_type'] == 'IN']
            out_times = [c['time'] for c in checkins if c['log_type'] == 'OUT']

            if in_times and out_times:
                first_in = min(in_times)
                last_out = max(out_times)

                duration_seconds = (last_out - first_in).total_seconds()
                attendance_date = first_in.strftime('%Y-%m-%d')

                if duration_seconds >= 7200:
                    create_attendance(student_id, group_name, attendance_date, 'Present')
                else:
                    create_attendance(student_id, group_name, attendance_date, 'Absent')
            else:
                create_attendance(student_id, group_name, today, 'Absent')

def create_attendance(student_id, group_name, date, status):
    if frappe.get_value('Student Attendance', {'student': student_id, 'date': date}):
        return

    attendance = frappe.new_doc('Student Attendance')
    attendance.student = student_id
    attendance.student_group = group_name
    attendance.date = date
    attendance.status = status
    attendance.submit()
    frappe.db.commit()



# import frappe
# from datetime import datetime

# def check_in_out_attendance_scheduler():
#     today = frappe.utils.nowdate()

#     # 1. Find all Active Student Groups (Disabled = 0)
#     active_student_groups = frappe.get_all('Student Group', filters={'disabled': 0}, fields=['name'])

#     for group in active_student_groups:
#         group_name = group.name

#         # 2. Find all Students inside each Group
#         students = frappe.get_all('Student Group Student', filters={'parent': group_name}, fields=['student'])

#         for student in students:
#             student_id = student.student

#             # 3. Check if student already has Leave recorded today
#             existing_attendance = frappe.get_value('Student Attendance', {
#                 'student': student_id,
#                 'date': today,
#                 'status': 'Leave'
#             })

#             if existing_attendance:
#                 continue  # Skip this student because they are on leave

#             # 4. Fetch all check-ins for today
#             checkins = frappe.get_all('Students Checkin', filters={
#                 'students': student_id,
#                 'time': ['between', [f'{today} 00:00:00', f'{today} 23:59:59']]
#             }, fields=['log_type', 'time'], order_by='time asc')

#             if not checkins:
#                 # No check-in records ➔ Mark Absent
#                 create_attendance(student_id, group_name, today, 'Absent')
#                 continue

#             # Find first IN and last OUT
#             in_times = [c['time'] for c in checkins if c['log_type'] == 'IN']
#             out_times = [c['time'] for c in checkins if c['log_type'] == 'OUT']

#             if in_times and out_times:
#                 first_in = min(in_times)
#                 last_out = max(out_times)

#                 # Check if time difference >= 2 hours
#                 if (last_out - first_in).seconds >= 7200:
#                     create_attendance(student_id, group_name, today, 'Present')
#                 else:
#                     create_attendance(student_id, group_name, today, 'Absent')
#             else:
#                 # Missing either IN or OUT ➔ Mark Absent
#                 create_attendance(student_id, group_name, today, 'Absent')

# def create_attendance(student_id, group_name, date, status):
#     # Check if attendance record already exists for the student on the given date
#     existing_attendance = frappe.get_value('Student Attendance', {
#         'student': student_id,
#         'date': date
#     })

#     if existing_attendance:
#         # If the attendance already exists, skip creating a new record
#         return

#     # Create Student Attendance record if no existing record
#     attendance = frappe.new_doc('Student Attendance')
#     attendance.student = student_id
#     attendance.student_group = group_name
#     attendance.date = date  # Use only the date portion from check-ins
#     attendance.status = status  # Present / Absent
#     attendance.save(ignore_permissions=True)
