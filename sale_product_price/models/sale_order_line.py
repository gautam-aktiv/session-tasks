# -*- coding: utf-8 -*-
from odoo import api, fields, models


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    pricelist_id = fields.Many2one('product.pricelist', 'Pricelist')

    @api.depends('product_id', 'product_uom',
                 'product_uom_qty', 'pricelist_id')
    def _compute_price_unit(self):

        super()._compute_price_unit()

        pricelists = self.env['product.pricelist'].with_context({
            'customer_id': self.order_id.partner_id.id,
            'order_date': self.order_id.date_order
        }).search([
            ('item_ids.product_tmpl_id', '=', self.product_template_id.id),
        ])

        lowest_price = float('inf')
        lowest_pricelist_id = False
        for pricelist in pricelists:
            price = pricelist._get_product_price(
                self.product_id,
                quantity=self.product_uom_qty,
                partner=self.order_id.partner_id
            )
            if price < lowest_price:
                lowest_price = price
                lowest_pricelist_id = pricelist.id

        if lowest_pricelist_id:
            self.pricelist_id = lowest_pricelist_id
        else:
            self.pricelist_id = self.order_id.pricelist_id.id

    @api.onchange('pricelist_id', 'product_id', 'product_uom_qty')
    def _onchange_pricelist_id(self):
        """Update price based on the selected pricelist."""
        if self.pricelist_id and self.product_id:
            new_price_unit = self.pricelist_id._get_product_price(
                self.product_id,
                quantity=self.product_uom_qty,
                partner=self.order_id.partner_id
            )
            self.price_unit = new_price_unit
