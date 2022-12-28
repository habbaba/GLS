from odoo import models, fields, api


class StockMove(models.Model):
    _inherit = "stock.move"


    @api.model
    def create(self, vals_list):
        res = super().create(vals_list)
        analysis_ids = res.product_id.product_tmpl_id.analysis_ids.mapped('analysis_id')
        for analysis in analysis_ids:
            self.env['gls.stock'].create({
                'stock_move_id': res.id,
                'analysis_id': analysis.id,
                'state': 'waiting'

            })    

        return res

      

       