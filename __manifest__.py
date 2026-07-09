{
    'name': 'Hospital Website',
    'version': '1.0',
    'depends': ['website','payment'],

    'data': [
        'security/hospital_security.xml',
        'security/ir.model.access.csv',
        'views/home.xml',
        'views/inherit_layout.xml',
        'views/booking.xml',
        'views/doctors.xml',
        'views/appoinment_report.xml',
        'data/mail_template_new.xml',
        'views/doctor_slot_views.xml'

    ],

    'assets': {
        'web.assets_frontend': [
            'hospital_management/static/src/css/style.css',
        ],
    },

    'installable': True,
    'application': True,
}