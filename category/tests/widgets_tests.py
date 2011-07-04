from django import test as unittest
from category.models import Category
from category.widgets import CategorySelectWidget
from category import getLogger

log = getLogger(__file__)

class TestWidgets(unittest.TestCase):
    fixtures = ['category_data.json']

    def tearUp(self):
        self.blogs = Category.objects.get(slug = 'blogs')
        self.pingpong = Category.objects.get(slug = 'pingpong')

    def testData(self):
        self.assertEquals(Category.objects.count(), 6)
        self.assertEquals(Category.objects.filter(root = self.blogs).count(), 4)

    def testInit(self):
        widget = CategorySelectWidget(choices = Category.objects.filter(root = self.blogs))
        self.assertEquals(widget.built, True)
        self.assertNotEquals(widget.root, None)
        self.assertEquals(widget.root.node.pk, self.blogs.pk)
        self.assertEquals(widget.root.children.count(), 1)
        self.assertEquals(widget.root.children[0].children.count(), 2)


    def testRender(self):
        widget = CategorySelectWidget(choices = \
        Category.objects.filter(root = self.blogs), attrs = {'id' : 'navigator'})
        result = widget.render()
        log.debug(result)
