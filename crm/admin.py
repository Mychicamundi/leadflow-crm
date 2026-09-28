from django.contrib import admin
from .models import Activity, Lead

@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    list_display = ["name", "company", "stage", "value", "owner", "created_at"]
    list_filter = ["stage", "source"]
    search_fields = ["name", "email", "company"]
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs if request.user.is_superuser else qs.filter(owner=request.user)
    def save_model(self, request, obj, form, change):
        if not change:
            obj.owner = request.user
        super().save_model(request, obj, form, change)

@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ["title", "lead", "due_at", "done", "auto_generated"]
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs if request.user.is_superuser else qs.filter(lead__owner=request.user)
