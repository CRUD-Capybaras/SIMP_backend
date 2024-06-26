from django.db import models


class Carrier(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Line(models.Model):
    name = models.CharField(max_length=100)
    carrier = models.ForeignKey(Carrier, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} by {self.carrier.name}"


class Stop(models.Model):
    name = models.CharField(max_length=100)
    latitude = models.FloatField()
    longitude = models.FloatField()
    line = models.ForeignKey(Line, on_delete=models.CASCADE, related_name='stops')
    previous_stop = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='next_stops')

    def __str__(self):
        return self.name


class Timetable(models.Model):
    WEEKDAY = 'weekday'
    SATURDAY = 'saturday'
    SUNDAY_HOLIDAY = 'sunday_holiday'

    DAY_TYPE_CHOICES = [
        (WEEKDAY, 'Weekday'),
        (SATURDAY, 'Saturday'),
        (SUNDAY_HOLIDAY, 'Sunday/Holiday'),
    ]

    stop = models.ForeignKey(Stop, on_delete=models.CASCADE)
    time = models.TimeField()
    day_type = models.CharField(max_length=15, choices=DAY_TYPE_CHOICES)

    def __str__(self):
        return f"{self.stop.line.name} - {self.stop.name} at {self.time} on {self.get_day_type_display()}"
