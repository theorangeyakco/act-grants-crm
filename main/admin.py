from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from main.models import User


class UserAdmin(BaseUserAdmin):
	list_display = ('name', 'phone', 'email', 'name', 'date_joined', 'is_staff')
	list_filter = ('is_staff', 'is_active')
	fieldsets = (
		(None, {'fields': ('email', 'password')}),
		('Personal info', {'fields': ('name', 'phone', 'company', 'avatar')}),
		('Permissions', {'fields': ('is_active', 'is_staff', 'notification_level', 'groups', 'user_permissions')}),
	)

	search_fields = ('email', 'name', 'phone')
	ordering = ('name',)
	filter_horizontal = ('user_permissions', 'groups')


admin.site.register(User, UserAdmin)