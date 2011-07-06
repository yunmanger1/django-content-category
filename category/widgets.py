from django import forms
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe
from category import getLogger
from category.utils.tree import construct_tree
from category.utils.render import build_attrs_string

log = getLogger(__file__)

class CategorySelectWidget(forms.Select):
    built = False
    display_root = False
    collapse = True
    template_name = 'category/form/render-field.html'

    class Media:
        css = {
            'screen': ('category/style.css', 'treeview/jquery.treeview.css')
        }
        js = ('jquery/jquery.min.js', 'treeview/jquery.treeview.min.js', 'cookie/jquery.cookie.js',)

    def construct(self, choices):
        self.map = {}
        all = [category for key, category in choices]
        self.root = construct_tree(all, map = self.map)
        self.built = True

    def _set_choices(self, value):
        self._choices = value
        self.construct(value)

    def _get_choices(self):
        return self._choices

    choices = property(_get_choices, _set_choices)

    def render(self, name, value, attrs):
        attrs = self.build_attrs(attrs)
        if value is None:
            value = ''
        result = render_to_string(self.template_name, \
        {'roots' : self.root, 'display_root' : self.display_root, \
         'attrs_str' : build_attrs_string(attrs), 'attrs' : attrs, \
         'name' : name, 'value' : value, 'collapse' : self.collapse })
        return result



