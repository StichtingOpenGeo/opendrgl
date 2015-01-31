from django.contrib import admin
from data.models import Agency, Line, Stop, TripPattern, TripPatternStop, Trip, UserProfile, CalendarException, Calendar

admin.site.register(UserProfile)
admin.site.register(Agency)
admin.site.register(Line)
admin.site.register(Stop)

class TripPatternStopAdmin(admin.TabularInline):
    model = TripPatternStop

class TripAdmin(admin.StackedInline):
    model = Trip

@admin.register(TripPattern)
class TripPatternAdmin(admin.ModelAdmin):
    inlines = [TripPatternStopAdmin, TripAdmin]

class CalendarExceptionAdmin(admin.TabularInline):
    model = CalendarException

@admin.register(Calendar)
class CalendarAdmin(admin.ModelAdmin):
    inlines = [CalendarExceptionAdmin]