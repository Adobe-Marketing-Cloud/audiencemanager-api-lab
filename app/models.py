from __future__ import unicode_literals
from django.db import models
from . import utils


class Category(models.Model):
    name = models.CharField(max_length=255, blank=False)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

    def get_products(self):
        return Product.objects.filter(category=self.id)

    def save(self, *args, **kwargs):
        if not self.id:
            # Category is being created
            super(Category, self).save(*args, **kwargs)
        else:
            # Category is being updated
            old_category = Category.objects.get(id=self.id)
            super(Category, self).save(*args, **kwargs)


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
            # Product is being created
            super(Product, self).save(*args, **kwargs)
        else:
            # Product is being updated
            old_product = Product.objects.get(id=self.id)
            super(Product, self).save(*args, **kwargs)
