from django.contrib import admin
from django.db.models.loading import get_model
from django import forms
from category.fields import CategoryField

Category = get_model('category', 'category')

class CategoryAdminForm(forms.ModelForm):
    parent = CategoryField(display_root = True, collapse = False, required = False)

    class Meta:
        model = Category
        exclude = ('root',)

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    form = CategoryAdminForm

admin.site.register(Category, CategoryAdmin)
