from odoo import fields, models, api

STOCK_LOCATION_ID = 10
STOCK_PICKING_TYPE_ID = 24


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
                                and sml.location_dest_id=%(STOCK_LOCATION_ID)s
                                and spt.id=%(STOCK_PICKING_TYPE_ID)s
                                """,{
            'STOCK_LOCATION_ID': STOCK_LOCATION_ID,
            'STOCK_PICKING_TYPE_ID': STOCK_PICKING_TYPE_ID,
        } )  
        result = self.env.cr.fetchall()
        moves = self.env['stock.move.line'].browse([tup[0] for tup in result])
        return [
            ('id', 'in', moves.ids),
        ]

    gls_stock_id = fields.Many2one('gls.stock', compute="compute_gls_stock_id")
    partner_id = fields.Many2one('res.partner', compute="compute_partner_id", string='Tedarikçi',store=True)
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
            if rec.stock_move_line_id:
                rec.gls_stock_id = self.env['gls.stock'].search(
                    [('stock_move_id', '=', rec.stock_move_line_id.move_id.id), ('analysis_id.pallet_weight', '=', True)], limit=1).id
            else:
                rec.gls_stock_id = False
            
    @api.depends('stock_move_line_id')
    def compute_partner_id(self):
        for rec in self:
            if rec.stock_move_line_id:
                rec.partner_id = self.env['stock.picking'].search(
                    [('origin', '=', rec.stock_move_line_id.move_id.origin), ('partner_id', '!=', False)], limit=1).partner_id.id
            else:
                rec.partner_id = False


class WeightMeasurementLine(models.Model):
    _name = 'weight.measurement.line'

    name = fields.Char("No")
    value = fields.Integer("Değer")
    weight_measurement_id = fields.Many2one('weight.measurement')
