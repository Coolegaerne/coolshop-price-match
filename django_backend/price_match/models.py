from django.db import models


class PriceMatch(models.Model):
    name = models.CharField(max_length=512, null=True, blank=True, default="Not Found")
    url = models.CharField(max_length=512, null=True, blank=True, default="Not Found")
    price = models.CharField(max_length=512, null=True, blank=True, default="Not Found")
    ean = models.CharField(max_length=512, null=True, blank=True, default="Not Found")
    color = models.CharField(max_length=512, null=True, blank=True, default="Not Found")
    shipping_price = models.CharField(max_length=512, null=True, blank=True, default="Not Found")
    stock_status = models.CharField(max_length=512, null=True, blank=True, default="Not Found")
    total_price = models.FloatField(null=True, blank=True)
    accepted = models.BooleanField(default=False)
    creation_datetime = models.DateTimeField(auto_now_add=True)
    acceptance_datetime = models.DateTimeField(null=True, blank=True)
    product_image = models.BinaryField(null=True, blank=True)
    postal_code = models.CharField(max_length=512, null=True, blank=True)
    email = models.EmailField(max_length=512, null=True, blank=True)


    def save(self, *args, **kwargs):
        try:
            self.total_price = float(self.price) + float(self.shipping_price)
        except:
            self.total_price = None
        super(PriceMatch, self).save(*args, **kwargs)


    def __str__(self):
        return (
            f"Name: {self.name}\n"
            f"URL: {self.url}\n"
            f"Price: {self.price}\n"
            f"EAN: {self.ean}\n"
            f"Color: {self.color}\n"
            f"Shipping Cost: {self.shipping_price}\n"
            f"In Stock: {self.stock_status}\n"
            f"Total Price: {self.total_price}\n"
            f"Accepted: {self.accepted}\n"
            f"Creation Datetime: {self.creation_datetime}\n"
            f"Acceptance Datetime: {self.acceptance_datetime}\n"
            f"Postal Code: {self.postal_code}\n"
            f"Email: {self.email}\n"
            f"Product Image: {type(self.product_image)}\n"
        )


class Config(models.Model):
    base_url = models.CharField(max_length=512, blank=False, null=False, primary_key=True)
    slowest_element_selector = models.CharField(max_length=512, blank=True)
    cookie_selector = models.CharField(max_length=512, blank=True)
    specification_selector = models.CharField(max_length=512, blank=True)
    price_selector = models.CharField(max_length=512, blank=True)
    name_selector = models.CharField(max_length=512, blank=True)
    ean_selector = models.CharField(max_length=512, blank=True)
    color_selector = models.CharField(max_length=512, blank=True)
    stock_status_selector = models.CharField(max_length=512, blank=True)
    shipping_price_selector = models.CharField(max_length=512, blank=True)
    currency = models.CharField(max_length=512, blank=True)
