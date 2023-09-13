# -*- coding: utf-8 -*-
##########################################################################
# Author : Webkul Software Pvt. Ltd. (<https://webkul.com/>;)
# Copyright(c): 2017-Present Webkul Software Pvt. Ltd.
# All Rights Reserved.
#
#
#
# This program is copyright property of the author mentioned above.
# You can`t redistribute it and/or modify it.
#
#
# You should have received a copy of the License along with this program.
# If not, see <https://store.webkul.com/license.html/>;
##########################################################################

# Python Module
import logging
_log = logging.getLogger(__name__)

# Odoo Module
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class AttachDoc(models.TransientModel):
    _name = "customer.document"
    _description = "Attached customer document image"
    add_docs_ids = fields.Many2many('ir.attachment', string="Document")
    description=fields.Text("Description")


    # -------------------------------------------------------------------------
    # BUSINESS METHODS
    # -------------------------------------------------------------------------
    def confirm_doc(self):
        """Confirm document wizard
        """
        active_booking_id = self.env['hotel.booking'].browse(
            self._context.get("active_ids"))
        active_booking_id.docs_ids=self.add_docs_ids
        active_booking_id.doc_description=self.description
        active_booking_id.status_bar="allot"
