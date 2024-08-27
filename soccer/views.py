from collections import defaultdict

from django.shortcuts import render

from soccer.models import Fixture

priority_leagues = [1, 2, 3, 848, 39, 78, 140, 135, 61, 88, 94, 144, 71]


def index(request):
    fixtures = Fixture.objects.filter(status_type='Live')

    sorted_fixtures = sorted(fixtures, key=lambda x: (
        priority_leagues.index(x.league_id) if x.league_id in priority_leagues else len(priority_leagues),
        -x.date.timestamp()))

    grouped_fixtures = defaultdict(lambda: defaultdict(list))
    for fixture in sorted_fixtures:
        league_key = (fixture.league_country, fixture.league_name)
        date_key = fixture.date.strftime('%Y-%m-%d %H:%M')
        grouped_fixtures[league_key][date_key].append(fixture)

    grouped_fixtures = {k: dict(v) for k, v in grouped_fixtures.items()}

    context = {'grouped_fixtures': grouped_fixtures}
    return render(request, 'soccer/index.html', context)
