from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(["POST"])
def scrape_website(request, url):
    return Response({'url': url})
