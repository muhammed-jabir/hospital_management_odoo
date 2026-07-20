from odoo import models,fields

class Patient(models.Model):
    _name='hospital.patient'
    _description = 'patient details'

    name=fields.Char(string='Patient name',required=True)
    phone=fields.Char(string='Phone number')
    email=fields.Char(string='Email address',required=True)

    age=fields.Integer(string='Age')
    gender=fields.Selection([('male','Male'),('female','Female')],string='Gender')

    user_id=fields.Many2one('res.users',string='Portal User')
    partner_id=fields.Many2one('res.partner',string='Contact')


def id():
    return None