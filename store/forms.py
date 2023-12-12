from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from crispy_forms.helper import FormHelper

class SignUpForm(UserCreationForm):
    """
    A custom form for user registration that extends Django's UserCreationForm.

    This form adds additional fields for first name, last name, and email to the default
    user creation form provided by Django. It uses Django's built-in User model.
    """

    # Defining additional fields to be included in the form:
    # First name field, with a maximum length of 100 characters and marked as required.
    first_name = forms.CharField(max_length=100, required=True)

    # Last name field, with a maximum length of 100 characters and marked as required.
    last_name = forms.CharField(max_length=100, required=True)

    # Email field, with a maximum length of 250 characters.
    # The help_text provides additional guidance to the user.
    email = forms.EmailField(max_length=250, help_text='eg. youremail@gmail.com')

    class Meta:
        """
        Meta class to provide additional information about the form.
        """

        # Specifying that this form is linked to the Django's built-in User model.
        model = User

        # Defining the fields that should be included in the form.
        # This includes the fields defined above plus the default 'username',
        # 'password1', and 'password2' fields from UserCreationForm.
        fields = ('first_name', 'last_name', 'username', 'password1', 'password2', 'email')

        # Note: 'password1' and 'password2' are for the password and password confirmation fields.
