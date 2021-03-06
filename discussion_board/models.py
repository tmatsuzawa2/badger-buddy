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
    anonymous = models.BooleanField(default=False)

    class Meta:
        ordering = ['-create_date']

    def __str__(self):
        return self.title

    def display_user(self):
        if self.anonymous:
            return "Anonymous"
        else:
            return self.user.username

    def super_display_user(self):
        display_name = self.user.username
        if self.anonymous:
            display_name  += " (Anonymous to other students)"
        return display_name

class Reply(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, default=None)
    details = models.CharField(max_length=1024)
    create_date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    anonymous = models.BooleanField(default=False)

    class Meta:
        ordering = ['create_date']

    def display_user(self):
        if self.anonymous:
            return "Anonymous"
        else:
            return self.user.username
    
    def super_display_user(self):
        display_name = self.user.username
        if self.anonymous:
            display_name  += " (Anonymous to other students)"
        return display_name 
        
    # What's a good __str__ function for Reply?
    def __str__(self):
        if self.user.profile.anonymous:
            return 'Comment {} by Anonymous at {}'.format(self.details, self.create_date)
        else:
            return 'Comment {} by {} at {}'.format(self.details, self.display_user(), self.create_date)


class Meeting(models.Model):
    link = models.URLField(max_length=250)
    date_time = models.DateTimeField()
    post = models.ForeignKey(Post, on_delete=models.CASCADE, default=None)

    def __str__(self):
        return str(self.id)


class MeetingUsers(models.Model):
    meeting = models.ForeignKey(Meeting, on_delete=models.CASCADE, default=None)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)


class Quotes(models.Model):
    text = models.TextField()
    author = models.TextField()

    def str(self):
        return self.content


class Prompts(models.Model):
    text = models.TextField()

    def str(self):
        return self.content