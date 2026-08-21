from django.contrib import admin

from apps.inventory.models import InventoryMovement


@admin.register(InventoryMovement)
class InventoryMovementAdmin(admin.ModelAdmin):
    list_display = (
        "product",
        "movement_type",
        "source",
        "quantity",
        "balance_after",
        "created_at",
    )

    list_filter = (
        "movement_type",
        "source",
    )

    search_fields = ("product__name",)
