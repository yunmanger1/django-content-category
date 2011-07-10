from django import forms
from category.fields import CategoryField
from django.db.models.loading import get_model
Category = get_model('category', 'category')

class CategoryForm(forms.ModelForm):

#    def __init__(self, root, *a, **kw):
#        self.root = root
#        super(CategoryForm, self).__init__(*a, **kw)
#
#        self.fields['category'].root = self.root
#
#    category = CategoryField()

    parent = CategoryField(required = False, collapse = False)

    def _get_root(self):
        return self._root

    def _set_root(self, value):
        self._root = value
        self.fields['parent'].root = value

    root = property(_get_root, _set_root)

    class Meta:
        model = Category
        exclude = ('slug', 'sort_order', 'root',)
