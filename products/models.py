from django.db import models

"""
Product category model
"""


class Category(models.Model):
    class Meta:
        verbose_name_plural = "Categories"

    name = models.CharField(max_length=254)
    friendly_name = models.CharField(max_length=254, null=True, blank=True)

    def __str__(self):
        return self.name

    def get_friendly_name(self):
        return self.friendly_name


"""
Model for each individual product item
"""


class Product(models.Model):
    category = models.ForeignKey(
        "Category", null=True, blank=True, on_delete=models.SET_NULL
    )
    sku = models.CharField(max_length=254, null=True, blank=True)
    name = models.CharField(max_length=254)
    desc = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    image_url = models.URLField(max_length=1024, null=True, blank=True)
    image = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.name


"""
Model for adding comments to products
"""


class ProductComment(models.Model):
    product = models.ForeignKey(Product, models.CASCADE,
                                related_name='comments')
    author = models.CharField(max_length=200)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '%s - %s' % (self.product.name, self.author)
