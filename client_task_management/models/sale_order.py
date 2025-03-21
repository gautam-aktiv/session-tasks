# -*- coding: utf-8 -*-
from odoo import models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def _action_confirm(self):
        """
        On SO confirmation, this method checks whether an existing
        project is linked to the selected customer (`partner_id`):
        - If a project already exists, it assigns the project to the sales order.
        - If no project exists, it creates a new one using the customer's name
          and assigns it to the sales order.
        """

        projectobj = self.env["project.project"]
        project_id = projectobj.search(
            [("partner_id", "=", self.partner_id.id)], limit=1
        )
        self.project_id = project_id
        if project_id:
            self.project_id = project_id
        else:
            project_detaild = {
                "name": self.partner_id.display_name,
                "partner_id": self.partner_id.id,
            }
            self.project_id = projectobj.create(project_detaild)
        res = super()._action_confirm()

        return res

    def _tasks_ids_domain(self):
        """
        Extends the domain filter for tasks to include only parent tasks.
        """
        res = super()._tasks_ids_domain()
        res.append(("is_parent_task", "=", True))

        return res
