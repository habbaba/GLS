from odoo import fields, models, api


class WeightMeasurement(models.Model):
    _name = 'weight.measurement'
    _rec_name = "gls_stock_id"


    @api.model
    def _get_move_line_domain(self):
        self.env.cr.execute("""
                                select sml.id from stock_move_line sml
                                join stock_picking sp on sp.id = sml.picking_id
                                join stock_picking_type spt on spt.id = sp.picking_type_id
                                where sml.lot_id is not NULL
                                and sml.location_dest_id=10
                                and spt.id=24
                                """)  
        result = self.env.cr.fetchall()
        print("result:", result)
        moves = self.env['stock.move.line'].browse([tup[0] for tup in result])
        return [
            ('id', 'in', moves.ids),
        ]

    gls_stock_id = fields.Many2one('gls.stock', compute="compute_gls_stock_id", store=True)
    partner_id = fields.Many2one('res.partner', related='stock_move_line_id.move_id.picking_id.partner_id', string='Tedarikçi')
    product_id = fields.Many2one('product.product', related='stock_move_line_id.move_id.product_id', string='Ürün')
    product_qty = fields.Float(related='stock_move_line_id.move_id.product_uom_qty', string='Adet')
    line_ids = fields.One2many('weight.measurement.line', 'weight_measurement_id')
    gross_weight = fields.Float()
    net_weight = fields.Float()
    stock_move_line_id = fields.Many2one('stock.move.line', "Lot Numarası",
                                         domain=lambda self: self._get_move_line_domain())

    def action_create_pallet_lines(self):
        self.ensure_one()
        if self.stock_move_line_id and not self.line_ids:
            self.line_ids = [(0, 0, {'name': f'Palet {i}', })
                             for i in range(1, int(self.product_qty) + 1)]

    @api.constrains('line_ids')
    def _constraint_line_ids(self):
        for rec in self:
            if rec.line_ids:
                rec.gross_weight = sum(rec.line_ids.mapped('value'))
                rec.net_weight = rec.gross_weight - 30

    @api.depends('stock_move_line_id')
    def compute_gls_stock_id(self):
        for rec in self:
            rec.gls_stock_id = self.env['gls.stock'].search(
                [('stock_move_id', '=', rec.stock_move_line_id.move_id.id), ('analysis_id.pallet_weight', '=', True)], limit=1).id


class WeightMeasurementLine(models.Model):
    _name = 'weight.measurement.line'

    name = fields.Char("No")
    value = fields.Integer("Değer")
    weight_measurement_id = fields.Many2one('weight.measurement')
