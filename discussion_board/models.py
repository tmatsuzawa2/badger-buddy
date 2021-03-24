from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Make user email field unique
User._meta.get_field('email')._unique = True

# Create your models here.
class Profile(models.Model):
    Overseer = 'Overseer'
    Student = 'Student'
    ROLE_CHOICES = (
        (Overseer, 'Overseer'),
        (Student, 'Student')
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_type = models.TextField(choices=ROLE_CHOICES, default=Student)
    anonymous = models.BooleanField(default=True)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

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

    class Meta:
        ordering = ['create_date']
        
    # What's a good __str__ function for Reply?
    def __str__(self):
        return 'Comment {} by {} at {}'.format(self.details, self.user.username, self.create_date)

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


