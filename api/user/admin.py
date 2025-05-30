from __future__ import annotations

from typing import Any

from django.contrib import admin

from api.clinical.models import DentistAssistant
from api.user.models import User


class DentistAssistantInline(admin.TabularInline):
    model = DentistAssistant
    fk_name = 'assistant'
    extra = 1
    verbose_name = "Assigned Dentist"
    verbose_name_plural = "Assigned Dentists"
    autocomplete_fields = ['dentist']

    def has_change_permission(self, request, obj=None):
        return True

    def has_add_permission(self, request, obj):
        return obj and obj.groups.filter(name='Assistant').exists()

    def has_delete_permission(self, request, obj=None):
        return True

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    inlines = [DentistAssistantInline]
    filter_horizontal = ("groups", "user_permissions")
    search_fields = ["username", "email", "first_name", "last_name"]
    list_display = (
        "username",
        "is_active",
        "is_staff",
        "is_superuser",
    )

    def save_model(
        self,
        request: Any,
        obj: User,
        form: None,
        change: bool,  # noqa: FBT001
    ) -> None:
        """Update user password if it is not raw.

        This is needed to hash password when updating user from admin panel.
        """
        has_raw_password = obj.password.startswith("pbkdf2_sha256")
        if not has_raw_password:
            obj.set_password(obj.password)

        super().save_model(request, obj, form, change)
