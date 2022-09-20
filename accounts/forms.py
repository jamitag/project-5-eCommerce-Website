from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Profile


"""
Registration form for new users to sign up
"""


class RegisterForm(UserCreationForm):
    first_name = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(
            attrs={"placeholder": "First Name", "class": "form-control"}
        ),
    )
    last_name = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(
            attrs={"placeholder": "Last Name", "class": "form-control"}
        ),
    )
    username = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(
            attrs={"placeholder": "Username", "class": "form-control"}
        ),
    )
    email = forms.EmailField(
        required=True,
        widget=forms.TextInput(
            attrs={"placeholder": "Email", "class": "form-control"}
        ),
    )
    password1 = forms.CharField(
        max_length=50,
        required=True,
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Password",
                "class": "form-control",
                "data-toggle": "password",
                "id": "password",
            }
        ),
    )
    password2 = forms.CharField(
        max_length=50,
        required=True,
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Confirm Password",
                "class": "form-control",
                "data-toggle": "password",
                "id": "password",
            }
        ),
    )

    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "username",
            "email",
            "password1",
            "password2",
        ]


"""
Authentication form for login
"""


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(
            attrs={"placeholder": "Username", "class": "form-control"}
        ),
    )
    password = forms.CharField(
        max_length=50,
        required=True,
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Password",
                "class": "form-control",
                "data-toggle": "password",
                "id": "password",
                "name": "password",
            }
        ),
    )
    remember_me = forms.BooleanField(required=False)

    class Meta:
        model = User
        fields = ["username", "password", "remember_me"]


"""
Updating the users details within profile
"""


class UpdateUserForm(forms.ModelForm):
    username = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    email = forms.EmailField(
        required=True, widget=forms.TextInput(attrs={"class": "form-control"})
    )

    class Meta:
        model = User
        fields = ["username", "email"]


"""
For additional details within profile to be updated
"""


class UpdateProfileForm(forms.ModelForm):
    avatar = forms.ImageField(
        widget=forms.FileInput(attrs={"class": "form-control-file"})
    )
    full_name = forms.CharField(
        max_length=255,
        required=False,
        widget=forms.TextInput(
            attrs={"placeholder": "Full Name", "class": "form-control"}
        ),
    )
    bio = forms.CharField(
        widget=forms.Textarea(
            attrs={"class": "form-control", "placeholder": "Bio", "rows": 5}
        )
    )
    address_1 = forms.CharField(
        max_length=300,
        widget=forms.Textarea(
            attrs={"class": "form-control", "placeholder": "Address",
                   "rows": 1}
        ),
    )
    city = forms.CharField(
        max_length=255,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "City"}
        ),
    )
    country = forms.CharField(
        max_length=255,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Country"}
        ),
    )
    post_code = forms.CharField(
        max_length=255,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Post Code"}
        ),
    )

    class Meta:
        model = Profile
        fields = [
            "avatar",
            "full_name",
            "bio",
            "address_1",
            "city",
            "country",
            "post_code",
        ]
