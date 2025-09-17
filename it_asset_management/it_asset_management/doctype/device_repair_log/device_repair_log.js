// Copyright (c) 2025, Ami Trambadiya and contributors
// For license information, please see license.txt

frappe.ui.form.on("Device Repair Log", {
    refresh(frm) {
        frm.set_query("device", function() {
            return {
                filters: {
                    status: "Not Assigned", docstatus: 1
                }
            };
        });
    },
});
