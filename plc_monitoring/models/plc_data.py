from odoo import models, fields, api
import pytz

class PlcData(models.Model):
    _name = 'plc.data'
    _description = 'PLC Data'
    _order = 'timestamp desc'

    machine_name = fields.Char(string="Nama Mesin", default="Manual Bending")
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
                user_tz = pytz.timezone(self.env.user.tz or 'Asia/Jakarta')
                local_time = pytz.utc.localize(rec.timestamp).astimezone(user_tz)
                hour = local_time.hour
                if 7 <= hour < 19:
                    rec.shift = "Shift 1"
                else:
                    rec.shift = "Shift 2"
            else:
                rec.shift = "-"

    @api.model
    def get_latest_info(self):
        """Fungsi ini akan dipanggil oleh JavaScript untuk mengisi Navbar"""
        record = self.search([], order="timestamp desc", limit=1)
        if record:
            return {
                'mp': record.man_power.name or '-',
                'shift': record.shift or '-'
            }
        return {'mp': '-', 'shift': '-'}