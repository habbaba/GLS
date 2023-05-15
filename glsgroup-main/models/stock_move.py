from odoo import models, fields, api


class StockMoveLine(models.Model):
    _inherit = "stock.move.line"

 
    
    def name_get(self):
        res = []
        for move in self:
            name = move.product_id.display_name
            if move.lot_id:
                name = '%s / %s' % (move.lot_id.name, name)
            res.append((move.id, name))
        return res

class Picking(models.Model):
    _inherit = "stock.picking"

    def button_validate(self):
        res = super().button_validate()
        for move in self.move_ids_without_package:
            analysis_ids = move.product_id.product_tmpl_id.analysis_ids.mapped('analysis_id')
            for analysis in analysis_ids:
                already_existing_records = self.env['gls.stock'].search([('stock_move_id', '=', move.id),('analysis_id', '=', analysis.id)])
                if analysis.location_id.id == move.location_dest_id.id and not already_existing_records:
                    self.env['gls.stock'].create({
                        'stock_move_id': move.id,
                        'analysis_id': analysis.id,
                        'state': 'waiting'
                    })
        return res


