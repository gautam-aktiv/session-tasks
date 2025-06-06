# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    @api.depends("product_id", "product_uom", "product_uom_qty")
    def _compute_discount(self):
        discount_enabled = self.env[
            "product.pricelist.item"
        ]._is_discount_feature_enabled()
        for line in self:
            if not line.product_id or line.display_type:
                line.discount = 0.0

            if not (line.order_id.pricelist_id and discount_enabled):
                continue

            line.discount = 0.0

            if not line.pricelist_item_id._show_discount():
                # No pricelist rule was found for the product
                # therefore, the pricelist didn't apply any discount/change
                # to the existing sales price.
                continue

            line = line.with_company(line.company_id)
            pricelist_price = line._get_pricelist_price()
            base_price = line._get_pricelist_price_before_discount()

            product_template = line.product_id.product_tmpl_id
            if (
                product_template.apply_bulk_disc
                and line.product_uom_qty >= product_template.sales_bulk_qty
            ):
                pricelist_item = self.env["product.pricelist.item"].search(
                    [
                        ("pricelist_id", "=", line.order_id.pricelist_id.id),
                        "|",
                        ("product_tmpl_id", "=", product_template.id),
                        ("categ_id", "=", product_template.categ_id.id),
                    ],
                    limit=1,
                )
                if pricelist_item and pricelist_item.sales_bulk_disc:
                    line.discount = pricelist_item.sales_bulk_disc
                    continue

            if base_price != 0:  # Avoid division by zero
                discount = (base_price - pricelist_price) / base_price * 100
                if (discount > 0 and base_price > 0) or (
                    discount < 0 and base_price < 0
                ):
                    # only show negative discounts if price is negative
                    # otherwise it's a surcharge which shouldn't be shown to the customer
                    line.discount = discount
