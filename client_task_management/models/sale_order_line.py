# -*- coding: utf-8 -*-
from odoo import models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    def _timesheet_create_task_prepare_values(self, project):
        """
        This method is triggered when a sales order is confirmed. It checks whether a
        product description exists and sets the task's name accordingly:
        - If `description` is available, it is used as the task `name`.
        - If `description` is not available, it falls back to the original `name`.
        - The `description` field is set to the original `name` to ensure
                            task details are preserved.
        """
        res = super()._timesheet_create_task_prepare_values(project)
        res['name'] = res.get('description') or res.get('name', '')
        res['description'] = res.get('name', '')

        return res
