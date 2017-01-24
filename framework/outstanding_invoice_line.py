# -*- coding: utf-8 -*-
# ©2016 ICTSTUDIO <http://www.ictstudio.eu>
# License: AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

from import_base import ImportBase
from vwn_import_tools import tools

class Import(ImportBase, tools):

    def import_file(self, odoo, file, ctx=None):
        return super(Import, self).import_file(
                odoo, file, ctx=ctx
        )

    def get_external_id(self, odoo, line, dict):
        return line['boeking'] + '_1'

    def get_dict(self, odoo, line, ctx=None):

        account_id = odoo.object_execute_search(
                'account.account',
                [
                    ('code', '=', '1230')
                ]
        )
        if ctx.get('openstaand_type') == 'crediteur':
            if line.get('tegenrekening') or ctx.get('tegenrekening_cred'):
                account_id = odoo.object_execute_search(
                        'account.account',
                        [
                            ('code', '=', line.get('tegenrekening') or ctx.get('tegenrekening_cred'))
                        ]
                )


        if ctx.get('openstaand_type') == 'debiteur':
            if line.get('tegenrekening') or ctx.get('tegenrekening_deb'):
                account_id = odoo.object_execute_search(
                        'account.account',
                        [
                            ('code', '=', line.get('tegenrekening') or ctx.get('tegenrekening_deb'))
                        ]
                )

        if not account_id:
            account_id =1

        #TODO: Check if value is postive or negative
        return_dict = {
            'invoice_id': odoo.get_id_from_external_id('__import_account_invoice__.' + line.get('boeking'), 'account.invoice'),
            'account_id': account_id and account_id[0] or 1,
            'name': line.get('omschrijving') or 'openstaande post',
            'quantity': 1,
            'price_unit': self.string_to_float(line.get('tevorderen') or line.get('tebetalen')),
            'price_subtotal': self.string_to_float(line.get('tevorderen') or line.get('tebetalen'))
        }

        print return_dict

        return return_dict


    def write_or_create(self, odoo, line, dict, external_id):
        return odoo.external_id_write_or_create('account.invoice.line', external_id, dict)

    def print_error(self, odoo, line, dict, count, external_id):
        return 'Account Invoice Line \"%s\" can\'t be added' % line['omschrijving']

    def action_after_create(self, odoo, line, id, ctx=None):
        try:
            invoice_id = odoo.get_id_from_external_id('__import_account_invoice__.' + line.get('boeking'), 'account.invoice')
            new_args = ('account.invoice', 'invoice_open', invoice_id)
            odoo.object_workflow(*new_args)
        except:
            print 'Error'

        return True