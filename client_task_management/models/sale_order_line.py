# -*- coding: utf-8 -*-
from odoo import models
from odoo.tools import html2plaintext


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    def _create_parent_task(self, project):
        """
        Generate parent task for the given so line.
        :return: record of the created parent task
        """

        parent_task_values = self._timesheet_create_task_prepare_values(project)
        parent_task_values["is_parent_task"] = True
        parent_task_values["product_id"] = self.product_id.id
        parent_task = self.env["project.task"].sudo().create(parent_task_values)
        return parent_task

    def _timesheet_create_task(self, project):
        """
        Generates a task for the given Sales Order line(SOL) and links it to a project.

        If a parent task does not exist for the given product in the project,
        a new parent task is created.The generated task is then associated with
        the appropriate parent task and updated with necessary values.

        :return: The created project task.
        :rtype: recordset of `project.task`
        """

        if project:
            parent_task_id = project.task_ids.filtered(
                lambda pt: pt.product_id.id == self.product_id.id and pt.is_parent_task
            )
            if not parent_task_id:
                parent_task_id = self._create_parent_task(project)
                task_values = self._timesheet_create_task_prepare_values(project)
                task_values["product_id"] = self.product_id.id
                task_values["parent_id"] = parent_task_id.id
                task_values["name"] = (
                    html2plaintext(task_values["description"])
                    if task_values["description"]
                    else task_values["name"]
                )
                task = self.env["project.task"].sudo().create(task_values)
            else:
                values = self._timesheet_create_task_prepare_values(project)
                values["product_id"] = self.product_id.id
                values["parent_id"] = parent_task_id.id
                values["name"] = (
                    html2plaintext(values["description"])
                    if values["description"]
                    else values["name"]
                )
                task = self.env["project.task"].sudo().create(values)

        self.task_id = task
        # post message on task
        task_msg = self.env._(
            "This task has been created from: %(order_link)s (%(product_name)s)",
            order_link=self.order_id._get_html_link(),
            product_name=self.product_id.name,
        )
        task.message_post(body=task_msg)
        return task
