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
        'views/doctor_slot_views.xml',
        'views/gallery.xml',
        'views/about.xml',
        'data/mail_template_new.xml',
        'data/crone.xml',


        ],

    'assets': {
        'web.assets_frontend': [
        'hospital_management/static/lib/gsap/gsap.min.js',
        'hospital_management/static/lib/gsap/Flip.min.js',
        'hospital_management/static/lib/gsap/ScrollTrigger.min.js',

        'hospital_management/static/src/css/style.css',
        'hospital_management/static/src/css/animation.css',

        'hospital_management/static/src/js/animation.js',
        ],
    },
        

    'installable': True,
    'application': True,
}