import json
import logging
import re

import moment
import requests
from django.db import models
from django.utils.translation import gettext as _

from investing.models import Security

logger = logging.getLogger(__name__)


class QuoteScraper(models.Model):
    security = models.ForeignKey(Security, verbose_name=_('security'), on_delete=models.CASCADE,
                                 related_name='security')

    url = models.URLField(_('url'), help_text=_('The url to scrape'), max_length=4096)

    regex = models.CharField(_('regex'), help_text='An optional regex to grab the json table',
                             max_length=256, blank=True)

    date_key = models.CharField(_('Date Key'), help_text='The key must yield a date',
                                max_length=32)
    price_key = models.CharField(_('Price Key'), help_text='The key must yield a price',
                                 max_length=32)

    class Meta:
        ordering = ['security__name']
        verbose_name = _('scraper')
        verbose_name_plural = _('scrapers')

    def __str__(self):
        return '{}'.format(self.security.name)

    def update_quotes(self):
        r = requests.get(self.url)

        if r.status_code == requests.codes.ok:
            quotes = []

            if self.regex:
                for result in re.findall(self.regex, str(r.text)):
                    quotes = quotes + json.loads(result)
            else:
                quotes = r.json()

            logging.info('Updating Quotes for {0}, with {1} quotes'.format(self.security.name, len(quotes)))
            for quote in sorted(quotes, key=lambda x: x[self.date_key], reverse=True):
                self.security.add_quote(moment.date(quote[self.date_key]).format('YYYY-MM-DD'), quote[self.price_key])

        else:
            logger.error('Got {0} for {1}'.format(r.status_code, self.url))
