from django.db import models
from django.db.models import Aggregate

# Create your models here.

class Account(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Transaction(models.Model):
    typeChoices = [
        ('Gasto','Gasto'),
        ('Ingreso','Ingreso')
    ]

    amount=models.IntegerField()
    type = models.CharField(max_length=255, choices=typeChoices)
    account = models.ForeignKey('Account', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.id) + self.account.name + str(self.amount) + self.type