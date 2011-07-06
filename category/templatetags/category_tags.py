from django import template
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe
from django.template.base import Variable, VariableDoesNotExist
from django.db.models import get_model
from category.utils.tree import construct_tree
from category.loading import cache
from django.conf import settings
from category.utils.catroot import get_root
from category.utils.render import build_attrs_string

Category = get_model('category', 'category')

register = template.Library()

def do_render_node(node, value = None, template_name = 'category/render-node.html'):
    subtree = None
    if node.children.count():
        subtree = "\n".join([do_render_node(child, value, template_name = template_name) for child in node.children])
        subtree = mark_safe(subtree)
    selected = node.node.pk == value
    return render_to_string(template_name, {'object' : node, 'subtree' : subtree, 'open' : selected, 'selected' : selected })
do_render_node.is_safe = True

class RenderNodeNode(template.Node):
    def __init__(self, node, value = None, template_name = None, *args, **kwargs):
        super(RenderNodeNode, self).__init__(*args, **kwargs)
        self.node, self.value, self.template_name = node, value, template_name

    def render(self, context):
        node = Variable(self.node).resolve(context)
        args = [node]
        value = None
        if self.value is not None:
            value = Variable(self.value).resolve(context)
        if value:
            args.append(value)
        template_name = None
        if self.template_name is not None:
            template_name = Variable(self.template_name).resolve(context)
        if template_name:
            args.append(template_name)
        args = tuple(args)
        return do_render_node(*args)

def do_render_tree(root, template_name, context = None):
    list = Category.objects.filter(root = root)
    map = {}
    roots = construct_tree(list, map)
    attrs = {'id' : 'category'}
    return render_to_string(template_name, {'roots' : roots, 'attrs_str': build_attrs_string(attrs), 'attrs' : attrs}, context)

class RenderTreeNode(template.Node):
    def __init__(self, provider, root = None, template_name = None, *args, **kwargs):
        super(RenderTreeNode, self).__init__(*args, **kwargs)
        self.provider, self.root, self.template_name = provider, root, template_name

    def render(self, context):
        provider = Variable(self.provider).resolve(context)
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
        cache.add_object(provider, '{0}'.format(root.pk))
        return do_render_tree(root, template_name, context)

def do_render_node_tag(parser, token):
    """
    {% render_node node value template_name %}
    """
    bits = token.split_contents()
    if len(bits) < 2 or len(bits) > 4:
        raise template.TemplateSyntaxError("'%s' takes 2-4 arguments" % bits[0])
    args = tuple(bits[1:])
    return RenderNodeNode(*args)

def do_get_category_url(category, provider):
    """
    {{ category|get_category_url:"ask.settings" }}
    """
    root = category.root
    assert root
    try:
        provider = cache.get_object('{0}'.format(root.pk))
        return provider.get_url(category)
    except KeyError:
        if settings.DEBUG:
            raise VariableDoesNotExist("there is no provider for %s in cache", (root.pk,))
        return ''

def do_render_tree_tag(parser, token):
    """
    {% render_category_tree "provider name" "root name" %}
    """
    bits = token.split_contents()
    if len(bits) < 2:
        raise template.TemplateSyntaxError("'%s' takes 2-n arguments" % bits[0])
    args = tuple(bits[1:])
    return RenderTreeNode(*args)


register.filter('get_category_url', do_get_category_url)
register.filter('render_node', do_render_node)
register.tag('render_node', do_render_node_tag)
register.tag('render_category_tree', do_render_tree_tag)

