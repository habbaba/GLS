from odoo import models,fields



class AcceptExample(models.TransientModel):
    _name = 'accept.example'



    gls_stock_id = fields.Many2one('gls.stock')
    date = fields.Date(default = fields.Date.today())

    def get_date(self):
        self.ensure_one()
        record = self.env['gls.stock'].browse(self.gls_stock_id.id)
        record.write({
            'accept_date':self.date,
            'state':'taken'
        })