from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import Profile, Interest, Module, Message

# Add the Profile model to the Django admin interface
class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profiles'

# Add the Interest model to the Django admin interface
class InterestInline(admin.StackedInline):
    model = Interest
    can_delete = False
    verbose_name_plural = 'Interests'

# Add the Module model to the Django admin interface
class ModuleInline(admin.StackedInline):
    model = Interest
    can_delete = False
    verbose_name_plural = 'Interests'

# It removes the unnecessary fields from the Django admin interface
# It only displays the username, password and full name
class UserAdmin(BaseUserAdmin):
    fieldsets = (
        ('Personal info', {'fields': ('username', 'password', 'first_name', 'last_name')}),
    )
    inlines = (ProfileInline,)

admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Interest)
admin.site.register(Module)
admin.site.register(Message)
