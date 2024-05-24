from django.contrib import admin
from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from price_match.views import PriceMatchList, scrape

urlpatterns = [
    path("admin/", admin.site.urls),
    path("scrape/", scrape),
    path("pricematches/", csrf_exempt(PriceMatchList.as_view())),
]
