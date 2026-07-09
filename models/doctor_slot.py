

from odoo import fields,models,api



class HospitalDoctorSlots(models.Model):
    _name='hospital.doctor.slots'
    _description = 'Hospital Doctor Slots'
    _order='date,time_slot'



    name=fields.Char(string='Slot Name',compute='_compute_name',store=True)
    doctor_id=fields.Many2one('hospital.doctor',string='Doctor',required=True)
    date=fields.Date(string='Date',required=True)
    time_slot=fields.Char(string='Time Slot',required=True)

    state=fields.Selection([
        ('available','Available'),
        ('booked','Booked')
    ],string='Status',default='available',required=True,readonly=True)


    @api.depends('time_slot')
    def _compute_name(self):
        for rec in self:
            rec.name = rec.time_slot or ''




