app_name = "ant_laurus"
app_title = "Ant Laurus"
app_publisher = "Hopeson"
app_description = "Custom app for tracking laurus customization"
app_email = "hopeson@anther.tech"
app_license = "mit"

# Apps
# ------------------

# required_apps = []

# Each item in the list will be shown as an app in the apps page
# add_to_apps_screen = [
# 	{
# 		"name": "ant_laurus",
# 		"logo": "/assets/ant_laurus/logo.png",
# 		"title": "Ant Laurus",
# 		"route": "/ant_laurus",
# 		"has_permission": "ant_laurus.api.permission.has_app_permission"
# 	}
# ]

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/ant_laurus/css/ant_laurus.css"
# app_include_js = "/assets/ant_laurus/js/ant_laurus.js"

# include js, css files in header of web template
# web_include_css = "/assets/ant_laurus/css/ant_laurus.css"
# web_include_js = "/assets/ant_laurus/js/ant_laurus.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "ant_laurus/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Svg Icons
# ------------------
# include app icons in desk
# app_include_icons = "ant_laurus/public/icons.svg"

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
# 	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
# 	"methods": "ant_laurus.utils.jinja_methods",
# 	"filters": "ant_laurus.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "ant_laurus.install.before_install"
# after_install = "ant_laurus.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "ant_laurus.uninstall.before_uninstall"
# after_uninstall = "ant_laurus.uninstall.after_uninstall"

# Integration Setup
# ------------------
# To set up dependencies/integrations with other apps
# Name of the app being installed is passed as an argument

# before_app_install = "ant_laurus.utils.before_app_install"
# after_app_install = "ant_laurus.utils.after_app_install"

# Integration Cleanup
# -------------------
# To clean up dependencies/integrations with other apps
# Name of the app being uninstalled is passed as an argument

# before_app_uninstall = "ant_laurus.utils.before_app_uninstall"
# after_app_uninstall = "ant_laurus.utils.after_app_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "ant_laurus.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

override_doctype_class = {
	"Assessment Plan": "ant_laurus.ant_laurus.api.assessment_plan.AssessmentPlan"
}

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
# 	}
# }

# Scheduled Tasks
# ---------------


scheduler_events = {
    "cron": {
        "0 22 * * *": [
            "ant_laurus.ant_laurus.api.student_attendance.check_in_out_attendance_scheduler"
        ]
    }
}


# my_app/hooks.py

doc_events = {
    "Student": {
        "before_insert": "ant_laurus.ant_laurus.api.student_details.on_student_insert"
    }
}

# doc_events = {
#     "Student Applicant": {
#         "on_update": "ant_laurus.ant_laurus.api.student_details.sync_guardians_to_student"
#     }
# }



# scheduler_events = {
# 	"all": [
# 		"ant_laurus.tasks.all"
# 	],
# 	"daily": [
# 		"ant_laurus.tasks.daily"
# 	],
# 	"hourly": [
# 		"ant_laurus.tasks.hourly"
# 	],
# 	"weekly": [
# 		"ant_laurus.tasks.weekly"
# 	],
# 	"monthly": [
# 		"ant_laurus.tasks.monthly"
# 	],
# }

# Testing
# -------

# before_tests = "ant_laurus.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "ant_laurus.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "ant_laurus.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# before_request = ["ant_laurus.utils.before_request"]
# after_request = ["ant_laurus.utils.after_request"]

# Job Events
# ----------
# before_job = ["ant_laurus.utils.before_job"]
# after_job = ["ant_laurus.utils.after_job"]

# User Data Protection
# --------------------

# user_data_fields = [
# 	{
# 		"doctype": "{doctype_1}",
# 		"filter_by": "{filter_by}",
# 		"redact_fields": ["{field_1}", "{field_2}"],
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_2}",
# 		"filter_by": "{filter_by}",
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_3}",
# 		"strict": False,
# 	},
# 	{
# 		"doctype": "{doctype_4}"
# 	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"ant_laurus.auth.validate"
# ]

# Automatically update python controller files with type annotations for this app.
# export_python_type_annotations = True

# default_log_clearing_doctypes = {
# 	"Logging DocType Name": 30  # days to retain logs
# }

fixtures = [
    {
        "dt": "Web Page",   
        "filters": [
            ["module", "=", "Ant Laurus"]
        ]
    },
    {
        "dt": "Custom Field",
        "filters": [
            ["module", "=", "Ant Laurus"]
        ]
    },
    {
        "dt": "Client Script",
        "filters": [
            ["module", "=", "Ant Laurus"]
        ]
    },
    {
        "dt": "Server Script",
        "filters": [
            ["module", "=", "Ant Laurus"]
        ]
    }
]