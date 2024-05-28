from rest_framework import serializers
from price_match.models import PriceMatch

class PriceMatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = PriceMatch
        fields = '__all__'
