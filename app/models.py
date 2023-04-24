# Create your models here.
from django.db import models
from django.core.exceptions import ValidationError

class User(models.Model):
    name = models.CharField(max_length=50, null=False, blank=False)
    lastname = models.CharField(max_length=50, null=False, blank=False)
    email = models.EmailField()
    phone = models.CharField(max_length=50, null=False, blank=False)
    address = models.CharField(max_length=50, null=False, blank=False)

    def __str__(self):
        return f'Full Name: {self.name} {self.lastname} - Email: {self.email}'
    
    def getPhone(self):
        return self.phone
    
    def getAddress(self):
        return self.address
    

class Transaction(models.Model):
    TRANSACTION_TYPE_CHOICES = (
        ('income', 'Income'),
        ('expense', 'Expense'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.CharField(max_length=255)
    date = models.DateField()
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPE_CHOICES)

    def __str__(self):
        return f'{self.transaction_type.capitalize()} - {self.description}'

    def clean(self):
        if self.transaction_type == 'income' and self.amount < 0:
            raise ValidationError("The amount of an income must be positive")
        elif self.transaction_type == 'expense' and self.amount > 0:
            raise ValidationError("The amount of an expense must be negative")


class Income(Transaction):
    class Meta:
        proxy = True

    def clean(self):
        if self.amount < 0:
            raise ValidationError("The amount of an income must be positive")


class Expense(Transaction):
    class Meta:
        proxy = True

    def clean(self):
        if self.amount > 0:
            raise ValidationError("The amount of an expense must be negative")
