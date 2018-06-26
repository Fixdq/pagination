from django.db import models

# Create your models here.
class Book(models.Model):
    title = models.CharField(max_length=16)
    publisher_date = models.DateField(auto_now_add=True)


class Publisher(models.Model):
    name = models.CharField(max_length=32)


class User(models.Model):
    username = models.CharField(max_length=32)
    pwd = models.CharField(max_length=32)
