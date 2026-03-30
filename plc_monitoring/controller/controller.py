from odoo import http
from odoo.http import request

class PlcController(http.Controller):

    @http.route('/plc/dashboard', type='http', auth='user')
    def plc_dashboard(self):

        action = request.env['plc.data'].sudo().get_action_with_header()

        return request.redirect(f"/web#action={action['id']}")