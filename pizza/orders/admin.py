from django.contrib import admin

from .models import Item, OrderItem, Order, Topping

# Register your models here.

admin.site.register(Item)
admin.site.register(Topping)
admin.site.register(Order)
admin.site.register(OrderItem)
