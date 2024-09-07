import asyncio
import json
from collections import defaultdict

from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django.utils.timezone import now, timedelta

from soccer.models import Fixture


class FixtureConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.group_name = "live_fixtures"
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()
        self.task = asyncio.create_task(self.send_fixtures_periodically())

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)
        self.task.cancel()

    @sync_to_async
    def get_fixtures(self):
        priority_leagues = [1, 2, 3, 4, 5, 6, 9, 848, 39, 40, 78, 140, 141, 135, 61, 88, 94, 144, 71, 36, 19, 536, 525,
                            531, 12, 13, 25, 17, 15, 16, 18, 20, 29, 30, 32, 31, 33, 34, 35, 179, 81, 169, 188,
                            210, 113, 203, 128, 79, 218, 247, 292, 98, 318, 307, 345, 106, 197, 119, 103, 866, 909, 713,
                            664, 310, 262, 235, ]
        now_time = now()
        past_24_hours = now_time - timedelta(hours=24)
        next_24_hours = now_time + timedelta(hours=24)

        fixtures_by_status = {
            'live': list(Fixture.objects.filter(status_type='Live')),
            'scheduled': list(Fixture.objects.filter(status_type='Scheduled', date__range=(now_time, next_24_hours))),
            'finished': list(Fixture.objects.filter(status_type='Finished', date__range=(past_24_hours, now_time))),
            'notplayed': list(Fixture.objects.filter(status_type__in=['Cancelled', 'Not Played'],
                                                     date__range=(past_24_hours, now_time)))
        }

        for status, fixtures in fixtures_by_status.items():
            fixtures_by_status[status] = sorted(fixtures, key=lambda x: (
                priority_leagues.index(x.league_id) if x.league_id in priority_leagues else len(priority_leagues),
                -x.date.timestamp()))

        return fixtures_by_status

    async def send_fixtures(self):
        fixtures_by_status = await self.get_fixtures()
        grouped_fixtures = {
            status: self.group_by_league_and_date(fixtures) for status, fixtures in fixtures_by_status.items()
        }
        await self.send(text_data=json.dumps({'fixtures': grouped_fixtures}))

    def group_by_league_and_date(self, fixtures):
        grouped = defaultdict(lambda: defaultdict(list))
        for fixture in fixtures:
            league_key = f"{fixture.league_country} : {fixture.league_name}"
            date_key = fixture.date.strftime('%Y-%m-%d %H:%M')
            grouped[league_key][date_key].append({
                'fixture_id': fixture.fixture_id,
                'home_team_name': fixture.home_team_name,
                'home_team_logo': fixture.home_team_logo,
                'home_goals': fixture.home_goals,
                'away_team_name': fixture.away_team_name,
                'away_team_logo': fixture.away_team_logo,
                'away_goals': fixture.away_goals,
                'home_team_winner': fixture.home_team_winner,
                'away_team_winner': fixture.away_team_winner,
                'status_short': fixture.status_short,
                'status_elapsed': fixture.status_elapsed,
                'halftime_home': fixture.halftime_home,
                'fulltime_home': fixture.fulltime_home,
                'extratime_home': fixture.extratime_home,
                'penalty_home': fixture.penalty_home,
                'halftime_away': fixture.halftime_away,
                'fulltime_away': fixture.fulltime_away,
                'extratime_away': fixture.extratime_away,
                'penalty_away': fixture.penalty_away,
                'league_country_flag': fixture.league_country_flag,
                'league_logo': fixture.league_logo,
                'league_country': fixture.league_country,
                'league_name': fixture.league_name,
            })
        return dict(grouped)

    async def send_fixtures_periodically(self):
        while True:
            await self.send_fixtures()
            await asyncio.sleep(5)
