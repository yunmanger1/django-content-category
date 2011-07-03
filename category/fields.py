from django import forms
from category.widgets import CategorySelectWidget
from category.models import Category
from django.db.models.fields import Field


class CategoryField(forms.ModelChoiceField):

    def __init__(self, widget = None, queryset = None, root = None, display_root = False, collapse = True, *a, **kw):
        if widget is None:
            kw['widget'] = CategorySelectWidget(attrs = {'class' : 'treeview-gray '})
        else:
            kw['widget'] = widget
        if queryset is None:
            empty = Category.objects.none()
#            self.choices = empty
            kw['queryset'] = empty
        else:
            kw['queryset'] = queryset
#            self.choices = queryset
        kw['empty_label'] = None
        super(CategoryField, self).__init__(*a, **kw)
        self.root = root
        self.widget.display_root = display_root
        self.widget.collapse = collapse

    def label_from_instance(self, obj):
        return obj

    def _get_root(self):
        return self._root

    def _set_root(self, value):
        self._root = value
        if self._root is None:
            queryset = Category.objects.all()
#            self.choices = queryset
            self.queryset = queryset
        else:
            queryset = Category.objects.filter(root = self._root)
#            self.choices = queryset
            self.queryset = queryset

    root = property(_get_root, _set_root)
