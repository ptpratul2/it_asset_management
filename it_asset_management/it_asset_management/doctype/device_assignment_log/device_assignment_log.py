# Copyright (c) 2025, Ami Trambadiya and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import today, getdate

class DeviceAssignmentLog(Document):
    def validate(self):
        # check for another active log
        if not self.return_date:
            exists = frappe.db.exists(
                "Device Assignment Log",
                {"device": self.device, "return_date": ["is", "null"], "name": ["!=", self.name]}
            )
            if exists:
                frappe.throw("This device is already assigned and not yet returned.")
        purchase_date = frappe.db.get_value("Device", self.device, "purchase_date")
        join_date = frappe.db.get_value("Employee", self.employee, "date_of_joining")
        if not self.assign_date:
            frappe.throw("Assign Date is required")

        if purchase_date and getdate(self.assign_date) < getdate(purchase_date):
            frappe.throw("Assign Date cannot be before the Device Purchase Date")

        if getdate(self.assign_date) > getdate(today()):
            frappe.throw("Assign Date cannot be in the future")

        if join_date and getdate(self.assign_date) < getdate(join_date):
            frappe.throw("Assign Date cannot be before the Employee's Join Date")

        if self.return_date:
            if getdate(self.return_date) < getdate(self.assign_date):
                frappe.throw("Return Date cannot be before the Assign Date")
            if getdate(self.return_date) > getdate(today()):
                frappe.throw("Return Date cannot be in the future")

        

    def after_insert(self):
            # When assignment created -> mark device as Assigned
            frappe.db.set_value("Device", self.device, "status", "Assigned")
    
    def on_update(self):
        # If return_date is set -> mark device as Not Assigned
        if self.return_date:
            frappe.db.set_value("Device", self.device, "status", "Not Assigned")

@frappe.whitelist()
def get_active_log(device):
    log = frappe.db.get_value(
        "Device Assignment Log",
        {"device": device, "return_date": ["is", "null"]},
        "name"
    )
    return log
 
@frappe.whitelist()
def get_active_assign_date(device):
    doc = frappe.get_doc(
        "Device Assignment Log", 
        {"device": device, "status": "Active"}
    )
    return doc

@frappe.whitelist()
def close_assignment(docname, return_date):
    doc = frappe.get_doc("Device Assignment Log", docname)
    doc.return_date = return_date
    doc.status = "Closed"
    doc.save(ignore_permissions=True)
    return "success"

@frappe.whitelist()
def create_assignment(device, employee, assign_date):
    # Create a new Device Assignment Log
    new_log = frappe.get_doc({
        "doctype": "Device Assignment Log",
        "device": device,
        "employee": employee,
        "assign_date": assign_date,
        "status": "Active"
    })
    new_log.insert(ignore_permissions=True)
    # Update Device status to Assigned
    frappe.db.set_value("Device", device, "status", "Assigned")
    return "success"
