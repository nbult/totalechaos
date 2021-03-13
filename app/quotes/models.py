import json
import logging
import re

import moment
import requests
from django.db import models
from django.utils.translation import gettext as _

logger = logging.getLogger(__name__)


class BaseModel(models.Model):
    created_at = models.DateTimeField(verbose_name='Created at', auto_now_add=True)

    class Meta:
        abstract = True


class Security(BaseModel):
    name = models.CharField(_('name'), help_text='A short descriptive name for the Security (max_length )',
                            max_length=256)
    isin = models.CharField(_('name'), help_text='International Securities Identification Number', max_length=12,
                            unique=True)

    class Meta:
        ordering = ['name']
        verbose_name = _('security')
        verbose_name_plural = _('securities')

    def __str__(self):
        return '{0}'.format(self.name)


class Quote(BaseModel):
    date = models.DateField(_('date'))
    price = models.DecimalField(_('price'), decimal_places=4, max_digits=8)
    security = models.ForeignKey(Security, verbose_name=_('security'), on_delete=models.CASCADE, related_name='quotes')

    class Meta:
        ordering = ['date']
        verbose_name = _('quote')
        verbose_name_plural = _('quotes')
        get_latest_by = 'date'
        unique_together = ('date', 'security')

    def __str__(self):
        return '{} ({}) = {}'.format(self.security, self.date, self.price)


class Scraper(BaseModel):
    name = models.CharField(_('name'), help_text='A short descriptive name for the Scraper',
                            max_length=256)
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
        ordering = ['name']
        verbose_name = _('scraper')
        verbose_name_plural = _('scrapers')

    def __str__(self):
        return '{}'.format(self.name)

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
                obj, created = Quote.objects.get_or_create(security=self.security,
                                                           date=moment.date(quote[self.date_key]).format('YYYY-MM-DD'),
                                                           defaults={"price": quote[self.price_key]})

                if not created:
                    break

        else:
            logger.error('Got {0} for {1}'.format(r.status_code, self.url))
