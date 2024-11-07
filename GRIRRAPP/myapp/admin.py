from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import CustomUser
from django.utils.html import format_html
from django.urls import reverse

class CustomUserAdmin(BaseUserAdmin):
    list_display = ('email', 'username', 'phone_number', 'is_admin', 'user_type','view_children_link')
    list_filter = ('is_admin', 'user_type')

    def view_children_link(self, obj):
        # Generate the URL that leads to the parent details view
        url = reverse('admin_parent_details', args=[obj.id])
        return format_html('<a href="{}">View Children</a>', url)

    view_children_link.short_description = 'View Children'

    fieldsets = (
        (None, {'fields': ('email', 'username', 'phone_number', 'password')}),
        ('Permissions', {'fields': ('is_admin', 'is_active', 'user_type')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'phone_number', 'password1', 'password2', 'is_admin', 'user_type'),
        }),
    )
    search_fields = ('email', 'username', 'phone_number')
    ordering = ('email',)

admin.site.register(CustomUser, CustomUserAdmin)
