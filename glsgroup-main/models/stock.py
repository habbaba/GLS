from odoo import models, fields, api, tools, _
from psycopg2 import sql
from datetime import datetime


class Stock(models.Model):
    _name = "gls.stock"

    ref_number = fields.Char(related='stock_move_id.picking_id.name',string='Referans')
    location_dest_id = fields.Many2one('stock.location', related='stock_move_id.location_dest_id', string='Location')
    lot_number = fields.Char(string='Lot Numarası',compute="_compute_lot_number")
    partner_id = fields.Many2one('res.partner',related='stock_move_id.picking_id.partner_id', string='Tedarikçi')
    product_id = fields.Many2one('product.product', related='stock_move_id.product_id', string='Ürün')
    source_document = fields.Char(related='stock_move_id.picking_id.origin', string='Kaynak Belge')
    state = fields.Selection(
        [('waiting', 'Bekliyor'), ('taken', 'Numune Alındı'), ('skipped', 'Analiz Yapılmadı'), ('done', 'Analiz Yapıldı')])
    accept_date = fields.Date("Numune Kabul Tarihi", readonly=True)
    stock_move_id = fields.Many2one('stock.move')
    analysis_id = fields.Many2one('gls.analysis', 'Analiz',)
    analysis_result_id = fields.Many2one('analysis.result')


    @api.depends('stock_move_id')
    def _compute_lot_number(self):
        for rec in self:
            stock_move_line = self.env['stock.move.line'].search([('move_id', '=', rec.stock_move_id.id), ('product_id', '=', rec.product_id.id)], limit=1)
            rec.lot_number = stock_move_line.lot_name


    def action_do_analysis(self):
        action = self.env['ir.actions.act_window']._for_xml_id('glsgroup-main.action_get_date')
        action['context'] = {'default_gls_stock_id': self.id}
        return action

    def action_dont_analysis(self):
        self.write({'state': 'skipped'})

    def action_set_data(self):
       
        action = self.env['ir.actions.act_window']._for_xml_id('glsgroup-main.action_set_data_table')
        action['context'] = self.env.context.copy()
        action['context'].update({
            'default_analysis_id': self.analysis_id.id,
            'default_product_id': self.product_id.id    
        })
        return action
        

    def action_reset(self):
        if self.state == 'done' and self.analysis_result_id:
            self.accept_date = False
            self.analysis_result_id.unlink()
        self.accept_date = False
        self.state = 'waiting'
