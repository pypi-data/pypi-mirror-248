# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.

from trytond.tests.test_tryton import ModuleTestCase


class ProductVariantTestCase(ModuleTestCase):
    "Test Product Variant module"
    module = 'product_variant'


del ModuleTestCase
