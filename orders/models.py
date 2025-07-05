from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

class Order(models.Model):
    name = models.CharField(max_length=100)
    number = models.PositiveIntegerField()
    phone = PhoneNumberField(blank=False, null=False)
    email = models.EmailField()
    to_email = models.EmailField()
    size = models.CharField(max_length=9)
    notes = models.TextField(blank=True, null=True)
    screenshot = models.ImageField(upload_to='screenshots/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order by {self.name}"
    
class Order_specific(models.Model):
    name = models.CharField(max_length=100)
    number = models.PositiveIntegerField()
    phone = PhoneNumberField(blank=False, null=False)
    email = models.EmailField()
    to_email = models.EmailField()
    size = models.CharField(max_length=9)
    notes = models.TextField(blank=True, null=True)
    design =models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order by {self.name}"
