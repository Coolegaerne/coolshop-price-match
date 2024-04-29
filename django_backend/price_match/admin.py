from base64 import b64encode
from django.contrib import admin
from price_match.models import Product, Config
from django.utils.html import format_html
from django.utils.safestring import mark_safe
class ProductAdmin(admin.ModelAdmin):
    readonly_fields = ["creation_datetime", "total_price", "display_product_image"]
    list_display = ["name", "url", "creation_datetime"]

    def display_product_image(self, obj):
        if obj.product_image:
            return mark_safe('<img src = "data: image/png; base64, {}" width="750" height="3000">'.format(b64encode(obj.product_image).decode('utf8')))
        else:
            return "No Image"
    display_product_image.allow_tags = True
    display_product_image.short_description = "Product Image"


class ConfigAdmin(admin.ModelAdmin):
    list_display = ["base_url"]


admin.site.register(Product, ProductAdmin)
admin.site.register(Config, ConfigAdmin)
