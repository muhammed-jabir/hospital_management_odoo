import base64
import time
import logging
from locale import currency

from odoo import http
from odoo.addons.base.models.ir_actions_report import available
from odoo.http import request
from odoo.addons.payment.controllers.post_processing import PaymentPostProcessing

_logger = logging.getLogger(__name__)


class Hospital(http.Controller):

    @http.route('/', auth='public', website=True)
    def home(self, **kw):
        return request.render('hospital_management.home_page')

    @http.route('/doctors', auth='public', website=True)
    def doctors(self, **kw):
        doctors = request.env['hospital.doctor'].sudo().search([])
        return request.render('hospital_management.doctors_page', {
            'doctors': doctors
        })

    @http.route('/booking', auth='public', website=True)
    def booking(self, **kw):
        departments = request.env['hospital.department'].sudo().search([])
        slots=request.env['hospital.doctor.slots'].sudo().search([('state','=','available')])
        return request.render('hospital_management.booking_page', {
            'departments': departments,
            'slots':slots
        })

    @http.route('/get_doctors', type='json', auth='public', website=True)
    def get_doctors(self, department_id=None, **kw):
        domain = []
        if department_id:
            domain = [('department_id', '=', int(department_id))]
        doctors = request.env['hospital.doctor'].sudo().search(domain)
        return [{'id': d.id, 'name': d.name} for d in doctors]

    @http.route('/booking/submit', type='http', auth='public', website=True, csrf=True)
    def booking_submit(self, **post):
        # STEP A: Remember what the patient typed (including slot_id)
        uploaded_file = post.get('medical_report')
        file_base64 = False
        file_name = False
        if uploaded_file and getattr(uploaded_file, 'filename', None):
            file_name = uploaded_file.filename
            file_base64 = base64.b64encode(uploaded_file.read()).decode('utf-8')

        request.session['booking_data'] = {
            'patient_name': post.get('patient_name'),
            'email': post.get('email'),
            'phone': post.get('phone'),
            'date': post.get('date'),
            'department_id': post.get('department_id'),
            'doctor_id': post.get('doctor_id'),
            'slot_id': post.get('slot_id'),  # Storing the slot safely inside session storage
            'medical_report': file_base64,
            'medical_report_filename': file_name,
        }

        # STEP B: Find or create a "contact" for this patient
        partner = request.env['res.partner'].sudo().search(
            [('email', '=', post.get('email'))], limit=1
        ) or request.env['res.partner'].sudo().create({
            'name': post.get('patient_name'),
            'email': post.get('email'),
            'phone': post.get('phone'),
        })

        # STEP C: Get the Razorpay provider
        provider = request.env['payment.provider'].sudo().search(
            [('code', '=', 'razorpay')], limit=1
        )
        if not provider:
            return request.redirect('/booking')

        inr_currency = request.env['res.currency'].sudo().search([('name', '=', 'INR')], limit=1)
        currency_id = inr_currency.id if inr_currency else request.env.company.currency_id.id

        # STEP D: Create the "payment attempt" record
        tx = request.env['payment.transaction'].sudo().create({
            'provider_id': provider.id,
            'amount': 500.0,
            'currency_id': currency_id,
            'reference': f"APPT-{post.get('phone')}-{int(time.time())}",
            'partner_id': partner.id,
            'operation': 'online_redirect',
        })
        PaymentPostProcessing.monitor_transactions(tx)
        tx.landing_route = f'/payment/success?reference={tx.reference}'

        # STEP E: Get Razorpay's checkout form and auto-submit it
        redirect_html = tx._get_processing_values().get('redirect_form_html')
        if not redirect_html:
            return request.redirect('/booking')

        page = str(redirect_html) + '<script>document.forms[0].submit();</script>'
        response = request.make_response(page)
        response.headers['Content-Type'] = 'text/html; charset=utf-8'
        return response

    @http.route('/payment/success', type='http', auth='public', website=True)
    def payment_success(self, **kwargs):

        # STEP F: Look up the payment attempt by its reference
        tx = request.env['payment.transaction'].sudo().search(
            [('reference', '=', kwargs.get('reference'))], limit=1
        )

        # STEP G: Only proceed if payment genuinely succeeded
        if not tx or tx.state != 'done':
            return request.redirect('/booking')

        data = request.session.get('booking_data')
        if not data:
            return request.redirect('/booking')

        # STEP H: NOW actually create the appointment (only reached if paid)
        appointment_vals = {
            'name': data.get('patient_name'),
            'email': data.get('email'),
            'phone': data.get('phone'),
            'date': data.get('date'),
            'department_id': int(data['department_id']) if data.get('department_id') else False,
            'doctor_id': int(data['doctor_id']) if data.get('doctor_id') else False,
            'slot_id': int(data['slot_id']) if data.get('slot_id') else False,
            'partner_id': tx.partner_id.id,
            'state': 'confirmed',
        }
        if data.get('medical_report'):
            appointment_vals['medical_report'] = data['medical_report'].encode('utf-8')
            appointment_vals['medical_report_filename'] = data['medical_report_filename']

        appointment = request.env['hospital.appoinment'].sudo().create(appointment_vals)

        template = request.env.ref(
            'hospital_management.mail_template_appointment_confirmation', raise_if_not_found=False
        )
        if template:
            template.sudo().send_mail(appointment.id, force_send=True)

        request.session.pop('booking_data', None)
        return request.redirect('/booking-thank-you')
    @http.route('/booking-thank-you', auth='public', website=True)
    def booking_thank_you(self, **kw):
        return request.render('hospital_management.booking_thank_you_page')

    @http.route('/my-appointments', auth='user', website=True)
    def my_appointments(self, **kw):
        partner = request.env.user.partner_id
        appointments = request.env['hospital.appoinment'].sudo().search([
            ('partner_id', '=', partner.id)
        ])
        return request.render('hospital_management.my_appointments_page', {
            'appointments': appointments
        })