# -*- coding: utf-8 -*-
# from odoo import http


# class Glsgroup(http.Controller):
#     @http.route('/glsgroup/glsgroup', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/glsgroup/glsgroup/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('glsgroup.listing', {
#             'root': '/glsgroup/glsgroup',
#             'objects': http.request.env['glsgroup.glsgroup'].search([]),
#         })

#     @http.route('/glsgroup/glsgroup/objects/<model("glsgroup.glsgroup"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('glsgroup.object', {
#             'object': obj
#         })
