from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class GeoluminateIdentityConfig(AppConfig):
    name = "geoluminate.identity"
    label = "identity"
    verbose_name = _("identity")
