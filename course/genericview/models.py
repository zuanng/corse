from django.db import models

class Cat(models.Model):
    name = models.CharField(max_length=128)

class Dog(models.Model):
    name = models.CharField(max_length=128)