from django import forms
from category.fields import CategoryField

class CategoryForm(forms.Form):

    def __init__(self, root, *a, **kw):
        self.root = root
        super(CategoryForm, self).__init__(*a, **kw)

        self.fields['category'].root = self.root

    category = CategoryField()
