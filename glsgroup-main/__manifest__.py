# -*- coding: utf-8 -*-
{
    'name': "glsgroup",
    'summary': "",
    'description': "",
    'author': "My Company",
    'website': "http://www.yourcompany.com",
    'category': 'Uncategorized',
    'version': '0.1',
    'depends': ['base','product','stock',],
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
        'report/product_label.xml',
        'report/report.xml',
        'data/mail_template.xml',
        'menu/menu.xml',
        
        
        
    ],

}
