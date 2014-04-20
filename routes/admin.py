from django.contrib import admin
from django.contrib.admin import ModelAdmin
from routes.models import Route

admin.site.register(Route, ModelAdmin)