from django.contrib import admin
from api.notification.models import Notification

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ("title", "type", "created_at", "read")
    list_filter = ("type", "read", "created_at")
    search_fields = ("title", "message")
    ordering = ("-created_at",)
    readonly_fields = ("created_at",)

