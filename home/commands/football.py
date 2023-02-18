from django import forms

from ..models import FootballPitch, FootballSchedule, FootballTable, \
    FootballTeam
from django.core.exceptions import BadRequest
from django.db.models import Q


def get_football_schedule() -> dict:
    """Return a dict of football schedules by pitches"""

    schedule = FootballSchedule.objects.select_related(
        "pitch_id").all().order_by(
        "time").values("pitch_id__name", "team__name", "opponent__name",
                       "team_score", "opponent_score", "time", "played")
    pitches = FootballPitch.objects.all().values("name")
    output = {pitch["name"]: [] for pitch in pitches}

    [output[game["pitch_id__name"]].append(
        {"game": f"{game['team__name']} vs {game['opponent__name']}",
         "time": game["time"].strftime("%H:%M"),
         "result": f"{game['team_score']} - {game['opponent_score']}",
         "played": game["played"]})
        for game in
        schedule]

    return output


def get_football_table() -> dict:
    """Return a dict of football table"""

    table = FootballTable.objects.all().select_related(
        "team_id").order_by("-points", "-goal_difference",
                            "-goals_for",
                            "-played").values("team_id__name",
                                              "team_id__group", "played",
                                              "won",
                                              "drawn", "lost",
                                              "goals_for", "goals_against",
                                              "goal_difference",
                                              "points")

    groups = FootballTeam.objects.all().values("group").distinct().order_by(
        "group")

    output = {group["group"]: [] for group in groups}

    [output[team["team_id__group"]].append(
        {"team": team["team_id__name"],
         "played": team["played"],
         "won": team["won"],
         "drawn": team["drawn"],
         "lost": team["lost"],
         "goals_for": team["goals_for"],
         "goals_against": team["goals_against"],
         "goal_difference": team["goal_difference"],
         "points": team["points"]})
        for team in table]

    return output


def initalise_football_table() -> None:
    """Initalise the football table"""

    current_table = FootballTable.objects.all()

    teams = FootballTeam.objects.all().values("team_id")

    for team in teams:
        if not current_table.filter(team_id=team["team_id"]).exists():
            FootballTable.objects.update_or_create(team_id_id=team["team_id"],
                                                   played=0,
                                                   won=0,
                                                   drawn=0,
                                                   lost=0,
                                                   goals_for=0,
                                                   goals_against=0,
                                                   goal_difference=0,
                                                   points=0)


def update_football_table(team_id: int) -> None:
    """
    Update the football table.

    :param team_id: The team ID to update the table for
    :return: The updated football table
    """
    if not team_id:
        raise BadRequest("Team ID is required")

    # If team id is not in table then initialise table
    if not FootballTable.objects.filter(team_id=team_id).exists():
        initalise_football_table()

    team_results = FootballSchedule.objects.filter(
        Q(team_id=team_id) | Q(opponent_id=team_id)).filter(
        played=True).values("team_id",
                            "opponent_id",
                            "team_score",
                            "opponent_score")

    games_played = len(team_results)
    games_won = 0
    games_drawn = 0
    games_lost = 0
    goals_for = 0
    goals_against = 0

    for result in team_results:
        if result["team_id"] == team_id:
            goals_for += result["team_score"]
            goals_against += result["opponent_score"]
            if result["team_score"] > result["opponent_score"]:
                games_won += 1
            elif result["team_score"] < result["opponent_score"]:
                games_lost += 1
            else:
                games_drawn += 1
        else:
            goals_for += result["opponent_score"]
            goals_against += result["team_score"]
            if result["team_score"] < result["opponent_score"]:
                games_won += 1
            elif result["team_score"] > result["opponent_score"]:
                games_lost += 1
            else:
                games_drawn += 1

    goal_difference = goals_for - goals_against
    points = games_won * 3 + games_drawn

    FootballTable.objects.update_or_create(team_id=team_id,
                                           defaults={"played": games_played,
                                                     "won": games_won,
                                                     "drawn": games_drawn,
                                                     "lost": games_lost,
                                                     "goals_for": goals_for,
                                                     "goals_against":
                                                         goals_against,
                                                     "goal_difference":
                                                         goal_difference,
                                                     "points": points})

    return


def get_unplayed_football_games() -> list:
    """Return a list of unplayed football games with the format [(schedule_id, game)]"""

    games = FootballSchedule.objects.filter(played=False).order_by("pitch_id",
                                                                   "time").values(
        "schedule_id",
        "team__name",
        "opponent__name",
        "pitch_id__name")

    return [(game["schedule_id"],
             f"{game['pitch_id__name']}: {game['team__name']} vs {game['opponent__name']}")
            for
            game in games]


class UnplayedGamesForm(forms.Form):
    """Form to validate unplayed games"""
    choices = get_unplayed_football_games()
    game = forms.ChoiceField(label="Game", choices=choices)
    team_1_score = forms.IntegerField(label="Team 1 Score")
    team_2_score = forms.IntegerField(label="Team 2 Score")


def log_football_score(schedule_id: int, home_score: int,
                       away_score: int) -> None:
    """Log a football score"""

    if not schedule_id:
        raise BadRequest("Schedule ID is required")

    if not home_score:
        raise BadRequest("Home score is required")

    if not away_score:
        raise BadRequest("Away score is required")

    FootballSchedule.objects.filter(schedule_id=schedule_id).update(
        team_score=home_score,
        opponent_score=away_score,
        played=True)

    update_football_table(FootballSchedule.objects.get(
        schedule_id=schedule_id).team_id)
    update_football_table(FootballSchedule.objects.get(
        schedule_id=schedule_id).opponent_id)

    return
