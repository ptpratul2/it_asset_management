# Copyright (c) 2025, Ami Trambadiya and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document
import frappe

class Device(Document):
	def on_submit(self):
		if not self.price:
			frappe.throw("Price is mandatory before submitting the Device.")
	
	def on_cancel(self):
		frappe.db.sql("""
			UPDATE `tabDevice`
			SET status = 'Cancelled'
			WHERE name = %s
		""", (self.name))
		self.reload()
		

	def on_update(self):
		if self.status == "Assigned":
			active_log = frappe.db.get_value(
				"Device Assignment Log",
				{"device": self.name, "return_date": ["is", "null"]},
				"name"
			)
			if not active_log:
				frappe.throw("Cannot set status to 'Assigned' without an active assignment log.")