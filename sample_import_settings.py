# -*- coding: utf-8 -*-
# ©2016 ICTSTUDIO <http://www.ictstudio.eu>
# License: AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

# De database die gevuld gaat worden met gegevens.
# Deze database moet bestaan voordat er iets kan worden geimporteerd.
_database = "odoo"

# De taal die wordt gebruikt voor dit verkoopkantoor.
# Dit heeft ook invloed op de vertalingen van producten die in de database komen.
_language = "nl_NL"

# Het server adres waar de database zich op bevind.
_host = "127.0.0.1"

# De poort waarop de openerpserver luistert.
# Deze veranderd niet
_port = "8069"

#Credentials
_user = "admin"
_password = "admin"

_folder = ""

_import_list = {
    'creddeb': _folder + '/deb-cred.csv',
    'opendeb': _folder + '/openstaand-debiteuren.csv',
    'opencred': _folder + '/openstaand-crediteuren.csv',
}

_prefix = "SAMPLE"