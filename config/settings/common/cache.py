# https://docs.djangoproject.com/en/4.0/ref/settings/#std:setting-CACHES

CACHES = dict(
    default=dict(
        BACKEND="django_redis.cache.RedisCache",
        OPTIONS=dict(
            CLIENT_CLASS="django_redis.client.DefaultClient",
            MAX_ENTRIES=1000,
        ),
    ),
)
