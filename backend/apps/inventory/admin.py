from django.contrib import admin

from apps.inventory.models import InventoryMovement


@admin.register(InventoryMovement)
class InventoryMovementAdmin(admin.ModelAdmin):
    list_display = (
        "product",
        "movement_type",
        "quantity",
        "reason",
        "created_at",
        "balance_after",
    )
