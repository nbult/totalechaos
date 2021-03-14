from unittest import mock

from django.test import TransactionTestCase

from scrapers.models import KeyValueScraper
from .models import Security, Quote


class DownloadQuotesTestCase(TransactionTestCase):

    def setUp(self):
        scraper = KeyValueScraper.objects.create(name="Scraper",
                                                 url="https://quote_url", key_path='$.[*].x', value_path='$.[*].y')
        self.security = Security.objects.create(name='Security', scraper=scraper)

    def test_3_scraped_quotes_creates_3_quotes(self):
        def mock_scrape(s):
            return [('2021-01-01', 10), ('2021-01-02', 10.5), ('2021-01-03', 11)]

        with mock.patch('scrapers.models.KeyValueScraper.scrape',
                        mock_scrape):
            self.assertEqual(self.security.quotes.count(), 0)
            self.security.download_quotes()
            self.assertEqual(self.security.quotes.count(), 3)
            self.assertNumQueries(3)
            self.assertQuerysetEqual(self.security.quotes.all(), [
                '<Quote: Security (2021-01-01) = 10.0000>',
                '<Quote: Security (2021-01-02) = 10.5000>',
                '<Quote: Security (2021-01-03) = 11.0000>'])

    def test_3_scraped_quotes_creates_1_new_quote(self):
        def mock_scrape(s):
            return [('2021-01-01', 10), ('2021-01-02', 10.5), ('2021-01-03', 11)]

        with mock.patch('scrapers.models.KeyValueScraper.scrape',
                        mock_scrape):
            Quote.objects.create(security=self.security, date='2021-01-02', price=10.5)

            self.assertEqual(self.security.quotes.count(), 1)
            self.security.download_quotes()
            self.assertEqual(self.security.quotes.count(), 2)
            self.assertNumQueries(2)
            self.assertQuerysetEqual(self.security.quotes.all(), [
                '<Quote: Security (2021-01-02) = 10.5000>',
                '<Quote: Security (2021-01-03) = 11.0000>'])
