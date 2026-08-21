from decimal import Decimal

from django.db import transaction
from django.db.models import Sum

from apps.finance.models.cash_movement import CashMovement
from apps.finance.models.cash_register import CashRegister


@transaction.atomic
def create_cash_movement(
    *,
    cash_register,
    movement_type,
    source,
    amount,
    description="",
):
    amount = Decimal(amount)

    if amount <= 0:
        raise ValueError("O valor da movimentação deve ser maior que zero.")

    if cash_register.status != CashRegister.Status.OPEN:
        raise ValueError("Não é possível movimentar um caixa fechado.")

    if movement_type == CashMovement.MovementType.IN:
        pass

    elif movement_type == CashMovement.MovementType.OUT:
        current_balance = get_cash_balance(cash_register)

        if amount > current_balance:
            raise ValueError("O caixa não pode ficar negativo.")

    else:
        raise ValueError("Tipo de movimentação inválido.")

    return CashMovement.objects.create(
        cash_register=cash_register,
        movement_type=movement_type,
        source=source,
        amount=amount,
        description=description,
    )


def get_cash_balance(cash_register):
    total_in = cash_register.movements.filter(
        movement_type=CashMovement.MovementType.IN
    ).aggregate(total=Sum("amount"))["total"] or Decimal("0.00")

    total_out = cash_register.movements.filter(
        movement_type=CashMovement.MovementType.OUT
    ).aggregate(total=Sum("amount"))["total"] or Decimal("0.00")

    return cash_register.opening_balance + total_in - total_out
