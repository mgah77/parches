# -*- coding: utf-8 -*-

{
    'name': 'Parches',
    'version': '1.04',
    'category': 'General',
    'summary': '',
    'description': """


       """,
    'author' : 'M.Gah',
    'website': '',
    'depends': ['stock','base','sale','l10n_cl_fe'],
    'data': [
	    "security/groups.xml",
	    "views/menu_informe.xml",
	    "views/export.xml",
        "views/libro2_view.xml",
        "views/account_payment_inherit.xml",
        "views/partner.xml",
        "security/ir.model.access.csv",
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}
