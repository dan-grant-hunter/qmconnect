from django.db import models
from django.contrib.auth.models import User

# It represents the students' interests
# e.g. Python Programming, Big Data Processing, etc.
class Interest(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Profile(models.Model):
    YEAR = (
        ('1', '1st Year'),
        ('2', '2nd Year'),
        ('3', '3rd Year'),
    )

    SUBJECT = (
        ('BCS', 'BSc Computer Science'),
        ('BCSM', 'BSc Computer Science and Mathematics'),
        ('BCSIE', 'BSc Computer Science with Industrial Experience'),
        ('BCSWM', 'BSc Computer Science with Management (ITMB)'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    dob = models.DateField(auto_now=False, auto_now_add=False)
    image = models.ImageField(upload_to='profile_images', default='')
    universityYear = models.CharField(choices=YEAR, max_length=1, default='')
    subject = models.CharField(choices=SUBJECT, max_length=5, default='')
    interest = models.ManyToManyField(Interest)

    def __str__(self):
        return self.user.username
