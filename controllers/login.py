import logging

from odoo import http
from odoo.http import request

_logger = logging.getLogger(__name__)


class HospitalAuth(http.Controller):

    @http.route(
        '/login',
        type='http',
        auth='public',
        website=True,
    )
    def login_page(self, **kwargs):
        return request.render('hospital_management.login_page')

    @http.route(
        '/login/submit',
        type='http',
        auth='public',
        website=True,
        methods=['POST']
    )
    def login_submit(self, **post):
        login = post.get('login')
        password = post.get('password')

        try:
            uid = request.session.authenticate(request.db, login, password)
        except Exception as e:
            _logger.warning("Login failed for %s: %s", login, e)
            return request.render(
                'hospital_management.login_page',
                {'error': 'Invalid login or password'}
            )

        if not uid:
            return request.render(
                'hospital_management.login_page',
                {'error': 'Invalid login or password'}
            )

        user = request.env.user

        # ADMIN
        if user.has_group('hospital_management.group_hospital_admin'):
            return request.redirect('/web')

        # DOCTOR
        elif user.has_group('hospital_management.group_hospital_doctor'):
            return request.redirect('/web')

        # DEPARTMENT MANAGER
        elif user.has_group('hospital_management.group_hospital_department_manager'):
            return request.redirect('/department/dashboard')

        # PATIENT
        else:
            return request.redirect('/my/appointments')

    @http.route(
        "/register/submit",
        type="http",
        auth="public",
        website=True,
        methods=["POST"],
        csrf=True,
    )
    def register_submit(self, **post):
        name = post.get('name')
        email = post.get('email')
        phone = post.get('phone')
        password = post.get('password')

        if not (name and email and password):
            return request.render(
                "hospital_management.register_page",
                {"error": "Please fill in all required fields."}
            )

        existing_user = request.env['res.users'].sudo().search(
            [('login', '=', email)], limit=1
        )
        if existing_user:
            return request.render(
                "hospital_management.register_page",
                {"error": "An account with this email already exists. Please login instead."}
            )

        portal_group = request.env.ref('base.group_portal')
        patient_group = request.env.ref('hospital_management.group_hospital_patient')

        try:
            user = request.env['res.users'].sudo().create({
                'name': name,
                'login': email,
                'password': password,
                'groups_id': [(6, 0, [portal_group.id, patient_group.id])],
            })

            request.env['hospital.patient'].sudo().create({
                'name': name,
                'email': email,
                'phone': phone,
                'user_id': user.id,
            })

        except Exception as e:
            # This is the important part: instead of a silent/blank failure,
            # log the real exception to the server terminal AND show a
            # readable message on the register page.
            _logger.exception("Patient registration failed for %s", email)
            return request.render(
                "hospital_management.register_page",
                {"error": str(e)}
            )

        return request.redirect('/login')