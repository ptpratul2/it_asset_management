# Copyright (c) 2025, Ami Trambadiya and contributors
# For license information, please see license.txt

# import frappe


import frappe
def execute(filters=None):
    columns = [
        {"label": "Device", "fieldname": "device", "fieldtype": "Link", "options": "Device", "width": 150},
        {"label": "Employee", "fieldname": "employee", "fieldtype": "Link", "options": "Employee", "width": 150},
        {"label": "Status", "fieldname": "status", "fieldtype": "Data", "width": 100},
        {"label": "Assign Date", "fieldname": "assign_date", "fieldtype": "Date", "width": 120},
        {"label": "Return Date", "fieldname": "return_date", "fieldtype": "Date", "width": 120},
        {"label": "Log ID", "fieldname": "log_id", "fieldtype": "Dynamic Link", "options": "doctype", "width": 200}
    ]

    conditions = []
    values = {}

    if filters.get("device"):
        conditions.append("device = %(device)s")
        values["device"] = filters.get("device")

    if filters.get("employee"):
        conditions.append("employee = %(employee)s")
        values["employee"] = filters.get("employee")

    if filters.get("status"):
        conditions.append("status = %(status)s")
        values["status"] = filters.get("status")

    if filters.get("from_date") and filters.get("to_date"):
        conditions.append("assign_date BETWEEN %(from_date)s AND %(to_date)s")
        values["from_date"] = filters.get("from_date")
        values["to_date"] = filters.get("to_date")

    condition_str = " AND ".join(conditions) if conditions else "1=1"

    data = frappe.db.sql(f"""
        SELECT
            device,
            employee,
            status,
            assign_date,
            return_date,
            name as log_id
        FROM `tabDevice Assignment Log`
        WHERE {condition_str}
        ORDER BY assign_date DESC
    """, values, as_dict=True)

    return columns, data
