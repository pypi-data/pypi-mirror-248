from django.apps import AppConfig

from . import __version__


class SyncAltContactsConfig(AppConfig):
    name = "standingssync"
    label = "standingssync"
    verbose_name = f"Standings Sync v{__version__}"
