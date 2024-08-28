# soccer/sitemaps.py
from django.contrib.sitemaps import Sitemap

from .models import Fixture


class FixtureSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.8

    def items(self):
        return Fixture.objects.all()

    def lastmod(self, obj):
        return obj.date
