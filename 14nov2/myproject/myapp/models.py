from django.db import models

# Create your models here.


class Post(models.Model):
 title = models.CharField(max_length=150)
 desc = models.TextField()


class Contact(models.Model):
 name = models.CharField(max_length=150)
 email = models.EmailField(max_length=150)
 address = models.CharField(max_length=500)
 message = models.TextField()