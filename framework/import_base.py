# -*- coding: utf-8 -*-
# ©2016 ICTSTUDIO <http://www.ictstudio.eu>
# License: AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

from csv_import import CSVImport

class ImportBase(object):

    def get_dict(self, odoo, line, ctx=None):
        return {}

    def write_or_create(self, odoo, line, dict, external_id):
        return 0

    def valid_line(self, odoo, line):
        return True

    def skip_line(self, odoo, line):
        return False

    def print_error(self, odoo, line, dict, count, external_id):
        return "No Message"

    def remove_empty_dict(self, dict):
        empty_keys = [k for k,v in dict.iteritems() if not v]
        for k in empty_keys:
            del dict[k]
        return dict

    def get_external_id(self, odoo, line, dict):
        return line['externalid']

    def import_file(self, odoo, file, ctx={}):
        if ctx.get('encoding'):
            encoding = ctx.get('encoding')
        else:
            encoding = 'utf-8'

        import_data = CSVImport(file, encoding=encoding)
        import_dict = import_data.dict_lines

        ## print_lines=None, limit=None, start_from=None, debug=None, dateformat=None
        count = 0
        fail_count = 0
        skip_count = 0
        invalid_count = 0
        old_line = {}

        for line in import_dict:
            line.update({'count': 1})

            if old_line and old_line.get('externalid') and not line.get('externalid'):
                work_line = old_line.copy()
                work_line.update(self.remove_empty_dict(line))
                work_line.update({'count': old_line.get('count') + 1})
            else:
                work_line = line.copy()

            if ctx.get('print_lines'):
                print "Line: %s, Failed Lines: %s, Skipped Lines: %s, Invalid Lines: %s" % (count, fail_count, skip_count, invalid_count)
            if ctx.get('start_from'):
                if ctx.get('start_from') > count:
                    count += 1
                    continue
            if ctx.get('limit'):
                if count >= ctx.get('limit'):
                    break
            if self.skip_line(odoo, work_line):
                # if debug:
                #     print "Skip   : %s" % line
                count += 1
                skip_count += 1
                continue

            # Check validity of line
            if not self.valid_line(odoo, work_line):
                if ctx.get('debug'):
                    print "Invalid  : %s" % work_line
                count += 1
                invalid_count += 1
                continue

            dict = self.get_dict(odoo, work_line, ctx=ctx)
            # if ctx.get('debug'):
            #     print "Incoming : %s" % work_line
            #     print "Mapped   : %s" % dict

            dict = self.remove_empty_dict(dict)
            dict = self.add_after_empty_dict(odoo, work_line, dict, ctx=ctx)
            # if ctx.get('debug'):
            #     print "Outgoing : %s" % dict

            return_id = 0
            external_id = self.get_external_id(odoo, work_line, dict)
            try:
                return_id = self.write_or_create(odoo, work_line, dict, external_id)

            except Exception, e:
                print e
                print dict
                try:
                    print self.print_error(odoo, work_line, dict, count, external_id).encode('utf-8')
                except e:
                    print ("Error importing line: %s with values: %s" % (count, dict)).encode('utf-8')
                count += 1
                fail_count += 1
                continue

            old_line = self.remove_before_old_line(work_line.copy())
            count += 1

            if return_id:
                self.action_after_create(odoo, work_line, return_id, ctx=ctx)
        return {'count': count, 'failed': fail_count, 'invalid': invalid_count, 'skip': skip_count}

    def remove_before_old_line(self, dict):
        return dict

    def add_after_empty_dict(self, odoo, line, dict, ctx=None):
        return dict

    def action_after_create(self, odoo, line, id, ctx=None):
        return True