from odoo import fields, models, api, _

STOCK_LOCATION_ID = 10   #10 #36
STOCK_PICKING_TYPE_ID = 24 #24 #5


class WeightMeasurement(models.Model):
    _name = 'weight.measurement'


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

    name = fields.Char(string='Referans No', required=True,
                          readonly=True, default=lambda self: _('New'))
    partner_id = fields.Many2one('res.partner', compute="compute_partner_id", string='Tedarikçi',store=True)
    product_id = fields.Many2one('product.product', related='stock_move_line_id.move_id.product_id', string='Ürün')
    product_qty = fields.Float(related='stock_move_line_id.move_id.product_uom_qty', string='Adet')
    line_ids = fields.One2many('weight.measurement.line', 'weight_measurement_id')
    gross_weight = fields.Float()
    net_weight = fields.Float()
    stock_move_line_id = fields.Many2one('stock.move.line', "Lot Numarası",
                                         domain=lambda self: self._get_move_line_domain())
    stock_move_id = fields.Many2one('stock.move', related='stock_move_line_id.move_id', store=True)

    def action_create_pallet_lines(self):
        self.ensure_one()
        if self.stock_move_line_id and not self.line_ids:
            self.line_ids = [(0, 0, {'name': f'Palet {i}', })
                             for i in range(1, int(self.product_qty) + 1)]

    @api.constrains('line_ids')
    def _constraint_line_ids(self):
        for rec in self:
            if rec.line_ids:
                rec.gross_weight = sum(rec.line_ids.mapped('value'))/len(rec.line_ids)
                rec.net_weight = rec.gross_weight - 30


            
    @api.depends('stock_move_line_id')
    def compute_partner_id(self):
        for rec in self:
            if rec.stock_move_line_id:
                rec.partner_id = self.env['stock.picking'].search(
                    [('origin', '=', rec.stock_move_line_id.move_id.origin), ('partner_id', '!=', False)], limit=1).partner_id.id
            else:
                rec.partner_id = False


    
    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code(
                'weight.measurement') or _('New')
        res = super(WeightMeasurement, self).create(vals)
        return res


class WeightMeasurementLine(models.Model):
    _name = 'weight.measurement.line'

    name = fields.Char("No")
    value = fields.Integer("Değer")
    weight_measurement_id = fields.Many2one('weight.measurement')
