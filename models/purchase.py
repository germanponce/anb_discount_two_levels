# -*- coding: utf-8 -*-
###############################################################################
#    License, author and contributors information in:                         #
#    __manifest__.py file at the root folder of this module.                  #
###############################################################################

from odoo import models, fields, api
from odoo.addons import decimal_precision as dp
import logging

_logger = logging.getLogger(__name__)


class PurchaseOrderLine(models.Model):
    _inherit = "purchase.order.line"

    discount2 = fields.Float(
        string='Discount 2 (%)',
        digits=dp.get_precision('Discount'),
        default=0.0
    )

    @api.depends('discount', 'discount2')
    def _compute_amount(self):
        return super()._compute_amount()

    def _prepare_compute_all_values(self):
        vals = super()._prepare_compute_all_values()
        vals.update({'price_unit': self._get_discounted_price_unit()})
        return vals

    def _get_discounted_price_unit(self):
        self.ensure_one()
        if self.discount or self.discount2:
            discount = self.price_unit * (1 - self.discount / 100)
            discount2 = discount * (1 - self.discount2 / 100)
            return discount2
        return self.price_unit

    @api.multi
    def _get_stock_move_price_unit(self):
        for record in self:
            price_unit = False
            price = record._get_discounted_price_unit()
            if price != record.price_unit:
                price_unit = record.price_unit
                self.price_unit = price
        price = super(PurchaseOrderLine, self)._get_stock_move_price_unit()
        for record in self:
            if price_unit:
                record.price_unit = price_unit
        return price
