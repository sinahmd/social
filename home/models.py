from django.db import models
from django.contrib.auth.models import User
class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField()
    slug = models.SlugField()
    created = models.DateTimeField(auto_now_add=True)  # auto_now_add for the first time use and once.
    updated = models.DateTimeField(auto_now=True)  # auto_now for  every time an object save or change.
    def __str__(self):
        return f'{self.slug} - {self.updated}'
