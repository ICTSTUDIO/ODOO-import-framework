# -*- coding: utf-8 -*-
# ©2016 ICTSTUDIO <http://www.ictstudio.eu>
# License: AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

import sample_import_settings as settings
from framework.main_import import BaseImport as sample_import

ctx = {
    'debug': True,
    'dateformat': 'dmy',
}

sample_import().main_import(settings, ctx)