# -*- coding: utf-8 -*-
# ©2016 ICTSTUDIO <http://www.ictstudio.eu>
# License: AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

from import_base import ImportBase
from vwn_import_tools import tools
import time

class Import(ImportBase, tools):

    def import_file(self, odoo, file, ctx=None):
        return super(Import, self).import_file(
                odoo, file, ctx=ctx
        )

    def get_external_id(self, odoo, line, dict):
        return line['boeking']

    def get_partner (self, odoo, line, ctx=None):
        partner_id = odoo.get_id_from_external_id('__import_res_partner__.' + line.get('code'), 'res.partner')

        if not partner_id:
            partner_ids = odoo.object_execute_search(
                    'res.partner',
                    [
                        ('ref','=', line.get('code'))
                    ]
            )
            if partner_ids:
                partner_id = partner_ids[0]
            else:
                partner_id = 1

        return partner_id

    def get_dict(self, odoo, line, ctx=None):

        partner_id = self.get_partner(odoo, line, ctx=ctx)

        if ctx.get('openstaand_type') == 'debiteur':
            account_id = odoo.object_execute_search(
                    'account.account',
                    [
                        ('code', '=', '1000')
                    ]
            )

            journal_id = odoo.object_execute_search(
                    'account.journal',
                    [
                        ('code','=', 'ODEB')
                    ]
            )

            if line.get('grootboekrekening'):
                spec_account_id = odoo.object_execute_search(
                        'account.account',
                        [
                            ('code', '=', line.get('grootboekrekening'))
                        ]
                )
                if spec_account_id:
                    account_id = spec_account_id

            if line.get('dagboek'):
                spec_journal_id = odoo.object_execute_search(
                        'account.journal',
                        [
                            ('code','=', line.get('dagboek'))
                        ]
                )
                if spec_journal_id:
                    journal_id = spec_journal_id

            return_dict = {
                'internal_number': line.get('boeking'),
                #'number': line.get('factuurnummer'),
                'type':  'out_invoice',
                'partner_id': odoo.get_id_from_external_id('__import_res_partner__.' + line.get('code'), 'res.partner') or 1,
                'journal_id': journal_id and journal_id[0] or 1,
                'account_id': account_id and account_id[0] or 1,
                'date_invoice': self.format_date(line.get('datum'), ctx=ctx),
                'date_due': self.format_date(line.get('vervaldatum'), ctx=ctx),
            }
        if ctx.get('openstaand_type') == 'crediteur':
            account_id = odoo.object_execute_search(
                    'account.account',
                    [
                        ('code', '=', '3400')
                    ]
            )
            journal_id = odoo.object_execute_search(
                    'account.journal',
                    [
                        ('code','=', 'OCRED')
                    ]
            )
            if line.get('grootboekrekening'):
                spec_account_id = odoo.object_execute_search(
                        'account.account',
                        [
                            ('code', '=', line.get('grootboekrekening'))
                        ]
                )
                if spec_account_id:
                    account_id = spec_account_id

            if line.get('dagboek'):
                spec_journal_id = odoo.object_execute_search(
                        'account.journal',
                        [
                            ('code','=', line.get('dagboek'))
                        ]
                )
                if spec_journal_id:
                    journal_id = spec_journal_id


            return_dict = {
                'internal_number': line.get('boeking'),
                'reference': line.get('factuur') or '',
                'type':  'in_invoice',
                'partner_id': partner_id,
                'journal_id': journal_id and journal_id[0] or 1,
                'account_id': account_id and account_id[0] or 1,
                'date_invoice': self.format_date(line.get('datum'), ctx=ctx),
                'date_due': self.format_date(line.get('vervaldatum'), ctx=ctx),
                'check_total': self.string_to_float(line.get('tebetalen'))
            }
        print return_dict
        if time.strptime(self.format_date(line.get('datum'), ctx=ctx), '%Y-%m-%d') < time.strptime('2016-01-01', '%Y-%m-%d'):
            # TODO: get period with name 01/2016
            period_id = odoo.object_execute_search(
                    'account.period',
                    [
                        ('name', '=', '01/2016')
                    ]
            )
            if period_id:
                return_dict.update({'period_id': period_id and period_id[0]})
        return return_dict


    def write_or_create(self, odoo, line, dict, external_id):
        return odoo.external_id_write_or_create('account.invoice', external_id, dict)

    def print_error(self, odoo, line, dict, count, external_id):
        return 'Account Invoice \"%s\" can\'t be added' % line.get('omschrijving')
