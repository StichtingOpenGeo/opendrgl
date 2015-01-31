from django.contrib.auth.models import User
from django.db import models
from django.db.models import Max

class Agency(models.Model):
    datacode = models.CharField(max_length=5, unique=True)
    name = models.CharField(max_length=25)

    def __str__(self):
        return self.datacode;


class UserProfile(models.Model):
    user = models.OneToOneField(User, related_name='profile')
    default_agency = models.ForeignKey(Agency, null=True)


class Stop(models.Model):
    agency = models.ForeignKey(Agency)
    public_number = models.CharField(max_length=13)
    planning_number = models.PositiveIntegerField()
    name = models.CharField(max_length=100)
    city = models.CharField(max_length=25, blank=True, null=True)
    # TODO: Make this Geo field
    lat = models.DecimalField(max_digits=10, decimal_places=8, blank=True, null=True)
    lon = models.DecimalField(max_digits=10, decimal_places=8, blank=True, null=True)

    def __str__(self):
        return "%s - %s" % (self.agency.name, self.public_number)

    class Meta:
        unique_together = (('agency', 'public_number'), ('agency', 'planning_number'))

    @staticmethod
    def get_next_number(agency):
        data = Stop.objects.filter(agency_id=agency).aggregate(Max('planning_number'))
        if 'planning_number__max' and data['planning_number__max'] is not None:
            return int(data['planning_number__max']) + 1
        else:
            return 1

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if self.planning_number is None or self.planning_number == '':
            self.planning_number = Stop.get_next_number(self.agency)
        if self.public_number is None or self.public_number == '':
            self.public_number = self.planning_number
        super(Stop, self).save(force_insert, force_update, using, update_fields)


class StopProperty(models.Model):
    stop = models.ForeignKey(Stop)
    key = models.CharField(max_length=10)
    value = models.TextField()

    class Meta:
        unique_together = (('stop', 'key'))

    def __str__(self):
        return "%s - %s" (self.stop, self.key);


class Line(models.Model):
    agency = models.ForeignKey(Agency)
    planning_number = models.CharField(max_length=10)
    public_number = models.PositiveSmallIntegerField()

    class Meta:
        unique_together = (('agency', 'planning_number'), )

    def save(self, *args, **kwargs):
        create = not self.pk
        super(Line, self).save(*args, **kwargs)
        if create:
            forward = TripPattern(line=self, is_forward=True)
            forward.save()
            backward = TripPattern(line=self, is_forward=False)
            backward.save()

    def __str__(self):
        return "%s line %s" % (self.agency, self.public_number)


class TripPattern(models.Model):
    line = models.ForeignKey(Line, related_name='patterns')
    is_forward = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        create = not self.pk
        super(TripPattern, self).save(*args, **kwargs)
        if create:
            trip = Trip(pattern=self, start_time=6*60*60)
            trip.save()

    def clone(self):
        p = TripPattern()
        p.line = self.line
        p.is_forward = self.is_forward
        p.save()
        for stop in self.stops.all():
            tps = TripPatternStop()
            tps.pattern = p
            tps.order = stop.order
            tps.stop = stop.stop
            tps.arrival_delta = stop.arrival_delta
            tps.departure_delta = stop.departure_delta
            tps.save()
        return p

    def insert_stop(self, stop_id, pre, post):
        # Insert a stop in a pattern
        # Walk through all the stops, from top to bottom, incrementing each order by one, up to and including the stop
        # after the position we want to insert
        post_stop_found = False
        pre_stop = None
        for stop in self.stops.all().order_by('-order'):
            if stop.pk == pre:
                pre_stop = stop
            elif stop.pk == post:
                post_stop_found = True
                stop.order += 1
                stop.save()
            elif post_stop_found is False and pre_stop is None:
                stop.order += 1
                stop.save()
        if pre_stop:
            tps = TripPatternStop()
            tps.pattern = self
            tps.stop_id = stop_id
            tps.order = pre_stop.order + 1
            tps.arrival_delta = pre_stop.arrival_delta
            tps.departure_delta = pre_stop.departure_delta
            tps.save()
            return tps
        return None

class TripPatternStop(models.Model):
    pattern = models.ForeignKey(TripPattern, related_name='stops')
    order = models.PositiveSmallIntegerField()
    stop = models.ForeignKey(Stop)
    arrival_delta = models.PositiveIntegerField(blank=True, null=True)  # Seconds since first stop, 0 if order = 0
    departure_delta = models.PositiveIntegerField(blank=True, null=True)

    class Meta:
        unique_together = (('pattern', 'order'), )


class Calendar(models.Model):
    agency = models.ForeignKey(Agency)
    from_date = models.DateField()
    to_date = models.DateField()
    on_monday = models.BooleanField(default=False)
    on_tuesday = models.BooleanField(default=False)
    on_wednesday = models.BooleanField(default=False)
    on_thursday = models.BooleanField(default=False)
    on_friday = models.BooleanField(default=False)
    on_saturday = models.BooleanField(default=False)
    on_sunday = models.BooleanField(default=False)


class CalenderExceptions(models.Model):
    calender = models.ForeignKey(Calendar)
    is_cancel = models.BooleanField(default=False)  # Otherwise it's an addition
    date = models.DateField()


class Trip(models.Model):
    pattern = models.ForeignKey(TripPattern, related_name="trips")
    start_time = models.PositiveIntegerField()  # Seconds since midnight
    calendar = models.ForeignKey(Calendar, blank=True, null=True)  # Null = every day

    class Meta:
        unique_together = (('pattern', 'start_time'), )
