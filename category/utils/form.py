from category.models import Category
from category.forms import CategoryForm

def get_category_form(root = None, *a, **kw):
    if root is None:
        try:
            return get_category_form(root = Category.objects.get(**kw))
        except Category.DoesNotExist:
            return None
        except Category.MultipleObjectsReturned:
            return None
    return CategoryForm(root = root)
