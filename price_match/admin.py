from django.contrib import admin
from price_match.models import Product

class ProductAdmin(admin.ModelAdmin):
    readonly_fields = ["creation_datetime", "total_price"]
    list_display = ["name", "url", "creation_datetime"]

admin.site.register(Product, ProductAdmin)
