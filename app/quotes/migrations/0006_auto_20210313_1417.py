# Generated by Django 3.1.7 on 2021-03-13 13:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quotes', '0005_auto_20210313_1031'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quote',
            name='date',
            field=models.DateField(verbose_name='date'),
        ),
        migrations.AlterField(
            model_name='scraper',
            name='url',
            field=models.URLField(help_text='The url to scrape', max_length=4096, verbose_name='url'),
        ),
        migrations.AlterUniqueTogether(
            name='quote',
            unique_together={('date', 'security')},
        ),
    ]