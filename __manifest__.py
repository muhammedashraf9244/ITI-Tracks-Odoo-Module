{
    'name':"iti",
    'summary': "IIT is a custome module for recording and organizing ITI Tracks Business   ",
    'description':'''IIT is a custome module for recording and organizing ITI Tracks Business ''',
    'author':"MuhammedAshraf@ITITrackPython",
    'company':"ITI",
    'website': 'https://github.com/muhammedashraf9244',
    'version':"13.0.1",
    'depends': ['base'],
    'data':[
        "views/student_view.xml",
        "views/track_view.xml",
        "views/iti_courses.xml",
        "security/iti_security.xml",
        "security/ir.model.access.csv",
        "reports/iti_report_template.xml",
        "reports/iti_report.xml",
    ],
    'image': [
        'static/description/iti_logo1.png'
    ],
    'category': 'ThirdPartyModule',
    'installable': True,
    'application': True,
    'auto_install': False,
}