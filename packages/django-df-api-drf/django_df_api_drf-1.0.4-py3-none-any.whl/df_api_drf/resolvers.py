from typing import Any

from django.contrib.sites.models import Site
from django.utils.module_loading import import_string

from df_api_drf.settings import api_settings


def client_url(**kwargs: Any) -> str:
    return import_string(api_settings.SITE_URL_RESOLVER)().format_url(**kwargs)


class BaseClientUrlResolver:
    def format_url(self, **kwargs: Any) -> str:
        raise NotImplementedError


class SiteUrlResolver(BaseClientUrlResolver):
    def get_site(self, **kwargs: Any) -> Site:
        return Site.objects.get_current()

    def format_url(self, **kwargs: Any) -> str:
        site = self.get_site(**kwargs)
        return api_settings.SITE_URL % site.domain
