# -*- coding: utf-8 -*-
from odoo import fields, models


class ProductPricelistItem(models.Model):
    _inherit = "product.pricelist.item"

    sales_bulk_disc = fields.Float(string="Sales Bulk Disc")
