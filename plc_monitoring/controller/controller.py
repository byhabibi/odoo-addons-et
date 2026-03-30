from odoo import http
from odoo.http import request

class PlcController(http.Controller):

    # Route untuk membuka halaman dashboard (sudah benar)
    @http.route('/plc/dashboard', type='http', auth='user')
    def plc_dashboard(self):
        # Pastikan model 'plc.data' dan method 'get_action_with_header' sudah ada
        action = request.env['plc.data'].sudo().search([], limit=1) # Contoh sederhana
        # Jika kamu punya method khusus, gunakan ini:
        # action = request.env['plc.data'].sudo().get_action_with_header()
        return request.redirect(f"/web#action={action.id if action else ''}")

    # ROUTE BARU: Untuk menyuplai data ke Header Navbar (JS)
    @http.route('/plc/latest', type='json', auth='user', methods=['POST'])
    def get_latest_plc_data(self):
        """
        Fungsi ini dipanggil oleh header_patch.js setiap 5 detik.
        """
        # Ambil data terbaru dari model PLC kamu
        # Kita gunakan sudo() agar semua user bisa lihat status di navbar
        latest_data = request.env['plc.data'].sudo().search([], order='create_date desc', limit=1)

        if latest_data:
            return {
                'mp': latest_data.mp or "-",
                'shift': latest_data.shift or "-",
            }
        
        # Fallback jika data kosong
        return {
            'mp': "No Data",
            'shift': "N/A",
        }