from django.contrib import admin
from .models import Topic

# Register your models here.
# Make the topics available in the admin dashboard
admin.site.register(Topic)
