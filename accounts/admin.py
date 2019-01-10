from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import Profile, Interest

# Register your models here.
class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profiles'

class InterestInline(admin.StackedInline):
    model = Interest
    can_delete = False
    verbose_name_plural = 'Interests'

class UserAdmin(BaseUserAdmin):
    fieldsets = (
        ('Personal info', {'fields': ('username', 'password', 'first_name', 'last_name')}),
    )
    inlines = (ProfileInline,)

admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Interest)
