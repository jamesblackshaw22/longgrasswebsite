from django.db import models
from django.contrib.auth.models import User
from shortuuidfield import ShortUUIDField


# Create your models here.
class Status(models.Model):
    name = models.CharField(max_length=30)
    creator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name


class Field(models.Model):
    name = models.CharField(max_length=30)
    description = models.TextField()
    code = ShortUUIDField()
    participants = models.ManyToManyField(User, related_name="participants", blank=True)
    creator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name


class Indecision(models.Model):
    title = models.CharField(max_length=45)
    description = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    no_earlier_than = models.DateField()
    status = models.ForeignKey(Status, on_delete=models.SET_NULL, null=True)
    field = models.ForeignKey(Field, on_delete=models.CASCADE)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name
