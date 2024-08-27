# soccer/models.py
from django.db import models


class Fixture(models.Model):
    fixture_id = models.IntegerField(unique=True)
    league_id = models.IntegerField()
    league_name = models.CharField(max_length=255)
    league_country = models.CharField(max_length=255)
    league_logo = models.URLField(null=True, blank=True)
    league_country_flag = models.URLField(null=True, blank=True)
    season = models.IntegerField()
    round = models.CharField(max_length=100, null=True, blank=True)
    date = models.DateTimeField()
    timestamp = models.IntegerField()
    status_short = models.CharField(max_length=10)
    status_long = models.CharField(max_length=255)
    status_elapsed = models.IntegerField(null=True, blank=True)
    status_type = models.CharField(max_length=50)  # Custom field for mapped status type
    referee = models.CharField(max_length=255, null=True, blank=True)
    timezone = models.CharField(max_length=50)
    venue_id = models.IntegerField(null=True, blank=True)
    venue_name = models.CharField(max_length=255, null=True, blank=True)
    venue_city = models.CharField(max_length=255, null=True, blank=True)

    home_team_id = models.IntegerField()
    home_team_name = models.CharField(max_length=255)
    home_team_logo = models.URLField(null=True, blank=True)
    home_team_winner = models.BooleanField(null=True, blank=True)

    away_team_id = models.IntegerField()
    away_team_name = models.CharField(max_length=255)
    away_team_logo = models.URLField(null=True, blank=True)
    away_team_winner = models.BooleanField(null=True, blank=True)

    home_goals = models.IntegerField(null=True, blank=True)
    away_goals = models.IntegerField(null=True, blank=True)

    halftime_home = models.IntegerField(null=True, blank=True)
    halftime_away = models.IntegerField(null=True, blank=True)

    fulltime_home = models.IntegerField(null=True, blank=True)
    fulltime_away = models.IntegerField(null=True, blank=True)

    extratime_home = models.IntegerField(null=True, blank=True)
    extratime_away = models.IntegerField(null=True, blank=True)

    penalty_home = models.IntegerField(null=True, blank=True)
    penalty_away = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.home_team_name} vs {self.away_team_name} - {self.date}"
