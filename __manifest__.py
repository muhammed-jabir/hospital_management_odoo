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
        'views/prescription.xml',
        'views/doctors.xml',
        'views/doctor_slot_views.xml',
        'views/gallery.xml',
        'views/about.xml',
        'views/login.xml',
        'views/register.xml',
        'data/mail_template_new.xml',
        'data/crone.xml',
        'data/prescription_sequence.xml',
        'report/appoinment_report.xml',
        'report/prescription_report.xml',
        'report/prescription_template.xml'



        ],

    'assets': {
        'web.assets_frontend': [
        'hospital_management/static/lib/gsap/gsap.min.js',
        'hospital_management/static/lib/gsap/Flip.min.js',
        'hospital_management/static/lib/gsap/ScrollTrigger.min.js',

        'hospital_management/static/src/css/style.css',
        'hospital_management/static/src/css/animation.css',
        'hospital_management/static/src/css/cursor.css',

        'hospital_management/static/src/js/animation.js',
        'hospital_management/static/src/js/cursor.js',

        ],
        'web.assets_backend':[

             'hospital_management/static/src/xml/doctor_dashboard.xml',
            'hospital_management/static/src/js/doctor_dashboard.js',

            'hospital_management/static/src/css/doctor_dashboard.css',

        ]
    },


        

    'installable': True,
    'application': True,
}