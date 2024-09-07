from collections import defaultdict

from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader

from soccer.models import Fixture

priority_leagues = [1, 2, 3, 4, 5, 6, 9, 848, 39, 40, 78, 140, 141, 135, 61, 88, 94, 144, 71, 36, 19, 536, 525, 531, 12, 13, 25, 17, 15, 16, 18, 20, 29, 30, 32, 31, 33, 34, 35, 179, 81, 169, 188,
                    210, 113, 203, 128, 79, 218, 247, 292, 98, 318, 307, 345, 106, 197, 119, 103, 866, 909, 713,
                    664, 310, 262, 235, ]


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


def robots_txt(request):
    template = loader.get_template('robots.txt')
    return HttpResponse(template.render(), content_type="text/plain")
