# -*- coding: utf-8 -*-
from odoo import api, fields, models


class Pricelist(models.Model):
    _inherit = "product.pricelist"

    customer_id = fields.Many2one('res.partner', 'Customer')
    start_from = fields.Date('From Date', required=True,
                             default=fields.Date.today())
    end_to = fields.Date('To Date')

    @api.model
    def _search(self, domain, offset=0, limit=None,
                order=None, access_rights_uid=None):
        if self._context.get('customer_id'):
            domain += [
                '|', ('customer_id', '=', self._context.get('customer_id')),
                ('customer_id', '=', False),

                ('start_from', '<=', self._context.get('order_date')),

                '|', ('end_to', '>=', self._context.get('order_date')),
                ('end_to', '=', False)
            ]
        return super()._search(domain, offset, limit, order, access_rights_uid)
