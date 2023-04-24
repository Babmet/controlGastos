# Create your models here.
from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('El email es obligatorio')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

class User(AbstractBaseUser):
    name = models.CharField(max_length=50, null=False, blank=False)
    lastname = models.CharField(max_length=50, null=False, blank=False)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=50, null=False, blank=False)
    address = models.CharField(max_length=50, null=False, blank=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'lastname', 'phone', 'address']

    objects = CustomUserManager()

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
