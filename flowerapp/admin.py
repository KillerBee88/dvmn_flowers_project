from django.contrib import admin
from .models import Order, Bouquet, Client, Courier

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
     list_display = ["client", "bouquet", "address", "delivery_date","delivery_time"]


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ["tg_id", "username"]


@admin.register(Courier)
class CourierAdmin(admin.ModelAdmin):
    list_display = ["tg_id", "username"]


@admin.register(Bouquet)
class BouquetAdmin(admin.ModelAdmin):
    list_display = ["name", "price", "desсription","type"]