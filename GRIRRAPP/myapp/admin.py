from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import CustomUser

class CustomUserAdmin(BaseUserAdmin):
    list_display = ('email', 'username', 'phone_number', 'is_admin', 'user_type')
    list_filter = ('is_admin', 'user_type')

    fieldsets = (
        (None, {'fields': ('email', 'username', 'phone_number', 'password')}),
        ('Permissions', {'fields': ('is_admin', 'is_active', 'user_type')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'phone_number', 'password1', 'password2', 'is_admin', 'user_type')},
        ),
    )
    search_fields = ('email', 'username', 'phone_number')
    ordering = ('email',)

admin.site.register(CustomUser, CustomUserAdmin)
