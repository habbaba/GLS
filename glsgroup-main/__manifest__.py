# -*- coding: utf-8 -*-
{
    'name': "glsgroup",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','product','stock',],

    # always loaded
    'data': [
        
        'security/ir.model.access.csv',
        'views/analysis_view.xml',
        'views/product_inherit_view.xml',
        'views/product_analysis_view.xml',
        'views/stock_view.xml',
        'wizard/configurator.xml',
        'wizard/get_date_view.xml',           
        'wizard/set_data.xml',
        'views/analysis_result_view.xml',
        'report/analysis_report.xml',
        'report/report.xml',
        'data/mail_template.xml',
        'menu/menu.xml',
        
        
        
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
