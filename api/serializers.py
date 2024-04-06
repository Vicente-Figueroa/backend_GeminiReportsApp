from api_gemini.models import Account, Transaction
from rest_framework import serializers
from api_gemini.choices import envelopedIdChoices

class AccountSerializer(serializers.ModelSerializer):
    total_transactions  = serializers.SerializerMethodField()

    def get_total_transactions(self, model):
        return model.total_transactions
    class Meta:
        model = Account
        fields = ['name', 'total_transactions']

class TransactionSerializer(serializers.ModelSerializer):
    
    envelope_id = serializers.CharField(source='get_envelope_id_display')
    class Meta:
        model = Transaction
        fields = "__all__"

    def to_representation(self, instance):
        rep = super(TransactionSerializer, self).to_representation(instance)
        rep['account'] = instance.account.name
        return rep