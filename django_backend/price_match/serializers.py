from price_match.models import PriceMatch
from rest_framework import serializers


class PriceMatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = PriceMatch
        fields = "__all__"
