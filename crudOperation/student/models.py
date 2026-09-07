from django.db import models
from django.core.validators import RegexValidator
import uuid

class Student(models.Model):
    id = models.BigAutoField(primary_key=True)
    uuid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False, db_index=True)
    student_name = models.CharField(max_length=256)
    student_email = models.EmailField(max_length=256, unique=True)
    student_address = models.TextField(max_length=1000)
    student_phone = models.CharField(
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
        db_table = 'students'
        ordering = ['-created_at']

    def __str__(self):
        return self.student_name
