from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import BaseUser

class CustomUserAdmin(UserAdmin):
    model = BaseUser
    list_display = ['email', 'first_name', 'last_name', 'is_active', 'is_staff']
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('role','first_name', 'last_name','phone_number','birthdate','Address','user_img')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important Dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    search_fields = ('email', 'first_name', 'last_name',)
    ordering = ('email',)

# Register the custom user model and its admin class
admin.site.register(BaseUser, CustomUserAdmin)
