from django.db import models
from projects.models import Project


class Line(models.Model):
    project = models.ForeignKey(Project)

class Trip(models.Model):
    line = models.ForeignKey(Line)