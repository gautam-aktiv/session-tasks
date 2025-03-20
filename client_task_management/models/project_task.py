from odoo import api, fields, models, _


class ProjectTask(models.Model):
    _inherit = "project.task"

    product_id = fields.Many2one('product.template')
    is_parent_task = fields.Boolean('Is Parent')
