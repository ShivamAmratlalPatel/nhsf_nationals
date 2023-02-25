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
    team = models.ForeignKey(
        FootballTeam, on_delete=models.CASCADE, related_name="team"
    )
    opponent = models.ForeignKey(
        FootballTeam, on_delete=models.CASCADE, related_name="opponent", null=True
    )
    team_score = models.IntegerField(null=True)
    opponent_score = models.IntegerField(null=True)
    played = models.BooleanField(default=False)
    time = models.TimeField(null=True)
    pitch = models.ForeignKey(FootballPitch, on_delete=models.CASCADE, null=True)
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
    opponent = models.ForeignKey(
        FootballTeam, on_delete=models.CASCADE, related_name="opponent_id"
    )
    team_score = models.IntegerField(null=True)
    opponent_score = models.IntegerField(null=True)
    played = models.BooleanField(default=False)
    team_penalty = models.IntegerField(null=True)
    opponent_penalty = models.IntegerField(null=True)
    time = models.TimeField(null=True)
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


class NetballTeam(models.Model):
    team_id = models.AutoField(primary_key=True, db_index=True)
    name = models.CharField(max_length=200)
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE)
    group = models.IntegerField()
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class NetballPitch(models.Model):
    pitch_id = models.AutoField(primary_key=True, db_index=True)
    name = models.CharField(max_length=200)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class NetballSchedule(models.Model):
    schedule_id = models.AutoField(primary_key=True, db_index=True)
    team = models.ForeignKey(NetballTeam, on_delete=models.CASCADE, related_name="team")
    opponent = models.ForeignKey(
        NetballTeam, on_delete=models.CASCADE, related_name="opponent", null=True
    )
    team_score = models.IntegerField(null=True)
    opponent_score = models.IntegerField(null=True)
    played = models.BooleanField(default=False)
    time = models.TimeField(null=True)
    pitch = models.ForeignKey(NetballPitch, on_delete=models.CASCADE, null=True)
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


class NetballTable(models.Model):
    id = models.AutoField(primary_key=True, db_index=True)
    team_id = models.ForeignKey(NetballTeam, on_delete=models.CASCADE)
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


class NetballKnockout(models.Model):
    id = models.AutoField(primary_key=True, db_index=True)
    team = models.ForeignKey(NetballTeam, on_delete=models.CASCADE)
    opponent = models.ForeignKey(
        NetballTeam, on_delete=models.CASCADE, related_name="opponent_id"
    )
    team_score = models.IntegerField(null=True)
    opponent_score = models.IntegerField(null=True)
    played = models.BooleanField(default=False)
    team_penalty = models.IntegerField(null=True)
    opponent_penalty = models.IntegerField(null=True)
    time = models.TimeField(null=True)
    pitch = models.ForeignKey(NetballPitch, on_delete=models.CASCADE)
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


class KhoTeam(models.Model):
    team_id = models.AutoField(primary_key=True, db_index=True)
    name = models.CharField(max_length=200)
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE)
    group = models.IntegerField()
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class KhoPitch(models.Model):
    pitch_id = models.AutoField(primary_key=True, db_index=True)
    name = models.CharField(max_length=200)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class KhoSchedule(models.Model):
    schedule_id = models.AutoField(primary_key=True, db_index=True)
    team = models.ForeignKey(KhoTeam, on_delete=models.CASCADE, related_name="team")
    opponent = models.ForeignKey(
        KhoTeam, on_delete=models.CASCADE, related_name="opponent", null=True
    )
    team_score = models.FloatField(null=True)
    opponent_score = models.FloatField(null=True)
    played = models.BooleanField(default=False)
    time = models.TimeField(null=True)
    pitch = models.ForeignKey(KhoPitch, on_delete=models.CASCADE, null=True)
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


class KhoTable(models.Model):
    id = models.AutoField(primary_key=True, db_index=True)
    team_id = models.ForeignKey(KhoTeam, on_delete=models.CASCADE)
    played = models.IntegerField()
    won = models.IntegerField()
    drawn = models.IntegerField()
    lost = models.IntegerField()
    goals_for = models.FloatField(null=True)
    goals_against = models.FloatField( null=True)
    goal_difference = models.FloatField(null=True)
    points = models.IntegerField()
    points_per_game = models.DecimalField(max_digits=7, decimal_places=4)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.team_id.name


class KhoKnockout(models.Model):
    id = models.AutoField(primary_key=True, db_index=True)
    team = models.ForeignKey(KhoTeam, on_delete=models.CASCADE)
    opponent = models.ForeignKey(
        KhoTeam, on_delete=models.CASCADE, related_name="opponent_id"
    )
    team_score = models.IntegerField(null=True)
    opponent_score = models.IntegerField(null=True)
    played = models.BooleanField(default=False)
    team_penalty = models.IntegerField(null=True)
    opponent_penalty = models.IntegerField(null=True)
    time = models.TimeField(null=True)
    pitch = models.ForeignKey(KhoPitch, on_delete=models.CASCADE)
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


class BadmintonTeam(models.Model):
    team_id = models.AutoField(primary_key=True, db_index=True)
    name = models.CharField(max_length=200)
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE)
    group = models.IntegerField()
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class BadmintonPitch(models.Model):
    pitch_id = models.AutoField(primary_key=True, db_index=True)
    name = models.CharField(max_length=200)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class BadmintonSchedule(models.Model):
    schedule_id = models.AutoField(primary_key=True, db_index=True)
    team = models.ForeignKey(
        BadmintonTeam, on_delete=models.CASCADE, related_name="team"
    )
    opponent = models.ForeignKey(
        BadmintonTeam, on_delete=models.CASCADE, related_name="opponent", null=True
    )
    team_score = models.IntegerField(null=True)
    opponent_score = models.IntegerField(null=True)
    played = models.BooleanField(default=False)
    time = models.TimeField(null=True)
    pitch = models.ForeignKey(BadmintonPitch, on_delete=models.CASCADE, null=True)
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


class BadmintonTable(models.Model):
    id = models.AutoField(primary_key=True, db_index=True)
    team_id = models.ForeignKey(BadmintonTeam, on_delete=models.CASCADE)
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


class BadmintonKnockout(models.Model):
    id = models.AutoField(primary_key=True, db_index=True)
    team = models.ForeignKey(BadmintonTeam, on_delete=models.CASCADE)
    opponent = models.ForeignKey(
        BadmintonTeam, on_delete=models.CASCADE, related_name="opponent_id"
    )
    team_score = models.IntegerField(null=True)
    opponent_score = models.IntegerField(null=True)
    played = models.BooleanField(default=False)
    team_penalty = models.IntegerField(null=True)
    opponent_penalty = models.IntegerField(null=True)
    time = models.TimeField(null=True)
    pitch = models.ForeignKey(BadmintonPitch, on_delete=models.CASCADE)
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


class KabaddiTeam(models.Model):
    team_id = models.AutoField(primary_key=True, db_index=True)
    name = models.CharField(max_length=200)
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE)
    group = models.IntegerField()
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class KabaddiPitch(models.Model):
    pitch_id = models.AutoField(primary_key=True, db_index=True)
    name = models.CharField(max_length=200)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class KabaddiSchedule(models.Model):
    schedule_id = models.AutoField(primary_key=True, db_index=True)
    team = models.ForeignKey(KabaddiTeam, on_delete=models.CASCADE, related_name="team")
    opponent = models.ForeignKey(
        KabaddiTeam, on_delete=models.CASCADE, related_name="opponent", null=True
    )
    team_score = models.IntegerField(null=True)
    opponent_score = models.IntegerField(null=True)
    played = models.BooleanField(default=False)
    time = models.TimeField(null=True)
    pitch = models.ForeignKey(KabaddiPitch, on_delete=models.CASCADE, null=True)
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


class KabaddiTable(models.Model):
    id = models.AutoField(primary_key=True, db_index=True)
    team_id = models.ForeignKey(KabaddiTeam, on_delete=models.CASCADE)
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


class KabaddiKnockout(models.Model):
    id = models.AutoField(primary_key=True, db_index=True)
    team = models.ForeignKey(KabaddiTeam, on_delete=models.CASCADE)
    opponent = models.ForeignKey(
        KabaddiTeam, on_delete=models.CASCADE, related_name="opponent_id"
    )
    team_score = models.IntegerField(null=True)
    opponent_score = models.IntegerField(null=True)
    played = models.BooleanField(default=False)
    team_penalty = models.IntegerField(null=True)
    opponent_penalty = models.IntegerField(null=True)
    time = models.TimeField(null=True)
    pitch = models.ForeignKey(KabaddiPitch, on_delete=models.CASCADE)
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


class CricketTeam(models.Model):
    team_id = models.AutoField(primary_key=True, db_index=True)
    name = models.CharField(max_length=200)
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE)
    group = models.IntegerField()
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class CricketPitch(models.Model):
    pitch_id = models.AutoField(primary_key=True, db_index=True)
    name = models.CharField(max_length=200)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class CricketSchedule(models.Model):
    schedule_id = models.AutoField(primary_key=True, db_index=True)
    team = models.ForeignKey(CricketTeam, on_delete=models.CASCADE, related_name="team")
    opponent = models.ForeignKey(
        CricketTeam, on_delete=models.CASCADE, related_name="opponent", null=True
    )
    team_score = models.IntegerField(null=True)
    opponent_score = models.IntegerField(null=True)
    played = models.BooleanField(default=False)
    time = models.TimeField(null=True)
    pitch = models.ForeignKey(CricketPitch, on_delete=models.CASCADE, null=True)
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


class CricketTable(models.Model):
    id = models.AutoField(primary_key=True, db_index=True)
    team_id = models.ForeignKey(CricketTeam, on_delete=models.CASCADE)
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


class CricketKnockout(models.Model):
    id = models.AutoField(primary_key=True, db_index=True)
    team = models.ForeignKey(CricketTeam, on_delete=models.CASCADE)
    opponent = models.ForeignKey(
        CricketTeam, on_delete=models.CASCADE, related_name="opponent_id"
    )
    team_score = models.IntegerField(null=True)
    opponent_score = models.IntegerField(null=True)
    played = models.BooleanField(default=False)
    team_penalty = models.IntegerField(null=True)
    opponent_penalty = models.IntegerField(null=True)
    time = models.TimeField(null=True)
    pitch = models.ForeignKey(CricketPitch, on_delete=models.CASCADE)
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
