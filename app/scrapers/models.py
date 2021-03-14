import json
import logging
import re

import requests
from django.db import models
from django.utils.translation import gettext as _
from jsonpath_rw import parse

logger = logging.getLogger(__name__)


class Scraper(models.Model):
    name = models.CharField(_('name'), help_text='A short descriptive name for the Scraper',
                            max_length=256)
    url = models.URLField(_('url'), help_text=_('The url to scrape'), max_length=4096)

    regex = models.CharField(_('regex'), help_text='An optional regex to grab a specific part of the webpage',
                             max_length=256, blank=True)

    class Meta:
        abstract: True

    def __str__(self):
        return '{}'.format(self.name)

    def __scrape__(self):
        r = requests.get(self.url)

        scraped = []
        if r.status_code == requests.codes.ok:

            if self.regex:
                for result in re.findall(self.regex, str(r.text)):
                    scraped += json.loads(result)
            else:
                scraped = r.json()

        return scraped


class KeyValueScraper(Scraper):
    key_path = models.CharField(_('Key Path'), help_text='The path must yield an array with keys',
                                max_length=32)
    value_path = models.CharField(_('Value Path'), help_text='The path must yield an array with values',
                                  max_length=32)

    class Meta:
        ordering = ['url']
        verbose_name = _('KeyValue Scraper')
        verbose_name_plural = _('KeyValue Scrapers')

    def scrape(self):
        scraped = self.__scrape__()

        key_values = []

        if scraped:
            keys = [m.value for m in parse(self.key_path).find(scraped)]
            values = [m.value for m in parse(self.value_path).find(scraped)]

            key_values = list(map(lambda k, v: (k, v), keys, values))

        return key_values
