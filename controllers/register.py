from odoo import http
from odoo.http import request

class HospitalRegister(http.Controller):
    @http.route('/register',auth='public',website=True,type='http')
    def register_page(self, **kw):
        return request.render("hospital_management.register_page")