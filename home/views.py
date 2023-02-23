from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import render
import os
from django.http import (
    HttpResponse,
    HttpRequest,
    HttpResponseServerError,
    HttpResponseBadRequest,
    HttpResponseForbidden,
)
from django.template import loader, Template

from .commands import (
    get_football_schedule,
    get_football_table,
    log_football_score,
    UnplayedFootballGamesForm,
    get_unplayed_football_games,
    get_football_knockout_stages,
    get_netball_schedule,
    get_netball_table,
    log_netball_score,
    UnplayedNetballGamesForm,
    get_unplayed_netball_games,
    get_netball_knockout_stages,
    get_kho_schedule,
    get_kho_table,
    log_kho_score,
    UnplayedKhoGamesForm,
    get_unplayed_kho_games,
    get_kho_knockout_stages,
    get_kabaddi_schedule,
    get_kabaddi_table,
    log_kabaddi_score,
    UnplayedKabaddiGamesForm,
    get_unplayed_kabaddi_games,
    get_kabaddi_knockout_stages,
    get_cricket_schedule,
    get_cricket_table,
    log_cricket_score,
    UnplayedCricketGamesForm,
    get_unplayed_cricket_games,
    get_cricket_knockout_stages,
    get_badminton_schedule,
    get_badminton_table,
    log_badminton_score,
    UnplayedBadmintonGamesForm,
    get_unplayed_badminton_games,
    get_badminton_knockout_stages,
    send_message,
)


# @cache_page(60 * 10)
def index(request: HttpRequest) -> HttpResponse:
    service = os.environ.get("K_SERVICE", "Unknown service")
    revision = os.environ.get("K_REVISION", "Unknown revision")

    return render(
        request,
        "homepage.html",
        context={
            "authenticated": request.user.is_authenticated,
        },
    )


# @cache_page(60 * 10)
def football(request: HttpRequest) -> HttpResponse:
    """Return the football.html template in template/home"""

    template: Template = loader.get_template("football.html")
    context = {
        "schedules": get_football_schedule(),
        "group_stages": get_football_table(),
        "authenticated": request.user.is_authenticated,
        "knockout_stages": get_football_knockout_stages(),
    }
    return HttpResponse(template.render(context))


@login_required
def logfootballscore(request: HttpRequest) -> HttpResponse:
    """Return the football_score.html template in template/home"""
    if request.user.is_authenticated:
        try:
            home_penalty_score = None
            away_penalty_score = None
            game_id = int(str(request.POST["game"]))
            home_score = int(str(request.POST["team_1_score"]))
            away_score = int(str(request.POST["team_2_score"]))
            try:
                home_penalty_score = int(str(request.POST["team_1_penalty"]))
                away_penalty_score = int(str(request.POST["team_2_penalty"]))
            except ValueError:
                home_penalty_score = None
                away_penalty_score = None
            except Exception as e:
                print(e)
            finally:
                score_log = log_football_score(
                    game_id,
                    home_score,
                    away_score,
                    home_penalty_score,
                    away_penalty_score,
                )
                send_message(
                    "football",
                    f"{request.user.first_name} {request.user.last_name} has logged game {score_log}",
                )
                return HttpResponse("Success")
        except KeyError:
            return HttpResponse("Missing data")
        except ValueError:
            return HttpResponse("Invalid data")
        except Exception:
            raise HttpResponseServerError
    else:
        raise PermissionDenied


@login_required
def scorefootball(request: HttpRequest) -> HttpResponse:
    """Return the football_score.html template in template/home"""
    if request.user.is_authenticated:
        if request.method == "POST":
            function_response = logfootballscore(request)
            if isinstance(function_response, HttpResponseBadRequest):
                return function_response
            # Initialise the form again
            form = UnplayedFootballGamesForm()
            form.fields["game"].choices = get_unplayed_football_games()
            template: Template = loader.get_template("football_score.html")
            return HttpResponse(
                template.render(
                    context={
                        "form": form,
                        "success": True,
                        "authenticated": request.user.is_authenticated,
                    },
                    request=request,
                )
            )
        else:
            form = UnplayedFootballGamesForm()
            form.fields["game"].choices = get_unplayed_football_games()
            template: Template = loader.get_template("football_score.html")
            return HttpResponse(
                template.render(
                    context={
                        "form": form,
                        "success": False,
                        "authenticated": request.user.is_authenticated,
                    },
                    request=request,
                )
            )
    else:
        return HttpResponseForbidden("You are not logged in")


def netball(request: HttpRequest) -> HttpResponse:
    """Return the netball.html template in template/home"""

    template: Template = loader.get_template("netball.html")
    context = {
        "schedules": get_netball_schedule(),
        "group_stages": get_netball_table(),
        "authenticated": request.user.is_authenticated,
        "knockout_stages": get_netball_knockout_stages(),
    }
    return HttpResponse(template.render(context))


@login_required
def lognetballscore(request: HttpRequest) -> HttpResponse:
    """Return the netball_score.html template in template/home"""
    if request.user.is_authenticated:
        try:
            game_id = int(str(request.POST["game"]))
            home_score = int(str(request.POST["team_1_score"]))
            away_score = int(str(request.POST["team_2_score"]))
            try:
                home_penalty_score = int(str(request.POST["team_1_penalty"]))
                away_penalty_score = int(str(request.POST["team_2_penalty"]))
            except Exception as e:
                print(e)
                home_penalty_score = None
                away_penalty_score = None
            finally:
                print(
                    game_id,
                    home_score,
                    away_score,
                    home_penalty_score,
                    away_penalty_score,
                )
                score_log = log_netball_score(
                    game_id,
                    home_score,
                    away_score,
                    home_penalty_score,
                    away_penalty_score,
                )
                send_message(
                    "netball",
                    f"{request.user.first_name} {request.user.last_name} has logged game {score_log}",
                )
                return HttpResponse("Success")
        except KeyError:
            return HttpResponse("Missing data")
        except ValueError:
            return HttpResponse("Invalid data")
        except Exception:
            raise HttpResponseServerError
    else:
        raise PermissionDenied


@login_required
def scorenetball(request: HttpRequest) -> HttpResponse:
    """Return the netball_score.html template in template/home"""
    if request.user.is_authenticated:
        if request.method == "POST":
            lognetballscore(request)
            # Initialise the form again
            form = UnplayedNetballGamesForm()
            form.fields["game"].choices = get_unplayed_netball_games()
            template: Template = loader.get_template("netball_score.html")
            return HttpResponse(
                template.render(
                    context={
                        "form": form,
                        "success": True,
                        "authenticated": request.user.is_authenticated,
                    },
                    request=request,
                )
            )
        else:
            form = UnplayedNetballGamesForm()
            form.fields["game"].choices = get_unplayed_netball_games()
            template: Template = loader.get_template("netball_score.html")
            return HttpResponse(
                template.render(
                    context={
                        "form": form,
                        "success": False,
                        "authenticated": request.user.is_authenticated,
                    },
                    request=request,
                )
            )
    else:
        raise PermissionDenied


def cricket(request: HttpRequest) -> HttpResponse:
    """Return the cricket.html template in template/home"""

    template: Template = loader.get_template("cricket.html")
    context = {
        "schedules": get_cricket_schedule(),
        "group_stages": get_cricket_table(),
        "authenticated": request.user.is_authenticated,
        "knockout_stages": get_cricket_knockout_stages(),
    }
    return HttpResponse(template.render(context))


@login_required
def logcricketscore(request: HttpRequest) -> HttpResponse:
    """Return the cricket_score.html template in template/home"""
    if request.user.is_authenticated:
        try:
            game_id = int(str(request.POST["game"]))
            home_score = int(str(request.POST["team_1_score"]))
            away_score = int(str(request.POST["team_2_score"]))
            try:
                home_penalty_score = int(str(request.POST["team_1_penalty"]))
                away_penalty_score = int(str(request.POST["team_2_penalty"]))
            except Exception as e:
                print(e)
                home_penalty_score = None
                away_penalty_score = None
            finally:
                print(
                    game_id,
                    home_score,
                    away_score,
                    home_penalty_score,
                    away_penalty_score,
                )
                score_log = log_cricket_score(
                    game_id,
                    home_score,
                    away_score,
                    home_penalty_score,
                    away_penalty_score,
                )
                send_message(
                    "cricket",
                    f"{request.user.first_name} {request.user.last_name} has logged game {score_log}",
                )
                return HttpResponse("Success")
        except KeyError:
            return HttpResponse("Missing data")
        except ValueError:
            return HttpResponse("Invalid data")
        except Exception:
            raise HttpResponseServerError
    else:
        raise PermissionDenied


@login_required
def scorecricket(request: HttpRequest) -> HttpResponse:
    """Return the cricket_score.html template in template/home"""
    if request.user.is_authenticated:
        if request.method == "POST":
            logcricketscore(request)
            # Initialise the form again
            form = UnplayedCricketGamesForm()
            form.fields["game"].choices = get_unplayed_cricket_games()
            template: Template = loader.get_template("cricket_score.html")
            return HttpResponse(
                template.render(
                    context={
                        "form": form,
                        "success": True,
                        "authenticated": request.user.is_authenticated,
                    },
                    request=request,
                )
            )
        else:
            form = UnplayedCricketGamesForm()
            form.fields["game"].choices = get_unplayed_cricket_games()
            template: Template = loader.get_template("cricket_score.html")
            return HttpResponse(
                template.render(
                    context={
                        "form": form,
                        "success": False,
                        "authenticated": request.user.is_authenticated,
                    },
                    request=request,
                )
            )
    else:
        raise PermissionDenied


def kabaddi(request: HttpRequest) -> HttpResponse:
    """Return the kabaddi.html template in template/home"""

    template: Template = loader.get_template("kabaddi.html")
    context = {
        "schedules": get_kabaddi_schedule(),
        "group_stages": get_kabaddi_table(),
        "authenticated": request.user.is_authenticated,
        "knockout_stages": get_kabaddi_knockout_stages(),
    }
    return HttpResponse(template.render(context))


@login_required
def logkabaddiscore(request: HttpRequest) -> HttpResponse:
    """Return the kabaddi_score.html template in template/home"""
    if request.user.is_authenticated:
        try:
            game_id = int(str(request.POST["game"]))
            home_score = int(str(request.POST["team_1_score"]))
            away_score = int(str(request.POST["team_2_score"]))
            try:
                home_penalty_score = int(str(request.POST["team_1_penalty"]))
                away_penalty_score = int(str(request.POST["team_2_penalty"]))
            except Exception as e:
                print(e)
                home_penalty_score = None
                away_penalty_score = None
            finally:
                print(
                    game_id,
                    home_score,
                    away_score,
                    home_penalty_score,
                    away_penalty_score,
                )
                score_log = log_kabaddi_score(
                    game_id,
                    home_score,
                    away_score,
                    home_penalty_score,
                    away_penalty_score,
                )
                send_message(
                    "kabaddi",
                    f"{request.user.first_name} {request.user.last_name} has logged game {score_log}",
                )
                return HttpResponse("Success")
        except KeyError:
            return HttpResponse("Missing data")
        except ValueError:
            return HttpResponse("Invalid data")
        except Exception:
            raise HttpResponseServerError
    else:
        raise PermissionDenied


@login_required
def scorekabaddi(request: HttpRequest) -> HttpResponse:
    """Return the kabaddi_score.html template in template/home"""
    if request.user.is_authenticated:
        if request.method == "POST":
            logkabaddiscore(request)
            # Initialise the form again
            form = UnplayedKabaddiGamesForm()
            form.fields["game"].choices = get_unplayed_kabaddi_games()
            template: Template = loader.get_template("kabaddi_score.html")
            return HttpResponse(
                template.render(
                    context={
                        "form": form,
                        "success": True,
                        "authenticated": request.user.is_authenticated,
                    },
                    request=request,
                )
            )
        else:
            form = UnplayedKabaddiGamesForm()
            form.fields["game"].choices = get_unplayed_kabaddi_games()
            template: Template = loader.get_template("kabaddi_score.html")
            return HttpResponse(
                template.render(
                    context={
                        "form": form,
                        "success": False,
                        "authenticated": request.user.is_authenticated,
                    },
                    request=request,
                )
            )
    else:
        raise PermissionDenied


def kho(request: HttpRequest) -> HttpResponse:
    """Return the kho.html template in template/home"""

    template: Template = loader.get_template("kho.html")
    context = {
        "schedules": get_kho_schedule(),
        "group_stages": get_kho_table(),
        "authenticated": request.user.is_authenticated,
        "knockout_stages": get_kho_knockout_stages(),
    }
    return HttpResponse(template.render(context))


@login_required
def logkhoscore(request: HttpRequest) -> HttpResponse:
    """Return the kho_score.html template in template/home"""
    if request.user.is_authenticated:
        try:
            game_id = int(str(request.POST["game"]))
            home_score = int(str(request.POST["team_1_score"]))
            away_score = int(str(request.POST["team_2_score"]))
            try:
                home_penalty_score = int(str(request.POST["team_1_penalty"]))
                away_penalty_score = int(str(request.POST["team_2_penalty"]))
            except Exception as e:
                print(e)
                home_penalty_score = None
                away_penalty_score = None
            finally:
                print(
                    game_id,
                    home_score,
                    away_score,
                    home_penalty_score,
                    away_penalty_score,
                )
                score_log = log_kho_score(
                    game_id,
                    home_score,
                    away_score,
                    home_penalty_score,
                    away_penalty_score,
                )
                send_message(
                    "kho",
                    f"{request.user.first_name} {request.user.last_name} has logged game {score_log}",
                )
                return HttpResponse("Success")
        except KeyError:
            return HttpResponse("Missing data")
        except ValueError:
            return HttpResponse("Invalid data")
        except Exception:
            raise HttpResponseServerError
    else:
        raise PermissionDenied


@login_required
def scorekho(request: HttpRequest) -> HttpResponse:
    """Return the kho_score.html template in template/home"""
    if request.user.is_authenticated:
        if request.method == "POST":
            logkhoscore(request)
            # Initialise the form again
            form = UnplayedKhoGamesForm()
            form.fields["game"].choices = get_unplayed_kho_games()
            template: Template = loader.get_template("kho_score.html")
            return HttpResponse(
                template.render(
                    context={
                        "form": form,
                        "success": True,
                        "authenticated": request.user.is_authenticated,
                    },
                    request=request,
                )
            )
        else:
            form = UnplayedKhoGamesForm()
            form.fields["game"].choices = get_unplayed_kho_games()
            template: Template = loader.get_template("kho_score.html")
            return HttpResponse(
                template.render(
                    context={
                        "form": form,
                        "success": False,
                        "authenticated": request.user.is_authenticated,
                    },
                    request=request,
                )
            )
    else:
        raise PermissionDenied


def badminton(request: HttpRequest) -> HttpResponse:
    """Return the badminton.html template in template/home"""

    template: Template = loader.get_template("badminton.html")
    context = {
        "schedules": get_badminton_schedule(),
        "group_stages": get_badminton_table(),
        "authenticated": request.user.is_authenticated,
        "knockout_stages": get_badminton_knockout_stages(),
    }
    return HttpResponse(template.render(context))


@login_required
def logbadmintonscore(request: HttpRequest) -> HttpResponse:
    """Return the badminton_score.html template in template/home"""
    if request.user.is_authenticated:
        try:
            game_id = int(str(request.POST["game"]))
            home_score = int(str(request.POST["team_1_score"]))
            away_score = int(str(request.POST["team_2_score"]))
            try:
                home_penalty_score = int(str(request.POST["team_1_penalty"]))
                away_penalty_score = int(str(request.POST["team_2_penalty"]))
            except Exception as e:
                print(e)
                home_penalty_score = None
                away_penalty_score = None
            finally:
                print(
                    game_id,
                    home_score,
                    away_score,
                    home_penalty_score,
                    away_penalty_score,
                )
                score_log = log_badminton_score(
                    game_id,
                    home_score,
                    away_score,
                    home_penalty_score,
                    away_penalty_score,
                )
                send_message(
                    "badminton",
                    f"{request.user.first_name} {request.user.last_name} has logged game {score_log}",
                )
                return HttpResponse("Success")
        except KeyError:
            return HttpResponse("Missing data")
        except ValueError:
            return HttpResponse("Invalid data")
        except Exception:
            raise HttpResponseServerError
    else:
        raise PermissionDenied


@login_required
def scorebadminton(request: HttpRequest) -> HttpResponse:
    """Return the badminton_score.html template in template/home"""
    if request.user.is_authenticated:
        if request.method == "POST":
            logbadmintonscore(request)
            # Initialise the form again
            form = UnplayedBadmintonGamesForm()
            form.fields["game"].choices = get_unplayed_badminton_games()
            template: Template = loader.get_template("badminton_score.html")
            return HttpResponse(
                template.render(
                    context={
                        "form": form,
                        "success": True,
                        "authenticated": request.user.is_authenticated,
                    },
                    request=request,
                )
            )
        else:
            form = UnplayedBadmintonGamesForm()
            form.fields["game"].choices = get_unplayed_badminton_games()
            template: Template = loader.get_template("badminton_score.html")
            return HttpResponse(
                template.render(
                    context={
                        "form": form,
                        "success": False,
                        "authenticated": request.user.is_authenticated,
                    },
                    request=request,
                )
            )
    else:
        raise PermissionDenied


def loaderio(request: HttpRequest) -> HttpResponse:
    """Return the loaderio verification token"""

    return HttpResponse("loaderio-6f638dd217ebc0c6ad2e477d8e9e2e8c")
