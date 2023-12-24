# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.i18n import gettext
from trytond.model import fields
from trytond.model.exceptions import ValidationError
from trytond.pool import PoolMeta


class TaxTemplate(metaclass=PoolMeta):
    __name__ = 'account.tax.template'

    reverse_charge = fields.Boolean('Reverse Charge')

    def _get_tax_value(self, tax=None):
        res = super()._get_tax_value(tax=tax)
        if not tax or tax.reverse_charge != self.reverse_charge:
            res['reverse_charge'] = self.reverse_charge
        return res


class Tax(metaclass=PoolMeta):
    __name__ = 'account.tax'

    reverse_charge = fields.Boolean('Reverse Charge')

    @classmethod
    def validate(cls, taxes):
        super().validate(taxes)
        for tax in taxes:
            tax.check_reverse_charge()

    def check_reverse_charge(self):

        def get_top(tax):
            top = tax
            while top.parent:
                top = get_top(top.parent)
            return top

        top = get_top(self)
        taxes = self.search([
                ('reverse_charge', '!=', top.reverse_charge),
                ('parent', 'child_of', top.id)
                ])
        if taxes:
            different = ', '.join([t.rec_name for t in taxes
                if t.reverse_charge != top.reverse_charge])
            raise ValidationError(gettext(
                    'account_tax_reverse_charge.same_reverse_charge',
                    first=top.rec_name, second=different))
