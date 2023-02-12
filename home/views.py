from django.shortcuts import render
import os
from django.http import HttpResponse
from django.template import loader, Template
from .commands import get_football_schedule


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
        "schedules": get_football_schedule()
    }
    return HttpResponse(template.render(context))