# -*- coding: utf-8 -*- 


{
 'name': 'Stock picking done cancel',
 'author': 'Soft-integration',
 'application': False,
 'installable': True,
 'auto_install': False,
 'qweb': [],
 'description': False,
 'images': [],
 'version': '1.0.1',
 'category': 'Stock',
 'demo': [],
 'depends': ['stock'],
 'data': [
          'security/stock_picking_done_cancel_security.xml',
          'security/ir.model.access.csv',
          'views/stock_picking_views.xml',
          'wizard/stock_picking_force_cancel_confirm_views.xml'
    ]
 }