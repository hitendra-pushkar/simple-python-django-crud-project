from django.db import models
from django.core.validators import RegexValidator
import uuid

class Employee(models.Model):

    id = models.BigAutoField(primary_key=True)
    uuid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False, db_index=True)
    emp_name = models.CharField(max_length=254)
    emp_email = models.EmailField(max_length=254, unique=True)
    emp_address = models.TextField(max_length=500)
    emp_phone = models.CharField(
        max_length=15, 
        validators=[
            RegexValidator(
                regex=r'^\+?[0-9]{10,15}$',
                message='Enter a valid phone number.'
            )
        ]
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'employees'
        ordering = ['-created_at']

    def __str__(self):
        return self.emp_name