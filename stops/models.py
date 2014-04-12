from django.contrib.gis.db import models
from projects.models import Project
from django.utils.translation import ugettext_lazy as _

class Stop(models.Model):
    project = models.ForeignKey(Project)
    stop_id = models.CharField(max_length=15)
    town = models.CharField(max_length=50)
    name = models.CharField(max_length=100)
    location = models.PointField()

    class Meta:
        verbose_name = _("Halte")
        verbose_name_plural = _("Haltes")
        unique_together = ('project', 'stop_id')

    # Custom manager for geomodels/searches
    objects = models.GeoManager()

