from rest_framework.decorators import api_view
from rest_framework.response import Response

from price_match.utils import scrape_website

@api_view(["POST"])
def scrape(request):
    url = request.data.get("url", "")
    postal_code = request.data.get("postal_code", "")
    email = request.data.get("email", "")
    
    message = scrape_website(url, postal_code, email)
    return Response(message)
