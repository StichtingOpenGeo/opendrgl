from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext_lazy as _

class Project(models.Model):
    name = models.CharField(_("Projectnaam"), max_length=100)
    description = models.TextField(_("Omschrijving"), blank=True)

    def __unicode__(self):
        return self.name

class UserProject(models.Model):
    project = models.ForeignKey(Project)
    user = models.ForeignKey(User)
    level = models.CharField(max_length=1)