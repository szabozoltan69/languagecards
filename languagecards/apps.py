from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class LanguagecardsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'languagecards'
    verbose_name = _('language cards')
