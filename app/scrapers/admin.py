from django.contrib import admin

from .models import KeyValueScraper


@admin.register(KeyValueScraper)
class QuoteScraperAdmin(admin.ModelAdmin):
    list_display = ('name', 'url', 'key_path', 'value_path')
