from django.contrib import admin
from django.utils.translation import gettext as _
from .models import Security, Quote


@admin.register(Quote)
class QuoteAdmin(admin.ModelAdmin):

    def view_price(self, obj):
        return '€ {0:.4f}'.format(obj.price)

    view_price.short_description = _('Price')

    date_hierarchy = 'date'
    list_display = ('date', 'security', 'view_price')
    list_filter = ('security',)


@admin.register(Security)
class SecurityAdmin(admin.ModelAdmin):

    def view_last_price(self, obj):
        return '€ {0:.4f}'.format(obj.quotes.latest().price)

    view_last_price.short_description = _('Latest Price')

    def view_last_date(self, obj):
        return '{0}'.format(obj.quotes.latest().date)

    view_last_date.short_description = _('Latest Date')

    list_display = ('name', 'view_last_date', 'view_last_price',)
    search_fields = ['name', ]
