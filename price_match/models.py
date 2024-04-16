from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=512, null=True, blank=True)
    url = models.CharField(max_length=512, null=True, blank=True)
    price = models.FloatField(default=0)
    ean = models.CharField(max_length=512, null=True, blank=True)
    color = models.CharField(max_length=512, null=True, blank=True)
    shipping_cost = models.FloatField(default=0)
    total_price = models.FloatField(null=True, blank=True)
    accepted = models.BooleanField(default=False)
    creation_datetime = models.DateTimeField(auto_now_add=True)
    acceptance_datetime = models.DateTimeField(null=True, blank=True)
    product_image = models.ImageField(null=True, blank=True)

    def save(self, *args, **kwargs):
        self.total_price = self.price + self.shipping_cost
        super(Product, self).save(*args, **kwargs)
