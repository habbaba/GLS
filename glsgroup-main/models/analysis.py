from collections import defaultdict, OrderedDict
from odoo import api, fields, models, _


class Analysis(models.Model): 
    _name = "gls.analysis"
    

    name=fields.Char(string="Analiz Adı")
    customer_share= fields.Boolean(string="Müşteri İle Paylaşılacak mı?")
    pallet_weight =fields.Boolean(string="Palet Ağırlığı Gerekli Mi?")
    analysis_line_ids = fields.One2many('gls.analysis.line', 'analysis_id', string="Analiz Satırları")
    note = fields.Html(string="Açıklama")
    location_id = fields.Many2one('stock.location', 'Analiz Konumu', domain="[('usage', '=', 'internal')]", required=True)
    count_waiting_process= fields.Integer(compute='_compute_all_process')
    count_taken_process= fields.Integer(compute='_compute_all_process')
    count_skipped_process= fields.Integer(compute='_compute_all_process')
    count_done_process= fields.Integer(compute='_compute_all_process')
    responsible_id = fields.Many2one('res.users', string='Analiz Sorumlusu')



    def get_stock_action(self):
        action= self.env['ir.actions.act_window']._for_xml_id('glsgroup-main.gls_stock_action')
        action["domain"] = [('analysis_id', '=', self.id)]
        return  action
    

    def _compute_all_process(self):
        for rec in self:
            rec.count_waiting_process = self.env['gls.stock'].search_count([('analysis_id', '=', rec.id), ('state', '=', 'waiting')])
            rec.count_taken_process = self.env['gls.stock'].search_count([('analysis_id', '=', rec.id), ('state', '=', 'taken')])
            rec.count_skipped_process = self.env['gls.stock'].search_count([('analysis_id', '=', rec.id), ('state', '=', 'skipped')])
            rec.count_done_process = self.env['gls.stock'].search_count([('analysis_id', '=', rec.id), ('state', '=', 'done')])

    
    def get_action_stock_ready(self):
        action= self.env['ir.actions.act_window']._for_xml_id('glsgroup-main.gls_stock_action')
        action["domain"] = [('analysis_id', '=', self.id), ('state', '=', 'waiting')]
        return  action

    def get_action_stock_taken(self):
        action= self.env['ir.actions.act_window']._for_xml_id('glsgroup-main.gls_stock_action')
        action["domain"] = [('analysis_id', '=', self.id), ('state', '=', 'taken')]
        return  action

    def get_action_stock_skipped(self):
        action= self.env['ir.actions.act_window']._for_xml_id('glsgroup-main.gls_stock_action')
        action["domain"] = [('analysis_id', '=', self.id), ('state', '=', 'skipped')]
        return  action    

    def get_action_stock_done(self):
        action= self.env['ir.actions.act_window']._for_xml_id('glsgroup-main.gls_stock_action')
        action["domain"] = [('analysis_id', '=', self.id), ('state', '=', 'done')]
        return  action   
    


class AnalysisLine(models.Model):
    _name= "gls.analysis.line"
    _rec_name="feature"
    
    analysis_id = fields.Many2one('gls.analysis', string= "Analiz Adı")
    feature = fields.Char(string="Analiz Kalemi")
    unit = fields.Char(string="Birim")   
    method = fields.Char(string="Metot")


class ProductAnalysisItem(models.Model):
    
    _name= "gls.product.analysis.item"
     
        
    analysis_id = fields.Many2one('gls.analysis', 'Analiz')
    analysis_line_id=fields.Many2one('gls.analysis.line', 'Özellik')
    value = fields.Char(string="Referans Aralığı")
    product_id=fields.Many2one('product.template', string= "Ürün")



class ProductAnalysis(models.Model):
    _name='gls.product.analysis'


    analysis_id = fields.Many2one('gls.analysis', 'Analiz')
    product_template_id = fields.Many2one('product.template')

    def action_open_reference(self):
        
        product_id = self.env.context.get('default_product_id')
        action = self.env['ir.actions.act_window']._for_xml_id('glsgroup-main.action_adjust_reference')
        action['context'] = self.env.context.copy()
        action['context'].update({
            'default_analysis_id': self.analysis_id.id,
            'default_product_id': product_id,             
        })
        return action
    

    
