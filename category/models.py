from django.db import models
from django.template.defaultfilters import slugify
from utils.model import change_subtree_root

class Category(models.Model):
    name = models.CharField(max_length = 255)
    slug = models.SlugField()
    parent = models.ForeignKey('self', null = True, blank = True, related_name = 'children')
    sort_order = models.IntegerField(default = 0)
    root = models.ForeignKey('self', null = True, blank = True, related_name = 'subtree')
    is_root = models.BooleanField(default = False, editable = False)

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'
        unique_together = ('parent', 'slug',)
        ordering = ('sort_order', 'slug',)

    def save(self, setroot = False, force_insert = False, force_update = False, *a, **kw):
        """
        All children have the same root 
        """
        inserted = False
        if self.parent is None:
            self.is_root = True
        else:
            self.is_root = False
            if not setroot:
                if self.pk and self.parent and self.root \
                and self.root.pk != self.parent.root.pk:
                    change_subtree_root(self, self.parent.root)
                try:
                    self.root = self.parent.root
                except Category.DoesNotExist:
                    self.root = None

        if not self.slug:
            self.slug = slugify(self.name)

        if self.is_root and self.root is None:
            if not self.pk:
                inserted = True
                super(Category, self).save(force_insert = force_insert, *a, **kw)
            self.root = self

        if inserted:
            super(Category, self).save(force_update = True, *a, **kw)
        else:
            super(Category, self).save(force_insert = force_insert, force_update = force_update, *a, **kw)


    def __unicode__(self):
        return self.name
