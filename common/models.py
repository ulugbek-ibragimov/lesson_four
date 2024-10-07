from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created at"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Updated at"))

    class Meta:
        abstract = True


class VersionHistory(BaseModel):
    version = models.CharField(_("Version"), max_length=64)
    required = models.BooleanField(_("Required"), default=True)

    class Meta:
        verbose_name = _("Version history")
        verbose_name_plural = _("Version histories")

    def __str__(self):
        return self.version


class Currency(BaseModel):
    name = models.CharField(_("Name"), max_length=128)
    code = models.CharField(_("Code"), max_length=64, unique=True)
    exchange_rate = models.DecimalField(_("Exchange Rate"), max_digits=12, decimal_places=8, default=1)
    is_default = models.BooleanField(_("Default"), default=False)

    class Meta:
        verbose_name = _("Currency")
        verbose_name_plural = _("Currencies")

    def __str__(self):
        return self.name

    def clean(self):
        if Currency.objects.filter(is_default=True).exists():
            raise ValidationError({'is_default': 'Is default currency exists'})
