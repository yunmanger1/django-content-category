from cache_object.loading import Cache
from cache_object.utils import CacheLibrary
from django.conf import settings


cache = Cache('django-content-category', 'category_providers', settings.CATEGORY_APP_LIST)
catreg = CacheLibrary(cache)
