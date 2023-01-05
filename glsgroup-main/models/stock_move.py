from odoo import models, fields, api


class StockMove(models.Model):
    _inherit = "stock.move"

    # @api.model_create_multi
    # def create(self, vals):
    #     res = super().create(vals)
    #     for rec in res:
    #         analysis_ids = res.product_id.product_tmpl_id.analysis_ids.mapped('analysis_id')
    #         for analysis in analysis_ids:
    #             if analysis.location_id.id == rec.location_dest_id.id:
    #                 self.env['gls.stock'].create({
    #                     'stock_move_id': rec.id,
    #                     'analysis_id': analysis.id,
    #                     'state': 'waiting'

    #                 })

    #     return res


class Picking(models.Model):
    _inherit = "stock.picking"

    def button_validate(self):
        res = super().button_validate()
        for move in self.move_ids_without_package:
            analysis_ids = move.product_id.product_tmpl_id.analysis_ids.mapped('analysis_id')
            for analysis in analysis_ids:
                if analysis.location_id.id == move.location_dest_id.id:
                    self.env['gls.stock'].create({
                        'stock_move_id': move.id,
                        'analysis_id': analysis.id,
                        'state': 'waiting'

                    })
        return res


