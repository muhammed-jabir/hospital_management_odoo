from odoo import models, fields

class HospitalDepartment(models.Model):
    _name = 'hospital.department'
    _description = 'Hospital Department'

    name = fields.Char(string='Department Name', required=True)
    doctor_ids = fields.One2many('hospital.doctor', 'department_id', string='Doctors') # department have many doctors
    manager_id=fields.Many2one('res.users',string='department manager') # dept have only one manger and manger is odoo res,user