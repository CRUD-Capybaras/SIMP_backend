from django.contrib import admin

from schedule.models import Carrier, Stop, Line, Timetable

admin.site.register(Carrier)
admin.site.register(Stop)
admin.site.register(Line)
admin.site.register(Timetable)