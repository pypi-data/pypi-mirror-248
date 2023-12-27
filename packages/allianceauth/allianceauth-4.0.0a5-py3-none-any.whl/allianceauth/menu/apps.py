import logging

from django.apps import AppConfig
from django.db.utils import ProgrammingError, OperationalError


logger = logging.getLogger(__name__)


class MenuConfig(AppConfig):
    name = "allianceauth.menu"
    label = "menu"

    def ready(self):
        try:
            from allianceauth.menu.providers import menu_provider
            menu_provider.clear_synced_flag()
        except (ProgrammingError, OperationalError):
            logger.warning("Migrations not completed for MenuItems")
