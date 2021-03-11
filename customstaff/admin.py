from django.contrib import admin
from django.contrib.auth import get_user_model
from .models import *
from django.contrib.auth.admin import UserAdmin


class CustomUserAdmin(UserAdmin):
	list_display = ('email', 'username', 'is_teacher', 'is_nonteacher','is_supervisor', 'is_viceprincipal','is_principal','is_secretary', 'is_admin')
	search_fields = ('email', 'username', 'is_teacher', 'is_nonteacher','is_supervisor', 'is_viceprincipal','is_principal','is_secretary', 'is_admin')
	readonly_field = ()

	fieldsets = ()
	filter_horizontal = ()
	list_filter = ()

admin.site.register(User, CustomUserAdmin)
admin.site.register(SecretaryDetail)
admin.site.register(TeachingStaffDetail)
admin.site.register(NonTeachingStaffDetail)
admin.site.register(SupervisorDetail)
admin.site.register(LeaveApplication)
admin.site.register(VicePrincipalDetail)
# admin.site.register(IncrementAll)