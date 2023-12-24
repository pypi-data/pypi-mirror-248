# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.

from trytond.tests.test_tryton import ModuleTestCase


class AccountTaxReverseChargeTestCase(ModuleTestCase):
    "Test Account Tax Reverse Charge module"
    module = 'account_tax_reverse_charge'


del ModuleTestCase
