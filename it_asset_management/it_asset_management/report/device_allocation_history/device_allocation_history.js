// Copyright (c) 2025, Ami Trambadiya and contributors
// For license information, please see license.txt
frappe.query_reports["Device Allocation History"] = {
    "filters": [
        {
            "fieldname": "device",
            "label": __("Device"),
            "fieldtype": "Link",
            "options": "Device",
            "reqd": 0
        },
        {
            "fieldname": "employee",
            "label": __("Employee"),
            "fieldtype": "Link",
            "options": "Employee",
            "reqd": 0
        },
        {
            "fieldname": "status",
            "label": __("Status"),
            "fieldtype": "Select",
            "options": "\nActive\nClosed",
            "reqd": 0
        },
        {
            "fieldname": "from_date",
            "label": __("From Date"),
            "fieldtype": "Date",
            "default": frappe.datetime.add_months(frappe.datetime.get_today(), -1) // default last month
        },
        {
            "fieldname": "to_date",
            "label": __("To Date"),
            "fieldtype": "Date",
            "default": frappe.datetime.get_today()
        }
    ],

    // 🎨 Custom formatter for status
    formatter: function(value, row, column, data, default_formatter) {
        value = default_formatter(value, row, column, data);

        if (column.fieldname === "status") {
            if (value === "Active") {
                value = `<span style="color: green; font-weight: bold;">${value}</span>`;
            } else if (value === "Closed") {
                value = `<span style="color: red; font-weight: bold;">${value}</span>`;
            }
        }

        return value;
    }
};
