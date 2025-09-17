// Copyright (c) 2025, Ami Trambadiya and contributors
// For license information, please see license.txt

// frappe.ui.form.on("Device", {
// 	refresh(frm) {

// 	},
// });
frappe.ui.form.on('Device', {
    refresh: function(frm) {
        if (frm.doc.docstatus === 1) {
        if (frm.doc.status === "Not Assigned") {
            frm.add_custom_button(__('Decommissioned'), function() {
                frm.set_value('status', 'Decommissioned');
                frm.save();
            }, __('Actions'));
            frm.add_custom_button(__('Assign Device'), function() {
                let d = new frappe.ui.Dialog({
                    title: __('Assign Device'),
                    fields: [
                        {
                            label: 'Employee',
                            fieldname: 'employee',
                            fieldtype: 'Link',
                            options: 'Employee',
                            reqd: 1,
                            get_query: function() {
                                return {
                                    filters: {
                                        status: 'Active'
                                    }
                                };
                            }
                        },
                        {
                            label: 'Assign Date',
                            fieldname: 'assign_date',
                            fieldtype: 'Date',
                            reqd: 1,
                            default: frappe.datetime.get_today()
                        }
                    ],
                    primary_action_label: __('Save'),
                    primary_action(values) {
                        // Validation: assign_date should be today or in future
                        if (values.assign_date && values.assign_date >= frm.doc.purchase_date) {
                            frappe.call({
                                method: 'it_asset_management.it_asset_management.doctype.device_assignment_log.device_assignment_log.create_assignment',
                                args: {
                                    device: frm.doc.name,
                                    employee: values.employee,
                                    assign_date: values.assign_date
                                },
                                callback: function(resp) {
                                    if (resp.message === "success") {
                                        frappe.msgprint("Device assigned successfully.");
                                        frm.reload_doc();
                                    } else {
                                        frappe.msgprint("Error assigning device.");
                                    }
                                }
                            });
                            d.hide();
                        } else {
                            frappe.msgprint("Assign Date must be after purchase date (" + frm.doc.purchase_date + ").");
                        }
                    }
                });
                d.show();
            }, __('Actions'));
        }

       if (frm.doc.status === "Assigned") {
        frm.add_custom_button(__('Return Device'), function() {
            // Fetch the assign_date for the active assignment log
            frappe.call({
                method: "it_asset_management.it_asset_management.doctype.device_assignment_log.device_assignment_log.get_active_assign_date",
                args: {
                    device: frm.doc.name
                },
                callback: function(r) {
                    if (r.message) {
                        let device_assignment_log_doc = r.message.name;
                        let assign_date = r.message.assign_date;
                        let d = new frappe.ui.Dialog({
                            title: __('Return Device'),
                            fields: [
                                {
                                    label: 'Return Date',
                                    fieldname: 'return_date',
                                    fieldtype: 'Date',
                                    reqd: 1
                                }
                            ],
                            primary_action_label: __('Save'),
                            primary_action(values) {
                                // Client-side validation
                                if (values.return_date && assign_date && values.return_date >= assign_date) {
                                    frappe.call({
                                        method: 'it_asset_management.it_asset_management.doctype.device_assignment_log.device_assignment_log.close_assignment',
                                        args: {
                                            docname: device_assignment_log_doc,
                                            return_date: values.return_date
                                        },
                                        callback: function(resp) {
                                            if (resp.message === "success") {
                                                frappe.msgprint("Device has been returned.");
                                                frm.reload_doc();
                                            } else {
                                                frappe.msgprint("Error closing assignment.");
                                            }
                                        }
                                    });
                                    d.hide();
                                } else {
                                    frappe.msgprint("Return Date must be on or after Assign Date (" + assign_date + ").");
                                }
                            }
                        });
                        d.show();
                    } else {
                        frappe.msgprint("Active assignment or assign date not found for this device.");
                    }
                }
        });
    }, __('Actions'));

        }
    }
}
});
