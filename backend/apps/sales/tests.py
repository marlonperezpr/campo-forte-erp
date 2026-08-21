from datetime import date
from decimal import Decimal

from django.core.exceptions import ValidationError
from django.test import TestCase

from apps.inventory.models import InventoryMovement
from apps.accounts.models.product import Product
from apps.sales.models.sale import Sale
from apps.sales.models.sale_item import SaleItem
from apps.sales.services.sale import confirm_sale


class SaleItemTests(TestCase):

    def setUp(self):
        self.product = Product.objects.create(
            name="Produto Teste",
            sale_price=Decimal("100.00"),
        )

        self.sale = Sale.objects.create(
            sale_date=date.today(),
        )

    def test_total_price_is_calculated_automatically(self):
        item = SaleItem.objects.create(
            sale=self.sale,
            product=self.product,
            quantity=Decimal("10.000"),
            unit_price=Decimal("50.00"),
        )

        self.assertEqual(
            item.total_price,
            Decimal("500.00"),
        )

    def test_quantity_cannot_be_negative(self):
        item = SaleItem(
            sale=self.sale,
            product=self.product,
            quantity=Decimal("-5.000"),
            unit_price=Decimal("50.00"),
        )

        with self.assertRaises(ValidationError):
            item.full_clean()

    def test_unit_price_cannot_be_negative(self):
        item = SaleItem(
            sale=self.sale,
            product=self.product,
            quantity=Decimal("10.000"),
            unit_price=Decimal("-50.00"),
        )

        with self.assertRaises(ValidationError):
            item.full_clean()


class SaleTests(TestCase):

    def setUp(self):
        self.product = Product.objects.create(
            name="Produto Teste",
            sale_price=Decimal("100.00"),
        )

        self.sale = Sale.objects.create(
            sale_date=date.today(),
        )

    def test_sale_starts_as_draft(self):
        self.assertEqual(
            self.sale.status,
            Sale.Status.DRAFT,
        )

    def test_sale_can_be_created_without_customer(self):
        self.assertIsNone(self.sale.customer)

    def test_recalculate_total(self):
        SaleItem.objects.create(
            sale=self.sale,
            product=self.product,
            quantity=Decimal("10.000"),
            unit_price=Decimal("50.00"),
        )

        self.sale.recalculate_total()
        self.sale.refresh_from_db()

        self.assertEqual(
            self.sale.total_amount,
            Decimal("500.00"),
        )

    def test_confirmed_sale_item_cannot_be_changed(self):
        item = SaleItem.objects.create(
            sale=self.sale,
            product=self.product,
            quantity=Decimal("20.000"),
            unit_price=Decimal("50.00"),
        )

        self.sale.status = Sale.Status.CONFIRMED
        self.sale.save()

        item.quantity = Decimal("50.000")

        with self.assertRaises(ValueError):
            item.save()

    def test_confirmed_sale_item_cannot_be_deleted(self):
        item = SaleItem.objects.create(
            sale=self.sale,
            product=self.product,
            quantity=Decimal("20.000"),
            unit_price=Decimal("50.00"),
        )

        self.sale.status = Sale.Status.CONFIRMED
        self.sale.save()

        with self.assertRaises(ValueError):
            item.delete()

    def test_confirm_sale(self):
        self.product.stock_quantity = Decimal("50.000")
        self.product.save()

        SaleItem.objects.create(
            sale=self.sale,
            product=self.product,
            quantity=Decimal("20.000"),
            unit_price=Decimal("50.00"),
        )

        confirm_sale(self.sale)

        self.sale.refresh_from_db()
        self.product.refresh_from_db()

        self.assertEqual(
            self.sale.status,
            Sale.Status.CONFIRMED,
        )

        self.assertEqual(
            self.sale.total_amount,
            Decimal("1000.00"),
        )

        self.assertEqual(
            self.product.stock_quantity,
            Decimal("30.000"),
        )

        self.assertTrue(
            InventoryMovement.objects.filter(
                product=self.product,
                source=InventoryMovement.Source.SALE,
                movement_type=InventoryMovement.MovementType.OUT,
                quantity=Decimal("20.000"),
            ).exists()
        )

    def test_cannot_confirm_sale_without_items(self):
        with self.assertRaises(ValueError):
            confirm_sale(self.sale)

    def test_cannot_confirm_sale_twice(self):
        self.product.stock_quantity = Decimal("50.000")
        self.product.save()

        SaleItem.objects.create(
            sale=self.sale,
            product=self.product,
            quantity=Decimal("10.000"),
            unit_price=Decimal("50.00"),
        )

        confirm_sale(self.sale)

        with self.assertRaises(ValueError):
            confirm_sale(self.sale)

    def test_cannot_confirm_sale_with_insufficient_stock(self):
        self.product.stock_quantity = Decimal("5.000")
        self.product.save()

        SaleItem.objects.create(
            sale=self.sale,
            product=self.product,
            quantity=Decimal("10.000"),
            unit_price=Decimal("50.00"),
        )

        with self.assertRaises(ValueError):
            confirm_sale(self.sale)

        self.product.refresh_from_db()

        self.assertEqual(
            self.product.stock_quantity,
            Decimal("5.000"),
        )

    def test_failed_sale_confirmation_does_not_create_inventory_movement(self):
        self.product.stock_quantity = Decimal("5.000")
        self.product.save()

        SaleItem.objects.create(
            sale=self.sale,
            product=self.product,
            quantity=Decimal("10.000"),
            unit_price=Decimal("50.00"),
        )

        with self.assertRaises(ValueError):
            confirm_sale(self.sale)

        self.assertFalse(
            InventoryMovement.objects.filter(
                product=self.product,
                source=InventoryMovement.Source.SALE,
            ).exists()
        )
