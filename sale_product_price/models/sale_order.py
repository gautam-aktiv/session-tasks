# -*- coding: utf-8 -*-
from odoo import api, fields, models


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    pricelist_message = fields.Text()

    @api.onchange('partner_id')
    def _onchange_partner_id(self):
        self.pricelist_id = False
        pricelist = self.env['product.pricelist'].search([
            ('start_from', '<=', self.date_order),
            '|', ('end_to', '>=', self.date_order),
            ('end_to', '=', False)
        ])
        if self.partner_id:
            partner_pricelist = pricelist.filtered(
                lambda p: p.customer_id == self.partner_id
            )
            if partner_pricelist:
                self.pricelist_id = partner_pricelist[0]
            else:
                self.pricelist_id = pricelist[0]
        else:
            self.pricelist_id = pricelist[0]
        self._recompute_prices()

    def action_update_prices(self):
        super().action_update_prices()
        self.message_post(body=self.pricelist_message)

    @api.onchange('pricelist_id')
    def _onchange_pricelist_id(self):

        self.pricelist_message = (f"you have change price list from"
                                  f" {self._origin.pricelist_id.name}"
                                  f" to {self.pricelist_id.name}.")
