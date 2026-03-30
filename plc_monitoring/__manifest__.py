{
    'name': 'PLC Dashboard',
    'version': '1.0',
    'depends': ['base', 'web'],
    'author': 'Habibi',
    'category': 'Custom',
    'data': [
        'security/ir.model.access.csv',
        'views/plc_view.xml',
    ],
    'installable': True,
    'application': True,
    'assets': {
        'web.assets_backend': [
            'plc_monitoring/static/src/js/header_patch.js',
            'plc_monitoring/static/src/xml/header.xml',
            'plc_monitoring/static/src/js/auto_refresh.js',
        ],
    }, 
}