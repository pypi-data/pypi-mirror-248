import logging

from django.core.cache import cache

from allianceauth.menu.models import MenuItem
from allianceauth.utils.django import StartupCommand

logger = logging.getLogger(__name__)

MENU_SYNC_CACHE_KEY = "ALLIANCEAUTH-MENU-SYNCED"
MENU_CACHE_KEY = "ALLIANCEAUTH-MENU-CACHE"


class MenuProvider():

    def clear_synced_flag(self) -> bool:
        return cache.delete(MENU_SYNC_CACHE_KEY)

    def set_synced_flag(self) -> bool:
        return cache.set(MENU_SYNC_CACHE_KEY, True)

    def get_synced_flag(self) -> bool:
        return cache.get(MENU_SYNC_CACHE_KEY, False)

    def sync_menu_models(self):
        MenuItem.sync_hook_models()
        self.set_synced_flag()

    def check_and_sync_menu(self) -> None:
        if self.get_synced_flag():
            # performance hit to each page view to ensure tests work.
            # tests clear DB but not cache.
            # TODO rethink all of this?
            if MenuItem.objects.all().count() > 0:
                logger.debug("Menu Hooks Synced")
            else:
                self.sync_menu_models()
        else:
            logger.debug("Syncing Menu Hooks")
            self.sync_menu_models()

    def get_and_cache_menu(self):
        pass

    def clear_menu_cache(self):
        pass


menu_provider = MenuProvider()
