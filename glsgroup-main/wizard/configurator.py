from odoo import models, fields


class ReferenceLinesList(models.TransientModel):
    _name = "gls.reference.lines.list"

    configurator_id = fields.Many2one(
        'gls.product.analysis.configurator.wizard')
    analysis_line_id = fields.Many2one('gls.analysis.line', 'Özellik')
    value = fields.Char(string="Referans Aralığı")


class ProductAnalysisConfigurator(models.TransientModel):
    _name = "gls.product.analysis.configurator.wizard"

    analysis_id = fields.Many2one('gls.analysis', 'Analiz')
    product_id = fields.Many2one('product.template', string="Ürün")
    reference_list_ids = fields.One2many(
        'gls.reference.lines.list', 'configurator_id', string="Analiz Özellikleri Listesi")

    def default_get(self, fields_list):
        res = super().default_get(fields_list)
        analysis_id = self.env['gls.analysis'].browse(res.get('analysis_id'))
        product_id = self.env['product.template'].browse(res.get('product_id'))
        records = self.env['gls.product.analysis.item'].search_read(
            [('product_id', '=', product_id.id), ('analysis_id', '=', analysis_id.id)], ['analysis_line_id', 'value'])


        analysis_dict_list = [{'analysis_line_id': record.id, 'value': 0.0} for record in analysis_id.analysis_line_ids]
        records_dict_list = [{'analysis_line_id': record['analysis_line_id'], 'value': record['value']} for record in records]

        for index, line in enumerate(analysis_dict_list):
            for record in records_dict_list:
                if record['analysis_line_id'][0] == line['analysis_line_id']:
                    analysis_dict_list[index]['value'] = record['value']
        
        res.update({
            'reference_list_ids': [(0, 0, {'analysis_line_id': record['analysis_line_id'], 'value': record['value']}) for record in analysis_dict_list],
        })

        return res

    def save_product_analysis(self):
        records = self.env['gls.product.analysis.item'].search(
            [('product_id', '=', self.product_id.id), ('analysis_id', '=', self.analysis_id.id)])
        if records:
            for record in self.reference_list_ids:
                update_record = self.env['gls.product.analysis.item'].search([('product_id', '=', self.product_id.id), (
                    'analysis_id', '=', self.analysis_id.id), ('analysis_line_id', '=', record.analysis_line_id.id)])
                if update_record:
                    update_record.value = record.value
                else:
                    vals = {
                        'product_id':self.product_id.id,
                        'analysis_id':self.analysis_id.id,
                        'analysis_line_id':record.analysis_line_id.id,
                        'value':record.value
                    }
                    self.env['gls.product.analysis.item'].create(vals)
        else:
            vals_list = [{
                'analysis_id': self.analysis_id.id,
                'analysis_line_id': record.analysis_line_id.id,
                'value': record.value,
                'product_id': self.product_id.id
            } for record in self.reference_list_ids]
            self.env['gls.product.analysis.item'].create(vals_list)
