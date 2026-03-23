from django.contrib import admin
from .models import Product, User, Address, Order, OrderItem, Review

admin.site.register(Product)
admin.site.register(User)
admin.site.register(Address)
admin.site.register(Review)

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0


class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderItemInline]


admin.site.register(Order, OrderAdmin)