from price_match.models import StatusMessages
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
