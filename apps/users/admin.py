from django.contrib import admin

from .models import OrderRequest, UserProfile


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "phone", "region")
    search_fields = ("user__username", "phone", "address")


@admin.register(OrderRequest)
class OrderRequestAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "material", "total_price", "status", "created_at")
    list_filter = ("status", "material", "created_at")
    list_editable = ("status",)
    search_fields = ("user__username", "phone", "address")
    readonly_fields = ("user", "material", "width", "height", "quantity", "total_price", "phone", "address", "comment", "created_at")
