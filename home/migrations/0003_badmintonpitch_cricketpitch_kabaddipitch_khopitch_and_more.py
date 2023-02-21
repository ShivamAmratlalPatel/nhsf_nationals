# Generated by Django 4.1.4 on 2023-02-20 19:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_alter_footballknockout_time'),
    ]

    operations = [
        migrations.CreateModel(
            name='BadmintonPitch',
            fields=[
                ('pitch_id', models.AutoField(db_index=True, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=200)),
                ('is_deleted', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='CricketPitch',
            fields=[
                ('pitch_id', models.AutoField(db_index=True, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=200)),
                ('is_deleted', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='KabaddiPitch',
            fields=[
                ('pitch_id', models.AutoField(db_index=True, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=200)),
                ('is_deleted', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='KhoPitch',
            fields=[
                ('pitch_id', models.AutoField(db_index=True, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=200)),
                ('is_deleted', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='NetballPitch',
            fields=[
                ('pitch_id', models.AutoField(db_index=True, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=200)),
                ('is_deleted', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='NetballTeam',
            fields=[
                ('team_id', models.AutoField(db_index=True, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=200)),
                ('group', models.IntegerField()),
                ('is_deleted', models.BooleanField(default=False)),
                ('chapter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.chapter')),
            ],
        ),
        migrations.CreateModel(
            name='NetballTable',
            fields=[
                ('id', models.AutoField(db_index=True, primary_key=True, serialize=False)),
                ('played', models.IntegerField()),
                ('won', models.IntegerField()),
                ('drawn', models.IntegerField()),
                ('lost', models.IntegerField()),
                ('goals_for', models.IntegerField()),
                ('goals_against', models.IntegerField()),
                ('goal_difference', models.IntegerField()),
                ('points', models.IntegerField()),
                ('points_per_game', models.DecimalField(decimal_places=4, max_digits=7)),
                ('is_deleted', models.BooleanField(default=False)),
                ('team_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.netballteam')),
            ],
        ),
        migrations.CreateModel(
            name='NetballSchedule',
            fields=[
                ('schedule_id', models.AutoField(db_index=True, primary_key=True, serialize=False)),
                ('team_score', models.IntegerField(null=True)),
                ('opponent_score', models.IntegerField(null=True)),
                ('played', models.BooleanField(default=False)),
                ('time', models.TimeField(null=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('opponent', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='opponent', to='home.netballteam')),
                ('pitch', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='home.netballpitch')),
                ('team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='team', to='home.netballteam')),
            ],
        ),
        migrations.CreateModel(
            name='NetballKnockout',
            fields=[
                ('id', models.AutoField(db_index=True, primary_key=True, serialize=False)),
                ('team_score', models.IntegerField(null=True)),
                ('opponent_score', models.IntegerField(null=True)),
                ('played', models.BooleanField(default=False)),
                ('team_penalty', models.IntegerField(null=True)),
                ('opponent_penalty', models.IntegerField(null=True)),
                ('time', models.TimeField(null=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('opponent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='opponent_id', to='home.netballteam')),
                ('pitch', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.netballpitch')),
                ('step', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.knockoutstep')),
                ('team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.netballteam')),
            ],
        ),
        migrations.CreateModel(
            name='KhoTeam',
            fields=[
                ('team_id', models.AutoField(db_index=True, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=200)),
                ('group', models.IntegerField()),
                ('is_deleted', models.BooleanField(default=False)),
                ('chapter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.chapter')),
            ],
        ),
        migrations.CreateModel(
            name='KhoTable',
            fields=[
                ('id', models.AutoField(db_index=True, primary_key=True, serialize=False)),
                ('played', models.IntegerField()),
                ('won', models.IntegerField()),
                ('drawn', models.IntegerField()),
                ('lost', models.IntegerField()),
                ('goals_for', models.IntegerField()),
                ('goals_against', models.IntegerField()),
                ('goal_difference', models.IntegerField()),
                ('points', models.IntegerField()),
                ('points_per_game', models.DecimalField(decimal_places=4, max_digits=7)),
                ('is_deleted', models.BooleanField(default=False)),
                ('team_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.khoteam')),
            ],
        ),
        migrations.CreateModel(
            name='KhoSchedule',
            fields=[
                ('schedule_id', models.AutoField(db_index=True, primary_key=True, serialize=False)),
                ('team_score', models.IntegerField(null=True)),
                ('opponent_score', models.IntegerField(null=True)),
                ('played', models.BooleanField(default=False)),
                ('time', models.TimeField(null=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('opponent', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='opponent', to='home.khoteam')),
                ('pitch', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='home.khopitch')),
                ('team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='team', to='home.khoteam')),
            ],
        ),
        migrations.CreateModel(
            name='KhoKnockout',
            fields=[
                ('id', models.AutoField(db_index=True, primary_key=True, serialize=False)),
                ('team_score', models.IntegerField(null=True)),
                ('opponent_score', models.IntegerField(null=True)),
                ('played', models.BooleanField(default=False)),
                ('team_penalty', models.IntegerField(null=True)),
                ('opponent_penalty', models.IntegerField(null=True)),
                ('time', models.TimeField(null=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('opponent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='opponent_id', to='home.khoteam')),
                ('pitch', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.khopitch')),
                ('step', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.knockoutstep')),
                ('team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.khoteam')),
            ],
        ),
        migrations.CreateModel(
            name='KabaddiTeam',
            fields=[
                ('team_id', models.AutoField(db_index=True, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=200)),
                ('group', models.IntegerField()),
                ('is_deleted', models.BooleanField(default=False)),
                ('chapter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.chapter')),
            ],
        ),
        migrations.CreateModel(
            name='KabaddiTable',
            fields=[
                ('id', models.AutoField(db_index=True, primary_key=True, serialize=False)),
                ('played', models.IntegerField()),
                ('won', models.IntegerField()),
                ('drawn', models.IntegerField()),
                ('lost', models.IntegerField()),
                ('goals_for', models.IntegerField()),
                ('goals_against', models.IntegerField()),
                ('goal_difference', models.IntegerField()),
                ('points', models.IntegerField()),
                ('points_per_game', models.DecimalField(decimal_places=4, max_digits=7)),
                ('is_deleted', models.BooleanField(default=False)),
                ('team_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.kabadditeam')),
            ],
        ),
        migrations.CreateModel(
            name='KabaddiSchedule',
            fields=[
                ('schedule_id', models.AutoField(db_index=True, primary_key=True, serialize=False)),
                ('team_score', models.IntegerField(null=True)),
                ('opponent_score', models.IntegerField(null=True)),
                ('played', models.BooleanField(default=False)),
                ('time', models.TimeField(null=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('opponent', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='opponent', to='home.kabadditeam')),
                ('pitch', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='home.kabaddipitch')),
                ('team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='team', to='home.kabadditeam')),
            ],
        ),
        migrations.CreateModel(
            name='KabaddiKnockout',
            fields=[
                ('id', models.AutoField(db_index=True, primary_key=True, serialize=False)),
                ('team_score', models.IntegerField(null=True)),
                ('opponent_score', models.IntegerField(null=True)),
                ('played', models.BooleanField(default=False)),
                ('team_penalty', models.IntegerField(null=True)),
                ('opponent_penalty', models.IntegerField(null=True)),
                ('time', models.TimeField(null=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('opponent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='opponent_id', to='home.kabadditeam')),
                ('pitch', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.kabaddipitch')),
                ('step', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.knockoutstep')),
                ('team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.kabadditeam')),
            ],
        ),
        migrations.CreateModel(
            name='CricketTeam',
            fields=[
                ('team_id', models.AutoField(db_index=True, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=200)),
                ('group', models.IntegerField()),
                ('is_deleted', models.BooleanField(default=False)),
                ('chapter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.chapter')),
            ],
        ),
        migrations.CreateModel(
            name='CricketTable',
            fields=[
                ('id', models.AutoField(db_index=True, primary_key=True, serialize=False)),
                ('played', models.IntegerField()),
                ('won', models.IntegerField()),
                ('drawn', models.IntegerField()),
                ('lost', models.IntegerField()),
                ('goals_for', models.IntegerField()),
                ('goals_against', models.IntegerField()),
                ('goal_difference', models.IntegerField()),
                ('points', models.IntegerField()),
                ('points_per_game', models.DecimalField(decimal_places=4, max_digits=7)),
                ('is_deleted', models.BooleanField(default=False)),
                ('team_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.cricketteam')),
            ],
        ),
        migrations.CreateModel(
            name='CricketSchedule',
            fields=[
                ('schedule_id', models.AutoField(db_index=True, primary_key=True, serialize=False)),
                ('team_score', models.IntegerField(null=True)),
                ('opponent_score', models.IntegerField(null=True)),
                ('played', models.BooleanField(default=False)),
                ('time', models.TimeField(null=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('opponent', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='opponent', to='home.cricketteam')),
                ('pitch', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='home.cricketpitch')),
                ('team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='team', to='home.cricketteam')),
            ],
        ),
        migrations.CreateModel(
            name='CricketKnockout',
            fields=[
                ('id', models.AutoField(db_index=True, primary_key=True, serialize=False)),
                ('team_score', models.IntegerField(null=True)),
                ('opponent_score', models.IntegerField(null=True)),
                ('played', models.BooleanField(default=False)),
                ('team_penalty', models.IntegerField(null=True)),
                ('opponent_penalty', models.IntegerField(null=True)),
                ('time', models.TimeField(null=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('opponent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='opponent_id', to='home.cricketteam')),
                ('pitch', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.cricketpitch')),
                ('step', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.knockoutstep')),
                ('team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.cricketteam')),
            ],
        ),
        migrations.CreateModel(
            name='BadmintonTeam',
            fields=[
                ('team_id', models.AutoField(db_index=True, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=200)),
                ('group', models.IntegerField()),
                ('is_deleted', models.BooleanField(default=False)),
                ('chapter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.chapter')),
            ],
        ),
        migrations.CreateModel(
            name='BadmintonTable',
            fields=[
                ('id', models.AutoField(db_index=True, primary_key=True, serialize=False)),
                ('played', models.IntegerField()),
                ('won', models.IntegerField()),
                ('drawn', models.IntegerField()),
                ('lost', models.IntegerField()),
                ('goals_for', models.IntegerField()),
                ('goals_against', models.IntegerField()),
                ('goal_difference', models.IntegerField()),
                ('points', models.IntegerField()),
                ('points_per_game', models.DecimalField(decimal_places=4, max_digits=7)),
                ('is_deleted', models.BooleanField(default=False)),
                ('team_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.badmintonteam')),
            ],
        ),
        migrations.CreateModel(
            name='BadmintonSchedule',
            fields=[
                ('schedule_id', models.AutoField(db_index=True, primary_key=True, serialize=False)),
                ('team_score', models.IntegerField(null=True)),
                ('opponent_score', models.IntegerField(null=True)),
                ('played', models.BooleanField(default=False)),
                ('time', models.TimeField(null=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('opponent', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='opponent', to='home.badmintonteam')),
                ('pitch', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='home.badmintonpitch')),
                ('team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='team', to='home.badmintonteam')),
            ],
        ),
        migrations.CreateModel(
            name='BadmintonKnockout',
            fields=[
                ('id', models.AutoField(db_index=True, primary_key=True, serialize=False)),
                ('team_score', models.IntegerField(null=True)),
                ('opponent_score', models.IntegerField(null=True)),
                ('played', models.BooleanField(default=False)),
                ('team_penalty', models.IntegerField(null=True)),
                ('opponent_penalty', models.IntegerField(null=True)),
                ('time', models.TimeField(null=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('opponent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='opponent_id', to='home.badmintonteam')),
                ('pitch', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.badmintonpitch')),
                ('step', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.knockoutstep')),
                ('team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.badmintonteam')),
            ],
        ),
    ]