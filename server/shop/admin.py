# testing CD
from django.contrib import admin
from django.utils.html import format_html
from .models import Product, ProductImage, User, Address, Order, OrderItem, Review


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    fields = ["id", "product", "image_preview", "image"]
    readonly_fields = ["id", "image_preview"]

    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" width="80" height="80" style="object-fit: cover; border-radius: 4px;" />',
                obj.image.url
            )
        return "No Image"

    image_preview.short_description = "Preview"


class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageInline]

    list_display = [
        "id",
        "tag",
        "tagline",
        "brand",
        "title",
        "info",
        "category",
        "flavor",
        "weight",
        "serve",
        "final_price",
        "original_price",
        "stock",
        "avg_rating",
        "review_count",
        "is_active",
        "created_at",
    ]

    fields = [
        "id",
        "tag",
        "tagline",
        "brand",
        "title",
        "info",
        "category",
        "flavor",
        "weight",
        "serve",
        "final_price",
        "original_price",
        "stock",
        "avg_rating",
        "review_count",
        "is_active",
        "created_at",
    ]

    readonly_fields = ["id", "created_at"] # "avg_rating", "review_count",
    search_fields = ["title", "brand", "category", "tagline", "info"]
    list_filter = ["tag", "category", "brand", "is_active"]


class ReviewAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "user",
        "product",
        "rating",
        "content",
        "created_at",
        "updated_at",
    ]

    fields = [
        "id",
        "user",
        "product",
        "rating",
        "content",
        "created_at",
        "updated_at",
    ]

    readonly_fields = ["id", "created_at", "updated_at"]
    search_fields = ["user__email", "product__title", "content"]
    list_filter = ["rating", "created_at", "updated_at"]


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0

    fields = [
        "id",
        "order",
        "product",
        "title_snapshot",
        "unit_price_snapshot",
        "image_url_snapshot",
        "quantity",
        "line_total",
    ]

    readonly_fields = ["id"]


class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderItemInline]

    list_display = [
        "id",
        "user",
        "order_number",
        "status",
        "subtotal",
        "shipping_fee",
        "discount",
        "total",
        "shipping_snapshot",
        "created_at",
        "updated_at",
    ]

    fields = [
        "id",
        "user",
        "order_number",
        "status",
        "subtotal",
        "shipping_fee",
        "discount",
        "total",
        "shipping_snapshot",
        "created_at",
        "updated_at",
    ]

    readonly_fields = ["id", "created_at", "updated_at"]
    search_fields = ["order_number", "user__email"]
    list_filter = ["status", "created_at", "updated_at"]


class AddressAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "user",
        "recipient",
        "phone",
        "zip",
        "addr1",
        "addr2",
        "is_default",
        "created_at",
        "updated_at",
    ]

    fields = [
        "id",
        "user",
        "recipient",
        "phone",
        "zip",
        "addr1",
        "addr2",
        "is_default",
        "created_at",
        "updated_at",
    ]

    readonly_fields = ["id", "created_at", "updated_at"]
    search_fields = ["user__email", "recipient", "phone", "zip", "addr1", "addr2"]
    list_filter = ["is_default", "created_at", "updated_at"]


class UserAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "email",
        "password",
        "name",
        "phone",
        "role",
        "is_active",
        "is_staff",
        "created_at",
    ]

    fields = [
        "id",
        "email",
        "password",
        "name",
        "phone",
        "role",
        "is_active",
        "is_staff",
        "is_superuser",
        "groups",
        "user_permissions",
        "last_login",
        "created_at",
    ]

    readonly_fields = ["id", "created_at", "last_login"]
    search_fields = ["email", "name", "phone"]
    list_filter = ["role", "is_active", "is_staff", "is_superuser"]


admin.site.register(Product, ProductAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(Address, AddressAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Order, OrderAdmin)