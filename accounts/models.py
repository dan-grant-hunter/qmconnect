from django.db import models
from django.contrib.auth.models import User

# It represents the modules studied by the user
# e.g. Procedural Programming, Web Programming, etc.
# Many-to-many relationship with the Profile model
class Module(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

# It represents the students' interests
# e.g. Python Programming, Big Data Processing, etc.
# Many-to-Many relationship with the Profile model
class Interest(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

# This model represents the user's profile
# Added to represent extra information about the users
class Profile(models.Model):
    YEAR = (
        ('1', '1st year'),
        ('2', '2nd year'),
        ('3', '3rd year'),
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
    module = models.ManyToManyField(Module)
    interest = models.ManyToManyField(Interest)

    def __str__(self):
        return self.user.username
