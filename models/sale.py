# -*- coding: utf-8 -*-
###############################################################################
#    License, author and contributors information in:                         #
#    __manifest__.py file at the root folder of this module.                  #
###############################################################################

from odoo import models, fields, api, _
from odoo.exceptions import UserError
from odoo.addons import decimal_precision as dp
import logging

_logger = logging.getLogger(__name__)


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    discount2 = fields.Float(
        string='Discount 2 (%)',
        digits=dp.get_precision('Discount'),
        default=0.0
    )

    @api.depends('product_uom_qty', 'discount', 'discount2', 'price_unit',
                 'tax_id')
    def _compute_amount(self):
        for line in self:
            price = line.price_unit * (1 - (line.discount or 0.0) / 100.0)
            price2 = price * (1 - (line.discount2 or 0.0) / 100.0)
            taxes = line.tax_id.compute_all(
                price2, line.order_id.currency_id, line.product_uom_qty,
                product=line.product_id,
                partner=line.order_id.partner_shipping_id)
            line.update({
                'price_tax': sum(t.get('amount', 0.0) for t in taxes.get(
                    'taxes', [])),
                'price_total': taxes['total_included'],
                'price_subtotal': taxes['total_excluded'],
            })

    @api.depends('price_unit', 'discount', 'discount2')
    def _get_price_reduce(self):
        for line in self:
            price_reduce = line.price_unit * (1.0 - line.discount / 100.0)
            line.price_reduce = price_reduce * (1.0 - line.discount2 / 100.0)

    @api.multi
    def _prepare_invoice_line(self, qty):
        self.ensure_one()
        res = {}
        product = self.product_id.with_context(
            force_company=self.company_id.id)
        account = product.property_account_income_id or \
            product.categ_id.property_account_income_categ_id
        if not account and self.product_id:
            raise UserError(_('Please define income account for this '
                              'product: "%s" (id:%d) - or for its '
                              'category: "%s".') % (
                                self.product_id.name,
                                self.product_id.id,
                                self.product_id.categ_id.name))
        fpos = self.order_id.fiscal_position_id or \
            self.order_id.partner_id.property_account_position_id
        if fpos and account:
            account = fpos.map_account(account)
        res = {
            'name': self.name,
            'sequence': self.sequence,
            'origin': self.order_id.name,
            'account_id': account.id,
            'price_unit': self.price_unit,
            'quantity': qty,
            'discount': self.discount,
            'discount2': self.discount2,
            'uom_id': self.product_uom.id,
            'product_id': self.product_id.id or False,
            'invoice_line_tax_ids': [(6, 0, self.tax_id.ids)],
            'account_analytic_id': self.order_id.analytic_account_id.id,
            'analytic_tag_ids': [(6, 0, self.analytic_tag_ids.ids)],
            'display_type': self.display_type,
        }
        return res
