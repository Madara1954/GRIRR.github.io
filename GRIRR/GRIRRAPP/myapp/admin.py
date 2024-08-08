from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import CustomUser

class CustomUserAdmin(BaseUserAdmin):
    list_display = ('email', 'username', 'phone_number', 'is_admin')
    search_fields = ('email', 'username', 'phone_number')
    ordering = ('email',)
    filter_horizontal = ()
    list_filter = ('is_admin',)

    fieldsets = (
        (None, {'fields': ('email', 'username', 'phone_number', 'password')}),
        ('Permissions', {'fields': ('is_admin', 'groups', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'phone_number', 'password1', 'password2', 'is_admin')}
        ),
    )

admin.site.register(CustomUser, CustomUserAdmin)
