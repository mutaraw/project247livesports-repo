# soccer/tasks.py
from datetime import datetime, timedelta

import requests
from celery import shared_task

from .models import Fixture

STATUS_TYPE_MAPPING = {
    'TBD': 'Scheduled',
    'NS': 'Scheduled',
    '1H': 'Live',
    'HT': 'Live',
    '2H': 'Live',
    'ET': 'Live',
    'BT': 'Live',
    'P': 'Live',
    'SUSP': 'Live',
    'INT': 'Live',
    'FT': 'Finished',
    'AET': 'Finished',
    'PEN': 'Finished',
    'PST': 'Postponed',
    'CANC': 'Cancelled',
    'ABD': 'Abandoned',
    'AWD': 'Not Played',
    'WO': 'Not Played',
    'LIVE': 'Live',
}


def fetch_fixtures_for_date(date_str):
    url = "https://v3.football.api-sports.io/fixtures"
    headers = {
        'x-rapidapi-host': "v3.football.api-sports.io",
        'x-rapidapi-key': "b0f4b023facb8c025154e0e24ca118b3"  # Replace with your actual API key
    }

    params = {'date': date_str}

    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        fixtures = response.json().get('response', [])
        for fixture_data in fixtures:
            fixture = fixture_data['fixture']
            league = fixture_data['league']
            teams = fixture_data['teams']
            goals = fixture_data['goals']
            score = fixture_data['score']

            Fixture.objects.update_or_create(
                fixture_id=fixture['id'],
                defaults={
                    'league_id': league['id'],
                    'league_name': league['name'],
                    'league_country': league['country'],
                    'league_logo': league['logo'],
                    'league_country_flag': league['flag'],
                    'season': league['season'],
                    'round': league.get('round'),
                    'date': fixture['date'],
                    'timestamp': fixture['timestamp'],
                    'status_short': fixture['status']['short'],
                    'status_long': fixture['status']['long'],
                    'status_elapsed': fixture['status'].get('elapsed'),
                    'status_type': STATUS_TYPE_MAPPING.get(fixture['status']['short'], 'Unknown'),
                    'referee': fixture.get('referee'),
                    'timezone': fixture['timezone'],
                    'venue_id': fixture['venue'].get('id'),
                    'venue_name': fixture['venue'].get('name'),
                    'venue_city': fixture['venue'].get('city'),
                    'home_team_id': teams['home']['id'],
                    'home_team_name': teams['home']['name'],
                    'home_team_logo': teams['home']['logo'],
                    'home_team_winner': teams['home']['winner'],
                    'away_team_id': teams['away']['id'],
                    'away_team_name': teams['away']['name'],
                    'away_team_logo': teams['away']['logo'],
                    'away_team_winner': teams['away']['winner'],
                    'home_goals': goals['home'],
                    'away_goals': goals['away'],
                    'halftime_home': score['halftime']['home'],
                    'halftime_away': score['halftime']['away'],
                    'fulltime_home': score['fulltime']['home'],
                    'fulltime_away': score['fulltime']['away'],
                    'extratime_home': score['extratime']['home'],
                    'extratime_away': score['extratime']['away'],
                    'penalty_home': score['penalty']['home'],
                    'penalty_away': score['penalty']['away'],
                }
            )
    else:
        print(f"Error: {response.status_code} - {response.text}")


@shared_task()
def fetch_fixtures_for_dates():
    today = datetime.now().strftime('%Y-%m-%d')
    yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
    tomorrow = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')

    fetch_fixtures_for_date(today)
    fetch_fixtures_for_date(yesterday)
    fetch_fixtures_for_date(tomorrow)
