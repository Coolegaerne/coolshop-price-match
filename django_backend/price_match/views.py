import base64
import json

from django.http import HttpResponse, JsonResponse
from django.views import View
from price_match.models import PriceMatch, StatusMessages
from price_match.serializers import PriceMatchSerializer
from price_match.utils import scrape_website
from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(["POST"])
def scrape(request):
    url = request.data.get("url", "")
    postal_code = request.data.get("postal_code", "")
    email = request.data.get("email", "")
    try:
        message = scrape_website(url, postal_code, email)
    except:
        message = StatusMessages.ERROR
    return Response(message)


class PriceMatchListCreate(generics.ListCreateAPIView):
    queryset = PriceMatch.objects.all()
    serializer_class = PriceMatchSerializer


class PriceMatchRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = PriceMatch.objects.all()
    serializer_class = PriceMatchSerializer
