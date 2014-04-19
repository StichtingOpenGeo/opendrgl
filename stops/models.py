from django.contrib.gis.db import models
from projects.models import Project
from django.utils.translation import ugettext_lazy as _


class Stop(models.Model):
    project = models.ForeignKey(Project, verbose_name=_("Project"))
    stop_id = models.CharField(_('Unieke Identificatie'), max_length=10)
    town = models.CharField(_('Plaats'), max_length=50)
    name = models.CharField(_('Naam'), max_length=100)

    class Meta:
        verbose_name = _("Halte")
        verbose_name_plural = _("Haltes")
        unique_together = ('project', 'stop_id')

class Quay(models.Model):
    stop = models.ForeignKey(Stop, verbose_name=_("Halte"))
    project = models.ForeignKey(Project, verbose_name=_("Project")) # Duplicated to preserve the unique key
    quay_id = models.CharField(_('Haltenummer'), max_length=15)
    town = models.CharField(_('Plaats'), max_length=50)
    name = models.CharField(_('Naam'), max_length=100)
    location = models.PointField()

    class Meta:
        verbose_name = _("Haltepaal")
        verbose_name_plural = _("Haltepalen")
        unique_together = ('project', 'quay_id')

    # Custom manager for geomodels/searches
    objects = models.GeoManager()

