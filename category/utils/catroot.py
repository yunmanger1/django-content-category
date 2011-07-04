from django.contrib.comments import get_model

Category = get_model('category', 'category')

def get_root(*args, **kwargs):
    try:
        category = Category.objects.get(is_root = True, *args, **kwargs)
    except Category.DoesNotExist:
        category = Category(is_root = True, *args, **kwargs)
        category.save()
    return category
