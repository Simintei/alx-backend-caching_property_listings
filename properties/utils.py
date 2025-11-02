from django.core.cache import cache
from .models import Property
import logging
from django_redis import get_redis_connection


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


logger = logging.getLogger(__name__)

def get_redis_cache_metrics():
    """
    Returns Redis hit/miss stats and hit ratio.
    """
    conn = get_redis_connection("default")
    info = conn.info("stats")

    hits = info.get("keyspace_hits", 0)
    misses = info.get("keyspace_misses", 0)
    total = hits + misses
    hit_ratio = (hits / total) if total > 0 else 0

    metrics = {
        "hits": hits,
        "misses": misses,
        "hit_ratio": round(hit_ratio, 4)
    }

    logger.info(f"Redis cache metrics: {metrics}")
    return metrics
