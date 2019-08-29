from django.contrib import admin

from .models import Item, OrderItem, Order, Topping

# Register your models here.

class ItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'position', 'size', 'name', 'type', 'price')
    list_display_links = ('name',)
    search_fields = ('name',)
    list_filter = ('type', 'size', 'position')
    #list_per_page = 25


admin.site.register(Item, ItemAdmin)
admin.site.register(Topping)
admin.site.register(Order)
admin.site.register(OrderItem)
