from django.db import models


# Create your models here.


class Sport(models.Model):
    sport_id = models.AutoField(primary_key=True, db_index=True)
    name = models.CharField(max_length=200)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Chapter(models.Model):
    chapter_id = models.AutoField(primary_key=True, db_index=True)
    name = models.CharField(max_length=200)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class KnockoutStep(models.Model):
    id = models.AutoField(primary_key=True, db_index=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class FootballTeam(models.Model):
    team_id = models.AutoField(primary_key=True, db_index=True)
    name = models.CharField(max_length=200)
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE)
    group = models.IntegerField()
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class FootballPitch(models.Model):
    pitch_id = models.AutoField(primary_key=True, db_index=True)
    name = models.CharField(max_length=200)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class FootballSchedule(models.Model):
    schedule_id = models.AutoField(primary_key=True, db_index=True)
    team = models.ForeignKey(FootballTeam, on_delete=models.CASCADE,
                             related_name="team")
    opponent = models.ForeignKey(FootballTeam, on_delete=models.CASCADE,
                                 related_name="opponent", null=True)
    team_score = models.IntegerField(null=True)
    opponent_score = models.IntegerField(null=True)
    played = models.BooleanField(default=False)
    time = models.TimeField(null=True)
    pitch = models.ForeignKey(FootballPitch, on_delete=models.CASCADE,
                              null=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.team.name} vs {self.opponent.name}"

    @property
    def get_pitch(self):
        return self.pitch.name

    @property
    def get_time(self):
        return self.time.strftime("%H:%M")

    @property
    def get_team(self):
        return self.team.name

    @property
    def get_opponent(self):
        return self.opponent.name

    @property
    def get_result(self):
        if self.team_score is None or self.opponent_score is None:
            return False
        else:
            return f"{self.team_score} - {self.opponent_score}"


class FootballTable(models.Model):
    id = models.AutoField(primary_key=True, db_index=True)
    team_id = models.ForeignKey(FootballTeam, on_delete=models.CASCADE)
    played = models.IntegerField()
    won = models.IntegerField()
    drawn = models.IntegerField()
    lost = models.IntegerField()
    goals_for = models.IntegerField()
    goals_against = models.IntegerField()
    goal_difference = models.IntegerField()
    points = models.IntegerField()
    points_per_game = models.DecimalField(max_digits=7, decimal_places=4)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.team_id.name


class FootballKnockout(models.Model):
    id = models.AutoField(primary_key=True, db_index=True)
    team = models.ForeignKey(FootballTeam, on_delete=models.CASCADE)
    opponent = models.ForeignKey(FootballTeam, on_delete=models.CASCADE,
                                 related_name="opponent_id")
    team_score = models.IntegerField(null=True)
    opponent_score = models.IntegerField(null=True)
    played = models.BooleanField(default=False)
    team_penalty = models.IntegerField(null=True)
    opponent_penalty = models.IntegerField(null=True)
    time = models.TimeField()
    pitch = models.ForeignKey(FootballPitch, on_delete=models.CASCADE)
    step = models.ForeignKey(KnockoutStep, on_delete=models.CASCADE)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.team.name} vs {self.opponent.name}"

    @property
    def get_pitch(self):
        return self.pitch.name

    @property
    def get_time(self):
        return self.time.strftime("%H:%M")

    @property
    def get_team(self):
        return self.team.name

    @property
    def get_opponent(self):
        return self.opponent.name

    @property
    def get_result(self):
        if self.team_score is None or self.opponent_score is None:
            return False
        elif self.team_score == self.opponent_score:
            return f"{self.team_score} - {self.opponent_score} \n (Penalties: {self.team_penalty} - {self.opponent_penalty}) "
        else:
            return f"{self.team_score} - {self.opponent_score}"

    @property
    def winner(self):
        if self.team_score is None or self.opponent_score is None:
            return False
        elif self.team_score > self.opponent_score:
            return self.team.team_id
        elif self.team_score < self.opponent_score:
            return self.opponent.team_id
        else:
            if self.team_penalty > self.opponent_penalty:
                return self.team.team_id
            else:
                return self.opponent.team_id
