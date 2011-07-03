from category.utils.form import get_category_form
from django.shortcuts import render
from category.models import Category

def test_view(request, template_name = 'category/test.html'):
    form = get_category_form(slug = 'blogs')
    form.initial = {'category' : Category.objects.get(slug = 'handmade')}
    return render(request, template_name, {'form': form})
