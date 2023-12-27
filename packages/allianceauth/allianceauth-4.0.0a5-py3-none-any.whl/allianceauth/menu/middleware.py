from django.utils.deprecation import MiddlewareMixin

import logging

from allianceauth.menu.providers import menu_provider

logger = logging.getLogger(__name__)


class MenuSyncMiddleware(MiddlewareMixin):

    def __call__(self, request):
        """Alliance Auth Menu Sync Middleware"""
        menu_provider.check_and_sync_menu()
        return super().__call__(request)
