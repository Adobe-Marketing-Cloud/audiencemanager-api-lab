from __future__ import unicode_literals
from django.db import models
from . import aam
from . import utils


# check API access
aam.get_self()


class Category(models.Model):
    name = models.CharField(max_length=255, blank=False)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

    def get_products(self):
        return Product.objects.filter(category=self.id)

    def save(self, *args, **kwargs):
        if not self.id:
            # object is being created
            super(Category, self).save(*args, **kwargs)
            #aam.create_category_trait_folder(self)
            #aam.create_category_segment(self)
        else:
            # object is being updated
            old_category = Category.objects.get(id=self.id)
            super(Category, self).save(*args, **kwargs)
            #aam.update_category_trait_folder(old_category, self)
            #aam.update_category_segment(old_category, self)


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, blank=False)
    description = models.TextField(blank=True)
    sku = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to=utils.image_path_wrapper('images/'), default='images/no-image.jpg')

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.id:
            # object is being created
            super(Product, self).save(*args, **kwargs)
            #aam.create_product_trait(self)
            #aam.update_category_segment(self.category, self.category)
        else:
            # object is being updated
            old_product = Product.objects.get(id=self.id)
            super(Product, self).save(*args, **kwargs)
            #aam.update_product_trait(old_product, self)
