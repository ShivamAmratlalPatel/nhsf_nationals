from django.contrib import admin

from .models import (
    Chapter,
    FootballKnockout,
    FootballPitch,
    FootballSchedule,
    FootballTable,
    FootballTeam,
    KnockoutStep,
    Sport,
)

# Register your models here.


admin.site.register(Sport)
admin.site.register(Chapter)
admin.site.register(KnockoutStep)
admin.site.register(FootballTeam)
admin.site.register(FootballPitch)
admin.site.register(FootballSchedule)
admin.site.register(FootballTable)
admin.site.register(FootballKnockout)
