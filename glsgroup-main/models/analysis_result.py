from odoo import models, fields, api,_
import pytz


class AnalysisResult(models.Model):
    _name = "analysis.result"
    _description = "Analiz Sonucu"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(compute="compute_name")
    analysis_id = fields.Many2one('gls.analysis', 'Analiz',)
    product_id = fields.Many2one('product.product', string='Ürün')
    lot_number = fields.Char(string='Lot Numarası')
    partner_id = fields.Many2one('res.partner', string='Tedarikçi')
    accept_date = fields.Date("Numune Kabul Tarihi", readonly=True)
    ref_number = fields.Char(string='Stok Hareketi Referans')
    result_line_ids = fields.One2many('analysis.result.line', 'analysis_result_id')
    create_date = fields.Datetime("Oluşturulma Tarihi", readonly=True)
    create_uid = fields.Many2one('res.users', string="Oluşturan", readonly=True)
    company_id = fields.Many2one('res.company', string='Company', required=True, readonly=True,
        default=lambda self: self.env.company)

    def compute_name(self):
        for rec in self:
            rec.name = rec.analysis_id.name+"/"+rec.product_id.display_name+"/"+ rec.lot_number if rec.lot_number else ""

    def _get_report_base_filename(self):
        self.ensure_one()
        return 'Analiz Raporu-%s' % (self.name)

    
    def _get_lot_id_create_date(self):
        custom_stock = self.env['gls.stock'].search([('analysis_result_id', '=', self.id)])
        time = None
        if custom_stock:
            user = self.env['res.users'].browse(self.env.uid)
            tz = pytz.timezone(user.tz)
            time = (pytz.utc.localize(custom_stock.lot_id.create_date).astimezone(tz)).strftime("%m/%d/%Y %H:%M:%S")
        return time

    

    def send_by_email_with_attachment(self):
        self.ensure_one()
        ir_model_data = self.env['ir.model.data']
        try:
            template_id = ir_model_data._xmlid_lookup('glsgroup-main.email_template_gls_analysis')[2]
        except ValueError:
            template_id = False
        try:
            compose_form_id = ir_model_data._xmlid_lookup('mail.email_compose_message_wizard_form')[2]
        except ValueError:
            compose_form_id = False
        ctx = dict(self.env.context or {})
        ctx.update({
            'default_model': 'analysis.result',
            'active_model': 'analysis.result',
            'active_id': self.ids[0],
            'default_res_id': self.ids[0],
            'default_use_template': bool(template_id),
            'default_template_id': template_id,
            'default_composition_mode': 'comment',
            'custom_layout': "mail.mail_notification_paynow",
            'force_email': True,
            'mark_rfq_as_sent': True,
            'model_description': "Analiz Sonucu",
        })
        return {
            'name': _('Compose Email'),
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'mail.compose.message',
            'views': [(compose_form_id, 'form')],
            'view_id': compose_form_id,
            'target': 'new',
            'context': ctx,
        }


class AnalysisResultLine(models.Model):
    _name = "analysis.result.line"

    feature = fields.Char(string="Analiz Kalemi", )
    unit = fields.Char(string="Birim")
    method = fields.Char(string="Metot")
    reference_range = fields.Char(string="Referans Aralığı")
    result = fields.Char(string="Sonuç")
    analysis_result_id = fields.Many2one('analysis.result')
    analysis_id = fields.Many2one('gls.analysis', 'Analiz', related='analysis_result_id.analysis_id', store=True)
    product_id = fields.Many2one('product.product', 'Ürün', related='analysis_result_id.product_id', store=True)
    lot_number = fields.Char(string='Lot Numarası',related='analysis_result_id.lot_number', store=True)
    partner_id = fields.Many2one('res.partner', string='Tedarikçi',related='analysis_result_id.partner_id', store=True)
