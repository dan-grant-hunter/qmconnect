from django.contrib import admin
from .models import Topic, Question, Answer

# Register your models here.
# Make the topics available in the admin dashboard
admin.site.register(Topic)
admin.site.register(Question)
admin.site.register(Answer)
