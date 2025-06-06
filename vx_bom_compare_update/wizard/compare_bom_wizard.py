# -*- encoding: utf-8 -*-

from odoo import _, api, fields, models


class CompareBom(models.TransientModel):
    _name = "compare.bom.wizard"
    _description = "Comare BOM Wizard"

    bom_a_id = fields.Many2one('mrp.bom', string='BOM A', required=True)
    bom_b_id = fields.Many2one('mrp.bom', string='BOM B', required=True)


    def action_compare(self):
        print("\n\n\n\nComparing BOMs:")