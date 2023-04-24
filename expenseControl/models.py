from django.db import models
from django.core.exceptions import ValidationError

class User(models.Model):
    name = models.CharField(max_length=50, null=False, blank=False)
    lastname = models.CharField(max_length=50, null=False, blank=False)
    email = models.EmailField()
    phone = models.PhoneNumberField()
    address = models.CharField(max_length=50, null=False, blank=False)

    def __str__(self):
        return f'Full Name: {self.name} {self.lastname} - Email: {self.email}'
    
    def getPhone(self):
        return self.phone
    
    def getAddress(self):
        return self.address
    
