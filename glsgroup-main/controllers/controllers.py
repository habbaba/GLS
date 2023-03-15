from odoo import http
from odoo.http import request,content_disposition
from odoo import exceptions, SUPERUSER_ID

class Glsgroup(http.Controller):
    @http.route('/analizsonuclari', website=True, auth='public')
    def index(self, **kw):
        context = {}
        if request.httprequest.method == 'POST':
            lot_number = kw.get('search', False)
            records = None
            if lot_number:
                records = request.env['analysis.result'].with_user(SUPERUSER_ID).search([('lot_number', 'ilike', lot_number),('analysis_id.customer_share', '=', True)])
            else:
                return request.redirect('/analizsonuclari')
            if records:
                return request.redirect('/analizsonuclari/rapor?lot=%s' % (records[0].lot_number))
            else:
                context.update({
                    'search': kw.get('search', False),
                    'error': True,
                })
        if request.httprequest.method == 'GET':
            context['error'] = False

        return request.render('glsgroup-main.search_page', context)

    @http.route('/analizsonuclari/rapor', auth='public')
    def detail(self, **kw):
        lot_number = kw.get('lot', False)
        record = request.env['analysis.result'].with_user(SUPERUSER_ID).search([('lot_number', 'ilike', lot_number),('analysis_id.customer_share', '=', True)], limit=1)
        if lot_number and record:
            context = {
                'record': record
            }
            return request.render('glsgroup-main.detail_page', context)

        else:
            return request.redirect('/analizsonuclari')

    @http.route('/file/download', auth='public')
    def download(self, **kw):
        records = None
        lot_number = kw.get('lot', False)
        if lot_number:
            records = request.env['analysis.result'].with_user(SUPERUSER_ID).search([('lot_number', 'ilike', lot_number),('analysis_id.customer_share', '=', True)])
        if records:
            pdf = request.env.ref('glsgroup-main.analysis_result_report').with_user(SUPERUSER_ID)._render_qweb_pdf(res_ids=records.ids)[0]
            report_content_disposition = content_disposition(f'{records[0].product_id.display_name}-analiz-sonucu.pdf')
            pdfhttpheaders = [
                ('Content-Type', 'application/pdf'),
                ('Content-Length', len(pdf)),
                ('Content-Disposition', report_content_disposition)
            ]
            return request.make_response(pdf, headers=pdfhttpheaders)