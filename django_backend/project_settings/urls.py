from django.contrib import admin
from django.urls import path
from price_match.views import scrape

urlpatterns = [
    path("admin/", admin.site.urls),
    path("scrape/", scrape),
]
