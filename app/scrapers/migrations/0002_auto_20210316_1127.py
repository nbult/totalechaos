# Generated by Django 3.1.7 on 2021-03-16 10:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scrapers', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='keyvaluescraper',
            options={'ordering': ['url'], 'verbose_name': 'KeyValue Scraper', 'verbose_name_plural': 'KeyValue Scrapers'},
        ),
    ]