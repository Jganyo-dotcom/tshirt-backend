from django.db import models

class Order(models.Model):
    name = models.CharField(max_length=100)
    number = models.PositiveIntegerField()
    email = models.EmailField()
    to_email = models.EmailField()
    design_upload = models.ImageField(upload_to='designs/', blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    screenshot = models.ImageField(upload_to='screenshots/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order by {self.name}"
