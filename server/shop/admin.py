# admin.py

from django.contrib import admin
from .models import User

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display  = ("id", "username", "email", "is_active", "is_staff", "is_superuser", "last_login", "date_joined")
    search_fields = ("username", "email")
    list_filter   = ("is_active", "is_staff", "is_superuser")

    fields = ("username", "email", "password", "is_active", "is_staff", "is_superuser", "last_login", "date_joined")
    readonly_fields = ("last_login", "date_joined")

    def save_model(self, request, obj, form, change):
        raw_pw = form.cleaned_data.get("password")
        if raw_pw and (not change or ("password" in form.changed_data)):
            obj.set_password(raw_pw)   # ← 해시 저장
        super().save_model(request, obj, form, change)
