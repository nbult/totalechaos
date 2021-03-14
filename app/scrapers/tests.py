import responses
from django.test import TransactionTestCase

from .models import QuoteScraper, Security


class QuoteScraperTestCase(TransactionTestCase):

    def setUp(self):
        self.security = Security.objects.create(name='Security')

    @responses.activate
    def test_update_quotes_not_found_0_quotes(self):
        scraper = QuoteScraper.objects.create(name="Scraper", security=self.security,
                                         url="https://quote_url", date_key='x', price_key='y')

        responses.add(responses.GET, 'https://quote_url',
                      json={'not found': '404'}, status=404)
        scraper.update_quotes()

        self.assertNumQueries(0)
        self.assertEqual(self.security.quotes.count(), 0)

    @responses.activate
    def test_update_quotes_json_creates_3_quotes(self):
        scraper = QuoteScraper.objects.create(name="Scraper", security=self.security,
                                         url="https://quote_url", date_key='x', price_key='y')
        data = [{"x": '2021-01-01', "y": 10}, {"x": '2021-01-02', "y": 10.5}, {"x": '2021-01-03', "y": 11}]

        responses.add(responses.GET, 'https://quote_url',
                      json=data, status=200)
        scraper.update_quotes()

        self.assertNumQueries(3)
        self.assertEqual(self.security.quotes.count(), 3)


    @responses.activate
    def test_update_quotes_invalid_date_key_raises_exception(self):
        scraper = QuoteScraper.objects.create(name="Scraper", security=self.security,
                                         url="https://quote_url", date_key='not_present', price_key='y')
        data = [{"x": '2021-01-01', "y": 10}]

        responses.add(responses.GET, 'https://quote_url',
                      json=data, status=200)

        with self.assertRaises(KeyError):
            scraper.update_quotes()

        self.assertNumQueries(0)
        self.assertEqual(self.security.quotes.count(), 0)


    @responses.activate
    def test_update_quotes_invalid_date_key_raises_exception(self):
        scraper = QuoteScraper.objects.create(name="Scraper", security=self.security,
                                         url="https://quote_url", date_key='x', price_key='not_present')
        data = [{"x": '2021-01-01', "y": 10}]

        responses.add(responses.GET, 'https://quote_url',
                      json=data, status=200)

        with self.assertRaises(KeyError):
            scraper.update_quotes()

        self.assertNumQueries(0)
        self.assertEqual(self.security.quotes.count(), 0)

    @responses.activate
    def test_update_quotes_matching_regex_creates_3_quotes(self):
        scraper = QuoteScraper.objects.create(name="Scraper", security=self.security,
                                         url="https://quote_url", date_key='x', price_key='y',
                                         regex="data:\s(\[{.*}+\])")

        body = "data: [{\"x\":\"2021-01-01\",\"y\":10}," \
               "{\"x\":\"2021-01-02\",\"y\":10.50}," \
               "{\"x\":\"2021-01-03\",\"y\":11}]"

        responses.add(responses.GET, 'https://quote_url',
                      body=body, status=200)

        scraper.update_quotes()

        self.assertNumQueries(3)
        self.assertEqual(self.security.quotes.count(), 3)

    @responses.activate
    def test_update_quotes_creates_only_new_quotes(self):
        data = [{"x": '2021-01-02', "y": 10}]
        responses.add(responses.GET, 'https://quote_url',
                      json=data, status=200)
        data = [{"x": '2021-01-01', "y": 10}, {"x": '2021-01-02', "y": 10.5}, {"x": '2021-01-03', "y": 11}]
        responses.add(responses.GET, 'https://quote_url',
                      json=data, status=200)

        scraper = QuoteScraper.objects.create(name="Scraper", security=self.security,
                                         url="https://quote_url", date_key='x', price_key='y')

        scraper.update_quotes()
        self.assertEqual(self.security.quotes.count(), 1)

        scraper.update_quotes()
        self.assertEqual(self.security.quotes.count(), 2)

        self.assertQuerysetEqual(self.security.quotes.all(), ['<Quote: Security (2021-01-02) = 10.0000>',
                                                              '<Quote: Security (2021-01-03) = 11.0000>'])
