from django.conf import settings
from django.core.cache import cache


def delete_cache(key_prefix: str) -> None:
    """
    Delete all cache keys with the given prefix.
    """
    keys_pattern = (
        f'views.decorators.cache.cache_*.{key_prefix}.'
        f'*.{settings.LANGUAGE_CODE}'
    )
    cache.delete_pattern(keys_pattern)
