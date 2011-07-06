from django import template, forms
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe
from django.template.base import Variable, VariableDoesNotExist
from django.db.models import get_model
from category.utils.tree import construct_tree
from category.loading import cache
from django.conf import settings
from category.utils.catroot import get_root
from category.utils.render import build_attrs_string
from django.template.defaultfilters import slugify
from category import widgets

Category = get_model('category', 'category')

register = template.Library()

def do_render_node(root, value, template_name):
    subtree = None
    if root.children.count():
        subtree = "\n".join([do_render_node(child, value, template_name = template_name) for child in root.children])
        subtree = mark_safe(subtree)
    selected = root.node.pk == value
    return render_to_string(template_name, {'object' : root, 'subtree' : subtree, 'open' : selected, 'selected' : selected })
do_render_node.is_safe = True

class RenderNodeNode(template.Node):

    def __init__(self, root, **kwargs):
        self.root = root
        self.attrs = kwargs

    def render(self, context):
        root = Variable(self.root).resolve(context)
        attrs = {
            'template_name' : 'category/render-node.html',
            'value' : None,
        }
        for key, value in self.attrs.items():
            if self.attrs[key] == True:
                attrs[key] = True
            else:
                attrs[key] = Variable(value).resolve(context)
        return do_render_node(root, **attrs)

def do_render_tree(provider, root, template_name, collapse, context = None, attrs = {}):
    list = provider.get_categories(root)
    map = {}
    roots = construct_tree(list, map)
    return render_to_string(template_name, {'roots' : roots, 'collapse' : collapse, \
        'attrs_str': build_attrs_string(attrs), 'attrs' : attrs}, context)


class RenderTreeNode(template.Node):

    def __init__(self, provider, root = None, template_name = None, collapse = True, media = 'media', *args, **kwargs):
        super(RenderTreeNode, self).__init__(*args, **kwargs)
        self.provider, self.root, self.template_name = provider, root, template_name
        self.attrs = kwargs
        self.collapse = collapse
        self.media_key = media

    def render(self, context):
        provider = Variable(self.provider).resolve(context)
        media = forms.Media(css = widgets.CategorySelectWidget.Media.css, \
                            js = widgets.CategorySelectWidget.Media.js)
        context[self.media_key] = media
        attrs = {
            'id': 'category-tree-{0}'.format(slugify(provider)),
            'class' : 'category-tree',
        }
        for key, value in self.attrs.items():
            if self.attrs[key] == True:
                attrs[key] = True
            else:
                attrs[key] = Variable(value).resolve(context)
        root = None
        if self.root:
            root = Variable(self.root).resolve(context)
        if self.template_name is None:
            template_name = 'category/render-tree.html'
        else:
            template_name = Variable(self.template_name).resolve(context)

        provider = cache.get_object(provider)
        if root:
            if isinstance(root, Category):
                if root.is_root:
                    root = root
                else:
                    root = root.root
            else:
                root = get_root(name = root)
        else:
            root = provider.get_root_category()
        cache.add_object(provider, root.pk)
        kw = {
            'template_name':template_name,
            'context': context,
            'collapse': self.collapse,
            'attrs' : attrs,
        }
        return do_render_tree(provider, root, **kw)

def do_get_category_url(category, provider = None):
    """
    {{ category|get_category_url:"ask.settings" }}
    """
    root = category.root
    assert root
    try:
        if provider is not None:
            provider = cache.get_object(provider)
        else:
            provider = cache.get_object(root.pk)
    except KeyError:
        if settings.DEBUG:
            raise VariableDoesNotExist("there is no provider for %s in cache", (root.pk,))
        return ''
    return provider.get_url(category)


def do_category_count(category, provider = None):
    """
    {{ category|category_count:"ask.settings" }}
    """
    root = category.root
    assert root
    try:
        if provider is not None:
            provider = cache.get_object(provider)
        else:
            provider = cache.get_object(root.pk)
    except KeyError:
        if settings.DEBUG:
            raise VariableDoesNotExist("there is no provider for %s in cache", (root.pk,))
        return ''
    return provider.get_count_for(category)

def do_render_tree_tag(parser, token):
    """
    {% render_category_tree provider="provider name" root="root name" collapse %}
    """
    bits = token.split_contents()
    kwargs = {}
    for bit in bits[1:]:
        chunks = bit.split('=')
        if len(chunks) == 2:
            kwargs[chunks[0]] = chunks[1]
        elif len(chunks) == 1:
            kwargs[chunks[0]] = True
    if len(bits) < 2 or not kwargs.get('provider', None):
        raise template.TemplateSyntaxError("'%s' takes 2-n arguments" % bits[0])
    return RenderTreeNode(**kwargs)


def do_render_node_tag(parser, token):
    """
    {% render_node node value template_name %}
    """
    bits = token.split_contents()
    kwargs = {}
    for bit in bits[1:]:
        chunks = bit.split('=')
        if len(chunks) == 2:
            kwargs[chunks[0]] = chunks[1]
        elif len(chunks) == 1:
            kwargs[chunks[0]] = True

    if len(bits) < 2 or not kwargs.get('root', None):
        raise template.TemplateSyntaxError("'%s' takes root must be set arguments" % bits[0])
    return RenderNodeNode(**kwargs)

register.filter('get_category_url', do_get_category_url)
register.filter('category_count', do_category_count)
register.filter('render_node', do_render_node)
register.tag('render_node', do_render_node_tag)
register.tag('render_category_tree', do_render_tree_tag)

