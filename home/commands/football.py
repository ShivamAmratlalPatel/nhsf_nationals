import datetime
import random

from django import forms
from django.http import HttpResponseBadRequest, HttpResponse

from ..models import (
    FootballPitch,
    FootballSchedule,
    FootballTable,
    FootballTeam,
    FootballKnockout,
)
from django.core.exceptions import BadRequest
from django.db.models import Q

number_of_groups = 5


def generate_schedule() -> None:
    """
    Generate the football schedule.

    The schedule is generated by:
    1. Each team plays every other team in their group
    2. There should be no more than 2 games in a row for a team

    :return: None
    """
    # If schedule already exists then don't generate it
    if FootballSchedule.objects.all().exists():
        return

    # Randomly assign teams to groups
    teams = FootballTeam.objects.all().order_by("name").values("team_id")
    # shuffle the teams
    random.shuffle(list(teams))
    for i, team in enumerate(teams):
        # Assign the team to a group
        FootballTeam.objects.filter(team_id=team["team_id"]).update(
            group=i % number_of_groups + 1
        )

    teams = (
        FootballTeam.objects.all().order_by("group", "name").values("team_id",
                                                                    "group")
    )

    # Generate fixtures for each group
    for group in teams.values("group").distinct():
        group_teams = list(teams.filter(group=group["group"]))

        # Generate fixtures for each team
        for team in group_teams:
            # Generate fixtures for each opponent
            for opponent in group_teams:
                # Don't generate a fixture for the team playing themselves
                if team["team_id"] != opponent["team_id"]:
                    # If the fixture doesn't already exist create it
                    if not FootballSchedule.objects.filter(
                            Q(team_id=team["team_id"]) & Q(
                                opponent_id=opponent["team_id"])
                    ).exists():
                        # If the fixture doesn't already exist the other way around
                        # create it
                        if not FootballSchedule.objects.filter(
                                Q(team_id=opponent["team_id"])
                                & Q(opponent_id=team["team_id"])
                        ).exists():
                            FootballSchedule.objects.update_or_create(
                                team_id=team["team_id"],
                                opponent_id=opponent["team_id"]
                            )

    # Assign group number as pitch number for each fixture and assign a random time
    # If there is no pitch for the group then assign a random pitch
    pitches = FootballPitch.objects.all().order_by("name")
    pitches_count = pitches.count()
    print("pitches_count: ", pitches_count)
    fixtures = (
        FootballSchedule.objects.filter(played=False)
            .values("schedule_id", "team_id", "opponent_id", "team__group")
    )

    group_4_or_5_games = list(fixtures.filter(team__group__in=[4, 5]))

    for i, group in enumerate(
            fixtures.order_by("team__group").values("team__group").distinct()):
        group_fixtures = list(
            fixtures.filter(team__group=group["team__group"]))
        random.shuffle(group_fixtures)
        pitch = i % pitches_count + 1
        print("pitch: ", pitch, "group: ", group["team__group"])
        if pitch == 0 or pitch > pitches_count or i >= 2:
            pitch = random.randint(1, pitches_count)
        #     For the first game in the group_fixtures, set the time = 0, update it in db and pop it from the list
        FootballSchedule.objects.filter(
            schedule_id=group_fixtures[0]["schedule_id"]).update(
            time="00:00:00",
            pitch_id=pitch)
        group_fixtures.pop(0)
        while len(group_fixtures) > 0:
            last_game = FootballSchedule.objects.filter(
                team__group=group["team__group"], time__isnull=False).order_by(
                "time").values(
                "time", "team_id", "opponent_id").last()
            condition_hit = False
            for fixture in group_fixtures:
                if i >= 2:
                    pitch = random.randint(1, pitches_count)
                last_teams = [last_game["team_id"], last_game["opponent_id"]]
                if (fixture["team_id"] not in last_teams) and (
                        fixture["opponent_id"] not in last_teams):
                    FootballSchedule.objects.filter(
                        schedule_id=fixture["schedule_id"]).update(
                        time=(datetime.datetime.combine(datetime.date.today(),
                                                        last_game[
                                                            "time"]) + datetime.timedelta(
                            minutes=30)).time(), pitch_id=pitch)
                    group_fixtures.pop(group_fixtures.index(fixture))
                    condition_hit = True
                    continue
            if not condition_hit:
                pitch = random.randint(1, pitches_count)
                print("condition not hit", pitch)
                try:
                    FootballSchedule.objects.filter(
                        schedule_id=group_4_or_5_games[0][
                            "schedule_id"]).update(
                        time=(datetime.datetime.combine(datetime.date.today(),
                                                        last_game[
                                                            "time"]) + datetime.timedelta(
                            minutes=30)).time(), pitch_id=pitch)
                    group_4_or_5_games.pop(0)
                except IndexError:
                    FootballSchedule.objects.filter(
                        schedule_id=group_fixtures[0]["schedule_id"]).update(
                        time=(datetime.datetime.combine(datetime.date.today(),
                                                        last_game[
                                                            "time"]) + datetime.timedelta(
                            minutes=30)).time(), pitch_id=pitch)
                    group_fixtures.pop(0)
    # Find the latest game from the db in that group
    # Find the next game in the group_fixtures where the team or opponents is not in the game before
    # Set the time = time of the last game + 1, update it in db and pop it from the list
    # Repeat until all games in the group_fixtures are updated
    # If there are no more games in the group_fixtures, then find the next game in the group_fixtures where the team or opponents is not in the game before
    # Set first game in the group fixtures to time of the last game + 1, update it in db and pop it from the list


def initalise_football_table() -> None:
    """Initalise the football table"""

    current_table = FootballTable.objects.all()

    teams = FootballTeam.objects.all().values("team_id")

    for team in teams:
        if not current_table.filter(team_id=team["team_id"]).exists():
            FootballTable.objects.update_or_create(
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


def get_football_schedule() -> dict:
    """Return a dict of football schedules by pitches"""

    # If schedule is empty, initalise it
    if not FootballSchedule.objects.all().exists():
        generate_schedule()

    initalise_football_table()

    schedule = (
        FootballSchedule.objects.select_related("pitch")
            .all()
            .order_by("time")
            .values(
            "pitch_id__name",
            "team__name",
            "opponent__name",
            "team_score",
            "opponent_score",
            "time",
            "played",
        )
    )
    pitches = FootballPitch.objects.all().values("name")
    output = {pitch["name"]: [] for pitch in pitches}

    [
        output[game["pitch_id__name"]].append(
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


def get_football_table() -> dict:
    """Return a dict of football table"""

    table = (
        FootballTable.objects.all()
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

    groups = FootballTeam.objects.all().values("group").distinct().order_by(
        "group")

    output = {group["group"]: [] for group in groups}

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

    team_results = (
        FootballSchedule.objects.filter(
            Q(team_id=team_id) | Q(opponent_id=team_id))
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

    FootballTable.objects.update_or_create(
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


def get_unplayed_football_games() -> list:
    """Return a list of unplayed football games with the format [(schedule_id, game)]"""

    games = (
        FootballSchedule.objects.filter(played=False)
            .order_by("pitch_id__name", "time")
            .values("schedule_id", "team__name", "opponent__name",
                    "pitch_id__name")
    )

    output = [
        (
            game["schedule_id"],
            f"{game['pitch_id__name']}: {game['team__name']} vs {game['opponent__name']}",
        )
        for game in games
    ]

    knockout_games = (
        FootballKnockout.objects.filter(played=False)
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


class UnplayedFootballGamesForm(forms.Form):
    """Form to validate unplayed games"""

    choices = get_unplayed_football_games()
    game = forms.ChoiceField(label="Game", choices=choices)
    team_1_score = forms.IntegerField(label="Team 1 Goals", min_value=0)
    team_2_score = forms.IntegerField(label="Team 2 Goals", min_value=0)
    team_1_penalty = forms.IntegerField(
        label="Team 1 Penalties", min_value=0, required=False
    )
    team_2_penalty = forms.IntegerField(
        label="Team 2 Penalties", min_value=0, required=False
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

    if FootballKnockout.objects.exists():
        return

    if FootballSchedule.objects.filter(played=False).exists():
        return

    # Get top team from each group
    top_teams = (
        FootballTable.objects.all()
            .order_by("-points_per_game", "-goal_difference", "-goals_for")
            .values("team_id", "team_id__group")
    )

    knockout_teams = []
    # Get the top team from each group
    for group in range(1, number_of_groups + 1):
        top_team = top_teams.filter(team_id__group=group).first()
        knockout_teams.append(top_team["team_id"])

    # Get the next best teams from any league based on highest average
    # points per game played until there are 8 teams
    while len(knockout_teams) < 8:
        next_best_team = (
            FootballTable.objects.exclude(team_id__in=knockout_teams)
                .order_by("-points_per_game", "-goal_difference", "-goals_for")
                .values("team_id")
                .first()
        )
        knockout_teams.append(next_best_team["team_id"])

    # Order these teams based on average points per games
    knockout_teams = (
        FootballTable.objects.filter(team_id__in=knockout_teams)
            .order_by("-points_per_game", "-goal_difference", "-goals_for")
            .values("team_id")
    )

    # Create the knockout table
    # Quarter Final 1
    FootballKnockout.objects.create(
        team_id=knockout_teams[0]["team_id"],
        opponent_id=knockout_teams[7]["team_id"],
        played=False,
        step_id=1,
        pitch_id=1,
    )
    # Quarter Final 4
    FootballKnockout.objects.create(
        team_id=knockout_teams[1]["team_id"],
        opponent_id=knockout_teams[6]["team_id"],
        played=False,
        step_id=4,
        pitch_id=2,
    )
    # Quarter Final 3
    FootballKnockout.objects.create(
        team_id=knockout_teams[2]["team_id"],
        opponent_id=knockout_teams[5]["team_id"],
        played=False,
        step_id=3,
        pitch_id=3,
    )
    # Quarter Final 2
    FootballKnockout.objects.create(
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

    if FootballKnockout.objects.exists():
        if FootballKnockout.objects.filter(step_id=1, played=False).exists():
            return
        elif FootballKnockout.objects.filter(step_id=2, played=False).exists():
            return
        else:
            if not FootballKnockout.objects.filter(step_id=5).exists():
                # Get the winners of QF1 and QF2
                qf1 = FootballKnockout.objects.get(step_id=1)
                qf2 = FootballKnockout.objects.get(step_id=2)

                # Create SF1
                FootballKnockout.objects.create(
                    team_id=qf1.winner,
                    opponent_id=qf2.winner,
                    played=False,
                    step_id=5,
                    pitch_id=2,
                )

        if FootballKnockout.objects.filter(step_id=3, played=False).exists():
            return
        elif FootballKnockout.objects.filter(step_id=4, played=False).exists():
            return
        else:
            if not FootballKnockout.objects.filter(step_id=6).exists():
                # Get the winners of QF3 and QF4
                qf3: FootballKnockout = FootballKnockout.objects.get(step_id=3)
                qf4: FootballKnockout = FootballKnockout.objects.get(step_id=4)

                # Create SF2
                FootballKnockout.objects.create(
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
            FootballKnockout.objects.filter(step_id=5).exists()
            or FootballKnockout.objects.filter(step_id=6).exists()
    ):
        if FootballKnockout.objects.filter(step_id=5, played=False).exists():
            return
        elif FootballKnockout.objects.filter(step_id=6, played=False).exists():
            return
        else:
            if not FootballKnockout.objects.filter(step_id=7).exists():
                # Get the winners of SF1 and SF2
                sf1: FootballKnockout = FootballKnockout.objects.get(step_id=5)
                sf2: FootballKnockout = FootballKnockout.objects.get(step_id=6)

                # Create the final
                FootballKnockout.objects.create(
                    team_id=sf1.winner,
                    opponent_id=sf2.winner,
                    played=False,
                    step_id=7,
                    pitch_id=3,
                )

        return


def log_football_score(
        schedule_id: int,
        home_score: int,
        away_score: int,
        home_penalties: int,
        away_penalties: int,
) -> str:
    """Log a football score"""

    if home_score == away_score and home_score == 1000:
        # Delete all rows in schedule table
        FootballSchedule.objects.all().delete()
        # Delete all rows in knockout table
        FootballKnockout.objects.all().delete()

    if not schedule_id and schedule_id != 0:
        raise BadRequest("Schedule ID is required")

    if not away_score and home_score != 0:
        raise BadRequest("Home score is required")

    if not away_score and away_score != 0:
        raise BadRequest("Away score is required")

    if FootballSchedule.objects.filter(played=False).exists():
        FootballSchedule.objects.filter(schedule_id=schedule_id).update(
            team_score=home_score, opponent_score=away_score, played=True
        )

        update_football_table(
            FootballSchedule.objects.get(schedule_id=schedule_id).team_id
        )
        update_football_table(
            FootballSchedule.objects.get(schedule_id=schedule_id).opponent_id
        )

        generate_quarter_final()
        game = FootballSchedule.objects.get(schedule_id=schedule_id)
        message = f"{game.team.name} vs {game.opponent.name} with a score of {home_score} - {away_score}"
        return message
    else:
        print(home_score, away_score, home_penalties, away_penalties)
        if home_score == away_score:
            if home_penalties is None or away_penalties is None:
                print("Penalties are required")
                return HttpResponseBadRequest("Penalties are required")
            if not home_penalties and not away_penalties:
                return HttpResponseBadRequest()
            elif home_penalties == away_penalties:
                return HttpResponseBadRequest()
        FootballKnockout.objects.filter(id=schedule_id).update(
            team_score=home_score,
            opponent_score=away_score,
            team_penalty=home_penalties,
            opponent_penalty=away_penalties,
            played=True,
        )

        generate_semi_final()
        generate_final()
        game = FootballKnockout.objects.get(id=schedule_id)
        message = f"{game.team.name} vs {game.opponent.name} score is {home_score} - {away_score}"
        if home_penalties and away_penalties:
            message += f" with penalties of {home_penalties} - {away_penalties}"
        return message


def get_football_knockout_stages() -> dict:
    """
    Get the knockout stages.


    :return: dict
    """

    knockout_stages = {}
    if FootballKnockout.objects.filter(step_id=1).exists():
        knockout_stages["Quarter Final 1"] = {
            "team": FootballKnockout.objects.get(step_id=1).team.name,
            "opponent": FootballKnockout.objects.get(step_id=1).opponent.name,
            "result": FootballKnockout.objects.get(step_id=1).get_result,
            "played": FootballKnockout.objects.get(step_id=1).played,
        }
    if FootballKnockout.objects.filter(step_id=2).exists():
        knockout_stages["Quarter Final 2"] = {
            "team": FootballKnockout.objects.get(step_id=2).team.name,
            "opponent": FootballKnockout.objects.get(step_id=2).opponent.name,
            "result": FootballKnockout.objects.get(step_id=2).get_result,
            "played": FootballKnockout.objects.get(step_id=2).played,
        }
    if FootballKnockout.objects.filter(step_id=3).exists():
        knockout_stages["Quarter Final 3"] = {
            "team": FootballKnockout.objects.get(step_id=3).team.name,
            "opponent": FootballKnockout.objects.get(step_id=3).opponent.name,
            "result": FootballKnockout.objects.get(step_id=3).get_result,
            "played": FootballKnockout.objects.get(step_id=3).played,
        }
    if FootballKnockout.objects.filter(step_id=4).exists():
        knockout_stages["Quarter Final 4"] = {
            "team": FootballKnockout.objects.get(step_id=4).team.name,
            "opponent": FootballKnockout.objects.get(step_id=4).opponent.name,
            "result": FootballKnockout.objects.get(step_id=4).get_result,
            "played": FootballKnockout.objects.get(step_id=4).played,
        }
    if FootballKnockout.objects.filter(step_id=5).exists():
        knockout_stages["Semi Final 1"] = {
            "team": FootballKnockout.objects.get(step_id=5).team.name,
            "opponent": FootballKnockout.objects.get(step_id=5).opponent.name,
            "result": FootballKnockout.objects.get(step_id=5).get_result,
            "played": FootballKnockout.objects.get(step_id=5).played,
        }
    if FootballKnockout.objects.filter(step_id=6).exists():
        knockout_stages["Semi Final 2"] = {
            "team": FootballKnockout.objects.get(step_id=6).team.name,
            "opponent": FootballKnockout.objects.get(step_id=6).opponent.name,
            "result": FootballKnockout.objects.get(step_id=6).get_result,
            "played": FootballKnockout.objects.get(step_id=6).played,
        }
    if FootballKnockout.objects.filter(step_id=7).exists():
        knockout_stages["Final"] = {
            "team": FootballKnockout.objects.get(step_id=7).team.name,
            "opponent": FootballKnockout.objects.get(step_id=7).opponent.name,
            "result": FootballKnockout.objects.get(step_id=7).get_result,
            "played": FootballKnockout.objects.get(step_id=7).played,
        }
    return knockout_stages
