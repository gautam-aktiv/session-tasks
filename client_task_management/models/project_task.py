# -*- coding: utf-8 -*-
from odoo import fields, models


class ProjectTask(models.Model):
    _inherit = "project.task"

    # product_id is used to task product with SOL
    product_id = fields.Many2one("product.template")
    # is_parent_task : to indicate if the task is a parent task
    is_parent_task = fields.Boolean("Is Parent")
