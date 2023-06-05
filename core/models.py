from django.db import models

# Create your models here.

class Email(models.Model):
    email = models.CharField(max_length=255)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email
