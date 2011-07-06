
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


def construct_tree(list, map):
    root = []
    for category in list:
        current = map.get(category.pk, None)
        if current is None:
            current = Node(category)
            map[category.pk] = current
        else:
            current.node = category
        if category.parent_id == None:
            root.append(current)
        else:
            parent = map.get(category.parent_id, None)
            if parent is None:
                parent = Node()
                map[category.parent_id] = parent
            parent.append(current)
    return root
