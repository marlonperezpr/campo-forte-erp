from decimal import Decimal

from django.test import TestCase

from apps.accounts.models.product import Product
from apps.inventory.models import InventoryMovement
from apps.inventory.services.inventory import create_inventory_movement


class InventoryMovementTests(TestCase):

    def setUp(self):
        self.product = Product.objects.create(
            name="Produto Teste",
            sale_price=Decimal("100.00"),
        )

    def test_in_movement_increases_stock(self):
        movement = create_inventory_movement(
            product=self.product,
            movement_type=InventoryMovement.MovementType.IN,
            source=InventoryMovement.Source.PURCHASE,
            quantity=Decimal("10.000"),
        )

        self.product.refresh_from_db()

        self.assertEqual(
            self.product.stock_quantity,
            Decimal("10.000"),
        )

        self.assertEqual(
            movement.balance_after,
            Decimal("10.000"),
        )

    def test_out_movement_decreases_stock(self):
        self.product.stock_quantity = Decimal("20.000")
        self.product.save()

        movement = create_inventory_movement(
            product=self.product,
            movement_type=InventoryMovement.MovementType.OUT,
            source=InventoryMovement.Source.SALE,
            quantity=Decimal("5.000"),
        )

        self.product.refresh_from_db()

        self.assertEqual(
            self.product.stock_quantity,
            Decimal("15.000"),
        )

        self.assertEqual(
            movement.balance_after,
            Decimal("15.000"),
        )

    def test_stock_cannot_become_negative(self):
        self.product.stock_quantity = Decimal("5.000")
        self.product.save()

        with self.assertRaises(ValueError):
            create_inventory_movement(
                product=self.product,
                movement_type=InventoryMovement.MovementType.OUT,
                source=InventoryMovement.Source.SALE,
                quantity=Decimal("10.000"),
            )

    def test_purchase_cannot_create_out_movement(self):
        with self.assertRaises(ValueError):
            create_inventory_movement(
                product=self.product,
                movement_type=InventoryMovement.MovementType.OUT,
                source=InventoryMovement.Source.PURCHASE,
                quantity=Decimal("10.000"),
            )

    def test_sale_cannot_create_in_movement(self):
        with self.assertRaises(ValueError):
            create_inventory_movement(
                product=self.product,
                movement_type=InventoryMovement.MovementType.IN,
                source=InventoryMovement.Source.SALE,
                quantity=Decimal("10.000"),
            )

    def test_adjustment_can_increase_stock(self):
        self.product.stock_quantity = Decimal("20.000")
        self.product.save()

        movement = create_inventory_movement(
            product=self.product,
            movement_type=InventoryMovement.MovementType.ADJUSTMENT,
            source=InventoryMovement.Source.ADJUSTMENT,
            quantity=Decimal("5.000"),
            reason="Contagem física",
        )

        self.product.refresh_from_db()

        self.assertEqual(
            self.product.stock_quantity,
            Decimal("25.000"),
        )

        self.assertEqual(
            movement.balance_after,
            Decimal("25.000"),
        )

    def test_adjustment_can_decrease_stock(self):
        self.product.stock_quantity = Decimal("20.000")
        self.product.save()

        movement = create_inventory_movement(
            product=self.product,
            movement_type=InventoryMovement.MovementType.ADJUSTMENT,
            source=InventoryMovement.Source.ADJUSTMENT,
            quantity=Decimal("-5.000"),
            reason="Perda identificada no estoque",
        )

        self.product.refresh_from_db()

        self.assertEqual(
            self.product.stock_quantity,
            Decimal("15.000"),
        )

        self.assertEqual(
            movement.balance_after,
            Decimal("15.000"),
        )

    def test_quantity_cannot_be_zero(self):
        with self.assertRaises(ValueError):
            create_inventory_movement(
                product=self.product,
                movement_type=InventoryMovement.MovementType.IN,
                source=InventoryMovement.Source.PURCHASE,
                quantity=Decimal("0.000"),
            )
