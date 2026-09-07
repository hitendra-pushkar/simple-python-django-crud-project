from django import forms
from django.core.exceptions import ValidationError
import re

from .models import Student

class StudentForm(forms.ModelForm):

    class Meta:
        model = Student

        fields = [
            'student_name',
            'student_email',
            'student_address',
            'student_phone',
        ]

        widgets = {
            'student_name': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'student_name',
                'maxlength': '256',
                'autocomplete': 'name'
            }),
            'student_email': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'student_email',
                'maxlength': '256',
                'autocomplete': 'email'
            }),
            'student_address': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'student_address',
                'maxlength': '500',
                'rows': '3'
            }),
            'student_phone': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'student_phone',
                'maxlength': '15',
                'autocomplete': 'phone'
            })
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['student_name'].required = False
        self.fields['student_email'].required = False
        self.fields['student_address'].required = False
        self.fields['student_phone'].required = False

    # -----------------------------------------
    # Student Name
    # -----------------------------------------

    def clean_student_name(self):

        name = self.cleaned_data.get('student_name')

        if not name:
            raise ValidationError(
                'Student name is required.'
            )

        name = ' '.join(name.split())

        if len(name) < 2:
            raise ValidationError(
                'Name must contain at least 2 characters.'
            )

        if len(name) > 100:
            raise ValidationError(
                'Name cannot exceed 100 characters.'
            )

        if not re.match(
            r"^[A-Za-zÀ-ÿ][A-Za-zÀ-ÿ .'-]*$",
            name
        ):
            raise ValidationError(
                'Name contains invalid characters.'
            )

        return name

    # -----------------------------------------
    # Email
    # -----------------------------------------

    def clean_student_email(self):

        email = self.cleaned_data.get('student_email')

        if not email:
            raise ValidationError(
                'Email address is required.'
            )

        email = email.strip().lower()

        if len(email) > 254:
            raise ValidationError(
                'Email address cannot exceed 254 characters.'
            )

        queryset = Student.objects.filter(
            student_email__iexact=email
        )

        # Exclude current student during UPDATE
        if self.instance.pk:
            queryset = queryset.exclude(
                pk=self.instance.pk
            )

        if queryset.exists():
            raise ValidationError(
                'An student with this email already exists.'
            )

        return email

    # -----------------------------------------
    # Address
    # -----------------------------------------

    def clean_student_address(self):

        address = self.cleaned_data.get('student_address')

        if not address:
            raise ValidationError(
                'Address is required.'
            )

        address = ' '.join(address.split())

        if len(address) < 10:
            raise ValidationError(
                'Address must contain at least 10 characters.'
            )

        if len(address) > 500:
            raise ValidationError(
                'Address cannot exceed 500 characters.'
            )

        return address

    # -----------------------------------------
    # Phone
    # -----------------------------------------

    def clean_student_phone(self):

        phone = self.cleaned_data.get('student_phone')

        if not phone:
            raise ValidationError(
                'Phone number is required.'
            )

        # Remove spaces, -, (, )
        phone = re.sub(
            r'[\s\-()]',
            '',
            phone
        )

        if not re.match(
            r'^\+?[0-9]{10,15}$',
            phone
        ):
            raise ValidationError(
                'Enter a valid phone number with 10 to 15 digits.'
            )

        queryset = Student.objects.filter(
            student_phone=phone
        )

        # Exclude current student during UPDATE
        if self.instance.pk:
            queryset = queryset.exclude(
                pk=self.instance.pk
            )

        if queryset.exists():
            raise ValidationError(
                'An Student with this phone number already exists.'
            )

        return phone

    