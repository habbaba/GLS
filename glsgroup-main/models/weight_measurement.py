from odoo import fields, models,api


class WeightMeasurement(models.Model):
    _name = 'weight.measurement'
    _rec_name = "gls_stock_id"



    gls_stock_id = fields.Many2one('gls.stock', compute="compute_gls_stock_id", store=True)
    partner_id = fields.Many2one('res.partner',related='gls_stock_id.partner_id', string='Tedarikçi')
    product_id = fields.Many2one('product.product', related='gls_stock_id.product_id', string='Ürün')
    product_qty = fields.Float(related='gls_stock_id.stock_move_id.product_qty',string='Adet')
    line_ids = fields.One2many('weight.measurement.line', 'weight_measurement_id')
    gross_weight = fields.Float()
    net_weight = fields.Float()
    stock_move_line_id = fields.Many2one('stock.move.line', "Lot Numarası", domain=lambda self: [('location_dest_id', '=', self.env.ref('stock.stock_location_company').id)])

    def action_create_pallet_lines(self):
        self.ensure_one()
        if self.gls_stock_id and not self.line_ids:
            self.line_ids = [(0,0,{'name':f'Palet {i}',}) for i in range(1, int(self.gls_stock_id.stock_move_id.product_qty) + 1)]

    
    @api.constrains('line_ids')
    def _constraint_line_ids(self):
        for rec in self:
            if rec.line_ids:
                rec.gross_weight = sum(rec.line_ids.mapped('value'))
                rec.net_weight = rec.gross_weight - 30



    @api.depends('stock_move_line_id')
    def compute_gls_stock_id(self):
        for rec in self:
            rec.gls_stock_id = self.env['gls.stock'].search([('stock_move_id', '=', rec.stock_move_line_id.move_id.id), ('analysis_id.pallet_weight', '=', True)], limit=1).id



class WeightMeasurementLine(models.Model):
    _name = 'weight.measurement.line'


    name = fields.Char("No")
    value = fields.Integer("Değer")
    weight_measurement_id = fields.Many2one('weight.measurement')