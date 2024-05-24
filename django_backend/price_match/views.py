import base64
import json

from django.http import HttpResponse, JsonResponse
from django.views import View
from price_match.models import PriceMatch, StatusMessages
from price_match.utils import scrape_website
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


class PriceMatchList(View):
    def get(self, request):
        price_matches = PriceMatch.objects.all()
        data = []
        for match in price_matches:
            match_data = {
                "pk": match.pk,
                "name": match.name,
                "url": match.url,
                "price": match.price,
                "ean": match.ean,
                "shipping_price": match.shipping_price,
                "stock_status": match.stock_status,
                "total_price": match.total_price,
                "accepted": match.accepted,
                "creation_datetime": match.creation_datetime,
                "acceptance_datetime": match.acceptance_datetime,
                "postal_code": match.postal_code,
                "email": match.email,
                "product_image": base64.b64encode(match.product_image).decode("utf-8")
                if match.product_image
                else None,
            }
            data.append(match_data)
        return JsonResponse(data, safe=False)

    def put(self, request):
        try:
            data_str = request.body.decode()
            new_pricematch_data = json.loads(data_str)
            primary_key = new_pricematch_data.get("pk")

            if primary_key:
                old_pricematch_data = PriceMatch.objects.filter(pk=primary_key).first()
                if old_pricematch_data:
                    for key, value in new_pricematch_data.items():
                        if key == "pk" or key == "product_image":
                            continue
                        setattr(old_pricematch_data, key, value)

                    old_pricematch_data.save()
                    return HttpResponse("PriceMatch Updated Successfully", status=200)
                else:
                    return HttpResponse("PriceMatch Not Found", status=404)

            else:
                return HttpResponse("Primary Key Not Found", status=400)

        except Exception as e:
            return HttpResponse("Error Updating PriceMatch", status=500)
