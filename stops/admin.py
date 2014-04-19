from django.contrib import admin

# Register your models here.
from leaflet.admin import LeafletGeoAdmin
from .models import Stop, Quay


admin.site.register(Stop, LeafletGeoAdmin)
admin.site.register(Quay, LeafletGeoAdmin)