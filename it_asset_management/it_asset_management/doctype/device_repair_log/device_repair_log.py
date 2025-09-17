# Copyright (c) 2025, Ami Trambadiya and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class DeviceRepairLog(Document):
	def validate(self):
		self.set_status()
		
	def on_submit(self):
		if not self.price:
			frappe.throw("Price is mandatory before submitting the Device.")

	def on_update_after_submit(self):
		self.set_status()

	def set_status(self):
		if self.status == "Assigned to Vendor" and (not self.vendor_name or not self.vendor_contact_no or not self.vendor_address):
			frappe.throw("Vendor Name, Vendor Contact No and Vendor Address are mandatory when status is 'Assigned to Vendor'.")
		if (self.status == "Assigned to Vendor" and self.vendor_name and  self.vendor_contact_no and  self.vendor_address) or self.status == "Testing" or self.status == "Draft":
			frappe.db.set_value(
				"Device",
				self.device,
				{
					"status": "Maintenance",
				},
			)	
		elif self.status == "Completed":
			frappe.db.set_value(
				"Device",
				self.device,
				{
					"status": "Not Assigned",
				},
			)