from django.db import models


class ChbStop(models.Model):
    public_code = models.CharField(max_length=13, unique=True)
    type = models.CharField(max_length=25)
    name = models.CharField(max_length=100)
    city = models.CharField(max_length=100, blank=True, null=True)

class ChbQuay(models.Model):
    public_code = models.CharField(max_length=13, unique=True)
    stop = models.ForeignKey(ChbStop, related_name="quays")
    name = models.CharField(max_length=100)
    city = models.CharField(max_length=100, blank=True, null=True)
    # TODO: Make this Geo field
    lat = models.DecimalField(max_digits=10, decimal_places=8, blank=True, null=True)
    lon = models.DecimalField(max_digits=10, decimal_places=8, blank=True, null=True)