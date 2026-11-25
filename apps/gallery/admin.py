from django.contrib import admin

from .models import Materials


@admin.register(Materials)
class MaterialsAdmin(admin.ModelAdmin):
    list_display = ("name", "price", "rub", "in_stock")
    list_editable = ("price", "in_stock")
    fields = ("slug", "name", "image", "price", "rub", "in_stock")
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name",)
