from django.contrib import admin
from .models import UserProfile, Role, UserRoles
from .forms import UserProfileForm

# Register your models here.


class UserRoleInline(admin.TabularInline):
    model = UserProfile.role.through
    extra = 1


class UserProfileAdmin(admin.ModelAdmin):
    form = UserProfileForm
    inlines = [
        UserRoleInline,
    ]


admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Role)
admin.site.register(UserRoles)
