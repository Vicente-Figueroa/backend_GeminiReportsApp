from django.db import models
from django.db.models import Aggregate

# Create your models here.

class Account(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
    
    @property
    def total(self):
        return self.Transaction.aggregate(total = Aggregate.Sum('amount'))['total']
    
class Transaction(models.Model):
    typeChoices = [
        ('Gasto','Gasto'),
        ('Ingreso','Ingreso')
    ]

    amount=models.IntegerField()
    type = models.CharField(max_length=255, choices=typeChoices)
    account = models.ForeignKey('Account', on_delete=models.CASCADE)
