from django.contrib import admin
from django.urls import path

from price_match.views import scrape_website

urlpatterns = [
    path('admin/', admin.site.urls),
    path('scrape/<str:url>/', scrape_website),
]
