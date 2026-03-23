from django.contrib import admin
from .models import Product, User, Address, Order, OrderItem, Review


admin.site.register(Product)
admin.site.register(User)
admin.site.register(Address)


class ReviewAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "product", "rating", "created_at", "updated_at"]  # list page
    readonly_fields = ["created_at", "updated_at"]  # detail page
    fields = ["user", "product", "rating", "content", "created_at", "updated_at"]  # form order


admin.site.register(Review, ReviewAdmin)


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0


class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderItemInline]


admin.site.register(Order, OrderAdmin)