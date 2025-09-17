import frappe

def execute(filters=None):
    columns = [
        {"label": "Device Type", "fieldname": "device_type", "fieldtype": "Data", "width": 150},
        {"label": "Device", "fieldname": "device", "fieldtype": "Link", "options": "Device", "width": 200},
        {"label": "Total Repair Cost", "fieldname": "total_cost", "fieldtype": "Currency", "width": 150},
    ]

    conditions = "r.status = 'Completed'"
    values = {}

    if filters.get("device_type"):
        conditions += " AND d.device_type = %(device_type)s"
        values["device_type"] = filters["device_type"]

    data = frappe.db.sql(f"""
        SELECT 
            d.device_type,
            r.device,
            SUM(r.price) as total_cost
        FROM `tabDevice Repair Log` r
        LEFT JOIN `tabDevice` d ON r.device = d.name
        WHERE {conditions}
        GROUP BY d.device_type, r.device
        ORDER BY d.device_type, r.device
    """, values, as_dict=True)

    return columns, data
