from category.loading import cache
from category.forms import CategoryForm

def no_test_catreg():
    provider = cache.get_object('ask.question')
    print provider.get_root_category()


def test_form():
    form = CategoryForm()
