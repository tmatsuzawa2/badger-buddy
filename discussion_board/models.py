from django.db import models

# Create your models here.

class Post(models.Model):
    title = models.CharField(max_length=128)
    details = models.CharField(max_length=8192)
    create_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Reply(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    details = models.CharField(max_length=1024)
    create_date = models.DateTimeField(auto_now_add=True)

    # What's a good __str__ function for Reply?
    def __str__(self):
        return self.details
