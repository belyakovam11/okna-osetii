from django.contrib import admin

from .models import CompletedWork, CustomerReview, HomePageAppearance


@admin.register(HomePageAppearance)
class HomePageAppearanceAdmin(admin.ModelAdmin):
    list_display = ("id", "background_image")
    fields = ("background_image",)

    def has_add_permission(self, request):
        return not HomePageAppearance.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(CompletedWork)
class CompletedWorkAdmin(admin.ModelAdmin):
    list_display = ("title", "location", "created_at", "is_published")
    list_filter = ("is_published", "created_at")
    list_editable = ("is_published",)
    search_fields = ("title", "description", "location")
    readonly_fields = ("created_at",)


@admin.register(CustomerReview)
class CustomerReviewAdmin(admin.ModelAdmin):
    list_display = ("author_name", "rating", "created_at", "is_published")
    list_filter = ("is_published", "rating", "created_at")
    list_editable = ("is_published",)
    search_fields = ("author_name", "text")
    readonly_fields = ("author_name", "text", "rating", "created_at")
