# -*- coding: utf-8 -*-
# ©2016 ICTSTUDIO <http://www.ictstudio.eu>
# License: AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

from import_base import ImportBase
from import_tools import tools

class Import(ImportBase, tools):

    def import_file(self, odoo, file, ctx=None):
        return super(Import, self).import_file(
                odoo, file, ctx=ctx
        )

    def get_external_id(self, odoo, line, dict):
        return line['code']

    def get_dict(self, odoo, line, ctx=None):
        country_id = odoo.object_execute_search('res.country', [('name', '=', line.get('land'))])
        if not country_id:
            country_id = odoo.get_id_from_external_id("base.nl", "res.country")

        if isinstance(country_id, list):
            country_id = country_id[0]

        return_dict = {
            'lang': 'nl_NL',
            'name': line.get('naam'),
            'ref': line.get('code'),
            'active': True,
            'customer': self.odoo_boolean(line.get('klant')),
            'supplier': self.odoo_boolean(line.get('leverancier')),
            'street': line.get('adres'),
            'zip': line.get('postcode'),
            'city': line.get('plaats'),
            'phone': line.get('telefoon'),
            'email': line.get('e-mail'),
            'is_company': True,
            'comment': line.get('opmerkingen'),
            'country_id': country_id
        }
        if line.get("classification1"):
            category_id = odoo.get_or_create(
                    'res.partner.category',
                    [
                        ('name', '=', line.get('classification1'))
                    ]
            )
            if category_id:
                return_dict["category_id"] = [(6, 0, [category_id])]

        if line.get('grootboekrekening'):
            account_id = odoo.object_execute_search(
                    'account.account',
                    [
                        ('code','=', line.get('grootboekrekening'))
                    ]
            )

            if return_dict.get('customer') and account_id:
                return_dict.update({
                    'property_account_receivable': account_id and account_id[0]
                })

        if line.get('grootboekrekening'):
            account_id = odoo.object_execute_search(
                    'account.account',
                    [
                        ('code','=', line.get('grootboekrekening'))
                    ]
            )

            if return_dict.get('supplier') and account_id:
                return_dict.update({
                    'property_account_payable': account_id and account_id[0]
                })

        if line.get('betalingsconditie'):
            payment_term_id = odoo.object_execute_search(
                    'account.payment.term',
                    [
                        ('name', '=', line.get('betalingsconditie'))
                    ]
            )
            if return_dict.get('customer') and payment_term_id:
                return_dict.update({
                    'property_payment_term': payment_term_id and payment_term_id[0]
                })
            if return_dict.get('supplier') and payment_term_id:
                return_dict.update({
                    'property_supplier_payment_term': payment_term_id and payment_term_id[0]
                })

        return return_dict


    def write_or_create(self, odoo, line, dict, external_id):
        return odoo.external_id_write_or_create('res.partner', external_id, dict)

    def print_error(self, odoo, line, dict, count, external_id):
        return 'Error(%s): Partner \"%s\" can\'t be added' % (count, line['naam'])

    def add_after_empty_dict(self, odoo, line, dict, ctx=None):
        if not dict.get('customer'):
            dict.update({
                'customer': self.odoo_boolean(line.get('klant'))
            })
        if not dict.get('supplier'):
            dict.update({
                'supplier': self.odoo_boolean(line.get('leverancier'))
            })
        return dict