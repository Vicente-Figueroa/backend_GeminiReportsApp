from api_gemini.models import Account
from rest_framework import serializers

class AccountSerializer(serializers.Serializer):
    class Meta:
        model = Account
        fields = '__all__'