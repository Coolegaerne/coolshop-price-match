from base64 import b64encode

from django.contrib import admin
from django.utils.safestring import mark_safe
from price_match.models import Config, PriceMatch


class PriceMatchAdmin(admin.ModelAdmin):
    readonly_fields = ["creation_datetime", "total_price", "display_product_image"]
    list_display = ["name", "url", "creation_datetime"]

    def display_product_image(self, obj):
        if obj.product_image:
            return mark_safe(
                '<img src = "data: image/png; base64, {}" width="750" height="3000">'.format(
                    b64encode(obj.product_image).decode("utf8")
                )
            )
        else:
            return "Not Found"

    display_product_image.allow_tags = True
    display_product_image.short_description = "Product Image"


class ConfigAdmin(admin.ModelAdmin):
    list_display = ["base_url"]


admin.site.register(PriceMatch, PriceMatchAdmin)
admin.site.register(Config, ConfigAdmin)
