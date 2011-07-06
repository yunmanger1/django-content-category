from category.utils.catroot import get_root
from django.db.models import permalink

class Provider(object):

    multi_type_provider = False

    def __init__(self, root_name):
        self.root_name = root_name
        self.root = None

    def get_root_category(self):
        if self.root is None:
            self.root = get_root(name = self.root_name)
        return self.root

    def get_root_name(self):
        return self.root_name

    @permalink
    def get_url(self, category):
        raise NotImplementedError
