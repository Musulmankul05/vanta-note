from django.contrib import admin

from users.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    fields = ('username', 'first_name', 'last_name', 'email', 'is_staff', 'is_active', 'salt')
    readonly_fields = ('salt',)
    list_display = ('username', 'first_name', 'last_name', 'email')
    list_filter = ('is_staff', 'is_active')