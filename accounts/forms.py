from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password

class SignUpForm(forms.Form):
    email = forms.EmailField(max_length=254, label="Email")
    password = forms.CharField(widget=forms.PasswordInput(), label="Password")
    password_confirm = forms.CharField(widget=forms.PasswordInput(), label="Confirm password")

    def clean_email(self):
        email = self.cleaned_data["email"]

        if User.objects.filter(username=email).exists():
            raise forms.ValidationError(
                "An account with this email already exists."
            )

        return email

    def clean(self):
        cleaned_data = super().clean()

        email = cleaned_data.get("email")
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")

        if (password and password_confirm and password != password_confirm):
            self.add_error(
                "password_confirm",
                "Passwords do not match."
            )

        if password and email:
            try:
                validate_password(
                    password,
                    user=User(username=email, email=email)
                )
            except forms.ValidationError as error:
                self.add_error("password", error)
        
        return cleaned_data
    
class LoginForm(forms.Form):
    email = forms.EmailField(max_length=254, label="Email")
    password = forms.CharField(widget=forms.PasswordInput(), label="Password")

    def __init__(self, *args, request=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = request
        self.user = None

    def clean(self):
        cleaned_data = super().clean()

        email = cleaned_data.get("email")
        password = cleaned_data.get("password")

        if email and password:
            self.user = authenticate(self.request, username=email, password=password,)

            if self.user is None:
                raise forms.ValidationError("Invalid email or password.")
        
        return cleaned_data
    
class ForgotPasswordForm(forms.Form):
    email = forms.EmailField(max_length=254, label="Email")

class ResetPasswordForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput(), label="Password")
    password_confirm = forms.CharField(widget=forms.PasswordInput(), label="Confirm password")

    def clean(self):
        cleaned_data = super().clean()

        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")

        if (password and password_confirm and password != password_confirm):
            self.add_error(
                "password_confirm",
                "Passwords do not match."
            )
        
        return cleaned_data
