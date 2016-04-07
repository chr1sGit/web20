from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


# Create your models here.

class Project(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    creation_date = timezone.now()

    def __str__(self):
        return self.description


class Sprint(models.Model):
    name = models.CharField(max_length=100)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)


class Task(models.Model):
    sprint = models.ForeignKey(Sprint, on_delete=models.CASCADE)
    PHASE = (
        ('ToDo', 'To Do'),
        ('iP', 'in Progress'),
        ('iR', 'in Review'),
        ('F', 'Finished'),
    )
    description = models.TextField()
    assignedUser = models.ForeignKey(User, related_name='tasks', verbose_name='User')


class InProjectIdea(models.Model):
    project = models.ForeignKey(Project)
    title = models.CharField(max_length=200)
    description = models.TextField()
    votes = models.IntegerField()


class GeneralIdea(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    votes = models.IntegerField()
