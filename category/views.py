from django.shortcuts import render
from category.forms import CategoryForm
from django.contrib.auth.decorators import login_required

@login_required
def category_new(request, root_id = None, template_name = "category/category_new.html"):
    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = form.save()
    else:
        form = CategoryForm()
    return render(request, template_name, {'form' : form})
