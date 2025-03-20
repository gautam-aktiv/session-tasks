# -*- coding: utf-8 -*-
from odoo import models
from odoo.tools import html2plaintext



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
        res['name'] = self.product_template_id.display_name if self.product_template_id else self.product_id.display_name

        return res


    def _timesheet_create_task(self, project):

        if project:
            project_task_ids = project.task_ids.filtered(lambda ptp: ptp.id == self.product_id.id)
            print("project_task_ids===>",project_task_ids)
            parent_task_id = project.task_ids.filtered(lambda pt: pt.is_parent_task)
            if not parent_task_id:
                main = parent_task_id.filtered(lambda ptp: ptp.id == self.product_id.id)
                print(main,".....main")
                parent_task_values = self._timesheet_create_task_prepare_values(project)
                parent_task_values['is_parent_task'] = True
                parent_task_values['product_id'] = self.product_id.id
                parent_task_id = self.env['project.task'].sudo().create(parent_task_values)

        res = super()._timesheet_create_task(project)
        res.parent_id = parent_task_id
        res.product_id = self.product_id.id
        res.name = html2plaintext(res.description)  if res.description else res.name

        return res
