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

    def skip_line(self, odoo, line):
        if not line['bankrekening']:
            return True
        return False

    def get_external_id(self, odoo, line, dict):
        return line['code'] + '_bank_1'

    def get_dict(self, odoo, line, ctx=None):

        return_dict = {
            'state': 'iban',
            'acc_number': line['bankrekening'],
            'partner_id': odoo.get_id_from_external_id('__import_res_partner__.' + line['code'], 'res.partner')
        }

        return return_dict


    def write_or_create(self, odoo, line, dict, external_id):
        return odoo.external_id_write_or_create('res.partner.bank', external_id, dict)

    def print_error(self, odoo, line, dict, count, external_id):
        return 'Partner \"%s\" can\'t be added' % line['bankrekening']
