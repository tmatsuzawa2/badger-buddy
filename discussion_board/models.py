from django.db import models

# Create your models here.
class User(models.Model):
    Overseer = 'Overseer'
    Student = 'Student'
    ROLE_CHOICES = (
        (Overseer, 'Overseer'),
        (Student, 'Student')
    )

    user_type = models.TextField(choices=ROLE_CHOICES)
    username = models.CharField(max_length=255, default='foo', unique=True)
    password = models.CharField(max_length=255, default='foo')
    email = models.EmailField(max_length=254)
    anonymous = models.BooleanField()
    first_name = models.CharField(max_length=128)
    last_name = models.CharField(max_length=128)

    def __str__(self):
        return self.username

class Post(models.Model):
    title = models.CharField(max_length=128)
    details = models.CharField(max_length=8192)
    create_date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)

    def __str__(self):
        return self.title

class Tags(models.Model):
    title = models.CharField(max_length=128)

    def __str__(self):
        return self.title

class Post_Tags(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, default=None)
    tag = models.ForeignKey(Tags, on_delete=models.CASCADE,default=None)

class Reply(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, default=None)
    details = models.CharField(max_length=1024)
    create_date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    # What's a good __str__ function for Reply?
    def __str__(self):
        return self.details

class Meeting(models.Model):
    link = models.URLField(max_length=250)
    date_time = models.DateTimeField()
    post = models.ForeignKey(Post, on_delete=models.CASCADE, default=None)

    def __str__(self):
        return str(self.id)

class MeetingUsers(models.Model):
    meeting = models.ForeignKey(Meeting, on_delete=models.CASCADE, default=None)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)

class Activity(models.Model):
    Prompt = 'Prompt'
    Quote = 'Quote'
    ROLE_CHOICES = (
        (Prompt, 'Prompt'),
        (Quote, 'Quote')
    )

    type_id = models.TextField(choices=ROLE_CHOICES)
    content = models.CharField(max_length=8192)

    def __str__(self):
        return self.content


