from django import test as unittest
from category.models import Category

class TestModels(unittest.TestCase):
    fixtures = ['category_data.json']

    def setUp(self):
        self.blogs = Category.objects.get(slug = 'blogs')
        self.pingpong = Category.objects.get(slug = 'pingpong')

    def testNewCategory(self):
        """ Verify category creating is ok """
        category = Category(name = 'test')
        category.save()
        self.assertNotEquals(category.root, None)
        self.assertEquals(category.root.pk, category.pk)

    def testData(self):
        self.assertEquals(self.blogs.root.pk, self.blogs.pk)
        self.assertEquals(self.pingpong.root.pk, self.pingpong.pk)
        self.assertEquals(self.pingpong.is_root, True)
        self.assertEquals(self.blogs.is_root, True)

    def testNewCategoryWithParent(self):
        """ Verify create with parent and change parent is ok """
        category = Category(name = 'level1', parent = self.blogs)
        self.assertNumQueries(1, category.save())
        self.assertEquals(category.parent.pk, self.blogs.pk)
        print category

        category2 = Category(name = 'level2', parent = category)
        self.assertNumQueries(1, category2.save())

        self.assertEquals(category2.parent.pk, category.pk)
        self.assertEquals(category2.root.pk, self.blogs.pk)

        category3 = Category(name = 'level1.2', parent = self.blogs)
        self.assertNumQueries(1, category3.save())

        category.parent = self.pingpong
        self.assertNumQueries(3, category.save())


        category2 = Category.objects.get(pk = category2.pk)
        category3 = Category.objects.get(pk = category3.pk)
        self.assertEquals(category2.root.pk, self.pingpong.pk)
        self.assertEquals(category2.parent.pk, category.pk)
        self.assertEquals(category3.root.pk, self.blogs.pk)
        self.assertEquals(category3.parent.pk, self.blogs.pk)

    def testGetOrCreate(self):
        category, created = Category.objects.get_or_create(name = 'someblogs')
        self.assertEquals(category.root.pk, category.pk)


