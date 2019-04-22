import django_filters
from .models import Profile

'''
Code written by myself
'''

class ProfileFilter(django_filters.FilterSet):
    class Meta:
        model = Profile
        fields = {
            'interest': ['exact'],
            'universityYear': ['exact'],
            'subject': ['exact'],
            'module': ['exact']
        }
