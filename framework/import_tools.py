# -*- coding: utf-8 -*-
# ©2016 ICTSTUDIO <http://www.ictstudio.eu>
# License: AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

class tools:

    def odoo_boolean(self, value):
        if value in ('TRUE', 'True', 'true', 'WAAR', 'Waar', 'waar', 'V', 'v', 'j', 'J', 'ja', 'Ja'):
            return True
        else:
            return False

    def odoo_gender(self, value):
        if value in ('Man', 'man', 'Male', 'male'):
            return 'male'
        elif value in ('Vrouw', 'vrouw', 'Female', 'female'):
            return 'female'
        else:
            return 'unknown'

    def commaTodot(self, f):
        s = str(f)
        comma = s.find(',')
        dot = s.find('.')
        if (comma > -1):
            if (dot < 0):
                s = s.replace(',', '.')
            else:
                if (comma > dot):
                    s = s[:comma].replace('.', '')+','+s[(comma+1):]
                else:
                    s = s.replace(',', '')
        return (s)

    def string_to_float(self, string_float):
        string_float = self.commaTodot(string_float)
        if string_float != '0':
            return string_float
        else:
            return '0.0'

    def floattoint(self, string_float):
        return string_float.split(',')[0]

    def get_product_tmpl_id_from_product_code(self, odoo, product_external_id):
        product_id = odoo.get_id_from_external_id(product_external_id, 'product.product')
        if product_id:
            product_id_read = odoo.object_execute_read_many('product.product', [product_id], ['product_tmpl_id'])
            return (product_id_read and product_id_read[0]['product_tmpl_id'][0]) or False
        else:
            return False

    def get_product_type(self, type):
        if type == 'stockable':
            type = 'product'
        elif type not in ('consu', 'service'):
            type = 'product'
        return type

    def get_tax_from_foreign_id(self, odoo, foreign_id, type_tax):
        if foreign_id == '1':  # TODO: BTW Hoog
            tax_id = odoo.object_execute_search('account.tax', [
                ('type_tax_use', '=', type_tax),
                ('amount', '=', 0.21),
                ('description', 'in', ['21% BTW','NL-21% BTW'])
            ])
        elif foreign_id == '2':  # TODO: BTW Laag
            tax_id = odoo.object_execute_search('account.tax', [
                ('type_tax_use', '=', type_tax),
                ('amount','=', 0.06),
                ('description', 'in', ['6% BTW', 'NL-6% BTW'])
            ])
        else:
            tax_id = False

        return tax_id

    def get_uom_id_from_product_code(self, odoo, product_id):
        product_read = odoo.object_execute_read_many('product.product', [product_id], ['uom_id'])
        if product_read:
            return product_read[0]['uom_id'][0]
        return False

    def get_product_name_from_product_code(self, odoo, product_id):
        product_read = odoo.object_execute_read_many('product.product', [product_id], ['name'])
        if product_read:
            return product_read[0]['name']
        return False

    def get_logic(self, reorderingmode):
        #if reorderingmode in ('max', 'MAX', 'Order to Max', 'order to max'):
        return 'max'
        #else:
        #    return 'price'

    def get_mrp_bom_type(self, type):
        if type in ('Phantom','phantom','Set','set'):
            type = 'phantom'
        else:
            type = 'normal'
        return type

    def parse_credit_limit(self, creditlimit):
        if creditlimit[1:] == "-":
            return '0'
        elif creditlimit:
            return creditlimit.split(",")[0]
        else:
            return '0'
