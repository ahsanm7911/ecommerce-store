from rest_framework import serializers
from .models import IGPost
from accounts.models import Newsletter
from core.models import ConfirmedOrder

class IGPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = IGPost
        fields = '__all__'

class ConfirmedOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConfirmedOrder
        fields = ('shippingAddress', 'order_details')

class NewsletterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Newsletter
        fields = '__all__'