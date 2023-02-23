from django.contrib import admin

# Register your models here.

from .models import (
    Sport,
    Chapter,
    KnockoutStep,
    FootballTeam,
    FootballPitch,
    FootballSchedule,
    FootballTable,
    FootballKnockout,
)

admin.site.register(Sport)
admin.site.register(Chapter)
admin.site.register(KnockoutStep)
admin.site.register(FootballTeam)
admin.site.register(FootballPitch)
admin.site.register(FootballSchedule)
admin.site.register(FootballTable)
admin.site.register(FootballKnockout)
