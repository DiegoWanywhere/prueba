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
from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    """Module to snippet rooms

    Parameters
    ----------
    models : importing Model
    """
    _inherit = 'res.config.settings'

    # -------------------------------------------------------------------------//
    #  TRANSIENT MODEL FIELDS
    # -------------------------------------------------------------------------//

    website_homepage_product_ids = fields.Many2many('product.template',related="website_id.website_homepage_product_ids",readonly=False)
