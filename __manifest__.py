# -*- coding: utf-8 -*-

{
    'name': 'Parches',
    'version': '1.03',
    'category': 'General',
    'summary': '',
    'description': """
        - Agrega atributo de reparable a producto
    - Menu Taller
       """,
    'author' : 'M.Gah',
    'website': '',
    'depends': ['stock','base','sale'],
    'data': [
	    "security/groups.xml",
	    "views/menu_informe.xml",
	    "views/export.xml",
        "views/libro2_view.xml",
        "views/account_payment_inherit.xml",
        "views/partner.xml"
        "security/ir.model.access.csv",
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}
