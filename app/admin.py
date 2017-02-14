from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from django.utils.html import format_html
from django.db import models
from django import forms
from .models import Product, Category


admin.site.site_title = 'Shop Administration'
admin.site.site_header = 'Shop Administration'
admin.site.index_title = 'Shop Administration'


class ImageFieldWidget(forms.FileInput):
    def __init__(self, attrs={}):
        super(ImageFieldWidget, self).__init__(attrs)

    def render(self, name, value, attrs=None):
        output = []
        if value and hasattr(value, "url"):
            output.append(('<a target="_blank" href="%s">'
                           '<img src="%s" style="height: 100px;" /></a><br><br> '
                           % (value.url, value.url)))
        output.append(super(ImageFieldWidget, self).render(name, value, attrs))
        return format_html(u''.join(output))


class ProductAdmin(admin.ModelAdmin):
    def image_tag(self, obj):
        return format_html('<img src="{}" height="100"/>'.format(obj.image.url))
    image_tag.short_description = 'Image'
    list_display = ['name','description','sku','price','image_tag']
    formfield_overrides = {
        models.ImageField: {'widget': ImageFieldWidget},
    }


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name','description']
    readonly_fields = ['products']

    def products(self, obj):
        output = []
        output.append('<table class="table table-striped table-bordered">')
        products = obj.get_products()
        if products:
            for product in products:
                url = '/admin/app/product/%s' % product.id
                output.append(('<tr><td><a href="%s">%s</a></td></tr>'
                               % (url, product.name)))
        else:
            output.append('<tr><td>None</td></tr>')
        output.append('</table>')
        return format_html(u''.join(output))


# register our app models
admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)

# un-register user and group models for less noise
admin.site.unregister(User)
admin.site.unregister(Group)
