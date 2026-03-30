from odoo import models, fields, api

class PlcData(models.Model):
    _name = 'plc.data'
    _description = 'PLC Data'
    _order = 'timestamp desc'

    machine_name = fields.Char(string="Mesin Manual Bending")
    counter = fields.Integer(string="Sensor Counter")
    timestamp = fields.Datetime(
        string="Timestamp",
        default=fields.Datetime.now
    )
    shift = fields.Char(compute="_compute_shift", store=True)
    man_power = fields.Many2one("hr.employee", string="Operator")

    @api.depends('timestamp')
    def _compute_shift(self):
        for rec in self:
            if rec.timestamp:
                hour = rec.timestamp.hour
                if 7 <= hour < 19:
                    rec.shift = "Shift 1"
                else:
                    rec.shift = "Shift 2"

    @api.model
    def get_latest_info(self):
        record = self.search([], order="timestamp desc", limit=1)

        return {
            'mp': record.man_power.name if record.man_power else '-',
            'shift': record.shift or '-'
        }
    
    def get_action_with_header(self):
        action = self.env.ref('plc_monitoring.action_plc_data').read()[0]

        latest = self.get_latest_info()

        action['name'] = f"Mesin Manual Bending | MP: {latest['mp']} | {latest['shift']}"

        return action