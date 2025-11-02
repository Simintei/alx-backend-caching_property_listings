from django.core.cache import cache
from .models import Property

CACHE_KEY_ALL_PROPERTIES = "all_properties"

def get_all_properties():
    """Return all Property records, cached in Redis for 1 hour."""
    cached_data = cache.get(CACHE_KEY_ALL_PROPERTIES)

    if cached_data is not None:
        return cached_data  # cache hit ✅

    # cache miss ❌ → fetch from DB
    queryset = list(Property.objects.all())
    cache.set(CACHE_KEY_ALL_PROPERTIES, queryset, 3600)  # TTL: 1 hour

    return queryset
