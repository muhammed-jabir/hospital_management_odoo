from odoo import fields, models, api
from odoo.exceptions import ValidationError


class HospitalAppoinment(models.Model):
    _name = 'hospital.appoinment'
    _description = 'Hospital Appointment'

    name = fields.Char(string='Patient Name', required=True)
    email = fields.Char(string='Email Address')
    phone = fields.Char(string='Phone Number', required=True)
    date = fields.Date(string='Date of Appointment', required=True)
    department_id = fields.Many2one('hospital.department', string='Department')
    doctor_id = fields.Many2one('hospital.doctor', string='Doctor', required=True)
    partner_id = fields.Many2one('res.partner', string='Partner account')
    patient_id = fields.Many2one('hospital.patient', string='Patient',required=True)
    state = fields.Selection([
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ], string='Status', default='pending')
    medical_report = fields.Binary(string='Medical Report')
    medical_report_filename = fields.Char(string='Medical report filename')
    slot_id = fields.Many2one('hospital.doctor.slots', string='Available Time Slots', required=True)
    amount = fields.Float(string='Fees', default=500.0)
    revenue = fields.Float(string='Revenue', compute='_compute_revenue', store=True)

    @api.depends('amount', 'state')
    def _compute_revenue(self):
        for rec in self:
            rec.revenue = rec.amount if rec.state in ('confirmed', 'completed') else 0.0

    @api.model
    def create(self, vals):
        appointment = super(HospitalAppoinment, self).create(vals)
        if appointment.slot_id:
            appointment.slot_id.write({'state': 'booked', 'held_at': False})
        return appointment

    def write(self, vals):
        if 'slot_id' in vals:
            old_slot = self.slot_id
            res = super(HospitalAppoinment, self).write(vals)
            if old_slot and old_slot != self.slot_id:
                old_slot.write({'state': 'available'})
            if self.slot_id:
                self.slot_id.write({'state': 'booked'})
            return res
        return super(HospitalAppoinment, self).write(vals)

    def unlink(self):
        for rec in self:
            if rec.slot_id:
                rec.slot_id.write({'state': 'available'})
        return super(HospitalAppoinment, self).unlink()

    @api.constrains('slot_id')
    def _check_slot_available(self):
        for rec in self:
            if rec.slot_id and rec.slot_id.state == 'booked':
                existing = self.search_count([
                    ('slot_id', '=', rec.slot_id.id),
                    ('id', '!=', rec.id),
                    ('state', '!=', 'cancelled'),
                ])
                if existing:
                    raise ValidationError('This slot has already been booked. Please choose another.')

    # ---------------------------------------------------------------
    # Doctor-facing workflow actions
    # ---------------------------------------------------------------

    def action_confirm(self):
        for rec in self:
            if rec.state != 'pending':
                raise ValidationError('Only pending appointments can be confirmed.')
            rec.state = 'confirmed'

            template = self.env.ref(
                'hospital_management.mail_template_appointment_confirmation',
                raise_if_not_found=False
            )
            if template:
                template.sudo().send_mail(rec.id, force_send=True)

    

    def action_complete(self):
        for rec in self:
            if rec.state != 'confirmed':
                raise ValidationError('Only confirmed appointments can be marked completed.')
            rec.state = 'completed'

    def action_cancel(self):
        for rec in self:
            if rec.state not in ('pending', 'confirmed'):
                raise ValidationError('This appointment cannot be cancelled from its current status.')
            rec.state = 'cancelled'
            if rec.slot_id:
                rec.slot_id.write({'state': 'available', 'held_at': False})