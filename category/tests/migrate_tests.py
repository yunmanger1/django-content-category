from django import test as unittest
from django.db.models import get_model
from category.utils.catroot import get_root
from ask.batchtest import dive, ask_root

Category = get_model('category', 'category')
BlogCategory = get_model('blog', 'category')
DEPTH_LIMIT = 10

def dive_new(category, depth = 0):
    if depth >= DEPTH_LIMIT:
        print 'LIMIT: ', DEPTH_LIMIT
        return
    if category is not None:
        dive_new(category.parent, depth + 1)
        print category, '->',



class TestMigration(unittest.TestCase):
    fixtures = ['blog_category.json']

    def testGetOrCreate(self):
        for bc in BlogCategory.objects.all():
            if bc.children.count() == 0:
                category = dive(bc, dry = False)
                print category
                self.assertEquals(category.root.pk, ask_root.pk)
                self.assertEquals(category.name, bc.title)
                if bc.parent:
                    self.assertEquals(category.parent.name, bc.parent.title)
#        print '=' * 80
#        dive_new(category)
#        print


