from odoo import api, fields, models, _


class ProductTemplate(models.Model): 
    _inherit = "product.template"
    
 
    
    analysis_ids = fields.Many2many('gls.product.analysis','product_template_id' ,string="Analiz Satırları")



