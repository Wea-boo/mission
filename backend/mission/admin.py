from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Group, Profile, Direction, Employee

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff')

    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('employee', 'main_profile')}),
    )
        
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'employee', 'main_profile', 'is_staff', 'is_active', 'groups')}
         ),
    )

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Group)
admin.site.register(Profile)
admin.site.register(Direction)
admin.site.register(Employee)


