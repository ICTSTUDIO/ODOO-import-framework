# -*- coding: utf-8 -*-
# ©2016 ICTSTUDIO <http://www.ictstudio.eu>
# License: AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

import datetime
import time

from base_import import BaseImport


class BaseImport(BaseImport):

    def main_import(self, settings, ctx={}):
        global_start = time.time()
        print 'Starting time: %s' % (datetime.datetime.now().time())

        if not ctx.get('prefix') and settings._prefix:
            ctx['prefix'] = settings._prefix
        elif not ctx.get('prefix'):
            ctx['prefix'] = 'PREF'

        if settings._import_list.get('creddeb'):
            # Import Partners
            self.quick_import(
                    settings,
                    settings._import_list.get('creddeb'),
                    'res_partner',
                    'Partners',
                    ctx=ctx
            )

            # Import Partners Contacts
            self.quick_import(
                    settings,
                    settings._import_list.get('creddeb'),
                    'res_partner_contact',
                    'Partner Contacts',
                    ctx=ctx
            )

            # Import Partner Banks
            self.quick_import(
                    settings,
                    settings._import_list.get('creddeb'),
                    'res_partner_bank',
                    'Partner Banks',
                    ctx=ctx
            )

        if settings._import_list.get('opendeb'):
            if ctx.get('dateformat'):
                ctx.update({'openstaand_type': 'debiteur'})
            else:
                ctx.update({'dateformat': 'dmy',
                            'openstaand_type': 'debiteur'})

            # Import Openstaande Debiteuren
            self.quick_import(
                    settings,
                    settings._import_list.get('opendeb'),
                    'outstanding_invoice',
                    'Openstaande Debiteuren',
                    ctx=ctx
            )

            # Import Openstaande Debiteuren regels
            self.quick_import(
                    settings,
                    settings._import_list.get('opendeb'),
                    'outstanding_invoice_line',
                    'Openstaande Debiteuren Regels',
                    ctx=ctx
            )

        if settings._import_list.get('opencred'):
            if ctx.get('dateformat'):
                ctx.update({'openstaand_type': 'crediteur'})
            else:
                ctx.update({'dateformat': 'dmy',
                            'openstaand_type': 'crediteur'})

            # Import Openstaande Debiteuren
            self.quick_import(
                    settings,
                    settings._import_list.get('opencred'),
                    'outstanding_invoice',
                    'Openstaande Crediteuren',
                    ctx=ctx
            )

            # Import Openstaande Debiteuren regels
            self.quick_import(
                    settings,
                    settings._import_list.get('opencred'),
                    'outstanding_invoice_line',
                    'Openstaande Crediteuren Regels',
                    ctx=ctx
            )


        print 'Total import: %f sec.' % (time.time() - global_start)
        print 'Import completed on %s' % (datetime.datetime.now().time())
        return {}
