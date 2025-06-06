# -*- coding: utf-8 -*-
from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    sales_bulk_qty = fields.Float(string="Sales Bulk Qty")
    apply_bulk_disc = fields.Boolean(string="Apply Bulk Disc")
