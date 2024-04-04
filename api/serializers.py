from api_gemini.models import Account, Transaction
from rest_framework import serializers

class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = "__all__"

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = "__all__"

    def to_representation(self, instance):
        rep = super(TransactionSerializer, self).to_representation(instance)
        rep['account'] = instance.account.name
        return rep