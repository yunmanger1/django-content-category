from category.loading import cache

def test_catreg():
    provider = cache.get_object('ask.question')
    print provider.get_root_category()
