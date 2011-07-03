from django import forms
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe
from category import getLogger

log = getLogger(__file__)

class TemplateList(list):

    def count(self):
        return len(self)

class Node(object):

    node = None
    _children = None

    def __init__(self, node = None):
        self.node = node
        self._children = TemplateList()

    def _set_children(self, value):
        self._children = value

    def _get_children(self):
        return self._children

    children = property(_get_children, _set_children)

    def append(self, child):
        self._children.append(child)

    def __unicode__(self):
        if self.node:
            return self.node.name
        super(Node, self).__unicode__()

class CategorySelectWidget(forms.Select):
    built = False
    display_root = False
    collapse = True
    template_name = 'category/render-field.html'

    class Media:
        css = {
            'screen': ('category/style.css', 'treeview/jquery.treeview.css')
        }
        js = ('jquery/jquery.min.js', 'treeview/jquery.treeview.min.js', 'cookie/jquery.cookie.js',)

    def construct_tree(self, choices):
        self.map = {}
        self.root = []
        for key, category in choices:
            print key, category
            current = self.map.get(category.pk, None)
            if current is None:
                current = Node(category)
                self.map[category.pk] = current
            else:
                current.node = category
            if category.parent_id == None:
                self.root.append(current)
            else:
                parent = self.map.get(category.parent_id, None)
                if parent is None:
                    parent = Node()
                    self.map[category.parent_id] = parent
                parent.append(current)
        self.built = True

    def _set_choices(self, value):
        self._choices = value
        self.construct_tree(value)

    def _get_choices(self):
        return self._choices

    choices = property(_get_choices, _set_choices)

    def render_attrs(self, attrs):
        box = []
        for key, value in attrs.items():
            box.append(u"{0}=\"{1}\"".format(key, value))
        return mark_safe(" ".join(box))

    def render(self, name, value, attrs):
        attrs = self.build_attrs(attrs)
        if value is None:
            value = ''
        result = render_to_string(self.template_name, \
        {'roots' : self.root, 'display_root' : self.display_root, \
         'attrs_str' : self.render_attrs(attrs), 'attrs' : attrs, \
         'name' : name, 'value' : value, 'collapse' : self.collapse })
        return result



