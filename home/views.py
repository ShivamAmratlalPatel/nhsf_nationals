from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import render
import os
from django.http import HttpResponse, HttpRequest, HttpResponseServerError
from django.template import loader, Template

from .commands import get_football_schedule, get_football_table, log_football_score, \
    UnplayedGamesForm, get_unplayed_football_games


# @cache_page(60 * 10)
def index(request: HttpRequest) -> HttpResponse:
    service = os.environ.get('K_SERVICE', 'Unknown service')
    revision = os.environ.get('K_REVISION', 'Unknown revision')

    return render(request, 'homepage.html', context={
        "authenticated": request.user.is_authenticated,
    })


# @cache_page(60 * 10)
def football(request: HttpRequest) -> HttpResponse:
    """Return the football.html template in template/home"""

    template: Template = loader.get_template("football.html")
    context = {
        "schedules": get_football_schedule(),
        "group_stages": get_football_table(),
        "authenticated": request.user.is_authenticated,

    }
    return HttpResponse(template.render(context))


def loaderio(request: HttpRequest) -> HttpResponse:
    """Return the loaderio verification token"""

    return HttpResponse("loaderio-6f638dd217ebc0c6ad2e477d8e9e2e8c")


@login_required
def logfootballscore(request: HttpRequest) -> HttpResponse:
    """Return the football_score.html template in template/home"""
    if request.user.is_authenticated:
        try:
            game_id = int(str(request.POST["game"]))
            home_score = int(str(request.POST["team_1_score"]))
            away_score = int(str(request.POST["team_2_score"]))
            log_football_score(game_id, home_score, away_score)
            return HttpResponse("Success")
        except KeyError:
            return HttpResponse("Missing data")
        except ValueError:
            return HttpResponse("Invalid data")
        except Exception:
            raise HttpResponseServerError
    else:
        raise PermissionDenied


def score(request: HttpRequest) -> HttpResponse:
    """Return the football_score.html template in template/home"""
    if request.user.is_authenticated:
        if request.method == "POST":
            logfootballscore(request)

            # Initialise the form again
            form = UnplayedGamesForm()
            form.fields["game"].choices = get_unplayed_football_games()
            template: Template = loader.get_template("football_score.html")
            return HttpResponse(template.render(context={
                "form": form, "success": True,
                "authenticated": request.user.is_authenticated
            }, request=request))
        else:
            form = UnplayedGamesForm()
            template: Template = loader.get_template("football_score.html")
            return HttpResponse(template.render(context={
                "form": form, "success": False,
                "authenticated": request.user.is_authenticated
            }, request=request))
    else:
        raise PermissionDenied
