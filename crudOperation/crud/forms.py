import re

from django import forms
from django.core.exceptions import ValidationError

from .models import Employee


class EmployeeForm(forms.ModelForm):

    class Meta:
        model = Employee

        fields = [
            'emp_name',
            'emp_email',
            'emp_address',
            'emp_phone',
        ]

        widgets = {
            'emp_name': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'emp_name',
                'maxlength': '100',
                'autocomplete': 'name',
            }),

            'emp_email': forms.EmailInput(attrs={
                'class': 'form-control',
                'id': 'emp_email',
                'maxlength': '254',
                'autocomplete': 'email',
            }),

            'emp_address': forms.Textarea(attrs={
                'class': 'form-control',
                'id': 'emp_address',
                'maxlength': '500',
                'rows': '3',
            }),

            'emp_phone': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'emp_phone',
                'maxlength': '15',
                'autocomplete': 'tel',
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['emp_name'].required = False
        self.fields['emp_email'].required = False
        self.fields['emp_address'].required = False
        self.fields['emp_phone'].required = False

    # -----------------------------------------
    # Employee Name
    # -----------------------------------------

    def clean_emp_name(self):

        name = self.cleaned_data.get('emp_name')

        if not name:
            raise ValidationError(
                'Employee name is required.'
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

    def clean_emp_email(self):

        email = self.cleaned_data.get('emp_email')

        if not email:
            raise ValidationError(
                'Email address is required.'
            )

        email = email.strip().lower()

        if len(email) > 254:
            raise ValidationError(
                'Email address cannot exceed 254 characters.'
            )

        queryset = Employee.objects.filter(
            emp_email__iexact=email
        )

        # Exclude current employee during UPDATE
        if self.instance.pk:
            queryset = queryset.exclude(
                pk=self.instance.pk
            )

        if queryset.exists():
            raise ValidationError(
                'An employee with this email already exists.'
            )

        return email

    # -----------------------------------------
    # Address
    # -----------------------------------------

    def clean_emp_address(self):

        address = self.cleaned_data.get('emp_address')

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

    def clean_emp_phone(self):

        phone = self.cleaned_data.get('emp_phone')

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

        queryset = Employee.objects.filter(
            emp_phone=phone
        )

        # Exclude current employee during UPDATE
        if self.instance.pk:
            queryset = queryset.exclude(
                pk=self.instance.pk
            )

        if queryset.exists():
            raise ValidationError(
                'An employee with this phone number already exists.'
            )

        return phone