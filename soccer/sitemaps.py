from django.contrib.sitemaps import Sitemap
from django.urls import reverse


class SimpleSitemap(Sitemap):
    changefreq = "daily"
    priority = 1.0

    def items(self):
        return ['index']

    def location(self, item):
        return reverse(item)
