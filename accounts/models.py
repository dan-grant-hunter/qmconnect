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
    # The 'default' field is needed because the fields below were added later
    image = models.ImageField(upload_to='profile_images', default='')
    universityYear = models.CharField(choices=YEAR, max_length=1, default='')
    subject = models.CharField(choices=SUBJECT, max_length=5, default='')
    # Many-to-many relationship with other classes/models
    module = models.ManyToManyField(Module)
    interest = models.ManyToManyField(Interest)
    # By default, the value of 'symmetrical' is 'True' for Many-to-many relationship which is a bi-directional relationship.
    # For messages, there is no need for a bi-directional relationship
    # e.g. a user can send a message and not get a reply
    message = models.ManyToManyField('self', blank=True, symmetrical=False, through="Message")

    def __str__(self):
        return self.user.username

# Model used for messages between the users
class Message(models.Model):
    sender = models.ForeignKey(Profile, related_name="sender", on_delete=models.CASCADE)
    receiver = models.ForeignKey(Profile, related_name="receiver", on_delete=models.CASCADE)
    text = models.CharField(max_length=4096)
    time = models.DateTimeField()

    def __str__(self):
        return '{} to {}: {}'.format(self.sender, self.receiver, self.text)
