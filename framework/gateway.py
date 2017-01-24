# -*- coding: utf-8 -*-
# ©2016 ICTSTUDIO <http://www.ictstudio.eu>
# License: AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

import pytz, time, traceback, xmlrpclib

def echo_error(func):
    def f(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception, e:
            traceback.print_exc()
            raise
    return f


class OpenErpServerProxy(object):
    def __init__(self, url):
        self._url = url
        self._proxies = {}

    def __getattr__(self, name):
        if name not in self._proxies:
            self._proxies[name] = xmlrpclib.ServerProxy('%s/xmlrpc/%s' % (self._url, name), use_datetime=True)
        return self._proxies[name]



class LazyOpenErpServerProxy(OpenErpServerProxy):
    def __init__(self, url, database, username, password):
        super(LazyOpenErpServerProxy, self).__init__(url)
        self._database = database
        self._username = username
        self._userid = None
        self._password = password
        self._info_dict = {'lang': 'nl_NL', 'contact_display': 'partner'} #'tz': unused, 'active_id(s)': open menus


    def _authenticate(self):
        if self._userid is None:
            self._userid = OpenErpServerProxy.__getattr__(self, 'common').login(self._database, self._username, self._password)

    def object_execute(self, *args):
        self._authenticate()
        new_args = (self._database, self._userid, self._password) + args + (self._info_dict,)
        return self.object.execute(*new_args)

    def object_workflow(self, *args):
        self._authenticate()
        new_args = (self._database, self._userid, self._password) + args
        return self.object.exec_workflow(*new_args)

    def object_execute_method(self, model, method, ids):
        new_args = (model, method, ids)
        return self.object_execute(*new_args)

    def object_execute_read(self, model, id, fields):
        return self.object_execute_read_many(model, (id,), fields)[0]

    def object_execute_read_many(self, model, ids, fields):
        new_args = (model, 'read', ids, fields)
        return self.object_execute(*new_args)

    def object_execute_search(self, model, query):
        new_args = (model, 'search', query, 0.0, 80.0, 0) # 0.0-80.0 = pagination, 0 = unknown
        return self.object_execute(*new_args)

    def object_execute_write(self, model, id, dict):
        return self.object_execute_write_many(model, (id,), dict)

    def object_execute_write_many(self, model, ids, dict):
        new_args = (model, 'write', ids, dict)
        return self.object_execute(*new_args)

    def object_execute_unlink(self, model, id):
        return self.object_execute_unlink_many(model, (id,))

    def object_execute_unlink_many(self, model, ids):
        new_args = (model, 'unlink', ids)
        return self.object_execute(*new_args)

    def object_execute_create(self, model, dict):
        new_args = (model, 'create', dict)
        return self.object_execute(*new_args)

    def wizard_create(self, *args):
        self._authenticate()
        new_args = (self._database, self._userid, self._password) + args + (self._info_dict,)
        return self.wizard.create(*new_args)

    def wizard_execute(self, *args):
        self._authenticate()
        new_args = (self._database, self._userid, self._password) + args + (self._info_dict,)
        return self.wizard.execute(*new_args)

    def get_or_create(self, model, search, defaults=None):
        model_id = self.object_execute_search(model, search)
        if not model_id:
            if not defaults:
                defaults = {}
            for s in search:
                defaults[s[0]] = s[2]
            return self.object_execute_create(model, defaults)
        else:
            return model_id[0]

    def external_id_write_or_create(self, model, external_id, values, defaults=None):
        model_id = self.get_id_from_external_id(external_id, model)
        if not model_id:
            if not defaults:
                defaults = {}
            model_id = self.object_execute_create(model, values)
            if model_id:
                self.create_external_id(model, model_id, external_id)
            return model_id
        else:
            self.object_execute_write(model, model_id, values)
            return model_id


    def model_to_import_name(self, model):
        return "__import_" + model.replace(".", "_") + "__"

    def create_external_id(self, model, res_id, external_id):
        if len(external_id.split('.')) == 2:
            module, name = external_id.split('.', 1)
        else:
            module = self.model_to_import_name(model)
            name = external_id

        dict = {
            'name': name,
            'model': model,
            'res_id': res_id,
            'module': module
        }

        try:
            self.object_execute_create('ir.model.data', dict)
            return True
        except Exception, e:
            print "External Reference for %s(%s) can\'t be added" % (model, res_id)
            return False

    def get_id_from_external_id(self, external_id, model=None):
        if len(external_id.split('.')) == 2:
            module, name = external_id.split('.', 1)
        else:
            if model:
                module = self.model_to_import_name(model)
            else:
                module = "__import__"
            name = external_id

        if model:
            model_data_ids = self.object_execute_search(
                    'ir.model.data',
                    [
                        ('module', '=', module),
                        ('name', '=', name),
                        ('model', '=', model)
                    ]
            )
        else:
            model_data_ids = self.object_execute_search(
                    'ir.model.data',
                    [
                        ('module', '=', module),
                        ('name', '=', name)
                    ]
            )

        res_id = self.object_execute_read_many('ir.model.data', model_data_ids, ['res_id'])
        return (res_id and res_id[0]['res_id']) or []
