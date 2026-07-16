
from odoo import http
from odoo.http import request


class HospitalAuth(http.Controller):

    @http.route(
        '/login',
        type='http',
        auth='public',
        website=True,

    )

    def login_page(self,**kwargs):
        return request.render('hospital_management.login_page')

    @http.route(
        '/login/submit',
        type='http',
        auth='public',
        website=True,
        methods=['POST']
    )
    def login_submit(self, **post):

        if request.httprequest.method == 'POST':
            login=post.get('login')
            password=post.get('password')

            try:
                uid=request.session.authenticate(request.db,login,password)

                if uid:

                    user = request.env.user

                    # ADMIN

                    if user.has_group(
                            'hospital_management.group_hospital_admin'
                    ):

                        return request.redirect('/web')


                    # DOCTOR

                    elif user.has_group(
                            'hospital_management.group_hospital_doctor'
                    ):

                        return request.redirect(
                            '/web'
                        )


                    # DEPARTMENT MANAGER

                    elif user.has_group(
                            'hospital_management.group_hospital_department_manager'
                    ):

                        return request.redirect(
                            '/department/dashboard'
                        )


                    # PATIENT

                    else:

                        return request.redirect(
                            '/my/appointments'
                        )


            except Exception:
                return request.render(
                    'hospital_management.login_page',
                    {
                        'error':'invalid login or password',

                    }

                )