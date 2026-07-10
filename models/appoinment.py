from datetime import date

from odoo import fields, models,api
from odoo.exceptions import ValidationError



class HospitalAppoinment(models.Model):
    _name = 'hospital.appoinment'
    _description = 'Hospital Appoinment'

    name = fields.Char(string='Patient Name', required=True)
    email = fields.Char(string='Email Address')
    phone = fields.Char(string='Phone Number', required=True)
    date = fields.Date(string='Date of Appointment', required=True)
    department_id = fields.Many2one('hospital.department', string='Department') #one dept can have multiple appoinmnet
    doctor_id = fields.Many2one('hospital.doctor', string='Doctor', required=True) # many appoinments can get one doctor
    partner_id=fields.Many2one('res.partner', string='Partner account')
    state = fields.Selection([
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
    ], string='Status', default='pending')
    medical_report=fields.Binary(string='Medical Report')
    medical_report_filename=fields.Char(string='Medical report filename')
    slot_id=fields.Many2one('hospital.doctor.slots',string='Available Time Slots',required=True)
    amount=fields.Float(string='Fees',default=500.0)
    revenue=fields.Float(string='Revenue',compute='_compute_revenue',store=True)

    @api.model
    def _compute_revenue(self):
        for rec in self:
            rec.revenue=rec.amount if rec.state=='confirmed' else 0.0

    @api.model
    def create(self,vals):
        appointment=super(HospitalAppoinment,self).create(vals)
        if appointment.slot_id:
            appointment.slot_id.state='booked'
        return appointment


    def write(self,vals):
        if 'slot_in' in vals:
            old_slot=self.slot_id
            res=super(HospitalAppoinment,self).write(vals)
            if old_slot:
                old_slot.state= 'available'
            self.slot_id.state='booked'
            return res
        return super(HospitalAppoinment,self).write(vals)

    def unlink(self):
        for rec in self:
            if rec.slot_id:
                rec.slot_id.state='Available'
        return super(HospitalAppoinment,self).unlink()


    @api.constrains('date')
    def _check_date(self):
        for dat in self:
            if dat.date and dat.date < date.today():
                raise ValidationError('Date must be future')


    


