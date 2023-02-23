from odoo import fields, models


class WeightMeasurement(models.Model):
    _name = 'weight.measurement'
    _rec_name = "gls_stock_id"



    gls_stock_id = fields.Many2one('gls.stock', "Lot Numarası", domain="[('analysis_id.pallet_weight', '=', True)]")
    partner_id = fields.Many2one('res.partner',related='gls_stock_id.partner_id', string='Tedarikçi')
    product_id = fields.Many2one('product.product', related='gls_stock_id.product_id', string='Ürün')
    product_qty = fields.Float(related='gls_stock_id.stock_move_id.product_qty',string='Adet')
    line_ids = fields.One2many('weight.measurement.line', 'weight_measurement_id')


    def action_create_pallet_lines(self):
        self.ensure_one()
        if self.gls_stock_id and not self.line_ids:
            self.line_ids = [(0,0,{'name':f'Palet {i}',}) for i in range(1, int(self.gls_stock_id.stock_move_id.product_qty) + 1)]




class WeightMeasurementLine(models.Model):
    _name = 'weight.measurement.line'


    name = fields.Char("No")
    value = fields.Integer("Değer")
    weight_measurement_id = fields.Many2one('weight.measurement')