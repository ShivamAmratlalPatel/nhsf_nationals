import random

from django import forms

from ..models import (
    KabaddiPitch,
    KabaddiSchedule,
    KabaddiTable,
    KabaddiTeam,
    KabaddiKnockout,
)
from django.core.exceptions import BadRequest
from django.db.models import Q

number_of_groups = 2


def randomise_teams() -> None:
    """Randomise the team names"""
    if not KabaddiTable.objects.all().exists():
        names = list(KabaddiTeam.objects.all().values("name"))
        random.shuffle(names)
        for i, name in enumerate(names):
            KabaddiTeam.objects.filter(team_id=i + 1).update(
                name=name["name"])


def initalise_kabaddi_table() -> None:
    """Initalise the kabaddi table"""

    current_table = KabaddiTable.objects.all()

    teams = KabaddiTeam.objects.all().values("team_id")

    for team in teams:
        if not current_table.filter(team_id=team["team_id"]).exists():
            KabaddiTable.objects.update_or_create(
                team_id_id=team["team_id"],
                played=0,
                won=0,
                drawn=0,
                lost=0,
                goals_for=0,
                goals_against=0,
                goal_difference=0,
                points=0,
                points_per_game=0,
            )


def get_kabaddi_schedule() -> dict:
    """Return a dict of kabaddi schedules by pitches"""

    randomise_teams()
    initalise_kabaddi_table()

    schedule = (
        KabaddiSchedule.objects.select_related("pitch")
        .all()
        .order_by("time")
        .values(
            "pitch__name",
            "team__name",
            "opponent__name",
            "team_score",
            "opponent_score",
            "time",
            "played",
        )
    )
    pitches = KabaddiPitch.objects.all().values("name")
    output = {pitch["name"]: [] for pitch in pitches}

    [
        output[game["pitch__name"]].append(
            {
                "game": f"{game['team__name']} vs {game['opponent__name']}",
                "time": game["time"].strftime("%H:%M"),
                "result": f"{game['team_score']} - {game['opponent_score']}",
                "played": game["played"],
            }
        )
        for game in schedule
    ]

    return output


def get_kabaddi_table() -> dict:
    """Return a dict of kabaddi table"""

    table = (
        KabaddiTable.objects.all()
        .select_related("team_id")
        .order_by("-points", "-goal_difference", "-goals_for", "-played")
        .values(
            "team_id__name",
            "team_id__group",
            "played",
            "won",
            "drawn",
            "lost",
            "goals_for",
            "goals_against",
            "goal_difference",
            "points",
        )
    )

    groups = KabaddiTeam.objects.all().values("group").distinct().order_by("group")

    output: dict = {group["group"]: [] for group in groups}

    [
        output[team["team_id__group"]].append(
            {
                "team": team["team_id__name"],
                "played": team["played"],
                "won": team["won"],
                "drawn": team["drawn"],
                "lost": team["lost"],
                "goals_for": team["goals_for"],
                "goals_against": team["goals_against"],
                "goal_difference": team["goal_difference"],
                "points": team["points"],
            }
        )
        for team in table
    ]

    return output


def update_kabaddi_table(team_id: int) -> None:
    """
    Update the kabaddi table.

    :param team_id: The team ID to update the table for
    :return: The updated kabaddi table
    """
    if not team_id:
        raise BadRequest("Team ID is required")

    # If team id is not in table then initialise table
    if not KabaddiTable.objects.filter(team_id=team_id).exists():
        initalise_kabaddi_table()

    team_results = (
        KabaddiSchedule.objects.filter(Q(team_id=team_id) | Q(opponent_id=team_id))
        .filter(played=True)
        .values("team_id", "opponent_id", "team_score", "opponent_score")
    )

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

    KabaddiTable.objects.update_or_create(
        team_id=team_id,
        defaults={
            "played": games_played,
            "won": games_won,
            "drawn": games_drawn,
            "lost": games_lost,
            "goals_for": goals_for,
            "goals_against": goals_against,
            "goal_difference": goal_difference,
            "points": points,
            "points_per_game": points / games_played if games_played else 0,
        },
    )

    return


def get_unplayed_kabaddi_games() -> list:
    """Return a list of unplayed kabaddi games with the format [(schedule_id, game)]"""

    games = (
        KabaddiSchedule.objects.filter(played=False)
        .order_by("pitch_id__name", "time")
        .values("schedule_id", "team__name", "opponent__name", "pitch_id__name")
    )

    output = [
        (
            game["schedule_id"],
            f"{game['pitch_id__name']}: {game['team__name']} vs {game['opponent__name']}",
        )
        for game in games
    ]

    knockout_games = (
        KabaddiKnockout.objects.filter(played=False)
        .order_by("step_id")
        .values("id", "team__name", "opponent__name", "step__name")
    )

    [
        output.append(
            (
                game["id"],
                f"{game['step__name']}: {game['team__name']} vs {game['opponent__name']}",
            )
        )
        for game in knockout_games
    ]

    return output


class UnplayedKabaddiGamesForm(forms.Form):
    """Form to validate unplayed games"""

    choices = get_unplayed_kabaddi_games()
    game = forms.ChoiceField(label="Game", choices=choices)
    team_1_score = forms.IntegerField(label="Team 1 Goals", min_value=0)
    team_2_score = forms.IntegerField(label="Team 2 Goals", min_value=0)
    team_1_penalty = forms.IntegerField(
        label="Team 1 Penalties", required=False, min_value=0
    )
    team_2_penalty = forms.IntegerField(
        label="Team 2 Penalties", required=False, min_value=0
    )


def generate_quarter_final() -> None:
    """
    Generate the knockout teams.

    If the knockout table already exists it should not generate it.

    If the group stages have not all finished it should not generate it.

    It should pick the top team from each league and then pick the next best teams
    from any league based on highest average points per game played until there are 8
    teams. It should then order these teams based on average points per games and then
    top team should play worst team and so on.

    :return: None
    """

    if KabaddiKnockout.objects.exists():
        return

    if KabaddiSchedule.objects.filter(played=False).exists():
        return

    # Get top team from each group
    top_teams = (
        KabaddiTable.objects.all()
        .order_by("-points_per_game", "-goal_difference", "-goals_for")
        .values("team_id", "team_id__group")
    )

    knockout_teams = []
    # Get the top team from each group
    for group in range(1, number_of_groups):
        top_team = top_teams.filter(team_id__group=group).first()
        knockout_teams.append(top_team["team_id"])

    # Get the next best teams from any league based on highest average
    # points per game played until there are 8 teams
    while len(knockout_teams) < 8:
        next_best_team = (
            KabaddiTable.objects.exclude(team_id__in=knockout_teams)
            .order_by("-points_per_game", "-goal_difference", "-goals_for")
            .values("team_id")
            .first()
        )
        knockout_teams.append(next_best_team["team_id"])

    # Order these teams based on average points per games
    knockout_teams = (
        KabaddiTable.objects.filter(team_id__in=knockout_teams)
        .order_by("-points_per_game", "-goal_difference", "-goals_for")
        .values("team_id")
    )

    # Create the knockout table
    # Quarter Final 1
    KabaddiKnockout.objects.create(
        team_id=knockout_teams[0]["team_id"],
        opponent_id=knockout_teams[7]["team_id"],
        played=False,
        step_id=1,
        pitch_id=1,
    )
    # Quarter Final 4
    KabaddiKnockout.objects.create(
        team_id=knockout_teams[1]["team_id"],
        opponent_id=knockout_teams[6]["team_id"],
        played=False,
        step_id=4,
        pitch_id=2,
    )
    # Quarter Final 3
    KabaddiKnockout.objects.create(
        team_id=knockout_teams[2]["team_id"],
        opponent_id=knockout_teams[5]["team_id"],
        played=False,
        step_id=3,
        pitch_id=3,
    )
    # Quarter Final 2
    KabaddiKnockout.objects.create(
        team_id=knockout_teams[3]["team_id"],
        opponent_id=knockout_teams[4]["team_id"],
        played=False,
        step_id=2,
        pitch_id=1,
    )
    return


def generate_semi_final() -> None:
    """
    Generate the semi-final teams.

    If QF1 and QF2 have not been played it should not generate SF1.

    If QF3 and QF4 have not been played it should not generate SF3.
    """

    if KabaddiKnockout.objects.exists():
        if KabaddiKnockout.objects.filter(step_id=1, played=False).exists():
            return
        elif KabaddiKnockout.objects.filter(step_id=2, played=False).exists():
            return
        else:
            if not KabaddiKnockout.objects.filter(step_id=5).exists():
                # Get the winners of QF1 and QF2
                qf1 = KabaddiKnockout.objects.get(step_id=1)
                qf2 = KabaddiKnockout.objects.get(step_id=2)

                # Create SF1
                KabaddiKnockout.objects.create(
                    team_id=qf1.winner,
                    opponent_id=qf2.winner,
                    played=False,
                    step_id=5,
                    pitch_id=2,
                )

        if KabaddiKnockout.objects.filter(step_id=3, played=False).exists():
            return
        elif KabaddiKnockout.objects.filter(step_id=4, played=False).exists():
            return
        else:
            if not KabaddiKnockout.objects.filter(step_id=6).exists():
                # Get the winners of QF3 and QF4
                qf3: KabaddiKnockout = KabaddiKnockout.objects.get(step_id=3)
                qf4: KabaddiKnockout = KabaddiKnockout.objects.get(step_id=4)

                # Create SF2
                KabaddiKnockout.objects.create(
                    team_id=qf3.winner,
                    opponent_id=qf4.winner,
                    played=False,
                    step_id=6,
                    pitch_id=2,
                )

        return


def generate_final() -> None:
    """
    Generate the final teams.

    If SF1 and SF2 have not been played it should not generate the final.
    """

    if (
        KabaddiKnockout.objects.filter(step_id=5).exists()
        or KabaddiKnockout.objects.filter(step_id=6).exists()
    ):
        if KabaddiKnockout.objects.filter(step_id=5, played=False).exists():
            return
        elif KabaddiKnockout.objects.filter(step_id=6, played=False).exists():
            return
        else:
            if not KabaddiKnockout.objects.filter(step_id=7).exists():
                # Get the winners of SF1 and SF2
                sf1: KabaddiKnockout = KabaddiKnockout.objects.get(step_id=5)
                sf2: KabaddiKnockout = KabaddiKnockout.objects.get(step_id=6)

                # Create the final
                KabaddiKnockout.objects.create(
                    team_id=sf1.winner,
                    opponent_id=sf2.winner,
                    played=False,
                    step_id=7,
                    pitch_id=3,
                )

        return


def log_kabaddi_score(
    schedule_id: int,
    home_score: int,
    away_score: int,
    home_penalties: int,
    away_penalties: int,
) -> str:
    """Log a kabaddi score"""

    if not schedule_id and schedule_id != 0:
        raise BadRequest("Schedule ID is required")

    if not away_score and home_score != 0:
        raise BadRequest("Home score is required")

    if not away_score and away_score != 0:
        raise BadRequest("Away score is required")

    if KabaddiSchedule.objects.filter(played=False).exists():
        KabaddiSchedule.objects.filter(schedule_id=schedule_id).update(
            team_score=home_score, opponent_score=away_score, played=True
        )

        update_kabaddi_table(
            KabaddiSchedule.objects.get(schedule_id=schedule_id).team_id
        )
        update_kabaddi_table(
            KabaddiSchedule.objects.get(schedule_id=schedule_id).opponent_id
        )

        generate_quarter_final()
        game = KabaddiSchedule.objects.get(schedule_id=schedule_id)
        message = f"{game.team.name} vs {game.opponent.name} with a score of {home_score} - {away_score}"
        return message
    else:
        if home_score == away_score:
            if home_penalties is None or away_penalties is None:
                raise BadRequest("Penalties are required")
            if not home_penalties and not away_penalties:
                raise BadRequest("Penalties are required")
            elif home_penalties == away_penalties:
                raise BadRequest("Penalties cannot be equal")
        KabaddiKnockout.objects.filter(id=schedule_id).update(
            team_score=home_score,
            opponent_score=away_score,
            team_penalty=home_penalties,
            opponent_penalty=away_penalties,
            played=True,
        )

        generate_semi_final()
        generate_final()
        game = KabaddiKnockout.objects.get(id=schedule_id)
        message = f"{game.team.name} vs {game.opponent.name} score is {home_score} - {away_score}"
        if home_penalties and away_penalties:
            message += f" with penalties of {home_penalties} - {away_penalties}"
        return message


def get_kabaddi_knockout_stages() -> dict:
    """
    Get the knockout stages.


    :return: dict
    """

    knockout_stages = {}
    if KabaddiKnockout.objects.filter(step_id=1).exists():
        knockout_stages["Quarter Final 1"] = {
            "team": KabaddiKnockout.objects.get(step_id=1).team.name,
            "opponent": KabaddiKnockout.objects.get(step_id=1).opponent.name,
            "result": KabaddiKnockout.objects.get(step_id=1).get_result,
            "played": KabaddiKnockout.objects.get(step_id=1).played,
        }
    if KabaddiKnockout.objects.filter(step_id=2).exists():
        knockout_stages["Quarter Final 2"] = {
            "team": KabaddiKnockout.objects.get(step_id=2).team.name,
            "opponent": KabaddiKnockout.objects.get(step_id=2).opponent.name,
            "result": KabaddiKnockout.objects.get(step_id=2).get_result,
            "played": KabaddiKnockout.objects.get(step_id=2).played,
        }
    if KabaddiKnockout.objects.filter(step_id=3).exists():
        knockout_stages["Quarter Final 3"] = {
            "team": KabaddiKnockout.objects.get(step_id=3).team.name,
            "opponent": KabaddiKnockout.objects.get(step_id=3).opponent.name,
            "result": KabaddiKnockout.objects.get(step_id=3).get_result,
            "played": KabaddiKnockout.objects.get(step_id=3).played,
        }
    if KabaddiKnockout.objects.filter(step_id=4).exists():
        knockout_stages["Quarter Final 4"] = {
            "team": KabaddiKnockout.objects.get(step_id=4).team.name,
            "opponent": KabaddiKnockout.objects.get(step_id=4).opponent.name,
            "result": KabaddiKnockout.objects.get(step_id=4).get_result,
            "played": KabaddiKnockout.objects.get(step_id=4).played,
        }
    if KabaddiKnockout.objects.filter(step_id=5).exists():
        knockout_stages["Semi Final 1"] = {
            "team": KabaddiKnockout.objects.get(step_id=5).team.name,
            "opponent": KabaddiKnockout.objects.get(step_id=5).opponent.name,
            "result": KabaddiKnockout.objects.get(step_id=5).get_result,
            "played": KabaddiKnockout.objects.get(step_id=5).played,
        }
    if KabaddiKnockout.objects.filter(step_id=6).exists():
        knockout_stages["Semi Final 2"] = {
            "team": KabaddiKnockout.objects.get(step_id=6).team.name,
            "opponent": KabaddiKnockout.objects.get(step_id=6).opponent.name,
            "result": KabaddiKnockout.objects.get(step_id=6).get_result,
            "played": KabaddiKnockout.objects.get(step_id=6).played,
        }
    if KabaddiKnockout.objects.filter(step_id=7).exists():
        knockout_stages["Final"] = {
            "team": KabaddiKnockout.objects.get(step_id=7).team.name,
            "opponent": KabaddiKnockout.objects.get(step_id=7).opponent.name,
            "result": KabaddiKnockout.objects.get(step_id=7).get_result,
            "played": KabaddiKnockout.objects.get(step_id=7).played,
        }
    return knockout_stages
