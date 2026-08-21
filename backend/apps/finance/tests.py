from decimal import Decimal

from django.test import TestCase

from apps.finance.models.cash_movement import CashMovement
from apps.finance.models.cash_register import CashRegister
from apps.finance.services.cash import create_cash_movement, get_cash_balance


class CashRegisterTests(TestCase):

    def test_cash_register_starts_open(self):
        cash_register = CashRegister.objects.create()

        self.assertEqual(
            cash_register.status,
            CashRegister.Status.OPEN,
        )

    def test_cash_register_starts_with_zero_balance(self):
        cash_register = CashRegister.objects.create()

        self.assertEqual(
            cash_register.opening_balance,
            Decimal("0.00"),
        )

    def test_cash_register_can_have_opening_balance(self):
        cash_register = CashRegister.objects.create(
            opening_balance=Decimal("500.00"),
        )

        self.assertEqual(
            cash_register.opening_balance,
            Decimal("500.00"),
        )

    def test_cash_register_can_be_closed(self):
        cash_register = CashRegister.objects.create(
            opening_balance=Decimal("500.00"),
        )

        cash_register.status = CashRegister.Status.CLOSED
        cash_register.closing_balance = Decimal("750.00")
        cash_register.save()

        cash_register.refresh_from_db()

        self.assertEqual(
            cash_register.status,
            CashRegister.Status.CLOSED,
        )

        self.assertEqual(
            cash_register.closing_balance,
            Decimal("750.00"),
        )


class CashMovementTests(TestCase):

    def setUp(self):
        self.cash_register = CashRegister.objects.create(
            opening_balance=Decimal("500.00"),
        )

    def test_cash_movement_can_be_created_as_in(self):
        movement = CashMovement.objects.create(
            cash_register=self.cash_register,
            movement_type=CashMovement.MovementType.IN,
            source=CashMovement.Source.SALE,
            amount=Decimal("100.00"),
        )

        self.assertEqual(
            movement.movement_type,
            CashMovement.MovementType.IN,
        )

        self.assertEqual(
            movement.amount,
            Decimal("100.00"),
        )

    def test_cash_movement_can_be_created_as_out(self):
        movement = CashMovement.objects.create(
            cash_register=self.cash_register,
            movement_type=CashMovement.MovementType.OUT,
            source=CashMovement.Source.PURCHASE,
            amount=Decimal("200.00"),
        )

        self.assertEqual(
            movement.movement_type,
            CashMovement.MovementType.OUT,
        )

        self.assertEqual(
            movement.amount,
            Decimal("200.00"),
        )

    def test_cash_movement_is_linked_to_cash_register(self):
        movement = CashMovement.objects.create(
            cash_register=self.cash_register,
            movement_type=CashMovement.MovementType.IN,
            source=CashMovement.Source.SALE,
            amount=Decimal("150.00"),
        )

        self.assertEqual(
            movement.cash_register,
            self.cash_register,
        )

        self.assertEqual(
            self.cash_register.movements.count(),
            1,
        )

    def test_cash_movement_can_have_description(self):
        movement = CashMovement.objects.create(
            cash_register=self.cash_register,
            movement_type=CashMovement.MovementType.OUT,
            source=CashMovement.Source.OTHER,
            amount=Decimal("50.00"),
            description="Retirada de dinheiro",
        )

        self.assertEqual(
            movement.description,
            "Retirada de dinheiro",
        )


class CashServiceTests(TestCase):

    def setUp(self):
        self.cash_register = CashRegister.objects.create(
            opening_balance=Decimal("500.00"),
        )

    def test_get_cash_balance_starts_with_opening_balance(self):
        balance = get_cash_balance(self.cash_register)

        self.assertEqual(
            balance,
            Decimal("500.00"),
        )

    def test_cash_entry_increases_balance(self):
        create_cash_movement(
            cash_register=self.cash_register,
            movement_type=CashMovement.MovementType.IN,
            source=CashMovement.Source.SALE,
            amount=Decimal("100.00"),
        )

        balance = get_cash_balance(self.cash_register)

        self.assertEqual(
            balance,
            Decimal("600.00"),
        )

    def test_cash_exit_decreases_balance(self):
        create_cash_movement(
            cash_register=self.cash_register,
            movement_type=CashMovement.MovementType.OUT,
            source=CashMovement.Source.PURCHASE,
            amount=Decimal("200.00"),
        )

        balance = get_cash_balance(self.cash_register)

        self.assertEqual(
            balance,
            Decimal("300.00"),
        )

    def test_cash_cannot_become_negative(self):
        with self.assertRaises(ValueError):
            create_cash_movement(
                cash_register=self.cash_register,
                movement_type=CashMovement.MovementType.OUT,
                source=CashMovement.Source.PURCHASE,
                amount=Decimal("600.00"),
            )

    def test_closed_cash_cannot_receive_movement(self):
        self.cash_register.status = CashRegister.Status.CLOSED
        self.cash_register.save()

        with self.assertRaises(ValueError):
            create_cash_movement(
                cash_register=self.cash_register,
                movement_type=CashMovement.MovementType.IN,
                source=CashMovement.Source.SALE,
                amount=Decimal("100.00"),
            )

    def test_zero_amount_is_not_allowed(self):
        with self.assertRaises(ValueError):
            create_cash_movement(
                cash_register=self.cash_register,
                movement_type=CashMovement.MovementType.IN,
                source=CashMovement.Source.SALE,
                amount=Decimal("0.00"),
            )
