# -*- coding: utf-8 -*-
# Copyright 2019-TODAY Daniel Lago Suarez <dls@anuia.es>
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Multi Discount on Sale and Purchase',
    'summary': 'Shows a second level of sale/purchase discount reflected in '
               'accounting',
    'description': """Description in HTML file.
- descuento
- ventas
- compras
- descuento en pedido
- descuento en factura
- segundo
- segundo descuento
- multiple
- multiple descuento
- invoice
- sale
- purchase
- level
- second level
- level discount
- sale discount
- invoice discount
- discount
- discount in order
- discount on order
- discount in sale
- discount on sale
- discount in sale order
- discount on sale order
- discount in purchase
- discount on purchase
- discount in purchase order
- discount on purchase order
- discount in invoice
- discount on invoice
- second
- second discount
- multiple
- multiple discount
- multi
- multi discount
- several discounts
- remise
- remises multiples
- korting
- rabatt
- dos
- dos descuentos
- two
- two discounts
- two levels
- two levels discount
""",
    'category': 'Accounting',
    'version': '12.0.0.1',
    'license': 'AGPL-3',
    'author': 'Anubía Soluciones en la Nube, S.L.',
    'maintainer': 'Anubía Soluciones en la Nube, S.L.',
    'contributors': [
        'Daniel Lago Suarez <dls@anubia.es>',
    ],
    'website': 'http://www.anubia.es',
    'depends': [
        'sale',
        'account',
        'purchase_discount',
    ],
    'data': [
        'report/account.xml',
        'report/purchase.xml',
        'report/sale.xml',
        'views/account.xml',
        'views/purchase.xml',
        'views/sale.xml',
    ],
    'demo': [],
    'test': [],
    'images': [
        'static/description/main_screenshot.png',
        'static/description/main_1.png',
        'static/description/main_2.png',
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
    'price': 0,
    'currency': 'EUR',
}
