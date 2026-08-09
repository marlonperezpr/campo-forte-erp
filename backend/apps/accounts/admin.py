from django.contrib import admin

from apps.accounts.models import Customer
from apps.accounts.models import Supplier
from apps.accounts.models import Product
from apps.accounts.models import ProductSupplier

# Registre seus modelos aqui.


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ("name", "phone", "email", "active")


@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ("name", "trade_name", "phone", "email", "active")


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "sale_price", "active")


@admin.register(ProductSupplier)
class ProductSupplierAdmin(admin.ModelAdmin):
    list_display = ("product", "supplier", "purchase_price")
