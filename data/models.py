from django.db import models

class Agency(models.Model):
    datacode = models.CharField(max_length=5, unique=True)
    name = models.CharField(max_length=25)

    def __str__(self):
        return self.datacode;


class Stop(models.Model):
    public_number = models.CharField(max_length=10, unique=True)
    planning_number = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=100)
    city = models.CharField(max_length=25)
    # TODO: Make this Geo field
    lat = models.DecimalField(max_digits=10, decimal_places=8)
    lng = models.DecimalField(max_digits=10, decimal_places=8)

    def __str__(self):
        return self.public_number;


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

    def __str__(self):
        return "%s line %s" % (self.agency, self.public_number)


class TripPattern(models.Model):
    line = models.ForeignKey(Line)


class TripPatternStop(models.Model):
    pattern = models.ForeignKey(TripPattern)
    order = models.PositiveSmallIntegerField()
    stop = models.ForeignKey(Stop)
    arrival_delta = models.PositiveIntegerField() # Seconds since first stop, 0 if order = 0
    departure_delta = models.PositiveIntegerField()

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
    is_cancel = models.BooleanField(default=False) # Otherwise it's an addition
    date = models.DateField()


class Trip(models.Model):
    trip_pattern = models.ForeignKey(TripPattern)
    start_time = models.TimeField()
    calendar = models.ForeignKey(Calendar)

    class Meta:
        unique_together = (('trip_pattern', 'start_time'), )
