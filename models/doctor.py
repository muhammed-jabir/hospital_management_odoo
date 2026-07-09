from odoo import models,fields,api
from odoo.exceptions import ValidationError

class HospitalDoctor(models.Model):
    _name='hospital.doctor'
    _description='Hospital Doctor'

    name=fields.Char(string='Doctor Name',required=True)
    registration_no=fields.Char(string='Registration Number',required=True)
    age=fields.Integer(string='Age')
    phone=fields.Char(string='Phone Number',required=True)
    email=fields.Char(string='Email Address')
    department_id = fields.Many2one(
        "hospital.department"
    )  # mahy doctors can one dept
    image= fields.Image(string="Doctor Image")
    experience_level=fields.Char(string="Experience Level",compute="_compute_experience_level")
    user_id=fields.Many2one('res.users',string='Linked user login')# link with users  linked user setting in odoo
    slot_id=fields.One2many('hospital.doctor.slots','doctor_id',string='Available Slot')

    @api.depends('age')
    def _compute_experience_level(self):
        for doc in self:
            if doc.age>=45:
                doc.experience_level= 'senior'
            elif doc.age>=30:
                doc.experience_level='Mid-level'
            else:
                doc.experience_level= 'junior'

    @api.constrains('phone')
    def _check_phone(self):
        for ph in self:
            if ph.phone and (not ph.phone.isdigit() or len(ph.phone)!=10):
                raise ValidationError('phone number must be exact 10 numbers')











            




