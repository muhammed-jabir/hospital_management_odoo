from odoo.tests import TransactionCase
from odoo.exceptions import ValidationError


class TestAppointmentBooking(TransactionCase):

    def setUp(self):
        super(TestAppointmentBooking, self).setUp()
        self.department = self.env['hospital.department'].create({
            'name': 'Test Department',
        })
        self.doctor = self.env['hospital.doctor'].create({
            'name': 'Dr Test',
            'registration_no': 'REG001',
            'phone': '9876543210',
            'department_id': self.department.id,
        })
        self.slot = self.env['hospital.doctor.slots'].create({
            'doctor_id': self.doctor.id,
            'date': '2026-08-01',
            'time_slot': '10:00-11:00',
        })

    def test_slot_starts_available(self):
        """A freshly created slot should default to available"""
        self.assertEqual(self.slot.state, 'available')

    def test_booking_marks_slot_as_booked(self):
        """Creating an appointment should flip the slot to booked"""
        self.env['hospital.appoinment'].create({
            'name': 'Priya',
            'phone': '9000000001',
            'date': '2026-08-01',
            'doctor_id': self.doctor.id,
            'slot_id': self.slot.id,
        })
        self.assertEqual(self.slot.state, 'booked')

    def test_double_booking_same_slot_is_blocked(self):
        """A second appointment on an already-booked slot must be rejected"""
        self.env['hospital.appoinment'].create({
            'name': 'Priya',
            'phone': '9000000001',
            'date': '2026-08-01',
            'doctor_id': self.doctor.id,
            'slot_id': self.slot.id,
        })
        with self.assertRaises(ValidationError):
            self.env['hospital.appoinment'].create({
                'name': 'Anand',
                'phone': '9000000002',
                'date': '2026-08-01',
                'doctor_id': self.doctor.id,
                'slot_id': self.slot.id,
            })