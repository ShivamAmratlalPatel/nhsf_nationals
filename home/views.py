from django.shortcuts import render
import os
from django.http import HttpResponse
from django.template import loader, Template
from .commands import get_football_schedule, get_football_table


def index(request):
    service = os.environ.get('K_SERVICE', 'Unknown service')
    revision = os.environ.get('K_REVISION', 'Unknown revision')

    return render(request, 'homepage.html', context={
        "message": "It's running!",
        "Service": service,
        "Revision": revision,
    })


def football(request):
    """Return the football.html template in template/home"""

    template: Template = loader.get_template("football.html")
    context = {
        "schedules": get_football_schedule(),
        "group_stages": get_football_table()
    }
    return HttpResponse(template.render(context))


def loaderio(request):
    """Return the loaderio verification token"""

    return HttpResponse("loaderio-6f638dd217ebc0c6ad2e477d8e9e2e8c")
