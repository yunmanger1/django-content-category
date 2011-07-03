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

    def save(self, setroot = False, *a, **kw):
        """
        All children have the same root 
        """
        if self.parent is None:
#            if setroot and self.root and self.root.pk == self.pk:
#                raise AttributeError('Parent is null while root is set')
            self.is_root = True
        else:
            self.is_root = False
            if not setroot:
                if self.pk and self.parent and self.root \
                and self.root.pk != self.parent.root.pk:
                    change_subtree_root(self, self.parent.root)
                self.root = self.parent.root

        if not self.slug:
            self.slug = slugify(self.name)

        if self.is_root and self.root is None:
            if not self.pk:
                super(Category, self).save(*a, **kw)
            self.root = self

        super(Category, self).save(*a, **kw)


    def __unicode__(self):
        return self.name
