from odoo import models, fields, api
from odoo.exceptions import ValidationError


class HospitalPrescription(models.Model):
    _name = 'hospital.prescription'
    _description = 'Hospital Prescription'
    _rec_name = 'name'

    name = fields.Char(
        string='Prescription No',
        default='New',
        readonly=True,
        copy=False
    )

    appointment_id = fields.Many2one(
        'hospital.appoinment',
        string='Appointment',
        required=True,
        ondelete='cascade'
    )

    patient_id = fields.Many2one(
        'hospital.patient',
        string='Patient',
        related='appointment_id.patient_id',
        store=True,
        readonly=True
    )

    doctor_id = fields.Many2one(
        'hospital.doctor',
        string='Doctor',
        related='appointment_id.doctor_id',
        store=True,
        readonly=True
    )

    date = fields.Date(
        string='Prescription Date',
        default=fields.Date.today,
        required=True
    )

    diagnosis = fields.Text(string='Diagnosis')
    advice = fields.Text(string='Advice / Instructions')

    line_ids = fields.One2many(
        'hospital.prescription.line',
        'prescription_id',
        string='Medicines'
    )

    @api.model
    def create(self, vals):
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code(
                'hospital.prescription'
            ) or 'New'

        prescription = super().create(vals)

        # link back to appointment
        if prescription.appointment_id:
            prescription.appointment_id.prescription_id = prescription.id

        return prescription


class HospitalPrescriptionLine(models.Model):
    _name = 'hospital.prescription.line'
    _description = 'Prescription Medicine Line'

    prescription_id = fields.Many2one(
        'hospital.prescription',
        string='Prescription',
        required=True,
        ondelete='cascade'
    )

    medicine_name = fields.Char(string='Medicine', required=True)
    dosage = fields.Char(string='Dosage', required=True)
    frequency = fields.Char(string='Frequency')
    duration = fields.Char(string='Duration', required=True)
    notes = fields.Char(string='Notes')