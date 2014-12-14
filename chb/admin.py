from django.contrib import admin

# Register your models here.
from chb.models import ChbQuay, ChbStop

admin.site.register(ChbStop)
admin.site.register(ChbQuay)