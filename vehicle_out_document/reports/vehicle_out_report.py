from odoo import models, fields, api
from odoo.exceptions import UserError

class ReportVehicleOutReport(models.AbstractModel):
    _name = 'report.vehicle_out_document.vehicle_out_report'
    _description = 'Araç Çıkış Belgesi'

    @api.model
    def _get_report_values(self, docids, data=None):
        docs = self.env['stock.picking'].browse(docids)
        transfer_type = docs.mapped('picking_type_code')[0]
        edespatch_delivery_type = docs.mapped('edespatch_delivery_type')[0]
        if transfer_type != 'outgoing':
            raise UserError('Sadece çıkış işlemleri için bu belgeyi verebilirsiniz!')
        
        if not edespatch_delivery_type == "edespatch":
            raise UserError('Sadece E-İrsaliye için bu belgeyi verebilirsiniz!')

        return {
            'docs': docs,
        }