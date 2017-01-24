# -*- coding: utf-8 -*-
# ©2016 ICTSTUDIO <http://www.ictstudio.eu>
# License: AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

import datetime
import time
import importlib

from gateway import LazyOpenErpServerProxy

class BaseImport(object):

    def main_import(self, settings):
        return {}

    def quick_import(self, settings, file, import_module, description='Geen', ctx=None):
        try:
            ImportModule = importlib.import_module(import_module)
        except ImportError:
            print "No %s module available" % import_module
            return {}
        odoo = LazyOpenErpServerProxy(
                'http://' + settings._host + ':' + settings._port,
                settings._database,
                settings._user,
                settings._password
        )
        print 'Start Import: %s: time: %s' % (description, datetime.datetime.now().time())
        start = time.time()

        return_values = ImportModule.Import().import_file(
                odoo,
                file,
                ctx=ctx
        )
        print '.. Import: %s: Done! %.3f sec. Lines: %s Failed: %s, Skipped: %s, Invalid: %s' % (
            description,
            time.time() - start,
            return_values.get('count'),
            return_values.get('failed'),
            return_values.get('skip'),
            return_values.get('invalid')
        )
        return return_values