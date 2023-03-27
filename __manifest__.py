{
    'name': 'MICEN_RH',
    'version': '1.0',
    'description': 'Module Permettant de gerer le flux de demande du Ministère',
    'summary': 'PROCESS DE GESTION DES DOCUMENTS RH Du MICEN',
    'author': 'N"Doua Jean Marie',
    'images': ['static/description/img1.jpeg'],
    'website': '',
    'license': 'LGPL-3',
    'category': 'Gestion',
    'depends': [
        'mail',
        'base',
        'hr',
        'hr_holidays',
    ],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/assets.xml',
        'views/flux_demande_view.xml',
        
        'report/flux_demande_report.xml',
        'report/attestation_presence_report.xml',
        'report/attestation_travail_report.xml',
        'report/certificat_prise_service_report.xml',
        'report/certificat_travail_report.xml',
        'report/note_affectation_report.xml',
        'report/reprise_service_report.xml',
        'report/fiche_signaletique_report.xml',
        'report/cessation_travail_report.xml',
        
        'views/home_views.xml',
        'views/mon_profil_view.xml',
        'views/certificat_prise_service.xml',
        'views/reprise_service.xml',
        'views/attestation_presence.xml',
        'views/attestation_travail.xml',
        'views/certificat_travail.xml',
        'views/note_affectation.xml',
        'views/cessation_service.xml',
        'views/espace_rh.xml',
        'views/menu.xml',
    ],
    'auto_install': False,
    'application': False,
}

# 'assets': {
        
#     }