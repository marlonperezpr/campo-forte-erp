from decimal import Decimal

from django.core.exceptions import ValidationError
from django.test import TestCase

from apps.accounts.models.product import Product
from apps.accounts.models.supplier import Supplier
from apps.purchases.models.purchase import Purchase
from apps.purchases.models.purchase_item import PurchaseItem


class PurchaseItemTests(TestCase):
    def test_quantity_cannot_be_negative(self):
        item = PurchaseItem(
            purchase=self.purchase,
            product=self.product,
            quantity=Decimal("-5.000"),
            unit_cost=Decimal("50.00"),
        )

        with self.assertRaises(ValidationError):
            item.full_clean()

    def test_unit_cost_cannot_be_negative(self):
        item = PurchaseItem(
            purchase=self.purchase,
            product=self.product,
            quantity=Decimal("10.000"),
            unit_cost=Decimal("-50.00"),
        )

        with self.assertRaises(ValidationError):
            item.full_clean()
