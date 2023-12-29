from django.utils.translation import gettext_lazy as _

from allianceauth import hooks
from allianceauth.services.hooks import MenuItemHook, UrlHook

from . import __title__, urls


class standingssyncMenuItem(MenuItemHook):
    """This class ensures only authorized users will see the menu entry"""

    def __init__(self):
        # setup menu entry for sidebar
        MenuItemHook.__init__(
            self,
            _(__title__),
            "fas fa-sync-alt",
            "standingssync:characters",
            navactive=["standingssync:characters"],
        )

    def render(self, request):
        if request.user.has_perm("standingssync.add_syncedcharacter"):
            return MenuItemHook.render(self, request)
        return ""


@hooks.register("menu_item_hook")
def register_menu():
    return standingssyncMenuItem()


@hooks.register("url_hook")
def register_urls():
    return UrlHook(urls, "standingssync", r"^standingssync/")
