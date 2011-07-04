from django import forms
from category.widgets import CategorySelectWidget
from category.models import Category
from django.core import validators
from django.core.exceptions import ValidationError


class CategoryField(forms.ModelChoiceField):

    def __init__(self, widget = None, queryset = None, root = None, display_root = False, collapse = True, *a, **kw):
        if widget is None:
            kw['widget'] = CategorySelectWidget(attrs = {'class' : 'treeview-gray '})
        else:
            kw['widget'] = widget
        if queryset is None:
            empty = Category.objects.none()
            kw['queryset'] = empty
        else:
            kw['queryset'] = queryset
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
            self.queryset = queryset
        else:
            queryset = Category.objects.filter(root = self._root)
            self.queryset = queryset

    root = property(_get_root, _set_root)

    def validate(self, value):
        if value in validators.EMPTY_VALUES:
            if self.required:
                raise ValidationError(self.error_messages['required'])
        else:
            key = self.to_field_name or 'pk'
            try:
                self.queryset.get(**{key : getattr(value, key)})
            except:
                raise ValidationError(self.error_messages['invalid_choice'])
