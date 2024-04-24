from django.contrib import admin
from price_match.models import Product, Config

class ProductAdmin(admin.ModelAdmin):
    readonly_fields = ["creation_datetime", "total_price"]
    list_display = ["name", "url", "creation_datetime"]


class ConfigAdmin(admin.ModelAdmin):
    list_display = ["base_url"]


admin.site.register(Product, ProductAdmin)
admin.site.register(Config, ConfigAdmin)
