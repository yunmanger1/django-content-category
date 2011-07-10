from django.contrib import admin
from django.db.models.loading import get_model
from django import forms
from category.fields import CategoryField

Category = get_model('category', 'category')

class CategoryAdminForm(forms.ModelForm):
    def __init__(self, *a, **kw):
        super(CategoryAdminForm, self).__init__(*a, **kw)
        self.fields['parent'].root = None

    parent = CategoryField(display_root = True, collapse = False, required = False)

    class Meta:
        model = Category
        exclude = ('root',)

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name', 'slug')
    form = CategoryAdminForm

admin.site.register(Category, CategoryAdmin)
