from cache_object.loading import Cache
from cache_object.utils import CacheLibrary


cache = Cache('django-content-category', 'category_providers')
catreg = CacheLibrary(cache)
