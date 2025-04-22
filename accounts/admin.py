from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
from django.contrib.auth import get_user_model
User = get_user_model()

class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ['username', 'email', 'phone', 'is_staff']
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Info', {'fields': ('phone', 'profile_picture')}),
    )

admin.site.register(User, CustomUserAdmin)
