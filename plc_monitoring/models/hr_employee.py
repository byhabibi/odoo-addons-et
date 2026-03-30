from odoo import models, fields

class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    rfid_uid = fields.Char(string="RFID UID")