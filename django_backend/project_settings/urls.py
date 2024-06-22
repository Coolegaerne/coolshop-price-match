from django.contrib import admin
from django.urls import path
from price_match.views import (PriceMatchListCreate,
                                PriceMatchRetrieveUpdateDestroy, scrape)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("scrape/", scrape),
    path(
        "pricematches/", PriceMatchListCreate.as_view(), name="pricematch-list-create"
    ),
    path(
        "pricematches/<int:pk>/",
        PriceMatchRetrieveUpdateDestroy.as_view(),
        name="pricematch-detail",
    ),
]
