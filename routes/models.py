from django.db import models
from projects.models import Project
from django.utils.translation import ugettext_lazy as _

class Route(models.Model):
    project = models.ForeignKey(Project)
    route_id = models.CharField(_("Lijnnummer"),max_length=10)
    destination = models.CharField(_("Eindbestemming"),max_length=100, blank=True)

    def __unicode__(self):
        return "%s - %s" % (self.route_id, self.destination)

class Trip(models.Model):
    line = models.ForeignKey(Route)