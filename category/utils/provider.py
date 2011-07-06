from category.utils.catroot import get_root
from django.db.models import permalink
from django.db.models.loading import get_model

Category = get_model('category', 'category')

class Provider(object):

    multi_type_provider = False

    def __init__(self, root_name):
        self.root_name = root_name
        self.root = None

    def get_root_category(self):
        if self.root is None:
            self.root = get_root(name = self.root_name)
        return self.root

    def get_categories(self, root):
        return Category.objects.filter(root = root)

    def get_root_name(self):
        return self.root_name

    def get_count_for(self, category):
        raise NotImplementedError

    @permalink
    def get_url(self, category):
        raise NotImplementedError
