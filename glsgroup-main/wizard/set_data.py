from odoo import models, fields
from odoo.exceptions import ValidationError


class AnalysisConfTable(models.Model):
    _name = "gls.set.data.table.wizard"

    result_ids = fields.One2many(
        'gls.set.data.wizard', 'table_id', string='Sonuçları Giriniz')

    def default_get(self, fields_list):
        res = super().default_get(fields_list)
        analysis_id = self.env.context.get('default_analysis_id')
        product_id = self.env['product.product'].browse(self.env.context.get('default_product_id'))
        pallet_weight = self.env['gls.analysis'].browse(self.env.context.get('default_analysis_id')).pallet_weight


        result_line_ids = self.env['gls.product.analysis.item'].search(
            [('product_id', '=', product_id.product_tmpl_id.id), ('analysis_id', '=', analysis_id)])

        if not result_line_ids:
            raise ValidationError(
                "Belirtilen Ürün İçin Referans Aralığı Giriniz")

        res.update({
            'result_ids': [(0, 0, {'analysis_id': record.analysis_id.id, 'product_id': product_id.id, 'analysis_line_id': record.analysis_line_id.id, 'value': record.value}) for record in result_line_ids]
        })

        if pallet_weight:
            gross_weight_line_id = self.env['gls.analysis.line'].search([('analysis_id', '=', analysis_id), ('feature', 'ilike', '%brüt%')])
            net_weight_line_id = self.env['gls.analysis.line'].search([('analysis_id', '=', analysis_id), ('feature', 'ilike', '%net%')])
            stock_move_id = self.env.context.get('stock_move_id')
            weight_measurement_id = self.env['weight.measurement'].search([('stock_move_id', '=', stock_move_id)], limit=1)
            if weight_measurement_id:
                for item in res['result_ids']:
                    if item[2]['analysis_line_id'] == gross_weight_line_id.id:
                        item[2]['result']=weight_measurement_id.gross_weight
                    if item[2]['analysis_line_id'] == net_weight_line_id.id:
                        item[2]['result']=weight_measurement_id.net_weight

        return res

    def save_data_analysis(self):
        product_move_id, analysis_result_vals = self.prepare_values()
        result_line_ids = self.env['gls.product.analysis.item'].search(
            [('product_id', '=', product_move_id.product_id.product_tmpl_id.id), ('analysis_id', '=', product_move_id.analysis_id.id)])
        analysis_result_vals.update({
            'result_line_ids': [(0, 0,
                                 {'feature': second.analysis_line_id.feature,
                                  'unit': second.analysis_line_id.unit,
                                  'method': second.analysis_line_id.method,
                                  'reference_range': second.value,
                                  'result': first.result}) for first, second in zip(self.result_ids, result_line_ids)]
        })
        record = self.env['analysis.result'].create(analysis_result_vals)
        if record:
            product_move_id.state = 'done'
            product_move_id.write({
                'state':'done',
                'analysis_result_id': record.id
            })


    def prepare_values(self):
        ctx = self.env.context
        active_model = ctx.get('active_model')
        active_id = ctx.get('active_id')
        product_move_id = self.env[active_model].browse(active_id)
        vals = {
            'analysis_id': product_move_id.analysis_id.id,
            'product_id': product_move_id.product_id.id,
            'lot_number': product_move_id.lot_number,
            'partner_id': product_move_id.partner_id.id,
            'accept_date': product_move_id.accept_date,
            'ref_number': product_move_id.ref_number,
        }
        return product_move_id,vals


class SetDataConfigurator(models.Model):
    _name = "gls.set.data.wizard"

    analysis_id = fields.Many2one('gls.analysis', 'Analiz')
    analysis_line_id = fields.Many2one('gls.analysis.line', 'Özellik')
    feature = fields.Char(related='analysis_line_id.feature', string="Analiz Kalemi")
    unit = fields.Char(related='analysis_line_id.unit', string="Birim")
    method = fields.Char(related='analysis_line_id.method', string="Metot")
    value = fields.Char(string="Referans Aralığı", readonly=True)
    product_id = fields.Many2one('product.template', string="Ürün")
    result = fields.Char(string="Sonuç")
    table_id = fields.Many2one('gls.set.data.table.wizard')
