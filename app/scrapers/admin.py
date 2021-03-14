from django.contrib import admin

from .models import QuoteScraper


@admin.register(QuoteScraper)
class QuoteScraperAdmin(admin.ModelAdmin):
    list_display = ('security', 'url',)
    search_fields = ['security__name', ]
