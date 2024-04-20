from django.db import models
from django.db.models import Aggregate
from api_gemini.choices import typeChoices,envelopedIdChoices
# Create your models here.

class Account(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
    
    @property
    def total_transactions(self):
        qs = self.transactions.all().aggregate(total=models.Sum('amount'))
        return qs['total']


class Transaction(models.Model):

    date = models.DateField()
    amount=models.IntegerField()
    type = models.CharField(max_length=255, choices=typeChoices)
    envelope_id = models.IntegerField(choices=envelopedIdChoices)
    account = models.ForeignKey('Account',related_name='transactions', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.id) + self.account.name + str(self.amount) + self.type