from django import test as unittest
from category.models import Category
from category import getLogger
from category.utils.form import get_category_form

log = getLogger(__file__)

class TestForm(unittest.TestCase):
    fixtures = ['category_data.json']

    blogs = Category.objects.get(slug = 'blogs')
    pingpong = Category.objects.get(slug = 'pingpong')

    def testBlogsForm(self):
        form = get_category_form(slug = 'blogs')
        print form.as_p()

