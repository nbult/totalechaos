from django.db import models
from django.utils.translation import gettext as _


class BaseModel(models.Model):
    created_at = models.DateTimeField(verbose_name='Created at', auto_now_add=True)

    class Meta:
        abstract = True


class Security(BaseModel):
    name = models.CharField(_('name'), help_text='A short descriptive name for the Security (max_length )',
                            max_length=256)
    isin = models.CharField(_('isin'), help_text='International Securities Identification Number', max_length=12,
                            unique=True)

    class Meta:
        ordering = ['name']
        verbose_name = _('security')
        verbose_name_plural = _('securities')

    def __str__(self):
        return '{0}'.format(self.name)

    def add_quote(self, date, price):
        pass


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
