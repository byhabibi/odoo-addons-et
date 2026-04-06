from odoo import api, fields, models


class PlcProductGroup(models.Model):
    _name = 'plc.product.group'
    _description = 'PLC Product Group'

    name = fields.Char(string='Nama Group', required=True)
    description = fields.Text(string='Deskripsi')
    plc_action_id = fields.Many2one('ir.actions.act_window', string='Aksi PLC')

    def action_open_plc_data(self):
        self.ensure_one()
        action = self.plc_action_id or self.env.ref('plc_monitoring.action_plc_data')
        result = action.read()[0]
        if self.name:
            result['context'] = dict(result.get('context') or {})
            result['domain'] = [('machine_name', '=', self.name)]
        return result
