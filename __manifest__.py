{
    'name': 'Solicitudes',
    'summary': 'Módulo de solicitudes.',
    'description': 'Módulo para la gestión de solicitudes.',
    'author': 'Contreras Pumamango Gianmarco - gmcontrpuma@gmail.com',
    'website': 'https://github.com/CodigoByte2020',
    'category': 'Tools',
    'version': '16.0.0.0.1',
    'depends': [
        'openeducat_admission',
        'portal'
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/isep_requests_menus.xml',
        'views/request_views.xml',
        'views/catalog_request_views.xml',
        'views/portal_templates.xml',
        'wizards/observe_document_views.xml'
    ],
    'installable': True,
}
