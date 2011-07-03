from django import template
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe
from django.template.base import resolve_variable, Variable

register = template.Library()

def do_render_node(node, value = None, template_name = 'category/render-node.html'):
    subtree = None
    if node.children.count():
        subtree = "\n".join([do_render_node(child, value) for child in node.children])
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

def do_render_node_tag(parser, token):
    bits = token.split_contents()
    if len(bits) < 2 or len(bits) > 4:
        raise template.TemplateSyntaxError("'%s' takes 2-4 arguments" % bits[0])
    args = tuple(bits[1:])
    return RenderNodeNode(*args)

register.filter('render_node', do_render_node)
register.tag('render_node', do_render_node_tag)
