from category import getLogger

log = getLogger(__file__)

def change_subtree_root(node, newroot):
    """
    Recursively change all subtree node's root attribute
    """
    log.debug(u'change subtree root: pk={0.pk} name={0.name} newroot={1.name}'.format(node, newroot))
    for child in node.children.all():
        child.root = newroot
        child.save(setroot = True)
        change_subtree_root(child, newroot)

